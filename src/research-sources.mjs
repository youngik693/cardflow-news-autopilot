import {digest} from './research.mjs';
// Configured primary endpoints only. Reject redirects, access walls and huge responses.
export async function fetchResearchSources(registry,{fetchImpl=fetch,now=()=>Date.now()}={}) {
 const sources=[];
 for(const s of registry){
  const u=new URL(s.url);
  if(u.protocol!=='https:'||u.username||u.password||!s.allowedOrigins?.includes(u.origin)||!s.primary||!s.rightsVerified||!s.aiProcessingAllowed)throw Error('SOURCE_NOT_APPROVED');
  if(/^(localhost|127\.|10\.|192\.168\.|169\.254\.|\[|0\.)/.test(u.hostname))throw Error('SOURCE_NOT_APPROVED');
  const r=await fetchImpl(u,{redirect:'error',cache:'no-store',signal:AbortSignal.timeout(15000)});
  if(!r.ok||Number(r.headers.get('age'))>300||!/text\/|json|xml/i.test(r.headers.get('content-type')||''))throw Error('RESEARCH_SOURCE_UNAVAILABLE');
  const reader=r.body.getReader(),chunks=[];let bytes=0;
  try{while(true){const {done,value}=await reader.read();if(done)break;bytes+=value.length;if(bytes>250000)throw Error('RESEARCH_SOURCE_TOO_LARGE');chunks.push(value)}}finally{await reader.cancel().catch(()=>{})}
  const raw=Buffer.concat(chunks).toString('utf8');
  if(/verify you are human|<title[^>]*>\s*(access denied|just a moment|sign in)/i.test(raw))throw Error('RESEARCH_SOURCE_ACCESS_WALL');
  const text=raw.replace(/<(script|style|noscript)\b[^>]*>[\s\S]*?<\/\1\s*>/gi,' ').replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
  if(text.length<30||text.length>30000)throw Error('RESEARCH_SOURCE_TEXT_BOUND');
  sources.push({...s,text,sha256:digest(text),fetchedAt:new Date(now()).toISOString()});
 }
 return sources;
}
