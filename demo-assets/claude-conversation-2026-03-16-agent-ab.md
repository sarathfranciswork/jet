# Claude Conversation Log

Session ID: agent-ab4a3a61657ccdb1d
Date: 2026-03-16 15:48:05

---

## 👤 User

Do a very thorough exploration of this repository. I need to understand:
1. The full directory structure
2. All configuration files (package.json, tsconfig, docker, etc.)
3. The tech stack and frameworks used
4. The app architecture
5. Key source files and their purposes
6. Testing setup
7. Build/deployment configuration
8. Any existing .claude or CLAUDE.md files
9. Environment variables and secrets patterns
10. API integrations

Start with listing the top-level directory, then explore each major directory. Read key config files like package.json, any docker files, any CI/CD configs, etc.

---

## 🤖 Claude

I'll conduct a thorough exploration of this repository. Let me start by examining the top-level directory structure and then dive into the major components.

---

## 🤖 Claude

Now let me explore the directory structure more systematically and check for key configuration files.

---

## 🤖 Claude

Let me look for more config files and get a better sense of the directory structure.

---

## 🤖 Claude

Good, I can see the main directories. Now let me read the key configuration files and explore each major directory.

---

## 🤖 Claude

Excellent! Now let me explore the directory structure of each major component and check for more config files.

---

## 🤖 Claude

Great! Now let me read some key files to understand the architecture and tech stack better.

---

## 🤖 Claude

Let me continue exploring the frontend, database, and other key files.

---

## 🤖 Claude

Let me explore more of the architecture, test setup, and check for deployment configs.

---

## 🤖 Claude

Let me check the documentation files and explore the CVS API structure in more detail.

---

## 🤖 Claude

Now let me explore more of the API structure and check for test files.

---

## 🤖 Claude

Let me explore a few more key areas - the CVS API endpoints, voice setup, and authentication routes.

---

## 🤖 Claude

Excellent! Let me check the realtime API and get a complete picture of the frontend components.

---

## 🤖 Claude

Perfect! Let me check a couple more key areas - the MCP server tools and the bootstrap process.

---

## 🤖 Claude

Perfect! Now let me check the project structure and create a comprehensive summary. Let me look at one more thing - the frontend API layer.

---

## 🤖 Claude

Perfect! I now have a comprehensive understanding of the repository. Let me create a final summary document.

## Comprehensive Repository Exploration Report

I've conducted a thorough exploration of the CVS Voice Scheduling application. Here's a complete breakdown of the repository structure, architecture, and technology stack:

### 1. DIRECTORY STRUCTURE

```
voice-scheduling/
├── app/                    # FastAPI backend for chat & auth
├── capture/               # Phase 1: Network traffic capture (mitmproxy)
├── cvs_api/              # Phase 2: CVS API wrappers & session management
├── mcp_server/           # Phase 2: MCP server exposing CVS API as tools
├── frontend/             # Phase 3: React + TypeScript + Vite UI
├── docs/                 # Documentation (A2UI protocol)
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── CVS.png              # Logo/diagram
```

### 2. CONFIGURATION FILES

**Environment Variables (.env.example)**
- `OPENAI_API_KEY`: OpenAI API credentials
- `MCP_SERVER_URL`: MCP server endpoint (http://localhost:8001/mcp)
- `CVS_AUTO_BOOTSTRAP`: Auto-launch Playwright for session bootstrap
- `CVS_GUEST_TOKEN`: Manual guest token (optional, expires ~15 min)

**Python Dependencies (requirements.txt)**
- **Phase 1**: mitmproxy>=10.0
- **Phase 2**: httpx>=0.27, pydantic>=2.0, fastmcp>=2.0, uvicorn>=0.30
- **Phase 3**: fastapi>=0.115, websockets>=12.0, openai>=1.50, aiosqlite>=0.20, python-dotenv>=1.0
- **Bootstrap**: playwright>=1.40

**Frontend (package.json)**
- React 19.2.0 + TypeScript 5.9.3
- Vite 7.3.1 (build tool with HMR)
- Tailwind CSS 4.2.0 (styling)
- ESLint + TypeScript-ESLint (linting)
- @openai/agents 0.4.14 (OpenAI Realtime integration)
- Zod 4.3.6 (TypeScript-first schema validation)

**Frontend TypeScript Config (tsconfig.json)**
- Two configs: tsconfig.app.json (app) & tsconfig.node.json (build tools)

**Frontend Build (vite.config.ts)**
- Port 5173 for dev server
- API proxy: /api → http://localhost:8000
- WebSocket proxy: /ws → ws://localhost:8000

### 3. TECH STACK OVERVIEW

**Backend (Python)**
- **Framework**: FastAPI (async, WebSocket support)
- **Web Server**: Uvicorn
- **Database**: SQLite with aiosqlite (async)
- **Browser Automation**: Playwright (anti-detection stealth mode)
- **HTTP Client**: httpx (async)
- **API Integration**: fastmcp (MCP server framework)
- **OpenAI Integration**: openai SDK (GPT-4o, Realtime)
- **Config Management**: python-dotenv

**Frontend (TypeScript/React)**
- **Framework**: React 19 (with hooks)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Type Safety**: TypeScript + Zod
- **State Management**: React Context (ChatContext, AuthContext, VoiceContext, ThemeContext)
- **Voice Integration**: OpenAI Realtime Agents (@openai/agents)

**CVS API Integration**
- **Session Management**: Guest tokens + Akamai cookie fingerprinting
- **Authentication**: OTP (SMS) + Password + Manual browser login
- **Browser Emulation**: Playwright headless + stealth JS injection

### 4. APPLICATION ARCHITECTURE

**Three-Phase Architecture:**

**Phase 1: API Capture (capture/)**
- Network traffic analysis with mitmproxy
- Extracts CVS API endpoints, request/response patterns
- Files: `mitmproxy_addon.py`, `analyze_capture.py`, `start_capture.sh`

**Phase 2: API Wrappers + MCP Server (cvs_api/ + mcp_server/)**

CVS API Layer (cvs_api/):
- **client.py**: High-level async CVSClient interface
- **session.py**: Guest token lifecycle, fingerprint, auth cookies
- **bootstrap.py**: PlaywrightBootstrapper (guest) + AuthenticatedBootstrapper (login)
- **config.py**: Base URLs, API keys, experience UUIDs, default headers
- **endpoints/**:
  - vaccines.py: Eligibility checking
  - stores.py: Store search, time slots
  - scheduling.py: Slot reservation, patient details, questionnaire, confirmation
  - appointments.py: Authenticated profile, appointments, cancellation
- **exceptions.py**: Custom error types (AuthenticationError, SessionExpiredError, etc.)
- **models.py**: Pydantic data structures

MCP Server (mcp_server/):
- Exposes CVS API as MCP tools via FastMCP
- HTTP transport on port 8001
- Tools wrapped in mcp_server/tools/:
  - scheduling_tools.py
  - vaccine_tools.py
  - store_tools.py
- Server startup: `python -m mcp_server.server`

**Phase 3: Chat Assistant + Frontend (app/ + frontend/)**

Backend (app/):
- **main.py**: FastAPI app entry point, CORS, static file serving
- **config.py**: Configuration loader, SYSTEM_PROMPT, VOICE_SYSTEM_PROMPT
- **database.py**: SQLite conversation/message persistence (aiosqlite)
- **chat_agent.py**: OpenAI Chat Completions orchestration with streaming
- **mcp_bridge.py**: Connection to MCP server, tool discovery, tool execution
- **routes/**:
  - auth.py: CVS login flow endpoints (/api/auth/start-login, /api/auth/status, /api/auth/logout)
  - conversations.py: Conversation CRUD endpoints
  - chat_ws.py: WebSocket endpoint for real-time chat streaming (/ws/chat/{conversation_id})
  - realtime.py: Voice mode endpoints (/api/realtime/token, /api/realtime/tool-call, transcript saving)

Frontend (frontend/):
- **App.tsx**: Root component with provider nesting
- **contexts/**:
  - AuthContext.tsx: Authentication state (login, logout, profile)
  - ChatContext.tsx: Conversation list, messages, WebSocket management
  - VoiceContext.tsx: Voice session state (recording, agent state)
  - ThemeContext.tsx: Light/dark mode toggle
- **components/**:
  - Layout/: Main app layout structure
  - Chat/: ChatArea, MessageBubble, TypingIndicator, ToolIndicator
  - Sidebar/: Conversation list, ConversationItem
  - Header/: Nav, login button
  - Input/: ChatInput component
  - Voice/: VoiceOrb, VoicePanel (OpenAI Realtime UI)
  - Auth/: LoginOverlay
- **voice/tools.ts**: OpenAI Realtime tool definitions (Zod schemas + execute functions)
- **api/conversations.ts**: REST client for conversation endpoints
- **lib/markdown.ts**: Markdown parsing utility
- **types/index.ts**: TypeScript interfaces (Conversation, Message, etc.)

### 5. KEY SOURCE FILES & PURPOSES

**Backend Core Files:**
- `/app/main.py`: FastAPI app, lifespan hooks, database/MCP initialization
- `/app/config.py`: Environment config, system prompts for chat & voice
- `/app/database.py`: SQLite schema (conversations, messages), CRUD operations
- `/app/chat_agent.py`: OpenAI streaming with tool-call loop
- `/app/mcp_bridge.py`: MCP client, tool schema conversion, tool execution
- `/app/routes/chat_ws.py`: WebSocket real-time chat streaming
- `/app/routes/realtime.py`: OpenAI Realtime ephemeral keys, tool proxy, transcript storage
- `/app/routes/auth.py`: CVS login redirect flow

**CVS API Files:**
- `/cvs_api/client.py`: Async CVSClient with all scheduling workflows
- `/cvs_api/session.py`: Token management, cookie injection, auth state
- `/cvs_api/bootstrap.py`: Playwright automation (guest + authenticated login)
- `/cvs_api/config.py`: CVS API keys, UUIDs, headers, endpoints
- `/cvs_api/endpoints/vaccines.py`: Vaccine eligibility queries
- `/cvs_api/endpoints/stores.py`: Store search, time slot availability
- `/cvs_api/endpoints/scheduling.py`: Slot reservation, patient details, questionnaire, confirmation
- `/cvs_api/endpoints/appointments.py`: Authenticated profile, appointments, cancellation

**MCP Server Files:**
- `/mcp_server/server.py`: FastMCP application with tool definitions
- `/mcp_server/__main__.py`: Entry point (uvicorn runner)
- `/mcp_server/tools/*.py`: Tool implementations (scheduling, vaccines, stores)

**Frontend Core Files:**
- `/frontend/src/App.tsx`: Root component
- `/frontend/src/main.tsx`: React bootstrap
- `/frontend/src/types/index.ts`: TypeScript interfaces
- `/frontend/src/contexts/*.tsx`: State management contexts
- `/frontend/src/components/**/*.tsx`: UI components
- `/frontend/src/voice/tools.ts`: OpenAI Realtime tool defs
- `/frontend/src/api/conversations.ts`: REST client
- `/frontend/vite.config.ts`: Vite configuration

### 6. TESTING SETUP

**Status**: No test files found in the repository
- No pytest.ini, setup.py, or pyproject.toml
- No test/ directory
- No *_test.py or *_spec.ts files
- Application appears to rely on manual testing and real CVS API integration

### 7. BUILD & DEPLOYMENT CONFIGURATION

**Build Process:**
- Frontend: `npm run build` (TypeScript compile + Vite bundle → frontend/dist/)
- Backend: Direct uvicorn execution, no build step
- MCP Server: Direct Python execution

**Development Servers:**
- Frontend dev: `npm run dev` (Vite, port 5173)
- Backend: `python app/main.py` (Uvicorn, port 8000)
- MCP Server: `python -m mcp_server.server` (Uvicorn, port 8001)

**Static Files:**
- Frontend built dist/ served by FastAPI at root path
- Frontend dev proxies API/WS to backend

**No Docker/CI-CD:**
- No Dockerfile, docker-compose.yml, or GitHub Actions workflows found
- Designed for local development and manual deployment

### 8. .CLAUDE & CLAUDE.MD FILES

**Status**: None found
- No .claude directory
- No CLAUDE.md documentation
- Open for project-specific Claude Code documentation

### 9. ENVIRONMENT VARIABLES & SECRETS

**Required in .env:**
- `OPENAI_API_KEY`: sk-proj-* (OpenAI API credentials)
- `MCP_SERVER_URL`: http://localhost:8001/mcp (MCP server location)
- `CVS_AUTO_BOOTSTRAP`: true/false (Playwright automation toggle)

**Optional:**
- `CVS_GUEST_TOKEN`: Manual token (bypasses Playwright, expires ~15 min)
- `DATABASE_PATH`: SQLite location (default: data/chat.db)
- `API_HOST`: Backend host (default: 0.0.0.0)
- `API_PORT`: Backend port (default: 8000)
- `OPENAI_MODEL`: LLM model (default: gpt-5.2)

**Sensitive Data in .gitignore:**
- .env (not committed)
- __pycache__, *.pyc
- node_modules, frontend/dist
- data/ (SQLite database)
- .cvs_auth_browser/ (Playwright browser profile)
- capture/raw_flows/, *.har (captured traffic)
- .mitmproxy/

### 10. API INTEGRATIONS

**OpenAI Integration:**
1. **Chat Completions API**: Streaming GPT-4o with function calling
2. **Realtime API**: WebRTC voice sessions with gpt-realtime model
   - Ephemeral keys generated at `/api/realtime/token`
   - Tool calling via `/api/realtime/tool-call` proxy
   - Voice model: "coral"

**CVS Pharmacy API:**
- Base: https://www.cvs.com
- Guest scheduling (no auth)
- Authenticated scheduling (OTP + password)
- Akamai anti-bot fingerprinting (Playwright-based TLS fingerprint)
- Endpoints:
  - /api/guest/v1/token: Guest token acquisition
  - /scheduling/client/experience/v2/load: Guest experience API
  - /api/locator/v2/stores: Store search
  - /api/unified/scheduling/v2/content: Content/pricing
  - /api/auth/experience/v2/load: Authenticated operations

**System Architecture Flow:**
```
Frontend (React + Realtime API)
    ↓
FastAPI Backend (chat_agent + mcp_bridge)
    ↓
MCP Server (tools)
    ↓
CVS API Client (cvs_api)
    ↓
CVS.com (Playwright session)
```

---

### Key Absolute File Paths

**Python Files (34 total):**
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/*.py
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/cvs_api/**/*.py
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/mcp_server/**/*.py
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/capture/*.py

**TypeScript Files (22 total):**
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/**/*.tsx
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/**/*.ts

**Configuration Files:**
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/package.json (root frontend)
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/requirements.txt
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/.env.example
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/package.json
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/tsconfig.json
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/vite.config.ts

This is a production-grade voice-first AI application for vaccine scheduling at CVS Pharmacy locations, featuring real-time voice conversations, multi-modal chat, and deep CVS API integration via MCP tools.

---

