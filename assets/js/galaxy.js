import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { createAvatar, renderErrorState, renderLoadingGrid, showToast, statusClass } from "./ui.js";
import { escapeHtml, formatPercentage, getRequiredQueryParam, qs } from "./utils.js";

function difficultyLabel(value) {
  return `Difficulty ${value}`;
}

function renderPlanetCard(planet) {
  return `
    <article class="list-card">
      <div class="list-card-head">
        <div>
          <p class="eyebrow">Planet ${escapeHtml(planet.order_number)}</p>
          <h2 class="list-card-title">${escapeHtml(planet.name)}</h2>
          <div class="list-card-meta">
            <span>${escapeHtml(difficultyLabel(planet.difficulty))}</span>
            <span>·</span>
            <span>${escapeHtml(planet.discoveries_count)} discoveries</span>
            <span>·</span>
            <span>${escapeHtml(planet.practices_count)} practices</span>
            <span>·</span>
            <span>${escapeHtml(planet.quiz_questions_count)} quiz questions</span>
          </div>
        </div>
        <span class="${statusClass(planet.status)}">${escapeHtml(planet.status.replaceAll("_", " "))}</span>
      </div>
      <p class="list-card-description">${escapeHtml(planet.tagline || planet.description || "No description available.")}</p>
      <div class="progress-stack">
        <div class="progress-labels">
          <span>Planet progress</span>
          <span>${escapeHtml(formatPercentage(planet.progress_percent))}</span>
        </div>
        <div class="progress-bar"><span style="width:${planet.progress_percent}%"></span></div>
      </div>
      <div class="callout">Unlock condition: ${escapeHtml(planet.unlock_condition || "Available now")}</div>
      <div class="inline">
        <a class="button button-primary" href="./planet.html?id=${planet.id}">View planet</a>
      </div>
    </article>
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
    actions: '<a class="button button-secondary" href="./galaxies.html">All galaxies</a>'
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
      subtitle: galaxy.description || "Browse every planet in this learning galaxy.",
      actions: '<a class="button button-secondary" href="./galaxies.html">All galaxies</a>'
    });

    content.innerHTML = `
      <section class="hero-surface stack">
        <div class="hero-grid">
          <div class="user-stack" style="align-items: flex-start;">
            ${createAvatar(galaxy.name, galaxy.icon_url, true)}
            <div>
              <p class="eyebrow">${escapeHtml(galaxy.programming_language || "Programming language")}</p>
              <h2 class="page-title" style="font-size: 2rem;">${escapeHtml(galaxy.name)}</h2>
              <p class="page-subtitle">${escapeHtml(galaxy.description || "No description available for this galaxy.")}</p>
            </div>
          </div>
          <div class="card stack">
            <div class="inline" style="justify-content: space-between; align-items: center;">
              <span class="${statusClass(galaxy.is_locked ? "LOCKED" : "UNLOCKED")}">${galaxy.is_locked ? "Locked" : "Unlocked"}</span>
              <span class="badge badge-primary">${escapeHtml(galaxy.planets.length)} planets</span>
            </div>
            <p class="activity-note">Planets unlock sequentially based on your backend progress data.</p>
          </div>
        </div>
      </section>
      <section class="planet-grid">${galaxy.planets.map(renderPlanetCard).join("")}</section>
    `;
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadGalaxyDetail);
    showToast({ type: "error", title: "Galaxy unavailable", message: error.message });
  }
}

loadGalaxyDetail();
