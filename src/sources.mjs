import {createHash} from 'node:crypto';
import {createDaumNewsService} from '../lib/daum-news.mjs';
import {normalizeItems} from '../lib/naver-news.mjs';
export function storyKey(title){return createHash('sha256').update(String(title).toLowerCase().replace(/\[[^\]]*\]/g,'').replace(/[\s\p{P}\p{S}]/gu,'')).digest('hex').slice(0,24)}
export async function collectNews(config,secrets){const candidates=[],sources=[];try{const service=createDaumNewsService();const result=await service.main();candidates.push(...result.items.map((r,i)=>({...r,provider:'daum',portalRank:i+1,storyKey:storyKey(r.title)})));sources.push({provider:'daum',status:'ok',count:result.items.length});}catch{sources.push({provider:'daum',status:'fetch_failed',count:0})}
if(secrets.naver_client_id&&secrets.naver_client_secret){try{const rows=await fetchNaverNews(config,secrets);candidates.push(...rows);sources.push({provider:'naver',status:'ok',count:rows.length})}catch(e){sources.push({provider:'naver',status:'fetch_failed',count:0,...naverFailure(e)})}}else sources.push({provider:'naver',status:'credentials_required',count:0});return {candidates,sources}}
export async function enrichCandidate(row){if(row.provider!=='daum'||row.description)return row;const service=createDaumNewsService();try{const result=await service.enrich([row.url]);return {...row,...result.items[0]}}catch{return row}}

export function naverFailure(error){return {errorCode:/^NAVER_HTTP_[0-9]{3}$/.test(error?.message)?error.message:['NAVER_KEY_FORMAT_INVALID','NAVER_RESPONSE_INVALID','NAVER_API_MODE_INVALID'].includes(error?.message)?error.message:'NAVER_NETWORK_ERROR',...(/^(?:[0-9]{3}|SE[0-9]{2})$/.test(error?.apiCode)?{apiCode:error.apiCode}:{})};}
export async function fetchNaverNews(config,secrets,{fetchImpl=fetch}={}){
 const id=String(secrets.naver_client_id||'').trim(),secret=String(secrets.naver_client_secret||'').trim();
 if(!/^[\x21-\x7e]{1,200}$/.test(id)||!/^[\x21-\x7e]{1,200}$/.test(secret))throw Error('NAVER_KEY_FORMAT_INVALID');
 const mode=secrets.naver_api_mode||config.naverApiMode||'hub';if(!['hub','legacy'].includes(mode))throw Error('NAVER_API_MODE_INVALID');
 const rows=[];
 for(const query of config.queries.slice(0,3)){
  const url=new URL(mode==='hub'?'https://naverapihub.apigw.ntruss.com/search/v1/news':'https://openapi.naver.com/v1/search/news.json');url.search=new URLSearchParams({query,display:'20',start:'1',sort:'date',...(mode==='hub'?{format:'json'}:{})});
  const response=await fetchImpl(url,{headers:mode==='hub'?{'X-NCP-APIGW-API-KEY-ID':id,'X-NCP-APIGW-API-KEY':secret}:{'X-Naver-Client-Id':id,'X-Naver-Client-Secret':secret},signal:AbortSignal.timeout(12000),redirect:'error'});
  if(!response.ok){const error=Error('NAVER_HTTP_'+response.status);try{const body=await response.json();const code=body.errorCode||body.error?.errorCode;if(/^(?:[0-9]{3}|SE[0-9]{2})$/.test(code))error.apiCode=code}catch{}throw error}
  const data=await response.json();if(!Array.isArray(data.items))throw Error('NAVER_RESPONSE_INVALID');
  rows.push(...normalizeItems(data.items,24).map(r=>({...r,provider:'naver',portalRank:null,storyKey:storyKey(r.title)})));
 }
 return rows;
}
