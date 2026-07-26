import { logoutUser } from "./auth.js";
import { initializeThemeToggle } from "./theme.js";
import { createAvatar } from "./ui.js";
import { escapeHtml, qs } from "./utils.js";

const NAV_ITEMS = [
  {
    label: "Core",
    items: [
      { key: "dashboard", href: "./dashboard.html", label: "Dashboard", icon: "dashboard" },
      { key: "galaxies", href: "./galaxies.html", label: "Galaxies", icon: "galaxy" },
      { key: "leaderboard", href: "./leaderboard.html", label: "Leaderboard", icon: "leaderboard" },
      { key: "artifacts", href: "./artifacts.html", label: "Artifacts", icon: "artifact" },
      { key: "nova", href: "./nova.html", label: "Nova", icon: "nova" }
    ]
  },
  {
    label: "Account",
    items: [
      { key: "profile", href: "./profile.html", label: "Profile", icon: "profile" },
      { key: "settings", href: "./settings.html", label: "Settings", icon: "settings" }
    ]
  }
];

function icon(name) {
  const icons = {
    dashboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 13h6V4H4zM14 20h6v-9h-6zM14 10h6V4h-6zM4 20h6v-3H4z"/></svg>',
    galaxy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="2.5"/><path d="M4.5 13.5c4.5-7 11.5-9 15-6s2 9-2.5 11-11 .5-12-2.5 4-4.5 8-4.5"/></svg>',
    leaderboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 20V10M12 20V4M17 20v-7"/><path d="M4 20h16"/></svg>',
    artifact: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m12 3 7 4v5c0 4.5-3 7-7 9-4-2-7-4.5-7-9V7z"/><path d="m9.5 11.5 1.5 1.5 3.5-3.5"/></svg>',
    nova: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 2v6M12 16v6M4.9 4.9l4.2 4.2M14.9 14.9l4.2 4.2M2 12h6M16 12h6M4.9 19.1l4.2-4.2M14.9 9.1l4.2-4.2"/></svg>',
    profile: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M4 20c1.8-3.3 4.5-5 8-5s6.2 1.7 8 5"/></svg>',
    settings: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 8.5A3.5 3.5 0 1 0 12 15.5A3.5 3.5 0 1 0 12 8.5Z"/><path d="M19.4 15a1 1 0 0 0 .2 1.1l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1 1 0 0 0-1.1-.2 1 1 0 0 0-.6.9V20a2 2 0 1 1-4 0v-.1a1 1 0 0 0-.6-.9 1 1 0 0 0-1.1.2l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1 1 0 0 0 .2-1.1 1 1 0 0 0-.9-.6H4a2 2 0 1 1 0-4h.1a1 1 0 0 0 .9-.6 1 1 0 0 0-.2-1.1l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1 1 0 0 0 1.1.2 1 1 0 0 0 .6-.9V4a2 2 0 1 1 4 0v.1a1 1 0 0 0 .6.9 1 1 0 0 0 1.1-.2l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1 1 0 0 0-.2 1.1 1 1 0 0 0 .9.6H20a2 2 0 1 1 0 4h-.1a1 1 0 0 0-.5.3Z"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    theme: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>',
    logout: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 7V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-3"/><path d="M10 12h11M18 8l4 4-4 4"/></svg>'
  };
  return icons[name] || "";
}

function renderSidebar(user, activeNav) {
  const groups = NAV_ITEMS.map(
    (group) => `
      <section class="nav-group">
        <div class="nav-label">${escapeHtml(group.label)}</div>
        ${group.items
          .map(
            (item) => `
              <a class="nav-link ${item.key === activeNav ? "is-active" : ""}" href="${item.href}">
                ${icon(item.icon)}
                <span>${escapeHtml(item.label)}</span>
              </a>
            `
          )
          .join("")}
      </section>
    `
  ).join("");

  return `
    <div class="sidebar-brand">
      <div class="brand-mark" aria-hidden="true">${icon("nova")}</div>
      <div class="brand-copy">
        <strong>AlgoLingo</strong>
        <span>Python learning platform</span>
      </div>
    </div>
    ${groups}
    <div class="sidebar-footer">
      <div class="sidebar-user">
        ${createAvatar(user.username, user.avatar_url)}
        <div class="sidebar-user-copy">
          <strong>${escapeHtml(user.username)}</strong>
          <span>${escapeHtml(user.rank_title)} · Level ${escapeHtml(user.level)}</span>
        </div>
      </div>
      <button class="button button-ghost button-block" data-logout-trigger>
        ${icon("logout")}
        <span>Logout</span>
      </button>
    </div>
  `;
}

function renderTopbar(user) {
  return `
    <div class="topbar-left">
      <button class="button button-secondary mobile-menu-button" data-mobile-menu-toggle aria-label="Open navigation">
        ${icon("menu")}
      </button>
      <div>
        <strong style="display:block; color: var(--text-strong);">Welcome back</strong>
        <span class="activity-note">Keep your streak moving, ${escapeHtml(user.username)}.</span>
      </div>
    </div>
    <div class="topbar-right">
      <button class="button button-secondary" data-theme-toggle>
        ${icon("theme")}
        <span data-theme-toggle-label>Theme</span>
      </button>
      <div class="topbar-user">
        ${createAvatar(user.username, user.avatar_url)}
        <div class="topbar-user-copy">
          <strong>${escapeHtml(user.username)}</strong>
          <span>${escapeHtml(user.email)}</span>
        </div>
      </div>
    </div>
  `;
}

function bindShellInteractions() {
  const toggleButton = qs("[data-mobile-menu-toggle]");
  const backdrop = qs("#sidebar-backdrop");
  toggleButton?.addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
  });
  backdrop?.addEventListener("click", () => {
    document.body.classList.remove("sidebar-open");
  });

  document.querySelectorAll("[data-logout-trigger]").forEach((button) => {
    button.addEventListener("click", () => logoutUser());
  });

  initializeThemeToggle(document);
}

export function setPageMeta({ title, subtitle = "", actions = "" }) {
  const titleElement = qs("#page-title");
  const subtitleElement = qs("#page-subtitle");
  const actionsElement = qs("#page-actions");
  if (titleElement) titleElement.textContent = title;
  if (subtitleElement) subtitleElement.textContent = subtitle;
  if (actionsElement) actionsElement.innerHTML = actions;
  document.title = `${title} · AlgoLingo`;
}

export function initializePrivateLayout({ user, activeNav, title, subtitle, actions = "" }) {
  const sidebarRoot = qs("#sidebar-root");
  const topbarRoot = qs("#topbar-root");
  if (sidebarRoot) sidebarRoot.innerHTML = renderSidebar(user, activeNav);
  if (topbarRoot) topbarRoot.innerHTML = renderTopbar(user);
  setPageMeta({ title, subtitle, actions });
  bindShellInteractions();
}
