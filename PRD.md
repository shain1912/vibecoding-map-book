# PRD — 『바이브코딩으로 만드는 나만의 지도 웹』

## 한 줄 정의

AI 에이전트(Claude Code)와 페어 코딩하는 "바이브코딩" 방식으로, 카카오지도 API 기반 **나만의 장소 지도 웹앱**(맛집·여행·데이트 지도)을 밑바닥부터 만들어 GitHub Pages에 배포하기까지를 다루는 **200쪽 이상 튜토리얼 책**.

## 독자

- 코딩을 몰라도 AI에게 시켜서 결과물을 만들고 싶은 입문자
- 웹 기초는 없지만 "내 맛집 지도"를 갖고 싶은 사람
- 바이브코딩 워크플로(Claude Code, Orca, Git, GitHub CLI)를 익히고 싶은 사람

## 최종 산출물

1. **책**: mkdocs material 기반, 26장 + 부록 2편, 200쪽 이상 (장당 평균 8쪽)
2. **앱**: `app/` — Vite + 바닐라 JS + Kakao Maps JS SDK 지도 웹앱 (책 진도에 따라 장별 완성 단계 존재)
3. **이미지**: 스크린샷(브라우저/터미널 캡처) + 일러스트(Google Flow 생성) — FIG 마커 & images.yaml 규약

## 앱 기능 명세 (완성 기준)

- 카카오 지도 표시, 이동/줌/컨트롤
- 마커 + 커스텀 오버레이 말풍선
- 장소 데이터(JSON): 이름, 카테고리, 좌표, 별점, 메모
- 카테고리 필터 (🍜맛집 / ☕카페 / 🏝여행 / 💕데이트)
- 키워드 장소 검색 (services 라이브러리)
- 지도 클릭 + 검색으로 장소 추가
- localStorage 영속화 (내보내기/가져오기 JSON)
- 사이드바 장소 목록 + 상세 패널
- 내 위치(Geolocation), URL 상태 공유, 마커 클러스터러
- 반응형(모바일), GitHub Pages 배포

## 기술 결정

- **Vite + 바닐라 JS** (프레임워크 없음 — 입문자 대상, AI가 코드 주도)
- Kakao JS 키: `.env`의 `KAKAO_MAP_API` → Vite `VITE_KAKAO_JS_KEY`로 노출, `import.meta.env` 사용
- 플랫폼 등록: `http://localhost:5173` (발급 완료), 배포 시 Pages 도메인 추가
- kakao.maps.load() autoload=false 패턴 사용

## 제약

- 24시간 내 완성, 15분 자율 루프
- 사용자 피드백 불가 → 모든 결정은 추천답안(합리적 기본값)으로
- 검증: 자체 멀티에이전트 E2E + 외부 에이전트(codex/antigravity) 적대적 리뷰
- 포맷: FORMAT_SPEC.md (YLBooks 계승) 엄수
