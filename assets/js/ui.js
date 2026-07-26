import { createElementFromHtml, escapeHtml, getInitials } from "./utils.js";

let activeModalCleanup = null;

function getToastRoot() {
  return document.getElementById("toast-root");
}

export function showToast({ type = "info", title = "Notice", message = "" }) {
  const root = getToastRoot();
  if (!root) return;

  const toast = createElementFromHtml(`
    <article class="toast ${type}" role="status">
      <div class="toast-title">${escapeHtml(title)}</div>
      <div class="toast-message">${escapeHtml(message)}</div>
    </article>
  `);

  root.appendChild(toast);
  window.setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(8px)";
    window.setTimeout(() => toast.remove(), 180);
  }, 3600);
}

export function renderEmptyState({ icon = "📘", title, text, actions = "" }) {
  return `
    <section class="empty-state" role="status">
      <div class="empty-state-icon" aria-hidden="true">${icon}</div>
      <div>
        <h2 class="empty-state-title">${escapeHtml(title)}</h2>
        <p class="empty-state-text">${escapeHtml(text)}</p>
      </div>
      ${actions}
    </section>
  `;
}

export function renderErrorState({ title = "Something went wrong", text, actionLabel = "Try again", actionId = "retry-action" }) {
  return `
    <section class="error-state" role="alert">
      <div class="error-state-icon" aria-hidden="true">⚠</div>
      <div>
        <h2 class="error-state-title">${escapeHtml(title)}</h2>
        <p class="error-state-text">${escapeHtml(text || "We could not complete that request.")}</p>
      </div>
      <button class="button button-secondary" id="${escapeHtml(actionId)}">${escapeHtml(actionLabel)}</button>
    </section>
  `;
}

export function renderLoadingGrid(count = 3) {
  return `
    <div class="grid-three">
      ${Array.from({ length: count })
        .map(
          () => `
            <div class="card stack">
              <div class="skeleton-line" style="width: 45%;"></div>
              <div class="skeleton-line" style="width: 85%;"></div>
              <div class="skeleton-line" style="width: 65%;"></div>
              <div class="skeleton-block"></div>
            </div>
          `
        )
        .join("")}
    </div>
  `;
}

export function createAvatar(name, avatarUrl = null, square = false) {
  if (avatarUrl) {
    return `<img class="${square ? "avatar-square" : "avatar"}" src="${escapeHtml(avatarUrl)}" alt="${escapeHtml(name)} avatar">`;
  }
  return `<span class="${square ? "avatar-square" : "avatar"}" aria-hidden="true">${escapeHtml(getInitials(name))}</span>`;
}

export function statusClass(status = "") {
  const normalized = String(status).toLowerCase().replaceAll("_", "-");
  return `status-chip status-${normalized}`;
}

export function setInlineAlert(element, { type = "error", message = "" } = {}) {
  if (!element) return;
  if (!message) {
    element.className = "form-alert";
    element.textContent = "";
    return;
  }
  element.className = `form-alert is-visible ${type}`;
  element.textContent = message;
}

export function clearFormErrors(form) {
  if (!form) return;
  form.querySelectorAll("[data-field-error]").forEach((field) => {
    field.textContent = "";
  });
  form.querySelectorAll("[aria-invalid='true']").forEach((field) => {
    field.setAttribute("aria-invalid", "false");
  });
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
    const messageTarget = form.querySelector(`[data-field-error="${fieldName}"]`);
    if (input) input.setAttribute("aria-invalid", "true");
    if (messageTarget) messageTarget.textContent = error.msg || error.message || "Invalid value";
  });
  return true;
}

export function createButtonSpinner(label = "Working…") {
  return `<span class="inline"><span aria-hidden="true">⏳</span><span>${escapeHtml(label)}</span></span>`;
}

export function setButtonLoading(button, isLoading, loadingLabel = "Working…") {
  if (!button) return;
  if (isLoading) {
    button.dataset.originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = createButtonSpinner(loadingLabel);
    return;
  }
  button.disabled = false;
  if (button.dataset.originalText) {
    button.innerHTML = button.dataset.originalText;
  }
}

function ensureModalRoot() {
  let modal = document.getElementById("modal-root");
  if (!modal) {
    modal = createElementFromHtml('<div id="modal-root" class="modal-root" aria-hidden="true"></div>');
    document.body.appendChild(modal);
  }
  return modal;
}

export function closeModal() {
  const root = document.getElementById("modal-root");
  if (root) {
    root.classList.remove("is-open");
    root.setAttribute("aria-hidden", "true");
    root.innerHTML = "";
  }
  document.body.classList.remove("no-scroll");
  if (activeModalCleanup) activeModalCleanup();
  activeModalCleanup = null;
}

export function openModal({ title, body, actions = [] }) {
  const root = ensureModalRoot();
  root.innerHTML = `
    <div class="modal-card" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div class="card-header">
        <div>
          <h2 class="card-title" id="modal-title">${escapeHtml(title)}</h2>
        </div>
        <button class="button button-ghost" data-modal-close aria-label="Close modal">✕</button>
      </div>
      <div>${typeof body === "string" ? body : ""}</div>
      <div class="modal-actions"></div>
    </div>
  `;

  const actionsRoot = root.querySelector(".modal-actions");
  actions.forEach((action) => {
    const button = createElementFromHtml(
      `<button class="button ${action.className || "button-secondary"}">${escapeHtml(action.label)}</button>`
    );
    button.addEventListener("click", () => action.onClick?.());
    actionsRoot.appendChild(button);
  });

  root.querySelector("[data-modal-close]").addEventListener("click", closeModal);
  const onBackdropClick = (event) => {
    if (event.target === root) closeModal();
  };
  root.addEventListener("click", onBackdropClick);
  const onEscape = (event) => {
    if (event.key === "Escape") closeModal();
  };
  document.addEventListener("keydown", onEscape);
  activeModalCleanup = () => {
    document.removeEventListener("keydown", onEscape);
    root.removeEventListener("click", onBackdropClick);
  };

  root.classList.add("is-open");
  root.setAttribute("aria-hidden", "false");
  document.body.classList.add("no-scroll");
}

export function confirmAction({ title, body, confirmLabel = "Confirm", cancelLabel = "Cancel", confirmClassName = "button-primary" }) {
  return new Promise((resolve) => {
    openModal({
      title,
      body,
      actions: [
        {
          label: cancelLabel,
          className: "button-secondary",
          onClick: () => {
            closeModal();
            resolve(false);
          }
        },
        {
          label: confirmLabel,
          className: confirmClassName,
          onClick: () => {
            closeModal();
            resolve(true);
          }
        }
      ]
    });
  });
}
