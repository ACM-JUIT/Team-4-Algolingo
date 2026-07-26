import { getPostAuthRedirect, loginUser, redirectIfAuthenticated } from '../core/auth.js';
import { applyValidationErrors, setButtonLoading, setInlineAlert, showToast } from '../core/ui.js';
import { mountAmbientWorld } from '../core/ambient.js';
import { qs } from '../core/utils.js';

async function bootstrap() {
  mountAmbientWorld({ world: 'auth' });
  const redirected = await redirectIfAuthenticated('./dashboard.html');
  if (redirected) return;

  const params = new URLSearchParams(window.location.search);
  const form = qs('#login-form');
  const submitButton = qs('#login-button');
  const alert = qs('#auth-alert');

  if (params.get('message')) {
    setInlineAlert(alert, { type: 'success', message: params.get('message') });
  }

  form?.addEventListener('submit', async (event) => {
    event.preventDefault();
    applyValidationErrors(form, null);
    setInlineAlert(alert, {});

    const formData = new FormData(form);
    const payload = {
      email: String(formData.get('email') || '').trim(),
      password: String(formData.get('password') || '')
    };

    setButtonLoading(submitButton, true, 'Authenticating…');
    try {
      await loginUser(payload);
      showToast({ type: 'success', title: 'Welcome back', message: 'Your mission control session is ready.' });
      window.location.href = getPostAuthRedirect();
    } catch (error) {
      const applied = applyValidationErrors(form, error);
      setInlineAlert(alert, { type: 'error', message: applied ? 'Please review the highlighted fields.' : error.message });
    } finally {
      setButtonLoading(submitButton, false);
    }
  });
}

bootstrap();
