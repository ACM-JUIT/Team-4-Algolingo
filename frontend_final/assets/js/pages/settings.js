import { request } from '../core/api.js';
import { ensureAuthenticated, logoutUser } from '../core/auth.js';
import { icon } from '../core/icons.js';
import { initializePrivateLayout } from '../core/layout.js';
import { getApiBaseUrl, setApiBaseUrl } from '../core/storage.js';
import { renderErrorState, renderLoadingGrid, setButtonLoading, setInlineAlert, showToast } from '../core/ui.js';
import { qs } from '../core/utils.js';

function renderSettings() {
  return `
    <section class="settings-shell">
      <section class="detail-grid settings-overview-grid">
        <div class="card stack settings-overview-card">
          <div>
            <p class="eyebrow">Workspace preferences</p>
            <h2 class="page-title" style="font-size:clamp(1.72rem,1.34rem + .78vw,2.2rem)">Keep the learning environment calm, clear, and free from friction.</h2>
            <p class="page-subtitle">These settings change only this browser experience. They do not alter your account or learning history.</p>
          </div>
          <div class="metric-ribbon">
            <div class="segment surface-soft"><div class="metric-label">Interface mode</div><div class="metric-value" style="font-size:1rem">Light</div><div class="metric-meta">AlgoLingo uses one bright exploration theme.</div></div>
            <div class="segment surface-soft"><div class="metric-label">Saved drafts</div><div class="metric-value" style="font-size:1rem">Local</div><div class="metric-meta">Stored only on this device.</div></div>
            <div class="segment surface-soft"><div class="metric-label">Support</div><div class="metric-value" style="font-size:1rem">Optional</div><div class="metric-meta">Advanced connection tools stay hidden unless needed.</div></div>
          </div>
        </div>
        <aside class="card stack settings-guide-card">
          <div class="section-header"><div><h2 class="section-title">What you can change</h2><p class="section-description">Only learner-friendly settings are visible by default.</p></div></div>
          <div class="dashboard-mini-facts">
            <div class="dashboard-mini-row"><span>Appearance</span><strong>Single curated light theme</strong></div>
            <div class="dashboard-mini-row"><span>Privacy</span><strong>Sign out on this device</strong></div>
            <div class="dashboard-mini-row"><span>Drafts</span><strong>Clear local mission notes</strong></div>
            <div class="dashboard-mini-row"><span>Help</span><strong>Optional connection tools</strong></div>
          </div>
        </aside>
      </section>

      <section class="detail-grid settings-content-grid">
        <div class="stack">
          <section class="card stack settings-card">
            <div class="section-header"><div><h2 class="section-title">Appearance</h2><p class="section-description">AlgoLingo currently uses one bright, premium exploration theme by design.</p></div></div>
            <div class="callout info">Dark mode is intentionally disabled in this frontend build so the universe always keeps its light atmospheric identity.</div>
          </section>

          <section class="card stack settings-card">
            <div class="section-header"><div><h2 class="section-title">Account & privacy</h2><p class="section-description">Close your session on this browser whenever you need to secure your current device.</p></div></div>
            <div class="callout info">Signing out clears the local session on this device. Your account and learning progress remain unchanged.</div>
            <div class="inline"><button class="button button-danger" id="sign-out-button">${icon('logout')}Exit this device</button></div>
          </section>

          <section class="card stack settings-card">
            <div class="section-header"><div><h2 class="section-title">Troubleshooting</h2><p class="section-description">Only open this if AlgoLingo is connecting to a different server or if the usual local setup is failing.</p></div></div>
            <details class="settings-advanced">
              <summary><span>${icon('settings')}</span><span>Show connection tools</span></summary>
              <div class="settings-advanced-panel">
                <form id="api-settings-form" class="form-grid">
                  <div id="api-settings-alert" class="form-alert"></div>
                  <div class="form-row">
                    <label class="form-label" for="api_base_url">Connection address</label>
                    <input class="input" id="api_base_url" name="api_base_url" type="url" value="${getApiBaseUrl()}">
                  </div>
                  <div class="inline">
                    <button class="button button-primary" id="save-api-button">${icon('check')}Save</button>
                    <button class="button button-secondary" type="button" id="test-api-button">${icon('refresh')}Test</button>
                    <button class="button button-ghost" type="button" id="reset-api-button">Reset</button>
                  </div>
                </form>
                <div class="settings-note">Use this only if your app should connect somewhere other than the usual local address.</div>
              </div>
            </details>
          </section>
        </div>

        <aside class="settings-rail">
          <section class="card stack settings-card">
            <div class="section-header"><div><h2 class="section-title">Local browser data</h2><p class="section-description">Mission drafts are stored only in this browser and can be cleared independently of your account.</p></div></div>
            <div class="callout">Clear saved drafts if you want a fresh start for local mission notes on this device.</div>
            <button class="button button-secondary" id="clear-drafts-button">${icon('refresh')}Clear saved drafts</button>
          </section>
        </aside>
      </section>
    </section>
  `;
}

async function bootstrap() {
  const user = await ensureAuthenticated();
  if (!user) return;
  initializePrivateLayout({
    user,
    activeNav: 'settings',
    title: 'Settings',
    subtitle: 'Adjust the local explorer environment without turning the page into a technical console.',
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon('dashboard')}Mission Control</a>`,
    world: 'settings'
  });

  const content = qs('#page-content');
  content.innerHTML = renderLoadingGrid(2);
  content.innerHTML = renderSettings();

  qs('#sign-out-button')?.addEventListener('click', () => logoutUser());
  qs('#clear-drafts-button')?.addEventListener('click', () => {
    Object.keys(localStorage).filter((key) => key.startsWith('algolingo-final:practice-draft:')).forEach((key) => localStorage.removeItem(key));
    showToast({ type: 'success', title: 'Drafts cleared', message: 'All locally saved mission drafts were removed.' });
  });

  const form = qs('#api-settings-form');
  const alert = qs('#api-settings-alert');
  const saveButton = qs('#save-api-button');
  const testButton = qs('#test-api-button');

  form?.addEventListener('submit', (event) => {
    event.preventDefault();
    const nextUrl = String(new FormData(form).get('api_base_url') || '').trim();
    setApiBaseUrl(nextUrl);
    setInlineAlert(alert, { type: 'success', message: 'This connection preference was saved for this browser.' });
  });

  testButton?.addEventListener('click', async () => {
    setButtonLoading(testButton, true, 'Testing…');
    setInlineAlert(alert, {});
    try {
      const formData = new FormData(form);
      setApiBaseUrl(String(formData.get('api_base_url') || '').trim());
      await request('/health', { auth: false });
      setInlineAlert(alert, { type: 'success', message: 'Connection successful. The selected address responded correctly.' });
    } catch (error) {
      setInlineAlert(alert, { type: 'error', message: error.message });
    } finally {
      setButtonLoading(testButton, false);
    }
  });

  qs('#reset-api-button')?.addEventListener('click', () => {
    setApiBaseUrl('');
    qs('#api_base_url').value = getApiBaseUrl();
    showToast({ type: 'success', title: 'Connection reset', message: 'The default local connection address was restored.' });
  });
}

bootstrap();
