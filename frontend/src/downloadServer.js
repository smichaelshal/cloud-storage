const axios = require("axios");
const WebSocket = require("ws");
const path = require("path");
const fs = require("fs");
import { log } from "console";
import { HOST } from "./background";
import { HOST_WS } from "./background";
import { win } from "./background";


let timerID_Download = null;
let listDownload = [];
let listDownloadNow = [];

const downloadFileFromClient = (RES_DATA) => {
  const token = RES_DATA.token;
  const pathSource = RES_DATA.pathSource;
  const pathDestination = RES_DATA.pathDestination;
  const idFile = RES_DATA.idFile;
  const nameFile = RES_DATA.nameFile;
  const typeFile = RES_DATA.typeFile;
  const isDirectory = RES_DATA.isDirectory;

  if (isDirectory) {
    const body = {
      pathDestination: pathDestination,
      pathSource: pathSource,
    };
    sendToServerGetDirectoriesList(body, token);
    // createDir()
  } else {
    let downloadObjectData = {
      token: token,
      pathSource: pathSource,
      pathDestination: pathDestination,
      idFile: idFile,
      nameFile: nameFile,
      typeFile: typeFile,
    };

    listDownload.push(downloadObjectData);

    if (
      listDownload.length == 1 &&
      listDownloadNow.length == 0 &&
      !isDirectory
    ) {
      timerID_Download = setInterval(manageDownload, 1000);
    }
  }

  // downloadFile(token, pathSource, pathDestination, idFile, nameFile, typeFile);

  // res.send("download");
};

const downloadFile = (
  token,
  pathSource,
  pathDestination,
  idFile,
  nameFile,
  typeFile
) => {
  let msgResponse = "download";
  // let seekFile = req.body.data.seekFile;
  const pathDestinationFile = pathDestination + nameFile + "." + typeFile;
  let seekFile = 0;

  try {
    let fileFSDownload = fs.statSync(pathDestinationFile);
    seekFile = fileFSDownload.size;
  } catch (error) {
    seekFile = 0;
  }

  const ws = new WebSocket(HOST_WS + "ws/download/");
  ws.on("open", function open() {
    let dict = {
      token: token,
      pathSource: pathSource,
      pathDestination: pathDestination,
      idFile: idFile,
      seekFile: seekFile,
    };

    ws.send(JSON.stringify(dict));
  });

  ws.on("message", function incoming(data) {
    const flag = String.fromCharCode(data[0]);
    if (flag == "S") {
      ws.send("D" + seekFile.toString());
    } else if (flag == "C") {
      const newData = data.slice(1, data.length);

      fs.appendFileSync(pathDestinationFile, newData, (err) => {
        if (err) return console.log(err);
      });

      seekFile += newData.length;
      // console.log("seekFileDownload:", seekFile + '%');
      ws.send("D" + seekFile);
    } else if (flag == "E") {
      ws.close();
      listDownloadNow.shift();
    } else if (flag == "R") {
      console.log("ERROR");
      msgResponse = "error";
      ws.close();
      listDownloadNow.shift();
    }
  });
};

const flatten = (lists) => {
  return lists.reduce((a, b) => a.concat(b), []);
};

const getDirectories = (srcpath) => {
  return fs
    .readdirSync(srcpath)
    .map((file) => path.join(srcpath, file))
    .filter((path) => fs.statSync(path).isDirectory());
};

const getDirectoriesRecursive = (srcpath) => {
  return [
    srcpath,
    ...flatten(getDirectories(srcpath).map(getDirectoriesRecursive)),
  ];
};

const getPath = (pathSource, pathDestination) => {
  if (
    pathSource[pathSource.length - 1] == "/" ||
    pathSource === "" ||
    pathDestination === ""
  ) {
    return pathSource + pathDestination;
  } else {
    return pathSource + "/" + pathDestination;
  }
};

const manageDownload = () => {
  if (listDownload.length != 0 && listDownloadNow.length == 0) {
    listDownloadNow.push(listDownload.shift());
    //.replaceAll('//', '/')
    console.log('start download');
    win.webContents.send('upload-datas', 'start-download')


    let token = listDownloadNow[0].token;
    let pathSource = listDownloadNow[0].pathSource;
    let pathDestination = listDownloadNow[0].pathDestination;
    let idFile = listDownloadNow[0].idFile;
    let nameFile = listDownloadNow[0].nameFile;
    let typeFile = listDownloadNow[0].typeFile;

    downloadFile(
      token,
      pathSource,
      pathDestination,
      idFile,
      nameFile,
      typeFile
    );
  } else if (listDownload.length == 0 && listDownloadNow.length == 0) {
    clearInterval(timerID_Download);
    console.log('end download');
    win.webContents.send('upload-datas', 'end-download')


  }
};

const createDir = (dirPath, pathDestination) => {
  fs.mkdirSync(
    pathDestination + "/" + dirPath,
    { recursive: true },
    (error) => {
      if (error) {
        console.log("error");
      } else {
        console.log("sucessful");
      }
    }
  );
};

const sendToServerGetDirectoriesList = (body, token) => {
  axios
    .post(HOST + "files/api/getstructdirectry/", body, {
      headers: {
        Authorization: "Token " + token,
      },
    })
    .then((response) => {
      const listPaths = response.data.listPathsDirectories;

      let listPathsCreated = [];

      let pathRootListTemp = body.pathSource.split("/");
      listPaths.forEach((element) => {
        let pathListTemp = element.split("/");
        let pathLocal =
          "/" +
          pathListTemp
            .slice(pathRootListTemp.length - 1, pathListTemp.length)
            .join("/");
        listPathsCreated.push(pathLocal);
      });

      listPathsCreated.forEach((path) => {
        createDir(path, body.pathDestination);
      });
      let requsetPathes = [];
      const srcpath = body.pathDestination;
      const listPathsToSend = getDirectoriesRecursive(srcpath);
      const arrPath = srcpath.split("/");
      const lenArrPath = arrPath.length;
      let tempListsSource = body.pathSource.split("/");
      let toAddPath = tempListsSource
        .slice(0, tempListsSource.length - 1)
        .join("/");

      for (let index = 1; index < listPathsToSend.length; index++) {
        const element = listPathsToSend[index];
        const arrElement = element.split("/");
        let tempLists = arrElement.slice(lenArrPath, arrElement.length);

        let pathToRequset = "/" + getPath(toAddPath, tempLists.join("/"));

        if (pathToRequset == "") {
          continue;
        }
        requsetPathes.push(pathToRequset);
      }
      const url = "files/api/getlistfilesdirectories/";

      sendToServerDownload(
        url,
        0,
        requsetPathes.length,
        requsetPathes,
        token,
        body.pathDestination
      );
    });
};

const sendToServerDownload = (
  url,
  indexStart,
  indexEnd,
  requsetPathes,
  token,
  pathDestination
) => {
  let pathFileNow = requsetPathes[indexStart];
  if(pathFileNow[0] === '/' && pathFileNow[1] === '/'){
    pathFileNow = pathFileNow.slice(1);
  }




  let body = {
    token: token,
    pathSource: pathFileNow,
  };
  axios
    .post(HOST + url, body, {
      headers: {
        Authorization: "Token " + body.token,
      },
    })
    .then((response) => {
      let listFilesFromServer = response.data.listFiles;

      for (let index = 0; index < listFilesFromServer.length; index++) {
        if(pathFileNow[0] === '/' && pathFileNow[1] === '/'){
          pathFileNow = pathFileNow.slice(1);
        }

        // pathFileNow = '/'pathFileNow.split('/')[pathFileNow.split('/').length - 1]
        // if(pathFileNow[0] === '/' && pathFileNow[1] === '/'){
        //   pathFileNow = pathFileNow.slice(1);
        // }


        let tempStrPath = '/' + requsetPathes[0].split('/')[requsetPathes[0].split('/').length - 1]
        if(tempStrPath[tempStrPath.length - 1] !== '/'){
          tempStrPath += '/'
        }

        tempStrPath += pathFileNow.slice(requsetPathes[0].length)
        tempStrPath = tempStrPath.replace('//', '/')

      
        let downloadObjectData = {
          token: token,
          pathSource: pathFileNow,
          pathDestination: pathDestination + tempStrPath + "/",
          idFile: listFilesFromServer[index].idFile,
          nameFile: listFilesFromServer[index].nameFile,
          typeFile: listFilesFromServer[index].typeFile,
        };

        // console.log("downloadObjectData.pathDestination_s2:", downloadObjectData.pathDestination);

        listDownload.push(downloadObjectData);

        if (listDownload.length == 1 && listDownloadNow.length == 0) {
          timerID_Download = setInterval(manageDownload, 1000);
        }
      }

      if (indexStart < indexEnd - 1) {
        sendToServerDownload(
          url,
          indexStart + 1,
          indexEnd,
          requsetPathes,
          token,
          pathDestination
        );
      }
    })

    .catch((error) => {
      console.log("Error");
    });
};



// const wsMessage = new WebSocket("ws://localhost:8000/ws/message/");

// wsMessage.on("open", function open() {
//   ws.send();
// });

export { downloadFileFromClient };

// const findStrEnd = (str1, str2) => {
//   for (let index = 0; index < str1.length; index++) {
//     const element = str1[index];

//     for (let j = 0; j < array.length; j++) {
//       const element2 = str2[j];
      
//       if(element !== element2){
//         return i
//       }
//     }
    
//   }
// };