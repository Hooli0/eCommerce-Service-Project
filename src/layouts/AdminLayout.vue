<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar style="height: 8vh">
        <q-toolbar-title >
          <div style="color:black; font-weight: bold; font-size: 28px; cursor: pointer;" @click="returnToDefault()"> Admin </div>
        </q-toolbar-title>
        <div class="row" style="color:black; padding-right: 20px;">
          <div> Signed in as </div>
          <div style="font-weight: bold; margin-left: 6px;">   {{ $q.localStorage.getItem('username') }} </div>
        </div>
        <q-btn to="/Admin/Profile" label="Profile" style="margin-right: 20px; background: #ffcf33;" flat text-color="black"/>
        <q-btn @click="handleLogout()" label="Logout" style="background: #ffcf33;" flat text-color="black"/>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>

import { Notify, useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'AdminLayout',

  setup() {
    const $q = useQuasar()
    return {
      async handleLogout() {
        await axios.post('/admin/logout', {
          token: $q.localStorage.getItem('token')
        }).then( res => {
          if (res.data['success'] == true) {
            this.$router.push('/')
          }
        })
      },
      returnToDefault() {
        this.$router.push('/Admin/Default')
      }
    }
  }
})
</script>
