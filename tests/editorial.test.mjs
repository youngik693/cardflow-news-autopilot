import {test} from 'node:test';import assert from 'node:assert/strict';
import {buildEditorial,briefExcerpt} from '../src/editorial.mjs';
test('새 디자인이 기사 사실과 편집 질문을 구분하고 미연결 상품을 홍보하지 않음',()=>{const e=buildEditorial({title:'결혼 생활의 기준',description:'기사가 확인한 소개문'});assert.equal(e.headline,'결혼 생활의 기준');assert.match(e.opinionLabel,/확인 완료된 사실 목록이 아닙니다/);assert.equal(e.conversion.status,'not_connected');assert(!JSON.stringify(e).includes('무료 다운로드'));assert(!JSON.stringify(e).includes('매출 보장'))});
test('독립 뉴스는 연애 상품이나 운세로 유도하지 않으며 경제·기술 맥락을 구분',()=>{const a=buildEditorial({category:'money_life',title:'산업 실적 발표'}),b=buildEditorial({category:'technology',title:'새 기술 발표'});assert.notEqual(a.label,b.label);assert.notEqual(a.prompt,b.prompt);for(const e of [a,b]){assert.equal(e.productMode,'standalone_news');assert(!/내연사|운세|대화 도구/.test(JSON.stringify(e)));assert.equal(e.conversion.status,'not_connected')}});
test('원문 소개문이 없으면 새 사실을 작성하지 않고 인용 분량을 제한',()=>{assert.equal(briefExcerpt(''),'');const text=Array.from({length:40},(_,i)=>'단어'+i).join(' ');assert(briefExcerpt(text).split(' ').length<=19);assert.match(briefExcerpt(text),/…$/)});

import {isReaderRelevant} from '../src/topic-fit.mjs';
test('기업 실적에 AI가 등장해도 생활 도구 뉴스로 뽑지 않음',()=>{assert.equal(isReaderRelevant({category:'technology',title:'A사 분기 매출 AI 덕분에 급증'}),false);assert.equal(isReaderRelevant({category:'technology',title:'챗GPT 새 기능 공개, 구독 요금은?'}),true);assert.equal(isReaderRelevant({category:'relationships',title:'부부 사망 사고'}),false)});
