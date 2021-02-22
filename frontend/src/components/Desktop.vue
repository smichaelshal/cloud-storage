<template>
  <div class="desktop">
    
    <!-- <el-row style="height: 100%;"> -->
      <el-col :span="6">
        <SideMenu v-if="false" @cd-directory-menu="blas"/>
      </el-col>
      <el-col :span="24">
         <MainDesktop :pathSideMenu="path"/>
      </el-col>
  <!-- </el-row> -->

  </div>
</template>

<script>
import SideMenu from '@/components/SideMenu.vue'
import MainDesktop from '@/components/MainDesktop.vue'


export default {
  name: 'Desktop',
  props: {
  },
  components: {
    SideMenu,
    MainDesktop,
  },
  methods: {
    blas(val){
      this.path = val;
      console.log("blas: ", val);
    },
  },
  data(){
    return {
      path: null
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* .desktop{
  height: 100%;
  background: red;
  width: 100%;
  left: 0;
  top: 0;
} */
</style>
