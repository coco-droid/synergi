const { app, BrowserWindow, screen, Menu, Tray,ipcMain} = require('electron');
const childProcess = require('child_process');
const path = require('path');
const fs = require('fs');
let appTray = null;
let mainWindow = null;
const currentDir = __dirname;
const serverPath = path.join(currentDir, '../core/server.py');
fs.chmodSync(serverPath, 0o755);
const backendProcess = childProcess.spawn('python3', [serverPath]);
const appIconPath = path.join(__dirname, 'public/preview.png');

function createWindow() {
    backendProcess.stdout.on('data', data => {
        console.log(data.toString());
    });
    const primaryDisplay = screen.getPrimaryDisplay();
    
    // Create the browser window.
    let win = new BrowserWindow({
        width: 400,
        height: screen.getPrimaryDisplay().workAreaSize.height,
        transparent: true,
        frame: false,
        //show:false,
        x:screen.getPrimaryDisplay().workAreaSize.width - 400,
        y: 0,
        icon: path.join(__dirname, 'public/preview.png'),
        webPreferences: {
            nodeIntegration: true,
            contextIsolation:false,
        },
    });
    global.win =win;
    // Load the index.html of the app.
    win.loadFile('./public/index.html');

    // Open the DevTools.
    win.webContents.openDevTools();

    // Display the index.html when the window is ready
    win.once('ready-to-show', () => {
        win.show();
    });

    // Slide right appear transition
    win.webContents.on('did-finish-load', () => {
        win.webContents.executeJavaScript(`
            document.body.style.opacity = 0;
            document.body.style.transition = "opacity 0.5s ease-in-out";
            setTimeout(() => {
                document.body.style.opacity = 1;
            }, 100);
        `);
    });
    win.on('ready-to-show', () => {
        // Animation
        /*let position =400
        const step = 5
        const animationDuration = 500 // Durée de l'animation en millisecondes
    
        const slideOutAnimation = () => {
            position -= step
            if (position >= 0) {
              win.setBounds({ x: position })
              setTimeout(slideOutAnimation, animationDuration / (x / step))
            } else {
              win.show()
            }
          }
      
          setTimeout(() => {
            slideOutAnimation()
          }, 1000) // Délai de 1 seconde avant de commencer l'animation
        */
        })
        win.on('minimize', () => {
            mainWindow.hide()
          })
          
    // Define the menu bar
    const menu = Menu.buildFromTemplate([
        {
            label: 'App',
            submenu: [
                {
                    label: 'Launch',
                    click: () => {
                        win.show();
                    },
                },
                {
                    label: 'Send to Synergie', // Ajout de l'option dans le menu de l'application
                    click: () => sendToSynergy(), // Appel à la fonction pour envoyer à Synergie
                },
                {
                    label: 'Quit',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        backendProcess.kill();
                        app.quit();
                    },
                },
            ],
        },
    ]);
    Menu.setApplicationMenu(menu);
}

app.whenReady().then(() => {
    createWindow();
    
    appTray = new Tray(appIconPath);

    // Définissez un menu contextuel pour le tray icon (optionnel)
    const contextMenu = Menu.buildFromTemplate([
        { label: 'Open App', click: () => mainWindow.show() },
        { label: 'Quit', click: () => app.quit() },
    ]);
    appTray.setToolTip('Synergi');
    appTray.setContextMenu(contextMenu);
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });

    const menu = Menu.buildFromTemplate([
        {
            label: 'App',
            submenu: [
                {
                    label: 'Launch',
                    click: () => {
                        mainWindow.show();
                    },
                },
                {
                    label: 'Send to Synergie', // Ajout de l'option dans le menu de l'application
                    click: () => sendToSynergy(), // Appel à la fonction pour envoyer à Synergie
                },
                {
                    label: 'Quit',
                    accelerator: 'CmdOrCtrl+Q',
                    click: () => {
                        backendProcess.kill();
                        app.quit();
                    },
                },
            ],
        },
    ]);
    Menu.setApplicationMenu(menu);
});

function sendToSynergy() {
    console.log('send to synergi');
}

app.on('window-all-closed', () => {
    backendProcess.kill();
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
ipcMain.on('close', () => {
    app.quit()
  })
ipcMain.on('minimise',()=>{
    //minimize the window
    win.minimize();
})