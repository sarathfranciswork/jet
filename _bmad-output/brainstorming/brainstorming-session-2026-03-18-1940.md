---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: []
session_topic: 'Complete rebranding of Plane to Jet — total rebrand across all layers with zero remaining Plane references'
session_goals: 'Identify every rebrand touchpoint, generate new brand identity ideas, plan asset creation, ensure zero Plane references remain'
selected_approach: 'ai-recommended'
techniques_used: ['Morphological Analysis', 'Cross-Pollination', 'Constraint Mapping']
ideas_generated: 125
context_file: 'docs/index.md'
session_active: false
workflow_completed: true
facilitation_notes: 'User was decisive and action-oriented. Preferred AI-driven recommendations over exploratory discussion. Fast-paced session with clear goals. Zero ambiguity in scope — total rebrand, no exceptions.'
---

# Brainstorming Session Results

**Facilitator:** Franc
**Date:** 2026-03-18

## Session Overview

**Topic:** Complete rebranding of the Plane project management tool to "Jet" — covering every layer of the codebase, all assets, all configurations, all references both user-facing and internal. ZERO references to Plane should remain after completion.

**Goals:**
- Total elimination of all Plane references (code, configs, comments, docs, assets, metadata)
- New brand identity: logo, icons, favicon, images, color scheme, typography
- Consistency across all 5 parts: web, space, apiserver, packages, infrastructure
- Non-user-facing areas included: Django internals, Docker image names, CI/CD, email templates, env vars, database references

### Context Guidance

_Brownfield project: Plane v0.13.2, monorepo with Next.js frontends (web, space), Django REST API backend, shared TypeScript packages, Docker/Nginx infrastructure. Project documentation available at docs/index.md._

### Session Setup

_Complete rebrand session — the scope is exhaustive and covers every touchpoint in the application stack._

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Complete rebrand Plane → Jet with focus on exhaustive coverage + creative identity

**Recommended Techniques:**

- **Morphological Analysis:** Systematically map every rebrand dimension to ensure zero missed references
- **Cross-Pollination:** Draw brand identity inspiration from aviation, speed, and successful rebrands
- **Constraint Mapping:** Identify technical dependencies and prioritize execution sequence

**AI Rationale:** A total rebrand requires both exhaustive systematic analysis (nothing missed) and creative identity generation (new brand must feel distinct, not just renamed). The three-phase approach ensures coverage, creativity, and feasibility.

## Technique Execution Results

### Morphological Analysis

**Interactive Focus:** Systematically mapped every rebrand dimension across 13 categories
**Key Breakthroughs:** Identified 125 distinct touchpoints across code, assets, config, integrations, data, docs, and edge cases
**Energy Level:** High — user was decisive and action-oriented, preferred AI-driven exploration

### Cross-Pollination

**Building on Previous:** Used mapped dimensions to generate creative brand identity options
**New Insights:** "Jet Black" Vercel-inspired aesthetic, Chevron "J" favicon-friendly logo mark, "Jet Fuel" gradient brand identity, jet trail loading animation as branded micro-interaction
**Developed Ideas:** 4 logo concepts, 4 color palettes, 2 illustration styles, brand voice/personality concepts

### Constraint Mapping

**Building on Previous:** Converted morphological map + brand concepts into feasible execution plan
**New Insights:** Critical path dependencies (assets before code, backend before frontend, code before infra), in-flight Celery task naming issue at deploy time, Django content type data migration requirement, automated import replacement script necessity
**Developed Ideas:** 7-phase execution plan with parallel workstreams

### Creative Facilitation Narrative

_This was a focused, high-velocity brainstorming session. Franc came in with absolute clarity on the goal — zero references to Plane, total rebrand to Jet, no exceptions. The session moved quickly from systematic mapping through creative identity generation to execution planning. The most valuable technique was Morphological Analysis, which ensured exhaustive coverage across 13 dimensions. Cross-Pollination yielded strong brand identity options, with "Jet Black" (Vercel-inspired) and the Chevron "J" mark emerging as standout concepts. Constraint Mapping revealed non-obvious dependencies like Django content type migrations and in-flight Celery task handling._

## Idea Organization and Prioritization

### Thematic Organization (125 ideas across 8 themes)

**Theme 1: Code & Module Renaming** (16 ideas)
Core identifier renaming across Python, TypeScript, Docker, and config:
- Python module `plane/` → `jet/` (225 files, all imports)
- npm packages `@plane/*` → `@jet/*` (5 packages)
- Docker images/services `plane-*` → `jet-*`
- Django settings, WSGI, ASGI, Celery module paths
- Gunicorn, Procfile, test file imports
- TypeScript path aliases, package.json names

**Theme 2: Visual Identity & Brand Assets** (18 ideas)
New logo, colors, icons, illustrations, and visual language:
- Logo concepts: Jet Stream, Sonic Boom, Chevron "J", Jet Stream Wordmark
- Color palettes: Velocity Blue, Midnight Jet, Warm Jet, "Jet Fuel" gradient, "Afterburner"
- Typography: Space Grotesk or Outfit for headings, keep Inter for body
- Assets: Favicon (10+ sizes), empty states, onboarding, auth, OG/social images
- Illustration styles: Technical Blueprint, Motion Trails
- Micro-interactions: Jet trail loading animation

**Theme 3: UI Copy & User-Facing Text** (14 ideas)
Every string, label, tooltip, and message users see:
- SEO metadata, OG tags, manifest.json
- Toast messages, command palette, keyboard shortcuts modal
- 404/error pages, browser tab titles
- Onboarding tour text, workspace defaults
- Public board branding (Space app)
- Django admin site header
- Brand voice: taglines, error messages, empty/loading state copy

**Theme 4: Configuration & Infrastructure** (12 ideas)
Docker, Nginx, CI/CD, env vars, deployment configs:
- Dockerfiles (root + apiserver)
- Docker Compose files (3 files, 8 services)
- Nginx upstream names and config
- GitHub Actions workflows (3 pipelines)
- Heroku config, setup/start scripts
- Environment templates, supervisor config
- Docker networks and volumes

**Theme 5: External Integrations & Auth** (14 ideas)
OAuth, third-party services, API keys, webhooks:
- Email sender identity and SMTP config
- S3/image URL references in next.config.js
- Analytics/tracking IDs (PostHog, Plausible, Clarity, Jitsu, Sentry)
- OAuth app re-registration (Google, GitHub)
- Slack bot and GitHub App identity
- OpenAI API prompt context
- Unsplash API registration
- CORS allowed origins
- GitHub release notes endpoint repo reference

**Theme 6: Backend Specifics** (11 ideas)
Django-specific renaming, email templates, signals:
- Email templates (`templates/emails/`)
- User model Slack signal message
- API token label generation
- Management commands help text
- Debug/IDE configuration
- JWT secret key loading path
- In-flight Celery task name handling
- Log messages, print statements, user agent strings
- Static file collection path

**Theme 7: Database & Data Migration** (7 ideas)
Schema, content types, migration files, existing data:
- Django content types table (data migration required)
- Migration file relocation (46+ files)
- Existing database content type records
- Database table name prefix verification
- S3 upload path prefix (existing file accessibility)
- Cookie names (session continuity)
- WebSocket channel names

**Theme 8: Documentation & Community** (8 ideas)
All markdown files, GitHub templates, legal:
- README.md full rewrite with new branding
- CONTRIBUTING.md, ENV_SETUP.md, CODE_OF_CONDUCT.md
- Generated docs (regenerate post-rebrand)
- GitHub issue templates
- LICENSE attribution check
- Onboarding tour interactive flow rewrite

### Breakthrough Concepts

| Idea | Why It's Breakthrough |
|------|----------------------|
| "Jet Black" Vercel-inspired aesthetic | Natural brand pairing — "jet black" is a real phrase, developer credibility |
| Chevron "J" logo mark | Angular = speed + precision, works at 16px favicon, distinctive |
| "Jet Fuel" gradient brand | Gradient identity like Instagram — memorable and distinctive |
| Jet trail loading animation | Users see loading constantly — branded micro-moment |
| Automated import replacement script | Solves the 225-file Python rename problem reliably |
| Final grep audit for verification | The "proof" step guaranteeing zero references remain |
| In-flight Celery task handling | Non-obvious deploy-time failure mode most rebrands miss |

### Prioritization Results

**Execution Order (7 Phases):**

| Phase | Focus | Dependencies | Effort |
|-------|-------|-------------|--------|
| 0 — Design | Logo, colors, all visual assets | None — start immediately | Design |
| 1 — Backend | Python `plane/` → `jet/`, migrations, templates | Phase 0 (logo for emails) | Heavy |
| 2 — Frontend | npm rename, string literals, asset placement | Phase 0 (all visual assets) | Heavy |
| 3 — Infra | Docker, Nginx, CI/CD, scripts | Phases 1-2 (module paths) | Medium |
| 4 — Integrations | OAuth, Sentry, Slack, GitHub apps | Phase 3 (stable build) | Medium |
| 5 — Docs | README, guides, community docs | Phases 1-4 (final state) | Light |
| 6 — Verify | Grep audit, tests, build, UI walkthrough | All phases | Critical |

**Quick Wins:**
- Automated `sed`/script for Python import replacement (#73)
- Grep-based identification of all string literals containing "Plane" (#75)
- README rewrite can begin immediately (#44)

**Top Priority Brand Decisions Needed:**
1. Logo mark — Chevron "J" recommended
2. Color palette — Velocity Blue or Jet Black
3. npm scope — verify `@jet` availability
4. Domain — `jetpm.app` or equivalent for emails/URLs

## Session Summary and Insights

**Key Achievements:**

- 125 rebrand touchpoints identified across 13 dimensions — exhaustive coverage
- 4 logo concepts and 5 color palettes generated for brand identity
- 7-phase execution plan with clear dependencies and parallel workstreams
- Non-obvious edge cases caught: content type migrations, in-flight Celery tasks, cookie names, WebSocket channels
- Verification strategy defined: automated grep audit + test suite + build + manual walkthrough

**Session Reflections:**

This brainstorming session transformed a broad "rebrand everything" goal into a structured, exhaustive, and actionable plan. The morphological analysis technique was particularly effective for ensuring zero missed touchpoints — mapping 13 dimensions systematically. The cross-pollination technique added creative depth to what could have been a mechanical find-and-replace exercise, generating a genuine brand identity for Jet. The constraint mapping technique converted ideas into a feasible execution sequence with clear dependencies.

The session identified that this rebrand is fundamentally a 3-layer problem: (1) creative identity (design), (2) systematic code transformation (automation-assisted), and (3) external service re-registration (manual). The 7-phase plan sequences these layers to minimize risk and maximize parallelism.
