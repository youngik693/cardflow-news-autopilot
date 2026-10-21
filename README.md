# 1분 리포트 뉴스 자동운영

대상 계정은 사용자가 지정한 **@my.love.manual**입니다.

## 최우선 제작 기준 — 2026-10-21 제정

**뉴스가 나온 순간, 사건·이유·배경·파장·독자의 효용을 한눈에 이해시키는 근거 있는 실시간 분석 정보지**가 목표입니다. 기본은 한 장의 완결된 핵심 분석이며, 추가 카드는 필요한 경우에만 사용합니다.

- [제작·사업 헌법](docs/editorial-constitution.md): 사용자의 두 차례 핵심 지시를 정리한 편집·디자인·사업 기준.
- [출처·레퍼런스·이용 정책](docs/source-reference-policy.md): 근거 표시와 상업 이용 조건을 구분하는 운영 기준.
- [후속 개발 작업 지침](AGENTS.md): 이후 작업 시 두 문서를 먼저 읽도록 지정.

아래의 기존 다장 템플릿·초안 설명은 구현 이력입니다. 새 헌법을 충족하는 자동 심층 리서치·한 장 축약·품질 판정이 모두 구현됐다는 의미가 아닙니다.

## 현재 단계

5분 주기 실행, 다음 메인 수집, 새 기사 카드 JPEG 제작과 출처 보존, 네이버 API 연결 경로, 인스타 게시 제어 코드를 준비했습니다. **코드가 설치됐다는 사실은 인스타 게시가 시작됐다는 뜻이 아닙니다.**

인스타 인증·운영 게시 상한·실제 인스타 반응 근거가 모두 확인된 기사만 게시합니다. 현재 반응 데이터가 없으면 초안만 만들고 게시를 보류합니다. 데이터가 없는 상태에서 ‘인스타 1위’라고 표시하지 않습니다.

## 결과 확인

- [Actions 실행 기록](../../actions): 실행을 열면 요약에 최근 카드 미리보기와 연결 상태가 표시됩니다.
- `autopilot-data` 브랜치 `data/state.json`: 수집 상태, 후보, 초안, 게시 원장. 이 저장소는 공개이므로 이 파일에는 공개 뉴스 정보·공개 게시물 분석 정보만 저장합니다.
- `autopilot-data` 브랜치 `media/`: 1080×1350 JPEG 카드 5장. 직접 제작한 배경과 한글 글꼴을 사용하며 기사 사진은 가져오지 않습니다.
- 실행은 매시간 02·07·12·17·22·27·32·37·42·47·52·57분을 목표로 하며 GitHub 사정으로 늦어질 수 있습니다. 정확한 실시간 보장은 아닙니다.

## 독립 카드뉴스 사업 — 2026-10-21 변경

이 프로젝트는 내연사·사주·운세 사업과 분리된 독립 뉴스 미디어입니다. 기존에 사용자가 선택한 게시 계정 `@my.love.manual`은 유지하며, 계정 이름이 다른 상품 연결을 의미하지는 않습니다.

주제 필터의 연애·생활 중심 제한을 해제했습니다. 경제·기술·문화·사회 등 실제 수집한 기사를 대상으로 인스타 관측 근거와 시의성으로 선별합니다. 현재 인스타 관측 어댑터가 연결되지 않아 자동 게시가 보류됩니다. 키만 넣으면 그 연결까지 자동 완성되는 것은 아닙니다.

기존 초안 템플릿의 5장 구조는 `표지 → 기사 제목·짧은 소개 → 맥락 확인 질문 → 독해 체크리스트 → 후속 정보 질문`입니다. 이 방식은 새 헌법의 완성 상품 기준이 아닙니다. 질문은 일반 편집 템플릿이며 기사별 추가 취재나 심층 해설이 아닙니다. 관련 상품 구매나 자동 DM으로 유도하지 않습니다. 뉴스 재사용 권리는 아직 확보 완료 상태가 아닙니다. 공개 소개문·제목의 이용 조건도 출처별 검토 대상입니다.

기존 `docs/previews/` 이미지와 [초기 시장 조사](docs/market-research.md)의 관계·생활 중심 제안은 이전 검토 기록입니다. 현재 운영 방향은 위 독립 뉴스 방침을 따릅니다. 기존 시안과 생성 초안은 보존하고 `news-v3`부터 새 방향을 적용합니다.

## 네이버 API HUB 연결 — 2026-10-21 수정

검색 API는 2026-07-31부터 기존 개발자센터에서 신규 신청이 중단됐다. 현재 기본값은 NAVER API HUB다. 기존 키를 구버전 주소로 호출하던 코드를 수정했으며, API HUB 키를 다시 발급할 필요는 없다.

- 새 주소: `https://naverapihub.apigw.ntruss.com/search/v1/news`
- 인증 헤더: `X-NCP-APIGW-API-KEY-ID`, `X-NCP-APIGW-API-KEY`
- `AUTOPILOT_CONFIG`의 `naver_client_id`, `naver_client_secret` 이름은 유지하되 실제 값은 API HUB의 발급값이다.
- 별도 Repository Secrets `NAVER_API_HUB_CLIENT_ID`, `NAVER_API_HUB_CLIENT_SECRET`도 지원한다. JSON에 값이 있으면 JSON 값이 우선한다.
- 기존 개발자센터 키를 보유한 사용자는 명시적으로 `naver_api_mode: "legacy"`를 지정해야 한다. 실패 시 인증값을 다른 호스트로 자동 전송하지 않는다.
- 공식 안내상 현재 한시적 무료이며 향후 유료 전환 가능성이 있다. 영구 무료로 보장하지 않는다. 이번 수정은 별도 클라우드 서버나 유료 상품을 생성하지 않는다.
- [공식 이관 공지](https://developers.naver.com/notice/article/32530), [공식 뉴스 API 명세](https://api.ncloud-docs.com/docs/naver-api-hub-search-news), [공식 이용 요금 안내](https://guide.ncloud-docs.com/docs/apihub-overview)

## 1회 연결 설정

[Settings → Secrets and variables → Actions](../../settings/secrets/actions)에서 Repository secret **AUTOPILOT_CONFIG**를 만드세요. 비밀값은 코드·이슈·채팅에 넣지 않습니다.

값의 구조(아래 예시 문자열은 실제 키가 아닙니다):

```json
{
  "naver_client_id": "네이버 검색 API Client ID",
  "naver_client_secret": "네이버 검색 API Client Secret",
  "ig_user_id": "인스타 프로페셔널 계정 ID",
  "ig_access_token": "게시 권한이 있는 Meta 액세스 토큰",
  "ig_graph_host": "graph.instagram.com",
  "ig_graph_version": "Meta 앱에서 확인한 v숫자.숫자 API 버전",
  "daily_cap": 2
}
```

- `daily_cap`의 2는 형식 예시입니다. 안전한 최대량이나 추천 성과를 뜻하지 않습니다. 계정 API 허용 상한과 운영 상한은 별도로 검사합니다.
- 토큰의 권한·만료·재연결은 실제 계정에 맞춰 확인해야 합니다. 현재 코드는 토큰 자동 갱신을 구현하지 않았습니다. 만료 시 게시를 중지합니다.
- Facebook Login을 쓰는 계정은 해당 토큰과 `graph.facebook.com` 호스트를 사용해야 합니다. 계정 소유자명이 @my.love.manual과 일치하는지 게시 전에 검사합니다.
- 네이버 값이 없으면 다음 메인만 수집합니다. 그 상태를 두 소스 연결 완료로 표시하지 않습니다.

## 인스타 인기 선별 데이터

`data/state.json`의 `signals`에는 **실제로 관측한 게시물**의 근거가 필요합니다. 자동 수집 어댑터 연결은 아직 남아 있습니다. 임의 값이나 추정 수치를 넣지 않습니다.

```json
{
  "platform": "instagram",
  "storyKey": "실제 뉴스 후보의 storyKey",
  "url": "실제로 관측한 인스타 게시물 URL",
  "observedAt": "ISO 8601 관측 시각",
  "metrics": {"comments": 30, "likes": 100},
  "baselines": {"comments": 10, "likes": 50}
}
```

누락된 조회수·저장·공유를 0으로 채우지 않습니다. 비교 기준이 없는 수치를 보편적인 인기 점수로 바꾸지 않습니다. 점수 가중치와 제목 키워드 카테고리는 검증 전 초기 가설입니다. 전 세계·한국 전체 인스타의 카테고리 1위를 의미하지 않습니다.

## 실행·비용·중복 게시

공개 저장소의 표준 GitHub Linux 실행기를 사용합니다. 실행에는 GitHub 및 네이버·Meta의 이용 한도가 적용됩니다. 별도 유료 AI 호출은 사용하지 않습니다. 렌더링은 Pillow와 Noto CJK 글꼴로 처리합니다.

같은 계정의 작업은 GitHub Actions concurrency로 직렬화합니다. 게시 전 원장을 GitHub에 먼저 저장하고, 게시 결과가 불명확하면 `needs_reconcile` 상태로 멈춥니다. 동일 기사를 무조건 다시 게시하지 않습니다.

카드가 매번 생성되는 것을 보장하지 않습니다. 중복·오래된 기사·출처 접속 실패·관측 근거 부족·게시 한도 도달 때는 생성을 생략하거나 게시를 보류합니다. 생성한 초안은 공개 저장소에 보관되므로 장기간 운영 시 미디어 호스팅과 보관 정책을 분리해야 합니다.

## 검증

```sh
npm test
```

단위 테스트는 모의 응답으로 검증합니다. 실제 Meta 게시·권한·계정 할당량은 인증 연결 후 따로 확인해야 합니다.

## 조사 근거

- https://metricool.com/instagram-trends/
- https://www.socialinsider.io/social-media-benchmarks/social-media-content-trends
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://developers.facebook.com/docs/instagram-platform/content-publishing/
