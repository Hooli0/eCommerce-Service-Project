<template>
  <q-layout style="background-color: aliceblue;" view="lHh Lpr lFf">
    <div class="column justify-between" style="padding-left: 10%; padding-right: 10%; padding-top: 0%; padding-bottom: 5%;">
      <q-card class="q-pa-xl back" style="margin: 5%; border-radius: 50px;">  
        <h4 style="font-weight: bold; font-family: Arial; margin-top: -1%"> Register a new account  </h4>
        <h6 style="margin-top: 10px; margin-bottom: 10px"> First Name </h6>
        <q-input v-model="firstName"/>
        <h6 style="margin-top: 50px; margin-bottom: 10px"> Last Name </h6>
        <q-input v-model="lastName"/>
        <h6 style="margin-top: 50px; margin-bottom: 10px"> Username </h6>
        <q-input v-model="username"/>
        <h6 style="margin-top: 50px; margin-bottom: 10px"> Email </h6>
        <q-input v-model="email"/>
        <h6 style="margin-top: 50px; margin-bottom: 10px"> Password </h6>
        <q-input v-model="password" :type="true ? 'password' : 'text'"/>
        <h6 style="margin-top: 50px; margin-bottom: 10px"> Password again </h6>
        <q-input v-model="password2" :type="true ? 'password' : 'text'"/>
        <h6 style="margin-top: 50px; margin-bottom: 10px"> Register as: </h6>
        <div class="row justify-between">
          <q-checkbox v-model="admin" label="Admin" color="secondary" @click="handleAdminToggle()" />
          <q-checkbox v-model="user" label="User" color="secondary" @click="handleUserToggle()"/>
        </div>
        <div>
          <q-btn @click="handleRegister()" style="float: right; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="Register >" flat/>
        </div>
      </q-card>
    </div>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { Notify } from 'quasar'
import axios from 'axios'

export default defineComponent({
  name: 'Register',
  
  setup() {
    let firstName = ref('')
    let lastName = ref('')
    let username = ref('')
    let email = ref('')
    let password = ref('')
    let password2 = ref('')
    let admin = ref(false)
    let user = ref(false)

    return {
      firstName,
      lastName,
      username,
      email,
      password,
      password2,
      admin,
      user,
      async handleRegister() {
        if (firstName.value == '' || lastName.value == '' || username.value == '' || password.value == '' || password2.value == '') {
          Notify.create('Please fill all fields')
          return
        }
        if (!admin.value && !user.value) {
          Notify.create('Must choose registration as admin or user')
          return
        }
        if (admin.value) {
          this.registerAdmin()
        } else if (user.value) {
          this.registerUser()
        } 
      }, 
      async registerAdmin() {
        await axios.post('/admin/register', {
          first_name: firstName.value,
          last_name: lastName.value,
          username: username.value,
          email: email.value,
          password: password.value
        }).then(res => {
          if (res.data['success'] == false) {
            Notify.create('Error in register details: ' + res.data['message'])
          } else {
            this.$router.push('/PostRegister')
          }
        })
      },
      async registerUser() {
        await axios.post('/user/register', {
          first_name: firstName.value,
          last_name: lastName.value,
          username: username.value,
          email: email.value,
          password: password.value
        }).then(res => {
          if (res.data['success'] == false) {
            Notify.create('Error in register details: ' + res.data['message'])
          } else {
            this.$router.push('/PostRegister')
          }
        })
      },
      handleAdminToggle() {
        if (admin.value) {
          user.value = false
        }
      },
      handleUserToggle() {
        if (user.value) {
          admin.value = false
        }
      }
    }
  }
})
</script>

<style lang="scss" scoped>
  .back {
    background: $primary
  }
</style>
