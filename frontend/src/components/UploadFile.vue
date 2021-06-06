<template>
  <div class="upload-file">
    <!-- uploadPercent: {{uploadPercent}} -->
    <el-button type="primary" @click="openFile"
      >Upload File<i class="el-icon-upload el-icon-right"></i
    ></el-button>
    <el-button type="primary" @click="openDirectory"
      >Upload Directory <i class="el-icon-upload el-icon-right"></i
    ></el-button>
  </div>
</template>

<script>
const { ipcRenderer } = require("electron");
const CHANNEL = "main";

// import axios from 'axios';
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "UploadFile",
  props: ["pathNow"],
  components: {},
  computed: {
    ...mapGetters([
      "getToken",
      "getNamePage",
      "getUsername",
      "getHost",
      "getTrees",
      "getIsChangeDataToSendWs",
      "getIdUser",
      "getDataToSendWs",
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
    ]),
    openFile() {
      ipcRenderer.send("openFile", this.pathNow);
    },
    openDirectory() {
      ipcRenderer.send("openDirectory", this.pathNow);
    },

    sendRequestUploadFile() {
      const _this = this;

      // const url = 'http://localhost:3000/upload/';
      // let config = {
      //       headers: {
      //           }
      //     }
      let body = {
        data: {
          token: this.getToken,
          pathSource: _this.uploadPath,
          pathDestination: _this.pathNow,
          modeUpload: 1,
        },
      };

      ipcRenderer.send("uploadChannel", body);

      // axios.post(url, body, config)
      // .then(function (response) {
      //   console.log(response);
      // })

      // .catch(error => console.log(this.errors = error));
    },
  },
  data() {
    return {
      uploadPath: null,
      uploadPercent: 0,
    };
  },
  created() {
    const _this = this;
    ipcRenderer.on(CHANNEL, (event, data) => {
      this.uploadPath = data;
      this.sendRequestUploadFile();
    });
    ipcRenderer.on("uploadPercent", (event, data) => {
      this.uploadPercent = data;
    });
    ipcRenderer.on("mains", (event, data) => {
      console.log(event, data);
      _this.setDataToSendWs({
        type: "directory",
        msg: "bla",
        ids: [_this.getIdUser],
      });
      _this.setIsChangeDataToSendWs(!_this.getIsChangeDataToSendWs);
    });
  },
  watch: {
    uploadPath: function() {
      // this.sendRequestUploadFile()
      // console.log("vs3");
    },
  },
};
</script>

<style scoped></style>
