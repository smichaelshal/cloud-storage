"use strict";

import { app, protocol, BrowserWindow, Menu, dialog, ipcMain } from "electron";
import { createProtocol } from "vue-cli-plugin-electron-builder/lib";
import installExtension, { VUEJS_DEVTOOLS } from "electron-devtools-installer";
const isDevelopment = process.env.NODE_ENV !== "production";
let win = null;
const fs = require("fs");

let isConnected = null;
let isFirstNotConnected = true;
let isFirstConnected = true;

const templateConnected = [
  {
    label: "User",
    submenu: [
      {
        label: "Logout",
        click() {
          win.webContents.send("menu", "logout");
        },
      },
      {
        label: "Change Password",
        click() {
          win.webContents.send("menu", "change-password");
        },
      },
    ],
  },
];

const templateNotConnected = [
  {
    label: "Actions",
    submenu: [{ role: "cut" }, { role: "copy" }, { role: "paste" }],
  },
  {
    label: "User",
    submenu: [
      {
        label: "Login",
        // accelerator: "CmdorCtrl+O",
        click() {
          // openFile();
          win.webContents.send("menu", "login");
        },
      },
      {
        label: "Register",
        click() {
          win.webContents.send("menu", "register");
        },
      },
      {
        label: "Forgot Password",
        click() {
          win.webContents.send("menu", "forgot-password");
        },
      },
    ],
  },
];

let template = templateNotConnected;

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { secure: true, standard: true } },
]);

const createWindow = async () => {
  // Create the browser window.
  win = new BrowserWindow({
    width: 800,
    height: 600,
    minWidth:800,
    minHeight: 600,
    // icon: __dirname + '/i1.icns',
    // title: 'mmm',
    webPreferences: {
      devTools: true,
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      // webSecurity: false
    },
  });

  let template = [];

  if (process.platform == "darwin") {
    template.unshift({
      label: app.name,
      submenu: [{ role: "about" }, { role: "quit" }],
    });
  }
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL);
    if (!process.env.IS_TEST) win.webContents.openDevTools();
  } else {
    createProtocol("app");
    // Load the index.html when not in development
    win.loadURL("app://./index.html");
  }

  win.webContents.send("menu", "?");
};

// Quit when all windows are closed.
app.on("window-all-closed", () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS_DEVTOOLS);
    } catch (e) {
      console.error("Vue Devtools failed to install:", e.toString());
    }
  }
  createWindow();
});

if (isDevelopment) {
  if (process.platform === "win32") {
    process.on("message", (data) => {
      if (data === "graceful-exit") {
        app.quit();
      }
    });
  } else {
    process.on("SIGTERM", () => {
      app.quit();
    });
  }
}

const openFile = () => {
  dialog
    .showOpenDialog(win, {
      properties: ["openFile", "openDirectory", "multiSelections"],
    })
    .then((files) => {
      const CHANNEL = "main";
      files.filePaths.forEach((path) => {
        win.webContents.send(CHANNEL, path);
      });
    });
};

const CHANNEL_NAME = "main";
const MESSAGE = "pong";

ipcMain.on("openFile", (event, data) => {
  openFile();
});

ipcMain.on("menu", (event, data) => {
  isConnected = data;
  let template = null;

  if (isConnected) {
    template = templateConnected;

    if (process.platform == "darwin" && isFirstConnected) {
      template.unshift({
        label: app.name,
        submenu: [{ role: "about" }, { role: "quit" }],
      });

      isFirstConnected = false;
    }
  } else {
    template = templateNotConnected;
    if (process.platform == "darwin" && isFirstNotConnected) {
      template.unshift({
        label: app.name,
        submenu: [{ role: "about" }, { role: "quit" }],
      });
      isFirstNotConnected = false;
    }
  }

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
});

const express = require("express");
const axios = require("axios");
const appExpress = express();
const WebSocket = require("ws");
const cors = require("cors");

let portListen = 3000;

// middleware
// appExpress.use(express.json());
// appExpress.use(express.urlencoded()); //body-parser
// appExpress.use(cors({ origin: "*" }));

//---------------------------------------------------------------------
// Server HTTP

import { uploadFileFromClient } from "./uploadServer";
import { downloadFileFromClient } from "./downloadServer";

const HOST = "http://localhost:8000/";
const HOST_WS = 'ws://localhost:8000/';

// appExpress.post("/upload/", (req, res) => {
//   const RES_DATA = req.body.data;
//   console.log("RES_DATA1: ", RES_DATA);
//   uploadFileFromClient(RES_DATA);
//   res.send("upload");
// });

ipcMain.on("uploadChannel", (event, data) => {
  const RES_DATA = data.data
  uploadFileFromClient(RES_DATA);
});
ipcMain.on("downloadChannel", (event, data) => {
  const RES_DATA = data.data
  downloadFileFromClient(RES_DATA);
});

// appExpress.post("/download/", (req, res) => {
//   // downloadFileFromClient(req, res);
//   const RES_DATA = req.body.data;
//   console.log("RES_DATA2: ", RES_DATA);
//   downloadFileFromClient(RES_DATA);
//   res.send("download");
// });

// appExpress.listen(portListen, () => console.log(`appExpress is running`));

export { HOST };
export { HOST_WS };
export { win };
