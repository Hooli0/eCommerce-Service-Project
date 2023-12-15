<template>
  <router-view />
</template>
<script>
import { defineComponent } from 'vue';
import axios from 'axios'

export default defineComponent({
  name: 'App',
  setup() {
    axios.defaults.baseURL = 'http://localhost:2434';
    // THIS DOES NOT WORK. CORS BLOCKED??? WHYYYYY
    // axios.defaults.headers.common['DefaultSending'] = 'PLEASESEEME';
  }
})
</script>
