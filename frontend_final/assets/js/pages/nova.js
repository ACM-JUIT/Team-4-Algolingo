import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { enhanceRenderedMarkdown, renderMarkdown } from "../core/markdown.js";
import { getNovaSessionMap, setNovaSessionMap } from "../core/storage.js";
import { renderErrorState, renderLoadingGrid, setButtonLoading, showToast } from "../core/ui.js";
import { escapeHtml, qs } from "../core/utils.js";

const state = {
  sessions: getNovaSessionMap(),
  galaxies: [],
  galaxyDetails: new Map(),
  planetDetails: new Map(),
  activeTab: "ask",
  selectedGalaxyId: "",
  selectedPlanetId: "",
  selectedDiscoveryId: "",
  selectedPracticeId: "",
  drafts: {
    askMessage: "",
    hintProblem: "",
    hintCode: "",
    debugCode: "",
    debugProblem: ""
  }
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

async function ensureGalaxyDetail(galaxyId) {
  if (!galaxyId) return null;
  if (!state.galaxyDetails.has(galaxyId)) {
    const payload = await api.get(`/galaxies/${galaxyId}`);
    state.galaxyDetails.set(galaxyId, payload.data);
  }
  return state.galaxyDetails.get(galaxyId);
}

async function ensurePlanetDetail(planetId) {
  if (!planetId) return null;
  if (!state.planetDetails.has(planetId)) {
    const payload = await api.get(`/planets/${planetId}`);
    state.planetDetails.set(planetId, payload.data);
  }
  return state.planetDetails.get(planetId);
}

function selectedGalaxy() {
  return state.galaxies.find((item) => item.id === state.selectedGalaxyId) || null;
}

function selectedPlanetSummary() {
  const galaxy = state.galaxyDetails.get(state.selectedGalaxyId);
  return galaxy?.planets?.find((item) => item.id === state.selectedPlanetId) || null;
}

function selectedPlanetDetail() {
  return state.planetDetails.get(state.selectedPlanetId) || null;
}

function optionLabel(base, status) {
  return status ? `${base} · ${status.toLowerCase().replaceAll("_", " ")}` : base;
}

function datalistOptions(items, labelBuilder) {
  return items.map((item) => `<option value="${escapeHtml(labelBuilder(item))}" data-id="${escapeHtml(item.id)}"></option>`).join("");
}

function contextValueById(items, selectedId, labelBuilder) {
  const match = items.find((item) => item.id === selectedId);
  return match ? labelBuilder(match) : "";
}

function readSelectedId(input, datalistId) {
  const list = document.getElementById(datalistId);
  const value = input.value.trim();
  const match = Array.from(list?.options || []).find((option) => option.value === value);
  return match?.dataset.id || "";
}

function renderMessages(messages) {
  if (!messages?.length) {
    return '<div class="callout info">Start a NOVA request to see the conversation history for the current mode.</div>';
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

function renderContextPanel() {
  const galaxyValue = contextValueById(state.galaxies, state.selectedGalaxyId, (item) => item.name);
  const galaxyPlanets = state.galaxyDetails.get(state.selectedGalaxyId)?.planets || [];
  const planetValue = contextValueById(galaxyPlanets, state.selectedPlanetId, (item) => optionLabel(item.name, item.status));
  const planetDetail = selectedPlanetDetail();
  const discoveries = planetDetail?.discoveries || [];
  const practices = planetDetail?.practice_challenges || [];
  const discoveryValue = contextValueById(discoveries, state.selectedDiscoveryId, (item) => optionLabel(item.title, item.status));
  const practiceValue = contextValueById(practices, state.selectedPracticeId, (item) => optionLabel(item.title, item.status));

  return `
    <section class="card stack nova-context-card mission-signal-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">Navigation lock</p>
          <h2 class="section-title">Current universe context</h2>
          <p class="section-description">Choose real galaxies, planets, discoveries, and missions from your current universe. NOVA receives the route quietly behind the scenes, so you can talk naturally.</p>
        </div>
      </div>
      <div class="form-row-inline">
        <div class="form-row">
          <label class="form-label" for="context-galaxy">Galaxy</label>
          <input class="input" id="context-galaxy" list="context-galaxy-options" value="${escapeHtml(galaxyValue)}" placeholder="Search galaxies">
          <datalist id="context-galaxy-options">${datalistOptions(state.galaxies, (item) => item.name)}</datalist>
        </div>
        <div class="form-row">
          <label class="form-label" for="context-planet">Planet</label>
          <input class="input" id="context-planet" list="context-planet-options" value="${escapeHtml(planetValue)}" placeholder="Search planets" ${state.selectedGalaxyId ? "" : "disabled"}>
          <datalist id="context-planet-options">${datalistOptions(galaxyPlanets, (item) => optionLabel(item.name, item.status))}</datalist>
        </div>
      </div>
      <div class="form-row-inline">
        <div class="form-row">
          <label class="form-label" for="context-discovery">Discovery</label>
          <input class="input" id="context-discovery" list="context-discovery-options" value="${escapeHtml(discoveryValue)}" placeholder="Search discoveries" ${state.selectedPlanetId ? "" : "disabled"}>
          <datalist id="context-discovery-options">${datalistOptions(discoveries, (item) => optionLabel(item.title, item.status))}</datalist>
        </div>
        <div class="form-row">
          <label class="form-label" for="context-practice">Mission</label>
          <input class="input" id="context-practice" list="context-practice-options" value="${escapeHtml(practiceValue)}" placeholder="Search missions" ${state.selectedPlanetId ? "" : "disabled"}>
          <datalist id="context-practice-options">${datalistOptions(practices, (item) => optionLabel(item.title, item.status))}</datalist>
        </div>
      </div>
      <div class="world-hero-badges">
        ${state.selectedGalaxyId ? `<span class="badge badge-primary">${icon("galaxy")} ${escapeHtml(selectedGalaxy()?.name || "Galaxy selected")}</span>` : ""}
        ${state.selectedPlanetId ? `<span class="badge badge-primary">${icon("planet")} ${escapeHtml(selectedPlanetSummary()?.name || "Planet selected")}</span>` : ""}
        ${state.selectedPracticeId ? `<span class="badge badge-success">${icon("mission")} Mission context ready</span>` : ""}
        ${state.selectedDiscoveryId ? `<span class="badge badge-success">${icon("discovery")} Discovery context ready</span>` : ""}
      </div>
    </section>
  `;
}

function snapshotFormDrafts() {
  const askMessage = qs("#ask-message");
  const hintProblem = qs("#hint-problem");
  const hintCode = qs("#hint-code");
  const debugCode = qs("#debug-code");
  const debugProblem = qs("#debug-problem");
  if (askMessage) state.drafts.askMessage = askMessage.value;
  if (hintProblem) state.drafts.hintProblem = hintProblem.value;
  if (hintCode) state.drafts.hintCode = hintCode.value;
  if (debugCode) state.drafts.debugCode = debugCode.value;
  if (debugProblem) state.drafts.debugProblem = debugProblem.value;
}

function renderModePanels() {
  return `
    <section class="card stack nova-task-card mission-signal-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">NOVA command deck</p>
          <h2 class="section-title">Choose a guidance mode</h2>
          <p class="section-description">Each channel is shaped around an explorer need rather than a technical workflow.</p>
        </div>
      </div>
      <div class="tabs">
        <button class="tab-button ${state.activeTab === "ask" ? "is-active" : ""}" data-tab="ask">Ask about a discovery</button>
        <button class="tab-button ${state.activeTab === "hint" ? "is-active" : ""}" data-tab="hint">Request a mission hint</button>
        <button class="tab-button ${state.activeTab === "debug" ? "is-active" : ""}" data-tab="debug">Debug a draft</button>
        <button class="tab-button ${state.activeTab === "recommend" ? "is-active" : ""}" data-tab="recommend">Plot the next route</button>
      </div>
    </section>

    <section class="card stack nova-task-card mission-signal-card">
      <div class="section-header">
        <div>
          <p class="eyebrow">Quick launch</p>
          <h2 class="section-title">Starter prompts</h2>
          <p class="section-description">Use these to begin a guided tutor-style exchange with one click.</p>
        </div>
      </div>
      <div class="nova-suggestion-grid">
        <button class="nova-suggestion" data-suggestion-mode="ask" data-suggestion-text="Can you explain the main idea behind this lesson in simpler words?">
          <strong>Explain the current discovery</strong>
          <div class="activity-note">Ask NOVA to restate the concept in clearer, simpler language.</div>
        </button>
        <button class="nova-suggestion" data-suggestion-mode="hint" data-suggestion-text="Give me a hint without showing the full solution.">
          <strong>Request a small hint</strong>
          <div class="activity-note">Best when you know the direction but need a gentle nudge.</div>
        </button>
        <button class="nova-suggestion" data-suggestion-mode="debug" data-suggestion-text="Help me find the bug and explain why it happens.">
          <strong>Debug a mission draft</strong>
          <div class="activity-note">Ideal when your code almost works but still fails a case.</div>
        </button>
        <button class="nova-suggestion" data-suggestion-mode="recommend" data-suggestion-text="What should I study next based on my current progress?">
          <strong>Ask for the next best route</strong>
          <div class="activity-note">Let NOVA interpret your current world context and suggest the best jump.</div>
        </button>
      </div>
    </section>

    <section class="card stack nova-task-card mission-signal-card" data-panel="ask" ${state.activeTab === "ask" ? "" : "hidden"}>
      <div class="section-header"><div><h2 class="section-title">Ask about what you are currently learning</h2><p class="section-description">Use the selected route context above to make NOVA's answer more precise and grounded.</p></div></div>
      <form id="ask-form" class="form-grid">
        <div class="form-row"><label class="form-label" for="ask-message">Question</label><textarea class="textarea" id="ask-message" name="message" required placeholder="Example: Can you explain why this variable name is better than the other one?">${escapeHtml(state.drafts.askMessage)}</textarea></div>
        <button class="button button-primary" id="ask-button">${icon("nova")}Ask NOVA</button>
      </form>
    </section>

    <section class="card stack nova-task-card mission-signal-card" data-panel="hint" ${state.activeTab === "hint" ? "" : "hidden"}>
      <div class="section-header"><div><h2 class="section-title">Need a hint for a mission?</h2><p class="section-description">Choose a mission from the context panel, then describe exactly where the route feels blocked.</p></div></div>
      <form id="hint-form" class="form-grid">
        <div class="callout ${state.selectedPracticeId ? "info" : "warning"}">${state.selectedPracticeId ? "Mission context is ready. NOVA will quietly include it in the request." : "Choose a mission above before requesting a hint."}</div>
        <div class="form-row"><label class="form-label" for="hint-problem">What part feels confusing?</label><textarea class="textarea" id="hint-problem" name="specific_problem" placeholder="Example: I know I need a loop, but I don't understand how to stop it correctly.">${escapeHtml(state.drafts.hintProblem)}</textarea></div>
        <div class="form-row"><label class="form-label" for="hint-code">Current code (optional)</label><textarea class="textarea" id="hint-code" name="current_code" placeholder="Paste your current solution if you want NOVA to tailor the hint.">${escapeHtml(state.drafts.hintCode)}</textarea></div>
        <button class="button button-primary" id="hint-button" ${state.selectedPracticeId ? "" : "disabled"}>${icon("spark")}Get hint</button>
      </form>
    </section>

    <section class="card stack nova-task-card mission-signal-card" data-panel="debug" ${state.activeTab === "debug" ? "" : "hidden"}>
      <div class="section-header"><div><h2 class="section-title">Debug your current draft</h2><p class="section-description">Paste the failing code and describe what feels wrong in plain language.</p></div></div>
      <form id="debug-form" class="form-grid">
        <div class="form-row"><label class="form-label" for="debug-code">Code to debug</label><textarea class="textarea" id="debug-code" name="code" required placeholder="Paste the Python code you want NOVA to inspect.">${escapeHtml(state.drafts.debugCode)}</textarea></div>
        <div class="form-row"><label class="form-label" for="debug-problem">What is going wrong?</label><textarea class="textarea" id="debug-problem" name="problem_description" placeholder="Example: The output is off by one on the last test case.">${escapeHtml(state.drafts.debugProblem)}</textarea></div>
        <button class="button button-primary" id="debug-button">${icon("code")}Debug with NOVA</button>
      </form>
    </section>

    <section class="card stack nova-task-card mission-signal-card" data-panel="recommend" ${state.activeTab === "recommend" ? "" : "hidden"}>
      <div class="section-header"><div><h2 class="section-title">Ask NOVA to plot your next route</h2><p class="section-description">Use your current galaxy or planet selection to ask where your energy should go next.</p></div></div>
      <form id="recommend-form" class="form-grid">
        <div class="callout info">Selected context is included automatically. Leave discovery and mission empty if you want high-level direction.</div>
        <button class="button button-primary" id="recommend-button">${icon("target")}Get recommendation</button>
      </form>
    </section>
  `;
}

function renderNovaPage() {
  return `
    <section class="nova-shell">
      <section class="world-hero report-hero">
        <div class="world-hero-copy">
          <p class="eyebrow">NOVA · onboard intelligence</p>
          <h2 class="landing-system-title">A guide woven into your real route through the universe.</h2>
          <p class="world-hero-subtitle">Select your current galaxy, planet, discovery, or mission by name. The frontend supplies the technical context automatically so NOVA can stay conversational.</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("nova")} Ask</span>
            <span class="badge badge-muted">${icon("spark")} Hint</span>
            <span class="badge badge-muted">${icon("code")} Debug</span>
            <span class="badge badge-primary">${icon("target")} Recommend</span>
          </div>
        </div>

        <div class="world-hero-visual report-score-visual">
          <div class="report-score-facts">
            <div class="planet-briefing-fact"><span class="metric-label">Discovery help</span><strong class="metric-value" style="font-size:1rem">Ask</strong></div>
            <div class="planet-briefing-fact"><span class="metric-label">Mission help</span><strong class="metric-value" style="font-size:1rem">Hint</strong></div>
          </div>
          <div class="report-score-facts">
            <div class="planet-briefing-fact"><span class="metric-label">Debug drafts</span><strong class="metric-value" style="font-size:1rem">Debug</strong></div>
            <div class="planet-briefing-fact"><span class="metric-label">Next route</span><strong class="metric-value" style="font-size:1rem">Recommend</strong></div>
          </div>
        </div>
      </section>

      <section class="detail-grid nova-layout-grid">
        <div class="stack nova-left-column">
          ${renderContextPanel()}
          ${renderModePanels()}
        </div>

        <aside class="card stack nova-response-card mission-signal-card desktop-sticky">
          <div class="section-header">
            <div>
              <p class="eyebrow">Response channel</p>
              <h2 class="section-title">NOVA transmission</h2>
              <p class="section-description">Conversation history for the active mode appears here and stays grouped by the saved NOVA session.</p>
            </div>
          </div>
          <div id="nova-response-root"><div class="callout info">Choose a guidance mode and NOVA will respond in a tutor-style format.</div></div>
        </aside>
      </section>
    </section>
  `;
}

function setWorking() {
  qs("#nova-response-root").innerHTML = '<div class="skeleton-block"></div>';
}

function renderResponse(payload) {
  const root = qs("#nova-response-root");
  root.innerHTML = `
    <div class="callout success">NOVA session locked. This guidance channel now remembers the recent exchange for the current mode.</div>
    ${renderMessages(payload.messages)}
  `;
  enhanceRenderedMarkdown(root);
}

function bindTabs() {
  document.querySelectorAll("[data-tab]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeTab = button.dataset.tab;
      renderAndBind();
    });
  });

  document.querySelectorAll("[data-suggestion-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      const mode = button.dataset.suggestionMode;
      const text = button.dataset.suggestionText || "";
      state.activeTab = mode;
      if (mode === "ask") state.drafts.askMessage = text;
      if (mode === "hint") state.drafts.hintProblem = text;
      if (mode === "debug") state.drafts.debugProblem = text;
      renderAndBind();
    });
  });
}

async function bindContextControls() {
  const galaxyInput = qs("#context-galaxy");
  const planetInput = qs("#context-planet");
  const discoveryInput = qs("#context-discovery");
  const practiceInput = qs("#context-practice");

  galaxyInput?.addEventListener("change", async () => {
    state.selectedGalaxyId = readSelectedId(galaxyInput, "context-galaxy-options");
    state.selectedPlanetId = "";
    state.selectedDiscoveryId = "";
    state.selectedPracticeId = "";
    if (state.selectedGalaxyId) await ensureGalaxyDetail(state.selectedGalaxyId);
    renderAndBind();
  });

  planetInput?.addEventListener("change", async () => {
    state.selectedPlanetId = readSelectedId(planetInput, "context-planet-options");
    state.selectedDiscoveryId = "";
    state.selectedPracticeId = "";
    if (state.selectedPlanetId) await ensurePlanetDetail(state.selectedPlanetId);
    renderAndBind();
  });

  discoveryInput?.addEventListener("change", () => {
    state.selectedDiscoveryId = readSelectedId(discoveryInput, "context-discovery-options");
  });

  practiceInput?.addEventListener("change", () => {
    state.selectedPracticeId = readSelectedId(practiceInput, "context-practice-options");
    renderAndBind();
  });
}

function buildAskPayload(form) {
  const formData = new FormData(form);
  return {
    message: String(formData.get("message") || "").trim(),
    session_id: getRememberedSession("ask"),
    galaxy_id: state.selectedGalaxyId || null,
    planet_id: state.selectedPlanetId || null,
    discovery_id: state.selectedDiscoveryId || null,
    practice_id: state.selectedPracticeId || null
  };
}

function buildHintPayload(form) {
  const formData = new FormData(form);
  return {
    current_code: String(formData.get("current_code") || "").trim() || null,
    specific_problem: String(formData.get("specific_problem") || "").trim() || null,
    session_id: getRememberedSession("hint", state.selectedPracticeId)
  };
}

function buildDebugPayload(form) {
  const formData = new FormData(form);
  return {
    code: String(formData.get("code") || "").trim(),
    problem_description: String(formData.get("problem_description") || "").trim() || null,
    session_id: getRememberedSession("debug"),
    galaxy_id: state.selectedGalaxyId || null,
    planet_id: state.selectedPlanetId || null,
    practice_id: state.selectedPracticeId || null
  };
}

function buildRecommendPayload() {
  return {
    session_id: getRememberedSession("recommend"),
    galaxy_id: state.selectedGalaxyId || null,
    planet_id: state.selectedPlanetId || null
  };
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
      const payload = await api.post("/nova/ask", buildAskPayload(askForm));
      rememberSession("ask", payload.data.session_id);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "NOVA could not answer", message: error.message });
    } finally {
      setButtonLoading(button, false);
    }
  });

  hintForm?.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!state.selectedPracticeId) {
      showToast({ type: "warning", title: "Choose a mission first", message: "Select a mission from the learning context panel before requesting a hint." });
      return;
    }
    const button = qs("#hint-button");
    setButtonLoading(button, true, "Generating hint…");
    setWorking();
    try {
      const payload = await api.post(`/nova/hint/${state.selectedPracticeId}`, buildHintPayload(hintForm));
      rememberSession("hint", payload.data.session_id, state.selectedPracticeId);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "Hint request failed", message: error.message });
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
      const payload = await api.post("/nova/debug", buildDebugPayload(debugForm));
      rememberSession("debug", payload.data.session_id);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "Debug request failed", message: error.message });
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
      const payload = await api.post("/nova/recommend", buildRecommendPayload());
      rememberSession("recommend", payload.data.session_id);
      renderResponse(payload.data);
    } catch (error) {
      qs("#nova-response-root").innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      showToast({ type: "error", title: "Recommendation request failed", message: error.message });
    } finally {
      setButtonLoading(button, false);
    }
  });
}

function renderAndBind() {
  snapshotFormDrafts();
  qs("#page-content").innerHTML = renderNovaPage();
  bindTabs();
  bindForms();
  bindContextControls();
}

async function bootstrap() {
  const user = await ensureAuthenticated();
  if (!user) return;
  initializePrivateLayout({
    user,
    activeNav: "nova",
    title: "NOVA AI",
    subtitle: "A guided onboard tutor that understands your current route and learning context.",
    actions: `<a class="button button-secondary" href="./dashboard.html">${icon("dashboard")}Mission Control</a>`,
    world: "nova"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(3);
  try {
    const galaxiesPayload = await api.get("/galaxies");
    state.galaxies = galaxiesPayload.data;

    const firstVisibleGalaxy = state.galaxies.find((item) => !item.is_locked) || state.galaxies[0] || null;
    state.selectedGalaxyId = firstVisibleGalaxy?.id || "";
    if (state.selectedGalaxyId) {
      const galaxy = await ensureGalaxyDetail(state.selectedGalaxyId);
      const firstPlanet = galaxy?.planets?.find((item) => item.status !== "LOCKED") || galaxy?.planets?.[0] || null;
      state.selectedPlanetId = firstPlanet?.id || "";
      if (state.selectedPlanetId) await ensurePlanetDetail(state.selectedPlanetId);
    }

    renderAndBind();
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", bootstrap);
  }
}

bootstrap();
