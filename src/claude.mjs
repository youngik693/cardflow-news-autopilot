import {validatePricing} from './api-budget.mjs';
export class ClaudeClient {
 constructor({key,fetchImpl=fetch,now=()=>Date.now()}) {if(!key)throw Error('ANTHROPIC_API_KEY_REQUIRED');Object.assign(this,{key,fetchImpl,now});}
 async api(path,body) {
  const r=await this.fetchImpl('https://api.anthropic.com/v1/'+path,{method:body?'POST':'GET',headers:{'x-api-key':this.key,'anthropic-version':'2023-06-01','content-type':'application/json'},...(body?{body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(120000)});
  if(!r.ok)throw Error('CLAUDE_HTTP_'+r.status);return r.json();
 }
 async model(id) {if(!/^[a-zA-Z0-9._-]+$/.test(id||''))throw Error('CLAUDE_MODEL_REQUIRED');const m=await this.api('models/'+id);if(m.id!==id||m.lifecycle==='retired'||!Number.isInteger(m.max_input_tokens)||m.max_input_tokens<=0||!Number.isInteger(m.max_tokens)||m.max_tokens<=0)throw Error('CLAUDE_MODEL_UNAVAILABLE');return m;}
 async complete({model,pricing,budget,stage,system,prompt,maxTokens=2000,maxSearches=0,searchType}) {
  validatePricing(pricing,this.now());const info=await this.model(model);
  if(!Number.isInteger(maxTokens)||maxTokens<1||maxTokens>info.max_tokens||!Number.isInteger(maxSearches)||maxSearches<0||maxSearches>3)throw Error('CLAUDE_LIMIT_INVALID');
  const body={model,max_tokens:maxTokens,system,messages:[{role:'user',content:prompt}]};
  if(maxSearches){if(!info.capabilities?.server_tools?.web_search?.supported||!/^web_search_\d{8}$/.test(searchType||''))throw Error('WEB_SEARCH_CAPABILITY_REQUIRED');body.tools=[{type:searchType,name:'web_search',max_uses:maxSearches,allowed_callers:['direct']}];}
  const count=await this.api('messages/count_tokens',body),input=count.input_tokens;
  if(!Number.isInteger(input)||input<=0||input>info.max_input_tokens)throw Error('INPUT_COST_UNKNOWN');
  // Server results are re-billed at each search iteration. Reserve the full model
  // context for every potential iteration; never mistake max_uses for a token cap.
  const inputBound=maxSearches?info.max_input_tokens*(maxSearches+1):input;
  const bound=inputBound*pricing.inputPerMTok/1e6+maxTokens*pricing.outputPerMTok/1e6+maxSearches*pricing.searchPerRequest;
  const entry=await budget.reserve({model,stage,maximumUSD:bound,pricing});
  let response;
  try{response=await this.api('messages',body)}catch{await budget.unknown(entry);throw Error('CLAUDE_REQUEST_UNRECONCILED');}
  const actualUSD=await budget.settle(entry,response.usage);
  if(response.stop_reason!=='end_turn'||response.content?.some(x=>/error/.test(x.type)||x.type==='web_search_tool_result'&&!Array.isArray(x.content)))throw Error('CLAUDE_RESULT_INCOMPLETE');
  const text=(response.content||[]).filter(x=>x.type==='text').map(x=>x.text).join('\n');
  let data;try{data=JSON.parse(text.replace(/^```json\s*|\s*```$/g,''))}catch{throw Error('CLAUDE_JSON_REQUIRED');}
  return {data,actualUSD,model,usage:entry.usage};
 }
}
