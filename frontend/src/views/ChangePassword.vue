<template>
  <div class="changePassword">
    <div>
      <el-input
        style="width: 300px; margin: 10px;"
        placeholder="Enter old password"
        v-model="oldPassword"
        type="password"
        show-password
      ></el-input>
    </div>
    <div>
      <el-input
        style="width: 300px; margin: 10px;"
        placeholder="Enter new password"
        v-model="newPassword"
        type="password"
        show-password
      ></el-input>
    </div>

    <el-button @click="sendChangePassword">Send</el-button>
  </div>
</template>

<script>
import axios from "axios";
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "ChangePassword",
  components: {},
  data() {
    return {
      oldPassword: "",
      newPassword: "",
    };
  },
  computed: {
    ...mapGetters(["getToken", "getHost", "getIdMsg"]),
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
    sendChangePassword() {
      const url = this.getHost + "users/api/change-password/";
      const _this = this;
      let config = {
        headers: {
          Authorization: "Token " + this.getToken,
        },
      };
      let data = {
        old_password: this.oldPassword,
        new_password: this.newPassword,
      };
      axios
        .put(url, data, config)
        .then(function(response) {
          console.log(response);
          _this.setTypeMsg("success");
          _this.setDataMsg("You have successfully changed your password");
          _this.setIdMsg(_this.getIdMsg + 1);
          _this.$router.push({ path: "/" });
        })
        .catch(function(error) {
          console.log(error.response.data);
          let errorText = "Password too simple, please try another password";
          if (error.response.data.old_password) {
            errorText = error.response.data.old_password[0];
          } else if (error.response.data.new_password) {
            errorText = error.response.data.new_password[0];
          }
          _this.setTypeMsg("error");
          _this.setDataMsg(errorText);
          _this.setIdMsg(_this.getIdMsg + 1);
        });
    },
  },
};
</script>
