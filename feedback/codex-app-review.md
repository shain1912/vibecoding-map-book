node.exe : Reading additional input from stdin...
At C:\Users\seong\AppData\Roaming\npm\codex.ps1:24 char:5
+     & "node$exe"  "$basedir/node_modules/@openai/codex/bin/codex.js"  ...
+     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (Reading additional input from stdin...:String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
OpenAI Codex v0.148.0
--------
workdir: H:\YLBooks2
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a05f6c-70f7-7de3-b1d0-d55a5014afb1
--------
user
너는 적대적 코드 리뷰어다. H:\YLBooks2\app 의 카카오지도 웹앱(Vite+바닐라JS)을 리뷰하라. app/src/*.js, index.html, style.css를 전부 읽고: ①실제로 깨지는 버그(재현 시나리오 포함) ②XSS 등 보안 문제 ③카카오 Maps JS SDK API 오용 ④엣지케이스(빈 데이터, localStorage 실패, 좌표 경계) ⑤사소한 개선 순으로, 심각도 표기하여 한국어로 보고하라. 파일:줄번호를 명시하라. 확실하지 않은 것은 '추정'으로 표시하라.
hook: SessionStart
hook: SessionStart Completed
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
요청 범위의 파일을 모두 읽고, 실제 실행 경로를 따라가며 증거가 있는 문제부터 분류하겠습니다. SDK 관련 지적은 현재 공식 카카오 문서와 대조해 확정/추정을 구분하겠습니다.
hook: PreToolUse
hook: PreToolUse Completed
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command "Get-ChildItem -LiteralPath 'H:\\YLBooks2\\app\\src' -Filter '*.js' -File | Select-Object -ExpandProperty FullName; Get-Item -LiteralPath 'H:\\YLBooks2\\app\\index.html','H:\\YLBooks2\\app\\style.css' | Select-Object -ExpandProperty FullName" in H:\YLBooks2
 exited 1 in 628ms:
C:\Users\seong\Documents\WindowsPowerShell\profile.ps1 : Cannot dot-source this command because it was defined in a different language mode. To invoke this command without importing its contents, omit the '.' operator.
At line:1 char:1
+ . 'C:\Users\seong\Documents\WindowsPowerShell\profile.ps1'
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [profile.ps1], NotSupportedException
    + FullyQualifiedErrorId : DotSourceNotSupported,profile.ps1
 
C:\Users\seong\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 : Cannot dot-source this command because it was defined in a different language mode. To invoke this command without importing its contents, omit the '.' operator.
At line:1 char:1
+ . 'C:\Users\seong\Documents\WindowsPowerShell\Microsoft.PowerShell_pr ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [Microsoft.PowerShell_profile.ps1], NotSupportedException
    + FullyQualifiedErrorId : DotSourceNotSupported,Microsoft.PowerShell_profile.ps1
 
H:\YLBooks2\app\src\categories.js
H:\YLBooks2\app\src\defaultPlaces.js
H:\YLBooks2\app\src\detail.js
H:\YLBooks2\app\src\loader.js
H:\YLBooks2\app\src\main.js
H:\YLBooks2\app\src\mapView.js
H:\YLBooks2\app\src\search.js
H:\YLBooks2\app\src\share.js
H:\YLBooks2\app\src\sidebar.js
H:\YLBooks2\app\src\store.js
H:\YLBooks2\app\index.html
Get-Item : Cannot find path 'H:\YLBooks2\app\style.css' because it does not exist.
At line:2 char:113
+ ... y FullName; Get-Item -LiteralPath 'H:\YLBooks2\app\index.html','H:\YL ...
+                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (H:\YLBooks2\app\style.css:String) [Get-Item], ItemNotFoundException
    + FullyQualifiedErrorId : PathNotFound,Microsoft.PowerShell.Commands.GetItemCommand
 

hook: PostToolUse
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -Command "rg --files 'H:\\YLBooks2\\app' | rg '("'^|['"\\\\/])(style\\.css|["'^'"\\\\/]+\\.css)"'$'"'" in H:\YLBooks2
 exited 1 in 376ms:
hook: PostToolUse
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -Command "rg --files 'H:\\YLBooks2\\app'" in H:\YLBooks2
 succeeded in 239ms:
H:\YLBooks2\app\package.json
H:\YLBooks2\app\package-lock.json
H:\YLBooks2\app\src\categories.js
H:\YLBooks2\app\src\main.js
H:\YLBooks2\app\src\defaultPlaces.js
H:\YLBooks2\app\src\loader.js
H:\YLBooks2\app\src\detail.js
H:\YLBooks2\app\index.html
H:\YLBooks2\app\src\style.css
H:\YLBooks2\app\src\store.js
H:\YLBooks2\app\src\sidebar.js
H:\YLBooks2\app\src\share.js
H:\YLBooks2\app\src\search.js
H:\YLBooks2\app\src\mapView.js

hook: PostToolUse
hook: PostToolUse Completed
hook: PreToolUse
hook: PreToolUse Completed
exec
"C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -Command '$files = @(Get-ChildItem -LiteralPath '"'H:\\YLBooks2\\app\\src' -Filter '*.js' -File | Sort-Object Name) + @(Get-Item -LiteralPath 'H:\\YLBooks2\\app\\index.html','H:\\YLBooks2\\app\\src\\style.css'); foreach ("'$f in $files) { Write-Output ('"'===== ' + "'$f.F
ullName + '"' ====='); "'$n=0; Get-Content -LiteralPath $f.FullName -Encoding UTF8 | ForEach-Object { $n++; '"'{0,5}: {1}' -f "'$n, $_ } }' in H:\YLBooks2
 succeeded in 652ms:
===== H:\YLBooks2\app\src\categories.js =====
    1: // 카테고리 정의 — 지도 전체에서 이 한 곳만 고치면 된다.
    2: export const CATEGORIES = {
    3:   food:   { label: '맛집',   emoji: '🍜', color: '#e74c3c' },
    4:   cafe:   { label: '카페',   emoji: '☕', color: '#8e5a2d' },
    5:   travel: { label: '여행',   emoji: '🏝', color: '#1e90ff' },
    6:   date:   { label: '데이트', emoji: '💕', color: '#e84393' },
    7: };
    8: 
    9: export function categoryOf(id) {
   10:   return CATEGORIES[id] ?? { label: '기타', emoji: '📍', color: '#555' };
   11: }
===== H:\YLBooks2\app\src\defaultPlaces.js =====
    1: // 처음 실행할 때 보여줄 예시 장소들 (서울 유명 스팟)
    2: export const DEFAULT_PLACES = [
    3:   {
    4:     id: 'seed01',
    5:     name: '광장시장',
    6:     category: 'food',
    7:     lat: 37.5701,
    8:     lng: 126.9996,
    9:     rating: 5,
   10:     memo: '빈대떡과 마약김밥. 주말엔 사람이 아주 많다.',
   11:   },
   12:   {
   13:     id: 'seed02',
   14:     name: '성수동 카페거리',
   15:     category: 'cafe',
   16:     lat: 37.5446,
   17:     lng: 127.0562,
   18:     rating: 4,
   19:     memo: '공장 개조 카페 투어. 평일 오후 추천.',
   20:   },
   21:   {
   22:     id: 'seed03',
   23:     name: '경복궁',
   24:     category: 'travel',
   25:     lat: 37.5796,
   26:     lng: 126.977,
   27:     rating: 5,
   28:     memo: '한복 입으면 무료 입장. 수문장 교대식 10시/14시.',
   29:   },
   30:   {
   31:     id: 'seed04',
   32:     name: '남산서울타워',
   33:     category: 'date',
   34:     lat: 37.5512,
   35:     lng: 126.9882,
   36:     rating: 4,
   37:     memo: '야경 명소. 케이블카 타고 올라가기.',
   38:   },
   39:   {
   40:     id: 'seed05',
   41:     name: '망원한강공원',
   42:     category: 'date',
   43:     lat: 37.5546,
   44:     lng: 126.8957,
   45:     rating: 4,
   46:     memo: '라면 끓여 먹기 좋은 곳. 노을이 예쁘다.',
   47:   },
   48: ];
===== H:\YLBooks2\app\src\detail.js =====
    1: // 상세 패널 — 별점·메모 편집, 삭제
    2: import { store } from './store.js';
    3: import { categoryOf } from './categories.js';
    4: import { escapeHtml } from './mapView.js';
    5: import { toast } from './sidebar.js';
    6: 
    7: let currentId = null;
    8: 
    9: export function openDetail(id) {
   10:   const place = store.get(id);
   11:   if (!place) return;
   12:   currentId = id;
   13:   const panel = document.getElementById('detail-panel');
   14:   const cat = categoryOf(place.category);
   15:   panel.hidden = false;
   16:   panel.innerHTML = `
   17:     <header>
   18:       <h2>${cat.emoji} ${escapeHtml(place.name)}</h2>
   19:       <button id="detail-close" title="닫기">×</button>
   20:     </header>
   21:     <p class="detail-cat" style="color:${cat.color}">${cat.label}</p>
   22:     <div class="detail-stars" id="detail-stars">
   23:       ${[1, 2, 3, 4, 5]
   24:         .map((n) => `<button class="star ${n <= (place.rating || 0) ? 'on' : ''}" data-n="${n}">★</button>`)
   25:         .join('')}
   26:     </div>
   27:     <textarea id="detail-memo" rows="4" placeholder="메모를 남겨 보세요">${escapeHtml(place.memo || '')}</textarea>
   28:     <div class="detail-actions">
   29:       <button id="detail-save" class="primary">저장</button>
   30:       <button id="detail-delete" class="danger">삭제</button>
   31:     </div>`;
   32: 
   33:   panel.querySelector('#detail-close').addEventListener('click', closeDetail);
   34:   panel.querySelectorAll('.star').forEach((btn) => {
   35:     btn.addEventListener('click', () => {
   36:       const n = Number(btn.dataset.n);
   37:       store.update(id, { rating: n });
   38:       openDetail(id); // 다시 그려서 별 반영
   39:     });
   40:   });
   41:   panel.querySelector('#detail-save').addEventListener('click', () => {
   42:     store.update(id, { memo: panel.querySelector('#detail-memo').value });
   43:     toast('저장했습니다.');
   44:   });
   45:   panel.querySelector('#detail-delete').addEventListener('click', () => {
   46:     if (confirm(`'${place.name}'을(를) 삭제할까요?`)) {
   47:       store.remove(id);
   48:       closeDetail();
   49:       toast('삭제했습니다.');
   50:     }
   51:   });
   52: }
   53: 
   54: export function closeDetail() {
   55:   const panel = document.getElementById('detail-panel');
   56:   panel.hidden = true;
   57:   currentId = null;
   58: }
   59: 
   60: export function getOpenDetailId() {
   61:   return currentId;
   62: }
===== H:\YLBooks2\app\src\loader.js =====
    1: // 카카오 지도 SDK를 동적으로 불러오는 모듈
    2: // autoload=false로 받아서 kakao.maps.load() 콜백 안에서 지도를 만든다.
    3: export function loadKakaoSdk() {
    4:   return new Promise((resolve, reject) => {
    5:     const key = import.meta.env.VITE_KAKAO_JS_KEY;
    6:     if (!key) {
    7:       reject(new Error('VITE_KAKAO_JS_KEY가 .env에 없습니다.'));
    8:       return;
    9:     }
   10:     const script = document.createElement('script');
   11:     script.src =
   12:       `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${key}` +
   13:       `&autoload=false&libraries=services,clusterer`;
   14:     script.onload = () => kakao.maps.load(() => resolve(kakao));
   15:     script.onerror = () => reject(new Error('카카오 SDK 로드 실패 — 키/도메인 확인'));
   16:     document.head.appendChild(script);
   17:   });
   18: }
===== H:\YLBooks2\app\src\main.js =====
    1: // 앱 진입점 — 모든 모듈을 조립한다
    2: import './style.css';
    3: import { loadKakaoSdk } from './loader.js';
    4: import { store } from './store.js';
    5: import {
    6:   createMap, renderPlaces, focusPlace, setMarkerClickHandler,
    7:   showMyLocation, getMap,
    8: } from './mapView.js';
    9: import { initSidebar, filteredPlaces, toast } from './sidebar.js';
   10: import { initSearch, openAddDialog } from './search.js';
   11: import { openDetail } from './detail.js';
   12: import { initShare, parseHash } from './share.js';
   13: 
   14: async function main() {
   15:   try {
   16:     await loadKakaoSdk();
   17:   } catch (e) {
   18:     document.getElementById('map').innerHTML =
   19:       `<p class="sdk-error">지도를 불러오지 못했습니다.<br>${e.message}</p>`;
   20:     return;
   21:   }
   22: 
   23:   // 공유 링크(#lat,lng,level)로 들어왔으면 그 위치에서 시작
   24:   const hashState = parseHash();
   25:   const map = createMap(
   26:     document.getElementById('map'),
   27:     hashState ?? { lat: 37.5665, lng: 126.978 },
   28:     hashState?.level ?? 7
   29:   );
   30:   window.__map = map; // 사이드바 접기에서 resize 트리거용
   31: 
   32:   const rerender = () => renderPlaces(filteredPlaces());
   33: 
   34:   setMarkerClickHandler((id) => openDetail(id));
   35:   initSidebar({
   36:     onSelectPlace: (id) => {
   37:       const p = store.get(id);
   38:       if (p) {
   39:         focusPlace(p);
   40:         openDetail(id);
   41:       }
   42:     },
   43:     onFilter: rerender,
   44:   });
   45:   initSearch();
   46:   initShare();
   47:   store.subscribe(rerender);
   48:   rerender();
   49: 
   50:   // 지도 클릭 → 장소 추가
   51:   kakao.maps.event.addListener(map, 'click', (e) => {
   52:     openAddDialog({ lat: e.latLng.getLat(), lng: e.latLng.getLng() });
   53:   });
   54: 
   55:   // 내 위치
   56:   document.getElementById('btn-mylocation').addEventListener('click', () => {
   57:     if (!navigator.geolocation) {
   58:       toast('이 브라우저는 위치를 지원하지 않습니다.');
   59:       return;
   60:     }
   61:     navigator.geolocation.getCurrentPosition(
   62:       (pos) => showMyLocation(pos.coords.latitude, pos.coords.longitude),
   63:       () => toast('위치 권한이 거부되었습니다.')
   64:     );
   65:   });
   66: }
   67: 
   68: main();
===== H:\YLBooks2\app\src\mapView.js =====
    1: // 지도 담당 모듈 — 지도 생성, 마커/오버레이/클러스터러 렌더링
    2: import { categoryOf } from './categories.js';
    3: 
    4: let map;
    5: let clusterer;
    6: let markers = []; // { marker, overlay, place }
    7: let onMarkerClick = () => {};
    8: 
    9: export function createMap(container, center = { lat: 37.5665, lng: 126.978 }, level = 7) {
   10:   map = new kakao.maps.Map(container, {
   11:     center: new kakao.maps.LatLng(center.lat, center.lng),
   12:     level,
   13:   });
   14:   map.addControl(new kakao.maps.MapTypeControl(), kakao.maps.ControlPosition.TOPRIGHT);
   15:   map.addControl(new kakao.maps.ZoomControl(), kakao.maps.ControlPosition.RIGHT);
   16: 
   17:   clusterer = new kakao.maps.MarkerClusterer({
   18:     map,
   19:     averageCenter: true,
   20:     minLevel: 6,
   21:     minClusterSize: 3,
   22:   });
   23:   return map;
   24: }
   25: 
   26: export function getMap() {
   27:   return map;
   28: }
   29: 
   30: export function setMarkerClickHandler(fn) {
   31:   onMarkerClick = fn;
   32: }
   33: 
   34: function markerImageFor(category) {
   35:   const { emoji, color } = categoryOf(category);
   36:   const svg = `
   37:     <svg xmlns="http://www.w3.org/2000/svg" width="36" height="46" viewBox="0 0 36 46">
   38:       <path d="M18 0C8 0 0 8 0 18c0 12 18 28 18 28s18-16 18-28C36 8 28 0 18 0z" fill="${color}"/>
   39:       <circle cx="18" cy="17" r="12" fill="white"/>
   40:       <text x="18" y="22" font-size="14" text-anchor="middle">${emoji}</text>
   41:     </svg>`;
   42:   const url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
   43:   return new kakao.maps.MarkerImage(url, new kakao.maps.Size(36, 46), {
   44:     offset: new kakao.maps.Point(18, 46),
   45:   });
   46: }
   47: 
   48: function overlayContent(place) {
   49:   const cat = categoryOf(place.category);
   50:   const stars = '★'.repeat(place.rating || 0) + '☆'.repeat(5 - (place.rating || 0));
   51:   const el = document.createElement('div');
   52:   el.className = 'bubble';
   53:   el.innerHTML = `
   54:     <div class="bubble-inner">
   55:       <strong>${cat.emoji} ${escapeHtml(place.name)}</strong>
   56:       <span class="bubble-stars">${stars}</span>
   57:       <button class="bubble-close" title="닫기">×</button>
   58:     </div>
   59:     <div class="bubble-tail"></div>`;
   60:   return el;
   61: }
   62: 
   63: export function escapeHtml(s = '') {
   64:   return s.replace(/[&<>"']/g, (c) => ({
   65:     '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
   66:   })[c]);
   67: }
   68: 
   69: let openOverlay = null;
   70: 
   71: export function closeOverlay() {
   72:   if (openOverlay) {
   73:     openOverlay.setMap(null);
   74:     openOverlay = null;
   75:   }
   76: }
   77: 
   78: export function renderPlaces(places) {
   79:   closeOverlay();
   80:   clusterer.removeMarkers(markers.map((m) => m.marker));
   81:   markers = [];
   82: 
   83:   for (const place of places) {
   84:     const pos = new kakao.maps.LatLng(place.lat, place.lng);
   85:     const marker = new kakao.maps.Marker({
   86:       position: pos,
   87:       image: markerImageFor(place.category),
   88:       title: place.name,
   89:     });
   90: 
   91:     const el = overlayContent(place);
   92:     const overlay = new kakao.maps.CustomOverlay({
   93:       content: el,
   94:       position: pos,
   95:       yAnchor: 1.35,
   96:       zIndex: 10,
   97:     });
   98:     el.querySelector('.bubble-close').addEventListener('click', (e) => {
   99:       e.stopPropagation();
  100:       closeOverlay();
  101:     });
  102:     el.querySelector('.bubble-inner').addEventListener('click', () => onMarkerClick(place.id));
  103: 
  104:     kakao.maps.event.addListener(marker, 'click', () => {
  105:       closeOverlay();
  106:       overlay.setMap(map);
  107:       openOverlay = overlay;
  108:       onMarkerClick(place.id);
  109:     });
  110: 
  111:     markers.push({ marker, overlay, place });
  112:   }
  113:   clusterer.addMarkers(markers.map((m) => m.marker));
  114: }
  115: 
  116: export function focusPlace(place, level = 4) {
  117:   const pos = new kakao.maps.LatLng(place.lat, place.lng);
  118:   map.setLevel(level);
  119:   map.panTo(pos);
  120:   const entry = markers.find((m) => m.place.id === place.id);
  121:   if (entry) {
  122:     closeOverlay();
  123:     entry.overlay.setMap(map);
  124:     openOverlay = entry.overlay;
  125:   }
  126: }
  127: 
  128: let myLocationMarker = null;
  129: 
  130: export function showMyLocation(lat, lng) {
  131:   const pos = new kakao.maps.LatLng(lat, lng);
  132:   if (!myLocationMarker) {
  133:     const el = document.createElement('div');
  134:     el.className = 'my-location-dot';
  135:     myLocationMarker = new kakao.maps.CustomOverlay({ content: el, position: pos, zIndex: 5 });
  136:   }
  137:   myLocationMarker.setPosition(pos);
  138:   myLocationMarker.setMap(map);
  139:   map.setLevel(4);
  140:   map.panTo(pos);
  141: }
===== H:\YLBooks2\app\src\search.js =====
    1: // 키워드 장소 검색 — kakao.maps.services.Places
    2: import { store } from './store.js';
    3: import { escapeHtml, getMap } from './mapView.js';
    4: import { toast } from './sidebar.js';
    5: 
    6: let ps;
    7: 
    8: export function initSearch() {
    9:   ps = new kakao.maps.services.Places();
   10:   const input = document.getElementById('search-input');
   11:   const btn = document.getElementById('btn-search');
   12:   const resultsEl = document.getElementById('search-results');
   13: 
   14:   const run = () => {
   15:     const q = input.value.trim();
   16:     if (!q) return;
   17:     ps.keywordSearch(q, (data, status) => {
   18:       if (status !== kakao.maps.services.Status.OK) {
   19:         toast('검색 결과가 없습니다.');
   20:         resultsEl.hidden = true;
   21:         return;
   22:       }
   23:       renderResults(data.slice(0, 7));
   24:     });
   25:   };
   26: 
   27:   btn.addEventListener('click', run);
   28:   input.addEventListener('keydown', (e) => {
   29:     if (e.key === 'Enter') run();
   30:   });
   31: 
   32:   function renderResults(items) {
   33:     resultsEl.hidden = false;
   34:     resultsEl.innerHTML = items
   35:       .map(
   36:         (item, i) => `
   37:         <li class="search-item" data-i="${i}">
   38:           <span class="search-info">
   39:             <strong>${escapeHtml(item.place_name)}</strong>
   40:             <small>${escapeHtml(item.road_address_name || item.address_name || '')}</small>
   41:           </span>
   42:           <button class="btn-add" title="내 지도에 추가">＋</button>
   43:         </li>`
   44:       )
   45:       .join('');
   46: 
   47:     resultsEl.querySelectorAll('.search-item').forEach((li) => {
   48:       const item = items[Number(li.dataset.i)];
   49:       const lat = Number(item.y);
   50:       const lng = Number(item.x);
   51:       // 결과 클릭 → 지도 이동
   52:       li.querySelector('.search-info').addEventListener('click', () => {
   53:         getMap().setLevel(3);
   54:         getMap().panTo(new kakao.maps.LatLng(lat, lng));
   55:       });
   56:       // ＋ 클릭 → 내 지도에 추가
   57:       li.querySelector('.btn-add').addEventListener('click', (e) => {
   58:         e.stopPropagation();
   59:         openAddDialog({ name: item.place_name, lat, lng });
   60:         resultsEl.hidden = true;
   61:       });
   62:     });
   63:   }
   64: }
   65: 
   66: // 장소 추가 폼 (검색 추가 + 지도 클릭 추가 공용)
   67: export function openAddDialog({ name = '', lat, lng }) {
   68:   closeAddDialog();
   69:   const wrap = document.createElement('div');
   70:   wrap.id = 'add-dialog';
   71:   wrap.innerHTML = `
   72:     <div class="dialog-card">
   73:       <h2>장소 추가</h2>
   74:       <label>이름 <input id="add-name" value="${escapeHtml(name)}" placeholder="장소 이름" /></label>
   75:       <label>카테고리
   76:         <select id="add-category">
   77:           <option value="food">🍜 맛집</option>
   78:           <option value="cafe">☕ 카페</option>
   79:           <option value="travel">🏝 여행</option>
   80:           <option value="date">💕 데이트</option>
   81:         </select>
   82:       </label>
   83:       <label>메모 <textarea id="add-memo" rows="2" placeholder="한 줄 메모"></textarea></label>
   84:       <div class="dialog-actions">
   85:         <button id="add-cancel">취소</button>
   86:         <button id="add-ok" class="primary">추가</button>
   87:       </div>
   88:     </div>`;
   89:   document.body.appendChild(wrap);
   90:   wrap.querySelector('#add-cancel').addEventListener('click', closeAddDialog);
   91:   wrap.querySelector('#add-ok').addEventListener('click', () => {
   92:     const nameVal = wrap.querySelector('#add-name').value.trim();
   93:     if (!nameVal) {
   94:       toast('이름을 입력하세요.');
   95:       return;
   96:     }
   97:     store.add({
   98:       name: nameVal,
   99:       category: wrap.querySelector('#add-category').value,
  100:       memo: wrap.querySelector('#add-memo').value.trim(),
  101:       lat,
  102:       lng,
  103:     });
  104:     toast('내 지도에 추가했습니다!');
  105:     closeAddDialog();
  106:   });
  107: }
  108: 
  109: export function closeAddDialog() {
  110:   document.getElementById('add-dialog')?.remove();
  111: }
===== H:\YLBooks2\app\src\share.js =====
    1: // URL 해시로 지도 상태 공유 — #lat,lng,level
    2: import { getMap } from './mapView.js';
    3: import { toast } from './sidebar.js';
    4: 
    5: export function initShare() {
    6:   document.getElementById('btn-share').addEventListener('click', async () => {
    7:     const map = getMap();
    8:     const c = map.getCenter();
    9:     const hash = `#${c.getLat().toFixed(5)},${c.getLng().toFixed(5)},${map.getLevel()}`;
   10:     const url = location.origin + location.pathname + hash;
   11:     history.replaceState(null, '', hash);
   12:     try {
   13:       await navigator.clipboard.writeText(url);
   14:       toast('지도 링크를 복사했습니다!');
   15:     } catch {
   16:       toast('복사 실패 — 주소창의 URL을 직접 복사하세요.');
   17:     }
   18:   });
   19: }
   20: 
   21: // 접속 시 해시가 있으면 그 위치로 시작
   22: export function parseHash() {
   23:   const m = location.hash.match(/^#(-?[\d.]+),(-?[\d.]+),(\d+)$/);
   24:   if (!m) return null;
   25:   return { lat: Number(m[1]), lng: Number(m[2]), level: Number(m[3]) };
   26: }
===== H:\YLBooks2\app\src\sidebar.js =====
    1: // 사이드바 — 장소 목록, 카테고리 필터, 내보내기/가져오기
    2: import { store } from './store.js';
    3: import { categoryOf } from './categories.js';
    4: import { escapeHtml } from './mapView.js';
    5: 
    6: let currentFilter = 'all';
    7: let onSelect = () => {};
    8: let onFilterChange = () => {};
    9: 
   10: export function getFilter() {
   11:   return currentFilter;
   12: }
   13: 
   14: export function filteredPlaces() {
   15:   const all = store.all();
   16:   return currentFilter === 'all' ? all : all.filter((p) => p.category === currentFilter);
   17: }
   18: 
   19: export function initSidebar({ onSelectPlace, onFilter }) {
   20:   onSelect = onSelectPlace;
   21:   onFilterChange = onFilter;
   22: 
   23:   document.querySelectorAll('.filter-btn').forEach((btn) => {
   24:     btn.addEventListener('click', () => {
   25:       currentFilter = btn.dataset.category;
   26:       document.querySelectorAll('.filter-btn').forEach((b) => b.classList.toggle('active', b === btn));
   27:       renderList();
   28:       onFilterChange();
   29:     });
   30:   });
   31: 
   32:   document.getElementById('btn-collapse').addEventListener('click', () => toggleSidebar(false));
   33:   document.getElementById('btn-expand').addEventListener('click', () => toggleSidebar(true));
   34: 
   35:   // 내보내기 — JSON 파일 다운로드
   36:   document.getElementById('btn-export').addEventListener('click', () => {
   37:     const blob = new Blob([store.exportJson()], { type: 'application/json' });
   38:     const a = document.createElement('a');
   39:     a.href = URL.createObjectURL(blob);
   40:     a.download = 'my-map-places.json';
   41:     a.click();
   42:     URL.revokeObjectURL(a.href);
   43:   });
   44: 
   45:   // 가져오기 — JSON 파일 업로드
   46:   const fileInput = document.getElementById('import-file');
   47:   document.getElementById('btn-import').addEventListener('click', () => fileInput.click());
   48:   fileInput.addEventListener('change', async () => {
   49:     const file = fileInput.files[0];
   50:     if (!file) return;
   51:     try {
   52:       store.importJson(await file.text());
   53:       toast('가져오기 완료!');
   54:     } catch (e) {
   55:       toast('가져오기 실패: ' + e.message);
   56:     }
   57:     fileInput.value = '';
   58:   });
   59: 
   60:   store.subscribe(renderList);
   61:   renderList();
   62: }
   63: 
   64: export function toggleSidebar(open) {
   65:   document.getElementById('sidebar').classList.toggle('collapsed', !open);
   66:   document.getElementById('btn-expand').hidden = open;
   67:   // 지도 크기가 변하므로 카카오 지도에 알려준다 (CSS 트랜지션 0.25s가 끝난 뒤)
   68:   setTimeout(() => window.__map.relayout(), 300);
   69: }
   70: 
   71: export function renderList() {
   72:   const ul = document.getElementById('place-list');
   73:   const places = filteredPlaces();
   74:   if (places.length === 0) {
   75:     ul.innerHTML = '<li class="empty">장소가 없습니다.<br>검색하거나 지도를 클릭해 추가해 보세요!</li>';
   76:     return;
   77:   }
   78:   ul.innerHTML = places
   79:     .map((p) => {
   80:       const cat = categoryOf(p.category);
   81:       const stars = '★'.repeat(p.rating || 0);
   82:       return `
   83:         <li class="place-item" data-id="${p.id}">
   84:           <span class="place-emoji" style="background:${cat.color}22">${cat.emoji}</span>
   85:           <span class="place-info">
   86:             <strong>${escapeHtml(p.name)}</strong>
   87:             <small>${cat.label} ${stars ? '· ' + stars : ''}</small>
   88:           </span>
   89:         </li>`;
   90:     })
   91:     .join('');
   92:   ul.querySelectorAll('.place-item').forEach((li) => {
   93:     li.addEventListener('click', () => onSelect(li.dataset.id));
   94:   });
   95: }
   96: 
   97: let toastTimer;
   98: export function toast(msg) {
   99:   const el = document.getElementById('toast');
  100:   el.textContent = msg;
  101:   el.hidden = false;
  102:   clearTimeout(toastTimer);
  103:   toastTimer = setTimeout(() => (el.hidden = true), 2200);
  104: }
===== H:\YLBooks2\app\src\store.js =====
    1: // 장소 데이터 저장소 — localStorage 영속화 + 구독(pub/sub)
    2: import { DEFAULT_PLACES } from './defaultPlaces.js';
    3: 
    4: const STORAGE_KEY = 'my-map-places-v1';
    5: const listeners = [];
    6: 
    7: let places = load();
    8: 
    9: function load() {
   10:   try {
   11:     const raw = localStorage.getItem(STORAGE_KEY);
   12:     if (raw) return JSON.parse(raw);
   13:   } catch (e) {
   14:     console.warn('저장 데이터를 읽지 못해 기본 데이터로 시작합니다.', e);
   15:   }
   16:   return structuredClone(DEFAULT_PLACES);
   17: }
   18: 
   19: function save() {
   20:   try {
   21:     localStorage.setItem(STORAGE_KEY, JSON.stringify(places));
   22:   } catch (e) {
   23:     console.warn('localStorage 저장 실패', e);
   24:   }
   25:   listeners.forEach((fn) => fn(places));
   26: }
   27: 
   28: export const store = {
   29:   all() {
   30:     return places;
   31:   },
   32:   get(id) {
   33:     return places.find((p) => p.id === id);
   34:   },
   35:   add(place) {
   36:     const id = 'p' + Date.now().toString(36);
   37:     const item = { id, rating: 0, memo: '', ...place };
   38:     places.push(item);
   39:     save();
   40:     return item;
   41:   },
   42:   update(id, patch) {
   43:     const p = this.get(id);
   44:     if (!p) return;
   45:     Object.assign(p, patch);
   46:     save();
   47:   },
   48:   remove(id) {
   49:     places = places.filter((p) => p.id !== id);
   50:     save();
   51:   },
   52:   replaceAll(next) {
   53:     places = next;
   54:     save();
   55:   },
   56:   subscribe(fn) {
   57:     listeners.push(fn);
   58:   },
   59:   exportJson() {
   60:     return JSON.stringify(places, null, 2);
   61:   },
   62:   importJson(text) {
   63:     const data = JSON.parse(text);
   64:     if (!Array.isArray(data)) throw new Error('배열(JSON)이 아닙니다.');
   65:     for (const p of data) {
   66:       if (typeof p.name !== 'string' || typeof p.lat !== 'number' || typeof p.lng !== 'number') {
   67:         throw new Error('name/lat/lng 형식이 올바르지 않은 항목이 있습니다.');
   68:       }
   69:     }
   70:     places = data;
   71:     save();
   72:   },
   73: };
===== H:\YLBooks2\app\index.html =====
    1: <!DOCTYPE html>
    2: <html lang="ko">
    3:   <head>
    4:     <meta charset="UTF-8" />
    5:     <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    6:     <title>나만의 지도</title>
    7:     <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📍</text></svg>" />
    8:   </head>
    9:   <body>
   10:     <div id="app">
   11:       <aside id="sidebar">
   12:         <header id="sidebar-header">
   13:           <h1>📍 나만의 지도</h1>
   14:           <button id="btn-collapse" title="사이드바 접기">◀</button>
   15:         </header>
   16: 
   17:         <div id="search-box">
   18:           <input id="search-input" type="text" placeholder="장소 검색 (예: 성수동 카페)" />
   19:           <button id="btn-search">🔍</button>
   20:         </div>
   21:         <ul id="search-results" hidden></ul>
   22: 
   23:         <nav id="filter-bar">
   24:           <button class="filter-btn active" data-category="all">전체</button>
   25:           <button class="filter-btn" data-category="food">🍜 맛집</button>
   26:           <button class="filter-btn" data-category="cafe">☕ 카페</button>
   27:           <button class="filter-btn" data-category="travel">🏝 여행</button>
   28:           <button class="filter-btn" data-category="date">💕 데이트</button>
   29:         </nav>
   30: 
   31:         <ul id="place-list"></ul>
   32: 
   33:         <footer id="sidebar-footer">
   34:           <button id="btn-export">내보내기</button>
   35:           <button id="btn-import">가져오기</button>
   36:           <input id="import-file" type="file" accept=".json" hidden />
   37:         </footer>
   38:       </aside>
   39: 
   40:       <main id="map-wrap">
   41:         <div id="map"></div>
   42:         <button id="btn-expand" title="사이드바 열기" hidden>▶</button>
   43:         <button id="btn-mylocation" title="내 위치">🧭</button>
   44:         <button id="btn-share" title="지도 공유">🔗</button>
   45:       </main>
   46: 
   47:       <section id="detail-panel" hidden></section>
   48:       <div id="toast" hidden></div>
   49:     </div>
   50:     <script type="module" src="/src/main.js"></script>
   51:   </body>
   52: </html>
===== H:\YLBooks2\app\src\style.css =====
    1: * { box-sizing: border-box; margin: 0; padding: 0; }
    2: 
    3: :root {
    4:   --brand: #0d9488;
    5:   --bg: #ffffff;
    6:   --line: #e5e7eb;
    7:   --text: #1f2937;
    8:   --muted: #6b7280;
    9:   --sidebar-w: 320px;
   10: }
   11: 
   12: html, body, #app { height: 100%; }
   13: body {
   14:   font-family: 'Pretendard', 'Malgun Gothic', system-ui, sans-serif;
   15:   color: var(--text);
   16: }
   17: 
   18: #app { display: flex; position: relative; overflow: hidden; }
   19: 
   20: /* ── 사이드바 ─────────────────────────── */
   21: #sidebar {
   22:   width: var(--sidebar-w);
   23:   min-width: var(--sidebar-w);
   24:   height: 100%;
   25:   display: flex;
   26:   flex-direction: column;
   27:   border-right: 1px solid var(--line);
   28:   background: var(--bg);
   29:   transition: margin-left 0.25s ease;
   30:   z-index: 20;
   31: }
   32: #sidebar.collapsed { margin-left: calc(-1 * var(--sidebar-w)); }
   33: 
   34: #sidebar-header {
   35:   display: flex; align-items: center; justify-content: space-between;
   36:   padding: 14px 16px; border-bottom: 1px solid var(--line);
   37: }
   38: #sidebar-header h1 { font-size: 18px; color: var(--brand); }
   39: #btn-collapse { border: none; background: none; cursor: pointer; font-size: 14px; color: var(--muted); }
   40: 
   41: #search-box { display: flex; gap: 6px; padding: 12px 16px 6px; }
   42: #search-input {
   43:   flex: 1; padding: 9px 12px; border: 1px solid var(--line); border-radius: 8px; font-size: 14px;
   44: }
   45: #search-input:focus { outline: 2px solid var(--brand); border-color: transparent; }
   46: #btn-search { border: none; background: var(--brand); color: #fff; border-radius: 8px; width: 40px; cursor: pointer; }
   47: 
   48: #search-results {
   49:   list-style: none; margin: 4px 16px; border: 1px solid var(--line); border-radius: 8px;
   50:   max-height: 240px; overflow-y: auto; background: #fff;
   51: }
   52: .search-item {
   53:   display: flex; align-items: center; justify-content: space-between;
   54:   padding: 8px 10px; border-bottom: 1px solid var(--line); cursor: pointer;
   55: }
   56: .search-item:last-child { border-bottom: none; }
   57: .search-item:hover { background: #f0fdfa; }
   58: .search-info { display: flex; flex-direction: column; }
   59: .search-info small { color: var(--muted); font-size: 11px; }
   60: .btn-add {
   61:   border: 1px solid var(--brand); color: var(--brand); background: none;
   62:   border-radius: 50%; width: 26px; height: 26px; cursor: pointer; font-size: 15px; flex-shrink: 0;
   63: }
   64: .btn-add:hover { background: var(--brand); color: #fff; }
   65: 
   66: #filter-bar { display: flex; flex-wrap: wrap; gap: 6px; padding: 10px 16px; }
   67: .filter-btn {
   68:   border: 1px solid var(--line); background: none; border-radius: 999px;
   69:   padding: 5px 11px; font-size: 13px; cursor: pointer; color: var(--text);
   70: }
   71: .filter-btn.active { background: var(--brand); border-color: var(--brand); color: #fff; }
   72: 
   73: #place-list { list-style: none; flex: 1; overflow-y: auto; padding: 4px 8px; }
   74: .place-item {
   75:   display: flex; align-items: center; gap: 10px;
   76:   padding: 10px; border-radius: 10px; cursor: pointer;
   77: }
   78: .place-item:hover { background: #f0fdfa; }
   79: .place-emoji {
   80:   width: 36px; height: 36px; border-radius: 10px;
   81:   display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;
   82: }
   83: .place-info { display: flex; flex-direction: column; }
   84: .place-info small { color: var(--muted); font-size: 12px; }
   85: .empty { text-align: center; color: var(--muted); padding: 40px 10px; font-size: 14px; line-height: 1.7; }
   86: 
   87: #sidebar-footer { display: flex; gap: 8px; padding: 12px 16px; border-top: 1px solid var(--line); }
   88: #sidebar-footer button {
   89:   flex: 1; padding: 8px; border: 1px solid var(--line); background: none;
   90:   border-radius: 8px; cursor: pointer; font-size: 13px;
   91: }
   92: #sidebar-footer button:hover { border-color: var(--brand); color: var(--brand); }
   93: 
   94: /* ── 지도 영역 ─────────────────────────── */
   95: #map-wrap { flex: 1; position: relative; }
   96: #map { width: 100%; height: 100%; }
   97: .sdk-error { padding: 40px; text-align: center; color: #b91c1c; line-height: 1.8; }
   98: 
   99: #btn-expand {
  100:   position: absolute; top: 12px; left: 12px; z-index: 15;
  101:   border: 1px solid var(--line); background: #fff; border-radius: 8px;
  102:   width: 34px; height: 34px; cursor: pointer; box-shadow: 0 2px 6px rgb(0 0 0 / 0.15);
  103: }
  104: #btn-mylocation, #btn-share {
  105:   position: absolute; right: 12px; z-index: 15;
  106:   border: 1px solid var(--line); background: #fff; border-radius: 50%;
  107:   width: 42px; height: 42px; cursor: pointer; font-size: 18px;
  108:   box-shadow: 0 2px 6px rgb(0 0 0 / 0.15);
  109: }
  110: #btn-mylocation { bottom: 76px; }
  111: #btn-share { bottom: 24px; }
  112: 
  113: .my-location-dot {
  114:   width: 16px; height: 16px; border-radius: 50%;
  115:   background: #2563eb; border: 3px solid #fff;
  116:   box-shadow: 0 0 0 6px rgb(37 99 235 / 0.25);
  117: }
  118: 
  119: /* ── 말풍선(커스텀 오버레이) ───────────── */
  120: .bubble { position: relative; }
  121: .bubble-inner {
  122:   background: #fff; border-radius: 10px; padding: 8px 30px 8px 12px;
  123:   box-shadow: 0 2px 10px rgb(0 0 0 / 0.2);
  124:   display: flex; flex-direction: column; cursor: pointer; white-space: nowrap;
  125: }
  126: .bubble-stars { color: #f59e0b; font-size: 12px; }
  127: .bubble-close {
  128:   position: absolute; top: 4px; right: 6px; border: none; background: none;
  129:   cursor: pointer; color: var(--muted); font-size: 15px;
  130: }
  131: .bubble-tail {
  132:   width: 0; height: 0; margin: 0 auto;
  133:   border: 8px solid transparent; border-top-color: #fff; border-bottom: none;
  134: }
  135: 
  136: /* ── 상세 패널 ─────────────────────────── */
  137: #detail-panel {
  138:   position: absolute; right: 12px; top: 12px; z-index: 25;
  139:   width: 280px; background: #fff; border-radius: 14px;
  140:   box-shadow: 0 6px 24px rgb(0 0 0 / 0.18); padding: 16px;
  141: }
  142: #detail-panel header { display: flex; justify-content: space-between; align-items: center; }
  143: #detail-panel h2 { font-size: 17px; }
  144: #detail-close { border: none; background: none; font-size: 20px; cursor: pointer; color: var(--muted); }
  145: .detail-cat { font-size: 13px; margin: 4px 0 8px; }
  146: .detail-stars .star {
  147:   border: none; background: none; font-size: 24px; cursor: pointer; color: #d1d5db;
  148: }
  149: .detail-stars .star.on { color: #f59e0b; }
  150: #detail-memo {
  151:   width: 100%; margin: 10px 0; padding: 8px; border: 1px solid var(--line);
  152:   border-radius: 8px; font-family: inherit; font-size: 13px; resize: vertical;
  153: }
  154: .detail-actions { display: flex; gap: 8px; }
  155: .detail-actions button {
  156:   flex: 1; padding: 8px; border-radius: 8px; cursor: pointer; border: 1px solid var(--line); background: none;
  157: }
  158: button.primary { background: var(--brand); border-color: var(--brand); color: #fff; }
  159: button.danger { color: #dc2626; border-color: #fecaca; }
  160: button.danger:hover { background: #fef2f2; }
  161: 
  162: /* ── 추가 다이얼로그 ───────────────────── */
  163: #add-dialog {
  164:   position: fixed; inset: 0; z-index: 50;
  165:   background: rgb(0 0 0 / 0.35);
  166:   display: flex; align-items: center; justify-content: center;
  167: }
  168: .dialog-card {
  169:   background: #fff; border-radius: 16px; padding: 22px; width: 320px;
  170:   display: flex; flex-direction: column; gap: 12px;
  171: }
  172: .dialog-card h2 { font-size: 17px; }
  173: .dialog-card label { display: flex; flex-direction: column; gap: 4px; font-size: 13px; color: var(--muted); }
  174: .dialog-card input, .dialog-card select, .dialog-card textarea {
  175:   padding: 8px 10px; border: 1px solid var(--line); border-radius: 8px;
  176:   font-family: inherit; font-size: 14px; color: var(--text);
  177: }
  178: .dialog-actions { display: flex; gap: 8px; margin-top: 4px; }
  179: .dialog-actions button { flex: 1; padding: 9px; border-radius: 8px; cursor: pointer; border: 1px solid var(--line); background: none; }
  180: 
  181: /* ── 토스트 ────────────────────────────── */
  182: #toast {
  183:   position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%);
  184:   background: #111827; color: #fff; padding: 10px 18px; border-radius: 999px;
  185:   font-size: 14px; z-index: 60; box-shadow: 0 4px 12px rgb(0 0 0 / 0.3);
  186: }
  187: 
  188: /* ── 모바일 ────────────────────────────── */
  189: @media (max-width: 640px) {
  190:   :root { --sidebar-w: 84vw; }
  191:   #sidebar { position: absolute; left: 0; top: 0; box-shadow: 4px 0 16px rgb(0 0 0 / 0.12); }
  192:   #sidebar.collapsed { margin-left: -100vw; }
  193:   #detail-panel { left: 12px; width: auto; top: auto; bottom: 12px; }
  194: }

hook: PostToolUse
hook: PostToolUse Completed
codex
초기 확인에서 가져오기 데이터의 `id`가 HTML 속성에 그대로 들어가는 경로와, 저장 데이터 스키마가 깨졌을 때 앱 전체가 중단되는 경로가 보입니다. 좌표·별점·해시 값도 검증 없이 SDK/문자열 반복 연산으로 넘어가므로 재현 가능한 실패 조건을 더 좁히고 있습니다.
hook: PreToolUse
hook: PreToolUse Completed
web search: 
web search: site:apis.map.kakao.com/web/documentation LatLng MarkerClusterer minLevel CustomOverlay content relayout keywordSearch Status official
hook: PostToolUse
hook: PostToolUse Completed
codex
## 코드 리뷰 결과

범위: `app/src/*.js`, `app/index.html`, `app/src/style.css` 전체.  
정적 분석 기준이며, 카카오 SDK 동작은 [공식 Web API 문서](https://apis.map.kakao.com/web/documentation/)와 대조했다.

### 1. 실제로 깨지는 버그

#### [높음] 가져온 데이터의 비정상 별점 하나로 전체 렌더링 중단

- [mapView.js:50](H:/YLBooks2/app/src/mapView.js:50)
- [sidebar.js:81](H:/YLBooks2/app/src/sidebar.js:81)
- [store.js:65](H:/YLBooks2/app/src/store.js:65)

`rating`을 검증하지 않는데 다음과 같이 문자열 반복 횟수로 직접 사용한다.

```js
'★'.repeat(place.rating || 0)
'☆'.repeat(5 - (place.rating || 0))
```

재현:

```json
[
  {
    "id": "bad",
    "name": "깨지는 장소",
    "lat": 37.5,
    "lng": 127,
    "rating": 6
  }
]
```

가져오면 `mapView.js:50`의 `'☆'.repeat(-1)`이 `RangeError: Invalid count value`를 던진다. 저장은 이미 `store.js:70`에서 교체된 뒤이므로 이후 재실행해도 localStorage에서 같은 데이터가 로드되어 앱이 계속 깨질 수 있다.

`rating: -1`, 매우 큰 값, 문자열, `null`도 각각 잘못된 표시나 예외·메모리 소모를 일으킨다.

#### [높음] localStorage 내용이 “유효한 JSON이지만 배열이 아닌 경우” 앱 시작 실패

- [store.js:9](H:/YLBooks2/app/src/store.js:9)
- [store.js:12](H:/YLBooks2/app/src/store.js:12)
- [sidebar.js:15](H:/YLBooks2/app/src/sidebar.js:15)
- [mapView.js:83](H:/YLBooks2/app/src/mapView.js:83)

`load()`는 JSON 파싱 성공 여부만 확인하고 데이터 구조는 확인하지 않는다.

재현:

```js
localStorage.setItem('my-map-places-v1', 'null');
location.reload();
```

이후 `filteredPlaces()`가 `null`을 반환하고, `renderList()`의 `places.length` 또는 `renderPlaces()`의 반복문에서 예외가 발생한다. `{}`, `123`, `"text"`도 유사하게 앱을 중단시킨다.

#### [중간] 메모를 입력한 뒤 별점을 누르면 저장하지 않은 메모가 사라짐

- [detail.js:35](H:/YLBooks2/app/src/detail.js:35)
- [detail.js:37](H:/YLBooks2/app/src/detail.js:37)
- [detail.js:38](H:/YLBooks2/app/src/detail.js:38)

별점 버튼은 별점만 저장한 다음 `openDetail(id)`로 패널 전체를 다시 만든다.

재현:

1. 장소 상세를 연다.
2. 메모를 수정하되 저장하지 않는다.
3. 별점을 누른다.
4. textarea가 저장된 이전 메모로 돌아간다.

사용자가 작성하던 내용이 아무 경고 없이 유실된다.

#### [중간] 저장 실패를 성공으로 표시하고 데이터는 새로고침 시 유실

- [store.js:19](H:/YLBooks2/app/src/store.js:19)
- [store.js:22](H:/YLBooks2/app/src/store.js:22)
- [search.js:97](H:/YLBooks2/app/src/search.js:97)
- [search.js:104](H:/YLBooks2/app/src/search.js:104)
- [detail.js:42](H:/YLBooks2/app/src/detail.js:42)

localStorage quota 초과, 브라우저 보안 설정, 사생활 보호 모드 등의 이유로 `setItem()`이 실패해도 `save()`는 오류를 삼킨다. 호출부는 항상 “추가했습니다”, “저장했습니다”라고 알린다.

재현:

1. 개발자 도구에서 `Storage.prototype.setItem`이 예외를 던지게 하거나 저장 공간을 소진한다.
2. 장소를 추가한다.
3. 성공 토스트가 표시되고 현재 세션에서는 보인다.
4. 새로고침하면 장소가 사라진다.

#### [중간] ID 누락·중복 데이터 가져오기 후 장소 선택/수정 대상이 잘못됨

- [store.js:65](H:/YLBooks2/app/src/store.js:65)
- [store.js:32](H:/YLBooks2/app/src/store.js:32)
- [sidebar.js:83](H:/YLBooks2/app/src/sidebar.js:83)
- [sidebar.js:93](H:/YLBooks2/app/src/sidebar.js:93)

가져오기 검증에서 `id`의 존재·형식·유일성을 검사하지 않는다.

- `id`가 없으면 DOM에는 `data-id="undefined"`가 생기지만 실제 값은 `undefined`이므로 `store.get("undefined")`가 찾지 못한다.
- ID가 중복되면 어느 항목을 클릭해도 `find()`가 반환하는 첫 번째 항목이 열리고 수정·삭제된다.

#### [중간] 장소 ID 생성 충돌 가능

- [store.js:35](H:/YLBooks2/app/src/store.js:35)
- [store.js:36](H:/YLBooks2/app/src/store.js:36)

ID가 밀리초 단위 `Date.now()`뿐이다. 같은 밀리초에 두 번 추가되면 중복 ID가 된다. 일반 UI 조작에서는 드물지만 자동화, 빠른 연속 이벤트, API를 직접 호출하는 테스트에서는 재현 가능하다. 이후 상세 조회·삭제가 첫 번째 항목에 잘못 적용된다.

#### [낮음] 검색 실패와 검색 결과 없음이 구분되지 않음

- [search.js:17](H:/YLBooks2/app/src/search.js:17)
- [search.js:18](H:/YLBooks2/app/src/search.js:18)

카카오 SDK는 `ZERO_RESULT`와 `ERROR`를 별도로 제공하지만 둘 다 “검색 결과가 없습니다”로 표시한다. 네트워크/서버/API 키 문제도 사용자에게 정상적인 0건 검색처럼 보인다. 공식 상태 정의도 `OK`, `ZERO_RESULT`, `ERROR`를 구분한다. [카카오 공식 문서](https://apis.map.kakao.com/web/documentation/)

---

### 2. 보안 문제

#### [높음] JSON 가져오기를 통한 저장형 DOM XSS

- [store.js:65](H:/YLBooks2/app/src/store.js:65)
- [sidebar.js:83](H:/YLBooks2/app/src/sidebar.js:83)
- [sidebar.js:78](H:/YLBooks2/app/src/sidebar.js:78)

가져온 `id`가 속성 컨텍스트에 이스케이프 없이 들어간 뒤 `innerHTML`로 파싱된다.

악성 파일 예:

```json
[
  {
    "id": "x\" onmouseover=\"alert(document.domain)",
    "name": "악성 장소",
    "lat": 37.5,
    "lng": 127
  }
]
```

생성되는 HTML은 사실상 다음과 같다.

```html
<li data-id="x" onmouseover="alert(document.domain)">
```

파일을 가져온 뒤 해당 목록 항목 위에 마우스를 올리면 스크립트가 실행된다. 데이터가 localStorage에 저장되므로 새로고침 후에도 지속되는 저장형 XSS다.

`id`를 엄격한 문자 집합으로 검증하고, 목록은 `innerHTML` 문자열 조립 대신 DOM API와 `dataset.id`로 만들어야 한다.

#### [중간] 가져오기 파일 크기 제한이 없어 클라이언트 DoS 가능

- [sidebar.js:48](H:/YLBooks2/app/src/sidebar.js:48)
- [sidebar.js:52](H:/YLBooks2/app/src/sidebar.js:52)
- [store.js:63](H:/YLBooks2/app/src/store.js:63)
- [mapView.js:83](H:/YLBooks2/app/src/mapView.js:83)

파일 전체를 `file.text()`로 읽고, 항목 수 제한 없이 각 장소마다 SVG 이미지, 마커, 오버레이, 이벤트 리스너를 생성한다. 매우 큰 JSON이나 수십만 개 항목을 가져오면 메모리 고갈 또는 UI 정지가 가능하다.

#### [낮음] CSP가 없어 XSS 및 외부 스크립트 침해의 피해 범위가 큼

- [index.html:3](H:/YLBooks2/app/index.html:3)
- [loader.js:10](H:/YLBooks2/app/src/loader.js:10)

Content Security Policy가 없다. 이 자체가 즉시 취약점은 아니지만 위 저장형 XSS가 그대로 실행되고, 동적으로 로드하는 외부 SDK가 침해될 경우 방어층이 없다. 카카오 SDK·`data:` 이미지·필요한 스타일 정책을 고려한 CSP가 필요하다.

#### [낮음, 추정] SDK 오류 메시지를 `innerHTML`로 출력

- [main.js:18](H:/YLBooks2/app/src/main.js:18)
- [main.js:19](H:/YLBooks2/app/src/main.js:19)

현재 코드에서 생성하는 오류 메시지는 상수이므로 직접 악용 가능성은 낮다. 다만 장래에 SDK/서버에서 받은 문자열을 `Error.message`에 넣게 되면 DOM XSS sink가 된다. `textContent`와 별도 `<br>` 요소를 사용하는 편이 안전하다.

이름과 메모는 현재 `escapeHtml()`을 적용하므로 해당 두 필드에서 직접적인 XSS는 확인되지 않았다.

---

### 3. 카카오 Maps JS SDK API 오용

#### [중간] CustomOverlay에 `clickable: true`가 없어 지도 클릭 이벤트로 전파될 수 있음

- [mapView.js:92](H:/YLBooks2/app/src/mapView.js:92)
- [mapView.js:102](H:/YLBooks2/app/src/mapView.js:102)
- [main.js:51](H:/YLBooks2/app/src/main.js:51)

말풍선 클릭은 상세 패널을 열지만 CustomOverlay 생성 시 `clickable: true`가 없다. 공식 문서는 이 옵션을 켜야 콘텐츠 클릭이 지도 이벤트로 전달되는 것을 막는다고 명시한다. [CustomOverlay 공식 문서](https://apis.map.kakao.com/web/documentation/)

따라서 말풍선을 클릭했을 때 아래 지도 `click` 이벤트까지 발생하여 장소 추가 다이얼로그가 함께 열릴 수 있다. 브라우저와 SDK 이벤트 처리에 영향을 받을 수 있으므로 실제 중복 발생 여부는 **추정**이지만, API 사용 자체는 잘못되어 있다.

#### [중간] `yAnchor: 1.35`가 문서상 허용 범위 밖

- [mapView.js:95](H:/YLBooks2/app/src/mapView.js:95)

공식 문서에서 CustomOverlay의 `xAnchor`, `yAnchor` 범위는 `0~1`이다. 현재 `1.35`는 범위 밖이다. SDK가 값을 그대로 계산하면 의도보다 위쪽에 배치될 수 있고, 향후 검증이 엄격해지면 동작이 달라질 수 있다. [카카오 공식 문서](https://apis.map.kakao.com/web/documentation/)

#### [중간] 공유 해시의 지도 레벨을 SDK 유효 범위로 제한하지 않음

- [share.js:23](H:/YLBooks2/app/src/share.js:23)
- [share.js:25](H:/YLBooks2/app/src/share.js:25)
- [main.js:25](H:/YLBooks2/app/src/main.js:25)
- [mapView.js:12](H:/YLBooks2/app/src/mapView.js:12)

`#37.5,127,999999` 같은 해시를 그대로 지도 생성 옵션에 넣는다. 공식 문서상 ROADMAP 레벨 범위는 `1~14`다. [카카오 공식 문서](https://apis.map.kakao.com/web/documentation/)

SDK가 보정할 가능성은 있지만 문서 계약 밖의 입력이며, 이상한 초기 줌이나 초기화 실패 가능성이 있다.

#### [낮음] relayout을 고정 타이머로 한 번만 호출

- [sidebar.js:67](H:/YLBooks2/app/src/sidebar.js:67)
- [sidebar.js:68](H:/YLBooks2/app/src/sidebar.js:68)
- [style.css:29](H:/YLBooks2/app/src/style.css:29)

`300ms`가 현재 CSS transition `250ms`보다 길어서 보통 작동하지만, 애니메이션 축소 설정, 프레임 지연, CSS 변경에 취약하다. 공식 문서대로 컨테이너 크기 변경 후 `relayout()` 호출하는 방향은 맞다. [지도 영역 변경 공식 예제](https://apis.map.kakao.com/web/sample/mapRelayout/)

`transitionend` 또는 `ResizeObserver`를 사용하는 편이 정확하다.

클러스터러의 `minLevel`, `minClusterSize`, `addMarkers/removeMarkers`, Marker의 `title`, CustomOverlay의 DOM Node 사용 자체는 공식 API와 일치했다.

---

### 4. 엣지케이스

#### [높음] 좌표의 유한성 및 위·경도 경계를 전혀 검사하지 않음

- [store.js:66](H:/YLBooks2/app/src/store.js:66)
- [share.js:23](H:/YLBooks2/app/src/share.js:23)
- [share.js:25](H:/YLBooks2/app/src/share.js:25)
- [mapView.js:84](H:/YLBooks2/app/src/mapView.js:84)

가져오기는 `typeof === 'number'`만 검사한다. 위도 `[-90, 90]`, 경도 `[-180, 180]` 범위를 확인하지 않는다. 해시는 더 심해서 `#.,.,7`, `#999,999,7`도 정규식을 통과한다.

재현:

```text
#.,.,7
```

`Number('.')`는 `NaN`이 되고 이를 `new kakao.maps.LatLng(NaN, NaN)`에 전달한다. SDK 내부 보정 여부에 따라 지도 초기화 실패 또는 비정상 지도가 될 수 있다.

JSON은 `NaN`을 직접 표현할 수 없지만 `999` 같은 범위 밖 숫자는 가져올 수 있다.

#### [중간] localStorage 손상 시 사용자 데이터 대신 예제 데이터를 조용히 노출

- [store.js:11](H:/YLBooks2/app/src/store.js:11)
- [store.js:13](H:/YLBooks2/app/src/store.js:13)
- [store.js:16](H:/YLBooks2/app/src/store.js:16)

JSON 구문 오류가 있으면 콘솔 경고만 남기고 기본 장소를 표시한다. 사용자는 자신의 데이터가 사라졌다고 오인할 수 있다. 복구·초기화 선택이나 손상 데이터 백업 기능이 필요하다.

#### [중간] 빈 검색어가 기존 검색 결과를 닫지 않음

- [search.js:15](H:/YLBooks2/app/src/search.js:15)
- [search.js:16](H:/YLBooks2/app/src/search.js:16)

검색 결과가 열린 상태에서 입력을 지우고 검색/Enter를 누르면 아무 일도 하지 않아 이전 검색 결과가 계속 표시된다. 사용자는 빈 검색에 대한 결과로 오인할 수 있다.

#### [중간] 잘못된 저장 데이터는 가져오기 검증을 우회함

- [store.js:7](H:/YLBooks2/app/src/store.js:7)
- [store.js:9](H:/YLBooks2/app/src/store.js:9)
- [store.js:62](H:/YLBooks2/app/src/store.js:62)

`importJson()`에는 제한적인 검증이라도 있지만 `load()`에는 동일 검증이 없다. 개발자 도구, 다른 버전 앱, 브라우저 확장, 과거 스키마가 localStorage를 변경하면 앱 시작 경로에서 즉시 크래시한다.

#### [낮음] 빈 데이터 자체는 처리되지만 기본 데이터와 “의도적 빈 지도” 정책이 모호함

- [store.js:11](H:/YLBooks2/app/src/store.js:11)
- [store.js:16](H:/YLBooks2/app/src/store.js:16)
- [sidebar.js:74](H:/YLBooks2/app/src/sidebar.js:74)

저장된 `[]`는 정상 유지되고 빈 안내도 표시된다. 반면 키가 없거나 읽기 실패면 예제 데이터가 자동 생성된다. 읽기 실패와 최초 실행을 구분하지 않아 “빈 지도” 복구 정책이 불명확하다.

#### [낮음] 공유 링크에서 기존 query string을 버림

- [share.js:10](H:/YLBooks2/app/src/share.js:10)

URL을 `origin + pathname + hash`로 재구성해 `location.search`를 제외한다. 쿼리 기반 라우팅·배포 버전·기능 플래그를 사용하는 환경에서는 공유 링크가 원래 상태를 보존하지 않는다.

---

### 5. 사소한 개선

#### [낮음] 저장소 내부 배열을 외부에 그대로 노출

- [store.js:29](H:/YLBooks2/app/src/store.js:29)
- [store.js:30](H:/YLBooks2/app/src/store.js:30)

`store.all()`이 내부 배열 참조를 반환한다. 호출자가 직접 `push`, `splice`, 객체 수정 등을 하면 저장과 구독 알림 없이 상태가 변경된다. 얕은 복사 또는 읽기 전용 스냅샷을 반환하는 편이 안전하다.

#### [낮음] 구독 해제 기능 없음

- [store.js:56](H:/YLBooks2/app/src/store.js:56)
- [store.js:57](H:/YLBooks2/app/src/store.js:57)

현재 앱은 한 번만 초기화되어 당장 문제는 없지만 HMR, 테스트, 재마운트에서는 리스너가 중복되어 렌더링과 메모리 사용이 누적될 수 있다. `subscribe()`가 unsubscribe 함수를 반환해야 한다.

#### [낮음] 접근성 이름과 대화상자 의미 구조 부족

- [index.html:19](H:/YLBooks2/app/index.html:19)
- [index.html:43](H:/YLBooks2/app/index.html:43)
- [search.js:69](H:/YLBooks2/app/src/search.js:69)
- [detail.js:16](H:/YLBooks2/app/src/detail.js:16)

이모지만 있는 버튼은 `title`에 의존하거나 검색 버튼처럼 이름조차 불분명하다. 추가 UI에는 `role="dialog"`, `aria-modal`, 포커스 이동·포커스 트랩, Escape 닫기가 없다. 키보드 사용자에게 특히 불편하다.

#### [낮음] CSS에서 긴 장소명이 레이아웃을 밀어낼 수 있음

- [style.css:58](H:/YLBooks2/app/src/style.css:58)
- [style.css:83](H:/YLBooks2/app/src/style.css:83)
- [style.css:124](H:/YLBooks2/app/src/style.css:124)

검색 정보와 장소 정보에 `min-width: 0`, 줄바꿈/ellipsis 규칙이 없다. 말풍선은 `white-space: nowrap`이다. 매우 긴 이름이나 공백 없는 문자열을 가져오면 버튼이 밀리거나 화면 밖으로 오버플로할 수 있다.

#### [낮음] 전역 `window.__map` 결합

- [main.js:30](H:/YLBooks2/app/src/main.js:30)
- [sidebar.js:68](H:/YLBooks2/app/src/sidebar.js:68)

이미 `getMap()`이 있는데 별도 전역을 사용한다. 테스트가 어려워지고 초기화 순서가 어긋나면 `window.__map.relayout()`에서 예외가 난다.

---

가장 먼저 고칠 순서는 다음과 같다.

1. 가져오기 및 localStorage 로드에 공통 스키마 검증 추가
2. `id` 속성 문자열 조립 제거로 저장형 XSS 차단
3. 좌표·레벨·별점을 유한한 정수/범위로 정규화
4. localStorage 저장 실패를 호출자에게 반환하고 성공 토스트 금지
5. 별점 클릭 시 작성 중 메모 보존
6. CustomOverlay에 `clickable: true` 추가 및 anchor 정상 범위 사용
hook: Stop
hook: Stop Completed
tokens used
36,882
## 코드 리뷰 결과

범위: `app/src/*.js`, `app/index.html`, `app/src/style.css` 전체.  
정적 분석 기준이며, 카카오 SDK 동작은 [공식 Web API 문서](https://apis.map.kakao.com/web/documentation/)와 대조했다.

### 1. 실제로 깨지는 버그

#### [높음] 가져온 데이터의 비정상 별점 하나로 전체 렌더링 중단

- [mapView.js:50](H:/YLBooks2/app/src/mapView.js:50)
- [sidebar.js:81](H:/YLBooks2/app/src/sidebar.js:81)
- [store.js:65](H:/YLBooks2/app/src/store.js:65)

`rating`을 검증하지 않는데 다음과 같이 문자열 반복 횟수로 직접 사용한다.

```js
'★'.repeat(place.rating || 0)
'☆'.repeat(5 - (place.rating || 0))
```

재현:

```json
[
  {
    "id": "bad",
    "name": "깨지는 장소",
    "lat": 37.5,
    "lng": 127,
    "rating": 6
  }
]
```

가져오면 `mapView.js:50`의 `'☆'.repeat(-1)`이 `RangeError: Invalid count value`를 던진다. 저장은 이미 `store.js:70`에서 교체된 뒤이므로 이후 재실행해도 localStorage에서 같은 데이터가 로드되어 앱이 계속 깨질 수 있다.

`rating: -1`, 매우 큰 값, 문자열, `null`도 각각 잘못된 표시나 예외·메모리 소모를 일으킨다.

#### [높음] localStorage 내용이 “유효한 JSON이지만 배열이 아닌 경우” 앱 시작 실패

- [store.js:9](H:/YLBooks2/app/src/store.js:9)
- [store.js:12](H:/YLBooks2/app/src/store.js:12)
- [sidebar.js:15](H:/YLBooks2/app/src/sidebar.js:15)
- [mapView.js:83](H:/YLBooks2/app/src/mapView.js:83)

`load()`는 JSON 파싱 성공 여부만 확인하고 데이터 구조는 확인하지 않는다.

재현:

```js
localStorage.setItem('my-map-places-v1', 'null');
location.reload();
```

이후 `filteredPlaces()`가 `null`을 반환하고, `renderList()`의 `places.length` 또는 `renderPlaces()`의 반복문에서 예외가 발생한다. `{}`, `123`, `"text"`도 유사하게 앱을 중단시킨다.

#### [중간] 메모를 입력한 뒤 별점을 누르면 저장하지 않은 메모가 사라짐

- [detail.js:35](H:/YLBooks2/app/src/detail.js:35)
- [detail.js:37](H:/YLBooks2/app/src/detail.js:37)
- [detail.js:38](H:/YLBooks2/app/src/detail.js:38)

별점 버튼은 별점만 저장한 다음 `openDetail(id)`로 패널 전체를 다시 만든다.

재현:

1. 장소 상세를 연다.
2. 메모를 수정하되 저장하지 않는다.
3. 별점을 누른다.
4. textarea가 저장된 이전 메모로 돌아간다.

사용자가 작성하던 내용이 아무 경고 없이 유실된다.

#### [중간] 저장 실패를 성공으로 표시하고 데이터는 새로고침 시 유실

- [store.js:19](H:/YLBooks2/app/src/store.js:19)
- [store.js:22](H:/YLBooks2/app/src/store.js:22)
- [search.js:97](H:/YLBooks2/app/src/search.js:97)
- [search.js:104](H:/YLBooks2/app/src/search.js:104)
- [detail.js:42](H:/YLBooks2/app/src/detail.js:42)

localStorage quota 초과, 브라우저 보안 설정, 사생활 보호 모드 등의 이유로 `setItem()`이 실패해도 `save()`는 오류를 삼킨다. 호출부는 항상 “추가했습니다”, “저장했습니다”라고 알린다.

재현:

1. 개발자 도구에서 `Storage.prototype.setItem`이 예외를 던지게 하거나 저장 공간을 소진한다.
2. 장소를 추가한다.
3. 성공 토스트가 표시되고 현재 세션에서는 보인다.
4. 새로고침하면 장소가 사라진다.

#### [중간] ID 누락·중복 데이터 가져오기 후 장소 선택/수정 대상이 잘못됨

- [store.js:65](H:/YLBooks2/app/src/store.js:65)
- [store.js:32](H:/YLBooks2/app/src/store.js:32)
- [sidebar.js:83](H:/YLBooks2/app/src/sidebar.js:83)
- [sidebar.js:93](H:/YLBooks2/app/src/sidebar.js:93)

가져오기 검증에서 `id`의 존재·형식·유일성을 검사하지 않는다.

- `id`가 없으면 DOM에는 `data-id="undefined"`가 생기지만 실제 값은 `undefined`이므로 `store.get("undefined")`가 찾지 못한다.
- ID가 중복되면 어느 항목을 클릭해도 `find()`가 반환하는 첫 번째 항목이 열리고 수정·삭제된다.

#### [중간] 장소 ID 생성 충돌 가능

- [store.js:35](H:/YLBooks2/app/src/store.js:35)
- [store.js:36](H:/YLBooks2/app/src/store.js:36)

ID가 밀리초 단위 `Date.now()`뿐이다. 같은 밀리초에 두 번 추가되면 중복 ID가 된다. 일반 UI 조작에서는 드물지만 자동화, 빠른 연속 이벤트, API를 직접 호출하는 테스트에서는 재현 가능하다. 이후 상세 조회·삭제가 첫 번째 항목에 잘못 적용된다.

#### [낮음] 검색 실패와 검색 결과 없음이 구분되지 않음

- [search.js:17](H:/YLBooks2/app/src/search.js:17)
- [search.js:18](H:/YLBooks2/app/src/search.js:18)

카카오 SDK는 `ZERO_RESULT`와 `ERROR`를 별도로 제공하지만 둘 다 “검색 결과가 없습니다”로 표시한다. 네트워크/서버/API 키 문제도 사용자에게 정상적인 0건 검색처럼 보인다. 공식 상태 정의도 `OK`, `ZERO_RESULT`, `ERROR`를 구분한다. [카카오 공식 문서](https://apis.map.kakao.com/web/documentation/)

---

### 2. 보안 문제

#### [높음] JSON 가져오기를 통한 저장형 DOM XSS

- [store.js:65](H:/YLBooks2/app/src/store.js:65)
- [sidebar.js:83](H:/YLBooks2/app/src/sidebar.js:83)
- [sidebar.js:78](H:/YLBooks2/app/src/sidebar.js:78)

가져온 `id`가 속성 컨텍스트에 이스케이프 없이 들어간 뒤 `innerHTML`로 파싱된다.

악성 파일 예:

```json
[
  {
    "id": "x\" onmouseover=\"alert(document.domain)",
    "name": "악성 장소",
    "lat": 37.5,
    "lng": 127
  }
]
```

생성되는 HTML은 사실상 다음과 같다.

```html
<li data-id="x" onmouseover="alert(document.domain)">
```

파일을 가져온 뒤 해당 목록 항목 위에 마우스를 올리면 스크립트가 실행된다. 데이터가 localStorage에 저장되므로 새로고침 후에도 지속되는 저장형 XSS다.

`id`를 엄격한 문자 집합으로 검증하고, 목록은 `innerHTML` 문자열 조립 대신 DOM API와 `dataset.id`로 만들어야 한다.

#### [중간] 가져오기 파일 크기 제한이 없어 클라이언트 DoS 가능

- [sidebar.js:48](H:/YLBooks2/app/src/sidebar.js:48)
- [sidebar.js:52](H:/YLBooks2/app/src/sidebar.js:52)
- [store.js:63](H:/YLBooks2/app/src/store.js:63)
- [mapView.js:83](H:/YLBooks2/app/src/mapView.js:83)

파일 전체를 `file.text()`로 읽고, 항목 수 제한 없이 각 장소마다 SVG 이미지, 마커, 오버레이, 이벤트 리스너를 생성한다. 매우 큰 JSON이나 수십만 개 항목을 가져오면 메모리 고갈 또는 UI 정지가 가능하다.

#### [낮음] CSP가 없어 XSS 및 외부 스크립트 침해의 피해 범위가 큼

- [index.html:3](H:/YLBooks2/app/index.html:3)
- [loader.js:10](H:/YLBooks2/app/src/loader.js:10)

Content Security Policy가 없다. 이 자체가 즉시 취약점은 아니지만 위 저장형 XSS가 그대로 실행되고, 동적으로 로드하는 외부 SDK가 침해될 경우 방어층이 없다. 카카오 SDK·`data:` 이미지·필요한 스타일 정책을 고려한 CSP가 필요하다.

#### [낮음, 추정] SDK 오류 메시지를 `innerHTML`로 출력

- [main.js:18](H:/YLBooks2/app/src/main.js:18)
- [main.js:19](H:/YLBooks2/app/src/main.js:19)

현재 코드에서 생성하는 오류 메시지는 상수이므로 직접 악용 가능성은 낮다. 다만 장래에 SDK/서버에서 받은 문자열을 `Error.message`에 넣게 되면 DOM XSS sink가 된다. `textContent`와 별도 `<br>` 요소를 사용하는 편이 안전하다.

이름과 메모는 현재 `escapeHtml()`을 적용하므로 해당 두 필드에서 직접적인 XSS는 확인되지 않았다.

---

### 3. 카카오 Maps JS SDK API 오용

#### [중간] CustomOverlay에 `clickable: true`가 없어 지도 클릭 이벤트로 전파될 수 있음

- [mapView.js:92](H:/YLBooks2/app/src/mapView.js:92)
- [mapView.js:102](H:/YLBooks2/app/src/mapView.js:102)
- [main.js:51](H:/YLBooks2/app/src/main.js:51)

말풍선 클릭은 상세 패널을 열지만 CustomOverlay 생성 시 `clickable: true`가 없다. 공식 문서는 이 옵션을 켜야 콘텐츠 클릭이 지도 이벤트로 전달되는 것을 막는다고 명시한다. [CustomOverlay 공식 문서](https://apis.map.kakao.com/web/documentation/)

따라서 말풍선을 클릭했을 때 아래 지도 `click` 이벤트까지 발생하여 장소 추가 다이얼로그가 함께 열릴 수 있다. 브라우저와 SDK 이벤트 처리에 영향을 받을 수 있으므로 실제 중복 발생 여부는 **추정**이지만, API 사용 자체는 잘못되어 있다.

#### [중간] `yAnchor: 1.35`가 문서상 허용 범위 밖

- [mapView.js:95](H:/YLBooks2/app/src/mapView.js:95)

공식 문서에서 CustomOverlay의 `xAnchor`, `yAnchor` 범위는 `0~1`이다. 현재 `1.35`는 범위 밖이다. SDK가 값을 그대로 계산하면 의도보다 위쪽에 배치될 수 있고, 향후 검증이 엄격해지면 동작이 달라질 수 있다. [카카오 공식 문서](https://apis.map.kakao.com/web/documentation/)

#### [중간] 공유 해시의 지도 레벨을 SDK 유효 범위로 제한하지 않음

- [share.js:23](H:/YLBooks2/app/src/share.js:23)
- [share.js:25](H:/YLBooks2/app/src/share.js:25)
- [main.js:25](H:/YLBooks2/app/src/main.js:25)
- [mapView.js:12](H:/YLBooks2/app/src/mapView.js:12)

`#37.5,127,999999` 같은 해시를 그대로 지도 생성 옵션에 넣는다. 공식 문서상 ROADMAP 레벨 범위는 `1~14`다. [카카오 공식 문서](https://apis.map.kakao.com/web/documentation/)

SDK가 보정할 가능성은 있지만 문서 계약 밖의 입력이며, 이상한 초기 줌이나 초기화 실패 가능성이 있다.

#### [낮음] relayout을 고정 타이머로 한 번만 호출

- [sidebar.js:67](H:/YLBooks2/app/src/sidebar.js:67)
- [sidebar.js:68](H:/YLBooks2/app/src/sidebar.js:68)
- [style.css:29](H:/YLBooks2/app/src/style.css:29)

`300ms`가 현재 CSS transition `250ms`보다 길어서 보통 작동하지만, 애니메이션 축소 설정, 프레임 지연, CSS 변경에 취약하다. 공식 문서대로 컨테이너 크기 변경 후 `relayout()` 호출하는 방향은 맞다. [지도 영역 변경 공식 예제](https://apis.map.kakao.com/web/sample/mapRelayout/)

`transitionend` 또는 `ResizeObserver`를 사용하는 편이 정확하다.

클러스터러의 `minLevel`, `minClusterSize`, `addMarkers/removeMarkers`, Marker의 `title`, CustomOverlay의 DOM Node 사용 자체는 공식 API와 일치했다.

---

### 4. 엣지케이스

#### [높음] 좌표의 유한성 및 위·경도 경계를 전혀 검사하지 않음

- [store.js:66](H:/YLBooks2/app/src/store.js:66)
- [share.js:23](H:/YLBooks2/app/src/share.js:23)
- [share.js:25](H:/YLBooks2/app/src/share.js:25)
- [mapView.js:84](H:/YLBooks2/app/src/mapView.js:84)

가져오기는 `typeof === 'number'`만 검사한다. 위도 `[-90, 90]`, 경도 `[-180, 180]` 범위를 확인하지 않는다. 해시는 더 심해서 `#.,.,7`, `#999,999,7`도 정규식을 통과한다.

재현:

```text
#.,.,7
```

`Number('.')`는 `NaN`이 되고 이를 `new kakao.maps.LatLng(NaN, NaN)`에 전달한다. SDK 내부 보정 여부에 따라 지도 초기화 실패 또는 비정상 지도가 될 수 있다.

JSON은 `NaN`을 직접 표현할 수 없지만 `999` 같은 범위 밖 숫자는 가져올 수 있다.

#### [중간] localStorage 손상 시 사용자 데이터 대신 예제 데이터를 조용히 노출

- [store.js:11](H:/YLBooks2/app/src/store.js:11)
- [store.js:13](H:/YLBooks2/app/src/store.js:13)
- [store.js:16](H:/YLBooks2/app/src/store.js:16)

JSON 구문 오류가 있으면 콘솔 경고만 남기고 기본 장소를 표시한다. 사용자는 자신의 데이터가 사라졌다고 오인할 수 있다. 복구·초기화 선택이나 손상 데이터 백업 기능이 필요하다.

#### [중간] 빈 검색어가 기존 검색 결과를 닫지 않음

- [search.js:15](H:/YLBooks2/app/src/search.js:15)
- [search.js:16](H:/YLBooks2/app/src/search.js:16)

검색 결과가 열린 상태에서 입력을 지우고 검색/Enter를 누르면 아무 일도 하지 않아 이전 검색 결과가 계속 표시된다. 사용자는 빈 검색에 대한 결과로 오인할 수 있다.

#### [중간] 잘못된 저장 데이터는 가져오기 검증을 우회함

- [store.js:7](H:/YLBooks2/app/src/store.js:7)
- [store.js:9](H:/YLBooks2/app/src/store.js:9)
- [store.js:62](H:/YLBooks2/app/src/store.js:62)

`importJson()`에는 제한적인 검증이라도 있지만 `load()`에는 동일 검증이 없다. 개발자 도구, 다른 버전 앱, 브라우저 확장, 과거 스키마가 localStorage를 변경하면 앱 시작 경로에서 즉시 크래시한다.

#### [낮음] 빈 데이터 자체는 처리되지만 기본 데이터와 “의도적 빈 지도” 정책이 모호함

- [store.js:11](H:/YLBooks2/app/src/store.js:11)
- [store.js:16](H:/YLBooks2/app/src/store.js:16)
- [sidebar.js:74](H:/YLBooks2/app/src/sidebar.js:74)

저장된 `[]`는 정상 유지되고 빈 안내도 표시된다. 반면 키가 없거나 읽기 실패면 예제 데이터가 자동 생성된다. 읽기 실패와 최초 실행을 구분하지 않아 “빈 지도” 복구 정책이 불명확하다.

#### [낮음] 공유 링크에서 기존 query string을 버림

- [share.js:10](H:/YLBooks2/app/src/share.js:10)

URL을 `origin + pathname + hash`로 재구성해 `location.search`를 제외한다. 쿼리 기반 라우팅·배포 버전·기능 플래그를 사용하는 환경에서는 공유 링크가 원래 상태를 보존하지 않는다.

---

### 5. 사소한 개선

#### [낮음] 저장소 내부 배열을 외부에 그대로 노출

- [store.js:29](H:/YLBooks2/app/src/store.js:29)
- [store.js:30](H:/YLBooks2/app/src/store.js:30)

`store.all()`이 내부 배열 참조를 반환한다. 호출자가 직접 `push`, `splice`, 객체 수정 등을 하면 저장과 구독 알림 없이 상태가 변경된다. 얕은 복사 또는 읽기 전용 스냅샷을 반환하는 편이 안전하다.

#### [낮음] 구독 해제 기능 없음

- [store.js:56](H:/YLBooks2/app/src/store.js:56)
- [store.js:57](H:/YLBooks2/app/src/store.js:57)

현재 앱은 한 번만 초기화되어 당장 문제는 없지만 HMR, 테스트, 재마운트에서는 리스너가 중복되어 렌더링과 메모리 사용이 누적될 수 있다. `subscribe()`가 unsubscribe 함수를 반환해야 한다.

#### [낮음] 접근성 이름과 대화상자 의미 구조 부족

- [index.html:19](H:/YLBooks2/app/index.html:19)
- [index.html:43](H:/YLBooks2/app/index.html:43)
- [search.js:69](H:/YLBooks2/app/src/search.js:69)
- [detail.js:16](H:/YLBooks2/app/src/detail.js:16)

이모지만 있는 버튼은 `title`에 의존하거나 검색 버튼처럼 이름조차 불분명하다. 추가 UI에는 `role="dialog"`, `aria-modal`, 포커스 이동·포커스 트랩, Escape 닫기가 없다. 키보드 사용자에게 특히 불편하다.

#### [낮음] CSS에서 긴 장소명이 레이아웃을 밀어낼 수 있음

- [style.css:58](H:/YLBooks2/app/src/style.css:58)
- [style.css:83](H:/YLBooks2/app/src/style.css:83)
- [style.css:124](H:/YLBooks2/app/src/style.css:124)

검색 정보와 장소 정보에 `min-width: 0`, 줄바꿈/ellipsis 규칙이 없다. 말풍선은 `white-space: nowrap`이다. 매우 긴 이름이나 공백 없는 문자열을 가져오면 버튼이 밀리거나 화면 밖으로 오버플로할 수 있다.

#### [낮음] 전역 `window.__map` 결합

- [main.js:30](H:/YLBooks2/app/src/main.js:30)
- [sidebar.js:68](H:/YLBooks2/app/src/sidebar.js:68)

이미 `getMap()`이 있는데 별도 전역을 사용한다. 테스트가 어려워지고 초기화 순서가 어긋나면 `window.__map.relayout()`에서 예외가 난다.

---

가장 먼저 고칠 순서는 다음과 같다.

1. 가져오기 및 localStorage 로드에 공통 스키마 검증 추가
2. `id` 속성 문자열 조립 제거로 저장형 XSS 차단
3. 좌표·레벨·별점을 유한한 정수/범위로 정규화
4. localStorage 저장 실패를 호출자에게 반환하고 성공 토스트 금지
5. 별점 클릭 시 작성 중 메모 보존
6. CustomOverlay에 `clickable: true` 추가 및 anchor 정상 범위 사용
