// 카카오 지도 SDK를 동적으로 불러오는 모듈
// autoload=false로 받아서 kakao.maps.load() 콜백 안에서 지도를 만든다.
export function loadKakaoSdk() {
  return new Promise((resolve, reject) => {
    const key = import.meta.env.VITE_KAKAO_JS_KEY;
    if (!key) {
      reject(new Error('VITE_KAKAO_JS_KEY가 .env에 없습니다.'));
      return;
    }
    const script = document.createElement('script');
    script.src =
      `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${key}` +
      `&autoload=false&libraries=services,clusterer`;
    script.onload = () => kakao.maps.load(() => resolve(kakao));
    script.onerror = () => reject(new Error('카카오 SDK 로드 실패 — 키/도메인 확인'));
    document.head.appendChild(script);
  });
}
