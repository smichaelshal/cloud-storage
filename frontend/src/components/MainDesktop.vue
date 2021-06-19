<template>
  <div class="main-desktop">
    Username: {{ getUsername }}
    <div style="margin-top: 20px; margin-bottom: 20px;">
      <UploadFile :pathNow="pathNow" style="margin-bottom: 10px;" />

      <el-button type="primary" @click="refreshFunc">
        refresh
      </el-button>

      <el-button
        type="primary"
        icon="el-icon-back"
        v-if="stackFuture.length > 0"
        @click="returnDirectory"
      >
        RETURN
      </el-button>
      <el-button
        disabled
        type="primary"
        icon="el-icon-back"
        v-if="stackFuture.length === 0"
        @click="returnDirectory"
      >
        RETURN
      </el-button>

      <el-button
        type="primary"
        icon="el-icon-right"
        v-if="stackHistory.length > 0"
        @click="returnBackDirectory"
      >
        BACK
      </el-button>
      <el-button
        disabled
        type="primary"
        icon="el-icon-right"
        v-if="stackHistory.length === 0"
        @click="returnBackDirectory"
      >
        BACK
      </el-button>
    </div>
    <div class="main">
      <RightMenu />

      <MenuFile
        :name="downloadNameFile"
        :id="downloadIdFile"
        :type="downloadTypeFile"
        :isDirectory="isDirectory"
      />
      <MenuDirectory
        :name="downloadNameDirectory"
        :path="downloadPathDirectory"
      />

      <Directory
        v-for="(directory, index) in listDirectories"
        :key="'d' + index"
        @cd-directory="changeDirectory"
        @open-menu-directory="openMenuDirecotry"
        :name="directory.name_directory"
        :size="directory.size_directory"
        :path="directory.pathDestination"
        :usernameUpload="directory.username"
      />

      <File
        v-for="(file, index) in listFiles"
        :key="'f' + index"
        @open-menu-file="openMenuFile"
        :name="file.nameFile"
        :type="file.typeFile"
        :id="file.idFile"
        :size="file.sizeFile"
        :usernameUpload="file.username"
      />
    </div>
  </div>
</template>

<script>
import File from "@/components/File.vue";
import Directory from "@/components/Directory.vue";
import UploadFile from "@/components/UploadFile.vue";
import MenuFile from "@/components/MenuFile.vue";
import MenuDirectory from "@/components/MenuDirectory.vue";
import RightMenu from "@/components/RightMenu.vue";

import { mapGetters, mapMutations } from "vuex";
import axios from "axios";

export default {
  name: "MainDesktop",
  props: ["pathSideMenu"],
  components: {
    File,
    Directory,
    UploadFile,
    MenuFile,
    MenuDirectory,
    RightMenu,
  },
  data() {
    return {
      listFiles: [],
      listDirectories: [],
      stackHistory: [],
      stackFuture: [],
      pathNow: "/",
      pathDir: null,
      downloadNameFile: null,
      downloadTypeFile: null,
      downloadIdFile: null,

      downloadNameDirectory: null,
      downloadPathDirectory: null,
      isDirectory: null,
      isClickRight: false,
    };
  },
  computed: {
    ...mapGetters([
      "getToken",
      "getNamePage",
      "getUsername",
      "getHost",
      "getTrees",
      "getListSelected",
      "getListSelectedDirectories",
      "getDataToSendWs",
      "getIsChangeDataToSendWs",
      "getReturnListDirFiles",
      "getIdUser",
      "getListSelectedLength",
    ]),
  },
  methods: {
    ...mapMutations([
      "setToken",
      "setNamePage",
      "setUsername",
      "setPathNow",
      "setDataToSendWs",
      "setIsChangeDataToSendWs",
      "setReturnListDirFiles",
    ]),
    refreshFunc() {
      this.setReturnListDirFiles(!this.getReturnListDirFiles);
    },
    openMenuFile(name, id, type, isDirectory) {
      this.downloadNameFile = name;
      this.downloadIdFile = id;
      this.downloadTypeFile = type;
      this.isDirectory = isDirectory;
      this.isClickRight = true;
    },
    openMenuDirecotry(name, path) {
      this.downloadNameDirectory = name;
      this.downloadPathDirectory = path;
    },
    getListFilesFromServer(path) {
      const _this = this;
      const url = _this.getHost + "files/api/getlistfilesdirectories/";
      let config = {
        headers: {
          Authorization: "Token " + this.getToken,
        },
      };
      let body = {
        pathSource: path,
      };

      axios
        .post(url, body, config)
        .then(function(response) {
          _this.listFiles = response.data.listFiles;
        })

        .catch((error) => console.log((this.errors = error)));
    },
    getListDirectoriesFromServer(path) {
      const _this = this;
      const url = _this.getHost + "files/api/getlistdirectories/";
      let config = {
        headers: {
          Authorization: "Token " + this.getToken,
        },
      };
      let body = {
        pathSource: path,
      };

      axios
        .post(url, body, config)
        .then(function(response) {
          _this.listDirectories = response.data.listDirectories;
        })

        .catch((error) => console.log((this.errors = error)));
    },
    getLists(path) {
      this.getListFilesFromServer(path);
      this.getListDirectoriesFromServer(path);
      this.pathNow = path;
    },
    returnBackDirectory() {
      this.stackFuture.push(this.pathNow);
      this.pathNow = this.stackHistory.pop();
      this.getLists(this.pathNow);
      this.deleteLists();
    },
    returnDirectory() {
      this.stackHistory.push(this.pathNow);
      this.pathNow = this.stackFuture.pop();
      this.getLists(this.pathNow);
      this.deleteLists();
    },
    changeDirectory(path) {
      this.stackHistory.push(this.pathNow);
      this.getLists(path);
      this.deleteLists();
    },

    deleteLists() {
      this.deleteDownloadsFiles();
      this.deleteDownloadsDirectories();
    },

    deleteDownloadsFiles() {
      for (let id in this.getListSelected) {
        delete this.getListSelected[id];
      }
    },
    deleteDownloadsDirectories() {
      for (let path in this.getListSelectedDirectories) {
        delete this.getListSelectedDirectories[path];
      }
    },
    labelToPath(treePointer, name, path) {
      if (treePointer.label === name) {
        this.pathDir = path;
        return;
      } else {
        treePointer.nodes.forEach((element) => {
          return this.labelToPath(element, name, path + "/" + element.label);
        });
      }
    },
  },
  watch: {
    getReturnListDirFiles: function() {
      this.getListFilesFromServer(this.pathNow);
      this.getListDirectoriesFromServer(this.pathNow);
    },
    listFiles: function() {},
    listDirectories: function() {},
    pathDir: function() {
      this.changeDirectory(this.pathDir);
    },

    pathSideMenu: function(val) {
      this.labelToPath(this.getTrees, val, "");
    },

    pathNow: function(val) {
      this.setPathNow(val);
    },
  },
  mounted: function() {
    this.getLists("/");
  },
};

// _this.setDataToSendWs({
//   'type': 'directory',
//   'msg':'bla',
//   'ids': [_this.getToken]
//   })
//   _this.setIsChangeDataToSendWs(!_this.getIsChangeDataToSendWs)
</script>

<style scoped>
.main {
  position: absolute;
  height: 90%;
  width: 75%;
}
</style>
