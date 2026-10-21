import {test} from 'node:test';
import assert from 'node:assert/strict';
import {publicationSlotGate} from '../src/schedule.mjs';
import {DEFAULT_POLICY,publicationGate,runAutopilotTick} from '../src/engine.mjs';

const policy={mode:'live',targetAccount:'example',dailyCap:8,minGapMinutes:10,
  publicationUntil:'2026-10-21T18:00:00+09:00',slotWindowMinutes:10,
  publicationSlots:['2026-10-21T16:00:00+09:00','2026-10-21T16:30:00+09:00','2026-10-21T17:00:00+09:00','2026-10-21T17:30:00+09:00']};
const gate=(at,ledger=[])=>publicationSlotGate({policy,ledger,now:Date.parse(at)});

test('한국시간과 UTC가 동일 회차를 가리키고 시작 직전에는 발행하지 않는다',()=>{
  assert.equal(gate('2026-10-21T06:59:59Z').allowed,false);
  assert.equal(gate('2026-10-21T07:00:00Z').slotAt,policy.publicationSlots[0]);
  assert.equal(gate('2026-10-21T07:09:59Z').allowed,true);
});
test('지연 허용 시간을 지난 회차를 소급 발행하지 않는다',()=>{
  assert.equal(gate('2026-10-21T07:10:00Z').allowed,false);
  assert.equal(gate('2026-10-21T07:20:00Z').allowed,false);
  assert.equal(gate('2026-10-21T07:30:00Z').slotAt,policy.publicationSlots[1]);
});
test('같은 회차는 다른 기사여도 재게시하지 않고 미확정 결과도 막는다',()=>{
  for(const status of ['published','publishing','needs_reconcile']) {
    assert.deepEqual(gate('2026-10-21T07:05:00Z',[
      {account:'example',status,slotAt:'2026-10-21T07:00:00Z',storyKey:'another-story'}
    ]).blocks,['PUBLICATION_SLOT_USED']);
  }
  assert.equal(gate('2026-10-21T07:30:00Z',[
    {account:'example',status:'published',slotAt:policy.publicationSlots[0]}
  ]).allowed,true);
});
test('18시·다음날·다음해에는 반복 발행하지 않는다',()=>{
  for(const at of ['2026-10-21T09:00:00Z','2026-10-22T07:00:00Z','2027-10-21T07:00:00Z'])
    assert.equal(gate(at).allowed,false);
});
test('시간대 없는 설정·중복 시각·잘못된 지연 설정은 차단한다',()=>{
  for(const overrides of [{publicationSlots:[]},{publicationSlots:['2026-10-21T16:00:00']},
    {publicationSlots:[...policy.publicationSlots,policy.publicationSlots[0]]},{slotWindowMinutes:0}])
    assert.deepEqual(publicationSlotGate({policy:{...policy,...overrides}}).blocks,['PUBLICATION_SCHEDULE_INVALID']);
});
test('회차가 열려도 실제 할당량과 운영 한도를 우회할 수 없다',()=>{
  const now=Date.parse('2026-10-21T07:00:00Z'),quota={usage:0,total:50,durationSeconds:86400,checkedAt:new Date(now).toISOString()};
  assert.equal(publicationGate({policy,quota,now,targetConfirmed:true}).allowed,true);
  assert(publicationGate({policy,quota:null,now,targetConfirmed:true}).blocks.includes('LIVE_QUOTA_UNKNOWN'));
  assert(publicationGate({policy:{...policy,dailyCap:1},quota,now,targetConfirmed:true,ledger:[
    {account:'example',status:'published',at:'2026-10-21T05:00:00Z'}
  ]}).blocks.includes('OPERATIONAL_CAP_REACHED'));
  assert(publicationGate({policy,quota:{...quota,checkedAt:'2026-10-21T07:20:00Z'},now:Date.parse('2026-10-21T07:20:00Z'),targetConfirmed:true}).blocks.includes('OUTSIDE_PUBLICATION_SLOT'));
});
test('카드 제작 중 회차가 닫히면 게시하지 않고 다음 허용 회차는 최종 시각으로 기록한다',async()=>{
  for(const finish of ['2026-10-21T07:20:00Z','2026-10-21T07:30:00Z']) {
    let clock=Date.parse('2026-10-21T07:05:00Z'),data={ledger:[]},published=0;
    const candidate={storyKey:'one',title:'AI 발표',url:'https://example.org/story',provider:'daum',portalRank:1,publishedAt:'2026-10-21T06:55:00Z'};
    const signal={platform:'instagram',storyKey:'one',url:'https://www.instagram.com/p/example/',observedAt:'2026-10-21T07:00:00Z',metrics:{views:300,comments:30},baselines:{views:100,comments:10}};
    const result=await runAutopilotTick({policy:{...DEFAULT_POLICY,...policy,requirePrepublicationVerification:false,requireLiveSourceRecheck:false},
      now:()=>clock,targetConfirmed:true,readNews:async()=>[candidate],readSignals:async()=>[signal],
      store:{withAccountLease:async(_,fn)=>fn(),load:async()=>data,save:async v=>{data=structuredClone(v)}},
      readQuota:async()=>({usage:0,total:50,durationSeconds:86400,checkedAt:new Date(clock).toISOString()}),
      renderAndHost:async()=>{clock=Date.parse(finish);return {images:['https://example.org/card.jpg'],idempotencyKey:'image-one'}},
      publish:async()=>{published++;return {mediaId:'posted'}}});
    if(finish.endsWith('20:00Z')) {assert.equal(result.status,'blocked');assert.equal(published,0);}
    else {assert.equal(result.status,'published');assert.equal(data.ledger[0].slotAt,policy.publicationSlots[1]);}
  }
});

test('permanent slot outcomes preserve absolute keys, expired reasons and real URLs',async()=>{const {recordSlotOutcomes}=await import('../src/schedule.mjs');const policy={targetAccount:'account',slotWindowMinutes:10,publicationSlots:['2026-10-21T16:00:00+09:00','2026-10-21T16:30:00+09:00']};const state={ledger:[]};recordSlotOutcomes(state,policy,{now:Date.parse('2026-10-21T16:11:00+09:00'),blockers:['AUTH_REQUIRED']});assert.equal(state.slotOutcomes[0].status,'SKIPPED');assert.equal(state.slotOutcomes[1].status,'PENDING');state.ledger.push({account:'account',slotAt:policy.publicationSlots[1],status:'published',externalPostURL:'https://www.instagram.com/p/test/'});recordSlotOutcomes(state,policy,{now:Date.parse('2026-10-22T16:00:00+09:00')});assert.equal(state.slotOutcomes[1].status,'POSTED');assert.equal(state.slotOutcomes[1].publicURL,'https://www.instagram.com/p/test/');assert(state.slotOutcomes[0].reasons.includes('AUTH_REQUIRED'))});
