---
date: 2026-03-19
author: Franc
type: architecture
---

# Architecture: Jet Desktop + Marketing Landing Page

## 1. Electron App Architecture

### 1.1 Directory Structure

```
desktop/
├── package.json
├── electron-builder.yml          # Build config for all platforms
├── tsconfig.json
├── src/
│   ├── main/
│   │   ├── index.ts              # Main process entry
│   │   ├── window-manager.ts     # Window creation/management
│   │   ├── tray.ts               # System tray integration
│   │   ├── auto-updater.ts       # electron-updater config
│   │   ├── deep-links.ts         # jet:// protocol handler
│   │   ├── notifications.ts     # Native notification bridge
│   │   ├── menu.ts               # Application menu bar
│   │   └── preload.ts            # Preload script for IPC
│   └── renderer/
│       └── index.html            # Shell HTML that loads web app
├── assets/
│   ├── icon.icns                 # macOS icon
│   ├── icon.ico                  # Windows icon
│   ├── icon.png                  # Linux icon (512x512)
│   └── tray-icon.png             # System tray icon (16x16/22x22)
└── build/                        # Build output
```

### 1.2 Main Process (`src/main/index.ts`)

```typescript
// Core responsibilities:
// 1. Create BrowserWindow pointing to WEB_APP_URL
// 2. Set up system tray with menu
// 3. Handle deep links (jet:// protocol)
// 4. Configure auto-updater
// 5. Bridge native notifications from web app via IPC

const WEB_APP_URL = process.env.JET_WEB_URL || 'http://34.55.60.88';
```

### 1.3 Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Renderer content | Load remote URL | Zero code duplication, instant feature parity |
| IPC usage | Minimal — notifications, tray badge | Keep the shell thin |
| Build tool | electron-builder | Best cross-platform support, auto-update |
| Auto-update | electron-updater + GitHub Releases | Free, no infrastructure needed |
| Package format | DMG (mac), NSIS (win), AppImage+deb (linux) | Standard formats per platform |

### 1.4 IPC Bridge

The preload script exposes a minimal API to the web app:

```typescript
// preload.ts
contextBridge.exposeInMainWorld('jetDesktop', {
  isDesktop: true,
  platform: process.platform,
  showNotification: (title: string, body: string) => ipcRenderer.send('show-notification', { title, body }),
  setBadgeCount: (count: number) => ipcRenderer.send('set-badge-count', count),
  getVersion: () => ipcRenderer.invoke('get-version'),
});
```

### 1.5 Auto-Update Flow

```
App starts → Check for updates (GitHub Releases API)
         → Download update in background
         → Show "Update available" notification
         → User clicks "Restart" → Install and relaunch
```

## 2. Landing Page Architecture

### 2.1 Technology

- **Framework**: Static HTML/CSS/JS (no framework needed — it's a single marketing page)
- **Location**: `landing/` directory in the monorepo
- **Hosting**: Served by nginx as the root `/` route, before the web app
- **Design**: Dark theme matching Jet's aesthetic, responsive

### 2.2 Directory Structure

```
landing/
├── index.html              # Single-page marketing site
├── css/
│   └── style.css           # Tailwind-built styles
├── js/
│   └── main.js             # OS detection, smooth scroll, animations
├── images/
│   ├── hero-screenshot.png # App screenshot for hero section
│   ├── jet-logo.svg        # Logo
│   └── features/           # Feature illustration images
└── downloads/              # Symlinks to latest releases (or redirect)
```

### 2.3 Sections

1. **Navigation**: Logo, "Features", "Download", "Web App" links
2. **Hero**: Headline + subheadline + screenshot + CTA buttons
3. **Features**: 6 feature cards with icons (Issues, Cycles, Modules, Views, Pages, Analytics)
4. **GitHub Integration**: Showcase the sync feature
5. **Desktop App**: Platform screenshots + download buttons
6. **Footer**: Links, copyright

### 2.4 OS Detection for Downloads

```javascript
function detectOS() {
  const ua = navigator.userAgent;
  if (ua.includes('Mac')) return 'macos';
  if (ua.includes('Win')) return 'windows';
  if (ua.includes('Linux')) return 'linux';
  return 'unknown';
}
```

## 3. Build & Release Pipeline

### 3.1 GitHub Actions Workflow

```yaml
# .github/workflows/build-desktop.yml
name: Build Jet Desktop
on:
  push:
    tags: ['v*']  # Trigger on version tags
jobs:
  build:
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: cd desktop && npm ci
      - run: cd desktop && npm run build
      - uses: softprops/action-gh-release@v2
        with:
          files: desktop/build/*
```

## 4. nginx Configuration Changes

```nginx
# Add landing page as root, web app under /app
location = / {
    root /app/landing;
    try_files /index.html =404;
}

location /css/ {
    root /app/landing;
}

location /js/ {
    root /app/landing;
}

location /images/ {
    root /app/landing;
}

# Existing web app routes remain unchanged
location / {
    proxy_pass http://web:3000;
}
```
