// 장소 데이터 저장소 — localStorage 영속화 + 구독(pub/sub)
import { DEFAULT_PLACES } from './defaultPlaces.js';

const STORAGE_KEY = 'my-map-places-v1';
const listeners = [];

let places = load();

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
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
    for (const p of data) {
      if (typeof p.name !== 'string' || typeof p.lat !== 'number' || typeof p.lng !== 'number') {
        throw new Error('name/lat/lng 형식이 올바르지 않은 항목이 있습니다.');
      }
    }
    places = data;
    save();
  },
};
