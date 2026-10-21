# 브레이크 브리핑 연결·검증 상태 · 2026-10-21

기준 커밋 a7504467ebb2c6fdad187a4d87152cdf0508326b에서 이어받았다. 기존 로컬 변경은 별도 작업트리에 보존했다. 생활경제·리빙 전환은 시행 보류 그대로다.

## 구현과 검증

- Claude Messages/Models/Count Tokens HTTP 어댑터. 모델 ID는 환경변수로 명시하고 Models API에서 접근·입출력 한도·검색 기능을 확인한다. 자동 모델 선택·다른 모델로의 무단 대체 없음.
- 가격표는 공식 문서 확인일·출처·모델별 입력/출력/검색 단가를 저장한다. 7일 초과·가격 없음·비용 미확인은 중단한다. 모델/가격표를 영구 최신이라고 주장하지 않는다.
- API 호출 전에 최대 비용을 원장에 기록하고 저장 성공 후 호출한다. 최초 비공개 테스트 누적 $1, 한국 날짜별 $5. 예약·불명확 비용은 실제 비용처럼 차감한다. 응답의 input/output/search usage로 정산하며 타임아웃·알 수 없는 유료 도구·캐시 사용은 중단·정산 대기한다. 재시도 자동 실행 없음.
- 검색 max_uses는 입력 토큰 상한이 아니다. 검색 중 재입력 비용을 모델 최대 문맥×최대 반복으로 보수적으로 확보한다. Sonnet/Opus 검색의 최대 예상액이 $1을 넘으면 첫 시험에서는 요청 자체를 보내지 않는다. 이때 검색 기능을 연결·실행했다고 보고하지 않는다.
- 등록·허용된 1차 원자료를 독립 HTTP 조회하고 짧은 인용문 존재·자료 해시·확인 시각·수치 문맥을 코드로 검사한다. 등록 자료의 값을 이용한 차이·증감률·곱셈을 계산한다. 자료의 값 등록과 의미 판정은 별도 검토가 필요하다.
- 리서치→구조화 원고→별도 검수 호출→기존 Pillow 텍스트 배치 재사용→비공개 이미지까지 연결한 명시 실행 명령 `npm run research:private`를 추가했다. 최종 상태는 `awaiting_final_image_review` 또는 `held`이며 게시 함수는 호출하지 않는다.
- 별도 모델 검수는 독립 승인서가 아니다. 인용문 존재·계산 검사는 문장 전체의 진실성 증명이 아니다. 제목·질문·결론·캡션 전체의 의미·출처 충돌·후속 발표·이미지 최종 검수는 아직 자동 승인으로 연결하지 않았다.
- GitHub ref 생성의 원자성을 이용한 계정 잠금. 다른 실행·다른 워크플로 중첩도 거절한다. 강제 종료로 남은 잠금은 게시/비용 결과를 대조한 뒤 수동 해제해야 하며 자동 만료·강탈하지 않는다.
- 절대 회차별 영구 고유키, POSTED/PENDING/SKIPPED/ERROR와 이유 기록. 오래된 상태를 계정 잠금 밖에서 저장하는 경로를 제거했다.
- 공식 Instagram 어댑터에 단일 이미지 지원 및 게시 후 ID/permalink 조회를 추가했다. URL 확인 실패는 재게시 대신 결과 확인 대기로 남긴다.
- 실제 API 키 값·토큰·계정 비밀값·조직 ID를 코드나 이 문서에 기록하지 않는다. 원격 실행 상태에는 인증값의 존재 여부만 기록한다.

## 비공개 실행 입력

로컬 또는 사용자의 비공개 영구 실행 환경에 `ANTHROPIC_API_KEY`를 환경변수로 넣는다. 채팅에 키를 붙이지 않는다. GitHub Actions에는 저장소 Settings → Secrets and variables → Actions → New repository secret → `ANTHROPIC_API_KEY`. 이 Secret을 자동 실행기에 전달하도록 매핑했다. Secret 설정 자체가 리서치·검수·게시 연결 완료를 뜻하지 않는다.

비공개 시험은 동일한 절대경로 `PRIVATE_RESEARCH_DIR`를 모든 호출에서 재사용한다. 비용 원장·잠금·검토본은 이 경로에만 둔다. 초기화·삭제·다른 경로 분리로 한도를 우회하지 않는다. 비용 원장 없는 임시 GitHub runner에서 유료 시험을 실행하지 않는다. API 상한은 이 통합을 거치는 호출만 통제하며 다른 앱/키의 조직 전체 지출을 제한하는 Console 설정을 대신하지 않는다.

필수 환경변수: `PRIVATE_RESEARCH_DIR`, `RESEARCH_INPUT_FILE`, `ANTHROPIC_API_KEY`, `CLAUDE_RESEARCH_MODEL`, `CLAUDE_REVIEW_MODEL`. 검색을 켤 때만 `CLAUDE_MAX_SEARCHES` 및 현재 공식 지원 `CLAUDE_SEARCH_TOOL`. 기본 검색 횟수 0. 모델은 코드 기본값 없이 사용 가능한 ID를 명시한다.

입력 JSON: `{candidate:{title,storyKey,url},sources:[{id,url,label,primary:true,rightsVerified:true,aiProcessingAllowed:true,allowedOrigins:["https://기관의정확한호스트"],values:{선택:{value:숫자,quote:"값의 정확한 원문"}}}]}`. 권리 플래그는 검토 완료된 등록에만 설정한다. 모델이 스스로 권리를 승인하도록 하지 않는다. 텍스트 3만자·응답 25만바이트 상한, 리다이렉트·접근 차단·실패는 보류한다. 등록 원자료/수요 신호 자동 선정은 아직 연결되지 않았다.

## 실측과 한계

- 로컬 Claude 키 미설정. 실제 잔액 약 $450·조직·만료일·크레딧 적용·사용 가능한 모델·조직 한도는 미확인.
- 첫 실제 유료 종단 호출은 미실행, 토큰/검색 실측값 없음. 이 작업의 Claude 지출 $0. 모의 HTTP 응답 검증과 실제 API 실측을 구분한다.
- 69개 테스트 통과 및 가상 시험 자료 카드 1080×1350 / 390px 축소 시각 검수. 실제 뉴스의 내용 품질·실제 자동 게시 성공을 뜻하지 않는다.
- 오늘 공개 발행 영수증 4건, 운영 dailyCap=3. 제한은 유지한다. Meta 실제 계정 quota 조회가 없는 상태에서 상한을 올리지 않는다.
- 현재 연결 사용자명은 기존 계정으로 확인했다. 프로필 로고는 기존 최신 이미지를 복구하고 새 작은 BRIEFING 시안을 별도로 제작해 채팅 제공. 실제 프로필 이름·사진 미변경. 이미지 생성 비용이 Claude 크레딧으로 결제된다고 주장하지 않는다.

## 여전히 필요한 연결

1. 비공개 키 주입과 Console 크레딧·조직·만료·spend limit 확인.
2. 사용 가능한 모델 확인 후 최초 $1 내 실제 비공개 시험. 원자료 기반 시험을 먼저 하고 서버 검색은 사전 최대 비용 내일 때만 수행.
3. 자동 조사 대상·원자료/권리 등록·관측한 독자 수요 신호 입력 및 기존 생산 실행기 연결.
4. 최종 이미지·캡션·전체 주장과 원자료를 대조하는 신뢰 가능한 독립 검증기. 기존 차단 관문 유지.
5. Meta 공식 토큰·계정 ID·Graph 버전/로그인 유형·권한 확인 및 read-only 사용자명/실제 quota 조회. 기존 AUTOPILOT_CONFIG의 비공개 ig_access_token/ig_user_id/ig_graph_version/선택 ig_graph_host 경로 사용. 신규 비공식 로그인 자동화 없음.
6. 실제 게시 후 ID/URL·계정 확인. 무인 가동 전에는 운영 시작 완료로 표시하지 않는다.

## 공식 문서 확인

- https://platform.claude.com/docs/en/about-claude/pricing
- https://platform.claude.com/docs/en/api/models/list
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
- https://help.metricool.com/mcp-vs-api-access-what-is-the-difference-5y3ib
- https://help.metricool.com/basic-guide-for-api-integration-r97af

확인일 Sonnet 5.5 입력 $2/출력 $10, Opus 5.5 입력 $4/출력 $20 (각 100만 토큰당); 검색 $10/1,000회 및 입력 토큰 별도. 실제 키의 모델 접근·현재 가격과 다시 대조해야 한다. Metricool MCP는 무료 포함 모든 플랜, 코드 API는 Advanced/Custom 전용. 이 계정의 요금제·API 토큰·업그레이드는 확인/변경하지 않았다. Meta 게시 공식 문서는 검색 결과에서 확인했으나 전문 접근 실패, 실제 토큰/권한 read-only 검증은 미실행.
