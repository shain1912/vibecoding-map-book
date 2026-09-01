// 사이드바 — 장소 목록, 카테고리 필터, 내보내기/가져오기
import { store } from './store.js';
import { categoryOf } from './categories.js';
import { escapeHtml } from './mapView.js';

let currentFilter = 'all';
let onSelect = () => {};
let onFilterChange = () => {};

export function getFilter() {
  return currentFilter;
}

export function filteredPlaces() {
  const all = store.all();
  return currentFilter === 'all' ? all : all.filter((p) => p.category === currentFilter);
}

export function initSidebar({ onSelectPlace, onFilter }) {
  onSelect = onSelectPlace;
  onFilterChange = onFilter;

  document.querySelectorAll('.filter-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      currentFilter = btn.dataset.category;
      document.querySelectorAll('.filter-btn').forEach((b) => b.classList.toggle('active', b === btn));
      renderList();
      onFilterChange();
    });
  });

  document.getElementById('btn-collapse').addEventListener('click', () => toggleSidebar(false));
  document.getElementById('btn-expand').addEventListener('click', () => toggleSidebar(true));

  // 내보내기 — JSON 파일 다운로드
  document.getElementById('btn-export').addEventListener('click', () => {
    const blob = new Blob([store.exportJson()], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'my-map-places.json';
    a.click();
    URL.revokeObjectURL(a.href);
  });

  // 가져오기 — JSON 파일 업로드
  const fileInput = document.getElementById('import-file');
  document.getElementById('btn-import').addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', async () => {
    const file = fileInput.files[0];
    if (!file) return;
    try {
      store.importJson(await file.text());
      toast('가져오기 완료!');
    } catch (e) {
      toast('가져오기 실패: ' + e.message);
    }
    fileInput.value = '';
  });

  store.subscribe(renderList);
  renderList();
}

export function toggleSidebar(open) {
  document.getElementById('sidebar').classList.toggle('collapsed', !open);
  document.getElementById('btn-expand').hidden = open;
  // 지도 크기가 변하므로 카카오 지도에 알려준다
  setTimeout(() => kakao.maps.event.trigger(window.__map, 'resize'), 250);
}

export function renderList() {
  const ul = document.getElementById('place-list');
  const places = filteredPlaces();
  if (places.length === 0) {
    ul.innerHTML = '<li class="empty">장소가 없습니다.<br>검색하거나 지도를 클릭해 추가해 보세요!</li>';
    return;
  }
  ul.innerHTML = places
    .map((p) => {
      const cat = categoryOf(p.category);
      const stars = '★'.repeat(p.rating || 0);
      return `
        <li class="place-item" data-id="${p.id}">
          <span class="place-emoji" style="background:${cat.color}22">${cat.emoji}</span>
          <span class="place-info">
            <strong>${escapeHtml(p.name)}</strong>
            <small>${cat.label} ${stars ? '· ' + stars : ''}</small>
          </span>
        </li>`;
    })
    .join('');
  ul.querySelectorAll('.place-item').forEach((li) => {
    li.addEventListener('click', () => onSelect(li.dataset.id));
  });
}

let toastTimer;
export function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (el.hidden = true), 2200);
}
