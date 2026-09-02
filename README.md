# 바이브코딩으로 만드는 나만의 지도 웹

> AI 에이전트(Claude Code)에게 말로 시켜서, 카카오지도 API 기반 **나만의 맛집·여행·데이트 지도 웹앱**을 만들어 GitHub Pages에 공개하기까지 — 26장 + 부록 2편, 200쪽+ 튜토리얼 책.

![완성 앱](docs/images/raw/app-main.jpg)

## 구성

| 경로 | 내용 |
|---|---|
| `chapters/` | 원고 소스 (ch00~ch28 = 0~26장 + 부록 A·B) |
| `docs/` | mkdocs 입력 (chapters 복사본 + `images/`) |
| `app/` | 책에서 만드는 지도 웹앱 완성본 (Vite + 바닐라 JS + Kakao Maps SDK) |
| `images.yaml` | 그림 매니페스트 (FIG 마커 ↔ 캡처 상태) |
| `feedback/` | 적대적 리뷰 보고서 (codex 코드/사실 검증, grok 독자 경험) |
| `PRD.md` / `PLAN.md` / `WRITING_GUIDE.md` / `FORMAT_SPEC.md` | 기획·목차·집필 규약 |
| `STATUS.md` | 제작 태스크보드 & 루프 로그 |

## 책 보기

```bash
pip install mkdocs-material
mkdocs serve   # http://localhost:8000
```

## 앱 실행

```bash
cd app
npm install
# app/.env 에 VITE_KAKAO_JS_KEY=<카카오 JavaScript 키> 작성
# (developers.kakao.com → 앱 → 플랫폼 키 → JavaScript 키에 JS SDK 도메인 http://localhost:5173 등록)
npm run dev    # http://localhost:5173
```

### 앱 기능

카카오 지도 · 카테고리별 커스텀 SVG 마커(🍜☕🏝💕) · 커스텀 오버레이 말풍선 · 카테고리 필터 · 키워드 장소 검색(services) · 지도 클릭/검색으로 장소 추가 · 별점·메모 상세 패널 · localStorage 영속화 + JSON 내보내기/가져오기 · 내 위치(Geolocation) · URL 해시 공유 · 마커 클러스터러 · 반응형(모바일)

## 제작 방식

이 책과 앱은 Claude Code가 멀티에이전트(집필 29개 장 병렬, 이미지 파이프라인, 코드-원고 동기화)로 제작하고, codex·grok의 적대적 리뷰와 브라우저 E2E로 검증했다. 스크린샷은 Chrome 자동화·orca computer-use, 일러스트는 Google Flow로 생성했다.
