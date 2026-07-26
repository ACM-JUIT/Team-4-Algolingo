import { STORAGE_KEYS } from "./config.js";
import { qs } from "./utils.js";

export function getResolvedTheme() {
  const stored = localStorage.getItem(STORAGE_KEYS.theme);
  if (stored === "light" || stored === "dark") return stored;
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  localStorage.setItem(STORAGE_KEYS.theme, theme);
}

export function toggleTheme() {
  const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(next);
  return next;
}

export function initializeThemeToggle(scope = document) {
  const button = qs("[data-theme-toggle]", scope);
  if (!button) return;
  const syncLabel = () => {
    const theme = document.documentElement.dataset.theme || getResolvedTheme();
    button.setAttribute("aria-pressed", String(theme === "dark"));
    const label = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
    button.setAttribute("aria-label", label);
    const textNode = qs("[data-theme-toggle-label]", button);
    if (textNode) textNode.textContent = theme === "dark" ? "Dark" : "Light";
  };
  button.addEventListener("click", () => {
    toggleTheme();
    syncLabel();
  });
  syncLabel();
}
