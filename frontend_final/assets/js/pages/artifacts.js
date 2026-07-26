import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { createAvatar, renderEmptyState, renderErrorState, renderLoadingGrid, showToast, statusClass } from "../core/ui.js";
import { escapeHtml, formatDateTime, qs } from "../core/utils.js";

let artifactItems = [];
let filter = "all";

function filteredArtifacts() {
  if (filter === "unlocked") return artifactItems.filter((item) => item.collected);
  if (filter === "locked") return artifactItems.filter((item) => !item.collected);
  return artifactItems;
}

function rarityClass(rarity) {
  const normalized = String(rarity || "").toLowerCase();
  if (normalized === "epic" || normalized === "legendary") return "badge-warning";
  if (normalized === "rare" || normalized === "uncommon") return "badge-primary";
  return "badge-muted";
}

function collectionPercent() {
  if (!artifactItems.length) return 0;
  return Math.round((artifactItems.filter((item) => item.collected).length / artifactItems.length) * 100);
}

function unlockNote(item) {
  const artifact = item.artifact;
  if (item.collected) return `Recovered ${formatDateTime(item.unlocked_at)}`;
  if (artifact.is_hidden) return "This relic remains veiled until the route reveals it.";
  return artifact.unlock_condition || "Unlock through progression";
}

function renderArtifactCard(item) {
  const artifact = item.artifact;
  const unlocked = Boolean(item.collected);
  return `
    <article class="artifact-pedestal ${unlocked ? "is-unlocked" : "is-locked"}">
      <div class="artifact-pedestal-orb">${createAvatar(artifact.name, artifact.icon_url, true)}</div>
      <div class="artifact-pedestal-copy">
        <div class="artifact-pedestal-head">
          <div>
            <p class="eyebrow">Treasure</p>
            <h2 class="artifact-card-title">${escapeHtml(artifact.name)}</h2>
          </div>
          <span class="${statusClass(unlocked ? "COMPLETED" : "LOCKED")}">${unlocked ? `${icon("artifact")}Recovered` : `${icon("lock")}Sealed`}</span>
        </div>
        <div class="artifact-card-badges">
          <span class="badge ${rarityClass(artifact.rarity)}">${escapeHtml(artifact.rarity)}</span>
          <span class="badge badge-muted">${escapeHtml(artifact.category)}</span>
          <span class="badge badge-primary">${icon("spark")} +${escapeHtml(artifact.xp_bonus_percent)}% XP</span>
        </div>
        <p class="route-manifest-description">${escapeHtml(artifact.description || "No artifact description available.")}</p>
        <div class="artifact-pedestal-footer">
          <p class="route-manifest-note">${escapeHtml(unlockNote(item))}</p>
          <a class="button button-secondary" href="./artifact.html?id=${artifact.id}">${icon("artifact")}Inspect relic</a>
        </div>
      </div>
    </article>
  `;
}

function bindArtifactEvents() {
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
  const percent = collectionPercent();
  const lockedCount = artifactItems.length - unlockedCount;
  const unlockedBonus = artifactItems.filter((item) => item.collected).reduce((sum, item) => sum + (item.artifact.xp_bonus_percent || 0), 0);

  content.innerHTML = `
    <section class="artifact-museum-shell">
      <section class="world-hero artifact-museum-hero">
        <div class="world-hero-copy">
          <p class="eyebrow">Artifact Museum</p>
          <h2 class="landing-system-title">A treasure chamber for every world you have truly mastered.</h2>
          <p class="world-hero-subtitle">Artifacts are not normal badges. They are recovered relics tied to mission-briefing victory, planet completion, and long-term XP momentum across the universe.</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("artifact")} ${unlockedCount} recovered</span>
            <span class="badge badge-muted">${lockedCount} still veiled</span>
            <span class="badge badge-primary">${icon("spark")} +${unlockedBonus}% active bonus</span>
          </div>
        </div>

        <div class="world-hero-visual report-score-visual">
          <div class="stat-ring stat-ring--large" data-label="${percent}%\nrecovered" style="--value:${percent}%"></div>
          <div class="report-score-facts">
            <div class="planet-briefing-fact"><span class="metric-label">Recovered</span><strong class="metric-value">${unlockedCount}</strong></div>
            <div class="planet-briefing-fact"><span class="metric-label">Catalog</span><strong class="metric-value">${artifactItems.length}</strong></div>
          </div>
        </div>
      </section>

      <section class="card expedition-card stack">
        <div class="section-header">
          <div>
            <p class="eyebrow">Museum floor</p>
            <h2 class="section-title">Browse the full relic catalog</h2>
            <p class="section-description">The museum never hides future treasures entirely. Locked relics stay visible so the next reward always feels real.</p>
          </div>
        </div>
        <div class="filter-bar">
          <button class="tab-button ${filter === "all" ? "is-active" : ""}" data-filter="all">All relics</button>
          <button class="tab-button ${filter === "unlocked" ? "is-active" : ""}" data-filter="unlocked">Recovered</button>
          <button class="tab-button ${filter === "locked" ? "is-active" : ""}" data-filter="locked">Veiled</button>
        </div>
        ${list.length ? `<div class="artifact-gallery">${list.map(renderArtifactCard).join("")}</div>` : renderEmptyState({ iconName: "artifact", title: "No relics in this view", text: "Switch the museum filter to inspect the rest of the collection." })}
      </section>
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
    title: "Artifact Museum",
    subtitle: "Recover, inspect, and admire every relic in your collection universe.",
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon("dashboard")}Mission Control</a>`,
    world: "artifacts"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(4);

  try {
    const payload = await api.get("/artifacts");
    artifactItems = payload.data;
    renderArtifacts();
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadArtifacts);
    showToast({ type: "error", title: "Museum unavailable", message: error.message });
  }
}

loadArtifacts();
