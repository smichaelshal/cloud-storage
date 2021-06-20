const axios = require("axios");
const WebSocket = require("ws");
const path = require("path");
const fs = require("fs");
import { HOST } from "./background";
import { HOST_WS } from "./background";
import { win } from "./background";

let modeUpload = 1;
let sumFiles = 0;
let sumFilesUploads = 0;

let dictFilesDirectory = {};
let listFiles = [];
let sizeFileUpload = null;

// Global Varibel

let listUpload = [];
let listUploadNow = [];
let timerID = null;
let isUpload = false

// constants
const TIME_TO_LOOP = 1000;

const uploadFileFromClient = (RES_DATA) => {
  const token = RES_DATA.token;
  const pathSource = RES_DATA.pathSource;
  const pathDestination = RES_DATA.pathDestination;
  const modeUpload = RES_DATA.modeUpload;

  if (fs.statSync(pathSource).isDirectory()) {
    uploadDirectories(pathSource, pathDestination, token, modeUpload); // ????1
  } else {
    let uploadObjectData = {
      token: token,
      pathSource: pathSource,
      pathDestination: pathDestination,
      modeUpload: modeUpload,
    };
    listUpload.push(uploadObjectData);
    sumFiles += 1;

    if (
      listUpload.length == 1 &&
      listUploadNow.length == 0 &&
      !fs.statSync(pathSource).isDirectory()
    ) {
      timerID = setInterval(manageUpload, TIME_TO_LOOP);
    }
  }
};

const uploadFile = (token, pathSource, pathDestination, modeUpload) => {
  let responseData = null;
  let errors = null;
  let idFile = null;
  let seekFile = null;

  const typeFile = path
    .extname(pathSource)
    .slice(1, path.extname(pathSource).length);
  const nameFile = path.basename(pathSource, "." + typeFile);
  let fileFS = fs.statSync(pathSource);
  const sizeFile = fileFS.size;
  
  const isFirst = modeUpload.toString();
  sizeFileUpload = sizeFile;

  const body = {
    name_file: nameFile,
    type_file: typeFile,
    size_file: sizeFile,
    pathSource: pathSource,
    pathDestination: pathDestination,
    is_first: isFirst,
  };

  axios
    .post(HOST + "files/api/uploadfileapi/", body, {
      headers: {
        Authorization: "Token " + token,
      },
    })
    .then((response) => {
      idFile = response.data.idFile;
      seekFile = response.data.seekFile;

      const ws = new WebSocket(HOST_WS + "ws/upload/");

      ws.on("open", function open() {
        let dict = {
          token: token,
          pathSource: pathSource,
          pathDestination: pathDestination,
          idFile: idFile,
        };
        ws.send(JSON.stringify(dict));

        var readableStream = fs.createReadStream(pathSource);
        var data = "";
        var chunk;
        const sizeChunk = 1024 * 1024 * 10;
        let sumSend = 0;

        readableStream.on("readable", function() {
          while ((chunk = readableStream.read(sizeChunk)) != null) {
            let buf1 = Buffer.from("C");
            let arr = [buf1, chunk];
            let buf = Buffer.concat(arr);

            sumSend += buf.length - 1;
            if (seekFile < sumSend) {
              ws.send(buf);
              win.webContents.send('uploadPercent', (sumSend / sizeFileUpload) * 100 + '%');
            } else {
              let buf2 = Buffer.from("A");
              ws.send(buf2);
            }
          }
        });

        readableStream.on("end", function() {
          let buf1 = Buffer.from("E"); // >>
          ws.send(buf1);
          win.webContents.send('mains', 'end')
          if (listUploadNow.length == 1) {
            listUploadNow.shift();
          }
        });
      });

      ws.on("message", function incoming(data) {
        if(data === "ACK-E"){
          sumFilesUploads += 1
        }
        console.log('sumFilesUploads', sumFilesUploads);
        
        if(sumFilesUploads === sumFiles){
          sumFilesUploads = 0;
          sumFiles = 0;
          win.webContents.send('upload-datas', 'end-upload')

          console.log('yytt');
        }
      });

      ws.on("close", function close(data) {
        const flag = String.fromCharCode(data[0]);
        if (listUploadNow.length == 1) {
          listUploadNow.shift();
        }
      });
    })

    .catch((error) => {
      console.log(error.response);
    });

  // up2
};
//---------------------------------------------------------------------

const manageUpload = () => {
  // if (isUpload){
  //   console.log('start upload');
  // }
  if (listUpload.length != 0 && listUploadNow.length == 0) {
    listUploadNow.push(listUpload.shift());
    isUpload = true;
    console.log('start upload');
    win.webContents.send('upload-datas', 'start-upload')

    let token = listUploadNow[0].token;
    let pathSource = listUploadNow[0].pathSource;
    let pathDestination = listUploadNow[0].pathDestination;
    let modeUpload = listUploadNow[0].modeUpload;

    // uploadFile(token, pathSource, pathDestination, modeUpload); //up3
    shellUploadFile(token, pathSource, pathDestination, modeUpload);
  } else if (listUpload.length == 0 && listUploadNow.length == 0) {
    clearInterval(timerID);
    // console.log('end upload', sumFiles);
    // win.webContents.send('upload-datas', 'end-upload')
    // isUpload = false;
  }
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

const uploadDirectories = (path, pathDestination, token, modeUpload) => {
  let root_path = path;
  let tempListPath = root_path.split("/");
  let nameRoot = tempListPath[tempListPath.length - 1];
  let listSubDirectories = getDirectoriesRecursive(path);

  let listToCreate = [];

  const listSubDirectoriesSorted = listSubDirectories.sort(function(a, b) {
    return b.split("/").length - a.split("/").length;
  });

  let listToSend = [];

  listToSend.push(listSubDirectoriesSorted[0]);

  listSubDirectoriesSorted.forEach((value) => {
    if (!isIncludes(listToSend, value)) {
      listToSend.push(value);
    }
  });

  listToSend.forEach((pathDirectory) => {
    listToCreate.push({
      pathDestination: addRoot(
        pathDirectory.slice(
          root_path.length - nameRoot.length,
          pathDirectory.length
        ),
        pathDestination
      ),
      pathSource: pathDirectory,
    });
  });

  listToCreate.forEach((direcotryObject) => {
    const body = {
      pathDestination: direcotryObject.pathDestination,
      pathSource: direcotryObject.pathSource,
    };
    sendToServerCreateDirectory(body, token);
  });
  let arrPath = path.split("/");
  getStartUploadDirectory(
    getPath(pathDestination, arrPath[arrPath.length - 1]),
    path,
    token,
    modeUpload
  );
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

const isIncludes = (lists1, val) => {
  let sumTrue = 0;
  lists1.forEach((numStr) => {
    if (numStr.includes(val)) {
      sumTrue += 1;
    }
  });

  if (sumTrue > 0) return true;
  return false;
};

const sendToServerCreateDirectory = (body, token) => {
  axios
    .post(HOST + "files/api/createpathapi/", body, {
      headers: {
        Authorization: "Token " + token,
      },
    })
    .then((response) => {
      console.log(response.data);
    })

    .catch((error) => {
      console.log(error.response);
    });
};

const getListFiles = (path) => {
  return fs
    .readdirSync(path, { withFileTypes: true })
    .filter((item) => !item.isDirectory())
    .map((item) => item.name);
};

const getListDirectories = (path) => {
  return fs
    .readdirSync(path, { withFileTypes: true })
    .filter((item) => item.isDirectory())
    .map((item) => item.name);
};

const sendAllDirectories = (
  pathDestination,
  pathSource,
  token,
  modeUpload,
  listUploadedFiles,
  pathDirectoryLastFile,
  nameLastFile
) => {
  let listDirectories = getListDirectories(pathSource);
  let listFiles = getListFiles(pathSource);

  listFiles.forEach((file) => {
    let uploadObjectData = {
      token: token,
      pathSource: getPath(pathSource, file),
      pathDestination: getPath(pathDestination, file),
      modeUpload: modeUpload,
    };
    if (!isInListObjects(file, listUploadedFiles)) {
      listUpload.push(uploadObjectData);
      sumFiles += 1;
    } else if (
      pathDestination === pathDirectoryLastFile &&
      nameLastFile === file
    ) {
      let uploadObjectData = {
        token: token,
        pathSource: getPath(pathSource, file),
        pathDestination: getPath(pathDestination, file),
        modeUpload: "2", // <<2
      };
      listUpload.push(uploadObjectData);
      sumFiles += 1;
    }
  });

  listDirectories.forEach((directory) => {
    shellSendAllDirectories(
      getPath(pathDestination, directory),
      getPath(pathSource, directory),
      token,
      modeUpload,
      pathDirectoryLastFile,
      nameLastFile
    );
  });

  timerID = setInterval(manageUpload, TIME_TO_LOOP);
};

const shellSendAllDirectories = (
  pathDestination,
  pathSource,
  token,
  modeUpload,
  pathDirectoryLastFile,
  nameLastFile
) => {
  let bodys = {
    token: token,
    pathSource: pathDestination,
  };
  axios
    .post(HOST + "files/api/getlistfilesdirectories/", bodys, {
      headers: {
        Authorization: "Token " + token,
      },
    })
    .then((response) => {
      let listUploadedFiles = response.data.listFiles;
      sendAllDirectories(
        pathDestination,
        pathSource,
        token,
        modeUpload,
        listUploadedFiles,
        pathDirectoryLastFile,
        nameLastFile
      );
    })
    .catch((error) => {
      console.log(error.response);
    });
};

const isInListObjects = (nameFile, listUploadedFiles) => {
  for (let index = 0; index < listUploadedFiles.length; index++) {
    const element = listUploadedFiles[index];
    let pathFile = element.nameFile;

    if (element.typeFile.length != 0) {
      pathFile += "." + element.typeFile;
    }

    if (pathFile == nameFile) {
      return true;
    }
  }

  return false;
};

const getStartUploadDirectory = (
  pathDestination,
  pathSource,
  token,
  modeUpload
) => {
  let body = {};

  axios
    .post(HOST + "files/api/getlastupload/", body, {
      headers: {
        Authorization: "Token " + token,
      },
    })
    .then((response) => {
      let pathSourceLastFile = response.data.pathDestination;

      let tempArrPathLarUpload = pathSourceLastFile.split("/");
      let nameLastFile = tempArrPathLarUpload[tempArrPathLarUpload.length - 1];

      let pathLastFile = tempArrPathLarUpload
        .slice(0, tempArrPathLarUpload.length - 1)
        .join("/");

      shellSendAllDirectories(
        pathDestination,
        pathSource,
        token,
        modeUpload,
        pathLastFile,
        nameLastFile
      );
    })

    .catch((error) => {
      console.log(error.response);
    });
};

const shellUploadFile = (token, pathSource, pathDestination, modeUpload) => {
  if (modeUpload === 1) {
    let bodys = {
      token: token,
      pathSource: pathDestination,
    };
    axios
      .post(HOST + "files/api/getlistfilesdirectories/", bodys, {
        headers: {
          Authorization: "Token " + token,
        },
      })
      .then((response) => {
        let pathList = pathSource.split("/");
        const nameFileNew = pathList[pathList.length - 1];
        let isInList = false;
        let listUploadedFiles = response.data.listFiles;
        listUploadedFiles.forEach((item) => {
          let pathTemp = item.nameFile;
          if (item.typeFile !== "") {
            pathTemp += "." + item.typeFile;
          }

          if (nameFileNew === pathTemp) {
            isInList = true;
            modeUpload = 2; // <<2
          }
        });
        uploadFile(token, pathSource, pathDestination, modeUpload);
      })
      .catch((error) => {
        console.log(error.response);
      });
  }
};

const addRoot = (pathDestination, pathSource) => {
  if (pathSource[pathSource.length - 1] === "/") {
    return pathSource + pathDestination;
  }
  return pathSource + "/" + pathDestination;
};

export { uploadFileFromClient };
