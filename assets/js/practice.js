import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { attachCodeEditor } from "./editor.js";
import { initializePrivateLayout } from "./layout.js";
import { renderMarkdown } from "./markdown.js";
import { getPracticeDraftKey } from "./storage.js";
import { confirmAction, renderErrorState, setButtonLoading, showToast, statusClass } from "./ui.js";
import { escapeHtml, getRequiredQueryParam, qs } from "./utils.js";

function findPracticeState(planet, practiceId) {
  return planet.practice_challenges.find((item) => item.id === practiceId) || null;
}

function renderTestCases(testCases) {
  return testCases
    .map(
      (testCase) => `
        <div class="test-case-item">
          <strong>${escapeHtml(testCase.name || "Test case")}</strong>
          <div class="activity-note">Input</div>
          <pre>${escapeHtml(String(testCase.input || ""))}</pre>
          <div class="activity-note">Expected output</div>
          <pre>${escapeHtml(String(testCase.expected_output || ""))}</pre>
        </div>
      `
    )
    .join("");
}

function renderHints(hints) {
  return hints.map((hint) => `<div class="hint-item">${escapeHtml(hint)}</div>`).join("");
}

function renderResultTable(result) {
  if (!result) return "";
  return `
    <section class="card stack">
      <div class="section-header">
        <div>
          <h2 class="section-title">Submission result</h2>
          <p class="section-description">The backend evaluated your code against the configured test cases.</p>
        </div>
        <span class="${statusClass(result.passed ? "PASSED" : "FAILED")}">${result.passed ? "Passed" : "Needs work"}</span>
      </div>
      <div class="callout ${result.passed ? "success" : "warning"}">${escapeHtml(result.feedback)}</div>
      <div class="inline">
        <span class="badge badge-primary">${escapeHtml(result.xp_awarded)} XP awarded</span>
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
    </section>
  `;
}

function renderPracticePage(practice, planet, state) {
  return `
    <section class="hero-surface stack">
      <div class="hero-grid">
        <div>
          <p class="eyebrow">Practice ${escapeHtml(practice.order_number)}</p>
          <h2 class="page-title" style="font-size: 2rem;">${escapeHtml(practice.title)}</h2>
          <p class="page-subtitle">${escapeHtml(practice.learning_outcome || practice.description || "Backend-evaluated coding challenge.")}</p>
          <div class="inline" style="margin-top: 1rem;">
            <span class="${statusClass(state?.status || practice.status)}">${escapeHtml((state?.status || practice.status).replaceAll("_", " "))}</span>
            <span class="badge badge-primary">${escapeHtml(practice.xp_reward)} XP</span>
            <span class="badge badge-muted">${escapeHtml(practice.challenge_type.replaceAll("_", " "))}</span>
          </div>
        </div>
        <div class="card stack">
          <div class="callout warning">Separate code execution is not exposed by the backend. This interface submits directly to the backend evaluator when you click submit.</div>
          <div class="callout">Viewing the official solution records a backend event and may reduce later XP to half.</div>
        </div>
      </div>
    </section>

    <section class="practice-layout">
      <div class="stack">
        <article class="card markdown">
          ${renderMarkdown(practice.description || "No description available.")}
        </article>

        <section class="code-shell">
          <div class="code-toolbar">
            <div>
              <strong>Solution editor</strong>
              <div class="activity-note">Your draft is saved locally in this browser.</div>
            </div>
            <div class="inline">
              <button class="button button-secondary" id="copy-draft-button">Copy code</button>
              <button class="button button-primary" id="submit-practice-button" ${state?.status === "LOCKED" ? "disabled" : ""}>Submit solution</button>
            </div>
          </div>
          <div class="code-area">
            <div class="code-gutter" id="editor-gutter"></div>
            <textarea class="code-input" id="practice-editor" spellcheck="false" aria-label="Python editor"></textarea>
          </div>
        </section>

        <div id="result-root"></div>
      </div>

      <aside class="stack">
        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Challenge details</h2>
              <p class="section-description">Backend-provided metadata for this exercise.</p>
            </div>
          </div>
          <div class="callout">Planet progress: ${escapeHtml(planet.progress?.progress_percent || 0)}%</div>
          <div class="callout">Difficulty: ${escapeHtml(practice.difficulty)}</div>
          ${state?.status === "LOCKED" ? '<div class="callout warning">This practice is still locked according to planet progression. You can read it, but the backend may reject completion until earlier steps are finished.</div>' : ""}
          <a class="button button-secondary" href="./planet.html?id=${planet.id}">Back to planet</a>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Hints</h2>
              <p class="section-description">Local hints from the backend challenge record.</p>
            </div>
          </div>
          <div class="hint-list">${renderHints(practice.hints)}</div>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Test cases</h2>
              <p class="section-description">The evaluator compares your output with these expectations.</p>
            </div>
          </div>
          <div class="test-case-list">${renderTestCases(practice.test_cases)}</div>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Official solution</h2>
              <p class="section-description">Reveal the backend-stored solution only when you need it.</p>
            </div>
          </div>
          <button class="button button-warning" id="reveal-solution-button">Reveal solution</button>
          <div id="solution-root"></div>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">NOVA help</h2>
              <p class="section-description">Request a contextual hint or debugging guidance.</p>
            </div>
          </div>
          <div class="form-grid">
            <div class="form-row">
              <label class="form-label" for="nova-problem">Specific problem (optional)</label>
              <textarea class="textarea" id="nova-problem" placeholder="Describe where you are stuck."></textarea>
            </div>
            <div class="inline">
              <button class="button button-secondary" id="nova-hint-button">Get hint</button>
              <button class="button button-secondary" id="nova-debug-button">Debug code</button>
            </div>
          </div>
          <div id="nova-response-root"></div>
        </section>
      </aside>
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
    title: "Practice",
    subtitle: "Loading practice challenge…",
    actions: '<a class="button button-secondary" href="./galaxies.html">All galaxies</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = '<div class="skeleton-block"></div>';

  try {
    const practicePayload = await api.get(`/practices/${practiceId}`);
    const practice = practicePayload.data;
    const planetPayload = await api.get(`/planets/${practice.planet_id}`);
    const planet = planetPayload.data;
    const practiceState = findPracticeState(planet, practice.id);

    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: practice.title,
      subtitle: practice.description || "Solve the challenge and submit your Python code to the backend evaluator.",
      actions: `<a class="button button-secondary" href="./planet.html?id=${planet.id}">Back to ${escapeHtml(planet.name)}</a>`
    });

    content.innerHTML = renderPracticePage(practice, planet, practiceState);

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
        await navigator.clipboard.writeText(editor.value);
        showToast({ type: "success", title: "Code copied", message: "Your current draft is in the clipboard." });
      } catch {
        showToast({ type: "error", title: "Copy failed", message: "Clipboard access is not available in this browser." });
      }
    });

    const submitButton = qs("#submit-practice-button");
    submitButton?.addEventListener("click", async () => {
      setButtonLoading(submitButton, true, "Submitting…");
      try {
        const payload = await api.post(`/practices/${practice.id}/submit`, { submitted_code: editor.value });
        const resultRoot = qs("#result-root");
        resultRoot.innerHTML = renderResultTable(payload.data);
        showToast({
          type: payload.data.passed ? "success" : "warning",
          title: payload.data.passed ? "Practice passed" : "Practice needs revision",
          message: payload.data.feedback
        });
      } catch (error) {
        showToast({ type: "error", title: "Submission failed", message: error.message });
      } finally {
        setButtonLoading(submitButton, false);
      }
    });

    qs("#reveal-solution-button")?.addEventListener("click", async () => {
      const confirmed = await confirmAction({
        title: "Reveal official solution?",
        body: '<p class="activity-note">The backend records solution views. If you later pass this challenge, your awarded XP may be reduced to half.</p>',
        confirmLabel: "Reveal solution",
        confirmClassName: "button-warning"
      });
      if (!confirmed) return;
      try {
        const payload = await api.get(`/practices/${practice.id}/solution`);
        qs("#solution-root").innerHTML = `
          <div class="callout warning">Viewing the solution means later completion may award only ${escapeHtml(payload.data.xp_if_claimed)} XP.</div>
          <pre class="code-block"><code>${escapeHtml(payload.data.solution_code)}</code></pre>
        `;
        showToast({ type: "warning", title: "Solution revealed", message: "The backend has recorded this solution view." });
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
    showToast({ type: "error", title: "Practice unavailable", message: error.message });
  }
}

loadPractice();
