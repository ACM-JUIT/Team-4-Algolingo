import { api, request, setAuthFailureHandler } from "./api.js";
import { clearSession, getSession, setSession } from "./storage.js";
import { showToast } from "./ui.js";

let currentUser = getSession()?.user ?? null;

function currentLocationValue() {
  return `${window.location.pathname}${window.location.search}${window.location.hash}`;
}

export function getSessionData() {
  return getSession();
}

export function getCurrentUser() {
  return currentUser || getSession()?.user || null;
}

export function isAuthenticated() {
  const session = getSession();
  return Boolean(session?.tokens?.access_token && session?.tokens?.refresh_token);
}

export function saveAuthSession(session) {
  setSession(session);
  currentUser = session.user;
}

export function clearAuthSession() {
  currentUser = null;
  clearSession();
}

export function redirectToLogin(message = "Please sign in to continue.") {
  if (window.location.pathname.endsWith("login.html")) return;
  const next = encodeURIComponent(currentLocationValue());
  window.location.href = `./login.html?next=${next}&message=${encodeURIComponent(message)}`;
}

export async function fetchCurrentUser() {
  const payload = await api.get("/auth/me");
  const session = getSession();
  const nextSession = {
    ...(session || {}),
    user: payload.data.user,
    tokens: session?.tokens || null
  };
  saveAuthSession(nextSession);
  return payload.data.user;
}

export async function ensureAuthenticated() {
  if (!isAuthenticated()) {
    redirectToLogin();
    return null;
  }
  try {
    return await fetchCurrentUser();
  } catch (error) {
    redirectToLogin(error.message || "Your session has expired. Please sign in again.");
    return null;
  }
}

export async function redirectIfAuthenticated(destination = "./dashboard.html") {
  if (!isAuthenticated()) return false;
  try {
    await fetchCurrentUser();
    window.location.href = destination;
    return true;
  } catch {
    clearAuthSession();
    return false;
  }
}

export async function loginUser(credentials) {
  const payload = await request("/auth/login", {
    method: "POST",
    auth: false,
    body: credentials
  });
  saveAuthSession(payload.data);
  return payload.data;
}

export async function registerUser(formData) {
  const payload = await request("/auth/register", {
    method: "POST",
    auth: false,
    body: formData
  });
  saveAuthSession(payload.data);
  return payload.data;
}

export async function logoutUser({ redirect = true } = {}) {
  const session = getSession();
  try {
    if (session?.tokens?.refresh_token) {
      await api.post("/auth/logout", { refresh_token: session.tokens.refresh_token });
    }
  } catch {
    // Intentionally ignore logout API failures so local sign-out always completes.
  } finally {
    clearAuthSession();
  }

  if (redirect) {
    window.location.href = "./login.html?message=You%20have%20been%20signed%20out.";
  }
}

export function getPostAuthRedirect() {
  const params = new URLSearchParams(window.location.search);
  const next = params.get("next");
  return next || "./dashboard.html";
}

setAuthFailureHandler((error) => {
  clearAuthSession();
  showToast({
    type: "warning",
    title: "Session expired",
    message: error?.message || "Please sign in again."
  });
});
