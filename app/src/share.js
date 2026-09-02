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
  const lat = Number(m[1]);
  const lng = Number(m[2]);
  const level = Number(m[3]);
  // 이상한 링크(#.,.,7 같은)로 들어와도 지도가 깨지지 않게 범위를 확인한다
  if (!Number.isFinite(lat) || lat < -90 || lat > 90) return null;
  if (!Number.isFinite(lng) || lng < -180 || lng > 180) return null;
  if (!Number.isInteger(level) || level < 1 || level > 14) return null;
  return { lat, lng, level };
}
