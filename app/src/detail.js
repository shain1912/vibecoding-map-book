// 상세 패널 — 별점·메모 편집, 삭제
import { store } from './store.js';
import { categoryOf } from './categories.js';
import { escapeHtml } from './mapView.js';
import { toast } from './sidebar.js';

let currentId = null;

export function openDetail(id) {
  const place = store.get(id);
  if (!place) return;
  currentId = id;
  const panel = document.getElementById('detail-panel');
  const cat = categoryOf(place.category);
  panel.hidden = false;
  panel.innerHTML = `
    <header>
      <h2>${cat.emoji} ${escapeHtml(place.name)}</h2>
      <button id="detail-close" title="닫기">×</button>
    </header>
    <p class="detail-cat" style="color:${cat.color}">${cat.label}</p>
    <div class="detail-stars" id="detail-stars">
      ${[1, 2, 3, 4, 5]
        .map((n) => `<button class="star ${n <= (place.rating || 0) ? 'on' : ''}" data-n="${n}">★</button>`)
        .join('')}
    </div>
    <textarea id="detail-memo" rows="4" placeholder="메모를 남겨 보세요">${escapeHtml(place.memo || '')}</textarea>
    <div class="detail-actions">
      <button id="detail-save" class="primary">저장</button>
      <button id="detail-delete" class="danger">삭제</button>
    </div>`;

  panel.querySelector('#detail-close').addEventListener('click', closeDetail);
  panel.querySelectorAll('.star').forEach((btn) => {
    btn.addEventListener('click', () => {
      const n = Number(btn.dataset.n);
      // 다시 그리기 전에 쓰던 메모를 잃지 않게 보관한다
      const draft = panel.querySelector('#detail-memo').value;
      store.update(id, { rating: n });
      openDetail(id); // 다시 그려서 별 반영
      panel.querySelector('#detail-memo').value = draft;
    });
  });
  panel.querySelector('#detail-save').addEventListener('click', () => {
    store.update(id, { memo: panel.querySelector('#detail-memo').value });
    toast('저장했습니다.');
  });
  panel.querySelector('#detail-delete').addEventListener('click', () => {
    if (confirm(`'${place.name}'을(를) 삭제할까요?`)) {
      store.remove(id);
      closeDetail();
      toast('삭제했습니다.');
    }
  });
}

export function closeDetail() {
  const panel = document.getElementById('detail-panel');
  panel.hidden = true;
  currentId = null;
}

export function getOpenDetailId() {
  return currentId;
}
