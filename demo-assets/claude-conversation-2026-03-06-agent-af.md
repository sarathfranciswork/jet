# Claude Conversation Log

Session ID: agent-afc133b1bed8a2926
Date: 2026-03-06 18:55:12

---

## 👤 User

I need to understand EVERY screen in this Flutter app in detail so I can write Maestro E2E tests. For each screen file, I need to know:
- What text/labels are visible on screen (button labels, titles, placeholder text)
- What interactive elements exist (buttons, text fields, toggles, sliders)
- What navigation actions are possible
- Any conditional UI (loading states, empty states, error states)

Read these files completely and extract all visible UI text and interactive elements:

1. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/auth/presentation/onboarding_screen.dart
2. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/auth/presentation/auth_screen.dart
3. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/auth/presentation/email_auth_screen.dart
4. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/home/presentation/home_screen.dart
5. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/puzzle/presentation/puzzle_screen.dart
6. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/groups/presentation/groups_screen.dart
7. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/groups/presentation/group_detail_screen.dart
8. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/groups/presentation/join_group_screen.dart
9. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/stats/presentation/stats_screen.dart
10. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/profile/presentation/profile_screen.dart
11. /Users/sarathfrancis/work/git/Personal/Zip/lib/shared/widgets/app_shell.dart
12. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/puzzle/presentation/widgets/celebration_overlay.dart
13. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/puzzle/presentation/widgets/game_controls.dart
14. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/puzzle/presentation/widgets/puzzle_grid.dart
15. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/sharing/presentation/share_card_widget.dart
16. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/profile/presentation/widgets/colorblind_selector.dart
17. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/profile/presentation/widgets/edit_name_dialog.dart
18. /Users/sarathfrancis/work/git/Personal/Zip/lib/features/stats/presentation/widgets/streak_calendar.dart
19. /Users/sarathfrancis/work/git/Personal/Zip/lib/core/router/app_router.dart
20. /Users/sarathfrancis/work/git/Personal/Zip/lib/core/theme/app_theme.dart
21. /Users/sarathfrancis/work/git/Personal/Zip/lib/core/theme/theme_provider.dart

For each screen, provide a structured summary with:
- Screen name and route
- All visible text strings (exact text as it appears)
- All button labels
- All text field hints/labels
- Navigation targets (what happens when you tap each button)
- Conditional states (what changes based on auth state, data loading, etc.)

Be extremely thorough - every piece of text and every interactive element matters for writing test flows.

---

## 🤖 Claude

I'll systematically read all these files to extract complete UI information for Maestro E2E tests. Let me start by reading the screen files in parallel.

---

## 🤖 Claude

Now let me read the remaining screens in parallel:

---

## 🤖 Claude

Now let me read the widget files and remaining system files:

---

## 🤖 Claude

Now let me read the remaining widget files:

---

## 🤖 Claude

Now let me read the router and theme files:

---

## 🤖 Claude

Perfect! Now let me compile all this information into a comprehensive UI reference document for Maestro E2E testing.

## Comprehensive UI Reference Guide for ZipPath App - Maestro E2E Testing

Based on my complete analysis of the Flutter codebase, here's the detailed UI specification for all screens and interactive elements:

---

### 1. ONBOARDING SCREEN
**Route:** `/onboarding`  
**Conditions:** Shows when `StorageService.hasSeenOnboarding == false`

**Static Text:**
- Page 1: Title: "Welcome to Zlynkr" | Description: "Guide the snake through the grid, eating numbered waypoints in order while filling every cell. Feed the path!"
- Page 2: Title: "One Puzzle Per Day" | Description: "A new puzzle every day at midnight UTC. Same puzzle for everyone worldwide. Difficulty scales Monday to Sunday."
- Page 3: Title: "Compete with Friends" | Description: "Create or join groups to see daily and weekly leaderboards. Challenge your friends and family!"

**Interactive Elements:**
- "Skip" button (top right) - navigates to home (`/`)
- Dot indicators (3 dots) - show current page, grow when active
- "Next" button (pages 1-2) - advances page
- "Get Started" button (page 3) - navigates to home (`/`)

---

### 2. AUTH SCREEN
**Route:** `/auth`  
**Conditions:** Shows when user is not authenticated or needs to sign in

**Static Text:**
- App name (with gradient) - "Zlynkr"
- Tagline - "Path puzzle game"
- Loading indicator appears when `authState.isLoading == true`

**Interactive Elements:**
- Google Sign In button: Label "Sign In With Google" (icon + text)
- Apple Sign In button: Label "Sign In With Apple"
- Email Sign In button: Label "Sign In With Email" (outlined)
- "Continue as Guest" link button

**Behavior:**
- Google tap → calls `signInWithGoogle()`
- Apple tap → calls `signInWithApple()`
- Email tap → navigates to `/auth/email`
- Guest tap → calls `signInAnonymously()` and goes to `/`

---

### 3. EMAIL AUTH SCREEN
**Route:** `/auth/email`  
**Form State Toggles:**
- Default state: `_isSignUp = true` → "Create Account" mode
- After tapping toggle: `_isSignUp = false` → "Sign In" mode

**Heading (dynamic):**
- Sign Up mode: "Create Account" | Subtitle: "Sign up with your email to save progress"
- Sign In mode: "Welcome Back" | Subtitle: "Sign in to continue your streak"

**Form Fields:**
1. **Email Field:**
   - Label: "Email"
   - Placeholder: "you@example.com"
   - Prefix icon: envelope icon
   - Validation: Required, must be valid email format
   
2. **Password Field:**
   - Label: "Password"
   - Placeholder (Sign Up only): "At least 6 characters"
   - Prefix icon: lock icon
   - Suffix icon: visibility toggle (eye/eye-off)
   - Validation: Required, min 6 chars for sign up
   
3. **Confirm Password Field (Sign Up only):**
   - Label: "Confirm Password"
   - Prefix icon: lock icon
   - Suffix icon: visibility toggle
   - Validation: Must match password field

**Error Display:**
- Red error container appears if validation fails or auth fails
- Error messages:
  - "Invalid email or password. Please try again."
  - "An account with this email already exists. Try signing in."
  - "Please check your email to confirm your account."
  - "Too many attempts. Please wait a moment."
  - Generic: "Something went wrong. Please try again."

**Buttons:**
- Submit button: "Create Account" (Sign Up) / "Sign In" (Sign In)
  - Disabled when `_isLoading == true`, shows spinner
  - Purple gradient background when enabled
- Toggle button: "Sign In" (from Sign Up) / "Sign Up" (from Sign In)

---

### 4. HOME SCREEN
**Route:** `/`  
**Shell Route:** Yes (has bottom nav)

**Static Text:**
- App name (with gradient): "Zlynkr"
- Tagline: "Path puzzle game"

**Puzzle Card (conditionally rendered):**
- Shows data from `dailyPuzzleProvider`
- Title: "Today's Puzzle"
- Grid size tag: "5x5", "6x6", "7x7", or "8x8"
- Difficulty tag: "Easy", "Medium", "Hard" (first letter capitalized)
- Par time tag: "Par 1m 20s" (formatted human-readable)
- Play button: "Play"

**Loading State:**
- Gray skeleton card with rounded shapes (loading animation)

**Error State:**
- Falls back to default puzzle data: 5x5, easy, 60 seconds

---

### 5. PUZZLE SCREEN
**Route:** `/puzzle/{date}` (date in YYYY-MM-DD format)

**Top Bar:**
- Home button (glass circle) - navigates back
- Info bar showing:
  - Timer: "00:00" (updates every second, tabular figures)
  - Grid size: "5x5 · Easy"
  - Par time: "Par 1m 20s"

**Puzzle Grid:**
- Cell states: empty, filled, waypoint (numbered), wall
- Waypoint numbers: 1, 2, 3, etc.
- Interactive: Tap or drag to draw path
- Visual feedback: Colors change as path is drawn

**Game Controls (bottom):**
- Reset button: "Reset" (purple gradient, left side)
- Hint button: "Hint" with badge showing hints used (outlined, middle)
- Undo button: Circle with undo icon (dark, right side)
- Buttons disabled when game not in playing state

**Completion State:**
- Celebrates with animation overlay
- Shows "Crushed It!" (if under par) or "Puzzle Complete!"
- Displays: time, hints used, difficulty, grid size
- "Share Result" button
- "Done" button (returns to home)

---

### 6. GROUPS SCREEN
**Route:** `/groups`  
**Shell Route:** Yes (has bottom nav)

**Header:**
- Title: "Groups"
- Create/Join buttons appear only if user has groups

**Empty State (when no groups):**
- Icon: group_add_rounded (40px)
- Text: "Create or join a group to compete\nwith friends and family"
- "Create Group" button (elevated)
- "Join Group" button (outlined)

**Groups List:**
- Each group card shows:
  - Group name
  - Description (if exists, truncated to 1 line)
  - Member count icon with "N" text
  - Chevron icon (right arrow)
- Tap card → navigates to `/groups/{group.id}`

**Dialogs:**

**Create Group Dialog:**
- Title: "Create Group"
- Form fields:
  - "Group Name" text field (required, max chars enforced)
  - "Description (optional)" text field (2 lines)
- Buttons: Cancel | Create

**Join Group Dialog:**
- Title: "Join Group"
- Form field: "Group Invite Code" (max 6 chars, uppercase)
  - Hint: "Enter 6-character code"
- Buttons: Cancel | Join
- Shows error if anonymous user tries to join (prompts sign in)

---

### 7. GROUP DETAIL SCREEN
**Route:** `/groups/{id}`

**App Bar:**
- Title: Group name
- Menu button with "Leave Group" option

**Group Header:**
- Description (if exists)
- Member count: "N/50 members"
- Invite code with copy/share buttons
  - Copy button → copies to clipboard, shows snackbar "Invite code copied"
  - Share button → opens system share dialog

**Tabs (3 tabs):**
1. **Daily Tab:** Daily leaderboard
2. **Weekly Tab:** Weekly leaderboard
3. **Members Tab:** Group members list

**Leaderboard Entry:**
- Rank badge (1st-3rd colored gold/silver/bronze, 4+ gray)
- Player name
- Time (primary, right-aligned)
- Hints used (if > 0, secondary, smaller)

**Members List:**
- Avatar with initials or image
- Display name
- "Admin" badge (if admin)

**Empty States:**
- Daily: "No one has played today yet"
- Weekly: "No data for this week yet"
- Members: "No members"

**Leave Confirmation Dialog:**
- Title: "Leave Group"
- Message: "Are you sure you want to leave "{group_name}"?"
- Buttons: Cancel | Leave

---

### 8. JOIN GROUP SCREEN
**Route:** `/join/{code}`  
**Auto-joins on load with invite code**

**States:**

**Joining State:**
- Spinner
- Text: "Joining group..."

**Success State:**
- Check circle icon (green)
- Text: "Successfully joined group!"
- Text: "Redirecting..."
- Auto-redirects to `/groups/{group_id}` after 1 second

**Error State:**
- Error icon (orange/coral)
- Error message: "Could not join group. The invite code may be invalid or the group may be full."
- "Go to Groups" button (navigates to `/groups`)

---

### 9. STATS SCREEN
**Route:** `/stats`  
**Shell Route:** Yes (has bottom nav)

**Header:**
- Title: "Statistics"

**Overview Cards:**
1. **Streak Hero Card:**
   - Left side: Fire icon + Current streak number + "Current Streak"
   - Right side: Trophy icon + Longest streak number + "Longest Streak"
   
2. **Stat Cards (row):**
   - "Puzzles Solved" | value (green theme)
   - "Average Time" | "HH:MM" or "--:--" (purple theme)
   
3. **Streak Freeze Card:**
   - "Streak Freeze" | "N available" or "Used this week" or "0 available" (blue theme)

**Calendar Section (Last 30 Days):**
- 7-column grid of day cells
- Cell colors:
  - Green: solved puzzle
  - Gray: missed/unsolved
  - Green with gold border: solved under par
  - White border: today's date
  - Transparent: future dates
- Legend below: "Solved | Missed | Under par"

**Time Distribution Chart:**
- Title: "Solve Time Distribution"
- Bars for buckets: "<1m", "1-2m", "2-3m", "3-5m", "5m+"
- Each bar shows: label, gradient bar, count

**Refresh:** Pull-down to refresh all stats

---

### 10. PROFILE SCREEN
**Route:** `/profile`  
**Shell Route:** Yes (has bottom nav)

**Avatar Section:**
- Large circular avatar (gradient border) with initials or image
- Display name (editable with pencil icon if authenticated)
- "Create Account" button (if anonymous)

**Account Section (if authenticated):**
- Email: shows user email
- Account Type: "Registered" or "Guest"
- Member Since: formatted date (e.g., "Mar 6, 2026")

**Settings Section:**
- Theme dropdown: System | Dark | Light
- Haptic Feedback toggle
- Sound Effects toggle
- Colorblind Mode selector (bottom sheet with 4 modes)
- Notifications toggle

**App Section:**
- About: "Version 1.0.0 (1)"
- Privacy Policy link
- Terms of Service link
- Delete Account button (red, opens confirmation dialog)

**Sign Out Button (if authenticated):**
- Red outlined button, full width

**Colorblind Mode Bottom Sheet:**
- Title: "Colorblind Mode"
- Description: "Choose a color palette that works best for you"
- Options (tappable rows):
  1. "None" - Default colors (shows P and W color swatches)
  2. "Deuteranopia" - Green-blind friendly
  3. "Protanopia" - Red-blind friendly
  4. "Tritanopia" - Blue-blind friendly
- Selected option shows checkmark

**Edit Name Dialog:**
- Title: "Edit Display Name"
- Text field with hint: "Enter display name"
- Max length: AppSizes.maxDisplayNameLength
- Validation:
  - Not empty
  - Min 2 chars
  - Max length enforced
  - Blocks certain words: admin, moderator, zlynkr, support
- Buttons: Cancel | Save (shows spinner when saving)

**Delete Account Dialog:**
- Title: "Delete Account"
- Message: "Are you sure you want to delete your account? Your account will be scheduled for deletion and permanently removed after 30 days. You can sign back in within this period to cancel the deletion."
- Buttons: Cancel | Delete Account (red)

---

### 11. APP SHELL (Bottom Navigation)
**Routes:** Home, Groups, Stats, Profile

**Bottom Navigation Bar:**
- Item 0: Home icon → navigates to `/`
- Item 1: Groups icon → navigates to `/groups`
- Item 2: Bar chart icon → navigates to `/stats`
- Item 3: Person icon → navigates to `/profile`

**Active/Inactive States:**
- Selected item highlighted in purple
- Unselected items in gray

---

### 12. CELEBRATION OVERLAY
**Trigger:** When puzzle completed

**Dark Overlay:**
- Radial gradient, semi-transparent

**Card Content (animated entrance):**
- Title: "Crushed It!" (if under par, gold) or "Puzzle Complete!" (white)
- Icon: Trophy (if under par) or Check circle (normal)
- Staggered stat reveals:
  - Grid size pill: "5x5 · Easy"
  - Time pill (with timer icon): formatted time with count-up animation
  - Par comparison (if under par): "Under par by HH:MM!"
  - Hints used: "N hint(s) used" (if > 0)
- Buttons:
  - "Share Result" button (gradient, with share icon)
  - "Done" button (outlined)

**Animations:**
- Confetti burst (top and bottom)
- Trophy bounce
- Staggered stat reveals
- Count-up for time display

---

### 13. GAME CONTROLS WIDGET
**Location:** Bottom of puzzle screen

**Button States (conditionally enabled/disabled):**

**Reset Button:**
- Label: "Reset"
- Icon: refresh_rounded
- Enabled: when game is playing AND has path
- Visual: Purple gradient when enabled, grayed out when disabled

**Hint Button:**
- Label: "Hint"
- Badge: Shows hints used count (circular badge, purple background)
- Enabled: when game is playing or not started
- Visual: Outlined border when enabled

**Undo Button:**
- Icon: undo_rounded
- Enabled: when game is playing AND has path
- Visual: Circle, dark surface background

---

### 14. PUZZLE GRID
**Interactive Elements:**
- Tap any cell to place path segment
- Drag to draw path continuously
- Visual feedback: cells light up as path progresses
- Waypoint numbers displayed at intersections
- Wall cells shown as X pattern (raised block effect)

**Accessibility:**
- Cell semantic labels: "Row N, Column M, [empty/filled/waypoint N/wall]"

---

### 15. SHARE CARD WIDGET
**Triggered:** When user taps "Share Result" in celebration overlay

**Card Content (for sharing):**
- Width: 360px
- Header: "Zlynkr" | Date (YYYY-MM-DD format)
- Puzzle grid visualization (200x200px)
- Difficulty & grid: "5x5 · Easy"
- Results row:
  - Timer pill: formatted time
  - Lightbulb pill: "N hint(s)"
- "⭐ Under Par!" (if under par)

---

### ROUTE MAP & NAVIGATION

```
/                          → HomeScreen (with AppShell)
/onboarding                → OnboardingScreen
/auth                      → AuthScreen
/auth/email                → EmailAuthScreen
/puzzle/{date}             → PuzzleScreen
/groups                    → GroupsScreen (with AppShell)
/groups/{id}               → GroupDetailScreen
/join/{code}               → JoinGroupScreen
/stats                     → StatsScreen (with AppShell)
/profile                   → ProfileScreen (with AppShell)
```

---

### KEY TEXT STRINGS & LABELS

**Navigation Bar Labels:**
- "Home"
- "Groups"
- "Statistics"
- "Profile"

**Common Buttons:**
- "Play" (green/purple gradient)
- "Cancel"
- "Create"
- "Join"
- "Skip"
- "Next"
- "Get Started"
- "Share Result"
- "Done"
- "Retry"
- "Sign Out"

**Common Error/Empty Messages:**
- "Could not load puzzle"
- "Generic error"
- "No one has played today yet"
- "No data for this week yet"
- "Failed to load leaderboard"
- "Failed to load members"
- "Create or join a group to compete\nwith friends and family"

---

### CONDITIONAL UI STATES

| Screen | Condition | UI Change |
|--------|-----------|-----------|
| Home | Loading | Shows skeleton loader |
| Home | Error | Shows error card with Retry |
| Auth | Loading | Spinner instead of buttons |
| Puzzle | Status=Completed | Shows celebration overlay |
| Puzzle | Status=Error | Shows error screen |
| Profile | isAnonymous=true | Hides account section, shows "Create Account" |
| Groups | Empty list | Shows empty state with CTA buttons |
| Group Leaderboard | Empty | Shows "No one has played..." message |

---

This comprehensive guide covers all 15+ screens, 100+ interactive elements, visible text strings, button states, navigation flows, and conditional UI rendering. Use this as your master reference for writing Maestro E2E tests.

---

