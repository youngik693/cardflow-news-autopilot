import {createHash} from 'node:crypto';
import {createDaumNewsService} from '../lib/daum-news.mjs';
import {normalizeItems} from '../lib/naver-news.mjs';
export function storyKey(title){return createHash('sha256').update(String(title).toLowerCase().replace(/\[[^\]]*\]/g,'').replace(/[\s\p{P}\p{S}]/gu,'')).digest('hex').slice(0,24)}
export async function collectNews(config,secrets){const candidates=[],sources=[];try{const service=createDaumNewsService();const result=await service.main();candidates.push(...result.items.map((r,i)=>({...r,provider:'daum',portalRank:i+1,storyKey:storyKey(r.title)})));sources.push({provider:'daum',status:'ok',count:result.items.length});}catch{sources.push({provider:'daum',status:'fetch_failed',count:0})}
if(secrets.naver_client_id&&secrets.naver_client_secret){try{const rows=await fetchNaverNews(config,secrets);candidates.push(...rows);sources.push({provider:'naver',status:'ok',count:rows.length})}catch(e){sources.push({provider:'naver',status:'fetch_failed',count:0,...naverFailure(e)})}}else sources.push({provider:'naver',status:'credentials_required',count:0});return {candidates,sources}}
export async function enrichCandidate(row){if(row.provider!=='daum'||row.description)return row;const service=createDaumNewsService();try{const result=await service.enrich([row.url]);return {...row,...result.items[0]}}catch{return row}}

export function naverFailure(error){return {errorCode:/^NAVER_HTTP_[0-9]{3}$/.test(error?.message)?error.message:['NAVER_KEY_FORMAT_INVALID','NAVER_RESPONSE_INVALID'].includes(error?.message)?error.message:'NAVER_NETWORK_ERROR',...(/^[0-9]{3}$/.test(error?.apiCode)?{apiCode:error.apiCode}:{})};}
export async function fetchNaverNews(config,secrets,{fetchImpl=fetch}={}){
 const id=String(secrets.naver_client_id||'').trim(),secret=String(secrets.naver_client_secret||'').trim();
 if(!/^[\x21-\x7e]{1,200}$/.test(id)||!/^[\x21-\x7e]{1,200}$/.test(secret))throw Error('NAVER_KEY_FORMAT_INVALID');
 const rows=[];
 for(const query of config.queries.slice(0,3)){
  const url=new URL('https://openapi.naver.com/v1/search/news.json');url.search=new URLSearchParams({query,display:'20',sort:'date'});
  const response=await fetchImpl(url,{headers:{'X-Naver-Client-Id':id,'X-Naver-Client-Secret':secret},signal:AbortSignal.timeout(12000),redirect:'error'});
  if(!response.ok){const error=Error('NAVER_HTTP_'+response.status);try{const body=await response.json();if(/^[0-9]{3}$/.test(body.errorCode))error.apiCode=body.errorCode}catch{}throw error}
  const data=await response.json();if(!Array.isArray(data.items))throw Error('NAVER_RESPONSE_INVALID');
  rows.push(...normalizeItems(data.items,24).map(r=>({...r,provider:'naver',portalRank:null,storyKey:storyKey(r.title)})));
 }
 return rows;
}
