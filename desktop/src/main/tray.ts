import {
  app,
  Tray,
  Menu,
  nativeImage,
  BrowserWindow,
  ipcMain,
  Notification,
} from "electron";
import path from "path";
import log from "electron-log";
import { appState } from "./app-state";

let tray: Tray | null = null;

export function createTray(
  mainWindow: BrowserWindow,
  webUrl: string
): void {
  const iconPath = getTrayIconPath();
  const icon = nativeImage.createFromPath(iconPath);

  // On macOS, template images are used for the menu bar
  if (process.platform === "darwin") {
    icon.setTemplateImage(true);
  }

  tray = new Tray(icon);
  tray.setToolTip("Jet — Project Management");

  const contextMenu = Menu.buildFromTemplate([
    {
      label: "Open Jet",
      click: (): void => {
        showMainWindow(mainWindow);
      },
    },
    {
      label: "New Issue",
      click: (): void => {
        showMainWindow(mainWindow);
        mainWindow.webContents
          .executeJavaScript(
            `
          const btn = document.querySelector('[data-testid="create-issue-btn"]') ||
                      document.querySelector('button[title="New Issue"]');
          if (btn) btn.click();
        `
          )
          .catch((err: Error) => {
            log.warn("Could not trigger New Issue from tray:", err.message);
          });
      },
    },
    { type: "separator" },
    {
      label: "Quit Jet",
      click: (): void => {
        appState.isQuitting = true;
        app.quit();
      },
    },
  ]);

  tray.setContextMenu(contextMenu);

  // Double-click on tray icon opens the window
  tray.on("double-click", () => {
    showMainWindow(mainWindow);
  });

  // Handle badge count from renderer
  ipcMain.on("set-badge-count", (_event, count: number) => {
    setBadgeCount(count);
  });

  // Handle show notification from renderer
  ipcMain.on(
    "show-notification",
    (_event, { title, body }: { title: string; body: string }) => {
      showNativeNotification(title, body, mainWindow);
    }
  );

  // Handle get-version request
  ipcMain.handle("get-version", () => {
    return app.getVersion();
  });

  // Handle navigate-to request
  ipcMain.on("navigate-to", (_event, navPath: string) => {
    const url = `${webUrl}${navPath}`;
    mainWindow.loadURL(url).catch((err: Error) => {
      log.error(`Failed to navigate to ${url}:`, err.message);
    });
  });

  log.info("System tray created");
}

export function destroyTray(): void {
  if (tray) {
    tray.destroy();
    tray = null;
  }
}

function showMainWindow(mainWindow: BrowserWindow): void {
  if (mainWindow.isMinimized()) {
    mainWindow.restore();
  }
  mainWindow.show();
  mainWindow.focus();
}

function getTrayIconPath(): string {
  const assetsDir = path.join(__dirname, "../../assets");

  if (process.platform === "darwin") {
    // macOS uses template images (automatically handles dark/light mode)
    return path.join(assetsDir, "tray-iconTemplate.png");
  } else if (process.platform === "win32") {
    return path.join(assetsDir, "tray-icon.png");
  } else {
    return path.join(assetsDir, "tray-icon.png");
  }
}

function setBadgeCount(count: number): void {
  if (process.platform === "darwin") {
    // macOS dock badge
    app.setBadgeCount(count);
  } else if (process.platform === "win32") {
    // Windows doesn't have a built-in badge, but we can set overlay icon
    // This is handled in the main window
    log.info(`Badge count set to ${count} (Windows overlay not implemented)`);
  }

  // Update tray tooltip with count
  if (tray) {
    const tooltip =
      count > 0
        ? `Jet — ${count} unread notification${count !== 1 ? "s" : ""}`
        : "Jet — Project Management";
    tray.setToolTip(tooltip);
  }
}

function showNativeNotification(
  title: string,
  body: string,
  mainWindow: BrowserWindow
): void {
  if (!Notification.isSupported()) {
    log.warn("Notifications not supported on this platform");
    return;
  }

  const notification = new Notification({
    title,
    body,
    icon: path.join(__dirname, "../../assets/icon.png"),
  });

  notification.on("click", () => {
    showMainWindow(mainWindow);
  });

  notification.show();
}
