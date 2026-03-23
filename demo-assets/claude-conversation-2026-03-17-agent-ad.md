# Claude Conversation Log

Session ID: agent-ad38e3b1f2cc29196
Date: 2026-03-17 20:24:37

---

## 👤 User

Search for the ElevenLabs Swift SDK source files on this Mac. The package is named "elevenlabs-swift-sdk" and was declared as a dependency in /Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/Package.swift.

1. First check: ls ~/.spm/ or ~/Library/Developer/Xcode/ for cached package sources
2. Check: find /Users/sarathfrancis -path "*elevenlabs-swift-sdk*" -name "*.swift" 2>/dev/null | head -20
3. Check /Users/sarathfrancis/Library/Developer/Xcode/DerivedData/ for any cached sources
4. Check ~/Library/Caches/org.swift.swiftpm/ for package cache

If found, read the files:
- ConversationConfig.swift
- ElevenLabs.swift (main entry point)
- ElevenLabsConfiguration.swift
- Conversation.swift (the class returned by startConversation)

I need to know:
- The exact initializer of ConversationConfig - is it via `init()` with mutable properties, or via memberwise init with all params?
- The exact type names and signatures for `startConversation`
- What `ElevenLabsConfiguration` cases exist

Return the complete content of these key files.

---

## 🤖 Claude

I'll help you locate the ElevenLabs Swift SDK source files on this Mac. Let me search through the common Swift Package Manager cache locations systematically.

---

## 🤖 Claude

Let me search for the package in the Xcode and SPM caches:

---

## 🤖 Claude

Perfect! The SDK is cached in DerivedData. Let me find the key Swift files:

---

## 🤖 Claude

Excellent! I found all the key files. Let me read them now:

---

## 🤖 Claude

Perfect! I found all four key files and have complete information. Here's a comprehensive summary of the ElevenLabs Swift SDK:

## Summary of ElevenLabs Swift SDK Key Files

All files are located at:
```
/Users/sarathfrancis/Library/Developer/Xcode/DerivedData/ios-gjmvwrshtqojhpcxearobwvuuvzu/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Public/
```

### Key Findings

**1. ConversationConfig Initializer (ConversationConfig.swift)**

Uses a **full memberwise initializer with all parameters optional**:
```swift
public init(
    agentOverrides: AgentOverrides? = nil,
    ttsOverrides: TTSOverrides? = nil,
    conversationOverrides: ConversationOverrides? = nil,
    customLlmExtraBody: [String: String]? = nil,
    dynamicVariables: [String: String]? = nil,
    userId: String? = nil,
    onAgentReady: (@Sendable () -> Void)? = nil,
    onDisconnect: (@Sendable (DisconnectionReason) -> Void)? = nil,
    onStartupStateChange: (@Sendable (ConversationStartupState) -> Void)? = nil,
    startupConfiguration: ConversationStartupConfiguration = .default,
    audioConfiguration: AudioPipelineConfiguration? = nil,
    networkConfiguration: LiveKitNetworkConfiguration = .default,
    onError: (@Sendable (ConversationError) -> Void)? = nil,
    onSpeechActivity: (@Sendable (SpeechActivityEvent) -> Void)? = nil,
    onAgentResponse: (@Sendable (_ text: String, _ eventId: Int) -> Void)? = nil,
    onAgentResponseCorrection: (@Sendable (_ original: String, _ corrected: String, _ eventId: Int) -> Void)? = nil,
    onAgentResponseMetadata: (@Sendable (_ metadataData: Data, _ eventId: Int) -> Void)? = nil,
    onUserTranscript: (@Sendable (_ text: String, _ eventId: Int) -> Void)? = nil,
    onConversationMetadata: (@Sendable (ConversationMetadataEvent) -> Void)? = nil,
    onAgentToolResponse: (@Sendable (AgentToolResponseEvent) -> Void)? = nil,
    onAgentToolRequest: (@Sendable (AgentToolRequestEvent) -> Void)? = nil,
    onInterruption: (@Sendable (_ eventId: Int) -> Void)? = nil,
    onVadScore: (@Sendable (_ score: Double) -> Void)? = nil,
    onAudioAlignment: (@Sendable (AudioAlignment) -> Void)? = nil,
    onCanSendFeedbackChange: (@Sendable (Bool) -> Void)? = nil,
    onUnhandledClientToolCall: (@Sendable (ClientToolCallEvent) -> Void)? = nil,
    agentStateConfiguration: AgentStateConfiguration? = nil,
    onAgentStateChange: (@Sendable (ElevenLabs.AgentState) -> Void)? = nil
)
```

**Key property structure**: All properties are mutable (`var`), not constants (`let`). Can be instantiated with `.init()` for a default config.

**2. startConversation Signatures (ElevenLabs.swift)**

There are **four overloaded methods** in the `ElevenLabs` enum:

```swift
// Method 1: Public agent ID (most common)
@MainActor
public static func startConversation(
    agentId: String,
    config: ConversationConfig = .init(),
    onAgentReady: (@Sendable () -> Void)? = nil,
    onDisconnect: (@Sendable (DisconnectionReason) -> Void)? = nil
) async throws -> Conversation

// Method 2: Conversation token (private agents)
@MainActor
public static func startConversation(
    conversationToken: String,
    config: ConversationConfig = .init(),
    onAgentReady: (@Sendable () -> Void)? = nil,
    onDisconnect: (@Sendable (DisconnectionReason) -> Void)? = nil
) async throws -> Conversation

// Method 3: Custom token provider (advanced)
@MainActor
public static func startConversation(
    tokenProvider: @escaping @Sendable () async throws -> String,
    config: ConversationConfig = .init(),
    onAgentReady: (@Sendable () -> Void)? = nil,
    onDisconnect: (@Sendable (DisconnectionReason) -> Void)? = nil
) async throws -> Conversation

// Method 4: Full auth control (advanced)
@MainActor
public static func startConversation(
    auth: ElevenLabsConfiguration,
    config: ConversationConfig = .init()
) async throws -> Conversation
```

**All return `Conversation` (marked `@MainActor`)**

**3. ElevenLabsConfiguration Cases (ElevenLabsConfiguration.swift)**

`ElevenLabsConfiguration` is a **struct with static factory methods**. The underlying `AuthSource` enum has three cases:

```swift
public enum AuthSource: Sendable {
    case publicAgentId(String)              // Public agent ID
    case conversationToken(String)          // Backend conversation token
    case customTokenProvider(              // Advanced: dynamic token generation
        @Sendable () async throws -> String
    )
}
```

**Factory methods**:
```swift
public static func publicAgent(
    id: String, 
    participantName: String = "user"
) -> Self

public static func conversationToken(
    _ token: String, 
    participantName: String = "user"
) -> Self

public static func customTokenProvider(
    _ provider: @escaping @Sendable () async throws -> String,
    participantName: String = "user"
) -> Self
```

**4. Conversation Class (Conversation.swift)**

Returns a `Conversation` class with key public API methods:
- `startConversation(with agentId:, options:)` async throws
- `startConversation(auth:, options:)` async throws
- `endConversation()` async
- `sendMessage(_ text: String)` async throws
- `setMuted(_ muted: Bool)` async throws
- `toggleMute()` async throws
- `interruptAgent()` async throws
- `sendFeedback(_ score:, eventId:)` async throws
- `sendToolResult(for:, result:, isError:)` async throws
- `sendMCPToolApproval(toolCallId:, isApproved:)` async throws

**Published properties for UI binding** (via `@Published`):
- `state: ConversationState`
- `messages: [Message]`
- `agentState: ElevenLabs.AgentState`
- `isMuted: Bool`
- `pendingToolCalls: [ClientToolCallEvent]`
- `mcpToolCalls: [MCPToolCallEvent]`

Complete file contents have been read and are available above.

---

