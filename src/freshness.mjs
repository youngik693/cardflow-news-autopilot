import {createHash} from 'node:crypto';
const sha=value=>createHash('sha256').update(value).digest('hex');
const stamp=now=>new Date(now).toISOString();
export const FRESHNESS_TTL_MS=5*60*1000;
const validHash=s=>typeof s==='string'&&/^[a-f0-9]{64}$/.test(s);
function permitted(input,origins){try{const u=new URL(input);return u.protocol==='https:'&&!u.username&&!u.password&&origins.includes(u.origin)?u:null}catch{return null}}
function decode(s){return s.replace(/&amp;/gi,'&').replace(/&quot;/gi,'"').replace(/&#39;|&apos;/gi,"'").replace(/&nbsp;/gi,' ').replace(/&#(\d+);/g,(_,n)=>+n<=0x10ffff?String.fromCodePoint(+n):' ')}
function textOnly(html){return decode(html.replace(/<!--[\s\S]*?-->/g,' ').replace(/<(script|style|noscript)\b[^>]*>[\s\S]*?<\/\1\s*>/gi,' ').replace(/<[^>]+>/g,' ')).replace(/\s+/g,' ').trim()}
async function bounded(response,max=1500000){const reader=response.body?.getReader();if(!reader)throw Error('SOURCE_EMPTY');let size=0;const chunks=[];try{while(true){const {value,done}=await reader.read();if(done)break;size+=value.length;if(size>max)throw Error('SOURCE_TOO_LARGE');chunks.push(value)}}finally{await reader.cancel().catch(()=>{})}return Buffer.concat(chunks).toString('utf8')}
/** Reads only explicitly approved public endpoints. Stores hashes/links, never article bodies. */
export async function fetchSourceSnapshot(source,{allowedOrigins,fetchImpl=fetch,now=()=>Date.now()}={}){
 const url=permitted(source.url,allowedOrigins||[]);if(!url)throw Error('SOURCE_NOT_APPROVED');
 const response=await fetchImpl(url.href,{cache:'no-store',redirect:'error',headers:{'Cache-Control':'no-cache','Pragma':'no-cache','Accept':'text/html,application/xml,application/json,text/plain','User-Agent':'CardflowSourceCheck/1.0'},signal:AbortSignal.timeout(12000)});
 if(!response.ok||response.status===304)throw Error('SOURCE_HTTP_'+response.status);
 if(Number(response.headers.get('age'))>300)throw Error('SOURCE_UPSTREAM_CACHE_STALE');
 if(response.url&&!permitted(response.url,allowedOrigins))throw Error('SOURCE_REDIRECT_UNAPPROVED');
 const type=response.headers.get('content-type')||'';if(!/text\/|json|xml|html/i.test(type))throw Error('SOURCE_TYPE_UNSUPPORTED');
 const full=await bounded(response,Math.min(source.maxBytes||1500000,8000000));if(/<title[^>]*>\s*(?:access denied|just a moment|attention required|sign in|login)|verify you are human/i.test(full))throw Error('SOURCE_ACCESS_WALL');
 const html=source.scope==='metadata'?full.split(/<\/head\s*>/i)[0]:full;
 let content=textOnly(html);const metadata=[...html.matchAll(/<meta\b[^>]*(?:property|name)\s*=\s*["'](?:og:title|og:description|article:published_time|article:modified_time|dateModified)["'][^>]*>/gi)].map(m=>m[0]);
 // Public description changes must be noticed even though meta tags are not visible text.
 content+=' '+metadata.join(' ');
 if(content.trim().length<24)throw Error('SOURCE_NOT_EXTRACTABLE');
 const links=[];if(source.role==='discovery'){
  if(!source.linkPattern)throw Error('DISCOVERY_PATTERN_REQUIRED');const pattern=new RegExp(source.linkPattern,'i');
  for(const m of full.matchAll(/<(?:a|link)\b[^>]*href\s*=\s*["']([^"']+)["']/gi)){
   try{const u=permitted(new URL(decode(m[1]),url).href,allowedOrigins);if(u&&pattern.test(u.href)){u.hash='';links.push(u.href)}}catch{}
  }
  // Customs publishes verified board identifiers on JavaScript anchor attributes.
  // Construct its observed public detail route; never execute page JavaScript.
  if(source.extractor==='customs-board'&&url.hostname==='customs.go.kr'){
   for(const match of full.matchAll(/<a\b[^>]*>/gi)){
    const tag=match[0],id=tag.match(/data-id=["'](\d+)["']/i)?.[1],token=tag.match(/data-url=["']([a-f0-9]+)["']/i)?.[1];
    if(!id||!token)continue;const detail=new URL('/kcs/na/ntt/selectNttInfo.do',url);detail.search=new URLSearchParams({bbsId:url.searchParams.get('bbsId')||'1362',mi:url.searchParams.get('mi')||'2891',nttSn:id,nttSnUrl:token});if(pattern.test(detail.href))links.push(detail.href);
   }
  }
  if(!links.length)throw Error('DISCOVERY_LINKS_UNAVAILABLE');
 }
 const modifiedAt=html.match(/(?:article:modified_time|dateModified)["']?\s*(?:content\s*=|:)\s*["']([^"']+)/i)?.[1]||null;
 return {sourceId:source.id,url:url.href,scope:source.scope||'public_text',role:source.role||'evidence',sha256:sha(content+'\n'+[...new Set(links)].sort().join('\n')),links:[...new Set(links)].sort(),modifiedAt:modifiedAt&&Number.isFinite(Date.parse(modifiedAt))?new Date(modifiedAt).toISOString():null,lastModified:response.headers.get('last-modified'),fetchedAt:stamp(now()),status:'checked',coverage:source.scope==='metadata'?'public_head_metadata_only':'registered_public_endpoint_only'};
}
export function invalidateStory(state,storyKey,{reason,at,sourceId}){
 state.regenerationQueue??=[];let task=state.regenerationQueue.find(x=>x.storyKey===storyKey&&x.status==='needs_research');
 if(!task){task={storyKey,status:'needs_research',createdAt:at,reasons:[],sourceIds:[]};state.regenerationQueue.push(task)}
 task.updatedAt=at;task.reasons=[...new Set([...task.reasons,reason])];task.sourceIds=[...new Set([...task.sourceIds,sourceId])];
 for(const group of ['drafts','reviewedDrafts','ownedDrafts','scheduledDrafts'])for(const draft of state[group]||[]){
  if(![draft.storyKey,draft.id,draft.watchStoryKey].includes(storyKey))continue;
  if(draft.status==='published'){draft.correctionReviewRequired=true;continue}
  if(draft.status==='needs_reconcile'){draft.sourceReviewRequired=true;continue}
  const wasScheduled=draft.status==='scheduled'||Boolean(draft.externalScheduledId);
  draft.status='invalidated';draft.invalidation={reason,at,sourceId};draft.publicationAuthorized=false;draft.verification=null;draft.sourceManifest=null;
  if(wasScheduled)draft.externalCancellationRequired=true;
 }
 state.regenerationQueue=state.regenerationQueue.slice(-300);
}
/** Existing stories stay watched even when their original publication date was yesterday. */
export async function refreshWatchedSources(state,watchlist,{fetchImpl=fetch,now=()=>Date.now()}={}){
 state.sourceSnapshots??={};const sources=watchlist.stories.flatMap(story=>story.sources.map(s=>({...s,storyKey:story.storyKey})));
 const summary={checked:0,changed:0,failed:0,initial:0,at:stamp(now())};
 // Bound concurrency so a growing history cannot flood a provider.
 for(let offset=0;offset<sources.length;offset+=4){const batch=sources.slice(offset,offset+4);const results=await Promise.allSettled(batch.map(source=>fetchSourceSnapshot(source,{allowedOrigins:watchlist.allowedOrigins,fetchImpl,now})));
  for(let i=0;i<batch.length;i++){
   const source=batch[i],result=results[i],old=state.sourceSnapshots[source.id];
   if(result.status==='rejected'){
    summary.failed++;state.sourceSnapshots[source.id]={...old,sourceId:source.id,url:source.url,status:'unverified',lastAttemptAt:stamp(now()),error:/^[A-Z0-9_]+$/.test(result.reason?.message)?result.reason.message:'SOURCE_FETCH_FAILED'};
    invalidateStory(state,source.storyKey,{reason:'SOURCE_UNVERIFIED',at:stamp(now()),sourceId:source.id});continue;
   }
   const next=result.value;summary.checked++;const changed=old?.sha256&&old.sha256!==next.sha256;
   next.lastChangedAt=changed?stamp(now()):old?.lastChangedAt||null;state.sourceSnapshots[source.id]=next;
   if(!old?.sha256){summary.initial++;invalidateStory(state,source.storyKey,{reason:'INITIAL_SOURCE_REVIEW_REQUIRED',at:stamp(now()),sourceId:source.id})}
   else if(changed){summary.changed++;invalidateStory(state,source.storyKey,{reason:source.role==='discovery'?'FOLLOWUP_INDEX_CHANGED':'SOURCE_CONTENT_CHANGED',at:stamp(now()),sourceId:source.id})}
  }
 }
 state.sourceWatchLastRun=summary;return summary;
}
export function rememberRecentArticles(state,candidates,{now=Date.now(),days=30,max=60}={}){
 const entries=new Map((state.watchedArticles||[]).map(x=>[x.url,x]));
 for(const row of candidates){let u;try{u=new URL(row.url)}catch{continue}if(u.origin!=='https://v.daum.net'||!/^\/v\/\d{17}$/.test(u.pathname))continue;
  const previous=entries.get(row.url);entries.set(row.url,{url:row.url,storyKey:row.storyKey,firstSeenAt:previous?.firstSeenAt||stamp(now),lastSeenAt:stamp(now)});
 }
 // Preserve watched source URLs from existing drafts/posts ahead of transient headlines.
 for(const group of ['drafts','reviewedDrafts','ownedDrafts','scheduledDrafts'])for(const draft of state[group]||[]){
  const firstAt=draft.at||draft.publication?.publishedAt;for(const raw of [draft.sourceURL,...(draft.sourceURLs||[])]){
   let u;try{u=new URL(raw)}catch{continue}if(u.origin!=='https://v.daum.net'||!/^\/v\/\d{17}$/.test(u.pathname))continue;
   const old=entries.get(u.href);if(!old&&firstAt&&now-Date.parse(firstAt)>=days*86400000)continue;
   entries.set(u.href,{url:u.href,storyKey:draft.watchStoryKey||draft.storyKey||draft.id,firstSeenAt:old?.firstSeenAt||firstAt||stamp(now),lastSeenAt:old?.lastSeenAt||firstAt||stamp(now),priority:true});
  }
 }
 state.watchedArticles=[...entries.values()].filter(x=>now-Date.parse(x.lastSeenAt)<days*86400000).sort((a,b)=>Number(Boolean(b.priority))-Number(Boolean(a.priority))||Date.parse(b.lastSeenAt)-Date.parse(a.lastSeenAt)).slice(0,max);
}
export function withArticleHistory(watchlist,state){return {...watchlist,stories:[...watchlist.stories,...(state.watchedArticles||[]).map(x=>({storyKey:x.storyKey,sources:[{id:'article-'+sha(x.url).slice(0,20),url:x.url,scope:'metadata',role:'evidence'}]}))]}}
/** Immediate prepublication network recheck against the exact source versions used to render. */
export async function checkPublicationFreshness({candidate,assets,watchlist,fetchImpl=fetch,now=()=>Date.now()}){
 const key=candidate.watchStoryKey||candidate.storyKey||candidate.url,story=watchlist.stories.find(x=>x.storyKey===key),blocks=[];
 if(!story?.sources?.length)return {allowed:false,blocks:['STORY_SOURCE_REGISTRY_MISSING']};
 if(!story.sources.some(s=>s.role==='discovery'))blocks.push('FOLLOWUP_DISCOVERY_REQUIRED');
 const manifest=assets.sourceManifest;if(!Array.isArray(manifest)||!manifest.length)return {allowed:false,blocks:['RENDER_SOURCE_MANIFEST_REQUIRED']};
 const snapshots=[];
 for(const source of story.sources){const used=manifest.find(x=>x.sourceId===source.id);
  if(!used||!validHash(used.sha256)){blocks.push('RENDER_SOURCE_VERSION_MISSING');continue}
  const reviewed=Date.parse(used.reviewedAt);if(!Number.isFinite(reviewed)||reviewed>now()||now()-reviewed>FRESHNESS_TTL_MS)blocks.push('RENDER_SOURCE_REVIEW_STALE');
  try{const current=await fetchSourceSnapshot(source,{allowedOrigins:watchlist.allowedOrigins,fetchImpl,now});snapshots.push(current);if(current.sha256!==used.sha256)blocks.push('SOURCE_CHANGED_AFTER_RENDER')}catch{blocks.push('LIVE_SOURCE_RECHECK_FAILED')}
 }
 return {allowed:blocks.length===0,blocks:[...new Set(blocks)],snapshots};
}
