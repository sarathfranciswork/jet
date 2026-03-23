# Claude Conversation Log

Session ID: agent-aed7fe83d704df22d
Date: 2026-03-18 18:57:33

---

## 👤 User

I need to implement real-time transcript streaming during video mode in an iOS app that uses HeyGen LiveAvatar with an ElevenLabs Agent Plugin. Here's the architecture:

**Current setup:**
- iOS app connects to HeyGen via LiveKit for video/audio
- HeyGen manages an ElevenLabs conversation session (server-to-server)
- iOS has NO direct connection to the ElevenLabs session during video mode
- Backend is FastAPI on Cloud Run: https://cvs-scheduling-backend-876802621972.us-central1.run.app

**ElevenLabs Monitoring WebSocket:**
- Endpoint: `wss://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/monitor`
- Requires: `monitoring_enabled: true` on agent
- Sends real-time events: `user_transcript`, `agent_response`, `agent_response_correction`
- Requires knowing the `conversation_id` (obtained from conversations list API)
- May be enterprise-only feature

**Event formats:**
```json
{"type": "user_transcript", "user_transcription_event": {"user_transcript": "text"}}
{"type": "agent_response", "agent_response_event": {"agent_response": "text"}}
```

**Files involved:**
- Backend: `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/ios.py` (FastAPI router)
- iOS: `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/ViewModels/ConversationCoordinator.swift`
- iOS: `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/BackendAPIService.swift`

**Requirements:**
1. When iOS enters video mode, the backend should find the latest ElevenLabs conversation and connect to the monitoring WebSocket
2. Backend buffers transcript events in memory
3. iOS polls the backend every 1-2 seconds for new events
4. Events are added to the chat message list so it looks like a seamless conversation
5. When video ends, clean up the monitoring connection

**Considerations:**
- Backend is on Cloud Run (stateless by default, but we use min-instances=1)
- Need `websockets` or `aiohttp` for the monitoring WebSocket client
- Need to handle the delay between HeyGen starting the session and the conversation appearing in ElevenLabs API
- Need to handle the case where monitoring WebSocket is enterprise-only (fallback gracefully)
- The conversation_id needs to be discovered by polling `GET /v1/convai/conversations?agent_id=xxx`

**Dependencies available:**
- Read /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/requirements-deploy.txt to check what Python packages are available

Please create a detailed implementation plan considering all edge cases and the best approach for each component.

---

## 🤖 Claude



I'll start by thoroughly exploring the existing codebase to understand the current architecture, patterns, and conventions before designing the implementation plan.

---

## 🤖 Claude

Good, I can see the current state. The existing `video-transcript` endpoint uses a polling approach against the ElevenLabs conversations REST API (not the monitoring WebSocket). Now let me explore more of the codebase to understand the full picture.

---

## 🤖 Claude

Now let me examine additional related files to understand the ElevenLabs webhook and tools routes, and check what other patterns exist.

---

## 🤖 Claude

Now let me look at the ElevenLabsService on iOS and the database module to understand the full data flow.

---

## 🤖 Claude

Now I have a thorough understanding of the entire system. Let me check one more thing -- the dynamic surfaces module and look at how Cloud Run handles the deployment.

---

## 🤖 Claude

Now I have a complete picture of the system. Let me verify the `websockets` package is already in the dependencies (I saw it in requirements-deploy.txt) and check the HeyGenRoomDelegate data channel messages more closely.

---

## 🤖 Claude

Now I have a complete understanding of the entire system. Let me synthesize the plan.

---

## Implementation Plan: Real-Time Transcript Streaming During Video Mode

### Problem Analysis

The current implementation (`/api/ios/video-transcript`) polls the ElevenLabs **REST API** (`GET /v1/convai/conversations/{id}`) every 2 seconds from the iOS client. This approach has two fundamental problems:

1. **High latency**: The REST transcript API only returns data after the conversation is complete or with significant delay (ElevenLabs batches transcript data). During an active conversation, the transcript array is often empty or stale.
2. **Conversation discovery delay**: There is a race between HeyGen creating the ElevenLabs session and it appearing in the `GET /v1/convai/conversations` list API. The current code has a 4-second initial wait, but this is fragile.

The proposed solution uses the **ElevenLabs Monitoring WebSocket** (`wss://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/monitor`) which streams events in real time. However, this requires the backend to maintain a persistent WebSocket client connection and buffer events for the iOS polling client.

### Architecture Decision: Dual-Source Transcript Strategy

There are actually **two** paths for transcripts reaching the iOS client already:

1. **LiveKit Data Channel** (line 162 of `HeyGenService.swift`): The `HeyGenRoomDelegate` already listens for `agent_response` and `user_transcript` events via the LiveKit data channel. These events are forwarded via `onTranscript` callback to `ConversationCoordinator`, which appends them to `elevenLabs.messages`.

2. **Backend Polling** (line 290-313 of `ConversationCoordinator.swift`): The `startTranscriptPolling()` method polls `GET /api/ios/video-transcript` every 2 seconds.

This means **transcripts could arrive from both sources simultaneously**, causing duplicates. The plan must handle deduplication.

### Recommended Approach: Backend WebSocket Monitor + Improved Polling

Rather than trying to get iOS to connect directly to the monitoring WebSocket (which would require exposing the ElevenLabs API key to the client), the backend should:

1. Maintain a server-side WebSocket client to the ElevenLabs monitoring endpoint
2. Buffer events in an in-memory store (keyed by a session identifier)
3. Serve them via the existing polling endpoint with cursor-based pagination
4. Handle the LiveKit data channel transcripts as a fallback/complement

---

### Step-by-Step Implementation

#### Phase 1: Backend -- ElevenLabs Monitor WebSocket Client

**File: `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/ios.py`**

The backend already has `websockets>=12.0` in `requirements-deploy.txt`, so no new dependency is needed.

**1a. In-Memory Event Buffer**

Replace the simple `_transcript_state` dict (line 342) with a proper buffer class:

```python
import asyncio
import time
from dataclasses import dataclass, field

@dataclass
class TranscriptEvent:
    role: str          # "user" or "agent"
    content: str
    timestamp: float   # time.monotonic() for ordering
    event_type: str    # "user_transcript", "agent_response", "agent_response_correction"

@dataclass
class MonitorSession:
    conversation_id: str | None = None
    events: list[TranscriptEvent] = field(default_factory=list)
    cursor: int = 0           # tracks what iOS has already fetched
    ws_task: asyncio.Task | None = None
    started_at: float = 0.0
    is_connected: bool = False
    error: str | None = None
```

Key design points:
- The `cursor` tracks what the iOS client has already received (replaces `sent_count`)
- Events are append-only with monotonic timestamps for ordering
- `agent_response_correction` events need special handling: they **replace** the most recent agent response (ElevenLabs sends corrections when it refines the transcript)

**1b. Conversation Discovery Loop**

When iOS calls `POST /api/ios/video-transcript/start` (new endpoint -- replaces `reset`), the backend should:

1. Start an async task that polls `GET /v1/convai/conversations?agent_id=xxx` every 2 seconds
2. Look for a conversation with `created_at` within the last 30 seconds (indicating it was just created by the HeyGen session)
3. Once found, attempt to connect to the monitoring WebSocket
4. If monitoring WebSocket fails (403/enterprise-only), fall back to the existing REST polling approach

```python
async def _discover_and_monitor(session: MonitorSession):
    """Background task: discover ElevenLabs conversation, then connect monitor."""
    max_attempts = 15  # 15 * 2s = 30 seconds max wait
    for attempt in range(max_attempts):
        await asyncio.sleep(2)
        conv_id = await _find_latest_conversation()
        if conv_id and conv_id != session.conversation_id:
            session.conversation_id = conv_id
            logger.info("Discovered ElevenLabs conversation: %s", conv_id)
            await _connect_monitor_ws(session)
            return
    logger.warning("Could not discover ElevenLabs conversation after %d attempts", max_attempts)
    session.error = "conversation_not_found"
```

**1c. WebSocket Monitor Connection**

```python
import websockets

async def _connect_monitor_ws(session: MonitorSession):
    """Connect to ElevenLabs monitoring WebSocket and buffer events."""
    url = f"wss://api.elevenlabs.io/v1/convai/conversations/{session.conversation_id}/monitor"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    try:
        async with websockets.connect(url, additional_headers=headers) as ws:
            session.is_connected = True
            logger.info("Connected to ElevenLabs monitor WS for %s", session.conversation_id)
            async for raw in ws:
                msg = json.loads(raw)
                _process_monitor_event(session, msg)
    except websockets.exceptions.InvalidStatusCode as e:
        if e.status_code == 403:
            logger.warning("Monitoring WebSocket returned 403 -- feature may be enterprise-only")
            session.error = "monitoring_not_available"
            # Fall back to REST polling
            await _fallback_rest_polling(session)
        else:
            logger.error("Monitor WS error: %s", e)
            session.error = str(e)
    except Exception as e:
        logger.error("Monitor WS unexpected error: %s", e)
        session.error = str(e)
    finally:
        session.is_connected = False
```

**1d. Event Processing**

Handle three event types from the monitoring WebSocket:

```python
def _process_monitor_event(session: MonitorSession, msg: dict):
    event_type = msg.get("type", "")
    
    if event_type == "user_transcript":
        event = msg.get("user_transcription_event", {})
        text = event.get("user_transcript", "")
        if text:
            session.events.append(TranscriptEvent(
                role="user", content=text,
                timestamp=time.monotonic(), event_type=event_type
            ))
    
    elif event_type == "agent_response":
        event = msg.get("agent_response_event", {})
        text = event.get("agent_response", "")
        if text:
            session.events.append(TranscriptEvent(
                role="agent", content=text,
                timestamp=time.monotonic(), event_type=event_type
            ))
    
    elif event_type == "agent_response_correction":
        event = msg.get("agent_response_correction_event", {})
        text = event.get("agent_response", "")
        if text:
            # Replace the last agent event
            for i in range(len(session.events) - 1, -1, -1):
                if session.events[i].role == "agent":
                    session.events[i] = TranscriptEvent(
                        role="agent", content=text,
                        timestamp=session.events[i].timestamp,
                        event_type=event_type
                    )
                    break
```

The `agent_response_correction` handling is important: ElevenLabs sometimes sends an initial `agent_response` followed by a corrected version. If the cursor has already passed the original event, the correction needs to be sent as a separate "correction" event to iOS so it can update the message in place.

**1e. REST Fallback Polling**

If the monitoring WebSocket returns 403, fall back to the existing approach (polling the REST transcript API from the backend):

```python
async def _fallback_rest_polling(session: MonitorSession):
    """Poll ElevenLabs REST API for transcript data (fallback)."""
    rest_cursor = 0
    while session.conversation_id:
        await asyncio.sleep(2)
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(
                f"https://api.elevenlabs.io/v1/convai/conversations/{session.conversation_id}",
                headers={"xi-api-key": ELEVENLABS_API_KEY},
            )
            if resp.status_code != 200:
                continue
            transcript = resp.json().get("transcript", [])
            new_entries = transcript[rest_cursor:]
            rest_cursor = len(transcript)
            for entry in new_entries:
                msg = entry.get("message", "")
                if msg:
                    session.events.append(TranscriptEvent(
                        role=entry.get("role", "agent"),
                        content=msg,
                        timestamp=time.monotonic(),
                        event_type="rest_poll"
                    ))
```

**1f. New/Modified Endpoints**

Three endpoints (modifying the existing two and adding one):

1. **`POST /api/ios/video-transcript/start`** -- Start monitoring for a new video session. Returns immediately. Spawns the background discovery+monitor task.

2. **`GET /api/ios/video-transcript`** (modified) -- Return events since the cursor. Include a `corrections` array for any events that were already sent but have been corrected. Include monitoring status so iOS knows if it should use the LiveKit data channel as primary.

   Response shape:
   ```json
   {
     "messages": [{"role": "agent", "content": "..."}],
     "corrections": [{"index": 3, "content": "corrected text"}],
     "status": "monitoring" | "fallback" | "discovering" | "error",
     "conversation_id": "xxx"
   }
   ```

3. **`POST /api/ios/video-transcript/stop`** (replaces `reset`) -- Cancel the monitoring task and clean up. Called when video ends.

#### Phase 2: iOS Client -- Improved Polling and Deduplication

**File: `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/BackendAPIService.swift`**

**2a. Updated API Models**

Add models for the new response shape:

```swift
struct TranscriptCorrection: Codable {
    let index: Int
    let content: String
}

struct TranscriptResponse: Codable {
    let messages: [TranscriptMessage]
    let corrections: [TranscriptCorrection]
    let status: String  // "monitoring", "fallback", "discovering", "error"
    let conversationId: String?
    
    enum CodingKeys: String, CodingKey {
        case messages, corrections, status
        case conversationId = "conversation_id"
    }
}
```

**2b. New `startVideoMonitoring` and `stopVideoMonitoring` methods**

```swift
func startVideoMonitoring() async throws {
    let url = baseURL.appendingPathComponent("api/ios/video-transcript/start")
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    _ = try await session.data(for: request)
}

func stopVideoMonitoring() async throws {
    let url = baseURL.appendingPathComponent("api/ios/video-transcript/stop")
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    _ = try await session.data(for: request)
}
```

**File: `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/ViewModels/ConversationCoordinator.swift`**

**2c. Deduplication Strategy**

The critical challenge: transcripts can arrive from two sources simultaneously:
- **LiveKit data channel** (via `HeyGenRoomDelegate` -> `onTranscript` callback, line 63-69)
- **Backend polling** (via `startTranscriptPolling()`, line 290-313)

To deduplicate, track a set of "seen" content hashes:

```swift
private var seenTranscriptHashes: Set<String> = []

private func transcriptHash(_ role: String, _ content: String) -> String {
    // Use a simple hash of role + normalized content
    let normalized = content.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
    return "\(role):\(normalized.prefix(50))"
}
```

Modify the `onTranscript` callback (line 63-69) to check before appending:

```swift
heyGen.onTranscript = { [weak self] role, content in
    Task { @MainActor [weak self] in
        guard let self else { return }
        let hash = self.transcriptHash(role, content)
        guard !self.seenTranscriptHashes.contains(hash) else { return }
        self.seenTranscriptHashes.insert(hash)
        self.elevenLabs.messages.append(
            ElevenLabsService.ChatEntry(role: role, content: content)
        )
    }
}
```

Apply the same deduplication in the polling handler.

**2d. Adaptive Polling Interval**

When the backend reports `status: "monitoring"`, iOS knows the monitoring WebSocket is active and events are arriving in near-real-time. It can poll more frequently (every 1 second). When in `"fallback"` mode, poll every 2 seconds. When `"discovering"`, use 3 seconds (the events won't be ready yet anyway).

```swift
private func startTranscriptPolling() {
    transcriptPollTask?.cancel()
    transcriptPollTask = Task { [weak self] in
        // Signal backend to start monitoring
        try? await self?.backend.startVideoMonitoring()
        // Give HeyGen a moment to spin up
        try? await Task.sleep(nanoseconds: 3_000_000_000)
        
        var pollInterval: UInt64 = 2_000_000_000 // default 2s
        
        while !Task.isCancelled {
            guard let self, self.isVideoActive else { break }
            do {
                let response = try await self.backend.getVideoTranscript()
                for msg in response.messages {
                    let hash = self.transcriptHash(msg.role, msg.content)
                    guard !self.seenTranscriptHashes.contains(hash) else { continue }
                    self.seenTranscriptHashes.insert(hash)
                    self.elevenLabs.messages.append(
                        ElevenLabsService.ChatEntry(role: msg.role, content: msg.content)
                    )
                }
                // Handle corrections (update existing messages in place)
                for correction in response.corrections {
                    // Find and update the message at the original index
                    // (relative to video session start)
                }
                
                // Adaptive interval
                switch response.status {
                case "monitoring": pollInterval = 1_000_000_000
                case "fallback": pollInterval = 2_000_000_000
                default: pollInterval = 3_000_000_000
                }
            } catch {}
            try? await Task.sleep(nanoseconds: pollInterval)
        }
    }
}
```

**2e. Cleanup on Video End**

Modify `stopTranscriptPolling()` (line 310-313) to also notify the backend:

```swift
private func stopTranscriptPolling() {
    transcriptPollTask?.cancel()
    transcriptPollTask = nil
    seenTranscriptHashes.removeAll()
    Task { try? await backend.stopVideoMonitoring() }
}
```

And in `toggleVideo()` (line 221), the `stopTranscriptPolling()` call already happens at the right place.

#### Phase 3: Cloud Run Considerations

**Statelessness concern**: Cloud Run instances are stateless by default. The in-memory `MonitorSession` will be lost if the instance is recycled. However:

- The project already uses `min-instances=1` (mentioned in the requirements)
- The in-memory `_transcript_state` dict already exists on line 342 of `ios.py` -- this new approach is structurally identical
- Video sessions are short-lived (minutes, not hours) so the risk of instance recycling mid-session is low
- If the instance does recycle, the next poll from iOS will get an empty response and the LiveKit data channel serves as a backup

**Cold start**: The WebSocket connection adds no cold-start overhead since it is only created when a video session starts.

**Concurrent sessions**: The current design (module-level `_transcript_state`) only supports one active video session at a time. This is fine for a single-user demo app. If multi-tenancy is needed later, key the session by a session ID passed from iOS.

#### Phase 4: Edge Cases

1. **HeyGen session starts but ElevenLabs conversation never appears**: The discovery loop times out after 30 seconds. iOS falls back to LiveKit data channel transcripts (which already work independently via `HeyGenRoomDelegate`). Backend returns `status: "error"` with `error: "conversation_not_found"`.

2. **Monitoring WebSocket is enterprise-only (403)**: Fall back to REST polling automatically. Backend returns `status: "fallback"`. iOS continues to work, just with 2-3 second latency on transcripts.

3. **WebSocket disconnects mid-session**: Implement reconnection with exponential backoff (1s, 2s, 4s, max 10s). After 3 failed reconnection attempts, fall back to REST polling.

4. **Duplicate messages from LiveKit + polling**: The content-hash deduplication on iOS handles this. The hash uses `role + normalized_content.prefix(50)` which is sufficient to catch duplicates even when wording is identical.

5. **Agent response corrections**: When ElevenLabs sends `agent_response_correction`, the backend checks if the original event was already sent to iOS (cursor has advanced past it). If so, it includes the correction in the `corrections` array. iOS finds the matching message in `elevenLabs.messages` and updates its content in place.

6. **Backend restarts during video session**: iOS polls get empty results (no events buffered). LiveKit data channel continues to work as the primary source. On the next `POST /video-transcript/start`, a new monitoring session starts. If the ElevenLabs conversation is still active, it re-discovers and reconnects.

7. **Multiple rapid video on/off toggles**: Each `start` cancels any existing monitoring task. Each `stop` cleans up. The `asyncio.Task` cancellation is handled gracefully via `try/except asyncio.CancelledError`.

---

### Implementation Order

1. **Backend: Buffer + Discovery + Monitor** -- Modify `ios.py` to add the `MonitorSession` class, discovery loop, and WebSocket monitor client. Add `start`/`stop` endpoints.
2. **Backend: Fallback** -- Add REST polling fallback when monitoring returns 403.
3. **iOS: BackendAPIService** -- Add `startVideoMonitoring`, `stopVideoMonitoring`, update `TranscriptResponse` model.
4. **iOS: ConversationCoordinator** -- Add deduplication, call start/stop monitoring, adaptive polling.
5. **Testing** -- Manual test cycle: start video, verify transcripts appear, verify dedup, test 403 fallback, test reconnection.

### Dependency Note

No new Python packages are needed -- `websockets>=12.0` is already in `requirements-deploy.txt`. No new Swift packages are needed -- all functionality uses Foundation `URLSession`.

---

### Critical Files for Implementation
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/ios.py` - Backend router: add MonitorSession, discovery loop, WebSocket monitor client, modify transcript endpoints
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/ViewModels/ConversationCoordinator.swift` - iOS coordinator: add deduplication, call start/stop monitoring, adaptive polling intervals
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/BackendAPIService.swift` - iOS API client: add startVideoMonitoring, stopVideoMonitoring, update TranscriptResponse model
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/CVSScheduling/Services/HeyGenService.swift` - Reference for LiveKit data channel event format (HeyGenRoomDelegate) to ensure deduplication alignment
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/requirements-deploy.txt` - Verify websockets dependency is present (it is: websockets>=12.0)

---

