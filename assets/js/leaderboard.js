import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { createAvatar, renderEmptyState, renderErrorState, renderLoadingGrid, showToast } from "./ui.js";
import { escapeHtml, getRequiredQueryParam, qs, updateQueryParams } from "./utils.js";

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
            <option value="">Select a galaxy</option>
            ${state.galaxies.map((galaxy) => `<option value="${galaxy.id}" ${state.galaxyId === galaxy.id ? "selected" : ""}>${escapeHtml(galaxy.name)}</option>`).join("")}
          </select>
        ` : ""}
      </div>
    </section>
  `;
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
              <th>User</th>
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
                    <td class="leaderboard-rank">#${item.position}</td>
                    <td>
                      <div class="user-stack">
                        ${createAvatar(item.username, item.avatar_url)}
                        <div>
                          <strong>${escapeHtml(item.username)}</strong>
                          ${item.user_id === state.currentUser.id ? '<div class="activity-note">You</div>' : ""}
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
        icon: "📉",
        title: "No leaderboard entries",
        text: state.type === "galaxy" ? "This galaxy leaderboard has no ranked users yet." : "There is no snapshot data for this leaderboard yet."
      });

  return `
    ${renderToolbar()}
    <section class="grid-two">
      <article class="card stack">
        <div class="section-header">
          <div>
            <h2 class="section-title">${escapeHtml(data.leaderboard_type)} leaderboard</h2>
            <p class="section-description">The frontend is rendering live backend leaderboard data without reshaping the API contract.</p>
          </div>
        </div>
        ${itemsHtml}
        <div class="inline" style="justify-content: space-between; align-items: center;">
          <div class="activity-note">Page ${data.page} of ${totalPages}${data.snapshot_date ? ` · Snapshot ${escapeHtml(data.snapshot_date)}` : ""}</div>
          <div class="inline">
            <button class="button button-secondary" id="prev-page-button" ${data.page <= 1 ? "disabled" : ""}>Previous</button>
            <button class="button button-secondary" id="next-page-button" ${data.page >= totalPages ? "disabled" : ""}>Next</button>
          </div>
        </div>
      </article>
      <article class="card stack">
        <div class="section-header">
          <div>
            <h2 class="section-title">Your position</h2>
            <p class="section-description">Pulled from the backend's user_position summary.</p>
          </div>
        </div>
        ${data.user_position ? `
          <div class="metric-card">
            <div class="metric-label">Current rank</div>
            <div class="metric-value">#${data.user_position.position}</div>
            <div class="metric-meta">XP counted in this board: ${data.user_position.xp}</div>
          </div>
        ` : '<div class="callout warning">You do not currently appear in this leaderboard scope.</div>'}
      </article>
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
  content.innerHTML = renderLoadingGrid(2);

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
    title: "Leaderboard",
    subtitle: "Compare your progress across global, periodic, and galaxy-specific ranking scopes.",
    actions: '<a class="button button-secondary" href="./dashboard.html">Back to dashboard</a>'
  });
  await loadLeaderboard();
}

bootstrap();
