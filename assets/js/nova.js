import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { renderMarkdown } from "./markdown.js";
import { getNovaSessionMap, setNovaSessionMap } from "./storage.js";
import { renderErrorState, renderLoadingGrid, setButtonLoading, showToast } from "./ui.js";
import { escapeHtml, qs } from "./utils.js";

const state = {
  sessions: getNovaSessionMap(),
  galaxies: [],
  activeTab: "ask"
};

function getSessionKey(mode, practiceId = "") {
  return mode === "hint" ? `hint:${practiceId}` : mode;
}

function rememberSession(mode, sessionId, practiceId = "") {
  state.sessions[getSessionKey(mode, practiceId)] = sessionId;
  setNovaSessionMap(state.sessions);
}

function getRememberedSession(mode, practiceId = "") {
  return state.sessions[getSessionKey(mode, practiceId)] || null;
}

function renderMessages(messages) {
  if (!messages?.length) {
    return '<div class="callout">No conversation history has been returned yet.</div>';
  }
  return `
    <div class="nova-chat">
      ${messages
        .map(
          (message) => `
            <article class="chat-bubble ${message.sender === "user" ? "user" : "assistant"}">
              <div class="chat-meta">${escapeHtml(message.sender)} · ${escapeHtml(message.created_at)}</div>
              <div class="markdown">${renderMarkdown(message.message || "")}</div>
            </article>
          `
        )
        .join("")}
    </div>
  `;
}

function galaxyOptions() {
  return ['<option value="">No galaxy context</option>']
    .concat(state.galaxies.map((galaxy) => `<option value="${galaxy.id}">${escapeHtml(galaxy.name)}</option>`))
    .join("");
}

function renderNovaPage() {
  return `
    <section class="card stack">
      <div class="section-header">
        <div>
          <h2 class="section-title">NOVA workspace</h2>
          <p class="section-description">Every form here calls the existing NOVA backend routes directly with backend-defined payloads.</p>
        </div>
      </div>
      <div class="tabs">
        <button class="tab-button ${state.activeTab === "ask" ? "is-active" : ""}" data-tab="ask">Ask</button>
        <button class="tab-button ${state.activeTab === "hint" ? "is-active" : ""}" data-tab="hint">Hint</button>
        <button class="tab-button ${state.activeTab === "debug" ? "is-active" : ""}" data-tab="debug">Debug</button>
        <button class="tab-button ${state.activeTab === "recommend" ? "is-active" : ""}" data-tab="recommend">Recommend</button>
      </div>
    </section>

    <section class="nova-grid">
      <section class="form-card stack" data-panel="ask" ${state.activeTab === "ask" ? "" : "hidden"}>
        <div class="section-header"><div><h2 class="section-title">Ask NOVA</h2><p class="section-description">General questions with optional learning context.</p></div></div>
        <form id="ask-form" class="form-grid">
          <div class="form-row"><label class="form-label" for="ask-message">Message</label><textarea class="textarea" id="ask-message" name="message" required></textarea></div>
          <div class="form-row-inline">
            <div class="form-row"><label class="form-label" for="ask-galaxy">Galaxy</label><select class="select" id="ask-galaxy" name="galaxy_id">${galaxyOptions()}</select></div>
            <div class="form-row"><label class="form-label" for="ask-planet">Planet ID</label><input class="input" id="ask-planet" name="planet_id"></div>
          </div>
          <div class="form-row-inline">
            <div class="form-row"><label class="form-label" for="ask-discovery">Discovery ID</label><input class="input" id="ask-discovery" name="discovery_id"></div>
            <div class="form-row"><label class="form-label" for="ask-practice">Practice ID</label><input class="input" id="ask-practice" name="practice_id"></div>
          </div>
          <button class="button button-primary" id="ask-button">Send question</button>
        </form>
      </section>

      <section class="form-card stack" data-panel="hint" ${state.activeTab === "hint" ? "" : "hidden"}>
        <div class="section-header"><div><h2 class="section-title">Request a hint</h2><p class="section-description">Calls <code>/nova/hint/{practice_id}</code>.</p></div></div>
        <form id="hint-form" class="form-grid">
          <div class="form-row"><label class="form-label" for="hint-practice-id">Practice ID</label><input class="input" id="hint-practice-id" name="practice_id" required></div>
          <div class="form-row"><label class="form-label" for="hint-problem">Specific problem</label><textarea class="textarea" id="hint-problem" name="specific_problem"></textarea></div>
          <div class="form-row"><label class="form-label" for="hint-code">Current code</label><textarea class="textarea" id="hint-code" name="current_code"></textarea></div>
          <button class="button button-primary" id="hint-button">Get hint</button>
        </form>
      </section>

      <section class="form-card stack" data-panel="debug" ${state.activeTab === "debug" ? "" : "hidden"}>
        <div class="section-header"><div><h2 class="section-title">Debug with NOVA</h2><p class="section-description">Share code plus optional problem context.</p></div></div>
        <form id="debug-form" class="form-grid">
          <div class="form-row"><label class="form-label" for="debug-code">Code</label><textarea class="textarea" id="debug-code" name="code" required></textarea></div>
          <div class="form-row"><label class="form-label" for="debug-problem">Problem description</label><textarea class="textarea" id="debug-problem" name="problem_description"></textarea></div>
          <div class="form-row-inline">
            <div class="form-row"><label class="form-label" for="debug-galaxy">Galaxy</label><select class="select" id="debug-galaxy" name="galaxy_id">${galaxyOptions()}</select></div>
            <div class="form-row"><label class="form-label" for="debug-planet">Planet ID</label><input class="input" id="debug-planet" name="planet_id"></div>
          </div>
          <div class="form-row"><label class="form-label" for="debug-practice">Practice ID</label><input class="input" id="debug-practice" name="practice_id"></div>
          <button class="button button-primary" id="debug-button">Debug code</button>
        </form>
      </section>

      <section class="form-card stack" data-panel="recommend" ${state.activeTab === "recommend" ? "" : "hidden"}>
        <div class="section-header"><div><h2 class="section-title">Request recommendations</h2><p class="section-description">Ask NOVA for the next best topic or review step.</p></div></div>
        <form id="recommend-form" class="form-grid">
          <div class="form-row-inline">
            <div class="form-row"><label class="form-label" for="recommend-galaxy">Galaxy</label><select class="select" id="recommend-galaxy" name="galaxy_id">${galaxyOptions()}</select></div>
            <div class="form-row"><label class="form-label" for="recommend-planet">Planet ID</label><input class="input" id="recommend-planet" name="planet_id"></div>
          </div>
          <button class="button button-primary" id="recommend-button">Get recommendation</button>
        </form>
      </section>

      <section class="card stack">
        <div class="section-header"><div><h2 class="section-title">Response</h2><p class="section-description">Rendered from the latest <code>messages</code> returned by the backend.</p></div></div>
        <div id="nova-response-root"><div class="callout">Pick a NOVA mode and submit a request.</div></div>
      </section>
    </section>
  `;
}

function bindTabs() {
  document.querySelectorAll("[data-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeTab = button.dataset.tab;
      qs("#page-content").innerHTML = renderNovaPage();
      bindTabs();
      bindForms();
    });
  });
}

function getFormValue(form, field) {
  return String(new FormData(form).get(field) || "").trim() || null;
}

function renderResponse(payload) {
  const responseRoot = qs("#nova-response-root");
  responseRoot.innerHTML = `
    <div class="callout success">Active session: ${escapeHtml(payload.session_id)}</div>
    ${renderMessages(payload.messages)}
  `;
}

function setWorking(rootText = "Generating response…") {
  qs("#nova-response-root").innerHTML = `<div class="skeleton-block" aria-label="${escapeHtml(rootText)}"></div>`;
}

function bindForms() {
  const askForm = qs("#ask-form");
  const hintForm = qs("#hint-form");
  const debugForm = qs("#debug-form");
  const recommendForm = qs("#recommend-form");

  askForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = qs("#ask-button");
    setButtonLoading(button, true, "Sending…");
    setWorking();
    try {
      const payload = await api.post("/nova/ask", {
        message: getFormValue(askForm, "message"),
        session_id: getRememberedSession("ask"),
        galaxy_id: getFormValue(askForm, "galaxy_id"),
        planet_id: getFormValue(askForm, "planet_id"),
        discovery_id: getFormValue(askForm, "discovery_id"),
        practice_id: getFormValue(askForm, "practice_id")
      });
      rememberSession("ask", payload.data.session_id);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "NOVA ask failed", message: error.message });
    } finally {
      setButtonLoading(button, false);
    }
  });

  hintForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = qs("#hint-button");
    const practiceId = getFormValue(hintForm, "practice_id");
    setButtonLoading(button, true, "Generating hint…");
    setWorking();
    try {
      const payload = await api.post(`/nova/hint/${practiceId}`, {
        current_code: getFormValue(hintForm, "current_code"),
        specific_problem: getFormValue(hintForm, "specific_problem"),
        session_id: getRememberedSession("hint", practiceId)
      });
      rememberSession("hint", payload.data.session_id, practiceId);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "NOVA hint failed", message: error.message });
    } finally {
      setButtonLoading(button, false);
    }
  });

  debugForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = qs("#debug-button");
    setButtonLoading(button, true, "Debugging…");
    setWorking();
    try {
      const payload = await api.post("/nova/debug", {
        code: getFormValue(debugForm, "code"),
        problem_description: getFormValue(debugForm, "problem_description"),
        session_id: getRememberedSession("debug"),
        galaxy_id: getFormValue(debugForm, "galaxy_id"),
        planet_id: getFormValue(debugForm, "planet_id"),
        practice_id: getFormValue(debugForm, "practice_id")
      });
      rememberSession("debug", payload.data.session_id);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "NOVA debug failed", message: error.message });
    } finally {
      setButtonLoading(button, false);
    }
  });

  recommendForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const button = qs("#recommend-button");
    setButtonLoading(button, true, "Requesting…");
    setWorking();
    try {
      const payload = await api.post("/nova/recommend", {
        session_id: getRememberedSession("recommend"),
        galaxy_id: getFormValue(recommendForm, "galaxy_id"),
        planet_id: getFormValue(recommendForm, "planet_id")
      });
      rememberSession("recommend", payload.data.session_id);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "NOVA recommendation failed", message: error.message });
    } finally {
      setButtonLoading(button, false);
    }
  });
}

async function bootstrap() {
  const user = await ensureAuthenticated();
  if (!user) return;
  initializePrivateLayout({
    user,
    activeNav: "nova",
    title: "NOVA AI",
    subtitle: "Use every currently supported NOVA endpoint from a handcrafted frontend workspace.",
    actions: '<a class="button button-secondary" href="./dashboard.html">Back to dashboard</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(2);
  try {
    const galaxiesPayload = await api.get("/galaxies");
    state.galaxies = galaxiesPayload.data;
    content.innerHTML = renderNovaPage();
    bindTabs();
    bindForms();
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", bootstrap);
  }
}

bootstrap();
