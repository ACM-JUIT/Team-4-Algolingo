import { api, request } from "./api.js";
import { ensureAuthenticated } from "./auth.js";
import { initializePrivateLayout } from "./layout.js";
import { renderMarkdown } from "./markdown.js";
import { setButtonLoading, renderErrorState, showToast, statusClass } from "./ui.js";
import { escapeHtml, formatDateTime, getRequiredQueryParam, qs } from "./utils.js";

function getDiscoveryProgressState(planet, discoveryId) {
  return planet.discoveries.find((item) => item.id === discoveryId) || null;
}

function findNextAction(planet, discoveryId) {
  const discoveries = planet.discoveries;
  const currentIndex = discoveries.findIndex((item) => item.id === discoveryId);
  const nextDiscovery = discoveries.slice(currentIndex + 1).find((item) => item.status !== "LOCKED");
  if (nextDiscovery) {
    return { label: "Open next discovery", href: `./discovery.html?id=${nextDiscovery.id}` };
  }
  const nextPractice = planet.practice_challenges.find((item) => item.status !== "LOCKED");
  if (nextPractice) {
    return { label: "Go to practice", href: `./practice.html?id=${nextPractice.id}` };
  }
  if (planet.quiz?.status !== "LOCKED") {
    return { label: "Open quiz", href: `./quiz.html?planetId=${planet.id}` };
  }
  return { label: "Back to planet", href: `./planet.html?id=${planet.id}` };
}

function renderDiscoveryPage(discovery, planet, state) {
  const nextAction = findNextAction(planet, discovery.id);
  const isCompleted = state?.status === "COMPLETED";
  return `
    <section class="detail-grid">
      <article class="card markdown" id="discovery-article">
        ${renderMarkdown(discovery.content_md || "")}
      </article>
      <aside class="stack">
        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Lesson details</h2>
              <p class="section-description">Backend content and completion data for this discovery.</p>
            </div>
          </div>
          <div class="inline">
            <span class="${statusClass(state?.status || discovery.status)}">${escapeHtml((state?.status || discovery.status).replaceAll("_", " "))}</span>
            <span class="badge badge-primary">${escapeHtml(discovery.xp_reward)} XP</span>
          </div>
          <div class="callout">Read time: ${escapeHtml(discovery.read_time_minutes || 0)} minutes</div>
          <div class="callout">Objective: ${escapeHtml(discovery.learning_objective || "No learning objective provided.")}</div>
          ${discovery.prerequisites?.length ? `<div class="callout">Prerequisites: ${escapeHtml(discovery.prerequisites.join(", "))}</div>` : ""}
          <div class="inline">
            <button class="button ${isCompleted ? "button-success" : "button-primary"}" id="complete-discovery-button" ${isCompleted ? "disabled" : ""}>${isCompleted ? "Completed" : "Mark as complete"}</button>
            <a class="button button-secondary" href="./planet.html?id=${planet.id}">Back to planet</a>
          </div>
        </section>

        <section class="card stack">
          <div class="section-header">
            <div>
              <h2 class="section-title">Next step</h2>
              <p class="section-description">Continue the learning flow without breaking backend rules.</p>
            </div>
          </div>
          <a class="button button-primary" href="${nextAction.href}">${escapeHtml(nextAction.label)}</a>
          ${planet.progress ? `<div class="callout">Planet progress: ${escapeHtml(planet.progress.progress_percent)}%</div>` : ""}
        </section>
      </aside>
    </section>
  `;
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
    subtitle: "Loading discovery content…",
    actions: '<a class="button button-secondary" href="./galaxies.html">All galaxies</a>'
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
      subtitle: discovery.description || "Read the lesson carefully, then mark it complete to move forward.",
      actions: `<a class="button button-secondary" href="./planet.html?id=${planet.id}">Back to ${escapeHtml(planet.name)}</a>`
    });

    content.innerHTML = renderDiscoveryPage(discovery, planet, discoveryState);

    const completeButton = qs("#complete-discovery-button");
    completeButton?.addEventListener("click", async () => {
      setButtonLoading(completeButton, true, "Completing…");
      try {
        const result = await request(`/discoveries/${discovery.id}/complete`, { method: "POST" });
        showToast({
          type: "success",
          title: "Discovery completed",
          message: `You earned ${result.data.xp_awarded} XP.`
        });
        await loadDiscovery();
      } catch (error) {
        showToast({ type: "error", title: "Could not complete discovery", message: error.message });
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
