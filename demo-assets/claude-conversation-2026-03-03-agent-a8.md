# Claude Conversation Log

Session ID: agent-a8227a8d446c1b4f0
Date: 2026-03-03 00:02:52

---

## 👤 User

Read the full PRD at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/prd.md and identify ANY production-readiness gaps. Specifically look for:

1. Missing error handling requirements (what happens when things fail?)
2. Missing edge cases in user journeys (what if user has no internet on first launch? what if puzzle generation fails?)
3. Missing data management requirements (data export, GDPR compliance beyond deletion?)
4. Missing security requirements (brute force protection on invite codes? session management?)
5. Missing app lifecycle requirements (app backgrounding during puzzle, force update mechanism, maintenance mode?)
6. Missing onboarding/tutorial requirements
7. Missing notification requirements beyond basic push
8. Missing analytics/tracking requirements for product decisions
9. Missing moderation/abuse prevention (offensive display names, group name moderation?)
10. Missing monetization infrastructure (even if free, any foundation needed?)
11. Missing app store requirements (rating prompts, review handling?)
12. Missing legal/compliance (age gating, COPPA, privacy consent flows?)
13. Missing migration/versioning requirements (what happens when schema changes?)
14. Missing timezone handling requirements
15. Missing localization/i18n infrastructure

Report ALL findings as a categorized list with severity (Critical/High/Medium/Low) and whether each is MVP or post-MVP.

---

## 🤖 Claude



I'll start by reading the full PRD document.

---

## 🤖 Claude

The file is 409 lines. Now let me also check if there are any other related planning documents to understand the full context.

---

## 🤖 Claude

Let me also read the architecture doc and PLAN.md for additional context on what's been specified elsewhere.

---

## 🤖 Claude

Now let me read the epics and UX specification for additional context.

---

## 🤖 Claude

Now I have a thorough understanding of the PRD and its supporting documents. Let me compile the comprehensive gap analysis.

---

# ZipPath PRD Production-Readiness Gap Analysis

Below is a categorized audit of every production-readiness gap identified in `/Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/prd.md`. Each finding includes its severity, whether it is needed for MVP or post-MVP, and a brief explanation.

---

## 1. Missing Error Handling Requirements

**1.1 No error states defined for puzzle loading failure**
- Severity: **Critical**
- Phase: **MVP**
- The PRD specifies performance targets for puzzle loading (FR3/NFR3, NFR4) and bundled fallback puzzles (FR52) but never defines what the user sees when a network puzzle fetch fails and no cache exists beyond the 7 bundled puzzles. What happens on day 8+ if the user has never connected? What is the error UI? Is there a retry mechanism?

**1.2 No error handling for score submission failure**
- Severity: **Critical**
- Phase: **MVP**
- FR51 mentions offline queuing and automatic sync, but there is no requirement for what happens when the server rejects a submission (e.g., anti-cheat rejection per NFR11, server-side validation failure, rate limit hit per NFR10). Does the user get notified? Is the solve still shown locally? Is there an appeal path?

**1.3 No error handling for authentication failures**
- Severity: **High**
- Phase: **MVP**
- FR20-FR22 cover anonymous play and account linking, but there is no requirement for what happens when Google/Apple Sign-In fails, when account linking fails due to a conflict, when token refresh fails, or when the anonymous session expires server-side.

**1.4 No error handling for group operations**
- Severity: **High**
- Phase: **MVP**
- FR34-FR43 describe group CRUD, but there is no requirement for: invalid invite code entry, expired/regenerated invite code (user journey 5 mentions regeneration but not the error the old-link user sees), group full (50 members), or attempting to join a group you were removed from.

**1.5 No error handling for deep link failures**
- Severity: **High**
- Phase: **MVP**
- FR61 mentions deep link support, but no requirement covers: malformed deep link, deep link to a deleted group, deep link to a group the user was banned from, or universal link fallback behavior.

**1.6 No error handling for puzzle pre-generation failure**
- Severity: **High**
- Phase: **MVP**
- FR15 requires 30-day pre-generation via server-side scheduled function, but there is no requirement for: alerting if generation fails, fallback if tomorrow's puzzle is missing, or monitoring/retry strategy.

**1.7 No error handling for background fetch failure**
- Severity: **Medium**
- Phase: **MVP**
- NFR22 requires 95% cache refresh success, but no requirement defines what happens in the 5% failure case. Does the app fetch on-demand at launch? Is the user notified?

**1.8 No error handling for hint computation failure**
- Severity: **Medium**
- Phase: **MVP**
- FR17 says hints reveal the correct next 2-3 cells. If the hint calculation fails (e.g., user is in an unsolvable state), what happens? Is there a "no hint available" state?

---

## 2. Missing Edge Cases in User Journeys

**2.1 No journey for first launch with no internet**
- Severity: **High**
- Phase: **MVP**
- FR52 bundles 7 fallback puzzles, but there is no user journey describing this experience. Can the user create an anonymous session offline? How do streaks work with bundled puzzles? What leaderboard data is shown? How does the app behave when it reconnects for the first time?

**2.2 No journey for mid-puzzle app termination**
- Severity: **High**
- Phase: **MVP**
- None of the FRs address saving puzzle progress. If the user closes the app mid-solve, is the partial path preserved? Is the timer paused? This is critical for a timed game.

**2.3 No journey for timezone-crossing user**
- Severity: **High**
- Phase: **MVP**
- FR12 says one puzzle per day for all users worldwide, but there is no requirement defining when "today" rolls over for the user. Is it midnight UTC? Midnight local? What if a user travels across time zones mid-day? The architecture mentions `timezone` in the profiles table but the PRD never specifies the behavior.

**2.4 No journey for user who already solved trying to view puzzle again**
- Severity: **Medium**
- Phase: **MVP**
- After solving, can the user view their completed path? Replay their solve? Or is the puzzle screen locked? The PRD is silent on post-solve puzzle screen state.

**2.5 No journey for multiple device usage**
- Severity: **Medium**
- Phase: **MVP**
- What happens if a user plays on two devices? Can they start on one and finish on another? If they solve on device A while offline and solve on device B while online, which solve wins?

**2.6 No journey for user who runs out of bundled offline puzzles**
- Severity: **Medium**
- Phase: **MVP**
- After 7 days offline (consuming all bundled puzzles), what happens on day 8?

**2.7 No journey for group admin leaving/deleting account**
- Severity: **Medium**
- Phase: **MVP**
- FR43 says admins can delete groups, but what happens if the sole admin deletes their account (FR26)? Is admin transferred? Does the group become orphaned?

---

## 3. Missing Data Management Requirements

**3.1 No data export/portability requirement**
- Severity: **High**
- Phase: **MVP** (required by GDPR Article 20)
- FR26 covers account deletion with a 30-day grace period, but there is no requirement for data portability/export. GDPR requires the right to data portability, not just deletion. Users should be able to export their solve history, streak data, and group membership data.

**3.2 No data retention policy for anonymous users**
- Severity: **High**
- Phase: **MVP**
- FR20 allows anonymous play, but there is no requirement for how long anonymous user data is retained. What if an anonymous session is abandoned? Is stale anonymous data ever purged?

**3.3 No backup/disaster recovery requirements**
- Severity: **High**
- Phase: **MVP**
- No requirement specifies database backup frequency, RPO (recovery point objective), or RTO (recovery time objective). For a game with streaks, losing even one day of data could destroy user trust.

**3.4 No requirement for data minimization**
- Severity: **Medium**
- Phase: **MVP**
- The PRD does not specify what data is collected beyond functional requirements. GDPR's data minimization principle requires explicit documentation of what is collected and why.

**3.5 No requirement for account deletion cascade behavior**
- Severity: **Medium**
- Phase: **MVP**
- FR26 says 30-day grace period, but does not specify what happens to the user's leaderboard entries, group memberships, or whether their scores are anonymized or deleted from group histories.

---

## 4. Missing Security Requirements

**4.1 No brute force protection on invite codes**
- Severity: **Critical**
- Phase: **MVP**
- FR35 specifies 6-character alphanumeric invite codes. That is only ~2.18 billion combinations (36^6). With no rate limiting on join attempts, an attacker could enumerate valid codes and join private groups. There is rate limiting on score submissions (NFR10) but none on group join attempts.

**4.2 No session management requirements**
- Severity: **High**
- Phase: **MVP**
- No requirement specifies: maximum concurrent sessions, session timeout duration, forced logout capability, or what happens when a token is compromised. The architecture mentions JWT token refresh but the PRD has no requirements around session lifecycle.

**4.3 No input validation requirements for user-generated content**
- Severity: **High**
- Phase: **MVP**
- FR23 (display name, max 20 chars) and FR34 (group name, max 30 chars) specify length limits but no content validation: no profanity filter, no Unicode abuse prevention (zalgo text, invisible characters), no SQL/XSS injection prevention requirement, no emoji/special character policy.

**4.4 No abuse prevention for group creation**
- Severity: **Medium**
- Phase: **MVP**
- No limit on how many groups a single user can create. An attacker could spam thousands of groups consuming database resources.

**4.5 No requirement for secure puzzle delivery**
- Severity: **Medium**
- Phase: **MVP**
- NFR9 says solution paths are never transmitted to the client, but there is no requirement preventing a sophisticated attacker from intercepting puzzle data (waypoints + walls) and running a solver locally to get the answer before starting the timer. Certificate pinning, obfuscation, or timing-start-on-server are not mentioned.

**4.6 No requirement for API key/secret management**
- Severity: **Medium**
- Phase: **MVP**
- No requirement for how Supabase keys, Firebase keys, and other credentials are managed in the app binary. These are extractable from APK/IPA files if not properly handled.

---

## 5. Missing App Lifecycle Requirements

**5.1 No requirement for app backgrounding during active puzzle**
- Severity: **Critical**
- Phase: **MVP**
- When a user backgrounds the app mid-puzzle (phone call, notification, switching apps), what happens to the timer? Is the puzzle state saved? On resume, does the timer continue from where it was, or does it include background time? This directly affects fairness of leaderboard rankings.

**5.2 No force update mechanism**
- Severity: **Critical**
- Phase: **MVP**
- No requirement for forcing users to update when a critical bug is found or when the backend API changes. Without this, old clients could submit malformed data or miss security patches. Firebase Remote Config is mentioned in PLAN.md but not as a PRD requirement.

**5.3 No maintenance mode requirement**
- Severity: **High**
- Phase: **MVP**
- No requirement for what happens during server maintenance or outages. Is there a server status check? A maintenance screen? Graceful degradation to offline mode?

**5.4 No app state restoration requirement**
- Severity: **High**
- Phase: **MVP**
- No requirement for restoring app state after the OS kills the app in the background (common on Android). The user might lose their mid-puzzle progress.

**5.5 No requirement for handling clock manipulation**
- Severity: **High**
- Phase: **MVP**
- For a game that depends on daily puzzle timing and solve duration, there is no requirement for detecting or handling device clock manipulation. A user could set their clock forward to get tomorrow's puzzle early, or manipulate the system clock to fake a faster solve time.

---

## 6. Missing Onboarding/Tutorial Requirements

**6.1 No first-time user experience specification**
- Severity: **High**
- Phase: **MVP**
- The PRD says "no tutorial gate" and the UX spec says "onboarding without onboarding," but there is zero specification of how the user learns the rules. How does a user learn they must visit ALL cells (not just waypoints)? How do they learn about walls? The only mention of a tutorial is in "Growth Features (Post-MVP)" as an "Interactive onboarding tutorial." For a novel mechanic, this is a significant gap.

**6.2 No progressive disclosure specification**
- Severity: **Medium**
- Phase: **MVP**
- The UX spec mentions "progressive disclosure and affordances" but the PRD has no requirement for contextual tooltips, first-time feature highlights (e.g., first time seeing the hint button, first time completing a puzzle, first time seeing the share screen), or coach marks.

**6.3 No re-engagement onboarding for returning users**
- Severity: **Low**
- Phase: **Post-MVP**
- No requirement for how the app greets a user who returns after 30+ days of inactivity. Is the streak lost? Is there a "welcome back" flow?

---

## 7. Missing Notification Requirements

**7.1 No notification permission request strategy**
- Severity: **High**
- Phase: **MVP**
- Push notifications are mentioned (Journey 3, Growth Features) but there is no requirement for when and how the app requests notification permission. On iOS, you get one chance -- if the user declines, they must go to Settings to re-enable. The timing of this prompt is critical for opt-in rates.

**7.2 No notification content/frequency specification**
- Severity: **High**
- Phase: **MVP**
- "Push notification strategy" is listed as post-MVP in Growth Features, but Journey 3 (Sam) already shows push notifications in the MVP ("You're the last one!"). There is a contradiction. The MVP needs at least basic notification types defined: daily puzzle reminder, group activity nudge, streak at risk.

**7.3 No notification opt-out granularity**
- Severity: **Medium**
- Phase: **MVP**
- FR57 says "configure notification preferences per group" but does not address: global notification mute, quiet hours, notification type filtering (daily puzzle vs. group activity vs. streak reminders), or per-notification-type opt-out.

**7.4 No in-app notification/inbox requirement**
- Severity: **Medium**
- Phase: **Post-MVP**
- No requirement for in-app notifications (e.g., "3 friends solved today!" badge on Groups tab). All notifications appear to be push-only, which means users who decline push permissions miss all notifications entirely.

---

## 8. Missing Analytics/Tracking Requirements

**8.1 No analytics event taxonomy**
- Severity: **High**
- Phase: **MVP**
- The architecture document mentions Firebase Analytics, but the PRD has no specification of which events to track. For a product that lists specific success metrics (DAU/MAU, viral coefficient, D7/D30 retention, share rate), there needs to be a defined event taxonomy: puzzle_started, puzzle_completed, hint_used, share_tapped, group_created, group_joined, invite_sent, etc.

**8.2 No funnel tracking requirements**
- Severity: **High**
- Phase: **MVP**
- Success criteria include "complete first puzzle within 90 seconds" and "3+ puzzles in first week -> 40% D7 return," but there is no requirement for tracking the first-time user funnel: app_opened -> puzzle_started -> puzzle_completed -> account_created -> group_joined.

**8.3 No A/B testing infrastructure requirement**
- Severity: **Medium**
- Phase: **MVP**
- The Innovation section mentions "A/B testing with Firebase Remote Config" but there is no functional requirement for the infrastructure. What can be A/B tested? Hint count? Difficulty curve? Onboarding flow?

**8.4 No attribution tracking requirement**
- Severity: **Medium**
- Phase: **MVP**
- Success criteria include "viral coefficient > 0.5" and the Measurable Outcomes table lists "Attribution tracking," but there is no FR specifying how the app tracks whether a new user came from a share card, a deep link, an organic app store search, etc.

**8.5 No performance monitoring requirements**
- Severity: **Medium**
- Phase: **MVP**
- NFRs define performance targets but there is no requirement for monitoring them in production (real-time dashboards, alerting thresholds, anomaly detection).

---

## 9. Missing Moderation/Abuse Prevention

**9.1 No display name moderation**
- Severity: **High**
- Phase: **MVP**
- FR23 allows 20-character display names. Journey 5 shows an admin removing a user with an "offensive display name," but there is no system-level requirement for profanity filtering, prohibited word lists, or automated detection. The PRD relies entirely on admin manual removal, which only works within groups -- globally, offensive names are unchecked.

**9.2 No group name/description moderation**
- Severity: **Medium**
- Phase: **MVP**
- FR34 allows group creation with names and descriptions. There is no content moderation for group names. An offensive group name visible in leaderboard contexts has no remediation path.

**9.3 No spam/abuse prevention for share cards**
- Severity: **Medium**
- Phase: **Post-MVP**
- FR45-FR47 describe share card generation and sharing. There is no requirement for rate limiting share generation or preventing automated spam of share cards.

**9.4 No reporting mechanism**
- Severity: **High**
- Phase: **MVP**
- Journey 5 shows admin removing an offensive user, but there is no requirement for non-admin users to report offensive display names, group names, or abusive behavior. Apple App Store Review Guidelines (Guideline 1.2) require apps with user-generated content to have a reporting mechanism.

**9.5 No ban/suspension system**
- Severity: **Medium**
- Phase: **MVP**
- FR40 allows group-level member removal, but there is no system-level ban capability for users who create multiple accounts to harass groups, manipulate leaderboards, or generate offensive content.

---

## 10. Missing Monetization Infrastructure

**10.1 No monetization framework or extensibility requirement**
- Severity: **Low**
- Phase: **Post-MVP**
- The 12-month target mentions "Explore optional cosmetic monetization (themes, path colors)." There is no requirement for: in-app purchase infrastructure, a virtual currency system, a storefront UI, price point management, or receipt validation. Even if monetization is post-MVP, the data model and architecture should plan for it.

**10.2 No ad framework mentioned (even to explicitly exclude it)**
- Severity: **Low**
- Phase: **Post-MVP**
- PLAN.md mentions "watching optional ad" for hints, but the PRD does not include or explicitly exclude ads. This creates ambiguity.

---

## 11. Missing App Store Requirements

**11.1 No app store rating prompt strategy**
- Severity: **High**
- Phase: **MVP**
- Success criteria include "4.5+ average App Store / Play Store rating," but there is no requirement for when to prompt users for a rating. Both Apple and Google provide in-app review APIs. Best practice is to prompt after a positive moment (e.g., after a fast solve, after a streak milestone). No FR addresses this.

**11.2 No app store metadata/ASO requirements**
- Severity: **Medium**
- Phase: **MVP**
- No requirement for app store description, keywords, screenshots, or preview video strategy. These directly impact discoverability and the 5,000 MAU 3-month target.

**11.3 No app store review compliance checklist**
- Severity: **High**
- Phase: **MVP**
- Apple's App Store Review Guidelines have specific requirements for apps with user-generated content (Guideline 1.2: user reporting, blocking), apps with account creation (Guideline 5.1.1: must allow account deletion -- covered by FR26), and apps with anonymous auth (must still comply with data collection transparency). No FR systematically addresses App Store Guidelines compliance.

---

## 12. Missing Legal/Compliance

**12.1 No age gating or COPPA compliance**
- Severity: **Critical**
- Phase: **MVP**
- The PRD targets 22-45 year olds but has no age gate. Without an age gate, children under 13 can use the app, triggering COPPA requirements in the US and similar regulations in the EU (GDPR-K). Apple and Google both require apps to declare an age rating. The PRD classification states "no regulatory compliance" which is incorrect -- any app available to children requires COPPA compliance unless it gates to 13+.

**12.2 No privacy consent flow**
- Severity: **Critical**
- Phase: **MVP**
- FR58 says users can "view the app's privacy policy and terms of service," but there is no requirement for active consent (accepting terms before use), consent management (withdrawing consent), or cookie/tracking consent (required in the EU under ePrivacy Directive). Firebase Analytics collects data from the first launch -- consent must be obtained before or at that point.

**12.3 No Apple App Tracking Transparency (ATT) requirement**
- Severity: **Critical**
- Phase: **MVP**
- If Firebase Analytics or any attribution tracking is used, iOS requires an ATT prompt before tracking. The PRD has no requirement for this. Submitting to the App Store without proper ATT handling results in rejection.

**12.4 No terms of service requirements specified**
- Severity: **High**
- Phase: **MVP**
- FR58 mentions viewing ToS but does not specify what the ToS must cover: user-generated content policies, dispute resolution, limitation of liability, intellectual property (puzzle ownership), or acceptable use policy.

**12.5 No DSAR (Data Subject Access Request) handling**
- Severity: **Medium**
- Phase: **MVP**
- GDPR requires responding to data access requests within 30 days. No requirement or process is defined for handling these requests.

---

## 13. Missing Migration/Versioning Requirements

**13.1 No client-server API versioning strategy**
- Severity: **Critical**
- Phase: **MVP**
- No requirement for API versioning. When the server changes (new puzzle format, new leaderboard algorithm), old app versions need to either continue working or be force-updated. Without versioning, server changes can break old clients.

**13.2 No database schema migration strategy in PRD**
- Severity: **High**
- Phase: **MVP**
- The architecture mentions SQL migration files, but the PRD has no requirement for: backward-compatible schema changes, zero-downtime migrations, or data migration testing. This is critical because the game tracks streaks -- a botched migration could destroy streak data.

**13.3 No local cache migration requirement**
- Severity: **High**
- Phase: **MVP**
- The app uses Hive for local caching. When the app updates and the cached puzzle format changes, there is no requirement for migrating local Hive data to the new schema. A naive approach would wipe the cache, potentially losing offline queued results.

**13.4 No feature flag infrastructure requirement**
- Severity: **Medium**
- Phase: **MVP**
- Firebase Remote Config is mentioned in PLAN.md but not as a PRD requirement. Feature flags are essential for: gradual rollouts, kill switches for broken features, and A/B testing.

---

## 14. Missing Timezone Handling Requirements

**14.1 No specification of daily puzzle rollover time**
- Severity: **Critical**
- Phase: **MVP**
- FR12 says "one puzzle per day, identical for all users worldwide." FR18 says hints reset "at midnight UTC." But the PRD never specifies when the daily puzzle changes for the user. Midnight UTC? Midnight local time? This affects: when the puzzle appears as "new," when leaderboards reset, when streaks are evaluated, and when the "already solved" state resets.

**14.2 No specification of streak evaluation timing**
- Severity: **High**
- Phase: **MVP**
- FR28-FR32 define streak behavior but never specify when a "missed day" is evaluated. If the puzzle day is UTC-based, a user in UTC-12 has until noon the next day to solve, while a user in UTC+12 has until midnight the same day. This creates significant fairness issues.

**14.3 No specification of weekly leaderboard boundaries**
- Severity: **Medium**
- Phase: **MVP**
- FR39 mentions weekly leaderboards but does not specify when the week starts (Monday? Sunday?) or what timezone defines the boundary.

**14.4 No handling of daylight saving time transitions**
- Severity: **Low**
- Phase: **MVP**
- If any local time is used for daily boundaries, DST transitions create 23-hour and 25-hour days. No requirement addresses this edge case.

---

## 15. Missing Localization/i18n Infrastructure

**15.1 No localization requirement or strategy**
- Severity: **Medium**
- Phase: **Post-MVP**
- The PRD targets a global audience (implied by "all users worldwide") but has zero mention of localization, internationalization, or language support. Even for an English-only MVP, the codebase should use a localization framework from the start to avoid costly refactoring later.

**15.2 No right-to-left (RTL) layout consideration**
- Severity: **Low**
- Phase: **Post-MVP**
- No requirement for RTL layout support. If the app expands to Arabic/Hebrew markets, this requires significant UI work.

**15.3 No locale-aware formatting**
- Severity: **Medium**
- Phase: **MVP**
- Solve times are displayed (e.g., "0:38," "1:12") but no requirement specifies the time format. Date formatting for puzzle dates, number formatting for statistics -- none of this is locale-specified.

**15.4 No content localization plan for static text**
- Severity: **Low**
- Phase: **Post-MVP**
- Error messages, UI labels, share card text ("I solved today's ZipPath in..."), notification text -- all are English-only with no plan for translation.

---

## Summary Table

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| 1. Error Handling | 2 | 4 | 2 | 0 | **8** |
| 2. Edge Cases | 0 | 3 | 4 | 0 | **7** |
| 3. Data Management | 0 | 3 | 2 | 0 | **5** |
| 4. Security | 1 | 2 | 3 | 0 | **6** |
| 5. App Lifecycle | 2 | 3 | 0 | 0 | **5** |
| 6. Onboarding/Tutorial | 0 | 1 | 1 | 1 | **3** |
| 7. Notifications | 0 | 2 | 2 | 0 | **4** |
| 8. Analytics/Tracking | 0 | 2 | 3 | 0 | **5** |
| 9. Moderation/Abuse | 0 | 2 | 3 | 0 | **5** |
| 10. Monetization | 0 | 0 | 0 | 2 | **2** |
| 11. App Store | 0 | 2 | 1 | 0 | **3** |
| 12. Legal/Compliance | 3 | 1 | 1 | 0 | **5** |
| 13. Migration/Versioning | 1 | 2 | 1 | 0 | **4** |
| 14. Timezone Handling | 1 | 1 | 1 | 1 | **4** |
| 15. Localization/i18n | 0 | 0 | 2 | 2 | **4** |
| **Total** | **10** | **28** | **26** | **6** | **70** |

---

## Top 10 Items to Address Before MVP Launch

1. **12.1 Age gating / COPPA** -- App Store rejection risk; legal liability
2. **12.2 Privacy consent flow** -- GDPR violation from first launch (Firebase Analytics fires before consent)
3. **12.3 Apple ATT prompt** -- App Store rejection on iOS
4. **5.1 App backgrounding during puzzle** -- Directly affects fairness; users will complain immediately
5. **14.1 Daily puzzle rollover time** -- Ambiguous core mechanic; must be defined before any implementation
6. **4.1 Brute force protection on invite codes** -- 6-char codes are trivially enumerable without rate limiting
7. **5.2 Force update mechanism** -- Without this, you cannot fix critical bugs or security issues for deployed users
8. **13.1 API versioning** -- Without this, the first backend change breaks all existing clients
9. **1.1/1.2 Puzzle load + score submission error states** -- Core gameplay loop has undefined failure behavior
10. **9.4 Reporting mechanism** -- Apple App Store Guideline 1.2 requirement for user-generated content; rejection risk

---

