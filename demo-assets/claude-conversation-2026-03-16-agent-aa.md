# Claude Conversation Log

Session ID: agent-aab0d0875f2d26a19
Date: 2026-03-16 17:16:17

---

## 👤 User

Design a detailed Dynamic UI system for an iOS chat interface where AI responses can include rich interactive controls embedded within the conversation flow. This is for a CVS vaccine scheduling app.

## Context
The app uses ElevenLabs Agents Platform as the unified AI brain. When the user is in Chat mode, the AI should be able to render rich interactive widgets WITHIN chat bubbles instead of plain text. The user can interact with these widgets (tap dates, fill forms, select options) and the results feed back into the conversation.

## Dynamic UI Components Needed

For CVS vaccine scheduling, these interactive elements should appear inline in chat:

1. **Vaccine Selection Card** — Grid/list of eligible vaccines with icons, names, descriptions. User taps to select.
2. **Store Finder Card** — List of nearby CVS stores with address, distance, available dates. Possibly a mini map view. User taps to select a store.
3. **Date Picker** — Calendar-style date picker showing available dates (highlighted). User taps a date.
4. **Time Slot Selector** — Grid of available time slots grouped by morning/afternoon/evening. User taps a time.
5. **Patient Details Form** — Inline form with fields for name, email, phone, address, gender. Has a submit button.
6. **Questionnaire Card** — Sequential health screening questions with Yes/No toggle buttons.
7. **Confirmation Summary Card** — Shows appointment details (vaccine, store, date, time, patient) with a "Confirm Booking" button.
8. **Appointment Card** — Shows existing appointments with cancel button.
9. **Login Card** — Email/password input for CVS login within chat.
10. **OTP Verification Card** — 6-digit code input with auto-advance.

## Design Questions to Address

1. **Protocol**: How does the AI signal "render a date picker" vs "render plain text"? What's the message format? Consider using structured JSON within the AI response that the iOS app parses.
2. **Interaction Flow**: When a user interacts with a widget (e.g., selects a date), how does that feed back to the AI conversation? Does it become a user message?
3. **State Management**: How to handle partially filled forms, validation, and widget state?
4. **SwiftUI Architecture**: How to implement a dynamic chat bubble renderer that can display any of these widget types?
5. **Fallback**: What happens if the AI sends a dynamic UI component that the app doesn't recognize? Graceful degradation to text.
6. **Accessibility**: How to make these dynamic widgets accessible with VoiceOver?
7. **Message Format**: Define the exact JSON schema for dynamic UI messages.
8. **Tool Integration**: How does widget interaction trigger MCP tool calls?

## Technical Constraints
- iOS native app using SwiftUI
- Must work within a chat bubble paradigm (scrollable conversation)
- Must be accessible (VoiceOver, Dynamic Type)
- Must handle both AI-initiated widgets and user responses
- Should feel native iOS, not web-view based

Provide a detailed technical design with JSON schemas, SwiftUI component architecture, and interaction flow diagrams.

---

## 🤖 Claude



I'll start by thoroughly exploring the existing codebase to understand the current architecture, patterns, and conventions before designing the Dynamic UI system.

---

## 🤖 Claude

The project is a React/TypeScript web frontend, not an iOS/SwiftUI app. Let me explore the existing codebase more deeply to understand the current architecture, ElevenLabs integration, and chat patterns.

---

## 🤖 Claude

Now let me read all the key source files to understand the existing architecture deeply.

---

## 🤖 Claude

Now let me read the remaining component files.

---

## 🤖 Claude

Let me also read the remaining component files for completeness.

---

## 🤖 Claude

Now let me check if there's a backend folder to understand the server-side architecture.

---

## 🤖 Claude

Let me read the backend chat agent and WebSocket handler to understand how tools are called and responses streamed.

---

## 🤖 Claude

Now let me check the docs directory for any existing A2UI protocol documentation referenced in the CLAUDE.md.

---

## 🤖 Claude

This is very helpful - the project already references the A2UI protocol. Let me read more of the spec.

---

## 🤖 Claude

Let me continue reading the A2UI specification, particularly the component types and action model.

---

## 🤖 Claude

Now let me read the component reference and messages reference sections of the A2UI docs.

---

## 🤖 Claude

I now have a thorough understanding of the entire codebase and the A2UI protocol documentation. Let me read the remaining A2UI message reference to understand the action model fully.

---

## 🤖 Claude

Now I have a comprehensive understanding of the entire codebase and the A2UI protocol. Let me also check the ThemeContext quickly.

---

## 🤖 Claude

I now have a thorough understanding of the entire codebase. Let me provide the comprehensive technical design.

---

# Dynamic UI System for CVS Vaccine Scheduling -- iOS Chat Interface

## Technical Design Document

---

## 1. Foundational Context

The user asks for an iOS SwiftUI design, but the actual application is a **React + TypeScript + Vite web frontend** that communicates with a Python FastAPI backend via WebSocket. The backend uses OpenAI Chat Completions (GPT-5.2) with MCP tool calls for CVS API integration. The project already includes A2UI protocol documentation (Google's Agent-to-UI protocol, v0.8) in `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/docs/A2UI_docs.md`.

Rather than designing for SwiftUI (which this project is not), I will design this Dynamic UI system for the **existing React/TypeScript frontend**, drawing heavily from A2UI principles while adapting them to work within the existing WebSocket streaming architecture. The design will be structured so that a future SwiftUI client could consume the same protocol with its own renderer.

---

## 2. Protocol Design: How the AI Signals "Render a Widget"

### 2.1 The Approach: Structured JSON Blocks in AI Response Stream

The current system streams AI responses as text chunks via WebSocket events (`chunk`, `tool_start`, `tool_result`, `done`). The dynamic UI system introduces a new event type: `ui_surface`.

The AI model will be prompted (via system prompt in `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/config.py`) to emit structured JSON blocks delimited by a marker when it wants to render a rich UI widget. The backend `chat_agent.py` will parse these blocks from the streaming text and emit them as separate WebSocket events.

### 2.2 New WebSocket Event Types

Add to the `WSEvent` union type in `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/types/index.ts`:

```typescript
// New event types for Dynamic UI
| { type: 'ui_surface'; surfaceId: string; surface: DynamicSurface }
| { type: 'ui_data'; surfaceId: string; path?: string; data: Record<string, unknown> }
| { type: 'ui_delete'; surfaceId: string }
```

And a new client message type:

```typescript
| { type: 'ui_action'; surfaceId: string; action: string; data: Record<string, unknown> }
```

### 2.3 The DynamicSurface Schema

Inspired by A2UI but simplified for our use case. Instead of the full adjacency list model, we use a typed component model with an explicit component catalog tailored to CVS scheduling:

```typescript
// --- Component Type Catalog ---

type ComponentType =
  | 'vaccine_selection'
  | 'store_finder'
  | 'date_picker'
  | 'time_slot_selector'
  | 'patient_form'
  | 'questionnaire'
  | 'confirmation_summary'
  | 'appointment_card'
  | 'login_card'
  | 'otp_verification';

interface DynamicSurface {
  surfaceId: string;
  componentType: ComponentType;
  data: Record<string, unknown>;    // Component-specific payload
  actions: SurfaceAction[];          // Available user actions
  state: 'interactive' | 'submitted' | 'loading' | 'error' | 'dismissed';
}

interface SurfaceAction {
  name: string;                      // e.g., "select_vaccine", "submit_form"
  label: string;                     // Display label
  style: 'primary' | 'secondary' | 'destructive';
  requiresConfirmation?: boolean;
}
```

### 2.4 Component-Specific Data Schemas

Each `componentType` has a well-defined data payload. Here are all ten:

```typescript
// 1. Vaccine Selection
interface VaccineSelectionData {
  vaccines: Array<{
    code: string;
    name: string;
    description: string;
    icon: string;           // SF Symbol name or emoji
    selected: boolean;
  }>;
  multiSelect: boolean;
}

// 2. Store Finder
interface StoreFinderData {
  stores: Array<{
    storeId: string;
    clinicId: string;
    name: string;
    address: string;
    distance: string;       // e.g., "2.3 miles"
    availableDates: string[];
    phone?: string;
    selected: boolean;
  }>;
  userLocation?: { lat: number; lng: number };
}

// 3. Date Picker
interface DatePickerData {
  availableDates: string[];      // ISO date strings YYYY-MM-DD
  selectedDate: string | null;
  month: string;                 // e.g., "March 2026"
  minDate: string;
  maxDate: string;
}

// 4. Time Slot Selector
interface TimeSlotData {
  slots: Array<{
    time: string;            // "HH:MM"
    displayTime: string;     // "9:00 AM"
    period: 'morning' | 'afternoon' | 'evening';
    available: boolean;
  }>;
  selectedTime: string | null;
  date: string;
  storeName: string;
}

// 5. Patient Form
interface PatientFormData {
  fields: Array<{
    name: string;
    label: string;
    type: 'text' | 'email' | 'phone' | 'select';
    value: string;
    required: boolean;
    options?: Array<{ label: string; value: string }>;
    error?: string;
  }>;
  prefilled: boolean;        // true if data came from profile
}

// 6. Questionnaire
interface QuestionnaireData {
  questions: Array<{
    id: string;
    text: string;
    type: 'yes_no' | 'text' | 'select';
    answer: string | boolean | null;
    options?: string[];
  }>;
  currentIndex: number;
  totalCount: number;
}

// 7. Confirmation Summary
interface ConfirmationSummaryData {
  vaccine: string;
  store: { name: string; address: string };
  date: string;
  time: string;
  patient: { name: string; email: string; phone: string };
  confirmationNumber?: string;  // present after booking
}

// 8. Appointment Card
interface AppointmentCardData {
  appointments: Array<{
    appointmentId: string;
    vaccine: string;
    store: { name: string; address: string };
    date: string;
    time: string;
    status: 'confirmed' | 'pending' | 'cancelled';
  }>;
}

// 9. Login Card
interface LoginCardData {
  method: 'otp' | 'password';
  email: string;
  error?: string;
  loading: boolean;
}

// 10. OTP Verification
interface OTPVerificationData {
  email: string;
  digits: number;        // typically 6
  error?: string;
  loading: boolean;
}
```

---

## 3. Backend Integration: AI-to-UI Pipeline

### 3.1 System Prompt Additions

Add to the `SYSTEM_PROMPT` in `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/config.py`:

```
== DYNAMIC UI GUIDELINES ==
When presenting options to the user (vaccines, stores, time slots, forms, etc.), 
you SHOULD emit a structured UI block instead of listing items as text.

To emit a UI widget, include a JSON block in your response delimited by:
---CVS_UI_START---
{ ... JSON ... }
---CVS_UI_END---

The JSON must follow the DynamicSurface schema. You can include text before and 
after the block. The frontend will render the block as an interactive widget 
within your chat bubble.

When a user interacts with a widget (selects a vaccine, picks a date, submits a 
form), their selection will be sent back to you as a tool result with the 
surface action details. Continue the conversation based on their selection.

IMPORTANT: Only emit ONE UI block per response. Include brief conversational 
text around it.
```

### 3.2 Backend Parsing (chat_agent.py)

Modify the streaming logic in `stream_response()` at `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/chat_agent.py`. After the `done` event accumulates `full_content`, scan it for `---CVS_UI_START---` / `---CVS_UI_END---` delimiters. If found:

1. Extract the JSON block.
2. Parse and validate it.
3. Emit a `ui_surface` WebSocket event with the parsed surface.
4. Store the surface metadata alongside the message in the database.
5. Strip the raw JSON from the text content so the frontend only sees clean prose.

The WebSocket handler at `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/chat_ws.py` needs a new handler for `ui_action` client messages. When the frontend sends a `ui_action`, the backend:

1. Formats the action as a synthetic user message (e.g., "I selected the Flu vaccine (code: FLU) from the vaccine list").
2. Feeds it back into `stream_response()` as if the user typed it.
3. This triggers the normal tool-call loop -- the AI sees the selection and proceeds to the next step.

### 3.3 Alternative: Tool-Driven UI Emission

A cleaner alternative is to have the backend emit `ui_surface` events **directly from tool results**, not from the AI text. When `_summarize_tool_result()` in `chat_agent.py` processes a `search_stores` result, for example, it also builds a `StoreFinderData` surface and emits it via WebSocket before the AI's text response arrives. This keeps the protocol simpler because:

- The AI does not need to generate JSON (error-prone with LLMs).
- The backend transforms structured MCP tool results directly into UI surfaces.
- The AI response text can naturally reference the widget ("I found 5 stores near you -- please select one from the list above").

**This is the recommended approach.** The mapping would be:

| MCP Tool Result | UI Surface Type |
|---|---|
| `get_eligible_vaccines` | `vaccine_selection` |
| `search_stores` | `store_finder` |
| `get_available_time_slots` | `time_slot_selector` |
| `get_questionnaire` | `questionnaire` |
| `get_my_appointments` | `appointment_card` |

The `patient_form`, `confirmation_summary`, `date_picker`, `login_card`, and `otp_verification` surfaces would be emitted by the backend at appropriate points in the scheduling flow based on conversation state.

---

## 4. Frontend Architecture: React Component System

### 4.1 New Type Definitions

Add to `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/types/index.ts`:

```typescript
// Full DynamicSurface type and all component data interfaces (as defined above)
// Plus the new WSEvent variants
```

### 4.2 New Context: DynamicUIContext

Create `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/contexts/DynamicUIContext.tsx`:

```typescript
interface DynamicUIContextValue {
  surfaces: Map<string, DynamicSurface>;     // Active surfaces keyed by surfaceId
  surfaceOrder: string[];                     // Ordered list of surfaceIds as they appeared
  updateSurfaceData: (surfaceId: string, data: Record<string, unknown>) => void;
  submitAction: (surfaceId: string, action: string, data: Record<string, unknown>) => void;
  dismissSurface: (surfaceId: string) => void;
}
```

This context manages the lifecycle of all dynamic surfaces. It receives `ui_surface`, `ui_data`, and `ui_delete` events from the WebSocket (forwarded by ChatContext). When a user interacts with a widget, it calls `submitAction` which sends a `ui_action` message over the WebSocket.

### 4.3 Modifying ChatContext

In `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/contexts/ChatContext.tsx`, the `handleWSEvent` function needs new cases:

```typescript
case 'ui_surface':
  dynamicUI.addSurface(event.surfaceId, event.surface);
  break;
case 'ui_data':
  dynamicUI.updateSurfaceData(event.surfaceId, event.data);
  break;
case 'ui_delete':
  dynamicUI.removeSurface(event.surfaceId);
  break;
```

### 4.4 Message Model Changes

The `Message` interface needs an optional `surfaces` field:

```typescript
interface Message {
  // ... existing fields ...
  surfaces?: DynamicSurface[];  // UI surfaces attached to this message
}
```

When a `done` event arrives, any active surfaces that were emitted during that response cycle are attached to the assistant message. This allows them to persist and re-render when scrolling through chat history.

### 4.5 Dynamic Surface Renderer Component

Create `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/components/DynamicUI/DynamicSurfaceRenderer.tsx`:

```typescript
interface DynamicSurfaceRendererProps {
  surface: DynamicSurface;
  onAction: (action: string, data: Record<string, unknown>) => void;
}

function DynamicSurfaceRenderer({ surface, onAction }: DynamicSurfaceRendererProps) {
  switch (surface.componentType) {
    case 'vaccine_selection':
      return <VaccineSelectionCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'store_finder':
      return <StoreFinderCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'date_picker':
      return <DatePickerCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'time_slot_selector':
      return <TimeSlotCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'patient_form':
      return <PatientFormCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'questionnaire':
      return <QuestionnaireCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'confirmation_summary':
      return <ConfirmationCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'appointment_card':
      return <AppointmentCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'login_card':
      return <LoginCard data={surface.data} onAction={onAction} state={surface.state} />;
    case 'otp_verification':
      return <OTPVerificationCard data={surface.data} onAction={onAction} state={surface.state} />;
    default:
      return <FallbackCard surface={surface} />;
  }
}
```

The `default` case handles graceful degradation -- if the backend sends an unrecognized component type, `FallbackCard` renders the surface data as formatted text.

### 4.6 Integrating into MessageBubble

Modify `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/components/Chat/MessageBubble.tsx`:

Currently, assistant messages render markdown via `dangerouslySetInnerHTML`. The modified version checks if the message has attached surfaces:

```typescript
export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} px-4 py-1.5`}>
      <div className={`max-w-[80%] md:max-w-[70%] ...`}>
        {/* Text content */}
        {message.content && (
          isUser ? (
            <p className="whitespace-pre-wrap">{message.content}</p>
          ) : (
            <div className="markdown-content" dangerouslySetInnerHTML={{ __html: renderMarkdown(message.content) }} />
          )
        )}
        
        {/* Dynamic UI surfaces */}
        {message.surfaces?.map(surface => (
          <DynamicSurfaceRenderer
            key={surface.surfaceId}
            surface={surface}
            onAction={(action, data) => handleSurfaceAction(surface.surfaceId, action, data)}
          />
        ))}
      </div>
    </div>
  );
}
```

For surfaces that are wider than a typical chat bubble (like the date picker or store finder), the bubble width constraint is relaxed to `max-w-[95%]` when a surface is present.

### 4.7 New Directory Structure

```
frontend/src/components/DynamicUI/
  DynamicSurfaceRenderer.tsx      -- Router component
  FallbackCard.tsx                -- Graceful degradation
  VaccineSelectionCard.tsx        -- Vaccine grid
  StoreFinderCard.tsx             -- Store list with distance
  DatePickerCard.tsx              -- Calendar grid
  TimeSlotCard.tsx                -- Grouped time slots
  PatientFormCard.tsx             -- Inline form
  QuestionnaireCard.tsx           -- Q&A with toggles
  ConfirmationCard.tsx            -- Summary + confirm button
  AppointmentCard.tsx             -- Existing appointments
  LoginCard.tsx                   -- Email/password
  OTPVerificationCard.tsx         -- 6-digit code input
  shared/
    CardWrapper.tsx               -- Common card chrome (border, padding, CVS styling)
    ActionButton.tsx              -- Styled action buttons
    LoadingOverlay.tsx            -- Loading state overlay
```

---

## 5. Interaction Flow: User Actions Feeding Back to AI

### 5.1 Action Lifecycle

1. User taps a vaccine in the `VaccineSelectionCard`.
2. The component calls `onAction('select_vaccine', { code: 'FLU', name: 'Influenza (Flu)' })`.
3. `DynamicUIContext.submitAction()` does two things:
   a. Updates the surface state to `'submitted'` (disabling further interaction).
   b. Sends a WebSocket message: `{ type: 'ui_action', surfaceId: 'vaccines-1', action: 'select_vaccine', data: { code: 'FLU', name: 'Influenza (Flu)' } }`.
4. The backend receives this, formats it as a natural language message for the AI: "User selected: Influenza (Flu) [code: FLU]".
5. The AI continues the flow, calling `check_vaccine_eligibility`, then `search_stores`, which triggers the next `ui_surface` event.

### 5.2 User Message vs. UI Action

UI actions are distinct from typed user messages. They do NOT appear as chat bubbles. Instead:
- The surface transitions to `submitted` state (shows a checkmark or collapsed state).
- A brief confirmation appears inline: "Selected: Influenza (Flu)".
- The AI response that follows appears as a normal assistant bubble (potentially with the next surface).

However, the user CAN also just type a response instead of using the widget. If the user types "I want the flu vaccine" while the vaccine selection card is showing, the card should be dismissed and the typed message processed normally. This is handled by:
- When a new `user_message` is sent while surfaces are active, all active surfaces transition to `'dismissed'` state.
- Dismissed surfaces collapse to a single line showing what was available but not used.

### 5.3 Partial Form State

For multi-field components like `PatientFormCard`:
- State is managed locally in the component via React state (useState).
- Validation runs client-side before submission.
- The form is NOT submitted until the user explicitly taps the submit action button.
- If the user navigates away or the conversation moves on, partially filled data is lost (this is acceptable since the AI will re-ask).

---

## 6. State Management

### 6.1 Surface Lifecycle States

```
interactive  -->  submitted  (user completed the action)
interactive  -->  dismissed  (user typed a message instead)
interactive  -->  loading    (action in progress, waiting for server)
loading      -->  submitted  (server confirmed the action)
loading      -->  error      (action failed)
error        -->  interactive (allow retry)
```

### 6.2 Historical Surfaces

When a conversation is loaded from history (via `api.getConversation(id)` in `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/api/conversations.ts`), surfaces embedded in past messages render in their final state (`submitted` or `dismissed`). They are not interactive -- they serve as a visual record of what the user selected.

### 6.3 Database Schema Changes

Add a `surfaces` JSON column to the messages table in `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/database.py`. When a message with surfaces is stored via `add_message()`, the surfaces JSON is serialized alongside it. The `get_messages()` function deserializes it when loading conversation history.

---

## 7. Accessibility

### 7.1 ARIA Roles and Semantic HTML

Each DynamicUI component must use semantic HTML:
- `VaccineSelectionCard`: `role="listbox"` with `role="option"` for each vaccine. Arrow key navigation.
- `DatePickerCard`: `role="grid"` with `role="gridcell"` for each date. Arrow key navigation between dates.
- `TimeSlotCard`: `role="radiogroup"` with `role="radio"` for each slot.
- `PatientFormCard`: Standard `<form>` with `<label>` elements, `aria-required`, `aria-invalid`.
- `QuestionnaireCard`: `role="group"` with `aria-labelledby` pointing to the question text.
- `ActionButton`: Proper `aria-label` and `aria-disabled` states.

### 7.2 Dynamic Type / Font Scaling

The Tailwind CSS in `index.css` already uses `rem` units. The DynamicUI components should use the existing Tailwind scale (`text-sm`, `text-base`, etc.) to automatically respect browser font size settings.

### 7.3 Focus Management

When a new surface appears in the chat:
- Focus should NOT automatically move to the widget (this would disrupt screen reader flow).
- Instead, a live region (`aria-live="polite"`) announces: "Interactive vaccine selection card available."
- Users can Tab into the widget when ready.

When a surface is submitted:
- Focus returns to the chat input.
- A live region announces the result: "Flu vaccine selected. Waiting for response."

### 7.4 Keyboard Navigation

All interactive surfaces must be fully keyboard-accessible:
- Tab to enter the widget, Tab to move between elements.
- Enter/Space to select.
- Escape to dismiss without selecting (if appropriate).

---

## 8. Full JSON Message Format Examples

### 8.1 Vaccine Selection (emitted after `get_eligible_vaccines` tool result)

```json
{
  "type": "ui_surface",
  "surfaceId": "vaccines-a1b2c3",
  "surface": {
    "surfaceId": "vaccines-a1b2c3",
    "componentType": "vaccine_selection",
    "data": {
      "vaccines": [
        {
          "code": "FLU",
          "name": "Influenza (Flu)",
          "description": "Annual flu shot, recommended for ages 6 months+",
          "icon": "💉",
          "selected": false
        },
        {
          "code": "COVID",
          "name": "COVID-19",
          "description": "Updated COVID-19 vaccine, 2025-2026 formula",
          "icon": "🦠",
          "selected": false
        },
        {
          "code": "SHINGLES",
          "name": "Shingrix (Shingles)",
          "description": "2-dose series for adults 50+",
          "icon": "🛡️",
          "selected": false
        }
      ],
      "multiSelect": false
    },
    "actions": [
      { "name": "select_vaccine", "label": "Select", "style": "primary" }
    ],
    "state": "interactive"
  }
}
```

### 8.2 Store Finder (emitted after `search_stores` tool result)

```json
{
  "type": "ui_surface",
  "surfaceId": "stores-d4e5f6",
  "surface": {
    "surfaceId": "stores-d4e5f6",
    "componentType": "store_finder",
    "data": {
      "stores": [
        {
          "storeId": "2345",
          "clinicId": "CVS-2345",
          "name": "CVS Pharmacy #2345",
          "address": "123 Main St, Springfield, IL 62701",
          "distance": "1.2 mi",
          "availableDates": ["2026-03-18", "2026-03-19", "2026-03-20"],
          "phone": "(217) 555-0123",
          "selected": false
        },
        {
          "storeId": "6789",
          "clinicId": "CVS-6789",
          "name": "CVS Pharmacy #6789",
          "address": "456 Oak Ave, Springfield, IL 62702",
          "distance": "3.5 mi",
          "availableDates": ["2026-03-18", "2026-03-21"],
          "phone": "(217) 555-0456",
          "selected": false
        }
      ]
    },
    "actions": [
      { "name": "select_store", "label": "Select Store", "style": "primary" }
    ],
    "state": "interactive"
  }
}
```

### 8.3 User Action Response

```json
{
  "type": "ui_action",
  "surfaceId": "stores-d4e5f6",
  "action": "select_store",
  "data": {
    "storeId": "2345",
    "clinicId": "CVS-2345",
    "name": "CVS Pharmacy #2345",
    "selectedDate": "2026-03-18"
  }
}
```

---

## 9. Tool-to-Surface Mapping (Backend Implementation)

The cleanest implementation builds surfaces directly from MCP tool results in `chat_agent.py`. A new function `_build_surface_from_tool_result(tool_name, result)` handles this:

```python
def _build_surface_from_tool_result(tool_name: str, result: str) -> dict | None:
    """Build a DynamicSurface from an MCP tool result, if applicable."""
    try:
        data = json.loads(result)
    except (json.JSONDecodeError, TypeError):
        return None

    surface_id = f"{tool_name}-{uuid4().hex[:8]}"

    if tool_name == "get_eligible_vaccines":
        vaccines = data.get("eligibleVaccineData", [])
        return {
            "surfaceId": surface_id,
            "componentType": "vaccine_selection",
            "data": {
                "vaccines": [
                    {
                        "code": v.get("vaccineCode", ""),
                        "name": v.get("vaccineName", ""),
                        "description": v.get("vaccineDescription", ""),
                        "icon": _vaccine_icon(v.get("vaccineCode", "")),
                        "selected": False,
                    }
                    for v in vaccines
                ],
                "multiSelect": True,
            },
            "actions": [{"name": "select_vaccine", "label": "Select", "style": "primary"}],
            "state": "interactive",
        }

    elif tool_name == "search_stores":
        clinics = data.get("listOfClinics", [])
        return {
            "surfaceId": surface_id,
            "componentType": "store_finder",
            "data": {
                "stores": [
                    {
                        "storeId": c.get("storeId", ""),
                        "clinicId": c.get("clinicId", ""),
                        "name": f"CVS Pharmacy #{c.get('storeId', '')}",
                        "address": c.get("address", ""),
                        "distance": c.get("distance", ""),
                        "availableDates": c.get("availableDates", []),
                        "selected": False,
                    }
                    for c in clinics
                ],
            },
            "actions": [{"name": "select_store", "label": "Select Store", "style": "primary"}],
            "state": "interactive",
        }

    # ... similar mappings for other tools ...
    return None
```

This function is called right after `call_tool()` succeeds, and if it returns a surface, a `ui_surface` event is yielded via the WebSocket stream.

---

## 10. Fallback and Graceful Degradation

### 10.1 Unknown Component Type

If the backend sends a `componentType` the frontend does not recognize:

```typescript
function FallbackCard({ surface }: { surface: DynamicSurface }) {
  return (
    <div className="bg-cvs-surface border border-cvs-border rounded-xl p-4 mt-2">
      <p className="text-sm text-cvs-text-secondary italic">
        Interactive content available. Please type your response.
      </p>
      {/* Optionally render data as a formatted list */}
      <pre className="text-xs mt-2 overflow-auto">
        {JSON.stringify(surface.data, null, 2)}
      </pre>
    </div>
  );
}
```

### 10.2 Network Errors During Action Submission

If the WebSocket is disconnected when the user taps an action:
1. The surface transitions to `'error'` state with a "Connection lost" message.
2. When WebSocket reconnects, the user can retry.
3. The retry replays the same `ui_action` message.

### 10.3 Text-Only Fallback

If the frontend fails to render a surface for any reason, the AI's text response alone should still make sense. The AI text should always include a natural language version of the options: "I found the Flu vaccine, COVID-19 vaccine, and Shingrix. Which would you like?" This ensures the conversation works even without the widget.

---

## 11. Implementation Sequencing

### Phase 1: Foundation (3-4 days)
1. Define all TypeScript types in `types/index.ts`.
2. Create `DynamicUIContext.tsx`.
3. Create `DynamicSurfaceRenderer.tsx` and `FallbackCard.tsx`.
4. Modify `ChatContext.tsx` to handle new WebSocket events.
5. Modify `MessageBubble.tsx` to render surfaces.
6. Add `ui_action` handler in `chat_ws.py`.

### Phase 2: Backend Surface Generation (2-3 days)
1. Add `_build_surface_from_tool_result()` to `chat_agent.py`.
2. Add `ui_surface` event emission in the streaming loop.
3. Add `ui_action` to `ui_message` translation in the WebSocket handler.
4. Add surfaces column to the database schema.

### Phase 3: Individual Components (5-7 days)
1. `VaccineSelectionCard` -- grid with tap-to-select.
2. `StoreFinderCard` -- list with distance badges.
3. `DatePickerCard` -- calendar grid.
4. `TimeSlotCard` -- grouped time grid.
5. `PatientFormCard` -- inline form with validation.
6. `QuestionnaireCard` -- sequential yes/no.
7. `ConfirmationCard` -- summary with confirm button.
8. `AppointmentCard` -- list with cancel action.
9. `LoginCard` and `OTPVerificationCard`.

### Phase 4: Polish (2-3 days)
1. Accessibility audit (ARIA, keyboard nav, screen reader testing).
2. Animation (surface entrance/exit transitions).
3. Historical surface rendering (loading from database).
4. Edge case handling (dismissed surfaces, retry logic).

---

## 12. Potential Challenges

1. **LLM Text vs. UI Surface Coordination**: If using the LLM-generates-JSON approach, the model may produce invalid JSON or forget the delimiter. The tool-result-driven approach avoids this entirely and is strongly recommended.

2. **Surface Ordering in Chat**: Surfaces should appear between the tool indicator and the AI text response. The current rendering order in `ChatArea.tsx` is: messages, tool indicators, streaming content. Surfaces need to be inserted at the right position.

3. **Conversation History Replay**: When loading a conversation, surfaces stored in the database need to be deserialized and re-attached to their messages. They should render in `submitted`/`dismissed` state, not `interactive`.

4. **WebSocket Reconnection**: If the WebSocket reconnects mid-surface interaction, the active surfaces should be preserved in DynamicUIContext (they are client-side state). Only the WebSocket send for actions needs to be retried.

5. **Mobile Responsiveness**: The existing Tailwind setup handles responsive widths. Dynamic surfaces should use the same `max-w-3xl` container as the chat area, with internal responsive grids (e.g., vaccine cards: 2 columns on mobile, 3 on desktop).

---

### Critical Files for Implementation
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/types/index.ts` - Must add all DynamicSurface types, ComponentType union, component data interfaces, and new WSEvent/WSClientMessage variants
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/contexts/ChatContext.tsx` - Must handle new ui_surface/ui_data/ui_delete WebSocket events and integrate with DynamicUIContext
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/frontend/src/components/Chat/MessageBubble.tsx` - Must render DynamicSurfaceRenderer alongside markdown content within chat bubbles
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/chat_agent.py` - Must add _build_surface_from_tool_result() to transform MCP tool results into UI surfaces and emit ui_surface events during streaming
- `/Users/sarathfrancis/work/git/innovation_lab/voice-scheduling/app/routes/chat_ws.py` - Must handle incoming ui_action messages from the client and translate them into the AI conversation flow

---

