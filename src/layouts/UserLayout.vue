<template>
  <q-layout view="lHh Lpr lFf" >
    <q-header elevated>
      <q-toolbar class="row justify-between" style="height: 8vh">
        <q-toolbar-title class="row">
          <div style="color:black; font-weight: bold; font-size: 28px; cursor: pointer;" @click="returnToDefault()"> User </div>
          <q-input v-show="searchType == 'Name'" dense square flat filled v-model="search" placeholder="Search by name..." class="q-ml-md" bg-color="grey-11" style="margin-left: 5%; width: 59vw;" @keyup.enter="handleSearch()">
            <template v-slot:append>
              <q-icon v-if="search === ''" name="search" color="secondary"/>
              <q-icon v-else name="clear" class="cursor-pointer" @click="search = ''" color="secondary"/>
            </template>
          </q-input>
          <q-input v-show="searchType == 'Tag'" dense square flat filled v-model="search" placeholder="Search by tag..." class="q-ml-md" bg-color="grey-11" style="margin-left: 5%; width: 59vw;" @keyup.enter="handleSearch()">
            <template v-slot:append>
              <q-icon v-if="search === ''" name="search" color="secondary"/>
              <q-icon v-else name="clear" class="cursor-pointer" @click="search = ''" color="secondary"/>
            </template>
          </q-input>
          <q-btn-dropdown flat text-color="black" :label="searchType">
            <q-list>
              <q-item clickable v-close-popup @click="changeSearch('name')">
                <q-item-section>
                  <q-item-label>Name</q-item-label>
                </q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="changeSearch('tag')">
                <q-item-section>
                  <q-item-label>Tag</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </q-toolbar-title>
        <div class="row" style="color:black; padding-right: 20px;">
          <div> Signed in as </div>
          <div style="font-weight: bold; margin-left: 6px;">   {{ $q.localStorage.getItem('username') }} </div>
        </div>
        <q-btn to="/User/Cart" label="Cart" style="margin-right: 20px; background: #ffcf33;" flat text-color="black"/>
        <q-btn to="/User/Profile" label="Profile" style="margin-right: 20px; background: #ffcf33;" flat text-color="black"/>
        <q-btn @click="handleLogout()" label="Logout" style="background: #ffcf33;" flat text-color="black"/>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>

import { useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import GetCoupon from 'src/components/GetCoupon.vue'

export default defineComponent({
  name: 'UserLayout',

  setup() {
    let searchType = ref('Name')
    let search = ref('')
    const $q = useQuasar()

    axios.post('/user/check_for_daily_reward', {
      token: $q.localStorage.getItem('token'),
    }).then( () => {
      axios.get('/user/has_claimable_coupon', { params: {
        token: $q.localStorage.getItem('token')
      }}).then( res => {
        if (res.data == true) {
          $q.dialog({
            component: GetCoupon,
            componentProps: {
              couponDeal: '10% off!'
            }
          }).onOk(() => {
            console.log('OK')
          }).onCancel(() => {
            console.log('Cancel')
          }).onDismiss(() => {
            console.log('Called on OK or Cancel')
          })
        }
      })
    })

    return {
      search,
      searchType,
      changeSearch(type) {
        if (type == 'name') {
          searchType.value = 'Name'
        } else if (type == 'tag') {
          searchType.value = 'Tag'
        } 
      },
      async handleLogout() {
        await axios.post('/user/logout', {
          token: $q.localStorage.getItem('token')
        }).then( res => {
          if (res.data['success'] == false) {
          } else {
            this.$router.push('/')
          }
        })
      },
      async handleSearch() {
        if (search.value.length == 0) return
        if (searchType.value == 'Name') {
          this.$router.push('/User/PostSearch/'+'query/' +search.value)
        } else if (searchType.value == 'Tag') {
          this.$router.push('/User/PostSearch/'+'tag/'+search.value)
        }
      },
      returnToDefault() {
        this.$router.push('/User/Default')
      }
    }
  },
})
</script>
