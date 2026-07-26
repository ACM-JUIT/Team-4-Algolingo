import { api } from "../core/api.js";
import { ensureAuthenticated, fetchCurrentUser } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { createAvatar, renderErrorState, renderLoadingGrid, setButtonLoading, setInlineAlert, showToast } from "../core/ui.js";
import { escapeHtml, formatDate, formatDateTime, qs } from "../core/utils.js";

async function renderProfile(user) {
  const [profilePayload, artifactsPayload] = await Promise.all([
    api.get(`/profile/${encodeURIComponent(user.username)}`),
    api.get(`/users/${user.id}/artifacts`)
  ]);

  const profile = profilePayload.data;
  const artifacts = artifactsPayload.data.slice(0, 4);

  return `
    <section class="detail-grid">
      <div class="stack">
        <section class="hero-surface profile-hero">
          <div class="user-stack" style="align-items: flex-start; gap: 1rem;">
            ${createAvatar(user.username, user.avatar_url, true)}
            <div>
              <p class="eyebrow">Explorer logbook</p>
              <h2 class="page-title" style="font-size: clamp(1.95rem, 1.5rem + 1vw, 2.8rem);">${escapeHtml(user.username)}</h2>
              <p class="page-subtitle">${escapeHtml(user.bio || "Add a short line about what you are exploring right now and where you want to travel next.")}</p>
            </div>
          </div>
          <div class="metric-ribbon">
            <div class="segment surface-soft"><div class="metric-label">XP</div><div class="metric-value">${user.xp}</div><div class="metric-meta">Total earned so far.</div></div>
            <div class="segment surface-soft"><div class="metric-label">Level</div><div class="metric-value">${user.level}</div><div class="metric-meta">${escapeHtml(user.rank_title)}</div></div>
            <div class="segment surface-soft"><div class="metric-label">Streak</div><div class="metric-value">${user.streak_days}</div><div class="metric-meta">Days of consistency.</div></div>
          </div>
        </section>

        <section class="grid-four">
          <article class="metric-card"><div class="metric-label">Completed planets</div><div class="metric-value">${profile.stats.completed_planets}</div></article>
          <article class="metric-card"><div class="metric-label">Discoveries</div><div class="metric-value">${profile.stats.completed_discoveries}</div></article>
          <article class="metric-card"><div class="metric-label">Missions</div><div class="metric-value">${profile.stats.completed_practices}</div></article>
          <article class="metric-card"><div class="metric-label">Artifacts</div><div class="metric-value">${profile.stats.artifacts_earned}</div></article>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Logbook details</h2>
              <p class="section-description">Update the parts of your explorer identity that are meant to be visible across the universe.</p>
            </div>
          </div>
          <form id="profile-form" class="form-grid">
            <div id="profile-alert" class="form-alert"></div>
            <div class="form-row">
              <label class="form-label" for="avatar_url">Avatar URL</label>
              <input class="input" id="avatar_url" name="avatar_url" type="url" value="${escapeHtml(user.avatar_url || "")}" placeholder="https://example.com/avatar.png">
              <div class="field-error" data-field-error="avatar_url"></div>
            </div>
            <div class="form-row">
              <label class="form-label" for="bio">Bio</label>
              <textarea class="textarea" id="bio" name="bio" maxlength="500" placeholder="What are you learning right now?">${escapeHtml(user.bio || "")}</textarea>
              <div class="field-error" data-field-error="bio"></div>
            </div>
            <div class="inline">
              <button class="button button-primary" id="profile-save-button">${icon("check")}Save changes</button>
            </div>
          </form>
        </section>
      </div>

      <aside class="stack">
        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Explorer snapshot</h2>
              <p class="section-description">A concise readout of the identity and route state attached to this account.</p>
            </div>
          </div>
          <div class="info-list">
            <div class="info-row"><span>Email</span><strong>${escapeHtml(user.email)}</strong></div>
            <div class="info-row"><span>Journey state</span><strong>${escapeHtml(user.status)}</strong></div>
            <div class="info-row"><span>Explorer class</span><strong>${escapeHtml(user.role)}</strong></div>
            <div class="info-row"><span>Created</span><strong>${escapeHtml(formatDate(user.created_at))}</strong></div>
            <div class="info-row"><span>Last login</span><strong>${escapeHtml(user.last_login_date ? formatDateTime(user.last_login_date) : "—")}</strong></div>
          </div>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Recent relics</h2>
              <p class="section-description">A preview of the latest treasures added to your museum.</p>
            </div>
          </div>
          ${artifacts.length ? `
            <div class="profile-artifact-row">
              ${artifacts
                .map(
                  (item) => `
                    <div class="list-card" style="padding: 1rem;">
                      <div class="user-stack">
                        ${createAvatar(item.artifact.name, item.artifact.icon_url, true)}
                        <div>
                          <strong>${escapeHtml(item.artifact.name)}</strong>
                          <div class="activity-note">${escapeHtml(item.artifact.rarity)} · ${escapeHtml(formatDateTime(item.unlocked_at))}</div>
                        </div>
                      </div>
                    </div>
                  `
                )
                .join("")}
            </div>
          ` : '<div class="callout warning">No artifacts unlocked yet.</div>'}
          <a class="button button-secondary" href="./artifacts.html">${icon("artifact")}Open artifact museum</a>
        </section>
      </aside>
    </section>
  `;
}

async function bootstrap() {
  const user = await ensureAuthenticated();
  if (!user) return;
  initializePrivateLayout({
    user,
    activeNav: "profile",
    title: "Explorer Logbook",
    subtitle: "Review your route, your public identity, and the relics that now define your journey.",
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon("dashboard")}Mission Control</a>`,
    world: "profile"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);

  try {
    content.innerHTML = await renderProfile(user);
    const form = qs("#profile-form");
    const alert = qs("#profile-alert");
    const saveButton = qs("#profile-save-button");

    form?.addEventListener("submit", async (event) => {
      event.preventDefault();
      setInlineAlert(alert, {});
      setButtonLoading(saveButton, true, "Saving…");
      try {
        const formData = new FormData(form);
        await api.patch("/profile/me", {
          avatar_url: String(formData.get("avatar_url") || "").trim() || null,
          bio: String(formData.get("bio") || "").trim() || null
        });
        await fetchCurrentUser();
        showToast({ type: "success", title: "Profile updated", message: "Your profile changes were saved successfully." });
        bootstrap();
      } catch (error) {
        setInlineAlert(alert, { type: "error", message: error.message });
      } finally {
        setButtonLoading(saveButton, false);
      }
    });
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", bootstrap);
  }
}

bootstrap();
