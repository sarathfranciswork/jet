import { autoUpdater, UpdateInfo } from "electron-updater";
import { BrowserWindow, dialog, ipcMain, Notification } from "electron";
import log from "electron-log";

export function setupAutoUpdater(mainWindow: BrowserWindow): void {
  // Configure logging for auto-updater
  autoUpdater.logger = log;

  // Don't auto-download; let us control the flow
  autoUpdater.autoDownload = false;
  autoUpdater.autoInstallOnAppQuit = true;

  // Check for updates on startup (with a delay to not block app launch)
  setTimeout(() => {
    checkForUpdates();
  }, 10000);

  // Handle manual check from renderer
  ipcMain.on("check-for-updates", () => {
    checkForUpdates();
  });

  // Handle install request from renderer
  ipcMain.on("install-update", () => {
    autoUpdater.quitAndInstall(false, true);
  });

  // Update available
  autoUpdater.on("update-available", (info: UpdateInfo) => {
    log.info("Update available:", info.version);

    // Notify the renderer
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("update-available", {
        version: info.version,
        releaseDate: info.releaseDate,
      });
    }

    // Show notification
    if (Notification.isSupported()) {
      const notification = new Notification({
        title: "Jet Update Available",
        body: `Version ${info.version} is available. Downloading...`,
      });
      notification.show();
    }

    // Start downloading
    autoUpdater.downloadUpdate().catch((err) => {
      log.error("Failed to download update:", err);
    });
  });

  // Update not available
  autoUpdater.on("update-not-available", (info: UpdateInfo) => {
    log.info("No update available. Current version:", info.version);
  });

  // Download progress
  autoUpdater.on("download-progress", (progress) => {
    log.info(`Download progress: ${progress.percent.toFixed(1)}%`);
  });

  // Update downloaded
  autoUpdater.on("update-downloaded", (info: UpdateInfo) => {
    log.info("Update downloaded:", info.version);

    // Notify the renderer
    if (mainWindow && !mainWindow.isDestroyed()) {
      mainWindow.webContents.send("update-downloaded", {
        version: info.version,
        releaseDate: info.releaseDate,
      });
    }

    // Show dialog to restart
    dialog
      .showMessageBox(mainWindow, {
        type: "info",
        title: "Update Ready",
        message: `Jet ${info.version} has been downloaded.`,
        detail:
          "The update will be installed when you restart the application. Would you like to restart now?",
        buttons: ["Restart Now", "Later"],
        defaultId: 0,
        cancelId: 1,
      })
      .then((result) => {
        if (result.response === 0) {
          autoUpdater.quitAndInstall(false, true);
        }
      });
  });

  // Error handling
  autoUpdater.on("error", (err) => {
    log.error("Auto-updater error:", err);
  });
}

function checkForUpdates(): void {
  log.info("Checking for updates...");
  autoUpdater.checkForUpdates().catch((err) => {
    log.error("Failed to check for updates:", err);
  });
}
