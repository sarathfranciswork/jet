# Claude Conversation Log

Session ID: agent-a1618a085a6ff7877
Date: 2026-03-16 17:12:44

---

## 👤 User

Research the Retell AI and ElevenLabs Agent platforms to understand their capabilities for a unified AI brain approach. Fetch and read the following documentation:

**Retell AI:**
- https://docs.retellai.com/api-references/introduction
- https://docs.retellai.com/get-started/quick-start
- https://docs.retellai.com/features/custom-llm
- https://docs.retellai.com/api-references/create-web-call
- https://docs.retellai.com/retell-llm/overview

I need to understand:
1. Can Retell be used as the central AI brain (LLM orchestrator) that handles conversation context?
2. Does Retell support custom tool calling (like our CVS MCP tools)?
3. Can Retell's audio output be streamed to an external system (like HeyGen avatar)?
4. Does Retell have iOS SDK support?
5. How does Retell handle conversation state/context persistence?
6. Can Retell be used for text chat as well, or is it voice-only?
7. What is the WebSocket protocol for real-time communication?

**ElevenLabs Conversational AI:**
- https://elevenlabs.io/docs/conversational-ai/overview
- https://elevenlabs.io/docs/conversational-ai/customization/tools
- https://elevenlabs.io/docs/conversational-ai/customization/dynamic-variables
- https://elevenlabs.io/docs/api-reference/conversational-ai

I need to understand:
1. Can ElevenLabs agent platform be used for both chat AND voice?
2. Does it support custom tool calling?
3. Can it maintain conversation context across modality switches?
4. Does it have iOS SDK?
5. Can you stream TTS audio output to an external system?
6. How does the agent platform differ from just the TTS API?

The goal is to determine which platform (Retell vs ElevenLabs) is better suited as the unified AI brain for chat + voice + video avatar.

---

## 🤖 Claude

I'll research both Retell AI and ElevenLabs Agent platforms by fetching their documentation. Let me start by retrieving all the documentation links you provided.

---

## 🤖 Claude

I'm encountering 404 errors on most of the documentation links. Let me try searching for the current documentation locations and alternative resources for both platforms.

---

## 🤖 Claude

Let me fetch the actual documentation pages that were found in the search results.

---

## 🤖 Claude

Let me search for more specific Retell and ElevenLabs documentation and try alternative URLs.

---

## 🤖 Claude

Now let me fetch the detailed comparison pages and additional documentation.

---

## 🤖 Claude

Let me search for more specific documentation on both platforms.

---

## 🤖 Claude

Let me fetch the specific documentation pages for MCP and tools on both platforms.

---

## 🤖 Claude

Now let me search for more specific information about both platforms' capabilities for unified architecture.

---

## 🤖 Claude

Perfect! I now have comprehensive information. Let me fetch a few more specific documentation pages to round out the research.

---

## 🤖 Claude

Excellent! I now have enough comprehensive research. Let me compile the findings into a detailed analysis.

## Comprehensive Research: Retell AI vs ElevenLabs for Unified AI Brain Architecture

Based on my research of both platforms' documentation and capabilities, here's a detailed analysis to help you determine which is better suited as the unified AI brain for your chat + voice + video avatar application.

---

## EXECUTIVE SUMMARY

**For a Unified AI Brain Approach:**
- **ElevenLabs Agents Platform** is better suited as a central AI brain for multimodal (chat + voice) orchestration with solid MCP/custom LLM support
- **Retell AI** is more specialized for voice-first enterprise telephony with excellent custom LLM integration but less emphasis on multimodal flexibility

---

## DETAILED FINDINGS

### 1. Central AI Brain Capabilities (LLM Orchestration)

#### Retell AI
**Strengths:**
- Exceptional custom LLM support via WebSocket with bidirectional communication
- Full control over conversation flow with custom server implementations
- Real-time transcript streaming and interrupt capabilities
- Supports bring-your-own-LLM architecture (OpenAI, Claude, custom implementations)
- WebSocket protocol enables dynamic conversation control

**Limitations:**
- Originally voice-focused; text chat is a secondary feature
- Higher latency (620ms average, <800ms p99) due to orchestration layer
- Less emphasis on unified brain; more of a voice orchestrator
- No built-in MCP support (unlike ElevenLabs)

**Custom LLM Architecture:**
- Uses WebSocket with JSON event streaming
- Event types: `ping_pong`, `update_only`, `response_required`, `reminder_required`, `tool_call_invocation`, `tool_call_result`
- Supports dynamic variables injection into prompts
- Full transcript and context passed with each turn

---

#### ElevenLabs Agents Platform
**Strengths:**
- Built as a unified multi-modal platform (voice + text + video)
- Native support for **Model Context Protocol (MCP)** - directly integrates with MCP servers
- Custom LLM via OpenAI-compatible endpoints (Chat Completions API and Responses API)
- Lower latency (sub-300ms) due to end-to-end ownership of voice stack
- True multimodality with simultaneous voice + text processing
- Conversation context persistence with system variables (`system__conversation_id`, `system__agent_turns`)
- Dynamic variables for runtime personalization
- Support for external agent integration with state management

**Limitations:**
- Less mature enterprise telephony features (warm transfer, IVR, DTMF)
- Smaller ecosystem of pre-built integrations vs Retell
- Still relatively newer platform compared to Retell

**Custom LLM Architecture:**
- OpenAI-compatible REST endpoints
- Supports both Chat Completions and Responses API formats
- Can trigger system tools to control conversation flow
- LLM Cascading for failover across providers
- Full flexibility in model selection and provider switching

---

### 2. Custom Tool Calling Support (MCP/Function Calling)

#### Retell AI
**Function Calling Capabilities:**
- Supports tool calling via agent frameworks (Single Prompt, Conversation Flow)
- Custom tool invocation through webhook triggers
- Tool call outputs can be weaved into transcripts
- Integration with n8n for workflow automation
- Pre-built tools: call transfer, call ending, calendar integration (Cal.com), appointment booking

**Limitations:**
- No native MCP support
- Function calling marked as "not production ready" in documentation - requires custom state management to prevent duplicate calls
- Less sophisticated tool orchestration compared to ElevenLabs

---

#### ElevenLabs Agents Platform
**Tool Support (Both Native and MCP):**

**Native Tools:**
- Server-side tools via HTTP/API calls
- Client-side tools for browser/UI integration
- System tools for conversation control
- Pre-built integrations (400+ available): Salesforce, Zendesk, Stripe, etc.

**Model Context Protocol (MCP) Support:**
- Official ElevenLabs MCP server (fully maintained)
- Can connect any MCP-compatible server to agents
- Works with Claude Desktop, Cursor, Windsurf, OpenAI Agents
- Flexible approval controls at MCP server and individual tool levels
- Supports both SSE and HTTP streamable MCP transport

**Advantages:**
- MCP provides standardized tool integration without custom implementations
- Can directly integrate your CVS MCP tools without custom wrapper code
- More mature and production-ready tool ecosystem

---

### 3. iOS SDK Support

#### Retell AI
- **No official iOS SDK**
- JavaScript SDK available for web
- Must use REST API directly or JavaScript SDK via web view for mobile
- Better for phone/web call integrations than native mobile apps

---

#### ElevenLabs Agents Platform
- **Official Swift SDK** (iOS 14.0+, macOS 11.0+, Swift 5.9+)
- React Native SDK with WebRTC support for cross-platform mobile
- Expo support for both iOS and Android
- Optimized for native mobile with reactive UI patterns
- Built-in microphone and audio handling

**Winner for iOS:** ElevenLabs (by far)

---

### 4. Audio Output Streaming to External Systems (HeyGen Avatar)

#### Retell AI
**Audio Streaming Capability:**
- Supports WebRTC-based audio streaming
- Audio WebSocket API (though marked as deprecated in favor of WebRTC)
- Can stream raw audio bytes via WebSocket
- Integrates with Twilio, Vonage, Telnyx for telephony

**Limitations:**
- No documented direct integration with HeyGen
- Would require custom implementation to extract and route audio streams
- Higher latency (620ms) makes real-time avatar sync challenging

---

#### ElevenLabs Agents Platform
**Audio Streaming:**
- Built on WebRTC with sub-300ms latency
- Native real-time audio output
- Better suited for avatar integration due to lower latency
- Streaming audio generation (not just batch generation)
- Can be integrated with HeyGen's Streaming Avatar SDK via WebRTC

**Architecture Advantage:**
- Lower latency (300ms vs 620ms) provides better lip-sync with avatars
- WebRTC transport is more suitable for avatar streaming

---

### 5. Conversation State/Context Persistence

#### Retell AI
**Context Management:**
- Transformer architecture maintains context throughout conversation
- Multi-turn conversation support with full history
- Conversation Flow nodes with specific prompts and transition logic
- Dynamic variable mapping and context inheritance in multi-agent transfers
- Call metadata storage
- Post-call analytics and call state tracking

**Limitations:**
- Context primarily designed for single-call scenarios
- Limited cross-session persistence
- Context reset between calls

---

#### ElevenLabs Agents Platform
**Context Management:**
- System variables: `system__conversation_id`, `system__agent_turns`
- Conversation identifiers for tracking across channels
- Dynamic variables for runtime personalization
- Multi-channel state persistence (can follow customer across voice/text/web)
- Optional integration with Mem0 for persistent memory across sessions
- External agent state management support
- Workflow-based context tracking across complex multi-step conversations

**Advantages:**
- Better support for cross-session persistence
- Multi-channel context (voice → text → voice)
- Integration with external memory systems
- More sophisticated context management overall

---

### 6. Text Chat Support (Non-Voice)

#### Retell AI
**Text Capabilities:**
- SMS support (via SMS nodes and standalone texting agents)
- Chatbot support for web/in-app chat
- Omni-channel approach (voice + text + hybrid flows)
- Same compliance as voice (HIPAA, SOC 2, PCI-DSS)

**Limitations:**
- Text/SMS presented as newer features, not core to platform
- Not as seamlessly integrated as voice
- Less documentation on text-specific capabilities

---

#### ElevenLabs Agents Platform
**Chat Capabilities:**
- **Native Chat Mode** - first-class feature for text-only conversations
- Can enable Chat Mode instantly on existing voice agents
- Web integration via single HTML snippet
- Dedicated concurrency pool for text conversations (independent of voice limits)
- Full multimodality with simultaneous voice + text processing
- Identical agent logic for voice and text
- Support for high-throughput chat applications (customer support, chatbots)

**Advantages:**
- Chat is a native, first-class capability (not an afterthought)
- Better for applications mixing voice and text in same conversation
- Higher throughput capacity for text-only scenarios

---

### 7. WebSocket Protocol & Real-Time Communication

#### Retell AI
**WebSocket Protocol (LLM WebSocket):**
- **Protocol:** wss:// with `/llm-websocket` route
- **Message Format:** JSON-stringified text events with type field
- **Retell → Server Events:** `ping_pong` (keepalive every 2s), `call_details`, `update_only`, `response_required`, `reminder_required`
- **Server → Retell Events:** `config`, `response`, `agent_interrupt`, `tool_call_invocation`, `tool_call_result`, `metadata`, `update_agent`
- **Latency Tracking:** Includes round-trip latency measurement
- **Auto-Reconnect:** Automatic reconnection with ping/pong keepalive

**Use Case:** Perfect for implementing a custom unified brain - you control the entire LLM orchestration logic

---

#### ElevenLabs Agents Platform
**API Architecture:**
- REST API for agent management and conversation control
- WebSocket API for real-time communication
- OpenAI-compatible endpoints for custom LLMs
- WebRTC for audio streaming (lower latency than WebSocket)
- Post-call webhooks for async event handling

**Advantage:** More flexible protocol options depending on use case

---

## RECOMMENDATION FOR UNIFIED AI BRAIN

### Use ElevenLabs Agents Platform If:
1. **You need multimodal support** (voice + text + video avatar in unified system)
2. **iOS/mobile app support is required** (native Swift SDK)
3. **Lower latency is critical** (300ms vs 620ms for avatar lip-sync)
4. **You want to use MCP tools** (direct integration with your CVS MCP tools)
5. **You need cross-channel context** (seamlessly switch voice → text → voice)
6. **You want text chat as a first-class feature** (not an afterthought)
7. **Cost matters** (more efficient due to end-to-end ownership)

### Use Retell AI If:
1. **Enterprise telephony is primary** (warm transfer, IVR, DTMF needed)
2. **You need mature compliance features** (SOC 2 Type I & II, HIPAA BAA)
3. **You're building call center automation** (not general multimodal AI)
4. **You want maximum control via custom LLM** (WebSocket gives you full control)
5. **Phone numbers and carrier integrations are critical** (more partnerships)

---

## UNIFIED BRAIN ARCHITECTURE RECOMMENDATION

**For your use case (chat + voice + video avatar):**

```
ElevenLabs Agents Platform
├── Custom LLM (OpenAI-compatible endpoint)
├── MCP Tools Integration (CVS MCP tools)
├── Voice Channel (native, sub-300ms latency)
├── Text Channel (Chat Mode, native)
└── Avatar Integration (HeyGen via WebRTC)
```

**Why ElevenLabs wins for unified brain:**
1. True multimodality - not adding text as an afterthought
2. MCP support means you can plug in your CVS tools without custom wrappers
3. Lower latency for better avatar synchronization
4. iOS SDK for mobile client apps
5. Native support for context across modalities
6. Better designed for applications mixing multiple modalities

**For the avatar specifically:**
- Use HeyGen Streaming Avatar SDK with ElevenLabs' WebRTC audio output
- ~300ms latency from ElevenLabs provides acceptable avatar lip-sync
- Text responses can be shown in real-time in chat interface
- Voice responses stream to avatar while chat displays transcript

---

## SOURCES

- [Retell AI Introduction](https://docs.retellai.com/general/introduction)
- [Retell AI Quick Start](https://docs.retellai.com/get-started/quick-start)
- [Retell AI LLM WebSocket Protocol](https://docs.retellai.com/api-references/llm-websocket)
- [Retell AI Function Calling](https://docs.retellai.com/integrate-llm/integrate-function-calling)
- [Retell AI Custom LLM Overview](https://docs.retellai.com/integrate-llm/overview)
- [Retell AI Web Call Integration](https://docs.retellai.com/deploy/web-call)
- [Retell AI SDK Documentation](https://docs.retellai.com/get-started/sdk)
- [Retell AI vs ElevenLabs Comparison (Retell)](https://www.retellai.com/comparisons/retell-vs-elevenlabs)
- [ElevenLabs vs Retell AI Blog Post](https://elevenlabs.io/blog/elevenlabs-vs-retell-ai)
- [ElevenLabs Agents Platform Overview](https://elevenlabs.io/docs/agents-platform/overview)
- [ElevenLabs Custom LLM Integration](https://elevenlabs.io/docs/agents-platform/customization/llm/custom-llm)
- [ElevenLabs Model Context Protocol (MCP)](https://elevenlabs.io/docs/agents-platform/customization/tools/mcp)
- [ElevenLabs Chat Mode](https://elevenlabs.io/docs/agents-platform/guides/chat-mode)
- [ElevenLabs iOS SDK (Swift)](https://elevenlabs.io/docs/conversational-ai/libraries/conversational-ai-sdk-swift)
- [ElevenLabs Conversational AI Overview](https://elevenlabs.io/docs/conversational-ai/overview)
- [ElevenLabs Agents Platform Tools](https://elevenlabs.io/docs/agents-platform/customization/tools)
- [ElevenLabs Agents Chat Mode Blog](https://elevenlabs.io/blog/elevenlabs-agents-now-support-chat-mode)
- [Retell AI MCP Integration Support](https://www.retellai.com/blog/connect-any-ai-voice-agent-to-mcp-with-retell-ai-mcp-node)
- [HeyGen Streaming Avatar SDK](https://docs.heygen.com/docs/streaming-avatar-sdk)
- [Retell AI Function Calling Documentation](https://docs.retellai.com/integrate-llm/integrate-function-calling)

---

