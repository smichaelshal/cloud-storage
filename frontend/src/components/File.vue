<template>
  <div class="file" @contextmenu="rightClick" @click="select" >

    <!-- getListSelected {{getListSelected}} -->

  

    <el-card class="box-card file-box" :class="{selected: isSelected}">
       <div slot="header" class="clearfix">
            <span>
              <i class="el-icon-document" style="font-size: 2rem;"></i>
            </span>
        </div>
        
        <div class="text item">
            <span v-if="getName().length < 17">{{getName()}}</span>
            <span v-if="getName().length >= 17">{{getName().slice(0, 15) + '...'}}</span>
        </div>
    </el-card>
    
  </div>
</template>

<script>
import { mapGetters, mapMutations} from 'vuex';

export default {
  name: 'File',
  props: ['name', 'type', 'id','size'],
  data(){
    return {
      nameView: null,
      maxLength: 16,
      isSelected: false,
      isRightClick: false,
    }
  },
  components: {
  },
  computed: {
    ...mapGetters([
        'getListSelected',
        'getListSelectedLength',
        'getPathNow',
    ]),
  },
  methods: {
    ...mapMutations([
      'setIsRightClick',
      'setListSelectedLength',
    ]),
    openMenuFile(name, id, type){
      this.$emit('open-menu-file', name, id, type, false)
    },
    getName(){
      if(this.type === ''){
        return this.name
      }
      return this.name + '.' + this.type;
    },

    viewName(){
      this.nameView = this.getName();
    },
    select(){
      this.isSelected = !this.isSelected;
      if(this.isSelected){
        this.setListSelectedLength(this.getListSelectedLength + 1);
        this.getListSelected[this.id.toString()] = {
          "name": this.name,
          "type": this.type,
          "size": this.size,
          
        };

      }else{
        delete this.getListSelected[this.id]
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
.file-box{
  width: 180px;
  float: right;
  margin-right: 10px;
  margin-top: 10px;
}
.selected{
  /* border-style: solid; */
  /* border-color: #f48c06; */
  /* background: #727272; */
  /* color: white; */
  border: 1px solid #727272;
}


</style>
