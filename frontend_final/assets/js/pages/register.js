import { getPostAuthRedirect, redirectIfAuthenticated, registerUser } from '../core/auth.js';
import { applyValidationErrors, setButtonLoading, setInlineAlert, showToast } from '../core/ui.js';
import { mountAmbientWorld } from '../core/ambient.js';
import { qs } from '../core/utils.js';

function validateBeforeSubmit(payload) {
  if (!payload.username || !payload.email || !payload.password || !payload.confirm_password) return 'All fields are required.';
  if (payload.password !== payload.confirm_password) return 'Passwords do not match.';
  return '';
}

async function bootstrap() {
  mountAmbientWorld({ world: 'auth' });
  const redirected = await redirectIfAuthenticated('./dashboard.html');
  if (redirected) return;

  const form = qs('#register-form');
  const submitButton = qs('#register-button');
  const alert = qs('#auth-alert');

  form?.addEventListener('submit', async (event) => {
    event.preventDefault();
    applyValidationErrors(form, null);
    setInlineAlert(alert, {});

    const formData = new FormData(form);
    const payload = {
      username: String(formData.get('username') || '').trim(),
      email: String(formData.get('email') || '').trim(),
      password: String(formData.get('password') || ''),
      confirm_password: String(formData.get('confirm_password') || '')
    };

    const clientError = validateBeforeSubmit(payload);
    if (clientError) {
      setInlineAlert(alert, { type: 'error', message: clientError });
      return;
    }

    setButtonLoading(submitButton, true, 'Launching…');
    try {
      await registerUser(payload);
      showToast({ type: 'success', title: 'Explorer identity created', message: 'Your journey begins now.' });
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
