import { logoutUser } from './auth.js';
import { icon } from './icons.js';
import { createAvatar, showToast } from './ui.js';
import { qs, qsa, escapeHtml } from './utils.js';
import { mountAmbientWorld } from './ambient.js';
import { STORAGE_KEYS } from './config.js';

function renderWordmark(size = 'sm') {
  return `<span class="brand-wordmark brand-wordmark--${size}">AlgoLingo</span>`;
}

const NAV_ITEMS = [
  {
    label: 'Navigation',
    items: [
      { key: 'dashboard', href: './dashboard.html', label: 'Mission Control', iconName: 'dashboard' },
      { key: 'galaxies', href: './galaxies.html', label: 'Galaxy Map', iconName: 'galaxy' },
      { key: 'search', href: './search.html', label: 'Star Search', iconName: 'search' },
      { key: 'nova', href: './nova.html', label: 'NOVA', iconName: 'nova' }
    ]
  },
  {
    label: 'Journey',
    items: [
      { key: 'leaderboard', href: './leaderboard.html', label: 'Constellation Rank', iconName: 'leaderboard' },
      { key: 'achievements', href: './achievements.html', label: 'Achievement Vault', iconName: 'trophy' },
      { key: 'artifacts', href: './artifacts.html', label: 'Artifact Museum', iconName: 'artifact' }
    ]
  },
  {
    label: 'Explorer',
    items: [
      { key: 'notifications', href: './notifications.html', label: 'Signal Archive', iconName: 'bell' },
      { key: 'profile', href: './profile.html', label: 'Logbook', iconName: 'profile' },
      { key: 'settings', href: './settings.html', label: 'Settings', iconName: 'settings' }
    ]
  }
];

function isSidebarCollapsed() {
  return localStorage.getItem(STORAGE_KEYS.sidebarCollapsed) === 'true';
}

function setSidebarCollapsed(next) {
  localStorage.setItem(STORAGE_KEYS.sidebarCollapsed, String(next));
  document.body.classList.toggle('sidebar-collapsed', next);
}

function renderSidebar(user, activeNav) {
  return `
    <div class="sidebar-header">
      <a class="sidebar-brand" href="./dashboard.html" aria-label="AlgoLingo home">${renderWordmark('sm')}</a>
      <button class="button button-ghost sidebar-toggle" data-sidebar-toggle aria-label="Collapse star map rail">${icon('chevronLeft')}</button>
    </div>
    <div class="sidebar-scroll">
      ${NAV_ITEMS.map((group) => `
        <section class="nav-group">
          <div class="nav-label">${escapeHtml(group.label)}</div>
          ${group.items.map((item) => `
            <a class="nav-link ${item.key === activeNav ? 'is-active' : ''}" href="${item.href}" ${item.key === activeNav ? 'aria-current="page"' : ''}>
              ${icon(item.iconName)}
              <span class="nav-link-label">${escapeHtml(item.label)}</span>
            </a>
          `).join('')}
        </section>
      `).join('')}
    </div>
    <div class="sidebar-footer">
      <div class="sidebar-user">
        ${createAvatar(user.username, user.avatar_url)}
        <div class="sidebar-user-copy">
          <strong>${escapeHtml(user.username)}</strong>
          <span>${escapeHtml(user.rank_title)} · Level ${escapeHtml(user.level)}</span>
        </div>
      </div>
      <button class="button button-secondary sidebar-logout" data-logout-trigger>${icon('logout')}<span class="sidebar-logout-label">Exit orbit</span></button>
    </div>
  `;
}

function buildNotifications(user) {
  return [
    {
      title: user.streak_days > 0 ? `${user.streak_days}-day streak active` : 'Begin your first streak',
      body: user.streak_days > 0 ? 'Complete one guided action today to keep your route glowing.' : 'Complete any discovery today to start your first orbit streak.'
    },
    {
      title: 'NOVA is online',
      body: 'Use your onboard guide whenever you need an explanation, hint, or debugging pass.'
    },
    {
      title: 'Artifact path available',
      body: 'Planet mastery and successful boss battles open the museum of earned relics.'
    }
  ];
}

function renderNotificationsMenu(user) {
  const notices = buildNotifications(user);
  return `
    <div class="shell-menu" data-shell-menu="signals">
      <button class="button button-secondary shell-trigger" data-shell-trigger="signals" aria-label="Open signals" aria-expanded="false">${icon('bell')}<span class="shell-dot"></span></button>
      <div class="shell-panel" data-shell-panel="signals" hidden>
        <div class="shell-panel-header">
          <div><strong>Signals</strong><span>Ambient reminders from your journey</span></div>
        </div>
        <div class="shell-panel-list">
          ${notices.map((notice) => `
            <article class="shell-notice">
              <strong>${escapeHtml(notice.title)}</strong>
              <p>${escapeHtml(notice.body)}</p>
            </article>
          `).join('')}
          <a class="shell-action" href="./notifications.html">${icon('bell')}Open signal archive</a>
        </div>
      </div>
    </div>
  `;
}

function renderProfileMenu(user) {
  return `
    <div class="shell-menu" data-shell-menu="profile">
      <button class="shell-user-trigger" data-shell-trigger="profile" aria-expanded="false">
        ${createAvatar(user.username, user.avatar_url)}
        <div class="topbar-user-copy">
          <strong>${escapeHtml(user.username)}</strong>
          <span>${escapeHtml(user.rank_title)} · Explorer</span>
        </div>
        ${icon('chevronDown')}
      </button>
      <div class="shell-panel profile-panel" data-shell-panel="profile" hidden>
        <div class="shell-panel-header profile-panel-header">
          ${createAvatar(user.username, user.avatar_url)}
          <div>
            <strong>${escapeHtml(user.username)}</strong>
            <span>${escapeHtml(user.email)}</span>
          </div>
        </div>
        <div class="shell-panel-list">
          <a class="shell-action" href="./profile.html">${icon('profile')}Open logbook</a>
          <a class="shell-action" href="./settings.html">${icon('settings')}Adjust workspace</a>
          <button class="shell-action shell-action-danger" data-logout-trigger>${icon('logout')}Exit orbit</button>
        </div>
      </div>
    </div>
  `;
}

function renderTopbar(user, activeNav) {
  return `
    <div class="topbar-left">
      <button class="button button-secondary mobile-menu-button" data-mobile-menu-toggle aria-label="Open star map rail">${icon('menu')}</button>
      <div class="topbar-context">
        <strong>Learning universe</strong>
        <span id="network-status">${navigator.onLine ? 'Universe signal stable' : 'Offline · some routes may pause'}</span>
      </div>
    </div>
    <div class="topbar-right">
      <div class="topbar-actions">
        <a class="button ${activeNav === 'search' ? 'button-primary' : 'button-secondary'}" href="./search.html" aria-label="Open star search" ${activeNav === 'search' ? 'aria-current="page"' : ''}>${icon('search')}</a>
        ${renderNotificationsMenu(user)}
      </div>
      ${renderProfileMenu(user)}
    </div>
  `;
}

function closeSidebar() {
  document.body.classList.remove('sidebar-open');
}

function closeShellMenus() {
  qsa('[data-shell-panel]').forEach((panel) => { panel.hidden = true; });
  qsa('[data-shell-trigger]').forEach((trigger) => { trigger.setAttribute('aria-expanded', 'false'); });
}

function bindShellMenus() {
  qsa('[data-shell-trigger]').forEach((trigger) => {
    trigger.addEventListener('click', (event) => {
      event.stopPropagation();
      const key = trigger.dataset.shellTrigger;
      const panel = qs(`[data-shell-panel="${key}"]`);
      const isOpen = trigger.getAttribute('aria-expanded') === 'true';
      closeShellMenus();
      if (!isOpen && panel) {
        panel.hidden = false;
        trigger.setAttribute('aria-expanded', 'true');
      }
    });
  });

  qsa('[data-shell-panel]').forEach((panel) => {
    panel.addEventListener('click', (event) => event.stopPropagation());
  });

  if (!window.__algolingoFinalShellMenusBound) {
    document.addEventListener('click', closeShellMenus);
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        closeShellMenus();
        closeSidebar();
      }
    });
    window.__algolingoFinalShellMenusBound = true;
  }
}

function bindNetworkStatus() {
  const status = qs('#network-status');
  if (!status) return;
  const sync = () => {
    const current = qs('#network-status');
    if (current) current.textContent = navigator.onLine ? 'Universe signal stable' : 'Offline · some routes may pause';
  };
  if (!window.__algolingoFinalNetworkBound) {
    window.addEventListener('online', () => {
      sync();
      showToast({ type: 'success', title: 'Back online', message: 'Your link to the universe has been restored.' });
    });
    window.addEventListener('offline', () => {
      sync();
      showToast({ type: 'warning', title: 'Signal interrupted', message: 'You are offline. Some requests may not complete.' });
    });
    window.__algolingoFinalNetworkBound = true;
  }
  sync();
}

function bindShellInteractions() {
  const collapseButton = qs('[data-sidebar-toggle]');
  const drawerButton = qs('[data-mobile-menu-toggle]');
  const backdrop = qs('#sidebar-backdrop');

  collapseButton?.addEventListener('click', () => {
    const next = !document.body.classList.contains('sidebar-collapsed');
    setSidebarCollapsed(next);
  });

  drawerButton?.addEventListener('click', () => {
    document.body.classList.toggle('sidebar-open');
  });

  backdrop?.addEventListener('click', closeSidebar);

  qsa('.nav-link, .sidebar-brand, .sidebar-logout, .shell-action[href], .topbar-actions a.button').forEach((node) => {
    node.addEventListener('click', () => closeSidebar());
  });

  qsa('[data-logout-trigger]').forEach((button) => button.addEventListener('click', () => logoutUser()));
  bindShellMenus();
  bindNetworkStatus();
}

export function setPageMeta({ title, subtitle = '', actions = '' }) {
  const titleNode = qs('#page-title');
  const subtitleNode = qs('#page-subtitle');
  const actionsNode = qs('#page-actions');
  if (titleNode) titleNode.textContent = title;
  if (subtitleNode) subtitleNode.textContent = subtitle;
  if (actionsNode) actionsNode.innerHTML = actions;
  document.title = `${title} · AlgoLingo`;
}

export function initializePrivateLayout({ user, activeNav, title, subtitle, actions = '', world = activeNav || 'default' }) {
  mountAmbientWorld({ world });
  document.body.classList.add('app-body');
  document.body.classList.toggle('sidebar-collapsed', isSidebarCollapsed());
  const sidebarRoot = qs('#sidebar-root');
  const topbarRoot = qs('#topbar-root');
  if (sidebarRoot) sidebarRoot.innerHTML = renderSidebar(user, activeNav);
  if (topbarRoot) topbarRoot.innerHTML = renderTopbar(user, activeNav);
  setPageMeta({ title, subtitle, actions });
  bindShellInteractions();
}

export function renderPublicBrand(size = 'md') {
  return renderWordmark(size);
}
