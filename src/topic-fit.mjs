// Initial editorial scope, not a measured Instagram popularity model.
export function isReaderRelevant(row){
 const title=String(row.title||'');
 if(/살인|성폭행|성추행|사망|참사|폭행|자살/.test(title))return false;
 const topics={relationships:/연애|결혼|이혼|커플|부부|소개팅|동거|출산|육아/,money_life:/지원금|소비|월세|전세|대출|월급|취업|청년|세금|물가|보험|교통비|생활비/,technology:/챗GPT|챗지피티|ChatGPT|클로드|Claude|생성형|서비스|기능|사용법|앱|스마트폰|아이폰|구독|요금/,food_travel:/맛집|여행|항공|숙박|축제|음식|카페|호텔|관광|전시/};
 return Boolean(topics[row.category]?.test(title));
}
