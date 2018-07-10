const { app, BrowserWindow } = require('electron')
const url = require('url')
const path = require('path')


let win

function createWindow() {
    win = new BrowserWindow({ show: false, resizable: false, icon:'public/img/logo-1.png', frame: false })
	win.maximize()
	win.show()
    win.setMenu(null)
    
    win.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file:',
        slashes: true
    }))

    win.on('closed', _ => win = null);
}

app.on('ready', createWindow) 

app.on('window-all-closed', _ => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('settings', _ => {
    console.log(555555);
});

