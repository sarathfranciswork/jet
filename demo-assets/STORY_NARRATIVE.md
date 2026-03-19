# Jet: Building an Enterprise Feature in a Brownfield Project with Claude Code + BMAD

## The Story Arc

This is the story of how we took an open-source project management tool (Plane v0.13.2), rebranded it as "Jet", deployed it to Google Cloud, and then used Claude Code with the BMAD (Business-Model-Aligned Development) methodology to plan and implement a full-featured GitHub Integration — all as a demonstration of AI-assisted software development on a real brownfield codebase.

---

## Chapter 1: Setting Up Claude Code

**What happened:** We started by installing Claude Code (Anthropic's CLI for AI-assisted development) and configuring it for our project. Claude Code is a terminal-based AI agent that can read, write, and execute code across an entire codebase.

**Key moments:**
- Installed Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- Configured project memory system at `~/.claude/projects/` for persistent context
- Set up BMAD methodology skills — a framework for structured product development
- Claude learns the user's preferences and working style over time

**Why it matters:** Claude Code isn't just autocomplete — it's an autonomous agent that can plan, implement, test, and deploy features while understanding the full codebase context.

---

## Chapter 2: BMAD Planning Methodology

**What happened:** Before writing any code, we used BMAD (Business-Model-Aligned Development) to structure the work. BMAD provides specialized agent roles: Product Manager, Architect, Developer, QA — each with specific skills.

**BMAD** stands for **Breakthrough Method for Agile AI-Driven Development** ([github.com/bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)). It's a framework that provides specialized agent roles and structured workflows for AI-assisted development.

**Key moments:**
- Used `/bmad-architect` to design the technical architecture
- Used `/bmad-create-epics-and-stories` to break requirements into implementable units
- Created a comprehensive Product Requirements Document (PRD) with `/bmad-create-prd`
- Broke down into 9 epics with ~45 stories
- Estimated ~30 days of work across: Data Layer, API Client, Webhook Handler, Sync Engine (both directions), PR Automation, Config APIs, Frontend, Testing
- Used `/bmad-dev-story` for story-by-story implementation

**Why it matters:** Even with AI, good planning prevents wasted effort. BMAD ensures the AI understands the "why" behind each feature, not just the "what". It's the methodology layer that turns Claude Code from a code generator into a structured engineering partner.

---

## Chapter 3: The Rebrand — Plane to Jet

**What happened:** We took the open-source Plane project management tool (v0.13.2, ~500+ files) and completely rebranded it to "Jet" — a custom project management tool.

**Key changes:**
- npm packages: `@plane/*` → `@jet/*`
- Python modules: `plane.*` → `jet.*`
- Docker services: `plane-*` → `jet-*`
- Database tables: maintained existing names for backward compatibility
- Brand identity: Jet Black (#09090B), Jet Blue (#3B82F6), Jet Cyan (#06B6D4)
- Email domain: `jetpm.app`
- Logo: Custom Jet logo replacing all Plane logos

**Files changed:** 500+ files across the entire codebase
**Verification:** Zero "Plane" references remaining in the production app

---

## Chapter 4: GCP Deployment

**What happened:** Deployed the rebranded Jet application to Google Cloud Platform using Docker Compose on a Compute Engine VM.

**Infrastructure:**
- GCP Project: `innovation-labs-489916`
- VM: `jet-server` in `us-central1-a`
- External IP: `34.55.60.88`
- Services: Web (Next.js), API (Django/Gunicorn), Worker (Celery), Beat, PostgreSQL, Redis, MinIO, Nginx proxy

**CI/CD Pipeline:**
- GitHub Actions workflow triggers on push to `feat/jet-rebrand`
- SSHs into GCP VM, pulls latest code, rebuilds Docker containers
- Health check verification with retry loop (12 attempts, 10s apart)

**Key challenges solved:**
- GCP IAM permissions for CI service account
- Git safe directory configuration on VM
- Health check timing for container startup

---

## Chapter 5: The GitHub Integration Feature

**What happened:** This is the centerpiece — implementing a full-featured GitHub Integration (bidirectional sync, PR automation, webhooks) in a brownfield Django + Next.js codebase. Claude Code planned and implemented all 9 epics.

### What was built:

**Backend (Django/Python):**
- 4 new database models: `GithubSyncConfig`, `GithubPullRequest`, `GithubUserMapping`, `GithubSyncLog`
- Extended 2 existing models with new fields
- `GithubAPIClient` class for GitHub API interactions (JWT auth, CRUD for issues/comments/labels/PRs)
- Webhook endpoint with HMAC-SHA256 signature verification
- Celery tasks for bidirectional sync:
  - GitHub → Jet: issue creation, updates, state changes, labels, assignees, comments
  - Jet → GitHub: issue updates, comment sync, label-triggered creation
- PR automation: `[WEB-123]` bracket notation for state automation, bare `WEB-123` for link-only
- Loop prevention: Last-write-wins with 5-second debounce + bot user detection
- Reference parser: Extracts issue references from PR titles/bodies
- Management command for backfilling existing syncs
- Initial sync task: imports all existing GitHub issues when a repo is first connected

**Frontend (Next.js/TypeScript/MobX):**
- TypeScript types for all new entities
- `GithubSyncService` — full CRUD API service
- MobX store for state management
- 7 React components: sync config form, state mapping, PR state mapping, sync logs, user mapping, PR list, PR badge
- Fixed repository selector (API base URL bug from original Plane codebase)

**Infrastructure:**
- Created GitHub App (`jet-gh-app`) via manifest flow
- Configured app credentials on GCP VM
- Database migration with integration record seeding

### The numbers:
- 44 files changed, 4200+ lines added
- 20 new files, 17 modified files
- 4 test files with unit + integration tests
- End-to-end flow: GitHub issue created → synced to Jet in real-time

---

## Chapter 6: Debugging Production Issues

**What happened:** Several real-world production issues were encountered and fixed during deployment — demonstrating how Claude Code handles debugging in production.

**Issues fixed:**
1. **TypeScript build error**: `Property 'states' does not exist on type 'IProjectStateStore'` — used wrong store API, fixed to use `ProjectStateService` + SWR pattern
2. **Loader component**: Required children elements (skeleton items)
3. **PEM key parsing**: Private key stored with escaped `\n` failed to parse — added base64 + file-path fallback support
4. **Repository selector invisible**: `process.env.NEXT_PUBLIC_API_BASE_URL` was `undefined`, producing `"undefined/api/..."` URLs — fixed to use relative paths
5. **Empty integrations page**: No `Integration` records in database — created data migration to seed GitHub + Slack records
6. **Health check timing**: API container needed more startup time — added retry loop

---

## Chapter 7: @Claude on GitHub — Automated Development Workflow

**What happened:** Set up Claude Code GitHub Action so that mentioning `@claude` in GitHub issues automatically triggers implementation.

**The automated flow:**
1. Create issue on GitHub: "Add dark mode toggle to settings"
2. Mention `@claude implement this` in the issue
3. Claude Code Action activates:
   - Reads the issue and understands the codebase
   - Creates a feature branch (`feat/dark-mode-toggle`)
   - Implements the changes
   - Opens a Pull Request with description
4. Claude reviews the PR code
5. PR is reviewed, approved, and merged
6. GitHub Actions deploys to GCP automatically

---

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 13, TypeScript, MobX, Tailwind CSS, SWR |
| Backend | Django 4, Django REST Framework, Celery, PostgreSQL 15 |
| Infrastructure | Docker Compose, Nginx, GCP Compute Engine |
| CI/CD | GitHub Actions |
| AI Tools | Claude Code (Opus 4.6), BMAD Methodology |
| Integration | GitHub App, Webhooks, JWT Auth |

---

## Chapter 8: The Numbers — Cost, Time, and ROI

### What Claude Code Did (Actual Metrics)

| Metric | Value |
|--------|-------|
| **Total tokens processed** | 195.4 million |
| **Output tokens (code + reasoning)** | 273,896 |
| **Cache read tokens** | 192.1 million |
| **Total API cost** | ~$436 |
| **Wall-clock time** | ~4 hours (planning session + implementation session) |
| **Commits produced** | 14 total (10 for GitHub integration feature) |
| **Files changed** | 52 files (GitHub integration only) |
| **Lines of code added** | 4,592 lines |
| **New files created** | 20 files |
| **Epics completed** | 9 epics across backend, frontend, testing |
| **Models created** | 4 new Django models + 2 extended |
| **API endpoints** | 12 new REST endpoints |
| **React components** | 7 new components |
| **Test files** | 4 test files |
| **Production deployments** | 8 successful deployments |
| **Production bugs diagnosed + fixed** | 6 issues found and fixed |

### What This Would Cost Manually

| Approach | Time Estimate | Cost Estimate |
|----------|--------------|---------------|
| **Senior full-stack developer** | 25-30 working days | $15,000-25,000 |
| **Small team (2 devs)** | 15-20 working days | $12,000-20,000 |
| **Freelance/agency** | 4-6 weeks | $20,000-40,000 |
| **Claude Code** | **~4 hours** | **~$436** |

### Breakdown of Manual Effort

A human developer doing this work would need to:
- **Read & understand** the brownfield codebase (500+ files): 2-3 days
- **Design** the data models, API, sync architecture: 2-3 days
- **Implement** backend models + migration: 1-2 days
- **Implement** GitHub API client: 1-2 days
- **Implement** webhook handler: 2-3 days
- **Implement** bidirectional sync engine: 4-5 days
- **Implement** PR automation: 2-3 days
- **Implement** REST APIs: 1-2 days
- **Implement** frontend (types, service, store, 7 components): 3-5 days
- **Write** tests: 2-3 days
- **Debug** production issues: 1-2 days
- **Configure** GitHub App + deploy: 1 day
- **Total**: ~25-30 working days

### The Autonomous Factor

What makes this remarkable is the **autonomy**:
- Claude Code explored the codebase, understood patterns, and matched them
- When production builds failed (TypeScript errors, PEM parsing), Claude diagnosed the root cause from CI logs and fixed it — without being told what went wrong
- Created a GitHub App programmatically via the manifest flow
- SSHed into GCP VMs to configure environment variables
- Ran Django management commands inside Docker containers on remote servers
- Fixed the repo selector bug (a pre-existing bug from Plane's codebase) by tracing the network request path

---

## Key Takeaways

1. **AI can handle brownfield codebases** — Claude Code understood 500+ file codebase, its patterns, and extended it consistently
2. **Planning matters even with AI** — BMAD methodology prevented scope creep and ensured architectural alignment
3. **Real debugging, not toy demos** — Production issues (PEM parsing, TypeScript errors, env var handling) were diagnosed and fixed systematically
4. **End-to-end autonomy** — From planning to deployment to debugging production, Claude Code handled the full lifecycle
5. **The future is @claude** — Mentioning an AI agent in a GitHub issue and having it deliver a working PR is the new development workflow
