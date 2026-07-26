import { api } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { renderMarkdown } from "./markdown.js";
import { renderEmptyState, renderErrorState, setButtonLoading, showToast, statusClass } from "./ui.js";
import { escapeHtml, formatPercentage, getRequiredQueryParam, qs } from "./utils.js";

let questions = [];
let answers = {};
let currentIndex = 0;
let planet = null;

function currentQuestion() {
  return questions[currentIndex];
}

function answeredCount() {
  return Object.values(answers).filter(Boolean).length;
}

function renderOption(option, selected) {
  return `
    <label class="answer-option ${selected ? "is-selected" : ""}">
      <input type="radio" name="quiz-answer" value="${escapeHtml(option.id)}" ${selected ? "checked" : ""}>
      <div>
        <strong>${escapeHtml(option.id)}</strong>
        <div class="activity-note">${escapeHtml(option.text)}</div>
      </div>
    </label>
  `;
}

function renderQuestionView() {
  const question = currentQuestion();
  if (!question) {
    return renderEmptyState({ icon: "🧠", title: "No quiz questions found", text: "This planet has no quiz questions configured in the backend." });
  }

  const selectedAnswer = answers[question.id] || "";
  return `
    <div class="quiz-layout">
      <section class="card quiz-question">
        <div class="quiz-question-head">
          <div>
            <p class="eyebrow">Question ${currentIndex + 1} of ${questions.length}</p>
            <h2 class="section-title">${escapeHtml(question.question_type.replaceAll("_", " "))}</h2>
          </div>
          <span class="badge badge-primary">${escapeHtml(question.xp_reward)} XP</span>
        </div>
        <article class="markdown">${renderMarkdown(question.question_text)}</article>
        <div class="answer-options">${question.options.map((option) => renderOption(option, selectedAnswer === option.id)).join("")}</div>
        <div class="inline" style="justify-content: space-between;">
          <button class="button button-secondary" id="prev-question-button" ${currentIndex === 0 ? "disabled" : ""}>Previous</button>
          <div class="inline">
            <button class="button button-secondary" id="next-question-button">${currentIndex === questions.length - 1 ? "Review answers" : "Next"}</button>
            <button class="button button-primary" id="submit-quiz-button">Submit quiz</button>
          </div>
        </div>
      </section>
      <aside class="question-nav">
        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Quiz progress</h2>
              <p class="section-description">Use question navigation or submit when you are ready.</p>
            </div>
          </div>
          <div class="progress-stack">
            <div class="progress-labels"><span>Answered</span><span>${answeredCount()}/${questions.length}</span></div>
            <div class="progress-bar"><span style="width:${(answeredCount() / Math.max(questions.length, 1)) * 100}%"></span></div>
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
          <div class="callout ${planet.quiz?.status === "PASSED" ? "warning" : ""}">
            Status: ${escapeHtml((planet.quiz?.status || "LOCKED").replaceAll("_", " "))}
            ${planet.quiz?.passed ? " · This quiz has already been passed once." : ""}
          </div>
        </section>
      </aside>
    </div>
  `;
}

function renderResults(result) {
  return `
    <section class="stack">
      <section class="hero-surface stack">
        <div class="hero-grid">
          <div>
            <p class="eyebrow">Quiz results</p>
            <h2 class="page-title" style="font-size: 2rem;">${result.passed ? "Quiz passed" : "Quiz complete"}</h2>
            <p class="page-subtitle">You scored ${result.score} out of ${result.total_questions} (${formatPercentage(result.percentage)}). Backend status: ${result.quiz_status}.</p>
            <div class="inline" style="margin-top: 1rem;">
              <span class="${statusClass(result.quiz_status)}">${escapeHtml(result.quiz_status.replaceAll("_", " "))}</span>
              <span class="badge badge-primary">${escapeHtml(result.xp_awarded)} XP awarded</span>
            </div>
          </div>
          <div class="card stack">
            ${result.artifact_unlocked ? `
              <div class="callout success">Artifact unlocked: ${escapeHtml(result.artifact_unlocked.name)} (+${escapeHtml(result.artifact_unlocked.xp_bonus_percent)}% XP bonus)</div>
            ` : '<div class="callout">No new artifact was unlocked by this submission.</div>'}
            <div class="inline">
              <a class="button button-secondary" href="./planet.html?id=${planet.id}">Back to planet</a>
              <a class="button button-primary" href="./artifacts.html">View artifacts</a>
            </div>
          </div>
        </div>
      </section>

      <section class="stack">
        ${result.results
          .map(
            (item, index) => `
              <article class="card stack ${item.is_correct ? "result-pass" : "result-fail"}">
                <div class="result-row">
                  <div>
                    <p class="eyebrow">Question ${index + 1}</p>
                    <h3 class="card-title">${item.is_correct ? "Correct" : "Incorrect"}</h3>
                  </div>
                  <span class="${statusClass(item.is_correct ? "PASSED" : "FAILED")}">${item.is_correct ? "Correct" : "Incorrect"}</span>
                </div>
                <div class="callout">Submitted answer: ${escapeHtml(item.submitted_answer || "No answer")}</div>
                <div class="callout">Correct answer: ${escapeHtml(item.correct_answer)}</div>
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
      .filter((item) => item.answer);

    if (!submittedAnswers.length) {
      showToast({ type: "warning", title: "Answer at least one question", message: "The backend requires at least one submitted answer." });
      return;
    }

    setButtonLoading(submitButton, true, "Submitting…");
    try {
      const payload = await api.post(`/quizzes/${planet.id}/submit`, {
        answers: submittedAnswers
      });
      qs("#page-content").innerHTML = renderResults(payload.data);
      showToast({
        type: payload.data.passed ? "success" : "warning",
        title: payload.data.passed ? "Quiz passed" : "Quiz submitted",
        message: payload.data.passed ? `You earned ${payload.data.xp_awarded} XP.` : "Review the explanations and try again later."
      });
    } catch (error) {
      showToast({ type: "error", title: "Quiz submission failed", message: error.message });
    } finally {
      setButtonLoading(submitButton, false);
    }
  });
}

function renderQuiz() {
  const content = qs("#page-content");
  content.innerHTML = renderQuestionView();
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
    title: "Quiz",
    subtitle: "Loading quiz questions…",
    actions: '<a class="button button-secondary" href="./galaxies.html">All galaxies</a>'
  });

  const content = qs("#page-content");
  content.innerHTML = '<div class="skeleton-block"></div>';

  try {
    const planetPayload = await api.get(`/planets/${planetId}`);
    planet = planetPayload.data;

    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: `${planet.name} quiz`,
      subtitle: "Answer each question using the backend-provided options. Correct answers are never exposed until submission.",
      actions: `<a class="button button-secondary" href="./planet.html?id=${planet.id}">Back to ${escapeHtml(planet.name)}</a>`
    });

    if (planet.quiz?.status === "LOCKED") {
      content.innerHTML = renderEmptyState({
        icon: "🔒",
        title: "Quiz locked",
        text: "Finish every discovery and practice challenge on this planet before attempting the quiz.",
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
    showToast({ type: "error", title: "Quiz unavailable", message: error.message });
  }
}

loadQuiz();
