<template>
  <div class="right-menu">
    <el-dialog
      title=""
      :visible.sync="isRightClick"
      width="30%"
      center>
      <span slot="footer" class="dialog-footer">
      <div>
        <el-button style="margin-bottom: 10px;" @click="downloadObjects">Download</el-button>
      </div>

      <div v-if="getLengthObject(getListSelectedDirectories) + getLengthObject(getListSelected) === 1">
        <el-button style="margin-bottom: 10px;" @click="changeNameOpen = true">Change Name</el-button>
      </div>

      <div v-if="changeNameOpen">
        <el-input style="width: 150px; margin: 10px; padding-top: 15px; padding-bottom: 20px;" placeholder="Enter a new name" v-model="inputNewName" type="text"></el-input>
        <el-button style="margin-bottom: 10px;" @click="changeName">Change Name</el-button>
      </div>

      <div>
        <el-button style="margin-bottom: 10px;"  @click="setIsRightClick(false)">Share</el-button>
      </div>
      <div>
        <el-button style="margin-bottom: 10px;"  @click="setIsRightClick(false)">Delete</el-button>
      </div>
      </span>
    </el-dialog>

  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations} from 'vuex';

export default {
  name: 'RightMenu',
  props: [],
  data(){
    return {
      isRightClick: null,
      changeNameOpen: false,
      inputNewName: "",
    }
  },
  computed: {
    ...mapGetters([
        'getListSelected',
        'getIsRightClick',
        'getToken',
        'getPathNow',
        'getPathHome',
        'getListSelectedLength',
        'getListSelectedLengthDirectories',
        'getListSelectedDirectories',
    ]),
  },
  methods: {
    ...mapMutations([
      'setIsRightClick',
      'setListSelectedLength',

    ]),
    downloadObjects(){
      console.log(this.getListSelected);
      this.downloadFile();
      this.downloadDirectory();
      this.setIsRightClick(false);
     

    },
    downloadFile(){
      for (let id in this.getListSelected){
         this.sendDownloadFile(id, this.getListSelected[id].name, this.getListSelected[id].type)
      }
    },
    
    downloadDirectory(){
      for (let path in this.getListSelectedDirectories){
        this.sendDownloadDirectory(path, this.getListSelectedDirectories[path].name)
      }
    },

    getLengthObject(obj){
      let sumFiled = 0;
      for(const filed in obj){
        sumFiled += 1;
        console.log(filed);
      }

      return sumFiled;

    },
  sendDownloadFile(id, name, type){
    const url = 'http://localhost:3000/download/';
    let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
        }
        let body = {
            "data": {
                "token": this.getToken,
                "pathSource": this.getPathNow,
                "pathDestination": this.getPathHome + '/',
                "idFile": id,
                "nameFile": name,
                "typeFile": type,
                "isDirectory": false
            }
        }

    axios.post(url, body, config)
    .then(function (response) {
        console.log(response.data);
    })

    .catch(error => console.log(this.errors = error));

    },
  sendDownloadDirectory(path, name){
    const url = 'http://localhost:3000/download/';
    let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
        }
        let body = {
            "data": {
                "token": this.getToken,
                "pathSource": path,
                "pathDestination": this.getPathHome,
                "idFile": '',
                "nameFile": name,
                "typeFile": '',
                "isDirectory": true
            }
        }

    axios.post(url, body, config)
    .then(function (response) {
        console.log(response.data);
    })

    .catch(error => console.log(this.errors = error));

    },
    changeName(){
      this.setIsRightClick(false);
      const newName = this.inputNewName;
      let body = {}
      let idFile;
      let path;
      let isFile;
      
    if(this.getLengthObject(this.getListSelectedDirectories) === 1){
      for(path in this.getListSelectedDirectories){
        console.log(path);
        isFile = "0";
      }
    }else{
      for(idFile in this.getListSelected){
        console.log(idFile);
        isFile = "1";
      }
    }
    
    
      
    const url = 'http://localhost:8000/files/api/chnagenameobject/';
    let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
        }
        
        body = {
            "data": {
                "token": this.getToken,
                "isFile": isFile,
                "newName": newName,
                "pathSource": this.getPathNow,
                "idFile": idFile,
                "path": path,
            }
        }

    axios.post(url, body, config)
    .then(function (response) {
        console.log(response.data);
    })

    .catch(error => console.log(this.errors = error));
    },
  },
  mounted: function () {
    this.isRightClick = this.getIsRightClick;
  },

  watch: {
    isRightClick: function (val) {
      this.setIsRightClick(val);

      if(!val){
        this.changeNameOpen = false;
      }
      
      
    },
    getIsRightClick: function (val) {
      this.isRightClick = val;
      if(!val){
        this.changeNameOpen = false;
      }
    },
  },

    
}
</script>

<style scoped>
.file-box{
  width: 180px;
  float: right;
  margin-right: 10px;
  margin-top: 10px;
}

</style>
