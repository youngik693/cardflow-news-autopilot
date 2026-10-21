import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {execFile} from 'node:child_process';import {promisify} from 'node:util';
import {ClaudeClient} from './claude.mjs';import {ApiBudget} from './api-budget.mjs';import {researchDraft,digest} from './research.mjs';
// Explicit local execution: never schedules, publishes, uploads or touches public state.
const config=JSON.parse(await readFile(new URL('../config.json',import.meta.url),'utf8'));
if(config.claudeApiEnabled!==true)throw Error('CLAUDE_API_DISABLED');
const exec=promisify(execFile);const dir=process.env.PRIVATE_RESEARCH_DIR;
if(!dir||!dir.startsWith('/'))throw Error('PRIVATE_RESEARCH_DIRECTORY_REQUIRED');
await mkdir(dir,{recursive:true,mode:0o700});
const {open,unlink}=await import('node:fs/promises');let lock;
try{lock=await open(dir+'/research.lock','wx',0o600)}catch{throw Error('PRIVATE_RESEARCH_LOCKED')}
let state;try{state=JSON.parse(await readFile(dir+'/cost-ledger.json','utf8'))}catch(e){if(e.code!=='ENOENT')throw e;state={apiCosts:[]}}
const store={insideLease:true,async save(s){await writeFile(dir+'/cost-ledger.json',JSON.stringify(s,null,2),{mode:0o600})}};
try{
 const input=JSON.parse(await readFile(process.env.RESEARCH_INPUT_FILE,'utf8'));
 if(input.sources.some(s=>!s.primary||!s.rightsVerified||!s.aiProcessingAllowed))throw Error('PRIMARY_SOURCE_RIGHTS_REQUIRED');
 const {fetchResearchSources}=await import('./research-sources.mjs');
 const sources=await fetchResearchSources(input.sources);
 const models={research:process.env.CLAUDE_RESEARCH_MODEL,review:process.env.CLAUDE_REVIEW_MODEL};
 const prices=JSON.parse(await readFile(new URL('../config-api-prices.json',import.meta.url),'utf8'));
 const constitution=await readFile(new URL('../docs/editorial-constitution.md',import.meta.url),'utf8');
 const client=new ClaudeClient({key:process.env.ANTHROPIC_API_KEY});
 const result=await researchDraft({client,budget:new ApiBudget({store,state,test:true}),models,prices,candidate:input.candidate,sources,constitution,maxSearches:Number(process.env.CLAUDE_MAX_SEARCHES||0),searchType:process.env.CLAUDE_SEARCH_TOOL});
 const model={draft:result.draft,sourceLabel:input.sources.map(s=>s.label).join(' · ')+' / 확인 '+new Date().toISOString()};
 await writeFile(dir+'/result.json',JSON.stringify(result,null,2),{mode:0o600});
 if(result.checks.allowed){await writeFile(dir+'/render-input.json',JSON.stringify(model),{mode:0o600});await exec('python',['render-researched.py',dir+'/render-input.json',dir+'/cards']);}
 console.log(JSON.stringify({status:result.status,publicationAuthorized:false,actualUSD:state.apiCosts.reduce((n,x)=>n+(x.actualUSD||0),0)}));
}finally{await lock.close();await unlink(dir+'/research.lock')}
