// Preload script (optional). Expose safe APIs here if needed.
// const { contextBridge } = require('electron');
// contextBridge.exposeInMainWorld('api', { /* ... */ });
const { contextBridge } = require('electron');

contextBridge.exposeInMainWorld('NOMINA', {
  apiBaseUrl: 'http://localhost:3000',
});