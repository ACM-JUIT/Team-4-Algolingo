import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { createAvatar, renderEmptyState, renderErrorState, renderLoadingGrid, showToast } from "../core/ui.js";
import { escapeHtml, getRequiredQueryParam, qs, updateQueryParams } from "../core/utils.js";

const state = {
  type: getRequiredQueryParam("type", "global"),
  page: Number(getRequiredQueryParam("page", "1")) || 1,
  galaxyId: getRequiredQueryParam("galaxyId", "") || "",
  galaxies: [],
  currentUser: null
};

function buildLeaderboardQuery() {
  const params = new URLSearchParams({
    type: state.type,
    page: String(state.page),
    limit: "20"
  });
  if (state.type === "galaxy" && state.galaxyId) {
    params.set("galaxy_id", state.galaxyId);
  }
  return `/leaderboard?${params.toString()}`;
}

function renderToolbar() {
  const tabs = [
    { value: "global", label: "Global" },
    { value: "weekly", label: "Weekly" },
    { value: "monthly", label: "Monthly" },
    { value: "galaxy", label: "Galaxy" }
  ];

  return `
    <section class="card stack">
      <div class="filter-bar">
        ${tabs
          .map(
            (tab) => `<button class="tab-button ${state.type === tab.value ? "is-active" : ""}" data-type="${tab.value}">${tab.label}</button>`
          )
          .join("")}
        ${state.type === "galaxy" ? `
          <select class="select" id="galaxy-filter" style="max-width: 18rem;">
            <option value="">Choose a galaxy</option>
            ${state.galaxies.map((galaxy) => `<option value="${galaxy.id}" ${state.galaxyId === galaxy.id ? "selected" : ""}>${escapeHtml(galaxy.name)}</option>`).join("")}
          </select>
        ` : ""}
      </div>
    </section>
  `;
}

function rankLabel(position) {
  if (position === 1) return "Top rank";
  if (position <= 3) return "Podium";
  if (position <= 10) return "Strong standing";
  return "In the field";
}

function renderLeaderboard(data) {
  const totalPages = Math.max(1, Math.ceil(data.total / data.limit));
  const itemsHtml = data.items.length
    ? `
      <div class="table-wrap leaderboard-table">
        <table class="table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Learner</th>
              <th>Level</th>
              <th>Rank title</th>
              <th>XP</th>
            </tr>
          </thead>
          <tbody>
            ${data.items
              .map(
                (item) => `
                  <tr class="${item.user_id === state.currentUser.id ? "is-current-user" : ""}">
                    <td>
                      <div class="leaderboard-rank">#${item.position}</div>
                      <div class="activity-note">${rankLabel(item.position)}</div>
                    </td>
                    <td>
                      <div class="user-stack">
                        ${createAvatar(item.username, item.avatar_url)}
                        <div>
                          <strong>${escapeHtml(item.username)}</strong>
                          <div class="activity-note">${item.user_id === state.currentUser.id ? "Current user" : "Learner"}</div>
                        </div>
                      </div>
                    </td>
                    <td>${item.level}</td>
                    <td>${escapeHtml(item.rank_title)}</td>
                    <td>${item.xp}</td>
                  </tr>
                `
              )
              .join("")}
          </tbody>
        </table>
      </div>
    `
    : renderEmptyState({
        iconName: "trophy",
        title: "No leaderboard entries yet",
        text: state.type === "galaxy" ? "No users currently appear in this galaxy leaderboard scope." : "This leaderboard scope does not have snapshot data yet."
      });

  return `
    <section class="hero-surface stack">
      <div class="hero-grid">
        <div class="stack">
          <div>
            <p class="eyebrow">Constellation rank</p>
            <h2 class="page-title" style="font-size: clamp(1.9rem, 1.45rem + 1vw, 2.7rem);">See how your route glows against the rest of the universe.</h2>
            <p class="page-subtitle">Shift between global, weekly, monthly, and galaxy constellations to understand where your current momentum places you.</p>
          </div>
          <div class="metric-ribbon">
            <div class="segment surface-soft"><div class="metric-label">Scope</div><div class="metric-value">${escapeHtml(data.leaderboard_type)}</div></div>
            <div class="segment surface-soft"><div class="metric-label">Entries</div><div class="metric-value">${data.total}</div></div>
            <div class="segment surface-soft"><div class="metric-label">Page</div><div class="metric-value">${data.page}</div></div>
          </div>
        </div>
        <div class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Your standing</h2>
              <p class="section-description">A quick read of where your current route sits inside the selected constellation.</p>
            </div>
          </div>
          ${data.user_position ? `
            <div class="metric-card">
              <div class="metric-label">Current rank</div>
              <div class="metric-value">#${data.user_position.position}</div>
              <div class="metric-meta">XP counted in this board: ${data.user_position.xp}</div>
            </div>
          ` : '<div class="callout warning">You do not currently appear in this leaderboard scope.</div>'}
          ${data.snapshot_date ? `<div class="callout info">Snapshot date: ${escapeHtml(data.snapshot_date)}</div>` : '<div class="callout">This scope is using live ranking data rather than a dated snapshot.</div>'}
        </div>
      </div>
    </section>

    ${renderToolbar()}

    <section class="card stack">
      <div class="section-header">
        <div>
          <h2 class="section-title">Explorer field</h2>
          <p class="section-description">Current ranking page for the selected constellation scope.</p>
        </div>
      </div>
      ${itemsHtml}
      <div class="inline" style="justify-content: space-between; align-items: center;">
        <div class="activity-note">Page ${data.page} of ${totalPages}</div>
        <div class="inline">
          <button class="button button-secondary" id="prev-page-button" ${data.page <= 1 ? "disabled" : ""}>${icon("chevronLeft")}Previous</button>
          <button class="button button-secondary" id="next-page-button" ${data.page >= totalPages ? "disabled" : ""}>Next${icon("chevronRight")}</button>
        </div>
      </div>
    </section>
  `;
}

function bindEvents() {
  document.querySelectorAll("[data-type]").forEach((button) => {
    button.addEventListener("click", () => {
      state.type = button.dataset.type;
      state.page = 1;
      if (state.type !== "galaxy") state.galaxyId = "";
      loadLeaderboard();
    });
  });

  qs("#galaxy-filter")?.addEventListener("change", (event) => {
    state.galaxyId = event.target.value;
    state.page = 1;
    loadLeaderboard();
  });

  qs("#prev-page-button")?.addEventListener("click", () => {
    state.page = Math.max(1, state.page - 1);
    loadLeaderboard();
  });

  qs("#next-page-button")?.addEventListener("click", () => {
    state.page += 1;
    loadLeaderboard();
  });
}

async function loadLeaderboard() {
  updateQueryParams({
    type: state.type,
    page: state.page,
    galaxyId: state.type === "galaxy" ? state.galaxyId : ""
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);

  try {
    if (!state.galaxies.length) {
      const galaxiesPayload = await api.get("/galaxies");
      state.galaxies = galaxiesPayload.data;
    }

    if (state.type === "galaxy" && !state.galaxyId && state.galaxies.length) {
      state.galaxyId = state.galaxies[0].id;
    }

    const payload = await api.get(buildLeaderboardQuery());
    content.innerHTML = renderLeaderboard(payload.data);
    bindEvents();
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadLeaderboard);
    showToast({ type: "error", title: "Leaderboard unavailable", message: error.message });
  }
}

async function bootstrap() {
  const user = await ensureAuthenticated();
  if (!user) return;
  state.currentUser = user;
  initializePrivateLayout({
    user,
    activeNav: "leaderboard",
    title: "Constellation Rank",
    subtitle: "Compare your momentum across global, timed, and galaxy-specific explorer fields.",
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon("dashboard")}Mission Control</a>`,
    world: "leaderboard"
  });
  await loadLeaderboard();
}

bootstrap();
