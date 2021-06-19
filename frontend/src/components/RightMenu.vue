<template>
  <div class="right-menu">
    <!-- {{getListSelectedDirectories}} -->
    <!-- {{getListSelected}} -->
    <!-- sizeFilesNow: {{sizeFilesNow}} -->

    <el-dialog
      title=""
      :visible.sync="isRightClick"
      width="30%"
      center>
      <span slot="footer" class="dialog-footer">
      <div>
        <el-button style="margin-bottom: 10px;" @click="downloadObjects">Download</el-button>
      </div>

      <div v-if="(getLengthObject(getListSelectedDirectories) + getLengthObject(getListSelected) === 1) && checkUserUpload()">
        <el-button style="margin-bottom: 10px;" @click="changeNameOpen = true">Change Name</el-button>
      </div>

      <div v-if="changeNameOpen">
        <el-input style="width: 150px; margin: 10px; padding-top: 15px; padding-bottom: 20px;" placeholder="Enter a new name" v-model="inputNewName" type="text"></el-input>
        <el-button style="margin-bottom: 10px;" @click="changeName">Change Name</el-button>
      </div>

      <div>
        <el-button style="margin-bottom: 10px;"  @click="shareOpen = true">Share</el-button>
      </div>

      <div v-if="shareOpen">
        <el-input style="width: 150px; margin: 10px; padding-top: 15px; padding-bottom: 20px;" placeholder="Enter usernames to share" v-model="inputShare" type="text"></el-input>
        <el-button style="margin-bottom: 10px;" @click="shareObjects">Share</el-button>
      </div>
      <div>
        <el-button style="margin-bottom: 10px;"  @click="DeleteObject">Delete</el-button>
      </div>
      </span>
    </el-dialog>

    <el-dialog
  :title="titleError"
  :visible.sync="dialogVisible"
  width="30%">
  <span>{{spanError}}</span>
  <div>
   
    <div v-if="typeof dataError === 'string'">
      {{dataError}}
    </div>
    <div v-else>
      <ul>
      <li v-for="user in listFailds" :key="user">{{user}}</li>
      </ul>
    </div>
    
  </div>
  <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="dialogVisible = false">Cencel</el-button>
  </span>
</el-dialog>

  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapMutations} from 'vuex';
const { ipcRenderer } = require('electron')


export default {
  name: 'RightMenu',
  props: [],
  data(){
    return {
      dialogVisible: false,
      listFailds: [],
      isRightClick: null,
      changeNameOpen: false,
      shareOpen: false,
      inputNewName: "",
      inputShare: "",
      sumFiles: 0,
      sumDirectories: 0,
      sizeFilesNow: 0,
      titleError: '',
      dataError: '',
      spanError: '',
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
        'getIsChangeDataToSendWs',
        'getIdUser',
        'getHost',
        'getUsername',
    ]),
  },
  methods: {
    ...mapMutations([
      'setIsRightClick',
      'setListSelectedLength',
      'setIsChangeDataToSendWs',
      'setDataToSendWs',

    ]),
    shareFunction(listUser){
    const _this = this;
    const urlids = _this.getHost + 'files/api/getidsusers/';

    let configs = {
        headers: {
            Authorization: 'Token ' + _this.getToken,
            }
      }

    let bodys = {
              "data": {
                  "token": _this.getToken,
                  "listUsers": listUser,
              }
          }

    axios.post(urlids, bodys, configs)
      .then(function (response) {
        _this.sumFiles = 0;
        _this.setDataToSendWs({
          'type': 'directory',
          'msg':'bla',
          'ids': [_this.getIdUser, ...response.data.listIds],
          })
        _this.setIsChangeDataToSendWs(!_this.getIsChangeDataToSendWs);
        _this.listFailds = response.data.listFailds;
        if(_this.listFailds.length > 0){
          _this.dialogVisible = true;
          _this.spanError = "Sharing failed for users:";
          _this.dataError = [];
          _this.titleError = "Sharing failed for some users";
        }
      })
      .catch(error => console.log(this.errors = error));
  },

    shareObjects(){
      this.setIsRightClick(false);
      let listUsers = this.inputShare.split(' ');// >>>
      this.inputShare = '';


      for (let path in this.getListSelectedDirectories){
        this.sendShare(listUsers, path, 'id', '0');
      }

      for (let id in this.getListSelected){
        this.sendShare(listUsers, this.getPathNow, id, '1');
      }


    },
    sendShare(listUser, path, id, isFile){
      const _this = this;
      
      let lenDirectories = this.lenObj(this.getListSelectedDirectories);
      let lenFiles = this.lenObj(this.getListSelected);

      const url = this.getHost + 'files/api/shareobject/';


      let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
      }

      let body = {
          "data": {
              "token": this.getToken,
              "isFile": isFile,
              "pathSource": path,
              "listUsers": listUser,
              "id": id,
          }
      }
axios.post(url, body, config)
.then(function (response) {
  console.log(response);

  if(isFile === '1'){
    _this.sumFiles += 1;
  }else{
    _this.sumDirectories += 1;
  }


  if((lenFiles === _this.sumFiles && isFile === '1') 
    || (lenDirectories === _this.sumDirectories && isFile === '0')){
      _this.shareFunction(listUser);
  }
})

.catch(error => console.log(this.errors = error));

     
      
    },
    lenObj(obj){
      let index = 0;
      for(const item in obj){
        console.log(item);
        index += 1;
      }

      return index;
    },
    downloadObjects(){
      this.sizeFilesNow = 0;

      this.downloadFile();
      this.downloadDirectory();
      this.setIsRightClick(false);
      
    },
    downloadFile(){
      for (let id in this.getListSelected){
         this.sendDownloadFile(id, this.getListSelected[id].name, this.getListSelected[id].type)
         this.sizeFilesNow +=  this.getListSelected[id].size;
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

    checkUserUpload(){
      for (let path in this.getListSelectedDirectories){
        if(this.getListSelectedDirectories[path].usernameUpload != this.getUsername){
          return false;
        }
      }

      for (let idFile in this.getListSelected){
        if(this.getListSelected[idFile].usernameUpload != this.getUsername){
          return false;
        }
      }

      return true;
    },
  sendDownloadFile(id, name, type){
    
    // const url = 'http://localhost:3000/download/';
    // let config = {
    //       headers: {
    //           Authorization: 'Token ' + this.getToken,
    //           }
    //     }
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

    // axios.post(url, body, config)
    // .then(function (response) {
    //     console.log(response.data);
    // })

    // .catch(error => console.log(this.errors = error));

    ipcRenderer.send('downloadChannel', body);

    },
  sendDownloadDirectory(path, name){
    // const url = 'http://localhost:3000/download/';
    // let config = {
    //       headers: {
    //           Authorization: 'Token ' + this.getToken,
    //           }
    //     }
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

    // axios.post(url, body, config)
    // .then(function (response) {
    //     console.log(response.data);
    // })

    // .catch(error => console.log(this.errors = error));

    ipcRenderer.send('downloadChannel', body);

    },
    DeleteObject(){
      // >>
      let sumDirectories = 0;
      let sumFiles = 0;
      const _this = this;

      let lenDirectories = this.lenObj(this.getListSelectedDirectories);
      let lenFiles = this.lenObj(this.getListSelected);

      const url = this.getHost + 'files/api/deleteobject/';
      let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
        }
      
      
      for (const property in this.getListSelectedDirectories) {
        const item = this.getListSelectedDirectories[property];
        console.log(item);

        let body = {
            "data": {
                "token": this.getToken,
                "isDirectory": '1',
                "pathSource": property,
            }
        }

        axios.post(url, body, config)
        .then(function (response) {
          sumDirectories += 1;
            console.log(response.data);
            if(sumDirectories === lenDirectories){

          _this.setDataToSendWs({
            'type': 'directory',
            'msg':'bla',
            'ids': [_this.getIdUser]
            })
            _this.setIsChangeDataToSendWs(!_this.getIsChangeDataToSendWs)
            }
            delete _this.getListSelectedDirectories[property]
        })

      .catch(error => console.log(this.errors = error));
      
      }

      for (const property in this.getListSelected) {
        const item = this.getListSelected[property];
        console.log(property);
        console.log(item);

        let pathFileDel = this.getPathNow + '/' + item.name + '.' + item.type;
        if(pathFileDel[0] === '/' && pathFileDel[1] === '/'){
          pathFileDel = pathFileDel.slice(1)
        }
        

        let body = {
            "data": {
                "token": this.getToken,
                "isDirectory": '0',
                "pathSource": this.getPathNow + '/' + item.name + '.' + item.type,
                "idFile": property,
            }
        }


        axios.post(url, body, config)
        .then(function (response) {
          sumFiles += 1;
            console.log(response.data);
             if(sumFiles === lenFiles){

          _this.setDataToSendWs({
            'type': 'directory',
            'msg':'bla',
            'ids': [_this.getIdUser]
            })
            _this.setIsChangeDataToSendWs(!_this.getIsChangeDataToSendWs)
            }


            delete _this.getListSelected[property]
        })

      .catch(error => console.log(this.errors = error));
      }

      this.setIsRightClick(false);



    },
    changeName(){ // >>
      this.setIsRightClick(false);
      const newName = this.inputNewName;
      let body = {}
      let idFile;
      let path;
      let isFile;
      
    if(this.getLengthObject(this.getListSelectedDirectories) === 1){
      for(path in this.getListSelectedDirectories){
        console.log(path);// ???
        isFile = "0";
      }
    }else{
      for(idFile in this.getListSelected){
        console.log(idFile);
        isFile = "1";
      }
    }
    
    
      
    const url = this.getHost + 'files/api/chnagenameobject/';
    const _this = this;
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
        _this.setDataToSendWs({
        'type': 'directory',
        'msg':'bla',
        'ids': [_this.getIdUser]
        })
        _this.getListSelected[idFile].name = newName;
        _this.setIsChangeDataToSendWs(!_this.getIsChangeDataToSendWs)
        delete _this.getListSelectedDirectories[path];

    
    })

    .catch(function (error) {
      if(error.response.status === 400){
        _this.spanError = "";
        _this.dataError = "The name used"
        _this.titleError = "Error renaming the file";
        _this.dialogVisible = true;
      }

    });
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

    dialogVisible: function (val) {
      if(val === false){ // true => false
      this.setIsRightClick(true);
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
