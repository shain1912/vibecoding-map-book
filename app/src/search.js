// 키워드 장소 검색 — kakao.maps.services.Places
import { store } from './store.js';
import { escapeHtml, getMap } from './mapView.js';
import { toast } from './sidebar.js';

let ps;

export function initSearch() {
  ps = new kakao.maps.services.Places();
  const input = document.getElementById('search-input');
  const btn = document.getElementById('btn-search');
  const resultsEl = document.getElementById('search-results');

  const run = () => {
    const q = input.value.trim();
    if (!q) return;
    ps.keywordSearch(q, (data, status) => {
      if (status !== kakao.maps.services.Status.OK) {
        toast('검색 결과가 없습니다.');
        resultsEl.hidden = true;
        return;
      }
      renderResults(data.slice(0, 7));
    });
  };

  btn.addEventListener('click', run);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') run();
  });

  function renderResults(items) {
    resultsEl.hidden = false;
    resultsEl.innerHTML = items
      .map(
        (item, i) => `
        <li class="search-item" data-i="${i}">
          <span class="search-info">
            <strong>${escapeHtml(item.place_name)}</strong>
            <small>${escapeHtml(item.road_address_name || item.address_name || '')}</small>
          </span>
          <button class="btn-add" title="내 지도에 추가">＋</button>
        </li>`
      )
      .join('');

    resultsEl.querySelectorAll('.search-item').forEach((li) => {
      const item = items[Number(li.dataset.i)];
      const lat = Number(item.y);
      const lng = Number(item.x);
      // 결과 클릭 → 지도 이동
      li.querySelector('.search-info').addEventListener('click', () => {
        getMap().setLevel(3);
        getMap().panTo(new kakao.maps.LatLng(lat, lng));
      });
      // ＋ 클릭 → 내 지도에 추가
      li.querySelector('.btn-add').addEventListener('click', (e) => {
        e.stopPropagation();
        openAddDialog({ name: item.place_name, lat, lng });
        resultsEl.hidden = true;
      });
    });
  }
}

// 장소 추가 폼 (검색 추가 + 지도 클릭 추가 공용)
export function openAddDialog({ name = '', lat, lng }) {
  closeAddDialog();
  const wrap = document.createElement('div');
  wrap.id = 'add-dialog';
  wrap.innerHTML = `
    <div class="dialog-card">
      <h2>장소 추가</h2>
      <label>이름 <input id="add-name" value="${escapeHtml(name)}" placeholder="장소 이름" /></label>
      <label>카테고리
        <select id="add-category">
          <option value="food">🍜 맛집</option>
          <option value="cafe">☕ 카페</option>
          <option value="travel">🏝 여행</option>
          <option value="date">💕 데이트</option>
        </select>
      </label>
      <label>메모 <textarea id="add-memo" rows="2" placeholder="한 줄 메모"></textarea></label>
      <div class="dialog-actions">
        <button id="add-cancel">취소</button>
        <button id="add-ok" class="primary">추가</button>
      </div>
    </div>`;
  document.body.appendChild(wrap);
  wrap.querySelector('#add-cancel').addEventListener('click', closeAddDialog);
  wrap.querySelector('#add-ok').addEventListener('click', () => {
    const nameVal = wrap.querySelector('#add-name').value.trim();
    if (!nameVal) {
      toast('이름을 입력하세요.');
      return;
    }
    store.add({
      name: nameVal,
      category: wrap.querySelector('#add-category').value,
      memo: wrap.querySelector('#add-memo').value.trim(),
      lat,
      lng,
    });
    toast('내 지도에 추가했습니다!');
    closeAddDialog();
  });
}

export function closeAddDialog() {
  document.getElementById('add-dialog')?.remove();
}
