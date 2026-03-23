# Claude Conversation Log

Session ID: agent-a1afa42efca0afb31
Date: 2026-03-03 00:43:40

---

## 👤 User

You need to write detailed epic and story sections for Epics 9 through 11 of the ZipPath project.

IMPORTANT: Other agents are writing Epics 1-8. You should write Epics 9-11 to a TEMPORARY file at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics-9-11-temp.md so they can be merged later.

First read the main epics.md at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics.md to understand the epic structure, FR coverage map, and requirements. Then write Epics 9 through 11 to the temp file.

Generate stories using EXACTLY this format for each story:

```
### Story {N}.{M}: {story_title}

As a {user_type},
I want {capability},
So that {value_benefit}.

**Acceptance Criteria:**

**Given** {precondition}
**When** {action}
**Then** {expected_outcome}
**And** {additional_criteria}
```

Each story must:
- Be completable by a single dev agent
- Have clear user value  
- Include 3-6 specific, testable Given/When/Then acceptance criteria
- Reference the FRs it covers
- NOT depend on future stories (only on previous stories)

Here are the stories to generate:

## Epic 9: Accessibility & Inclusive Design

**Story 9.1: Screen Reader Support for Non-Game UI**
FRs: FR111
- All non-game screens (Home, Groups, Stats, Profile, Settings) fully navigable via VoiceOver (iOS) and TalkBack (Android). Every interactive element has semantic label. Navigation landmarks (headings, buttons, lists) properly tagged. Custom widgets wrapped in Semantics. Decorative elements excluded via ExcludeSemantics.

**Story 9.2: Screen Reader Support for Puzzle Grid**
FRs: FR112
- Grid cells labeled: "Row N, Column M, [empty/filled/waypoint N/wall]". Waypoints identified: "Waypoint N, [reached/unreached]". Path state announced on change: "Path drawn through N of M cells". Navigable via VoiceOver swipe gestures. MergeSemantics for logically grouped elements.

**Story 9.3: Colorblind Mode & Discoverability**
FRs: FR96, FR117
- Three alternative palettes selectable in Settings > Accessibility: deuteranopia, protanopia, tritanopia. Patterns/textures added: crosshatch on path cells, dots on waypoints, dashes on walls. Discoverability: if system accessibility color filters detected, show one-time prompt suggesting colorblind mode. Prominent "Accessibility" section in Settings.

**Story 9.4: Dynamic Type, Focus Indicators & Alternative Feedback**
FRs: FR114, FR115, FR116
- Dynamic type: all text scales up to 200% system font scaling without layout overflow. Layouts adapt via scrolling, text wrapping, or reduced density. Golden tests at 100%, 150%, 200%. Focus indicators: visible focus ring on all interactive elements when navigating via external keyboard or switch control. Visual alternatives: screen flash and icon animations for audio/haptic cues on devices without haptic motors.

## Epic 10: Error Recovery & App Resilience

**Story 10.1: Force Update & Maintenance Mode**
FRs: FR68, FR73
- Force update: on app launch, check minimum required version via Firebase Remote Config or Supabase. If current version < minimum, display full-screen blocking UI with app store link, explanation text, and no dismiss option. Maintenance mode: when backend returns 503 or health check fails, show branded maintenance screen with estimated restoration time, automatic retry every 30s, graceful offline fallback for cached content.

**Story 10.2: App State Restoration & Session Lifecycle**
FRs: FR74, FR87
- State restoration: after OS process death, restore user to correct screen based on persisted navigation state (home, puzzle in progress with saved state, result pending). Session lifecycle: tokens expire after 30 days inactivity, refresh tokens after 90 days, expired sessions require re-authentication with friendly prompt. Users can view active sessions (future: revoke sessions).

**Story 10.3: Clock Manipulation Detection**
FRs: FR75
- Score submission includes client timestamp. Server compares against server wall-clock time. Configurable tolerance window (default: ±5 minutes). Submissions outside tolerance rejected with "Time verification failed" error. Solve times validated: must be >3s (per NFR11), must be <24h (sanity check). Rejected submissions do NOT count as the daily attempt — user can retry.

**Story 10.4: Error Recovery for Auth & Puzzle Operations**
FRs: FR99, FR102, FR103
- OAuth failure: if Google/Apple sign-in fails or account linking fails, anonymous session fully preserved, error message explains what happened ("Sign-in failed. Your progress is safe."), retry and dismiss options. Puzzle load failure: when no cache AND no network, show illustration + "No puzzle available" + retry button; fall back to bundled puzzles if available. Puzzle generation failure: if cron fails, retry 3x with exponential backoff, trigger alert (email/Slack) to developer, previous day's puzzle type serves as emergency fallback.

**Story 10.5: Data Export & DSAR Handling**
FRs: FR66, FR67
- Data export: users can tap "Export My Data" in Profile > Settings to generate downloadable JSON/CSV containing: profile info, solve history (dates, times, hints, undos), streak history, group memberships. Export generated as file, shared via native share sheet. DSAR backend: Edge Function or admin endpoint generates complete data package for any user_id within 30 days per GDPR requirement.

## Epic 11: Analytics, Feature Flags & Optimization

**Story 11.1: Analytics Event Taxonomy & Core Tracking**
FRs: FR118
- Implement defined event taxonomy via Firebase Analytics: app_opened, screen_view (on every screen mount), puzzle_started, puzzle_completed (with solve_time_ms, hints_used, grid_size params), hint_used, share_tapped, share_completed, group_created, group_joined, invite_sent, account_created, account_linked, streak_milestone (with streak_count param). All events include user_id (anonymized for anonymous users) and timestamp. Analytics consent respected per FR63.

**Story 11.2: Funnel & Attribution Tracking**
FRs: FR119, FR120
- First-time user funnel: track sequential events app_installed → first_puzzle_started → first_puzzle_completed → account_created → first_group_joined with timestamps for conversion analysis. Attribution: track install source — deep link (group invite), share card link, organic app store, unknown. Store attribution source in profiles table (acquisition_source field). UTM parameters parsed from deep links.

**Story 11.3: Feature Flags & A/B Testing Infrastructure**
FRs: FR121, FR122
- Firebase Remote Config setup with default fallback values for all flags. Feature flags: kill switches for broken features (e.g., disable_share_cards, disable_notifications), gradual rollout flags (e.g., enable_new_celebration). A/B testing: user cohort assignment based on user_id hash, experiment parameters configurable (e.g., daily_hint_count: 3 vs 5, onboarding_flow: "minimal" vs "guided"). Experiment events tracked linking user cohort to outcomes. 12-hour minimum fetch interval, 24-hour stale config TTL.

IMPORTANT: Write the full epic header and all stories with complete acceptance criteria in Given/When/Then format. Each story needs 3-6 independently testable acceptance criteria. This is the actual implementation specification that developers will follow.

---

## 🤖 Claude



I'll start by reading the main epics.md file to understand the structure, FR coverage map, and requirements.

---

## 🤖 Claude

Let me read the file in sections to get the full content.

---

## 🤖 Claude

Now I have the complete picture of the epics file. Let me also check the output directory exists.

---

## 🤖 Claude

Good, the directory exists. Now let me write the comprehensive Epics 9-11 temp file with all stories and acceptance criteria.

---

## 🤖 Claude

Now let me verify the file was written correctly by reading it back.

---

## 🤖 Claude

Let me also verify the acceptance criteria counts per story.

---

## 🤖 Claude

Let me also verify the FR coverage is complete by checking all the FRs mentioned in the coverage map for Epics 9-11 are referenced in the stories.

---

## 🤖 Claude

All FRs are properly covered. Here is a summary of what was generated:

---

The file has been written to `/Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics-9-11-temp.md` (565 lines, 12 stories across 3 epics).

**Structure summary:**

**Epic 9: Accessibility & Inclusive Design** (4 stories)
- **Story 9.1: Screen Reader Support for Non-Game UI** (FR111) -- 6 acceptance criteria covering VoiceOver/TalkBack for Home, Groups, Stats, Profile, Settings screens; semantic labels, landmarks, decorative element exclusion, and CI accessibility tests.
- **Story 9.2: Screen Reader Support for Puzzle Grid** (FR112) -- 6 acceptance criteria covering cell labeling ("Row N, Column M, [state]"), waypoint reached/unreached announcements, swipe navigation order, MergeSemantics for grouped elements, live region updates on path changes, and completion announcements.
- **Story 9.3: Colorblind Mode & Discoverability** (FR96, FR117) -- 6 acceptance criteria covering three palette options (deuteranopia, protanopia, tritanopia) with preview swatches, pattern overlays (crosshatch/dots/dashes), system accessibility detection prompt, prominent Settings placement, share card exclusion from colorblind palettes, and golden tests.
- **Story 9.4: Dynamic Type, Focus Indicators & Alternative Feedback** (FR114, FR115, FR116) -- 6 acceptance criteria covering 200% font scaling without overflow, golden tests at 100%/150%/200%, visible focus rings for keyboard/switch navigation, visual alternatives (screen flash, icon animations) for haptic/audio on unsupported devices, reduced motion respect, and live font scaling on app foreground.

**Epic 10: Error Recovery & App Resilience** (5 stories)
- **Story 10.1: Force Update & Maintenance Mode** (FR68, FR73) -- 5 acceptance criteria covering blocking force-update UI with app store link, maintenance screen with 30s auto-retry, offline fallback during maintenance, no-connectivity bypass of version check, and platform-specific minimum versions.
- **Story 10.2: App State Restoration & Session Lifecycle** (FR74, FR87) -- 6 acceptance criteria covering puzzle-in-progress restoration after process death, result screen restoration, home screen/tab restoration, 30-day token expiry with friendly re-auth prompt, 90-day refresh token expiry, and active sessions list display.
- **Story 10.3: Clock Manipulation Detection** (FR75) -- 6 acceptance criteria covering server-side timestamp comparison with configurable tolerance (default 5 min), minimum solve time (>3s) and maximum solve time (<24h) validation, rejected submissions not counting as daily attempt, legitimate clock drift handling, and structured audit logging.
- **Story 10.4: Error Recovery for Auth & Puzzle Operations** (FR99, FR102, FR103) -- 5 acceptance criteria covering OAuth failure with anonymous session preservation, puzzle load failure with bundled fallback option, cron generation failure with 3x exponential backoff retry and developer alerting, emergency fallback puzzle generation, and corrupted cache recovery.
- **Story 10.5: Data Export & DSAR Handling** (FR66, FR67) -- 5 acceptance criteria covering user-facing "Export My Data" with JSON output via share sheet, export failure handling with retry, DSAR backend endpoint with admin auth and 30-day compliance window, and export availability during account deletion grace period.

**Epic 11: Analytics, Feature Flags & Optimization** (3 stories)
- **Story 11.1: Analytics Event Taxonomy & Core Tracking** (FR118) -- 6 acceptance criteria covering the full event taxonomy (app_opened, screen_view, puzzle_started/completed, hint_used, share_tapped/completed, group_created/joined, invite_sent, account_created/linked, streak_milestone), parameter specifications, consent gating per FR63, centralized event constants file, and crash reporting independence from analytics consent.
- **Story 11.2: Funnel & Attribution Tracking** (FR119, FR120) -- 6 acceptance criteria covering sequential funnel event tracking (installed through first_group_joined) with time_since_install_ms, deep link attribution with UTM parsing, share card attribution with referrer capture, organic/unknown fallback sources, and profiles.acquisition_source queryability.
- **Story 11.3: Feature Flags & A/B Testing Infrastructure** (FR121, FR122) -- 6 acceptance criteria covering Remote Config with hardcoded defaults and 12h/24h fetch/stale intervals, kill switch flags with `disable_{feature}` convention, A/B test cohort assignment via user_id hash with experiment event tracking, gradual rollout percentage controls, offline config fallback chain, and typed provider access via central defaults file.

**FR Coverage verification:** All 22 FRs assigned to Epics 9-11 (FR66, FR67, FR68, FR73, FR74, FR75, FR87, FR96, FR99, FR102, FR103, FR111, FR112, FR114, FR115, FR116, FR117, FR118, FR119, FR120, FR121, FR122) are explicitly covered by story `**Covers:**` tags.

---

