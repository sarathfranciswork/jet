import {
  app,
  Menu,
  MenuItemConstructorOptions,
  BrowserWindow,
  dialog,
  shell,
} from "electron";
import log from "electron-log";

export function createMenu(
  mainWindow: BrowserWindow,
  webUrl: string
): void {
  const isMac = process.platform === "darwin";

  const template: MenuItemConstructorOptions[] = [
    // App menu (macOS only)
    ...(isMac
      ? [
          {
            label: app.getName(),
            submenu: [
              {
                label: "About Jet",
                click: (): void => {
                  showAboutDialog();
                },
              },
              { type: "separator" as const },
              {
                label: "Settings...",
                accelerator: "CmdOrCtrl+," as const,
                click: (): void => {
                  navigateTo(mainWindow, webUrl, "/profile");
                },
              },
              { type: "separator" as const },
              { role: "services" as const },
              { type: "separator" as const },
              { role: "hide" as const },
              { role: "hideOthers" as const },
              { role: "unhide" as const },
              { type: "separator" as const },
              { role: "quit" as const },
            ],
          } as MenuItemConstructorOptions,
        ]
      : []),

    // File menu
    {
      label: "File",
      submenu: [
        {
          label: "New Issue",
          accelerator: "CmdOrCtrl+N",
          click: (): void => {
            // Inject a click on the "New Issue" button or navigate
            mainWindow.webContents
              .executeJavaScript(
                `
              const btn = document.querySelector('[data-testid="create-issue-btn"]') ||
                          document.querySelector('button[title="New Issue"]');
              if (btn) btn.click();
              else window.location.href = window.location.origin;
            `
              )
              .catch((err: Error) => {
                log.warn("Could not trigger New Issue:", err.message);
              });
          },
        },
        { type: "separator" },
        {
          label: "Dashboard",
          accelerator: "CmdOrCtrl+D",
          click: (): void => {
            navigateTo(mainWindow, webUrl, "/");
          },
        },
        { type: "separator" },
        ...(isMac
          ? [{ role: "close" as const }]
          : [
              {
                label: "Settings",
                accelerator: "CmdOrCtrl+,",
                click: (): void => {
                  navigateTo(mainWindow, webUrl, "/profile");
                },
              },
              { type: "separator" as const },
              { role: "quit" as const },
            ]),
      ],
    },

    // Edit menu
    {
      label: "Edit",
      submenu: [
        { role: "undo" },
        { role: "redo" },
        { type: "separator" },
        { role: "cut" },
        { role: "copy" },
        { role: "paste" },
        { role: "pasteAndMatchStyle" },
        { role: "delete" },
        { role: "selectAll" },
        ...(isMac
          ? [
              { type: "separator" as const },
              {
                label: "Speech",
                submenu: [
                  { role: "startSpeaking" as const },
                  { role: "stopSpeaking" as const },
                ],
              },
            ]
          : []),
      ],
    },

    // View menu
    {
      label: "View",
      submenu: [
        { role: "reload" },
        { role: "forceReload" },
        { role: "toggleDevTools" },
        { type: "separator" },
        { role: "resetZoom" },
        { role: "zoomIn" },
        { role: "zoomOut" },
        { type: "separator" },
        { role: "togglefullscreen" },
      ],
    },

    // Window menu
    {
      label: "Window",
      submenu: [
        { role: "minimize" },
        { role: "zoom" },
        ...(isMac
          ? [
              { type: "separator" as const },
              { role: "front" as const },
              { type: "separator" as const },
              { role: "window" as const },
            ]
          : [{ role: "close" as const }]),
      ],
    },

    // Help menu
    {
      label: "Help",
      submenu: [
        {
          label: "Jet Documentation",
          click: (): void => {
            shell.openExternal("https://docs.plane.so");
          },
        },
        {
          label: "Report Issue",
          click: (): void => {
            shell.openExternal(
              "https://github.com/jet-pm/jet/issues/new"
            );
          },
        },
        { type: "separator" },
        {
          label: "About Jet",
          click: (): void => {
            showAboutDialog();
          },
        },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
  log.info("Application menu created");
}

function navigateTo(
  mainWindow: BrowserWindow,
  webUrl: string,
  path: string
): void {
  const url = `${webUrl}${path}`;
  mainWindow.loadURL(url).catch((err: Error) => {
    log.error(`Failed to navigate to ${url}:`, err.message);
  });
}

function showAboutDialog(): void {
  dialog.showMessageBox({
    type: "info",
    title: "About Jet",
    message: "Jet",
    detail: `Version ${app.getVersion()}\n\nProject management, redefined.\n\nBuilt with Electron ${process.versions.electron}\nChromium ${process.versions.chrome}\nNode.js ${process.versions.node}`,
    buttons: ["OK"],
  });
}
