<template>
  <q-layout style="background-color: aliceblue" view="lHh Lpr lFf">
    <div class="row justify-between" style="padding-left: 10%; padding-right: 10%; padding-top: 5%; padding-bottom: 5%;">
      <div class="column">
        <h1 style="margin-bottom: 10px; font-weight: bold; font-family: Garamond"> COMP3900 </h1>
        <h6 style="margin-top: 0px"> E-commerce Project (Development build)</h6>
        <q-btn @click="setupTestEnv()" style="background: #ffcf33; float: right; margin-top: 20px;" flat :label="testBtnName" :disable="testBtnDisable" />
        <h6 v-if="testBtnDisable" style="margin-bottom: 10px">Loading... (this may take up to 10 seconds)</h6>
        <div v-if="environLoaded">
          <h6>Testing environment loaded!</h6>
          <b>Admins</b>
          <div>Username: MainAdmin Password: password</div>
          <div>Username: OtherAdmin Password: password</div>
          <b>Users</b>
          <div>Username: User1 Password: password</div>
          <div>Username: User2 Password: password</div>
        </div>
      </div>
      <login-card v-bind:guard="false" />
    </div>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'
import LoginCard from 'src/components/LoginCard.vue'

export default defineComponent({
  name: 'LandingPage',
  components: {
    LoginCard
  },

  setup() {
    let testBtnName = ref('Load Testing Environment')
    let testBtnDisable = ref(false)
    let environLoaded = ref(false)
    const $q = useQuasar()
    
    return {
      testBtnName,
      testBtnDisable,
      environLoaded,
      async setupTestEnv() {
        testBtnDisable.value = true
        await axios.post('/test/reset')
        testBtnName.value = 'Reset testing environment'
        testBtnDisable.value = false
        environLoaded.value = true
      }
    }
  }

})
</script>

<style lang="scss" scoped>
  .login {
    background: $primary;
    height: 670px;
    width: 550px;
    border-radius: 50px;
  }
  .loginCard {
    background: $primary;
    padding-top: 10px;
    padding-bottom: 30px;
  }
  ul::-webkit-scrollbar {
  width: 4px;
  height: 8px;
  }
  ul::-webkit-scrollbar-thumb {
  background-color: rgb(189, 189, 189);    /* color of the scroll thumb */
  border-radius: 20px;       /* roundness of the scroll thumb */
  }
</style>
