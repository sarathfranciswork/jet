# Claude Conversation Log

Session ID: agent-a9221155ac18f4cd0
Date: 2026-03-06 18:51:47

---

## 👤 User

I need to understand the full app structure of this Flutter app (Zlynkr/ZipPath). Please find:

1. All screen/page files (presentation layer) - list every screen widget
2. All route definitions (GoRouter or similar)
3. What themes exist (light/dark/colorblind)
4. Auth flow files (login, register, OAuth)
5. Any existing test files (unit, widget, integration, golden)
6. What testing dependencies are in pubspec.yaml (integration_test, flutter_test, golden_toolkit, etc.)
7. Any existing test configuration or driver files

Be thorough - I need to know every user-facing screen in the app.

---

## 🤖 Claude

I'll help you understand the full app structure. Let me search for all the key files.

---

## 🤖 Claude

Now let me read the key files for screens, routing, themes, and auth:

---

## 🤖 Claude

Now let me check the theme provider and remaining screen files:

---

## 🤖 Claude

Now let me check the remaining screens and the profile/groups/stats screens:

---

## 🤖 Claude

Now let me check the email auth screen and the remaining auth flow:

---

## 🤖 Claude

Now let me check the test files and app shell:

---

## 🤖 Claude

Perfect! Now I have all the information I need. Let me create a comprehensive summary of the app structure.

## Complete Flutter App Structure - ZipPath/Zlynkr

### 1. SCREEN/PAGE FILES (Presentation Layer)

All screens are located in `/lib/features/{feature}/presentation/` and `/lib/shared/`:

**Authentication Flow:**
- `/lib/features/auth/presentation/onboarding_screen.dart` - 3-page onboarding carousel (Welcome, One Puzzle Per Day, Compete with Friends)
- `/lib/features/auth/presentation/auth_screen.dart` - OAuth sign-in hub (Google, Apple, Email, Guest)
- `/lib/features/auth/presentation/email_auth_screen.dart` - Email sign-up/sign-in form

**Bottom Navigation Tabs (4 main screens):**
- `/lib/features/home/presentation/home_screen.dart` - Daily puzzle card with play button
- `/lib/features/groups/presentation/groups_screen.dart` - Create/join groups, list user's groups
- `/lib/features/stats/presentation/stats_screen.dart` - Streaks, statistics, solve history calendar
- `/lib/features/profile/presentation/profile_screen.dart` - Avatar, account info, settings (theme, haptic, sound, colorblind mode, notifications)

**Puzzle Gameplay:**
- `/lib/features/puzzle/presentation/puzzle_screen.dart` - Main puzzle game screen with grid, controls, timer
- `/lib/features/puzzle/presentation/widgets/puzzle_grid.dart` - Grid rendering (5x5 to 8x8)
- `/lib/features/puzzle/presentation/widgets/snake_renderer.dart` - Snake path animation
- `/lib/features/puzzle/presentation/widgets/game_controls.dart` - Undo/Reset/Hint buttons
- `/lib/features/puzzle/presentation/widgets/celebration_overlay.dart` - Completion celebration with confetti

**Groups:**
- `/lib/features/groups/presentation/group_detail_screen.dart` - Group view with 3 tabs: Daily Leaderboard, Weekly Leaderboard, Members
- `/lib/features/groups/presentation/join_group_screen.dart` - Deep-link join screen (auto-joins via invite code)

**Shared Widgets:**
- `/lib/shared/widgets/app_shell.dart` - Bottom navigation bar container (4 tabs: Home, Groups, Stats, Profile)
- `/lib/shared/widgets/animated_background.dart` - Animated background for full-screen effects
- `/lib/shared/widgets/particle_field.dart` - Particle animation layer
- `/lib/shared/widgets/spring_button.dart` - Custom spring physics button
- `/lib/shared/widgets/celebration_overlay.dart` - Confetti celebration overlay
- `/lib/features/sharing/presentation/share_card_widget.dart` - Share card generation (client-side via RepaintBoundary)

**Settings/Profile Widgets:**
- `/lib/features/profile/presentation/widgets/colorblind_selector.dart` - Colorblind mode selector (deuteranopia, protanopia, tritanopia)
- `/lib/features/profile/presentation/widgets/edit_name_dialog.dart` - Display name edit dialog

**Stats Widgets:**
- `/lib/features/stats/presentation/widgets/streak_calendar.dart` - Solve history calendar visualization

### 2. ROUTE DEFINITIONS (GoRouter)

**File:** `/lib/core/router/app_router.dart`

**Routes:**
```
/onboarding                    → OnboardingScreen (fullscreen, no tabs)
/                              → HomeScreen (ShellRoute with bottom nav)
/groups                        → GroupsScreen (ShellRoute with bottom nav)
/stats                         → StatsScreen (ShellRoute with bottom nav)
/profile                       → ProfileScreen (ShellRoute with bottom nav)
/puzzle/:date                  → PuzzleScreen (fullscreen, no tabs)
/groups/:id                    → GroupDetailScreen (fullscreen, no tabs)
/join/:code                    → JoinGroupScreen (deep link, fullscreen)
/auth                          → AuthScreen (fullscreen, no tabs)
/auth/email                    → EmailAuthScreen (fullscreen, no tabs)
```

**Navigation Structure:**
- **ShellRoute** wraps Home/Groups/Stats/Profile with AppShell (bottom nav)
- **Root Navigator** handles modal screens (puzzle, auth, groups detail, join)
- **Redirect Logic:** Forces `/onboarding` on first launch unless already seen

### 3. THEMES (Light/Dark/Colorblind)

**File:** `/lib/core/theme/app_theme.dart`

**Available Themes:**
- **Dark Theme** (default) - Deep navy (#0A1628) background, electric blue and orange path, purple buttons
- **Light Theme** - Light background (#F8FAFC), similar colors adapted for light

**Theme Management:**
- `/lib/core/theme/theme_provider.dart` - Riverpod NotifierProvider manages ThemeMode (light/dark/system)
- Persisted in SharedPreferences

**Color Palette:**
- `/lib/core/constants/app_colors.dart` - 160+ defined colors:
  - **Dark backgrounds:** deepBlack, darkSurface, cardSurface, elevatedSurface
  - **Grid cells:** cellBackground, cellHighlight, cellShadow, cellBorder
  - **Path:** pathOrange → pathYellow gradient (5 stops)
  - **Waypoints:** White with brown for waypoint #1
  - **Walls:** Gray (#2E3A50)
  - **Snake:** Neon green gradient (tail → head)
  - **UI:** Purple (buttons), electric blue, coral orange
  - **Colorblind modes:** Deuteranopia, Protanopia, Tritanopia palettes defined

### 4. AUTH FLOW FILES

**Providers:** `/lib/features/auth/providers/auth_provider.dart` (Riverpod NotifierProvider)

**Auth Methods:**
1. **Anonymous Auth** - First launch, no sign-up wall
2. **Google OAuth** - signInWithGoogle()
3. **Apple OAuth** - signInWithApple()
4. **Email/Password** - signUpWithEmail(), signInWithEmail()
5. **Guest Continue** - signInAnonymously()

**Account Creation Trigger:** After 3rd puzzle solve OR group join attempt

**Session Management:**
- Tokens expire after 30 days inactivity
- Refresh tokens expire after 90 days
- Stored in platform-secure credential storage

### 5. EXISTING TEST FILES

**Unit Tests:** `/test/unit/`
- `/test/core/utils/date_utils_test.dart` - Date formatting tests
- `/test/core/theme/app_theme_test.dart` - Theme validation tests
- `/test/features/puzzle/domain/game_engine_test.dart` - Path validation and game logic

**Widget Tests:** `/test/widget/`
- `/test/features/home/presentation/home_screen_test.dart`
- `/test/features/auth/presentation/onboarding_screen_test.dart`
- `/test/features/puzzle/presentation/widgets/celebration_overlay_test.dart`
- `/test/features/puzzle/presentation/widgets/game_controls_test.dart`
- `/test/shared/widgets/app_shell_test.dart`

**Test Helpers:**
- `/test/helpers/test_helpers.dart` - Mock factories and utilities

**Integration Tests:** `/integration_test/`
- `/integration_test/visual_app_test.dart` - Full app visual validation
- `/integration_test/puzzle_drag_test.dart` - Puzzle drag/drop interaction tests
- `/integration_test/full_visual_audit.dart` - Comprehensive visual regression audit

### 6. TESTING DEPENDENCIES (pubspec.yaml)

**Testing Packages:**
```yaml
flutter_test:                    # Built-in widget testing
integration_test:                # Built-in integration testing
mocktail: ^1.0.4                # Mocking library (instead of mockito)
build_runner: ^2.4.14           # Code generation (for riverpod_generator)
riverpod_generator: ^2.6.4      # Riverpod code generation
freezed: ^3.0.0                 # Data class generation
json_serializable: ^6.9.4       # JSON serialization
flutter_lints: ^6.0.0           # Linting rules (strict)
```

**MISSING (not yet implemented):**
- Golden test framework (`golden_toolkit`) - Visual regression snapshots
- Integration test driver (custom test driver for CI/CD)

### 7. TEST CONFIGURATION FILES

**Analysis:** `analysis_options.yaml` - Strict lint rules (all warnings are errors)

**No custom test driver yet** - Standard `flutter test` and `flutter drive` would be used

### 8. KEY ARCHITECTURAL DETAILS

**State Management:** Riverpod 3.x with code generation
- `@riverpod` annotations on functions
- `AsyncNotifierProvider` for async server state
- `StreamProvider` for Realtime subscriptions
- `NotifierProvider` for local state

**Offline-First:**
- Hive cache for puzzle data
- 7 bundled fallback puzzles
- Offline sync queue with exponential backoff

**Game Engine:**
- `/lib/features/puzzle/domain/game_engine.dart` - Hamiltonian path validation
- `/lib/features/puzzle/domain/models/game_state.dart` - Game state (completed, hints, undos)

**Accessibility:**
- Colorblind mode selector (3 palettes)
- VoiceOver/TalkBack semantic labels
- Focus indicators for keyboard navigation
- Reduced motion support
- Dynamic type scaling support

**Performance Targets:**
- 60 FPS on path drawing
- Cold start < 2 seconds
- Score submission < 300ms
- Memory < 100MB during gameplay

**Absolute file paths for key files:**
- `/Users/sarathfrancis/work/git/Personal/Zip/lib/core/router/app_router.dart`
- `/Users/sarathfrancis/work/git/Personal/Zip/lib/core/theme/app_theme.dart`
- `/Users/sarathfrancis/work/git/Personal/Zip/lib/core/constants/app_colors.dart`
- `/Users/sarathfrancis/work/git/Personal/Zip/lib/features/auth/providers/auth_provider.dart`
- `/Users/sarathfrancis/work/git/Personal/Zip/lib/features/puzzle/presentation/puzzle_screen.dart`
- `/Users/sarathfrancis/work/git/Personal/Zip/lib/shared/widgets/app_shell.dart`

---

