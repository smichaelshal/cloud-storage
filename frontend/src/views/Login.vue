<template>
  <div class="login">
    <div style="padding-top: 50px;">
      <div class="div-form">
        <el-input
          style="width: 300px; margin: 10px;"
          placeholder="Enter a username"
          v-model="inputUsername"
          type="text"
        ></el-input>
      </div>

      <div class="div-form">
        <el-input
          style="width: 300px; margin: 10px; padding-top: 15px; padding-bottom: 20px;"
          placeholder="Enter a password"
          v-model="inputPassword"
          type="password"
          show-password
        ></el-input>
      </div>

      <el-button class="" @click="sendLogin">Log In</el-button>

      <div>
        <el-button
          style="padding: 3px 10px; margin-top: 15px"
          type="text"
          @click="toForgetPassword"
          >Forger password</el-button
        >
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters, mapMutations } from "vuex";
const { ipcRenderer } = require("electron");

export default {
  name: "Login",
  components: {},
  data() {
    return {
      inputUsername: "", // u1
      inputPassword: "", //toor4321
      responseData: null,
    };
  },
  computed: {
    ...mapGetters([
      "getToken",
      "getNamePage",
      "getUsername",
      "getHost",
      "getIdMsg",
      "getIdUser",
    ]),
  },
  methods: {
    ...mapMutations([
      "setToken",
      "setNamePage",
      "setUsername",
      "setDataMsg",
      "setTypeMsg",
      "setIdMsg",
      "setIdUser",
    ]),
    sendLogin() {
      const _this = this;
      axios
        .post(this.getHost + "users/api/login/", {
          username: this.inputUsername,
          password: this.inputPassword,
        })

        .then(function(response) {
          _this.setToken(response.data.token);
          ipcRenderer.send("menu", true);
          _this.$router.push({ path: "/" });
          _this.setTypeMsg("success");
          _this.setDataMsg("You have successfully connected");
          _this.setIdUser(response.data.id);
          _this.setIdMsg(_this.getIdMsg + 1);
          _this.setUsername(_this.inputUsername);
        })

        .catch(function(response) {
          console.log(response.response.data);
          _this.setTypeMsg("error");
          _this.setDataMsg("The username or password is incorrect");
          _this.setIdMsg(_this.getIdMsg + 1);
        });
    },
    toForgetPassword() {
      this.$router.push({ path: "/forgot-password" });
    },
  },
  mounted: function() {
    this.setNamePage("/login");
  },
  watch: {},
};
</script>

<style scoped></style>
