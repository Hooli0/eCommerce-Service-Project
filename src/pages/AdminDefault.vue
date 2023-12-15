<template>
  <q-page style="padding-top: 30px; background-color: aliceblue" view="lHh Lpr lFf">
    <div class="row justify-between" style="padding-left: 10%; padding-right: 10%; padding-top: 0%; padding-bottom: 5%;">
      <div class="column">
        <h1 style="margin-bottom: 10px; font-weight: bold; font-family: Garamond"> Listings </h1>
        <h6 v-show="empty" style="margin-top: 0px; margin-bottom: 10px"> You have no current listings</h6>
        <div>
          <ul style="margin-left:0px; padding-left:0px; width: 520px; height: 100%; overflow: auto;" role="list">
            <li v-for="(item, index) in items" :key="index">
              <admin-listing-card  v-on:deleteItem="refresh()" v-bind:itemDetails="item" />
              <div style="margin-top: 20px; margin-bottom: 20px; height: 1px; background-color: rgb(37, 37, 37);" />
            </li>
          </ul>
        </div>
      </div>
      <div class="column justify-top" style="padding-top: 170px">
        <q-card class="addListingCard q-pa-xl" flat >
          <h4 style="font-family: Arial; font-size: 100px; margin-top: 0px; margin-bottom: 50px; line-height: 100px;"> Add New Listing </h4>
          <q-btn to="/Admin/Listings" style="background: #ffcf33; float: right; margin-top: 0px; margin-bottom: 10px" flat label="Continue >" />
        </q-card>
        <div>
          <q-btn to="/Admin/Sales" style="background: #ffcf33; float: right; margin-top: 50px;" flat label="Sales >" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, onBeforeMount, onMounted, ref } from 'vue'
import axios from 'axios'
import AdminListingCard from 'components/AdminListingCard.vue'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'AdminDefault',
  components: {
    AdminListingCard
  },

  setup() {
    const $q = useQuasar()
    let empty = ref(false)
    let items = ref([])
    axios.get('/admin/items', { params: {
      token: $q.localStorage.getItem('token')
    }}).then ( res => {
      items.value = JSON.parse(res.data['details'])
      if (items.value.length == 0) {
        empty.value = true
      }
    })

    return {
      items,
      empty,
      async refresh() {
        axios.get('/admin/items', { params: {
          token: $q.localStorage.getItem('token')
        }}).then ( res => {
          items.value = JSON.parse(res.data['details'])
          if (items.value.length == 0) {
            empty.value = true
          }
        })
      }
    }
  }
})
</script>

<style lang="scss" scoped>
  .addListingCard {
    background: $primary;
    width: 550px;
    border-radius: 50px;
    padding-bottom: 15%;
  }
  ul::-webkit-scrollbar {
    width: 4px;
    height: 8px;
  }
  ul::-webkit-scrollbar-thumb {
    background-color: rgb(189, 189, 189);
    border-radius: 20px;
  }
</style>
