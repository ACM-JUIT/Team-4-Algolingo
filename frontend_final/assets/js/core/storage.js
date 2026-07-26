import { STORAGE_KEYS, getDefaultApiBaseUrl } from './config.js';

export function readJson(key, fallback = null) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export function writeJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

export function removeItem(key) {
  localStorage.removeItem(key);
}

export function getSession() {
  return readJson(STORAGE_KEYS.session, null);
}

export function setSession(session) {
  writeJson(STORAGE_KEYS.session, session);
}

export function clearSession() {
  removeItem(STORAGE_KEYS.session);
}

export function getApiBaseUrl() {
  return localStorage.getItem(STORAGE_KEYS.apiBaseUrl) || getDefaultApiBaseUrl();
}

export function setApiBaseUrl(url) {
  if (!url) {
    removeItem(STORAGE_KEYS.apiBaseUrl);
    return;
  }
  localStorage.setItem(STORAGE_KEYS.apiBaseUrl, url.trim().replace(/\/$/, ''));
}

export function getPracticeDraftKey(practiceId) {
  return `${STORAGE_KEYS.practiceDraftPrefix}${practiceId}`;
}

export function getNovaSessionMap() {
  return readJson(STORAGE_KEYS.novaSessions, {});
}

export function setNovaSessionMap(map) {
  writeJson(STORAGE_KEYS.novaSessions, map);
}
