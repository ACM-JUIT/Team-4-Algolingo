import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { enhanceRenderedMarkdown, renderMarkdown } from "../core/markdown.js";
import { renderEmptyState, renderErrorState, setButtonLoading, showToast, statusClass } from "../core/ui.js";
import { escapeHtml, formatPercentage, getRequiredQueryParam, qs } from "../core/utils.js";

let questions = [];
let answers = {};
let currentIndex = 0;
let planet = null;

function humanizeStatus(status = "") {
  return String(status || "UNKNOWN").replaceAll("_", " ");
}

function currentQuestion() {
  return questions[currentIndex];
}

function answeredCount() {
  return Object.values(answers).filter((value) => String(value || "").trim()).length;
}

function renderOption(option, selected) {
  return `
    <label class="answer-option ${selected ? "is-selected" : ""}">
      <input type="radio" name="quiz-answer" value="${escapeHtml(option.id)}" ${selected ? "checked" : ""}>
      <div class="answer-option-copy">
        <strong>${escapeHtml(option.id)}</strong>
        <span>${escapeHtml(option.text)}</span>
      </div>
    </label>
  `;
}

function briefingStageStrip() {
  return `
    <div class="stage-strip">
      <div class="stage-node is-complete"><span>Arrival</span></div>
      <div class="stage-node is-complete"><span>Discoveries</span></div>
      <div class="stage-node is-complete"><span>Missions</span></div>
      <div class="stage-node is-active"><span>Briefing</span></div>
      <div class="stage-node is-next"><span>Artifact</span></div>
    </div>
  `;
}

function renderQuestionView() {
  const question = currentQuestion();
  if (!question) {
    return renderEmptyState({ iconName: "quiz", title: "No briefing questions found", text: "This planet currently has no visible briefing questions." });
  }

  const selectedAnswer = answers[question.id] || "";
  const answerOptions = question.options?.length
    ? question.options.map((option) => renderOption(option, selectedAnswer === option.id)).join("")
    : `
      <div class="form-row">
        <label class="form-label" for="typed-answer">Your answer</label>
        <input class="input" id="typed-answer" value="${escapeHtml(selectedAnswer)}" placeholder="Type your answer here">
      </div>
    `;

  const completionPercent = (answeredCount() / Math.max(questions.length, 1)) * 100;

  return `
    <section class="quiz-shell">
      <section class="world-hero lesson-command-shell lesson-command-shell--briefing">
        <div class="world-hero-copy">
          <p class="eyebrow">Mission briefing · ${escapeHtml(planet.name)}</p>
          <h2 class="landing-system-title">Hold the route in memory, then answer with confidence.</h2>
          <p class="world-hero-subtitle">Questions are shown without correct answers. The truth is revealed only after you submit the briefing.</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("quiz")} ${escapeHtml(humanizeStatus(planet.quiz?.status || "AVAILABLE"))}</span>
            <span class="badge badge-muted">${icon("spark")} ${questions.reduce((sum, item) => sum + (Number(item.xp_reward) || 0), 0)} XP potential</span>
            <span class="badge badge-muted">${icon("bolt")} ${answeredCount()}/${questions.length} answered</span>
          </div>
          ${briefingStageStrip()}
          <div class="reading-progress-shell briefing-progress-shell">
            <div class="reading-progress-label"><span>Briefing completion</span><strong>${answeredCount()}/${questions.length}</strong></div>
            <div class="progress-bar"><span style="width:${completionPercent}%"></span></div>
          </div>
        </div>

        <div class="world-hero-visual lesson-orbitarium lesson-orbitarium--briefing">
          <div class="lesson-orbit-core"></div>
          <div class="lesson-orbit-ring lesson-orbit-ring--a"></div>
          <div class="lesson-orbit-ring lesson-orbit-ring--b"></div>
          <div class="lesson-orbit-node lesson-orbit-node--read"><strong>${currentIndex + 1}</strong><span>Current</span></div>
          <div class="lesson-orbit-node lesson-orbit-node--xp"><strong>${questions.length}</strong><span>Questions</span></div>
          <div class="lesson-orbit-node lesson-orbit-node--planet"><strong>${answeredCount()}</strong><span>Answered</span></div>
        </div>
      </section>

      <div class="quiz-layout briefing-layout">
        <section class="card stack question-panel">
          <div class="question-panel-head">
            <div>
              <p class="eyebrow">Question ${currentIndex + 1}</p>
              <h2 class="section-title">${escapeHtml(humanizeStatus(question.question_type || "Question"))}</h2>
              <p class="section-description">Difficulty ${escapeHtml(question.difficulty || "—")} · ${escapeHtml(question.order_number || currentIndex + 1)} in the current sequence</p>
            </div>
            <span class="badge badge-primary">${icon("spark")} ${escapeHtml(question.xp_reward)} XP</span>
          </div>
          <article class="markdown question-markdown">${renderMarkdown(question.question_text)}</article>
          <div class="answer-options">${answerOptions}</div>
          <div class="inline briefing-actions">
            <button class="button button-secondary" id="prev-question-button" ${currentIndex === 0 ? "disabled" : ""}>${icon("chevronLeft")}Previous</button>
            <div class="inline">
              <button class="button button-secondary" id="next-question-button">${currentIndex === questions.length - 1 ? "Review answers" : `Next${icon("chevronRight")}`}</button>
              <button class="button button-primary" id="submit-quiz-button">${icon("quiz")}Submit briefing</button>
            </div>
          </div>
        </section>

        <aside class="question-nav desktop-sticky">
          <section class="card stack question-map-card">
            <div class="section-header">
              <div>
                <p class="eyebrow">Navigation map</p>
                <h2 class="section-title">Question field</h2>
                <p class="section-description">Move freely through the briefing while tracking what has already been answered.</p>
              </div>
            </div>
            <div class="question-nav-grid">
              ${questions
                .map(
                  (item, index) => `
                    <button class="question-nav-button ${index === currentIndex ? "is-current" : ""} ${answers[item.id] ? "is-answered" : ""}" data-question-index="${index}">
                      ${index + 1}
                    </button>
                  `
                )
                .join("")}
            </div>
            <div class="telemetry-list">
              <div class="telemetry-row"><span>Briefing state</span><strong>${escapeHtml(humanizeStatus(planet.quiz?.status || "AVAILABLE"))}</strong></div>
              <div class="telemetry-row"><span>Attempts</span><strong>${escapeHtml(planet.quiz?.attempts_count || 0)}</strong></div>
              <div class="telemetry-row"><span>Best score</span><strong>${escapeHtml((planet.quiz?.best_score ?? planet.progress?.quiz_best_score) ?? "—")}</strong></div>
            </div>
            <div class="callout info">You may submit with partial answers, but only the responses you provide will be scored.</div>
          </section>
        </aside>
      </div>
    </section>
  `;
}

function renderResults(result) {
  const scorePercent = Number(result.percentage || 0);
  return `
    <section class="report-shell stack">
      <section class="world-hero report-hero ${result.passed ? "report-hero--success" : "report-hero--warning"}">
        <div class="world-hero-copy">
          <p class="eyebrow">Mission report · ${escapeHtml(planet.name)}</p>
          <h2 class="landing-system-title">${result.passed ? "Boss battle cleared" : "Boss battle reviewed"}</h2>
          <p class="world-hero-subtitle">Score: ${result.score} out of ${result.total_questions} (${formatPercentage(scorePercent)}). This attempt now stands in your record as ${escapeHtml(humanizeStatus(result.quiz_status))}.</p>
          <div class="world-hero-badges">
            <span class="${statusClass(result.quiz_status)}">${escapeHtml(humanizeStatus(result.quiz_status))}</span>
            <span class="badge badge-primary">${icon("spark")} ${escapeHtml(result.xp_awarded)} XP awarded</span>
          </div>
          <div class="inline">
            <a class="button button-secondary" href="./planet.html?id=${planet.id}">${icon("planet")}Return to planet</a>
            <a class="button button-primary" href="./artifacts.html">${icon("artifact")}Open museum</a>
          </div>
        </div>

        <div class="world-hero-visual report-score-visual">
          <div class="stat-ring stat-ring--large" data-label="${Math.round(scorePercent)}%\nscore" style="--value:${scorePercent}%"></div>
          <div class="report-score-facts">
            <div class="planet-briefing-fact"><span class="metric-label">Correct</span><strong class="metric-value">${result.score}</strong></div>
            <div class="planet-briefing-fact"><span class="metric-label">Questions</span><strong class="metric-value">${result.total_questions}</strong></div>
          </div>
        </div>
      </section>

      <section class="card stack report-summary-card">
        ${result.artifact_unlocked
          ? `<div class="callout success">Artifact unlocked: ${escapeHtml(result.artifact_unlocked.name)} (+${escapeHtml(result.artifact_unlocked.xp_bonus_percent)}% XP bonus)</div>`
          : '<div class="callout info">No new artifact was unlocked by this briefing.</div>'}
      </section>

      <section class="stack report-list">
        ${result.results
          .map(
            (item, index) => `
              <article class="card stack report-item ${item.is_correct ? "result-pass" : "result-fail"}">
                <div class="result-row">
                  <div>
                    <p class="eyebrow">Question ${index + 1}</p>
                    <h3 class="card-title">${item.is_correct ? "Correct answer" : "Needs review"}</h3>
                  </div>
                  <span class="${statusClass(item.is_correct ? "PASSED" : "FAILED")}">${item.is_correct ? `${icon("check")}Correct` : `${icon("alert")}Incorrect`}</span>
                </div>
                <div class="callout">Submitted answer: ${escapeHtml(item.submitted_answer || "No answer")}</div>
                <div class="callout info">Correct answer: ${escapeHtml(item.correct_answer)}</div>
                ${item.explanation ? `<div class="markdown">${renderMarkdown(item.explanation)}</div>` : ""}
              </article>
            `
          )
          .join("")}
      </section>
    </section>
  `;
}

function bindQuizInteractions() {
  const question = currentQuestion();

  document.querySelectorAll('input[name="quiz-answer"]').forEach((input) => {
    input.addEventListener("change", (event) => {
      answers[question.id] = event.target.value;
      renderQuiz();
    });
  });

  qs("#typed-answer")?.addEventListener("input", (event) => {
    answers[question.id] = event.target.value;
  });

  qs("#prev-question-button")?.addEventListener("click", () => {
    currentIndex = Math.max(0, currentIndex - 1);
    renderQuiz();
  });

  qs("#next-question-button")?.addEventListener("click", () => {
    currentIndex = Math.min(questions.length - 1, currentIndex + 1);
    renderQuiz();
  });

  document.querySelectorAll("[data-question-index]").forEach((button) => {
    button.addEventListener("click", () => {
      currentIndex = Number(button.dataset.questionIndex);
      renderQuiz();
    });
  });

  const submitButton = qs("#submit-quiz-button");
  submitButton?.addEventListener("click", async () => {
    const submittedAnswers = questions
      .map((item) => ({ question_id: item.id, answer: answers[item.id] || "" }))
      .filter((item) => item.answer && String(item.answer).trim());

    if (!submittedAnswers.length) {
      showToast({ type: "warning", title: "Answer at least one question", message: "Submit at least one answer before sending the briefing." });
      return;
    }

    setButtonLoading(submitButton, true, "Submitting…");
    try {
      const payload = await api.post(`/quizzes/${planet.id}/submit`, { answers: submittedAnswers });
      const pageContent = qs("#page-content");
      pageContent.innerHTML = renderResults(payload.data);
      enhanceRenderedMarkdown(pageContent);
      showToast({
        type: payload.data.passed ? "success" : "warning",
        title: payload.data.passed ? "Boss battle cleared" : "Briefing submitted",
        message: payload.data.passed ? `You earned ${payload.data.xp_awarded} XP.` : "Review the report, then continue refining your command of this world."
      });
    } catch (error) {
      showToast({ type: "error", title: "Briefing submission failed", message: error.message });
    } finally {
      setButtonLoading(submitButton, false);
    }
  });
}

function renderQuiz() {
  const content = qs("#page-content");
  content.innerHTML = renderQuestionView();
  enhanceRenderedMarkdown(content);
  bindQuizInteractions();
}

async function loadQuiz() {
  const planetId = getRequiredQueryParam("planetId") || getRequiredQueryParam("id");
  if (!planetId) {
    window.location.href = "./galaxies.html";
    return;
  }

  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "galaxies",
    title: "Mission Briefing",
    subtitle: "Preparing the final question field…",
    actions: `<a class="button button-secondary" href="./galaxies.html">${icon("galaxy")}Galaxy map</a>`,
    world: "quiz"
  });

  const content = qs("#page-content");
  content.innerHTML = '<div class="skeleton-block"></div>';

  try {
    const planetPayload = await api.get(`/planets/${planetId}`);
    planet = planetPayload.data;

    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: `${planet.name} briefing`,
      subtitle: "Answer the boss-gate questions, then let the mission report decide what opens next.",
      actions: `<a class="button button-secondary" href="./planet.html?id=${planet.id}">${icon("chevronLeft")}Back to ${escapeHtml(planet.name)}</a>`,
      world: "quiz"
    });

    if (planet.quiz?.status === "LOCKED") {
      content.innerHTML = renderEmptyState({
        iconName: "lock",
        title: "Mission briefing sealed",
        text: "Finish every discovery and mission on this planet before entering the boss gate.",
        actions: `<a class="button button-primary" href="./planet.html?id=${planet.id}">Return to planet</a>`
      });
      return;
    }

    const quizPayload = await api.get(`/quizzes/${planet.id}`);
    questions = quizPayload.data;
    answers = {};
    currentIndex = 0;
    renderQuiz();
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadQuiz);
    showToast({ type: "error", title: "Mission briefing unavailable", message: error.message });
  }
}

loadQuiz();
