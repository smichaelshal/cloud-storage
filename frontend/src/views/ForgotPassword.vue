<template>
  <div class="forgot-password">
    <el-input style="width: 300px; margin: 10px;" placeholder="Enter a email" v-model="email" type="email" :disabled="isSend"></el-input>
    <el-button :disabled="isSend" @click="sendRequestRestPassword">Send</el-button>

    <div style="margin: 20px;" v-if="isSend">
        <el-input style="width: 300px; margin: 10px;" placeholder="Enter a code number" v-model="codeNumber" type="text"></el-input>
    </div>

    <div style="margin: 20px;" v-if="isSend">
        <el-input style="width: 300px; margin: 10px;" placeholder="Enter a new password" v-model="password" type="password" ></el-input>
    </div>
    <!-- <div style="margin: 20px;" v-if="isSend">
        <el-input style="width: 300px; margin: 10px;" placeholder="Enter a new password" v-model="password" type="password" :disabled="isSend"></el-input>
    </div> -->

    <div v-if="isSend">
        <el-button @click="sendThePassword">Send</el-button>
    </div>

    <div style="margin: 20px;" v-if="isSend">
        <el-button style="padding: 3px 10px" type="text" @click="sendRequestRestPassword">The email did not arrive? send again.</el-button>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  name: 'ForgotPassword',
  components: {
  },
  computed: {
...mapGetters([
        'getHost',
    ]),
  },
  data(){
      return {
          email: '',
          isSend: false,
          codeNumber: '',
          password: '',
          isArrive: false,
      }
  },
  methods: {
      sendRequestRestPassword(){
        this.isSend =  true;
          
        const _this = this;

        axios.post(this.getHost + 'users/api/password_reset/', {
        email: this.email,

        })
        .then(function getCodeToResetPassword(response) {
            console.log(response.data);
             _this.isArrive = true;
           

        })
        .catch(error => console.log(error.response));
      },
    sendThePassword(){
        const _this = this;
        axios.post(this.getHost + 'users/api/password_reset/confirm/', {
            token: _this.codeNumber,
            password: _this.password,
        })

        .then(function getCodeToResetPassword(response) {
            console.log(response.data);
            _this.$router.push({ path: '/login'});
        })
        .catch(error => console.log(error.response));

    }
  }
}
</script>
