<template>
  <div class="home">
    <Desktop v-if="getToken.length > 0" />
      <div v-else>
       Not registered yet?
      Register today
      </div>
  </div>
</template>

<script>
import Desktop from '@/components/Desktop.vue'
import { mapGetters } from 'vuex';


export default {
  name: 'Home',
  components: {
    Desktop
  },
    computed: {
    ...mapGetters([
        'getToken',
        'getUsername',
    ]),
  },
}
</script>
