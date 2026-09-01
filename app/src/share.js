// URL 해시로 지도 상태 공유 — #lat,lng,level
import { getMap } from './mapView.js';
import { toast } from './sidebar.js';

export function initShare() {
  document.getElementById('btn-share').addEventListener('click', async () => {
    const map = getMap();
    const c = map.getCenter();
    const hash = `#${c.getLat().toFixed(5)},${c.getLng().toFixed(5)},${map.getLevel()}`;
    const url = location.origin + location.pathname + hash;
    history.replaceState(null, '', hash);
    try {
      await navigator.clipboard.writeText(url);
      toast('지도 링크를 복사했습니다!');
    } catch {
      toast('복사 실패 — 주소창의 URL을 직접 복사하세요.');
    }
  });
}

// 접속 시 해시가 있으면 그 위치로 시작
export function parseHash() {
  const m = location.hash.match(/^#(-?[\d.]+),(-?[\d.]+),(\d+)$/);
  if (!m) return null;
  return { lat: Number(m[1]), lng: Number(m[2]), level: Number(m[3]) };
}
