<template>
  <q-card class="login q-pa-sm" flat >
    <q-tabs
      v-model="tab"
      dense
      class="text-black"
      active-color="secondary"
      align="justify"
      style="background: $primary; margin-top: 5px"
      >
      <q-tab v-show="showUserTab" name="user" label="User" />
      <q-tab v-show="showAdminTab" name="admin" label="Admin" />
    </q-tabs>
    <q-tab-panels v-model="tab" animated class="loginCard q-pa-md">
      <q-tab-panel name="user">
        <h4 style="font-family: Garamond; font-weight: bold;"> User Login </h4>
        <h6 style="margin-top: 0px; margin-bottom: 20px">Username</h6>
        <q-input v-model="userUsername"/>
        <h6 style="margin-bottom: 20px"> Password</h6>
        <q-input v-model="userPassword" :type="true ? 'password' : 'text'"/>
        <div style="margin-top:30px; font-size: 16px;"> Don't have an account? </div>
        <router-link style="margin-bottom:20px; color: blue; font-size: 16px;" to="/Register">Register</router-link>
        <q-btn @click="handleUserLogin()" style="background: #ffcf33; float: right; margin-top: 60px;" flat label="Log In" />
      </q-tab-panel>

      <q-tab-panel name="admin">
        <h4 style="font-family: Garamond; font-weight: bold;"> Admin Login </h4>
        <h6 style="margin-top: 0px; margin-bottom: 20px">Username</h6>
        <q-input v-model="adminUsername"/>
        <h6 style="margin-bottom: 20px"> Password</h6>
        <q-input v-model="adminPassword" :type="true ? 'password' : 'text'"/>
        <div style="margin-top:30px; font-size: 16px;"> Don't have an account? </div>
        <router-link style="margin-bottom:20px; color: blue; font-size: 16px;" to="/Register">Register</router-link>
        <q-btn @click="handleAdminLogin()" style="background: #ffcf33; float: right; margin-top: 60px;" flat label="Log In" />
      </q-tab-panel>
    </q-tab-panels>
  </q-card>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { Notify, useQuasar } from 'quasar'
import axios from 'axios'

export default defineComponent({
  props: ['guard'],

  setup(props) {
    const $q = useQuasar()
    let done = ref(false)
    let showUserTab = ref(true)
    let showAdminTab = ref(true)
    let userUsername = ref('')
    let userPassword = ref('')
    let adminUsername = ref('')
    let adminPassword = ref('')
    let tab = ref('user')
    let to = ''

    if (props.guard) {
      to = $q.localStorage.getItem('navigatingTo')
      const split = to.toString().split('/')
      if (props.guard) {
        if (split[1] == 'User') {
          showAdminTab.value = false
        } else if (split[1] == 'Admin') {
          showUserTab.value = false
          tab.value = 'admin'
        }
      }
    }

    return {
      showUserTab,
      showAdminTab,
      userUsername,
      userPassword,
      adminUsername,
      adminPassword,
      tab,
      done,
      async handleAdminLogin() {
        await axios.post('/admin/login', {
          username: adminUsername.value,
          password: adminPassword.value
        }).then( async (res) => {
          if (res.data['success'] == false) {
            Notify.create(res.data['message'])
          } else if (res.data['success'] == true) {
            this.saveToLocal(res, 'admin')
            if (props.guard) {
              this.$router.push(to)
              $q.localStorage.set('navigatingTo', '')
            } else {
              this.$router.push('/Admin/Default')
            }
          }
        })
      },
      async handleUserLogin() {
        await axios.post('/user/login', {
          username: userUsername.value,
          password: userPassword.value
        }).then( async (res) => {
          if (res.data['success'] == false) {
            Notify.create(res.data['message'])
          } else if (res.data['success'] == true) {
            this.saveToLocal(res, 'user')
            if (props.guard) {
              this.$router.push(to)
              $q.localStorage.set('navigatingTo', '')
            } else {
              this.$router.push('/User/Default')
            }
          }
        })
      },
      async saveToLocal(res, type) {
        $q.localStorage.set('token', res.data['token'])
        if (type == 'admin') {
          await axios.get('/admin/details', { params: { 
            token: res.data['token'] 
          }}).then( userData => {
            userData = JSON.parse(userData.data['details'])
            $q.localStorage.set('username', userData['username'])
            $q.localStorage.set('firstName', userData['first_name'])
            $q.localStorage.set('lastName', userData['last_name'])
            $q.localStorage.set('email', userData['email'])
          })
        } else {
          await axios.get('/user/details', { params: { 
            token: res.data['token'] 
          }}).then( userData => {
            userData = JSON.parse(userData.data['details'])
            $q.localStorage.set('username', userData['username'])
            $q.localStorage.set('firstName', userData['first_name'])
            $q.localStorage.set('lastName', userData['last_name'])
            $q.localStorage.set('email', userData['email'])
          })
        }
      },
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
</style>
