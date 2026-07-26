# AlgoLingo Frontend

A production-ready **vanilla HTML/CSS/JavaScript frontend** for **AlgoLingo**, designed as a **living exploration universe** where programming is learned through galaxies, planets, discoveries, missions, briefings, and artifacts.

> This is not a dashboard, SaaS template, or admin panel.
> It is a world-first learning experience built on top of an existing FastAPI backend.

---

## Overview

AlgoLingo turns programming education into a journey:

- **Galaxies** represent programming language routes
- **Planets** represent topic destinations
- **Discoveries** represent guided lessons
- **Missions** represent coding practice
- **Mission Briefings** represent quizzes
- **Artifacts / Relics** represent mastery rewards
- **NOVA** represents the onboard AI guide

This frontend is built to feel bright, premium, immersive, and launch-ready while remaining fully integrated with the current backend contracts.

---

## Highlights

- **Light-theme only** immersive UI
- **Text-only AlgoLingo branding**
- **Persistent authentication** with token refresh
- **Fully backend-connected core journey**
- **Dedicated pages** for search, achievements, notifications, and artifact details
- **Local mission draft persistence**
- **NOVA AI integration** across ask / hint / debug / recommend flows
- **Responsive shell** with sidebar, topbar, notifications, and profile menu
- **Graceful loading, empty, error, offline, and auth states**

---

## Tech Stack

- **HTML5**
- **CSS3**
- **Vanilla JavaScript (ES Modules)**

No framework is used.

Specifically:
- No React
- No Vue
- No Angular
- No Bootstrap
- No Tailwind

---

## Project Structure

```text
frontend_final/
├── README.md
├── HANDOFF.md
├── index.html
├── assets/
│   ├── css/
│   │   ├── 00-tokens.css
│   │   ├── 01-reset.css
│   │   ├── 02-base.css
│   │   ├── 03-layout.css
│   │   ├── 04-components.css
│   │   ├── 05-pages.css
│   │   └── 06-animations.css
│   └── js/
│       ├── core/
│       │   ├── api.js
│       │   ├── auth.js
│       │   ├── ambient.js
│       │   ├── config.js
│       │   ├── editor.js
│       │   ├── icons.js
│       │   ├── layout.js
│       │   ├── markdown.js
│       │   ├── storage.js
│       │   ├── theme.js
│       │   ├── ui.js
│       │   └── utils.js
│       └── pages/
│           ├── achievements.js
│           ├── artifact.js
│           ├── artifacts.js
│           ├── dashboard.js
│           ├── discovery.js
│           ├── error.js
│           ├── forgot-password.js
│           ├── galaxies.js
│           ├── galaxy.js
│           ├── index.js
│           ├── leaderboard.js
│           ├── login.js
│           ├── notifications.js
│           ├── nova.js
│           ├── planet.js
│           ├── practice.js
│           ├── profile.js
│           ├── quiz.js
│           ├── register.js
│           ├── search.js
│           └── settings.js
└── pages/
    ├── 401.html
    ├── 403.html
    ├── 404.html
    ├── 500.html
    ├── achievements.html
    ├── artifact.html
    ├── artifacts.html
    ├── dashboard.html
    ├── discovery.html
    ├── forgot-password.html
    ├── galaxies.html
    ├── galaxy.html
    ├── leaderboard.html
    ├── login.html
    ├── notifications.html
    ├── nova.html
    ├── offline.html
    ├── planet.html
    ├── practice.html
    ├── profile.html
    ├── quiz.html
    ├── register.html
    ├── search.html
    └── settings.html
```

---

## Experience Model

AlgoLingo uses the following user-facing vocabulary:

| Product Concept | UI Language |
|---|---|
| Programming language path | Galaxy |
| Topic | Planet |
| Lesson | Discovery |
| Coding challenge | Mission |
| Quiz | Mission Briefing |
| Quiz result | Mission Report |
| Badge / reward | Artifact / Relic |
| Profile | Explorer Logbook |
| AI assistant | NOVA |

---

## Main Pages

### Public Pages
- Landing
- Login
- Register
- Forgot Password
- 401 / 403 / 404 / 500 / Offline

### Protected Pages
- Mission Control
- Galaxy Map
- Galaxy Route
- Planet
- Discovery
- Mission
- Mission Briefing
- Artifact Museum
- Artifact Detail
- Achievement Vault
- Signal Archive
- Star Search
- NOVA
- Explorer Logbook
- Constellation Rank
- Settings

---

## Backend Integration

This frontend is designed for the existing FastAPI backend and **must not change backend contracts**.

### Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/logout`

### Core Learning Flow
- `GET /api/v1/dashboard`
- `GET /api/v1/galaxies`
- `GET /api/v1/galaxies/{galaxy_id}`
- `GET /api/v1/planets/{planet_id}`
- `GET /api/v1/discoveries/{discovery_id}`
- `POST /api/v1/discoveries/{discovery_id}/complete`
- `GET /api/v1/practices/{practice_id}`
- `POST /api/v1/practices/{practice_id}/submit`
- `GET /api/v1/practices/{practice_id}/solution`
- `GET /api/v1/quizzes/{planet_id}`
- `POST /api/v1/quizzes/{planet_id}/submit`

### Collection / Ranking / Profile
- `GET /api/v1/artifacts`
- `GET /api/v1/artifacts/{artifact_id}`
- `GET /api/v1/users/{user_id}/artifacts`
- `GET /api/v1/leaderboard`
- `GET /api/v1/profile/{username}`
- `PATCH /api/v1/profile/me`

### NOVA
- `POST /api/v1/nova/ask`
- `POST /api/v1/nova/hint/{practice_id}`
- `POST /api/v1/nova/debug`
- `POST /api/v1/nova/recommend`

### Health
- `GET /api/v1/health`

---

## Important Behavior

### Authentication
- Session is stored in `localStorage`
- Access tokens are attached automatically to authenticated requests
- On `401`, the frontend attempts token refresh once
- If refresh fails, the user is logged out and redirected to login

### Mission Drafts
Mission/editor drafts are stored locally per mission.

### NOVA Sessions
NOVA keeps session IDs in local storage so conversations remain continuous per mode.

### Search
The search page builds a live index using current universe data from the backend.

### Settings
Settings are **local-browser only** and do not modify server-side account data.

---

## Setup

### Requirements
- Python 3.x for serving static files locally
- A running AlgoLingo FastAPI backend

### Run the frontend
From this folder:

```bash
cd /home/user/frontend_final
python -m http.server 5173
```

Open in browser:

```text
http://localhost:5173
```

---

## Backend Base URL

By default, the frontend resolves API requests to:

```text
http://<hostname>:8000/api/v1
```

This logic lives in:
- `assets/js/core/config.js`

The API base URL can also be overridden from the **Settings** page and is saved in local storage.

---

## Design Principles

This frontend intentionally follows these rules:

- **Light theme only**
- **No dark mode** in this build
- **No blue as the main product color**
- **No logo icon**
- **No initials like AL**
- **Text-only wordmark: `AlgoLingo`**
- **Space is the product, not the wallpaper**
- **Galaxies and planets should feel like destinations, not cards**
- **Avoid admin / enterprise / analytics dashboard styling**

---

## Reusable Frontend Architecture

### CSS layering
- `00-tokens.css` → colors, spacing, typography, radii, shadows
- `01-reset.css` → reset / normalization
- `02-base.css` → base typography, backgrounds, global primitives
- `03-layout.css` → shell layout, sidebar, topbar, menus
- `04-components.css` → reusable components
- `05-pages.css` → page-level visual systems
- `06-animations.css` → motion and ambient behavior

### JS core modules
- `api.js` → request wrapper, timeout, token refresh flow
- `auth.js` → auth/session lifecycle
- `layout.js` → shell rendering and page meta
- `ui.js` → toasts, modals, loading/error/empty states
- `storage.js` → local persistence
- `markdown.js` → markdown rendering and code copy behavior
- `editor.js` → mission editor behavior
- `utils.js` → DOM/query/formatting helpers

---

## Current Limitations

### No password reset endpoint
The backend currently does not expose a password reset flow.
The forgot-password page is intentionally informational.

### No standalone code runner endpoint
Missions support submission and official solution reveal, but not a separate run-code action.

### No dedicated backend endpoints for some derived pages
These pages are assembled from existing data:
- Achievement Vault
- Signal Archive
- Star Search

---

## Local Storage Keys

Used by the frontend:

- `algolingo-final:session`
- `algolingo-final:api-base-url`
- `algolingo-final:sidebar-collapsed`
- `algolingo-final:practice-draft:*`
- `algolingo-final:nova-sessions`

---

## Recommended QA Checklist

Before shipping or demoing:

- Verify login and registration
- Verify protected-route redirects
- Verify token refresh after expiry
- Verify discovery completion flow
- Verify mission submission and result rendering
- Verify official solution reveal flow
- Verify mission briefing submit flow
- Verify artifact museum → artifact detail flow
- Verify profile update flow
- Verify leaderboard scope switching and pagination
- Verify NOVA ask / hint / debug / recommend
- Verify search across all major content types
- Verify mobile sidebar and shell interactions
- Verify offline and error states

---

## Development Notes

If continuing work, safest extension points are:

- `assets/css/05-pages.css` for visual refinement
- `assets/js/pages/*.js` for page behavior
- `assets/js/core/ui.js` for reusable UX helpers
- `assets/js/core/layout.js` for shell behavior and navigation

Avoid changing backend assumptions unless backend contracts are intentionally updated.

---

## Related Documentation

For a more implementation-oriented handoff, see:

- `HANDOFF.md`

That file contains:
- page-to-endpoint mapping
- architecture notes
- QA notes
- continuation guidance

---

## Status

This frontend is currently a **complete production-oriented frontend foundation** for AlgoLingo with:
- immersive world-first UI
- backend-connected learning flow
- auth persistence
- route progression
- NOVA integration
- museum / achievement / search / notification systems

It is the correct frontend folder to continue from.
