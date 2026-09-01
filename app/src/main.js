// 앱 진입점 — 모든 모듈을 조립한다
import './style.css';
import { loadKakaoSdk } from './loader.js';
import { store } from './store.js';
import {
  createMap, renderPlaces, focusPlace, setMarkerClickHandler,
  showMyLocation, getMap,
} from './mapView.js';
import { initSidebar, filteredPlaces, toast } from './sidebar.js';
import { initSearch, openAddDialog } from './search.js';
import { openDetail } from './detail.js';
import { initShare, parseHash } from './share.js';

async function main() {
  try {
    await loadKakaoSdk();
  } catch (e) {
    document.getElementById('map').innerHTML =
      `<p class="sdk-error">지도를 불러오지 못했습니다.<br>${e.message}</p>`;
    return;
  }

  // 공유 링크(#lat,lng,level)로 들어왔으면 그 위치에서 시작
  const hashState = parseHash();
  const map = createMap(
    document.getElementById('map'),
    hashState ?? { lat: 37.5665, lng: 126.978 },
    hashState?.level ?? 7
  );
  window.__map = map; // 사이드바 접기에서 resize 트리거용

  const rerender = () => renderPlaces(filteredPlaces());

  setMarkerClickHandler((id) => openDetail(id));
  initSidebar({
    onSelectPlace: (id) => {
      const p = store.get(id);
      if (p) {
        focusPlace(p);
        openDetail(id);
      }
    },
    onFilter: rerender,
  });
  initSearch();
  initShare();
  store.subscribe(rerender);
  rerender();

  // 지도 클릭 → 장소 추가
  kakao.maps.event.addListener(map, 'click', (e) => {
    openAddDialog({ lat: e.latLng.getLat(), lng: e.latLng.getLng() });
  });

  // 내 위치
  document.getElementById('btn-mylocation').addEventListener('click', () => {
    if (!navigator.geolocation) {
      toast('이 브라우저는 위치를 지원하지 않습니다.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => showMyLocation(pos.coords.latitude, pos.coords.longitude),
      () => toast('위치 권한이 거부되었습니다.')
    );
  });
}

main();
