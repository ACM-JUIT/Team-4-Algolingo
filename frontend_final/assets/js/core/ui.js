import { icon } from './icons.js';
import { createElementFromHtml, escapeHtml, getInitials } from './utils.js';

let modalCleanup = null;

export function showToast({ type = 'info', title = 'Notice', message = '' }) {
  const root = document.getElementById('toast-root');
  if (!root) return;
  const toast = createElementFromHtml(`
    <article class="toast toast-${type}" role="status">
      <div class="toast-title">${escapeHtml(title)}</div>
      <div class="toast-message">${escapeHtml(message)}</div>
    </article>
  `);
  root.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(8px)';
    setTimeout(() => toast.remove(), 200);
  }, 3600);
}

export function renderEmptyState({ iconName = 'star', title, text, actions = '' }) {
  return `
    <section class="empty-state" role="status">
      <div class="empty-state-icon">${icon(iconName)}</div>
      <div class="stack empty-state-copy">
        <h2 class="empty-state-title">${escapeHtml(title)}</h2>
        <p class="empty-state-text">${escapeHtml(text)}</p>
      </div>
      ${actions}
    </section>
  `;
}

export function renderErrorState({ title = 'Signal lost', text = 'We could not complete that request.', actionLabel = 'Try again', actionId = 'retry-action' }) {
  return `
    <section class="error-state" role="alert">
      <div class="error-state-icon">${icon('alert')}</div>
      <div class="stack empty-state-copy">
        <h2 class="empty-state-title">${escapeHtml(title)}</h2>
        <p class="empty-state-text">${escapeHtml(text)}</p>
      </div>
      <button class="button button-secondary" id="${escapeHtml(actionId)}">${icon('refresh')}${escapeHtml(actionLabel)}</button>
    </section>
  `;
}

export function renderLoadingGrid(count = 3) {
  return `<div class="grid-three">${Array.from({ length: count }).map(() => `
    <article class="card stack">
      <div class="skeleton-line" style="width:30%"></div>
      <div class="skeleton-line" style="width:70%"></div>
      <div class="skeleton-block"></div>
    </article>
  `).join('')}</div>`;
}

export function createAvatar(name, avatarUrl = null, square = false) {
  if (avatarUrl) return `<img class="${square ? 'avatar-square' : 'avatar'}" src="${escapeHtml(avatarUrl)}" alt="${escapeHtml(name)} avatar">`;
  return `<span class="${square ? 'avatar-square' : 'avatar'}">${escapeHtml(getInitials(name))}</span>`;
}

export function statusClass(status = '') {
  return `status-chip status-${String(status).toLowerCase().replaceAll('_', '-')}`;
}

export function setInlineAlert(element, { type = 'error', message = '' } = {}) {
  if (!element) return;
  if (!message) {
    element.className = 'form-alert';
    element.textContent = '';
    return;
  }
  element.className = `form-alert is-visible ${type}`;
  element.textContent = message;
}

export function clearFormErrors(form) {
  if (!form) return;
  form.querySelectorAll('[data-field-error]').forEach((target) => { target.textContent = ''; });
  form.querySelectorAll('[aria-invalid="true"]').forEach((field) => field.setAttribute('aria-invalid', 'false'));
}

export function applyValidationErrors(form, apiError) {
  clearFormErrors(form);
  const errors = apiError?.payload?.errors;
  if (!Array.isArray(errors)) return false;
  errors.forEach((error) => {
    const location = Array.isArray(error.loc) ? error.loc : [];
    const fieldName = location[location.length - 1];
    if (!fieldName) return;
    const input = form.querySelector(`[name="${fieldName}"]`);
    const target = form.querySelector(`[data-field-error="${fieldName}"]`);
    if (input) input.setAttribute('aria-invalid', 'true');
    if (target) target.textContent = error.msg || error.message || 'Invalid value';
  });
  return true;
}

export function setButtonLoading(button, loading, label = 'Working…') {
  if (!button) return;
  if (loading) {
    button.dataset.originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = `<span class="inline"><span class="spin-icon">${icon('refresh')}</span><span>${escapeHtml(label)}</span></span>`;
    return;
  }
  button.disabled = false;
  if (button.dataset.originalText) button.innerHTML = button.dataset.originalText;
}

function ensureModalRoot() {
  let root = document.getElementById('modal-root');
  if (!root) {
    root = createElementFromHtml('<div id="modal-root" class="modal-root" aria-hidden="true"></div>');
    document.body.appendChild(root);
  }
  return root;
}

export function closeModal() {
  const root = document.getElementById('modal-root');
  if (root) {
    root.classList.remove('is-open');
    root.setAttribute('aria-hidden', 'true');
    root.innerHTML = '';
  }
  document.body.classList.remove('no-scroll');
  if (modalCleanup) modalCleanup();
  modalCleanup = null;
}

export function openModal({ title, body, actions = [] }) {
  const root = ensureModalRoot();
  root.innerHTML = `
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div class="card-header">
        <div><h2 class="card-title" id="modal-title">${escapeHtml(title)}</h2></div>
        <button class="button button-ghost" data-modal-close aria-label="Close dialog">${icon('close')}</button>
      </div>
      <div>${typeof body === 'string' ? body : ''}</div>
      <div class="modal-actions"></div>
    </div>
  `;
  const actionsRoot = root.querySelector('.modal-actions');
  actions.forEach((action) => {
    const button = createElementFromHtml(`<button class="button ${action.className || 'button-secondary'}">${escapeHtml(action.label)}</button>`);
    button.addEventListener('click', () => action.onClick?.());
    actionsRoot.appendChild(button);
  });
  root.querySelector('[data-modal-close]').addEventListener('click', closeModal);
  const onBackdrop = (event) => { if (event.target === root) closeModal(); };
  const onEscape = (event) => { if (event.key === 'Escape') closeModal(); };
  root.addEventListener('click', onBackdrop);
  document.addEventListener('keydown', onEscape);
  modalCleanup = () => {
    root.removeEventListener('click', onBackdrop);
    document.removeEventListener('keydown', onEscape);
  };
  root.classList.add('is-open');
  root.setAttribute('aria-hidden', 'false');
  document.body.classList.add('no-scroll');
}

export function confirmAction({ title, body, confirmLabel = 'Confirm', cancelLabel = 'Cancel', confirmClassName = 'button-primary' }) {
  return new Promise((resolve) => {
    openModal({
      title,
      body,
      actions: [
        { label: cancelLabel, className: 'button-secondary', onClick: () => { closeModal(); resolve(false); } },
        { label: confirmLabel, className: confirmClassName, onClick: () => { closeModal(); resolve(true); } }
      ]
    });
  });
}
