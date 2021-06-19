<template>
  <div class="directory" @dblclick="$emit('cd-directory', path)"  @contextmenu="rightClick" @click="select">
    <!-- getListSelectedDirectories: {{getListSelectedDirectories}} -->

    <!-- getListSelectedDirectories {{getListSelectedDirectories}} -->
    <!-- openMenuDirectory(name, path) -->
    <el-card class="box-card directory-box" :class="{selected: isSelected}">
        <div slot="header" class="clearfix">
            <span>
              <i class="el-icon-folder" style="font-size: 2rem;"></i>
              <i v-if="usernameUpload != getUsername" class="el-icon-share" style="font-size: 1rem;"></i>

            </span>
            <div v-if="usernameUpload != getUsername">@</div>
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
  props: ['name', 'size', 'path', 'usernameUpload'],
    computed: {
    ...mapGetters([
        'getListSelectedDirectories',
        'getListSelectedLengthDirectories',
        'getPathNow',
        'getListSelectedLength',
        'getUsername',
        
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
      'setListSelectedLength',
    ]),
    // openMenuDirectory(name, path){
    //   //  this.$emit('open-menu-directory', name, path)
    // },
    select(){
      this.isSelected = !this.isSelected;
      if(this.isSelected){
        this.setListSelectedLength(this.getListSelectedLength + 1);

        this.getListSelectedDirectories[this.path.toString()] = {
          "name": this.name,
          "usernameUpload": this.usernameUpload,
        };
      }else{
        delete this.getListSelectedDirectories[this.path];
        this.setListSelectedLength(this.getListSelectedLength - 1);
      }
    },
    rightClick(){   
      if(this.getListSelectedLength === 0){
        this.select();
      }
      this.setIsRightClick(true);
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
