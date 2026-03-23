# Claude Conversation Log

Session ID: agent-a5fd5223258a71d46
Date: 2026-03-16 17:12:28

---

## 👤 User

Very thoroughly explore the existing CVS API integration and MCP server in this repository. I need to understand:

1. All MCP tools available (read mcp_server/server.py and mcp_server/tools/*.py)
2. The CVS API client capabilities (read cvs_api/client.py, cvs_api/endpoints/*.py)
3. The current chat agent implementation (read app/chat_agent.py, app/mcp_bridge.py)
4. The current voice implementation (read app/routes/realtime.py, frontend/src/voice/tools.ts)
5. How the current app handles conversation context and state management
6. The data models used (read cvs_api/models.py, frontend/src/types/index.ts)
7. How auth state is managed across the app

Focus on understanding the complete tool/API surface that any new iOS app would need to interact with, and how conversation context flows between components.

---

## 🤖 Claude

I'll conduct a thorough exploration of the CVS API integration, MCP server, and chat agent implementation. Let me start by mapping the repository structure and then diving into each component.

---

## 🤖 Claude

Let me get a better view of the project structure first:

---

## 🤖 Claude

Now let me systematically explore all the key files mentioned. I'll start with the MCP server:

---

## 🤖 Claude

Now let me read the full MCP server file and continue exploring the other components:

---

## 🤖 Claude

Let me continue exploring the other key files:

---

## 🤖 Claude

Now let me explore the data models and authentication handling:

---

## 🤖 Claude

Now let me check the frontend voice implementation and other endpoints:

---

## 🤖 Claude

Let me now check the auth-related tools in the MCP server and examine conversation context handling:

---

## 🤖 Claude

Now let me check the endpoints and CVS API session management:

---

## 🤖 Claude

Let me check one more component - the VoiceContext to understand how voice state is managed:

---

## 🤖 Claude

Perfect! Now I have a comprehensive understanding. Let me create a detailed exploration report:

## Comprehensive CVS API Integration & MCP Server Exploration

I've thoroughly explored the CVS voice scheduling application. Here's a complete breakdown:

---

## 1. MCP TOOLS AVAILABLE

### Vaccine & Eligibility Tools
- **get_eligible_vaccines(date_of_birth)** - Returns available vaccines based on DOB
- **check_vaccine_eligibility(date_of_birth, vaccine_codes)** - Gets NDC codes and eligibility details

### Store & Time Slot Tools
- **search_stores(address, radius, max_results)** - Finds nearby CVS pharmacies with availability
- **get_available_time_slots(visit_date, clinic_id)** - Returns morning/afternoon/evening slots
- **get_store_details(store_id)** - Gets full store info (address, phone, hours)

### Scheduling Workflow Tools
- **soft_reserve_slot(clinic_id, appointment_date, appointment_time)** - Holds time slot
- **submit_patient_details(first_name, last_name, email, phone_number, street_address, city, state, zip_code, gender)** - Saves demographics
- **get_questionnaire()** - Retrieves health screening questions
- **submit_questionnaire(answers)** - Submits questionnaire responses
- **get_user_schedule()** - Checks for duplicate appointments
- **confirm_appointment()** - Final booking confirmation
- **address_typeahead(search_text, max_results)** - Address autocomplete

### Authentication & Account Management Tools
- **login_to_cvs(email, password)** - OTP or password login
- **verify_otp(code)** - Submits 6-digit SMS code (OTP flow)
- **verify_dob(month, day, year)** - Completes OTP authentication
- **get_patient_profile()** - Gets authenticated user's profile
- **get_my_appointments()** - Lists user's upcoming appointments
- **cancel_appointment(appointment_id)** - Cancels an appointment
- **logout()** - Signs out user
- **start_manual_login()** - Opens CVS login in browser
- **check_login_status()** - Polls login completion
- **refresh_session()** - Re-bootstraps if token expired

---

## 2. CVS API CLIENT CAPABILITIES

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/cvs_api/client.py`

### CVSClient Class Architecture
```
CVSClient
├── Bootstrap Methods
│   ├── bootstrap() - Establishes session via: manual token → Playwright → direct acquisition
│   └── refresh_session() - Refreshes expired sessions
├── Vaccine Endpoints
│   ├── get_eligible_vaccines(date_of_birth, flow)
│   └── check_vaccine_eligibility(vaccine_eligibility_input)
├── Store/Slot Endpoints
│   ├── search_stores(address, vaccine_codes, date_of_birth, vaccine_eligibility_data)
│   ├── get_available_time_slots(visit_date, vaccine_codes, store_search_results)
│   └── get_store_details(store_id)
├── Scheduling Endpoints
│   ├── soft_reserve_slot(scheduling_input)
│   ├── submit_patient_details(patient_details_input)
│   ├── get_questionnaire(questionnaire_input)
│   ├── submit_questionnaire(scheduling_questionnaire_input)
│   ├── get_user_schedule(check_duplicate)
│   └── confirm_appointment(confirm_appointment_input)
├── Utility Endpoints
│   └── address_typeahead(search_text, max_results)
├── Authentication
│   ├── login(email) - OTP flow
│   ├── login_with_password(email, password)
│   ├── start_manual_login()
│   ├── check_login_status()
│   ├── submit_otp(code)
│   └── verify_dob(month, day, year)
└── Authenticated Endpoints
    ├── get_patient_profile()
    ├── get_upcoming_appointments(lob_list)
    ├── cancel_appointment(lob, vaccine_ids, confirmation_number)
    └── auth_post() - Proxy through Playwright for cookie-dependent calls
```

### Session Management (CVSSession)
- **Token lifecycle:** Bootstrap token → refresh with buffer → token_valid property
- **Cookie handling:** Guest cookies from Playwright OR authenticated cookies from login browser
- **Fingerprinting:** SHA256 visitor_id hash for request validation
- **Headers:** Dynamic headers including x-visitor-id, x-experienceid, x-client-fingerprint-id

---

## 3. CHAT AGENT IMPLEMENTATION

**Location:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/chat_agent.py`

### stream_response() Flow
1. Saves user message to DB
2. Auto-titles conversation on first message
3. Loads full conversation history
4. Converts to OpenAI format with system prompt
5. Calls GPT-4o with MCP tool definitions
6. Accumulates tool calls from streaming response
7. Executes tools via MCP bridge if finish_reason == "tool_calls"
8. Saves tool_call and tool_result entries to DB
9. Loops back to step 4 with updated messages (MAX 8 rounds)
10. Yields StreamEvent dicts:
    - `{"type": "chunk", "content": "..."}` - Streamed text
    - `{"type": "tool_start", "name": "...", "display": "..."}` - Tool execution started
    - `{"type": "tool_result", "name": "...", "summary": "..."}` - Tool completed
    - `{"type": "done", "message_id": "...", "full_content": "..."}` - Response complete
    - `{"type": "error", "message": "..."}` - Error occurred

### Context Building
- **_build_system_prompt()** - Dynamically injects authenticated user info if logged in
  - Pre-fills user name, email, DOB, phone, address, gender
  - Tells agent NOT to ask for login or re-request cached info
  - Guides agent to use cached profile for scheduling

- **_build_openai_messages()** - Reconstructs conversation with proper roles:
  - Rebuilds tool_call messages with id, name, arguments from DB
  - Rebuilds tool_result messages with tool_call_id and content

---

## 4. VOICE IMPLEMENTATION

**MCP Bridge (Frontend Integration):** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/mcp_bridge.py`
- Connects to MCP server at `MCP_SERVER_URL` (default: http://localhost:8001/mcp)
- Caches tool definitions in OpenAI function format
- Maps tool names to schemas
- Executes tools and syncs auth state on login/logout

**Voice Realtime Endpoint:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/realtime.py`

```python
GET /api/realtime/token
  Returns: {"key", "instructions", "voice", "tools"}
  - Generates ephemeral OpenAI client key
  - Builds voice-optimized system prompt (NO login tools for security)
  - Filters tools (excludes: login_to_cvs, verify_otp, verify_dob, etc.)
  - Returns voice="coral"

POST /api/realtime/tool-call
  {name: str, arguments: dict}
  - Proxies tool calls to MCP server
  - Used by voice agent's tool() execute functions in browser

POST /api/realtime/conversations/{conversation_id}/messages
  {messages: [{role, content}, ...]}
  - Persists voice transcript to conversation DB
  - Called when voice session ends
```

**Frontend Voice Context:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/contexts/VoiceContext.tsx`

```typescript
VoiceProvider
├── State
│   ├── voiceState: 'idle' | 'connecting' | 'active' | 'error'
│   ├── isMuted: boolean
│   ├── transcript: TranscriptEntry[]  // user/assistant messages
│   └── currentToolName: string | null
├── startVoice(conversationId, textHistory)
│   1. Fetches ephemeral token from /api/realtime/token
│   2. Creates RealtimeAgent with voice tools
│   3. Creates RealtimeSession with semantic VAD (voice activity detection)
│   4. Injects text history (last 10 messages) for context
│   5. Listens to history_updated, tool_start/end, error events
└── stopVoice()
    1. Extracts final transcript from session history
    2. Closes session
    3. POSTs transcript to /api/realtime/conversations/{id}/messages
    4. Calls onSessionEnd callback
```

**Voice Tools Definitions:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/voice/tools.ts`
- 15 tools defined using Zod schemas + openai/agents tool() wrapper
- Each calls `/api/realtime/tool-call` endpoint
- Excludes auth tools (login_to_cvs, verify_otp, verify_dob, etc.)

---

## 5. CONVERSATION CONTEXT & STATE MANAGEMENT

### Context Flow
```
User Message (WebSocket)
  → chat_agent.stream_response(conversation_id, user_message)
    → db.add_message(conversation_id, "user", message)
    → db.get_messages(conversation_id)  [full history]
    → _build_system_prompt()  [dynamic auth context]
    → _build_openai_messages()  [reconstruct with roles]
    → openai.chat.completions.create(model, messages, tools)
    → mcp_bridge.call_tool(tool_name, arguments)
    → db.add_message(conversation_id, "tool_call", tool_name, args)
    → db.add_message(conversation_id, "tool_result", result)
    → re-loop if finish_reason == "tool_calls"
    → Stream events back to client
    → Final: db.add_message(conversation_id, "assistant", full_content)
```

### Database Schema
```sql
conversations
  id (UUID)
  title (auto-generated from first user message)
  theme ('red' or 'blue')
  created_at, updated_at

messages
  id (UUID)
  conversation_id (FK)
  role ('user' | 'assistant' | 'tool_call' | 'tool_result')
  content (text)
  tool_name (nullable)
  tool_call_id (nullable)
  tool_args (JSON)
  tool_result (JSON)
  created_at
```

### Message Role Types
- **user** - Content from user
- **assistant** - Response text from GPT-4o
- **tool_call** - Tool invocation with args
- **tool_result** - Tool execution result

---

## 6. DATA MODELS

**CVS API Models:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/cvs_api/models.py`

```
Vaccine
  code, name, type, ndc[], manufacturers[], age_restriction, dosage_info, series, lob

EligibleVaccinesResponse
  eligible_vaccine_data[]

Clinic
  clinic_id, store_id, store_number, address{}, distance, available_dates[], scheduling_dates[]

TimeSlotDetail
  visit_date, morning[], afternoon[], evening[], earliest[]

PatientInput
  patientReferenceId, firstName, middleName, lastName, gender, dateOfBirth,
  email, phoneNumber, address{city, state, postalCode, line[]}

ConfirmationResponse
  statusCode, statusDescription, responseDetails

CVSAPIResponse
  statusCode, statusDescription, data{}
```

**Frontend Types:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/types/index.ts`

```typescript
Conversation { id, title, theme, created_at, updated_at }
Message { id, conversation_id, role, content, tool_name?, tool_call_id?, tool_args?, tool_result?, created_at }
TranscriptEntry { role, text, timestamp, isFinal }
VoiceState: 'idle' | 'connecting' | 'active' | 'error'
WSEvent: chunk | tool_start | tool_result | done | error | pong | conversation_created
```

---

## 7. AUTH STATE MANAGEMENT

### Server-Side Auth State
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/app/config.py`

```python
_auth_state: dict = {
  "authenticated": bool,
  "profile": {
    "firstName": str,
    "lastName": str,
    "email": str,
    "dateOfBirth": str,  # YYYY-MM-DD
    "phone": str,
    "gender": str,
    "address": {
      "street": str,
      "city": str,
      "state": str,
      "zip": str
    }
  }
}

Functions:
  set_auth_state(authenticated, profile)
  get_auth_state() → dict (copy)
```

### Auth Flow
```
Frontend POST /api/auth/start-login
  → mcp_bridge.call_tool("start_manual_login", {})
  → Opens CVS login in Playwright browser
  → Returns {"status": "browser_opened"}

Frontend GET /api/auth/status (poll every 3s)
  → mcp_bridge.call_tool("check_login_status", {})
  → If authenticated:
    ├── set_auth_state(authenticated=True, profile=...)
    └── Returns profile with firstName, lastName, email, dateOfBirth
  → Updates frontend auth context

Frontend POST /api/auth/logout
  → mcp_bridge.call_tool("logout", {})
  → set_auth_state(authenticated=False, profile=None)
```

### Auth Context (Frontend)
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/contexts/AuthContext.tsx`

```typescript
AuthState {
  isAuthenticated: boolean
  isLoggingIn: boolean
  user: UserProfile {firstName, lastName, email, dateOfBirth} | null
  error: string | null
}

Methods:
  startLogin() - Opens browser, polls status
  logout() - Clears auth
  cancelLogin() - Stops polling, clears error
```

### MCP Session Cache (Server-Side)
**Location:** `/Users/sarathfrancis/work/git/innovation_lab/mcp_server/server.py`

```python
_session_cache = {
  # Guest scheduling
  "date_of_birth": str | None
  "vaccine_codes": list[str] | None
  "vaccine_eligibility_data": dict | None
  "store_search_results": dict | None
  "reservation": dict | None
  "selected_clinic": dict | None
  "appointment_date": str | None
  "appointment_time": str | None
  "patient_details_submitted": bool
  "questionnaire_data": dict | None
  "questionnaire_submitted": bool
  
  # Authenticated
  "authenticated": bool
  "patient_profile": dict | None
  "appointments": list[dict] | None
}
```

**Cache Purpose:** Server avoids asking LLM to pass 50KB JSON payloads between steps. Tools automatically inject cached data into API payloads.

---

## 8. API ENDPOINTS SUMMARY

### Conversations
```
GET    /api/conversations              - List all conversations
POST   /api/conversations              - Create conversation
GET    /api/conversations/{id}         - Get conversation + messages
PATCH  /api/conversations/{id}         - Update title/theme
DELETE /api/conversations/{id}         - Delete conversation
WS     /ws/chat/{conversation_id}      - Chat WebSocket
```

### Authentication
```
POST   /api/auth/start-login           - Open login browser
GET    /api/auth/status                - Poll login completion
POST   /api/auth/logout                - Sign out
```

### Voice/Realtime
```
GET    /api/realtime/token             - Get ephemeral key + tools + instructions
POST   /api/realtime/tool-call         - Execute MCP tool from voice
POST   /api/realtime/conversations/{id}/messages - Save voice transcript
```

---

## 9. COMPLETE TOOL/API SURFACE FOR iOS APP

An iOS app would need to support:

### Phase 1: Core Scheduling (Guest)
1. `GET_ELIGIBLE_VACCINES(dob)` → returns vaccine list
2. `CHECK_VACCINE_ELIGIBILITY(dob, vaccine_codes)` → returns NDC codes
3. `SEARCH_STORES(address, vaccine_codes)` → returns clinics with availability
4. `GET_AVAILABLE_TIME_SLOTS(visit_date)` → returns morning/afternoon/evening slots
5. `SOFT_RESERVE_SLOT(clinic_id, date, time)` → holds reservation
6. `SUBMIT_PATIENT_DETAILS(name, email, phone, address, gender)` → saves demographics
7. `GET_QUESTIONNAIRE()` → returns health screening questions
8. `SUBMIT_QUESTIONNAIRE(answers)` → submits responses
9. `CONFIRM_APPOINTMENT()` → final booking

### Phase 2: Authentication
1. `LOGIN_TO_CVS(email, password?)` → OTP or password
2. `VERIFY_OTP(code)` → 6-digit code
3. `VERIFY_DOB(month, day, year)` → DOB verification
4. `GET_PATIENT_PROFILE()` → fetch user profile
5. `LOGOUT()` → clear auth

### Phase 3: Account Management
1. `GET_MY_APPOINTMENTS()` → list upcoming appointments
2. `CANCEL_APPOINTMENT(appointment_id)` → cancel specific appointment

### Phase 4: Utilities
1. `ADDRESS_TYPEAHEAD(search_text)` → autocomplete addresses
2. `GET_STORE_DETAILS(store_id)` → store info
3. `GET_USER_SCHEDULE()` → duplicate detection

---

## 10. KEY ARCHITECTURAL INSIGHTS

### Conversation Context Flow
- **Stateless HTTP + Stateful DB**: Conversation ID + message history in DB reconstructs context on each request
- **Tool chaining**: LLM gets full message history including previous tool calls and results
- **Automatic caching**: MCP server caches large payloads (vaccine eligibility, store search) so LLM doesn't pass them
- **Dynamic prompting**: System prompt includes authenticated user info if logged in

### Voice Integration
- **Parallel channels**: WebSocket chat AND voice realtime can run independently
- **Transcript persistence**: Voice messages auto-saved to conversation DB
- **Tool filtering**: Auth tools excluded from voice (security + usability)
- **Token ephemeral**: New ephemeral key generated per voice session

### Auth State Synchronization
- **Server-side cache**: Auth state stored in app/config.py
- **Profile injection**: Authenticated user details injected into:
  - System prompt (to personalize responses)
  - Tool execution (to pre-fill patient details)
  - Conversation context (for addressing by first name)
- **Cookie lifecycle**: Auth cookies tied to Playwright browser for Akamai compliance

### Session Resilience
- **Token refresh**: Auto-refresh if token expired
- **Bootstrap retry**: 3 attempts with exponential backoff
- **Fallback**: Manual token from env var if Playwright unavailable
- **Auth browser**: Separate Playwright instance for authenticated API calls (TLS fingerprinting)

---

## 11. CRITICAL FILES FOR iOS INTEGRATION

| File | Purpose |
|------|---------|
| `/mcp_server/server.py` | MCP tool definitions (24+ tools) |
| `/app/mcp_bridge.py` | Tool execution and auth sync |
| `/app/chat_agent.py` | LLM orchestration + streaming |
| `/app/routes/realtime.py` | Voice token + tool-call proxy |
| `/cvs_api/client.py` | CVS API wrapper (all endpoints) |
| `/cvs_api/session.py` | Token/cookie lifecycle |
| `/app/database.py` | Conversation + message persistence |
| `/app/routes/auth.py` | Login/logout endpoints |
| `/app/config.py` | Auth state + system prompts |
| `/frontend/src/voice/tools.ts` | Voice tool schemas |

---

This comprehensive exploration covers all aspects an iOS app would need to replicate or integrate with. The key takeaway: context flows from frontend → conversation DB → chat agent → MCP server → CVS API, with auth state synchronized globally and tools automatically chaining data via server-side caching.

---

