// 장소 데이터 저장소 — localStorage 영속화 + 구독(pub/sub)
import { DEFAULT_PLACES } from './defaultPlaces.js';

const STORAGE_KEY = 'my-map-places-v1';
const listeners = [];

// 어디서 온 데이터든(저장소·가져오기) 화면에 올리기 전에 한 번 걸러낸다.
function normalize(p) {
  if (typeof p !== 'object' || p === null) return null;
  if (typeof p.name !== 'string' || !p.name.trim()) return null;
  const lat = Number(p.lat);
  const lng = Number(p.lng);
  if (!Number.isFinite(lat) || lat < -90 || lat > 90) return null;
  if (!Number.isFinite(lng) || lng < -180 || lng > 180) return null;
  const id = typeof p.id === 'string' && /^[\w-]{1,40}$/.test(p.id)
    ? p.id
    : 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
  let rating = Math.floor(Number(p.rating));
  if (!Number.isFinite(rating)) rating = 0;
  rating = Math.min(5, Math.max(0, rating));
  return {
    id,
    name: p.name.trim().slice(0, 60),
    category: typeof p.category === 'string' ? p.category : 'food',
    lat,
    lng,
    rating,
    memo: typeof p.memo === 'string' ? p.memo.slice(0, 500) : '',
  };
}

let places = load();

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const data = JSON.parse(raw);
      if (Array.isArray(data)) return data.map(normalize).filter(Boolean);
    }
  } catch (e) {
    console.warn('저장 데이터를 읽지 못해 기본 데이터로 시작합니다.', e);
  }
  return structuredClone(DEFAULT_PLACES);
}

function save() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(places));
  } catch (e) {
    console.warn('localStorage 저장 실패', e);
  }
  listeners.forEach((fn) => fn(places));
}

export const store = {
  all() {
    return places;
  },
  get(id) {
    return places.find((p) => p.id === id);
  },
  add(place) {
    const id = 'p' + Date.now().toString(36);
    const item = { id, rating: 0, memo: '', ...place };
    places.push(item);
    save();
    return item;
  },
  update(id, patch) {
    const p = this.get(id);
    if (!p) return;
    Object.assign(p, patch);
    save();
  },
  remove(id) {
    places = places.filter((p) => p.id !== id);
    save();
  },
  replaceAll(next) {
    places = next;
    save();
  },
  subscribe(fn) {
    listeners.push(fn);
  },
  exportJson() {
    return JSON.stringify(places, null, 2);
  },
  importJson(text) {
    const data = JSON.parse(text);
    if (!Array.isArray(data)) throw new Error('배열(JSON)이 아닙니다.');
    const cleaned = data.map(normalize);
    if (cleaned.some((p) => p === null)) {
      throw new Error('name/lat/lng 형식이 올바르지 않은 항목이 있습니다.');
    }
    places = cleaned;
    save();
  },
};
