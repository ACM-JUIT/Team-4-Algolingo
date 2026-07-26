import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { createAvatar, renderErrorState, renderLoadingGrid, showToast, statusClass } from "../core/ui.js";
import { escapeHtml, formatPercentage, getRequiredQueryParam, qs } from "../core/utils.js";

function difficultyLabel(value) {
  return `Difficulty ${value}`;
}

function renderPlanetCard(planet) {
  const isLocked = planet.status === "LOCKED";
  const isCompleted = planet.status === "COMPLETED";
  return `
    <article class="list-card ${isLocked ? "surface-soft" : ""}">
      <div class="list-card-head">
        <div>
          <p class="eyebrow">Planet ${escapeHtml(planet.order_number)}</p>
          <h2 class="list-card-title">${escapeHtml(planet.name)}</h2>
          <div class="list-card-meta">
            <span>${icon("spark")} ${escapeHtml(difficultyLabel(planet.difficulty))}</span>
            <span>${icon("book")} ${escapeHtml(planet.discoveries_count)} discoveries</span>
            <span>${icon("mission")} ${escapeHtml(planet.practices_count)} missions</span>
            <span>${icon("target")} ${escapeHtml(planet.quiz_questions_count)} briefing questions</span>
          </div>
        </div>
        <span class="${statusClass(planet.status)}">${isLocked ? `${icon("lock")} Locked` : isCompleted ? `${icon("check")} Completed` : escapeHtml(planet.status.replaceAll("_", " "))}</span>
      </div>
      <p class="list-card-description">${escapeHtml(planet.tagline || planet.description || "No description available.")}</p>
      <div class="summary-grid">
        <div class="segment surface-soft">
          <div class="metric-label">XP reward</div>
          <div class="metric-value">${planet.xp_total}</div>
          <div class="metric-meta">Total XP tied to this planet.</div>
        </div>
        <div class="segment surface-soft">
          <div class="metric-label">Estimated time</div>
          <div class="metric-value">${planet.estimated_time_minutes ?? "—"}</div>
          <div class="metric-meta">Minutes for the overall path.</div>
        </div>
      </div>
      <div class="progress-stack">
        <div class="progress-labels"><span>Completion</span><span>${escapeHtml(formatPercentage(planet.progress_percent))}</span></div>
        <div class="progress-bar"><span style="width:${planet.progress_percent}%"></span></div>
      </div>
      <div class="callout ${isLocked ? "warning" : isCompleted ? "success" : "info"}">${escapeHtml(planet.unlock_condition || "Available now")}</div>
      <div class="inline">
        <a class="button ${isLocked ? "button-secondary" : "button-primary"}" href="./planet.html?id=${planet.id}">${isLocked ? `${icon("lock")}View planet` : `${icon("rocket")}Open planet`}</a>
      </div>
    </article>
  `;
}

function renderGalaxyDetail(galaxy) {
  const completedPlanets = galaxy.planets.filter((planet) => planet.status === "COMPLETED").length;
  const unlockedPlanets = galaxy.planets.filter((planet) => planet.status !== "LOCKED").length;

  return `
    <section class="hero-surface stack">
      <div class="hero-grid">
        <div class="stack">
          <div class="user-stack" style="align-items: flex-start;">
            ${createAvatar(galaxy.name, galaxy.icon_url, true)}
            <div>
              <p class="eyebrow">${escapeHtml(galaxy.programming_language || "Programming language")}</p>
              <h2 class="page-title" style="font-size: clamp(1.9rem, 1.45rem + 1vw, 2.7rem);">${escapeHtml(galaxy.name)}</h2>
              <p class="page-subtitle">${escapeHtml(galaxy.description || "Travel every planet in this learning galaxy.")}</p>
            </div>
          </div>
          <div class="metric-ribbon">
            <div class="segment surface-soft">
              <div class="metric-label">Planets</div>
              <div class="metric-value">${galaxy.planets.length}</div>
            </div>
            <div class="segment surface-soft">
              <div class="metric-label">Unlocked now</div>
              <div class="metric-value">${unlockedPlanets}</div>
            </div>
            <div class="segment surface-soft">
              <div class="metric-label">Completed</div>
              <div class="metric-value">${completedPlanets}</div>
            </div>
          </div>
        </div>
        <div class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Progression model</h2>
              <p class="section-description">Planets unlock in sequence as your route through the galaxy strengthens.</p>
            </div>
          </div>
          <div class="info-list">
            <div class="info-row"><span>Current state</span><strong>${galaxy.is_locked ? "Locked" : "Visible"}</strong></div>
            <div class="info-row"><span>Planet order</span><strong>Linear progression</strong></div>
            <div class="info-row"><span>Future content</span><strong>Shown even when locked</strong></div>
          </div>
        </div>
      </div>
    </section>

    <section class="planet-grid">
      ${galaxy.planets.map(renderPlanetCard).join("")}
    </section>
  `;
}

async function loadGalaxyDetail() {
  const galaxyId = getRequiredQueryParam("id");
  if (!galaxyId) {
    window.location.href = "./galaxies.html";
    return;
  }

  const user = await ensureAuthenticated();
  if (!user) return;
  initializePrivateLayout({
    user,
    activeNav: "galaxies",
    title: "Galaxy",
    subtitle: "Loading the current galaxy…",
    actions: `<a class="button button-secondary" href="./galaxies.html">${icon("galaxy")}All galaxies</a>`
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);

  try {
    const payload = await api.get(`/galaxies/${galaxyId}`);
    const galaxy = payload.data;
    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: galaxy.name,
      subtitle: galaxy.description || "Travel every planet in this learning galaxy.",
      actions: `<a class="button button-secondary" href="./galaxies.html">${icon("chevronLeft")}All galaxies</a>`
    });

    content.innerHTML = renderGalaxyDetail(galaxy);
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadGalaxyDetail);
    showToast({ type: "error", title: "Galaxy unavailable", message: error.message });
  }
}

loadGalaxyDetail();
