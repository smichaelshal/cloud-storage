<template>
  <div class="side-menu">
    <el-menu>
      <tree-menu :label="trees.label" :nodes="trees.nodes" @cd-directory-menu="sendEventCD"></tree-menu>
    </el-menu>
  </div>
</template>

<script>
import TreeMenu from '@/components/TreeMenu.vue'
import { mapGetters, mapMutations } from 'vuex';
import axios from 'axios';
var _ = require("lodash");

export default {
  name: 'SideMenu',
  props: [],
  components: {
    TreeMenu,
  },
    data(){
    return {
      trees: {},
      paths: '',
      pathDir: null
      
    }
  },
    computed: {
    ...mapGetters([
      'getToken',
      'getNamePage',
      'getUsername',
      'getHost',
      'getReturnListDirFiles',
      'getListFilesFromServer',
      'getListDirectoriesFromServer',
    ]),
  },

  methods:{
    ...mapMutations([
        'setToken',
        'setNamePage',
        'setUsername',
        'setTrees',
    ]),
    getListPaths(){
    const _this = this;
    const url = this.getHost + 'files/api/getstructdirectry/';
    let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
        }
        let body = {
          "pathSource": '/',
          "pathDestination": '/'
        }

    axios.post(url, body, config)
    .then(function (response) {
      _this.paths = response.data.listPathsDirectories;

      _this.pathString2Tree(_this.paths, function (tree) {
        _this.trees = {"label": '/', "nodes": tree};
        })

    })

    .catch(error => console.log(this.errors = error));
    },
    pathString2Tree(paths, cb) {
  var tree = [];

  _.each(paths, function (path) {
    var pathParts = path.split("/");
    pathParts.shift();
    var currentLevel = tree;

    _.each(pathParts, function (part) {
      var existingPath = _.find(currentLevel, {
        label: part,
      });

      if (existingPath) {
        currentLevel = existingPath.nodes;
      } else {
        var newPart = {
          label: part,
          nodes: [],
        };

        currentLevel.push(newPart);
        currentLevel = newPart.nodes;
      }
    });
  });

  cb(tree);
},
  sendEventCD(label){
    this.$emit('cd-directory-menu', label)
  }
  },
  mounted: function () {
    this.getListPaths()
  },
  watch: {
    trees: function (val) {
      this.setTrees(val);
      },

      getReturnListDirFiles: function () {
        this.getListPaths()
    },
    },
}
</script>

<style scoped>
</style>
