<template>
  <q-page class="backImg" view="lHh Lpr lFf" style="min-height: 650px; background-color: aliceblue">
    <div class="column justify-between" style="padding-left: 0%; padding-right: 0%; padding-top: 0%; padding-bottom: 0%;">
      <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Change Username </h4>
      <div> Current username: {{ $q.localStorage.getItem('username') }}</div>
      <q-input filled dense v-model="username" />
      <div> 
        <q-btn @click="changeUsername()" style="float: right; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="Change User" flat/>
      </div>
      <h4 style="font-weight: bold; font-family: Arial"> Change password </h4>
      <q-input filled dense v-model="password" :type="true ? 'password' : 'text'" />
      <div>
        <q-btn @click="changePassword()" style="float: right; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="Change pass" flat/>
      </div>
      <div style="margin-bottom: 0px"> Current email: {{ $q.localStorage.getItem('email') }}</div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { Notify, useQuasar } from 'quasar'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default defineComponent({
  setup() {
    const $q = useQuasar()
    const $router = useRoute()
    let username = ref('')
    let password = ref('')
    const type = $router.matched[0]

    return {
      username,
      password,
      async changeUsername() {
        if ($router.matched[0].path == '/Admin') {
          await axios.post('/admin/change_username', {
            token: $q.localStorage.getItem('token'),
            new_username: username.value
          }).then( res => {
            if (res.data['success'] == true) {
              $q.localStorage.set('username', username.value)
              Notify.create('Username changed')
              username.value = ''
            }
          })
        } else if ( $router.matched[0].path == '/User') {
          await axios.post('/user/change_username', {
            token: $q.localStorage.getItem('token'),
            new_username: username.value
          }).then( res => {
            if (res.data['success'] == true) {
              $q.localStorage.set('username', username.value)
              Notify.create('Username changed')
              username.value = ''
            }
          })
        }
      },
      async changePassword() {
        if ($router.matched[0].path == '/Admin') {
          await axios.post('/admin/change_password', {
            token: $q.localStorage.getItem('token'),
            new_password: password.value
          }).then( res => { 
            if (res.data['success'] == true) {
              Notify.create('Password changed')
              password.value = ''
            } else {
              Notify.create(res.data['message'])
            }
          })
        } else if ($router.matched[0].path == '/User') {
          await axios.post('/user/change_password', {
            token: $q.localStorage.getItem('token'),
            new_password: password.value
          }).then( res => { 
            if (res.data['success'] == true) {
              Notify.create('Password changed')
              password.value = ''
            } else {
              Notify.create(res.data['message'])
            }
          })
        }
      }
    }
  }
})
</script>

<style lang="scss" scoped>
  .backImg {
    background-color: aliceblue;
  }
</style>
