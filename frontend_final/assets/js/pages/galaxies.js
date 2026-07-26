import { api } from '../core/api.js';
import { ensureAuthenticated } from '../core/auth.js';
import { icon } from '../core/icons.js';
import { initializePrivateLayout } from '../core/layout.js';
import { renderEmptyState, renderErrorState, renderLoadingGrid, showToast, statusClass } from '../core/ui.js';
import { escapeHtml, formatPercentage, qs } from '../core/utils.js';

const ROADMAP_GALAXIES = [
  {
    id: 'roadmap-c',
    name: 'C',
    description: 'Upcoming low-level programming track focused on memory, control flow, and systems thinking.',
    programming_language: 'C',
    order_number: 2,
    is_locked: true,
    total_planets: 6,
    completed_planets: 0,
    progress_percent: 0,
    roadmap: true,
    unlock_note: 'Planned upcoming track'
  },
  {
    id: 'roadmap-cpp',
    name: 'C++',
    description: 'Planned object-oriented and performance-focused journey for deeper problem solving and application design.',
    programming_language: 'C++',
    order_number: 3,
    is_locked: true,
    total_planets: 7,
    completed_planets: 0,
    progress_percent: 0,
    roadmap: true,
    unlock_note: 'Planned upcoming track'
  },
  {
    id: 'roadmap-java',
    name: 'Java',
    description: 'A future structured learning path for classes, enterprise fundamentals, and application architecture.',
    programming_language: 'Java',
    order_number: 4,
    is_locked: true,
    total_planets: 6,
    completed_planets: 0,
    progress_percent: 0,
    roadmap: true,
    unlock_note: 'Planned upcoming track'
  }
];

const GALAXY_MOODS = {
  python: { tone: 'python', aura: 'Lush foundational systems and living knowledge routes.' },
  c: { tone: 'c', aura: 'Industrial forge atmosphere and low-level mechanical precision.' },
  'c++': { tone: 'cpp', aura: 'Advanced engineering arcs with layered technological motion.' },
  java: { tone: 'java', aura: 'A rising city-world of stable structures and modular systems.' }
};

function mergeRoadmapGalaxies(apiGalaxies) {
  const seenNames = new Set(apiGalaxies.map((item) => String(item.name).toLowerCase()));
  const extras = ROADMAP_GALAXIES.filter((item) => !seenNames.has(item.name.toLowerCase()));
  return [...apiGalaxies, ...extras].sort((a, b) => a.order_number - b.order_number);
}

function moodForGalaxy(galaxy) {
  return GALAXY_MOODS[String(galaxy.programming_language || galaxy.name).toLowerCase()] || { tone: 'python', aura: 'A developing route in the expanding AlgoLingo universe.' };
}

function renderRoadmapStrip(galaxies) {
  return `
    <section class="galaxy-roadmap">
      ${galaxies.map((galaxy) => {
        const isLocked = Boolean(galaxy.is_locked);
        const isCompleted = galaxy.completed_planets === galaxy.total_planets && galaxy.total_planets > 0;
        const isCurrent = !isLocked && !isCompleted && galaxy.progress_percent > 0;
        return `
          <article class="galaxy-roadmap-card">
            <div class="inline" style="justify-content:space-between;align-items:center;gap:.6rem;">
              <strong>${escapeHtml(galaxy.name)}</strong>
              <span class="${statusClass(isLocked ? 'LOCKED' : isCompleted ? 'COMPLETED' : isCurrent ? 'IN_PROGRESS' : 'UNLOCKED')}">${isLocked ? 'Locked' : isCompleted ? 'Completed' : isCurrent ? 'Current' : 'Open'}</span>
            </div>
            <div class="activity-note">${escapeHtml(galaxy.programming_language || galaxy.name)} · ${escapeHtml(galaxy.total_planets)} planets</div>
          </article>
        `;
      }).join('')}
    </section>
  `;
}

function renderGalaxySector(galaxy) {
  const isLocked = Boolean(galaxy.is_locked);
  const isCompleted = galaxy.completed_planets === galaxy.total_planets && galaxy.total_planets > 0;
  const isCurrent = !isLocked && !isCompleted && galaxy.progress_percent > 0;
  const stateKey = isLocked ? 'LOCKED' : isCompleted ? 'COMPLETED' : isCurrent ? 'IN_PROGRESS' : 'UNLOCKED';
  const stateLabel = isLocked ? `${icon('lock')}Locked` : isCompleted ? `${icon('check')}Completed` : isCurrent ? `${icon('planet')}Current path` : 'Unlocked';
  const mood = moodForGalaxy(galaxy);

  return `
    <article class="galaxy-sector galaxy-sector--${mood.tone} ${isLocked ? 'is-locked' : ''}">
      <div class="galaxy-sector-visual">
        <div class="galaxy-sector-orbit orbit-a"></div>
        <div class="galaxy-sector-orbit orbit-b"></div>
        <div class="galaxy-sector-core"></div>
        <div class="galaxy-sector-satellite satellite-a"></div>
        <div class="galaxy-sector-satellite satellite-b"></div>
      </div>
      <div class="galaxy-sector-copy">
        <div class="galaxy-sector-header">
          <div>
            <p class="eyebrow">Galaxy ${escapeHtml(galaxy.order_number)}</p>
            <h2 class="section-title galaxy-sector-title">${escapeHtml(galaxy.name)}</h2>
            <p class="galaxy-sector-language">${escapeHtml(galaxy.programming_language || galaxy.name)}</p>
          </div>
          <span class="${statusClass(stateKey)}">${stateLabel}</span>
        </div>
        <p class="galaxy-sector-description">${escapeHtml(galaxy.description || mood.aura)}</p>
        <div class="galaxy-sector-meta">
          <div class="galaxy-sector-meta-item"><span class="metric-label">Planets</span><strong>${escapeHtml(galaxy.total_planets)}</strong></div>
          <div class="galaxy-sector-meta-item"><span class="metric-label">State</span><strong>${isLocked ? 'Locked' : isCompleted ? 'Completed' : isCurrent ? 'Current' : 'Open'}</strong></div>
        </div>
        <div class="progress-stack">
          <div class="progress-labels"><span>Completion</span><span>${escapeHtml(formatPercentage(galaxy.progress_percent))}</span></div>
          <div class="progress-bar"><span style="width:${galaxy.progress_percent}%"></span></div>
        </div>
        <div class="galaxy-sector-footer">
          <p class="artifact-card-note">${galaxy.roadmap ? escapeHtml(galaxy.unlock_note) : isLocked ? 'Visible in the roadmap but not yet available.' : `${escapeHtml(galaxy.completed_planets)} of ${escapeHtml(galaxy.total_planets)} planets complete.`}</p>
          ${galaxy.roadmap ? `<button class="button button-secondary" disabled>${icon('lock')}Coming soon</button>` : `<a class="button ${isLocked ? 'button-secondary' : 'button-primary'}" href="./galaxy.html?id=${galaxy.id}">${isLocked ? `${icon('lock')}View route` : `${icon('galaxy')}Enter galaxy`}</a>`}
        </div>
      </div>
    </article>
  `;
}

function renderGalaxyPage(galaxies) {
  const unlocked = galaxies.filter((item) => !item.is_locked).length;
  const locked = galaxies.filter((item) => item.is_locked).length;

  return `
    <section class="galaxy-shell">
      <section class="detail-grid galaxy-hero-grid">
        <div class="card stack galaxy-overview-card">
          <div>
            <p class="eyebrow">Galaxy map</p>
            <h2 class="landing-system-title">Plot a course through live systems, future routes, and locked destinations.</h2>
            <p class="page-subtitle">Only the routes that are truly open today can be entered, but the explorer still sees the larger universe ahead.</p>
          </div>
          <div class="metric-ribbon">
            <div class="segment surface-soft"><div class="metric-label">Total galaxies</div><div class="metric-value">${galaxies.length}</div><div class="metric-meta">Visible across the star atlas.</div></div>
            <div class="segment surface-soft"><div class="metric-label">Unlocked now</div><div class="metric-value">${unlocked}</div><div class="metric-meta">Accessible for exploration.</div></div>
            <div class="segment surface-soft"><div class="metric-label">Locked ahead</div><div class="metric-value">${locked}</div><div class="metric-meta">Future destinations still visible.</div></div>
          </div>
          ${renderRoadmapStrip(galaxies)}
        </div>

        <aside class="card stack galaxy-guide-card">
          <div class="section-header">
            <div>
              <h2 class="section-title">Route states</h2>
              <p class="section-description">Each visible galaxy tells you whether it is active, future, or fully secured.</p>
            </div>
          </div>
          <div class="dashboard-mini-facts">
            <div class="dashboard-mini-row"><span>Unlocked</span><strong>Available for immediate exploration</strong></div>
            <div class="dashboard-mini-row"><span>Current</span><strong>Your active language path</strong></div>
            <div class="dashboard-mini-row"><span>Locked</span><strong>Visible but not yet accessible</strong></div>
            <div class="dashboard-mini-row"><span>Completed</span><strong>All planets already secured</strong></div>
          </div>
        </aside>
      </section>

      <section class="galaxy-sector-grid">
        ${galaxies.map(renderGalaxySector).join('')}
      </section>
    </section>
  `;
}

async function loadGalaxies() {
  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: 'galaxies',
    title: 'Galaxy Map',
    subtitle: 'Browse every visible learning galaxy, including routes that are still locked ahead.',
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon('dashboard')}Mission Control</a>`,
    world: 'galaxies'
  });

  const content = qs('#page-content');
  content.innerHTML = renderLoadingGrid(4);

  try {
    const payload = await api.get('/galaxies');
    const galaxies = mergeRoadmapGalaxies(payload.data);
    content.innerHTML = galaxies.length
      ? renderGalaxyPage(galaxies)
      : renderEmptyState({ iconName: 'galaxy', title: 'No galaxies available', text: 'No galaxies are visible yet. The universe may still be preparing your first route.' });
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs('#retry-action')?.addEventListener('click', loadGalaxies);
    showToast({ type: 'error', title: 'Galaxy map unavailable', message: error.message });
  }
}

loadGalaxies();
