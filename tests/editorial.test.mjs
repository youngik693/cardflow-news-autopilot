import {test} from 'node:test';import assert from 'node:assert/strict';
import {buildEditorial,briefExcerpt} from '../src/editorial.mjs';
test('새 디자인이 기사 사실과 편집 질문을 구분하고 미연결 상품을 홍보하지 않음',()=>{const e=buildEditorial({title:'결혼 생활의 기준',description:'기사가 확인한 소개문'});assert.equal(e.headline,'결혼 생활의 기준');assert.match(e.opinionLabel,/기사에서 단정한 사실이 아닙니다/);assert.equal(e.conversion.status,'not_connected');assert(!JSON.stringify(e).includes('무료 다운로드'));assert(!JSON.stringify(e).includes('매출 보장'))});
test('경제·관계·도구 소식은 같은 판매 문구 대신 다른 독자 질문을 제공',()=>{const a=buildEditorial({category:'relationships',title:'사례'}),b=buildEditorial({category:'money_life',title:'사례'}),c=buildEditorial({category:'technology',title:'사례'});assert.notDeepEqual(a.questions,b.questions);assert.notDeepEqual(b.questions,c.questions);assert.match(b.questions.join(' '),/비용/);assert.match(c.questions.join(' '),/개인정보/)});
test('원문 소개문이 없으면 새 사실을 작성하지 않고 인용 분량을 제한',()=>{assert.equal(briefExcerpt(''),'');const text=Array.from({length:40},(_,i)=>'단어'+i).join(' ');assert(briefExcerpt(text).split(' ').length<=19);assert.match(briefExcerpt(text),/…$/)});

import {isReaderRelevant} from '../src/topic-fit.mjs';
test('기업 실적에 AI가 등장해도 생활 도구 뉴스로 뽑지 않음',()=>{assert.equal(isReaderRelevant({category:'technology',title:'A사 분기 매출 AI 덕분에 급증'}),false);assert.equal(isReaderRelevant({category:'technology',title:'챗GPT 새 기능 공개, 구독 요금은?'}),true);assert.equal(isReaderRelevant({category:'relationships',title:'부부 사망 사고'}),false)});
