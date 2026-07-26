import { api, request } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { enhanceRenderedMarkdown, renderMarkdown } from "../core/markdown.js";
import { renderErrorState, setButtonLoading, showToast, statusClass } from "../core/ui.js";
import { escapeHtml, formatDateTime, getRequiredQueryParam, qs } from "../core/utils.js";

let lessonProgressCleanup = null;

function humanizeStatus(status = "") {
  return String(status || "UNKNOWN").replaceAll("_", " ");
}

function getDiscoveryProgressState(planet, discoveryId) {
  return planet.discoveries.find((item) => item.id === discoveryId) || null;
}

function findNextAction(planet, discoveryId) {
  const discoveries = planet.discoveries;
  const currentIndex = discoveries.findIndex((item) => item.id === discoveryId);
  const nextDiscovery = discoveries.slice(currentIndex + 1).find((item) => item.status !== "LOCKED");
  if (nextDiscovery) return { label: "Open next discovery", href: `./discovery.html?id=${nextDiscovery.id}`, iconName: "discovery" };

  const nextPractice = planet.practice_challenges.find((item) => item.status !== "LOCKED");
  if (nextPractice) return { label: "Launch next mission", href: `./practice.html?id=${nextPractice.id}`, iconName: "mission" };

  if (planet.quiz?.status !== "LOCKED") return { label: "Enter mission briefing", href: `./quiz.html?planetId=${planet.id}`, iconName: "quiz" };
  return { label: "Return to planet", href: `./planet.html?id=${planet.id}`, iconName: "planet" };
}

function lessonStageStrip(state, planet) {
  const isCompleted = state?.status === "COMPLETED";
  const quizUnlocked = planet.quiz?.status !== "LOCKED";
  return `
    <div class="stage-strip">
      <div class="stage-node is-complete"><span>Arrival</span></div>
      <div class="stage-node ${isCompleted ? "is-complete" : "is-active"}"><span>Reading</span></div>
      <div class="stage-node ${isCompleted ? "is-next" : ""}"><span>Mission</span></div>
      <div class="stage-node ${quizUnlocked ? "is-next" : ""}"><span>Briefing</span></div>
      <div class="stage-node ${quizUnlocked ? "is-next" : ""}"><span>Artifact</span></div>
    </div>
  `;
}

function renderDiscoveryPage(discovery, planet, state) {
  const nextAction = findNextAction(planet, discovery.id);
  const isCompleted = state?.status === "COMPLETED";
  const progressPercent = Number(planet.progress?.progress_percent || 0);

  return `
    <section class="discovery-shell">
      <section class="world-hero lesson-command-shell lesson-command-shell--discovery">
        <div class="world-hero-copy">
          <p class="eyebrow">Discovery ${escapeHtml(discovery.order_number)} · ${escapeHtml(planet.name)}</p>
          <h2 class="landing-system-title">${escapeHtml(discovery.title)}</h2>
          <p class="world-hero-subtitle">${escapeHtml(discovery.description || discovery.learning_objective || "Read carefully, absorb the route, then record completion to move deeper into the planet.")}</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("discovery")} ${escapeHtml(humanizeStatus(state?.status || discovery.status))}</span>
            <span class="badge badge-muted">${icon("clock")} ${escapeHtml(discovery.read_time_minutes || 0)} min read</span>
            <span class="badge badge-primary">${icon("spark")} ${escapeHtml(discovery.xp_reward)} XP</span>
          </div>
          ${lessonStageStrip(state, planet)}
          <div class="inline">
            <a class="button button-secondary" href="./planet.html?id=${planet.id}">${icon("chevronLeft")}Back to planet</a>
            <a class="button button-primary" href="${nextAction.href}">${icon(nextAction.iconName)}${escapeHtml(nextAction.label)}</a>
          </div>
        </div>

        <div class="world-hero-visual lesson-orbitarium">
          <div class="lesson-orbit-core"></div>
          <div class="lesson-orbit-ring lesson-orbit-ring--a"></div>
          <div class="lesson-orbit-ring lesson-orbit-ring--b"></div>
          <div class="lesson-orbit-node lesson-orbit-node--read"><strong>${escapeHtml(discovery.read_time_minutes || 0)}</strong><span>Minutes</span></div>
          <div class="lesson-orbit-node lesson-orbit-node--xp"><strong>${escapeHtml(discovery.xp_reward)}</strong><span>XP</span></div>
          <div class="lesson-orbit-node lesson-orbit-node--planet"><strong>${Math.round(progressPercent)}</strong><span>Planet %</span></div>
        </div>
      </section>

      <section class="detail-grid discovery-reading-grid">
        <article class="card stack lesson-reading-panel">
          <div class="section-header">
            <div>
              <p class="eyebrow">Observation deck</p>
              <h2 class="section-title">Read the signal</h2>
              <p class="section-description">The lesson below is the living text of this route and remains the primary way through the discovery.</p>
            </div>
          </div>
          <div class="progress-grid-inline">
            <div class="reading-progress-shell">
              <div class="reading-progress-label"><span>Planet completion</span><strong>${progressPercent.toFixed(0)}%</strong></div>
              <div class="progress-bar"><span style="width:${progressPercent}%"></span></div>
            </div>
            <div class="reading-progress-shell">
              <div class="reading-progress-label"><span>Reading progress</span><strong id="reading-progress-value">0%</strong></div>
              <div class="progress-bar" id="reading-progress-bar"><span style="width:0%"></span></div>
            </div>
          </div>
          <div class="lesson-reading markdown" id="discovery-article">
            ${renderMarkdown(discovery.content_md || "")}
          </div>
        </article>

        <aside class="lesson-sidebar desktop-sticky">
          <section class="card stack lesson-support-panel">
            <div class="section-header">
              <div>
                <p class="eyebrow">Route map</p>
                <h2 class="section-title">Lesson outline</h2>
                <p class="section-description">Jump across headings without losing your reading trail.</p>
              </div>
            </div>
            <nav id="lesson-outline" class="lesson-outline" aria-label="Lesson outline"></nav>
          </section>

          <section class="card stack lesson-complete-dock">
            <div class="section-header">
              <div>
                <p class="eyebrow">Completion dock</p>
                <h2 class="section-title">Record this discovery</h2>
                <p class="section-description">When the lesson is truly understood, archive it and claim the XP tied to this route.</p>
              </div>
            </div>
            <div class="inline">
              <span class="badge badge-primary">${icon("spark")} ${escapeHtml(discovery.xp_reward)} XP</span>
              <span class="${statusClass(state?.status || discovery.status)}">${escapeHtml(humanizeStatus(state?.status || discovery.status))}</span>
            </div>
            <div class="callout info">${escapeHtml(discovery.learning_objective || "This discovery is one step in a larger planetary sequence.")}</div>
            ${discovery.prerequisites?.length ? `<div class="callout warning">Prerequisites: ${escapeHtml(discovery.prerequisites.join(", "))}</div>` : ""}
            <div class="inline">
              <button class="button ${isCompleted ? "button-secondary" : "button-primary"}" id="complete-discovery-button" ${isCompleted ? "disabled" : ""}>${isCompleted ? `${icon("check")}Archived` : `${icon("check")}Mark discovery complete`}</button>
            </div>
          </section>

          <section class="card stack lesson-support-panel">
            <div class="section-header">
              <div>
                <p class="eyebrow">Next jump</p>
                <h2 class="section-title">Continue the route</h2>
                <p class="section-description">AlgoLingo keeps you moving through the intended route without losing your place.</p>
              </div>
            </div>
            <a class="button button-primary" href="${nextAction.href}">${icon(nextAction.iconName)}${escapeHtml(nextAction.label)}</a>
            ${planet.progress?.last_activity_at ? `<div class="callout">Last planet activity ${escapeHtml(formatDateTime(planet.progress.last_activity_at))}</div>` : ""}
          </section>
        </aside>
      </section>
    </section>
  `;
}

function classifyCalloutHeading(text) {
  const normalized = text.trim().toLowerCase();
  if (normalized.includes("tip")) return "tip";
  if (normalized.includes("common mistake")) return "mistakes";
  if (normalized.includes("mini summary") || normalized.includes("summary")) return "summary";
  if (normalized.includes("did you know")) return "fact";
  return "";
}

function enhanceLessonArticle() {
  const article = qs("#discovery-article");
  if (!article) return;

  const headings = Array.from(article.querySelectorAll("h1, h2, h3"));
  headings.forEach((heading, index) => {
    const anchorId = `lesson-section-${index + 1}`;
    heading.id = anchorId;
    heading.classList.add("lesson-anchor");

    const type = classifyCalloutHeading(heading.textContent || "");
    if (!type || heading.parentElement.classList.contains("lesson-callout")) return;

    const wrapper = document.createElement("section");
    wrapper.className = `lesson-callout lesson-callout--${type}`;
    heading.parentNode.insertBefore(wrapper, heading);
    wrapper.appendChild(heading);

    let sibling = wrapper.nextSibling;
    while (sibling) {
      const next = sibling.nextSibling;
      if (sibling.nodeType === 1 && /H1|H2|H3/.test(sibling.tagName)) break;
      wrapper.appendChild(sibling);
      sibling = next;
    }
  });

  const outlineRoot = qs("#lesson-outline");
  if (outlineRoot) {
    const relevantHeadings = Array.from(article.querySelectorAll("h2, h3"));
    outlineRoot.innerHTML = relevantHeadings
      .map((heading) => `<a href="#${heading.id}">${icon("chevronRight")}<span>${escapeHtml(heading.textContent || "Section")}</span></a>`)
      .join("");
  }
}

function bindLessonProgress() {
  if (lessonProgressCleanup) lessonProgressCleanup();

  const article = qs("#discovery-article");
  const value = qs("#reading-progress-value");
  const fill = qs("#reading-progress-bar span");
  const outlineLinks = Array.from(document.querySelectorAll("#lesson-outline a"));
  if (!article || !value || !fill) return;

  const sync = () => {
    const rect = article.getBoundingClientRect();
    const viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    const totalScrollable = Math.max(article.offsetHeight - viewportHeight * 0.55, 1);
    const progressed = Math.min(Math.max((viewportHeight * 0.25 - rect.top) / totalScrollable, 0), 1);
    const percent = Math.round(progressed * 100);
    value.textContent = `${percent}%`;
    fill.style.width = `${percent}%`;

    let activeId = "";
    const lessonHeadings = Array.from(article.querySelectorAll("h2, h3"));
    lessonHeadings.forEach((heading) => {
      const headingTop = heading.getBoundingClientRect().top;
      if (headingTop <= 160) activeId = heading.id;
    });
    outlineLinks.forEach((link) => {
      link.classList.toggle("is-active", link.getAttribute("href") === `#${activeId}`);
    });
  };

  window.addEventListener("scroll", sync, { passive: true });
  window.addEventListener("resize", sync);
  lessonProgressCleanup = () => {
    window.removeEventListener("scroll", sync);
    window.removeEventListener("resize", sync);
  };
  sync();
}

async function loadDiscovery() {
  const discoveryId = getRequiredQueryParam("id");
  if (!discoveryId) {
    window.location.href = "./galaxies.html";
    return;
  }

  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "galaxies",
    title: "Discovery",
    subtitle: "Preparing the reading route…",
    actions: `<a class="button button-secondary" href="./galaxies.html">${icon("galaxy")}Galaxy map</a>`,
    world: "discovery"
  });

  const content = qs("#page-content");
  content.innerHTML = '<div class="skeleton-block"></div>';

  try {
    const discoveryPayload = await api.get(`/discoveries/${discoveryId}`);
    const discovery = discoveryPayload.data;
    const planetPayload = await api.get(`/planets/${discovery.planet_id}`);
    const planet = planetPayload.data;
    const discoveryState = getDiscoveryProgressState(planet, discovery.id);

    initializePrivateLayout({
      user,
      activeNav: "galaxies",
      title: discovery.title,
      subtitle: discovery.description || "Read the lesson, understand the objective, and archive the discovery when ready.",
      actions: `<a class="button button-secondary" href="./planet.html?id=${planet.id}">${icon("chevronLeft")}Back to ${escapeHtml(planet.name)}</a>`,
      world: "discovery"
    });

    content.innerHTML = renderDiscoveryPage(discovery, planet, discoveryState);
    enhanceLessonArticle();
    enhanceRenderedMarkdown(content);
    bindLessonProgress();

    const completeButton = qs("#complete-discovery-button");
    completeButton?.addEventListener("click", async () => {
      setButtonLoading(completeButton, true, "Archiving…");
      try {
        const result = await request(`/discoveries/${discovery.id}/complete`, { method: "POST" });
        showToast({ type: "success", title: "Discovery archived", message: `You earned ${result.data.xp_awarded} XP.` });
        await loadDiscovery();
      } catch (error) {
        showToast({ type: "error", title: "Could not archive discovery", message: error.message });
      } finally {
        setButtonLoading(completeButton, false);
      }
    });
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadDiscovery);
  }
}

loadDiscovery();
