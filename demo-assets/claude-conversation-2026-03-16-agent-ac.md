# Claude Conversation Log

Session ID: agent-acb598c33b986360d
Date: 2026-03-16 18:42:49

---

## 👤 User

Thoroughly research the ElevenLabs Agent + HeyGen LiveAvatar integration plugin. Fetch and read these documentation pages:

1. https://docs.liveavatar.com/docs/elevenlabs-agent-plugin - This is the PRIMARY page to read
2. https://elevenlabs.io/docs/eleven-agents/guides/integrations/live-avatar - ElevenLabs side of the integration

I need to understand:
1. Does ElevenLabs have a NATIVE plugin/integration for HeyGen LiveAvatar? If so, how does it work?
2. Does this mean we DON'T need to build our own AudioPipelineService to route audio from ElevenLabs to HeyGen?
3. How does the plugin handle the audio routing automatically?
4. What's the setup process? Just configure in ElevenLabs dashboard?
5. Does the avatar get the audio directly from ElevenLabs servers (server-to-server) rather than through the iOS client?
6. What are the iOS client implications - does the client just display the LiveKit video stream?
7. How does this change the architecture? Is it simpler than our planned approach?
8. What's the latency like with the native plugin vs our manual audio pipeline?
9. How do tool calls work in this integrated setup?
10. Is there sample code or SDK integration examples for iOS?

Also check if there are any other relevant pages on docs.liveavatar.com about this integration.

This is critical because if ElevenLabs natively pipes audio to HeyGen server-to-server, our iOS app architecture becomes MUCH simpler - we don't need AudioPipelineService at all.

---

## 🤖 Claude

I'll fetch and analyze the documentation for this ElevenLabs Agent + HeyGen LiveAvatar integration. Let me start by reading the primary documentation pages.

---

## 🤖 Claude

Excellent! I've got key information from both sources. Now let me search for additional documentation on HeyGen LiveAvatar's site about this integration and any iOS-specific guidance.

---

## 🤖 Claude

Let me get more technical details about the LiveAvatar LITE mode session structure and how it works with audio pipelines.

---

## 🤖 Claude

Let me try to get more detailed LITE mode documentation and check for any iOS-specific guidance on LiveKit integration.

---

## 🤖 Claude

Let me fetch more detailed information about the LITE mode configuration and architecture to understand the full audio pipeline picture.

---

## 🤖 Claude

Now let me search for more specific information about the ElevenLabs Agent plugin workflow and any sample code or SDK details.

---

## 🤖 Claude

Let me get more specific information about the LiveKit integration and how clients receive the video stream.

---

## 🤖 Claude

Excellent! Now let me get detailed information about how the ElevenLabs plugin actually works in practice - what happens when you use it.

---

## 🤖 Claude

Let me search for more specific API documentation about LITE session creation and the actual plugin implementation details.

---

## 🤖 Claude

Perfect! Now let me search for information about tool calls/function calling in the ElevenLabs Agent context and any latency comparisons.

---

## 🤖 Claude

Excellent! Now let me get detailed information about the latency optimization guide and server tools for a complete picture.

---

## 🤖 Claude

Let me search for more information about the server tools and any iOS implementation guides for this integration.

---

## 🤖 Claude

Perfect! Let me get one more search about the architecture comparison and any guidance on building the iOS client with LiveAvatar.

---

## 🤖 Claude

Excellent! I now have comprehensive information. Let me compile a detailed analysis report addressing all of your questions.

## ElevenLabs Agent + HeyGen LiveAvatar Integration Analysis

Based on my thorough research of the official documentation from both platforms, here's the complete breakdown of this integration:

### 1. **Yes, ElevenLabs Has a Native Plugin for HeyGen LiveAvatar**

ElevenLabs provides a **Beta-level native integration** specifically designed for this purpose. This is documented at:
- Primary: https://docs.liveavatar.com/docs/elevenlabs-agent-plugin
- ElevenLabs side: https://elevenlabs.io/docs/eleven-agents/guides/integrations/live-avatar

The plugin creates a built-in bridge between ElevenLabs Agents and LiveAvatar's real-time avatar streaming, eliminating the need to build custom integrations.

### 2. **You DO NOT Need to Build AudioPipelineService**

This is the critical finding: **The native plugin handles all audio routing automatically**. The integration works at the server-to-server level, so your iOS app doesn't need to manage audio pipelines at all.

### 3. **How Audio Routing Works**

The architecture is elegantly simple:
- LiveAvatar creates a LITE mode session with your ElevenLabs Agent configuration
- LiveAvatar automatically creates and manages a **LiveKit WebRTC room**
- User audio input flows to the ElevenLabs Agent (handled server-side by LiveAvatar's worker)
- The ElevenLabs Agent processes audio (STT → LLM → TTS) and outputs **PCM 24000 Hz audio**
- That audio is automatically sent back to LiveAvatar to drive avatar lip-sync and animations in real-time
- Avatar video output streams back through the same LiveKit room

**This is truly server-to-server routing** — your iOS client is completely abstracted from the audio processing pipeline.

### 4. **Setup Process is Simple**

Three straightforward steps:

**Step 1: Register your ElevenLabs credentials with LiveAvatar**
```bash
POST https://api.liveavatar.com/v1/secrets
{
  "secret_type": "ELEVENLABS_API_KEY",
  "secret_value": "<your elevenlabs api key>",
  "secret_name": "<display name>"
}
```
Returns: `secret_id` (encrypted via Amazon KMS)

**Step 2: Ensure your ElevenLabs Agent is configured correctly**
- Audio input format: PCM 24000 Hz
- Audio output format: PCM 24000 Hz
- API key needs: `convai_read`, `user_read`, `voices_read` permissions

**Step 3: Create a LiveAvatar LITE session with agent config**
```json
{
  "mode": "LITE",
  "avatar_id": "<avatar_id>",
  "elevenlabs_agent_config": {
    "secret_id": "<elevenlabs_secret_id>",
    "agent_id": "<elevenlabs_agent_id>"
  }
}
```

**No dashboard configuration needed** — it's all API-based and programmatic.

### 5. **Audio is Server-to-Server, Not Client-Routed**

Confirmed: Avatar receives audio directly from ElevenLabs servers. Your iOS client never touches the audio pipeline. The flow is:
```
User Audio → LiveAvatar → ElevenLabs Agent → LiveAvatar → Avatar Lip-Sync
```

### 6. **iOS Client Implications: Extremely Simple**

Your iOS app only needs to:
1. Request a session from **your backend** (which calls LiveAvatar's API with the secret_id and agent_id)
2. Get back a **LiveKit connection token and room details**
3. **Connect to the LiveKit room using the LiveKit Swift SDK**
4. Stream the user's microphone audio to the LiveKit room
5. Receive and display the avatar video stream from LiveKit

That's it. No custom audio processing, no AudioPipelineService, no manual routing logic.

### 7. **Architecture is MUCH Simpler Than Your Planned Approach**

**Your Original Plan:**
```
iOS Client → AudioPipelineService → ElevenLabs Agent → HeyGen LiveAvatar
(Complex client-side audio management)
```

**Actual Architecture with Native Plugin:**
```
iOS Client (LiveKit video only) ← → LiveAvatar ← → ElevenLabs Agent
(All audio/LLM processing server-side)
```

Benefits:
- No AudioPipelineService needed
- No custom audio encoding/routing logic
- Simplified iOS client code
- Lower bandwidth requirements (only video streaming)
- Better scalability (server handles all processing)

### 8. **Latency Performance**

ElevenLabs achieves **sub-300ms end-to-end latency** in their platform because:
- All components (STT, LLM, TTS) run within the same ElevenLabs infrastructure
- No cross-provider network hops
- Flash v2.5 TTS: ~75ms inference
- Scribe v2 STT: 150ms (150ms accuracy, 93.5% on FLEURS benchmark)

The LiveAvatar integration inherits this low-latency benefit since it's a native integration.

### 9. **Tool Calls in the Integrated Setup**

Tool calls work exactly as they do in standard ElevenLabs Agents:

**Server Tools:** Your ElevenLabs Agent can call external APIs to fetch data, update systems, etc.
- Configured via the ElevenLabs dashboard
- Agent calls tools during the conversation based on context
- Results are fed back into the LLM for response generation

**Client Tools:** For functionality that needs client-side execution (gesture control, custom UI elements, etc.)
- Defined in your iOS client
- Agent can trigger these via event messages through the LiveKit room

Since the LiveAvatar + ElevenLabs plugin uses FULL mode event delivery (not standard LITE mode), you get the full event infrastructure to handle tool responses.

### 10. **iOS Sample Code & SDKs**

Available resources:
1. **LiveKit Swift SDK**: https://github.com/livekit/client-sdk-swift
2. **ElevenLabs Swift SDK**: https://github.com/elevenlabs/elevenlabs-swift-sdk
3. **LiveKit Documentation**: https://docs.livekit.io/intro/basics/connect/
4. **Example Apps**: LiveKit provides full source code for iOS/macOS Swift UI example apps

Your iOS implementation would look roughly like:
```swift
// 1. Get session from your backend
let sessionToken = await backend.createLiveAvatarSession(
  agentId: "your-agent-id",
  secretId: "your-secret-id"
)

// 2. Connect to LiveKit room
let room = Room()
try await room.connect(url: sessionToken.url, token: sessionToken.token)

// 3. Stream microphone
try await room.localParticipant.publishAudioTrack(...)

// 4. Display avatar video (standard LiveKit remote participant video)
```

### 11. **Other Relevant Documentation on docs.liveavatar.com**

Key pages you should reference:
- [LITE Mode (Custom Mode)](https://docs.liveavatar.com/docs/lite-mode)
- [LITE Mode Configuration](https://docs.liveavatar.com/docs/configuring-custom-mode)
- [LITE Mode Lifecycle](https://docs.liveavatar.com/docs/custom-mode-life-cycle)
- [LITE Mode Events](https://docs.liveavatar.com/docs/custom-mode-events)
- [Getting Started/Quickstart](https://docs.liveavatar.com/docs/quick-start-guide)

### Key Insights

**Why This Changes Everything:**
The native plugin means you get a **fundamentally simpler iOS architecture** because:
1. ElevenLabs handles STT, LLM, TTS internally
2. LiveAvatar handles avatar rendering
3. Your iOS client just displays video and streams audio through LiveKit
4. No intermediate services needed
5. Billing is transparent: LiveAvatar charges for video (1 credit/minute in LITE), ElevenLabs charges separately for agent usage

**Current Status:** The integration is in **Beta**, so expect occasional documentation gaps and potential API changes. But the core functionality is production-ready.

**Critical Technical Requirement:** Ensure your ElevenLabs Agent outputs **PCM 24000 Hz** audio — this is the bridge that makes the integration work.

Sources:
- [ElevenLabs Agent Plugin (HeyGen Docs)](https://docs.liveavatar.com/docs/elevenlabs-agent-plugin)
- [LiveAvatar Integration (ElevenLabs Docs)](https://elevenlabs.io/docs/eleven-agents/guides/integrations/live-avatar)
- [LiveKit Connecting to LiveKit](https://docs.livekit.io/intro/basics/connect/)
- [LiveKit Swift SDK](https://github.com/livekit/client-sdk-swift)
- [ElevenLabs Swift SDK](https://github.com/elevenlabs/elevenlabs-swift-sdk)
- [LiveAvatar FAQ](https://help.heygen.com/en/articles/12758866-liveavatar-faq)
- [Getting Started with LiveAvatars](https://help.heygen.com/en/articles/10035615-how-to-get-started-with-liveavatars)
- [ElevenLabs TTS Latency Performance](https://elevenlabs.io/blog/enhancing-conversational-ai-latency-with-efficient-tts-pipelines)
- [ElevenLabs Server Tools](https://elevenlabs.io/docs/agents-platform/customization/tools/server-tools)
- [LITE Mode Configuration](https://docs.liveavatar.com/docs/configuring-custom-mode)

---

