# WRITING_GUIDE — 챕터 집필 에이전트용 지침

이 문서는 챕터 집필 서브에이전트가 반드시 따라야 하는 규칙이다. `FORMAT_SPEC.md`와 함께 읽을 것.

## 절대 규칙

1. **출력 파일**: `chapters/chNN.md` (zero-pad 2자리). 다른 파일은 건드리지 않는다.
2. **포맷**: FORMAT_SPEC.md의 장 템플릿 엄수 — 장 첫머리 `!!! note "이 장에서 배우는 것"`, 장 끝 `📌 핵심 요약` → `🤔 생각해보기`(워크북 밑줄 2개) → `✏️ 연습 문제` → `🔎 더 찾아보기` → `> **다음 장 예고**`.
3. **분량**: 본문 한국어 기준 **5,500자 이상** (코드/FIG 블록 제외). 인쇄 8쪽 목표.
4. **그림**: 장당 FIG 마커 **5개 이상**. `<!-- FIG: id=chNN-fXX | type=스크린샷|일러스트 | file=images/chNN/chNN-fXX.png -->` + 캡션 블록쿼트 + 캡처 지시문. 그림 번호는 `그림 N.X` 점 표기.
5. **톤**: 존댓말("~합니다"), 입문자 대상, 친근하지만 정확. 참조 문체는 이 리포의 기존 장(있다면) 또는 아래 예시를 따른다: "복사-붙여넣기가 없습니다." 같은 짧은 강조문 활용.
6. **바이브코딩 서사**: 이 책의 핵심 정체성. 코드를 직접 치라고 하지 않는다 — **Claude Code에게 시키는 프롬프트를 먼저 보여주고**, AI가 만들어 준 코드를 함께 읽으며 이해하는 흐름. 각 실습 절은 ①프롬프트 박스 → ②AI가 생성한 코드 → ③코드 해설 → ④실행 확인 순서.
7. **프롬프트 박스 표기**:
   ```
   !!! tip "🗣 이렇게 시키세요"
       > 지도를 화면 전체에 꽉 차게 띄워줘. 카카오지도 JS SDK를 쓰고, 키는 .env에서 읽어줘.
   ```
8. **코드 출처**: 앱 코드는 `app/src/*.js`가 단일 진실. 장 진도에 맞는 코드만 발췌한다(그 장 시점에 아직 안 배운 모듈 import는 빼거나 단순화). 코드를 지어내지 말 것 — 반드시 실제 파일을 읽고 발췌·단순화한다.
9. **사실 정확성**: 카카오 API 명칭·콘솔 메뉴 이름은 실제와 일치시킨다 (developers.kakao.com → 내 애플리케이션 → 앱 설정 → 플랫폼 → Web). JS 키는 본문에서 `여러분의 JS 키`로 표기, 예시 키는 `0123abcd...` 형태 더미 사용.
10. **각 장 끝 STATUS 갱신 금지** — 오케스트레이터가 한다. 집필만 할 것.

## 장별 브리프

### 0장 — 이 책에서 만드는 것
완성 앱 스크린샷 투어(지도·마커·말풍선·필터·검색·상세패널·공유), "바이브코딩으로 만든다"는 선언, 준비물(윈도우 PC, 카카오 계정, Claude Pro), 책의 로드맵(5부 구성 안내). FIG: 완성 화면 다수.

### 1장 — 왜 바이브코딩인가
바이브코딩 정의(말로 시키고 AI가 코드 작성), 저자의 실제 워크플로 소개(Claude Code + Orca + Git + GitHub CLI 조합), "코드를 이해하려 노력하되 외우지 않는다" 철학, 에이전트에게 일 시키는 마음가짐(작게 시키기, 확인하기, 되돌리기), 이 책에서 쓸 도구 5종 개관.

### 2장 — Node.js 설치
왜 필요한가(Vite/Claude Code가 Node 위에서 동작), node -v 확인, nodejs.org LTS 다운로드·설치(윈도우 스크린샷 단계별), PATH 문제 해결, npm 소개. FIG: 다운로드 페이지, 설치 마법사, 터미널 버전 확인.

### 3장 — Git for Windows 설치
git이 왜 필요한가(되돌리기 = 바이브코딩의 안전벨트), gitforwindows.org 다운로드, 설치 옵션 해설(기본값 추천, 에디터 선택, PATH 옵션), git -v 확인, git config user.name/email 첫 설정, 개념 최소한(저장소·커밋·브랜치 한 컷 설명). FIG: 설치 단계, 터미널.

### 4장 — Claude Code 설치하고 길들이기
가입·Pro 플랜, npm install -g @anthropic-ai/claude-code, 첫 실행과 로그인, 프롬프트 4요소(맥락·목표·제약·출력), 안전하게 쓰기(권한 프롬프트 의미), 무료 대안 박스(opencode/codex/antigravity). FIG: 설치 터미널, 첫 실행 화면.

### 5장 — GitHub CLI로 깃허브 연결
GitHub 계정 만들기, gh 설치(winget install GitHub.cli), gh auth login 흐름(브라우저 인증), gh repo create 로 첫 리포, git push 기초. FIG: gh auth login 터미널 단계.

### 6장 — Orca로 에이전트 지휘하기
Orca 소개(여러 에이전트를 워크트리로 병렬 지휘하는 데스크톱 앱), 설치, 워크트리 개념, 터미널에 Claude Code 띄우기, 여러 작업 병렬로 돌리기, 저자의 실전 화면 구성. FIG: Orca 화면. (설치 세부가 불확실하면 개념+워크플로 중심으로, 화면은 일러스트로 대체 가능)

### 7장 — 카카오 개발자 계정과 앱 만들기
developers.kakao.com 가입, 내 애플리케이션 → 애플리케이션 추가, 앱 키 4종 중 JavaScript 키의 의미, 앱 설정→플랫폼→Web에 http://localhost:5173 등록(왜 이 주소인지 예고), 키를 공개하면 안 되는 이유와 도메인 제한의 의미. FIG: 콘솔 각 단계.

### 8장 — Vite로 프로젝트 시작
Vite가 뭔지(개발 서버+빌드), npm create vite@latest(vanilla), 폴더 구조 투어, npm run dev와 5173 포트, .env에 VITE_KAKAO_JS_KEY 넣기, .gitignore에 .env(키 보호), import.meta.env 동작 원리. 코드: app/package.json, .env 예시.

### 9장 — 첫 지도 띄우기
SDK script 태그 vs 동적 로드, autoload=false와 kakao.maps.load()가 필요한 이유, loader.js 전체, index.html의 #map, 지도 생성 3요소(컨테이너·center·level), LatLng 위경도 개념. 코드: app/src/loader.js, main.js 축약판. 트러블슈팅: 회색 화면, 401/403(도메인 미등록).

### 10장 — 지도 다루기
setCenter/panTo 차이, setLevel(레벨 숫자와 축척 감각), MapTypeControl/ZoomControl, 지도 이벤트(click, dragend), 클릭한 곳 좌표 얻기(latLng). 미니 실습: 클릭하면 콘솔에 좌표 찍기(16장 예고).

### 11장 — 마커 찍기
kakao.maps.Marker 기본, 마커 여러 개(배열→반복), MarkerImage로 이미지 교체, SVG data URI 커스텀 핀(mapView.js의 markerImageFor 해설 — 카테고리 색·이모지). 코드: mapView.js 발췌.

### 12장 — 장소 데이터 설계
"데이터와 화면 분리" 개념, 장소 객체 스키마(id/name/category/lat/lng/rating/memo), defaultPlaces.js, categories.js(한 곳에서 관리), 데이터→마커 렌더링 함수. 좌표 얻는 법(카카오맵에서 우클릭, 지도 클릭 콘솔).

### 13장 — 커스텀 오버레이 말풍선
InfoWindow의 한계(스타일 제약), CustomOverlay + HTML/CSS 말풍선, yAnchor 개념, 열고 닫기 상태 관리(openOverlay 하나만), 말풍선 꼬리 CSS 트릭. 코드: mapView.js overlayContent/closeOverlay, style.css .bubble.

### 14장 — 카테고리 필터
필터 상태(currentFilter), filter() 메서드, 버튼 active 토글, 필터→마커 재렌더링 흐름(단방향: 상태→화면), "전체" 처리. 코드: sidebar.js 필터 부분.

### 15장 — 키워드 장소 검색
services 라이브러리(SDK URL에 &libraries=services), Places.keywordSearch, 콜백과 Status.OK, 검색 결과 상위 7개 렌더링, 결과 클릭→panTo. 코드: search.js 발췌. REST API와의 차이 짧은 박스.

### 16장 — 클릭·검색으로 장소 추가
지도 click 이벤트→추가 다이얼로그, 검색 결과 ＋버튼→같은 다이얼로그 재사용, 폼 값 검증(이름 필수), store.add()와 id 생성(Date.now().toString(36)). 코드: search.js openAddDialog, main.js 클릭 리스너.

### 17장 — localStorage 저장
새로고침하면 사라지는 문제 재현, localStorage 개념(키-값, 문자열만), JSON.stringify/parse, try-catch(사생활 모드), 저장 시점(save() 한 곳), 내보내기(Blob 다운로드)/가져오기(FileReader) — 백업의 중요성. 코드: store.js 전체 해설.

### 18장 — 사이드바 장소 목록
목록 렌더링(map→join), 목록 클릭→focusPlace(지도 이동+말풍선), 구독 패턴(store.subscribe — 데이터 바뀌면 화면 자동 갱신), 빈 목록 안내. 코드: sidebar.js renderList, store.js subscribe.

### 19장 — 상세 패널
상세 패널 UI, 별점 버튼(1~5), 메모 저장, 삭제와 confirm, XSS와 escapeHtml(사용자 입력을 innerHTML에 넣을 때 위험) — 보안 첫 경험. 코드: detail.js.

### 20장 — 내 위치 표시
Geolocation API, 권한 프롬프트 UX, 성공/실패 콜백, 파란 점 오버레이(CSS), https/localhost에서만 동작하는 이유. 코드: main.js 내위치, mapView.js showMyLocation.

### 21장 — URL로 지도 공유
URL 해시 개념, 상태 인코딩(#lat,lng,level), 정규식 파싱, clipboard API, history.replaceState. 코드: share.js. 한계와 확장 아이디어(장소까지 공유하려면?).

### 22장 — 마커 클러스터러
마커 100개 문제 시연, clusterer 라이브러리(&libraries=clusterer), MarkerClusterer 옵션(averageCenter, minLevel, minClusterSize), 클러스터 숫자 의미. 코드: mapView.js clusterer 부분. 실습: 예시 데이터 왕창 넣어보기.

### 23장 — 모바일 대응
개발자도구 디바이스 모드, 미디어쿼리(@media max-width:640px), 사이드바 접기/펼치기(collapsed 클래스, 지도 resize 트리거), 터치 확인. 코드: style.css 모바일 부분, sidebar.js toggleSidebar.

### 24장 — GitHub에 올리기
git init/add/commit 실전, .gitignore 재점검(.env·node_modules), gh repo create --public --source, 커밋 메시지 습관, 푸시 확인. FIG: GitHub 리포 화면.

### 25장 — GitHub Pages 배포
vite build와 dist, base 설정(vite.config.js), GitHub Actions로 Pages 배포(공식 워크플로), 카카오 콘솔에 Pages 도메인 추가(안 하면 403), 배포 URL 접속 확인. FIG: Actions 성공, 배포된 사이트.

### 26장 — README와 자랑하기
README 구조(스크린샷·기능·기술·실행법), 스크린샷 찍는 법, 셰어할 곳(친구·SNS), 다음 단계 로드맵(백엔드 저장, 로그인, 사진 업로드, 다른 API), 바이브코딩 마무리 회고.

### 부록 A (ch27) — 프롬프트 템플릿 모음
장별 핵심 프롬프트 전부 모음 + 상황별(버그 잡기, 리팩토링, 설명 요청, 되돌리기) 템플릿.

### 부록 B (ch28) — 트러블슈팅 & 치트시트
증상→원인→해결 표(회색 지도, 401, 403, CORS, .env 안 읽힘, 5173 충돌, 마커 안 보임 등), git/gh/npm 명령 치트시트, 카카오 SDK 객체 치트시트.
