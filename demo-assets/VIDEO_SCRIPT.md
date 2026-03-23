# The Future of Software Engineering: How an AI Agent Built a Production Feature in 4 Hours

## Opening Hook

What if you could take a 500-file open-source codebase, completely rebrand it, add a complex enterprise feature, deploy it to the cloud, and have an AI agent autonomously pick up GitHub issues and deliver working pull requests — all in a single evening?

This is not a demo. This is not a prototype. This actually happened. And the total cost? $436.

This is the story of Jet — and how Agentic AI engineering is rewriting the rules of software development.

---

## Act 1: The Setup — Claude Code Meets a Real Codebase

The project starts with Plane — a popular open-source project management tool with over 30,000 GitHub stars. It's a production-grade application: Django backend, Next.js frontend, Celery workers, PostgreSQL, Redis, nginx — the full modern web stack. Over 500 files of real, complex, interconnected code.

The tool: Claude Code by Anthropic — not a code autocomplete, not a chatbot with a code editor. An autonomous AI agent that lives in your terminal, reads entire codebases, writes files, runs commands, manages git, deploys to servers, and debugs production issues. Powered by Claude Opus 4.6 with a 1-million token context window.

The methodology: BMAD — the Breakthrough Method for Agile AI-Driven Development. A structured framework that gives AI agents specialized roles: Product Manager for requirements, Architect for system design, Developer for implementation, QA for testing. Think of it as giving your AI the same structure a human team uses, but executing at machine speed.

---

## Act 2: The Rebrand — 500 Files Changed Without Breaking Anything

First challenge: transform Plane into Jet. Every reference in every file — Python modules, npm packages, Docker services, database models, email domains, logos, favicons, meta tags — all need to change from "Plane" to "Jet" without breaking a single feature.

Claude Code read the entire codebase, understood the dependency graph, and systematically renamed everything:
- Python: plane.* became jet.*
- npm: @plane/* became @jet/*
- Docker: plane-* became jet-*
- Brand: New colors, new logo, new identity

Result: 500+ files changed. Zero "Plane" references remaining. Zero broken features. The app loaded perfectly with full Jet branding.

---

## Act 3: Deploying to the Cloud

Next: get it running on Google Cloud Platform. Claude Code didn't just write a deployment script — it:

1. Created a GitHub Actions CI/CD pipeline that triggers on every push
2. Configured SSH access to a GCP Compute Engine VM
3. Built Docker images for all 7 services (web, api, worker, beat, database, redis, proxy)
4. Set up health check verification with intelligent retry logic
5. Fixed IAM permission issues by granting the right roles to the service account
6. Diagnosed and fixed a git safe directory error on the remote server

The production app was live at a public IP address, serving real traffic.

---

## Act 4: The Main Event — Building GitHub Integration in 4 Hours

This is the centerpiece. The plan called for a full-featured GitHub integration — something that would normally take a team of developers 25-30 working days:

Bidirectional sync between GitHub and Jet. When you create an issue on GitHub with a "Jet" label, it appears in Jet. When you update it in Jet, it syncs back to GitHub. Comments, labels, assignees — everything stays in sync.

PR automation: mention an issue number in a pull request title with bracket notation like [JET-123], and when the PR is merged, the Jet issue automatically moves to "Done."

Webhook handling: GitHub sends real-time events, verified with HMAC-SHA256 signatures, processed by Celery background tasks with loop prevention to avoid infinite sync cycles.

Claude Code delivered all of this across 9 implementation epics:

Epic 1 - Data Layer: 4 new Django models, 1 database migration, extended 2 existing models
Epic 2 - API Client: GithubAPIClient class with JWT authentication, CRUD operations for issues, comments, labels, pull requests
Epic 3 - Webhook Handler: Public endpoint with signature verification, async Celery task dispatching
Epic 4 - Inbound Sync: GitHub issues, comments, labels, assignees flowing into Jet
Epic 5 - Outbound Sync: Jet changes flowing back to GitHub
Epic 6 - PR Automation: Reference parsing from PR titles, state mapping for the PR lifecycle
Epic 7 - Configuration APIs: CRUD endpoints for sync config, user mappings, pull requests, sync logs
Epic 8 - Frontend: TypeScript types, API service, MobX store, 7 React components
Epic 9 - Tests: Unit tests for reference parsing, HMAC verification, loop prevention

The numbers: 52 files changed. 4,592 lines of code added. 20 new files created. 10 commits. Wall-clock time: approximately 4 hours.

---

## Act 5: When Things Break — AI Debugging Production

Real software development isn't just writing code. It's debugging when things go wrong. Here's where Claude Code truly proved itself:

Bug 1 — TypeScript Build Failure: The frontend build failed because the code used a store property that didn't exist. Claude read the CI error logs, traced the issue to a wrong API pattern, and fixed it by switching to the correct SWR data fetching approach.

Bug 2 — PEM Key Parsing: The GitHub App private key stored in environment variables had literal backslash-n characters instead of real newlines. The cryptography library couldn't parse it. Claude added three fallback methods: base64-encoded env var, escaped newline replacement, and file path loading.

Bug 3 — Invisible Repository Selector: Users couldn't see the dropdown to select a GitHub repository. Claude traced it to a variable that was "undefined" being concatenated into API URLs, producing "undefined/api/workspaces/..." — a pre-existing bug from the original Plane codebase that only manifests in self-hosted deployments. Fixed with relative paths.

Bug 4 — Empty Integrations Page: No GitHub or Slack cards appeared because the database had no Integration records. Claude created a data migration to seed them automatically.

Each bug was diagnosed from CI logs or user-reported screenshots, root-caused, and fixed — without being told what to look for.

---

## Act 6: The @Claude Workflow — AI as a GitHub Teammate

The final piece: making Claude a permanent member of the development team on GitHub.

With the Claude Code GitHub Action installed, any team member can mention @claude on a GitHub issue and Claude autonomously:
1. Reads the issue and understands the requirement
2. Explores the codebase to find relevant files
3. Creates a feature branch
4. Implements the changes
5. Opens a pull request with a description
6. Responds to review comments

We demonstrated this live: created a detailed feature request for a "Project-level Analytics Dashboard with Burndown Charts" — complete with API endpoint specifications, component mockups in ASCII, and acceptance criteria. Commented "@claude implement this feature." Within seconds, Claude acknowledged the task, posted a progress checklist, and began working.

This is what the future of software development looks like: AI agents that are always available, never get tired, understand your entire codebase, and deliver working code from a single comment.

---

## Act 7: The Numbers That Matter

Here is the cost and efficiency comparison:

Total tokens processed: 195.4 million
Total API cost: approximately $436
Wall-clock time: approximately 4 hours across planning and implementation sessions

What would this cost with human developers?
A senior full-stack developer: 25 to 30 working days, $15,000 to $25,000
A small team of two developers: 15 to 20 working days, $12,000 to $20,000
A freelance agency: 4 to 6 weeks, $20,000 to $40,000

The AI delivered the same output for approximately 2-3% of the cost and in less than 1% of the time.

But the real value isn't just speed or cost. It's the quality of autonomous execution:
- Claude explored a 500-file brownfield codebase and matched its patterns perfectly
- When production builds failed, Claude diagnosed root causes from CI logs
- Claude created a GitHub App programmatically using the manifest flow
- Claude SSHed into GCP VMs to configure environment variables
- Claude ran Django management commands inside Docker containers on remote servers
- Claude fixed a pre-existing bug from the upstream Plane project that the original developers missed

---

## Closing: The Age of Agentic Engineering

We are at an inflection point. The tools demonstrated here — Claude Code, the BMAD methodology, GitHub Actions integration — are not experimental. They are production-ready today.

The software engineer of tomorrow doesn't write every line of code. They architect systems, define requirements, and orchestrate AI agents that execute at scale. They review pull requests from both human and AI contributors. They focus on the creative and strategic decisions that matter, while AI handles the implementation.

This is not about replacing developers. It's about amplifying them. A single developer with Claude Code can deliver what used to require a team. A team with Claude Code can tackle projects that were previously impossible within their timeline and budget.

The question is no longer "Can AI write production code?" The answer is definitively yes. The question now is: "How fast can your organization adopt this workflow?"

The future of software engineering is agentic. And it's already here.
