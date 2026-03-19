---
date: 2026-03-19
author: Franc
type: epics-and-stories
---

# Epics & Stories: Jet Desktop + Marketing Landing Page

## Epic 1: Electron App Core Shell

### Story 1.1: Project Scaffold
- Initialize `desktop/` directory with package.json, tsconfig, electron-builder.yml
- Install dependencies: electron, electron-builder, electron-updater, typescript
- Set up build scripts for dev and production

### Story 1.2: Main Process — Window Manager
- Create main process that opens a BrowserWindow
- Load the Jet web app URL (configurable via env var)
- Handle window lifecycle (close, minimize, restore)
- Remember window size and position between sessions
- Set application icon for all platforms

### Story 1.3: Preload Script & IPC Bridge
- Create preload script with contextBridge
- Expose `window.jetDesktop` API: isDesktop, platform, showNotification, setBadgeCount, getVersion
- Set up IPC handlers in main process

### Story 1.4: Application Menu
- Create native menu bar (File, Edit, View, Window, Help)
- Add Jet-specific menu items (New Issue, Dashboard, Settings)
- Keyboard shortcuts: Cmd/Ctrl+N (new issue), Cmd/Ctrl+, (settings)
- About dialog with version info

### Story 1.5: System Tray
- Create system tray icon with context menu
- Menu items: Open Jet, New Issue, separator, Quit
- Badge count on tray icon (macOS dock badge, Windows overlay icon)

## Epic 2: Native OS Integration

### Story 2.1: Native Notifications
- Bridge web app notifications to OS-level notifications
- Click notification → focus app and navigate to relevant issue
- Notification preferences respect web app settings

### Story 2.2: Deep Link Protocol
- Register `jet://` protocol handler
- Parse deep links: `jet://workspace/project/issue/123`
- Open app or focus existing window and navigate

### Story 2.3: Auto-Updater
- Configure electron-updater with GitHub Releases provider
- Check for updates on app start (silent)
- Show notification when update available
- Download in background, prompt to restart
- Verify update signature

## Epic 3: Cross-Platform Build & Packaging

### Story 3.1: macOS Build
- Configure electron-builder for DMG output
- Set app icon (.icns format, all sizes)
- Set app category, bundle ID (com.jetpm.desktop)
- Test on macOS 12+

### Story 3.2: Windows Build
- Configure electron-builder for NSIS installer
- Set app icon (.ico format)
- Configure install directory, start menu shortcuts
- Test on Windows 10+

### Story 3.3: Linux Build
- Configure electron-builder for AppImage and .deb
- Set app icon (.png 512x512)
- Create .desktop file with proper categories
- Test on Ubuntu 20.04+

### Story 3.4: GitHub Actions CI/CD
- Create workflow for building on all 3 platforms
- Trigger on version tags (v*)
- Upload artifacts to GitHub Releases
- Generate checksums for each artifact

## Epic 4: Marketing Landing Page

### Story 4.1: Page Structure & Hero Section
- Create `landing/` directory
- Build responsive HTML structure
- Hero section: headline "Ship faster with Jet", subheadline, product screenshot
- CTA buttons: "Try Jet Free" (→ web app), "Download Desktop" (→ download section)
- Dark theme matching Jet brand identity

### Story 4.2: Features Section
- 6 feature cards in responsive grid:
  - Issues & Tracking
  - Cycles & Sprints
  - Modules & Roadmaps
  - Custom Views & Filters
  - Pages & Documentation
  - Analytics & Insights
- Each with icon, title, description
- Subtle hover animations

### Story 4.3: Desktop App Section
- Platform showcase with download buttons
- Auto-detect user OS and highlight correct download
- Show all 3 platform options (macOS, Windows, Linux)
- App screenshots or mockup

### Story 4.4: GitHub Integration Section
- Showcase bidirectional sync feature
- Visual diagram of GitHub ↔ Jet flow
- Mention @claude automation

### Story 4.5: Footer & Navigation
- Sticky navigation with smooth scroll
- Footer with links: GitHub, Documentation, Web App
- "Built with Jet" branding

## Epic 5: Integration & Testing

### Story 5.1: Web App Desktop Detection
- Add `window.jetDesktop` detection in web app
- Conditionally show/hide browser-only UI elements
- Use native notifications when in desktop context

### Story 5.2: End-to-End Testing
- Test desktop app on macOS: install, launch, login, use features
- Test desktop app on Windows: install, launch, login, use features
- Test desktop app on Linux: install, launch, login, use features
- Verify auto-update flow
- Verify deep links
- Verify system tray

### Story 5.3: Landing Page Testing
- Test responsive layout on mobile, tablet, desktop
- Test download button OS detection
- Verify all links work
- Lighthouse performance audit (target 90+)

## Summary

| Epic | Stories | Estimated Effort |
|------|---------|-----------------|
| 1. Electron Core Shell | 5 | 2 days |
| 2. Native OS Integration | 3 | 1 day |
| 3. Cross-Platform Build | 4 | 1 day |
| 4. Marketing Landing Page | 5 | 1.5 days |
| 5. Integration & Testing | 3 | 1 day |
| **Total** | **20** | **~6.5 days** |
