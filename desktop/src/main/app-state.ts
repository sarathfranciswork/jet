/**
 * Shared application state for tracking quit behavior.
 * Used to differentiate between window close (hide) and app quit on macOS.
 */
export const appState = {
  isQuitting: false,
};
