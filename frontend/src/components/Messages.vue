<template style="color: blue;">
  <div class="messages">
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Messages',
  props: ['data', 'type', 'id'],
  computed: {
  ...mapGetters([
      'getToken',
      'getNamePage',
      'getUsername',
      'getHost',
    ]),
  },
  methods: {
      openAlert() {
        console.log(this.data);
        const h = this.$createElement;

        this.$notify({
          title: this.type,
          message: h('i', { style: "font-family: Avenir, Helvetica, Arial, sans-serif;-webkit-font-smoothing: antialiased;-moz-osx-font-smoothing: grayscale;text-align: center;color: #2c3e50;" }, this.data),
          type: this.type,
        });
      },
  },
      watch: {
        id: function () {
            this.openAlert()
        },
    },
}


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
