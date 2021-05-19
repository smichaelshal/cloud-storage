<template>
  <div class="register">
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
          style="width: 300px; margin: 10px; padding-top: 15px;"
          placeholder="Enter a email"
          v-model="inputEmail"
          type="email"
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

      <el-button class="" @click="sendRegister">Register</el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "Register",
  components: {},
  data() {
    return {
      inputUsername: "",
      inputPassword: "",
      inputEmail: "",
      responseData: null,
      errors: null,
      bla: "bla",
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
    sendRegister() {
      const _this = this;
      const url = this.getHost + "users/api/register/";
      const data = {
        username: this.inputUsername,
        email: this.inputEmail,
        password: this.inputPassword,
      };

      let config = {
        headers: {},
      };

      axios
        .post(url, data, config)

        .then(function(response) {
          console.log(response);
          _this.setTypeMsg("success");
          _this.setDataMsg("You have successfully registered");
          _this.setIdMsg(_this.getIdMsg + 1);

          _this.$router.push({ path: "/login" });
        })

        .catch(function(error) {
          console.log(error);
          let errorText = "The username or password is incorrect";
          let errorData = error.response.data;
          console.log(errorData);
          if (errorData.username) {
            errorText = "Username: " + errorData.username[0];
          } else if (errorData.email) {
            errorText = "Email: " + errorData.email[0];
          } else if (errorData.password) {
            errorText = "Password: " + errorData.password[0];
          }

          _this.setTypeMsg("error");
          _this.setDataMsg(errorText);
          _this.setIdMsg(_this.getIdMsg + 1);
        });
    },
  },
  mounted: function() {
    this.setNamePage("/register");
  },
  watch: {
    errors() {
      // if(val.response.data.username !== undefined){
      //   this.Error(val.response.data.username[0], 'username');
      // }else if(val.response.data.password !== undefined){
      //   this.Error(val.response.data.password[0], 'username');
      // }else if(val.response.data.email !== undefined){
      //   this.Error(val.response.data.email[0], 'email');
      // }else{
      //   this.Error(val.response.data, '');
      // }
    },
  },
};
</script>

<style scoped></style>
