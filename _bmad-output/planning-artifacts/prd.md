---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish', 'step-12-complete']
inputDocuments:
  - '_bmad-output/brainstorming/brainstorming-session-2026-03-18-1940.md'
  - '_bmad-output/planning-artifacts/jet-brand-identity.md'
  - 'docs/index.md'
  - 'docs/project-overview.md'
  - 'docs/source-tree-analysis.md'
  - 'docs/architecture-web.md'
  - 'docs/architecture-apiserver.md'
  - 'docs/architecture-space.md'
  - 'docs/architecture-packages.md'
  - 'docs/architecture-infra.md'
  - 'docs/api-contracts-apiserver.md'
  - 'docs/data-models-apiserver.md'
  - 'docs/component-inventory-web.md'
  - 'docs/component-inventory-packages.md'
  - 'docs/integration-architecture.md'
  - 'docs/development-guide.md'
  - 'docs/deployment-guide.md'
workflowType: 'prd'
documentCounts:
  briefs: 0
  research: 0
  brainstorming: 1
  planningArtifacts: 1
  projectDocs: 15
classification:
  projectType: 'saas_b2b'
  domain: 'general'
  complexity: 'low-medium'
  projectContext: 'brownfield'
---

# Product Requirements Document — Jet Rebrand

**Author:** Franc
**Date:** 2026-03-18
**Version:** 1.0
**Status:** Complete

## Executive Summary

Jet is a complete rebrand of the open-source Plane project management platform (v0.13.2). The goal is total identity transformation — every reference to "Plane" across every layer of the technology stack is replaced with "Jet," and a new visual identity (logo, colors, typography, illustrations, assets) is applied throughout.

This is not a feature change. No functionality is added, removed, or altered. The product's capabilities — issue tracking, cycles/sprints, modules, views, pages, inbox, analytics, and integrations — remain identical. What changes is the product's name, visual identity, code identity, deployment identity, and brand voice across all 5 monorepo parts (web dashboard, Space public sharing app, Django API server, shared TypeScript packages, and Docker/Nginx infrastructure).

The rebrand must be total: zero references to "Plane" remain in the codebase after completion. This includes user-facing UI, backend Python modules, Docker image/service names, email templates, CI/CD pipelines, environment variable templates, and documentation.

### What Makes This Special

This is a comprehensive identity rebirth, not a find-and-replace. The new Jet identity is designed to be distinctive and developer-credible:

- **Chevron "J" logo mark** — Angular, geometric, works from 16px favicon to full display
- **"Jet Black" color palette** — Dark-first aesthetic (#09090B) with electric blue (#3B82F6) accent, inspired by Vercel/Linear
- **"Jet Fuel" gradient** — Blue-to-cyan gradient for branded highlights
- **Space Grotesk headings** — Geometric display font paired with Inter body text
- **Technical Blueprint illustrations** — Line-art style empty states and onboarding visuals
- **Brand voice** — "Ship faster with Jet" — professional, concise, speed-focused

The rebrand touches 125+ identified touchpoints across 13 dimensions, including non-obvious edge cases like Django content type migrations, in-flight Celery task naming, cookie names, and WebSocket channel names.

## Project Classification

- **Project Type:** SaaS B2B — Multi-tenant project management platform
- **Domain:** General (project management / developer tools)
- **Complexity:** Low-medium (straightforward domain, complex execution scope)
- **Project Context:** Brownfield — Existing Plane v0.13.2 monorepo
- **Change Type:** Identity transformation (no functional changes)

## Success Criteria

### User Success

- Users see "Jet" branding consistently across every screen, email, and interaction — no "Plane" artifacts visible anywhere
- The new visual identity (Jet Black palette, Chevron "J" logo) renders correctly across all themes (dark, light, light-contrast, dark-contrast, custom)
- PWA installation shows "Jet" name, icon, and theme color on all platforms
- Public shared boards (Space app) display Jet branding to anonymous viewers
- Browser tabs show "Jet - [Page Name]" consistently

### Business Success

- Complete brand independence from Plane — the codebase can be deployed as a standalone product with its own identity
- No trademark or brand confusion with the original Plane project
- The rebrand enables independent marketing, documentation, and community building under the Jet name

### Technical Success

- Zero references to "Plane" remain in the codebase (verified by automated grep audit)
- All builds pass: `yarn build` (web + space), `python manage.py test` (apiserver), Docker image builds
- Django migrations run successfully (including content type data migration)
- All Docker services start and communicate correctly with new service names
- CI/CD pipelines execute without errors
- No runtime errors from missed module path renames (WSGI, ASGI, Celery, Gunicorn)

### Measurable Outcomes

| Metric | Target | Verification |
|--------|--------|-------------|
| "Plane" references in codebase | 0 | `grep -ri "plane" --include=...` audit |
| Build success (web) | Pass | `yarn build --filter=web` |
| Build success (space) | Pass | `yarn build --filter=space` |
| Test suite (apiserver) | Pass | `python manage.py test` |
| Docker Compose up | All services healthy | `docker compose up -d` + health checks |
| Visual regression | No broken layouts | Manual UI walkthrough |
| Email rendering | Jet branding correct | Send test emails |

## Product Scope

### MVP — Phase 0-2 (Core Rebrand)

The minimum viable rebrand that makes the product deployable as "Jet":

- New logo, favicon, and app icons (all sizes)
- Python module rename `plane/` → `jet/` with all import updates
- npm package rename `@plane/*` → `@jet/*`
- All UI text referencing "Plane" updated to "Jet"
- Docker image/service names updated to `jet-*`
- Email templates rebranded
- Django content type data migration
- SEO metadata, manifest.json, OG tags updated
- README rewritten

### Growth Features (Post-MVP)

- Custom Jet loading animation (jet trail)
- Blueprint-style empty state illustrations
- Onboarding flow with new imagery
- Brand voice polish (empty state copy, error messages)
- Custom icon redesign (91 SVG components in angular Chevron style)

### Vision (Future)

- Independent documentation site
- Community rebranding (Discord, GitHub org)
- Marketplace/plugin ecosystem under Jet brand
- Custom theme presets reflecting Jet identity

## User Journeys

### Journey 1: Developer Setting Up Local Environment

A developer clones the Jet repository. They run `./setup.sh`, which generates `.env` files with Jet-branded defaults (`admin@jetpm.app`). They run `docker compose -f docker-compose-local.yml up -d` and see `jet-db`, `jet-redis`, `jet-minio` services start. They run `yarn install && yarn dev`, open `http://localhost:3000`, and see the Jet logo, Jet Black color scheme, and "Welcome to Jet" on the sign-in page. At no point do they encounter any reference to "Plane."

**Capabilities Revealed:** Setup script branding, Docker service naming, environment defaults, sign-in page branding, logo/favicon display.

### Journey 2: End User First Login

A user receives an email invitation: "Team Jet <team@jetpm.app>" invites them to a workspace. The email template shows the Chevron "J" logo and Jet branding. They click the link, land on the auth page with Jet logo and dark background, create their account, and enter the onboarding flow: "Welcome to Jet. Let's set up your workspace." They see the Jet favicon in their browser tab ("Jet - Dashboard"). They press Cmd+K and the command palette says "Search in Jet..." Every tooltip, toast, and modal references Jet.

**Capabilities Revealed:** Email template branding, auth screen assets, onboarding copy, favicon, command palette, toast messages, browser tab titles.

### Journey 3: External Viewer on Public Board

An external stakeholder receives a shared project link. They open it in the Space app and see the Jet logo in the header, "Powered by Jet" in the footer, and issue cards with Jet color scheme. They can view, react, vote, and comment — all within a Jet-branded experience. The OG preview when sharing the link on Slack shows "Jet — Project management at jet speed" with the Jet Fuel gradient background.

**Capabilities Revealed:** Space app branding, public board header/footer, OG social images, Space favicon.

### Journey 4: DevOps Deploying to Production

An ops engineer pulls `jet-frontend:latest`, `jet-backend:latest`, `jet-space:latest`, `jet-proxy:latest` from the container registry. Docker Compose starts services named `jet-api`, `jet-worker`, `jet-beat-worker`, `jet-db`, `jet-redis`, `jet-minio`. Nginx routes `/` to web, `/api/` to API, `/spaces/` to Space. Gunicorn starts `jet.wsgi:application`. Celery discovers tasks from `jet.bgtasks`. Sentry reports errors under the "Jet" project. All logs show `jet.*` module paths.

**Capabilities Revealed:** Docker image names, service names, Gunicorn WSGI path, Celery autodiscovery, Nginx config, Sentry project, log output.

### Journey Requirements Summary

| Journey | Key Capability Areas |
|---------|---------------------|
| Developer Setup | Scripts, env defaults, Docker services, sign-in UI |
| First Login | Email templates, auth UI, onboarding, command palette, browser tabs |
| Public Board | Space branding, OG images, public board chrome |
| Production Deploy | Docker images/services, WSGI/ASGI/Celery paths, monitoring |

## SaaS B2B Specific Requirements

### Multi-Tenant Considerations

- Workspace-level branding remains user-customizable (custom themes) — Jet branding is the default, not a forced override
- The `custom` theme option continues to work; Jet colors are the new default theme, not a hard constraint
- All 5 theme variants (light, dark, light-contrast, dark-contrast, custom) must reflect Jet defaults

### Permission Model

- No changes to RBAC (Owner/Admin/Member/Guest at workspace level, Admin/Member/Viewer/Guest at project level)
- Admin-visible areas (Django admin panel) must show "Jet Administration" header

### Integration Points

- OAuth apps must be re-registered under Jet identity (Google, GitHub)
- Slack bot must be re-registered as "Jet"
- GitHub App must be re-registered for repository sync
- OpenAI prompts must reference "Jet" not "Plane"
- Unsplash API app name updated

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Phased execution with design assets as the critical path prerequisite. Code changes are automation-assisted (scripted bulk renames) followed by manual review. The rebrand is done in a single feature branch and merged as one atomic change.

**Resource Requirements:** 1 developer (full-stack), design asset generation (AI-assisted or manual), QA for visual regression and grep audit.

### Phase 0 — Design Assets (Prerequisite)

| Deliverable | Specification |
|-------------|--------------|
| Logo SVG | Chevron "J" mark, vector source |
| Favicon set | 16, 32, 48, 72, 96, 128, 144, 192, 384, 512px PNGs + ICO |
| OG image | 1200x630px with Jet Fuel gradient + logo + tagline |
| Auth background | Dark Jet Black with subtle grid pattern |
| Empty state images | Blueprint-style line art (at least 5 variants) |
| Onboarding images | 3-4 step flow visuals |
| Email header logo | PNG for email templates |

### Phase 1 — Backend Rename

| Task | Files | Approach |
|------|-------|----------|
| Rename `apiserver/plane/` → `apiserver/jet/` | Directory | `mv` command |
| Update all Python imports | ~225 files | Automated `sed` script: `s/from plane\./from jet./g`, `s/import plane\./import jet./g` |
| Update Django settings module | 6 settings files | Manual |
| Update WSGI/ASGI/Celery config | 3 files | Manual |
| Update Gunicorn config | 1 file | Manual |
| Update Procfile | 1 file | Manual |
| Create content type data migration | 1 new migration | Manual Django migration |
| Update email templates | ~10 templates | Manual — replace logos, text, links |
| Update test imports | ~10 files | Automated sed |
| Update management commands | 1 file | Manual |
| Update Slack signal message | 1 file | Manual |

### Phase 2 — Frontend Rename

| Task | Files | Approach |
|------|-------|----------|
| Update npm package names to `@jet/*` | 7 package.json files | Manual |
| Replace all "Plane" string literals | ~990 TSX/TS files | `grep -rn "Plane\|plane" web/ space/` then targeted edits |
| Update SEO constants | 1 file | Manual |
| Update manifest.json | 2 files (web + space) | Manual |
| Update next.config.js image domains | 2 files | Manual |
| Replace all visual assets | ~50 image files | Copy from Phase 0 outputs |
| Update CSS variables (default theme) | 1 file (globals.css) | Manual |
| Update `_document.tsx` meta tags | 2 files | Manual |
| Update `_app.tsx` providers | 2 files | Manual |
| Replace 91 custom SVG icons | 91 files | Batch replacement or redesign |

### Phase 3 — Infrastructure

| Task | Files | Approach |
|------|-------|----------|
| Update root Dockerfile | 1 file | Manual — module paths, user/group names |
| Update apiserver Dockerfiles | 2 files | Manual |
| Update docker-compose.yml (dev) | 1 file | Find-replace `plane-` → `jet-` |
| Update docker-compose-local.yml | 1 file | Find-replace |
| Update deploy/selfhost/docker-compose.yml | 1 file | Find-replace |
| Update nginx config template | 1 file | Update upstream names |
| Update supervisor config | 1 file | Update process names |
| Update GitHub Actions workflows | 3 files | Update image names, repo references |
| Update setup.sh | 1 file | Update any Plane references |
| Update Heroku config | 2 files | Update app name |
| Update environment templates | 3+ files | Update comments, defaults |

### Phase 4 — Integrations (External Services)

| Task | Action |
|------|--------|
| Create new Google OAuth app | Register at console.cloud.google.com as "Jet" |
| Create new GitHub OAuth app | Register at github.com/settings/applications |
| Create new GitHub App | Register for repo sync functionality |
| Create new Slack app | Register at api.slack.com as "Jet" |
| Update Sentry project | Rename or create new project |
| Update analytics services | PostHog, Plausible, Clarity — update project names |
| Update Unsplash app | Re-register under Jet name |
| Update CORS origins | Add Jet domains, remove Plane domains |
| Update OpenAI prompts | Update system prompt context |

### Phase 5 — Documentation

| Task | Files | Approach |
|------|-------|----------|
| Rewrite README.md | 1 file | Full rewrite with new screenshots |
| Update CONTRIBUTING.md | 1 file | Replace references |
| Update ENV_SETUP.md | 1 file | Replace references |
| Update CODE_OF_CONDUCT.md | 1 file | Replace references |
| Update GitHub issue templates | 3 files | Replace references |
| Check LICENSE.txt | 1 file | Verify attribution |
| Regenerate docs/ | 16 files | Re-run `/bmad-bmm-document-project` |

### Phase 6 — Verification

| Check | Command/Method | Pass Criteria |
|-------|---------------|---------------|
| Grep audit | `grep -ri "plane" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.json" --include="*.yml" --include="*.yaml" --include="*.md" --include="*.html" --include="*.css" --include="*.conf" --include="*.env" --include="*.txt" . \| grep -v node_modules \| grep -v .git \| grep -v _bmad` | 0 results |
| Backend tests | `cd apiserver && python manage.py test` | All pass |
| Frontend build (web) | `yarn build --filter=web` | Success |
| Frontend build (space) | `yarn build --filter=space` | Success |
| Docker build | `docker compose build` | All images built |
| Docker up | `docker compose up -d` | All services healthy |
| UI walkthrough | Manual check of all routes | No "Plane" visible |
| Email test | Trigger invitation email | Jet branding correct |
| Public board test | View Space app | Jet branding correct |

### Risk Mitigation Strategy

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Missed "Plane" references | Medium | Low | Automated grep audit in Phase 6; CI check |
| Django content type migration failure | Low | High | Test migration on database copy first |
| In-flight Celery tasks fail at deploy | Low | Medium | Deploy during low-traffic window; drain queues first |
| npm `@jet` scope unavailable | Low | Medium | Fallback to `@jetpm` scope |
| S3 upload paths break | Low | High | Verify `upload_to` paths don't contain "plane"; alias if needed |
| Cookie name change breaks sessions | Low | Low | Users re-login; acceptable for one-time rebrand |
| Build failures from missed imports | Medium | Medium | Automated sed + manual review + full build test |

## Functional Requirements

### FR-ASSET: Brand Asset Creation

- FR-ASSET-1: Designer can generate Chevron "J" logo mark as SVG vector source
- FR-ASSET-2: Designer can export favicon in all required sizes (16, 32, 48, 72, 96, 128, 144, 192, 384, 512px)
- FR-ASSET-3: Designer can create OG social preview image (1200x630px) with Jet Fuel gradient
- FR-ASSET-4: Designer can create auth screen background image with Jet Black aesthetic
- FR-ASSET-5: Designer can create empty state illustrations in Technical Blueprint style (minimum 5 variants)
- FR-ASSET-6: Designer can create onboarding step images (3-4 visuals)
- FR-ASSET-7: Designer can create email header logo for email templates

### FR-BACKEND: Backend Code Rename

- FR-BACKEND-1: Developer can rename `apiserver/plane/` directory to `apiserver/jet/`
- FR-BACKEND-2: Developer can update all Python imports from `plane.*` to `jet.*` across ~225 files
- FR-BACKEND-3: Developer can update `DJANGO_SETTINGS_MODULE` to `jet.settings.*` in all settings and config files
- FR-BACKEND-4: Developer can update WSGI application path to `jet.wsgi:application`
- FR-BACKEND-5: Developer can update ASGI application path to `jet.asgi:application`
- FR-BACKEND-6: Developer can update Celery app configuration to discover tasks from `jet.*`
- FR-BACKEND-7: Developer can create and run a Django data migration to update `django_content_type` records
- FR-BACKEND-8: Developer can update all email templates to display Jet logo, name, and contact information
- FR-BACKEND-9: Developer can update the user model Slack notification signal to reference "Jet"
- FR-BACKEND-10: Developer can update default settings values (DEFAULT_EMAIL, EMAIL_FROM, WEB_URL)
- FR-BACKEND-11: Developer can update Gunicorn configuration to reference `jet.wsgi`
- FR-BACKEND-12: Developer can update Procfile to reference `jet.*` module paths

### FR-FRONTEND: Frontend Code Rename

- FR-FRONTEND-1: Developer can rename all npm packages from `@plane/*` to `@jet/*`
- FR-FRONTEND-2: Developer can update all string literals containing "Plane" to "Jet" across web and space apps
- FR-FRONTEND-3: Developer can update SEO metadata constants (title, description, OG tags)
- FR-FRONTEND-4: Developer can update `manifest.json` (name, short_name, description, theme_color, icons)
- FR-FRONTEND-5: Developer can update `next.config.js` image domains to remove Plane S3 references
- FR-FRONTEND-6: Developer can replace all visual assets (logos, favicons, empty states, onboarding, auth images)
- FR-FRONTEND-7: Developer can update CSS variables in `globals.css` to Jet Black default palette
- FR-FRONTEND-8: Developer can update `_document.tsx` meta tags and analytics references
- FR-FRONTEND-9: Developer can update command palette placeholder text and labels
- FR-FRONTEND-10: Developer can update all browser tab titles from "Plane - *" to "Jet - *"
- FR-FRONTEND-11: Developer can update onboarding tour text to reference Jet

### FR-INFRA: Infrastructure Rename

- FR-INFRA-1: Developer can update root Dockerfile module paths and user/group names
- FR-INFRA-2: Developer can update all Docker Compose files to use `jet-*` service names
- FR-INFRA-3: Developer can update Nginx configuration upstream names to match new service names
- FR-INFRA-4: Developer can update GitHub Actions workflows with new Docker image names
- FR-INFRA-5: Developer can update setup.sh to generate Jet-branded environment files
- FR-INFRA-6: Developer can update supervisor configuration process names
- FR-INFRA-7: Developer can update Heroku configuration (app.json, heroku.yml)
- FR-INFRA-8: Developer can update all environment variable templates to replace Plane references

### FR-INTEGRATE: External Integration Updates

- FR-INTEGRATE-1: Admin can register new Google OAuth application under Jet identity
- FR-INTEGRATE-2: Admin can register new GitHub OAuth application under Jet identity
- FR-INTEGRATE-3: Admin can register new GitHub App for repository sync
- FR-INTEGRATE-4: Admin can register new Slack app/bot under Jet identity
- FR-INTEGRATE-5: Admin can update Sentry project to Jet
- FR-INTEGRATE-6: Admin can update CORS allowed origins to Jet domains
- FR-INTEGRATE-7: Developer can update OpenAI system prompt to reference Jet

### FR-DOCS: Documentation Updates

- FR-DOCS-1: Developer can rewrite README.md with Jet branding, logo, and screenshots
- FR-DOCS-2: Developer can update CONTRIBUTING.md, ENV_SETUP.md, CODE_OF_CONDUCT.md
- FR-DOCS-3: Developer can update GitHub issue templates to reference Jet
- FR-DOCS-4: Developer can verify LICENSE.txt attribution
- FR-DOCS-5: Developer can regenerate project documentation with `/bmad-bmm-document-project`

### FR-VERIFY: Verification

- FR-VERIFY-1: Developer can run automated grep audit confirming zero "Plane" references
- FR-VERIFY-2: Developer can run full backend test suite with all tests passing
- FR-VERIFY-3: Developer can build web and space apps without errors
- FR-VERIFY-4: Developer can build and start all Docker services
- FR-VERIFY-5: Developer can perform manual UI walkthrough confirming Jet branding on every screen
- FR-VERIFY-6: Developer can trigger test emails confirming Jet branding
- FR-VERIFY-7: Developer can verify public board (Space app) displays Jet branding

## Non-Functional Requirements

### Visual Consistency

- NFR-VIS-1: The Jet Black color palette must render correctly across Chrome, Firefox, Safari, and Edge (latest 2 versions)
- NFR-VIS-2: All theme variants (dark, light, light-contrast, dark-contrast, custom) must use Jet defaults unless user-customized
- NFR-VIS-3: The Chevron "J" favicon must be visually recognizable at 16x16px
- NFR-VIS-4: Email templates must render Jet branding correctly in Gmail, Outlook, and Apple Mail

### Build & Deployment

- NFR-BUILD-1: The complete rebrand must be deployable as a single atomic release (one branch, one merge)
- NFR-BUILD-2: No additional runtime dependencies introduced by the rebrand
- NFR-BUILD-3: Docker images must build successfully with new names
- NFR-BUILD-4: Self-hosted deployment via `deploy/selfhost/` must work with new configuration

### Data Migration

- NFR-DATA-1: Django content type migration must be reversible
- NFR-DATA-2: Existing uploaded files (S3/MinIO) must remain accessible after rebrand
- NFR-DATA-3: Existing user sessions may be invalidated (acceptable one-time impact)

### Performance

- NFR-PERF-1: No measurable performance regression from the rebrand (no new dependencies, no additional API calls)
- NFR-PERF-2: New visual assets (logo, favicon, illustrations) must be optimized (SVG where possible, compressed PNGs)

### Maintainability

- NFR-MAINT-1: The `plane/` → `jet/` directory rename should be a single git commit for clean blame history
- NFR-MAINT-2: A CI check should be added to prevent future "Plane" references from being introduced (grep-based pre-commit or CI step)
