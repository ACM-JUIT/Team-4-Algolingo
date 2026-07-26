import { request } from "./api.js";
import { ensureAuthenticated, getSessionData, logoutUser } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { applyTheme } from "./theme.js";
import { getApiBaseUrl, setApiBaseUrl } from "./storage.js";
import { renderErrorState, renderLoadingGrid, setButtonLoading, setInlineAlert, showToast } from "./ui.js";
import { escapeHtml, qs } from "./utils.js";

function renderSettings(session) {
  return `
    <section class="detail-grid">
      <div class="stack">
        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Appearance</h2>
              <p class="section-description">Theme preference is stored in <code>localStorage</code>.</p>
            </div>
          </div>
          <div class="settings-list">
            <div class="settings-item">
              <div>
                <strong>Theme</strong>
                <div class="activity-note">Switch between light and dark without a page flash.</div>
              </div>
              <div class="inline">
                <button class="button button-secondary" data-set-theme="light">Light</button>
                <button class="button button-secondary" data-set-theme="dark">Dark</button>
              </div>
            </div>
          </div>
        </section>

        <section class="form-card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">API endpoint</h2>
              <p class="section-description">Use this if the backend is running somewhere other than the default <code>http://localhost:8000/api/v1</code>.</p>
            </div>
          </div>
          <form id="api-settings-form" class="form-grid">
            <div id="api-settings-alert" class="form-alert"></div>
            <div class="form-row">
              <label class="form-label" for="api_base_url">API base URL</label>
              <input class="input" id="api_base_url" name="api_base_url" type="url" value="${escapeHtml(getApiBaseUrl())}">
            </div>
            <div class="inline">
              <button class="button button-primary" id="save-api-button">Save API URL</button>
              <button class="button button-secondary" type="button" id="test-api-button">Test connection</button>
              <button class="button button-ghost" type="button" id="reset-api-button">Reset</button>
            </div>
          </form>
        </section>
      </div>

      <aside class="stack">
        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Session summary</h2>
              <p class="section-description">Stored tokens are used for access, refresh, and logout.</p>
            </div>
          </div>
          <div class="callout">Signed in as ${escapeHtml(session.user.username)}</div>
          <div class="callout">Token type: ${escapeHtml(session.tokens.token_type)}</div>
          <div class="callout">Access token lifetime: ${escapeHtml(session.tokens.expires_in)} seconds</div>
          <button class="button button-danger" id="sign-out-button">Sign out everywhere on this device</button>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Local browser data</h2>
              <p class="section-description">Practice drafts are saved only in this browser.</p>
            </div>
          </div>
          <button class="button button-secondary" id="clear-drafts-button">Clear saved drafts</button>
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
    activeNav: "settings",
    title: "Settings",
    subtitle: "Adjust the frontend runtime environment without changing the backend contract.",
    actions: '<a class="button button-secondary" href="./dashboard.html">Back to dashboard</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(1);

  const session = getSessionData();
  if (!session) {
    content.innerHTML = renderErrorState({ text: "No session data is available." });
    return;
  }

  content.innerHTML = renderSettings(session);

  qs("#sign-out-button")?.addEventListener("click", () => logoutUser());
  qs("#clear-drafts-button")?.addEventListener("click", () => {
    Object.keys(localStorage)
      .filter((key) => key.startsWith("algolingo:practice-draft:"))
      .forEach((key) => localStorage.removeItem(key));
    showToast({ type: "success", title: "Drafts cleared", message: "All locally saved practice drafts were removed." });
  });

  document.querySelectorAll("[data-set-theme]").forEach((button) => {
    button.addEventListener("click", () => {
      applyTheme(button.dataset.setTheme);
      showToast({ type: "success", title: "Theme updated", message: `Switched to ${button.dataset.setTheme} mode.` });
    });
  });

  const form = qs("#api-settings-form");
  const alert = qs("#api-settings-alert");
  const saveButton = qs("#save-api-button");
  const testButton = qs("#test-api-button");

  form?.addEventListener("submit", (event) => {
    event.preventDefault();
    const nextUrl = String(new FormData(form).get("api_base_url") || "").trim();
    setApiBaseUrl(nextUrl);
    setInlineAlert(alert, { type: "success", message: "API base URL saved. Future requests will use this value." });
  });

  testButton?.addEventListener("click", async () => {
    setButtonLoading(testButton, true, "Testing…");
    setInlineAlert(alert, {});
    try {
      const formData = new FormData(form);
      setApiBaseUrl(String(formData.get("api_base_url") || "").trim());
      const response = await request("/health", { auth: false });
      setInlineAlert(alert, { type: "success", message: `Connection successful: ${response.message || "Health endpoint responded."}` });
    } catch (error) {
      setInlineAlert(alert, { type: "error", message: error.message });
    } finally {
      setButtonLoading(testButton, false);
    }
  });

  qs("#reset-api-button")?.addEventListener("click", () => {
    setApiBaseUrl("");
    qs("#api_base_url").value = getApiBaseUrl();
    showToast({ type: "success", title: "API URL reset", message: "The default local backend URL was restored." });
  });
}

bootstrap();
