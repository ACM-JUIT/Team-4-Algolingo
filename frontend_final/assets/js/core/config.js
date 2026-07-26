export const STORAGE_KEYS = {
  session: 'algolingo-final:session',
  apiBaseUrl: 'algolingo-final:api-base-url',
  sidebarCollapsed: 'algolingo-final:sidebar-collapsed',
  practiceDraftPrefix: 'algolingo-final:practice-draft:',
  novaSessions: 'algolingo-final:nova-sessions'
};

export const PUBLIC_PAGES = new Set(['index.html', 'login.html', 'register.html', 'forgot-password.html', '401.html', '403.html', '404.html', '500.html', 'offline.html']);

export function getDefaultApiBaseUrl() {
  const hostname = window.location.hostname || 'localhost';
  const protocol = ['http:', 'https:'].includes(window.location.protocol) ? window.location.protocol : 'http:';
  return `${protocol}//${hostname}:8000/api/v1`;
}
