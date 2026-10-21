import {classifyHeadline} from './engine.mjs';
export const DESIGN_VERSION='editorial-v2';
const angles={
 relationships:{label:'LOVE & LIFE',kicker:'오늘의 관계 사용설명서',hook:'이 뉴스, 우리라면?',lens:'기사 속 이야기를\n우리 대화로 바꿔 보면',questions:['서로 당연하다고 여긴 기준이 같은가?','돈·시간·집안일을 어떻게 나눌 것인가?','의견이 다를 때 어디까지 조율할 수 있나?'],checks:['추측 대신 내 기준을 한 문장으로 쓰기','상대의 기준도 직접 물어보기','둘이 합의한 내용과 남은 질문 나누기'],prompt:'우리 사이에 먼저\n맞춰야 할 것은?',a:'돈과 생활 방식',b:'말투와 갈등 푸는 법',route:'관계·생활 브랜드 협업 / 자체 대화 도구'},
 money_life:{label:'MONEY & LIFE',kicker:'오늘의 생활 사용설명서',hook:'내 지갑에도 해당될까?',lens:'큰 뉴스보다 중요한 건\n내 조건에 맞는지',questions:['내 지역·나이·소득·상황에도 해당하나?','시작일·마감일·예외 조건은 무엇인가?','실제 비용과 받을 수 있는 혜택은 얼마인가?'],checks:['공식 공고에서 대상과 기간 확인하기','총비용과 예외 조건을 함께 적기','신청·구매 전에 최신 조건 다시 확인하기'],prompt:'생활 정보에서\n먼저 보고 싶은 것은?',a:'실제 비용 비교',b:'해당 조건·마감일',route:'생활 서비스 협업 / 검증된 비교 자료'},
 technology:{label:'TOOLS & LIFE',kicker:'오늘의 도구 사용설명서',hook:'신기한데, 내게도 쓸모 있을까?',lens:'유행하는 기술을\n내 하루에 대입해 보면',questions:['내가 자주 하는 일에 실제로 쓸 수 있나?','무료 범위·유료 조건·제한은 무엇인가?','결과의 정확성과 개인정보 처리는 확인했나?'],checks:['내 작업 하나로 작게 시험하기','비용·권한·사용 제한 함께 확인하기','직접 쓴 결과를 기존 방식과 비교하기'],prompt:'새로운 도구에서\n더 중요한 것은?',a:'시간 절약',b:'결과의 정확성',route:'도구 브랜드 협업 / 자체 활용 자료'},
 food_travel:{label:'WEEKEND & LIFE',kicker:'오늘의 주말 사용설명서',hook:'저장만 할까, 같이 갈까?',lens:'가고 싶은 마음에\n현실적인 조건도 더하면',questions:['운영일·예약·교통편을 확인했나?','입장료·식비·이동비까지 예산에 맞나?','같이 갈 사람의 취향과 일정에도 맞나?'],checks:['공식 운영 시간과 예약 여부 확인하기','이동과 대기 시간을 함께 잡기','실제 예산과 대체 장소 하나 정하기'],prompt:'함께 가는 주말,\n당신의 선택은?',a:'새로운 경험',b:'편안하고 확실한 코스',route:'지역·여행 브랜드 협업 / 자체 일정 자료'},
 other:{label:'NEWS & LIFE',kicker:'오늘의 뉴스 사용설명서',hook:'이 뉴스, 내 생활에서는?',lens:'읽고 넘기기 전에\n한 번 더 확인할 것',questions:['기사에서 확인된 사실은 어디까지인가?','내 생활과 연결되는 부분이 있는가?','아직 확인되지 않은 조건은 무엇인가?'],checks:['기사 시각과 원출처 확인하기','사실과 의견 구분해서 읽기','행동 전에 공식 안내 다시 확인하기'],prompt:'뉴스를 볼 때\n더 궁금한 것은?',a:'왜 이런 일이 생겼나',b:'내 생활에 무엇이 달라지나',route:null}
};
export function briefExcerpt(description){const s=String(description||'').replace(/\s+/g,' ').trim();if(!s)return '';const words=s.split(' ');return words.slice(0,18).join(' ')+(words.length>18?' …':'');}
export function buildEditorial(row,config={}){
 const category=row.category||classifyHeadline(row.title||''),angle=angles[category]||angles.other;
 return {designVersion:DESIGN_VERSION,category,...angle,headline:row.title,excerpt:briefExcerpt(row.description),factLabel:'기사에서 확인한 내용',opinionLabel:'편집 질문 · 기사에서 단정한 사실이 아닙니다',conversion:{status:'not_connected',route:angle.route},cta:'이 주제가 떠오르는 사람이 있다면\n함께 읽고 각자의 기준을 나눠 보세요.',experiment:{id:'editorial-v2',status:'hypothesis_not_validated'}};
}
