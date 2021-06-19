<template>
  <div class="forgot-password">
    <el-input
      style="width: 300px; margin: 10px;"
      placeholder="Enter a email"
      v-model="email"
      type="email"
      :disabled="isSend"
    ></el-input>
    <el-button :disabled="isSend" @click="sendRequestRestPassword"
      >Send</el-button
    >

    <div style="margin: 20px;" v-if="isSend">
      <el-input
        style="width: 300px; margin: 10px;"
        placeholder="Enter a code number"
        v-model="codeNumber"
        type="text"
      ></el-input>
    </div>

    <div style="margin: 20px;" v-if="isSend">
      <el-input
        style="width: 300px; margin: 10px;"
        placeholder="Enter a new password"
        v-model="password"
        type="password"
        show-password
      ></el-input>
    </div>
    <!-- <div style="margin: 20px;" v-if="isSend">
        <el-input style="width: 300px; margin: 10px;" placeholder="Enter a new password" v-model="password" type="password" :disabled="isSend"></el-input>
    </div> -->

    <div v-if="isSend">
      <el-button @click="sendThePassword">Send</el-button>
    </div>

    <div style="margin: 20px;" v-if="isSend">
      <el-button
        style="padding: 3px 10px"
        type="text"
        @click="sendRequestRestPassword"
        >The email did not arrive? send again.</el-button
      >
    </div>
    <div v-if="waitVar">
      <i class="el-icon-loading" style="font-size: 2rem;"></i>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "ForgotPassword",
  components: {},
  data() {
    return {
      email: "",
      isSend: false,
      codeNumber: "",
      password: "",
      isArrive: false,
      waitVar: false,
    };
  },
  computed: {
    ...mapGetters([
      "getToken",
      "getNamePage",
      "getUsername",
      "getHost",
      "getIdMsg",
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
    ]),
    sendRequestRestPassword() {
      // this.isSend = true;
      this.waitVar = true;

      const _this = this;

      axios
        .post(this.getHost + "users/api/password_reset/", {
          email: this.email,
        })
        .then(function getCodeToResetPassword(response) {
          _this.waitVar = false;
          console.log(response.data);
          _this.isArrive = true;
          _this.isSend = true;
        })
        .catch(function(error) {
          _this.waitVar = false;

          console.log(error.response.data);
          let errorText = "Password too simple, please try another password";
          if (error.response.data.email) {
            errorText = error.response.data.email[0];
          } else if (1 === 1) {
          }
          _this.setTypeMsg("error");
          _this.setDataMsg(errorText);
          _this.setIdMsg(_this.getIdMsg + 1);
        });
    },
    sendThePassword() {
      const _this = this;
      axios
        .post(this.getHost + "users/api/password_reset/confirm/", {
          token: _this.codeNumber,
          password: _this.password,
        })

        .then(function getCodeToResetPassword(response) {
          console.log(response.data);
          _this.$router.push({ path: "/login" });
        })
        // .catch(error => console.log(error.response));
        .catch(function(error) {
          let errorText = "Password too simple, please try another password";
          _this.setTypeMsg("error");
          _this.setDataMsg(errorText);
          _this.setIdMsg(_this.getIdMsg + 1);
        });
    },
  },
};
</script>
