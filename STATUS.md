# STATUS — 자율 루프 태스크보드

> 매 루프(15분)마다 이 파일을 읽고 갱신한다. 상태: `todo` / `doing` / `draft` / `review` / `done`

- 시작: 2026-09-02 08:30 (마감: 2026-09-03 08:30)
- 현재 단계: 1차 집필 (ch00–07 에이전트 가동 중)

## 인프라

- [x] 리포 초기화, PRD/PLAN/FORMAT_SPEC/WRITING_GUIDE
- [x] mkdocs.yml + index.md
- [x] app/ Vite 스캐폴드 + 지도 표시 확인 (M1–M6 코드 완성, E2E: 지도/마커/필터/검색 통과)
- [x] 첫 커밋 (e81a971)

## 앱 마일스톤

| 마일스톤 | 상태 |
|---|---|
| M1 스캐폴드 | done |
| M2 지도 | done (E2E ✅) |
| M3 마커/데이터 | done (E2E ✅) |
| M4 필터/검색 | done (E2E ✅) |
| M5 CRUD | done (E2E ✅ 추가·별점·삭제·localStorage 영속성) |
| M6 고급 | done (E2E ✅ 클러스터러 80마커·사이드바 접기 — relayout 버그 발견·수정) |
| M7 배포 | todo (책 서술은 완료, 실배포는 선택) |

## 원고 (chNN.md — 상태)

| 장 | 상태 | 장 | 상태 |
|---|---|---|---|
| ch00 | draft | ch14 | draft |
| ch01 | draft | ch15 | draft |
| ch02 | draft | ch16 | doing(agent) |
| ch03 | draft | ch17 | doing(agent) |
| ch04 | draft | ch18 | doing(agent) |
| ch05 | draft | ch19 | doing(agent) |
| ch06 | draft | ch20 | doing(agent) |
| ch07 | draft | ch21 | doing(agent) |
| ch08 | draft | ch22 | doing(agent) |
| ch09 | draft | ch23 | doing(agent) |
| ch10 | draft | ch24 | todo |
| ch11 | draft | ch25 | todo |
| ch12 | draft | ch26 | todo |
| ch13 | draft | ch27(부록A) | todo |
| — | — | ch28(부록B) | todo |

## 이미지

- [ ] images.yaml 생성 (FIG 스캔)
- [ ] 앱 스크린샷 캡처 (장별)
- [ ] 터미널 스크린샷 캡처
- [ ] 카카오 콘솔 스크린샷
- [ ] Google Flow 일러스트 생성

## 검증

- [x] 앱 E2E (지도·마커·필터·검색·CRUD·영속성·클러스터러·공유해시 방어)
- [x] 외부 적대적 리뷰 3종 완료: codex 앱코드(→수정 반영 e35c12c), codex 사실검증(치명1·중요7·경미5 → 수리 에이전트 반영 중), grok 독자경험(16~17장 연속성 치명 → 수리 에이전트 반영 중). gemini는 OAuth 미로그인으로 제외.
- [x] mkdocs build 통과 (1차)
- [x] 분량 38.2만자(코드 제외) ≈ 290쪽 — 200쪽 초과
- [ ] 수리 반영 후 최종 빌드·검산

## 진행 중 에이전트

- 이미지 3차 치환(ch14–18 yaml 재동기화 + 신규 캡처 배정)

## 루프 로그 (계속)

- 2026-09-02 09:40 — 적대적 리뷰 3종 전부 반영 완료(커밋 bac86ef): grok 연속성 치명(16~18장 store 전환 서사 대수술), codex 사실검증(라이브러리 순서 모순·프로토콜 규칙·configure-pages·preview), ch00/08 독자경험. 본문 40.3만자(≈310쪽). mkdocs 재빌드 통과. README.md 작성. 신규 앱 캡처 1장(카페필터+말풍선+상세).

## 루프 로그

- 2026-09-02 08:30 — 부트스트랩: 리포/문서/앱 완성, E2E(지도·필터·검색) 통과, 커밋 e81a971
- 2026-09-02 08:50 — ch00–07 초고 완료(커밋 f5d20ad), ch08–15 초고 완료(커밋 29b99d6), 앱 스크린샷 raw 4장 확보, ch16–23 에이전트 투입
- 2026-09-02 09:20 — **전 29장 초고 완성**(커밋 f063b2a, 본문 38.2만자≈290쪽). Flow 일러스트 6종, 카카오 콘솔 4장(키 블러), 터미널 5장(node/git/gh/claude/vite) 캡처. ch07 신 콘솔 사실 교정(커밋 360b68a). images.yaml 178항목/12치환, 2차 치환 진행 중. mkdocs build 통과. E2E: CRUD·영속성·클러스터러·검색·필터 전부 통과, relayout 버그 수정. 적대적 리뷰 3종(codex 앱코드/gemini 사실검증/grok 독자경험) 백그라운드 가동 중.
