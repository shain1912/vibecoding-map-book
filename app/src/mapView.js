// 지도 담당 모듈 — 지도 생성, 마커/오버레이/클러스터러 렌더링
import { categoryOf } from './categories.js';

let map;
let clusterer;
let markers = []; // { marker, overlay, place }
let onMarkerClick = () => {};

export function createMap(container, center = { lat: 37.5665, lng: 126.978 }, level = 7) {
  map = new kakao.maps.Map(container, {
    center: new kakao.maps.LatLng(center.lat, center.lng),
    level,
  });
  map.addControl(new kakao.maps.MapTypeControl(), kakao.maps.ControlPosition.TOPRIGHT);
  map.addControl(new kakao.maps.ZoomControl(), kakao.maps.ControlPosition.RIGHT);

  clusterer = new kakao.maps.MarkerClusterer({
    map,
    averageCenter: true,
    minLevel: 6,
    minClusterSize: 3,
  });
  return map;
}

export function getMap() {
  return map;
}

export function setMarkerClickHandler(fn) {
  onMarkerClick = fn;
}

function markerImageFor(category) {
  const { emoji, color } = categoryOf(category);
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="36" height="46" viewBox="0 0 36 46">
      <path d="M18 0C8 0 0 8 0 18c0 12 18 28 18 28s18-16 18-28C36 8 28 0 18 0z" fill="${color}"/>
      <circle cx="18" cy="17" r="12" fill="white"/>
      <text x="18" y="22" font-size="14" text-anchor="middle">${emoji}</text>
    </svg>`;
  const url = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
  return new kakao.maps.MarkerImage(url, new kakao.maps.Size(36, 46), {
    offset: new kakao.maps.Point(18, 46),
  });
}

function overlayContent(place) {
  const cat = categoryOf(place.category);
  const stars = '★'.repeat(place.rating || 0) + '☆'.repeat(5 - (place.rating || 0));
  const el = document.createElement('div');
  el.className = 'bubble';
  el.innerHTML = `
    <div class="bubble-inner">
      <strong>${cat.emoji} ${escapeHtml(place.name)}</strong>
      <span class="bubble-stars">${stars}</span>
      <button class="bubble-close" title="닫기">×</button>
    </div>
    <div class="bubble-tail"></div>`;
  return el;
}

export function escapeHtml(s = '') {
  return s.replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  })[c]);
}

let openOverlay = null;

export function closeOverlay() {
  if (openOverlay) {
    openOverlay.setMap(null);
    openOverlay = null;
  }
}

export function renderPlaces(places) {
  closeOverlay();
  clusterer.removeMarkers(markers.map((m) => m.marker));
  markers = [];

  for (const place of places) {
    const pos = new kakao.maps.LatLng(place.lat, place.lng);
    const marker = new kakao.maps.Marker({
      position: pos,
      image: markerImageFor(place.category),
      title: place.name,
    });

    const el = overlayContent(place);
    const overlay = new kakao.maps.CustomOverlay({
      content: el,
      position: pos,
      yAnchor: 1.35,
      zIndex: 10,
      clickable: true, // 말풍선 클릭이 지도 클릭(장소 추가)으로 번지지 않게
    });
    el.querySelector('.bubble-close').addEventListener('click', (e) => {
      e.stopPropagation();
      closeOverlay();
    });
    el.querySelector('.bubble-inner').addEventListener('click', () => onMarkerClick(place.id));

    kakao.maps.event.addListener(marker, 'click', () => {
      closeOverlay();
      overlay.setMap(map);
      openOverlay = overlay;
      onMarkerClick(place.id);
    });

    markers.push({ marker, overlay, place });
  }
  clusterer.addMarkers(markers.map((m) => m.marker));
}

export function focusPlace(place, level = 4) {
  const pos = new kakao.maps.LatLng(place.lat, place.lng);
  map.setLevel(level);
  map.panTo(pos);
  const entry = markers.find((m) => m.place.id === place.id);
  if (entry) {
    closeOverlay();
    entry.overlay.setMap(map);
    openOverlay = entry.overlay;
  }
}

let myLocationMarker = null;

export function showMyLocation(lat, lng) {
  const pos = new kakao.maps.LatLng(lat, lng);
  if (!myLocationMarker) {
    const el = document.createElement('div');
    el.className = 'my-location-dot';
    myLocationMarker = new kakao.maps.CustomOverlay({ content: el, position: pos, zIndex: 5 });
  }
  myLocationMarker.setPosition(pos);
  myLocationMarker.setMap(map);
  map.setLevel(4);
  map.panTo(pos);
}
