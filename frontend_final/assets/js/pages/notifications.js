import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { renderEmptyState, renderErrorState, renderLoadingGrid, showToast } from "../core/ui.js";
import { escapeHtml, formatRelativeTime, qs } from "../core/utils.js";

function describeActivity(activity) {
  const data = activity.event_data || {};
  switch (activity.event_type) {
    case "discovery_completed":
      return { title: data.discovery_title || "Discovery archived", body: `You earned ${data.xp_awarded ?? 0} XP by completing a discovery.`, iconName: "discovery" };
    case "practice_completed":
      return { title: data.practice_title || "Mission cleared", body: `Mission reward: ${data.xp_awarded ?? 0} XP.`, iconName: "mission" };
    case "quiz_passed":
      return { title: data.planet_name || "Boss gate cleared", body: `Score: ${data.score ?? 0}/${data.total_questions ?? 0}.`, iconName: "quiz" };
    case "planet_completed":
      return { title: data.planet_name || "Planet secured", body: `Planet completion bonus: ${data.xp_awarded ?? 0} XP.`, iconName: "planet" };
    case "artifact_unlocked":
      return { title: data.artifact_name || "Relic recovered", body: "A new artifact has entered your museum collection.", iconName: "artifact" };
    case "nova_used":
      return { title: "NOVA contact logged", body: `Mode used: ${data.mode ?? "assistant"}.`, iconName: "nova" };
    default:
      return { title: String(activity.event_type || "signal").replaceAll("_", " "), body: "A new journey event was recorded.", iconName: "star" };
  }
}

function buildPrioritySignals(dashboard, artifacts) {
  const signals = [];
  const recentArtifact = artifacts
    .filter((item) => item.collected && item.unlocked_at)
    .sort((a, b) => new Date(b.unlocked_at).getTime() - new Date(a.unlocked_at).getTime())[0];

  if (dashboard.continue_learning) {
    const route = dashboard.continue_learning;
    signals.push({
      title: `Route ready: ${route.planet_name}`,
      body: `${route.galaxy_name} is the strongest next destination in your universe.`,
      iconName: "compass",
      href: route.next_discovery_id
        ? `./discovery.html?id=${route.next_discovery_id}`
        : route.next_practice_id
          ? `./practice.html?id=${route.next_practice_id}`
          : `./planet.html?id=${route.planet_id}`,
      actionLabel: route.next_discovery_id ? "Open discovery" : route.next_practice_id ? "Launch mission" : "View planet"
    });
  }

  if (dashboard.leaderboard_unlocked) {
    signals.push({
      title: "Constellation rank is live",
      body: "Your route is now visible inside the ranking network.",
      iconName: "leaderboard",
      href: "./leaderboard.html",
      actionLabel: "View rank"
    });
  }

  if (recentArtifact) {
    signals.push({
      title: `Museum signal: ${recentArtifact.artifact.name}`,
      body: "Your latest recovered relic is ready for closer inspection.",
      iconName: "artifact",
      href: `./artifact.html?id=${recentArtifact.artifact.id}`,
      actionLabel: "Inspect relic"
    });
  }

  if (dashboard.quick_stats.streak_days > 0) {
    signals.push({
      title: `${dashboard.quick_stats.streak_days}-day streak active`,
      body: "One meaningful action today keeps the wake alive.",
      iconName: "bolt",
      href: "./dashboard.html",
      actionLabel: "Open Mission Control"
    });
  }

  signals.push({
    title: "NOVA remains online",
    body: "When a discovery becomes dense or a mission fails, your onboard tutor is one jump away.",
    iconName: "nova",
    href: "./nova.html",
    actionLabel: "Open NOVA"
  });

  return signals.slice(0, 4);
}

function renderNotificationsPage(dashboard, artifacts) {
  const prioritySignals = buildPrioritySignals(dashboard, artifacts);
  const activity = dashboard.recent_activity || [];

  return `
    <section class="notifications-shell">
      <section class="world-hero notifications-hero">
        <div class="world-hero-copy">
          <p class="eyebrow">Signal Archive</p>
          <h2 class="landing-system-title">A readable stream of what the universe is telling you right now.</h2>
          <p class="world-hero-subtitle">This archive turns recent journey activity, unlocked routes, recovered relics, and guided recommendations into one calm signal field.</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("bell")} ${prioritySignals.length} priority signals</span>
            <span class="badge badge-muted">${activity.length} recent events</span>
          </div>
        </div>
        <div class="world-hero-visual report-score-visual">
          <div class="report-score-facts">
            <div class="planet-briefing-fact"><span class="metric-label">Next route</span><strong class="metric-value" style="font-size:1rem">${escapeHtml(dashboard.continue_learning?.planet_name || "All current routes complete")}</strong></div>
            <div class="planet-briefing-fact"><span class="metric-label">Streak</span><strong class="metric-value">${dashboard.quick_stats.streak_days}</strong></div>
          </div>
        </div>
      </section>

      <section class="signal-priority-grid">
        ${prioritySignals.map((signal) => `
          <article class="signal-card signal-card--priority">
            <span class="icon-spot">${icon(signal.iconName)}</span>
            <div class="stack" style="gap:.5rem;">
              <h3 class="section-title">${escapeHtml(signal.title)}</h3>
              <p class="section-description">${escapeHtml(signal.body)}</p>
            </div>
            <a class="button button-secondary" href="${signal.href}">${escapeHtml(signal.actionLabel)}</a>
          </article>
        `).join("")}
      </section>

      <section class="card expedition-card stack">
        <div class="section-header">
          <div>
            <p class="eyebrow">Recent transmissions</p>
            <h2 class="section-title">Journey event stream</h2>
            <p class="section-description">Every item below comes from the recent activity field returned by the dashboard endpoint.</p>
          </div>
        </div>
        ${activity.length ? `
          <div class="timeline signal-timeline">
            ${activity.map((item) => {
              const summary = describeActivity(item);
              return `
                <div class="timeline-item">
                  <div class="timeline-marker"></div>
                  <div class="timeline-body stack" style="gap:.45rem;">
                    <div class="signal-meta"><span class="icon-spot">${icon(summary.iconName)}</span><span>${escapeHtml(formatRelativeTime(item.created_at))}</span></div>
                    <strong>${escapeHtml(summary.title)}</strong>
                    <p class="section-description">${escapeHtml(summary.body)}</p>
                  </div>
                </div>
              `;
            }).join("")}
          </div>
        ` : renderEmptyState({ iconName: "bell", title: "No recent transmissions", text: "Complete a discovery, mission, or briefing to begin populating this signal archive." })}
      </section>
    </section>
  `;
}

async function loadNotifications() {
  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "notifications",
    title: "Signal Archive",
    subtitle: "Review route prompts, streak reminders, recent activity, and museum signals in one place.",
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon("dashboard")}Mission Control</a><a class="button button-primary" href="./nova.html">${icon("nova")}Open NOVA</a>`,
    world: "notifications"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);

  try {
    const [dashboardPayload, artifactsPayload] = await Promise.all([
      api.get("/dashboard"),
      api.get("/artifacts")
    ]);

    content.innerHTML = renderNotificationsPage(dashboardPayload.data, artifactsPayload.data);
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadNotifications);
    showToast({ type: "error", title: "Signal archive unavailable", message: error.message });
  }
}

loadNotifications();
