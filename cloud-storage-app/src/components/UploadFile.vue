<template>
  <div class="upload-file">
      <el-button type="primary" @click="openFile">Upload<i class="el-icon-upload el-icon-right"></i></el-button>
  </div>
</template>

<script>
const { ipcRenderer } = require('electron')
const CHANNEL = 'main';

import axios from 'axios';
import { mapGetters } from 'vuex';


export default {
  name: 'UploadFile',
  props: ['pathNow'],
  components: {
  },
    computed: {
    ...mapGetters([
      'getToken',
      'getNamePage',
      'getUsername',
      'getHost',
      'getTrees',
    ]),
  },
  methods: {
    openFile(){
      ipcRenderer.send('openFile', this.pathNow);
    },

    sendRequestUploadFile(){
      const _this = this;
      const url = 'http://localhost:3000/upload/';
      let config = {
            headers: {
                }
          }
          let body = {
            "data": {
                "token": this.getToken,
                "pathSource": _this.uploadPath,
                "pathDestination": _this.pathNow,
                "modeUpload": 1,
                // "pathNow": '',
            }
          }

          console.log("bodytt: ", body);

      axios.post(url, body, config)
      .then(function (response) {
        console.log(response);
      })

      .catch(error => console.log(this.errors = error));
    },
    
  },
  data(){
    return {
        uploadPath: null
    }
  },
    created() {
    ipcRenderer.on(CHANNEL, (event, data) => {
        this.uploadPath = data;
    });
  },watch: {
    uploadPath: function () {
      this.sendRequestUploadFile()
    },
  }
}
</script>

<style scoped>

</style>
