<template>
  <div id="app">
    <!-- getDataToSendWs: {{getDataToSendWs}} -->
    <Messages :type="getTypeMsg" :data="getDataMsg" :id="getIdMsg" />
    <router-view />
  </div>
</template>

<script>
import Messages from "@/components/Messages.vue";

const { ipcRenderer } = require("electron");
import { mapGetters, mapMutations } from "vuex";
import axios from "axios";

export default {
  name: "App",
  components: {
    Messages,
  },
  data() {
    return {
      connection: null,
    };
  },
  created() {
    ipcRenderer.on("menu", (event, data) => {
      if (data === "?") {
        ipcRenderer.send("menu", this.getToken.length > 0);
        return;
      } else if (data === "logout") {
        this.sendLogout();
        this.setTypeMsg("success");
        this.setDataMsg("You have successfully logged out");
        this.setIdMsg(this.getIdMsg + 1);
        return;
      }
      this.$router.push({ path: "/" + data });
    });
  },
  computed: {
    ...mapGetters([
      "getToken",
      "getUsername",
      "getHost",
      "getDataMsg",
      "getTypeMsg",
      "getIdMsg",
      "getListSelected",
      "getWsData",
      "getDataToSendWs",
      "getIsChangeDataToSendWs",
      "getReturnListDirFiles",
      "getIdUser",
      "getHost_ws",
    ]),
  },
  methods: {
    ...mapMutations([
      "setToken",
      "setUsername",
      "setIdMsg",
      "setDataMsg",
      "setTypeMsg",
      "setWsData",
      "setDataToSendWs",
      "setIsChangeDataToSendWs",
      "setReturnListDirFiles",
    ]),
    sendLogout() {
      const _this = this;
      const url = this.getHost + "users/api/logout/";
      let config = {
        headers: {
          Authorization: "Token " + this.getToken,
        },
      };
      let data = {};

      axios
        .post(url, data, config)
        .then(function resetDataUser() {
          _this.setToken("");
          _this.setUsername("");
          ipcRenderer.send("menu", false);
        })
        .catch((error) => console.log(error.response));
    },
  },
  watch: {
    getToken: function(val) {
      const _this = this;
      if (val.length > 0) {
        this.connection = new WebSocket(
          _this.getHost_ws + `ws/message/${this.getIdUser}/`
        );

        this.connection.onopen = function() {
          _this.connection.send(
            JSON.stringify({ type: "connect", token: _this.getToken })
          );
        };

        this.connection.onmessage = function(event) {
          console.log(event);
          let eventData = JSON.parse(event.data);
          let typeData = eventData.typeMsg;
          if (typeData === "directory") {
            _this.setReturnListDirFiles(!_this.getReturnListDirFiles);
          }
        };
      }
    },
    getIsChangeDataToSendWs: function() {
      console.log("getIsChangeDataToSendWs_1: ");
      // console.log(this.getDataToSendWs.ids);
      this.connection.send(JSON.stringify(this.getDataToSendWs));
    },
  },
  mounted: function() {},
};
</script>

<style scope>
#app {
  margin-top: 0px !important;
  margin-left: 0px !important;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  /* padding: 30px; */
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
