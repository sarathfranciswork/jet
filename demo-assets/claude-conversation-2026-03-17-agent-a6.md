# Claude Conversation Log

Session ID: agent-a6428b4f4db8bbca9
Date: 2026-03-17 12:39:15

---

## 👤 User

I need to find working examples of the ElevenLabs Swift SDK v3 being used in a text-only chat mode. Search for:

1. WebFetch https://raw.githubusercontent.com/elevenlabs/elevenlabs-swift-sdk/main/README.md — read the full README for usage examples
2. WebFetch https://raw.githubusercontent.com/elevenlabs/elevenlabs-swift-sdk/main/Example/ElevenLabsSDKExample/ElevenLabsSDKExample/ContentView.swift — look for the example app
3. Search GitHub for repos using "ElevenLabs" "startConversation" "textOnly" in Swift
4. WebFetch https://elevenlabs.io/docs/conversational-ai/guides/conversational-ai-sdk/swift — official Swift SDK docs
5. WebFetch https://elevenlabs.io/docs/conversational-ai/customization/chat-mode — chat mode docs

I need to know:
- The EXACT correct way to start a text-only conversation and receive responses
- Whether you need to observe $messages or use callbacks for text responses
- A complete working code example of text-only chat with the Swift SDK v3
- Whether `sendMessage()` responses come through `onAgentResponse` or only through `$messages`

Report exact code examples that work.

---

## 🤖 Claude



I'll fetch all the requested resources in parallel to gather the information you need.

---

## 🤖 Claude



Now let me fetch all the requested URLs in parallel.

---

## 🤖 Claude

The ElevenLabs docs pages returned 404s. Let me try alternative URLs and search GitHub for more examples.

---

## 🤖 Claude

Let me dig deeper into the actual SDK source code to find the `sendMessage` method and text-only mode support.

---

## 🤖 Claude

Found `sendMessage`. Now let me get the actual source files to understand the exact API.

---

## 🤖 Claude

Now let me fetch the key source files in parallel.

---

## 🤖 Claude

Excellent. Now I have the critical pieces. Let me get the remaining details - the Message model, the Usage.md text-only examples, and the tests.

---

## 🤖 Claude

Now let me get the complete Usage.md which should have the text-only examples, and also search for any example app in the repo.

---

## 🤖 Claude

Now let me also get the `ConversationState.swift` and check for any additional details about callbacks vs `$messages` for text-only mode.

---

## 🤖 Claude

Let me get one more critical file - the internal data handler that shows how messages get populated, plus the full ElevenLabs.swift file for the doc comments showing text-only examples.

---

## 🤖 Claude

Now I have all the information needed. Let me also check the `AgentChatResponsePartEvent` which is specifically relevant for text-only streaming responses.

---

## 🤖 Claude

Now I have comprehensive information. Let me also look at the existing iOS codebase to see what's already been implemented.

---

## 🤖 Claude

I have the actual SDK source checked out locally. Let me read the key files directly for complete accuracy.

---

## 🤖 Claude

Now let me also read the `ElevenLabs.swift` static entry point to confirm the factory method signatures and the `EventSerializer.swift` to see how `textOnly` is serialized.

---

## 🤖 Claude

I now have a complete picture from the actual SDK source code checked out in your project. Here is the full report.

---

## ElevenLabs Swift SDK v3 -- Text-Only Chat Mode: Complete Reference

**SDK Version:** 3.1.0 (from your local checkout at `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/`)

---

### 1. How to Start a Text-Only Conversation

Set `conversationOverrides: .init(textOnly: true)` in the `ConversationConfig`:

```swift
let conversation = try await ElevenLabs.startConversation(
    agentId: "your-agent-id",
    config: ConversationConfig(
        conversationOverrides: .init(textOnly: true)
    )
)
```

This causes `"text_only": true` to be sent in the `conversation_config_override.conversation` payload during the WebSocket/LiveKit `conversation_initiation_client_data` handshake (see `EventSerializer.swift` line 97-98). It also skips the microphone permission request during startup (confirmed in `ConversationStartupOrchestrator.swift`).

---

### 2. How to Send a Message

```swift
try await conversation.sendMessage("Hello, what vaccines do you have?")
```

The `sendMessage` method (Conversation.swift lines 334-341):
1. Checks `state.isActive` -- throws `ConversationError.notConnected` if not connected
2. Serializes as `{"type": "user_message", "text": "..."}` and publishes via LiveKit data channel
3. Calls `appendLocalMessage(text)` which immediately appends a `Message(role: .user, ...)` to the `messages` array

---

### 3. How Agent Responses Are Delivered -- BOTH Mechanisms

Agent responses come through **two parallel paths**. You can use either or both:

#### Path A: The `$messages` Published Property (Reactive/SwiftUI)

`conversation.messages` is a `@Published` `[Message]` array. In text-only mode, the agent sends responses via `agentChatResponsePart` events which stream in three phases:

- **`.start`** -- Creates a new `Message(role: .agent)` and appends it to `messages`
- **`.delta`** -- Removes the existing message by ID, concatenates new text, re-appends the updated message
- **`.stop`** -- Finalizes with any remaining text, clears `currentStreamingMessage`

This means you can observe the messages array reactively:

```swift
// SwiftUI binding
ForEach(conversation.messages) { msg in
    Text("\(msg.role == .user ? "You" : "Agent"): \(msg.content)")
}

// Or Combine
conversation.$messages
    .receive(on: DispatchQueue.main)
    .sink { messages in
        guard let last = messages.last, last.role == .agent else { return }
        print("Agent:", last.content)
    }
    .store(in: &cancellables)
```

#### Path B: The `onAgentResponse` Callback (Non-Streaming, Complete)

For non-streaming `agentResponse` events (the standard voice-mode response type), the callback fires:

```swift
let config = ConversationConfig(
    conversationOverrides: .init(textOnly: true),
    onAgentResponse: { text, eventId in
        print("Agent said: \(text), eventId: \(eventId)")
    }
)
```

**Important distinction:** In text-only mode, the agent primarily sends `agentChatResponsePart` streaming events (start/delta/stop). These do NOT trigger `onAgentResponse`. They only update `messages`. The `onAgentResponse` callback fires for `agentResponse` events (the non-streaming, finalized response type used in voice mode).

So for text-only mode, **`$messages` is the primary mechanism**. The `onAgentResponse` callback may or may not fire depending on whether the server also emits the non-streaming `agentResponse` event.

---

### 4. The `Message` Model

```swift
public struct Message: Identifiable, Sendable {
    public let id: String
    public let role: Role
    public let content: String
    public let timestamp: Date

    public enum Role: Sendable {
        case user
        case agent
    }
}
```

---

### 5. Complete Working Example -- Text-Only Chat

```swift
import SwiftUI
import ElevenLabs
import Combine

@MainActor
class TextChatViewModel: ObservableObject {
    @Published var conversation: Conversation?
    @Published var messages: [Message] = []
    @Published var isConnected = false
    @Published var isConnecting = false
    
    private var cancellables = Set<AnyCancellable>()
    
    func connect(agentId: String) async {
        isConnecting = true
        do {
            let conv = try await ElevenLabs.startConversation(
                agentId: agentId,
                config: ConversationConfig(
                    conversationOverrides: .init(textOnly: true),
                    onAgentReady: { [weak self] in
                        Task { @MainActor in
                            self?.isConnected = true
                            self?.isConnecting = false
                        }
                    },
                    onDisconnect: { [weak self] reason in
                        Task { @MainActor in
                            self?.isConnected = false
                            print("Disconnected: \(reason)")
                        }
                    },
                    onError: { error in
                        print("Error: \(error)")
                    },
                    // This fires for non-streaming agentResponse events
                    onAgentResponse: { text, eventId in
                        print("Agent response (non-streaming): \(text)")
                    }
                )
            )
            
            self.conversation = conv
            
            // Observe the messages array for streaming chat responses
            conv.$messages
                .receive(on: DispatchQueue.main)
                .assign(to: &$messages)
            
        } catch {
            isConnecting = false
            print("Failed to connect: \(error)")
        }
    }
    
    func send(_ text: String) async {
        guard let conversation else { return }
        do {
            try await conversation.sendMessage(text)
        } catch {
            print("Failed to send: \(error)")
        }
    }
    
    func disconnect() async {
        await conversation?.endConversation()
        conversation = nil
        isConnected = false
    }
}

struct TextChatView: View {
    @StateObject private var viewModel = TextChatViewModel()
    @State private var inputText = ""
    let agentId: String
    
    var body: some View {
        VStack {
            ScrollView {
                LazyVStack(alignment: .leading, spacing: 8) {
                    ForEach(viewModel.messages) { message in
                        HStack {
                            if message.role == .user { Spacer() }
                            Text(message.content)
                                .padding(10)
                                .background(message.role == .user ? Color.blue : Color.gray.opacity(0.2))
                                .foregroundColor(message.role == .user ? .white : .primary)
                                .cornerRadius(12)
                            if message.role == .agent { Spacer() }
                        }
                    }
                }
                .padding()
            }
            
            HStack {
                TextField("Message...", text: $inputText)
                    .textFieldStyle(.roundedBorder)
                    .disabled(!viewModel.isConnected)
                
                Button("Send") {
                    let text = inputText
                    inputText = ""
                    Task { await viewModel.send(text) }
                }
                .disabled(inputText.isEmpty || !viewModel.isConnected)
            }
            .padding()
        }
        .task {
            await viewModel.connect(agentId: agentId)
        }
    }
}
```

---

### 6. Key Findings Summary

| Question | Answer |
|----------|--------|
| How to enable text-only? | `ConversationConfig(conversationOverrides: .init(textOnly: true))` |
| How to send messages? | `try await conversation.sendMessage("text")` -- requires `state.isActive` |
| Where do responses appear? | Primarily in `conversation.messages` (`@Published [Message]`) via streaming `agentChatResponsePart` events |
| Does `onAgentResponse` fire in text-only? | It fires for `agentResponse` events (non-streaming). In text-only mode the server primarily sends `agentChatResponsePart` streaming events which only update `messages`, not the callback. |
| `$messages` or callbacks? | Use `$messages` for text-only mode -- it handles both streaming (start/delta/stop) and non-streaming responses. Use `onAgentResponse` as a supplementary signal. |
| Does `sendMessage` return the response? | No. It is fire-and-forget. The response arrives asynchronously via the `messages` array or callbacks. |
| Does text-only skip mic permission? | Yes -- the startup orchestrator checks `textOnly` and skips `requestMicrophonePermissionIfNeeded`. |

### Key Source Files

- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Public/ElevenLabs/ElevenLabs.swift` -- Factory methods with doc comments showing `textOnly: true`
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Public/Conversation/Conversation.swift` -- `sendMessage()` at line 334, `messages` at line 25, `appendLocalMessage` at line 658
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Internal/Conversation/Conversation+Events.swift` -- `handleAgentChatResponsePart` streaming logic at line 114, `handleIncomingEvent` showing both `agentResponse` (callback) and `agentChatResponsePart` (messages) paths
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Public/Conversation/ConversationConfig.swift` -- `ConversationOverrides.textOnly` at line 187
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/ios/build/SourcePackages/checkouts/elevenlabs-swift-sdk/Sources/ElevenLabs/Internal/Utilities/EventSerializer.swift` -- serializes `textOnly` as `"text_only": true` at line 97-98

---

