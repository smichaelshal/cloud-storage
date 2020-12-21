<template>
  <div class="directory" @dblclick="$emit('cd-directory', path)"  @contextmenu="setIsRightClick(true)" @click="select">
    <!-- openMenuDirectory(name, path) -->
    <el-card class="box-card directory-box" :class="{selected: isSelected}">
        <div slot="header" class="clearfix">
            <span>
              <i class="el-icon-folder" style="font-size: 2rem;"></i>
            </span>
        </div>
        <div class="text item">
            <!-- {{name}} -->
            <span v-if="name.length < 17">{{name}}</span>
            <span v-if="name.length >= 17">{{name.slice(0, 15) + '...'}}</span>
        </div>
    </el-card>
  </div>
</template>

<script>
import { mapGetters, mapMutations} from 'vuex';

export default {
  name: 'Directory',
  props: ['name', 'size', 'path'],
    computed: {
    ...mapGetters([
        'getListSelectedDirectories',
        'getListSelectedLengthDirectories',
        'getPathNow',
    ]),
  },
  data(){
    return {
      isSelected: false,
    }
  },
  methods: {
    ...mapMutations([
      'setIsRightClick',
    ]),
    openMenuDirectory(name, path){
      console.log(name, path);
      // console.log(name, path);
      //  this.$emit('open-menu-directory', name, path)
    },
    select(){
      this.isSelected = !this.isSelected;
      if(this.isSelected){
        this.getListSelectedDirectories[this.path.toString()] = {
          "name": this.name,          
        };
      }else{
        delete this.getListSelectedDirectories[this.path]
      }
    },

  },
      watch: {
        getPathNow: function () {
            this.isSelected = false;
        },
    },
}
</script>

<style scoped>
.directory-box{
  width: 180px; float: right;
  margin-right: 10px;
  margin-top: 10px;
}
.selected{
  border: 1px solid #727272;
}

/* @click="$emit('create-event', sendMsg())" */
</style>
