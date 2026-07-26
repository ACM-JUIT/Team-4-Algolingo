import { api } from '../core/api.js';
import { ensureAuthenticated } from '../core/auth.js';
import { icon } from '../core/icons.js';
import { initializePrivateLayout } from '../core/layout.js';
import { renderEmptyState, renderErrorState, renderLoadingGrid, showToast } from '../core/ui.js';
import { escapeHtml, formatDateTime, formatRelativeTime, qs } from '../core/utils.js';

function describeActivity(activity) {
  const data = activity.event_data || {};
  switch (activity.event_type) {
    case 'discovery_completed': return { title: data.discovery_title || 'Discovery logged', description: `You earned ${data.xp_awarded ?? 0} XP by completing a discovery.`, iconName: 'discovery' };
    case 'practice_completed': return { title: data.practice_title || 'Mission completed', description: `Mission reward: ${data.xp_awarded ?? 0} XP.`, iconName: 'mission' };
    case 'quiz_passed': return { title: data.planet_name || 'Boss battle cleared', description: `Score: ${data.score ?? 0}/${data.total_questions ?? 0}.`, iconName: 'quiz' };
    case 'planet_completed': return { title: data.planet_name || 'Planet secured', description: `Planet completion bonus: ${data.xp_awarded ?? 0} XP.`, iconName: 'planet' };
    case 'artifact_unlocked': return { title: data.artifact_name || 'Artifact recovered', description: 'A new relic has been added to your collection.', iconName: 'artifact' };
    case 'nova_used': return { title: 'NOVA contact', description: `Mode used: ${data.mode ?? 'assistant'}.`, iconName: 'nova' };
    default: return { title: activity.event_type.replaceAll('_', ' '), description: 'A new journey event was recorded.', iconName: 'star' };
  }
}

function buildActivityWeek(items) {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const activeDays = new Set(items.map((item) => {
    const date = new Date(item.created_at);
    date.setHours(0, 0, 0, 0);
    return date.getTime();
  }));
  return Array.from({ length: 7 }, (_, index) => {
    const date = new Date(today);
    date.setDate(today.getDate() - (6 - index));
    return { label: date.toLocaleDateString(undefined, { weekday: 'short' }), active: activeDays.has(date.getTime()), isToday: index === 6 };
  });
}

function renderWeekTrack(items) {
  const week = buildActivityWeek(items);
  const completed = week.filter((day) => day.active).length;
  return `
    <section class="mission-rhythm-card">
      <div class="reading-progress-label"><span>Flight rhythm</span><strong>${completed}/7 active days</strong></div>
      <div class="dashboard-week-grid">
        ${week.map((day) => `
          <div class="dashboard-week-cell ${day.active ? 'is-active' : ''}">
            <div class="metric-label">${escapeHtml(day.label)}</div>
            <div class="dashboard-week-dot">${day.active ? '●' : '○'}</div>
            <div class="metric-meta">${day.isToday ? 'Today' : day.active ? 'Active' : 'Quiet'}</div>
          </div>
        `).join('')}
      </div>
    </section>
  `;
}

function renderRecentActivity(items) {
  if (!items.length) {
    return renderEmptyState({ iconName: 'star', title: 'No journey events yet', text: 'Complete your first discovery or mission to populate the explorer timeline.' });
  }
  return `
    <div class="timeline">
      ${items.map((item) => {
        const summary = describeActivity(item);
        return `
          <div class="timeline-item">
            <div class="timeline-marker"></div>
            <div class="timeline-body stack" style="gap:.5rem">
              <div class="inline" style="justify-content:space-between;align-items:center;gap:1rem">
                <div class="user-stack">
                  <span class="icon-spot">${icon(summary.iconName)}</span>
                  <div>
                    <strong>${escapeHtml(summary.title)}</strong>
                    <div class="activity-note">${escapeHtml(summary.description)}</div>
                  </div>
                </div>
                <span class="activity-note">${escapeHtml(formatRelativeTime(item.created_at))}</span>
              </div>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

function renderContinueLearning(card, planetDetail) {
  if (!card) {
    return renderEmptyState({ iconName: 'planet', title: 'All current routes are complete', text: 'Explore the galaxy map, visit the museum, or ask NOVA where to travel next.' });
  }
  const artifactName = planetDetail?.artifact?.name || 'Relic reward ahead';
  const quizStatus = planetDetail?.quiz?.status || 'LOCKED';
  const nextStage = card.next_discovery_id ? 'Discovery' : card.next_practice_id ? 'Mission' : quizStatus !== 'LOCKED' ? 'Boss battle' : 'Planet review';
  return `
    <section class="journey-signal-card card">
      <div class="journey-signal-top">
        <div>
          <p class="eyebrow">Current route</p>
          <h2 class="section-title landing-system-title">${escapeHtml(card.planet_name)}</h2>
          <p class="section-description">${escapeHtml(card.galaxy_name)} is the strongest next route through the universe.</p>
        </div>
        <div class="journey-signal-ring stat-ring" data-label="${Math.round(card.progress_percent)}%\ncharted" style="--value:${card.progress_percent}%"></div>
      </div>
      <div class="journey-route-strip">
        <div class="journey-route-node is-complete"><span>Galaxy</span></div>
        <div class="journey-route-node is-active"><span>Planet</span></div>
        <div class="journey-route-node ${card.next_discovery_id ? 'is-next' : ''}"><span>Discovery</span></div>
        <div class="journey-route-node ${card.next_practice_id ? 'is-next' : ''}"><span>Mission</span></div>
        <div class="journey-route-node ${quizStatus !== 'LOCKED' ? 'is-next' : ''}"><span>Boss</span></div>
        <div class="journey-route-node"><span>Artifact</span></div>
      </div>
      <div class="metric-ribbon">
        <div class="segment surface-soft"><div class="metric-label">Current stage</div><div class="metric-value">${nextStage}</div><div class="metric-meta">Next recommended destination.</div></div>
        <div class="segment surface-soft"><div class="metric-label">Progress</div><div class="metric-value">${Math.round(card.progress_percent)}%</div><div class="metric-meta">Across discovery, mission, and battle.</div></div>
        <div class="segment surface-soft"><div class="metric-label">Artifact</div><div class="metric-value" style="font-size:.95rem;line-height:1.15">${escapeHtml(artifactName)}</div><div class="metric-meta">Treasure attached to this route.</div></div>
      </div>
      <div class="progress-stack">
        <div class="progress-labels"><span>Planet completion</span><span>${card.progress_percent.toFixed(2)}%</span></div>
        <div class="progress-bar"><span style="width:${card.progress_percent}%"></span></div>
      </div>
      <div class="inline">
        ${card.next_discovery_id ? `<a class="button button-primary" href="./discovery.html?id=${card.next_discovery_id}">${icon('discovery')}Open discovery</a>` : ''}
        ${card.next_practice_id ? `<a class="button button-secondary" href="./practice.html?id=${card.next_practice_id}">${icon('mission')}Open mission</a>` : ''}
        <a class="button button-ghost" href="./planet.html?id=${card.planet_id}">View planet</a>
      </div>
    </section>
  `;
}

function renderCommandStats(stats, leaderboardUnlocked) {
  return `
    <section class="command-stats-grid">
      <article class="command-stat command-stat-primary">
        <span class="metric-label">Explorer rank</span>
        <strong class="metric-value">${escapeHtml(stats.rank_title)}</strong>
        <span class="metric-meta">Level ${stats.level} · ${stats.xp} XP</span>
      </article>
      <article class="command-stat">
        <span class="metric-label">Streak</span>
        <strong class="metric-value">${stats.streak_days}</strong>
        <span class="metric-meta">days of consistent travel</span>
      </article>
      <article class="command-stat">
        <span class="metric-label">Constellation rank</span>
        <strong class="metric-value">${leaderboardUnlocked ? 'Open' : 'Locked'}</strong>
        <span class="metric-meta">${leaderboardUnlocked ? 'Ranking network available.' : 'Unlocks after one completed planet.'}</span>
      </article>
    </section>
  `;
}

function renderDashboard(data, planetDetail) {
  const { user, quick_stats: stats, continue_learning: continueLearning, recent_activity: activity, leaderboard_unlocked: leaderboardUnlocked } = data;
  const dailyGoalComplete = activity.some((item) => new Date(item.created_at).toDateString() === new Date().toDateString());
  return `
    <section class="dashboard-shell">
      <section class="mission-control-hero card">
        <div class="mission-control-copy">
          <p class="eyebrow">Mission Control</p>
          <h2 class="landing-system-title">Welcome back, ${escapeHtml(user.username)}.</h2>
          <p class="mission-control-subtitle">Re-enter the universe through structured discoveries, missions, boss battles, and artifact recovery.</p>
          <div class="mission-control-badges">
            <span class="badge badge-primary">${icon('bolt')} ${stats.xp} XP</span>
            <span class="badge ${dailyGoalComplete ? 'badge-success' : 'badge-warning'}">${icon(dailyGoalComplete ? 'check' : 'star')} ${dailyGoalComplete ? 'Daily objective complete' : 'Daily objective open'}</span>
          </div>
        </div>
        ${renderCommandStats(stats, leaderboardUnlocked)}
      </section>

      <section class="dashboard-top">
        ${renderContinueLearning(continueLearning, planetDetail)}

        <aside class="card stack dashboard-resume-card">
          <div class="section-header">
            <div>
              <h2 class="section-title">Launch bay</h2>
              <p class="section-description">Jump directly into the next meaningful route in your world.</p>
            </div>
          </div>
          <div class="dashboard-resume-list">
            <a class="list-card dashboard-action-card" href="./galaxies.html"><div class="user-stack"><span class="icon-spot">${icon('galaxy')}</span><div><div class="list-card-title">Open galaxy map</div><div class="list-card-description">See active, locked, and future destinations.</div></div></div></a>
            <a class="list-card dashboard-action-card" href="./leaderboard.html"><div class="user-stack"><span class="icon-spot">${icon('leaderboard')}</span><div><div class="list-card-title">View constellation rank</div><div class="list-card-description">${leaderboardUnlocked ? 'Your live ranking network is available.' : 'The ranking network unlocks later in the journey.'}</div></div></div></a>
            <a class="list-card dashboard-action-card" href="./nova.html"><div class="user-stack"><span class="icon-spot">${icon('nova')}</span><div><div class="list-card-title">Talk to NOVA</div><div class="list-card-description">Ask for guidance, debugging help, or next-route advice.</div></div></div></a>
          </div>
        </aside>
      </section>

      <section class="grid-four">
        <article class="metric-card"><div class="metric-label">Planets secured</div><div class="metric-value">${stats.completed_planets}</div><div class="metric-meta">Fully completed routes.</div></article>
        <article class="metric-card"><div class="metric-label">Discoveries logged</div><div class="metric-value">${stats.completed_discoveries}</div><div class="metric-meta">Knowledge entries archived.</div></article>
        <article class="metric-card"><div class="metric-label">Missions cleared</div><div class="metric-value">${stats.completed_practices}</div><div class="metric-meta">Hands-on missions already solved.</div></article>
        <article class="metric-card"><div class="metric-label">Artifacts earned</div><div class="metric-value">${stats.artifacts_earned}</div><div class="metric-meta">Recovered relics of mastery.</div></article>
      </section>

      <section class="dashboard-status-grid">
        <div class="card stack dashboard-activity-card">
          <div class="section-header"><div><h2 class="section-title">Explorer timeline</h2><p class="section-description">The latest events recorded for your journey.</p></div></div>
          ${renderRecentActivity(activity)}
        </div>
        <div class="dashboard-mini-facts">
          <section class="card stack">
            <div class="section-header"><div><h2 class="section-title">Journey posture</h2><p class="section-description">A compact read of your current explorer state.</p></div></div>
            <div class="dashboard-mini-row"><span>Explorer class</span><strong>${escapeHtml(user.role)}</strong></div>
            <div class="dashboard-mini-row"><span>Journey state</span><strong>${escapeHtml(user.status)}</strong></div>
            <div class="dashboard-mini-row"><span>Streak</span><strong>${stats.streak_days} days</strong></div>
            <div class="dashboard-mini-row"><span>Last login</span><strong>${escapeHtml(user.last_login_date ? formatDateTime(user.last_login_date) : 'Not available')}</strong></div>
          </section>
          <section class="card stack">
            <div class="section-header"><div><h2 class="section-title">Museum outlook</h2><p class="section-description">Artifacts shape long-term momentum.</p></div></div>
            <div class="callout info">Each unlocked artifact increases future XP through bonus percentages. Boss battle mastery compounds progress over time.</div>
            ${planetDetail?.artifact ? `<div class="callout">Nearby relic signal: ${escapeHtml(planetDetail.artifact.name)}</div>` : ''}
            <a class="button button-secondary" href="./artifacts.html">Visit artifact museum</a>
          </section>
        </div>
      </section>
    </section>
  `;
}

async function loadDashboard() {
  const user = await ensureAuthenticated();
  if (!user) return;
  initializePrivateLayout({
    user,
    activeNav: 'dashboard',
    title: 'Mission Control',
    subtitle: 'Track the current route, resume your strongest destination, and monitor exploration progress.',
    actions: `<a class="button button-secondary" href="./galaxies.html">${icon('galaxy')}Galaxy map</a><a class="button button-primary" href="./nova.html">${icon('nova')}Open NOVA</a>`,
    world: 'dashboard'
  });

  const content = qs('#page-content');
  content.innerHTML = renderLoadingGrid(4);
  try {
    const payload = await api.get('/dashboard');
    let planetDetail = null;
    if (payload.data.continue_learning?.planet_id) {
      try {
        const planetPayload = await api.get(`/planets/${payload.data.continue_learning.planet_id}`);
        planetDetail = planetPayload.data;
      } catch {
        planetDetail = null;
      }
    }
    content.innerHTML = renderDashboard(payload.data, planetDetail);
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs('#retry-action')?.addEventListener('click', loadDashboard);
    showToast({ type: 'error', title: 'Mission control unavailable', message: error.message });
  }
}

loadDashboard();
