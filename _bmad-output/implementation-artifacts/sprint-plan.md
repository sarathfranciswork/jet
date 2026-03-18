# Sprint Plan -- Jet Rebrand

**Author:** Scrum Master
**Date:** 2026-03-18
**Sprint Duration:** 1 week per sprint (5 working days)
**Total Stories:** 46 across 7 epics
**Source:** Epics & Stories v1.0, Architecture v1.0, PRD v1.0

---

## Sprint Overview

| Sprint | Dates (Projected) | Focus | Stories | Epic(s) |
|--------|-------------------|-------|---------|---------|
| Sprint 1 | Week 1 | Design Assets + Backend Kickstart | 10 | E0 (7) + E1 partial (3) |
| Sprint 2 | Week 2 | Backend Rename Completion | 5 | E1 remaining (5) |
| Sprint 3 | Week 3 | Frontend Rename | 9 | E2 (9) |
| Sprint 4 | Week 4 | Infrastructure + Integrations | 12 | E3 (7) + E4 (5) |
| Sprint 5 | Week 5 | Documentation + Verification & QA | 10 | E5 (4) + E6 (6) |

**Rationale for adjustments from suggested structure:**

The dependency graph shows that E1 (Backend) and E2 (Frontend) can start in parallel once E0 design assets are available. However, several E1 stories (E1-S1 directory rename, E1-S2 import updates, E1-S8 test fixes) have **no dependency on design assets** -- they are pure code renames. Moving these into Sprint 1 alongside E0 removes 3 stories of pressure from Sprint 2 and leverages the fact that a developer can work on backend renames while design assets are being created.

E4 (Integrations) depends on E3 (Infrastructure) at the epic level, but most E4 stories (OAuth registration, Slack app, Sentry) only need the logo from E0-S1, not completed infrastructure. These can start in parallel with E3 within Sprint 4.

---

## Sprint 1: Design Assets + Backend Kickstart

**Sprint Goal:** Deliver all visual design assets required by downstream sprints, and begin the backend directory rename and import updates (which have no design dependency).

**Duration:** Week 1

### Stories Allocated

| Story ID | Title | Effort | Dependencies | Track |
|----------|-------|--------|--------------|-------|
| E0-S1 | Create Chevron "J" Logo Mark SVG | M (1-2d) | None | Design |
| E0-S2 | Generate Favicon Set (All Sizes) | S (<1d) | E0-S1 | Design |
| E0-S3 | Create OG Social Preview Image | S (<1d) | E0-S1 | Design |
| E0-S4 | Create Auth Screen Background Image | S (<1d) | E0-S1 | Design |
| E0-S5 | Create Empty State Illustrations (Blueprint Style) | L (2-3d) | E0-S1 | Design |
| E0-S6 | Create Onboarding Step Images | M (1-2d) | E0-S1, E0-S5 | Design |
| E0-S7 | Create Email Header Logo | S (<1d) | E0-S1 | Design |
| E1-S1 | Rename `apiserver/plane/` to `apiserver/jet/` | S (<1d) | None | Backend |
| E1-S2 | Update All Python Imports (`plane.*` to `jet.*`) | M (1-2d) | E1-S1 | Backend |
| E1-S8 | Update Backend Test Suite Imports and Assertions | S (<1d) | E1-S2 | Backend |

### Parallel Execution Plan

```
Day 1-2:
  [Design Track]  E0-S1: Logo mark creation (CRITICAL PATH -- must complete by Day 2)
  [Backend Track] E1-S1: Directory rename (independent of design)

Day 2-3:
  [Design Track]  E0-S2, E0-S3, E0-S4, E0-S7 (all depend on E0-S1, can run in parallel)
  [Backend Track] E1-S2: Automated sed + manual review of Python imports

Day 3-5:
  [Design Track]  E0-S5: Empty state illustrations (largest design story, 2-3 days)
  [Design Track]  E0-S6: Onboarding images (after E0-S5 style established)
  [Backend Track] E1-S8: Test suite import fixes + run tests
```

### Sprint Deliverables

- Complete Jet visual identity asset set (logo, favicons, OG image, auth background, 5+ empty states, onboarding images, email logo)
- Backend directory renamed from `plane/` to `jet/`
- All ~225 Python import statements updated
- Test imports fixed (tests may not fully pass yet until E1-S3 completes settings updates)

### Exit Criteria

- [ ] All design assets exported and placed in a staging directory (ready for E2-S6)
- [ ] `apiserver/jet/` directory exists; `apiserver/plane/` does not
- [ ] `grep -rn "from plane\." apiserver/ --include="*.py"` returns 0 results
- [ ] `grep -rn "import plane\." apiserver/ --include="*.py"` returns 0 results
- [ ] E0-S1 logo approved by stakeholder

---

## Sprint 2: Backend Rename Completion

**Sprint Goal:** Complete all remaining backend rename work. By sprint end, `python manage.py check` passes, `python manage.py test` passes, and the API server starts with all `jet.*` module paths.

**Duration:** Week 2

### Stories Allocated

| Story ID | Title | Effort | Dependencies | Track |
|----------|-------|--------|--------------|-------|
| E1-S3 | Update Django Settings, WSGI, ASGI, Celery, Server Config | M (1-2d) | E1-S1, E1-S2 | Backend |
| E1-S4 | Create Django Content Type Data Migration | M (1-2d) | E1-S1, E1-S2 | Backend |
| E1-S5 | Rebrand Email Templates | M (1-2d) | E0-S7, E1-S1 | Backend |
| E1-S6 | Update Slack Signal and Notification Text | S (<1d) | E1-S2 | Backend |
| E1-S7 | Update Default Settings Values and Constants | S (<1d) | E1-S2 | Backend |

### Parallel Execution Plan

```
Day 1-2:
  [Track A] E1-S3: Settings, WSGI, ASGI, Celery config (foundational)
  [Track B] E1-S5: Email template rebranding (independent once E0-S7 done)

Day 2-3:
  [Track A] E1-S4: Content type data migration (depends on E1-S3 for settings)
  [Track B] E1-S6: Slack signal text update (small, independent)
  [Track B] E1-S7: Default settings values (small, independent)

Day 4-5:
  [Verification] Run python manage.py check, python manage.py test
  [Verification] Run python manage.py migrate on test database copy
  [Verification] Start API server with python manage.py runserver
  [Fix]          Address any failures discovered during verification
```

### Sprint Deliverables

- Fully renamed and functional Django API server under `jet.*` namespace
- Content type safety migration created and tested
- All email templates displaying Jet branding
- Slack notifications referencing Jet
- All default settings (EMAIL_FROM, WEB_URL, SCOUT_NAME) using Jet values

### Exit Criteria

- [ ] `python manage.py check` passes with 0 errors
- [ ] `python manage.py test` passes (all tests green)
- [ ] `python manage.py migrate` runs successfully on a test database
- [ ] `python manage.py runserver` starts without import errors
- [ ] `grep -ri "plane" apiserver/ --include="*.py" --include="*.html"` returns 0 brand-name results
- [ ] Celery worker starts: `celery -A jet worker -l info` discovers all tasks

---

## Sprint 3: Frontend Rename

**Sprint Goal:** Rename all frontend npm packages, replace all "Plane" string literals, swap all visual assets, and apply the Jet Black color palette. By sprint end, `yarn build` succeeds for both web and space apps.

**Duration:** Week 3

### Stories Allocated

| Story ID | Title | Effort | Dependencies | Track |
|----------|-------|--------|--------------|-------|
| E2-S1 | Rename npm Packages from `@plane/*` to `@jet/*` | L (2-3d) | None | Frontend-Core |
| E2-S2 | Replace "Plane" String Literals in Web App | L (2-3d) | E2-S1 | Frontend-Web |
| E2-S3 | Replace "Plane" String Literals in Space App | M (1-2d) | E2-S1 | Frontend-Space |
| E2-S4 | Update SEO Metadata, Manifest, and OG Tags | M (1-2d) | E0-S2, E0-S3 | Frontend-Config |
| E2-S5 | Update Next.js Config and Analytics References | S (<1d) | E2-S1 | Frontend-Config |
| E2-S6 | Replace All Visual Assets (Logos, Favicons, Images) | M (1-2d) | E0-S2 thru E0-S6 | Frontend-Assets |
| E2-S7 | Update CSS Variables and Default Theme to Jet Black | M (1-2d) | None | Frontend-Style |
| E2-S8 | Update Onboarding Tour and Welcome Copy | S (<1d) | E2-S2 | Frontend-Web |
| E2-S9 | Update Custom SVG Icon Components (91 Icons) | XL (3-5d) | E0-S1 | Frontend-Icons |

### Parallel Execution Plan

```
Day 1-2:
  [Track A] E2-S1: Package rename (all package.json + imports) -- CRITICAL PATH
  [Track B] E2-S7: CSS variable updates (independent of package rename)
  [Track C] E2-S9: Begin SVG icon audit and branded icon replacements
  [Track D] E2-S6: Copy all design assets to web/public/ and space/public/

Day 2-3:
  [Track A] E2-S2: Web app string literal replacement (depends on E2-S1)
  [Track B] E2-S3: Space app string literal replacement (depends on E2-S1)
  [Track C] E2-S4: SEO metadata, manifest.json, OG tags
  [Track D] E2-S9: Continue icon work

Day 4-5:
  [Track A] E2-S5: next.config.js and analytics references
  [Track B] E2-S8: Onboarding tour text (depends on E2-S2)
  [Track C] E2-S9: Complete icon updates (may carry over -- see note)
  [Verification] yarn install && yarn build (web + space)
  [Fix]    Address any build failures
```

**Note on E2-S9 (SVG Icons):** This is the largest single story at XL effort (3-5 days). For Sprint 3, the focus should be on renaming any icons that contain "Plane" branding and ensuring all icon component exports work. The full angular/chevron style redesign of all 91 icons can be partially deferred if it threatens sprint completion. The exit criterion is: no "Plane"-branded icons remain, and all icons render without errors.

### Sprint Deliverables

- All npm packages renamed from `@plane/*` to `@jet/*`
- Zero "Plane" string literals in user-facing web and space app text
- SEO metadata, manifest.json, and OG tags referencing Jet
- All visual assets (logos, favicons, empty states, onboarding, auth) replaced with Jet versions
- CSS variables updated to Jet Black palette
- Onboarding flow text referencing Jet
- Icon components renamed and functional (full redesign may be partial)

### Exit Criteria

- [ ] `yarn install` completes without errors
- [ ] `yarn build --filter=web` succeeds with exit code 0
- [ ] `yarn build --filter=space` succeeds with exit code 0
- [ ] `grep -rn "@plane/" web/ space/ packages/ --include="*.ts" --include="*.tsx" --include="*.json"` returns 0 results
- [ ] `grep -rn '"Plane"' web/components/ web/pages/ web/constants/ space/components/ space/pages/ --include="*.tsx" --include="*.ts"` returns 0 brand-name results
- [ ] All favicon sizes present in `web/public/favicon/`
- [ ] `manifest.json` shows `"name": "Jet"`

---

## Sprint 4: Infrastructure + Integrations

**Sprint Goal:** Update all Docker, Nginx, CI/CD, and deployment configurations to use `jet-*` naming. Register all external service integrations under Jet identity. By sprint end, `docker compose up -d` starts all services with Jet names.

**Duration:** Week 4

### Stories Allocated

| Story ID | Title | Effort | Dependencies | Track |
|----------|-------|--------|--------------|-------|
| E3-S1 | Update Dockerfiles (Root and API Server) | M (1-2d) | E1-S3 | Infrastructure |
| E3-S2 | Update Docker Compose Files (All 3 Variants) | M (1-2d) | E3-S1 | Infrastructure |
| E3-S3 | Update Nginx Config and Supervisor Config | S (<1d) | E3-S2 | Infrastructure |
| E3-S4 | Update GitHub Actions CI/CD Workflows | M (1-2d) | E3-S1, E3-S2 | Infrastructure |
| E3-S5 | Update Setup Script and Start Script | S (<1d) | E1-S7 | Infrastructure |
| E3-S6 | Update Heroku Configuration | S (<1d) | E3-S1 | Infrastructure |
| E3-S7 | Update Environment Variable Templates | S (<1d) | E1-S7 | Infrastructure |
| E4-S1 | Register Google and GitHub OAuth Applications | M (1-2d) | E0-S1 | Integrations |
| E4-S2 | Register GitHub App for Repository Sync | M (1-2d) | E3-S2 | Integrations |
| E4-S3 | Register Slack App/Bot | M (1-2d) | E1-S6 | Integrations |
| E4-S4 | Update Sentry and Analytics Projects | S (<1d) | E2-S5 | Integrations |
| E4-S5 | Update CORS Origins and OpenAI Prompts | S (<1d) | E1-S2 | Integrations |

### Parallel Execution Plan

```
Day 1-2:
  [Infra Track]        E3-S1: Dockerfiles (root + apiserver)
  [Infra Track]        E3-S5: Setup script + E3-S7: Env templates (small, independent)
  [Integration Track]  E4-S1: Register Google + GitHub OAuth apps (external, no code dependency)
  [Integration Track]  E4-S3: Register Slack app (external)
  [Integration Track]  E4-S5: CORS origins + OpenAI prompt updates (code changes)

Day 2-3:
  [Infra Track]        E3-S2: Docker Compose files (3 variants)
  [Infra Track]        E3-S6: Heroku config
  [Integration Track]  E4-S4: Sentry + analytics project updates

Day 3-4:
  [Infra Track]        E3-S3: Nginx + Supervisor config
  [Infra Track]        E3-S4: GitHub Actions workflows
  [Integration Track]  E4-S2: Register GitHub App (needs Jet API accessible)

Day 4-5:
  [Verification] docker compose build
  [Verification] docker compose up -d && docker compose ps
  [Verification] curl localhost:3000 (web), curl localhost:8000/api/ (API)
  [Fix]          Address any Docker or routing failures
```

### Sprint Deliverables

- All Dockerfiles updated with `jet` module paths and group names
- All 3 Docker Compose files using `jet-*` service names
- Nginx routing to correctly named services
- CI/CD pipelines building `jet-*` Docker images
- Setup script generating Jet-branded `.env` files
- Google OAuth, GitHub OAuth, GitHub App, and Slack bot registered as "Jet"
- Sentry project and analytics services renamed/updated
- CORS origins and OpenAI prompts updated

### Exit Criteria

- [ ] `docker compose build` completes successfully (all images built)
- [ ] `docker compose up -d` starts all services; `docker compose ps` shows all healthy/running
- [ ] `docker compose logs api | head -20` shows `jet.*` module paths
- [ ] Nginx routes correctly: `/` to web, `/api/` to API, `/spaces/` to Space
- [ ] `./setup.sh` generates `.env` files with zero "Plane" references
- [ ] OAuth sign-in flow tested for Google and GitHub (at least on staging)
- [ ] `grep -ri "plane" .github/ deploy/ nginx/ docker-compose*.yml Dockerfile* --include="*.yml" --include="*.yaml" --include="*.conf" --include="*.sh" --include="*.env"` returns 0 results
- [ ] GitHub Actions workflow YAML passes syntax validation

---

## Sprint 5: Documentation + Verification & QA

**Sprint Goal:** Update all documentation to reference Jet. Execute the full verification suite (grep audit, backend tests, frontend builds, Docker verification, UI walkthrough, email test, Space app test). Confirm ZERO "Plane" references remain. Gate for merge.

**Duration:** Week 5

### Stories Allocated

| Story ID | Title | Effort | Dependencies | Track |
|----------|-------|--------|--------------|-------|
| E5-S1 | Rewrite README.md | M (1-2d) | E2-S6 | Documentation |
| E5-S2 | Update Contributing Guide, Env Setup, CoC, License | M (1-2d) | E3-S7 | Documentation |
| E5-S3 | Update GitHub Issue and PR Templates | S (<1d) | None | Documentation |
| E5-S4 | Regenerate Project Documentation | M (1-2d) | E1, E2, E3 | Documentation |
| E6-S1 | Automated Grep Audit -- Zero "Plane" References | M (1-2d) | E5 | Verification |
| E6-S2 | Backend Test Suite Pass | S (<1d) | E1-S8, E1-S4 | Verification |
| E6-S3 | Frontend Build Verification (Web + Space) | S (<1d) | E2-S1 thru E2-S3 | Verification |
| E6-S4 | Docker Build and Compose Verification | M (1-2d) | E3-S1 thru E3-S3 | Verification |
| E6-S5 | Manual UI Walkthrough and Email Verification | L (2-3d) | E6-S3, E6-S4 | Verification |
| E6-S6 | Space App (Public Board) Verification | S (<1d) | E6-S4 | Verification |

### Parallel Execution Plan

```
Day 1-2:
  [Docs Track]         E5-S1: Rewrite README.md
  [Docs Track]         E5-S2: Contributing, Env Setup, CoC, License
  [Docs Track]         E5-S3: GitHub issue/PR templates (small, independent)
  [Verification Track] E6-S2: Run backend test suite (quick check)
  [Verification Track] E6-S3: Run frontend builds (quick check)

Day 2-3:
  [Docs Track]         E5-S4: Regenerate project documentation (docs/)
  [Verification Track] E6-S1: Full automated grep audit (after docs finalized)
  [Verification Track] E6-S4: Docker build + compose verification

Day 3-5:
  [Verification Track] E6-S5: Manual UI walkthrough (all screens, all themes, email test)
  [Verification Track] E6-S6: Space app public board verification
  [Fix Track]          Fix any issues discovered during verification
  [Fix Track]          Re-run grep audit after fixes

Day 5:
  [Gate]               Final grep audit: 0 results
  [Gate]               All builds pass
  [Gate]               UI walkthrough checklist complete
  [Gate]               MERGE READINESS DECISION
```

### Sprint Deliverables

- README.md fully rewritten with Jet branding, logo, and quick start instructions
- All contributing, setup, and community docs updated
- GitHub issue/PR templates referencing Jet
- Project documentation (16 files in `docs/`) regenerated
- Grep audit: 0 "Plane" references in codebase
- Backend tests: all passing
- Frontend builds: web + space both succeed
- Docker: all services build and start healthy
- UI walkthrough: complete checklist with screenshots of any findings
- Space app: Jet branding confirmed for public boards
- Email: Jet branding confirmed in all 7 email templates

### Exit Criteria

- [ ] `grep -ri "plane" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.md" --include="*.html" --include="*.css" --include="*.conf" --include="*.env" --include="*.txt" --include="*.sh" . | grep -v node_modules | grep -v .git | grep -v _bmad | grep -v yarn.lock` returns **0 results** (LICENSE attribution excepted)
- [ ] `python manage.py test` -- all tests pass
- [ ] `yarn build --filter=web` -- exit code 0
- [ ] `yarn build --filter=space` -- exit code 0
- [ ] `docker compose build` -- all images built
- [ ] `docker compose up -d` -- all services healthy
- [ ] UI walkthrough checklist: all items checked (no "Plane" visible on any screen)
- [ ] Email test: all 7 templates show Jet branding
- [ ] Space app: Jet logo, "Powered by Jet" footer, correct OG preview
- [ ] CI grep prevention check added to `.github/workflows/`
- [ ] **MERGE APPROVED** -- branch ready to merge to `develop`

---

## Summary Timeline

```
Week 1 (Sprint 1)     Week 2 (Sprint 2)     Week 3 (Sprint 3)     Week 4 (Sprint 4)     Week 5 (Sprint 5)
==================     ==================     ==================     ==================     ==================
E0: Design Assets      E1: Backend            E2: Frontend           E3: Infrastructure     E5: Documentation
  + E1-S1, S2, S8       Completion              Rename                 + E4: Integrations     + E6: Verification
  (Backend kickstart)

[Design] =============>
[Backend]  ============ ===================>
[Frontend]                                   ===================>
[Infrastructure]                                                    ===================>
[Integrations]                                                      ===================>
[Documentation]                                                                            ======>
[Verification]                                                                             =============>
                                                                                                        |
                                                                                                   MERGE GATE
```

## Capacity and Velocity Notes

- **Total effort estimate:** 35-52 person-days (from Epics Appendix A)
- **Sprint capacity:** 5 working days per sprint
- **Parallel tracks:** Design and Backend can run in parallel (Sprint 1). Infrastructure and Integrations can run in parallel (Sprint 4). Documentation and Verification can run in parallel (Sprint 5).
- **For 1 developer:** The plan above is tight. Sprint 1 and Sprint 3 carry the most risk of overrun due to design asset creation (E0-S5) and icon redesign (E2-S9) respectively. Consider extending to 6 sprints if velocity is lower than expected.
- **For 2 developers:** One developer focuses on Design (Sprint 1) then Frontend (Sprint 3) then Documentation (Sprint 5). The other focuses on Backend (Sprint 1-2) then Infrastructure (Sprint 4) then Verification (Sprint 5). This parallelism brings total duration down to approximately 4 weeks.
- **Buffer:** Sprint 5 includes verification and fix time. If earlier sprints complete on schedule, Sprint 5 can absorb any remaining work from E2-S9 (icon redesign) or fix issues found during verification.
