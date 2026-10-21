import {classifyHeadline} from './engine.mjs';
export const DESIGN_VERSION='news-v3';
const desks={
 relationships:{label:'SOCIETY / 사회',prompt:'이 이슈에서\n더 확인하고 싶은 것은?',a:'제도와 통계',b:'당사자의 다양한 관점'},
 money_life:{label:'ECONOMY / 경제',prompt:'경제 뉴스에서\n더 궁금한 것은?',a:'수치와 비교 기준',b:'산업과 소비자에 미칠 영향'},
 technology:{label:'TECH / 기술',prompt:'기술 뉴스에서\n더 궁금한 것은?',a:'기술의 실제 변화',b:'비용과 적용 가능성'},
 food_travel:{label:'CULTURE / 문화',prompt:'다음 편에서\n더 보고 싶은 것은?',a:'현장의 정보',b:'가격과 이용 조건'},
 entertainment:{label:'CULTURE / 연예',prompt:'이 소식에서\n더 보고 싶은 것은?',a:'공식 발표와 일정',b:'작품·활동의 배경'},
 other:{label:'NEWS / 주요 이슈',prompt:'이 뉴스에서\n더 확인하고 싶은 것은?',a:'사건의 배경',b:'앞으로의 공식 발표'}
};
export function briefExcerpt(description){const s=String(description||'').replace(/\s+/g,' ').trim();if(!s)return '';const words=s.split(' ');return words.slice(0,18).join(' ')+(words.length>18?' …':'');}
export function buildEditorial(row,config={}){
 const category=row.category||classifyHeadline(row.title||''),desk=desks[category]||desks.other;
 return {designVersion:DESIGN_VERSION,productMode:'standalone_news',category,...desk,kicker:'카드플로우 뉴스 브리핑',hook:'사실부터, 맥락까지',lens:'이 뉴스를 읽을 때\n함께 확인할 질문',questions:['발생·발표 시점과 보도 시점은 같은가?','공식 발표와 아직 확인되지 않은 부분은?','수치·인용·전망의 원출처는 어디인가?'],checks:['사실과 주장·전망을 나누어 읽기','숫자는 기간과 비교 대상을 함께 보기','후속 발표가 나왔는지 원문에서 확인하기'],headline:row.title,excerpt:briefExcerpt(row.description),factLabel:'기사에서 확인한 내용',opinionLabel:'편집 확인 질문 · 확인 완료된 사실 목록이 아닙니다',conversion:{status:'not_connected',route:'독립 미디어의 광고·스폰서십·뉴스레터 사업 검증'},cta:'기억해 둘 이슈라면 저장하고\n이 주제가 궁금한 사람과 함께 읽어보세요.',experiment:{id:DESIGN_VERSION,status:'hypothesis_not_validated'}};
}
