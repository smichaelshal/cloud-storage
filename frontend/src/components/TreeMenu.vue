<template>
  <div class="tree-menu">
    <div>


      <div v-if="nodes !== undefined && nodes.length > 0">
        <el-submenu :index="label">
        <template slot="title">
          <span @click="$emit('cd-directory-menu', label)">{{label}}</span>
        </template>
        <el-menu-item-group>

              <tree-menu 
      v-for="node in nodes" 
      :nodes="node.nodes" 
      :label="node.label"
      :key="node.label"
      @cd-directory-menu="sendEvent"
    >
    
    </tree-menu>

        </el-menu-item-group>
         </el-submenu>
      </div>

     <div v-if="nodes !== undefined && nodes.length === 0">
          <el-menu-item :index="label" @click="$emit('cd-directory-menu', label)">
              <template slot="title">
                  <span>{{label}}</span>
              </template>
          </el-menu-item>
     </div>
      

    </div>



    
  </div>
</template>

<script>
  export default { 
    props: [ 'label', 'nodes' ],
    name: 'tree-menu',
    methods: {
      sendEvent(item){
          this.$emit('cd-directory-menu', item)
      },
    }
  }
</script>