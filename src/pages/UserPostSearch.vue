<template>
  <q-page view="lHh Lpr lFf">
    <h4 v-if="$route.params.type == 'query'" class="q-pa-xl" style="font-weight: bold; font-family: Arial; margin-top: 5px; margin-bottom: 0px"> Results for: {{ $route.params.query }} </h4>
    <h4 v-if="$route.params.type == 'tag'" class="q-pa-xl" style="font-weight: bold; font-family: Arial; margin-top: 5px; margin-bottom: 0px"> Results for tag: {{ $route.params.query }} </h4>
    <div  v-if="loadSearch" class="row justify-center">
      <div v-for="item in items" :key="item.item_name" class="q-pa-sm column justify-center" style="background: #f5f5f5; max-width: 80vw;"> 
        <item-tile v-bind:itemDetails="item" class="column justify-center"/>
      </div>
      <div v-if="items.length == 0">
        No items for search: "{{ $route.params.query }}"
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import ItemTile from '/src/components/ItemTile.vue'
import { useRoute } from 'vue-router'
import { Notify, useQuasar } from 'quasar'
import axios from 'axios'

export default defineComponent({
  
  components: {
    ItemTile
  },
  watch: {
    $route(to) {
      let routeList = to.fullPath.split('/')
      if (routeList[2] == 'PostSearch') {
        this.reloadItems(to)
      }
    }
  },
  setup() {
    const $router = useRoute()
    const $q = useQuasar()
    let loadSearch = ref(false)
    let items = ref([])

    if ($router.params.type == 'query') {
      axios.get('/search/user_general', { params: {
        token: $q.localStorage.getItem('token'),
        string: $router.params.query
      }}).then( res => {
        items.value = res.data.items
        loadSearch.value = true
      })
    } else if ($router.params.type == 'tag') {
      axios.get('/search/tag', { params: {
        token: $q.localStorage.getItem('token'),
        tag: $router.params.query
      }}).then( res => {
        items.value = res.data.items
        loadSearch.value = true
      })
    }

    return {
      items,
      loadSearch,
      async reloadItems(query) {
        let routeList = query.fullPath.split('/')

        if (routeList[3] == 'query') {
          axios.get('/search/user_general', { params: {
            token: $q.localStorage.getItem('token'),
            string: query.params.query
          }}).then( res => {
            items.value = res.data.items
          })
        } else if (routeList[3] == 'tag') {
          axios.get('/search/tag', { params: {
            token: $q.localStorage.getItem('token'),
            tag: query.params.query
          }}).then( res => {
            items.value = res.data.items
            loadSearch.value = true
          })
        }
      }
    }
  }
})

</script>
