import { STORAGE_KEYS, getDefaultApiBaseUrl } from "./config.js";

export function loadJson(key, fallback = null) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

export function saveJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

export function removeItem(key) {
  localStorage.removeItem(key);
}

export function getThemePreference() {
  return localStorage.getItem(STORAGE_KEYS.theme);
}

export function setThemePreference(theme) {
  localStorage.setItem(STORAGE_KEYS.theme, theme);
}

export function getSession() {
  return loadJson(STORAGE_KEYS.session, null);
}

export function setSession(session) {
  saveJson(STORAGE_KEYS.session, session);
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
  localStorage.setItem(STORAGE_KEYS.apiBaseUrl, url.trim().replace(/\/$/, ""));
}

export function getPracticeDraftKey(practiceId) {
  return `${STORAGE_KEYS.practiceDraftPrefix}${practiceId}`;
}

export function getNovaSessionMap() {
  return loadJson(STORAGE_KEYS.novaSessions, {});
}

export function setNovaSessionMap(map) {
  saveJson(STORAGE_KEYS.novaSessions, map);
}
