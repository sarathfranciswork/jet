# Claude Conversation Log

Session ID: agent-a48add5fccadd7ce2
Date: 2026-03-17 20:04:29

---

## 👤 User

Fetch and research the ElevenLabs Swift voice starter kit to understand how to implement voice conversations with the ElevenLabs SDK.

1. Fetch https://raw.githubusercontent.com/elevenlabs/voice-starterkit-swift/main/VoiceStarterKit/ContentView.swift
2. Fetch https://raw.githubusercontent.com/elevenlabs/elevenlabs-swift-sdk/main/Sources/ElevenLabs/Conversation.swift (or similar path)
3. Fetch https://raw.githubusercontent.com/elevenlabs/voice-starterkit-swift/main/VoiceStarterKit/VoiceStarterKitApp.swift
4. Search for more files: https://api.github.com/repos/elevenlabs/voice-starterkit-swift/git/trees/main?recursive=1
5. After getting the file tree, fetch any relevant Swift files

Return the COMPLETE content of the key files, especially how they:
- Initialize the ElevenLabs Conversation
- Start/end voice sessions
- Handle callbacks (onConnect, onMessage, onDisconnect, etc.)
- Toggle mute
- Handle agent speaking state

Also look for documentation on how to use the ElevenLabs Swift SDK for voice, specifically what API does `ElevenLabs.Conversation` provide.

---

## 🤖 Claude

I'll fetch all the relevant files in parallel to research the ElevenLabs Swift voice starter kit.

---

## 🤖 Claude

Let me fetch all the files in parallel.

---

## 🤖 Claude

Now I have the file trees. Let me fetch all the key files in parallel.

---

## 🤖 Claude

Now let me fetch the remaining key files in parallel.

---

## 🤖 Claude

Here is the complete research summary on the ElevenLabs Swift voice SDK:

---

## ElevenLabs Swift SDK - Complete API Reference

### SDK Version: 3.1.0
### Transport Layer: LiveKit WebRTC (not WebSocket directly)

---

### 1. Initialization and Starting a Conversation

Three authentication patterns:

**Public agent (no backend needed):**
```swift
let conversation = try await ElevenLabs.startConversation(
    agentId: "agent_123",
    config: ConversationConfig(...)
)
```

**Private agent via backend token:**
```swift
let token = try await myBackend.fetchToken()
let conversation = try await ElevenLabs.startConversation(
    conversationToken: token,
    config: ConversationConfig(...)
)
```

**Custom token provider (lambda):**
```swift
let conversation = try await ElevenLabs.startConversation(
    tokenProvider: { try await myBackend.fetchToken() }
)
```

The starter kit uses the `auth: ElevenLabsConfiguration` overload:
```swift
let auth = ElevenLabsConfiguration.publicAgent(id: agentId)
let newConversation = try await ElevenLabs.startConversation(auth: auth, config: config)
```

The `Conversation` object is `@MainActor final class ObservableObject`. All calls must be from `@MainActor`.

---

### 2. ConversationConfig - All Callbacks

`ConversationConfig` is a `Sendable` struct with these key callbacks:

| Callback | Signature | Purpose |
|---|---|---|
| `onAgentReady` | `() -> Void` | Agent initialized, conversation can begin |
| `onDisconnect` | `(DisconnectionReason) -> Void` | Agent or user ended the session; `.agent`, `.user`, `.error` |
| `onStartupStateChange` | `(ConversationStartupState) -> Void` | Startup phase transitions (for progress UI) |
| `onError` | `(ConversationError) -> Void` | Non-fatal and startup errors |
| `onAgentResponse` | `(String, Int) -> Void` | Finalized agent transcript + eventId |
| `onUserTranscript` | `(String, Int) -> Void` | Finalized user transcript |
| `onAudioAlignment` | `(AudioAlignment) -> Void` | Per-character timing for word highlighting |
| `onVadScore` | `(Double) -> Void` | Voice activity 0.0–1.0 for audio visualizers |
| `onInterruption` | `(Int) -> Void` | User interrupted the agent |
| `onCanSendFeedbackChange` | `(Bool) -> Void` | Enable/disable thumbs up/down UI |
| `onSpeechActivity` | `(SpeechActivityEvent) -> Void` | LiveKit speech events while muted |
| `onAgentStateChange` | `(ElevenLabs.AgentState) -> Void` | Event-based state (requires `agentStateConfiguration`) |
| `onUnhandledClientToolCall` | `(ClientToolCallEvent) -> Void` | Tool calls with no registered handler |
| `onConversationMetadata` | `(ConversationMetadataEvent) -> Void` | conversationId, audio formats |

---

### 3. @Published Properties on Conversation

```swift
@Published var state: ConversationState          // .idle | .connecting | .active(CallInfo) | .ended(reason:) | .error
@Published var agentState: ElevenLabs.AgentState // .listening | .speaking | .thinking
@Published var isMuted: Bool                     // microphone mute state
@Published var messages: [Message]               // [id, role (.user/.agent), content, timestamp]
@Published var pendingToolCalls: [ClientToolCallEvent]  // client tools awaiting response
@Published var mcpToolCalls: [MCPToolCallEvent]         // MCP tools (approve/reject)
@Published var startupState: ConversationStartupState
@Published var startupMetrics: ConversationStartupMetrics?
@Published var latestAudioEvent: AudioEvent?     // raw audio + alignment
@Published var audioDevices: [AudioDevice]       // available mics
@Published var selectedAudioDeviceID: String
```

The starter kit's `AppViewModel` subscribes to these with Combine `.sink { }.store(in: &cancellables)`.

---

### 4. Agent Speaking State

`ElevenLabs.AgentState` is an enum:
- `.listening` — waiting for user speech
- `.speaking` — TTS audio playing
- `.thinking` — preparing response or tool call

**Two detection modes:**
1. **Default (LiveKit-based):** `room.remoteParticipant.didUpdateIsSpeaking` drives `.speaking`/`.listening`
2. **Event-based (VAD + protocol):** Pass `agentStateConfiguration: AgentStateConfiguration(...)` to `ConversationConfig` — state is computed from VAD scores and protocol events instead

The starter kit checks `conversation.agentState == .listening` for haptic feedback.

---

### 5. Start / End Session

```swift
// Start
let conversation = try await ElevenLabs.startConversation(agentId: agentId, config: config)

// End
await conversation.endConversation()
// fires onDisconnect(.user), sets state = .ended(reason: .userEnded)
```

The `Conversation` object can be reused — call `startConversation(with:)` on the same instance after it ends. Each call creates a fresh LiveKit `Room`.

---

### 6. Toggle Mute

```swift
// Toggle
try await conversation.toggleMute()

// Set explicitly
try await conversation.setMuted(true)   // mute
try await conversation.setMuted(false)  // unmute

// Force hardware mic off (bypasses software mute)
try await conversation.setMicrophoneMuted(true)
```

The `isMuted` `@Published` property reflects the current state reactively.

Software mute (audio zeroed but mic stays open) is enabled via `AudioPipelineConfiguration(useSoftwareMute: true)` — this also enables `onMutedSpeech` callbacks for "you are muted" UX.

---

### 7. Client Tool Calls

```swift
// Observe via Combine
conversation.$pendingToolCalls.sink { toolCalls in
    for toolCall in toolCalls {
        Task { await handleToolCall(toolCall) }
    }
}.store(in: &cancellables)

// Handle and respond
func handleToolCall(_ toolCall: ClientToolCallEvent) async {
    let params = try toolCall.getParameters()  // [String: Any]
    let result = await executeMyTool(params)
    try await conversation.sendToolResult(
        for: toolCall.toolCallId,
        result: result          // Any JSON-serializable
    )
    // On error:
    // try await conversation.sendToolResult(for: id, result: "msg", isError: true)
}
```

For tools that don't expect a response: `conversation.markToolCallCompleted(toolCallId)`.

---

### 8. Audio Pipeline Configuration

```swift
let audioConfig = AudioPipelineConfiguration(
    microphoneMuteMode: .inputMixer,       // or .voiceProcessing, .restart
    recordingAlwaysPrepared: true,         // keeps mic warm, reduces first-word latency
    voiceProcessingBypassed: false,        // bypass AEC/NS
    voiceProcessingAGCEnabled: true,
    useSoftwareMute: nil,
    onMutedSpeech: { event in },           // called when user speaks while muted
    mutedSpeechThreshold: -30.0            // dB
)
```

---

### 9. Token Fetching (for private agents)

The endpoint is:
```
GET https://api.us.elevenlabs.io/v1/convai/conversation/token?agent_id=<id>
Header: xi-api-key: <key>
Response: { "token": "..." }
```

The starter kit's `TokenService` actor (in `VoiceStarterKit/Auth/TokenService.swift`) shows the pattern — **never put the API key in production client code**; use a backend.

---

### 10. Key File Locations

- SDK entry point: `Sources/ElevenLabs/Public/ElevenLabs/ElevenLabs.swift`
- `Conversation` class: `Sources/ElevenLabs/Public/Conversation/Conversation.swift`
- All callbacks struct: `Sources/ElevenLabs/Public/Conversation/ConversationConfig.swift` (also `ConversationOptions.swift` — they are parallel and convert via `toConversationOptions()`)
- Agent state enum: `Sources/ElevenLabs/Public/ElevenLabs/ElevenLabs+AgentState.swift`
- All incoming event types: `Sources/ElevenLabs/Public/ElevenLabs/Events/IncomingEvents.swift`
- Auth config: `Sources/ElevenLabs/Public/ElevenLabs/ElevenLabsConfiguration.swift`
- Starter kit ViewModel: `VoiceStarterKit/App/AppViewModel.swift` — this is the canonical usage example
- Full documentation: `Documentation/Usage.md`

---

