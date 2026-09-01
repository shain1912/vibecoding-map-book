// 카테고리 정의 — 지도 전체에서 이 한 곳만 고치면 된다.
export const CATEGORIES = {
  food:   { label: '맛집',   emoji: '🍜', color: '#e74c3c' },
  cafe:   { label: '카페',   emoji: '☕', color: '#8e5a2d' },
  travel: { label: '여행',   emoji: '🏝', color: '#1e90ff' },
  date:   { label: '데이트', emoji: '💕', color: '#e84393' },
};

export function categoryOf(id) {
  return CATEGORIES[id] ?? { label: '기타', emoji: '📍', color: '#555' };
}
