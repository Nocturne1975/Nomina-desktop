const { app, BrowserWindow } = require('electron');
const path = require('path');
const { startLocalApi } = require('./localApi.cjs');

const isDev = !app.isPackaged;

let apiHandle = null;

async function ensureLocalApi() {
  try {
    apiHandle = await startLocalApi({ port: 3000 });
    console.log(`[offline-api] OK sur http://localhost:${apiHandle.port}`);
  } catch (e) {
    if (e && e.code === 'EADDRINUSE') {
      console.log('[offline-api] Port 3000 déjà utilisé, skip.');
      return;
    }
    console.error('[offline-api] Impossible de démarrer:', e);
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs'),
    },
  });

  if (isDev) {
    win.loadURL(process.env.VITE_DEV_SERVER_URL || 'http://localhost:5173');
    if (process.env.ELECTRON_OPEN_DEVTOOLS === '1') {
      win.webContents.openDevTools({ mode: 'detach' });
    }
  } else {
    win.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
  }
}

app.whenReady().then(async () => {
  await ensureLocalApi();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('before-quit', () => {
  try { apiHandle?.close?.(); } catch {}
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
