# CAPTURE_PLAN.md — 그림 전수조사 및 실행 계획

작성: 2026-09-02 (그림 감사 에이전트, 적대적 전수조사)

## 감사 결과 요약

- `images.yaml` 전체 엔트리: **178개** (captured 30 / pending 148)
- `chapters/ch00~ch28.md` 잔여 `<!-- FIG: id=... -->` 마커: **148개 (유니크 148)**
- **교차 검증: pending 148개 = 잔여 마커 148개, 1:1 완전 일치.** 마커만 있고 yaml에 없는 항목 0, yaml에만 있고 마커가 남은 captured 항목 0.
- captured 30개의 실물 파일은 `docs/images/ch*/`에 전부 존재 (yaml의 `file:` 경로는 `docs/` 기준 상대경로).
- 앱(`H:\YLBooks2\app`)은 완성본(검색·필터·상세패널·localStorage·공유·클러스터러·반응형 포함)이므로 A류 대부분은 `npm run dev` 후 즉시 연출 가능. 단 **초기 장(ch09~ch11)의 "미완성 단계" 화면은 완성 앱에서 역연출**이 필요하다(각 행에 명세).
- 전역 `window.__map` 노출 확인(main.js:30), localStorage 키 `my-map-places-v1`(store.js:4), 모바일 브레이크포인트 640px(style.css:189) 확인.

분류: **A** 앱 상태 캡처(53) · **B** 터미널 캡처(16) · **C** 공개 웹 캡처(16) · **D** 설치 마법사·로컬 창(14) · **E** 다이어그램 제작(47) · **F** 불가/보류(2) — 합계 148

공통 준비물:
- 앱 서버: `cd H:\YLBooks2\app; npm run dev` → http://localhost:5173
- 스크래치 루트(파괴적 명령 격리용): `%TEMP%\ylbooks-capture\` 이하에 `my-map`(vite 스캐폴드), `fakehome`(git 글로벌 설정 격리), `claude-demo`(Claude Code 시연) 3개 폴더
- 상태 리셋 스니펫(콘솔): `localStorage.removeItem('my-map-places-v1'); location.reload()`
- 테스트 100개 주입 스니펫(콘솔, ch22용):
  `const a=JSON.parse(localStorage.getItem('my-map-places-v1')||'[]');for(let i=1;i<=100;i++){a.push({id:'t'+i,name:'테스트 장소 '+i,category:['food','cafe','travel','date'][i%4],lat:37.45+Math.random()*0.18,lng:126.85+Math.random()*0.25,rating:0,memo:''})};localStorage.setItem('my-map-places-v1',JSON.stringify(a));location.reload()`

---

## A. 앱 상태 캡처 (localhost:5173) — 53건

전제: dev 서버 기동, 크롬. "콘솔"은 F12 DevTools Console. 브라우저 UI(주소창·권한 프롬프트·DevTools 자체)가 포함되는 컷은 페이지 캡처가 아닌 **OS 창 캡처** 필요(행에 [OS] 표기).

| FIG id | 장 | 캡션 | 실행 방법 |
|---|---|---|---|
| ch00-f02 | 0 | 마커 클릭 시 나타나는 커스텀 말풍선 | 기본 장소 마커 클릭 → 말풍선(이모지·이름·★·꼬리) 열린 상태를 확대 캡처 |
| ch00-f03 | 0 | 카테고리 필터로 카페만 표시한 화면 | 사이드바 "☕ 카페" 필터 클릭(active) → 카페 마커·목록만 남은 전체 화면. ch00-f01(app-main.jpg)과 같은 지도 영역 유지 |
| ch08-f04 | 8 | 브라우저에서 확인한 Vite 환영 페이지 | [OS] 스크래치에 `npm create vite@latest my-map -- --template vanilla` → `npm run dev` → 크롬으로 접속, 주소창 포함 창 캡처 (본 앱 서버는 잠시 중지해 포트 5173 확보) |
| ch08-f06 | 8 | 브라우저 콘솔에서 키 로드 확인 | 콘솔에서 `console.log('카카오 키 로드: 0123... (OK)')` 실행해 연출 후 Console 탭 캡처 (더미 4글자만) |
| ch09-f04 | 9 | 첫 지도! 서울시청 중심 화면 가득 카카오지도 | [OS] 연출: 콘솔에서 사이드바·컨트롤 숨김 `document.querySelector('#sidebar').hidden=true` + 마커 전부 제거(클러스터러 clear) 후 `__map.setCenter(new kakao.maps.LatLng(37.5665,126.978))` → 주소창 포함 창 캡처 |
| ch09-f05 | 9 | 도메인 미등록 시 콘솔 403 에러 | [OS] 연출: `.env`를 임시 더미 키로 바꿔 dev 재기동(또는 콘솔에서 `fetch('https://dapi.kakao.com/v2/maps/sdk.js?appkey=wrongkey')`) → Console 탭 빨간 403 확대. 캡처 후 .env 원복 |
| ch10-f01 | 10 | 콘솔 `__map.setLevel(3)` 확대 지도 | 콘솔에 `__map.setLevel(3)` 입력·실행 → 지도+콘솔이 한 화면에 보이게 DevTools 도킹 조절 [OS] |
| ch10-f03 | 10 | 레벨 3(좌)·레벨 7(우) 비교 | `__map.setLevel(3)` 캡처 → `__map.setLevel(7)` 캡처 → 좌우 합성 + "level: 3/7" 라벨(합성 후처리) |
| ch10-f04 | 10 | 지도 타입·줌 컨트롤 달린 지도 | 콘솔: `__map.addControl(new kakao.maps.MapTypeControl(),kakao.maps.ControlPosition.TOPRIGHT); __map.addControl(new kakao.maps.ZoomControl(),kakao.maps.ControlPosition.RIGHT)` → 전체 화면, 강조 박스는 후처리 |
| ch10-f05 | 10 | 스카이뷰 전환 지도 | 위 컨트롤 추가 후 "스카이뷰" 버튼 클릭(또는 `__map.setMapTypeId(kakao.maps.MapTypeId.HYBRID)`) → 컨트롤 선택 상태 포함 캡처 |
| ch10-f06 | 10 | 클릭마다 콘솔에 찍히는 좌표 | 콘솔: `kakao.maps.event.addListener(__map,'click',e=>console.log('클릭한 곳:',e.latLng.getLat(),e.latLng.getLng()))` 등록 → 지도 3~4회 클릭 → 지도+콘솔 동시 캡처 [OS] |
| ch11-f01 | 11 | 서울시청 위 첫 기본 마커 1개 | 연출: 기존 마커 숨김(빈 데이터로 리셋) 후 콘솔 `new kakao.maps.Marker({map:__map,position:new kakao.maps.LatLng(37.5665,126.978)})` → 마커 중앙 배치 캡처 |
| ch11-f02 | 11 | 반복문으로 찍은 기본 마커 4개 | 콘솔에서 경복궁·남산타워·광장시장·한강공원 4좌표 배열 forEach로 기본 마커+title 생성 → 남산타워에 호버해 툴팁 뜬 순간 캡처 |
| ch11-f04 | 11 | MarkerImage 별 마커 | 콘솔: 카카오 예제 starImage(`https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png`) 적용 마커 + 기본 마커 1개 나란히 생성 후 캡처 |
| ch11-f05 | 11 | 카테고리별 커스텀 핀 4종 | 빈 데이터 상태에서 콘솔로 4카테고리 장소 4개를 store에 추가(또는 markerImageFor 직접 호출로 4핀 생성) → 낮은 레벨로 4핀 나란히 캡처 |
| ch11-f06 | 11 | renderPlaces가 그린 장소 3곳 | localStorage에 광장시장🍜·연남동☕·남산타워💕 3건만 넣고 새로고침 → 핀 3개, 가능하면 title 툴팁 포함 |
| ch12-f04 | 12 | DEFAULT_PLACES 5곳 카테고리 핀 | 리셋 스니펫으로 초기화(기본 장소 5곳 로드) → 5핀 모두 보이게 레벨 조정 후 캡처 |
| ch12-f06 | 12 | 지도 클릭 → 콘솔 좌표 | ch10-f06과 동일 요령, "lat: 37.xxxx, lng: 126.xxxx" 포맷으로 로그 연출 [OS] |
| ch13-f01 | 13 | 기본 InfoWindow 열린 모습 | 콘솔: `new kakao.maps.InfoWindow({content:'<div style="padding:6px">광장시장</div>'}).open(__map, 기존마커)` → 흰 사각형+기본 꼬리 확대 캡처 |
| ch13-f06 | 13 | 완성된 커스텀 말풍선 | 여러 카테고리 마커 표시 상태에서 하나 클릭 → 말풍선(이모지·이름·★·×·꼬리) 확대 캡처 |
| ch14-f03 | 14 | 필터 바 UI, "전체" active | 초기 상태 사이드바 확대 캡처(검색창 아래 알약 버튼 5개, 전체만 채움) |
| ch14-f05 | 14 | 💕 데이트 필터 적용 | "💕 데이트" 클릭 → 필터 바 확대 + 남산타워·망원한강공원 2핀만 남은 지도 |
| ch15-f02 | 15 | 사이드바 상단 검색창 | 초기 화면 사이드바 위쪽 확대(검색 입력칸+🔍, 결과 목록 숨김) |
| ch15-f03 | 15 | 콘솔 keywordSearch 결과 | 콘솔: `new kakao.maps.services.Places().keywordSearch('성수동 카페',(d,s)=>{console.log(s,d)})` → OK+배열, 첫 항목 펼쳐 place_name·x·y 필드 보이게 |
| ch15-f04 | 15 | "성수동 카페" 결과 상위 7개 | 검색창에 "성수동 카페" 입력·검색 → 결과 7개 목록 펼쳐진 사이드바 캡처 |
| ch15-f05 | 15 | 결과 클릭 → 레벨 3 확대 이동 | 위 상태에서 결과 1개 클릭 → 확대된 지도+결과 목록 함께 캡처 |
| ch15-f06 | 15 | 결과 없음 토스트 | 검색창에 "ㅁㄴㅇㄹ" 검색 → "검색 결과가 없습니다." 토스트 뜬 순간 캡처(토스트 지속시간 짧으면 연사) |
| ch16-f03 | 16 | 이름 빈 채 추가 → 검증 토스트 | 지도 클릭으로 다이얼로그 열기 → 이름 비운 채 추가 클릭 → 토스트+열린 다이얼로그 동시 캡처 |
| ch16-f05 | 16 | ＋ 클릭 시 이름 미리 채워진 다이얼로그 | 검색 후 결과의 ＋ 클릭 → 이름 채워진 다이얼로그, 카테고리 select 펼쳐 ☕ 선택 중 상태 |
| ch16-f06 | 16 | 지도 클릭으로 추가한 장소 마커 | 지도 클릭 → "단골 산책길" 입력·🏝 선택·추가 → 새 마커+"내 지도에 추가했습니다!" 토스트 |
| ch17-f01 | 17 | 새로고침 전(좌)/후(우) 비교 | 연출 주의: 저장을 우회해야 함 — 콘솔에서 store를 거치지 않고 마커만 직접 2~3개 추가 → 캡처 → F5 → 캡처 → 좌우 합성+빨간 원 후처리 |
| ch17-f03 | 17 | Application 탭 localStorage "hello" | 콘솔 `localStorage.setItem('hello','반갑습니다')` → Application 탭 > Local Storage > localhost:5173 행 캡처 [OS] |
| ch17-f05 | 17 | 새로고침 후 살아남은 장소 + 저장 데이터 | 장소 추가 → F5 → 지도+Application 탭(`my-map-places-v1` JSON 행) 동시 캡처 [OS] |
| ch17-f07 | 17 | 가져오기 성공 토스트 | 내보내기로 받은 JSON을 가져오기 버튼으로 선택 → "가져오기 완료!" 토스트 순간 캡처 |
| ch18-f04 | 18 | 빈 목록 안내 문구 | 모든 장소 삭제(콘솔에서 `localStorage.setItem('my-map-places-v1','[]');location.reload()`) → 사이드바 목록의 안내 문구 확대 |
| ch18-f05 | 18 | 목록 클릭 → focusPlace | 목록 항목에 호버(배경색)+해당 장소로 확대·말풍선 열린 지도 전체 화면 |
| ch19-f03 | 19 | 별 5개 클릭, 패널·말풍선 동기화 | 상세 패널 열고 5번째 별 클릭 → 패널 ★5 + 말풍선 ★5 동시 보이게 캡처 |
| ch19-f04 | 19 | 삭제 confirm 다이얼로그 | [OS] 삭제 클릭 → 네이티브 confirm이 페이지를 블록하므로 Win+Shift+S 또는 별도 캡처 도구로 OS 수준 캡처 |
| ch19-f06 | 19 | escapeHtml로 태그가 글자 그대로 | 이름 `<b>굵은 국밥집</b>`으로 장소 추가 → 상세 패널 제목+말풍선에 문자열 그대로 보이는 상태 |
| ch20-f02 | 20 | 크롬 위치 권한 프롬프트 | [OS] 사이트 설정에서 위치 권한 '묻기'로 초기화 → 🧭 클릭 → 프롬프트 열린 순간 OS 캡처(브라우저 UI라 페이지 캡처 불가) |
| ch20-f03 | 20 | 지도 우하단 🧭 버튼 | 앱 전체 화면 캡처, 🧭 버튼 원형 강조는 후처리 |
| ch20-f05 | 20 | 내 위치 파란 점 | 개인 위치 노출 방지: DevTools > Sensors에서 좌표를 서울시청(37.5665,126.978)으로 오버라이드 → 🧭 클릭 → 파란 점+링, 인셋 확대는 후처리 |
| ch20-f06 | 20 | 권한 거부 토스트 | 사이트 설정에서 위치 '차단' → 🧭 클릭 → "위치 권한이 거부되었습니다" 토스트 캡처 |
| ch21-f02 | 21 | 공유 버튼 → 해시+복사 토스트 | [OS] 🔗 클릭 → 주소창 해시+토스트가 함께 보이게 창 전체 캡처 |
| ch21-f05 | 21 | 링크를 새 탭에서 연 결과 비교 | [OS] 창 2개를 좌우 배치(원본 탭/붙여넣어 연 탭, 같은 해시·같은 화면) → 모니터 영역 캡처 |
| ch22-f01 | 22 | 마커 100개 지도 (클러스터러 전) | 100개 주입 스니펫 실행 → 연출 주의: 완성 앱은 클러스터러가 켜져 있으므로 콘솔에서 minLevel을 크게(`14`) 올리거나 클러스터러 우회해 낱개 100핀 상태로 → 레벨 8~9 캡처 |
| ch22-f03 | 22 | 콘솔 MarkerClusterer 로드 확인 | 콘솔에 `kakao.maps.MarkerClusterer` 입력 → class 출력 캡처 ("undefined 기록 병기"는 services만 로드한 탭에서 먼저 찍으면 가능) |
| ch22-f06 | 22 | 확대하면 클러스터가 낱개로 | 100개 상태에서 클러스터 원 더블클릭/휠 확대 → 레벨 4~5 낱개 핀 화면. 확대 전후 좌우 합성 권장 |
| ch23-f01 | 23 | 디바이스 모드 진입 UI | [OS] F12 → Ctrl+Shift+M → iPhone SE 375×667 선택 상태의 크롬 창 전체 캡처(강조 후처리) |
| ch23-f02 | 23 | 모바일 대응 전 화면 | 연출 난이도 높음: DevTools > Elements에서 style.css의 `@media (max-width:640px)` 블록 규칙을 체크 해제(비활성)해 데스크톱 레이아웃 강제 → 375px 뷰에서 사이드바가 화면을 잡아먹는 상태 캡처 |
| ch23-f04 | 23 | 미디어쿼리 적용 후 모바일 화면 | 디바이스 모드 iPhone SE 기본 상태(지도 전면+84vw 사이드바 오버레이) 캡처 |
| ch23-f05 | 23 | 사이드바 접은 모바일 화면 | 디바이스 모드에서 사이드바 접기(◀) → 지도 전면+좌상단 ▶ 버튼만 남은 상태 |
| ch28-f02 | 28 | 403 Forbidden 콘솔 | ch09-f05와 동일 연출(더미 키) → Console 탭의 dapi.kakao.com 403 줄 확대 |

## B. 터미널 캡처 (Windows Terminal) — 16건

전제: Windows Terminal + PowerShell, 글꼴 크게(Ctrl+= 2~3회). 파괴적·시스템 변경 명령은 전부 스크래치(`%TEMP%\ylbooks-capture\`) 기준으로 재구성했다. **주의: 실제 계정 이메일(user.email)이 노출되는 컷은 격리 홈으로 연출.**

| FIG id | 장 | 캡션 | 실행 방법 |
|---|---|---|---|
| ch02-f01 | 2 | 설치 전 `node -v` 오류 | 새 PowerShell에서 `$env:Path=''` 후 `node -v` → "용어가 인식되지 않습니다" 오류 연출(현 PC엔 Node 설치됨). 해당 창만 캡처 후 닫기 |
| ch03-f01 | 3 | git 미설치 오류 | 동일 요령: `$env:Path=''; git -v` → 오류 문구 캡처 |
| ch03-f06 | 3 | user.name/email 등록된 모습 | 개인정보 격리: `$env:HOME="$env:TEMP\ylbooks-capture\fakehome"; $env:USERPROFILE=$env:HOME` 후 `git config --global user.name "홍길동"; git config --global user.email "hong@example.com"; git config --global --list` → 더미 2줄 캡처 |
| ch04-f03 | 4 | npm으로 Claude Code 설치 | `npm install -g @anthropic-ai/claude-code` 재실행(이미 설치돼 있어도 재설치라 안전) → "added ... packages" 완료 메시지 캡처 |
| ch04-f05 | 4 | Claude Code 첫 실행 화면 | 스크래치 `claude-demo` 폴더에서 `claude` 실행 → 환영 배너+프롬프트 캡처. 주의: 이미 온보딩된 계정이라 최초 설정(테마 선택 등) 화면은 안 나옴 — 환영 배너 컷으로 대체하거나 `claude --settings` 초기화는 시도하지 말 것(사용자 설정 파괴) |
| ch04-f07 | 4 | 권한 프롬프트(Yes/No) | `claude-demo`에서 `claude` 실행 → "test.txt 파일을 만들어줘" 요청 → 파일 생성 승인 다이얼로그(Yes/No) 화면 캡처 후 거절 |
| ch05-f02 | 5 | winget으로 GitHub CLI 설치 | gh 설치됨 → `winget install GitHub.cli --force`로 재설치 연출(동일 버전 덮어쓰기, 안전) → 진행 막대+완료 메시지 캡처 |
| ch05-f04 | 5 | gh auth login 질문 4단계 | `gh auth login` 실행, 4개 질문(GitHub.com/HTTPS/Yes/Login with a web browser) 답변까지 표시된 화면 캡처 → 코드 단계에서 Ctrl+C 중단(기존 인증 유지됨) |
| ch05-f05 | 5 | 일회용 코드 발급 | 위와 같은 세션에서 one-time code(XXXX-XXXX) 표시 화면 캡처 → 브라우저 진행 없이 Ctrl+C. 코드는 미사용 시 만료되므로 노출 무해(원하면 더미로 후처리) |
| ch08-f01 | 8 | npm create vite 프로젝트 생성 | 스크래치에서 `npm create vite@latest my-map -- --template vanilla` → "Scaffolding project..." 출력 캡처 (Claude Code 세션 컨텍스트가 필요하면 claude 안에서 실행 승인 장면으로) |
| ch12-f02 | 12 | Claude Code가 defaultPlaces.js 생성 | 스크래치 my-map에서 `claude` 실행 → 본문 프롬프트로 `src/defaultPlaces.js` 생성 요청 → 초록 diff 표시 화면 캡처(승인 전 화면이면 더 안전) |
| ch24-f02 | 24 | 커밋 전 git status | 스크래치 my-map에서 `.gitignore`(node_modules/dist/.env)+더미 `.env` 준비 → `git init; git status` → Untracked에 .env·node_modules 없는 목록 캡처 |
| ch24-f03 | 24 | 첫 커밋 완료 | 이어서 `git add .; git commit -m "첫 커밋: 나만의 지도 프로젝트 시작"` → root-commit 해시+files changed(그중 .env 없음) 캡처. 커미터는 위 fakehome 더미 설정 사용 |
| ch24-f04 | 24 | gh repo create 실행 결과 | 스크래치 my-map에서 `gh repo create my-map --public --source=. --push` → ✓ 3줄 캡처. **사전 확인: 본계정에 my-map 리포 존재 여부. 사후: ch24-f05/f06, ch25, ch26-f03 캡처 완료 전까지 유지 후 `gh repo delete` 여부를 사용자에게 확인** |
| ch24-f07 | 24 | git log --oneline | 스크래치 my-map에서 한국어 메시지 커밋 2~3개 추가 후 `git log --oneline` 캡처 |
| ch25-f01 | 25 | npm run build 결과 | 스크래치 my-map(또는 H:\YLBooks2\app 사본)에서 `npm run build` → "✓ built in ..."+dist 목록, 이어서 `ls dist` 출력 함께 캡처 |

## C. 공개 웹 캡처 — 16건

전제: 크롬. 비로그인 컷은 **시크릿 창**으로(개인 프로필·아바타 유입 차단). 로그인 필요 컷은 상태 명세+크롭/모자이크 표기.

| FIG id | 장 | 캡션 | 실행 방법 |
|---|---|---|---|
| ch03-f02 | 3 | gitforwindows.org 다운로드 페이지 | 시크릿 창 https://gitforwindows.org 첫 화면, Download 버튼 보이게 |
| ch04-f02 | 4 | claude.ai 가입 화면 | 시크릿 창 https://claude.ai → 로그인/가입 페이지(구글 버튼+이메일 입력란). 로그인 상태로 열면 개인 대화 노출되므로 반드시 시크릿 |
| ch05-f01 | 5 | GitHub 가입 페이지 | 시크릿 창 https://github.com/signup — 빈 입력 상태 |
| ch05-f06 | 5 | Device Activation 화면 | 시크릿 창 https://github.com/login/device — 주의: 비로그인 시 로그인 페이지로 우회될 수 있음 → 로그인 후엔 우상단 아바타 크롭 필요. 코드 미입력 상태 |
| ch05-f08 | 5 | 깃허브에 올라간 hello-github | 사전 작업: 스크래치에서 hello-github 리포 생성·push(B의 요령) → 본인 계정 리포 페이지 캡처. 사용자명·아바타 노출 — 저자 공개 계정이면 그대로, 아니면 크롭/모자이크. 사후 리포 정리 여부 확인 |
| ch07-f01 | 7 | 카카오 디벨로퍼스 첫 화면 | 시크릿 창 https://developers.kakao.com — 우상단 "로그인" 버튼 보이는 비로그인 상태 |
| ch07-f03 | 7 | 앱 생성 창 입력 상태 | **로그인 필요**: 콘솔 https://developers.kakao.com/console/app → + 앱 생성 → 이름 "나만의지도" 입력 상태. 저장 전 캡처 가능(실제 생성 불필요). 계정명 표시되면 크롭 |
| ch07-f06 | 7 | SDK 도메인에 localhost:5173 등록 | **로그인 필요**: 기존 앱의 JavaScript 키 수정 화면 → 도메인 목록에 http://localhost:5173 (기등록 상태) 캡처. **키 값 모자이크 필수** |
| ch24-f05 | 24 | 깃허브 my-map 저장소 | 사전 작업 ch24-f04 → github.com/<계정>/my-map 첫 화면(파일 목록+커밋 메시지+Public 배지). 계정명 노출 — 크롭 여지 |
| ch24-f06 | 24 | .env·node_modules 없는 파일 목록 | 같은 페이지 파일 목록 클로즈업 |
| ch25-f03 | 25 | Secrets에 VITE_KAKAO_JS_KEY 등록 | **로그인 필요**: my-map 리포 Settings→Secrets and variables→Actions→New repository secret, Name 입력+더미 값 일부. 실제 키 입력 금지(더미로 등록해도 무방) |
| ch25-f04 | 25 | Pages Source를 GitHub Actions로 | **로그인 필요**: Settings→Pages, Source 드롭다운 열린 상태(GitHub Actions 선택) |
| ch25-f05 | 25 | Actions build→deploy 초록 체크 | **사전 작업 큼**: my-map에 Pages 배포 워크플로(.github/workflows) push→실행 성공 필요. 성공 후 실행 상세 화면(배포 URL 링크 포함) 캡처 |
| ch25-f06 | 25 | 카카오 도메인에 github.io 추가 | **로그인 필요**(카카오): JS SDK 도메인에 localhost:5173+https://<계정>.github.io 두 줄 등록 상태. 키 모자이크 |
| ch25-f07 | 25 | github.io에서 동작하는 내 지도 | 사전 작업 ch25-f05 완료 후 https://<계정>.github.io/my-map/ 접속, 주소창 포함 창 캡처. 카카오 도메인 등록(ch25-f06)이 선행돼야 지도가 뜸 |
| ch26-f03 | 26 | 리포 첫 화면에 렌더링된 README | 사전 작업: my-map에 README(제목·배포 링크·스크린샷·기능 목록) push → 리포 메인+About 영역 캡처 |

## D. 설치 마법사·로컬 창 캡처 — 14건

설치 마법사는 **설치를 진행하지 않고 화면만 열람 후 Cancel** 가능 여부를 명세. 설치 파일은 스크래치에 다운로드.

| FIG id | 장 | 캡션 | 실행 방법 |
|---|---|---|---|
| ch02-f03 | 2 | Node.js 설치 마법사 Welcome | node-vXX-x64.msi 실행 → 첫 Welcome 화면 캡처 → Cancel. 주의: Node 기설치 PC에선 같은 버전 msi는 Repair/Remove 화면이 뜰 수 있음 → **더 최신 LTS msi**를 받으면 정상 Welcome 표시 |
| ch02-f04 | 2 | Custom Setup (npm·Add to PATH) | 같은 마법사에서 Next 진행(License 동의·경로 기본값) → Custom Setup 트리에서 npm package manager·Add to PATH 보이게 캡처 → Cancel. 설치 버튼(Install) 전까지는 시스템 무변경 |
| ch02-f05 | 2 | Tools for Native Modules 체크 해제 | 같은 진행에서 다음 화면, 체크박스 해제 상태 캡처 → Cancel |
| ch02-f06 | 2 | 설치 완료 화면 | **주의: Finish 화면은 실제 설치를 완료해야 표시.** 최신 LTS로 실제 업그레이드 설치를 감수하거나(권장: 사용자 확인 후), 불가 시 보류 처리 |
| ch02-f08 | 2 | 환경 변수 편집 창의 nodejs 경로 | `rundll32 sysdm.cpl,EditEnvironmentVariables` 실행 → Path 더블클릭 → `C:\Program Files\nodejs\` 선택(하이라이트) 상태 창 캡처. 무변경으로 취소 닫기 |
| ch03-f03 | 3 | Git 기본 에디터 Notepad 선택 | Git-*.exe 실행 → Next 수회 진행(Install 전 단계는 무변경) → "Choosing the default editor" 드롭다운에서 Notepad 선택 상태 캡처 → Cancel. 기설치 PC여도 인스톨러 재실행 무해(설치 안 누르면 됨) |
| ch03-f04 | 3 | PATH 환경 Recommended 선택 | 같은 진행의 "Adjusting your PATH environment"에서 가운데 옵션 선택 상태 캡처 → Cancel |
| ch06-f03 | 6 | Orca 첫 실행 화면 | Orca 실행 → 새 프로젝트 폴더(스크래치 my-map) 열기 → 카드 목록(비어있거나 main)+터미널 영역 창 전체 캡처 (computer-use 스킬로 창 캡처 가능) |
| ch06-f04 | 6 | 워크트리 터미널의 Claude Code | Orca에서 워크트리 카드 "마커 기능" 생성 → 터미널에서 claude 실행 → 환영 배너 보이는 상태 창 캡처 |
| ch06-f05 | 6 | 카드 3장 동시 진행 | 워크트리 카드 3장 생성(작업명 라벨), 한 카드 터미널에 에이전트 로그 출력 중 상태 연출 → 창 전체 캡처. 연출 시간 소요 큼 |
| ch08-f02 | 8 | my-map 폴더 구조 | 스크래치 my-map을 VS Code(또는 탐색기)로 열어 index.html·package.json·src 펼친 트리 캡처 |
| ch08-f05 | 8 | .env의 VITE_KAKAO_JS_KEY | 스크래치 my-map에 `.env` 생성, `VITE_KAKAO_JS_KEY=0123abcd...` **더미 키 한 줄**만 넣고 에디터 화면 캡처. 실키 절대 금지 |
| ch17-f06 | 17 | 내보내기 받은 my-map-places.json | A(ch17-f07) 연출 시 내려받은 파일을 메모장/VS Code로 열어 JSON 배열 필드(id/name/category/...) 보이게 캡처 |
| ch24-f01 | 24 | 점검 마친 .gitignore | 스크래치 my-map의 .gitignore(node_modules·dist·.env)를 에디터로 열고 .env 줄 강조(선택) 상태 캡처 |

## E. 다이어그램 제작 — 47건

캡션·지시문(steps)이 그대로 설계도다. HTML/SVG로 제작 → PNG 렌더 → `docs/images/chXX/`에 저장. 스타일 통일(플랫, 한글 라벨, 책 판형 가로 기준). 아래 "지시문 요약"은 원 지시문 축약.

| FIG id | 장 | 캡션 | 지시문 요약 |
|---|---|---|---|
| ch00-f07 | 0 | 이 책의 로드맵 | 등산로 지도: 1부(🔧)→2부(🗺️)→3부(📍)→4부(✨)→정상 5부(🚀) |
| ch01-f01 | 1 | 전통 코딩 vs 바이브코딩 순서 | 좌: 문법공부→문서→타이핑→에러→결과(긴 길) / 우: 말→AI코드→확인→수정(짧은 순환) |
| ch01-f02 | 1 | 저자의 워크플로 | 나(지휘자)→Orca 안 Claude Code 2~3개→Git(되돌리기)·GitHub CLI(업로드) 흐름 |
| ch01-f03 | 1 | 외울 것과 이해할 것 | 저울: 좌 "외울 필요 없음(문법·철자·옵션)"=AI가 들고, 우 "이해(데이터 흐름·구조·키 보안)"=사람, 우측으로 기움 |
| ch01-f04 | 1 | 바이브코딩 3원칙 | 순환 3아이콘: 바위 쪼개기(작게)·돋보기(확인)·반시계 화살표+안전벨트(되돌리기) |
| ch01-f05 | 1 | 도구 5종 역할 지도 | 공사장 비유: 기초 Node.js·작업자 Claude Code·현장사무소 Orca·타임머신 Git·물류 GitHub CLI |
| ch04-f06 | 4 | 프롬프트의 4요소 | 말풍선을 4조각 퍼즐로: 맥락·목표·제약·출력 형식 |
| ch06-f02 | 6 | 워크트리 개념도 | .git 원통 1개→폴더 3개(main/feature/review), 각 폴더에 에이전트, 점선 "침범 금지" |
| ch06-f06 | 6 | 작업 화면 배치도 | 와이드 모니터: 좌 Orca / 우 브라우저, "시킨다→확인한다→합친다" 루프 |
| ch09-f01 | 9 | SDK 불러오는 두 방법 | 좌 "HTML 직접"(키 노출 경고) vs 우 "동적 로드"(.env 금고→script 조립, 체크) |
| ch09-f02 | 9 | autoload=false 준비 순서 | 타임라인 4단계: script 삽입→다운로드(택배)→load() 호출(조립)→콜백(완성), "시점을 우리가 정함" |
| ch09-f03 | 9 | 위도·경도 개념 | 지구본 격자, 적도 위도0°·그리니치 경도0°, 서울시청(37.5665,126.978) 핀 |
| ch10-f02 | 10 | setCenter vs panTo | 좌 순간이동 핀 / 우 곡선 따라 미끄러지는 핀 |
| ch11-f03 | 11 | offset 기준점 | 좌 offset 없음(좌상단이 좌표에 붙음, 어긋남) / 우 offset(27,69)로 핀 끝이 좌표에 닿음, 픽셀 화살표 |
| ch12-f03 | 12 | categories.js 방사 구조 | 중앙 categories.js(4행)→마커 핀(11장)·필터 버튼(14장)·목록(18장), "한 곳만 고치면 전부" |
| ch13-f02 | 13 | yAnchor별 말풍선 위치 | 같은 좌표점에 yAnchor 0/0.5/1/1.35 네 경우 비교, 1.35 강조 |
| ch13-f03 | 13 | 말풍선 구조 분해도 | .bubble 안 .bubble-inner(이모지·이름·별점·×)+.bubble-tail 세로 배치 |
| ch13-f04 | 13 | border 삼각형 3단계 | ①4색 두꺼운 테두리 ②본체 0으로 삼각형 4개 ③위만 흰색, 아래 흰 삼각형 |
| ch13-f05 | 13 | "하나만 열기" 상태 흐름 | openOverlay null→A→(closeOverlay)→B→(×)→null 상태 전이도 |
| ch14-f02 | 14 | 단방향 데이터 흐름 | 버튼 클릭→currentFilter→filteredPlaces()→renderPlaces() 4박스 한 방향 화살표 |
| ch14-f06 | 14 | rerender 깔때기 | 필터·추가(16장)·삭제(19장) 세 입구→상태→rerender()→지도 화면 |
| ch15-f01 | 15 | SDK와 services 확장팩 | 큰 상자 SDK+플러그 상자 libraries=services, "&libraries=services" 꼬리표 |
| ch16-f01 | 16 | 입구는 둘, 문은 하나 | 검색 ＋버튼·지도 클릭 → openAddDialog → store.add() → 지도 |
| ch17-f02 | 17 | 책상(메모리)과 서랍(localStorage) | 좌 책상 서류(변수·증발) / 우 서랍(유지), save()/load() 양방향 화살표 |
| ch17-f04 | 17 | 직렬화 왕복 파이프라인 | stringify→문자열→setItem→서랍 / getItem→parse→배열 복원, 포장/개봉 라벨 |
| ch18-f01 | 18 | 하나의 데이터 두 화면 | store 원통→renderList()→목록 / →renderPlaces()→지도, 한 방향 |
| ch18-f06 | 18 | 구독 패턴 방송도 | 4입구→store.save() 확성기→rerender()·renderList() 구독자 |
| ch19-f01 | 19 | 상세 패널 4덩어리 | 카드 와이어프레임: 머리글·별점·textarea·[저장][삭제], 번호 말풍선 |
| ch19-f05 | 19 | XSS 원리 | 입력 폼→innerHTML 관문→빨강(escapeHtml 없음: alert 터짐)/초록(통과: 글자 그대로) |
| ch20-f04 | 20 | getCurrentPosition 두 갈래 | 순서도: 클릭→요청→분기(허용: 파란 점 / 차단: 토스트), 둘 다 앱 안 멈춤 |
| ch20-f07 | 20 | 보안 컨텍스트 문지방 | 문지기: https(자물쇠)·localhost(집) 통과, http(열린 자물쇠) ❌ |
| ch21-f01 | 21 | URL 해부도와 해시 | URL 부위별 색 구분, 해시만 "서버 전송 안 됨" ✕ |
| ch21-f03 | 21 | 정규식 해부도 | 정규식과 "#37.54444,127.05611,4" 부품 대응, m[1]~m[3] 라벨 |
| ch21-f04 | 21 | 공유의 왕복 | 브라우저 A 인코딩·복사→메신저→브라우저 B parseHash→같은 위치 |
| ch21-f06 | 21 | 공유되는 것/안 되는 것 | 카메라 상태 ✅ 이동, localStorage 장소 데이터 ❌ 잔류, 확장 아이디어 미니 분기 |
| ch22-f02 | 22 | 클러스터링 개념도 | 좌 핀 난립 / 우 숫자 원 "7","4"+낱개 1, "확대하면 낱개로" |
| ch22-f05 | 22 | 클러스터러 옵션 3형제 | averageCenter(무게중심)·minLevel(눈금자 6 기준)·minClusterSize(3부터 묶임) 3분할 |
| ch23-f03 | 23 | 미디어쿼리 개념 | HTML 하나→모니터(기본 CSS)/스마트폰(@media ≤640px), 브레이크포인트 점선 |
| ch25-f02 | 25 | base 설정이 필요한 이유 | 좌 base 없음: /assets 404 하얀 화면 / 우 base '/my-map/': 정상, 주소 블록 분해 |
| ch26-f01 | 26 | README 4단 구성 | 문서 카드 4구역: 스크린샷·기능·기술·실행법+방문자 말풍선 |
| ch26-f04 | 26 | 자랑하기 3단계 | 계단: 친구 링크→SNS→커뮤니티, 올라갈수록 피드백 커짐 |
| ch26-f05 | 26 | 다음 단계 네 갈래 길 | 현재 깃발→백엔드·로그인·사진·다른 API, 난이도 별 표기 |
| ch26-f06 | 26 | 이 책의 여정 지도 | 등산로 회고: 0장→5부 정상, 위기 푯말("회색 화면","403","핀 지옥") |
| ch27-f01 | 27 | 프롬프트 템플릿 사용법 | 뼈대 카드(4칸)→채운 말풍선, "베껴 쓰되 바꿔 쓴다" |
| ch27-f02 | 27 | 버그 리포트 3종 세트 | 벌레+돋보기 3개(증상·재현·기대), 에러 쪽지 든 사람 |
| ch27-f03 | 27 | 발사 전 점검판 | 체크보드: 4요소 큰 체크+3습관 작은 체크 |
| ch28-f01 | 28 | 고장 수리 3단계 | F12 확인→증상 표 대조→에러 전문 붙여넣기 흐름도 |

## F. 진짜 불가/보류 — 2건

| FIG id | 장 | 캡션 | 사유 |
|---|---|---|---|
| ch23-f07 | 23 | 실제 스마트폰에서 연 나만의 지도 | 실기기 촬영(스마트폰 실물+손가락 조작) — 에이전트 실행 불가, 저자 직접 촬영 필요. 촬영 조건: 같은 와이파이, `npm run dev -- --host`의 Network 주소 접속 |
| ch26-f02 | 26 | Win+Shift+S 캡처 도구로 앱 캡처 | 캡처 도구 오버레이 자체를 찍어야 하는 자기참조 컷 — 오버레이 활성 중엔 표준 캡처 입력이 도구에 잡아먹혀 통상 방법으론 불가. 우회안: OBS 화면 녹화 후 프레임 추출, 또는 두 번째 기기 촬영. 우회안 채택 시 D급으로 승격 가능 |

---

## 개수 요약

| 분류 | 건수 | 비고 |
|---|---|---|
| A. 앱 상태 캡처 | 53 | 이 중 [OS] 창 캡처 필요 12건, 합성 후처리 4건(ch10-f03·ch17-f01·ch21-f05·ch22-f06) |
| B. 터미널 캡처 | 16 | 파괴적 명령 전부 스크래치·격리 홈으로 재구성, 실이메일 노출 컷 격리 완료 |
| C. 공개 웹 캡처 | 16 | 로그인 필요 6건(카카오 3·GitHub 3), 크롭/모자이크 필수 표기, 사전 작업(리포·배포) 의존 6건 |
| D. 설치 마법사·로컬 창 | 14 | 마법사 6건은 Install 전 Cancel로 무변경 캡처 가능, 단 ch02-f06(완료 화면)은 실설치 필요 |
| E. 다이어그램 제작 | 47 | HTML/SVG → PNG 렌더, 지시문 그대로 설계도 사용 |
| F. 불가/보류 | 2 | 실기기 촬영 1, 자기참조 캡처 1(우회안 있음) |
| **합계** | **148** | images.yaml pending = 챕터 잔여 FIG 마커와 1:1 일치 |

## 권장 실행 순서

1. **E(47건) 먼저** — 외부 의존 0, 즉시 착수 가능하고 물량이 가장 큼. 스타일 가이드 1장 정한 뒤 일괄 생산.
2. **A(53건)** — dev 서버 하나 띄워 장 순서대로 연출. 상태를 쌓아가는 순서(리셋→ch09/11 최소 상태→ch12 기본 5곳→ch13~21 완성 상태→ch22 100개 주입→ch23 디바이스 모드)로 하면 리셋 횟수 최소화. [OS] 컷 12건은 같은 세션에서 몰아서.
3. **B(16건)** — 스크래치 3폴더 만들고 한 세션에 순서대로(ch02→03→04→05→08→12→24→25). ch24-f04(gh repo create)는 C의 사전 작업이므로 B 마지막에 실행.
4. **C(16건)** — 시크릿 창 6건 먼저(로그인 불필요), 이후 로그인 필요 컷(카카오·GitHub). ch25-f05/f07은 실제 Pages 배포 성공이 선행 조건이므로 마지막.
5. **D(14건)** — 로컬 창 8건(에디터·환경변수·Orca)은 아무 때나. 설치 마법사 6건은 인스톨러 다운로드 후 한 번에 진행하되, **ch02-f06은 실설치 수반이라 사용자 승인 후** 진행.
6. **F(2건)** — 사용자에게 실기기 촬영 요청 + ch26-f02 우회안(OBS) 채택 여부 확인.

리스크 항목(사용자 확인 필요): ch02-f06(Node 실설치/업그레이드), ch24-f04(공개 리포 실제 생성), ch25-f05·f07(실배포), 저자 계정명·아바타 노출 정책(C 전반), ch05-f05(일회용 코드 노출 — 만료로 무해하나 더미 후처리 권장).
