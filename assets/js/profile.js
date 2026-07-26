import { api } from "./api.js";
import { ensureAuthenticated, fetchCurrentUser } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { createAvatar, renderErrorState, renderLoadingGrid, setButtonLoading, setInlineAlert, showToast } from "./ui.js";
import { escapeHtml, formatDate, formatDateTime, qs } from "./utils.js";

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
        <section class="hero-surface stack">
          <div class="user-stack" style="align-items: flex-start;">
            ${createAvatar(user.username, user.avatar_url, true)}
            <div>
              <p class="eyebrow">Public profile</p>
              <h2 class="page-title" style="font-size: 2rem;">${escapeHtml(user.username)}</h2>
              <p class="page-subtitle">${escapeHtml(user.bio || "Add a short bio to tell other learners who you are and what you are working on.")}</p>
              <div class="inline" style="margin-top: 1rem;">
                <span class="badge badge-primary">${escapeHtml(user.xp)} XP</span>
                <span class="badge badge-success">Level ${escapeHtml(user.level)}</span>
                <span class="badge badge-muted">${escapeHtml(user.rank_title)}</span>
              </div>
            </div>
          </div>
        </section>

        <section class="grid-four">
          <article class="metric-card"><div class="metric-label">Completed planets</div><div class="metric-value">${profile.stats.completed_planets}</div></article>
          <article class="metric-card"><div class="metric-label">Discoveries</div><div class="metric-value">${profile.stats.completed_discoveries}</div></article>
          <article class="metric-card"><div class="metric-label">Practices</div><div class="metric-value">${profile.stats.completed_practices}</div></article>
          <article class="metric-card"><div class="metric-label">Artifacts</div><div class="metric-value">${profile.stats.artifacts_earned}</div></article>
        </section>
      </div>

      <aside class="stack">
        <section class="form-card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Edit profile</h2>
              <p class="section-description">This form submits directly to <code>/profile/me</code>.</p>
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
            <button class="button button-primary" id="profile-save-button">Save changes</button>
          </form>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Account snapshot</h2>
              <p class="section-description">Current backend account fields available to the frontend.</p>
            </div>
          </div>
          <div class="callout">Email: ${escapeHtml(user.email)}</div>
          <div class="callout">Status: ${escapeHtml(user.status)}</div>
          <div class="callout">Role: ${escapeHtml(user.role)}</div>
          <div class="callout">Created: ${escapeHtml(formatDate(user.created_at))}</div>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Recent artifacts</h2>
              <p class="section-description">A quick preview of the user's unlocked rewards.</p>
            </div>
          </div>
          ${artifacts.length ? artifacts.map((item) => `<div class="user-stack">${createAvatar(item.artifact.name, item.artifact.icon_url, true)}<div><strong>${escapeHtml(item.artifact.name)}</strong><div class="activity-note">${escapeHtml(item.artifact.rarity)} · ${escapeHtml(formatDateTime(item.unlocked_at))}</div></div></div>`).join("") : '<div class="callout warning">No artifacts unlocked yet.</div>'}
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
    title: "Profile",
    subtitle: "Review your public progress and update the editable profile fields supported by the backend.",
    actions: '<a class="button button-secondary" href="./dashboard.html">Back to dashboard</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(2);

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
        showToast({ type: "success", title: "Profile updated", message: "Your changes were saved successfully." });
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
