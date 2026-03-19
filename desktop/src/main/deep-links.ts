import { app, BrowserWindow } from "electron";
import log from "electron-log";

const PROTOCOL = "jet";

/**
 * Register the jet:// deep link protocol.
 * Must be called before app 'ready' event on some platforms.
 */
export function registerDeepLinks(): void {
  if (process.defaultApp) {
    // In development, register the protocol with the path to electron
    if (process.argv.length >= 2) {
      app.setAsDefaultProtocolClient(PROTOCOL, process.execPath, [
        process.argv[1],
      ]);
    }
  } else {
    app.setAsDefaultProtocolClient(PROTOCOL);
  }

  log.info(`Registered deep link protocol: ${PROTOCOL}://`);
}

/**
 * Parse a jet:// deep link URL and navigate the main window.
 *
 * Supported formats:
 *   jet://workspace/project/issues/123   -> /workspace/project/issues/123
 *   jet://workspace/project/cycles       -> /workspace/project/cycles
 *   jet://workspace/project/modules      -> /workspace/project/modules
 *   jet://workspace/settings             -> /workspace/settings
 *   jet://open                           -> just focus the window
 *
 * @param url The full jet:// URL
 * @param mainWindow The main BrowserWindow instance
 * @param webUrl The base web URL
 */
export function handleDeepLink(
  url: string,
  mainWindow: BrowserWindow,
  webUrl: string
): void {
  log.info(`Handling deep link: ${url}`);

  try {
    // Parse the URL: jet://workspace/project/issues/123
    // URL constructor expects a valid scheme, jet:// works
    const parsed = new URL(url);

    // The hostname is the first path segment (workspace slug)
    // The pathname contains the rest
    const workspace = parsed.hostname;
    const pathParts = parsed.pathname;

    if (!workspace || workspace === "open") {
      // Just focus the window
      showAndFocus(mainWindow);
      return;
    }

    // Construct the web URL path
    const webPath = `/${workspace}${pathParts}`;
    const targetUrl = `${webUrl}${webPath}`;

    log.info(`Deep link navigating to: ${targetUrl}`);

    showAndFocus(mainWindow);

    mainWindow.loadURL(targetUrl).catch((err: Error) => {
      log.error(`Failed to navigate via deep link: ${err.message}`);
    });
  } catch (err) {
    log.error(`Failed to parse deep link URL: ${url}`, err);
    showAndFocus(mainWindow);
  }
}

function showAndFocus(mainWindow: BrowserWindow): void {
  if (mainWindow.isMinimized()) {
    mainWindow.restore();
  }
  mainWindow.show();
  mainWindow.focus();
}
