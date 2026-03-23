# Claude Conversation Log

Session ID: agent-a4d5d4b3863793162
Date: 2026-03-03 00:42:18

---

## 👤 User

You need to append detailed epic and story sections to the file at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics.md

Read the current file first to understand the epic structure, FR coverage map, and requirements. Then APPEND (do not overwrite existing content) the following epic sections right after the last line of the file.

Generate stories for Epics 1 through 4 using EXACTLY this format for each story:

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
- NOT depend on future stories (only on previous stories within same epic)
- Create database tables/entities ONLY when the story needs them

Here are the stories to generate:

## Epic 1: App Foundation & User Identity

**Story 1.1: Flutter Project Initialization & App Shell**
User launches app, sees splash screen, navigates via bottom tabs, selects theme.
FRs: FR71, FR59, FR56, FR72, FR125
- Creates: Flutter project scaffold (PLAN.md Section 12 structure), core dependencies (Riverpod, GoRouter, Supabase SDK, Firebase SDK), splash screen, bottom navigation (Home/Groups/Stats/Profile tabs), theme system (light/dark/system with 300ms cross-fade), orientation lock to portrait on phones. Database: profiles table, Supabase project init with .env config.

**Story 1.2: Legal Consent & Age Verification Gate**
First-launch legal compliance flows.
FRs: FR62, FR63, FR64
- Age verification gate (13+) before any data collection, privacy consent flow with granular opt-in/opt-out for analytics/crash/personalization, Apple ATT prompt on iOS before tracking.

**Story 1.3: Anonymous Authentication**
User plays immediately without account.
FRs: FR20
- Silent anonymous auth on first app launch via Supabase Auth, user gets a session without seeing any auth UI, anonymous flag stored in profiles table.

**Story 1.4: Account Creation with Social Sign-In**
User creates an account with email, Google, or Apple.
FRs: FR21, FR65
- Email/password registration, Google Sign-In, Apple Sign-In, active ToS acceptance required before account creation, proper error handling for all auth methods.

**Story 1.5: Anonymous-to-Account Linking & Conversion Prompt**
Anonymous user upgrades to full account preserving all data.
FRs: FR22, FR27
- Link anonymous session to new account via Supabase linkIdentity/updateUser, preserve streaks/stats/groups, prompt at 3rd solve or group join attempt via bottom sheet (dismissible).

**Story 1.6: Profile Management**
User manages their identity.
FRs: FR23, FR24, FR25, FR26
- Set display name (max 20 chars), select from preset avatars, update at any time, delete account with 30-day grace period and confirmation dialog.

**Story 1.7: Settings & Preferences**
User configures app settings.
FRs: FR54, FR55, FR58, FR108, FR109, FR110, FR123
- Haptic feedback toggle, sound effects toggle, view privacy policy and ToS, localization framework (intl/ARB) for all strings, locale-aware date/time/number formatting, RTL-ready layout infrastructure (EdgeInsetsDirectional), keyboard scroll handling for all input fields.

## Epic 2: Core Puzzle Gameplay

**Story 2.1: Puzzle Grid Rendering**
User sees the puzzle grid with all visual elements.
FRs: FR1
- CustomPainter renders grid cells, numbered waypoint circles (coral-orange), wall barriers (thick lines between cells), empty cells distinct from filled. Respects current theme. Adapts to screen size via `(screen_width - 48px) / columns`.

**Story 2.2: Path Drawing with Touch Gestures**
User draws path by dragging finger.
FRs: FR2, FR8
- GestureDetector handles drag events, translates screen coordinates to grid cells, validates adjacency, enforces wall barriers, waypoint order, continuous path, draws blue fill (#3B82F6) with glow effect, current cell highlight.

**Story 2.3: Path Undo, Redo & Reset**
User corrects mistakes while solving.
FRs: FR3, FR4, FR5, FR6, FR7
- Drag backward undoes segments (smooth fade), undo button removes last segment, redo button restores undone segment, reset clears entire path (with confirmation), tap on drawn cell truncates from that point to end.

**Story 2.4: Puzzle Completion & Celebration**
User completes the puzzle and sees results.
FRs: FR9, FR10, FR14
- Detect completion (all cells filled + waypoints in order), celebration animation (800ms: 200ms grid ripple + 600ms confetti), reduced motion variant (simple glow), display solve time in large monospace, result screen with percentile placeholder.

**Story 2.5: Haptic Feedback & Sound Effects**
User feels and hears the game.
FRs: FR11, FR126
- 7 haptic patterns (cellEntry, waypointReached, wallCollision, puzzleComplete, hintUsed, buttonTap, streakMilestone) with iOS/Android implementations. Sound effects (soft tick, chime, thud, fanfare). Both respect toggle settings from FR54/FR55.

**Story 2.6: Hint System**
User gets help when stuck.
FRs: FR17, FR18, FR19
- Hint button reveals correct next 2-3 cells with glow animation, 3 free hints/day (midnight UTC reset), hint count badge on button, track hints used per attempt, "No hints remaining" state when exhausted, hint cells animate into place.

**Story 2.7: Puzzle State Auto-Save & Timer Management**
User's progress survives interruptions.
FRs: FR69, FR70
- Auto-save path, hints used, undos used, elapsed time to Hive on every move (<5ms non-blocking). Timer pauses when app backgrounded, resumes on foreground. On next launch, detect saved state and offer resume.

**Story 2.8: First-Time Affordances & Tap-to-Select Mode**
New users learn naturally; accessible input for all.
FRs: FR94, FR113
- First play: pulsing indicator on waypoint 1, "Drag to draw your path" tooltip (auto-dismiss after first drag). Tap-to-select mode: toggle in puzzle settings, tap adjacent cells one-at-a-time to build path. Both persist in user preferences.

## Epic 3: Daily Challenge, Streaks & Statistics

**Story 3.1: Daily Puzzle Delivery & Difficulty Scaling**
User gets a fresh puzzle every day.
FRs: FR12, FR13, FR76
- Fetch puzzle by UTC date from Supabase puzzles table, difficulty Mon(5x5) through Sun(8x8), midnight UTC rollover. Display day/difficulty on home screen. Database: puzzles table (id, puzzle_date UNIQUE, grid_width, grid_height, day_of_week, difficulty, waypoints JSONB, walls JSONB, solution_path JSONB).

**Story 3.2: Server-Side Puzzle Pre-Generation**
Puzzles are always ready 30 days ahead.
FRs: FR15
- Edge Function (daily-puzzle) runs on cron schedule, implements Backbite algorithm for Hamiltonian path generation, generates all grid sizes (5x5 through 8x8), stores in puzzles table with solution_path (never sent to client), 30-day buffer maintained.

**Story 3.3: Client-Side Puzzle Pre-Caching**
Tomorrow's puzzle is always ready on device.
FRs: FR16
- Background fetch caches next day's puzzle in Hive 24h before release, puzzle data excludes solution_path, cache includes waypoints + walls + grid dimensions, handles fetch failure gracefully with on-demand fetch at launch.

**Story 3.4: Score Submission & Server Validation**
User's solve is verified and recorded.
FRs: FR14 (submission), FR8 (server validation)
- Edge Function (submit-score): receives path + time + hints + undos, re-validates path against stored solution, checks timing (>3s minimum per NFR11), rate limit (10/hr per NFR10), records in puzzle_attempts table. Database: puzzle_attempts table (id, user_id, puzzle_id, puzzle_date, solve_time_ms, hints_used, undos_used, completed, verified, UNIQUE(user_id, puzzle_date)).

**Story 3.5: Streak Tracking & Freeze System**
User maintains their streak.
FRs: FR28, FR29, FR31, FR32, FR78
- Track current streak and longest-ever streak in streaks table. Evaluate at midnight UTC. Auto-apply streak freeze if missed day and freeze available (1/week). Database: streaks table (user_id PK, current_streak, longest_streak, last_solve_date, streak_freezes_remaining).

**Story 3.6: Statistics Screen**
User views their performance history.
FRs: FR30, FR33
- Dedicated stats screen showing: total puzzles solved, average solve time, solve time distribution chart, streak calendar heatmap, hints usage stats. Pulls from puzzle_attempts aggregation.

**Story 3.7: Home Screen Hub**
User sees their daily engagement dashboard.
FRs: FR60, FR77
- Home screen: DailyPuzzleCard (grid size, difficulty, play/solved state), StreakCounter (fire icon, current count, at-risk/frozen states), group activity summary (if in groups). Weekly leaderboard boundary displayed as Mon-Sun UTC.

**Story 3.8: Welcome Back Experience**
Returning users are re-engaged.
FRs: FR97
- Detect 7+ days of inactivity, show welcome back card on home screen with last streak status, "Start fresh" encouragement, gentle re-onboarding.

## Epic 4: Groups & Leaderboards

**Story 4.1: Group Creation & Invite Code Generation**
User creates a group for friends/coworkers.
FRs: FR34, FR35, FR82
- Create group form (name max 30 chars, optional description), generate unique 6-char alphanumeric invite code, rate limit 5 groups/day/user. Database: groups table (id, name, description, invite_code UNIQUE, created_by, max_members DEFAULT 50). Database: group_members table (group_id + user_id composite PK, role 'admin'|'member', joined_at).

**Story 4.2: Group Joining (Code, Deep Link, QR Scan)**
User joins groups via multiple methods.
FRs: FR36, FR37, FR100, FR124
- Join via: manual code entry (auto-uppercase, 6-char limit), deep link (/join/{code}), QR code scan (camera permission). Validate: membership limit (50), not already member. Error states: "Code not found", "Code expired", "Group is full", "Already a member". Edge Function: join-group.

**Story 4.3: Daily Group Leaderboard**
Users compete on today's puzzle.
FRs: FR38, FR44, FR106
- Daily leaderboard ranked by hints_used ASC → solve_time_ms ASC → undos_used ASC. Show solved members with rank/time/hints. Show unsolved members as "Hasn't solved yet" (only after viewer has solved). Data staleness indicator ("Updated N min ago"). Database RPC: get_group_daily_leaderboard. Real-time subscription for live updates.

**Story 4.4: Weekly Group Leaderboard**
Users see weekly standings.
FRs: FR39
- Weekly tab ranked by puzzles_completed DESC → avg_solve_time ASC. Weekly boundary Mon 00:00 - Sun 23:59 UTC. Database RPC: get_group_weekly_leaderboard.

**Story 4.5: Group Admin Controls**
Admins manage their groups.
FRs: FR40, FR41, FR43
- Remove member (confirmation dialog), regenerate invite code (invalidates old code, confirmation), delete group entirely (confirmation with "this cannot be undone").

**Story 4.6: Group Membership Management**
Users manage their group participation.
FRs: FR42, FR84
- Leave group (confirmation dialog). Admin succession: when admin deletes account, role transfers to longest-tenured member; if no members remain, group is deleted.

Use the Edit tool to append content after the last line in the file. Make sure all stories follow the exact Given/When/Then acceptance criteria format with 3-6 criteria per story. Each AC should be independently testable.

IMPORTANT: Write the full epic header and all stories with complete acceptance criteria. Do not use placeholders or abbreviations. This is the actual implementation specification that developers will follow.

---

## 🤖 Claude



Let me start by reading the current file to understand its structure and content.

---

## 🤖 Claude

Let me read the full file to see the complete content, especially the end.

---

## 🤖 Claude

Now I have the full picture. The file is 577 lines long, ending at line 576 with `NFR32 (alerting)` and line 577 is likely empty or the last line. Let me now append the detailed story sections for Epics 1 through 4.

---

## 🤖 Claude

Good. The file ends at line 578 with an empty line after "Dependencies: Epic 1 (auth, app shell)". Now I will append the detailed epic story sections after line 577.

---

## 🤖 Claude

The string appears twice. Let me use more context to make it unique.

---

## 🤖 Claude

Let me verify the file was updated correctly by checking the end of the file.

---

## 🤖 Claude

The file has been successfully updated. The content was appended correctly, starting at line 579 (after the existing Epic 11 content) and ending at line 1591. Let me provide a summary of what was added.

---

The detailed epic stories for Epics 1 through 4 have been appended to `/Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/epics.md`. The file grew from 577 lines to 1591 lines (1014 lines added).

Here is what was added:

**Epic 1: App Foundation & User Identity -- 7 Stories**
- **Story 1.1** (FR71, FR59, FR56, FR72, FR125): Flutter project scaffold, splash screen, bottom tabs, theme system, orientation lock, profiles table
- **Story 1.2** (FR62, FR63, FR64): Age verification gate (13+), privacy consent flow, Apple ATT prompt
- **Story 1.3** (FR20): Silent anonymous authentication via Supabase Auth
- **Story 1.4** (FR21, FR65): Email/Google/Apple sign-in with ToS acceptance
- **Story 1.5** (FR22, FR27): Anonymous-to-account linking via linkIdentity/updateUser, conversion prompt at 3rd solve or group join
- **Story 1.6** (FR23, FR24, FR25, FR26): Display name, avatar selection, account deletion with 30-day grace
- **Story 1.7** (FR54, FR55, FR58, FR108, FR109, FR110, FR123): Haptic/sound toggles, legal docs, localization framework, RTL infrastructure, keyboard handling

**Epic 2: Core Puzzle Gameplay -- 8 Stories**
- **Story 2.1** (FR1): CustomPainter grid rendering with waypoints, walls, theme support, responsive sizing
- **Story 2.2** (FR2, FR8): GestureDetector path drawing, adjacency/wall/waypoint validation
- **Story 2.3** (FR3, FR4, FR5, FR6, FR7): Drag-backward undo, undo/redo buttons, reset with confirmation, tap-to-truncate
- **Story 2.4** (FR9, FR10, FR14): Completion detection, 800ms celebration animation, reduced motion variant, result screen
- **Story 2.5** (FR11, FR126): 7 haptic patterns with iOS/Android implementations, 4 sound effects, toggle respect
- **Story 2.6** (FR17, FR18, FR19): Hint reveals 2-3 cells, 3/day limit with midnight UTC reset, hint tracking
- **Story 2.7** (FR69, FR70): Auto-save to Hive (<5ms), timer pause/resume on background/foreground, crash recovery
- **Story 2.8** (FR94, FR113): Pulsing waypoint 1 + tooltip for first play, tap-to-select alternative input mode

**Epic 3: Daily Challenge, Streaks & Statistics -- 8 Stories**
- **Story 3.1** (FR12, FR13, FR76): Daily puzzle fetch by UTC date, Mon(5x5)-Sun(8x8) scaling, puzzles table schema
- **Story 3.2** (FR15): Edge Function with Backbite algorithm, 30-day buffer, cron schedule, retry/alerting
- **Story 3.3** (FR16): Background fetch pre-caching to Hive, on-demand fallback, stale cache replacement
- **Story 3.4** (FR14, FR8): submit-score Edge Function, server-side path re-validation, puzzle_attempts table, rate limiting
- **Story 3.5** (FR28, FR29, FR31, FR32, FR78): streaks table, streak increment/reset logic, auto-freeze, weekly freeze reset
- **Story 3.6** (FR30, FR33): Stats screen with totals, averages, distribution chart, streak heatmap, hint stats
- **Story 3.7** (FR60, FR77): Home screen DailyPuzzleCard, StreakCounter, group activity summary, weekly boundary
- **Story 3.8** (FR97): Welcome back card for 7+ days inactive, messaging variants, 6-day threshold exclusion

**Epic 4: Groups & Leaderboards -- 6 Stories**
- **Story 4.1** (FR34, FR35, FR82): Group creation form, groups/group_members tables, 6-char invite code, 5/day rate limit
- **Story 4.2** (FR36, FR37, FR100, FR124): Join via code entry (auto-uppercase), deep link, QR scan, join-group Edge Function, error states
- **Story 4.3** (FR38, FR44, FR106): Daily leaderboard (hints->time->undos), spoiler-free states, staleness indicator, real-time subscription
- **Story 4.4** (FR39): Weekly leaderboard (completed->avg time), Mon-Sun UTC boundary, RPC function
- **Story 4.5** (FR40, FR41, FR43): Admin remove member, regenerate invite code, delete group, all with confirmations
- **Story 4.6** (FR42, FR84): Leave group, admin succession to longest-tenured member, auto-delete empty groups

Each story follows the exact Given/When/Then format with 3-6 independently testable acceptance criteria, references the FRs it covers, and creates database tables only when the story requires them.

---

