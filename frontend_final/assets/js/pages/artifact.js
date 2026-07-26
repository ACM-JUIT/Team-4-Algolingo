import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { createAvatar, renderErrorState, renderLoadingGrid, showToast, statusClass } from "../core/ui.js";
import { escapeHtml, formatDateTime, getRequiredQueryParam, qs } from "../core/utils.js";

function rarityClass(rarity) {
  const normalized = String(rarity || "").toLowerCase();
  if (normalized === "epic" || normalized === "legendary") return "badge-warning";
  if (normalized === "rare" || normalized === "uncommon") return "badge-primary";
  return "badge-muted";
}

function renderArtifactDetail(artifact, collectionItem) {
  const unlocked = Boolean(collectionItem?.collected);
  return `
    <section class="artifact-detail-shell">
      <section class="world-hero artifact-detail-hero">
        <div class="world-hero-copy">
          <p class="eyebrow">Artifact detail</p>
          <h2 class="landing-system-title">${escapeHtml(artifact.name)}</h2>
          <p class="world-hero-subtitle">${escapeHtml(artifact.description || "A relic preserved in the AlgoLingo museum.")}</p>
          <div class="world-hero-badges">
            <span class="badge ${rarityClass(artifact.rarity)}">${escapeHtml(artifact.rarity)}</span>
            <span class="badge badge-muted">${escapeHtml(artifact.category)}</span>
            <span class="badge badge-primary">${icon("spark")} +${escapeHtml(artifact.xp_bonus_percent)}% XP</span>
            <span class="${statusClass(unlocked ? "COMPLETED" : "LOCKED")}">${unlocked ? `${icon("artifact")}Recovered` : `${icon("lock")}Sealed`}</span>
          </div>
          <div class="inline">
            <a class="button button-secondary" href="./artifacts.html">${icon("chevronLeft")}Back to museum</a>
            <a class="button button-primary" href="./leaderboard.html">${icon("leaderboard")}View constellation rank</a>
          </div>
        </div>

        <div class="world-hero-visual artifact-shrine">
          <div class="artifact-shrine-ring artifact-shrine-ring--outer"></div>
          <div class="artifact-shrine-ring artifact-shrine-ring--inner"></div>
          <div class="artifact-shrine-core">${createAvatar(artifact.name, artifact.icon_url, true)}</div>
        </div>
      </section>

      <section class="detail-grid">
        <section class="card expedition-card stack">
          <div class="section-header">
            <div>
              <p class="eyebrow">Relic profile</p>
              <h2 class="section-title">Museum record</h2>
              <p class="section-description">This page preserves the official museum record of the relic and, when available, your personal recovery state.</p>
            </div>
          </div>
          <div class="telemetry-list">
            <div class="telemetry-row"><span>Rarity</span><strong>${escapeHtml(artifact.rarity)}</strong></div>
            <div class="telemetry-row"><span>Category</span><strong>${escapeHtml(artifact.category)}</strong></div>
            <div class="telemetry-row"><span>XP bonus</span><strong>+${escapeHtml(artifact.xp_bonus_percent)}%</strong></div>
            <div class="telemetry-row"><span>Visibility</span><strong>${artifact.is_hidden ? "Hidden until discovered" : "Visible in museum catalog"}</strong></div>
          </div>
        </section>

        <aside class="stack">
          <section class="card expedition-card stack">
            <div class="section-header">
              <div>
                <p class="eyebrow">Unlock state</p>
                <h2 class="section-title">Recovery signal</h2>
              </div>
            </div>
            <div class="callout ${unlocked ? "success" : "info"}">${escapeHtml(unlocked ? "This relic has already been recovered and is contributing to your long-term XP momentum." : artifact.unlock_condition || "Recover this artifact by completing the route tied to it.")}</div>
            ${collectionItem?.unlocked_at ? `<div class="callout success">Recovered on ${escapeHtml(formatDateTime(collectionItem.unlocked_at))}</div>` : ""}
            ${collectionItem?.showcased ? '<div class="callout info">This artifact is currently marked as showcased in your collection state.</div>' : ""}
          </section>

          <section class="card expedition-card stack">
            <div class="section-header">
              <div>
                <p class="eyebrow">Treasure path</p>
                <h2 class="section-title">How it fits the universe</h2>
              </div>
            </div>
            <div class="callout">Artifacts are the long-memory of progress in AlgoLingo. Each recovered relic turns planet mastery into a permanent advantage.</div>
            <a class="button button-secondary" href="./galaxies.html">${icon("galaxy")}Return to galaxy map</a>
          </section>
        </aside>
      </section>
    </section>
  `;
}

async function loadArtifact() {
  const artifactId = getRequiredQueryParam("id");
  if (!artifactId) {
    window.location.href = "./artifacts.html";
    return;
  }

  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "artifacts",
    title: "Artifact Detail",
    subtitle: "Preparing the museum record…",
    actions: `<a class="button button-secondary" href="./artifacts.html">${icon("artifact")}Artifact Museum</a>`,
    world: "artifacts"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(2);

  try {
    const [artifactPayload, collectionPayload] = await Promise.all([
      api.get(`/artifacts/${artifactId}`),
      api.get("/artifacts")
    ]);
    const artifact = artifactPayload.data;
    const collectionItem = collectionPayload.data.find((item) => item.artifact.id === artifact.id) || null;

    initializePrivateLayout({
      user,
      activeNav: "artifacts",
      title: artifact.name,
      subtitle: artifact.description || "Inspect this recovered relic and its role in your long-term progression.",
      actions: `<a class="button button-secondary" href="./artifacts.html">${icon("chevronLeft")}Back to museum</a>`,
      world: "artifacts"
    });

    content.innerHTML = renderArtifactDetail(artifact, collectionItem);
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadArtifact);
    showToast({ type: "error", title: "Artifact unavailable", message: error.message });
  }
}

loadArtifact();
