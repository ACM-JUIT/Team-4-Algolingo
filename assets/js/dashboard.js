import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { renderEmptyState, renderErrorState, renderLoadingGrid, showToast, statusClass } from "./ui.js";
import { escapeHtml, formatDate, formatPercentage, formatRelativeTime, qs } from "./utils.js";

function describeActivity(activity) {
  const data = activity.event_data || {};
  switch (activity.event_type) {
    case "discovery_completed":
      return `Completed a discovery and earned ${data.xp_awarded ?? 0} XP.`;
    case "practice_completed":
      return `Passed a practice challenge for ${data.xp_awarded ?? 0} XP.`;
    case "quiz_passed":
      return `Passed a quiz with ${data.score ?? 0}/${data.total_questions ?? 0}.`;
    case "planet_completed":
      return `Completed a planet and earned ${data.xp_awarded ?? 0} bonus XP.`;
    case "artifact_unlocked":
      return `Unlocked the ${data.artifact_name ?? "latest"} artifact.`;
    case "daily_login":
      return `Logged in and extended the streak.`;
    case "nova_used":
      return `Used NOVA in ${data.mode ?? "assistant"} mode.`;
    case "practice_solution_viewed":
      return "Viewed a reference solution.";
    default:
      return "Completed a learning activity.";
  }
}

function renderRecentActivity(items) {
  if (!items.length) {
    return renderEmptyState({
      icon: "🛰",
      title: "No recent activity yet",
      text: "Complete your first discovery or practice challenge to start building your activity timeline."
    });
  }

  return `
    <div class="timeline">
      ${items
        .map(
          (item) => `
            <div class="timeline-item">
              <div class="timeline-marker" aria-hidden="true"></div>
              <div class="timeline-body">
                <div class="inline" style="justify-content: space-between; align-items: center; margin-bottom: .35rem;">
                  <strong>${escapeHtml(item.event_type.replaceAll("_", " "))}</strong>
                  <span class="activity-note" title="${escapeHtml(formatDate(item.created_at))}">${escapeHtml(formatRelativeTime(item.created_at))}</span>
                </div>
                <p class="activity-note">${escapeHtml(describeActivity(item))}</p>
              </div>
            </div>
          `
        )
        .join("")}
    </div>
  `;
}

function renderDashboard(data) {
  const { user, quick_stats: stats, continue_learning: continueLearning, recent_activity: activity, leaderboard_unlocked: leaderboardUnlocked } = data;

  const continueCard = continueLearning
    ? `
      <div class="card stack">
        <div class="section-header">
          <div>
            <h2 class="section-title">Continue learning</h2>
            <p class="section-description">Resume the next best step in your current learning path.</p>
          </div>
          <div class="stat-ring" data-label="${Math.round(continueLearning.progress_percent)}%\nprogress" style="--value:${continueLearning.progress_percent}%"></div>
        </div>
        <div class="stack">
          <div>
            <div class="eyebrow">${escapeHtml(continueLearning.galaxy_name)}</div>
            <h3 class="card-title">${escapeHtml(continueLearning.planet_name)}</h3>
          </div>
          <div class="progress-stack">
            <div class="progress-labels"><span>Planet progress</span><span>${escapeHtml(formatPercentage(continueLearning.progress_percent))}</span></div>
            <div class="progress-bar"><span style="width:${continueLearning.progress_percent}%"></span></div>
          </div>
          <div class="inline">
            ${continueLearning.next_discovery_id ? `<a class="button button-primary" href="./discovery.html?id=${continueLearning.next_discovery_id}">Resume discovery</a>` : ""}
            ${continueLearning.next_practice_id ? `<a class="button button-secondary" href="./practice.html?id=${continueLearning.next_practice_id}">Open practice</a>` : ""}
            <a class="button button-ghost" href="./planet.html?id=${continueLearning.planet_id}">View planet</a>
          </div>
        </div>
      </div>
    `
    : renderEmptyState({
        icon: "🏁",
        title: "You are all caught up",
        text: "There is no incomplete planet in your path right now. Explore the galaxy map or check your leaderboard position."
      });

  const leaderboardState = leaderboardUnlocked
    ? `<div class="callout success">Leaderboard access is unlocked. Compare your progress with other explorers any time.</div>`
    : `<div class="callout warning">Leaderboard unlocks at level 3 after completing at least one planet.</div>`;

  return `
    <section class="hero-surface stack">
      <div class="hero-grid">
        <div class="stack">
          <div>
            <p class="eyebrow">Overview</p>
            <h2 class="page-title" style="font-size: 2rem;">Hello, ${escapeHtml(user.username)}.</h2>
            <p class="page-subtitle">You are currently level ${escapeHtml(user.level)} with a ${escapeHtml(user.rank_title)} rank. Keep building your Python fundamentals one planet at a time.</p>
          </div>
          <div class="inline">
            <span class="badge badge-primary">${escapeHtml(stats.xp)} XP</span>
            <span class="badge badge-success">${escapeHtml(stats.streak_days)} day streak</span>
            <span class="badge badge-warning">${escapeHtml(stats.artifacts_earned)} artifacts</span>
          </div>
        </div>
        <div class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Progress snapshot</h2>
              <p class="section-description">Live counts taken directly from the dashboard response.</p>
            </div>
          </div>
          <div class="stack">
            <div class="callout">Completed planets: ${stats.completed_planets}</div>
            <div class="callout">Completed discoveries: ${stats.completed_discoveries}</div>
            <div class="callout">Completed practices: ${stats.completed_practices}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="grid-four">
      <article class="metric-card">
        <div class="metric-label">Total XP</div>
        <div class="metric-value">${escapeHtml(stats.xp)}</div>
        <div class="metric-meta">Rewarded across all completed learning steps.</div>
      </article>
      <article class="metric-card">
        <div class="metric-label">Current level</div>
        <div class="metric-value">${escapeHtml(stats.level)}</div>
        <div class="metric-meta">Rank: ${escapeHtml(stats.rank_title)}</div>
      </article>
      <article class="metric-card">
        <div class="metric-label">Streak</div>
        <div class="metric-value">${escapeHtml(stats.streak_days)}</div>
        <div class="metric-meta">Log in and learn consistently to keep it alive.</div>
      </article>
      <article class="metric-card">
        <div class="metric-label">Artifacts earned</div>
        <div class="metric-value">${escapeHtml(stats.artifacts_earned)}</div>
        <div class="metric-meta">Planet rewards that boost your total XP gains.</div>
      </article>
    </section>

    <section class="detail-grid">
      <div class="stack">
        ${continueCard}
        <div class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Quick actions</h2>
              <p class="section-description">Jump into the parts of AlgoLingo you are most likely to need next.</p>
            </div>
          </div>
          <div class="quick-actions-grid">
            <a class="list-card" href="./galaxies.html">
              <div>
                <h3 class="list-card-title">Browse galaxies</h3>
                <p class="list-card-description">See every available planet and your unlock path.</p>
              </div>
            </a>
            <a class="list-card" href="./artifacts.html">
              <div>
                <h3 class="list-card-title">Review artifacts</h3>
                <p class="list-card-description">Track the rewards you have unlocked and what remains.</p>
              </div>
            </a>
            <a class="list-card" href="./leaderboard.html">
              <div>
                <h3 class="list-card-title">Open leaderboard</h3>
                <p class="list-card-description">See global, weekly, monthly, and galaxy-based rankings.</p>
              </div>
            </a>
            <a class="list-card" href="./nova.html">
              <div>
                <h3 class="list-card-title">Ask NOVA</h3>
                <p class="list-card-description">Use contextual help, debugging, hints, or recommendations.</p>
              </div>
            </a>
          </div>
        </div>
      </div>
      <div class="stack">
        <div class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Leaderboard status</h2>
              <p class="section-description">Access is tied to your current progression.</p>
            </div>
          </div>
          ${leaderboardState}
        </div>
        <div class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Recent activity</h2>
              <p class="section-description">The latest milestones recorded by the backend.</p>
            </div>
          </div>
          ${renderRecentActivity(activity)}
        </div>
      </div>
    </section>
  `;
}

async function loadDashboard() {
  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "dashboard",
    title: "Dashboard",
    subtitle: "Track your progress, revisit the next recommended lesson, and stay aware of your current streak.",
    actions: '<a class="button button-secondary" href="./galaxies.html">Explore galaxies</a><a class="button button-primary" href="./nova.html">Open NOVA</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);

  try {
    const payload = await api.get("/dashboard");
    content.innerHTML = renderDashboard(payload.data);
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadDashboard);
    showToast({ type: "error", title: "Dashboard unavailable", message: error.message });
  }
}

loadDashboard();
