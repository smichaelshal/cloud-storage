<template>
  <div class="menu-directory">
  </div>
</template>

<script>
    import axios from 'axios';
    import { mapGetters } from 'vuex';

    export default {
    name: 'MenuDirectory',
    props: ['name', 'path'],
    computed: {
    ...mapGetters([
      'getToken',
      'getNamePage',
      'getUsername',
      'getHost',
      'getPathNow',
      'getPathHome',
    ]),
  },
    methods: {
        sendRequsetDownloadDirectory(){

    const url = 'http://localhost:3000/download/';
    let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
        }
        let body = {
            "data": {
                "token": this.getToken,
                "pathSource": this.path,
                "pathDestination": this.getPathHome,
                "idFile": '',
                "nameFile": this.name,
                "typeFile": '',
                "isDirectory": true
            }
        }

    axios.post(url, body, config)
    .then(function (response) {
        console.log(response.data);
    })

    .catch(error => console.log(this.errors = error));

        },
    },
    watch: {
        name: function () {
            this.sendRequsetDownloadDirectory()
        },
    },
}
</script>

<style scoped>

</style>
