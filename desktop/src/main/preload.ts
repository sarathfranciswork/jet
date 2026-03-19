import { contextBridge, ipcRenderer } from "electron";

/**
 * Preload script for Jet Desktop.
 * Exposes a safe API to the renderer process via window.jetDesktop.
 */

contextBridge.exposeInMainWorld("jetDesktop", {
  /** Whether the app is running in the desktop wrapper */
  isDesktop: true,

  /** The current platform: 'darwin', 'win32', or 'linux' */
  platform: process.platform,

  /** Show a native OS notification */
  showNotification: (title: string, body: string): void => {
    ipcRenderer.send("show-notification", { title, body });
  },

  /** Set the dock/taskbar badge count (macOS dock badge, Windows overlay) */
  setBadgeCount: (count: number): void => {
    ipcRenderer.send("set-badge-count", count);
  },

  /** Get the app version */
  getVersion: (): Promise<string> => {
    return ipcRenderer.invoke("get-version");
  },

  /** Navigate to a specific path within Jet */
  navigateTo: (path: string): void => {
    ipcRenderer.send("navigate-to", path);
  },

  /** Listen for navigation events (e.g., from deep links or menu) */
  onNavigate: (callback: (path: string) => void): void => {
    ipcRenderer.on("navigate", (_event, path: string) => {
      callback(path);
    });
  },

  /** Check for app updates */
  checkForUpdates: (): void => {
    ipcRenderer.send("check-for-updates");
  },

  /** Listen for update available event */
  onUpdateAvailable: (callback: (info: unknown) => void): void => {
    ipcRenderer.on("update-available", (_event, info) => {
      callback(info);
    });
  },

  /** Listen for update downloaded event */
  onUpdateDownloaded: (callback: (info: unknown) => void): void => {
    ipcRenderer.on("update-downloaded", (_event, info) => {
      callback(info);
    });
  },

  /** Install downloaded update and restart */
  installUpdate: (): void => {
    ipcRenderer.send("install-update");
  },
});
