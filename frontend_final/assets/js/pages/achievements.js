import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { renderErrorState, renderLoadingGrid, showToast, statusClass } from "../core/ui.js";
import { escapeHtml, formatPercentage, qs } from "../core/utils.js";

function buildAchievements(dashboard, artifacts, galaxies) {
  const stats = dashboard.quick_stats;
  const unlockedArtifacts = artifacts.filter((item) => item.collected).length;
  const activeGalaxies = galaxies.filter((item) => !item.is_locked).length;
  const exploredGalaxies = galaxies.filter((item) => Number(item.progress_percent || 0) > 0 || Number(item.completed_planets || 0) > 0).length;
  const totalArtifactTarget = Math.max(1, Math.min(artifacts.length || 1, 3));

  const definitions = [
    { id: "first-discovery", title: "First Light", description: "Complete your first discovery anywhere in the universe.", iconName: "discovery", current: stats.completed_discoveries, target: 1, group: "Knowledge" },
    { id: "archive-builder", title: "Archive Builder", description: "Log five completed discoveries in your explorer archive.", iconName: "book", current: stats.completed_discoveries, target: 5, group: "Knowledge" },
    { id: "mission-ignition", title: "Mission Ignition", description: "Clear your first hands-on coding mission.", iconName: "mission", current: stats.completed_practices, target: 1, group: "Missions" },
    { id: "mission-fleet", title: "Mission Fleet", description: "Clear ten missions across your route map.", iconName: "rocket", current: stats.completed_practices, target: 10, group: "Missions" },
    { id: "planet-secured", title: "Planet Secured", description: "Fully complete your first planet route.", iconName: "planet", current: stats.completed_planets, target: 1, group: "Mastery" },
    { id: "system-voyager", title: "System Voyager", description: "Complete three full planets and prove consistent world mastery.", iconName: "galaxy", current: stats.completed_planets, target: 3, group: "Mastery" },
    { id: "relic-finder", title: "Relic Finder", description: "Recover your first artifact from a completed route.", iconName: "artifact", current: unlockedArtifacts, target: 1, group: "Relics" },
    { id: "museum-curator", title: "Museum Curator", description: "Recover several relics and begin shaping a true collection.", iconName: "artifact", current: unlockedArtifacts, target: totalArtifactTarget, group: "Relics" },
    { id: "streak-wake", title: "Streak Wake", description: "Hold a three-day learning streak.", iconName: "bolt", current: stats.streak_days, target: 3, group: "Momentum" },
    { id: "gravity-keeper", title: "Gravity Keeper", description: "Hold a seven-day streak without dropping out of orbit.", iconName: "star", current: stats.streak_days, target: 7, group: "Momentum" },
    { id: "level-climb", title: "Level Climb", description: "Reach the next explorer level through sustained XP growth.", iconName: "leaderboard", current: stats.level, target: 2, group: "Rank" },
    { id: "constellation-entry", title: "Constellation Entry", description: "Unlock access to the ranking constellations.", iconName: "trophy", current: dashboard.leaderboard_unlocked ? 1 : 0, target: 1, group: "Rank" },
    { id: "galaxy-scout", title: "Galaxy Scout", description: "Begin charting progress inside a live galaxy route.", iconName: "compass", current: exploredGalaxies, target: 1, group: "Exploration" },
    { id: "open-systems", title: "Open Systems", description: "Reach a point where multiple galaxies are visible for current exploration.", iconName: "galaxy", current: activeGalaxies, target: Math.max(1, Math.min(2, galaxies.length || 1)), group: "Exploration" }
  ];

  return definitions.map((item) => {
    const unlocked = item.current >= item.target;
    const progress = item.target <= 0 ? 100 : Math.min(100, Math.round((item.current / item.target) * 100));
    return { ...item, unlocked, progress };
  });
}

function renderAchievementCard(item) {
  return `
    <article class="honor-card ${item.unlocked ? "is-unlocked" : "is-locked"}">
      <div class="honor-card-head">
        <span class="icon-spot">${icon(item.iconName)}</span>
        <span class="${statusClass(item.unlocked ? "COMPLETED" : "LOCKED")}">${item.unlocked ? "Unlocked" : "Sealed"}</span>
      </div>
      <div class="stack" style="gap:.55rem;">
        <p class="eyebrow">${escapeHtml(item.group)}</p>
        <h3 class="section-title">${escapeHtml(item.title)}</h3>
        <p class="section-description">${escapeHtml(item.description)}</p>
      </div>
      <div class="progress-stack honor-progress">
        <div class="progress-labels"><span>Progress</span><span>${escapeHtml(item.current)}/${escapeHtml(item.target)}</span></div>
        <div class="progress-bar"><span style="width:${item.progress}%"></span></div>
      </div>
      <div class="metric-meta">${item.unlocked ? "This achievement now belongs to your explorer record." : `${formatPercentage(item.progress)} of the route complete.`}</div>
    </article>
  `;
}

function renderAchievementsPage(achievements, dashboard, artifacts) {
  const unlockedCount = achievements.filter((item) => item.unlocked).length;
  const nextAchievement = achievements.filter((item) => !item.unlocked).sort((a, b) => b.progress - a.progress)[0] || null;
  const unlockedArtifacts = artifacts.filter((item) => item.collected).length;

  return `
    <section class="achievements-shell">
      <section class="world-hero achievement-hero">
        <div class="world-hero-copy">
          <p class="eyebrow">Achievement Vault</p>
          <h2 class="landing-system-title">Milestones that turn effort into explorer history.</h2>
          <p class="world-hero-subtitle">These honors are derived from your real progress. They translate discoveries, missions, streaks, relics, and rank movement into a visible record of growth.</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("trophy")} ${unlockedCount} unlocked</span>
            <span class="badge badge-muted">${achievements.length - unlockedCount} still sealed</span>
            <span class="badge badge-primary">${icon("artifact")} ${unlockedArtifacts} relic milestones active</span>
          </div>
        </div>

        <div class="world-hero-visual report-score-visual">
          <div class="stat-ring stat-ring--large" data-label="${Math.round((unlockedCount / Math.max(achievements.length, 1)) * 100)}%\nunlocked" style="--value:${Math.round((unlockedCount / Math.max(achievements.length, 1)) * 100)}%"></div>
          <div class="report-score-facts">
            <div class="planet-briefing-fact"><span class="metric-label">Current rank</span><strong class="metric-value" style="font-size:1rem">${escapeHtml(dashboard.quick_stats.rank_title)}</strong></div>
            <div class="planet-briefing-fact"><span class="metric-label">Streak</span><strong class="metric-value">${dashboard.quick_stats.streak_days}</strong></div>
          </div>
        </div>
      </section>

      ${nextAchievement ? `
        <section class="card expedition-card stack">
          <div class="section-header">
            <div>
              <p class="eyebrow">Closest unlock</p>
              <h2 class="section-title">${escapeHtml(nextAchievement.title)}</h2>
              <p class="section-description">${escapeHtml(nextAchievement.description)}</p>
            </div>
            <span class="badge badge-primary">${formatPercentage(nextAchievement.progress)}</span>
          </div>
          <div class="progress-stack">
            <div class="progress-labels"><span>Route progress</span><span>${nextAchievement.current}/${nextAchievement.target}</span></div>
            <div class="progress-bar"><span style="width:${nextAchievement.progress}%"></span></div>
          </div>
        </section>
      ` : ""}

      <section class="honors-grid">
        ${achievements.map(renderAchievementCard).join("")}
      </section>
    </section>
  `;
}

async function loadAchievements() {
  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "achievements",
    title: "Achievement Vault",
    subtitle: "Trace the milestone record generated by your real journey across discoveries, missions, and relics.",
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon("dashboard")}Mission Control</a><a class="button button-primary" href="./artifacts.html">${icon("artifact")}Artifact Museum</a>`,
    world: "achievements"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(4);

  try {
    const [dashboardPayload, artifactsPayload, galaxiesPayload] = await Promise.all([
      api.get("/dashboard"),
      api.get("/artifacts"),
      api.get("/galaxies")
    ]);

    const achievements = buildAchievements(dashboardPayload.data, artifactsPayload.data, galaxiesPayload.data);
    content.innerHTML = renderAchievementsPage(achievements, dashboardPayload.data, artifactsPayload.data);
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadAchievements);
    showToast({ type: "error", title: "Achievement vault unavailable", message: error.message });
  }
}

loadAchievements();
