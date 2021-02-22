<template>
  <div class="menu">
    <router-link to="/" style="margin: 10px;">Home</router-link>
    <router-link to="/login" style="margin: 10px;">Login</router-link>
    <router-link to="/register" style="margin: 10px;">Register</router-link>
    <router-link to="/logout" style="margin: 10px;">Logout</router-link>
    <router-link to="/settings" style="margin: 10px;">Settings</router-link>
    <router-link to="/forget-password" style="margin: 10px;">Forget Password</router-link>
    <router-link to="/reset-password" style="margin: 10px;">Reset Password</router-link>

    {{getNamePage}}

  </div>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  name: 'Menu',
  props: {
  },
  computed: {
  ...mapGetters([
      'getToken',
      'getNamePage',
      'getUsername',
      'getHost',
    ]),
  },
  methods: {
    toRout(path){
      this.$router.push({ path: path })
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

</style>
