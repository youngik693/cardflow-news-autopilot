import {randomUUID} from 'node:crypto';
const money=x=>Math.ceil(x*1e8)/1e8;
export const kstDay=now=>new Date(now+9*3600000).toISOString().slice(0,10);
const valid=x=>Number.isFinite(x)&&x>=0;
export class ApiBudget {
 constructor({store,state,now=()=>Date.now(),test=true}) {Object.assign(this,{store,state,now,test});state.apiCosts??=[];}
 async reserve({model,stage,maximumUSD,pricing}) {
  if(!this.store.insideLease)throw Error('BUDGET_LEASE_REQUIRED');
  if(!valid(maximumUSD)||maximumUSD===0)throw Error('COST_BOUND_REQUIRED');
  const rows=this.state.apiCosts;
  if(rows.some(x=>['reserved','unknown','overrun'].includes(x.status)))throw Error('COST_RECONCILIATION_REQUIRED');
  const day=kstDay(this.now()),charge=x=>x.actualUSD??x.reservedUSD;
  if(rows.filter(x=>x.day===day).reduce((n,x)=>n+charge(x),0)+maximumUSD>5+1e-9)throw Error('DAILY_API_BUDGET_EXCEEDED');
  if(this.test&&rows.filter(x=>x.test).reduce((n,x)=>n+charge(x),0)+maximumUSD>1+1e-9)throw Error('TEST_API_BUDGET_EXCEEDED');
  const entry={id:randomUUID(),day,test:this.test,model,stage,status:'reserved',reservedUSD:money(maximumUSD),pricing,at:new Date(this.now()).toISOString()};rows.push(entry);await this.store.save(this.state);return entry;
 }
 async settle(entry,usage) {
  const p=entry.pricing,required=['input_tokens','output_tokens'];
  if(!usage||required.some(k=>!valid(usage[k]))||Object.keys(usage).some(k=>!['input_tokens','output_tokens','cache_read_input_tokens','cache_creation_input_tokens','server_tool_use','cache_creation'].includes(k))||usage.cache_creation_input_tokens||usage.cache_read_input_tokens||Object.keys(usage.server_tool_use||{}).some(k=>k!=='web_search_requests')||!valid(usage.server_tool_use?.web_search_requests??0)) {
   await this.unknown(entry);throw Error('USAGE_COST_UNKNOWN');
  }
  entry.usage={inputTokens:usage.input_tokens,outputTokens:usage.output_tokens,searchRequests:usage.server_tool_use?.web_search_requests??0};
  entry.actualUSD=money(usage.input_tokens*p.inputPerMTok/1e6+usage.output_tokens*p.outputPerMTok/1e6+entry.usage.searchRequests*p.searchPerRequest);
  entry.status=entry.actualUSD<=entry.reservedUSD+1e-8?'settled':'overrun';await this.store.save(this.state);
  if(entry.status==='overrun')throw Error('API_COST_BOUND_BREACHED');return entry.actualUSD;
 }
 async unknown(entry){entry.status='unknown';await this.store.save(this.state);}
}
export function validatePricing(p,now=Date.now()) {
 if(!p||!['inputPerMTok','outputPerMTok','searchPerRequest'].every(k=>valid(p[k]))||p.inputPerMTok===0||p.outputPerMTok===0||!/^https:\/\/(platform\.claude\.com|claude\.com)\//.test(p.source||'')||!Number.isFinite(Date.parse(p.checkedAt))||Date.parse(p.checkedAt)>now||now-Date.parse(p.checkedAt)>7*86400000)throw Error('CURRENT_MODEL_PRICING_REQUIRED');return p;
}
