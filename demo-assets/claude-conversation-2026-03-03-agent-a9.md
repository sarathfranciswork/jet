# Claude Conversation Log

Session ID: agent-a9a2b4e7ceee33281
Date: 2026-03-03 00:43:00

---

## 👤 User

You need to append detailed epic and story sections to the file at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics.md

IMPORTANT: Another agent is writing Epics 1-4 to this same file. You should write Epics 5-8 to a TEMPORARY file at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics-5-8-temp.md so they can be merged later.

First read the main epics.md to understand the epic structure, FR coverage map, and requirements. Then write Epics 5 through 8 to the temp file.

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
- Create database tables/entities ONLY when needed

Here are the stories to generate:

## Epic 5: Sharing & Viral Growth

**Story 5.1: Spoiler-Free Share Card Generation**
FRs: FR45
- Render share card image (ZipPath logo, day identifier, grid size, abstract path visualization that does NOT reveal solution, solve time, "Can you beat my time?" CTA). Dark background card (280x380px). Generated via RepaintBoundary + toImage. Cached for repeated sharing.

**Story 5.2: Share & Copy Actions**
FRs: FR46, FR47
- Share generated image via native OS share sheet (share_plus). Copy result as formatted text to clipboard. Success SnackBar feedback.

**Story 5.3: Group Invite Sharing & Deep Links**
FRs: FR48, FR61, FR101
- Share group invite via: deep link (https://zippath.app/join/{code}), invite code text, QR code image. Deep links open app to group join flow. If app not installed, redirect to App Store/Play Store. Handle deep link failures: deleted group, malformed URL, expired code → informative error screen with "Go to Home" button.

## Epic 6: Offline Play & Multi-Device Sync

**Story 6.1: Offline Puzzle Caching & Fallback Puzzles**
FRs: FR49, FR52
- Background fetch caches tomorrow's puzzle 12h+ before release in Hive. 7 fallback puzzles bundled in app binary (assets/puzzles/fallback_puzzles.json) for first-launch offline. Cache eviction via LRU when limit reached.

**Story 6.2: Offline Puzzle Play & UI Indicators**
FRs: FR50, FR53, FR107
- Full puzzle gameplay works offline (all FR1-FR11 features). Offline indicator on non-game screens (home, groups, stats). Offline banner SUPPRESSED during active puzzle play to preserve flow state. Result screen shows "Will sync when online" instead of percentile/rank when offline.

**Story 6.3: Automatic Sync & Score Recovery**
FRs: FR51, FR98
- Offline results queued in Hive sync queue. Auto-sync on connectivity return with exponential backoff (initial 1s, max 30s, 5 retries). Score submission failure recovery: result screen shows "Score pending" with manual retry button. Failed items flagged in local storage after max retries.

**Story 6.4: Multi-Device Enforcement & Session Sync**
FRs: FR85, FR86
- One puzzle attempt per day across devices: first server-verified solve is the recorded attempt. Subsequent attempts on other devices show "already solved" state with existing result. Concurrent session sync: streaks, stats, group memberships consistent across devices via Supabase real-time and pull-based refresh.

## Epic 7: Notifications & Engagement

**Story 7.1: Push Notification Infrastructure & Permission Flow**
FRs: FR88
- Firebase Cloud Messaging setup. Pre-permission screen after first puzzle completion explaining value ("Get daily puzzle reminders and group updates") with "Enable" and "Not Now" buttons. Only trigger OS permission dialog if user taps Enable. Store permission state. FCM topic subscriptions (daily_puzzle, group_{id}).

**Story 7.2: Daily Puzzle Reminder Notification**
FRs: FR89
- Send notification at user-configurable time (default 8:00 AM local): "Today's ZipPath is ready — [day] [grid_size]". Tap opens app to puzzle screen. Only sent if user hasn't solved today.

**Story 7.3: Group Activity & Streak Alert Notifications**
FRs: FR90, FR91
- Group nudge: "You're the last one! N/M members have solved today's puzzle" when applicable (only to unsolved members). Streak alert: "Solve today to keep your N-day streak!" if not solved by configurable time (default 6:00 PM local). Deep link in notification data for direct navigation.

**Story 7.4: Notification Preferences & In-App Badges**
FRs: FR57, FR92, FR93
- Settings: per-group notification toggle (on/off), notification type filtering (daily reminder, group activity, streak alerts — each independently toggleable). In-app badge on Groups tab when new group activity since last visit. Badge clears on Groups tab visit.

**Story 7.5: App Store Rating Prompt**
FRs: FR95
- Trigger in-app review API (StoreKit on iOS, Play In-App Review on Android) after 5th puzzle completion OR 7-day streak milestone. Max once per 90 days. Track last prompt date in SharedPreferences. Never show if user has already rated.

## Epic 8: Content Moderation & Safety

**Story 8.1: Content Filtering & Input Sanitization**
FRs: FR79, FR80
- Profanity filter: configurable word list checked on display name set/update and group name create/update. Reject with "Name contains prohibited content" error. Input sanitization: strip HTML tags, prevent SQL injection patterns, normalize Unicode (remove excessive combining marks, invisible characters, zalgo), reject emoji-only names. Applied both client-side (immediate feedback) and server-side (Edge Function validation).

**Story 8.2: In-App Reporting Mechanism**
FRs: FR81
- Report button on group member profiles and group detail screens. Report types: "Offensive display name", "Offensive group name", "Abusive behavior", "Other". Report stored in reports table (reporter_id, reported_user_id, report_type, description, created_at, status). Confirmation: "Report submitted. We'll review it within 48 hours."

**Story 8.3: User Ban System**
FRs: FR83
- System-level ban: banned users cannot create accounts, join groups, or submit scores. Ban enforced at auth layer (login rejected) and Edge Function layer (requests rejected with 403). Ban flag on profiles table (is_banned BOOLEAN). Admin tooling via Supabase dashboard for ban management.

**Story 8.4: Data Lifecycle Management**
FRs: FR104, FR105
- Automated purge: anonymous users with no activity for 90 days have their data deleted (scheduled Edge Function or database cron). Deleted account anonymization: leaderboard entries display "Deleted User" with anonymized avatar instead of removing historical scores from group leaderboards.

IMPORTANT: Write the full epic header and all stories with complete acceptance criteria in Given/When/Then format. Each story needs 3-6 independently testable acceptance criteria. This is the actual implementation specification that developers will follow.

---

## 🤖 Claude



I'll start by reading the main epics.md file to understand the structure, FR coverage map, and requirements.

---

## 🤖 Claude

Let me read the file in chunks to understand the full structure.

---

## 🤖 Claude

Now I have a thorough understanding of the full document structure, the FR definitions, the coverage map, and the epic summaries. Let me also look at the existing stories in the file to see if Epics 1-4 have already been written, so I can match the exact format.

---

## 🤖 Claude

Good -- the file ends at line 578 with just the epic summaries. No detailed stories have been written yet. Now I have all the information I need to write Epics 5-8 with full story details to the temporary file.

Let me also check the architecture doc for any specific database table schemas that I should reference in the stories.

---

## 🤖 Claude

Now I have all the context I need. Let me also quickly check the profiles table schema to understand what fields exist.

---

## 🤖 Claude

Now I have comprehensive understanding. Let me create the temporary file with Epics 5-8.

---

## 🤖 Claude

Now let me verify the file was written correctly by doing a quick check on the structure.

---

## 🤖 Claude

Let me also verify the acceptance criteria counts per story to make sure each has 3-6 criteria.

---

## 🤖 Claude

Let me do a quick count of acceptance criteria per story to validate:

---

## 🤖 Claude

All 16 stories have between 4-6 acceptance criteria each, meeting the requirement of 3-6 per story. Let me also verify FR coverage.

---

## 🤖 Claude

All 29 FRs are covered with zero missing and zero extra. Let me mark the task complete.

---

## 🤖 Claude

The temporary file has been written successfully at `/Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics-5-8-temp.md`. Here is a summary of what was generated:

## Summary

**File:** `/Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics-5-8-temp.md`
**Total lines:** 582
**Total stories:** 16 across 4 epics

### Epic 5: Sharing & Viral Growth (3 stories)
- **Story 5.1: Spoiler-Free Share Card Generation** (5 AC) -- FR45 -- RepaintBoundary + toImage rendering, 280x380px dark card, abstract path visualization, caching, timeout handling
- **Story 5.2: Share & Copy Actions** (5 AC) -- FR46, FR47 -- Native share sheet via share_plus, clipboard copy as formatted text, SnackBar feedback, graceful fallback on image generation failure
- **Story 5.3: Group Invite Sharing & Deep Links** (6 AC) -- FR48, FR61, FR101 -- Three sharing options (deep link, code, QR), GoRouter deep link handling, app store redirect for non-installed users, error screens for deleted/malformed/expired links

### Epic 6: Offline Play & Multi-Device Sync (4 stories)
- **Story 6.1: Offline Puzzle Caching & Fallback Puzzles** (5 AC) -- FR49, FR52 -- Background fetch 12h+ ahead, 7 bundled fallback puzzles in assets/puzzles/fallback_puzzles.json, LRU cache eviction, retry on fetch failure
- **Story 6.2: Offline Puzzle Play & UI Indicators** (5 AC) -- FR50, FR53, FR107 -- Full gameplay offline (all FR1-FR11 features), offline banner on non-game screens, banner suppressed during puzzle play, "Will sync when online" on result screen
- **Story 6.3: Automatic Sync & Score Recovery** (5 AC) -- FR51, FR98 -- Hive sync queue, exponential backoff (1s initial, 30s max, 5 retries), "Score pending" with manual retry, auto-retry on app launch
- **Story 6.4: Multi-Device Enforcement & Session Sync** (6 AC) -- FR85, FR86 -- One attempt per day across devices, "already solved" state on second device, pull-based refresh for streaks/stats/groups, Supabase Realtime for live leaderboard updates

### Epic 7: Notifications & Engagement (5 stories)
- **Story 7.1: Push Notification Infrastructure & Permission Flow** (6 AC) -- FR88 -- FCM setup, pre-permission screen after first puzzle, conditional OS dialog, FCM topic subscriptions per group
- **Story 7.2: Daily Puzzle Reminder Notification** (4 AC) -- FR89 -- Configurable time (default 8 AM), skip if already solved, deep link to puzzle on tap, time picker in settings
- **Story 7.3: Group Activity & Streak Alert Notifications** (5 AC) -- FR90, FR91 -- "Last one" group nudge, streak-at-risk alert at configurable time (default 6 PM), skip if solved, consolidated multi-group nudges
- **Story 7.4: Notification Preferences & In-App Badges** (6 AC) -- FR57, FR92, FR93 -- Three type toggles, per-group toggles, Groups tab badge on new activity, badge clears on visit
- **Story 7.5: App Store Rating Prompt** (4 AC) -- FR95 -- Trigger at 5th puzzle or 7-day streak, 90-day cooldown, native StoreKit/Play In-App Review API

### Epic 8: Content Moderation & Safety (4 stories)
- **Story 8.1: Content Filtering & Input Sanitization** (6 AC) -- FR79, FR80 -- Profanity filter on names, HTML/SQL/Unicode sanitization, client-side + server-side defense-in-depth, updatable word list
- **Story 8.2: In-App Reporting Mechanism** (6 AC) -- FR81 -- Report button on profiles and groups, 4 report types, `reports` table with RLS, duplicate prevention, 48-hour review confirmation
- **Story 8.3: User Ban System** (5 AC) -- FR83 -- `is_banned` boolean on profiles, login rejection, Edge Function 403 enforcement, account-level scoping (not device-level)
- **Story 8.4: Data Lifecycle Management** (5 AC) -- FR104, FR105 -- 90-day anonymous user purge via pg_cron, "Deleted User" anonymization on leaderboards, transactional purge with error handling

### FR Coverage Verification
All 29 expected FRs (FR45-FR48, FR49-FR53, FR57, FR61, FR79-FR81, FR83, FR85-FR86, FR88-FR93, FR95, FR98, FR101, FR104-FR105, FR107) are covered with zero gaps and zero extras.

---

