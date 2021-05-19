<template>
  <div class="home">
    <Desktop v-if="getToken.length > 0" />
    <div v-else>
      <h1>Not registered yet? Register today</h1>
      <el-button type="primary" @click="toRegister">To Register</el-button>
      <!-- <br /> -->
      <h3>Are you a registered user?</h3>
      <el-button type="primary" style="margin-top: 10px;" @click="toLogin"
        >To Login</el-button
      >
      <h3>Forgot your password?</h3>
      <el-button
        type="primary"
        style="margin-top: 10px;"
        @click="toForgetPassword"
        >To reset password</el-button
      >
    </div>
  </div>
</template>

<script>
import Desktop from "@/components/Desktop.vue";
import { mapGetters } from "vuex";

export default {
  name: "Home",
  components: {
    Desktop,
  },
  computed: {
    ...mapGetters(["getToken", "getUsername"]),
  },
  methods: {
    toLogin() {
      this.$router.push({ path: "/login" });
    },
    toRegister() {
      this.$router.push({ path: "/register" });
    },
    toForgetPassword() {
      this.$router.push({ path: "/forgot-password" });
    },
  },
};
</script>
