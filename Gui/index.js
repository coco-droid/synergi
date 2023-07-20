const { app, BrowserWindow, screen } = require('electron')
const childProcess = require('child_process')
const path = require('path');
const fs = require('fs');
const currentDir = __dirname; 
const serverPath = path.join(currentDir, '../core/server.py');
fs.chmodSync(serverPath, 0o755); 
const backendProcess = childProcess.spawn('python3', [serverPath]);
function createWindow () {
    backendProcess.stdout.on('data', data => {
        console.log(data.toString()) 
      })
    
    
    // Create the browser window.
    let win = new BrowserWindow({
        width: 400,
        height: screen.getPrimaryDisplay().workAreaSize.height,
        transparent: true,
        frame: false,
        x: screen.getPrimaryDisplay().workAreaSize.width - 400, // Add this line to set the window to the right of the screen
        y: 0, // Add this line to set the window to the top of the screen
        webPreferences: {
            nodeIntegration: true
        }

    })

    // Load the index.html of the app.
    win.loadFile('./public/index.html')

    // Open the DevTools.
    win.webContents.openDevTools()

    // Display the index.html when the window is ready
    win.once('ready-to-show', () => {
        win.show()
    })
    
    // Slide right appear transition
    win.webContents.on('did-finish-load', () => {
        win.webContents.executeJavaScript(`
            document.body.style.opacity = 0;
            document.body.style.transition = "opacity 0.5s ease-in-out";
            setTimeout(() => {
                document.body.style.opacity = 1;
            }, 100);
        `)
    })
}

app.whenReady().then(() => {
    createWindow()

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow()
        }
    })
})

app.on('window-all-closed', () => {
    backendProcess.kill() 
    if (process.platform !== 'darwin') {
        app.quit()
    }
})
