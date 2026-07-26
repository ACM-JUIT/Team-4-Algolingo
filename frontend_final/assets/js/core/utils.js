export const qs = (selector, scope = document) => scope.querySelector(selector);
export const qsa = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));

export function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

export function createElementFromHtml(html) {
  const template = document.createElement('template');
  template.innerHTML = html.trim();
  return template.content.firstElementChild;
}

export function getInitials(name = 'AlgoLingo') {
  return String(name)
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join('');
}

export function formatDate(value) {
  if (!value) return '—';
  return new Intl.DateTimeFormat(undefined, { year: 'numeric', month: 'short', day: 'numeric' }).format(new Date(value));
}

export function formatDateTime(value) {
  if (!value) return '—';
  return new Intl.DateTimeFormat(undefined, { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }).format(new Date(value));
}

export function formatRelativeTime(value) {
  if (!value) return '—';
  const diff = new Date(value).getTime() - Date.now();
  const absSeconds = Math.round(Math.abs(diff) / 1000);
  const rtf = new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' });
  if (absSeconds < 60) return rtf.format(Math.round(diff / 1000), 'second');
  const absMinutes = Math.round(absSeconds / 60);
  if (absMinutes < 60) return rtf.format(Math.round(diff / 60000), 'minute');
  const absHours = Math.round(absMinutes / 60);
  if (absHours < 24) return rtf.format(Math.round(diff / 3600000), 'hour');
  const absDays = Math.round(absHours / 24);
  return rtf.format(Math.round(diff / 86400000), 'day');
}

export function formatPercentage(value) {
  const number = Number(value) || 0;
  return `${Number.isInteger(number) ? number : number.toFixed(2)}%`;
}

export function pluralize(count, singular, plural = `${singular}s`) {
  return `${count} ${count === 1 ? singular : plural}`;
}

export function parseQuery() {
  return new URLSearchParams(window.location.search);
}

export function getQueryParam(name, fallback = null) {
  const params = parseQuery();
  return params.get(name) || fallback;
}

export function getRequiredQueryParam(name, fallback = null) {
  const value = getQueryParam(name, fallback);
  return value == null ? fallback : value;
}

export function updateQueryParams(values) {
  const url = new URL(window.location.href);
  Object.entries(values).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') url.searchParams.delete(key);
    else url.searchParams.set(key, value);
  });
  window.history.replaceState({}, '', url);
}

export function copyToClipboard(text) {
  return navigator.clipboard?.writeText(text) || Promise.reject(new Error('Clipboard unavailable'));
}

export function debounce(callback, delay = 220) {
  let timeoutId;
  return (...args) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => callback(...args), delay);
  };
}

export function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}
