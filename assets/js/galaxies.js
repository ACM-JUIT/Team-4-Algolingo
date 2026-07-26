import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { createAvatar, renderEmptyState, renderErrorState, renderLoadingGrid, showToast, statusClass } from "./ui.js";
import { escapeHtml, formatPercentage, qs } from "./utils.js";

function renderGalaxyCard(galaxy) {
  const status = galaxy.is_locked ? "LOCKED" : "UNLOCKED";
  return `
    <article class="list-card">
      <div class="list-card-head">
        <div class="user-stack">
          ${createAvatar(galaxy.name, galaxy.icon_url, true)}
          <div>
            <h2 class="list-card-title">${escapeHtml(galaxy.name)}</h2>
            <div class="list-card-meta">
              <span>${escapeHtml(galaxy.programming_language || "Language not specified")}</span>
              <span>·</span>
              <span>${escapeHtml(galaxy.total_planets)} planets</span>
            </div>
          </div>
        </div>
        <span class="${statusClass(status)}">${escapeHtml(status.replaceAll("_", " "))}</span>
      </div>
      <p class="list-card-description">${escapeHtml(galaxy.description || "No description is available for this galaxy yet.")}</p>
      <div class="progress-stack">
        <div class="progress-labels">
          <span>${escapeHtml(galaxy.completed_planets)} of ${escapeHtml(galaxy.total_planets)} planets completed</span>
          <span>${escapeHtml(formatPercentage(galaxy.progress_percent))}</span>
        </div>
        <div class="progress-bar"><span style="width:${galaxy.progress_percent}%"></span></div>
      </div>
      <div class="inline">
        <a class="button button-primary" href="./galaxy.html?id=${galaxy.id}">Open galaxy</a>
      </div>
    </article>
  `;
}

async function loadGalaxies() {
  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "galaxies",
    title: "Galaxies",
    subtitle: "Explore the backend-defined learning worlds and their planet progression paths.",
    actions: '<a class="button button-secondary" href="./dashboard.html">Back to dashboard</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(2);

  try {
    const payload = await api.get("/galaxies");
    const galaxies = payload.data;
    content.innerHTML = galaxies.length
      ? `<section class="collection-grid">${galaxies.map(renderGalaxyCard).join("")}</section>`
      : renderEmptyState({
          icon: "🌌",
          title: "No galaxies available",
          text: "The backend did not return any galaxies yet. Seed data may still be pending."
        });
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadGalaxies);
    showToast({ type: "error", title: "Could not load galaxies", message: error.message });
  }
}

loadGalaxies();
