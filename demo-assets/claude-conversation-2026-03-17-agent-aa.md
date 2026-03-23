# Claude Conversation Log

Session ID: agent-aa63af8f96d3da477
Date: 2026-03-17 14:19:08

---

## 👤 User

Research how the ElevenLabs Conversational AI agent handles multimodal input (images, files). I need to know:

1. Does the ElevenLabs WebSocket protocol support sending images/files alongside text messages?
2. Check the SDK source for any `multimodal_message` or `file_input` event types
3. Check the asyncapi schema for file/image support

Read these files:
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Internal/Utilities/EventSerializer.swift — look for multimodal, file, image
- /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Public/ElevenLabs/Events/OutgoingEvents.swift — look for file, multimodal, image events

Also search for "multimodal" and "file" in all Swift files under the SDK:
grep -r "multimodal\|file_input\|FileInput\|image\|Image" in the SDK Sources directory

Also use WebFetch to check:
- https://elevenlabs.io/docs/conversational-ai/customization/multimodal — multimodal docs
- https://elevenlabs.io/docs/api-reference/conversational-ai — API reference for file support

Report exact findings: does ElevenLabs support image/file input in conversations? If so, what's the exact protocol?

---

## 🤖 Claude



I'll research ElevenLabs Conversational AI multimodal support by reading the SDK source files, searching the codebase, and fetching documentation.

---

## 🤖 Claude



Now let me fetch the ElevenLabs documentation pages and also search for the AsyncAPI schema file and incoming events.

---

## 🤖 Claude

Now let me try the correct documentation URLs and also search the JavaScript/React SDK for multimodal support.

---

## 🤖 Claude

Let me try the actual ElevenLabs docs site with different URL patterns and also check the Conversation.swift public API for any send methods.

---

## 🤖 Claude

Now let me try the actual ElevenLabs docs with different URL patterns and check the JavaScript SDK for multimodal support as a cross-reference.

---

## 🤖 Claude

Let me also check the Message model and try the ElevenLabs changelog/blog for multimodal announcements.

---

## 🤖 Claude

Let me try a web search for this topic.

---

## 🤖 Claude

Let me also check the README for the SDK and look at the `custom_llm_extra_body` path more carefully, as that might be a mechanism for passing image data.

---

## 🤖 Claude

I now have a thorough picture. Let me also check the `contextual_update` mechanism and the `custom_llm_extra_body` more carefully, as those might be indirect workarounds. Let me also look at the Documentation folder referenced in the README.

---

## 🤖 Claude

I now have a comprehensive picture of the entire ElevenLabs Conversational AI SDK. Here is my complete findings report.

---

## Research Findings: ElevenLabs Conversational AI Multimodal Input Support

### Answer: ElevenLabs Conversational AI does NOT support sending images or files during a conversation.

This conclusion is based on exhaustive analysis of three authoritative sources: the AsyncAPI schema, the Swift SDK source code, and the SDK documentation.

---

### 1. AsyncAPI Schema (Definitive Protocol Spec)

**File:** `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Internal/Protocol/schemas/agent.asyncapi.yaml`

The complete list of **Client-to-Server (outgoing) message types** is:

| Message Type | Purpose |
|---|---|
| `UserAudio` | Base64-encoded PCM/u-law audio chunk |
| `Pong` | Response to server ping |
| `UserMessage` | Plain text string (`text` field only) |
| `UserActivity` | Signal that user is active |
| `UserFeedback` | Like/dislike score |
| `ClientToolResult` | String result from client tool execution |
| `MCPToolApprovalResult` | Approve/reject MCP tool call |
| `ContextualUpdate` | Plain text context injection |
| `ConversationInitiation` | Config overrides at session start |

There is **no** `multimodal_message`, `file_input`, `image_message`, `user_image`, or any binary content message type. The `UserMessagePayload` schema accepts only `{ type: "user_message", text: string }`. No `content` array, no `image_url` blocks, no `file` field.

---

### 2. Swift SDK Source Code (v3.1.0)

**`OutgoingEvents.swift`** defines the `OutgoingEvent` enum with exactly these cases:
- `.pong`, `.userAudio`, `.conversationInit`, `.feedback`, `.clientToolResult`, `.contextualUpdate`, `.userMessage`, `.userActivity`, `.mcpToolApprovalResult`

The `UserMessageEvent` struct has a single field: `public let text: String?`

**`EventSerializer.swift`** serializes `userMessage` as: `{ "type": "user_message", "text": messageEvent.text }` -- no image/file field.

**`Conversation.swift`** exposes exactly one method for sending content: `sendMessage(_ text: String)` -- accepts only a plain string.

**`Message.swift`** model: `content` is `String` only. No image attachment, no multimodal content array.

**`SentMessage.swift`**: The `Content` enum has a single case: `.userText(String)`.

A grep for `multimodal`, `file_input`, `FileInput`, `image`, `Image`, `vision`, `screenshot`, `ImageMessage`, `MultimodalMessage` across the entire SDK Sources directory returned **zero relevant results** (only `visionOS` platform references and `base64` for audio encoding).

---

### 3. `custom_llm_extra_body` -- Not a Viable Workaround

The `custom_llm_extra_body` field in `ConversationInitiationPayload` is typed as `[String: String]` in the Swift SDK and described as "Additional parameters passed to the LLM provider" in the schema. It is only sent **once at connection initiation time**, not per-message. It cannot be used to inject image content into individual conversation turns.

---

### 4. `contextual_update` -- Text Only

The `ContextualUpdatePayload` schema is `{ type: "contextual_update", text: string }`. It only accepts plain text. You could theoretically base64-encode an image into the text field, but the server-side orchestrator would treat it as a text string, not as an image for a vision model.

---

### 5. Documentation Confirms Absence

The SDK's `README.md` and `Documentation/Usage.md` cover: voice conversations, text-only mode, tool calls, MCP integration, feedback, contextual updates, audio pipeline, reconnection, VAD. There is **no mention** of multimodal, image, file, vision, or screenshot support anywhere.

ElevenLabs documentation URLs for multimodal features all return **404**, confirming no such documentation page exists:
- `/docs/conversational-ai/customization/multimodal` -- 404
- `/docs/conversational-ai/guides/multimodal` -- 404
- `/docs/conversational-ai/guides/multimodal-conversations` -- 404
- `/docs/conversational-ai/customization/multimodal-agent` -- 404

---

### Summary

| Question | Answer |
|---|---|
| Does the WebSocket protocol support images/files? | **No.** No message type exists for it. |
| Any `multimodal_message` or `file_input` event type? | **No.** Zero matches in SDK source or schema. |
| Does the AsyncAPI schema support file/image? | **No.** All payloads are text or audio-only. |
| Can `custom_llm_extra_body` be used? | **No.** It's `[String: String]`, sent once at init, not per-turn. |
| Can `contextual_update` carry images? | **No.** Text-only field, server treats it as text. |

**Bottom line:** If you need the ElevenLabs agent to process images/files during a conversation, you would need to build an indirect workaround -- for example, using a **client tool** that accepts an image on the app side, processes it locally (e.g., via a local vision model or a separate API call to GPT-4o), and returns the description as a string result back to the ElevenLabs agent via `sendToolResult`. The ElevenLabs protocol itself has no native path for multimodal input.

---

