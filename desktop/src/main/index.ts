import { app, BrowserWindow, shell } from "electron";
import path from "path";
import log from "electron-log";
import Store from "electron-store";
import { createMenu } from "./menu";
import { createTray, destroyTray } from "./tray";
import { setupAutoUpdater } from "./auto-updater";
import { registerDeepLinks, handleDeepLink } from "./deep-links";
import { appState } from "./app-state";

// Configure logging
log.transports.file.level = "info";
log.transports.console.level = "debug";
log.info("Jet Desktop starting...");

// App constants
const DEFAULT_WEB_URL = "http://34.55.60.88";
const WEB_URL = process.env.JET_WEB_URL || DEFAULT_WEB_URL;

// Window state store
interface WindowState {
  width: number;
  height: number;
  x?: number;
  y?: number;
  isMaximized: boolean;
}

const store = new Store<{ windowState: WindowState }>({
  defaults: {
    windowState: {
      width: 1280,
      height: 800,
      isMaximized: false,
    },
  },
});

let mainWindow: BrowserWindow | null = null;

function getWindowState(): WindowState {
  return store.get("windowState");
}

function saveWindowState(): void {
  if (!mainWindow) return;

  const isMaximized = mainWindow.isMaximized();

  if (!isMaximized) {
    const bounds = mainWindow.getBounds();
    store.set("windowState", {
      width: bounds.width,
      height: bounds.height,
      x: bounds.x,
      y: bounds.y,
      isMaximized: false,
    });
  } else {
    const current = getWindowState();
    store.set("windowState", {
      ...current,
      isMaximized: true,
    });
  }
}

function createMainWindow(): BrowserWindow {
  const windowState = getWindowState();

  const windowOptions: Electron.BrowserWindowConstructorOptions = {
    width: windowState.width,
    height: windowState.height,
    minWidth: 900,
    minHeight: 600,
    show: false,
    title: "Jet",
    titleBarStyle: process.platform === "darwin" ? "hiddenInset" : "default",
    trafficLightPosition: { x: 15, y: 15 },
    backgroundColor: "#09090B",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true,
      spellcheck: true,
    },
  };

  // Restore position if available
  if (windowState.x !== undefined && windowState.y !== undefined) {
    windowOptions.x = windowState.x;
    windowOptions.y = windowState.y;
  }

  // Set icon for Linux/Windows
  if (process.platform !== "darwin") {
    windowOptions.icon = path.join(__dirname, "../../assets/icon.png");
  }

  const win = new BrowserWindow(windowOptions);

  // Restore maximized state
  if (windowState.isMaximized) {
    win.maximize();
  }

  // Load the loading screen first, then redirect to the web app
  const loadingPagePath = path.join(
    __dirname,
    "../renderer/index.html"
  );
  win.loadFile(loadingPagePath);

  // Once the loading page is ready, navigate to the web app
  win.webContents.once("did-finish-load", () => {
    log.info(`Loading Jet web app from: ${WEB_URL}`);
    win.loadURL(WEB_URL).catch((err) => {
      log.error("Failed to load web app:", err);
      // Show reconnecting message via the loading page
      win.loadFile(loadingPagePath).then(() => {
        win.webContents.executeJavaScript(`
          document.getElementById('loading-text').textContent = 'Unable to connect to Jet. Retrying...';
          document.getElementById('loading-subtext').textContent = 'Please check your network connection.';
        `).catch(() => {});
      });
      // Retry after a delay
      scheduleRetry(win);
    });
  });

  // Handle load failures (e.g., server unreachable after initial load)
  win.webContents.on("did-fail-load", (_event, errorCode, errorDescription) => {
    if (errorCode === -3) return; // Ignore ERR_ABORTED (navigating away during load)
    log.error(`Page load failed: ${errorDescription} (${errorCode})`);
    win.loadFile(loadingPagePath).then(() => {
      win.webContents.executeJavaScript(`
        document.getElementById('loading-text').textContent = 'Connection lost. Reconnecting...';
        document.getElementById('loading-subtext').textContent = '${errorDescription}';
      `).catch(() => {});
    });
    scheduleRetry(win);
  });

  // Show window when ready
  win.once("ready-to-show", () => {
    win.show();
    win.focus();
  });

  // Save window state on changes
  win.on("resize", saveWindowState);
  win.on("move", saveWindowState);
  win.on("maximize", saveWindowState);
  win.on("unmaximize", saveWindowState);

  // Minimize to tray on close (macOS behavior)
  win.on("close", (event) => {
    if (process.platform === "darwin" && !appState.isQuitting) {
      event.preventDefault();
      win.hide();
    }
  });

  win.on("closed", () => {
    mainWindow = null;
  });

  // Open external links in default browser
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("http") && !url.startsWith(WEB_URL)) {
      shell.openExternal(url);
      return { action: "deny" };
    }
    return { action: "allow" };
  });

  // Handle navigation to external URLs
  win.webContents.on("will-navigate", (event, url) => {
    if (!url.startsWith(WEB_URL) && !url.startsWith("file://")) {
      event.preventDefault();
      shell.openExternal(url);
    }
  });

  return win;
}

let retryTimeout: ReturnType<typeof setTimeout> | null = null;

function scheduleRetry(win: BrowserWindow): void {
  if (retryTimeout) {
    clearTimeout(retryTimeout);
  }
  retryTimeout = setTimeout(() => {
    if (win && !win.isDestroyed()) {
      log.info("Retrying connection to Jet...");
      win.loadURL(WEB_URL).catch((err) => {
        log.error("Retry failed:", err);
        scheduleRetry(win);
      });
    }
  }, 5000);
}

// Single instance lock
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  log.info("Another instance is already running. Quitting.");
  app.quit();
} else {
  app.on("second-instance", (_event, commandLine) => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.show();
      mainWindow.focus();
    }

    // Handle deep link from second instance (Windows)
    const deepLink = commandLine.find((arg) => arg.startsWith("jet://"));
    if (deepLink && mainWindow) {
      handleDeepLink(deepLink, mainWindow, WEB_URL);
    }
  });

  app.on("ready", async () => {
    log.info("App ready");

    // Register deep link protocol
    registerDeepLinks();

    // Create main window
    mainWindow = createMainWindow();

    // Create application menu
    createMenu(mainWindow, WEB_URL);

    // Create system tray
    createTray(mainWindow, WEB_URL);

    // Setup auto-updater
    setupAutoUpdater(mainWindow);

    // Handle deep link on startup (macOS)
    app.on("open-url", (_event, url) => {
      if (mainWindow) {
        handleDeepLink(url, mainWindow, WEB_URL);
      }
    });
  });

  app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
      app.quit();
    }
  });

  app.on("activate", () => {
    if (mainWindow) {
      mainWindow.show();
      mainWindow.focus();
    } else {
      mainWindow = createMainWindow();
      createMenu(mainWindow, WEB_URL);
    }
  });

  app.on("before-quit", () => {
    appState.isQuitting = true;
    destroyTray();
    if (retryTimeout) {
      clearTimeout(retryTimeout);
    }
  });
}
