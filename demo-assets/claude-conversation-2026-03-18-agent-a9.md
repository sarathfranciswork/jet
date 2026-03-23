# Claude Conversation Log

Session ID: agent-a934a40f75103fa07
Date: 2026-03-18 18:53:50

---

## 👤 User

Research the ElevenLabs Conversational AI agent monitoring/webhook feature thoroughly. I need to understand exactly how to get real-time transcript events (user_transcript, agent_response) pushed to a webhook URL during an active conversation.

1. Search the web or documentation for ElevenLabs ConvAI agent monitoring webhook configuration
2. Check the ElevenLabs API at https://api.elevenlabs.io - specifically the agent PATCH endpoint for monitoring configuration
3. Look at the current agent config to understand what monitoring fields are available

Run this curl to get the full agent config and look at monitoring-related fields:
```
curl -s "https://api.elevenlabs.io/v1/convai/agents/agent_1601kkw1x9h4f67rm6zm09xsdb1a" \
  -H "xi-api-key: sk_17ef672536d5d125050d1df954661e0f27b1659b8fb3fe3e" | python3 -c "
import json, sys
d = json.load(sys.stdin)
# Print conversation config focusing on monitoring
conv = d.get('conversation_config', {})
print('=== conversation section ===')
print(json.dumps(conv.get('conversation', {}), indent=2))
print()
print('=== Full agent config keys ===')
for key in d:
    print(f'  {key}: {type(d[key]).__name__}')
print()
# Look for any webhook/monitoring/event related config
print('=== Looking for monitoring/webhook/event config ===')
def find_keys(obj, prefix=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f'{prefix}.{k}' if prefix else k
            if any(term in k.lower() for term in ['monitor', 'webhook', 'event', 'callback', 'notify', 'hook']):
                print(f'  FOUND: {path} = {json.dumps(v)[:200]}')
            find_keys(v, path)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_keys(v, f'{prefix}[{i}]')
find_keys(d)
"
```

Also check the ElevenLabs API docs for:
- Agent webhook configuration endpoint
- Monitoring events configuration
- Real-time event streaming options
- Any SSE or WebSocket endpoints for conversation events

Search in the resolved packages too:
/Users/sarathfrancis/Library/Developer/Xcode/DerivedData/CVSScheduling-bqclcarijkrxonagbptvpsjvdkim/SourcePackages/

Look for any monitoring, webhook, or event-related configuration in the ElevenLabs SDK source.

---

## 🤖 Claude

I'll help you research the ElevenLabs ConvAI agent monitoring/webhook feature thoroughly. Let me start by executing the curl command and searching for relevant documentation.

---

## 🤖 Claude

Excellent! Now let me search the ElevenLabs API documentation and the project for more details:

---

## 🤖 Claude

Now let me fetch the detailed ElevenLabs documentation pages for monitoring and webhooks:

---

## 🤖 Claude

Good! Let me search for more specific information about the monitoring events and webhook setup:

---

## 🤖 Claude

Perfect! Now let me check the existing elevenlabs webhook and tools files in the project:

---

## 🤖 Claude

Let me try another search for the actual monitoring webhook configuration:

---

## 🤖 Claude

Excellent! Now let me check the Client Events documentation:

---

## 🤖 Claude

Perfect! Now let me search for more specifics on monitoring webhook configuration and how to push events to a webhook URL:

---

## 🤖 Claude

Let me try to access the actual ElevenLabs API documentation for the update agent endpoint:

---

## 🤖 Claude

Excellent! Now let me get more details on the WebSocket API structure:

---

## 🤖 Claude

Perfect! Now let me check for server-side webhook configuration and any additional monitoring webhook setup:

---

## 🤖 Claude

Now let me check the actual agent config from the curl response to see what webhook configuration is available:

---

## 🤖 Claude

Let me read the full output to understand the webhook configuration structure:

---

## 🤖 Claude

Perfect! Now let me search for more details about how to actually enable real-time webhook push for monitoring events:

---

## 🤖 Claude

Excellent! Now I have comprehensive information. Let me create a final summary document:

## ElevenLabs ConvAI Agent Monitoring/Webhook Research Summary

Based on my thorough research of the ElevenLabs API and your current agent configuration, here's exactly how real-time transcript events are pushed during active conversations:

---

### Current Agent Configuration Status

Your agent (`agent_1601kkw1x9h4f67rm6zm09xsdb1a`) has monitoring **currently disabled**:

```json
"conversation": {
  "monitoring_enabled": false,
  "monitoring_events": [
    "user_transcript",
    "agent_response",
    "agent_response_correction"
  ]
}
```

The `monitoring_events` array is already configured with the transcript events you need.

---

### Two Separate Real-time Event Delivery Mechanisms

ElevenLabs provides two distinct mechanisms for getting real-time transcript events during active conversations:

#### 1. **Real-Time Monitoring (WebSocket)**
- **Primary mechanism** for live event streaming
- Uses WebSocket connection (not HTTP webhooks)
- Enterprise-only feature
- Endpoint: `wss://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/monitor`
- Authentication: API key with `ElevenLabs Agents Write` scope + `EDITOR` workspace access
- Delivers ALL selected events in real-time
- Can send control commands back (end call, transfer, human takeover)

**To Enable:**
```bash
PATCH /v1/convai/agents/{agent_id}
{
  "conversation_config": {
    "monitoring_enabled": true,
    "monitoring_events": [
      "user_transcript",
      "agent_response",
      "agent_response_correction"
    ]
  }
}
```

#### 2. **Post-Call Webhooks (HTTP)**
- Triggered AFTER conversation ends (not real-time during conversation)
- Standard webhook push model (POST to your URL)
- Three types: `post_call_transcription`, `post_call_audio`, `call_initiation_failure`
- Includes full transcript, analysis, metadata, and optional audio
- Not useful for live monitoring - only for post-conversation processing

---

### Available Monitoring Events (Client Events)

Your agent is configured to monitor these events via WebSocket when monitoring is enabled:

1. **`user_transcript`** - User's finalized speech-to-text results (complete utterances)
2. **`agent_response`** - Agent's complete response message
3. **`agent_response_correction`** - Truncated response when user interrupts

Also available but not configured:
- `audio` - Base64-encoded audio with timing data
- `interruption` - User interrupt detection
- `agent_response_metadata` - Custom LLM metadata
- `client_tool_call` - Client-side tool execution requests
- `agent_tool_response` - Tool execution completion
- `mcp_tool_call` - MCP tool execution (4 states: loading, awaiting_approval, success, failure)
- `agent_chat_response_part` - Text-only streaming with start/delta/stop

**Cannot be monitored:** VAD scores, turn probability metrics, ping events

---

### Event Payload Structures

Based on the Client Events documentation:

**user_transcript event:**
```json
{
  "type": "user_transcript",
  "user_transcription_event": {
    "user_transcript": "I need help with my voice cloning project."
  }
}
```

**agent_response event:**
```json
{
  "type": "agent_response",
  "agent_response_event": {
    "agent_response": "I'd be happy to help with your voice cloning project. Could you tell me what specific aspects you need assistance with?"
  }
}
```

---

### Setting Up Real-Time Monitoring

To push transcript events to your backend during active conversations:

1. **Enable monitoring on the agent:**
```bash
curl -X PATCH https://api.elevenlabs.io/v1/convai/agents/agent_1601kkw1x9h4f67rm6zm09xsdb1a \
  -H "xi-api-key: sk_17ef672536d5d125050d1df954661e0f27b1659b8fb3fe3e" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_config": {
      "monitoring_enabled": true,
      "monitoring_events": [
        "user_transcript",
        "agent_response",
        "agent_response_correction"
      ]
    }
  }'
```

2. **Create a server-side listener** that connects to the monitoring endpoint:
```python
import websockets
import json

async def monitor_conversation(conversation_id, api_key):
    uri = f"wss://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/monitor"
    headers = {
        "xi-api-key": api_key
    }
    
    async with websockets.connect(uri, subprotocols=["Sec-WebSocket-Extensions"]) as ws:
        async for message in ws:
            event = json.loads(message)
            if event['type'] == 'user_transcript':
                print(f"User said: {event['user_transcription_event']['user_transcript']}")
            elif event['type'] == 'agent_response':
                print(f"Agent said: {event['agent_response_event']['agent_response']}")
```

3. **Key requirements for monitoring:**
   - Conversation must be **active** before connecting (cannot monitor pre-initiation)
   - API key must have **`ElevenLabs Agents Write` scope**
   - User must have **`EDITOR` workspace access**
   - Connection is bidirectional (can send control commands)

---

### Current Project Integration

Your project already has webhook infrastructure for **post-call events**:

**File:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/elevenlabs_webhook.py`

Current webhook event types handled:
- `conversation.started` - Session lifecycle
- `conversation.ended` - Session termination
- `conversation.tool_call` - Dynamic UI surface generation
- `conversation.transcript` - Transcript storage

However, these are webhooks for post-call data, not real-time monitoring. For real-time events during the conversation, you need to use WebSocket monitoring instead.

---

### Important Distinctions

| Feature | Real-Time Monitoring (WebSocket) | Post-Call Webhooks (HTTP) |
|---------|----------------------------------|--------------------------|
| Timing | During active conversation | After conversation ends |
| Transport | WebSocket (bidirectional) | HTTP POST (one-way) |
| Event Types | Client events (15+ types) | Limited (transcript, audio, failure) |
| Control Capability | Yes (end call, transfer, etc.) | No |
| Enterprise Feature | Yes | Included |
| Configuration | `monitoring_enabled: true` | `post_call_webhook_id` in platform_settings |
| Authentication | API key + workspace access | Webhook signature validation |

---

### Configuration Fields Found in Agent Config

**conversation_config section** (for WebSocket monitoring):
- `monitoring_enabled` (boolean) - Enable real-time monitoring
- `monitoring_events` (array) - Which client events to stream
- `client_events` (array) - Which events go to normal clients

**platform_settings.workspace_overrides** (for post-call webhooks):
- `post_call_webhook_id` - Webhook ID for post-call events
- `webhooks.events` - Event types: ["transcript"], ["audio"], etc.
- `webhooks.send_audio` - Include base64 audio in webhook payload

---

### Recommended Architecture for Your iOS App

For real-time monitoring during voice conversations with the iOS app:

1. **On conversation start**, get `conversation_id` from ElevenLabs webhook or client
2. **In your backend**, create a dedicated monitoring connection:
   ```
   Backend → ElevenLabs WebSocket monitoring endpoint
   ```
3. **Stream events to iOS client** via:
   - Your existing WebSocket (`/ws/chat/{id}`)
   - Or separate monitoring WebSocket
   - Or Server-Sent Events (SSE)
4. **Store transcripts** in your database via existing webhook handler or during monitoring

This avoids exposing the API key to the client and lets you process/filter events server-side.

---

### Sources

- [Real-time monitoring | ElevenLabs Documentation](https://elevenlabs.io/docs/eleven-agents/guides/realtime-monitoring)
- [Post-call webhooks | ElevenLabs Documentation](https://elevenlabs.io/docs/agents-platform/workflows/post-call-webhooks)
- [Webhooks | ElevenLabs Documentation](https://elevenlabs.io/docs/overview/administration/webhooks)
- [Client events | ElevenLabs Documentation](https://elevenlabs.io/docs/agents-platform/customization/events/client-events)
- [Update agent | ElevenLabs Documentation](https://elevenlabs.io/docs/api-reference/agents/update)
- [Agent WebSockets | ElevenLabs Documentation](https://elevenlabs.io/docs/agents-platform/api-reference/agents-platform/websocket)
- [WebSocket | ElevenLabs Documentation](https://elevenlabs.io/docs/agents-platform/libraries/web-sockets)
- [API Authentication | ElevenLabs Documentation](https://elevenlabs.io/docs/api-reference/authentication)

---

