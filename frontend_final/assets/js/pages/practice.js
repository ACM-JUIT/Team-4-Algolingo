import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { attachCodeEditor } from "../core/editor.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { enhanceRenderedMarkdown, renderMarkdown } from "../core/markdown.js";
import { getPracticeDraftKey } from "../core/storage.js";
import { confirmAction, renderEmptyState, renderErrorState, setButtonLoading, showToast, statusClass } from "../core/ui.js";
import { copyToClipboard, escapeHtml, getRequiredQueryParam, qs } from "../core/utils.js";

function humanizeStatus(status = "") {
  return String(status || "UNKNOWN").replaceAll("_", " ");
}

function findPracticeState(planet, practiceId) {
  return planet.practice_challenges.find((item) => item.id === practiceId) || null;
}

function findNextPracticeAction(planet, practiceId) {
  const practices = planet.practice_challenges || [];
  const currentIndex = practices.findIndex((item) => item.id === practiceId);
  const nextPractice = practices.slice(currentIndex + 1).find((item) => item.status !== "LOCKED" && item.status !== "COMPLETED");
  if (nextPractice) {
    return {
      href: `./practice.html?id=${nextPractice.id}`,
      label: `Launch mission ${nextPractice.order_number}`,
      iconName: "mission"
    };
  }

  if (planet.quiz?.status !== "LOCKED") {
    return {
      href: `./quiz.html?planetId=${planet.id}`,
      label: "Enter mission briefing",
      iconName: "quiz"
    };
  }

  return {
    href: `./planet.html?id=${planet.id}`,
    label: "Return to planet",
    iconName: "planet"
  };
}

function renderTestCases(testCases = []) {
  if (!testCases.length) {
    return '<div class="callout info">This mission does not reveal sample test cases yet.</div>';
  }

  return testCases
    .map(
      (testCase) => `
        <div class="test-case-item stack">
          <strong>${escapeHtml(testCase.name || "Test case")}</strong>
          <div>
            <div class="activity-note">Input</div>
            <pre>${escapeHtml(String(testCase.input || ""))}</pre>
          </div>
          <div>
            <div class="activity-note">Expected output</div>
            <pre>${escapeHtml(String(testCase.expected_output || ""))}</pre>
          </div>
        </div>
      `
    )
    .join("");
}

function renderHints(hints = []) {
  if (!hints.length) {
    return '<div class="callout info">No built-in hints were attached to this mission. Use NOVA if you need a guided nudge.</div>';
  }

  return hints.map((hint, index) => `<div class="hint-item"><strong>Hint ${index + 1}</strong><span>${escapeHtml(hint)}</span></div>`).join("");
}

function renderResultTable(result, planet, practiceId) {
  const nextAction = findNextPracticeAction(planet, practiceId);
  return `
    <section class="card stack mission-report-card ${result.passed ? "mission-report-card--success" : "mission-report-card--warning"}">
      <div class="section-header">
        <div>
          <p class="eyebrow">Mission report</p>
          <h2 class="section-title">${result.passed ? "Mission cleared" : "Mission still unstable"}</h2>
          <p class="section-description">Your code was evaluated across the full mission checklist and returned with a structured report.</p>
        </div>
        <span class="${statusClass(result.passed ? "PASSED" : "FAILED")}">${result.passed ? `${icon("check")}Passed` : `${icon("alert")}Needs revision`}</span>
      </div>
      <div class="callout ${result.passed ? "success" : "warning"}">${escapeHtml(result.feedback)}</div>
      <div class="world-hero-badges">
        <span class="badge badge-primary">${icon("spark")} ${escapeHtml(result.xp_awarded)} XP awarded</span>
        <span class="badge badge-muted">Hints used: ${escapeHtml(result.hints_used || 0)}</span>
      </div>
      <div class="table-wrap leaderboard-table">
        <table class="table">
          <thead>
            <tr>
              <th>Case</th>
              <th>Expected</th>
              <th>Actual</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            ${result.test_results
              .map(
                (row) => `
                  <tr class="${row.passed ? "result-pass" : "result-fail"}">
                    <td>${escapeHtml(row.name || "Case")}</td>
                    <td><pre>${escapeHtml(String(row.expected_output || ""))}</pre></td>
                    <td><pre>${escapeHtml(String(row.actual_output || ""))}</pre></td>
                    <td>${row.passed ? "Pass" : "Fail"}</td>
                  </tr>
                `
              )
              .join("")}
          </tbody>
        </table>
      </div>
      <div class="inline">
        <a class="button button-secondary" href="./planet.html?id=${planet.id}">${icon("planet")}Return to planet</a>
        ${result.passed ? `<a class="button button-primary" href="${nextAction.href}">${icon(nextAction.iconName)}${escapeHtml(nextAction.label)}</a>` : ""}
      </div>
    </section>
  `;
}

function missionStageStrip(state, planet) {
  const quizUnlocked = planet.quiz?.status !== "LOCKED";
  const status = state?.status || "AVAILABLE";
  return `
    <div class="stage-strip">
      <div class="stage-node is-complete"><span>Arrival</span></div>
      <div class="stage-node is-complete"><span>Discovery</span></div>
      <div class="stage-node ${status === "COMPLETED" ? "is-complete" : status === "LOCKED" ? "" : "is-active"}"><span>Mission</span></div>
      <div class="stage-node ${quizUnlocked ? "is-next" : ""}"><span>Briefing</span></div>
      <div class="stage-node ${quizUnlocked ? "is-next" : ""}"><span>Artifact</span></div>
    </div>
  `;
}

function renderPracticePage(practice, planet, state) {
  return `
    <section class="practice-shell">
      <section class="world-hero lesson-command-shell lesson-command-shell--mission">
        <div class="world-hero-copy">
          <p class="eyebrow">Mission ${escapeHtml(practice.order_number)} · ${escapeHtml(planet.name)}</p>
          <h2 class="landing-system-title">${escapeHtml(practice.title)}</h2>
          <p class="world-hero-subtitle">${escapeHtml(practice.learning_outcome || practice.description || "A guided mission that turns this planet's ideas into working code.")}</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("mission")} ${escapeHtml(humanizeStatus(state?.status || practice.status))}</span>
            <span class="badge badge-muted">${escapeHtml(humanizeStatus(practice.challenge_type || "Mission"))}</span>
            <span class="badge badge-muted">${icon("bolt")} Difficulty ${escapeHtml(practice.difficulty)}</span>
            <span class="badge badge-primary">${icon("spark")} ${escapeHtml(practice.xp_reward)} XP</span>
          </div>
          ${missionStageStrip(state, planet)}
          <div class="inline">
            <a class="button button-secondary" href="./planet.html?id=${planet.id}">${icon("chevronLeft")}Back to planet</a>
            <a class="button button-primary" href="./nova.html">${icon("nova")}Open NOVA dock</a>
          </div>
        </div>

        <div class="world-hero-visual lesson-orbitarium lesson-orbitarium--mission">
          <div class="lesson-orbit-core"></div>
          <div class="lesson-orbit-ring lesson-orbit-ring--a"></div>
          <div class="lesson-orbit-ring lesson-orbit-ring--b"></div>
          <div class="lesson-orbit-node lesson-orbit-node--read"><strong>${escapeHtml(practice.xp_reward)}</strong><span>XP</span></div>
          <div class="lesson-orbit-node lesson-orbit-node--xp"><strong>${escapeHtml(practice.difficulty)}</strong><span>Difficulty</span></div>
          <div class="lesson-orbit-node lesson-orbit-node--planet"><strong>${Math.round(Number(planet.progress?.progress_percent || 0))}</strong><span>Planet %</span></div>
        </div>
      </section>

      <section class="practice-layout practice-content-grid">
        <div class="stack practice-main-column">
          <article class="card stack mission-brief-card">
            <div class="section-header">
              <div>
                <p class="eyebrow">Mission brief</p>
                <h2 class="section-title">What this mission is asking for</h2>
                <p class="section-description">Study the brief, then solve it in the cockpit below. The mission report will judge the route fairly once you submit.</p>
              </div>
            </div>
            <div class="markdown lesson-reading">${renderMarkdown(practice.description || "No mission brief was supplied for this mission yet.")}</div>
          </article>

          <section class="code-shell mission-cockpit-shell">
            <div class="code-toolbar mission-cockpit-toolbar">
              <div>
                <strong>Mission cockpit</strong>
                <div class="activity-note">Drafts are stored locally in this browser, so your work survives accidental reloads on this device.</div>
              </div>
              <div class="inline">
                <button class="button button-secondary" id="copy-draft-button">${icon("code")}Copy code</button>
                <button class="button button-primary" id="submit-practice-button" ${state?.status === "LOCKED" ? "disabled" : ""}>${icon("mission")}Submit mission</button>
              </div>
            </div>
            <div class="code-area">
              <div class="code-gutter" id="editor-gutter"></div>
              <textarea class="code-input" id="practice-editor" spellcheck="false" aria-label="Python mission editor"></textarea>
            </div>
          </section>

          <div id="result-root"></div>
        </div>

        <aside class="practice-sidebar desktop-sticky mission-side-stack">
          <section class="card stack mission-signal-card">
            <div class="section-header">
              <div>
                <p class="eyebrow">Signal readout</p>
                <h2 class="section-title">Mission status</h2>
              </div>
            </div>
            <div class="telemetry-list">
              <div class="telemetry-row"><span>Mission state</span><strong>${escapeHtml(humanizeStatus(state?.status || practice.status))}</strong></div>
              <div class="telemetry-row"><span>Planet progress</span><strong>${escapeHtml(planet.progress?.progress_percent || 0)}%</strong></div>
              <div class="telemetry-row"><span>Outcome</span><strong>${escapeHtml(practice.learning_outcome || "Hands-on coding")}</strong></div>
            </div>
            <div class="callout ${state?.status === "LOCKED" ? "warning" : "info"}">${escapeHtml(state?.status === "LOCKED" ? "This mission is visible but still progression-locked. Reading is fine; successful completion may require earlier steps first." : "When ready, submit once. The mission report will show exactly where the route passes or breaks.")}</div>
          </section>

          <section class="card stack mission-signal-card">
            <div class="section-header">
              <div>
                <p class="eyebrow">Hint drift</p>
                <h2 class="section-title">Built-in hints</h2>
                <p class="section-description">Small nudges stored directly in the challenge payload.</p>
              </div>
            </div>
            <div class="hint-list">${renderHints(practice.hints)}</div>
          </section>

          <section class="card stack mission-signal-card">
            <div class="section-header">
              <div>
                <p class="eyebrow">Probe deck</p>
                <h2 class="section-title">Test cases</h2>
                <p class="section-description">The evaluator compares your output against these targets.</p>
              </div>
            </div>
            <div class="test-case-list">${renderTestCases(practice.test_cases)}</div>
          </section>

          <section class="card stack mission-signal-card">
            <div class="section-header">
              <div>
                <p class="eyebrow">Solution vault</p>
                <h2 class="section-title">Reveal official solution</h2>
                <p class="section-description">Use this only if you truly need a reset. Revealing the solution can reduce the XP later awarded for this mission.</p>
              </div>
            </div>
            <button class="button button-warning" id="reveal-solution-button">${icon("discovery")}Reveal official solution</button>
            <div id="solution-root"></div>
          </section>

          <section class="card stack mission-signal-card">
            <div class="section-header">
              <div>
                <p class="eyebrow">NOVA dock</p>
                <h2 class="section-title">Ask for help mid-mission</h2>
                <p class="section-description">Need a hint or a bug hunt without leaving the current route?</p>
              </div>
            </div>
            <div class="form-grid">
              <div class="form-row">
                <label class="form-label" for="nova-problem">What feels blocked?</label>
                <textarea class="textarea" id="nova-problem" placeholder="Describe the bug, confusing concept, or failed case you need help with."></textarea>
              </div>
              <div class="inline">
                <button class="button button-secondary" id="nova-hint-button">${icon("spark")}Get hint</button>
                <button class="button button-secondary" id="nova-debug-button">${icon("nova")}Debug draft</button>
              </div>
            </div>
            <div id="nova-response-root"></div>
          </section>
        </aside>
      </section>
    </section>
  `;
}

async function loadPractice() {
  const practiceId = getRequiredQueryParam("id");
  if (!practiceId) {
    window.location.href = "./galaxies.html";
    return;
  }

  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "galaxies",
    title: "Mission",
    subtitle: "Preparing the mission cockpit…",
    actions: `<a class="button button-secondary" href="./galaxies.html">${icon("galaxy")}Galaxy map</a>`,
    world: "practice"
  });

  const content = qs("#page-content");
  content.innerHTML = '<div class="skeleton-block"></div>';

  try {
    const practicePayload = await api.get(`/practices/${practiceId}`);
    const practice = practicePayload.data;
    const planetPayload = await api.get(`/planets/${practice.planet_id}`);
    let livePlanet = planetPayload.data;
    const practiceState = findPracticeState(livePlanet, practice.id);

    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: practice.title,
      subtitle: practice.learning_outcome || practice.description || "Solve the mission and submit your Python code for evaluation.",
      actions: `<a class="button button-secondary" href="./planet.html?id=${livePlanet.id}">${icon("chevronLeft")}Back to ${escapeHtml(livePlanet.name)}</a>`,
      world: "practice"
    });

    content.innerHTML = renderPracticePage(practice, livePlanet, practiceState);
    enhanceRenderedMarkdown(content);

    const draftKey = getPracticeDraftKey(practice.id);
    const editor = qs("#practice-editor");
    const gutter = qs("#editor-gutter");
    const savedDraft = localStorage.getItem(draftKey);
    editor.value = savedDraft || "";
    attachCodeEditor({
      textarea: editor,
      gutter,
      onChange: (value) => localStorage.setItem(draftKey, value)
    });

    qs("#copy-draft-button")?.addEventListener("click", async () => {
      try {
        await copyToClipboard(editor.value);
        showToast({ type: "success", title: "Code copied", message: "Your current mission draft is now in the clipboard." });
      } catch {
        showToast({ type: "error", title: "Copy failed", message: "Clipboard access is not available in this browser." });
      }
    });

    const submitButton = qs("#submit-practice-button");
    submitButton?.addEventListener("click", async () => {
      setButtonLoading(submitButton, true, "Submitting…");
      try {
        const payload = await api.post(`/practices/${practice.id}/submit`, { submitted_code: editor.value });
        try {
          const refreshedPlanet = await api.get(`/planets/${practice.planet_id}`);
          livePlanet = refreshedPlanet.data;
        } catch {
          livePlanet = livePlanet;
        }
        qs("#result-root").innerHTML = renderResultTable(payload.data, livePlanet, practice.id);
        showToast({ type: payload.data.passed ? "success" : "warning", title: payload.data.passed ? "Mission cleared" : "Mission needs revision", message: payload.data.feedback });
      } catch (error) {
        showToast({ type: "error", title: "Mission submission failed", message: error.message });
      } finally {
        setButtonLoading(submitButton, false);
      }
    });

    qs("#reveal-solution-button")?.addEventListener("click", async () => {
      const confirmed = await confirmAction({
        title: "Reveal official solution?",
        body: '<p class="activity-note">Every solution reveal is recorded. A later successful mission may award only part of the original XP.</p>',
        confirmLabel: "Reveal solution",
        confirmClassName: "button-warning"
      });
      if (!confirmed) return;
      try {
        const payload = await api.get(`/practices/${practice.id}/solution`);
        qs("#solution-root").innerHTML = `
          <div class="callout warning">If you now complete this mission, you may receive only ${escapeHtml(payload.data.xp_if_claimed)} XP.</div>
          <pre class="code-block"><code>${escapeHtml(payload.data.solution_code)}</code></pre>
        `;
        showToast({ type: "warning", title: "Solution revealed", message: "This reveal has been recorded for the mission." });
      } catch (error) {
        showToast({ type: "error", title: "Could not fetch solution", message: error.message });
      }
    });

    async function runNova(mode) {
      const responseRoot = qs("#nova-response-root");
      const problem = qs("#nova-problem")?.value.trim() || null;
      const button = qs(mode === "hint" ? "#nova-hint-button" : "#nova-debug-button");
      setButtonLoading(button, true, mode === "hint" ? "Thinking…" : "Debugging…");
      responseRoot.innerHTML = '<div class="skeleton-block"></div>';
      try {
        const payload = mode === "hint"
          ? await api.post(`/nova/hint/${practice.id}`, {
              current_code: editor.value,
              specific_problem: problem,
              session_id: null
            })
          : await api.post("/nova/debug", {
              code: editor.value,
              problem_description: problem,
              session_id: null,
              galaxy_id: null,
              planet_id: practice.planet_id,
              practice_id: practice.id
            });

        responseRoot.innerHTML = `
          <div class="chat-bubble assistant">
            <div class="chat-meta">NOVA · just now</div>
            <div class="markdown">${renderMarkdown(payload.data.reply)}</div>
          </div>
        `;
        enhanceRenderedMarkdown(responseRoot);
      } catch (error) {
        responseRoot.innerHTML = `<div class="callout error">${escapeHtml(error.message)}</div>`;
      } finally {
        setButtonLoading(button, false);
      }
    }

    qs("#nova-hint-button")?.addEventListener("click", () => runNova("hint"));
    qs("#nova-debug-button")?.addEventListener("click", () => runNova("debug"));
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadPractice);
    showToast({ type: "error", title: "Mission unavailable", message: error.message });
  }
}

loadPractice();
