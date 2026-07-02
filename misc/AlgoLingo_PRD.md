# AlgoLingo — Product Requirements Document (PRD)

**Document Version:** 1.0  
**Status:** Final Draft  
**Author:** Senior Product Manager / Software Architect  
**Date:** 2026-06-14  
**Project Type:** Educational Technology (EdTech) Gamified Learning Platform  
**Code Name:** AlgoLingo

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Product Vision & Strategy](#2-product-vision--strategy)
3. [Branding & Terminology](#3-branding--terminology)
4. [Target Audience & Personas](#4-target-audience--personas)
5. [Platform Architecture Overview](#5-platform-architecture-overview)
6. [Galaxy System & MVP Scope](#6-galaxy-system--mvp-scope)
7. [Python Nebula — Complete Design](#7-python-nebula--complete-design)
8. [Planet 1: Syntax Station](#8-planet-1-syntax-station)
9. [Planet 2: Control Flow Crater](#9-planet-2-control-flow-crater)
10. [Planet 3: Data Depot](#10-planet-3-data-depot)
11. [Remaining Python Nebula Planets (Future Phase)](#11-remaining-python-nebula-planets-future-phase)
12. [Artifact System](#12-artifact-system)
13. [Knowledge Energy (XP) System](#13-knowledge-energy-xp-system)
14. [Rank System](#14-rank-system)
15. [Leaderboard System](#15-leaderboard-system)
16. [NOVA AI System](#16-nova-ai-system)
17. [User Flow Diagrams](#17-user-flow-diagrams)
18. [Database Design (ERD & Schema)](#18-database-design-erd--schema)
19. [MVP REST API Design](#19-mvp-rest-api-design)
20. [Admin Panel — Phase 2 Roadmap](#20-admin-panel--phase-2-roadmap)
21. [UI/UX Design Guidelines](#21-uiux-design-guidelines)
22. [Technical Implementation Notes](#22-technical-implementation-notes)
23. [Glossary](#23-glossary)

---

## 1. Executive Summary

AlgoLingo is a gamified educational technology platform that teaches programming fundamentals, data structures, and algorithms through an immersive space exploration metaphor. Learners embark on a journey across galaxies (programming languages), exploring planets (topics), making discoveries (lessons), solving challenges (practice), and earning artifacts (badges) and Knowledge Energy (XP).

The MVP delivers the first galaxy — **Python Nebula** — with its first three planets fully implemented, alongside the NOVA AI assistant for contextual learning support. The platform uses a REST API architecture with Python/FastAPI backend, PostgreSQL database, and vanilla HTML/CSS/JavaScript frontend, with a local LLM (Ollama) powering the AI features.

This PRD serves as the complete blueprint for engineering, design, and QA teams to build the AlgoLingo MVP.

---

## 2. Product Vision & Strategy

### 2.1 Vision Statement

To transform the way beginners learn programming by making it feel like exploring an infinite universe — where every concept discovered is a new planet visited, every skill mastered is an artifact earned, and every learner is a Galactic Explorer.

### 2.2 Mission

Democratize programming education through gamification, structured learning paths, and AI-powered personalized guidance — making Data Structures & Algorithms accessible, engaging, and addictive to learn.

### 2.3 Product Principles

| # | Principle | Description |
|---|-----------|-------------|
| 1 | **Learn by Doing** | Every concept is immediately reinforced with practice. |
| 2 | **Gamified Progression** | Learning feels like a game with levels, ranks, and rewards. |
| 3 | **AI-First Assistance** | NOVA provides instant, contextual help at every step. |
| 4 | **Structured but Flexible** | Predefined paths with freedom to revisit and explore. |
| 5 | **Visual & Narrative** | Space exploration theme makes abstract concepts tangible. |
| 6 | **Community & Competition** | Leaderboards foster healthy competition. |
| 7 | **Zero Friction** | No setup required — everything runs in the browser. |

### 2.4 Success Metrics (MVP)

| Metric | Target (3 Months Post-Launch) |
|--------|------------------------------|
| Registered Users | 5,000 |
| Active Weekly Learners | 1,500 |
| Planet Completion Rate (Planet 1) | ≥ 60% |
| Planet Completion Rate (Planet 3) | ≥ 25% |
| Average Session Duration | ≥ 20 minutes |
| NPS Score | ≥ 40 |
| Daily Active Users (DAU) | 500 |
| NOVA Interactions per User/Session | ≥ 3 |

---

## 3. Branding & Terminology

### 3.1 Official Terminology Map

| AlgoLingo Term | Real-World Meaning | UI Label |
|----------------|-------------------|----------|
| **AlgoLingo** | The Platform | Brand Name |
| **ATLAS** | Learning Navigation System | "ATLAS Navigator" |
| **NOVA** | AI Assistant | "NOVA — Your AI Guide" |
| **Galaxy** | Programming Language | "Python Nebula", "Java Metropolis" |
| **Planet** | Topic / Module | "Syntax Station", "Data Depot" |
| **Discovery** | Lesson / Concept | "Discovery 1: Variables" |
| **Practice Challenge** | Coding Exercise | "Practice: Loop Lab" |
| **Anomaly** | Quiz Question | "Anomaly Detected!" |
| **Artifact** | Achievement / Badge | "Artifact Unlocked!" |
| **Knowledge Energy (KE)** | Experience Points (XP) | "+150 KE" |
| **Orbit** | Learning Path / Curriculum | "Planet Orbit" |
| **Warp Drive** | Skip / Fast-Track | "Warp to Next Planet" |
| **Space Dock** | User Dashboard | "Space Dock" |
| **Comm Hub** | Leaderboards | "Comm Hub" |
| **Stellar Rank** | User Level / Rank | "Cadet", "Explorer" |

### 3.2 Visual Identity Keywords

- **Colors:** Deep space blue (#0B0C2A), Nebula purple (#6C2BD9), Stellar gold (#FFD700), Energy cyan (#00F0FF), Warning red (#FF3355)
- **Typography:** Monospace for code, clean sans-serif for UI
- **Iconography:** Planets, stars, rockets, satellites, asteroids, constellations
- **Sound Design (Phase 2):** Subtle ambient space sounds on actions

### 3.3 Tone of Voice

| Channel | Tone | Example |
|---------|------|---------|
| NOVA Chat | Helpful, encouraging, slightly futuristic | "Captain, I recommend exploring Variables next. It will boost your KE by 200!" |
| Artifact Unlock | Celebratory, epic | "🌟 ARTIFACT UNLOCKED: Syntax Sage — You've mastered the ancient language of Python!" |
| Error Messages | Playful, not frustrating | "Warp drive malfunction! Check your code and try again." |
| Quiz Feedback | Constructive | "Almost through the asteroid field! Review Conditionals to strengthen your shields." |

---

## 4. Target Audience & Personas

### 4.1 Primary Audience

| Segment | Description | Motivations |
|---------|-------------|-------------|
| **College Freshmen** | CS/IT students struggling with fundamentals | Pass exams, build foundation |
| **Career Switchers** | Adults (25–35) learning to code | Job readiness, portfolio |
| **High School Coders** | Teens (14–18) exploring programming | Curiosity, fun, competitive |
| **Self-Learners** | Hobbyists, autodidacts | Personal growth, projects |

### 4.2 User Personas

**Persona 1: Arjun — The College Freshman**
- Age: 19
- Background: First-year CS student in India
- Pain Point: Lectures are theoretical; needs hands-on practice
- Behavior: Studies 30–45 min/day, motivated by grades and ranks
- Goal: Ace his Data Structures exam
- AlgoLingo Fit: Structured path + practice + leaderboard

**Persona 2: Priya — The Career Switcher**
- Age: 29
- Background: Non-STEM graduate, learning Python for data analytics
- Pain Point: Overwhelmed by too many resources
- Behavior: Studies evenings/weekends, needs guided path
- Goal: Build portfolio projects within 6 months
- AlgoLingo Fit: Discovery → Practice → Quiz pipeline + NOVA guidance

**Persona 3: Rohan — The High School Explorer**
- Age: 16
- Background: Self-taught basics, loves gaming
- Pain Point: Finds traditional tutorials boring
- Behavior: Competitive, grinds for ranks and achievements
- Goal: Leaderboard #1 in his galaxy
- AlgoLingo Fit: Gamification, artifacts, leaderboard, streaks

---

## 5. Platform Architecture Overview

### 5.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                 │
│            HTML · CSS · JavaScript (Vanilla)                        │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Landing  │  │ Dashboard│  │ ATLAS    │  │ NOVA Chat UI     │  │
│  │ Page     │  │ (Space   │  │ Explorer │  │ (WebSocket or    │  │
│  │          │  │  Dock)   │  │          │  │  REST Poll)      │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ HTTP / REST
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       API GATEWAY LAYER                             │
│                    FastAPI (Python 3.11+)                           │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Auth     │  │ Galaxy   │  │ Planet   │  │ Discovery│          │
│  │ Routes   │  │ Routes   │  │ Routes   │  │ Routes   │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Practice │  │ Quiz     │  │ Artifact │  │ NOVA     │          │
│  │ Routes   │  │ Routes   │  │ Routes   │  │ Routes   │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│  ┌──────────┐  ┌──────────┐                                       │
│  │Leaderboard│  │ Profile  │                                       │
│  │ Routes   │  │ Routes   │                                       │
│  └──────────┘  └──────────┘                                       │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                   │
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                   │
│  │ Auth       │  │ Progress   │  │ Scoring    │                   │
│  │ Service    │  │ Service    │  │ Service    │                   │
│  └────────────┘  └────────────┘  └────────────┘                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                   │
│  │ Gamific-   │  │ NOVA AI    │  │ Content    │                   │
│  │ ation Svc  │  │ Service    │  │ Service    │                   │
│  └────────────┘  └────────────┘  └────────────┘                   │
│  ┌────────────┐  ┌────────────┐                                   │
│  │ Leaderboard│  │ Streak     │                                   │
│  │ Service    │  │ Service    │                                   │
│  └────────────┘  └────────────┘                                   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                    │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │  PostgreSQL Database                                     │      │
│  │  · SQLAlchemy ORM                                        │      │
│  │  · Alembic Migrations                                    │      │
│  │  · Connection Pooling (pgbouncer in production)          │      │
│  └──────────────────────────────────────────────────────────┘      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │  Ollama (Local LLM)                                      │      │
│  │  · Model: CodeLlama / Mistral (7B quantized)             │      │
│  │  · REST API via ollama python library                    │      │
│  │  · Local inference (no external API calls)               │      │
│  └──────────────────────────────────────────────────────────┘      │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │  Redis Cache (Phase 2 — for sessions & rate limiting)    │      │
│  └──────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Tech Stack Specification

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | HTML5 | — | Structure |
| Frontend | CSS3 | — | Styling & Animations |
| Frontend | JavaScript | ES6+ | Interactivity & API calls |
| Backend | Python | 3.11+ | Application logic |
| Backend Framework | FastAPI | 0.110+ | REST API server |
| Database | PostgreSQL | 15+ | Persistent data |
| ORM | SQLAlchemy | 2.0+ | Object-relational mapping |
| Migration | Alembic | 1.13+ | Schema migrations |
| AI | Ollama | Latest | Local LLM inference |
| AI Model | CodeLlama / Mistral | 7B Q4 | Code understanding |
| ASGI Server | Uvicorn | 0.29+ | Production server |
| Auth | JWT (python-jose) | — | Token-based auth |
| Password Hashing | bcrypt (passlib) | — | Security |
| Testing | pytest | 8+ | Unit/integration tests |
| API Docs | Swagger (auto) | — | Built into FastAPI |

### 5.3 Directory Structure

```
/algolingo/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   ├── main.css
│   │   ├── components.css
│   │   ├── planets.css
│   │   ├── animations.css
│   │   └── nova.css
│   ├── js/
│   │   ├── api.js              # API client
│   │   ├── auth.js             # Auth logic
│   │   ├── router.js           # SPA routing
│   │   ├── galaxy.js           # Galaxy view
│   │   ├── planet.js           # Planet view
│   │   ├── discovery.js        # Discovery reader
│   │   ├── practice.js         # Code editor / challenges
│   │   ├── quiz.js             # Quiz engine
│   │   ├── artifacts.js        # Artifact display
│   │   ├── leaderboard.js      # Leaderboard
│   │   ├── nova.js             # NOVA chat
│   │   └── dashboard.js        # Space Dock
│   └── assets/
│       ├── images/
│       │   ├── galaxies/
│       │   ├── planets/
│       │   ├── artifacts/
│       │   ├── ui/
│       │   └── backgrounds/
│       └── sounds/             # Phase 2
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── config.py               # Environment config
│   ├── database.py             # DB connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── galaxy.py
│   │   ├── planet.py
│   │   ├── discovery.py
│   │   ├── practice.py
│   │   ├── quiz.py
│   │   ├── artifact.py
│   │   ├── leaderboard.py
│   │   └── nova.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   ├── galaxy_schema.py
│   │   ├── planet_schema.py
│   │   ├── discovery_schema.py
│   │   ├── practice_schema.py
│   │   ├── quiz_schema.py
│   │   ├── artifact_schema.py
│   │   ├── leaderboard_schema.py
│   │   └── nova_schema.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── galaxy.py
│   │   ├── planet.py
│   │   ├── discovery.py
│   │   ├── practice.py
│   │   ├── quiz.py
│   │   ├── artifact.py
│   │   ├── leaderboard.py
│   │   ├── profile.py
│   │   └── nova.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── progress_service.py
│   │   ├── scoring_service.py
│   │   ├── gamification_service.py
│   │   ├── nova_service.py
│   │   ├── content_service.py
│   │   ├── leaderboard_service.py
│   │   └── streak_service.py
│   ├── middleware/
│   │   ├── auth_middleware.py
│   │   └── error_handler.py
│   ├── utils/
│   │   ├── jwt_handler.py
│   │   ├── password_utils.py
│   │   └── helpers.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_galaxy.py
│   │   ├── test_planet.py
│   │   ├── test_discovery.py
│   │   ├── test_practice.py
│   │   ├── test_quiz.py
│   │   ├── test_artifact.py
│   │   └── test_nova.py
│   └── alembic/
│       ├── alembic.ini
│       ├── env.py
│       └── versions/
├── docker-compose.yml          # Phase 2 (containerization)
├── .env.example
└── README.md
```

---

## 6. Galaxy System & MVP Scope

### 6.1 Galaxy Overview

| Galaxy Name | Programming Language | MVP Status | Planets Count |
|-------------|---------------------|------------|---------------|
| **Python Nebula** | Python | ✅ Fully Implemented (3 of 9 planets) | 9 (3 live) |
| **Java Metropolis** | Java | 🔒 Locked (Visual Only) | 8 |
| **C Forge** | C | 🔒 Locked (Visual Only) | 7 |
| **C++ Frontier** | C++ | 🔒 Locked (Visual Only) | 8 |

### 6.2 Locked Galaxy UX

Locked galaxies display:
- Dimmed / grayscale appearance
- "WARP DRIVE UNDER CONSTRUCTION — COMING SOON" overlay
- Estimated release month (e.g., "Launching Q3 2026")
- Count of planets (teaser)
- Option to "Notify Me" (email capture — Phase 2)

### 6.3 Galaxy Unlock Conditions (Future)

| Galaxy | Unlock Condition |
|--------|-----------------|
| Python Nebula | Available at registration (free) |
| Java Metropolis | Complete Python Nebula OR purchase individually |
| C Forge | Complete Java Metropolis OR purchase individually |
| C++ Frontier | Complete C Forge OR purchase individually |

---

## 7. Python Nebula — Complete Design

### 7.1 All Python Nebula Planets (Full Roadmap)

| # | Planet Name | Topic | MVP Status | Difficulty |
|---|------------|-------|------------|------------|
| 1 | **Syntax Station** | Python Basics (Variables, Data Types, I/O) | ✅ MVP | ⭐ Beginner |
| 2 | **Control Flow Crater** | Conditionals & Loops | ✅ MVP | ⭐⭐ Beginner+ |
| 3 | **Data Depot** | Lists, Tuples, Dictionaries, Sets | ✅ MVP | ⭐⭐ Intermediate |
| 4 | **Function Forge** | Functions, Scope, Lambda | 🔒 Phase 2 | ⭐⭐⭐ Intermediate |
| 5 | **String Star** | String Manipulation & Methods | 🔒 Phase 2 | ⭐⭐ Intermediate |
| 6 | **Module Moon** | Modules, Packages, pip | 🔒 Phase 2 | ⭐⭐⭐ Intermediate |
| 7 | **File Frontier** | File I/O, Context Managers | 🔒 Phase 2 | ⭐⭐⭐ Intermediate |
| 8 | **Exception Eclipse** | Error Handling, Exceptions | 🔒 Phase 2 | ⭐⭐⭐⭐ Advanced |
| 9 | **OOP Orbit** | Classes, Objects, Inheritance | 🔒 Phase 2 | ⭐⭐⭐⭐⭐ Advanced |

### 7.2 Planet Unlock Logic

| Planet | Unlock Condition |
|--------|-----------------|
| Syntax Station | Unlocked by default (first planet) |
| Control Flow Crater | Complete Syntax Station (all Discoveries + Quiz pass) |
| Data Depot | Complete Control Flow Crater |
| Function Forge (Phase 2) | Complete Data Depot |
| ... | Sequential unlock |

### 7.3 Planet Visual Design (Per Planet)

Each planet card in the ATLAS view shows:
- **Planet Name**
- **Planet Illustration** (SVG/CSS-drawn planet with unique color and ring/moon features)
- **Completion Percentage** (progress ring)
- **Difficulty Badge** (1–5 stars)
- **Estimated Time** (e.g., "~45 min")
- **KE Reward** (e.g., "+500 KE")
- **Artifact Preview** (silhouette if locked, full image if earned)
- **Lock/Unlock Status**

---

## 8. Planet 1: Syntax Station

### 8.1 Overview

| Attribute | Value |
|-----------|-------|
| **Planet Name** | Syntax Station |
| **Tagline** | "The Launchpad of All Code" |
| **Topic** | Python Basics — Variables, Data Types, I/O, Comments |
| **Difficulty** | ⭐ Beginner |
| **Estimated Learning Time** | 45–60 minutes |
| **Total KE Available** | 1,150 XP |
| **Planet Artifact** | "Syntax Sage" (Common) |
| **Unlock Condition** | First planet — automatically available |
| **Prerequisites** | None |

### 8.2 Learning Objectives

By the end of this planet, learners will be able to:
1. Write and run their first Python program using `print()`
2. Declare and assign variables with proper naming conventions
3. Identify and use basic data types: `int`, `float`, `str`, `bool`
4. Perform type conversion between data types
5. Read user input using `input()` and display output
6. Write single-line and multi-line comments
7. Use basic string operations (concatenation, repetition, f-strings)

### 8.3 Planet Description (UI Copy)

> "Welcome to Syntax Station, cadet. This is where every space journey begins. Here, you'll learn the fundamental building blocks of Python — variables to store your fuel, data types to categorize your discoveries, and input/output to communicate with the universe. Master Syntax Station, and you'll be ready to navigate the stars."

### 8.4 Discoveries (Lessons)

#### Discovery 1.1: Your First Python Program

| Attribute | Value |
|-----------|-------|
| **Title** | Your First Python Program |
| **Description** | Learn how to write your very first Python program using the `print()` function. Understand what Python is and why it's the perfect language for space explorers. |
| **Learning Objective** | Write and execute a simple Python program that prints output to the console. |
| **Content Preview** | History of Python, installing/online interpreters, print() syntax, strings in quotes, running code |
| **Estimated Read Time** | 8 minutes |
| **Difficulty** | ⭐ Beginner |
| **Completion XP** | 75 XP |
| **Prerequisites** | None |

#### Discovery 1.2: Variables — Your Fuel Tanks

| Attribute | Value |
|-----------|-------|
| **Title** | Variables — Your Fuel Tanks |
| **Description** | Variables store data in your program, just like fuel tanks store energy for your spaceship. Learn to create, name, and use variables. |
| **Learning Objective** | Declare variables with meaningful names using proper Python naming conventions (snake_case). |
| **Content Preview** | Variable assignment (`=`), naming rules, snake_case convention, dynamic typing, reassignment |
| **Estimated Read Time** | 10 minutes |
| **Difficulty** | ⭐ Beginner |
| **Completion XP** | 100 XP |
| **Prerequisites** | Discovery 1.1 |

#### Discovery 1.3: Data Types — The Elements of Code

| Attribute | Value |
|-----------|-------|
| **Title** | Data Types — The Elements of Code |
| **Description** | Everything in Python has a type. Just like elements in the universe — integers, floats, strings, and booleans — each type has unique properties and uses. |
| **Learning Objective** | Identify and use `int`, `float`, `str`, and `bool` data types. Use `type()` to inspect types. |
| **Content Preview** | int, float, str, bool, type() function, dynamic typing, type() examples |
| **Estimated Read Time** | 12 minutes |
| **Difficulty** | ⭐ Beginner |
| **Completion XP** | 100 XP |
| **Prerequisites** | Discovery 1.2 |

#### Discovery 1.4: Type Conversion — Warping Between Types

| Attribute | Value |
|-----------|-------|
| **Title** | Type Conversion — Warping Between Types |
| **Description** | Sometimes you need to convert one data type to another — like warping from integer to string or float to integer. Learn the conversion functions that make it possible. |
| **Learning Objective** | Convert between data types using `int()`, `float()`, `str()`, and `bool()`. Handle basic conversion safely. |
| **Content Preview** | int(), float(), str(), bool(), implicit vs explicit conversion, common errors |
| **Estimated Read Time** | 10 minutes |
| **Difficulty** | ⭐ Beginner |
| **Completion XP** | 100 XP |
| **Prerequisites** | Discovery 1.3 |

#### Discovery 1.5: Input and Output — Communicating with the Universe

| Attribute | Value |
|-----------|-------|
| **Title** | Input and Output — Communicating with the Universe |
| **Description** | Programs aren't useful if they can't talk to you! Learn how to read input from the user and format your output beautifully using f-strings and the `input()` function. |
| **Learning Objective** | Read user input using `input()`, display formatted output using f-strings and `print()`. |
| **Content Preview** | input() function, string output, print() with multiple arguments, f-strings basics, escape sequences |
| **Estimated Read Time** | 12 minutes |
| **Difficulty** | ⭐ Beginner |
| **Completion XP** | 100 XP |
| **Prerequisites** | Discovery 1.3 |

#### Discovery 1.6: Comments — Leaving Star Charts

| Attribute | Value |
|-----------|-------|
| **Title** | Comments — Leaving Star Charts |
| **Description** | Comments are notes you leave in your code for yourself and others. Like star charts that guide future explorers, comments make your code understandable. |
| **Learning Objective** | Write single-line and multi-line comments. Understand best practices for commenting code. |
| **Content Preview** | `#` for single-line, `"""` for multi-line, when to comment, when not to, docstrings introduction |
| **Estimated Read Time** | 6 minutes |
| **Difficulty** | ⭐ Beginner |
| **Completion XP** | 75 XP |
| **Prerequisites** | Discovery 1.2 |

#### Discovery 1.7: String Basics — Crafting Messages

| Attribute | Value |
|-----------|-------|
| **Title** | String Basics — Crafting Messages |
| **Description** | Strings are the most common data type you'll use. Learn to create strings, combine them, repeat them, and use f-strings for clean message formatting. |
| **Learning Objective** | Perform string concatenation, repetition (`*`), and f-string formatting. |
| **Content Preview** | String creation (single/double quotes), concatenation (+), repetition (*), f-string formatting, len(), escape characters |
| **Estimated Read Time** | 10 minutes |
| **Difficulty** | ⭐ Beginner |
| **Completion XP** | 100 XP |
| **Prerequisites** | Discovery 1.3 |

### 8.5 Practice Challenges

#### Challenge 1.1: Welcome Aboard!

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Welcome Aboard! |
| **Challenge Type** | Write Output |
| **Difficulty** | ⭐ Beginner |
| **Description** | Write a Python program that prints "Welcome to AlgoLingo, Explorer!" to the console. |
| **Expected Learning Outcome** | Learner demonstrates ability to use `print()` with a string literal. |
| **XP Reward** | 50 XP |
| **Solution** | `print("Welcome to AlgoLingo, Explorer!")` |
| **Hints (NOVA)** | 1. Use the `print()` function. 2. Put your message in quotes. |

#### Challenge 1.2: Variable Voyage

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Variable Voyage |
| **Challenge Type** | Fill in the Blanks |
| **Difficulty** | ⭐ Beginner |
| **Description** | Create a variable called `ship_name` and assign it the value "Voyager". Then print it. |
| **Expected Learning Outcome** | Learner demonstrates variable declaration and usage with `print()`. |
| **XP Reward** | 50 XP |
| **Solution** | `ship_name = "Voyager"` `print(ship_name)` |
| **Hints (NOVA)** | 1. Use `=` to assign. 2. Remember quotes for strings. |

#### Challenge 1.3: Type Checker

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Type Checker |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐ Beginner |
| **Description** | Given `x = 42`, `y = 3.14`, and `z = "Hello"`, write code to print the type of each variable. |
| **Expected Learning Outcome** | Learner uses `type()` function and understands data types. |
| **XP Reward** | 75 XP |
| **Solution** | `print(type(x))` `print(type(y))` `print(type(z))` |
| **Hints (NOVA)** | 1. Use the `type()` function. 2. Pass each variable inside `type()`. |

#### Challenge 1.4: Age Calculator

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Age Calculator |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Description** | Write a program that asks the user for their age (as a string), converts it to an integer, adds 5 to it, and prints the result in the format: "In 5 years, you will be X years old." |
| **Expected Learning Outcome** | Learner combines `input()`, type conversion with `int()`, and f-strings. |
| **XP Reward** | 100 XP |
| **Solution** | `age = input("Enter your age: ")` `future_age = int(age) + 5` `print(f"In 5 years, you will be {future_age} years old.")` |
| **Hints (NOVA)** | 1. `input()` returns a string. 2. Convert with `int()`. 3. Use f-strings with `{}`. |

#### Challenge 1.5: Mission Brief Generator

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Mission Brief Generator |
| **Challenge Type** | Code Writing (Scenario) |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Description** | Create a program that: (1) asks for the user's name, (2) asks for their mission name, (3) prints a mission brief: "Captain {name}, your mission '{mission}' begins now. Good luck!" |
| **Expected Learning Outcome** | Learner combines multiple input() calls, variables, and f-strings in a practical scenario. |
| **XP Reward** | 100 XP |
| **Solution** | `name = input("Enter your name: ")` `mission = input("Enter mission name: ")` `print(f"Captain {name}, your mission '{mission}' begins now. Good luck!")` |
| **Hints (NOVA)** | 1. Use `input()` twice. 2. Store in two variables. 3. Use f-string for final output. |

### 8.6 Quiz Structure

| Attribute | Value |
|-----------|-------|
| **Quiz Name** | Syntax Station Assessment |
| **Total Questions** | 10 |
| **Question Types** | Multiple Choice (6), True/False (2), Fill in the Blank (2) |
| **Passing Criteria** | 7 out of 10 correct (70%) |
| **Time Limit** | 15 minutes |
| **XP Reward** | 200 XP (pass) / 50 XP (fail — encouragement) |
| **Artifact Reward** | "Syntax Sage" (Common) |
| **Unlock Reward** | Access to Control Flow Crater |
| **Planet Completion Reward** | 200 XP + Artifact + Planet completion badge on profile |

#### Example Quiz Questions

**Q1 (Multiple Choice):**
What will `print(type(42))` output?
- A) `<class 'str'>`
- B) `<class 'int'>` ✅
- C) `<class 'float'>`
- D) `<class 'bool'>`

**Q2 (Multiple Choice):**
Which of the following is NOT a valid variable name in Python?
- A) `my_var`
- B) `_count`
- C) `2nd_place` ✅
- D) `data_1`

**Q3 (True/False):**
The `input()` function always returns a string, even if the user types a number.
- A) True ✅
- B) False

**Q4 (Multiple Choice):**
What is the output of: `print("Hello" + " " + "World")`?
- A) HelloWorld
- B) Hello World ✅
- C) "Hello World"
- D) Error

**Q5 (Fill in the Blank):**
The function used to convert a string to an integer is `______`.
- Answer: `int()` or `int`

**Q6 (True/False):**
In Python, variable names are case-sensitive.
- A) True ✅
- B) False

**Q7 (Multiple Choice):**
Which operator is used for exponentiation (power) in Python?
- A) `^`
- B) `**` ✅
- C) `^^`
- D) `pow`

**Q8 (Multiple Choice):**
What is the correct way to create a comment in Python?
- A) `// This is a comment`
- B) `<!-- This is a comment -->`
- C) `# This is a comment` ✅
- D) `/* This is a comment */`

**Q9 (Fill in the Blank):**
To print the value of variable `x` inside an f-string, you write `f"The value is {______}"`.
- Answer: `x`

**Q10 (Multiple Choice):**
What will this code output?
```python
x = "5"
y = 3
print(x * y)
```
- A) 15
- B) "555" (or 555)
- C) "53"
- D) Error
- Correct Answer: B) `555` ✅

### 8.7 Reward Structure Summary (Syntax Station)

| Activity | XP | Other Rewards |
|----------|----|---------------|
| Discovery 1.1 | 75 | — |
| Discovery 1.2 | 100 | — |
| Discovery 1.3 | 100 | — |
| Discovery 1.4 | 100 | — |
| Discovery 1.5 | 100 | — |
| Discovery 1.6 | 75 | — |
| Discovery 1.7 | 100 | — |
| **Total Discoveries** | **650** | — |
| Challenge 1.1 | 50 | — |
| Challenge 1.2 | 50 | — |
| Challenge 1.3 | 75 | — |
| Challenge 1.4 | 100 | — |
| Challenge 1.5 | 100 | — |
| **Total Practice** | **375** | — |
| Quiz (Pass) | 200 | Syntax Sage Artifact + Planet Unlock |
| Quiz (Fail) | 50 | Encouragement message |
| **Planet Total (if passed)** | **1,150** | Syntax Sage Artifact + Control Flow Crater Unlock |

---

## 9. Planet 2: Control Flow Crater

### 9.1 Overview

| Attribute | Value |
|-----------|-------|
| **Planet Name** | Control Flow Crater |
| **Tagline** | "Where Decisions Shape Your Destiny" |
| **Topic** | Conditionals (if/elif/else) and Loops (for/while) |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Estimated Learning Time** | 60–90 minutes |
| **Total KE Available** | 1,850 XP |
| **Planet Artifact** | "Flow Master" (Common) |
| **Unlock Condition** | Complete Syntax Station (all discoveries + pass quiz) |
| **Prerequisites** | Syntax Station |

### 9.2 Learning Objectives

By the end of this planet, learners will be able to:
1. Write `if`, `elif`, and `else` conditional statements
2. Use comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`)
3. Use logical operators (`and`, `or`, `not`)
4. Write `for` loops to iterate over sequences
5. Write `while` loops with proper exit conditions
6. Use `break` and `continue` for loop control
7. Combine conditionals and loops in practical programs
8. Understand indentation and block structure

### 9.3 Planet Description (UI Copy)

> "Control Flow Crater is where your code learns to think. Here, you'll master the art of decision-making with conditionals and the power of repetition with loops. Guide your spaceship through asteroid fields of if-else branches and orbit planets with for and while loops. Navigate wisely, explorer."

### 9.4 Discoveries

#### Discovery 2.1: Decision Time — If, Elif, Else

| Attribute | Value |
|-----------|-------|
| **Title** | Decision Time — If, Elif, Else |
| **Description** | Your code needs to make decisions. Learn how `if`, `elif`, and `else` let your program choose different paths based on conditions — just like choosing a route through the stars. |
| **Learning Objective** | Write conditional statements with `if`, `elif`, and `else` to control program flow. |
| **Content Preview** | if syntax, indentation, comparison operators, elif chains, else fallback |
| **Estimated Read Time** | 14 minutes |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Completion XP** | 125 XP |
| **Prerequisites** | Syntax Station |

#### Discovery 2.2: Comparison Operators — Measuring the Stars

| Attribute | Value |
|-----------|-------|
| **Title** | Comparison Operators — Measuring the Stars |
| **Description** | How do you compare values in Python? Learn the comparison operators that let you check equality, difference, and magnitude — essential for making decisions. |
| **Learning Objective** | Use comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) to build conditions. |
| **Content Preview** | == vs =, !=, <, >, <=, >=, chaining comparisons, comparing different types |
| **Estimated Read Time** | 10 minutes |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Completion XP** | 100 XP |
| **Prerequisites** | Discovery 2.1 |

#### Discovery 2.3: Logical Operators — Connecting Conditions

| Attribute | Value |
|-----------|-------|
| **Title** | Logical Operators — Connecting Conditions |
| **Description** | Combine multiple conditions using `and`, `or`, and `not`. Like connecting navigation coordinates, logical operators help you build complex decision paths. |
| **Learning Objective** | Combine multiple conditions using `and`, `or`, `not`. Build compound boolean expressions. |
| **Content Preview** | and, or, not, truth tables, short-circuit evaluation, precedence |
| **Estimated Read Time** | 12 minutes |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Completion XP** | 125 XP |
| **Prerequisites** | Discovery 2.1 |

#### Discovery 2.4: For Loops — Orbiting Sequences

| Attribute | Value |
|-----------|-------|
| **Title** | For Loops — Orbiting Sequences |
| **Description** | Loops let you repeat actions. The `for` loop is perfect for iterating over sequences — like orbiting a planet and collecting data at each pass. |
| **Learning Objective** | Write `for` loops to iterate over strings, lists, and `range()`. |
| **Content Preview** | for syntax, iterating over strings/lists/range(), loop variables, range(start, stop, step) |
| **Estimated Read Time** | 14 minutes |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Completion XP** | 125 XP |
| **Prerequisites** | Discovery 2.1 |

#### Discovery 2.5: While Loops — Reaching Orbit

| Attribute | Value |
|-----------|-------|
| **Title** | While Loops — Reaching Orbit |
| **Description** | Sometimes you don't know how many times you need to repeat. The `while` loop runs as long as a condition is true — like firing thrusters until you reach escape velocity. |
| **Learning Objective** | Write `while` loops with proper conditions. Avoid infinite loops. |
| **Content Preview** | while syntax, condition-based repetition, sentinel values, infinite loop dangers, break statement |
| **Estimated Read Time** | 12 minutes |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Completion XP** | 125 XP |
| **Prerequisites** | Discovery 2.4 |

#### Discovery 2.6: Break and Continue — Navigating the Loop

| Attribute | Value |
|-----------|-------|
| **Title** | Break and Continue — Navigating the Loop |
| **Description** | Sometimes you need to exit a loop early or skip an iteration. `break` and `continue` are your emergency thrusters and skip drives for loop navigation. |
| **Learning Objective** | Use `break` to exit loops early and `continue` to skip iterations. |
| **Content Preview** | break statement, continue statement, nested loops, practical use cases |
| **Estimated Read Time** | 10 minutes |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Completion XP** | 100 XP |
| **Prerequisites** | Discovery 2.4, Discovery 2.5 |

### 9.5 Practice Challenges

#### Challenge 2.1: Number Classifier

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Number Classifier |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Description** | Write a program that asks the user for a number. If it's positive, print "Positive". If negative, print "Negative". If zero, print "Zero". |
| **Expected Learning Outcome** | Use if/elif/else with comparison operators. |
| **XP Reward** | 75 XP |
| **Solution** | `num = int(input("Enter a number: "))` `if num > 0:` `    print("Positive")` `elif num < 0:` `    print("Negative")` `else:` `    print("Zero")` |
| **Hints (NOVA)** | 1. Convert input to int. 2. Use if/elif/else. 3. Three cases to check. |

#### Challenge 2.2: Even or Odd Quest

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Even or Odd Quest |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Description** | Write a program that checks if a number entered by the user is even or odd. Print "Even" or "Odd" accordingly. |
| **Expected Learning Outcome** | Use the modulo operator `%` with conditionals. |
| **XP Reward** | 75 XP |
| **Solution** | `num = int(input("Enter a number: "))` `if num % 2 == 0:` `    print("Even")` `else:` `    print("Odd")` |
| **Hints (NOVA)** | 1. Use `% 2` to check remainder. 2. If remainder is 0, it's even. |

#### Challenge 2.3: Countdown Lift-Off

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Countdown Lift-Off |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Description** | Write a program that counts down from 10 to 1 using a loop, then prints "LIFT OFF!". |
| **Expected Learning Outcome** | Use a `for` loop with `range()` in reverse order. |
| **XP Reward** | 100 XP |
| **Solution** | `for i in range(10, 0, -1):` `    print(i)` `print("LIFT OFF!")` |
| **Hints (NOVA)** | 1. Use `range(10, 0, -1)`. 2. Print each number. 3. Print "LIFT OFF!" after the loop. |

#### Challenge 2.4: Password Checker

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Password Checker |
| **Challenge Type** | Code Writing (Loop + Conditional) |
| **Difficulty** | ⭐⭐⭐ Intermediate |
| **Description** | Write a program that keeps asking for a password until the correct password "algolingo123" is entered. Use a `while` loop. Print "Access Granted" when correct. Print "Wrong password, try again" when wrong. |
| **Expected Learning Outcome** | Combine `while` loop with conditional. Understand sentinel-controlled loops. |
| **XP Reward** | 125 XP |
| **Solution** | `password = ""` `while password != "algolingo123":` `    password = input("Enter password: ")` `    if password != "algolingo123":` `        print("Wrong password, try again")` `print("Access Granted")` |
| **Hints (NOVA)** | 1. Use while loop with condition. 2. Compare input to the secret password. 3. Use if inside while for feedback. |

#### Challenge 2.5: FizzBuzz Voyage

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | FizzBuzz Voyage |
| **Challenge Type** | Code Writing (Classic Algorithm) |
| **Difficulty** | ⭐⭐⭐ Intermediate |
| **Description** | Print numbers from 1 to 50. For multiples of 3, print "Fizz" instead. For multiples of 5, print "Buzz". For multiples of both, print "FizzBuzz". |
| **Expected Learning Outcome** | Combine loops, conditionals, and modulo operator in a classic programming problem. |
| **XP Reward** | 150 XP |
| **Solution** | `for i in range(1, 51):` `    if i % 3 == 0 and i % 5 == 0:` `        print("FizzBuzz")` `    elif i % 3 == 0:` `        print("Fizz")` `    elif i % 5 == 0:` `        print("Buzz")` `    else:` `        print(i)` |
| **Hints (NOVA)** | 1. Loop from 1 to 50. 2. Check divisibility by 3 and 5 first. 3. Use elif for single conditions. |

#### Challenge 2.6: Sum of Planets

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Sum of Planets |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Beginner+ |
| **Description** | Write a program that asks the user for a number `n` and then calculates the sum of all numbers from 1 to `n` using a loop. Print the sum. |
| **Expected Learning Outcome** | Use a loop with an accumulator variable. |
| **XP Reward** | 100 XP |
| **Solution** | `n = int(input("Enter a number: "))` `total = 0` `for i in range(1, n + 1):` `    total += i` `print(f"Sum is {total}")` |
| **Hints (NOVA)** | 1. Use an accumulator variable. 2. Start it at 0. 3. Add each number in the loop. |

### 9.6 Quiz Structure

| Attribute | Value |
|-----------|-------|
| **Quiz Name** | Control Flow Crater Assessment |
| **Total Questions** | 12 |
| **Question Types** | Multiple Choice (6), True/False (3), Fill in the Blank (2), Code Output (1) |
| **Passing Criteria** | 9 out of 12 correct (75%) |
| **Time Limit** | 20 minutes |
| **XP Reward** | 300 XP (pass) / 75 XP (fail) |
| **Artifact Reward** | "Flow Master" (Common) |
| **Unlock Reward** | Access to Data Depot |
| **Planet Completion Reward** | 300 XP + Flow Master Artifact + Planet completion badge |

#### Example Quiz Questions

**Q1 (Multiple Choice):**
What is the output of this code?
```python
x = 10
if x > 5:
    print("A")
elif x > 8:
    print("B")
else:
    print("C")
```
- A) A ✅
- B) B
- C) C
- D) Error

**Q2 (True/False):**
The `elif` keyword is short for "else if" and can be used multiple times in a single if-block.
- A) True ✅
- B) False

**Q3 (Multiple Choice):**
What does `range(5)` generate?
- A) 0, 1, 2, 3, 4, 5
- B) 1, 2, 3, 4, 5
- C) 0, 1, 2, 3, 4 ✅
- D) 1, 2, 3, 4

**Q4 (Fill in the Blank):**
The operator used to check if two values are equal in Python is `______`.
- Answer: `==`

**Q5 (Multiple Choice):**
Which logical operator returns True only if BOTH conditions are True?
- A) `or`
- B) `and` ✅
- C) `not`
- D) `both`

**Q6 (Code Output — Multiple Choice):**
```python
count = 0
while count < 3:
    print(count)
    count += 1
```
What is the output?
- A) 0 1 2 ✅ (or each on a new line)
- B) 1 2 3
- C) 0 1 2 3
- D) Infinite loop

**Q7 (True/False):**
A `for` loop can iterate over a string, and each iteration gives one character.
- A) True ✅
- B) False

**Q8 (Multiple Choice):**
What does `break` do inside a loop?
- A) Skips the current iteration
- B) Exits the loop immediately ✅
- C) Restarts the loop
- D) Pauses the loop

**Q9 (Fill in the Blank):**
The `______` keyword skips the rest of the current loop iteration and moves to the next iteration.
- Answer: `continue`

**Q10 (True/False):**
An `else` block is mandatory after every `if` statement.
- A) True
- B) False ✅

**Q11 (Multiple Choice):**
What is the output?
```python
for i in range(3):
    for j in range(2):
        print(i, j)
```
How many lines are printed?
- A) 3
- B) 5
- C) 6 ✅
- D) 9

**Q12 (Multiple Choice):**
Which of the following correctly checks if `age` is between 18 and 60 (inclusive)?
- A) `age >= 18 and age <= 60` ✅
- B) `age >= 18 or age <= 60`
- C) `age > 18 and age < 60`
- D) `18 <= age < 60` (also correct, but A is the safest answer for teaching)

### 9.7 Reward Structure Summary (Control Flow Crater)

| Activity | XP | Other Rewards |
|----------|----|---------------|
| Discovery 2.1 | 125 | — |
| Discovery 2.2 | 100 | — |
| Discovery 2.3 | 125 | — |
| Discovery 2.4 | 125 | — |
| Discovery 2.5 | 125 | — |
| Discovery 2.6 | 100 | — |
| **Total Discoveries** | **700** | — |
| Challenge 2.1 | 75 | — |
| Challenge 2.2 | 75 | — |
| Challenge 2.3 | 100 | — |
| Challenge 2.4 | 125 | — |
| Challenge 2.5 | 150 | — |
| Challenge 2.6 | 100 | — |
| **Total Practice** | **625** | — |
| Quiz (Pass) | 300 | Flow Master Artifact + Data Depot Unlock |
| Quiz (Fail) | 75 | Encouragement message |
| **Planet Total (if passed)** | **1,850** | Flow Master + Data Depot Unlock |

---

## 10. Planet 3: Data Depot

### 10.1 Overview

| Attribute | Value |
|-----------|-------|
| **Planet Name** | Data Depot |
| **Tagline** | "Store, Organize, Conquer" |
| **Topic** | Lists, Tuples, Dictionaries, Sets |
| **Difficulty** | ⭐⭐ Intermediate |
| **Estimated Learning Time** | 90–120 minutes |
| **Total KE Available** | 2,325 XP |
| **Planet Artifact** | "Data Hoarder" (Rare) |
| **Unlock Condition** | Complete Control Flow Crater |
| **Prerequisites** | Control Flow Crater |

### 10.2 Learning Objectives

By the end of this planet, learners will be able to:
1. Create and manipulate lists (access, modify, slice, iterate)
2. Use list methods: `append()`, `remove()`, `pop()`, `sort()`, `reverse()`
3. Create and use tuples for immutable sequences
4. Create and manipulate dictionaries (key-value pairs)
5. Use dictionary methods: `keys()`, `values()`, `items()`, `get()`
6. Create and use sets for unique collections
7. Perform set operations: union, intersection, difference
8. Choose the right data structure for a given problem

### 10.3 Planet Description (UI Copy)

> "Welcome to the Data Depot — the central hub where all information is stored, organized, and protected. Here you'll master Python's built-in data structures: lists for ordered cargo, tuples for immutable records, dictionaries for lookup tables, and sets for unique collections. A true explorer knows how to organize their data."

### 10.4 Discoveries

#### Discovery 3.1: Lists — Your Cargo Bay

| Attribute | Value |
|-----------|-------|
| **Title** | Lists — Your Cargo Bay |
| **Description** | Lists are ordered collections that can hold any type of data — like a cargo bay on your spaceship. Learn to create, index, and manipulate lists. |
| **Learning Objective** | Create lists, access elements by index, modify elements, and understand list mutability. |
| **Content Preview** | List creation with [], indexing (0-based), negative indexing, slicing, mutability, nested lists |
| **Estimated Read Time** | 14 minutes |
| **Difficulty** | ⭐⭐ Intermediate |
| **Completion XP** | 150 XP |
| **Prerequisites** | Control Flow Crater |

#### Discovery 3.2: List Methods — Cargo Operations

| Attribute | Value |
|-----------|-------|
| **Title** | List Methods — Cargo Operations |
| **Description** | Lists come with built-in methods for common operations. Learn to add, remove, sort, and search through your data cargo. |
| **Learning Objective** | Use list methods: `append()`, `extend()`, `insert()`, `remove()`, `pop()`, `index()`, `count()`, `sort()`, `reverse()`. |
| **Content Preview** | append(), extend(), insert(), remove(), pop(), index(), count(), sort(), reverse(), sorted() vs .sort() |
| **Estimated Read Time** | 14 minutes |
| **Difficulty** | ⭐⭐ Intermediate |
| **Completion XP** | 150 XP |
| **Prerequisites** | Discovery 3.1 |

#### Discovery 3.3: Tuples — Immutable Records

| Attribute | Value |
|-----------|-------|
| **Title** | Tuples — Immutable Records |
| **Description** | Tuples are like lists but immutable — once created, they can't change. Perfect for fixed data like coordinates or configuration values. |
| **Learning Objective** | Create tuples, access elements, understand immutability, and know when to use tuples vs lists. |
| **Content Preview** | Tuple creation with (), immutability, tuple unpacking, when to use tuples, single-element tuples |
| **Estimated Read Time** | 10 minutes |
| **Difficulty** | ⭐⭐ Intermediate |
| **Completion XP** | 125 XP |
| **Prerequisites** | Discovery 3.1 |

#### Discovery 3.4: Dictionaries — Your Navigation Charts

| Attribute | Value |
|-----------|-------|
| **Title** | Dictionaries — Your Navigation Charts |
| **Description** | Dictionaries store key-value pairs — like a navigation chart mapping planet names to their coordinates. Look up values instantly by their keys. |
| **Learning Objective** | Create dictionaries, access/modify values by keys, iterate over key-value pairs. |
| **Content Preview** | dict creation with {}, key-value pairs, access with [], .get(), modifying, adding, deleting with del, key uniqueness |
| **Estimated Read Time** | 14 minutes |
| **Difficulty** | ⭐⭐ Intermediate |
| **Completion XP** | 150 XP |
| **Prerequisites** | Discovery 3.1 |

#### Discovery 3.5: Dictionary Methods — Chart Tools

| Attribute | Value |
|-----------|-------|
| **Title** | Dictionary Methods — Chart Tools |
| **Description** | Dictionaries have powerful methods for accessing keys, values, and items. Learn to use them effectively for data manipulation. |
| **Learning Objective** | Use dictionary methods: `keys()`, `values()`, `items()`, `get()`, `pop()`, `update()`, `setdefault()`. |
| **Content Preview** | .keys(), .values(), .items(), .get(default), .pop(), .update(), .setdefault(), dictionary iteration, dictionary comprehension intro |
| **Estimated Read Time** | 12 minutes |
| **Difficulty** | ⭐⭐ Intermediate |
| **Completion XP** | 150 XP |
| **Prerequisites** | Discovery 3.4 |

#### Discovery 3.6: Sets — Unique Elements

| Attribute | Value |
|-----------|-------|
| **Title** | Sets — Unique Elements |
| **Description** | Sets store unique elements — no duplicates allowed! Learn to create sets and perform powerful set operations. |
| **Learning Objective** | Create sets, understand uniqueness, perform union, intersection, difference operations. |
| **Content Preview** | Set creation with {}, set() constructor, uniqueness, add(), remove(), union (|), intersection (&), difference (-), symmetric difference |
| **Estimated Read Time** | 12 minutes |
| **Difficulty** | ⭐⭐ Intermediate |
| **Completion XP** | 125 XP |
| **Prerequisites** | Discovery 3.1 |

#### Discovery 3.7: Choosing the Right Structure

| Attribute | Value |
|-----------|-------|
| **Title** | Choosing the Right Structure |
| **Description** | Now that you know all four data structures, learn when to use each one. Choosing the right structure is the mark of a true programmer. |
| **Learning Objective** | Evaluate scenarios and select the appropriate data structure (list, tuple, dict, set). |
| **Content Preview** | Comparison table, use-case analysis, performance considerations, common patterns |
| **Estimated Read Time** | 10 minutes |
| **Difficulty** | ⭐⭐ Intermediate |
| **Completion XP** | 125 XP |
| **Prerequisites** | All prior Data Depot discoveries |

### 10.5 Practice Challenges

#### Challenge 3.1: List Navigator

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | List Navigator |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Intermediate |
| **Description** | Create a list called `planets` containing "Mercury", "Venus", "Earth", "Mars". Print the third planet. Then change "Mercury" to "Sun" and print the updated list. |
| **Expected Learning Outcome** | Create, index, and modify a list. |
| **XP Reward** | 75 XP |
| **Solution** | `planets = ["Mercury", "Venus", "Earth", "Mars"]` `print(planets[2])` `planets[0] = "Sun"` `print(planets)` |
| **Hints (NOVA)** | 1. Lists use square brackets. 2. Indexing starts at 0. |

#### Challenge 3.2: Shopping List Organizer

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Shopping List Organizer |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Intermediate |
| **Description** | Start with an empty list. Use `append()` to add "Fuel", "Oxygen", "Water". Use `insert()` to add "Food" at position 1. Then use `pop()` to remove the last item. Print the final list. |
| **Expected Learning Outcome** | Use `append()`, `insert()`, and `pop()` list methods. |
| **XP Reward** | 100 XP |
| **Solution** | `items = []` `items.append("Fuel")` `items.append("Oxygen")` `items.append("Water")` `items.insert(1, "Food")` `items.pop()` `print(items)` |
| **Hints (NOVA)** | 1. Start empty. 2. append() adds to end. 3. insert(index, item) adds at position. |

#### Challenge 3.3: Coordinate Tuple

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Coordinate Tuple |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Intermediate |
| **Description** | Create a tuple `coordinates` with values (10, 20). Print both values using tuple unpacking into variables `x` and `y`. |
| **Expected Learning Outcome** | Create a tuple and use tuple unpacking. |
| **XP Reward** | 75 XP |
| **Solution** | `coordinates = (10, 20)` `x, y = coordinates` `print(x, y)` |
| **Hints (NOVA)** | 1. Tuples use parentheses. 2. Use unpacking: var1, var2 = tuple. |

#### Challenge 3.4: Planet Dictionary

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Planet Dictionary |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Intermediate |
| **Description** | Create a dictionary `planet_info` with keys: "name" -> "Mars", "diameter" -> 6779, "moons" -> 2. Print the value of "diameter". Add a new key "temperature" with value -63. Print all keys using `.keys()`. |
| **Expected Learning Outcome** | Create, access, add to, and iterate dictionary keys. |
| **XP Reward** | 125 XP |
| **Solution** | `planet_info = {"name": "Mars", "diameter": 6779, "moons": 2}` `print(planet_info["diameter"])` `planet_info["temperature"] = -63` `print(planet_info.keys())` |
| **Hints (NOVA)** | 1. Dicts use curly braces. 2. Access with [key]. 3. Add by assigning to a new key. |

#### Challenge 3.5: Unique Space Rocks

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Unique Space Rocks |
| **Challenge Type** | Code Writing |
| **Difficulty** | ⭐⭐ Intermediate |
| **Description** | Given `rocks1 = {"quartz", "feldspar", "basalt"}` and `rocks2 = {"basalt", "obsidian", "granite"}`, find and print: the union of both sets, the intersection, and the difference (rocks1 - rocks2). |
| **Expected Learning Outcome** | Perform set operations: union, intersection, difference. |
| **XP Reward** | 125 XP |
| **Solution** | `rocks1 = {"quartz", "feldspar", "basalt"}` `rocks2 = {"basalt", "obsidian", "granite"}` `print(rocks1 | rocks2)` `print(rocks1 & rocks2)` `print(rocks1 - rocks2)` |
| **Hints (NOVA)** | 1. Union uses `\|`. 2. Intersection uses `&`. 3. Difference uses `-`. |

#### Challenge 3.6: Student Grades System

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Student Grades System |
| **Challenge Type** | Code Writing (Scenario) |
| **Difficulty** | ⭐⭐⭐ Intermediate+ |
| **Description** | Create a dictionary `grades` with student names as keys and their scores (list of integers) as values. Add 3 students with 3 scores each. Then calculate and print the average score for each student. |
| **Expected Learning Outcome** | Combine dictionaries, lists, and loops in a practical data processing scenario. |
| **XP Reward** | 175 XP |
| **Solution** | `grades = {` `    "Alice": [85, 90, 78],` `    "Bob": [72, 88, 91],` `    "Charlie": [95, 93, 89]` `}` `for student, scores in grades.items():` `    avg = sum(scores) / len(scores)` `    print(f"{student}: {avg:.2f}")` |
| **Hints (NOVA)** | 1. Use .items() to iterate dict. 2. Use sum() and len() for average. 3. Use f-string for formatting. |

#### Challenge 3.7: Data Structure Selector

| Attribute | Value |
|-----------|-------|
| **Challenge Title** | Data Structure Selector |
| **Challenge Type** | Multiple Choice / Conceptual |
| **Difficulty** | ⭐⭐ Intermediate |
| **Description** | For each scenario, select the best data structure: (a) Store a collection of unique usernames. (b) Store a student's name mapped to their ID. (c) Store fixed coordinates of a star. (d) Store a to-do list in order. |
| **Expected Learning Outcome** | Choose appropriate data structure for each scenario. |
| **XP Reward** | 100 XP |
| **Solution** | (a) Set, (b) Dictionary, (c) Tuple, (d) List |
| **Hints (NOVA)** | Think about whether you need: unique? pairs? immutable? ordered? |

### 10.6 Quiz Structure

| Attribute | Value |
|-----------|-------|
| **Quiz Name** | Data Depot Assessment |
| **Total Questions** | 15 |
| **Question Types** | Multiple Choice (7), True/False (3), Fill in the Blank (2), Code Output (2), Code Error Detection (1) |
| **Passing Criteria** | 11 out of 15 correct (73%) |
| **Time Limit** | 25 minutes |
| **XP Reward** | 400 XP (pass) / 100 XP (fail) |
| **Artifact Reward** | "Data Hoarder" (Rare) |
| **Unlock Reward** | Function Forge (Phase 2 — shows "Coming Soon" message) |
| **Planet Completion Reward** | 400 XP + Data Hoarder Artifact + Planet completion badge |

#### Example Quiz Questions

**Q1 (Multiple Choice):**
What is the output?
```python
my_list = [1, 2, 3, 4, 5]
print(my_list[1:3])
```
- A) [1, 2, 3]
- B) [2, 3] ✅
- C) [2, 3, 4]
- D) [1, 2]

**Q2 (True/False):**
Tuples can be modified after creation.
- A) True
- B) False ✅

**Q3 (Multiple Choice):**
Which method adds an element to the end of a list?
- A) `add()`
- B) `insert()`
- C) `append()` ✅
- D) `extend()`

**Q4 (Fill in the Blank):**
To get the value for a key in a dictionary without getting an error if the key doesn't exist, use the `______` method.
- Answer: `get()`

**Q5 (Multiple Choice):**
What is the output?
```python
s = {1, 2, 3, 3, 2, 1}
print(len(s))
```
- A) 6
- B) 3 ✅
- C) 1
- D) Error

**Q6 (Code Output):**
```python
d = {"a": 1, "b": 2, "c": 3}
for k, v in d.items():
    print(k, v)
```
How many lines are printed?
- A) 1
- B) 2
- C) 3 ✅
- D) 6

**Q7 (True/False):**
Lists in Python can contain elements of different data types.
- A) True ✅
- B) False

**Q8 (Multiple Choice):**
What does `pop()` do to a list?
- A) Removes the first element
- B) Removes the last element and returns it ✅
- C) Removes all elements
- D) Removes a random element

**Q9 (Fill in the Blank):**
The set operation for finding elements that are in set A OR set B is called ______.
- Answer: `union` (or `|`)

**Q10 (Code Error Detection):**
```python
my_dict = {[1, 2]: "value"}
```
What is wrong with this code?
- A) Nothing, it's correct
- B) Lists cannot be dictionary keys because they are mutable ✅
- C) Values must be strings
- D) Dictionary keys must be numbers

**Q11 (Multiple Choice):**
Which of these creates a tuple with one element?
- A) `t = (1)`
- B) `t = (1,)` ✅
- C) `t = tuple`
- D) `t = [1]`

**Q12 (True/False):**
The `sort()` method returns a new sorted list without modifying the original.
- A) True
- B) False ✅ (it sorts in-place and returns None)

**Q13 (Multiple Choice):**
What is the output?
```python
a = [1, 2, 3]
b = a
b.append(4)
print(a)
```
- A) [1, 2, 3]
- B) [1, 2, 3, 4] ✅
- C) [4]
- D) Error

**Q14 (Multiple Choice):**
Which data structure would you use to count the frequency of words in a document?
- A) List
- B) Tuple
- C) Dictionary ✅
- D) Set

**Q15 (Multiple Choice):**
What does `{1, 2, 3} - {2, 3, 4}` return?
- A) {1} ✅
- B) {1, 4}
- C) {1, 2, 3, 4}
- D) {2, 3}

### 10.7 Reward Structure Summary (Data Depot)

| Activity | XP | Other Rewards |
|----------|----|---------------|
| Discovery 3.1 | 150 | — |
| Discovery 3.2 | 150 | — |
| Discovery 3.3 | 125 | — |
| Discovery 3.4 | 150 | — |
| Discovery 3.5 | 150 | — |
| Discovery 3.6 | 125 | — |
| Discovery 3.7 | 125 | — |
| **Total Discoveries** | **975** | — |
| Challenge 3.1 | 75 | — |
| Challenge 3.2 | 100 | — |
| Challenge 3.3 | 75 | — |
| Challenge 3.4 | 125 | — |
| Challenge 3.5 | 125 | — |
| Challenge 3.6 | 175 | — |
| Challenge 3.7 | 100 | — |
| **Total Practice** | **775** | — |
| Quiz (Pass) | 400 | Data Hoarder Artifact |
| Quiz (Fail) | 100 | Encouragement message |
| **Planet Total (if passed)** | **2,325** | Data Hoarder Artifact |

---

## 11. Remaining Python Nebula Planets (Future Phase)

### 11.1 Planet Inventory (All 9)

| # | Planet | Phase | Topics Covered | KE Range | Difficulty |
|---|--------|-------|----------------|----------|------------|
| 1 | Syntax Station | MVP 1 | Variables, types, I/O, comments | 1,150 | ⭐ |
| 2 | Control Flow Crater | MVP 1 | if/elif/else, loops, break/continue | 1,850 | ⭐⭐ |
| 3 | Data Depot | MVP 1 | Lists, tuples, dicts, sets | 2,325 | ⭐⭐ |
| 4 | Function Forge | Phase 2 | Functions, scope, lambda, recursion | 2,500 | ⭐⭐⭐ |
| 5 | String Star | Phase 2 | String methods, formatting, regex | 2,000 | ⭐⭐ |
| 6 | Module Moon | Phase 2 | Modules, packages, pip, virtual env | 1,800 | ⭐⭐⭐ |
| 7 | File Frontier | Phase 2 | File I/O, csv, json, context managers | 2,200 | ⭐⭐⭐ |
| 8 | Exception Eclipse | Phase 2 | try/except, finally, custom exceptions | 2,000 | ⭐⭐⭐⭐ |
| 9 | OOP Orbit | Phase 2 | Classes, objects, inheritance, polymorphism | 3,000 | ⭐⭐⭐⭐⭐ |

---

## 12. Artifact System

### 12.1 Artifact Design Principles

- Every artifact has a unique visual icon (SVG/CSS-based)
- Artifacts are displayed on the user profile as a "Trophy Room"
- Sound and animation effects on unlock (Phase 2)
- Some artifacts are hidden (discovery-based secrets)
- Artifacts boost XP earnings (percentage bonus)

### 12.2 Rarity Classification

| Rarity | Color | XP Bonus | Drop Rate / Difficulty | Count Planned |
|--------|-------|----------|----------------------|---------------|
| **Common** | Bronze / Gray | +5% XP | Easy to earn | 15 |
| **Rare** | Silver / Blue | +10% XP | Moderate effort | 10 |
| **Epic** | Gold / Purple | +20% XP | Significant challenge | 6 |
| **Legendary** | Rainbow / Red | +35% XP | Extremely difficult / hidden | 4 |

### 12.3 Complete Artifact Catalog

#### Planet Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| Syntax Sage | You've mastered the ancient language of Python syntax | Common | Complete Syntax Station quiz (pass) | +5% | Profile: Python Nebula |
| Flow Master | You command the flow of control through any program | Common | Complete Control Flow Crater quiz (pass) | +5% | Profile: Python Nebula |
| Data Hoarder | You collect and organize data like a cosmic librarian | Rare | Complete Data Depot quiz (pass) | +10% | Profile: Python Nebula |
| Function Forgemaster | You forge functions like a celestial blacksmith (Phase 2) | Rare | Complete Function Forge | +10% | Profile: Python Nebula |
| String Weaver | You weave strings into beautiful constellations (Phase 2) | Common | Complete String Star | +5% | Profile: Python Nebula |
| Module Navigator | You navigate modules across the Python universe (Phase 2) | Rare | Complete Module Moon | +10% | Profile: Python Nebula |
| File Pioneer | You explore the frontiers of file systems (Phase 2) | Rare | Complete File Frontier | +10% | Profile: Python Nebula |
| Exception Shield | You deflect errors like cosmic radiation (Phase 2) | Epic | Complete Exception Eclipse | +20% | Profile: Python Nebula |
| OOP Architect | You design object-oriented worlds (Phase 2) | Epic | Complete OOP Orbit | +20% | Profile: Python Nebula |

#### Galaxy Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| Nebula Navigator | You've explored the entire Python Nebula | Epic | Complete all Python Nebula planets (all 9) | +20% | Profile: Galaxy |
| Java Traveler | Your journey in Java Metropolis begins (Phase 3) | Common | Enter Java Metropolis | +5% | Profile: Galaxy |
| Forge Apprentice | You step into C Forge (Phase 3) | Common | Enter C Forge | +5% | Profile: Galaxy |
| Frontier Scout | You explore C++ Frontier (Phase 3) | Common | Enter C++ Frontier | +5% | Profile: Galaxy |
| Universal Explorer | You've visited every galaxy (Phase 3) | Legendary | Complete all 4 galaxies | +35% | Profile: Hall of Fame |

#### Milestone Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| First Discovery | Your first discovery completed | Common | Complete any 1 discovery | +5% | Profile: Milestones |
| Knowledge Seeker | 10 discoveries completed | Common | Complete 10 discoveries | +5% | Profile: Milestones |
| Knowledge Scholar | 50 discoveries completed | Rare | Complete 50 discoveries | +10% | Profile: Milestones |
| Knowledge Sage | 100 discoveries completed | Epic | Complete 100 discoveries | +20% | Profile: Milestones |
| First Practice | Your first practice challenge solved | Common | Solve any 1 practice challenge | +5% | Profile: Milestones |
| Challenge Rookie | 10 challenges solved | Common | Solve 10 challenges | +5% | Profile: Milestones |
| Challenge Veteran | 50 challenges solved | Rare | Solve 50 challenges | +10% | Profile: Milestones |
| Challenge Legend | 100 challenges solved | Epic | Solve 100 challenges | +20% | Profile: Milestones |
| Quiz Taker | First quiz completed | Common | Complete any 1 quiz | +5% | Profile: Milestones |
| Quiz Master | 5 quizzes passed | Rare | Pass 5 quizzes | +10% | Profile: Milestones |
| Quiz Grandmaster | All quizzes passed | Epic | Pass all available quizzes | +20% | Profile: Milestones |
| Planet Explorer | First planet completed | Common | Complete any 1 planet | +5% | Profile: Milestones |
| Planet Conqueror | 3 planets completed | Rare | Complete 3 planets | +10% | Profile: Milestones |
| Planet Dominator | All planets in a galaxy completed | Epic | Complete all planets in any galaxy | +20% | Profile: Milestones |

#### Streak Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| Consistent Cadet | 3-day learning streak | Common | Maintain 3-day login streak | +5% | Profile: Streaks |
| Weekly Warrior | 7-day learning streak | Rare | Maintain 7-day login streak | +10% | Profile: Streaks |
| Monthly Mentor | 30-day learning streak | Epic | Maintain 30-day login streak | +20% | Profile: Streaks |
| Seasoned Starfarer | 100-day learning streak | Legendary | Maintain 100-day login streak | +35% | Profile: Streaks |
| Perfect Month | Complete all daily goals for 30 days (Phase 2) | Legendary | 30-day perfect daily goal completion | +35% | Profile: Streaks |

#### Quiz Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| First Pass | Passed your first quiz | Common | Pass any quiz | +5% | Profile: Quizzes |
| Perfect Score | Achieved 100% on any quiz | Rare | Score 100% on any quiz | +10% | Profile: Quizzes |
| Speed Runner | Completed a quiz in under half the time limit with 100% | Epic | Complete any quiz in <50% time with perfect score | +20% | Profile: Quizzes |
| Flawless Galaxy | 100% on all quizzes in a galaxy | Epic | Perfect score on all quizzes in one galaxy | +20% | Profile: Quizzes |

#### Completion Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| 100% Explorer | Complete all content on one planet fully | Common | Complete 100% of a planet (all discoveries + all practice + quiz pass) | +5% | Profile: Completion |
| Galaxy Finisher | Complete an entire galaxy | Epic | Complete all planets in a galaxy | +20% | Profile: Completion |
| Syllabus Complete | Complete All Current Content | Legendary | Complete all available MVP content (3 planets fully) | +35% | Profile: Hall of Fame |

#### Leaderboard Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| Rising Star | Top 100 on global leaderboard | Common | Rank in top 100 globally | +5% | Profile: Leaderboard |
| System Notable | Top 50 on global leaderboard | Rare | Rank in top 50 globally | +10% | Profile: Leaderboard |
| Galaxy Notable | Top 10 in any galaxy | Rare | Rank in top 10 in any galaxy | +10% | Profile: Leaderboard |
| Elite Explorer | Top 10 on global leaderboard | Epic | Rank in top 10 globally | +20% | Profile: Leaderboard |
| #1 Explorer | Rank #1 on global leaderboard | Legendary | Achieve #1 global rank | +35% | Profile: Hall of Fame |
| Weekly Champion | #1 on weekly leaderboard | Epic | Rank #1 on weekly leaderboard | +20% | Profile: Leaderboard |
| Monthly Legend | #1 on monthly leaderboard | Legendary | Rank #1 on monthly leaderboard | +35% | Profile: Hall of Fame |

#### NOVA Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| Curious Mind | First question asked to NOVA | Common | Ask NOVA your first question | +5% | Profile: NOVA |
| Apprentice of NOVA | 10 questions asked to NOVA | Common | Ask NOVA 10 questions | +5% | Profile: NOVA |
| Friend of NOVA | 50 questions asked to NOVA | Rare | Ask NOVA 50 questions | +10% | Profile: NOVA |
| NOVA's Confidant | 100 questions asked to NOVA | Epic | Ask NOVA 100 questions | +20% | Profile: NOVA |
| NOVA Whisperer | Ask NOVA a question that helps you debug a practice challenge successfully on first try (Phase 2) | Rare | Solve a challenge immediately after NOVA hint | +10% | Profile: NOVA |

#### Special Hidden Artifacts

| Artifact Name | Description | Rarity | Unlock Condition | XP Bonus | Display Location |
|--------------|-------------|--------|------------------|----------|-----------------|
| The Secret Planet | You found something no one else has... | Legendary | Complete a specific secret action (e.g., complete all 3 planets in one session) | +35% | Profile: Secrets (Hidden) |
| Easter Egg Hunter | Found a hidden easter egg in the UI | Rare | Click a specific hidden element 50 times | +10% | Profile: Secrets |
| Dark Mode Discoverer | You ventured into the void | Common | Toggle dark mode 10 times (Phase 2) | +5% | Profile: Secrets |
| NOVA's Secret | NOVA told you a joke | Rare | Ask NOVA to tell you a joke | +10% | Profile: Secrets |
| The Completionist | 100% all artifacts (not including hidden) | Legendary | Earn every non-hidden artifact | +35% | Profile: Hall of Fame |
| Midnight Explorer | Learning at the edge of dawn | Rare | Complete a discovery between 12 AM and 5 AM | +10% | Profile: Secrets |

### 12.4 Artifact UI Display

```
┌──────────────────────────────────────┐
│         A R T I F A C T S            │
│                                      │
│  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │  🌟  │  │  🌟  │  │  🔒  │      │
│  │Syntax│  │ Flow │  │ Data │      │
│  │ Sage │  │Master│  │Hoardr│      │
│  │COMMON│  │COMMON│  │ RARE │      │
│  └──────┘  └──────┘  └──────┘      │
│                                      │
│  Filter: [All] [Common] [Rare]      │
│  [Epic] [Legendary] [Hidden]        │
│                                      │
│  Collected: 2/35                     │
│  Completion: 5.7%                    │
└──────────────────────────────────────┘
```

---

## 13. Knowledge Energy (XP) System

### 13.1 XP Economy Overview

AlgoLingo uses "Knowledge Energy" (KE) as its experience point system. KE measures a learner's accumulated knowledge and engagement. It determines rank, leaderboard position, and unlocks certain content.

### 13.2 What Grants XP

| Activity | Base XP | Can Be Repeated? | Notes |
|----------|---------|-----------------|-------|
| Complete a Discovery | 75–150 (varies) | No (one-time) | Each discovery pays once |
| Complete a Practice Challenge | 50–175 (varies) | No (one-time) | Each challenge pays once |
| Pass a Planet Quiz | 200–400 (varies) | No (one-time) | Fail gives reduced XP (25%) |
| Complete 100% of a Planet | +200 bonus | No (one-time) | Auto-granted on full completion |
| Complete a Galaxy | +1,000 bonus | No (one-time) | Auto-granted on full galaxy completion |
| Daily Login | +25 | Yes (once/day) | Resets at midnight UTC |
| Login Streak (Day 3) | +50 bonus | Yes (per streak reset) | 3-day consecutive login |
| Login Streak (Day 7) | +100 bonus | Yes (per streak reset) | 7-day consecutive login |
| Login Streak (Day 30) | +500 bonus | Yes (per streak reset) | 30-day consecutive login |
| Leaderboard Position (Weekly Top 10) | +200 | Yes (weekly) | Granted Monday 00:00 UTC |
| Leaderboard Position (Monthly Top 10) | +500 | Yes (monthly) | Granted 1st of month |
| Artifact Unlock (Common) | +50 bonus | No (one-time) | Bonus per artifact earned |
| Artifact Unlock (Rare) | +150 bonus | No (one-time) | Bonus per artifact earned |
| Artifact Unlock (Epic) | +500 bonus | No (one-time) | Bonus per artifact earned |
| Artifact Unlock (Legendary) | +1,500 bonus | No (one-time) | Bonus per artifact earned |

### 13.3 XP Level Progression

| Level | Level Name | XP Required (Cumulative) | XP to Next Level | Benefits |
|-------|-----------|-------------------------|-----------------|----------|
| 1 | Cadet | 0 | 500 | Basic profile access |
| 2 | Cadet | 500 | 1,000 | Unlock profile customization |
| 3 | Explorer | 1,500 | 2,000 | Unlock NOVA chat |
| 4 | Explorer | 3,500 | 3,000 | Unlock leaderboard access |
| 5 | Explorer | 6,500 | 4,000 | +5% XP artifact slot unlocked |
| 6 | Navigator | 10,500 | 5,000 | Custom avatar (Phase 2) |
| 7 | Navigator | 15,500 | 6,000 | Unlock galaxy stats |
| 8 | Navigator | 21,500 | 8,000 | +10% XP artifact slot unlocked |
| 9 | Commander | 29,500 | 10,000 | Unlock NOVA advanced features |
| 10 | Commander | 39,500 | 15,000 | Special profile badge |
| 11 | Commander | 54,500 | 20,000 | +15% XP artifact slot unlocked |
| 12 | Galactic Legend | 74,500 | — | Hall of Fame access + Lifetime badge |

### 13.4 XP Formula for Level Thresholds

The XP required for level `n` follows a quadratic curve:

```
XP_required(n) = 250 * n² - 250 * n

Where n = level number (1-based)
```

| Level (n) | XP Required for Level n | Cumulative XP |
|-----------|------------------------|---------------|
| 1 | 0 | 0 |
| 2 | 250(4-2) = 500 | 500 |
| 3 | 250(9-3) = 1,500 | 1,500 (+1,000) |
| 4 | 250(16-4) = 3,000 | 3,500 (+2,000) |
| 5 | 250(25-5) = 5,000 | 6,500 (+3,000) |
| 6 | 250(36-6) = 7,500 | 10,500 (+4,000) |
| 7 | 250(49-7) = 10,500 | 15,500 (+5,000) |
| 8 | 250(64-8) = 14,000 | 21,500 (+6,000) |
| 9 | 250(81-9) = 18,000 | 29,500 (+8,000) |
| 10 | 250(100-10) = 22,500 | 39,500 (+10,000) |
| 11 | 250(121-11) = 27,500 | 54,500 (+15,000) |
| 12 | 250(144-12) = 33,000 | 74,500 (+20,000) |

### 13.5 Rank Progression

Ranks are gated by both level and specific achievements.

| Rank | Min Level | Additional Requirement |
|------|-----------|----------------------|
| Cadet | 1 | None |
| Explorer | 3 | Complete Syntax Station |
| Navigator | 6 | Complete Control Flow Crater |
| Commander | 9 | Complete Data Depot |
| Galactic Legend | 12 | Complete ALL MVP content + Top 50 on leaderboard |

### 13.6 Balance Recommendations

1. **XP Curve:** The quadratic growth ensures early levels are fast (motivating), while later levels require sustained effort
2. **Daily Login XP (25):** Encourages daily habit without being the primary XP source
3. **Artifact XP Bonus:** Stacks multiplicatively (e.g., 3 Common artifacts = +15% total, not +5% × 3)
4. **Quiz Fail XP (25%):** High enough to not feel punishing, low enough to incentivize retrying
5. **Planet Completion Bonus (200):** Provides closure and satisfaction per planet
6. **Total MVP XP Available:** ~5,325 XP (Syntax: 1,150 + Control Flow: 1,850 + Data Depot: 2,325)
7. **Max Level in MVP:** Level 3–4 (requires ~3,500 XP, achievable by completing Syntax Station + Control Flow Crater)
8. **Daily XP Cap:** No hard cap, but content is finite (one-time completions); daily login + streaks provide small recurring XP

### 13.7 Anti-Abuse Recommendations

| Mechanism | Implementation |
|-----------|---------------|
| **Rate Limiting** | Max 50 API calls/minute per user for practice/quiz submissions |
| **Quiz Retry Cooldown** | 24-hour cooldown before retaking a passed quiz (instant retry for failed) |
| **Daily Login Validation** | Server-side timestamp check (not client-side) |
| **Practice Solution Abuse** | Solutions are stored server-side; "View Solution" counts as completion but awards only 50% XP (learner must attempt first) |
| **NOVA Spam** | Max 30 NOVA queries per hour per user |
| **Leaderboard Farming** | Only activities from the past 7 days contribute to weekly; past 30 days to monthly |
| **Concurrent Sessions** | One active session per user; new login invalidates old JWT |
| **Artifact Farming** | Artifacts can only be earned once per account |
| **Bot Detection** | Server-side validation of practice submissions (not just frontend check) |

---

## 14. Rank System

### 14.1 Ranks Overview

| Rank Name | Min XP Required | Min Level | Visual Identity | Benefits |
|-----------|----------------|-----------|-----------------|----------|
| **Cadet** | 0 | 1 | Gray uniform, basic spaceship | Access to Syntax Station |
| **Explorer** | 1,500 | 3 | Blue uniform, small ship | Access to NOVA + Leaderboard |
| **Navigator** | 10,500 | 6 | Green uniform, medium ship | Access to Galaxy Stats + 2nd artifact slot |
| **Commander** | 29,500 | 9 | Purple uniform, large ship | Access to NOVA Advanced + 3rd artifact slot |
| **Galactic Legend** | 74,500 | 12 | Gold/Rainbow uniform, flagship | Hall of Fame + Lifetime badge + Custom badge |

### 14.2 Rank Visual Identity

Each rank has:
- **Title:** Displayed on profile, next to username in leaderboard
- **Badge Icon:** Star-based (1 star = Cadet, 5 stars = Galactic Legend)
- **Profile Border Color:** Rank-specific glow effect
- **Spaceship Illustration:** Upgraded ship per rank
- **Username Color:** Rank-specific color in chat/leaderboard

### 14.3 Rank Unlock Animation

On rank up:
1. Screen flash / overlay with rank name
2. Progress ring fills with celebration
3. Sound effect (Phase 2)
4. "Promotion: You are now a [RANK]!" message
5. Confetti animation (CSS-based)

---

## 15. Leaderboard System

### 15.1 Leaderboard Types

| Leaderboard | Scope | Reset Period | Calculation | MVP Status |
|-------------|-------|-------------|-------------|------------|
| Global | All users | All-time | Total XP (all-time) | ✅ MVP |
| Weekly | All users | Weekly (Monday 00:00 UTC) | XP earned in past 7 days | ✅ MVP |
| Monthly | All users | Monthly (1st 00:00 UTC) | XP earned in past 30 days | ✅ MVP |
| Galaxy | Per galaxy | All-time | Total XP earned within a specific galaxy | ✅ MVP |
| Planet | Per planet | All-time | Total XP earned within a specific planet | ✅ MVP (basic) |
| Friends | Friends list | All-time | Friend-only ranking | 🔒 Phase 2 |

### 15.2 Ranking Calculation

```
rank_score = SUM(all XP earned from completions)

For weekly:
rank_score_weekly = SUM(XP earned in last 7 days)
  WHERE activity_timestamp >= NOW() - INTERVAL '7 days'

For monthly:
rank_score_monthly = SUM(XP earned in last 30 days)
  WHERE activity_timestamp >= NOW() - INTERVAL '30 days'

For galaxy:
rank_score_galaxy = SUM(XP earned from planets IN galaxy)
```

### 15.3 Tie-Breaking

If two users have the same XP:
1. **Tie-breaker 1:** Fewer total activities (quality over quantity)
2. **Tie-breaker 2:** Earlier registration date
3. **Tie-breaker 3:** Alphabetical by username

### 15.4 Leaderboard Display

```
┌──────────────────────────────────────────────┐
│            C O M M   H U B                    │
│                                                │
│  [Global] [Weekly] [Monthly] [Galaxy]         │
│                                                │
│  ┌─────┬──────────┬──────────┬─────────┬────┐ │
│  │ #   │ Explorer │ Rank     │ Galaxy  │ XP │ │
│  ├─────┼──────────┼──────────┼─────────┼────┤ │
│  │ 🥇  │ AstroMax │ Navigator│ Python  │5200│ │
│  │ 🥈  │ CodeNova │ Explorer │ Python  │4800│ │
│  │ 🥉  │ HexaBolt │ Explorer │ Java    │4500│ │
│  │ 4   │ PyMaster │ Cadet    │ Python  │4200│ │
│  │ 5   │ ...      │ ...      │ ...     │... │ │
│  └─────┴──────────┴──────────┴─────────┴────┘ │
│                                                │
│  🔍 [Search Explorer...]         Page 1 of 25 │
│                                                │
│  YOUR RANK: #42  │  YOUR XP: 3,250             │
└──────────────────────────────────────────────┘
```

### 15.5 Leaderboard Rewards

| Position | Weekly Reward | Monthly Reward |
|----------|--------------|----------------|
| #1 | +200 XP + "Weekly Champion" artifact | +500 XP + "Monthly Legend" artifact |
| #2–3 | +150 XP | +300 XP |
| #4–10 | +100 XP | +200 XP |
| #11–50 | +50 XP | +100 XP |
| #51–100 | +25 XP | +50 XP |

### 15.6 Leaderboard Refresh

- **Real-time:** User's own rank updates immediately on activity
- **Cached (5 min):** Full leaderboard view refreshes every 5 minutes
- **Daily reset:** Weekly leaderboard resets Monday 00:00 UTC
- **Monthly reset:** Monthly leaderboard resets 1st of month 00:00 UTC

---

## 16. NOVA AI System

### 16.1 Overview

NOVA is the AI-powered learning assistant powered by a local Ollama LLM (CodeLlama 7B or Mistral 7B, quantized Q4). NOVA provides contextual, real-time help to learners throughout their journey.

### 16.2 MVP Functionality

| Feature | Description | MVP Status |
|---------|-------------|------------|
| **Explain Concepts** | User asks a conceptual question; NOVA explains in simple terms with examples | ✅ MVP |
| **Generate Hints** | User requests a hint for a practice challenge; NOVA provides step-by-step guidance (not the solution) | ✅ MVP |
| **Debug Code** | User pastes code; NOVA identifies bugs and suggests fixes | ✅ MVP |
| **Recommend Next Topic** | Based on user progress, NOVA suggests what to learn next | ✅ MVP |
| **Generate Practice Questions** | NOVA creates additional practice problems on request | ✅ MVP |
| **Learning Recommendations** | NOVA analyzes user's weak areas and recommends review | ✅ MVP |
| **Concept Quiz** | NOVA asks the user a short question to test understanding | 🔒 Phase 2 |
| **Mentor Mode** | NOVA provides a full study plan based on user goals | 🔒 Phase 2 |

### 16.3 Prompt Flow Architecture

```
User Question
    │
    ▼
┌─────────────────────────────────────┐
│ Prompt Builder                       │
│ ──────────────────────────────────   │
│ System Prompt:                       │
│ "You are NOVA, an AI learning        │
│  assistant on AlgoLingo...           │
│  Current context: Galaxy: Python     │
│  Nebula, Planet: Syntax Station,     │
│  Discovery: Variables. User XP: 450  │
│  User Level: Cadet"                  │
│                                      │
│ User Query + Context                 │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Context Enricher                     │
│ Attaches:                            │
│ - Current planet/discovery/practice  │
│ - User's recent progress             │
│ - Available artifacts                │
│ - Previous NOVA conversation (last 5)│
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Ollama LLM (Local)                   │
│ Model: codellama:7b-q4 / mistral:7b │
│ Temperature: 0.7 (creative)         │
│ Max Tokens: 512                     │
│ Top-p: 0.9                          │
│                                      │
│ Response Generated                   │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ Response Post-Processor               │
│ - Format as Markdown                 │
│ - Ensure code blocks use ```python   │
│ - Filter inappropriate content       │
│ - Add Artifact mention if applicable │
└─────────────────────────────────────┘
    │
    ▼
User receives response in NOVA Chat UI
```

### 16.4 System Prompt Template

```
You are NOVA, an AI learning assistant on the AlgoLingo platform.
You help students learn programming through the space exploration metaphor.

Your personality: Helpful, encouraging, slightly futuristic. Call the user "Captain" or "Explorer".
Use space/star/planet metaphors when appropriate.

Current Context:
- Galaxy: {galaxy_name}
- Planet: {planet_name}
- Topic: {current_topic}
- User Level: {user_level}
- User Rank: {user_rank}
- User XP: {user_xp}
- Streak: {streak_days} days

Rules:
1. NEVER give direct answers to quiz questions. Provide hints only.
2. For practice challenges, guide step-by-step. Don't write the full solution.
3. When debugging, explain WHY the bug exists, not just the fix.
4. Keep responses concise (under 150 words for MVP).
5. If you don't know something, say "I'm still learning, Captain. Consult the ATLAS for more."
6. Encourage artifact collection and streak maintenance.
7. Format code using ```python blocks.

User Query: {user_message}
```

### 16.5 Context Flow

**Minimal context sent per request:**
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
  "conversation_history": [
    {"role": "user", "content": "What is a variable?"},
    {"role": "assistant", "content": "A variable is like a fuel tank..."}
  ],
  "user_message": "Can you explain f-strings?"
}
```

### 16.6 Data Requirements

| Data Point | Source | Used For |
|-----------|--------|----------|
| User ID | Auth token | Identifying user |
| Current context | User session / API params | Providing contextual help |
| Progress data | Progress service | Learning recommendations |
| Streak data | Streak service | Motivation & encouragement |
| Leaderboard position | Leaderboard service | Competitive motivation |
| Weak areas | Quiz/practice performance data | Targeted recommendations (Phase 2) |

### 16.7 Limitations (MVP)

| Limitation | Reason | Future Improvement |
|-----------|--------|-------------------|
| No conversation memory across sessions | Session-only context (last 5 messages) | Redis-backed conversation history (Phase 2) |
| No personalized learning path generation | MVP scope — fixed curriculum | Adaptive learning engine (Phase 2) |
| No code execution | Security & resource concerns | Sandboxed code execution (Phase 2) |
| No multi-language support | MVP in English only | i18n (Phase 2) |
| No voice interface | MVP UI is text-only | Speech-to-text (Phase 3) |
| Model knowledge cutoff ~2024 | Local LLM limitation | Fine-tuned model (Phase 2) |
| No RAG (Retrieval Augmented Generation) | Simpler MVP implementation | RAG with curriculum docs (Phase 2) |
| 512 max tokens response | Latency & cost control | Adjustable token limits (Phase 2) |

### 16.8 Future Roadmap (NOVA)

| Feature | Phase | Description |
|---------|-------|-------------|
| Persistent conversation memory | Phase 2 | Redis-backed multi-session memory |
| Adaptive learning recommendations | Phase 2 | ML-based weak-spot analysis |
| Code execution sandbox | Phase 2 | Run user code in Docker sandbox, return output |
| Fine-tuned model | Phase 2 | Fine-tune on AlgoLingo curriculum data |
| RAG-based answers | Phase 2 | Retrieve relevant curriculum content for grounding |
| Voice interface | Phase 3 | Text-to-speech and speech-to-text |
| Multi-model support | Phase 3 | Claude/GPT fallback for complex queries |
| NOVA Mentor Mode | Phase 3 | Full study plan generation |

---

## 17. User Flow Diagrams

### 17.1 Complete User Journey (Text Flowchart)

```
                     ┌──────────────────┐
                     │   LANDING PAGE   │
                     │  algolingo.com   │
                     └────────┬─────────┘
                              │
                    ┌─────────▼──────────┐
                    │  [Login]  [Register]│
                    └─────────┬──────────┘
                              │
                 ┌────────────▼─────────────┐
                 │        REGISTER          │
                 │  ┌────────────────────┐  │
                 │  │ Username           │  │
                 │  │ Email              │  │
                 │  │ Password           │  │
                 │  │ Confirm Password   │  │
                 │  │ Accept Terms ☐     │  │
                 │  │ [Create Account]   │  │
                 │  └────────────────────┘  │
                 └────────────┬─────────────┘
                              │
                 ┌────────────▼─────────────┐
                 │   EMAIL VERIFICATION     │
                 │  (MVP: Optional/Simplified│
                 │   — skip for now)         │
                 └────────────┬─────────────┘
                              │
                 ┌────────────▼─────────────┐
                 │      ONBOARDING          │
                 │  ┌────────────────────┐  │
                 │  │ "Welcome, Cadet!   │  │
                 │  │  Your journey      │  │
                 │  │  begins..."        │  │
                 │  │                    │  │
                 │  │ Quick tutorial:    │  │
                 │  │ ┌──┐ ┌──┐ ┌──┐    │  │
                 │  │ │1 │ │2 │ │3 │    │  │
                 │  │ └──┘ └──┘ └──┘    │  │
                 │  │ Galaxies Planets NOVA│
                 │  └────────────────────┘  │
                 │  [Begin Exploration]     │
                 └────────────┬─────────────┘
                              │
                 ┌────────────▼─────────────┐
                 │     SPACE DOCK           │
                 │     (DASHBOARD)          │
                 │                          │
                 │  ┌────────────────────┐  │
                 │  │ Your Rank: Cadet   │  │
                 │  │ Your XP: 0         │  │
                 │  │ Streak: 0 days     │  │
                 │  │                    │  │
                 │  │ ⭐ Quick Actions:  │  │
                 │  │ [Continue Learning]│  │
                 │  │ [ATLAS Explorer]   │  │
                 │  │ [NOVA Assistant]   │  │
                 │  │ [Comm Hub]         │  │
                 │  │ [Profile]          │  │
                 │  └────────────────────┘  │
                 │                          │
                 │  ┌────────────────────┐  │
                 │  │ Active Planets:    │  │
                 │  │ Syntax Station     │  │
                 │  │  [■■□□□□□□□□] 17% │  │
                 │  └────────────────────┘  │
                 └────────────┬─────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
   │  ATLAS        │  │  NOVA Chat    │  │  Comm Hub     │
   │  EXPLORER     │  │               │  │  Leaderboard  │
   │               │  │ Minimized     │  │               │
   │ Galaxy View   │  │ widget        │  │ Global/Weekly │
   │               │  │               │  │ Monthly       │
   │ 4 Galaxies    │  │ "Ask NOVA     │  │               │
   │ displayed     │  │  anything..." │  │ User's rank   │
   │               │  │               │  │ highlighted   │
   │ Python Nebula │  └───────────────┘  └───────────────┘
   │ ✅ Unlocked   │
   │ Others 🔒     │
   └───────┬───────┘
           │ (Click Python Nebula)
           ▼
   ┌───────────────────────────────────────┐
   │        GALAXY VIEW                    │
   │        Python Nebula                  │
   │                                       │
   │  ┌──────┐ ┌──────┐ ┌──────┐          │
   │  │🪐Syntx│ │🪐Ctrl │ │🪐Data │          │
   │  │Station│ │ Flow │ │Depot │          │
   │  │UNLOCK │ │🔒    │ │🔒    │          │
   │  │ 97%   │ │ LOCK │ │ LOCK │          │
   │  └──────┘ └──────┘ └──────┘          │
   │                                       │
   │  ┌──────┐ ┌──────┐ ┌──────┐          │
   │  │🪐Func │ │🪐Str  │ │🪐Mod  │          │
   │  │ Forge │ │ Star │ │ Moon │          │
   │  │ 🔒    │ │ 🔒   │ │ 🔒   │          │
   │  └──────┘ └──────┘ └──────┘          │
   │                                       │
   │  ┌──────┐ ┌──────┐ ┌──────┐          │
   │  │🪐File │ │🪐Excep│ │🪐OOP  │          │
   │  │Frontr │ │Eclip │ │Orbit │          │
   │  │ 🔒    │ │ 🔒   │ │ 🔒   │          │
   │  └──────┘ └──────┘ └──────┘          │
   │                                       │
   │  Galaxy Progress: 11%                 │
   │  [Back to Space Dock]                │
   └───────────────────┬───────────────────┘
                       │ (Click Syntax Station)
                       ▼
   ┌───────────────────────────────────────────┐
   │         PLANET VIEW                        │
   │         Syntax Station                     │
   │                                            │
   │  ┌─────────────────────────────────────┐  │
   │  │ Planet Stats                        │  │
   │  │ Difficulty: ⭐                      │  │
   │  │ Time: ~45-60 min                    │  │
   │  │ KE Available: 1,150                 │  │
   │  │ Artifact: Syntax Sage 🏆            │  │
   │  │ Progress: 3/7 Discoveries ███░░░░░ │  │
   │  └─────────────────────────────────────┘  │
   │                                            │
   │  DISCOVERIES:                              │
   │  ├── ✅ 1.1 Your First Python Program      │
   │  ├── ✅ 1.2 Variables                      │
   │  ├── 📖 1.3 Data Types (ACTIVE)            │
   │  ├── 🔒 1.4 Type Conversion                │
   │  ├── 🔒 1.5 Input/Output                   │
   │  ├── 🔒 1.6 Comments                       │
   │  └── 🔒 1.7 String Basics                  │
   │                                            │
   │  PRACTICES:                                │
   │  ├── ✅ 1.1 Welcome Aboard!                │
   │  ├── ✅ 1.2 Variable Voyage                │
   │  ├── 🔒 1.3 Type Checker                   │
   │  └── 🔒 1.4+ (locked)                      │
   │                                            │
   │  QUIZ: 🔒 Complete all discoveries         │
   │                                            │
   │  [Back to Galaxy] [Ask NOVA]               │
   └───────────────────┬───────────────────────┘
                       │ (Click Discovery 1.3)
                       ▼
   ┌───────────────────────────────────────────────┐
   │           DISCOVERY VIEW                       │
   │           Data Types — The Elements of Code     │
   │                                                │
   │  ┌─────────────────────────────────────────┐  │
   │  │ 📘 Content (rendered Markdown)          │  │
   │  │                                          │  │
   │  │ In Python, everything has a type...      │  │
   │  │                                          │  │
   │  │ ```python                                │  │
   │  │ x = 42          # int                    │  │
   │  │ y = 3.14        # float                  │  │
   │  │ name = "NOVA"   # str                    │  │
   │  │ is_ready = True  # bool                  │  │
   │  │ ```                                      │  │
   │  │                                          │  │
   │  │  ... (more content)                      │  │
   │  └─────────────────────────────────────────┘  │
   │                                                │
   │  ⏱ Read time: 12 min                          │
   │  🏆 XP: 100 KE                                │
   │                                                │
   │  [Mark as Complete] [Ask NOVA] [Back]          │
   └───────────────────┬───────────────────────────┘
                       │ (Click "Mark as Complete")
                       ▼
   ┌───────────────────────────────────────────────┐
   │  ✅ Discovery Complete!                        │
   │  +100 KE                                      │
   │  [Continue to Next Discovery]                 │
   │  [Back to Planet View]                        │
   └───────────────────┬───────────────────────────┘
                       │
                       ▼ (After all discoveries done)
   ┌───────────────────────────────────────────────────┐
   │         PRACTICE CHALLENGE VIEW                     │
   │         Challenge 1.4: Age Calculator               │
   │                                                     │
   │  ┌─────────────────────────────────────────────┐  │
   │  │ 📝 Write a program that asks for age,       │  │
   │  │ converts to int, adds 5, and prints:        │  │
   │  │ "In 5 years, you will be X years old."       │  │
   │  │                                              │  │
   │  │ ┌──────────────────────────────────────┐    │  │
   │  │ │ # Your code here                     │    │  │
   │  │ │                                      │    │  │
   │  │ │                                      │    │  │
   │  │ │                                      │    │  │
   │  │ └──────────────────────────────────────┘    │  │
   │  │                                              │  │
   │  │ [Run Code] [Submit] [Get Hint] [View Sol]   │  │
   │  └─────────────────────────────────────────────┘  │
   │                                                     │
   │  XP: 100 KE | Difficulty: ⭐⭐                      │
   └───────────────────┬─────────────────────────────────┘
                       │ (Click Submit -> Server validation)
                       ▼
        ┌──────────────────────────────┐
        │  ✅ Correct! +100 KE         │
        │  🎉 "Excellent work!"        │
        │  [Next Challenge] [Back]     │
        └──────────────┬───────────────┘
                       │
                       ▼ (All challenges done -> Quiz available)
   ┌───────────────────────────────────────────────┐
   │              QUIZ VIEW                         │
   │              Syntax Station Assessment          │
   │                                                │
   │  ⏱ Time: 15:00                                 │
   │  📊 Q1 of 10                                    │
   │                                                │
   │  ┌─────────────────────────────────────────┐  │
   │  │ What will print(type(42)) output?       │  │
   │  │                                          │  │
   │  │ ○ <class 'str'>                          │  │
   │  │ ● <class 'int'>                          │  │
   │  │ ○ <class 'float'>                        │  │
   │  │ ○ <class 'bool'>                         │  │
   │  │                                          │  │
   │  │            [Next →]                      │  │
   │  └─────────────────────────────────────────┘  │
   │                                                │
   │  Progress: ██░░░░░░░░ 10%                       │
   └───────────────────┬───────────────────────────┘
                       │ (After Q10)
                       ▼
        ┌──────────────────────────────────────┐
        │        QUIZ RESULTS                   │
        │                                        │
        │  🎉 You Passed!                       │
        │  Score: 8/10 (80%)                    │
        │                                        │
        │  +200 KE                               │
        │                                        │
        │  🏆 ARTIFACT UNLOCKED:                │
        │     Syntax Sage [Common]               │
        │     +5% XP bonus applied               │
        │                                        │
        │  🔓 Control Flow Crater UNLOCKED!      │
        │                                        │
        │  [View Artifact] [Continue to           │
        │   Control Flow Crater] [Back to         │
        │   Space Dock]                          │
        └────────────────────────────────────────┘
```

### 17.2 NOVA Chat Flow

```
NOVA Chat Widget (persistent across all views)
─────────────────────────────────────────────────

User: What's a variable?
        │
        ▼
  ┌─────────────────────────────────┐
  │ NOVA: "Captain, a variable is  │
  │ like a fuel tank on your ship. │
  │ It stores data so you can use  │
  │ it later. For example:         │
  │                                │
  │ ```python                     │
  │ fuel = 100                    │
  │ print(fuel) # Outputs 100     │
  │ ```                           │
  │                                │
  │ Ready to explore more? Ask    │
  │ me about data types next!"     │
  └─────────────────────────────────┘
        │
User: Give me a hint for challenge 1.4
        │
        ▼
  ┌─────────────────────────────────┐
  │ NOVA: "For the Age Calculator: │
  │ 1. Use input() to get age      │
  │ 2. Convert with int()          │
  │ 3. Add 5 to the converted val  │
  │ 4. Use f-string to display     │
  │                                │
  │ Try it step by step! 🚀"       │
  └─────────────────────────────────┘
```

### 17.3 Quiz Retry Flow

```
Quiz Failed (5/10 = 50%)
        │
        ▼
┌────────────────────────────────────┐
│ Quiz Results: Did Not Pass         │
│ Score: 5/10 (50%)                  │
│ Passing: 70%                       │
│                                    │
│ +50 KE (encouragement XP)          │
│                                    │
│ 📋 Review Incorrect Answers:       │
│ Q2: You answered B, correct was C  │
│ Q5: You answered False, correct T  │
│ ...                                │
│                                    │
│ [Retry Quiz] [Review Planet]       │
│ [Ask NOVA for Help]                │
└────────────────────────────────────┘
        │
        ▼
  (24-hour cooldown for retry)
  (NOVA can help review concepts)
```

---

## 18. Database Design (ERD & Schema)

### 18.1 Entity-Relationship Diagram (Text)

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   users     │1──N▸│ user_progress    │N◄──1│    planets       │
│─────────────│     │──────────────────│     │──────────────────│
│ id (PK)     │     │ id (PK)          │     │ id (PK)          │
│ username    │     │ user_id (FK)     │     │ galaxy_id (FK)   │
│ email       │     │ planet_id (FK)   │     │ name             │
│ password_hash│    │ discovery_ids[]  │     │ tagline          │
│ xp          │     │ practice_ids[]   │     │ description      │
│ level       │     │ quiz_passed      │     │ difficulty       │
│ rank        │     │ quiz_score       │     │ order            │
│ streak_days │     │ completed        │     │ xp_total         │
│ last_login  │     │ xp_earned        │     │ artifact_id (FK) │
│ created_at  │     │ started_at       │     │ is_locked        │
│ updated_at  │     │ completed_at     │     │ unlock_condition │
└──────┬──────┘     └──────────────────┘     └────────┬─────────┘
       │                                               │
       │                                              N│
       │1                                              │
       │     ┌──────────────────┐     ┌────────────────┘
       │     │  discoveries     │     │
       │     │──────────────────│     │
       │     │ id (PK)          │◄─── N│
       │     │ planet_id (FK)   │     │
       │     │ title            │     │
       │     │ description      │     │
       │     │ content_md       │     │
       │     │ learning_objective│    │
       │     │ read_time        │     │
       │     │ difficulty       │     │
       │     │ xp_reward        │     │
       │     │ order            │     │
       │     │ prerequisites[]  │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │  practice_challenges   │
       │     │──────────────────│     │
       │     │ id (PK)          │◄─── N│
       │     │ planet_id (FK)   │     │
       │     │ title            │     │
       │     │ type             │     │
       │     │ difficulty       │     │
       │     │ description      │     │
       │     │ learning_outcome │     │
       │     │ xp_reward        │     │
       │     │ solution         │     │
       │     │ hints[]          │     │
       │     │ order            │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │  quiz_questions   │     │
       │     │──────────────────│     │
       │     │ id (PK)          │◄─── N│
       │     │ planet_id (FK)   │     │
       │     │ question_text    │     │
       │     │ question_type    │     │
       │     │ options[]        │     │
       │     │ correct_answer   │     │
       │     │ explanation      │     │
       │     │ order            │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │ quiz_attempts    │     │
       │     │──────────────────│     │
       │     │ id (PK)          │     │
       │     │ user_id (FK)     │     │
       │   ──│ planet_id (FK)   │     │
       │     │ score            │     │
       │     │ total_questions  │     │
       │     │ answers[]        │     │
       │     │ passed           │     │
       │     │ xp_earned        │     │
       │     │ attempted_at     │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │  galaxies        │     │
       │     │──────────────────│     │
       │     │ id (PK)          │     │
       │     │ name             │     │
       │     │ description      │     │
       │     │ programming_lang │     │
       │     │ order            │     │
       │     │ is_locked        │     │
       │     │ icon_url         │     │
       │     │ created_at       │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │  artifacts       │     │
       │     │──────────────────│     │
       │     │ id (PK)          │     │
       │     │ name             │     │
       │     │ description      │     │
       │     │ rarity           │     │
       │     │ xp_bonus         │     │
       │     │ unlock_condition │     │
       │     │ icon_url         │     │
       │     │ category         │     │
       │     │ is_hidden        │     │
       │     │ created_at       │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │ user_artifacts   │     │
       │     │──────────────────│     │
       │     │ id (PK)          │     │
       │     │ user_id (FK)     │     │
       │     │ artifact_id (FK) │     │
       │     │ unlocked_at      │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │ daily_logins     │     │
       │     │──────────────────│     │
       │     │ id (PK)          │     │
       │     │ user_id (FK)     │     │
       │     │ login_date       │     │
       │     │ xp_earned        │     │
       │     │ streak_day       │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │  nova_interactions     │
       │     │──────────────────│     │
       │     │ id (PK)          │     │
       │     │ user_id (FK)     │     │
       │     │ user_message     │     │
       │     │ nova_response    │     │
       │     │ context_data     │     │
       │     │ created_at       │     │
       │     └──────────────────┘     │
       │                              │
       │     ┌──────────────────┐     │
       │     │ leaderboard_snapshots  │
       │     │──────────────────│     │
       │     │ id (PK)          │     │
       │     │ leaderboard_type │     │
       │     │ user_rankings[]  │     │
       │     │ snapshot_date    │     │
       │     └──────────────────┘     │
```

### 18.2 Complete Table Definitions

#### Table: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, DEFAULT gen_random_uuid() | Unique user identifier |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Display name |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Login email |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hash |
| xp | INTEGER | NOT NULL, DEFAULT 0 | Total Knowledge Energy |
| level | INTEGER | NOT NULL, DEFAULT 1 | Current level |
| rank | VARCHAR(50) | NOT NULL, DEFAULT 'Cadet' | Current rank |
| streak_days | INTEGER | NOT NULL, DEFAULT 0 | Consecutive login days |
| last_login_date | DATE | | Last login date (for streak) |
| avatar_url | VARCHAR(255) | | Profile avatar |
| bio | TEXT | | Short bio |
| is_active | BOOLEAN | DEFAULT true | Account active |
| is_verified | BOOLEAN | DEFAULT false | Email verified |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update |

**Indexes:**
- `idx_users_email` on `email`
- `idx_users_username` on `username`
- `idx_users_xp` on `xp` DESC (for leaderboard)

**Constraints:**
- `CHECK (xp >= 0)`
- `CHECK (level >= 1)`
- `CHECK (streak_days >= 0)`

#### Table: `galaxies`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique galaxy identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Galaxy name (e.g., "Python Nebula") |
| description | TEXT | NOT NULL | Galaxy description |
| programming_language | VARCHAR(50) | NOT NULL | e.g., "Python" |
| order_number | INTEGER | UNIQUE, NOT NULL | Display order |
| is_locked | BOOLEAN | DEFAULT true | Locked/unlocked |
| unlock_condition | TEXT | | How to unlock (null if free) |
| icon_url | VARCHAR(255) | | Galaxy icon |
| color_theme | VARCHAR(50) | | CSS color class |
| planets_count | INTEGER | DEFAULT 0 | Total planets in galaxy |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_galaxies_order` on `order_number`

#### Table: `planets`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique planet identifier |
| galaxy_id | UUID | FK → galaxies.id, NOT NULL | Parent galaxy |
| name | VARCHAR(100) | NOT NULL | Planet name |
| tagline | VARCHAR(200) | | Short tagline |
| description | TEXT | | Planet description |
| difficulty | INTEGER | NOT NULL, DEFAULT 1 | 1–5 star difficulty |
| order_number | INTEGER | NOT NULL | Display order within galaxy |
| xp_total | INTEGER | NOT NULL | Total XP available on planet |
| estimated_time | INTEGER | | Time in minutes |
| is_locked | BOOLEAN | DEFAULT true | Locked/unlocked |
| unlock_condition | TEXT | | How to unlock |
| artifact_id | UUID | FK → artifacts.id | Planet completion artifact |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_planets_galaxy` on `galaxy_id`
- `idx_planets_order` on `galaxy_id, order_number`
- `UNIQUE (galaxy_id, order_number)`

**Constraints:**
- `CHECK (difficulty BETWEEN 1 AND 5)`
- `CHECK (xp_total >= 0)`

#### Table: `discoveries`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique discovery identifier |
| planet_id | UUID | FK → planets.id, NOT NULL | Parent planet |
| title | VARCHAR(200) | NOT NULL | Discovery title |
| description | TEXT | | Short description |
| content_md | TEXT | NOT NULL | Full content in Markdown |
| learning_objective | TEXT | | What user will learn |
| read_time | INTEGER | | Estimated reading time (minutes) |
| difficulty | INTEGER | DEFAULT 1 | 1–5 difficulty |
| xp_reward | INTEGER | NOT NULL | XP on completion |
| order_number | INTEGER | NOT NULL | Display order |
| prerequisites | JSONB | DEFAULT '[]' | Array of discovery IDs required |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_discoveries_planet` on `planet_id`
- `idx_discoveries_order` on `planet_id, order_number`

#### Table: `practice_challenges`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique challenge identifier |
| planet_id | UUID | FK → planets.id, NOT NULL | Parent planet |
| title | VARCHAR(200) | NOT NULL | Challenge title |
| challenge_type | VARCHAR(50) | NOT NULL | 'write_output', 'fill_blanks', 'code_writing', 'scenario', 'mcq_conceptual' |
| difficulty | INTEGER | DEFAULT 1 | 1–5 |
| description | TEXT | NOT NULL | Challenge description/prompt |
| learning_outcome | TEXT | | Expected outcome |
| xp_reward | INTEGER | NOT NULL | XP on completion |
| solution_code | TEXT | | Reference solution |
| hints | JSONB | DEFAULT '[]' | Array of hint strings |
| order_number | INTEGER | NOT NULL | Display order |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_practice_planet` on `planet_id`
- `idx_practice_order` on `planet_id, order_number`

#### Table: `quiz_questions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique question identifier |
| planet_id | UUID | FK → planets.id, NOT NULL | Parent planet |
| question_text | TEXT | NOT NULL | The question |
| question_type | VARCHAR(50) | NOT NULL | 'multiple_choice', 'true_false', 'fill_blank', 'code_output', 'error_detection' |
| options | JSONB | | Array of option objects for MC |
| correct_answer | TEXT | NOT NULL | Correct answer(s) |
| explanation | TEXT | | Explanation of correct answer |
| difficulty | INTEGER | DEFAULT 1 | 1–5 |
| order_number | INTEGER | NOT NULL | Display order |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_quiz_planet` on `planet_id`
- `idx_quiz_order` on `planet_id, order_number`

#### Table: `quiz_attempts`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique attempt identifier |
| user_id | UUID | FK → users.id, NOT NULL | User |
| planet_id | UUID | FK → planets.id, NOT NULL | Planet quiz |
| score | INTEGER | NOT NULL | Correct answers count |
| total_questions | INTEGER | NOT NULL | Total questions |
| answers | JSONB | | Array of {question_id, answer, correct} |
| passed | BOOLEAN | NOT NULL | Passed or failed |
| xp_earned | INTEGER | NOT NULL | XP awarded |
| attempted_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_quiz_attempts_user` on `user_id`
- `idx_quiz_attempts_planet` on `planet_id`
- `idx_quiz_attempts_recent` on `user_id, planet_id, attempted_at DESC`

#### Table: `user_progress`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique progress record |
| user_id | UUID | FK → users.id, NOT NULL | User |
| planet_id | UUID | FK → planets.id, NOT NULL | Planet |
| completed_discoveries | JSONB | DEFAULT '[]' | Array of discovery IDs completed |
| completed_practices | JSONB | DEFAULT '[]' | Array of practice IDs completed |
| quiz_passed | BOOLEAN | DEFAULT false | Quiz passed |
| quiz_best_score | INTEGER | | Best quiz score |
| completed | BOOLEAN | DEFAULT false | Planet fully completed |
| xp_earned | INTEGER | DEFAULT 0 | Total XP from this planet |
| started_at | TIMESTAMP | DEFAULT NOW() | When started |
| completed_at | TIMESTAMP | | When completed |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |

**Indexes:**
- `idx_progress_user_planet` UNIQUE on `(user_id, planet_id)`
- `idx_progress_user` on `user_id`

#### Table: `artifacts`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | Unique artifact identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Artifact name |
| description | TEXT | | Description |
| rarity | VARCHAR(20) | NOT NULL | 'Common', 'Rare', 'Epic', 'Legendary' |
| xp_bonus_percent | INTEGER | DEFAULT 5 | XP bonus percentage |
| unlock_condition | TEXT | | How to unlock (description) |
| icon_url | VARCHAR(255) | | Artifact icon |
| category | VARCHAR(50) | NOT NULL | 'planet', 'galaxy', 'milestone', 'streak', 'quiz', 'completion', 'leaderboard', 'nova', 'hidden' |
| is_hidden | BOOLEAN | DEFAULT false | Hidden artifact |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_artifacts_rarity` on `rarity`
- `idx_artifacts_category` on `category`

#### Table: `user_artifacts`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| artifact_id | UUID | FK → artifacts.id, NOT NULL | |
| unlocked_at | TIMESTAMP | DEFAULT NOW() | When unlocked |

**Indexes:**
- `idx_user_artifacts` UNIQUE on `(user_id, artifact_id)`
- `idx_user_artifacts_user` on `user_id`

#### Table: `daily_logins`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| login_date | DATE | NOT NULL | |
| xp_earned | INTEGER | DEFAULT 25 | XP from login |
| streak_day | INTEGER | NOT NULL | Current streak count |
| daily_goal_completed | BOOLEAN | DEFAULT false | Phase 2 |

**Indexes:**
- `idx_daily_logins_user_date` UNIQUE on `(user_id, login_date)`
- `idx_daily_logins_user` on `user_id`

#### Table: `nova_interactions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| user_id | UUID | FK → users.id, NOT NULL | |
| user_message | TEXT | NOT NULL | User's question |
| nova_response | TEXT | NOT NULL | NOVA's answer |
| context_data | JSONB | | Galaxy/planet/discovery context |
| session_id | VARCHAR(100) | | For conversation grouping |
| created_at | TIMESTAMP | DEFAULT NOW() | |

**Indexes:**
- `idx_nova_user` on `user_id`
- `idx_nova_session` on `session_id`
- `idx_nova_created` on `created_at`

#### Table: `leaderboard_snapshots`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK | |
| leaderboard_type | VARCHAR(20) | NOT NULL | 'global', 'weekly', 'monthly', 'galaxy' |
| galaxy_id | UUID | FK → galaxies.id (nullable) | For galaxy-specific |
| user_rankings | JSONB | NOT NULL | Array of {user_id, rank, xp, username} |
| snapshot_date | TIMESTAMP | NOT NULL | When snapshot taken |
| valid_from | TIMESTAMP | | Period start |
| valid_to | TIMESTAMP | | Period end |

**Indexes:**
- `idx_leaderboard_type_date` on `leaderboard_type, snapshot_date DESC`

### 18.3 Future Expansion Notes

1. **User Roles:** Add `roles` table for admin/instructor/student (Phase 2)
2. **Comments/Discussions:** Add `discovery_comments` table for social learning (Phase 2)
3. **Code Submissions:** Add `code_submissions` table for persisted practice attempts (Phase 2)
4. **Friend System:** Add `friends` table with user_id, friend_id, status (Phase 2)
5. **Notifications:** Add `notifications` table (Phase 2)
6. **Content Versioning:** Add version columns to discoveries and practices (Phase 2)
7. **Payment/Subscription:** Add `subscriptions` table for premium content (Phase 3)
8. **Multi-language content:** Add `locale` column to content tables (Phase 2)

---

## 19. MVP REST API Design

### 19.1 API Conventions

- **Base URL:** `/api/v1`
- **Format:** JSON request/response
- **Authentication:** JWT Bearer token in `Authorization` header
- **Pagination:** `?page=1&limit=20` pattern
- **Error Format:**
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Planet not found",
    "details": {}
  }
}
```

### 19.2 Authentication APIs

#### POST `/api/v1/auth/register`

| Field | Details |
|-------|---------|
| **Description** | Register a new user account |
| **Auth Required** | No |
| **Rate Limit** | 5 requests/IP/minute |

**Request Body:**
```json
{
  "username": "astromax",
  "email": "astro@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid",
    "username": "astromax",
    "email": "astro@example.com",
    "xp": 0,
    "level": 1,
    "rank": "Cadet",
    "created_at": "2026-06-14T10:00:00Z"
  },
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

**Validation Rules:**
- Username: 3–50 chars, alphanumeric + underscore
- Email: Valid email format
- Password: Min 8 chars, 1 uppercase, 1 number
- Username + Email must be unique

#### POST `/api/v1/auth/login`

| Field | Details |
|-------|---------|
| **Description** | Authenticate and receive JWT |
| **Auth Required** | No |
| **Rate Limit** | 10 requests/IP/minute |

**Request Body:**
```json
{
  "email": "astro@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid",
    "username": "astromax",
    "email": "astro@example.com",
    "xp": 1250,
    "level": 3,
    "rank": "Explorer",
    "streak_days": 5
  },
  "access_token": "eyJhbG...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### POST `/api/v1/auth/refresh`

| Field | Details |
|-------|---------|
| **Description** | Refresh JWT token |
| **Auth Required** | Yes (valid token) |

**Request Body:**
```json
{
  "refresh_token": "eyJhbG..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

#### GET `/api/v1/auth/me`

| Field | Details |
|-------|---------|
| **Description** | Get current user profile |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "id": "uuid",
  "username": "astromax",
  "email": "astro@example.com",
  "xp": 1250,
  "level": 3,
  "rank": "Explorer",
  "streak_days": 5,
  "bio": "Learning Python to explore the stars!",
  "avatar_url": "/assets/avatars/default.png",
  "created_at": "2026-06-10T10:00:00Z"
}
```

### 19.3 Galaxy APIs

#### GET `/api/v1/galaxies`

| Field | Details |
|-------|---------|
| **Description** | List all galaxies with status |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "galaxies": [
    {
      "id": "uuid",
      "name": "Python Nebula",
      "description": "The vibrant nebula of Python programming...",
      "programming_language": "Python",
      "order": 1,
      "is_locked": false,
      "icon_url": "/assets/galaxies/python-nebula.svg",
      "planets_count": 9,
      "completed_planets": 1,
      "total_planets": 3,
      "color_theme": "purple"
    },
    {
      "id": "uuid",
      "name": "Java Metropolis",
      "description": "The structured metropolis of Java...",
      "programming_language": "Java",
      "order": 2,
      "is_locked": true,
      "icon_url": "/assets/galaxies/java-metropolis.svg",
      "planets_count": 8,
      "completed_planets": 0,
      "total_planets": 0,
      "color_theme": "blue",
      "estimated_release": "Q3 2026"
    }
  ]
}
```

#### GET `/api/v1/galaxies/{galaxy_id}`

| Field | Details |
|-------|---------|
| **Description** | Get galaxy details including planets |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "id": "uuid",
  "name": "Python Nebula",
  "description": "...",
  "programming_language": "Python",
  "order": 1,
  "is_locked": false,
  "planets": [
    {
      "id": "uuid",
      "name": "Syntax Station",
      "tagline": "The Launchpad of All Code",
      "difficulty": 1,
      "order": 1,
      "is_locked": false,
      "is_completed": false,
      "progress_percent": 65,
      "xp_earned": 750,
      "xp_total": 1150,
      "estimated_time": 45,
      "artifact": {
        "id": "uuid",
        "name": "Syntax Sage",
        "rarity": "Common",
        "is_earned": false
      }
    }
  ]
}
```

### 19.4 Planet APIs

#### GET `/api/v1/planets/{planet_id}`

| Field | Details |
|-------|---------|
| **Description** | Get full planet details |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "id": "uuid",
  "galaxy_id": "uuid",
  "name": "Syntax Station",
  "tagline": "The Launchpad of All Code",
  "description": "Welcome to Syntax Station...",
  "difficulty": 1,
  "order": 1,
  "xp_total": 1150,
  "xp_earned": 750,
  "estimated_time": 45,
  "is_locked": false,
  "is_completed": false,
  "discoveries": [
    {
      "id": "uuid",
      "title": "Your First Python Program",
      "description": "Learn to write your first program...",
      "read_time": 8,
      "difficulty": 1,
      "xp_reward": 75,
      "order": 1,
      "is_completed": true,
      "is_locked": false
    }
  ],
  "practices": [
    {
      "id": "uuid",
      "title": "Welcome Aboard!",
      "challenge_type": "write_output",
      "difficulty": 1,
      "xp_reward": 50,
      "order": 1,
      "is_completed": true,
      "is_locked": false
    }
  ],
  "quiz": {
    "total_questions": 10,
    "passing_score": 70,
    "time_limit_minutes": 15,
    "xp_reward_pass": 200,
    "xp_reward_fail": 50,
    "is_available": true,
    "best_score": null,
    "best_result": null
  },
  "artifact": {
    "id": "uuid",
    "name": "Syntax Sage",
    "rarity": "Common",
    "description": "You've mastered the ancient language of Python syntax!",
    "is_earned": false
  }
}
```

### 19.5 Discovery APIs

#### GET `/api/v1/discoveries/{discovery_id}`

| Field | Details |
|-------|---------|
| **Description** | Get discovery content |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "id": "uuid",
  "planet_id": "uuid",
  "title": "Data Types — The Elements of Code",
  "description": "Everything in Python has a type...",
  "content_md": "# Data Types\n\nIn Python, everything...\n\n```python\nx = 42\nprint(type(x))\n```",
  "learning_objective": "Identify and use int, float, str, and bool data types",
  "read_time": 12,
  "difficulty": 1,
  "xp_reward": 100,
  "order": 3,
  "is_completed": false,
  "prerequisites": ["discovery_id_1", "discovery_id_2"]
}
```

#### POST `/api/v1/discoveries/{discovery_id}/complete`

| Field | Details |
|-------|---------|
| **Description** | Mark discovery as complete |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "success": true,
  "xp_earned": 100,
  "total_xp": 850,
  "new_artifact": null,
  "next_discovery_id": "uuid"
}
```

### 19.6 Practice APIs

#### GET `/api/v1/practices/{practice_id}`

| Field | Details |
|-------|---------|
| **Description** | Get practice challenge |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "id": "uuid",
  "planet_id": "uuid",
  "title": "Age Calculator",
  "challenge_type": "code_writing",
  "description": "Write a program that asks the user for their age...",
  "difficulty": 2,
  "xp_reward": 100,
  "learning_outcome": "Combine input(), type conversion, and f-strings",
  "is_completed": false,
  "hints": [
    "1. input() returns a string",
    "2. Convert with int()",
    "3. Use f-strings with {}"
  ]
}
```

#### POST `/api/v1/practices/{practice_id}/submit`

| Field | Details |
|-------|---------|
| **Description** | Submit practice solution |
| **Auth Required** | Yes |

**Request Body:**
```json
{
  "code": "age = input(...)\nfuture_age = int(age) + 5\nprint(...)",
  "language": "python"
}
```

**Response (200):**
```json
{
  "success": true,
  "is_correct": true,
  "xp_earned": 100,
  "feedback": "Excellent! You correctly used input(), int(), and f-strings.",
  "expected_output": "In 5 years, you will be 25 years old.",
  "actual_output": "In 5 years, you will be 25 years old.",
  "solution_available": true
}
```

**Response (200 — Incorrect):**
```json
{
  "success": true,
  "is_correct": false,
  "xp_earned": 0,
  "feedback": "Almost there! Check that you're converting the input to int before adding.",
  "expected_output": "In 5 years, you will be 25 years old.",
  "actual_output": "In 5 years, you will be 2525 years old.",
  "solution_available": false
}
```

#### GET `/api/v1/practices/{practice_id}/solution`

| Field | Details |
|-------|---------|
| **Description** | Get reference solution (after attempt) |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "solution_code": "age = input(\"Enter your age: \")\nfuture_age = int(age) + 5\nprint(f\"In 5 years, you will be {future_age} years old.\")",
  "explanation": "This solution uses input() to read the age...",
  "xp_if_viewed_without_attempt": 50
}
```

### 19.7 Quiz APIs

#### GET `/api/v1/planets/{planet_id}/quiz`

| Field | Details |
|-------|---------|
| **Description** | Get quiz questions for a planet |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "planet_id": "uuid",
  "quiz_id": "quiz_uuid",
  "total_questions": 10,
  "time_limit_minutes": 15,
  "questions": [
    {
      "id": "uuid",
      "question_text": "What will print(type(42)) output?",
      "question_type": "multiple_choice",
      "options": [
        {"id": "a", "text": "<class 'str'>"},
        {"id": "b", "text": "<class 'int'>"},
        {"id": "c", "text": "<class 'float'>"},
        {"id": "d", "text": "<class 'bool'>"}
      ],
      "order": 1
    }
  ]
}
```

#### POST `/api/v1/planets/{planet_id}/quiz/submit`

| Field | Details |
|-------|---------|
| **Description** | Submit quiz answers |
| **Auth Required** | Yes |

**Request Body:**
```json
{
  "answers": [
    {"question_id": "uuid", "answer": "b"},
    {"question_id": "uuid", "answer": "a"},
    {"question_id": "uuid", "answer": "int()"}
  ]
}
```

**Response (200):**
```json
{
  "success": true,
  "score": 8,
  "total_questions": 10,
  "percentage": 80,
  "passed": true,
  "xp_earned": 200,
  "artifacts_earned": [
    {
      "id": "uuid",
      "name": "Syntax Sage",
      "rarity": "Common",
      "icon_url": "/assets/artifacts/syntax-sage.svg"
    }
  ],
  "unlocks": [
    {"type": "planet", "id": "uuid", "name": "Control Flow Crater"}
  ],
  "results": [
    {"question_id": "uuid", "user_answer": "b", "correct_answer": "b", "is_correct": true, "explanation": "type(42) returns <class 'int'>"},
    {"question_id": "uuid", "user_answer": "a", "correct_answer": "c", "is_correct": false, "explanation": "The correct answer is <class 'float'>..."}
  ]
}
```

### 19.8 Profile APIs

#### GET `/api/v1/profile/{username}`

| Field | Details |
|-------|---------|
| **Description** | Get user profile (public) |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "username": "astromax",
  "rank": "Explorer",
  "level": 3,
  "xp": 1250,
  "streak_days": 5,
  "bio": "Learning Python...",
  "avatar_url": "/assets/avatars/default.png",
  "planet_completions": 1,
  "artifacts_count": 3,
  "total_artifacts": 35,
  "galaxies_progress": [
    {"name": "Python Nebula", "progress": 11}
  ],
  "recent_artifacts": [
    {"name": "Syntax Sage", "rarity": "Common", "unlocked_at": "2026-06-14T10:00:00Z"}
  ]
}
```

#### PATCH `/api/v1/profile/me`

| Field | Details |
|-------|---------|
| **Description** | Update own profile |
| **Auth Required** | Yes |

**Request Body:**
```json
{
  "bio": "New bio here",
  "avatar_url": "/assets/avatars/custom.png"
}
```

**Response (200):** Updated user object

### 19.9 Leaderboard APIs

#### GET `/api/v1/leaderboard?type=global&page=1&limit=20`

| Field | Details |
|-------|---------|
| **Description** | Get leaderboard |
| **Auth Required** | Yes |
| **Query Params** | `type`: global|weekly|monthly|galaxy, `galaxy_id` (for galaxy type), `page`, `limit` |

**Response (200):**
```json
{
  "leaderboard_type": "global",
  "total_users": 1520,
  "page": 1,
  "limit": 20,
  "entries": [
    {
      "rank": 1,
      "username": "astromax",
      "xp": 5200,
      "level": 6,
      "rank_title": "Navigator",
      "avatar_url": "/assets/avatars/astromax.png",
      "planet_completions": 3
    }
  ],
  "current_user": {
    "rank": 42,
    "username": "current_user",
    "xp": 3250,
    "level": 4,
    "rank_title": "Explorer"
  }
}
```

### 19.10 Artifact APIs

#### GET `/api/v1/artifacts`

| Field | Details |
|-------|---------|
| **Description** | List all artifacts (user's status) |
| **Auth Required** | Yes |

**Query Params:** `rarity`, `category`, `earned` (boolean)

**Response (200):**
```json
{
  "artifacts": [
    {
      "id": "uuid",
      "name": "Syntax Sage",
      "description": "You've mastered the ancient language of Python syntax!",
      "rarity": "Common",
      "category": "planet",
      "xp_bonus_percent": 5,
      "icon_url": "/assets/artifacts/syntax-sage.svg",
      "is_earned": true,
      "unlocked_at": "2026-06-14T10:00:00Z"
    }
  ],
  "total_earned": 3,
  "total_available": 35,
  "active_xp_bonus": 15
}
```

#### GET `/api/v1/artifacts/{artifact_id}`

| Field | Details |
|-------|---------|
| **Description** | Get artifact details |
| **Auth Required** | Yes |

#### GET `/api/v1/users/{user_id}/artifacts`

| Field | Details |
|-------|---------|
| **Description** | Get another user's earned artifacts |
| **Auth Required** | Yes |

### 19.11 NOVA APIs

#### POST `/api/v1/nova/ask`

| Field | Details |
|-------|---------|
| **Description** | Ask NOVA a question |
| **Auth Required** | Yes |
| **Rate Limit** | 30 requests/hour/user |

**Request Body:**
```json
{
  "message": "Can you explain f-strings?",
  "context": {
    "galaxy_id": "uuid",
    "planet_id": "uuid",
    "discovery_id": "uuid|null",
    "practice_id": "uuid|null"
  }
}
```

**Response (200):**
```json
{
  "response": "Captain, f-strings are like advanced communication...\n\n```python\nname = \"NOVA\"\nprint(f\"Hello, {name}!\")\n```\n\nThey let you embed variables directly in strings using `{}`!",
  "context_used": {
    "galaxy": "Python Nebula",
    "planet": "Syntax Station"
  },
  "suggestions": [
    "What are placeholders in f-strings?",
    "How do I format numbers with f-strings?"
  ],
  "can_ask_more": true,
  "remaining_quota": 28
}
```

#### POST `/api/v1/nova/hint/{practice_id}`

| Field | Details |
|-------|---------|
| **Description** | Request a hint for a practice |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "hint": "For the Age Calculator: Start by using input() to capture the user's age. Remember, input() returns a string!"
}
```

#### POST `/api/v1/nova/debug`

| Field | Details |
|-------|---------|
| **Description** | Ask NOVA to debug code |
| **Auth Required** | Yes |

**Request Body:**
```json
{
  "code": "print(\"Hello World\"",
  "language": "python",
  "context": {}
}
```

**Response (200):**
```json
{
  "issues": [
    {
      "line": 1,
      "column": 22,
      "message": "Missing closing parenthesis ')'",
      "severity": "error"
    }
  ],
  "fixed_code": "print(\"Hello World\")",
  "explanation": "You forgot to close the parenthesis after the string. Every opening ( needs a matching )."
}
```

#### POST `/api/v1/nova/recommend`

| Field | Details |
|-------|---------|
| **Description** | Get learning recommendations |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "recommendations": [
    {
      "type": "next_planet",
      "id": "uuid",
      "name": "Control Flow Crater",
      "reason": "You've mastered Syntax Station! Time to learn conditionals and loops."
    },
    {
      "type": "review",
      "topic": "Type Conversion",
      "reason": "Your quiz performance suggests you could strengthen this area."
    },
    {
      "type": "new_challenge",
      "reason": "Try the 'FizzBuzz Voyage' challenge on Control Flow Crater to test your loop skills!"
    }
  ]
}
```

### 19.12 Progress & Stats APIs

#### GET `/api/v1/dashboard`

| Field | Details |
|-------|---------|
| **Description** | Get user dashboard data |
| **Auth Required** | Yes |

**Response (200):**
```json
{
  "user": {
    "username": "astromax",
    "xp": 1250,
    "level": 3,
    "rank": "Explorer",
    "streak_days": 5,
    "next_level_xp": 1500
  },
  "quick_actions": {
    "continue_planet": {
      "id": "uuid",
      "name": "Syntax Station",
      "next_discovery": "Type Conversion",
      "progress_percent": 65
    }
  },
  "active_planets": [
    {"id": "uuid", "name": "Syntax Station", "progress": 65, "galaxy": "Python Nebula"}
  ],
  "recent_activity": [
    {"type": "discovery_complete", "text": "Completed 'Variables'", "timestamp": "2026-06-14T09:00:00Z", "xp": 100}
  ],
  "daily_xp": 275,
  "streak_milestone": "5 days — Next: 7 days (+100 XP bonus!)"
}
```

### 19.13 API Error Codes

| HTTP Status | Code | Description |
|-------------|------|-------------|
| 400 | BAD_REQUEST | Invalid input |
| 401 | UNAUTHORIZED | Missing/invalid JWT |
| 403 | FORBIDDEN | Access to locked content |
| 404 | NOT_FOUND | Resource not found |
| 409 | CONFLICT | Duplicate resource (e.g., email) |
| 422 | UNPROCESSABLE | Validation failed |
| 429 | RATE_LIMITED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |

---

## 20. Admin Panel — Phase 2 Roadmap

### 20.1 Purpose

An administrative interface for content managers to create, edit, and manage learning content without direct database access.

### 20.2 Features (Phase 2)

| Feature | Description |
|---------|-------------|
| **Dashboard** | Platform-wide stats: total users, active users, completion rates, average XP |
| **User Management** | View, search, suspend users; view progress details |
| **Galaxy Management** | Create/edit galaxies, set order and lock status |
| **Planet Management** | Create/edit planets in galaxies, set difficulty, XP, unlock conditions |
| **Discovery Editor** | Rich Markdown editor for discovery content, preview, set prerequisites |
| **Practice Manager** | Create/edit practice challenges, set solution, hints, validation logic |
| **Quiz Builder** | Create/edit quiz questions, set correct answers, explanations, question types |
| **Artifact Manager** | Create/edit artifacts, assign to planets/milestones |
| **Content Analytics** | Which content has highest/lowest completion, hardest quiz questions |
| **Bulk Import** | CSV/JSON import for content (Phase 2+) |

### 20.3 Non-Goals (MVP)

- No admin panel in MVP
- All content will be seeded via database migrations (Alembic seed scripts)
- Content changes in MVP require direct database updates or new deployment

---

## 21. UI/UX Design Guidelines

### 21.1 Design System (CSS Variables)

```css
:root {
  /* Space Theme Colors */
  --space-deep: #0B0C2A;
  --space-dark: #111238;
  --space-medium: #1A1B4B;
  --space-light: #2A2B6B;

  --nebula-purple: #6C2BD9;
  --nebula-purple-light: #8B5CF6;
  --nebula-purple-dark: #4C1D95;

  --stellar-gold: #FFD700;
  --stellar-gold-light: #FFED4A;

  --energy-cyan: #00F0FF;
  --energy-cyan-dark: #00B8C9;

  --warning-red: #FF3355;
  --success-green: #00E676;

  /* Text */
  --text-primary: #FFFFFF;
  --text-secondary: #B0B0C0;
  --text-muted: #6B6B80;

  /* Rarity Colors */
  --rarity-common: #B0B0C0;
  --rarity-rare: #4A90D9;
  --rarity-epic: #9B59B6;
  --rarity-legendary: #FF6B35;

  /* Typography */
  --font-ui: 'Segoe UI', system-ui, -apple-system, sans-serif;
  --font-code: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

  /* Sizing */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;
  --radius-xl: 24px;

  /* Animations */
  --transition-fast: 150ms ease;
  --transition-normal: 300ms ease;
  --transition-slow: 500ms ease;
}
```

### 21.2 Layout Structure

```
┌──────────────────────────────────────────────┐
│  HEADER                                       │
│  ┌──────┐  ┌─────┐ ┌────┐ ┌────┐ ┌──────┐  │
│  │ Logo │  │ATLAS│ │NOVA│ │Comm│ │Profile│  │
│  └──────┘  └─────┘ └────┘ └────┘ └──────┘  │
├──────────────────────────────────────────────┤
│                                              │
│           MAIN CONTENT AREA                   │
│           (Dynamic SPA View)                  │
│                                              │
│                                              │
│                                              │
│                                              │
├──────────────────────────────────────────────┤
│  FOOTER (Minimal)                             │
│  About · Terms · Privacy · v1.0.0            │
└──────────────────────────────────────────────┘

┌────────┐
│ NOVA   │  ← Floating chat widget (bottom-right)
│ Chat   │
└────────┘
```

### 21.3 Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| Mobile | < 640px | Single column, hamburger menu |
| Tablet | 640–1024px | Two-column, side nav |
| Desktop | > 1024px | Full layout with NOVA sidebar |

### 21.4 Animation Guidelines

- **Page transitions:** 300ms ease fade + slide
- **Artifact unlock:** Confetti burst (CSS keyframes), 2s duration
- **XP gain:** Floating "+100 KE" text that rises and fades over 1.5s
- **Planet hover:** Subtle scale(1.05) + glow effect
- **NOVA typing:** Animated dots (...) with 500ms pulse
- **Quiz timer:** Color shift from green → yellow → red as time decreases
- **Progress rings:** SVG circle stroke-dasharray animation, 1s ease-out

---

## 22. Technical Implementation Notes

### 22.1 Code Validation for Practice Challenges

**MVP Approach:** Server-side output comparison.

The user's code is sent to the backend, which:
1. Sanitizes the code (blocks dangerous imports like `os`, `subprocess`, `sys`)
2. Executes the code in a restricted Python environment (Phase 1: `exec()` with limited globals; Phase 2: Docker sandbox)
3. Captures stdout
4. Compares output to expected output
5. Returns correct/incorrect with feedback

**Dangerous patterns to block:**
```python
# Blocked
import os; os.system("rm -rf /")
import subprocess
import sys; sys.exit()
eval(input())
open("/etc/passwd")
__import__('os')
```

### 22.2 JWT Token Configuration

```python
# config.py
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # 256-bit random
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30
```

### 22.3 Rate Limiting (MVP — Simple)

```python
# middleware/rate_limit.py
# Uses in-memory dict (Redis in Phase 2)
RATE_LIMITS = {
    "/api/v1/auth/login": (10, 60),          # 10 per minute
    "/api/v1/auth/register": (5, 60),        # 5 per minute
    "/api/v1/nova/ask": (30, 3600),          # 30 per hour
    "/api/v1/practices/*/submit": (50, 60),  # 50 per minute
    "default": (100, 60)                     # 100 per minute default
}
```

### 22.4 Database Seeding (MVP Content)

All MVP content (galaxies, planets, discoveries, practices, quizzes, artifacts) will be seeded via Alembic migration scripts using SQLAlchemy inserts.

```python
# alembic/versions/xxxx_seed_mvp_content.py
def upgrade():
    # Insert Python Nebula
    # Insert Syntax Station planet
    # Insert 7 discoveries
    # Insert 5 practice challenges
    # Insert 10 quiz questions
    # Insert Syntax Sage artifact
    # Insert Control Flow Crater planet
    # ... etc
```

### 22.5 CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 22.6 Environment Variables

```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/algolingo
JWT_SECRET_KEY=your-256-bit-secret
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=codellama:7b-q4
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=*
```

---

## 23. Glossary

| Term | Definition |
|------|------------|
| **ATLAS** | AlgoLingo's learning navigation system |
| **NOVA** | AI-powered learning assistant |
| **Galaxy** | A programming language (e.g., Python Nebula) |
| **Planet** | A topic/module within a galaxy |
| **Discovery** | A lesson/concept page |
| **Practice Challenge** | A coding exercise to reinforce learning |
| **Anomaly** | A quiz question |
| **Artifact** | An achievement badge with XP bonus |
| **Knowledge Energy (KE)** | Experience points |
| **Space Dock** | User dashboard |
| **Comm Hub** | Leaderboard area |
| **Orbit** | Learning path for a planet |
| **Warp Drive** | Skip/fast-track option |
| **Stellar Rank** | User rank (Cadet → Galactic Legend) |
| **Ollama** | Local LLM server running CodeLlama/Mistral |
| **MVP** | Minimum Viable Product |
| **PRD** | Product Requirements Document |
| **ERD** | Entity Relationship Diagram |
| **JWT** | JSON Web Token (authentication) |
| **ORM** | Object-Relational Mapping (SQLAlchemy) |
| **REST** | Representational State Transfer (API architecture) |

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-14 | Senior PM / Architect | Initial complete PRD |

---

**END OF DOCUMENT — AlgoLingo MVP PRD v1.0**
