const ipc = require('electron').ipcRenderer

// close app
function closeApp() {
  ipc.send('close')
}

function minimizeApp() {
  ipc.send('minimize')
}