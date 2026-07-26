import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { closeModal, createAvatar, openModal, renderEmptyState, renderErrorState, renderLoadingGrid, showToast, statusClass } from "./ui.js";
import { escapeHtml, formatDateTime, qs } from "./utils.js";

let artifactItems = [];
let filter = "all";

function filteredArtifacts() {
  if (filter === "unlocked") return artifactItems.filter((item) => item.collected);
  if (filter === "locked") return artifactItems.filter((item) => !item.collected);
  return artifactItems;
}

function rarityClass(rarity) {
  return rarity?.toLowerCase() === "epic" ? "badge-warning" : rarity?.toLowerCase() === "rare" ? "badge-primary" : "badge-muted";
}

function renderArtifactCard(item) {
  const artifact = item.artifact;
  return `
    <article class="list-card" data-artifact-id="${artifact.id}">
      <div class="list-card-head">
        <div class="user-stack">
          ${createAvatar(artifact.name, artifact.icon_url, true)}
          <div>
            <h2 class="list-card-title">${escapeHtml(artifact.name)}</h2>
            <div class="list-card-meta">
              <span class="badge ${rarityClass(artifact.rarity)}">${escapeHtml(artifact.rarity)}</span>
              <span>${escapeHtml(artifact.category)}</span>
            </div>
          </div>
        </div>
        <span class="${statusClass(item.collected ? "COMPLETED" : "LOCKED")}">${item.collected ? "Unlocked" : "Locked"}</span>
      </div>
      <p class="list-card-description">${escapeHtml(artifact.description || "No description available.")}</p>
      <div class="inline">
        <span class="badge badge-primary">+${escapeHtml(artifact.xp_bonus_percent)}% XP bonus</span>
        ${item.unlocked_at ? `<span class="badge badge-success">Unlocked ${escapeHtml(formatDateTime(item.unlocked_at))}</span>` : ""}
      </div>
      <button class="button button-secondary">View details</button>
    </article>
  `;
}

function bindArtifactEvents() {
  document.querySelectorAll("[data-artifact-id]").forEach((card) => {
    card.addEventListener("click", () => {
      const item = artifactItems.find((entry) => entry.artifact.id === card.dataset.artifactId);
      if (!item) return;
      const artifact = item.artifact;
      openModal({
        title: artifact.name,
        body: `
          <div class="stack">
            <div class="inline">
              <span class="badge ${rarityClass(artifact.rarity)}">${escapeHtml(artifact.rarity)}</span>
              <span class="badge badge-primary">${escapeHtml(artifact.category)}</span>
              <span class="${statusClass(item.collected ? "COMPLETED" : "LOCKED")}">${item.collected ? "Unlocked" : "Locked"}</span>
            </div>
            <p class="activity-note">${escapeHtml(artifact.description || "No description available.")}</p>
            <div class="callout">Unlock condition: ${escapeHtml(artifact.unlock_condition || "Not specified")}</div>
            <div class="callout">XP bonus: ${escapeHtml(artifact.xp_bonus_percent)}%</div>
            ${item.unlocked_at ? `<div class="callout success">Unlocked on ${escapeHtml(formatDateTime(item.unlocked_at))}</div>` : ""}
          </div>
        `,
        actions: [{ label: "Close", className: "button-primary", onClick: closeModal }]
      });
    });
  });

  document.querySelectorAll("[data-filter]").forEach((button) => {
    button.addEventListener("click", () => {
      filter = button.dataset.filter;
      renderArtifacts();
    });
  });
}

function renderArtifacts() {
  const list = filteredArtifacts();
  const content = qs("#page-content");
  const unlockedCount = artifactItems.filter((item) => item.collected).length;
  content.innerHTML = `
    <section class="grid-four" style="margin-bottom: 1.5rem;">
      <article class="metric-card"><div class="metric-label">Total artifacts</div><div class="metric-value">${artifactItems.length}</div></article>
      <article class="metric-card"><div class="metric-label">Unlocked</div><div class="metric-value">${unlockedCount}</div></article>
      <article class="metric-card"><div class="metric-label">Locked</div><div class="metric-value">${artifactItems.length - unlockedCount}</div></article>
      <article class="metric-card"><div class="metric-label">Collection progress</div><div class="metric-value">${artifactItems.length ? Math.round((unlockedCount / artifactItems.length) * 100) : 0}%</div></article>
    </section>
    <section class="card stack">
      <div class="section-header">
        <div>
          <h2 class="section-title">Artifact collection</h2>
          <p class="section-description">Every artifact shown here comes directly from the backend artifact catalog.</p>
        </div>
      </div>
      <div class="filter-bar">
        <button class="tab-button ${filter === "all" ? "is-active" : ""}" data-filter="all">All</button>
        <button class="tab-button ${filter === "unlocked" ? "is-active" : ""}" data-filter="unlocked">Unlocked</button>
        <button class="tab-button ${filter === "locked" ? "is-active" : ""}" data-filter="locked">Locked</button>
      </div>
      ${list.length ? `<div class="artifact-grid">${list.map(renderArtifactCard).join("")}</div>` : renderEmptyState({ icon: "🏺", title: "No artifacts in this view", text: "Adjust the filter to see the full collection." })}
    </section>
  `;
  bindArtifactEvents();
}

async function loadArtifacts() {
  const user = await ensureAuthenticated();
  if (!user) return;
  initializePrivateLayout({
    user,
    activeNav: "artifacts",
    title: "Artifacts",
    subtitle: "Track every unlockable backend-defined artifact and the progress behind it.",
    actions: '<a class="button button-secondary" href="./dashboard.html">Back to dashboard</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);

  try {
    const payload = await api.get("/artifacts");
    artifactItems = payload.data;
    renderArtifacts();
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadArtifacts);
    showToast({ type: "error", title: "Artifacts unavailable", message: error.message });
  }
}

loadArtifacts();
