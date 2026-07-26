import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { createAvatar, renderEmptyState, renderErrorState, renderLoadingGrid, showToast, statusClass } from "../core/ui.js";
import { escapeHtml, formatDateTime, formatPercentage, getRequiredQueryParam, pluralize, qs } from "../core/utils.js";

function humanizeStatus(status = "") {
  return String(status || "UNKNOWN").replaceAll("_", " ");
}

function difficultyCopy(level) {
  if (Number(level) <= 1) return "Easy orbit · ideal for first contact";
  if (Number(level) === 2) return "Steady orbit · deeper logic ahead";
  if (Number(level) === 3) return "Dense orbit · strong fundamentals required";
  return "High gravity route · advanced exploration";
}

function planetTone(planet) {
  const difficulty = Number(planet.difficulty) || 1;
  if (difficulty <= 1) return "verdant";
  if (difficulty === 2) return "amber";
  if (difficulty === 3) return "violet";
  return "coral";
}

function completionCounts(planet) {
  const progress = planet.progress || {};
  return {
    discoveriesDone: progress.completed_discoveries_count ?? planet.discoveries.filter((item) => item.status === "COMPLETED").length,
    discoveriesTotal: progress.total_discoveries ?? planet.discoveries.length,
    practicesDone: progress.completed_practices_count ?? planet.practice_challenges.filter((item) => item.status === "COMPLETED").length,
    practicesTotal: progress.total_practices ?? planet.practice_challenges.length
  };
}

function determineNextAction(planet) {
  const nextDiscovery = planet.discoveries.find((item) => item.status !== "COMPLETED" && item.status !== "LOCKED");
  if (nextDiscovery) {
    return {
      href: `./discovery.html?id=${nextDiscovery.id}`,
      label: `Continue discovery ${nextDiscovery.order_number}`,
      iconName: "discovery",
      note: nextDiscovery.title || "Your next reading route is ready."
    };
  }

  const nextPractice = planet.practice_challenges.find((item) => item.status !== "COMPLETED" && item.status !== "LOCKED");
  if (nextPractice) {
    return {
      href: `./practice.html?id=${nextPractice.id}`,
      label: `Launch mission ${nextPractice.order_number}`,
      iconName: "mission",
      note: nextPractice.title || "Your next hands-on mission is unlocked."
    };
  }

  if (planet.quiz?.status !== "LOCKED") {
    return {
      href: `./quiz.html?planetId=${planet.id}`,
      label: planet.quiz?.passed ? "Review mission briefing" : "Open mission briefing",
      iconName: "quiz",
      note: planet.quiz?.passed ? "The boss battle is already cleared for this world." : "Only the final briefing remains between you and the artifact vault."
    };
  }

  return {
    href: `./galaxy.html?id=${planet.galaxy_id}`,
    label: "Return to galaxy route",
    iconName: "galaxy",
    note: "This world is visible, but its next step is still waiting for a prior unlock."
  };
}

function stageStrip(planet) {
  const counts = completionCounts(planet);
  const discoveriesComplete = counts.discoveriesDone >= Math.max(counts.discoveriesTotal, 1) && counts.discoveriesTotal > 0;
  const practicesComplete = counts.practicesDone >= Math.max(counts.practicesTotal, 1) && counts.practicesTotal > 0;
  const quizUnlocked = planet.quiz?.status !== "LOCKED";
  const quizPassed = Boolean(planet.quiz?.passed);
  const artifactUnlocked = Boolean(planet.progress?.completed || quizPassed);

  return `
    <div class="stage-strip">
      <div class="stage-node is-complete"><span>Arrival</span></div>
      <div class="stage-node ${discoveriesComplete ? "is-complete" : counts.discoveriesDone > 0 ? "is-active" : ""}"><span>Discoveries</span></div>
      <div class="stage-node ${practicesComplete ? "is-complete" : counts.practicesDone > 0 ? "is-active" : discoveriesComplete ? "is-next" : ""}"><span>Missions</span></div>
      <div class="stage-node ${quizPassed ? "is-complete" : quizUnlocked ? "is-next" : ""}"><span>Briefing</span></div>
      <div class="stage-node ${artifactUnlocked ? "is-complete" : quizUnlocked ? "is-next" : ""}"><span>Artifact</span></div>
    </div>
  `;
}

function renderDiscoveryManifestItem(item) {
  const locked = item.status === "LOCKED";
  return `
    <article class="route-manifest-item ${locked ? "route-manifest-item--locked" : ""}">
      <div class="route-manifest-marker">${escapeHtml(item.order_number)}</div>
      <div class="route-manifest-body">
        <div class="route-manifest-head">
          <div>
            <p class="eyebrow">Discovery route</p>
            <h3 class="section-title">${escapeHtml(item.title)}</h3>
          </div>
          <span class="${statusClass(item.status)}">${escapeHtml(humanizeStatus(item.status))}</span>
        </div>
        <p class="route-manifest-description">${escapeHtml(item.description || item.learning_objective || "No discovery description is available yet.")}</p>
        <div class="route-manifest-meta">
          <span class="badge badge-muted">${icon("clock")} ${escapeHtml(pluralize(item.read_time_minutes || 0, "minute"))}</span>
          <span class="badge badge-primary">${icon("spark")} ${escapeHtml(item.xp_reward)} XP</span>
          ${item.learning_objective ? `<span class="badge badge-muted">${icon("compass")} Objective</span>` : ""}
        </div>
        <div class="route-manifest-actions">
          <p class="route-manifest-note">${escapeHtml(locked ? "This route will illuminate after earlier discoveries are complete." : item.learning_objective || "Open this discovery to continue charting the planet.")}</p>
          <a class="button ${locked ? "button-secondary" : "button-primary"}" href="./discovery.html?id=${item.id}">${locked ? `${icon("lock")}Locked route` : `${icon("discovery")}Enter discovery`}</a>
        </div>
      </div>
    </article>
  `;
}

function renderPracticeManifestItem(item) {
  const locked = item.status === "LOCKED";
  return `
    <article class="route-manifest-item ${locked ? "route-manifest-item--locked" : ""}">
      <div class="route-manifest-marker route-manifest-marker--mission">${escapeHtml(item.order_number)}</div>
      <div class="route-manifest-body">
        <div class="route-manifest-head">
          <div>
            <p class="eyebrow">Mission</p>
            <h3 class="section-title">${escapeHtml(item.title)}</h3>
          </div>
          <span class="${statusClass(item.status)}">${escapeHtml(humanizeStatus(item.status))}</span>
        </div>
        <p class="route-manifest-description">${escapeHtml(item.description || item.learning_outcome || "No mission description is available yet.")}</p>
        <div class="route-manifest-meta">
          <span class="badge badge-muted">${escapeHtml(humanizeStatus(item.challenge_type || "Mission"))}</span>
          <span class="badge badge-primary">${icon("spark")} ${escapeHtml(item.xp_reward)} XP</span>
          <span class="badge badge-muted">${icon("bolt")} Difficulty ${escapeHtml(item.difficulty)}</span>
        </div>
        <div class="route-manifest-actions">
          <p class="route-manifest-note">${escapeHtml(locked ? "This mission bay remains sealed until the discovery route is stable." : item.learning_outcome || "Hands-on reinforcement for what you just learned.")}</p>
          <a class="button ${locked ? "button-secondary" : "button-primary"}" href="./practice.html?id=${item.id}">${locked ? `${icon("lock")}Locked bay` : `${icon("mission")}Launch mission`}</a>
        </div>
      </div>
    </article>
  `;
}

function renderQuizGate(planet) {
  const counts = completionCounts(planet);
  const quiz = planet.quiz || {};
  const locked = quiz.status === "LOCKED";
  const discoveryProgress = ((counts.discoveriesDone / Math.max(counts.discoveriesTotal, 1)) * 100) || 0;
  const practiceProgress = ((counts.practicesDone / Math.max(counts.practicesTotal, 1)) * 100) || 0;
  const actionHtml = locked
    ? `<button class="button button-secondary" disabled>${icon("lock")}Briefing sealed</button>`
    : `<a class="button button-primary" href="./quiz.html?planetId=${planet.id}">${icon("quiz")}${quiz.passed ? "Review mission briefing" : "Enter mission briefing"}</a>`;

  return `
    <section class="card stack expedition-card expedition-card--glow">
      <div class="section-header">
        <div>
          <p class="eyebrow">Boss gate</p>
          <h2 class="section-title">Mission briefing</h2>
          <p class="section-description">The final knowledge check for this world unlocks its treasure vault.</p>
        </div>
        <span class="${statusClass(quiz.status || "LOCKED")}">${escapeHtml(humanizeStatus(quiz.status || "LOCKED"))}</span>
      </div>

      <div class="planet-briefing-grid">
        <div class="planet-briefing-fact">
          <span class="metric-label">Questions</span>
          <strong class="metric-value">${escapeHtml(quiz.total_questions || 0)}</strong>
        </div>
        <div class="planet-briefing-fact">
          <span class="metric-label">Attempts</span>
          <strong class="metric-value">${escapeHtml(quiz.attempts_count || 0)}</strong>
        </div>
        <div class="planet-briefing-fact">
          <span class="metric-label">Best score</span>
          <strong class="metric-value">${escapeHtml((planet.progress?.quiz_best_score ?? quiz.best_score) ?? "—")}</strong>
        </div>
      </div>

      <div class="progress-stack">
        <div class="progress-labels"><span>Discovery clearance</span><span>${counts.discoveriesDone}/${counts.discoveriesTotal}</span></div>
        <div class="progress-bar"><span style="width:${discoveryProgress}%"></span></div>
      </div>
      <div class="progress-stack">
        <div class="progress-labels"><span>Mission clearance</span><span>${counts.practicesDone}/${counts.practicesTotal}</span></div>
        <div class="progress-bar"><span style="width:${practiceProgress}%"></span></div>
      </div>

      <div class="callout ${locked ? "warning" : quiz.passed ? "success" : "info"}">
        ${escapeHtml(
          locked
            ? "Finish every discovery and mission on this planet before the boss gate opens."
            : quiz.passed
              ? "This world's final briefing has already been cleared. You can revisit it anytime."
              : "The final briefing is ready. Correct answers will only be revealed after submission."
        )}
      </div>

      <div class="inline">${actionHtml}</div>
    </section>
  `;
}

function renderArtifactVault(artifact, planet) {
  if (!artifact) {
    return `
      <section class="card stack artifact-vault">
        <div class="section-header">
          <div>
            <p class="eyebrow">Treasure vault</p>
            <h2 class="section-title">No artifact attached</h2>
          </div>
        </div>
        <div class="callout info">This world currently has no visible artifact reward attached to it.</div>
      </section>
    `;
  }

  const unlocked = Boolean(planet.progress?.completed || planet.quiz?.passed);
  return `
    <section class="card stack artifact-vault">
      <div class="section-header">
        <div>
          <p class="eyebrow">Treasure vault</p>
          <h2 class="section-title">${escapeHtml(artifact.name)}</h2>
          <p class="section-description">The relic bound to this world waits behind the final briefing.</p>
        </div>
        <span class="${statusClass(unlocked ? "COMPLETED" : "LOCKED")}">${unlocked ? `${icon("artifact")}Recovered` : `${icon("lock")}Sealed`}</span>
      </div>
      <div class="artifact-vault-display">
        <div class="artifact-vault-emblem">${createAvatar(artifact.name, artifact.icon_url, true)}</div>
        <div class="artifact-vault-copy">
          <div class="artifact-card-badges">
            <span class="badge badge-muted">${escapeHtml(artifact.rarity)}</span>
            <span class="badge badge-muted">${escapeHtml(artifact.category)}</span>
            <span class="badge badge-primary">${icon("spark")} +${escapeHtml(artifact.xp_bonus_percent)}% XP</span>
          </div>
          <p class="route-manifest-description">${escapeHtml(artifact.description || "A rare object preserved in the AlgoLingo museum.")}</p>
        </div>
      </div>
      <div class="callout ${unlocked ? "success" : "info"}">${escapeHtml(unlocked ? "This artifact is already part of your museum collection." : artifact.unlock_condition || "Pass the final briefing to claim this reward.")}</div>
      <a class="button button-secondary" href="./artifacts.html">${icon("artifact")}Open museum</a>
    </section>
  `;
}

function renderTelemetry(planet, galaxy) {
  const progress = planet.progress || {};
  const currentAction = determineNextAction(planet);
  return `
    <section class="card stack expedition-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">Explorer telemetry</p>
          <h2 class="section-title">Current route signal</h2>
        </div>
      </div>
      <div class="telemetry-list">
        <div class="telemetry-row"><span>Galaxy</span><strong>${escapeHtml(galaxy?.name || "Current galaxy")}</strong></div>
        <div class="telemetry-row"><span>Planet state</span><strong>${escapeHtml(humanizeStatus(planet.status))}</strong></div>
        <div class="telemetry-row"><span>XP earned here</span><strong>${escapeHtml(progress.xp_earned || 0)}</strong></div>
        <div class="telemetry-row"><span>Unlock condition</span><strong>${escapeHtml(planet.unlock_condition || "Visible now")}</strong></div>
        <div class="telemetry-row"><span>Last activity</span><strong>${escapeHtml(progress.last_activity_at ? formatDateTime(progress.last_activity_at) : "—")}</strong></div>
      </div>
      <div class="callout info">${escapeHtml(currentAction.note)}</div>
      <a class="button button-primary" href="${currentAction.href}">${icon(currentAction.iconName)}${escapeHtml(currentAction.label)}</a>
    </section>
  `;
}

function renderPlanet(planet, galaxy) {
  const counts = completionCounts(planet);
  const progress = planet.progress || {};
  const nextAction = determineNextAction(planet);
  const tone = planetTone(planet);
  const masteryPercent = Number(progress.progress_percent || 0);

  return `
    <section class="planet-shell">
      <section class="world-hero planetfall-card planetfall-card--${tone}">
        <div class="world-hero-copy">
          <p class="eyebrow">Planetfall · ${escapeHtml(galaxy?.name || "Galaxy route")}</p>
          <h2 class="landing-system-title">${escapeHtml(planet.name)}</h2>
          <p class="world-hero-subtitle">${escapeHtml(planet.tagline || planet.description || "A living learning destination inside your current galaxy.")}</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("planet")} ${escapeHtml(humanizeStatus(planet.status))}</span>
            <span class="badge badge-muted">${icon("bolt")} Difficulty ${escapeHtml(planet.difficulty)}</span>
            <span class="badge badge-muted">${icon("clock")} ${escapeHtml(planet.estimated_time_minutes ?? "—")} min route</span>
            <span class="badge badge-primary">${icon("spark")} ${escapeHtml(planet.xp_total)} XP orbit</span>
          </div>
          ${stageStrip(planet)}
          <div class="inline">
            <a class="button button-primary" href="${nextAction.href}">${icon(nextAction.iconName)}${escapeHtml(nextAction.label)}</a>
            <a class="button button-secondary" href="./galaxy.html?id=${planet.galaxy_id}">${icon("chevronLeft")}Back to galaxy</a>
          </div>
        </div>

        <div class="world-hero-visual">
          <div class="planet-orbitarium planet-orbitarium--${tone}">
            <div class="planet-orbit planet-orbit--outer"></div>
            <div class="planet-orbit planet-orbit--inner"></div>
            <div class="planet-sphere"></div>
            <div class="planet-satellite planet-satellite--discoveries">
              <strong>${escapeHtml(counts.discoveriesDone)}</strong>
              <span>Discoveries</span>
            </div>
            <div class="planet-satellite planet-satellite--missions">
              <strong>${escapeHtml(counts.practicesDone)}</strong>
              <span>Missions</span>
            </div>
            <div class="planet-satellite planet-satellite--artifact">
              <strong>${planet.artifact ? "1" : "0"}</strong>
              <span>Artifact</span>
            </div>
            <div class="planet-orbit-caption">
              <span>Mastery</span>
              <strong>${escapeHtml(formatPercentage(masteryPercent))}</strong>
            </div>
          </div>
        </div>
      </section>

      <section class="grid-four planet-signal-grid">
        <article class="metric-card planet-signal-card"><div class="metric-label">Discoveries charted</div><div class="metric-value">${escapeHtml(counts.discoveriesDone)}</div><div class="metric-meta">of ${escapeHtml(counts.discoveriesTotal)}</div></article>
        <article class="metric-card planet-signal-card"><div class="metric-label">Missions cleared</div><div class="metric-value">${escapeHtml(counts.practicesDone)}</div><div class="metric-meta">of ${escapeHtml(counts.practicesTotal)}</div></article>
        <article class="metric-card planet-signal-card"><div class="metric-label">Briefing state</div><div class="metric-value">${escapeHtml(humanizeStatus(planet.quiz?.status || "LOCKED"))}</div><div class="metric-meta">Attempts: ${escapeHtml(planet.quiz?.attempts_count || 0)}</div></article>
        <article class="metric-card planet-signal-card"><div class="metric-label">Surface mood</div><div class="metric-value">${escapeHtml(difficultyCopy(planet.difficulty).split("·")[0].trim())}</div><div class="metric-meta">${escapeHtml(difficultyCopy(planet.difficulty))}</div></article>
      </section>

      <section class="detail-grid planet-content-grid">
        <div class="stack">
          <section class="card expedition-card stack">
            <div class="section-header">
              <div>
                <p class="eyebrow">Route archive</p>
                <h2 class="section-title">Discovery trail</h2>
                <p class="section-description">Read the planet in sequence. Each discovery lights the way for stronger missions later.</p>
              </div>
            </div>
            ${planet.discoveries.length ? `<div class="route-manifest">${planet.discoveries.map(renderDiscoveryManifestItem).join("")}</div>` : renderEmptyState({ iconName: "discovery", title: "No discoveries found", text: "This planet has no visible discovery routes yet." })}
          </section>

          <section class="card expedition-card stack">
            <div class="section-header">
              <div>
                <p class="eyebrow">Launch bays</p>
                <h2 class="section-title">Mission sequence</h2>
                <p class="section-description">Hands-on missions convert theory into movement. Every solved task pulls the artifact vault closer.</p>
              </div>
            </div>
            ${planet.practice_challenges.length ? `<div class="route-manifest">${planet.practice_challenges.map(renderPracticeManifestItem).join("")}</div>` : renderEmptyState({ iconName: "mission", title: "No missions found", text: "This planet has no visible mission challenges yet." })}
          </section>
        </div>

        <aside class="stack expedition-rail">
          ${renderQuizGate(planet)}
          ${renderArtifactVault(planet.artifact, planet)}
          ${renderTelemetry(planet, galaxy)}
        </aside>
      </section>
    </section>
  `;
}

async function loadPlanet() {
  const planetId = getRequiredQueryParam("id");
  if (!planetId) {
    window.location.href = "./galaxies.html";
    return;
  }

  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "galaxies",
    title: "Planet",
    subtitle: "Preparing the next destination…",
    actions: `<a class="button button-secondary" href="./galaxies.html">${icon("galaxy")}Galaxy map</a>`,
    world: "planet"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(4);

  try {
    const payload = await api.get(`/planets/${planetId}`);
    const planet = payload.data;

    let galaxy = null;
    try {
      const galaxyPayload = await api.get(`/galaxies/${planet.galaxy_id}`);
      galaxy = galaxyPayload.data;
    } catch {
      galaxy = null;
    }

    const nextAction = determineNextAction(planet);
    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: planet.name,
      subtitle: planet.tagline || planet.description || "Review this world's discoveries, missions, briefing, and artifact route.",
      actions: `<a class="button button-secondary" href="./galaxy.html?id=${planet.galaxy_id}">${icon("chevronLeft")}Back to galaxy</a><a class="button button-primary" href="${nextAction.href}">${icon(nextAction.iconName)}${escapeHtml(nextAction.label)}</a>`,
      world: "planet"
    });

    content.innerHTML = renderPlanet(planet, galaxy);
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadPlanet);
    showToast({ type: "error", title: "Planet unavailable", message: error.message });
  }
}

loadPlanet();
