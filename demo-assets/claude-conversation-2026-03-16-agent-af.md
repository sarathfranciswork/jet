# Claude Conversation Log

Session ID: agent-afa66c8d18fe61cf8
Date: 2026-03-16 17:12:36

---

## 👤 User

Research the HeyGen Live Avatar API, specifically the "custom mode" configuration. The user provided this documentation link: https://docs.liveavatar.com/docs/configuring-custom-mode

Fetch and thoroughly read this documentation page. Then explore related pages on the same docs site to understand:

1. What is "custom mode" in HeyGen Live Avatar?
2. How does custom mode allow using an external LLM instead of HeyGen's built-in brain?
3. What are the audio input/output mechanisms? Can you stream audio TO the avatar for lip-syncing?
4. What is the WebSocket/API protocol for real-time communication?
5. What SDKs are available (especially iOS)?
6. How does the avatar rendering work - is it a video stream, WebRTC, or something else?
7. What are the latency characteristics?
8. Can you pipe external TTS audio directly to the avatar for lip sync?

Also fetch these related pages if they exist:
- https://docs.liveavatar.com/docs/overview
- https://docs.liveavatar.com/docs/getting-started
- https://docs.liveavatar.com/docs/api-reference
- Any iOS SDK documentation

The goal is to determine if HeyGen Live Avatar can work as a "dumb avatar" that just lip-syncs to audio from an external AI/TTS system (like Retell or ElevenLabs).

---

## 🤖 Claude

I'll fetch and thoroughly read the HeyGen Live Avatar documentation to understand custom mode and the integration capabilities you're asking about.

---

## 🤖 Claude

Good start. Let me search for more specific documentation pages on the site:

---

## 🤖 Claude

Let me try more URL variations:

---

## 🤖 Claude

Let me try the root docs page to find available documentation:

---

## 🤖 Claude

Now let me get more detailed pages on LITE mode:

---

## 🤖 Claude

Let me try alternative URL paths based on what I found:

---

## 🤖 Claude

Let me try a broader search:

---

## 🤖 Claude

Let me fetch the HeyGen Help Center articles I found:

---

## 🤖 Claude

Let me fetch more specific documentation:

---

## 🤖 Claude

Great! Let me fetch the key technical documentation I found:

---

## 🤖 Claude

Excellent! Now let me get more specific details on LiveAvatar and the newer platform:

---

## 🤖 Claude

Let me fetch the ElevenLabs LiveAvatar documentation I found:

---

## 🤖 Claude

Perfect! Now let me fetch the LITE Mode Events page:

---

## 🤖 Claude

Excellent! Let me get one more piece about the rendering architecture:

---

## 🤖 Claude

Perfect! I have comprehensive information. Let me compile my findings into a thorough report.

## HeyGen Live Avatar Custom Mode (LITE Mode) Research Summary

Based on my thorough research of the HeyGen Live Avatar documentation and related resources, here are the answers to your questions:

### 1. What is "custom mode" in HeyGen Live Avatar?

**Custom Mode is now called LITE Mode.** It's a developer-focused configuration where HeyGen provides only the avatar rendering and video streaming layer. You maintain full control over the conversational infrastructure and are responsible for orchestrating your own ASR (speech-to-text), LLM (language model), and TTS (text-to-speech) stack. This is ideal for developers who already have existing conversation infrastructure or want granular control.

### 2. How does custom mode allow using an external LLM instead of HeyGen's built-in brain?

In LITE Mode, you are entirely responsible for configuring and running your own LLM. According to the documentation, "In this mode, we only provide the WebRTC room and media transport — you are responsible for configuring and running your own ASR, LLM, and TTS stack." You can connect any LLM you use (like OpenAI, Anthropic, etc.), giving you complete flexibility in model selection and customization.

### 3. What are the audio input/output mechanisms? Can you stream audio TO the avatar for lip-syncing?

**Yes, you can stream audio directly to the avatar for lip-syncing.** The LITE Mode supports the following audio mechanisms:

- **Audio Input:** You send audio via WebSocket using the `agent.speak` command with PCM 16-bit 24kHz audio encoded in Base64
- **Audio Output:** The avatar receives the audio stream and automatically lip-syncs to it
- **Format Requirements:** Audio must be PCM 16-bit 24kHz format (crucially, 24kHz, not 48kHz)
- **Chunking:** Send audio in chunks (~1 second per packet) to avoid >1MB messages
- **End Signaling:** Use `avatar.speak_end` to signal the end of audio streaming

This is critical for your use case: **HeyGen Live Avatar in LITE Mode is specifically designed to work as a "dumb avatar" that just lip-syncs to audio from external sources.** You can pipe TTS audio directly from any provider (Retell, ElevenLabs, Azure, etc.) and the avatar will synchronize its mouth movements.

### 4. What is the WebSocket/API protocol for real-time communication?

**LITE Mode uses WebSocket for bidirectional event-based communication with JSON message format:**

**Commands (Client → Server):**
- `agent.speak` - Stream audio chunks (Base64 encoded PCM 16-bit 24kHz)
- `avatar.speak_end` - Signal end of audio
- `agent.interrupt` - Stop all scheduled commands and clear speaking events
- `agent.start_listening` - Transition avatar to listening state
- `agent.stop_listening` - Move avatar to idle state
- `session.keep_alive` - Maintain session beyond 5-minute idle timeout

**Events (Server → Client):**
- `session.state_updated` - Session state changes (connecting, connected, closing, closed)
- `agent.speak_started` - Avatar begins speaking
- `agent.speak_ended` - Avatar finishes speaking

All events are JSON-formatted strings transmitted over WebSocket.

### 5. What SDKs are available (especially iOS)?

HeyGen provides:

- **Streaming Avatar SDK** - TypeScript/Node.js package for real-time integration
- **Web SDK** - Browser-based integration
- **iOS/Mobile** - Native Swift/SwiftUI demo available on GitHub (though HeyGen is phasing out the older "Interactive Avatar" in favor of the newer LiveAvatar platform)
- **React Native** - Community implementations available
- **LiveKit Integration** - SDKs available for various platforms including Swift for iOS

**Important note:** HeyGen is discontinuing its older "Interactive Avatar" on March 31, 2026, and recommends using LiveAvatar instead. For native iOS implementation with LiveAvatar, you'll use LiveKit's Swift SDK.

### 6. How does the avatar rendering work - is it a video stream, WebRTC, or something else?

**LiveAvatar uses WebRTC for real-time video streaming.** The system works as follows:

- Avatar rendering is done on HeyGen's servers and streamed as live video via WebRTC
- When you start a LITE Mode session, a LiveKit room is created with an agent token for your connection
- The avatar video streams directly into the LiveKit room as H.264 video
- You can optionally bring your own WebRTC infrastructure (Agora or LiveKit) instead of using HeyGen's default
- The rendering is real-time (not pre-recorded), using HeyGen's advanced rendering engine for lifelike facial animation, expressions, and lip-sync

### 7. What are the latency characteristics?

Based on documentation:
- **WebRTC provides low-latency communication** with sub-millisecond optimization
- **Sub-300ms audio latency is considered critical** for natural interactions
- **1080p streaming increases latency** and requires 1080p source footage for the avatar
- **Mobile performance may have higher latency**, though optimization is an ongoing focus
- Immediate interruptibility (barge-in support) is essential for natural conversation flow

### 8. Can you pipe external TTS audio directly to the avatar for lip sync?

**Yes, absolutely.** This is the primary use case for LITE Mode. Multiple TTS providers can be integrated:

- **ElevenLabs** - Has official integration with LiveAvatar in LITE Mode. The ElevenLabs agent's audio output drives the avatar's lip sync in real-time
- **Retell, Azure, Google Cloud TTS, etc.** - Can be used by implementing your own ASR/TTS pipeline and sending audio chunks via the WebSocket `agent.speak` command
- **Audio Format:** Audio must be PCM 24000 Hz for ElevenLabs, PCM 16-bit 24kHz for general LITE mode

When using ElevenLabs integration specifically, you need to configure "audio input and output formats set to PCM 24000 Hz" in the ElevenLabs agent settings.

### Architecture Summary for Your Use Case

For a "dumb avatar" that just lip-syncs to external TTS (like Retell or ElevenLabs):

1. **Your AI/LLM** generates text
2. **Your TTS Provider** (Retell, ElevenLabs, etc.) converts text to audio
3. **Your application** sends audio chunks to LiveAvatar LITE Mode via WebSocket in PCM format
4. **LiveAvatar** receives the audio and generates synchronized video with proper lip-sync
5. **WebRTC** streams the video to your client application

**Credit Cost:** 1 credit per minute of avatar streaming in LITE Mode (vs. 2 credits/minute for FULL Mode).

### Key Limitations

- Interactive Avatar (older version) is being deprecated as of March 31, 2026
- Direct audio input for lip-sync was not supported in the older Interactive Avatar API, but LITE Mode specifically supports it
- 4K output is not currently supported due to latency constraints
- Audio must be in specific PCM formats (16-bit 24kHz)

### Sources:

- [LITE Mode Configuration](https://docs.liveavatar.com/docs/configuring-custom-mode)
- [LITE Mode Overview](https://docs.liveavatar.com/docs/lite-mode)
- [LITE Mode Life Cycle](https://docs.liveavatar.com/docs/custom-mode-life-cycle)
- [LITE Mode Events](https://docs.liveavatar.com/docs/custom-mode-events)
- [LiveAvatar FAQ](https://help.heygen.com/en/articles/12758866-liveavatar-faq)
- [Getting Started with LiveAvatars](https://help.heygen.com/en/articles/10035615-how-to-get-started-with-liveavatars)
- [Introducing LiveAvatar](https://help.heygen.com/en/articles/12758516-introducing-liveavatar)
- [Streaming Avatar SDK](https://docs.heygen.com/docs/streaming-avatar-sdk)
- [WSS Audio to Video API](https://docs.heygen.com/reference/audio-to-video-api)
- [Streaming API Integration with LiveKit v2](https://docs.heygen.com/docs/streaming-api-integration-with-livekit-v2)
- [ElevenLabs LiveAvatar Integration](https://elevenlabs.io/docs/eleven-agents/guides/integrations/live-avatar)
- [Demo: Create an iOS App featuring Interactive Avatar](https://docs.heygen.com/docs/streaming-avatar-ios-sdk)
- [GitHub - HeyGen StreamingAvatarSDK](https://github.com/HeyGen-Official/StreamingAvatarSDK)
- [GitHub - liveavatar-web-sdk](https://github.com/heygen-com/liveavatar-web-sdk)
- [Building a Real-Time AI Avatar Assistant with OpenAI Realtime + HeyGen](https://medium.com/@silverskytechnology/building-a-real-time-ai-avatar-assistant-with-openai-realtime-heygen-cb5f222732a5)

---

