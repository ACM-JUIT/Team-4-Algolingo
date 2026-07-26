# AlgoLingo Frontend

A handcrafted frontend for the existing AlgoLingo FastAPI backend.

## Stack

- HTML5
- CSS3
- Vanilla JavaScript (ES modules)

No React, Vue, Angular, Tailwind, Bootstrap, jQuery, or other UI frameworks are used.

---

## Folder structure

```text
frontend/
  index.html
  README.md
  assets/
    css/
      variables.css
      themes.css
      base.css
      layout.css
      components.css
      pages.css
    img/
      favicon.svg
      logo.svg
    js/
      api.js
      auth.js
      config.js
      dashboard.js
      discovery.js
      editor.js
      galaxies.js
      galaxy.js
      index.js
      layout.js
      leaderboard.js
      login.js
      markdown.js
      nova.js
      planet.js
      practice.js
      profile.js
      quiz.js
      register.js
      settings.js
      storage.js
      theme.js
      ui.js
      utils.js
  pages/
    login.html
    register.html
    dashboard.html
    galaxies.html
    galaxy.html
    planet.html
    discovery.html
    practice.html
    quiz.html
    artifacts.html
    leaderboard.html
    profile.html
    settings.html
    nova.html
```

---

## Page map

### Public pages

- `index.html`
  - redirects to dashboard when a session exists
  - redirects to login otherwise
- `pages/login.html`
- `pages/register.html`

### Protected pages

- `pages/dashboard.html`
- `pages/galaxies.html`
- `pages/galaxy.html?id=<galaxy_id>`
- `pages/planet.html?id=<planet_id>`
- `pages/discovery.html?id=<discovery_id>`
- `pages/practice.html?id=<practice_id>`
- `pages/quiz.html?planetId=<planet_id>`
- `pages/artifacts.html`
- `pages/leaderboard.html`
- `pages/profile.html`
- `pages/settings.html`
- `pages/nova.html`

---

## Component map

### Layout

- Responsive sidebar navigation
- Sticky topbar
- Mobile drawer navigation
- Theme toggle
- Toast notification system
- Modal system

### Core UI

- Metric cards
- Status chips / badges
- Empty states
- Error states with retry actions
- Skeleton loading blocks
- Progress bars
- Tables
- Tabs
- Timeline items

### Learning UI

- Markdown lesson renderer for discoveries
- Practice editor with line gutter and local draft persistence
- Quiz question navigator and result summary
- Artifact collection cards and detail modal
- Leaderboard table with current-user highlighting
- NOVA response workspace with per-endpoint forms

---

## API integration summary

The frontend was built against the current backend contracts and does not create or assume any extra routes.

### Root auth flow

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`

### Main product pages

- `GET /api/v1/dashboard`
- `GET /api/v1/galaxies`
- `GET /api/v1/galaxies/{galaxy_id}`
- `GET /api/v1/planets/{planet_id}`
- `GET /api/v1/discoveries/{discovery_id}`
- `POST /api/v1/discoveries/{discovery_id}/complete`
- `GET /api/v1/practices/{practice_id}`
- `GET /api/v1/practices/{practice_id}/solution`
- `POST /api/v1/practices/{practice_id}/submit`
- `GET /api/v1/quizzes/{planet_id}`
- `POST /api/v1/quizzes/{planet_id}/submit`
- `GET /api/v1/artifacts`
- `GET /api/v1/users/{user_id}/artifacts`
- `GET /api/v1/leaderboard`
- `GET /api/v1/profile/{username}`
- `PATCH /api/v1/profile/me`

### NOVA

- `POST /api/v1/nova/ask`
- `POST /api/v1/nova/hint/{practice_id}`
- `POST /api/v1/nova/debug`
- `POST /api/v1/nova/recommend`

### Health / connectivity

- `GET /api/v1/health`

---

## Important backend-aligned behaviors

The frontend intentionally follows the backend's current behavior:

- login/register use bearer-token auth from JSON responses
- refresh-token rotation is used automatically after `401` responses
- logout sends the current refresh token in the request body
- quiz access is planet-based
- quiz alias routes use `planet_id`, not a separate quiz id
- practice submissions are the only backend-supported code evaluation path
- a separate "run code" endpoint is **not** implemented by the backend, so the UI does not fake one
- forgot password UI is omitted because the backend does not expose that route
- solution viewing uses the dedicated backend endpoint so the backend can record the event and adjust XP rules

---

## Theme support

- one-click light/dark mode toggle
- persisted in `localStorage`
- applied before render to reduce theme flash
- all core components support both themes

---

## Session handling

- access and refresh tokens are stored in `localStorage`
- protected pages verify the current session through `/auth/me`
- expired access tokens trigger automatic refresh via `/auth/refresh`
- refresh failure clears local session data and redirects to login

---

## Local setup

### 1. Start the backend

From the backend directory:

```bash
cd backend
uvicorn app.main:app --reload
```

### 2. Serve the frontend from an allowed CORS origin

The backend currently allows `localhost:3000`, `127.0.0.1:3000`, `localhost:5173`, and `127.0.0.1:5173` by default.

Recommended:

```bash
cd frontend
python -m http.server 3000
```

Then open:

```text
http://localhost:3000
```

### 3. If your backend is not on the default URL

The frontend assumes:

```text
http://localhost:8000/api/v1
```

If your API lives somewhere else, open the **Settings** page after login and update the API base URL.

---

## Notes

- Discovery content is rendered from backend markdown-like lesson text.
- Practice drafts are stored locally per practice id.
- Weekly and monthly leaderboard pages are supported, but if the backend has no snapshot rows yet the frontend shows a clean empty state.
- Artifact icons fall back to generated avatar-style monograms when `icon_url` is missing in backend data.
