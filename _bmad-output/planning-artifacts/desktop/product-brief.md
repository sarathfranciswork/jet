---
stepsCompleted: ['complete']
date: 2026-03-19
author: Franc
type: product-brief
---

# Product Brief: Jet Desktop + Marketing Landing Page

## Executive Summary

Jet Desktop is an Electron-based desktop application that delivers the complete Jet project management experience as a native app for macOS, Windows, and Linux. It connects to the same Jet backend API as the web version, ensuring seamless data sync — users can switch between desktop and web without losing any state.

Additionally, a marketing landing page will be built at the root URL to showcase Jet's features, provide download links for all platforms, and link to the web application.

## Vision

**"Jet everywhere — browser, desktop, every platform."**

Give teams the choice of how they access Jet. Power users get native OS integration (notifications, menu bar, keyboard shortcuts, offline-ready architecture), while the web version remains the primary access point. Both share the same backend, same data, same real-time state.

## Problem Statement

1. **Browser tab fatigue**: Project management tools compete with dozens of other tabs. A dedicated desktop app stays accessible via Cmd+Tab / Alt+Tab.
2. **Native notifications**: Browser notifications are unreliable and often blocked. Desktop apps get OS-level notification privileges.
3. **Offline resilience**: Desktop apps can cache data and show stale content when offline, unlike web apps that show blank screens.
4. **Professional perception**: A downloadable desktop app signals product maturity and commitment to enterprise users.
5. **No marketing presence**: Jet currently has no public-facing landing page — new users land directly on the login screen with no context about the product.

## Target Users

- **Existing Jet web users** who want a dedicated app experience
- **Engineering teams** that prefer desktop tools (similar to how many use Slack desktop vs web)
- **Enterprise IT** that wants to deploy a managed desktop app
- **Prospective users** who discover Jet and need a landing page to understand the product before signing up

## Scope

### Jet Desktop (Electron App)

| Feature | Description |
|---------|-------------|
| **Full feature parity** | Every feature in the web app works identically in the desktop app |
| **Same backend** | Connects to the same Django API — no separate backend |
| **Cross-platform** | macOS (.dmg), Windows (.exe/.msi), Linux (.AppImage/.deb) |
| **Native notifications** | OS-level notifications for mentions, assignments, updates |
| **System tray** | Tray icon with quick actions and unread count badge |
| **Deep linking** | `jet://` protocol handler for opening issues from external links |
| **Auto-update** | Automatic updates via electron-updater + GitHub Releases |
| **Keyboard shortcuts** | OS-native shortcuts (Cmd+Q, Cmd+W, etc.) |
| **Window management** | Remember window size/position, multiple windows |

### Marketing Landing Page

| Feature | Description |
|---------|-------------|
| **Hero section** | Bold headline, product screenshot, CTA buttons |
| **Feature showcase** | Visual cards highlighting key capabilities |
| **Download section** | Platform-specific download buttons with auto-detection |
| **Web app link** | Direct link to the hosted web application |
| **Responsive** | Works on mobile, tablet, desktop |
| **Dark theme** | Matches Jet's dark-first aesthetic |

## Architecture Decision: Electron Shell + Existing Web App

The desktop app is an **Electron shell** that loads the existing Next.js web application. This means:

- **Zero code duplication** — the web app code runs as-is inside Electron
- **Automatic feature parity** — any feature added to the web app instantly works in desktop
- **Single codebase** — the Electron layer is thin (~500 lines), just providing native OS integration
- **Same API** — desktop connects to the same backend URL as the web browser

### Architecture Diagram

```
┌─────────────────────────────────────────┐
│           Jet Desktop (Electron)         │
│  ┌─────────────────────────────────┐    │
│  │     BrowserWindow (Renderer)     │    │
│  │  ┌───────────────────────────┐  │    │
│  │  │   Next.js Web App         │  │    │
│  │  │   (loaded from server URL)│  │    │
│  │  └───────────────────────────┘  │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────┐ ┌───────────────┐  │
│  │  Main Process   │ │ System Tray   │  │
│  │  - Auto-update  │ │ - Quick menu  │  │
│  │  - Deep links   │ │ - Badge count │  │
│  │  - Notifications│ │               │  │
│  └─────────────────┘ └───────────────┘  │
└────────────────────┬────────────────────┘
                     │ HTTPS
          ┌──────────▼──────────┐
          │   Jet API Server    │
          │   (Same backend)    │
          └─────────────────────┘
```

## Success Criteria

1. Desktop app installs and runs on macOS 12+, Windows 10+, Ubuntu 20.04+
2. Every feature in the web app works in the desktop app
3. Auto-update works via GitHub Releases
4. System tray shows notification badge
5. Landing page loads in under 2 seconds, scores 90+ on Lighthouse
6. Download buttons correctly detect user's OS and offer the right installer

## Non-Functional Requirements

- **Bundle size**: < 100MB installer (excluding Electron runtime)
- **Startup time**: < 3 seconds to show the app window
- **Memory usage**: < 300MB RAM baseline
- **Auto-update**: Silent background download, prompt to restart
- **Code signing**: macOS notarization, Windows Authenticode (future)

## Out of Scope (v1)

- Offline mode with local database (future feature)
- End-to-end encryption
- Mobile apps (iOS/Android)
- Custom protocol handler registration on Linux (varies by distro)
