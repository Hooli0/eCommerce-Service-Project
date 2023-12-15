<template>
  <q-layout class="row justify-center backImg" style="margin: 0px; background-color: aliceblue;" view="lHh Lpr lFf">
    <div style="column justify-center margin-bottom: 50px">
      <h6>Please sign in</h6>
      <login-card v-bind:guard="true"/>
    </div>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import LoginCard from 'src/components/LoginCard.vue'

export default defineComponent({
  name: 'RequireAuth',
  components: {
     LoginCard 
    },
})

</script>
