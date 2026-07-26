import { isAuthenticated } from '../core/auth.js';
import { qs } from '../core/utils.js';

const launchLink = qs('#launch-link');
const secondaryLink = qs('#secondary-link');
const statusLine = qs('#landing-status');

if (isAuthenticated()) {
  if (launchLink) {
    launchLink.href = './pages/dashboard.html';
    launchLink.textContent = 'Resume journey';
  }
  if (secondaryLink) {
    secondaryLink.href = './pages/galaxies.html';
    secondaryLink.textContent = 'Open galaxy map';
  }
  if (statusLine) statusLine.textContent = 'Active explorer session detected.';
} else {
  if (launchLink) launchLink.href = './pages/register.html';
  if (secondaryLink) secondaryLink.href = './pages/login.html';
  if (statusLine) statusLine.textContent = 'Begin a new journey or return to your existing one.';
}
