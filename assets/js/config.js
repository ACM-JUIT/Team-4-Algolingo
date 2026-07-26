export const STORAGE_KEYS = {
  theme: "algolingo:theme",
  session: "algolingo:session",
  apiBaseUrl: "algolingo:api-base-url",
  practiceDraftPrefix: "algolingo:practice-draft:",
  novaSessions: "algolingo:nova-sessions"
};

export const PUBLIC_ROUTES = new Set(["login.html", "register.html"]);

export function getDefaultApiBaseUrl() {
  const hostname = window.location.hostname || "localhost";
  const protocol = ["http:", "https:"].includes(window.location.protocol) ? window.location.protocol : "http:";
  return `${protocol}//${hostname}:8000/api/v1`;
}
