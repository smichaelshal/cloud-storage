<template>
  <div class="menu-file">

  </div>
</template>

<script>
    import axios from 'axios';
    import { mapGetters } from 'vuex';

    export default {
    name: 'MenuFile',
    props: ['name', 'id', 'type', 'isDirectory'],
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
        sendRequsetDownloadFile(){

    const url = 'http://localhost:3000/download/';
    let config = {
          headers: {
              Authorization: 'Token ' + this.getToken,
              }
        }
        let body = {
            "data": {
                "token": this.getToken,
                "pathSource": this.getPathNow,
                "pathDestination": this.getPathHome + '/',
                "idFile": this.id,
                "nameFile": this.name,
                "typeFile": this.type,
                "isDirectory": this.isDirectory
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
            this.sendRequsetDownloadFile()
        },
    },
}
</script>

<style scoped>

</style>
