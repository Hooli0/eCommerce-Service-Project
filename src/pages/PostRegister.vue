<template>
  <q-layout style="background-color: aliceblue;" view="lHh Lpr lFf">
    <div class="column justify-between" style="padding-left: 10%; padding-right: 10%; padding-top: 0%; padding-bottom: 5%;">
      <q-card class="q-pa-xl back" style="margin: 5%; border-radius: 50px;">  
        <h4 style="font-weight: bold; font-family: Arial; margin-top: -1%"> Account Registered  </h4>
        <h6 style="margin-top: 10px; margin-bottom: 10px"> Go back to home page to log in </h6>
        <div>
          <q-btn to="/" style="float: right; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="Back to Log in >" flat/>
        </div>
      </q-card>
    </div>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'

export default defineComponent({  
  name: 'PostRegister'
})
</script>

<style lang="scss" scoped>
  .back {
    background: $primary
  }
</style>

