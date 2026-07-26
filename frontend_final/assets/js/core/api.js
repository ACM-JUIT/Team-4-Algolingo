import { clearSession, getApiBaseUrl, getSession, setSession } from './storage.js';

export class ApiError extends Error {
  constructor(message, { status = 0, payload = null } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.payload = payload;
  }
}

let authFailureHandler = () => {};
let refreshPromise = null;

export function setAuthFailureHandler(handler) {
  authFailureHandler = handler;
}

function buildUrl(path) {
  const base = getApiBaseUrl().replace(/\/$/, '');
  const normalized = path.startsWith('/') ? path : `/${path}`;
  return `${base}${normalized}`;
}

async function fetchWithTimeout(url, options = {}, timeout = 18000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } catch (error) {
    if (error.name === 'AbortError') throw new ApiError('The request timed out. Please try again.', { status: 0 });
    throw new ApiError('Unable to reach the server. Check your connection and try again.', { status: 0 });
  } finally {
    clearTimeout(timeoutId);
  }
}

async function parseResponse(response) {
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) return response.json();
  const text = await response.text();
  return text ? { message: text } : null;
}

async function refreshTokens() {
  if (refreshPromise) return refreshPromise;
  const session = getSession();
  if (!session?.tokens?.refresh_token) throw new ApiError('Your session has expired. Please sign in again.', { status: 401 });

  refreshPromise = (async () => {
    const response = await fetchWithTimeout(buildUrl('/auth/refresh'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: session.tokens.refresh_token })
    });
    const payload = await parseResponse(response);
    if (!response.ok || payload?.success === false) {
      clearSession();
      throw new ApiError(payload?.message || 'Your session has expired. Please sign in again.', { status: response.status, payload });
    }
    setSession(payload.data);
    return payload.data;
  })();

  try {
    return await refreshPromise;
  } finally {
    refreshPromise = null;
  }
}

export async function request(path, options = {}) {
  const { method = 'GET', headers = {}, body, auth = true, retry = true, timeout = 18000 } = options;
  const requestHeaders = new Headers(headers);

  if (body !== undefined && !requestHeaders.has('Content-Type')) {
    requestHeaders.set('Content-Type', 'application/json');
  }

  if (auth) {
    const session = getSession();
    if (session?.tokens?.access_token) requestHeaders.set('Authorization', `Bearer ${session.tokens.access_token}`);
  }

  const response = await fetchWithTimeout(buildUrl(path), {
    method,
    headers: requestHeaders,
    body: body === undefined ? undefined : requestHeaders.get('Content-Type')?.includes('application/json') ? JSON.stringify(body) : body
  }, timeout);

  const payload = await parseResponse(response);

  if (response.status === 401 && auth && retry) {
    try {
      await refreshTokens();
      return await request(path, { ...options, retry: false });
    } catch (error) {
      clearSession();
      authFailureHandler(error);
      throw error;
    }
  }

  if (!response.ok || payload?.success === false) {
    throw new ApiError(payload?.message || `Request failed with status ${response.status}.`, { status: response.status, payload });
  }

  return payload;
}

export const api = {
  get: (path, options) => request(path, { ...options, method: 'GET' }),
  post: (path, body, options) => request(path, { ...options, method: 'POST', body }),
  patch: (path, body, options) => request(path, { ...options, method: 'PATCH', body })
};
