# Claude Conversation Log

Session ID: agent-a6caf00e755b039d4
Date: 2026-03-03 00:03:08

---

## 👤 User

Read the full UX design specification at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/ux-design-specification.md and identify ANY production-readiness gaps. Specifically audit:

1. Missing error state designs (network timeout during puzzle solve, failed score submission, failed group join?)
2. Missing edge case UI states (user in 0 groups viewing groups tab, user with 0 solves viewing stats, expired invite code?)
3. Missing transition/navigation edge cases (deep link when already in puzzle, back button during celebration animation?)
4. Missing permission request UX (notification permission prompt timing, camera for QR scan?)
5. Missing app update UX (force update screen, optional update prompt?)
6. Missing first-run experience details (splash screen, any progressive disclosure?)
7. Missing keyboard/input handling (keyboard covering fields, input validation feedback timing?)
8. Missing pull-to-refresh and data staleness UX (how old can leaderboard data be before showing stale indicator?)
9. Missing multi-device UX (same account on two phones - what happens?)
10. Missing state restoration UX (app killed during puzzle - resume or restart?)
11. Missing connectivity transition UX (goes offline DURING puzzle solve, comes back online while viewing cached leaderboard?)
12. Missing dark/light mode transition (does it animate? instant switch? follow system?)
13. Missing tablet-specific UX beyond "centered content"
14. Missing landscape orientation handling (locked portrait or graceful landscape?)
15. Missing accessibility testing coverage gaps

Report ALL findings as a categorized list with severity (Critical/High/Medium/Low) and whether each is MVP or post-MVP.

---

## 🤖 Claude



I'll start by reading the full UX design specification document.

---

## 🤖 Claude

The file is large. Let me read the full saved output.

---

## 🤖 Claude

Now let me also check for any related documents that might provide additional context.

---

## 🤖 Claude

Now I have a thorough understanding of the UX design specification. Let me compile the comprehensive audit.

---

# ZipPath UX Design Specification -- Production-Readiness Audit

Below is a categorized audit of all gaps found in the UX design specification at `/Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/ux-design-specification.md`. Each finding includes severity and MVP/post-MVP classification.

---

## 1. Missing Error State Designs

### 1.1 Network Timeout During Puzzle Solve
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec describes offline play and result queuing (Journey 4, lines 750-774), but does not address the scenario where the user *starts online*, the network drops *during* the solve, and the completion event (score submission) fails. The spec mentions "Result Queued Locally -- 'Will sync when online'" for the offline journey, but there is no explicit design for the transition case where a score submission call times out or returns a server error after the user has already seen the celebration screen. What does the user see? Does the result screen show an error SnackBar? Does it silently queue? The current feedback patterns (lines 1042-1043) mention a generic "Network error: SnackBar with 'Retry' action" but do not specify this for the score submission flow specifically.

### 1.2 Failed Score Submission
- **Severity: High**
- **Phase: MVP**
- **Finding:** The spec never explicitly describes what happens when score submission to the server fails (server 500, timeout, rate limit). The PRD mentions "Score submission completes < 300ms" as a target, but the UX spec has no design for the failure path. Questions unanswered: Does the result screen show a retry button? Is there a persistent indicator on the home screen that a result is pending sync? Can the user view the leaderboard if their own score has not been submitted? What if they kill the app before the retry succeeds -- is the locally-queued result durable?

### 1.3 Failed Group Join
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** Journey 3 (lines 718-744) and the Group Join screen (line 1324) describe the happy path of joining a group. There is no design for: server error during join, group already at 50-member capacity (line 1049 mentions a dialog for "group full" but this is one line with no visual specification), invite code that exists but the user is already a member, or network failure during the join process. The "Group full" case is mentioned in the Warning Feedback section but the dialog content, actions, and visual design are not specified.

### 1.4 Failed Group Creation
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** No error design for group creation failure (name conflict, server error, network timeout during creation). The spec shows a `CircularProgressIndicator` for "network-dependent actions (score submission, group creation)" at line 1054, but does not describe the error recovery path if creation fails after the spinner.

### 1.5 Failed Account Conversion
- **Severity: High**
- **Phase: MVP**
- **Finding:** Journey 5 (lines 776-802) describes anonymous-to-account conversion. There is no error design for: OAuth flow failure (user cancels Google/Apple sign-in), email already in use by another account, network failure during account linking, or failure to link the anonymous session to the new account (data loss risk). This is critical because a failure here could leave the user confused about whether their streak/stats are preserved.

### 1.6 Failed Puzzle Fetch (No Cache, No Network)
- **Severity: High**
- **Phase: MVP**
- **Finding:** The spec mentions 7 bundled fallback puzzles (line 681) for first launch, and pre-caching for returning users. But there is no explicit design for the scenario where the cache is empty (app data cleared, fresh install without bundled puzzles due to a build issue) AND the network is unavailable. What does the home screen show? What does the DailyPuzzleCard display? Is there a "No puzzle available" state?

### 1.7 Server-Side Puzzle Validation Rejection
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The PRD mentions "Server-side puzzle validation prevents cheated scores." There is no UX design for what happens if a legitimately-solved puzzle is rejected by server validation (clock tampering detection, modified client, data corruption). Does the user see an error? Is their solve time still shown locally? Is their streak affected?

---

## 2. Missing Edge Case UI States

### 2.1 User in 0 Groups Viewing Groups Tab
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The spec mentions an empty state for "No groups joined" (line 1058): "Illustration + 'Join or create a group to compete with friends' + 'Create Group' / 'Join Group' buttons." This is mentioned but has no visual specification (illustration style, layout, sizing). It is acknowledged but underspecified.

### 2.2 User with 0 Solves Viewing Stats Tab
- **Severity: Low**
- **Phase: MVP**
- **Finding:** Similarly, "No stats yet: 'Solve your first puzzle to start tracking stats'" is listed (line 1060) but has no visual specification. What does the Stats screen look like with empty charts? Are the chart areas shown as empty containers, or is the entire layout replaced with the empty state illustration?

### 2.3 Expired or Invalid Invite Code
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** No design exists for entering an expired invite code, a code for a deleted group, or a malformed code. The Group Join screen (line 1324) mentions "Code input field, or auto-populated from deep link, group preview" but does not address validation failure states. What does the user see after entering an invalid code? Inline error text? A dialog? What is the copy?

### 2.4 User Already a Member Attempting to Join
- **Severity: Low**
- **Phase: MVP**
- **Finding:** No design for the case where a user taps a group invite link for a group they are already a member of. Do they see a "You're already a member" message and get redirected to the group detail page? Or does the join confirmation screen appear and error out?

### 2.5 User Removed from a Group
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec mentions "Admin: Manage Members" (line 1345) but does not describe the UX for a user who has been removed from a group. How are they notified? What happens to the group in their Groups tab? Is there a "You were removed from [Group Name]" state? Can they rejoin?

### 2.6 Maximum Groups Reached
- **Severity: Low**
- **Phase: Post-MVP**
- **Finding:** No design for when a user tries to create or join a group but has reached a maximum group count (if one exists). The spec does not mention a group limit per user at all.

### 2.7 Hint Usage When Path Is Complete Except One Cell
- **Severity: Low**
- **Phase: MVP**
- **Finding:** No design for edge cases around hints: What if the user uses a hint when only 1-2 cells remain? Does the hint auto-complete the puzzle? Is the hint button disabled when the puzzle is trivially close to completion?

### 2.8 Streak Freeze Already Used This Week
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec mentions "1 per week, auto-applied" streak freeze (line 217) but does not design the UX for when the user misses a second day in the same week. Is there a notification? Does the home screen show "Streak freeze unavailable this week"? What is the visual treatment of the broken streak?

### 2.9 Anonymous User Hitting Feature Gates
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec says account creation is prompted at "3rd solve or group join attempt" (line 780). But what about other gated actions? Can an anonymous user share results? Can they view stats beyond the current session? The spec does not systematically enumerate which features are available to anonymous vs. authenticated users and what the gate looks like for each.

---

## 3. Missing Transition/Navigation Edge Cases

### 3.1 Deep Link When Already in Puzzle
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The deep link navigation section (lines 1078-1082) describes links opening to group join confirmation or puzzle screen. No design exists for what happens if a deep link is received while the user is actively solving a puzzle. Is the puzzle paused? Is the deep link queued? Does a dialog appear asking the user to leave the puzzle? This could cause data loss if the puzzle state is interrupted.

### 3.2 Back Button During Celebration Animation
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The CelebrationOverlay (line 898) states it is "Non-blocking -- tapping during animation skips to result screen." However, the spec does not address what happens if the user presses the system back button (Android) or swipe-back gesture (iOS) during the celebration. Does it skip to result? Does it exit to home? Does it discard the result? The gesture priority list (lines 400-409) only covers the puzzle screen, not the celebration/result transition.

### 3.3 App Backgrounded During Celebration
- **Severity: Low**
- **Phase: MVP**
- **Finding:** If the user backgrounds the app during the celebration animation (incoming call, notification tap), the spec does not describe whether they return to the result screen or replay the celebration.

### 3.4 Navigation Stack After Multiple Deep Links
- **Severity: Low**
- **Phase: Post-MVP**
- **Finding:** The spec says each tab maintains its own navigation stack (line 1070), but does not address stack pollution from deep links. If the user opens 3 different group invite links in succession, what does the back button behavior look like?

### 3.5 Tab Switch While Data Is Loading
- **Severity: Low**
- **Phase: MVP**
- **Finding:** No design for what happens when a user switches tabs while a leaderboard or group list is still loading (skeleton state). Is the load cancelled? Resumed when they return? Does the data persist across tab switches?

---

## 4. Missing Permission Request UX

### 4.1 Notification Permission Prompt Timing
- **Severity: High**
- **Phase: MVP**
- **Finding:** The spec mentions notifications multiple times: "New puzzle ready" notifications (line 178), "You're the last one!" notifications (line 75, 193), per-group notification controls in settings (line 1365), and "Notifications are opt-in per group" (line 276). However, there is **no design for when or how the OS-level notification permission dialog is triggered**. This is critical because iOS only allows one shot at the system permission prompt. The spec does not describe: a pre-permission screen explaining the value of notifications, the timing of the prompt (after first solve? after joining a group? after enabling notifications in settings?), or the fallback UX if the user denies permission.

### 4.2 Camera Permission for QR Code Scanning
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The GroupInviteCard (lines 942-945) mentions QR code sharing. The Group Join screen mentions joining via "code entry" but if QR scanning is supported for joining, camera permission is needed. The spec does not address: camera permission request flow, fallback if denied, or whether QR scanning for joining groups is even an MVP feature (only QR display for sharing is described, not QR scanning for joining).

### 4.3 Photo Library Permission for Share Card
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The ShareCard (lines 935-938) describes generating an image for sharing. If the user chooses to save the share card to their photo library (rather than sharing directly), photo library write permission is needed. No UX for this permission request or denial is described.

---

## 5. Missing App Update UX

### 5.1 Force Update Screen
- **Severity: Critical**
- **Phase: MVP**
- **Finding:** The spec has **no design for forced app updates**. If the API version changes and the client must update to continue functioning (e.g., puzzle format change, authentication protocol change), there must be a full-screen blocking UI directing the user to update. This is completely absent. For a daily puzzle game where users have strong expectations about daily availability, a well-designed force update screen is critical to prevent confusion and churn.

### 5.2 Optional Update Prompt
- **Severity: Medium**
- **Phase: Post-MVP**
- **Finding:** No design for a gentle, dismissible prompt encouraging users to update to the latest version (for bug fixes, new features). This is less urgent than force update but important for long-term maintenance.

### 5.3 App Store Rating Prompt
- **Severity: Low**
- **Phase: Post-MVP**
- **Finding:** No design for when/how to prompt users for App Store/Play Store reviews. The PRD targets "4.5+ average rating" but the UX spec does not describe the timing or presentation of a review prompt.

---

## 6. Missing First-Run Experience Details

### 6.1 Splash Screen / Launch Screen
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** No design for the app launch screen (splash screen). Every mobile app needs a launch screen asset (required by both iOS and Android). The spec jumps directly from "App Opens" to "Home Screen" (line 657). What does the user see during the cold start (spec says < 2 seconds)? Is it a branded splash with the ZipPath logo? Is it a blank screen with the background color? This needs a visual specification.

### 6.2 Progressive Disclosure for First-Time Users
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec mentions "progressive disclosure and affordances, not instructions" (line 65) and "No tutorial gate" (line 273). However, there is no specific design for first-time user affordances on the puzzle screen. How does a brand new user know they should drag to draw? Are there subtle visual hints on the first cell (a pulsing indicator on waypoint 1)? A "Drag to start" tooltip that appears once and never again? The spec says "Show, don't tell" (line 823) but does not describe what is shown.

### 6.3 First Completion Moment
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The first puzzle completion is a critical onboarding moment. The spec does not distinguish the first-ever completion experience from subsequent ones. Should the first completion include an additional prompt (e.g., "Join a group to compete with friends"? "Create an account to save your streak"?). The account creation prompt is tied to the 3rd solve, but the first completion is a high-engagement moment that could include an extra nudge toward social features.

---

## 7. Missing Keyboard/Input Handling

### 7.1 Keyboard Covering Input Fields
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec includes text input fields for: group name (line 843), display name (line 843), invite code entry (line 1324), email and password for account creation (line 785). There is no design for how the screen responds when the soft keyboard appears. Do fields scroll into view? Does the bottom sheet (for account creation) resize? This is a common mobile UX issue that causes fields to be hidden behind the keyboard.

### 7.2 Input Validation Feedback Timing
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec mentions "Real-time validation with inline error text below field" (line 1130) for text inputs. But the timing is not specified. Does validation run on every keystroke? On field blur? After a debounce? For group name, does it check uniqueness against the server in real time (and what loading state accompanies that)? For email validation, is it format-only or does it check for existing accounts? The spec says "Real-time" but the actual behavior needs more definition.

### 7.3 Invite Code Input Format
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The invite code is shown as "ZP3K9M" (line 729) -- 6 alphanumeric characters. The input field for entering a code manually (Group Join screen) has no specified input formatting: uppercase enforcement, character limit indicator, auto-advance behavior, or whether lowercase input is auto-uppercased. These details affect perceived polish.

---

## 8. Missing Pull-to-Refresh and Data Staleness UX

### 8.1 Leaderboard Data Staleness Indicator
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec mentions "Pull-to-refresh for leaderboards" (line 122, 260) and "optimistic local state" (line 1055). However, there is **no design for how stale data is communicated to the user**. Questions unanswered: How old can leaderboard data be before a "Last updated X minutes ago" indicator appears? Is there a visual difference between cached and fresh data? If a user views a leaderboard from 6 hours ago, do they see a stale indicator or does it look current? This matters because the competitive context of leaderboards depends on freshness.

### 8.2 Pull-to-Refresh Failure
- **Severity: Low**
- **Phase: MVP**
- **Finding:** No design for when pull-to-refresh fails (no network, server error). Does the pull-to-refresh animation complete and show a SnackBar error? Does it show the previously cached data with a "Could not refresh" indicator?

### 8.3 Background Data Refresh
- **Severity: Low**
- **Phase: Post-MVP**
- **Finding:** No design for background data refresh behavior. When the user switches from another app back to ZipPath, does the leaderboard auto-refresh? Or only on pull-to-refresh? What about the home screen group activity summary?

---

## 9. Missing Multi-Device UX

### 9.1 Same Account on Two Devices
- **Severity: High**
- **Phase: MVP**
- **Finding:** The spec has **no design for multi-device usage**. If a user logs into their account on a second phone: Can they solve the puzzle on both devices? (Presumably the first solve counts, but what does the second device show?) Are streaks consistent across devices immediately? What happens if they solve offline on device A and then solve on device B while A is still offline -- does the first sync win? What about in-progress puzzle state -- is it synced or per-device? The PRD mentions "one attempt per user per day" but the UX for enforcing this across devices is not designed.

### 9.2 Account Signed In Elsewhere
- **Severity: Medium**
- **Phase: Post-MVP**
- **Finding:** No design for session management across devices. Is there a "Signed in on another device" notification? Can both devices be active simultaneously? If one device's session is invalidated, what is the UX?

---

## 10. Missing State Restoration UX

### 10.1 App Killed During Puzzle
- **Severity: High**
- **Phase: MVP**
- **Finding:** The spec describes a "Paused" touch state (line 396) when the finger is lifted, but does not address the app being killed by the OS (memory pressure, user force-quit) during an active puzzle. Questions unanswered: Is the partial path saved to local storage? On next app open, does the user see "Resume puzzle?" or does the puzzle reset? If the puzzle resets, does the timer reset too? The gesture priority list mentions "System back gesture -- Exits puzzle (with 'are you sure?' if in progress)" (line 409), implying there is an in-progress state, but the restoration of that state after process death is not specified.

### 10.2 App Backgrounded During Puzzle
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** Related but distinct: When the app is backgrounded (home button, app switcher, incoming call) but not killed, does the timer continue running? Does it pause? Is the puzzle screen preserved exactly? The "hidden timer" is only revealed on completion (line 158, lines 380-381), so users may not realize the timer is affected, but it impacts competitive fairness if backgrounding pauses vs. continues the timer.

### 10.3 Restoring After App Update
- **Severity: Low**
- **Phase: MVP**
- **Finding:** If the user updates the app mid-day, is their in-progress puzzle state preserved across the update? Is the pre-cached puzzle still valid? No design addresses the post-update first-launch experience.

---

## 11. Missing Connectivity Transition UX

### 11.1 Going Offline During Puzzle Solve
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The offline journey (lines 750-774) describes starting offline. It does not describe the transition from online to offline DURING a solve. The OfflineBanner (lines 958-963) says "Appears when network is lost" -- but does it appear over the puzzle grid during active play? This could be distracting and break flow state (which the spec explicitly protects at line 213). Should the offline banner be suppressed during active puzzle play and only shown on the result screen or home screen?

### 11.2 Coming Back Online While Viewing Cached Leaderboard
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The spec says the OfflineBanner "Auto-dismisses when network returns" (line 962). But when a user is viewing a cached leaderboard and connectivity returns, does the leaderboard auto-refresh? Does the user need to pull-to-refresh? Is there a visual indication that fresher data is available? The "optimistic local state" pattern (line 1055) is for writes, not for stale reads.

### 11.3 Queued Results Sync Notification
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The offline flow says "Background Sync Triggers Automatically" (line 763) and "Percentile + Group Rank Now Available" (line 765). But how is the user notified that their queued result has synced? A SnackBar that appears potentially hours later? An update to the home screen puzzle card? The spec does not define this feedback.

---

## 12. Missing Dark/Light Mode Transition

### 12.1 Mode Switching Behavior
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec defines both dark mode (lines 443-466) and light mode (lines 469-484) color systems, and mentions a theme selection toggle in Settings (line 1322). However, it does not specify: Does the app follow system theme by default (auto mode)? Is there a three-way toggle (Dark / Light / System)? When switching modes in settings, does the transition animate (cross-fade) or is it an instant switch? During puzzle play, can the theme be switched? Does a theme change mid-puzzle cause visual disruption? What are the animation curves and durations for the theme transition?

### 12.2 Theme Persistence
- **Severity: Low**
- **Phase: MVP**
- **Finding:** No mention of whether theme preference is stored locally only or synced with the account. If a user sets dark mode on one device, does it apply on another device?

---

## 13. Missing Tablet-Specific UX

### 13.1 Tablet Layout Beyond Centered Content
- **Severity: Medium**
- **Phase: Post-MVP**
- **Finding:** The tablet strategy (lines 1157-1161) is minimal: "Grid size is capped at max cell size of 64dp," "additional horizontal padding," "No split-view or multi-column layouts for MVP." While this is acknowledged as post-MVP, the spec should at least address: iPad multitasking (Split View, Slide Over) -- what happens when the app is resized? Is the app usable in a 1/3 width split view? Does the grid adapt? iPad keyboard shortcuts (if a hardware keyboard is connected)? iPad pointer/trackpad support (hover states on buttons, cursor changes)?

### 13.2 iPad Stage Manager
- **Severity: Low**
- **Phase: Post-MVP**
- **Finding:** No mention of iPadOS Stage Manager support (resizable windows). Even if not supported, the spec should declare whether the app locks to a minimum window size or adapts.

---

## 14. Missing Landscape Orientation Handling

### 14.1 Orientation Lock vs. Graceful Landscape
- **Severity: High**
- **Phase: MVP**
- **Finding:** The spec states "Portrait orientation is the primary layout. Landscape is NOT supported for puzzle play" (line 1152). However, it does not specify whether the app **locks orientation to portrait** system-wide, or merely does not optimize for landscape. This is a critical implementation decision. If orientation is not locked and the user rotates to landscape: Does the grid render in landscape (potentially with very small cells on a wide 8x8 grid)? Does the app show a "Please rotate to portrait" message? Does nothing happen (orientation locked)? The spec must explicitly state the orientation lock policy for both phones and tablets.

### 14.2 Tablet Landscape
- **Severity: Medium**
- **Phase: Post-MVP**
- **Finding:** Even if phone landscape is locked to portrait, iPads are frequently used in landscape. The spec's tablet strategy does not address landscape orientation at all. A 500dp max-width grid centered on a landscape iPad would have enormous amounts of empty space on the sides.

---

## 15. Missing Accessibility Testing Coverage Gaps

### 15.1 Screen Reader Support Deferred Entirely
- **Severity: Critical**
- **Phase: MVP (partial)**
- **Finding:** Screen reader support is explicitly marked as "Post-MVP Roadmap" (lines 1234-1248). However, **basic screen reader functionality should be considered MVP for app store compliance and ethical accessibility**. While the full grid-cell-by-cell navigation can be post-MVP, at minimum the following should be MVP: all navigation buttons labeled, all screens navigable, all non-game UI (home, groups, stats, profile, settings) screen-reader accessible. The spec defers ALL screen reader work to post-MVP, which risks shipping an app where blind users cannot even navigate the non-game screens.

### 15.2 Dynamic Type at Extreme Sizes
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec mentions "Dynamic type: All text respects system font size preferences up to 200% scaling" (line 588). However, there is no design for how the layout adapts at extreme text sizes. At 200% scaling, card layouts may overflow, button text may truncate, leaderboard entries may break. No truncation rules, overflow behaviors, or maximum line counts are specified for any text element.

### 15.3 Colorblind Mode Toggle Discovery
- **Severity: Medium**
- **Phase: MVP**
- **Finding:** The spec mentions colorblind modes in Settings (line 1214, 1322) with alternative palettes for deuteranopia, protanopia, and tritanopia. However, there is no design for how a colorblind user DISCOVERS this setting. If a user is colorblind and struggles to distinguish game elements on their first play, they may churn before finding the setting in Profile > Settings. Should there be a more prominent mention during onboarding or on the puzzle screen?

### 15.4 Tap-to-Select Alternative Not Specified Visually
- **Severity: Medium**
- **Phase: Post-MVP**
- **Finding:** The spec mentions "Tap-to-select mode: Tap adjacent cells one at a time to build the path" (line 1247) as an input alternative for users who cannot use drag gestures. This is post-MVP but has no visual design at all: How is the "current selectable cell" indicated? How does the user know which adjacent cells are valid? Is there a selection cursor? This needs at least a conceptual design to inform the architecture.

### 15.5 Focus Indicators for Switch/Keyboard Navigation
- **Severity: Low**
- **Phase: Post-MVP**
- **Finding:** External keyboard/switch support is mentioned (line 1248) but there is no design for focus indicators (visible focus ring) on interactive elements when using non-touch input. Flutter's Material 3 provides some focus support by default, but the custom game canvas would need explicit focus ring rendering.

### 15.6 Audio/Sound Accessibility
- **Severity: Low**
- **Phase: MVP**
- **Finding:** The feedback matrix (lines 425-435) includes an "Audio (if enabled)" column with sounds like "Soft tick," "Chime note," "Dull thud," and "Victory fanfare." The spec mentions a sound effects toggle in Settings (line 1322). However, there is no design for visual equivalents of audio cues for deaf/hard-of-hearing users beyond what haptic feedback provides. For users on devices without haptic motors (some tablets, older phones), audio and haptic cues may both be unavailable, leaving only visual feedback.

---

## Summary Table

| # | Finding | Severity | Phase |
|---|---------|----------|-------|
| 1.1 | Network timeout during puzzle solve | Medium | MVP |
| 1.2 | Failed score submission | High | MVP |
| 1.3 | Failed group join (error states) | Medium | MVP |
| 1.4 | Failed group creation | Medium | MVP |
| 1.5 | Failed account conversion (OAuth errors, email conflict) | High | MVP |
| 1.6 | Failed puzzle fetch (no cache, no network) | High | MVP |
| 1.7 | Server-side validation rejection | Medium | MVP |
| 2.1 | 0 groups empty state underspecified | Low | MVP |
| 2.2 | 0 solves stats empty state underspecified | Low | MVP |
| 2.3 | Expired/invalid invite code | Medium | MVP |
| 2.4 | Already-a-member join attempt | Low | MVP |
| 2.5 | User removed from group UX | Medium | MVP |
| 2.6 | Maximum groups reached | Low | Post-MVP |
| 2.7 | Hint edge case near completion | Low | MVP |
| 2.8 | Streak freeze already used this week | Medium | MVP |
| 2.9 | Anonymous user feature gates not enumerated | Medium | MVP |
| 3.1 | Deep link received during active puzzle | Medium | MVP |
| 3.2 | Back button during celebration animation | Low | MVP |
| 3.3 | App backgrounded during celebration | Low | MVP |
| 3.4 | Navigation stack after multiple deep links | Low | Post-MVP |
| 3.5 | Tab switch while data loading | Low | MVP |
| 4.1 | Notification permission prompt timing/design | High | MVP |
| 4.2 | Camera permission for QR scanning | Low | MVP |
| 4.3 | Photo library permission for share card save | Low | MVP |
| 5.1 | Force update screen | Critical | MVP |
| 5.2 | Optional update prompt | Medium | Post-MVP |
| 5.3 | App store rating prompt | Low | Post-MVP |
| 6.1 | Splash/launch screen design | Medium | MVP |
| 6.2 | First-time progressive disclosure on puzzle screen | Medium | MVP |
| 6.3 | First completion differentiated experience | Low | MVP |
| 7.1 | Keyboard covering input fields | Medium | MVP |
| 7.2 | Input validation timing specification | Medium | MVP |
| 7.3 | Invite code input formatting | Low | MVP |
| 8.1 | Leaderboard staleness indicator threshold | Medium | MVP |
| 8.2 | Pull-to-refresh failure design | Low | MVP |
| 8.3 | Background data refresh policy | Low | Post-MVP |
| 9.1 | Same account on two devices | High | MVP |
| 9.2 | Session management across devices | Medium | Post-MVP |
| 10.1 | App killed during puzzle -- resume vs restart | High | MVP |
| 10.2 | Timer behavior when app backgrounded | Medium | MVP |
| 10.3 | State preservation across app update | Low | MVP |
| 11.1 | Offline transition during active puzzle play | Medium | MVP |
| 11.2 | Auto-refresh when connectivity returns | Low | MVP |
| 11.3 | Queued result sync notification | Low | MVP |
| 12.1 | Dark/light mode switch animation and system-follow behavior | Medium | MVP |
| 12.2 | Theme preference sync across devices | Low | MVP |
| 13.1 | iPad multitasking, pointer, keyboard support | Medium | Post-MVP |
| 13.2 | iPad Stage Manager support | Low | Post-MVP |
| 14.1 | Orientation lock policy (phone) | High | MVP |
| 14.2 | Tablet landscape layout | Medium | Post-MVP |
| 15.1 | Basic screen reader support for non-game UI deferred entirely | Critical | MVP |
| 15.2 | Dynamic type at extreme sizes layout breakage | Medium | MVP |
| 15.3 | Colorblind mode discoverability | Medium | MVP |
| 15.4 | Tap-to-select mode visual design | Medium | Post-MVP |
| 15.5 | Focus indicators for keyboard/switch navigation | Low | Post-MVP |
| 15.6 | Visual-only feedback for deaf users on haptic-less devices | Low | MVP |

---

## Critical and High Priority Summary

**Critical (2 findings -- must resolve before development):**
1. **5.1 -- Force update screen:** Without this, any breaking API change will brick the app for users who don't manually update. This is a day-one production requirement.
2. **15.1 -- Basic screen reader for non-game UI:** Deferring ALL screen reader support to post-MVP means blind users cannot use the app at all. At minimum, standard Material 3 navigation screens (Home, Groups, Stats, Profile) should have proper semantic labels at launch.

**High (7 findings -- must resolve before MVP launch):**
1. **1.2 -- Failed score submission:** The core loop ends in score submission. Its failure path must be designed.
2. **1.5 -- Failed account conversion:** Data loss risk if anonymous-to-account linking fails.
3. **1.6 -- Failed puzzle fetch with empty cache:** First impression destruction if this edge case hits.
4. **4.1 -- Notification permission prompt:** iOS gives one chance. Blowing it means no daily engagement notifications ever.
5. **9.1 -- Multi-device puzzle solve conflict:** "One attempt per day" must be enforced with clear UX across devices.
6. **10.1 -- App killed during puzzle:** Users will lose progress without state restoration, causing frustration.
7. **14.1 -- Orientation lock policy:** Without explicit specification, developers may ship an app that renders incorrectly in landscape.

---

