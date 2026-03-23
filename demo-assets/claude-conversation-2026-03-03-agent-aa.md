# Claude Conversation Log

Session ID: agent-aa02abba945194029
Date: 2026-03-03 00:02:59

---

## 👤 User

Read the full architecture document at /Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/architecture.md and identify ANY production-readiness gaps. Specifically audit:

1. Missing infrastructure requirements (health checks, uptime monitoring, alerting?)
2. Missing backup/disaster recovery strategy
3. Missing rate limiting beyond score submission (auth attempts, group creation, API calls?)
4. Missing logging strategy (structured logging, log levels, log retention?)
5. Missing secrets management (how are API keys, service role keys managed in CI and production?)
6. Missing database maintenance (vacuum, connection pool sizing, query monitoring?)
7. Missing app update strategy (force update for breaking changes, graceful deprecation?)
8. Missing certificate pinning or API security beyond TLS
9. Missing image/asset CDN strategy
10. Missing crash recovery (what state is the app in after a crash? can user resume puzzle?)
11. Missing memory management strategy (large grid rendering, animation cleanup?)
12. Missing network retry/backoff strategy
13. Missing data validation at every boundary (client input validation, server response validation?)
14. Missing feature flag infrastructure details
15. Missing A/B testing infrastructure details
16. Missing dependency version pinning strategy
17. Missing code signing and release key management

Report ALL findings as a categorized list with severity (Critical/High/Medium/Low) and whether each is MVP or post-MVP.

---

## 🤖 Claude



I'll start by reading the architecture document thoroughly.

---

## 🤖 Claude

The file is large. Let me read the full output.

---

## 🤖 Claude

Let me read the original file in sections to get the full content.

---

## 🤖 Claude

Now I have read the entire architecture document (1207 lines). Let me compile the comprehensive production-readiness gap analysis.

---

# Production-Readiness Gap Audit: ZipPath Architecture Document

**Document audited:** `/Users/sarathfrancis/work/git/Personal/Zip/_bmad-output/planning-artifacts/architecture.md`

Below is a categorized list of every production-readiness gap identified, organized by the 17 audit categories requested.

---

## 1. Missing Infrastructure Requirements (Health Checks, Uptime Monitoring, Alerting)

**Gap 1.1 -- No health check endpoints for Edge Functions**
- Severity: **High**
- Phase: **MVP**
- The document defines 4 Edge Functions (`daily-puzzle`, `submit-score`, `join-group`, `generate-share-card`) but none include health check endpoints. There is no `/health` or `/readiness` endpoint defined for any function. If `submit-score` silently fails, there is no automated way to detect it.

**Gap 1.2 -- No uptime monitoring or synthetic probes**
- Severity: **High**
- Phase: **MVP**
- The document mentions Firebase Crashlytics and Firebase Performance Monitoring but these are client-side only. There is no server-side uptime monitoring (e.g., UptimeRobot, Checkly, Supabase health dashboard integration, or synthetic checks hitting the `submit-score` endpoint periodically). If Supabase has a regional outage or the cron function stops running, nobody is alerted.

**Gap 1.3 -- No alerting strategy**
- Severity: **High**
- Phase: **MVP**
- There is no mention of PagerDuty, Opsgenie, email alerts, Slack webhooks, or any alerting mechanism. The architecture says Crashlytics catches crashes but does not define alert thresholds (e.g., "alert if crash rate exceeds 2%", "alert if daily-puzzle cron fails to run", "alert if score submission error rate exceeds 5%"). There are no on-call procedures defined.

**Gap 1.4 -- No Supabase project health monitoring**
- Severity: **Medium**
- Phase: **MVP**
- Supabase provides dashboard metrics (database CPU, memory, connection count, disk usage), but the architecture does not mention monitoring these or setting up alerts for approaching limits, especially relevant for the Free/Pro tier at launch.

---

## 2. Missing Backup/Disaster Recovery Strategy

**Gap 2.1 -- No database backup strategy documented**
- Severity: **Critical**
- Phase: **MVP**
- The document never mentions database backups. While Supabase Pro provides daily automated backups, the architecture does not document: backup frequency, backup retention period, point-in-time recovery (PITR) availability, or how to restore from backup. For a game with streak data (which is emotionally valuable to users), losing data is unacceptable.

**Gap 2.2 -- No disaster recovery plan**
- Severity: **High**
- Phase: **MVP**
- There is no mention of RTO (Recovery Time Objective) or RPO (Recovery Point Objective). If the Supabase project becomes corrupted or a bad migration destroys data, there is no documented procedure for recovery. No mention of multi-region failover or even manual recovery steps.

**Gap 2.3 -- No migration rollback strategy**
- Severity: **High**
- Phase: **MVP**
- The document states migrations are "numbered sequentially" and "applied via `supabase db push`" but there is no mention of rollback migrations, pre-migration backups, or migration testing strategy. A bad migration (e.g., `DROP COLUMN` that should have been `ALTER`) could cause permanent data loss in production with no recovery path.

**Gap 2.4 -- No Edge Function rollback strategy**
- Severity: **Medium**
- Phase: **MVP**
- Edge Functions are deployed via `supabase functions deploy` but there is no versioning, canary deployment, or rollback procedure. A broken `submit-score` function would break the entire game with no quick revert.

---

## 3. Missing Rate Limiting Beyond Score Submission

**Gap 3.1 -- No rate limiting on authentication attempts**
- Severity: **High**
- Phase: **MVP**
- The document mentions "Rate limiting: max 10 score submissions per hour per user" (line 243) but says nothing about rate limiting auth attempts (login, sign-up, password reset). While Supabase Auth has some built-in rate limiting, the architecture does not acknowledge or configure it. This is a brute-force attack vector.

**Gap 3.2 -- No rate limiting on group creation**
- Severity: **Medium**
- Phase: **MVP**
- There is no limit on how many groups a user can create. A malicious user could create thousands of groups, polluting the database.

**Gap 3.3 -- No rate limiting on group join attempts**
- Severity: **Medium**
- Phase: **MVP**
- The `join-group` Edge Function has no rate limiting mentioned. An attacker could brute-force 6-character invite codes (the document specifies "invite_code (UNIQUE, 6-char)" at line 193).

**Gap 3.4 -- No rate limiting on general API calls**
- Severity: **Medium**
- Phase: **MVP**
- Direct PostgREST API calls (puzzle data fetch, profile updates, group queries) have no rate limiting mentioned. Supabase provides some built-in protection but the architecture does not configure or document it.

**Gap 3.5 -- No rate limiting on share card generation**
- Severity: **Low**
- Phase: **Post-MVP**
- The `generate-share-card` Edge Function generates images (computationally expensive) with no rate limiting mentioned.

---

## 4. Missing Logging Strategy

**Gap 4.1 -- No structured logging format defined**
- Severity: **High**
- Phase: **MVP**
- The document mentions Firebase Crashlytics for crash reporting but never defines a structured logging strategy. There is no mention of: log format (JSON structured logs?), log levels (debug, info, warn, error), what gets logged at each level, or consistent log context (user_id, request_id, correlation_id).

**Gap 4.2 -- No server-side logging strategy for Edge Functions**
- Severity: **High**
- Phase: **MVP**
- Edge Functions (Deno runtime) produce logs, but the architecture does not mention: how Edge Function logs are collected, where they are stored, how long they are retained, or how to search them when debugging production issues. Supabase provides limited log retention on lower tiers.

**Gap 4.3 -- No log retention policy**
- Severity: **Medium**
- Phase: **MVP**
- No mention of how long client-side or server-side logs are retained. Firebase Crashlytics retains crash data for 90 days by default, but this is not documented or acknowledged.

**Gap 4.4 -- No client-side debug logging strategy**
- Severity: **Medium**
- Phase: **MVP**
- The architecture does not define whether the app uses `debugPrint`, `log()`, or a logging package (e.g., `logger`). No mention of log levels in debug vs. release builds, or whether release builds strip debug logs.

**Gap 4.5 -- No audit logging for sensitive operations**
- Severity: **Medium**
- Phase: **Post-MVP**
- Operations like account deletion, group admin actions (removing members, regenerating invite codes), and anonymous-to-authenticated account linking have no audit trail mentioned.

---

## 5. Missing Secrets Management

**Gap 5.1 -- No secrets management strategy for CI/CD**
- Severity: **Critical**
- Phase: **MVP**
- The document mentions ".env files (development, staging, production) with Supabase URL and anon key" (line 312) and `.env.example` as a template, but never specifies how secrets are managed in CI/CD. GitHub Actions secrets? Encrypted environment variables? The Supabase service role key (used by Edge Functions for privileged operations, mentioned at line 237) is never discussed in terms of how it is provisioned, rotated, or protected.

**Gap 5.2 -- No secret rotation policy**
- Severity: **High**
- Phase: **Post-MVP**
- No mention of rotating Supabase service role keys, anon keys, Firebase API keys, or FCM server keys. No key rotation schedule or procedure documented.

**Gap 5.3 -- No distinction between secrets and configuration**
- Severity: **Medium**
- Phase: **MVP**
- The `.env` files are mentioned to contain "Supabase URL and anon key" but no distinction is made between public configuration (Supabase URL, anon key -- which are meant to be public) and actual secrets (service role key, Firebase server key). This conflation could lead to accidental secret exposure.

**Gap 5.4 -- Fastlane credentials management not specified**
- Severity: **High**
- Phase: **MVP**
- The architecture lists Fastlane for deployment with a `Matchfile` for code signing but does not specify how App Store Connect API keys, Google Play service account credentials, and Apple certificates/provisioning profiles are stored and accessed in CI.

---

## 6. Missing Database Maintenance

**Gap 6.1 -- No VACUUM/ANALYZE strategy**
- Severity: **Medium**
- Phase: **Post-MVP**
- The `puzzle_attempts` table will grow continuously (every user, every day). The architecture mentions no auto-vacuum tuning, manual vacuum scheduling, or table bloat monitoring. Supabase manages some of this, but the architecture should acknowledge it especially for the `puzzle_attempts` table.

**Gap 6.2 -- Connection pool sizing not specified**
- Severity: **Medium**
- Phase: **MVP**
- The document mentions "Connection pooling via PgBouncer (built into Supabase Pro tier)" (line 306) but does not specify pool sizes, connection limits per user, or timeouts. The scaling table mentions "10K concurrent users" at launch but does not validate whether the default PgBouncer configuration supports this.

**Gap 6.3 -- No query performance monitoring**
- Severity: **High**
- Phase: **MVP**
- Despite defining database functions (`get_group_daily_leaderboard`, `get_group_weekly_leaderboard`) and multiple indexes, the architecture does not mention: slow query logging, `pg_stat_statements` monitoring, query execution plan analysis, or performance baselines. When leaderboard queries slow down at scale, there is no mechanism to detect it before users complain.

**Gap 6.4 -- No data archival strategy**
- Severity: **Low**
- Phase: **Post-MVP**
- The `puzzle_attempts` table has no partitioning or archival plan for MVP. The scaling section mentions "database partitioning on puzzle_attempts by date" for the 100K+ phase, but there is no intermediate strategy. After one year with 50K MAU, this table could have 18M+ rows.

**Gap 6.5 -- No database schema versioning beyond sequential numbering**
- Severity: **Low**
- Phase: **Post-MVP**
- Migrations are "numbered sequentially (001_, 002_, etc.)" with no mention of a schema version tracking table, migration checksums, or tools like Flyway/Liquibase that provide idempotent migration guarantees.

---

## 7. Missing App Update Strategy

**Gap 7.1 -- No forced update mechanism for breaking changes**
- Severity: **Critical**
- Phase: **MVP**
- The architecture mentions no minimum app version enforcement. If a database migration changes the schema (e.g., renaming a column, changing the puzzle JSON format), old app versions will break silently. There is no mechanism to: check minimum required version at app launch, display a "Please update" dialog, or block API access from outdated clients.

**Gap 7.2 -- No API versioning strategy**
- Severity: **High**
- Phase: **MVP**
- Edge Functions have no versioning (e.g., `/v1/submit-score`). Direct PostgREST calls have no version namespacing. When the puzzle JSON format or score submission API changes, there is no backward compatibility layer.

**Gap 7.3 -- No graceful deprecation strategy**
- Severity: **Medium**
- Phase: **Post-MVP**
- No mention of sunset headers, deprecation warnings, or migration timelines for old API endpoints or features.

**Gap 7.4 -- No OTA update strategy for non-native changes**
- Severity: **Low**
- Phase: **Post-MVP**
- Flutter does not natively support code push/OTA updates (unlike React Native with CodePush). The architecture does not mention Shorebird or any equivalent for pushing hotfixes without store review cycles.

---

## 8. Missing Certificate Pinning or API Security Beyond TLS

**Gap 8.1 -- No certificate pinning**
- Severity: **Medium**
- Phase: **Post-MVP**
- The document states "All network communication over HTTPS/TLS 1.2+" (line 240) but there is no certificate pinning mentioned. Without pinning, the app is vulnerable to man-in-the-middle attacks via compromised CAs or user-installed certificates. For a game with anti-cheat concerns (solution validation), this is relevant.

**Gap 8.2 -- No API request signing or integrity verification**
- Severity: **Medium**
- Phase: **Post-MVP**
- Score submissions are validated server-side (path re-verification, timing checks), but API requests themselves are not signed. A sophisticated attacker could replay or tamper with requests. No HMAC signing, request nonces, or integrity tokens are mentioned.

**Gap 8.3 -- No anti-tampering / root/jailbreak detection**
- Severity: **Low**
- Phase: **Post-MVP**
- No mention of detecting rooted/jailbroken devices where the app binary could be modified to bypass anti-cheat measures (e.g., sending fabricated solve times).

**Gap 8.4 -- No Content Security Policy for Edge Functions**
- Severity: **Low**
- Phase: **Post-MVP**
- Edge Functions that return data (especially `generate-share-card` which generates images) have no CSP headers or CORS configuration documented.

---

## 9. Missing Image/Asset CDN Strategy

**Gap 9.1 -- No CDN for puzzle delivery**
- Severity: **Medium**
- Phase: **Post-MVP**
- The document acknowledges this in the "Deferred Decisions" section: "CDN for puzzle delivery (add when user base exceeds 100K)" (line 174). However, even at MVP scale, puzzle data fetched from a Supabase instance in a single region will have high latency for users in other regions. The architecture does not specify the Supabase region or how region selection relates to target user geography.

**Gap 9.2 -- No CDN for share card images**
- Severity: **Medium**
- Phase: **Post-MVP**
- The `generate-share-card` Edge Function generates images but there is no caching or CDN strategy for these generated images. If a share card link goes viral, every request hits the Edge Function to regenerate the image.

**Gap 9.3 -- No avatar asset CDN strategy**
- Severity: **Low**
- Phase: **Post-MVP**
- Preset avatar images are bundled in the app (`assets/images/avatars/`), but if avatars are ever served from Supabase Storage, there is no CDN mentioned for the Storage bucket.

**Gap 9.4 -- No asset cache invalidation strategy**
- Severity: **Low**
- Phase: **Post-MVP**
- Bundled assets (fallback puzzles, avatars, fonts) are part of the app binary. The architecture does not discuss how to update these between app releases or how cache headers are set for remotely fetched assets.

---

## 10. Missing Crash Recovery

**Gap 10.1 -- No puzzle state persistence on crash**
- Severity: **High**
- Phase: **MVP**
- The architecture defines `game_state_provider.dart` for "Active game state (path, time, hints)" but does not mention persisting this state to disk. If the app crashes or is killed by the OS during an active puzzle solve, the user loses all progress (path drawn, time elapsed, hints used). There is no mention of auto-saving game state to Hive or SharedPreferences periodically during play.

**Gap 10.2 -- No sync queue recovery after crash**
- Severity: **High**
- Phase: **MVP**
- The offline sync queue is stored in Hive, which should survive crashes. However, the architecture does not explicitly state that the sync queue is durable or that pending submissions are retried on next app launch. If a score was queued but the app crashed before the Hive write committed, the score is lost.

**Gap 10.3 -- No app state restoration strategy**
- Severity: **Medium**
- Phase: **MVP**
- When the app restarts after a crash, the document does not specify what state the user lands in. Does the app go back to the home screen? Does it resume the puzzle? Does it show the result screen if the puzzle was completed but the score submission was pending?

**Gap 10.4 -- No timer accuracy after background/crash**
- Severity: **Medium**
- Phase: **MVP**
- The `timer_provider.dart` manages the solve timer, but the architecture does not address: what happens to the timer when the app is backgrounded (pause? continue?), what happens to the timer accuracy after process death and restoration, or how the server validates timer accuracy against wall clock time.

---

## 11. Missing Memory Management Strategy

**Gap 11.1 -- No memory budget defined for puzzle rendering**
- Severity: **Medium**
- Phase: **MVP**
- The architecture specifies CustomPainter with Canvas API for 60 FPS rendering but does not define memory budgets. For larger grids (the document mentions variable grid sizes via `grid_width`, `grid_height`), path rendering could allocate many `Path` and `Paint` objects. No mention of object pooling, canvas layer management, or memory pressure monitoring.

**Gap 11.2 -- No animation lifecycle management**
- Severity: **Medium**
- Phase: **MVP**
- The document mentions "Rive animations loaded lazily on first puzzle completion" (line 299) but does not address: disposing animation controllers, releasing GPU resources on screen transitions, or handling animation state when the app is backgrounded. Rive animations can be memory-intensive.

**Gap 11.3 -- No Hive cache size limits**
- Severity: **Medium**
- Phase: **MVP**
- The architecture specifies "Puzzle data cached on-device 24 hours before release" but does not define maximum cache size, eviction policy (LRU?), or what happens when device storage is low. Over time, cached puzzles and sync queue entries could accumulate.

**Gap 11.4 -- No image memory management for share cards**
- Severity: **Low**
- Phase: **Post-MVP**
- Share card generation creates in-memory images. The architecture does not discuss image resolution limits, memory caps during generation, or disposal of generated images after sharing.

**Gap 11.5 -- No Realtime subscription cleanup strategy**
- Severity: **Medium**
- Phase: **MVP**
- The document mentions Realtime subscriptions for leaderboards are "paused when app is backgrounded, resumed on foreground" (line 272) but does not address cleanup when a user leaves a group, when subscriptions leak due to navigation bugs, or maximum concurrent subscription limits.

---

## 12. Missing Network Retry/Backoff Strategy

**Gap 12.1 -- No retry strategy for failed API calls**
- Severity: **High**
- Phase: **MVP**
- The document mentions "Network errors trigger offline fallback behavior" (line 267) and Riverpod's "automatic retry for transient failures" (line 278), but does not specify: how many retries, what backoff algorithm (exponential? jitter?), which errors are retryable (5xx yes, 4xx no?), or maximum retry duration. The offline sync queue mentions processing "in order" but not retry behavior for individual items.

**Gap 12.2 -- No timeout configuration**
- Severity: **High**
- Phase: **MVP**
- The NFRs specify performance targets (<500ms network puzzle load, <300ms score submission) but the architecture defines no HTTP timeout values. If Supabase is slow, what is the client-side timeout? 5 seconds? 30 seconds? No mention of connect timeout vs. read timeout.

**Gap 12.3 -- No circuit breaker pattern**
- Severity: **Medium**
- Phase: **Post-MVP**
- If the backend is down, the app will keep retrying indefinitely (based on the architecture as written). No circuit breaker pattern to stop hammering a failing service and degrade gracefully.

**Gap 12.4 -- No sync queue backoff strategy**
- Severity: **Medium**
- Phase: **MVP**
- The offline sync queue processes pending submissions "when connectivity returns" but there is no backoff if submissions keep failing. The queue could process endlessly on reconnection, draining battery.

---

## 13. Missing Data Validation at Every Boundary

**Gap 13.1 -- No server response validation schema**
- Severity: **High**
- Phase: **MVP**
- The document specifies `fromJson` factory constructors on model classes (line 570-581) but these perform only type casting (`as String`, `as int`). There is no schema validation: no null checks on required fields, no range validation (is `solve_time_ms` negative? is `grid_width` zero?), no enum validation (is `difficulty` a valid value?). A malformed server response could crash the app.

**Gap 13.2 -- No client input sanitization beyond path validation**
- Severity: **Medium**
- Phase: **MVP**
- User-editable fields (`display_name`, group `name`) have no client-side or server-side input sanitization documented. No maximum length, no profanity filter, no HTML/script injection prevention, no Unicode normalization.

**Gap 13.3 -- No deep link validation**
- Severity: **Medium**
- Phase: **MVP**
- Deep links (`/join/{invite_code}`, `/puzzle/{date}`) are routed via GoRouter but the architecture does not mention validating the `invite_code` format or `date` format before making API calls. Malformed deep links could cause unhandled exceptions.

**Gap 13.4 -- No Edge Function input validation specification**
- Severity: **High**
- Phase: **MVP**
- Edge Functions are described at a high level but their input validation is not specified. The `submit-score` function validates the path and timing, but: What if `puzzle_id` is missing? What if `solve_time_ms` is a string? What if the request body is malformed JSON? No input schema (e.g., Zod, JSON Schema) is specified for Edge Functions.

**Gap 13.5 -- No Realtime subscription data validation**
- Severity: **Medium**
- Phase: **MVP**
- Realtime subscriptions on `puzzle_attempts` deliver database change events. The architecture does not mention validating the shape of these events before processing them in the leaderboard provider.

---

## 14. Missing Feature Flag Infrastructure Details

**Gap 14.1 -- No feature flag naming convention**
- Severity: **Low**
- Phase: **Post-MVP**
- The document mentions "Firebase Remote Config: feature flags for A/B testing and gradual rollouts" (line 318) but provides no naming convention for flags, no list of planned flags, and no default values strategy.

**Gap 14.2 -- No feature flag caching/fallback behavior**
- Severity: **Medium**
- Phase: **MVP**
- Firebase Remote Config requires a network call to fetch values. The architecture does not specify: default values for all flags, fetch interval (minimum 12 hours for production?), stale config TTL, or behavior when Remote Config is unreachable.

**Gap 14.3 -- No feature flag governance**
- Severity: **Low**
- Phase: **Post-MVP**
- No mention of who can create/modify feature flags, how flags are cleaned up after rollout completes, or how flags interact with app versioning.

---

## 15. Missing A/B Testing Infrastructure Details

**Gap 15.1 -- No A/B testing framework specified**
- Severity: **Low**
- Phase: **Post-MVP**
- The architecture mentions "A/B testing: Firebase Remote Config is included but specific experiment definitions are deferred to post-launch" (line 1111). However, even the infrastructure details are missing: how are users assigned to experiment cohorts? How is statistical significance calculated? How are experiment results collected?

**Gap 15.2 -- No experiment event tracking integration**
- Severity: **Low**
- Phase: **Post-MVP**
- Firebase Analytics is specified for custom events, but the architecture does not describe how analytics events tie to Remote Config experiments for measuring experiment outcomes.

---

## 16. Missing Dependency Version Pinning Strategy

**Gap 16.1 -- No lockfile strategy documented**
- Severity: **Medium**
- Phase: **MVP**
- The architecture specifies package versions with caret ranges (`riverpod ^3.2.x`, `riverpod_annotation ^4.0.x`) but does not mention whether `pubspec.lock` is committed to version control. Without a committed lockfile, different developers and CI environments may resolve different dependency versions, causing "works on my machine" issues.

**Gap 16.2 -- No dependency update policy**
- Severity: **Medium**
- Phase: **MVP**
- No mention of how dependency updates are evaluated, tested, and applied. Flutter and its ecosystem evolve rapidly. No mention of Dependabot, Renovate, or manual review cadence.

**Gap 16.3 -- No Supabase CLI version pinning**
- Severity: **Low**
- Phase: **MVP**
- The CI/CD pipeline uses `supabase db push` and `supabase functions deploy` but does not specify which Supabase CLI version to use, creating risk of migration behavior changes between CI runs.

**Gap 16.4 -- No Flutter SDK version pinning**
- Severity: **Medium**
- Phase: **MVP**
- The document specifies "Flutter 3.41.x" but does not mention using `.fvm` (Flutter Version Management) or a similar tool to pin the exact Flutter SDK version across developers and CI. The `flutter` channel can drift.

---

## 17. Missing Code Signing and Release Key Management

**Gap 17.1 -- No Android keystore management strategy**
- Severity: **Critical**
- Phase: **MVP**
- The architecture mentions Fastlane for deployment but does not address: where the Android upload keystore is stored, how it is backed up (losing the keystore means you cannot update the app on Google Play ever), who has access, or how it is accessed in CI. This is an existential risk.

**Gap 17.2 -- No iOS code signing strategy beyond mentioning Matchfile**
- Severity: **High**
- Phase: **MVP**
- The document includes `fastlane/Matchfile` in the project structure (line 873) which implies using Fastlane Match for certificate management, but does not specify: the Git repo or storage backend for certificates, the Match encryption passphrase management, certificate type (development, ad-hoc, app-store), or provisioning profile management.

**Gap 17.3 -- No Play Store / App Store credential management**
- Severity: **High**
- Phase: **MVP**
- No mention of how App Store Connect API keys or Google Play service account JSON keys are stored, rotated, or accessed in CI for automated deployments.

**Gap 17.4 -- No code signing verification in CI**
- Severity: **Medium**
- Phase: **MVP**
- The CI workflow (`.github/workflows/release.yml`) is mentioned but there is no specification that release builds verify code signing integrity, or that debug builds use different signing configurations.

---

## Summary Table

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| 1. Infrastructure (Health/Monitoring/Alerting) | 0 | 3 | 1 | 0 | 4 |
| 2. Backup/Disaster Recovery | 1 | 2 | 1 | 0 | 4 |
| 3. Rate Limiting | 0 | 1 | 3 | 1 | 5 |
| 4. Logging Strategy | 0 | 2 | 3 | 0 | 5 |
| 5. Secrets Management | 1 | 2 | 1 | 0 | 4 |
| 6. Database Maintenance | 0 | 1 | 2 | 2 | 5 |
| 7. App Update Strategy | 1 | 1 | 1 | 1 | 4 |
| 8. Certificate Pinning / API Security | 0 | 0 | 2 | 2 | 4 |
| 9. Image/Asset CDN | 0 | 0 | 2 | 2 | 4 |
| 10. Crash Recovery | 0 | 2 | 2 | 0 | 4 |
| 11. Memory Management | 0 | 0 | 4 | 1 | 5 |
| 12. Network Retry/Backoff | 0 | 2 | 2 | 0 | 4 |
| 13. Data Validation | 0 | 2 | 3 | 0 | 5 |
| 14. Feature Flag Infrastructure | 0 | 0 | 1 | 2 | 3 |
| 15. A/B Testing Infrastructure | 0 | 0 | 0 | 2 | 2 |
| 16. Dependency Version Pinning | 0 | 0 | 3 | 1 | 4 |
| 17. Code Signing / Release Keys | 1 | 2 | 1 | 0 | 4 |
| **TOTALS** | **4** | **20** | **31** | **14** | **69** |

**MVP items:** 48 gaps (4 Critical, 17 High, 22 Medium, 5 Low)
**Post-MVP items:** 21 gaps (0 Critical, 3 High, 9 Medium, 9 Low)

---

## Top Priority Items (Must Address Before Launch)

The 4 **Critical** gaps that represent existential risks:

1. **Gap 2.1** -- No database backup strategy documented. If streak data or puzzle data is lost, users churn and recovery is impossible.
2. **Gap 5.1** -- No secrets management strategy for CI/CD. Unclear how the Supabase service role key (which bypasses all RLS) is secured.
3. **Gap 7.1** -- No forced update mechanism. A breaking backend change with no minimum version enforcement will break all existing app installs.
4. **Gap 17.1** -- No Android keystore management strategy. Losing the upload keystore is irrecoverable; you cannot update the app on Google Play.

---

