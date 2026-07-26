import { api } from "../core/api.js";
import { ensureAuthenticated } from "../core/auth.js";
import { icon } from "../core/icons.js";
import { initializePrivateLayout } from "../core/layout.js";
import { renderEmptyState, renderErrorState, renderLoadingGrid, showToast, statusClass } from "../core/ui.js";
import { debounce, escapeHtml, getQueryParam, qs, updateQueryParams } from "../core/utils.js";

const state = {
  query: getQueryParam("q", "") || "",
  type: getQueryParam("type", "all") || "all",
  items: []
};

const TYPE_META = {
  galaxy: { label: "Galaxy", iconName: "galaxy" },
  planet: { label: "Planet", iconName: "planet" },
  discovery: { label: "Discovery", iconName: "discovery" },
  mission: { label: "Mission", iconName: "mission" },
  artifact: { label: "Relic", iconName: "artifact" }
};

function normalize(value) {
  return String(value || "").trim().toLowerCase();
}

function buildSearchText(...parts) {
  return normalize(parts.filter(Boolean).join(" "));
}

function itemIsUnlocked(item) {
  return item.status !== "LOCKED";
}

function filteredItems() {
  let items = state.items;
  if (state.type !== "all") items = items.filter((item) => item.type === state.type);
  const query = normalize(state.query);
  if (query) items = items.filter((item) => item.searchText.includes(query));
  return items.sort((a, b) => {
    if (itemIsUnlocked(a) !== itemIsUnlocked(b)) return itemIsUnlocked(a) ? -1 : 1;
    return a.title.localeCompare(b.title);
  });
}

function renderResultCard(item) {
  const meta = TYPE_META[item.type];
  const actionLabel = item.status === "LOCKED" ? "View route" : item.type === "artifact" ? "Inspect relic" : `Open ${meta.label.toLowerCase()}`;
  return `
    <article class="search-result-card ${item.status === "LOCKED" ? "is-locked" : ""}">
      <div class="search-result-head">
        <div class="user-stack">
          <span class="icon-spot">${icon(meta.iconName)}</span>
          <div>
            <p class="eyebrow">${escapeHtml(meta.label)}</p>
            <h3 class="section-title">${escapeHtml(item.title)}</h3>
          </div>
        </div>
        <span class="${statusClass(item.status)}">${escapeHtml(String(item.status).replaceAll("_", " "))}</span>
      </div>
      <p class="section-description">${escapeHtml(item.description || "No description available.")}</p>
      <div class="artifact-card-badges">
        ${item.context ? `<span class="badge badge-muted">${escapeHtml(item.context)}</span>` : ""}
        ${item.meta ? `<span class="badge badge-muted">${escapeHtml(item.meta)}</span>` : ""}
      </div>
      <div class="artifact-pedestal-footer">
        <p class="route-manifest-note">${escapeHtml(item.note || "Navigate directly to continue exploring.")}</p>
        <a class="button ${item.status === "LOCKED" ? "button-secondary" : "button-primary"}" href="${item.href}">${icon(meta.iconName)}${escapeHtml(actionLabel)}</a>
      </div>
    </article>
  `;
}

function renderSearchPage() {
  const results = filteredItems();
  const counts = {
    all: state.items.length,
    galaxy: state.items.filter((item) => item.type === "galaxy").length,
    planet: state.items.filter((item) => item.type === "planet").length,
    discovery: state.items.filter((item) => item.type === "discovery").length,
    mission: state.items.filter((item) => item.type === "mission").length,
    artifact: state.items.filter((item) => item.type === "artifact").length
  };

  return `
    <section class="search-shell">
      <section class="world-hero search-hero">
        <div class="world-hero-copy">
          <p class="eyebrow">Star Search</p>
          <h2 class="landing-system-title">Search the universe by galaxy, planet, discovery, mission, or relic.</h2>
          <p class="world-hero-subtitle">This index is assembled from live universe data so you can move across the map without guessing where anything lives.</p>
          <div class="world-hero-badges">
            <span class="badge badge-primary">${icon("search")} ${state.items.length} indexed destinations</span>
            <span class="badge badge-muted">${results.length} matching the current signal</span>
          </div>
        </div>
        <div class="world-hero-visual report-score-visual">
          <div class="report-score-facts">
            <div class="planet-briefing-fact"><span class="metric-label">Indexed</span><strong class="metric-value">${state.items.length}</strong></div>
            <div class="planet-briefing-fact"><span class="metric-label">Visible</span><strong class="metric-value">${results.length}</strong></div>
          </div>
        </div>
      </section>

      <section class="card expedition-card stack search-bar-card">
        <div class="form-row">
          <label class="form-label" for="search-query">Search the universe</label>
          <input class="input" id="search-query" value="${escapeHtml(state.query)}" placeholder="Try: python, loops, function, artifact, quiz...">
        </div>
        <div class="filter-bar">
          <button class="tab-button ${state.type === "all" ? "is-active" : ""}" data-type="all">All (${counts.all})</button>
          <button class="tab-button ${state.type === "galaxy" ? "is-active" : ""}" data-type="galaxy">Galaxies (${counts.galaxy})</button>
          <button class="tab-button ${state.type === "planet" ? "is-active" : ""}" data-type="planet">Planets (${counts.planet})</button>
          <button class="tab-button ${state.type === "discovery" ? "is-active" : ""}" data-type="discovery">Discoveries (${counts.discovery})</button>
          <button class="tab-button ${state.type === "mission" ? "is-active" : ""}" data-type="mission">Missions (${counts.mission})</button>
          <button class="tab-button ${state.type === "artifact" ? "is-active" : ""}" data-type="artifact">Relics (${counts.artifact})</button>
        </div>
      </section>

      ${results.length
        ? `<section class="search-results-grid">${results.map(renderResultCard).join("")}</section>`
        : renderEmptyState({ iconName: "search", title: "No matching destination", text: state.query ? "Try a broader term or switch the filter to all destinations." : "Start typing to search across the indexed universe." })}
    </section>
  `;
}

function bindSearchInteractions() {
  const input = qs("#search-query");
  input?.addEventListener("input", debounce((event) => {
    state.query = event.target.value;
    updateQueryParams({ q: state.query, type: state.type === "all" ? "" : state.type });
    renderAndBind();
  }, 120));

  document.querySelectorAll("[data-type]").forEach((button) => {
    button.addEventListener("click", () => {
      state.type = button.dataset.type;
      updateQueryParams({ q: state.query, type: state.type === "all" ? "" : state.type });
      renderAndBind();
    });
  });
}

function renderAndBind() {
  qs("#page-content").innerHTML = renderSearchPage();
  bindSearchInteractions();
}

async function buildSearchIndex() {
  const [galaxiesPayload, artifactsPayload] = await Promise.all([
    api.get("/galaxies"),
    api.get("/artifacts")
  ]);

  const galaxies = galaxiesPayload.data;
  const galaxyDetails = await Promise.all(
    galaxies.map(async (galaxy) => {
      try {
        const payload = await api.get(`/galaxies/${galaxy.id}`);
        return payload.data;
      } catch {
        return null;
      }
    })
  );

  const planets = galaxyDetails.flatMap((item) => item?.planets || []);
  const planetDetails = await Promise.all(
    planets.map(async (planet) => {
      try {
        const payload = await api.get(`/planets/${planet.id}`);
        return payload.data;
      } catch {
        return null;
      }
    })
  );

  const items = [];

  galaxies.forEach((galaxy) => {
    items.push({
      type: "galaxy",
      id: galaxy.id,
      title: galaxy.name,
      description: galaxy.description,
      context: galaxy.programming_language || "Galaxy route",
      meta: `${galaxy.completed_planets}/${galaxy.total_planets} planets complete`,
      note: galaxy.is_locked ? "This galaxy is visible but currently sealed." : "Enter this galaxy to inspect its planets.",
      status: galaxy.is_locked ? "LOCKED" : galaxy.progress_percent > 0 ? "IN_PROGRESS" : "UNLOCKED",
      href: `./galaxy.html?id=${galaxy.id}`,
      searchText: buildSearchText(galaxy.name, galaxy.description, galaxy.programming_language)
    });
  });

  planetDetails.filter(Boolean).forEach((planet) => {
    const galaxy = galaxies.find((item) => item.id === planet.galaxy_id);
    items.push({
      type: "planet",
      id: planet.id,
      title: planet.name,
      description: planet.tagline || planet.description,
      context: galaxy?.name || "Planet route",
      meta: `Difficulty ${planet.difficulty} · ${planet.xp_total} XP`,
      note: planet.unlock_condition || "Open this planet to continue the route.",
      status: planet.status || "AVAILABLE",
      href: `./planet.html?id=${planet.id}`,
      searchText: buildSearchText(planet.name, planet.tagline, planet.description, galaxy?.name)
    });

    (planet.discoveries || []).forEach((discovery) => {
      items.push({
        type: "discovery",
        id: discovery.id,
        title: discovery.title,
        description: discovery.description || discovery.learning_objective,
        context: `${galaxy?.name || "Galaxy"} · ${planet.name}`,
        meta: `${discovery.read_time_minutes || 0} min · ${discovery.xp_reward} XP`,
        note: discovery.learning_objective || "Open this discovery to continue reading.",
        status: discovery.status || "AVAILABLE",
        href: `./discovery.html?id=${discovery.id}`,
        searchText: buildSearchText(discovery.title, discovery.description, discovery.learning_objective, planet.name, galaxy?.name)
      });
    });

    (planet.practice_challenges || []).forEach((mission) => {
      items.push({
        type: "mission",
        id: mission.id,
        title: mission.title,
        description: mission.description || mission.learning_outcome,
        context: `${galaxy?.name || "Galaxy"} · ${planet.name}`,
        meta: `${mission.challenge_type} · ${mission.xp_reward} XP`,
        note: mission.learning_outcome || "Open this mission to start coding.",
        status: mission.status || "AVAILABLE",
        href: `./practice.html?id=${mission.id}`,
        searchText: buildSearchText(mission.title, mission.description, mission.learning_outcome, mission.challenge_type, planet.name, galaxy?.name)
      });
    });
  });

  artifactsPayload.data.forEach((entry) => {
    const artifact = entry.artifact;
    items.push({
      type: "artifact",
      id: artifact.id,
      title: artifact.name,
      description: artifact.description,
      context: artifact.category,
      meta: `${artifact.rarity} · +${artifact.xp_bonus_percent}% XP`,
      note: entry.collected ? "Recovered and preserved in your museum." : artifact.unlock_condition || "Recover this relic by completing its route.",
      status: entry.collected ? "COMPLETED" : "LOCKED",
      href: `./artifact.html?id=${artifact.id}`,
      searchText: buildSearchText(artifact.name, artifact.description, artifact.category, artifact.rarity, artifact.unlock_condition)
    });
  });

  return items;
}

async function loadSearch() {
  const user = await ensureAuthenticated();
  if (!user) return;

  initializePrivateLayout({
    user,
    activeNav: "search",
    title: "Star Search",
    subtitle: "Search across live galaxies, planets, discoveries, missions, and relics indexed from your current universe.",
    actions: `<a class="button button-secondary" href="./galaxies.html">${icon("galaxy")}Galaxy Map</a>`,
    world: "search"
  });

  const content = qs("#page-content");
  content.innerHTML = renderLoadingGrid(4);

  try {
    state.items = await buildSearchIndex();
    renderAndBind();
  } catch (error) {
    content.innerHTML = renderErrorState({ text: error.message });
    qs("#retry-action")?.addEventListener("click", loadSearch);
    showToast({ type: "error", title: "Search index unavailable", message: error.message });
  }
}

loadSearch();
