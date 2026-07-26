import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { createAvatar, renderErrorState, renderLoadingGrid, showToast, statusClass } from "./ui.js";
import { escapeHtml, formatDateTime, formatPercentage, getRequiredQueryParam, pluralize, qs } from "./utils.js";

function renderDiscoveryItem(item) {
  const isLocked = item.status === "LOCKED";
  return `
    <article class="list-card">
      <div class="list-card-head">
        <div>
          <p class="eyebrow">Discovery ${escapeHtml(item.order_number)}</p>
          <h3 class="list-card-title">${escapeHtml(item.title)}</h3>
          <div class="list-card-meta">
            <span>${escapeHtml(pluralize(item.read_time_minutes || 0, "minute"))}</span>
            <span>·</span>
            <span>${escapeHtml(item.xp_reward)} XP</span>
          </div>
        </div>
        <span class="${statusClass(item.status)}">${escapeHtml(item.status.replaceAll("_", " "))}</span>
      </div>
      <p class="list-card-description">${escapeHtml(item.description || item.learning_objective || "No description available.")}</p>
      <div class="inline">
        <a class="button ${isLocked ? "button-ghost" : "button-primary"} ${isLocked ? "hidden" : ""}" href="./discovery.html?id=${item.id}">Open discovery</a>
        ${isLocked ? '<button class="button button-secondary" disabled>Locked</button>' : ""}
      </div>
    </article>
  `;
}

function renderPracticeItem(item) {
  const isLocked = item.status === "LOCKED";
  return `
    <article class="list-card">
      <div class="list-card-head">
        <div>
          <p class="eyebrow">Practice ${escapeHtml(item.order_number)}</p>
          <h3 class="list-card-title">${escapeHtml(item.title)}</h3>
          <div class="list-card-meta">
            <span>${escapeHtml(item.challenge_type.replaceAll("_", " "))}</span>
            <span>·</span>
            <span>${escapeHtml(item.xp_reward)} XP</span>
          </div>
        </div>
        <span class="${statusClass(item.status)}">${escapeHtml(item.status.replaceAll("_", " "))}</span>
      </div>
      <p class="list-card-description">${escapeHtml(item.description || item.learning_outcome || "No description available.")}</p>
      <div class="inline">
        <a class="button ${isLocked ? "button-ghost" : "button-primary"} ${isLocked ? "hidden" : ""}" href="./practice.html?id=${item.id}">Open practice</a>
        ${isLocked ? '<button class="button button-secondary" disabled>Locked</button>' : ""}
      </div>
    </article>
  `;
}

function renderQuizCard(planet) {
  const quiz = planet.quiz;
  const progress = planet.progress;
  const locked = quiz?.status === "LOCKED";
  const action = locked
    ? '<button class="button button-secondary" disabled>Quiz locked</button>'
    : `<a class="button button-primary" href="./quiz.html?planetId=${planet.id}">${quiz?.passed ? "Review quiz" : "Open quiz"}</a>`;

  return `
    <section class="card stack">
      <div class="section-header">
        <div>
          <h2 class="section-title">Planet quiz</h2>
          <p class="section-description">Unlock the artifact by passing the quiz after completing all discoveries and practices.</p>
        </div>
        <span class="${statusClass(quiz?.status || "LOCKED")}">${escapeHtml((quiz?.status || "LOCKED").replaceAll("_", " "))}</span>
      </div>
      <div class="grid-two">
        <div class="callout">${escapeHtml(quiz?.total_questions || 0)} questions · ${escapeHtml(quiz?.attempts_count || 0)} attempts · Best score: ${quiz?.best_score ?? "—"}</div>
        <div class="callout">Discoveries: ${progress?.completed_discoveries_count || 0}/${progress?.total_discoveries || planet.discoveries.length} · Practices: ${progress?.completed_practices_count || 0}/${progress?.total_practices || planet.practice_challenges.length}</div>
      </div>
      <div class="inline">${action}</div>
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
    subtitle: "Loading planet details…",
    actions: '<a class="button button-secondary" href="./galaxies.html">All galaxies</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);

  try {
    const payload = await api.get(`/planets/${planetId}`);
    const planet = payload.data;
    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: planet.name,
      subtitle: planet.description || planet.tagline || "Review the lessons, practices, and quiz for this planet.",
      actions: `<a class="button button-secondary" href="./galaxy.html?id=${planet.galaxy_id}">Back to galaxy</a>${planet.quiz?.status !== "LOCKED" ? `<a class="button button-primary" href="./quiz.html?planetId=${planet.id}">Open quiz</a>` : ""}`
    });

    content.innerHTML = `
      <section class="hero-surface stack">
        <div class="hero-grid">
          <div class="user-stack" style="align-items: flex-start;">
            ${createAvatar(planet.name, null, true)}
            <div>
              <p class="eyebrow">Planet ${escapeHtml(planet.order_number)}</p>
              <h2 class="page-title" style="font-size: 2rem;">${escapeHtml(planet.name)}</h2>
              <p class="page-subtitle">${escapeHtml(planet.tagline || planet.description || "A backend-driven learning planet.")}</p>
              <div class="inline" style="margin-top: 1rem;">
                <span class="${statusClass(planet.status)}">${escapeHtml(planet.status.replaceAll("_", " "))}</span>
                <span class="badge badge-primary">${escapeHtml(planet.xp_total)} XP total</span>
                <span class="badge badge-muted">${escapeHtml(planet.estimated_time_minutes ?? 0)} min</span>
              </div>
            </div>
          </div>
          <div class="card stack">
            <div class="progress-stack">
              <div class="progress-labels"><span>Completion</span><span>${escapeHtml(formatPercentage(planet.progress?.progress_percent || 0))}</span></div>
              <div class="progress-bar"><span style="width:${planet.progress?.progress_percent || 0}%"></span></div>
            </div>
            <div class="callout">Unlock condition: ${escapeHtml(planet.unlock_condition || "Available by default")}</div>
            ${planet.progress?.last_activity_at ? `<div class="activity-note">Last activity: ${escapeHtml(formatDateTime(planet.progress.last_activity_at))}</div>` : ""}
          </div>
        </div>
      </section>

      <section class="grid-four">
        <article class="metric-card">
          <div class="metric-label">Discoveries</div>
          <div class="metric-value">${planet.progress?.completed_discoveries_count || 0}/${planet.progress?.total_discoveries || planet.discoveries.length}</div>
          <div class="metric-meta">Core reading lessons completed.</div>
        </article>
        <article class="metric-card">
          <div class="metric-label">Practices</div>
          <div class="metric-value">${planet.progress?.completed_practices_count || 0}/${planet.progress?.total_practices || planet.practice_challenges.length}</div>
          <div class="metric-meta">Coding challenges completed.</div>
        </article>
        <article class="metric-card">
          <div class="metric-label">Quiz status</div>
          <div class="metric-value">${escapeHtml((planet.quiz?.status || "LOCKED").replaceAll("_", " "))}</div>
          <div class="metric-meta">Best score: ${planet.progress?.quiz_best_score ?? "—"}</div>
        </article>
        <article class="metric-card">
          <div class="metric-label">Artifact reward</div>
          <div class="metric-value">${escapeHtml(planet.artifact?.name || "—")}</div>
          <div class="metric-meta">${escapeHtml(planet.artifact?.xp_bonus_percent || 0)}% XP bonus</div>
        </article>
      </section>

      ${renderQuizCard(planet)}

      <section class="detail-grid">
        <div class="stack">
          <section class="card stack">
            <div class="section-header">
              <div>
                <h2 class="section-title">Discoveries</h2>
                <p class="section-description">Read each discovery in order to unlock practices and the quiz.</p>
              </div>
            </div>
            <div class="stack">${planet.discoveries.map(renderDiscoveryItem).join("")}</div>
          </section>
          <section class="card stack">
            <div class="section-header">
              <div>
                <h2 class="section-title">Practice challenges</h2>
                <p class="section-description">Work through backend-evaluated Python tasks to build momentum.</p>
              </div>
            </div>
            <div class="stack">${planet.practice_challenges.map(renderPracticeItem).join("")}</div>
          </section>
        </div>
        <div class="stack">
          <section class="card stack">
            <div class="section-header">
              <div>
                <h2 class="section-title">Artifact reward</h2>
                <p class="section-description">Pass the planet quiz to unlock the planet artifact.</p>
              </div>
            </div>
            ${planet.artifact ? `
              <div class="user-stack" style="align-items: flex-start;">
                ${createAvatar(planet.artifact.name, planet.artifact.icon_url, true)}
                <div>
                  <h3 class="card-title">${escapeHtml(planet.artifact.name)}</h3>
                  <div class="list-card-meta"><span>${escapeHtml(planet.artifact.category)}</span><span>·</span><span>${escapeHtml(planet.artifact.rarity)}</span></div>
                  <p class="list-card-description">${escapeHtml(planet.artifact.xp_bonus_percent)}% bonus XP when equipped in your collection.</p>
                </div>
              </div>
            ` : '<div class="callout">No artifact is associated with this planet.</div>'}
          </section>
          <section class="card stack">
            <div class="section-header">
              <div>
                <h2 class="section-title">Progress metadata</h2>
                <p class="section-description">Exact backend summary for this planet.</p>
              </div>
            </div>
            <div class="stack">
              <div class="callout">Planet status: ${escapeHtml(planet.progress?.status || planet.status)}</div>
              <div class="callout">Completed: ${planet.progress?.completed ? "Yes" : "No"}</div>
              <div class="callout">XP earned here: ${escapeHtml(planet.progress?.xp_earned || 0)}</div>
            </div>
          </section>
        </div>
      </section>
    `;
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadPlanet);
    showToast({ type: "error", title: "Planet unavailable", message: error.message });
  }
}

loadPlanet();
