# ALGOLINGO MVP — EXECUTION BLUEPRINT

**Document:** `ALGOLINGO_MVP_BLUEPRINT.md`  
**Derived From:** PRD v1.0  
**Audience:** Development Team  
**Purpose:** Single source of truth for building the MVP  
**Estimated Read Time:** 12 minutes

---

## SECTION 1: PROJECT OVERVIEW

| Field | Value |
|-------|-------|
| **Name** | AlgoLingo |
| **Core Idea** | Gamified platform teaching Python fundamentals. Space exploration theme: Galaxies = languages, Planets = topics, Discoveries = lessons, Practice = challenges, Artifacts = badges, XP = Knowledge Energy (KE) |
| **Target Users** | College freshmen, career switchers, high school coders, self-learners |
| **Architecture** | REST API (FastAPI) + PostgreSQL + Ollama LLM. Vanilla JS SPA frontend |
| **MVP Goal** | Ship Python Nebula galaxy with 3 fully-functional planets (Syntax Station, Control Flow Crater, Data Depot), working NOVA AI assistant, leaderboards, artifacts, and XP system |

### Tech Stack (Pinned Versions)

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | HTML5 / CSS3 / JavaScript (Vanilla SPA) | ES6+ |
| Backend | Python / FastAPI / Uvicorn | 3.11+ / 0.110+ / 0.29+ |
| Database | PostgreSQL | 15+ |
| ORM | SQLAlchemy | 2.0+ |
| Migration | Alembic | 1.13+ |
| AI | Ollama (local) — CodeLlama or Mistral 7B Q4 | Latest |
| Auth | JWT (python-jose) + bcrypt (passlib) | — |
| Testing | pytest | 8+ |

---

## SECTION 2: MVP FINAL SCOPE

### ✅ INCLUDED IN MVP

```
CATEGORY               ITEMS INCLUDED
───────                ─────────────
Galaxies               Python Nebula only (others locked, visually present)
Planets                Syntax Station, Control Flow Crater, Data Depot
Discoveries            20 total (7 + 6 + 7)
Practice Challenges    18 total (5 + 6 + 7)
Quiz Questions         37 total (10 + 12 + 15)
Artifacts              All Common & Rare artifacts from MVP planets + milestone/basic artifacts
NOVA                   Explain concepts, generate hints, debug code, recommend next topic
Leaderboard            Global, Weekly, Monthly, Galaxy (all-time)
XP System              Full economy with levels 1-12
Ranks                  Cadet, Explorer, Navigator (higher ranks gated by more content)
Authentication         Register, Login, JWT, Profile
Content Storage        Markdown for discoveries, JSON for quizzes/practices
```

### ❌ EXCLUDED FROM MVP

```
CATEGORY               EXCLUDED ITEMS               REASON
───────                ─────────────               ──────
Galaxies               Java Metropolis, C Forge,    Out of scope
                       C++ Frontier
Planets                Function Forge through        Future phases
                       OOP Orbit (Planets 4-9)
Admin Panel            All admin features            Phase 2
Redis Cache            Session caching               Phase 2 (in-memory for MVP)
Docker                 Containerization              Phase 2 (direct deployment for MVP)
Notifications          Push/email notifications      Phase 2
Social Features        Friends, teams, chat          Phase 2+
Sound Design           Ambient sounds, SFX           Phase 2
Voice Interface        NOVA voice                    Phase 3
Code Sandbox           Docker-based code execution   Phase 2 (basic exec() for MVP)
Conversation Memory   NOVA persistent history       Phase 2 (per-session only for MVP)
Adaptive Learning     ML-based path recommendations  Phase 2
File Uploads           Avatar uploads, attachments   Phase 2
Email Verification     Required email confirmation   MVP skip (optional)
Payment/Subscription   Paid content/plans            Phase 3
```

---

## SECTION 3: CORE USER FLOW

```
                          ┌─────────────┐
                          │   LANDING   │
                          │    PAGE     │
                          └──────┬──────┘
                                 │
                     ┌───────────▼───────────┐
                     │    REGISTER / LOGIN   │
                     └───────────┬───────────┘
                                 │
                     ┌───────────▼───────────┐
                     │     ONBOARDING        │
                     │  (single screen:      │
                     │   welcome + tutorial) │
                     └───────────┬───────────┘
                                 │
                     ┌───────────▼───────────┐
                     │    SPACE DOCK         │
                     │    (DASHBOARD)        │
                     │  - Continue learning  │
                     │  - Quick stats        │
                     │  - Recent activity    │
                     └───┬───┬───┬───┬───────┘
                         │   │   │   │
          ┌──────────────┘   │   │   └──────────────┐
          ▼                  ▼   ▼                  ▼
   ┌────────────┐    ┌────────────┐    ┌──────────────────┐
   │   ATLAS    │    │ COMM HUB   │    │ PROFILE /        │
   │  EXPLORER  │    │ LEADERBOARD│    │ ARTIFACT MUSEUM  │
   └──────┬─────┘    └────────────┘    └──────────────────┘
          │
          ▼
   ┌──────────────────────────────────┐
   │        GALAXY VIEW               │
   │  Python Nebula (unlocked)        │
   │  Java/C/C++ (locked, dimmed)     │
   │  Shows 9 planets, 3 accessible   │
   └──────────────┬───────────────────┘
                  │
                  ▼
   ┌──────────────────────────────────┐
   │        PLANET VIEW               │
   │  Shows: progress %, discoveries, │
   │  practices, quiz status, artifact│
   └──────────────┬───────────────────┘
                  │
          ┌───────┼───────────┐
          ▼       ▼           ▼
   ┌──────────┐ ┌──────┐ ┌────────┐
   │DISCOVERY │ │PRACTICE│ │ QUIZ  │
   │ (Lesson) │ │(Code) │ │(Test) │
   └────┬─────┘ └──┬───┘ └───┬────┘
        │          │         │
        ▼          ▼         ▼
   ┌──────────────────────────────┐
   │       RESULTS / REWARDS       │
   │  +XP, Artifact unlocks,      │
   │  Planet progression update   │
   └──────────────┬───────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  RETURN TO     │
         │  SPACE DOCK /  │
         │  NEXT PLANET   │
         └────────────────┘

FLOATING: NOVA Chat Widget (bottom-right, persistent across all views)
```

---

## SECTION 4: CONTENT STRUCTURE

### 4.1 Galaxies (MVP: 1 active, 3 locked)

| Galaxy | Language | MVP Status | Planets Total | Planets Active |
|--------|----------|------------|---------------|----------------|
| Python Nebula | Python | ✅ Active | 9 planned | 3 |
| Java Metropolis | Java | 🔒 Locked | 8 | 0 |
| C Forge | C | 🔒 Locked | 7 | 0 |
| C++ Frontier | C++ | 🔒 Locked | 8 | 0 |

### 4.2 Planets (MVP: 3 complete)

| # | Planet | Topic | Discoveries | Practices | Quiz Qs | XP Total | Difficulty | Unlock |
|---|--------|-------|-------------|-----------|---------|----------|------------|--------|
| 1 | **Syntax Station** | Variables, Types, I/O, Comments | 7 | 5 | 10 | 1,150 | ⭐ | Default |
| 2 | **Control Flow Crater** | if/elif/else, Loops, break/continue | 6 | 6 | 12 | 1,850 | ⭐⭐ | Complete Planet 1 |
| 3 | **Data Depot** | Lists, Tuples, Dicts, Sets | 7 | 7 | 15 | 2,325 | ⭐⭐ | Complete Planet 2 |

**Locked Planets (UI only — show "Coming Soon"):** Function Forge, String Star, Module Moon, File Frontier, Exception Eclipse, OOP Orbit

### 4.3 Discovery Manifest (20 total)

**Planet 1 — Syntax Station (7):**
| ID | Title | Read Time | XP | Prereq |
|----|-------|-----------|----|--------|
| D1.1 | Your First Python Program | 8 min | 75 | None |
| D1.2 | Variables — Your Fuel Tanks | 10 min | 100 | D1.1 |
| D1.3 | Data Types — The Elements of Code | 12 min | 100 | D1.2 |
| D1.4 | Type Conversion — Warping Between Types | 10 min | 100 | D1.3 |
| D1.5 | Input and Output — Communicating with the Universe | 12 min | 100 | D1.3 |
| D1.6 | Comments — Leaving Star Charts | 6 min | 75 | D1.2 |
| D1.7 | String Basics — Crafting Messages | 10 min | 100 | D1.3 |

**Planet 2 — Control Flow Crater (6):**
| ID | Title | Read Time | XP | Prereq |
|----|-------|-----------|----|--------|
| D2.1 | Decision Time — If, Elif, Else | 14 min | 125 | Planet 1 |
| D2.2 | Comparison Operators | 10 min | 100 | D2.1 |
| D2.3 | Logical Operators | 12 min | 125 | D2.1 |
| D2.4 | For Loops — Orbiting Sequences | 14 min | 125 | D2.1 |
| D2.5 | While Loops — Reaching Orbit | 12 min | 125 | D2.4 |
| D2.6 | Break and Continue | 10 min | 100 | D2.4, D2.5 |

**Planet 3 — Data Depot (7):**
| ID | Title | Read Time | XP | Prereq |
|----|-------|-----------|----|--------|
| D3.1 | Lists — Your Cargo Bay | 14 min | 150 | Planet 2 |
| D3.2 | List Methods — Cargo Operations | 14 min | 150 | D3.1 |
| D3.3 | Tuples — Immutable Records | 10 min | 125 | D3.1 |
| D3.4 | Dictionaries — Your Navigation Charts | 14 min | 150 | D3.1 |
| D3.5 | Dictionary Methods — Chart Tools | 12 min | 150 | D3.4 |
| D3.6 | Sets — Unique Elements | 12 min | 125 | D3.1 |
| D3.7 | Choosing the Right Structure | 10 min | 125 | All above |

### 4.4 Practice Challenge Manifest (18 total)

**Planet 1 — Syntax Station (5):**
| ID | Title | Type | Diff | XP |
|----|-------|------|------|----|
| P1.1 | Welcome Aboard! | write_output | ⭐ | 50 |
| P1.2 | Variable Voyage | fill_blanks | ⭐ | 50 |
| P1.3 | Type Checker | code_writing | ⭐ | 75 |
| P1.4 | Age Calculator | code_writing | ⭐⭐ | 100 |
| P1.5 | Mission Brief Generator | scenario | ⭐⭐ | 100 |

**Planet 2 — Control Flow Crater (6):**
| ID | Title | Type | Diff | XP |
|----|-------|------|------|----|
| P2.1 | Number Classifier | code_writing | ⭐⭐ | 75 |
| P2.2 | Even or Odd Quest | code_writing | ⭐⭐ | 75 |
| P2.3 | Countdown Lift-Off | code_writing | ⭐⭐ | 100 |
| P2.4 | Password Checker | scenario | ⭐⭐⭐ | 125 |
| P2.5 | FizzBuzz Voyage | algorithm | ⭐⭐⭐ | 150 |
| P2.6 | Sum of Planets | code_writing | ⭐⭐ | 100 |

**Planet 3 — Data Depot (7):**
| ID | Title | Type | Diff | XP |
|----|-------|------|------|----|
| P3.1 | List Navigator | code_writing | ⭐⭐ | 75 |
| P3.2 | Shopping List Organizer | code_writing | ⭐⭐ | 100 |
| P3.3 | Coordinate Tuple | code_writing | ⭐⭐ | 75 |
| P3.4 | Planet Dictionary | code_writing | ⭐⭐ | 125 |
| P3.5 | Unique Space Rocks | code_writing | ⭐⭐ | 125 |
| P3.6 | Student Grades System | scenario | ⭐⭐⭐ | 175 |
| P3.7 | Data Structure Selector | mcq_conceptual | ⭐⭐ | 100 |

### 4.5 Quiz Structure

| Planet | Questions | Passing | Time Limit | Pass XP | Fail XP | Artifact |
|--------|-----------|---------|------------|---------|---------|----------|
| Syntax Station | 10 | 7/10 (70%) | 15 min | 200 | 50 | Syntax Sage (Common) |
| Control Flow Crater | 12 | 9/12 (75%) | 20 min | 300 | 75 | Flow Master (Common) |
| Data Depot | 15 | 11/15 (73%) | 25 min | 400 | 100 | Data Hoarder (Rare) |

Question types allowed: `multiple_choice`, `true_false`, `fill_blank`, `code_output`, `error_detection`

### 4.6 MVP Artifact List (17 total)

| Artifact | Rarity | Unlock Condition | XP Bonus |
|----------|--------|------------------|----------|
| Syntax Sage | Common | Pass Syntax Station quiz | +5% |
| Flow Master | Common | Pass Control Flow Crater quiz | +5% |
| Data Hoarder | Rare | Pass Data Depot quiz | +10% |
| First Discovery | Common | Complete any 1 discovery | +5% |
| Knowledge Seeker | Common | Complete 10 discoveries | +5% |
| First Practice | Common | Solve any 1 practice | +5% |
| Challenge Rookie | Common | Solve 10 challenges | +5% |
| Quiz Taker | Common | Complete any 1 quiz | +5% |
| First Pass | Common | Pass any quiz | +5% |
| Planet Explorer | Common | Complete any 1 planet | +5% |
| Planet Conqueror | Rare | Complete 3 planets | +10% |
| Consistent Cadet | Common | 3-day login streak | +5% |
| Weekly Warrior | Rare | 7-day login streak | +10% |
| Curious Mind | Common | Ask NOVA 1 question | +5% |
| Rising Star | Common | Top 100 on global leaderboard | +5% |
| Perfect Score | Rare | 100% on any quiz | +10% |
| 100% Explorer | Common | 100% complete one planet | +5% |

---

## SECTION 5: DATABASE BLUEPRINT

### 5.1 Entity Summary

```
CORE:
  users ──┬── user_progress ─── planets ─── galaxies
          ├── user_artifacts ─── artifacts
          ├── quiz_attempts ─── planets
          ├── daily_logins
          ├── nova_interactions
          └── leaderboard_snapshots

CONTENT (seed data, not user-generated):
  galaxies ──┬── planets ──┬── discoveries
              │             ├── practice_challenges
              │             └── quiz_questions
              └── artifacts (standalone, linked via FK from planets)
```

### 5.2 Table Schemas (Developer Ready)

**users**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK, gen_random_uuid() | |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 3-50 chars, alphanumeric+underscore |
| email | VARCHAR(255) | UNIQUE, NOT NULL | |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt |
| xp | INTEGER | DEFAULT 0, CHECK >=0 | |
| level | INTEGER | DEFAULT 1, CHECK >=1 | |
| rank_title | VARCHAR(50) | DEFAULT 'Cadet' | |
| streak_days | INTEGER | DEFAULT 0 | |
| last_login_date | DATE | nullable | For streak calc |
| is_active | BOOLEAN | DEFAULT true | |
| created_at | TIMESTAMP | DEFAULT NOW() | |
| updated_at | TIMESTAMP | DEFAULT NOW() | |

Index: `username`, `email` (unique); `xp DESC` (leaderboard)

**galaxies**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| name | VARCHAR(100) | UNIQUE, NOT NULL | "Python Nebula" |
| description | TEXT | NOT NULL | |
| programming_language | VARCHAR(50) | NOT NULL | "Python" |
| order_number | INTEGER | UNIQUE, NOT NULL | |
| is_locked | BOOLEAN | DEFAULT true | |
| planets_count | INTEGER | DEFAULT 0 | |
| icon_url | VARCHAR(255) | | |

**planets**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| galaxy_id | UUID | FK → galaxies.id, NOT NULL | |
| name | VARCHAR(100) | NOT NULL | |
| tagline | VARCHAR(200) | | |
| description | TEXT | | |
| difficulty | INTEGER | CHECK 1-5, DEFAULT 1 | |
| order_number | INTEGER | NOT NULL | Unique per galaxy |
| xp_total | INTEGER | NOT NULL | |
| estimated_time_minutes | INTEGER | | |
| is_locked | BOOLEAN | DEFAULT true | |
| unlock_condition | TEXT | | e.g., "Complete Syntax Station" |
| artifact_id | UUID | FK → artifacts.id, nullable | Planet completion artifact |
| UNIQUE(galaxy_id, order_number) | | | |

**discoveries**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| planet_id | UUID | FK → planets.id, NOT NULL | |
| title | VARCHAR(200) | NOT NULL | |
| description | TEXT | | |
| content_md | TEXT | NOT NULL | Markdown content |
| learning_objective | TEXT | | |
| read_time_minutes | INTEGER | | |
| difficulty | INTEGER | DEFAULT 1 | |
| xp_reward | INTEGER | NOT NULL | |
| order_number | INTEGER | NOT NULL | |
| prerequisites | JSONB | DEFAULT '[]' | Array of discovery UUIDs |

**practice_challenges**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| planet_id | UUID | FK → planets.id, NOT NULL | |
| title | VARCHAR(200) | NOT NULL | |
| challenge_type | VARCHAR(50) | NOT NULL | enum: write_output, fill_blanks, code_writing, scenario, mcq_conceptual |
| difficulty | INTEGER | DEFAULT 1 | |
| description | TEXT | NOT NULL | Prompt shown to user |
| learning_outcome | TEXT | | |
| xp_reward | INTEGER | NOT NULL | |
| solution_code | TEXT | | Reference solution |
| hints | JSONB | DEFAULT '[]' | Array of hint strings |
| order_number | INTEGER | NOT NULL | |

**quiz_questions**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| planet_id | UUID | FK → planets.id, NOT NULL | |
| question_text | TEXT | NOT NULL | |
| question_type | VARCHAR(50) | NOT NULL | enum: multiple_choice, true_false, fill_blank, code_output, error_detection |
| options | JSONB | | [{id, text}] for MC |
| correct_answer | TEXT | NOT NULL | |
| explanation | TEXT | | Shown after quiz |
| order_number | INTEGER | NOT NULL | |

**quiz_attempts**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| planet_id | UUID | FK → planets.id, NOT NULL | |
| score | INTEGER | NOT NULL | Correct count |
| total_questions | INTEGER | NOT NULL | |
| answers | JSONB | | [{question_id, answer, is_correct}] |
| passed | BOOLEAN | NOT NULL | |
| xp_earned | INTEGER | NOT NULL | |
| attempted_at | TIMESTAMP | DEFAULT NOW() | |

**user_progress**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| planet_id | UUID | FK → planets.id, NOT NULL | |
| completed_discoveries | JSONB | DEFAULT '[]' | Array of discovery UUIDs |
| completed_practices | JSONB | DEFAULT '[]' | Array of practice UUIDs |
| quiz_passed | BOOLEAN | DEFAULT false | |
| quiz_best_score | INTEGER | | |
| completed | BOOLEAN | DEFAULT false | |
| xp_earned | INTEGER | DEFAULT 0 | |
| started_at | TIMESTAMP | DEFAULT NOW() | |
| completed_at | TIMESTAMP | nullable | |
| UNIQUE(user_id, planet_id) | | | |

**artifacts**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| name | VARCHAR(100) | UNIQUE, NOT NULL | |
| description | TEXT | | |
| rarity | VARCHAR(20) | NOT NULL | Common, Rare, Epic, Legendary |
| xp_bonus_percent | INTEGER | DEFAULT 5 | |
| unlock_condition | TEXT | | Human-readable |
| icon_url | VARCHAR(255) | | |
| category | VARCHAR(50) | NOT NULL | planet, galaxy, milestone, streak, quiz, completion, leaderboard, nova, hidden |
| is_hidden | BOOLEAN | DEFAULT false | |

**user_artifacts**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id | |
| artifact_id | UUID | FK → artifacts.id | |
| unlocked_at | TIMESTAMP | DEFAULT NOW() | |
| UNIQUE(user_id, artifact_id) | | | |

**daily_logins**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id | |
| login_date | DATE | NOT NULL | |
| xp_earned | INTEGER | DEFAULT 25 | |
| streak_day | INTEGER | NOT NULL | |
| UNIQUE(user_id, login_date) | | | |

**nova_interactions**
| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id | |
| user_message | TEXT | NOT NULL | |
| nova_response | TEXT | NOT NULL | |
| context_data | JSONB | | galaxy/planet/discovery context |
| session_id | VARCHAR(100) | | |
| created_at | TIMESTAMP | DEFAULT NOW() | |

---

## SECTION 6: API BLUEPRINT

Base URL: `/api/v1`  
Auth: `Authorization: Bearer <JWT>`  
Format: JSON

### 6.1 Auth Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/auth/register` | Create account | No |
| POST | `/auth/login` | Login, get JWT | No |
| POST | `/auth/refresh` | Refresh JWT token | Yes |
| GET | `/auth/me` | Get current user | Yes |

### 6.2 Galaxy Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/galaxies` | List all galaxies | Yes |
| GET | `/galaxies/{id}` | Galaxy detail + planets | Yes |

### 6.3 Planet Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/planets/{id}` | Full planet detail (discoveries, practices, quiz status, artifact) | Yes |

### 6.4 Discovery Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/discoveries/{id}` | Get discovery content (Markdown) | Yes |
| POST | `/discoveries/{id}/complete` | Mark discovery complete, award XP | Yes |

### 6.5 Practice Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/practices/{id}` | Get challenge details | Yes |
| POST | `/practices/{id}/submit` | Submit solution, get validation | Yes |
| GET | `/practices/{id}/solution` | Get reference solution (after attempt) | Yes |

### 6.6 Quiz Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/planets/{id}/quiz` | Get quiz questions (no answers) | Yes |
| POST | `/planets/{id}/quiz/submit` | Submit answers, get results | Yes |

### 6.7 Leaderboard Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/leaderboard?type=global&page=1&limit=20` | Get leaderboard (types: global, weekly, monthly, galaxy) | Yes |
| GET | `/leaderboard?type=galaxy&galaxy_id={id}` | Galaxy-specific leaderboard | Yes |

### 6.8 Artifact Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/artifacts` | List all artifacts + user's earned status | Yes |
| GET | `/artifacts/{id}` | Single artifact detail | Yes |
| GET | `/users/{userId}/artifacts` | Another user's artifact collection | Yes |

### 6.9 Profile / Dashboard Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| GET | `/profile/{username}` | Public profile | Yes |
| PATCH | `/profile/me` | Update own bio/avatar | Yes |
| GET | `/dashboard` | Dashboard data (quick stats, continue learning, recent activity) | Yes |

### 6.10 NOVA Endpoints

| Method | Endpoint | Purpose | Auth |
|--------|----------|---------|------|
| POST | `/nova/ask` | Ask NOVA a question | Yes |
| POST | `/nova/hint/{practiceId}` | Request hint for challenge | Yes |
| POST | `/nova/debug` | Debug submitted code | Yes |
| POST | `/nova/recommend` | Get next-topic recommendation | Yes |

---

## SECTION 7: PAGE CHECKLIST

| # | Page | SPA Route | Purpose | API Dependencies | Status |
|---|------|-----------|---------|------------------|--------|
| 1 | Landing | `/` | Hero, "Get Started" CTA | None | ✅ Build |
| 2 | Login | `/login` | Email + password form | POST /auth/login | ✅ Build |
| 3 | Register | `/register` | Username + email + password | POST /auth/register | ✅ Build |
| 4 | Dashboard | `/dashboard` | Progress summary, continue, stats | GET /dashboard | ✅ Build |
| 5 | Galaxy Explorer | `/atlas` | Galaxy cards (1 active, 3 locked) | GET /galaxies | ✅ Build |
| 6 | Galaxy View | `/galaxy/{id}` | Planet grid with progress rings | GET /galaxies/{id} | ✅ Build |
| 7 | Planet View | `/planet/{id}` | Discovery/practice/quiz lists | GET /planets/{id} | ✅ Build |
| 8 | Discovery Reader | `/discovery/{id}` | Markdown content + "Complete" btn | GET /discoveries/{id}, POST /.../complete | ✅ Build |
| 9 | Practice (Code) | `/practice/{id}` | Code editor + submit + hints | GET /practices/{id}, POST .../submit | ✅ Build |
| 10 | Quiz | `/quiz/{planetId}` | Timed question flow | GET /planets/{id}/quiz, POST .../submit | ✅ Build |
| 11 | Quiz Results | `/results/{planetId}` | Score, XP, artifact unlocks | Response from quiz submit | ✅ Build |
| 12 | Artifact Museum | `/artifacts` | Grid of all artifacts + user's collection | GET /artifacts | ✅ Build |
| 13 | Leaderboard | `/leaderboard` | Tabbed: Global/Weekly/Monthly/Galaxy | GET /leaderboard | ✅ Build |
| 14 | Profile | `/profile/{username}` | Stats, rank, artifacts, planets | GET /profile/{username} | ✅ Build |
| 15 | NOVA Chat | Floating widget | Persistent across all pages | POST /nova/ask | ✅ Build |
| 16 | Admin Panel | — | NOT IN MVP | — | ❌ Phase 2 |

---

## SECTION 8: XP SYSTEM

### 8.1 XP Sources & Values

| Activity | Base XP | Repeatable? |
|----------|---------|-------------|
| Discovery completion | 75–150 (per discovery) | No (one-time) |
| Practice completion | 50–175 (per challenge) | No (one-time) |
| Quiz pass | 200–400 (per planet) | No (one-time) |
| Quiz fail | 50–100 (25% of pass) | No (one-time) |
| Daily login | 25 | Yes (once/day) |
| 3-day streak bonus | 50 | Yes (per cycle) |
| 7-day streak bonus | 100 | Yes (per cycle) |
| 30-day streak bonus | 500 | Yes (per cycle) |
| Artifact unlock (Common) | 50 | No |
| Artifact unlock (Rare) | 150 | No |
| Artifact unlock (Epic) | 500 | No |
| Planet 100% completion | 200 bonus | No |
| Leaderboard weekly top 10 | 100-200 | Yes (weekly) |
| Leaderboard monthly top 10 | 200-500 | Yes (monthly) |

### 8.2 Level Progression (Quadratic Formula)

`XP_required_for_level(n) = 250 * n² - 250 * n`

| Level | Title | Cumulative XP | XP to Next |
|-------|-------|--------------|------------|
| 1 | Cadet | 0 | 500 |
| 2 | Cadet | 500 | 1,000 |
| 3 | Explorer | 1,500 | 2,000 |
| 4 | Explorer | 3,500 | 3,000 |
| 5 | Explorer | 6,500 | 4,000 |
| 6 | Navigator | 10,500 | 5,000 |
| 7 | Navigator | 15,500 | 6,000 |
| 8 | Navigator | 21,500 | 8,000 |
| 9 | Commander | 29,500 | 10,000 |
| 10 | Commander | 39,500 | 15,000 |
| 11 | Commander | 54,500 | 20,000 |
| 12 | Galactic Legend | 74,500 | Max |

**MVP Max Achievable:** ~5,325 XP (completing all 3 planets) → Level 3-4

### 8.3 Rank Progression

| Rank | Min Level | Additional Requirement |
|------|-----------|----------------------|
| Cadet | 1 | None |
| Explorer | 3 | Complete Syntax Station |
| Navigator | 6 | Complete Control Flow Crater |
| Commander | 9 | Complete Data Depot |
| Galactic Legend | 12 | Complete ALL MVP + Top 50 leaderboard |

### 8.4 Artifact XP Bonuses

Bonus is multiplicative across all earned artifacts: `total_bonus = SUM(bonus_percent_of_active_artifacts)`.  
Example: Syntax Sage (+5%) + Flow Master (+5%) + Data Hoarder (+10%) = +20% XP on all future earnings.

### 8.5 Unlock Rules

- Planets unlock sequentially (cannot skip)
- Quiz unlocks after ALL discoveries + ALL practices completed
- Artifacts unlock on specific condition triggers (quiz pass, streak, milestone)
- Leaderboard unlocks at Level 3 (after completing Syntax Station)
- NOVA chat unlocks at registration (always available)

---

## SECTION 9: ARTIFACT SYSTEM (MVP)

### 9.1 Planet Completion Artifacts

| Name | Rarity | How to Get | XP Bonus |
|------|--------|------------|----------|
| Syntax Sage | Common | Pass Syntax Station quiz | +5% |
| Flow Master | Common | Pass Control Flow Crater quiz | +5% |
| Data Hoarder | Rare | Pass Data Depot quiz | +10% |

### 9.2 Milestone Artifacts

| Name | Rarity | Unlock | XP Bonus |
|------|--------|--------|----------|
| First Discovery | Common | Complete 1 discovery | +5% |
| Knowledge Seeker | Common | Complete 10 discoveries | +5% |
| First Practice | Common | Solve 1 practice challenge | +5% |
| Challenge Rookie | Common | Solve 10 challenges | +5% |
| Quiz Taker | Common | Complete 1 quiz | +5% |
| First Pass | Common | Pass 1 quiz | +5% |
| Planet Explorer | Common | Complete 1 planet | +5% |
| Planet Conqueror | Rare | Complete 3 planets | +10% |
| 100% Explorer | Common | 100% complete 1 planet (all discoveries + all practices + quiz pass) | +5% |

### 9.3 Streak Artifacts

| Name | Rarity | Unlock | XP Bonus |
|------|--------|--------|----------|
| Consistent Cadet | Common | 3-day login streak | +5% |
| Weekly Warrior | Rare | 7-day login streak | +10% |

### 9.4 Quiz Artifacts

| Name | Rarity | Unlock | XP Bonus |
|------|--------|--------|----------|
| Perfect Score | Rare | 100% on any quiz | +10% |

### 9.5 Leaderboard Artifacts

| Name | Rarity | Unlock | XP Bonus |
|------|--------|--------|----------|
| Rising Star | Common | Top 100 global | +5% |

### 9.6 NOVA Artifacts

| Name | Rarity | Unlock | XP Bonus |
|------|--------|--------|----------|
| Curious Mind | Common | Ask NOVA 1 question | +5% |

**Total MVP Artifacts: 17** (13 Common, 4 Rare)

---

## SECTION 10: NOVA MVP

### 10.1 Capabilities (MVP)

| Capability | How it works |
|-----------|--------------|
| Explain Concepts | User asks concept question → NOVA gets context + query → Ollama generates response |
| Generate Hints | User clicks "Get Hint" on practice → NOVA gets practice context → returns step-by-step hint (NOT solution) |
| Debug Code | User pastes code + description → NOVA identifies bugs → returns issues + fixed code + explanation |
| Recommend Next Topic | NOVA checks user's progress → returns suggestion ("Review X" or "Try Y next") |
| Generate Practice Qs | User asks for more practice → NOVA generates similar problem |
| Learning Recommendations | Based on quiz performance, NOVA suggests weak areas to review |

### 10.2 Inputs (Sent to Ollama)

```json
{
  "user_id": "uuid",
  "galaxy_id": "uuid",
  "planet_id": "uuid",
  "discovery_id": "uuid|null",
  "practice_id": "uuid|null",
  "current_topic": "Variables and Data Types",
  "user_level": 3,
  "user_rank": "Explorer",
  "user_xp": 2450,
  "streak_days": 5,
  "recent_activity": ["completed_discovery_1_2", "solved_challenge_1_3"],
  "conversation_history": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
  "user_message": "Can you explain f-strings?"
}
```

### 10.3 System Prompt

```
You are NOVA, an AI learning assistant on AlgoLingo.
Help students learn programming using space exploration metaphors.
Call user "Captain" or "Explorer". Be concise (<150 words).
Rules: NEVER give direct quiz answers. Guide, don't provide full solutions for practice.
Format code with ```python blocks.

Current Context:
- Galaxy: {name}
- Planet: {name}
- Topic: {topic}
- User Level: {level} | Rank: {rank} | XP: {xp} | Streak: {days}
```

### 10.4 Limitations (MVP)

| Limitation | Impact |
|-----------|--------|
| No cross-session memory | Chat resets on page refresh (last 5 messages kept in session) |
| 512 max tokens response | Short answers only |
| No code execution | NOVA cannot run user code — only analyze text |
| No RAG | NOVA relies on LLM training data + minimal context |
| 30 requests/hour/user | Rate limited |
| ~2-5s response time | Ollama inference on local CPU/GPU |

---

## SECTION 11: USER PROGRESS RULES

| Question | Answer | Rationale |
|----------|--------|-----------|
| Can users skip discoveries? | **No.** Must complete sequentially within a planet | Ensures foundational knowledge |
| Can users replay discoveries? | **Yes.** Read-only replay, no additional XP | Good for review |
| Can users retake quizzes? | **Yes, if failed** (instant retry). **No, if passed** (24h cooldown) | Prevents XP farming while allowing recovery |
| Can users replay challenges? | **Yes.** Practice mode only, no additional XP after first completion | Practice is free, rewards are one-time |
| Can users lose XP? | **No.** XP only increases, never decreases | Avoids frustration |
| Can users revisit completed planets? | **Yes.** View-only mode | Portfolio / review |
| Can users earn duplicate artifacts? | **No.** One-time unlock per artifact | Rarity preserved |
| Can users unlock planets early? | **No.** Strict sequential unlock via planet completion | Curriculum integrity |
| Can users view solutions without attempting? | **Yes, but only 50% XP awarded** | Incentivizes genuine attempt |
| Can users see locked content? | **Yes, visually** (dimmed/locked state shown) | Teases future content |

---

## SECTION 12: DATABASE STATUS DEFINITIONS

### users
| Field | Status Values |
|-------|---------------|
| `rank_title` | `Cadet`, `Explorer`, `Navigator`, `Commander`, `Galactic Legend` |

### planets
| Status | Derived From | Logic |
|--------|-------------|-------|
| `LOCKED` | `is_locked=true` + no user_progress row | Default state |
| `UNLOCKED` | `is_locked=false` OR parent planet completed | When unlock condition met |
| `IN_PROGRESS` | user_progress exists AND `completed=false` | User has started |
| `COMPLETED` | user_progress.completed=true | All discoveries + practices + quiz passed |

### discoveries
| Status | Logic |
|--------|-------|
| `LOCKED` | Prerequisites not met |
| `AVAILABLE` | Prerequisites met, not yet completed |
| `COMPLETED` | UUID in user_progress.completed_discoveries |

### practice_challenges
| Status | Logic |
|--------|-------|
| `LOCKED` | Previous challenge not completed (sequential) |
| `AVAILABLE` | Previous challenge completed, this one not |
| `COMPLETED` | UUID in user_progress.completed_practices |

### quiz
| Status | Logic |
|--------|-------|
| `LOCKED` | Not all discoveries + practices completed |
| `AVAILABLE` | All content completed, no passed attempt |
| `PASSED` | Most recent attempt passed |
| `FAILED` | All attempts have failed |

### artifacts
| Status | Logic |
|--------|-------|
| `LOCKED` | No row in user_artifacts |
| `COLLECTED` | Row in user_artifacts exists |

---

## SECTION 13: AUTHENTICATION & AUTHORIZATION

### 13.1 Flows

**Register:**
1. Client sends `{username, email, password, confirm_password}`
2. Server validates (username 3-50 chars, email format, password >=8 chars with 1 upper + 1 number, passwords match)
3. Server checks uniqueness (username + email)
4. Hash password with bcrypt
5. Insert user, generate JWT, return `{user, access_token}`

**Login:**
1. Client sends `{email, password}`
2. Server looks up user by email
3. Verify bcrypt hash
4. Generate JWT (24h expiry) + refresh token (30d expiry)
5. Update `last_login_date`, calculate streak
6. Return `{user, access_token, refresh_token, expires_in}`

**JWT Payload:**
```json
{
  "sub": "user_uuid",
  "username": "astromax",
  "exp": 1718352000,
  "iat": 1718265600
}
```

### 13.2 Token Configuration

| Parameter | Value |
|-----------|-------|
| JWT Algorithm | HS256 |
| JWT Expiry | 24 hours |
| Refresh Token Expiry | 30 days |
| Password Min Length | 8 |
| Password Requirements | 1 uppercase, 1 number |

### 13.3 Protected Routes

- All routes except `/auth/register`, `/auth/login`, and `/` (landing) require valid JWT
- JWT sent in header: `Authorization: Bearer <token>`
- Invalid/expired JWT returns 401
- Expired JWT with valid refresh token → new JWT via `/auth/refresh`

### 13.4 Roles

| Role | Scope |
|------|-------|
| `USER` | All learner features (MVP only) |
| `ADMIN` | NOT in MVP (Phase 2) |

---

## SECTION 14: CONTENT STORAGE STRATEGY

| Content Type | Format | Rationale |
|-------------|--------|-----------|
| **Discoveries** | **Markdown** (stored in `content_md` column as TEXT) | Easy to write, render, version control. FastAPI can render to HTML or return raw MD. No extra parsing library needed. |
| **Quiz Questions** | **JSON** (stored in `options` column as JSONB) | Flexible structure for MC/TF/FillBlank. PostgreSQL JSONB allows querying. |
| **Practice Challenges** | **JSON** (hints stored as JSONB array) | Variable-length hints per challenge. |
| **Code Snippets** | **Markdown code blocks** within discovery content_md | Native Markdown. Syntax highlighting done client-side. |
| **Images** | **Static files** in `/assets/images/` | Served directly by FastAPI's StaticFiles mount. No DB needed. |

**Decision:** All content is seeded into PostgreSQL via Alembic migrations. No CMS or file-based content loading in MVP.

---

## SECTION 15: API RESPONSE STANDARDS

### Success Response
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

### Error Response
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Planet not found",
    "details": {}
  }
}
```

### Validation Error
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "username": ["Must be 3-50 characters"],
      "email": ["Invalid email format"]
    }
  }
}
```

### Authentication Error
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token",
    "details": {}
  }
}
```

### Standard HTTP Status Codes

| Code | When |
|------|------|
| 200 | Success |
| 201 | Created (registration) |
| 400 | Bad request / validation |
| 401 | Unauthenticated |
| 403 | Forbidden (locked content) |
| 404 | Not found |
| 409 | Conflict (duplicate) |
| 422 | Unprocessable entity |
| 429 | Rate limited |
| 500 | Internal server error |

---

## SECTION 16: NOVA CONTEXT ARCHITECTURE

### 16.1 What NOVA Receives

```
FROM USER SESSION:
  ✓ Current galaxy ID & name
  ✓ Current planet ID & name
  ✓ Current discovery ID (if viewing one)
  ✓ Current practice ID (if attempting one)
  ✓ User's level, rank, XP, streak

FROM DATABASE:
  ✓ Recent activity log (last 5 actions)
  ✓ Quiz scores for current planet
  ✓ Completed discovery list
  ✓ Completed practice list
  ✓ Earned artifact names

FROM FRONTEND:
  ✓ User's question text
  ✓ Last 5 message pairs (user + assistant) from current session
```

### 16.2 What NOVA Must NEVER Receive

```
  ✗ User password or password_hash
  ✗ JWT tokens
  ✗ Other users' data (usernames, emails, XP)
  ✗ Database connection strings
  ✗ API keys
  ✗ Server environment variables
  ✗ Admin credentials
```

### 16.3 Technical Constraints

| Parameter | MVP Value | Reason |
|-----------|-----------|--------|
| Max chat history | Last 5 exchanges (10 messages) | Token budget |
| Max prompt size | ~2,000 tokens (system + context + history + query) | Ollama context window |
| Response timeout | 10 seconds | UX latency threshold |
| Max response tokens | 512 | Latency + relevance |
| Rate limit | 30 requests/hour/user | Prevent abuse + Ollama load |
| Session persistence | In-memory only (no DB for session) | Simplifies MVP |

---

## SECTION 17: TESTING STRATEGY

| Layer | What to Test | Tool | Priority |
|-------|-------------|------|----------|
| **Unit** | All service functions (auth_service, scoring_service, progress_service, gamification_service) | pytest | HIGH |
| **Unit** | Model methods and validations | pytest | HIGH |
| **Unit** | JWT encode/decode, password hashing | pytest | HIGH |
| **API** | Every endpoint: success + error cases | pytest + httpx (TestClient) | HIGH |
| **API** | Auth middleware (unauthenticated, expired token, invalid token) | pytest + TestClient | HIGH |
| **API** | Rate limiting middleware | pytest + TestClient | MEDIUM |
| **Database** | Model CRUD operations | pytest + test DB | HIGH |
| **Database** | Alembic migrations (upgrade + downgrade) | pytest-alembic | HIGH |
| **Database** | Unique constraints, FK constraints | pytest | MEDIUM |
| **Frontend** | SPA routing (all 15 pages) | Manual + Playwright (optional) | HIGH |
| **Frontend** | Auth flow (register → login → JWT storage → protected pages) | Manual | HIGH |
| **Frontend** | Quiz engine (timer, question nav, submit) | Manual | HIGH |
| **Frontend** | Code submission flow (write → submit → result) | Manual | HIGH |
| **Integration** | Full planet completion flow (discoveries → practices → quiz → artifact) | pytest + TestClient | HIGH |
| **Integration** | NOVA API → Ollama integration | pytest (mock Ollama) | MEDIUM |
| **Integration** | Leaderboard calculations after multiple user activities | pytest | MEDIUM |

**Key Testing Decisions:**
- Use SQLite in-memory or separate test PostgreSQL for tests
- Mock Ollama responses (don't call real LLM in tests)
- Each test file mirrors a router module (e.g., `test_auth.py`, `test_galaxy.py`, `test_planet.py`)
- Minimum 80% code coverage target

---

## SECTION 18: DEPLOYMENT PLAN

### 18.1 Development Environment

| Component | Setup |
|-----------|-------|
| Frontend | `python -m http.server 8000` or live-server. Connect to local backend. |
| Backend | `uvicorn backend.main:app --reload --port 8000` |
| Database | Local PostgreSQL instance (`createdb algolingo`) |
| AI | Ollama installed locally. `ollama pull codellama:7b-q4` |
| ENV | `.env` file with `DATABASE_URL`, `JWT_SECRET_KEY`, `OLLAMA_BASE_URL=http://localhost:11434` |

### 18.2 Production Environment

| Component | Recommendation |
|-----------|---------------|
| Frontend | Static files served by nginx or CDN. No build step (vanilla JS). |
| Backend | Uvicorn behind nginx reverse proxy. Multiple workers. `systemd` service. |
| Database | PostgreSQL 15+ on same VPS or managed (RDS, Cloud SQL, DigitalOcean Managed DB) |
| AI | Ollama on same server (CPU inference OK for 7B Q4, ~2-5s response). Dedicated GPU instance optional. |
| Server | Single VPS minimum: 4 vCPU, 8GB RAM, 50GB SSD (for Ollama + DB + App) |

### 18.3 Production Checklist

| Item | Done |
|------|------|
| [ ] nginx reverse proxy configured (SSL termination, static file serving) |
| [ ] SSL certificate (Let's Encrypt / certbot) |
| [ ] Environment variables set (no `.env` in prod) |
| [ ] `JWT_SECRET_KEY` = strong random 256-bit value |
| [ ] PostgreSQL connection pooling (pgbouncer or built-in pool) |
| [ ] CORS restricted to frontend domain |
| [ ] Database backups configured (daily pg_dump) |
| [ ] Application logging to file (not stdout) |
| [ ] Ollama running as systemd service |
| [ ] Health check endpoint (`GET /health`) |
| [ ] Rate limiting enabled |
| [ ] Monitoring (basic: uptime, response time, error rate) |

---

## SECTION 19: MVP EXCLUSIONS

**The following must NOT be built in MVP. Any scope creep into these areas must be rejected:**

| Feature | Reason Excluded |
|---------|----------------|
| Java Metropolis galaxy | Out of MVP scope |
| C Forge galaxy | Out of MVP scope |
| C++ Frontier galaxy | Out of MVP scope |
| Planets 4-9 (Function Forge, String Star, Module Moon, File Frontier, Exception Eclipse, OOP Orbit) | Phase 2+ |
| Admin Panel (any admin interface) | Phase 2 |
| Redis / caching layer | Phase 2 |
| Docker / containerization | Phase 2 |
| Email verification flow | MVP skip (optional) |
| Push notifications | Phase 2 |
| Email notifications | Phase 2 |
| Friends system / social features | Phase 2+ |
| Teams / groups | Phase 2+ |
| Marketplace / shop | Phase 3 |
| Voice chat / speech-to-text | Phase 3 |
| Multi-model AI (Claude/GPT fallback) | Phase 3 |
| Advanced analytics dashboards | Phase 2 |
| Avatar uploads / customization | Phase 2 |
| Sound effects / music | Phase 2 |
| Dark mode toggle | Phase 2 |
| i18n / multi-language | Phase 2 |
| Code execution sandbox (Docker) | Phase 2 (MVP uses `exec()` with restrictions) |
| Adaptive/personalized learning paths | Phase 2 |
| Subscription / payments | Phase 3 |
| Password reset flow | Phase 2 (MVP: admin-assisted only) |
| OAuth / social login | Phase 2 |

---

## SECTION 20: OPEN QUESTIONS & DECISIONS REQUIRED

### Product Decisions

| # | Question | Priority | Recommended | Reasoning | Impact |
|---|----------|----------|-------------|-----------|--------|
| 1 | Should onboarding be skippable? | HIGH | Yes, skip button on onboarding screen | Power users want to start immediately | Low effort |
| 2 | Should daily login XP reset at midnight UTC or user's timezone? | HIGH | Midnight UTC | Simpler implementation, no timezone handling | Medium — affects streak logic |
| 3 | Should we show quiz answers after failure? | MEDIUM | Yes, show explanations for all questions | Learning opportunity | Low effort |
| 4 | How many quiz retries allowed per day? | MEDIUM | 3 attempts per 24h after failure | Balance between persistence and abuse | Low effort |
| 5 | Should locked planets show their name/description or be hidden? | LOW | Show name + "Coming Soon" overlay | Teases content, builds anticipation | Low effort |

### Gamification Decisions

| # | Question | Priority | Recommended | Reasoning | Impact |
|---|----------|----------|-------------|-----------|--------|
| 6 | Should artifact XP bonuses stack or only the highest apply? | HIGH | Stack (additive) | More rewarding, encourages collection | Medium — recalc on each artifact earn |
| 7 | Should leaderboard refresh be real-time or cached? | HIGH | Cached 5 min, user's own rank real-time | Performance + responsiveness | Medium |
| 8 | Should failed quiz still give XP? | MEDIUM | Yes, 25% of pass XP | Encourages retry, not punishing | Low |

### Database Decisions

| # | Question | Priority | Recommended | Reasoning | Impact |
|---|----------|----------|-------------|-----------|--------|
| 9 | JSONB vs separate tables for quiz answers/options? | HIGH | JSONB for options, separate quiz_attempts table with JSONB answers | Flexible for different question types, queryable when needed | Low |
| 10 | Store discovery content as file or DB column? | HIGH | DB column (content_md TEXT) | Simpler seeding, no filesystem dependency, easier backups | Low |

### Authentication Decisions

| # | Question | Priority | Recommended | Reasoning | Impact |
|---|----------|----------|-------------|-----------|--------|
| 11 | Email verification required for MVP? | HIGH | **No — skip for MVP** | Reduces friction, simpler launch | High — saves ~1 week dev time |
| 12 | Password reset flow needed? | MEDIUM | **No — Phase 2** | Complex flow, low usage in early stage | Medium |

### Content Decisions

| # | Question | Priority | Recommended | Reasoning | Impact |
|---|----------|----------|-------------|-----------|--------|
| 13 | Should discovery content include images/diagrams? | MEDIUM | Yes, static images referenced via Markdown | Visual learners benefit | Medium — asset creation needed |
| 14 | Code validation: exact output match or flexible? | HIGH | Exact output match (trim whitespace) | Simple, unambiguous | Low |
| 15 | Should practice challenges support multiple correct solutions? | MEDIUM | No — MVP uses exact output matching | Keeps validation simple | Low |

### NOVA Decisions

| # | Question | Priority | Recommended | Reasoning | Impact |
|---|----------|----------|-------------|-----------|--------|
| 16 | Ollama model: CodeLlama 7B vs Mistral 7B? | HIGH | Mistral 7B Q4 | Better general instruction following, smaller memory footprint | Low — easy to swap |
| 17 | Should NOVA responses include code examples? | MEDIUM | Yes, formatted in ```python blocks | Essential for learning | Low |
| 18 | Rate limit: what happens when exceeded? | MEDIUM | Return 429 with retry-after header | Standard practice | Low |

### Deployment Decisions

| # | Question | Priority | Recommended | Reasoning | Impact |
|---|----------|----------|-------------|-----------|--------|
| 19 | Single server or separate DB server? | HIGH | Single VPS for MVP | Cost-effective, simpler | Low |
| 20 | Ollama on same server or separate? | HIGH | Same server (CPU inference) | Simpler architecture, no network latency | Medium — needs 8GB RAM minimum |

---

## SECTION 21: ASSUMPTIONS MADE

| # | Assumption | Reasoning | Risk | Alternative |
|---|-----------|-----------|------|-------------|
| 1 | Users have modern browsers (ES6+, CSS Grid support) | Vanilla JS SPA | Low — target audience uses Chrome/Firefox | Add polyfills if needed |
| 2 | Ollama can run on MVP server hardware (4 vCPU, 8GB RAM) | Q4 quantized models are optimized for CPU | **MEDIUM RISK** — may need GPU or smaller model | Use phi-2 (2.7B) or Gemma 2B as fallback |
| 3 | All content can be written in Markdown without complex interactive elements | Standard educational content | Low | Embed iframe for interactive content in Phase 2 |
| 4 | Users will not attempt to hack the code execution endpoint | MVP uses `exec()` with sanitization | **HIGH RISK** — code injection possible | Phase 2: Docker sandbox. MVP: block dangerous imports, set resource limits |
| 5 | Sequential planet unlock is the right progression model | Standard curriculum design | Low — aligns with educational best practices | Allow reordering in Phase 2 adaptive learning |
| 6 | 512 tokens is sufficient for NOVA responses | Short, focused answers | Low — can increase if needed | Configurable in Phase 2 |
| 7 | Users will create meaningful usernames | Standard expectation | Low — can add profanity filter in Phase 2 | — |
| 8 | No email verification needed for MVP | Reduces friction | **MEDIUM RISK** — bot accounts possible | Add CAPTCHA on register (Google reCAPTCHA v3, free tier) |
| 9 | XP values are balanced for 3 planets | Based on estimated completion time | Low — can tune values in first month post-launch | Monitor completion rates, adjust XP if needed |
| 10 | Leaderboard with 500+ users will perform acceptably | Proper indexing + 5 min caching | Low | Add pagination + caching |

---

## SECTION 22: MISSING INFORMATION

| # | Missing Item | Priority | Suggested Resolution |
|---|-------------|----------|---------------------|
| 1 | **CAPTCHA on registration** — No mention of bot protection | MEDIUM | Add Google reCAPTCHA v3 (free) or simple math challenge |
| 2 | **Exact code validation logic** — PRD says "output comparison" but doesn't specify sanitization rules | HIGH | Document blocked imports: `os`, `subprocess`, `sys`, `eval`, `exec`, `open`, `__import__`. Set `timeout=5s` for code execution. |
| 3 | **Error message catalog** — PRD has tone examples but no standardized error message list | LOW | Create `errors.py` with all user-facing messages during implementation |
| 4 | **Avatar system** — PRD mentions avatars but no default/dynamic avatar generation | LOW | Generate avatars from initials + rank color (CSS-based, no file storage) |
| 5 | **Streak calculation timezone** — PRD says "midnight UTC" but doesn't specify handling | MEDIUM | Use UTC everywhere. Login date = UTC date of `last_login_date` check. |
| 6 | **Notification system** for artifact unlocks / quiz results | LOW | Inline on-page animation only. No email/push in MVP. |
| 7 | **Metrics/analytics tracking** — No mention of internal tracking for success metrics | MEDIUM | Add simple event logging table (`user_events`): user_id, event_type, event_data, timestamp. No external analytics in MVP. |
| 8 | **Daily goal definition** — PRD mentions "monthly perfect" but no daily goal logic | LOW | Skip daily goals in MVP. Only streak = login. |
| 9 | **Search functionality** for leaderboard — PRD has "Search Explorer" in mockup | LOW | Client-side filter only (no server-side search in MVP) |
| 10 | **Terms of Service / Privacy Policy** pages | LOW | Static Markdown pages served from backend. No DB needed. |

---

## SECTION 23: DEVELOPMENT READINESS REPORT

| Area | Score (1-10) | Notes |
|------|-------------|-------|
| **Product Readiness** | 9/10 | Clear scope, well-defined features, 3 planets fully detailed |
| **Database Readiness** | 8/10 | 12 tables defined with columns, types, FKs. Missing: index definitions for some queries |
| **Backend Readiness** | 7/10 | APIs defined. Missing: exact validation logic for code execution, error message standardization |
| **Frontend Readiness** | 6/10 | Pages listed but no wireframes or component breakdown. Design variables defined but no mockups. **Biggest gap.** |
| **AI Readiness** | 7/10 | System prompt defined, context flow defined. Risk: Ollama performance on MVP hardware. |
| **Deployment Readiness** | 5/10 | Environment plan exists but not tested. Docker config missing (MVP doesn't use it). **Need deploy scripts.** |
| **Testing Readiness** | 6/10 | Strategy defined but no test cases written. Need test data fixtures. |

### Biggest Blockers (Must be resolved before coding starts):

1. **🔴 Code Execution Security** — `exec()`-based validation is a security risk. Must finalize sanitization blocklist and resource limits before implementing practice submission.

2. **🔴 Frontend Wireframes** — No visual mockups exist. Development cannot start on UI without agreed layouts for all 15 pages/views. Minimum: hand-drawn wireframes or Figma prototypes.

3. **🟡 Ollama Hardware Validation** — Need to verify that the target MVP server can run Mistral 7B Q4 within acceptable latency (under 5s per response). If not, downgrade to phi-2 or Gemma 2B.

4. **🟡 Seed Content Authoring** — All 20 discoveries, 18 practices, and 37 quiz questions need to be written in Markdown/JSON before backend seeding can begin.

---

## SECTION 24: IMMEDIATE NEXT ACTIONS

### Execution Order (Build Sequence)

```
TASK 1: RESOLVE OPEN QUESTIONS
  Goal: Get all priority HIGH decisions signed off
  Deliverable: Signed decision log
  Dependencies: None
  Effort: 1 day
  Owner: PM + CTO

TASK 2: CREATE FRONTEND WIREFRAMES
  Goal: Agree on all 15 page layouts
  Deliverable: Figma / hand-drawn wireframes for all views
  Dependencies: Task 1 (scope confirmed)
  Effort: 3 days
  Owner: Designer / PM

TASK 3: SEED CONTENT AUTHORING
  Goal: Write all 20 discoveries (Markdown), 18 practices (JSON), 37 quiz questions (JSON)
  Deliverable: content/ directory with all seed data
  Dependencies: None (can run in parallel with Tasks 1-2)
  Effort: 5 days
  Owner: Content team / PM

TASK 4: SET UP PROJECT INFRASTRUCTURE
  Goal: Create repo, directory structure, config files, database
  Deliverable: Working dev environment
  Dependencies: None
  Effort: 1 day
  Owner: Tech Lead

TASK 5: CREATE DATABASE SCHEMA + MIGRATIONS
  Goal: Implement all 12 tables, relationships, indexes
  Deliverable: Alembic migrations (up + down)
  Dependencies: Task 4
  Effort: 2 days
  Owner: Backend Dev

TASK 6: BUILD AUTHENTICATION SYSTEM
  Goal: Register, login, JWT, middleware, profile endpoints
  Deliverable: Auth APIs working + tested
  Dependencies: Task 5
  Effort: 2 days
  Owner: Backend Dev

TASK 7: BUILD CONTENT APIS
  Goal: Galaxies, planets, discoveries, practices, quiz endpoints + progress tracking
  Deliverable: All learning flow APIs working + tested
  Dependencies: Tasks 5, 6, 3 (seed content)
  Effort: 4 days
  Owner: Backend Dev

TASK 8: BUILD XP + GAMIFICATION SYSTEM
  Goal: XP calculation, level/rank progression, artifact unlocks, leaderboard
  Deliverable: Scoring + gamification services + tested
  Dependencies: Tasks 5, 6, 7
  Effort: 3 days
  Owner: Backend Dev

TASK 9: BUILD NOVA AI SERVICE
  Goal: Ollama integration, prompt builder, context enricher, rate limiting
  Deliverable: NOVA APIs working + tested (mocked Ollama in tests)
  Dependencies: Task 6
  Effort: 2 days
  Owner: Backend Dev

TASK 10: BUILD FRONTEND — CORE LAYER
  Goal: SPA router, API client, auth guard, global CSS, component library
  Deliverable: Frontend skeleton with routing and auth
  Dependencies: Task 2 (wireframes)
  Effort: 3 days
  Owner: Frontend Dev

TASK 11: BUILD FRONTEND — LEARNING FLOW
  Goal: Dashboard → Galaxy → Planet → Discovery → Practice → Quiz → Results
  Deliverable: All learning flow pages functional
  Dependencies: Tasks 7, 8, 10
  Effort: 5 days
  Owner: Frontend Dev

TASK 12: BUILD FRONTEND — SECONDARY PAGES
  Goal: Leaderboard, Artifact Museum, Profile, NOVA chat widget
  Deliverable: All secondary pages functional
  Dependencies: Tasks 8, 9, 10
  Effort: 3 days
  Owner: Frontend Dev

TASK 13: INTEGRATION TESTING
  Goal: End-to-end flow testing, fix bugs, polish
  Deliverable: All flows tested, bugs documented + fixed
  Dependencies: Tasks 11, 12
  Effort: 3 days
  Owner: All devs

TASK 14: DEPLOYMENT SETUP
  Goal: Production server setup, deploy script, SSL, monitoring
  Deliverable: Live MVP at algolingo.com
  Dependencies: Task 13
  Effort: 2 days
  Owner: Tech Lead

TASK 15: LAUNCH
  Goal: Soft launch to beta users, monitor, fix critical issues
  Deliverable: Public MVP launch
  Dependencies: Task 14
  Effort: Ongoing
  Owner: PM
```

### Timeline Estimate

| Phase | Tasks | Estimated Time |
|-------|-------|---------------|
| Foundation | 1-4 | 6 days (parallel) |
| Backend Core | 5-9 | 8 days |
| Frontend | 10-12 | 8 days |
| Integration | 13 | 3 days |
| Launch | 14-15 | 3 days |
| **Total** | | **~28 working days (6 weeks)** |

### Critical Path

`Task 1 → Task 2 → Task 10 → Task 11 → Task 13 → Task 14 → Task 15`

Anything on the critical path that slips will delay the launch date.

---

**END OF BLUEPRINT — Ready for Development Sprint Planning**
