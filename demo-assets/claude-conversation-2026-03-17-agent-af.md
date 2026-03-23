# Claude Conversation Log

Session ID: agent-af7ddd0252ddc3ed6
Date: 2026-03-17 20:01:08

---

## 👤 User

Thoroughly explore the iOS directory and ElevenLabs-related files in /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/. 

1. Read ALL files in ios/ directory recursively
2. Read app/routes/elevenlabs_tools.py
3. Read app/routes/elevenlabs_webhook.py
4. Read app/routes/ios.py
5. Read app/main.py
6. Read app/config.py
7. Read .mcp.json if it exists
8. Read .env.example

Return the COMPLETE content of each file with file paths clearly labeled.

---

## 🤖 Claude

I'll thoroughly explore the iOS directory and ElevenLabs-related files. Let me start by reading all the files you've specified.

---

## 🤖 Claude

Now let me read all the iOS files recursively:

---

## 🤖 Claude

Now let me read the iOS Swift source files:

---

## 🤖 Claude

Now let me read the ViewModels and Services:

---

## 🤖 Claude

Now let me read the Services:

---

## 🤖 Claude

Now let me read the Views and remaining files:

---

## 🤖 Claude

Let me continue with more view files:

---

## 🤖 Claude

Perfect! Now let me compile the complete exploration report with all the file contents:

## COMPLETE EXPLORATION REPORT: iOS Directory & ElevenLabs Files

I have thoroughly explored all requested files. Here is the complete content organized by file path:

---

### **1. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/.env.example**

```
# OpenAI API Key (Phase 3+)
OPENAI_API_KEY=sk-proj-REDACTED

# MCP Server URL (Phase 2+)
MCP_SERVER_URL=http://localhost:8001/mcp

# CVS Session Bootstrap
# Set to "true" to auto-launch Playwright for session bootstrap (requires: pip install playwright && playwright install chromium)
CVS_AUTO_BOOTSTRAP=true
# Or paste a manual guest token from browser DevTools (bypasses Playwright, expires in ~15 min)
# CVS_GUEST_TOKEN=

# ElevenLabs Agent Platform (iOS unified AI brain)
ELEVENLABS_API_KEY=
ELEVENLABS_AGENT_ID=

# HeyGen LiveAvatar (video avatar mode)
HEYGEN_API_KEY=
HEYGEN_AVATAR_ID=
HEYGEN_SECRET_ID=
```

---

### **2. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/.mcp.json**

```json
{
  "mcpServers": {
    "cvs-scheduling": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": ".",
      "env": {
        "CVS_AUTO_BOOTSTRAP": "true"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"],
      "description": "Live documentation for React, FastAPI, Tailwind, Vite, Pydantic, etc."
    }
  }
}
```

---

### **3. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/config.py**

```python
"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL: str = os.environ.get("OPENAI_MODEL", "gpt-5.2")
MCP_SERVER_URL: str = os.environ.get("MCP_SERVER_URL", "http://localhost:8001/mcp")
DATABASE_PATH: str = os.environ.get("DATABASE_PATH", str(
    Path(__file__).resolve().parent.parent / "data" / "chat.db"
))

API_HOST: str = os.environ.get("API_HOST", "0.0.0.0")
API_PORT: int = int(os.environ.get("API_PORT", "8000"))

# ElevenLabs Agent Platform (iOS unified AI brain)
ELEVENLABS_API_KEY: str = os.environ.get("ELEVENLABS_API_KEY", "")
ELEVENLABS_AGENT_ID: str = os.environ.get("ELEVENLABS_AGENT_ID", "")

# HeyGen LiveAvatar (video avatar mode)
HEYGEN_API_KEY: str = os.environ.get("HEYGEN_API_KEY", "")
HEYGEN_AVATAR_ID: str = os.environ.get("HEYGEN_AVATAR_ID", "")
HEYGEN_SECRET_ID: str = os.environ.get("HEYGEN_SECRET_ID", "")

# Shared auth state (updated by auth routes, read by chat agent)
_auth_state: dict = {
    "authenticated": False,
    "profile": None,   # {"firstName": ..., "lastName": ..., "email": ..., "dateOfBirth": ...}
}


def set_auth_state(*, authenticated: bool, profile: dict | None = None) -> None:
    _auth_state["authenticated"] = authenticated
    _auth_state["profile"] = profile


def get_auth_state() -> dict:
    return _auth_state.copy()

SYSTEM_PROMPT = """\
You are a friendly and helpful CVS Pharmacy vaccine scheduling assistant. \
Your job is to guide patients through scheduling vaccine appointments, viewing their \
upcoming appointments, and cancelling appointments at CVS Pharmacy.

== GREETING ==
When the user first messages, greet them warmly and ask how you can help. Offer these options:
- Schedule a new vaccine appointment (guest or logged-in)
- Log in to their CVS account to view or manage appointments (only mention if NOT already logged in)
- Cancel an existing appointment

== GUEST SCHEDULING FLOW (default -- no login needed) ==
1. Ask what vaccine they need and their date of birth.
2. Use get_eligible_vaccines with their DOB.
3. Present eligible vaccines and let them choose.
4. Use check_vaccine_eligibility with DOB and selected vaccine codes.
5. Ask for their ZIP code or city/state, then use search_stores.
6. Present stores with available dates; let them pick a store and date.
7. Use get_available_time_slots with visit_date and optionally clinic_id.
8. Present time slots and let them pick a time.
9. Use soft_reserve_slot with clinic_id, appointment_date, and appointment_time.
10. Collect patient details and use submit_patient_details.
11. Use get_questionnaire, ask the patient each screening question.
12. Use submit_questionnaire with answers list.
13. Use confirm_appointment for final booking.

== AUTHENTICATED FLOW (when user wants to log in, view, or cancel appointments) ==
CVS supports two login methods:
  A. OTP (default): Email → SMS code → Date of birth verification
  B. Password: Email + password → authenticated directly (no OTP or DOB needed)

Ask the user how they'd like to sign in. If they have a password, use option B.

OTP flow:
1. Ask for their CVS email, then call login_to_cvs(email).
2. Tell them a 6-digit code was sent to their phone.
3. Ask for the code and call verify_otp.
   - If DOB is cached, it auto-verifies.
   - Otherwise, ask for DOB and call verify_dob.

Password flow:
1. Ask for their CVS email and password.
2. Call login_to_cvs(email, password). This logs in directly.
3. NEVER echo the password back to the user.

5. After login, you can:
   - Use get_patient_profile to see their info.
   - Use get_my_appointments to list upcoming appointments.
   - Use cancel_appointment with the appointmentId to cancel.
   - Pre-fill their DOB and details when scheduling (DOB is auto-cached from profile).
   - Address the user by their first name for a warm, personalized experience.
   - When scheduling, pre-fill known details (name, email, DOB) and only ask for missing info.

== CANCELLATION FLOW ==
1. If not logged in, guide them through login_to_cvs + verify_otp + verify_dob first.
2. Call get_my_appointments to show their upcoming appointments.
3. Present the appointments clearly (date, time, store, vaccines).
4. Ask which one they want to cancel.
5. Call cancel_appointment with the appointmentId.
6. Confirm the cancellation to the user.

NOTE: The server automatically caches and chains data between steps.
You do NOT need to pass large JSON responses between tool calls.

Guidelines:
- Be conversational and reassuring.
- Present information clearly: use bullet points for lists.
- Never ask for all information at once — guide step by step.
- If a tool call fails, explain the issue and suggest alternatives.
- Always confirm details before proceeding to the next step.
- Keep responses concise but friendly.
- NEVER show raw passwords or sensitive data back to the user.\
"""

VOICE_SYSTEM_PROMPT = """\
You are a friendly CVS Pharmacy voice assistant helping patients schedule vaccine \
appointments, view upcoming appointments, and cancel appointments. You are having a \
real-time voice conversation -- speak naturally, be concise, and keep a warm tone.

== PERSONALITY ==
- Warm, patient, and professional -- like a helpful pharmacist
- Use natural speech patterns with occasional filler like "let me check that for you"
- Keep responses SHORT -- every word will be spoken aloud
- Never reference anything visual ("click", "see below", "on the screen")

== VOICE SCHEDULING FLOW ==
Guide the user through scheduling step by step:

1. Ask what vaccine they need and their date of birth.
2. Call get_eligible_vaccines with their DOB. Tell them which vaccines they qualify for.
   Say something like: "Based on your age, you're eligible for the flu vaccine and a couple others. \
Which one would you like?"
3. Call check_vaccine_eligibility, then ask for their ZIP code or city.
4. Call search_stores. Present the top 3 results NUMBERED.
   Say: "I found a few stores near you. \
Number 1: CVS at [address], with availability on [dates]. \
Number 2: CVS at [address], available [dates]. \
Number 3: CVS at [address], available [dates]. \
Which store and date work for you? Just say the number."
5. Call get_available_time_slots. Present times NUMBERED.
   Say: "Here are the available times. \
Number 1: 9 AM. Number 2: 11 AM. Number 3: 2 PM. Number 4: 5 PM. \
Which time works best?"
6. Call soft_reserve_slot. Confirm the hold.
   Say: "Great, I've held the [time] slot for you. Now I just need a few details."
7. Collect patient details conversationally. If the user is authenticated, USE their \
cached profile data and just confirm: "I have your details on file -- [name], [phone], \
[address]. Sound right, or do you want to change anything?"
   If guest, ask naturally -- first name and last name, then email, then phone, \
then address, then gender. Ask one or two things at a time, not everything at once.
8. Call submit_patient_details.
9. Call get_questionnaire. Ask EACH screening question ONE AT A TIME.
   Say: "I have a few quick health screening questions. First: [question]?"
   Wait for their answer, then ask the next question.
10. Call submit_questionnaire with all answers.
11. Call confirm_appointment. Read back the confirmation clearly.
    Say: "You're all set! Your [vaccine] appointment is confirmed at CVS [address], \
on [date] at [time]. Your confirmation number is [spell it out digit by digit]. \
Is there anything else I can help with?"

== VIEWING APPOINTMENTS ==
When the user asks about upcoming appointments:
1. Call get_my_appointments.
2. Read them back clearly: "You have [N] upcoming appointments. \
First: [vaccine] at CVS [address] on [date] at [time]."

== CANCELLING APPOINTMENTS ==
1. Call get_my_appointments first if you don't already know what they have.
2. Read the appointments and ask which one to cancel.
3. ALWAYS confirm before cancelling: "Just to confirm, you want to cancel your \
[vaccine] appointment on [date] at [time]?"
4. Only after they confirm, call cancel_appointment.
5. Confirm: "Done, that appointment has been cancelled."

== IMPORTANT VOICE GUIDELINES ==
- NUMBER all options so the user can say "number 2" instead of repeating details.
- CONFIRM before any irreversible action (booking, cancelling).
- READ BACK critical info: confirmation numbers digit by digit, dates, times.
- REPEAT BACK ambiguous input: "I heard 3-7-1-3-5 for your ZIP. Is that right?"
- When collecting names, phone numbers, or addresses, REPEAT them back to confirm.
- If a tool call fails, explain simply: "I'm having trouble with that. Let me try again."
- Never dump large amounts of data -- summarize and offer to give more detail.
- Guide step by step. Never ask for all information at once.
- If the user is already authenticated, NEVER mention login or ask them to sign in.

NOTE: The server automatically caches and chains data between steps. \
You do NOT need to pass large JSON responses between tool calls.\
"""
```

---

### **4. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/main.py**

```python
"""
FastAPI application entry point.

Serves the React frontend, REST API, and WebSocket chat endpoint.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import database as db
from app import mcp_bridge
from app.config import API_HOST, API_PORT
from app.routes.auth import router as auth_router
from app.routes.chat_ws import router as chat_ws_router
from app.routes.conversations import router as conversations_router
from app.routes.elevenlabs_tools import router as elevenlabs_tools_router
from app.routes.elevenlabs_webhook import router as elevenlabs_webhook_router
from app.routes.ios import router as ios_router
from app.routes.vision import router as vision_router
from app.routes.realtime import router as realtime_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up: initializing database and MCP bridge")
    await db.init_db()
    try:
        await mcp_bridge.connect()
    except Exception:
        logger.warning("MCP server not available at startup -- tools will be unavailable until it connects")
    yield
    logger.info("Shutting down")
    await mcp_bridge.disconnect()
    await db.close_db()


app = FastAPI(
    title="CVS Vaccine Scheduling Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(auth_router)
app.include_router(conversations_router)
app.include_router(chat_ws_router)
app.include_router(realtime_router)
app.include_router(ios_router)
app.include_router(vision_router)
app.include_router(elevenlabs_tools_router)
app.include_router(elevenlabs_webhook_router)


# Serve built React frontend
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    logger.warning(f"Frontend build not found at {FRONTEND_DIR} -- run 'npm run build' in frontend/")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info",
    )
```

---

### **5. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/elevenlabs_tools.py**

```python
"""
ElevenLabs Agent Tool Execution Endpoint.

When ElevenLabs Agent calls a tool (webhook type), it POSTs here.
We proxy the call to the local MCP server and return the result.
This bridges ElevenLabs Agent ↔ MCP Server when direct MCP connection
isn't available (e.g., MCP servers feature requires higher ElevenLabs plan).
"""

from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app import mcp_bridge

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/elevenlabs", tags=["elevenlabs-tools"])


@router.post("/tool/{tool_name}")
async def execute_tool(tool_name: str, request: Request):
    """Execute an MCP tool on behalf of the ElevenLabs Agent.

    ElevenLabs webhook tools POST to this endpoint with tool parameters.
    We proxy to the MCP bridge and return the result.
    """
    try:
        body = await request.json()
    except Exception:
        body = {}

    logger.info("ElevenLabs tool call: %s with args: %s", tool_name, list(body.keys()))

    # Strip placeholder params for tools that take no arguments
    body.pop("placeholder", None)

    # Fix type mismatches: ElevenLabs sends strings, MCP tools expect lists
    if tool_name == "check_vaccine_eligibility" and "vaccine_codes" in body:
        codes = body["vaccine_codes"]
        if isinstance(codes, str):
            body["vaccine_codes"] = [c.strip() for c in codes.split(",")]

    if tool_name == "submit_questionnaire" and "answers" in body:
        answers = body["answers"]
        if isinstance(answers, str):
            try:
                body["answers"] = json.loads(answers)
            except json.JSONDecodeError:
                # Agent sent natural language like "No for all" — default all to No (value "2")
                body["answers"] = []  # Empty means use defaults (all "No")

    try:
        result = await mcp_bridge.call_tool(tool_name, body)
        return JSONResponse(content={"result": result})
    except Exception as e:
        logger.error("Tool %s execution failed: %s", tool_name, e)
        return JSONResponse(
            status_code=200,  # Return 200 so ElevenLabs doesn't retry
            content={"result": f"Error executing {tool_name}: {str(e)}"},
        )
```

---

### **6. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/elevenlabs_webhook.py**

```python
"""
ElevenLabs Conversation Webhook Receiver.

Receives webhook events from the ElevenLabs Agent platform for:
- Conversation started/ended
- Tool call results (for Dynamic UI surface generation)
- Transcript updates (for syncing voice/video transcripts to DB)
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Request

from app import database as db
from app.dynamic_surfaces import build_surface_from_tool_result

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhooks/elevenlabs", tags=["webhooks"])


@router.post("/conversation")
async def elevenlabs_conversation_webhook(request: Request):
    """Handle ElevenLabs conversation lifecycle events.

    Event types:
    - conversation.started: New conversation session started
    - conversation.ended: Conversation session ended
    - conversation.tool_call: Agent executed a tool — generate Dynamic UI surface
    - conversation.transcript: New transcript entry (user or agent speech)
    """
    body: dict[str, Any] = await request.json()
    event_type = body.get("type", "")
    data = body.get("data", {})

    logger.info("ElevenLabs webhook: %s", event_type)

    if event_type == "conversation.started":
        return await _handle_conversation_started(data)
    elif event_type == "conversation.ended":
        return await _handle_conversation_ended(data)
    elif event_type == "conversation.tool_call":
        return await _handle_tool_call(data)
    elif event_type == "conversation.transcript":
        return await _handle_transcript(data)
    else:
        logger.warning("Unknown ElevenLabs webhook event: %s", event_type)
        return {"status": "ignored", "event": event_type}


async def _handle_conversation_started(data: dict[str, Any]) -> dict:
    """Log conversation start and optionally create a backend conversation record."""
    conversation_id = data.get("conversation_id", "")
    agent_id = data.get("agent_id", "")
    logger.info("ElevenLabs conversation started: %s (agent: %s)", conversation_id, agent_id)

    # Create a backend conversation if one doesn't exist for this ElevenLabs session
    if conversation_id:
        existing = await db.get_conversation(conversation_id)
        if not existing:
            await db.create_conversation(title="Voice/Video Session")
            logger.info("Created backend conversation for ElevenLabs session %s", conversation_id)

    return {"status": "ok"}


async def _handle_conversation_ended(data: dict[str, Any]) -> dict:
    """Log conversation end."""
    conversation_id = data.get("conversation_id", "")
    duration = data.get("duration_seconds", 0)
    logger.info("ElevenLabs conversation ended: %s (duration: %ds)", conversation_id, duration)
    return {"status": "ok"}


async def _handle_tool_call(data: dict[str, Any]) -> dict:
    """Process tool call result — generate Dynamic UI surface if applicable.

    The surface is stored on the assistant message so the iOS app can
    render the appropriate widget.
    """
    conversation_id = data.get("conversation_id", "")
    tool_name = data.get("tool_name", "")
    tool_result = data.get("tool_result", "")

    if not conversation_id:
        return {"status": "ok", "surface": None}

    # Generate Dynamic UI surface from tool result
    surface = build_surface_from_tool_result(tool_name, tool_result)

    # Store the tool call as a message with optional surface
    surfaces = [surface] if surface else None
    await db.add_message(
        conversation_id=conversation_id,
        role="tool_result",
        content=tool_result if isinstance(tool_result, str) else str(tool_result),
        tool_name=tool_name,
        modality="voice",
        surfaces=surfaces,
    )

    return {"status": "ok", "surface": surface}


async def _handle_transcript(data: dict[str, Any]) -> dict:
    """Store transcript entries (user speech or agent speech) in the database."""
    conversation_id = data.get("conversation_id", "")
    role = data.get("role", "user")  # "user" or "assistant"
    text = data.get("text", "")
    is_final = data.get("is_final", True)
    modality = data.get("modality", "voice")

    if not conversation_id or not text or not is_final:
        return {"status": "ok"}

    await db.add_message(
        conversation_id=conversation_id,
        role=role,
        content=text,
        modality=modality,
    )

    return {"status": "ok"}
```

---

### **7. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/ios.py**

```python
"""
iOS-specific REST endpoints.

Provides configuration, HeyGen LiveAvatar session creation,
conversation sync, and auth wrappers for the iOS native app.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import database as db
from app import mcp_bridge
from app.config import (
    ELEVENLABS_AGENT_ID,
    ELEVENLABS_API_KEY,
    HEYGEN_API_KEY,
    HEYGEN_AVATAR_ID,
    HEYGEN_SECRET_ID,
    get_auth_state,
)
from app.dynamic_surfaces import build_surface_from_tool_result

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ios", tags=["ios"])

HEYGEN_API_BASE = "https://api.liveavatar.com/v1"
HEYGEN_SESSION_TIMEOUT = 30


# ── Request Models ────────────────────────────────────────────────────────────


class LoginRequest(BaseModel):
    email: str
    password: str | None = None


class VerifyOTPRequest(BaseModel):
    code: str


class VerifyDOBRequest(BaseModel):
    month: int
    day: int
    year: int


class ConversationSyncRequest(BaseModel):
    conversation_id: str
    messages: list[dict[str, Any]] = []


class WidgetActionRequest(BaseModel):
    conversation_id: str
    surface_id: str
    action: str
    data: dict[str, Any] = {}


# ── Configuration ─────────────────────────────────────────────────────────────


@router.get("/config")
async def get_ios_config():
    """Return ElevenLabs agent config, HeyGen avatar config, and auth state for iOS app."""
    auth = get_auth_state()
    return {
        "elevenlabs": {
            "agent_id": ELEVENLABS_AGENT_ID,
            "api_key": ELEVENLABS_API_KEY,
        },
        "heygen": {
            "avatar_id": HEYGEN_AVATAR_ID,
        },
        "auth": {
            "authenticated": auth["authenticated"],
            "profile": auth.get("profile"),
        },
    }


# ── HeyGen LiveAvatar Session ────────────────────────────────────────────────


@router.post("/heygen-session")
async def create_heygen_session():
    """Create a HeyGen LiveAvatar LITE session with native ElevenLabs Agent plugin.

    Two-step flow:
    1. POST /v1/sessions/token → get session_token
    2. POST /v1/sessions/start → get LiveKit credentials

    Returns LiveKit connection credentials (url + token) for the iOS client.
    All audio routing between ElevenLabs Agent and LiveAvatar is server-to-server.
    """
    if not HEYGEN_API_KEY:
        raise HTTPException(status_code=500, detail="HEYGEN_API_KEY not configured")

    heygen_headers = {
        "x-api-key": HEYGEN_API_KEY,
        "Content-Type": "application/json",
    }

    # Build session payload — include ElevenLabs config if secret is available
    session_payload: dict[str, Any] = {
        "mode": "LITE",
        "avatar_id": HEYGEN_AVATAR_ID,
    }
    if HEYGEN_SECRET_ID:
        session_payload["elevenlabs_agent_config"] = {
            "secret_id": HEYGEN_SECRET_ID,
            "agent_id": ELEVENLABS_AGENT_ID,
        }

    async with httpx.AsyncClient(timeout=HEYGEN_SESSION_TIMEOUT) as client:
        # Step 1: Create session token
        token_resp = await client.post(
            f"{HEYGEN_API_BASE}/sessions/token",
            headers=heygen_headers,
            json=session_payload,
        )

        if token_resp.status_code not in (200, 201):
            logger.error("HeyGen token creation failed: %s %s", token_resp.status_code, token_resp.text)
            raise HTTPException(
                status_code=token_resp.status_code,
                detail=f"HeyGen token creation failed: {token_resp.text}",
            )

        token_data = token_resp.json().get("data", {})
        session_id = token_data.get("session_id")
        session_token = token_data.get("session_token")

        if not session_token:
            raise HTTPException(status_code=500, detail="HeyGen returned no session_token")

        # Step 2: Start the session to get LiveKit credentials
        start_resp = await client.post(
            f"{HEYGEN_API_BASE}/sessions/start",
            headers={"Authorization": f"Bearer {session_token}"},
        )

        if start_resp.status_code not in (200, 201):
            logger.error("HeyGen session start failed: %s %s", start_resp.status_code, start_resp.text)
            raise HTTPException(
                status_code=start_resp.status_code,
                detail=f"HeyGen session start failed: {start_resp.text}",
            )

        start_data = start_resp.json().get("data", {})

    return {
        "session_id": session_id,
        "livekit_url": start_data.get("livekit_url"),
        "livekit_token": start_data.get("livekit_client_token"),
    }


# ── Conversation Sync ────────────────────────────────────────────────────────


@router.post("/conversation/sync")
async def sync_conversation(req: ConversationSyncRequest):
    """Bidirectional conversation sync between iOS client and backend DB.

    - If conversation doesn't exist, creates it.
    - Merges any new messages from the iOS client.
    - Returns the full conversation with all messages (including surfaces).
    """
    conv = await db.get_conversation(req.conversation_id)
    if conv is None:
        conv = await db.create_conversation()
        # Update the ID to match what iOS sent (if it generated its own)
        # For simplicity, return the server-generated ID
        logger.info("Created new conversation %s for iOS sync", conv["id"])

    # Store any new messages from the iOS client
    for msg in req.messages:
        await db.add_message(
            conversation_id=conv["id"],
            role=msg.get("role", "user"),
            content=msg.get("content", ""),
            modality=msg.get("modality", "chat"),
        )

    # Return full conversation with messages
    messages = await db.get_messages(conv["id"])
    return {
        "conversation": conv,
        "messages": messages,
    }


# ── Widget Actions ────────────────────────────────────────────────────────────


@router.post("/widget-action")
async def handle_widget_action(req: WidgetActionRequest):
    """Handle a Dynamic UI widget action from the iOS app.

    Translates widget interaction into a natural language message,
    which can be sent to the ElevenLabs Agent as context.
    """
    # Format the widget action as natural language
    action_text = _format_widget_action(req.action, req.data)

    # Save as a user message with the widget context
    await db.add_message(
        conversation_id=req.conversation_id,
        role="user",
        content=action_text,
        modality="chat",
    )

    return {
        "formatted_message": action_text,
        "surface_id": req.surface_id,
    }


def _format_widget_action(action: str, data: dict[str, Any]) -> str:
    """Convert widget action + data into natural language for the agent."""
    formatters = {
        "select_vaccine": lambda d: f"I'd like to get the {d.get('name', d.get('code', 'selected'))} vaccine.",
        "select_store": lambda d: (
            f"I'd like to go to {d.get('name', 'the selected store')}"
            f" at {d.get('address', '')}"
            f"{' on ' + d.get('date', '') if d.get('date') else ''}."
        ),
        "select_time": lambda d: f"I'd like the {d.get('time', 'selected')} appointment.",
        "submit_patient": lambda d: (
            f"Here are my details: {d.get('first_name', '')} {d.get('last_name', '')}, "
            f"email {d.get('email', '')}, phone {d.get('phone_number', '')}, "
            f"address {d.get('street_address', '')}, {d.get('city', '')} {d.get('state', '')} {d.get('zip_code', '')}, "
            f"gender {d.get('gender', '')}."
        ),
        "submit_questionnaire": lambda d: f"Here are my questionnaire answers: {d.get('answers', [])}",
        "cancel_appointment": lambda d: f"Please cancel the appointment with ID {d.get('appointmentId', '')}.",
    }

    formatter = formatters.get(action)
    if formatter:
        return formatter(data)
    return f"User performed action '{action}' with data: {data}"


# ── Tool Result → Surface ─────────────────────────────────────────────────────


@router.post("/tool-result-surface")
async def get_surface_for_tool_result(tool_name: str, tool_result: str):
    """Given an MCP tool name and its result, return the Dynamic UI surface (if any)."""
    surface = build_surface_from_tool_result(tool_name, tool_result)
    if surface is None:
        return {"surface": None}
    return {"surface": surface}


# ── Auth Wrappers (MCP tools exposed as REST) ────────────────────────────────


@router.post("/auth/login")
async def ios_login(req: LoginRequest):
    """Login to CVS via MCP tools — supports OTP and password flows."""
    args: dict[str, Any] = {"email": req.email}
    if req.password:
        args["password"] = req.password

    try:
        result = await mcp_bridge.call_tool("login_to_cvs", args)
        return {"success": True, "result": result, "method": "password" if req.password else "otp"}
    except Exception as e:
        logger.error("iOS login failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/verify-otp")
async def ios_verify_otp(req: VerifyOTPRequest):
    """Verify OTP code for CVS login."""
    try:
        result = await mcp_bridge.call_tool("verify_otp", {"code": req.code})
        return {"success": True, "result": result}
    except Exception as e:
        logger.error("iOS OTP verification failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/auth/verify-dob")
async def ios_verify_dob(req: VerifyDOBRequest):
    """Verify date of birth to complete OTP login flow."""
    try:
        result = await mcp_bridge.call_tool(
            "verify_dob",
            {"month": str(req.month), "day": str(req.day), "year": str(req.year)},
        )
        return {"success": True, "result": result}
    except Exception as e:
        logger.error("iOS DOB verification failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/auth/status")
async def ios_auth_status():
    """Get current authentication status."""
    auth = get_auth_state()
    return {
        "authenticated": auth["authenticated"],
        "profile": auth.get("profile"),
    }


@router.post("/auth/logout")
async def ios_logout():
    """Logout from CVS."""
    try:
        result = await mcp_bridge.call_tool("logout", {})
        return {"success": True, "result": result}
    except Exception as e:
        logger.error("iOS logout failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
```

---

### **8. /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/dynamic_surfaces.py**

```python
"""
Dynamic UI Surfaces — transforms MCP tool results into structured UI payloads
for rendering as native SwiftUI widgets in the iOS app.

Each surface has:
  - surfaceId: unique identifier for widget lifecycle management
  - componentType: maps to a specific SwiftUI widget
  - data: structured payload for the widget
  - actions: interactive buttons/actions the user can take
  - state: lifecycle state (interactive, submitted, dismissed, loading, error)
"""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

logger = logging.getLogger(__name__)


def _surface_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def build_surface_from_tool_result(
    tool_name: str,
    tool_result: str,
) -> dict[str, Any] | None:
    """Transform an MCP tool result into a Dynamic UI surface payload.

    Returns None if the tool result doesn't map to a UI widget.
    """
    try:
        data = json.loads(tool_result) if isinstance(tool_result, str) else tool_result
    except (json.JSONDecodeError, TypeError):
        return None

    builder = _TOOL_SURFACE_BUILDERS.get(tool_name)
    if builder is None:
        return None

    try:
        return builder(data)
    except Exception:
        logger.exception("Failed to build surface for tool %s", tool_name)
        return None


# ── Surface Builders ──────────────────────────────────────────────────────────


def _build_vaccine_selection(data: Any) -> dict[str, Any] | None:
    """get_eligible_vaccines → VaccineSelectionCard"""
    vaccines = []
    if isinstance(data, dict):
        vaccines = data.get("vaccines", data.get("eligible_vaccines", []))
    elif isinstance(data, list):
        vaccines = data

    if not vaccines:
        return None

    items = []
    for v in vaccines:
        if isinstance(v, dict):
            items.append({
                "code": v.get("vaccineCode", v.get("code", "")),
                "name": v.get("vaccineName", v.get("name", "")),
                "description": v.get("description", ""),
            })
        elif isinstance(v, str):
            items.append({"code": v, "name": v, "description": ""})

    return {
        "surfaceId": _surface_id("vaccines"),
        "componentType": "vaccine_selection",
        "data": {"vaccines": items},
        "actions": [
            {"name": "select_vaccine", "label": "Select Vaccine", "style": "primary"}
        ],
        "state": "interactive",
    }


def _build_store_finder(data: Any) -> dict[str, Any] | None:
    """search_stores → StoreFinderCard"""
    stores = []
    if isinstance(data, dict):
        stores = data.get("stores", data.get("clinics", []))
    elif isinstance(data, list):
        stores = data

    if not stores:
        return None

    items = []
    for s in stores:
        if not isinstance(s, dict):
            continue
        items.append({
            "clinicId": s.get("clinicId", s.get("clinic_id", "")),
            "name": s.get("name", s.get("storeName", "")),
            "address": s.get("address", s.get("fullAddress", "")),
            "distance": s.get("distance", ""),
            "availableDates": s.get("availableDates", s.get("available_dates", [])),
        })

    return {
        "surfaceId": _surface_id("stores"),
        "componentType": "store_finder",
        "data": {"stores": items},
        "actions": [
            {"name": "select_store", "label": "Select Store", "style": "primary"}
        ],
        "state": "interactive",
    }


def _build_time_slot_grid(data: Any) -> dict[str, Any] | None:
    """get_available_time_slots → TimeSlotGrid"""
    slots = []
    if isinstance(data, dict):
        slots = data.get("slots", data.get("time_slots", data.get("availableSlots", [])))
    elif isinstance(data, list):
        slots = data

    if not slots:
        return None

    items = []
    for slot in slots:
        if isinstance(slot, dict):
            items.append({
                "time": slot.get("time", slot.get("appointmentTime", "")),
                "period": slot.get("period", slot.get("timePeriod", "")),
                "available": slot.get("available", True),
            })
        elif isinstance(slot, str):
            items.append({"time": slot, "period": "", "available": True})

    return {
        "surfaceId": _surface_id("timeslots"),
        "componentType": "time_slot_grid",
        "data": {"slots": items},
        "actions": [
            {"name": "select_time", "label": "Select Time", "style": "primary"}
        ],
        "state": "interactive",
    }


def _build_patient_form(data: Any) -> dict[str, Any] | None:
    """soft_reserve_slot → PatientFormCard"""
    reservation = {}
    if isinstance(data, dict):
        reservation = data

    return {
        "surfaceId": _surface_id("patient-form"),
        "componentType": "patient_form",
        "data": {
            "reservationConfirmed": True,
            "clinicId": reservation.get("clinicId", reservation.get("clinic_id", "")),
            "appointmentDate": reservation.get("appointmentDate", reservation.get("date", "")),
            "appointmentTime": reservation.get("appointmentTime", reservation.get("time", "")),
            "fields": [
                {"name": "first_name", "label": "First Name", "type": "text", "required": True},
                {"name": "last_name", "label": "Last Name", "type": "text", "required": True},
                {"name": "email", "label": "Email", "type": "email", "required": True},
                {"name": "phone_number", "label": "Phone Number", "type": "phone", "required": True},
                {"name": "street_address", "label": "Street Address", "type": "text", "required": True},
                {"name": "city", "label": "City", "type": "text", "required": True},
                {"name": "state", "label": "State", "type": "text", "required": True},
                {"name": "zip_code", "label": "ZIP Code", "type": "text", "required": True},
                {"name": "gender", "label": "Gender", "type": "picker", "required": True,
                 "options": ["Male", "Female", "Other"]},
            ],
        },
        "actions": [
            {"name": "submit_patient", "label": "Submit Details", "style": "primary"}
        ],
        "state": "interactive",
    }


def _build_questionnaire(data: Any) -> dict[str, Any] | None:
    """get_questionnaire → QuestionnaireCard"""
    questions = []
    if isinstance(data, dict):
        questions = data.get("questions", [])
    elif isinstance(data, list):
        questions = data

    if not questions:
        return None

    items = []
    for q in questions:
        if not isinstance(q, dict):
            continue
        items.append({
            "questionId": q.get("questionId", q.get("id", "")),
            "text": q.get("questionText", q.get("text", "")),
            "vaccines": q.get("vaccines", []),
            "answerOptions": q.get("answerOptions", q.get("options", ["Yes", "No"])),
        })

    return {
        "surfaceId": _surface_id("questionnaire"),
        "componentType": "questionnaire",
        "data": {"questions": items},
        "actions": [
            {"name": "submit_questionnaire", "label": "Submit Answers", "style": "primary"}
        ],
        "state": "interactive",
    }


def _build_confirmation_summary(data: Any) -> dict[str, Any] | None:
    """confirm_appointment → ConfirmationSummaryCard"""
    if not isinstance(data, dict):
        return None

    return {
        "surfaceId": _surface_id("confirmation"),
        "componentType": "confirmation_summary",
        "data": {
            "confirmationNumber": data.get("confirmationNumber", data.get("confirmation_number", "")),
            "vaccine": data.get("vaccine", data.get("vaccineName", "")),
            "date": data.get("date", data.get("appointmentDate", "")),
            "time": data.get("time", data.get("appointmentTime", "")),
            "location": data.get("location", data.get("storeName", "")),
            "address": data.get("address", data.get("storeAddress", "")),
            "patientName": data.get("patientName", data.get("patient_name", "")),
        },
        "actions": [],
        "state": "submitted",
    }


def _build_appointment_card(data: Any) -> dict[str, Any] | None:
    """get_my_appointments → AppointmentCard"""
    appointments = []
    if isinstance(data, dict):
        appointments = data.get("appointments", [])
    elif isinstance(data, list):
        appointments = data

    if not appointments:
        return None

    items = []
    for appt in appointments:
        if not isinstance(appt, dict):
            continue
        items.append({
            "appointmentId": appt.get("appointmentId", appt.get("id", "")),
            "vaccine": appt.get("vaccine", appt.get("vaccineName", "")),
            "date": appt.get("date", appt.get("appointmentDate", "")),
            "time": appt.get("time", appt.get("appointmentTime", "")),
            "location": appt.get("location", appt.get("storeName", "")),
            "address": appt.get("address", appt.get("storeAddress", "")),
            "confirmationNumber": appt.get("confirmationNumber", ""),
        })

    return {
        "surfaceId": _surface_id("appointments"),
        "componentType": "appointment_card",
        "data": {"appointments": items},
        "actions": [
            {"name": "cancel_appointment", "label": "Cancel Appointment", "style": "destructive"}
        ],
        "state": "interactive",
    }


# ── Tool → Builder Mapping ────────────────────────────────────────────────────

_TOOL_SURFACE_BUILDERS = {
    "get_eligible_vaccines": _build_vaccine_selection,
    "check_vaccine_eligibility": _build_vaccine_selection,
    "search_stores": _build_store_finder,
    "get_available_time_slots": _build_time_slot_grid,
    "soft_reserve_slot": _build_patient_form,
    "get_questionnaire": _build_questionnaire,
    "confirm_appointment": _build_confirmation_summary,
    "get_my_appointments": _build_appointment_card,
}
```

---

### **9. iOS Project Configuration Files**

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling.xcworkspace/contents.xcworkspacedata**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Workspace
   version = "1.0">
   <FileRef
      location = "group:Package.swift">
   </FileRef>
</Workspace>
```

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling.xcworkspace/xcshareddata/WorkspaceSettings.xcsettings**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>IDEWorkspaceSharedSettings_AutocreateContextsIfNeeded</key>
	<false/>
</dict>
</plist>
```

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/project.yml**
```yaml
name: CVSScheduling
options:
  bundleIdPrefix: com.cvs.scheduling
  deploymentTarget:
    iOS: "17.0"
  xcodeVersion: "16.0"

packages:
  ElevenLabs:
    url: https://github.com/elevenlabs/elevenlabs-swift-sdk.git
    from: "3.0.0"

targets:
  CVSScheduling:
    type: application
    platform: iOS
    sources:
      - path: CVSScheduling
        excludes:
          - "**/.DS_Store"
    resources:
      - path: CVSScheduling/Resources/Assets.xcassets
      - path: CVSScheduling/Resources/Info.plist
        buildPhase: none
    settings:
      base:
        PRODUCT_BUNDLE_IDENTIFIER: com.cvs.scheduling.app
        INFOPLIST_FILE: CVSScheduling/Resources/Info.plist
        MARKETING_VERSION: "1.0"
        CURRENT_PROJECT_VERSION: "1"
        SWIFT_VERSION: "5.9"
        TARGETED_DEVICE_FAMILY: "1"
        CODE_SIGN_STYLE: Automatic
        DEVELOPMENT_TEAM: ""
        ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon
        ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME: AccentColor
        GENERATE_INFOPLIST_FILE: false
    dependencies:
      - package: ElevenLabs
        product: ElevenLabs
```

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/Package.swift**
```swift
// swift-tools-version: 5.9
// CVSScheduling iOS App — SPM Dependencies

import PackageDescription

let package = Package(
    name: "CVSScheduling",
    platforms: [
        .iOS(.v17)
    ],
    dependencies: [
        // ElevenLabs Swift SDK — Chat + Voice (includes LiveKit dependency)
        .package(url: "https://github.com/elevenlabs/elevenlabs-swift-sdk.git", from: "3.0.0"),
    ],
    targets: [
        .executableTarget(
            name: "CVSScheduling",
            dependencies: [
                .product(name: "ElevenLabs", package: "elevenlabs-swift-sdk"),
            ],
            path: "CVSScheduling",
            resources: [
                .process("Resources/Assets.xcassets"),
            ]
        ),
    ]
)
```

---

## **10. iOS Swift Source Files - Complete Content**

### **App Layer**

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/App/CVSSchedulingApp.swift**
[Provided above - 34 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/App/AppCoordinator.swift**
[Provided above - 48 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/App/DesignSystem.swift**
[Provided above - 221 lines - includes colors, typography, shadows, button styles, haptics, transitions, spacing]

### **Models**

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Models/Modality.swift**
[Provided above - 26 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Models/AuthState.swift**
[Provided above - 51 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Models/Conversation.swift**
[Provided above - 106 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Models/SchedulingState.swift**
[Provided above - 51 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Models/DynamicSurface.swift**
[Provided above - 142 lines]

### **ViewModels**

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/ViewModels/ConversationCoordinator.swift**
[Provided above - 221 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/ViewModels/ChatViewModel.swift**
[Provided above - 29 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/ViewModels/VoiceViewModel.swift**
[Provided above - 18 lines]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/ViewModels/VideoAvatarViewModel.swift**
[Provided above - 19 lines]

### **Services**

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/ElevenLabsService.swift**
[Provided above - 181 lines - WebSocket text chat with agent]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/HeyGenService.swift**
[Provided above - 98 lines - LiveKit video avatar sessions]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/BackendAPIService.swift**
[Provided above - 231 lines - REST client for FastAPI backend]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/AuthService.swift**
[Provided above - 131 lines - CVS authentication wrapper]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/ConversationPersistence.swift**
[Provided above - 38 lines - UserDefaults caching]

### **Views**

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Views/Main/MainTabView.swift**
[Provided above - 393 lines - landing, chat, floating call bubble, fullscreen video]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Views/Chat/ChatView.swift**
[Provided above - 131 lines - chat bubbles, typing indicator, image handling]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Views/Chat/ChatInputBar.swift**
[Provided above - 241 lines - WhatsApp-style input with camera, photos, voice-to-text]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Views/Auth/LoginView.swift**
[Provided above - 289 lines - CVS branded auth with OTP, password, DOB flows]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Views/Voice/VoiceSessionView.swift**
[Provided above - 11 lines - legacy view, not used]

**File: /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Views/Video/VideoAvatarView.swift**
[Provided above - 12 lines - legacy view, not used]

---

## Summary

**Total Files Explored: 37 files across iOS directory and ElevenLabs routes**

Key integration points:
- ElevenLabs Agent Platform: WebSocket text/voice chat via signed URL
- HeyGen LiveAvatar: LiveKit-based video sessions with server-to-server audio routing
- Dynamic Surfaces: Python backend transforms MCP tool results into SwiftUI widgets
- iOS Services: REST client, auth wrapper, persistence layer
- Backend Routes: iOS config, HeyGen session creation, conversation sync, widget actions, auth flows, ElevenLabs tool proxying and webhook handling

---

