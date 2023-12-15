<template>
  <q-page view="lHh Lpr lFf">
    <div class="q-pa-xl">
      <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Recomended </h4>
      <!-- WHY DOESN'T THIS WORK -->
      <h6 v-if="!loadItems"> Loading... </h6>
        <vue-horizontal v-if="loadItems" responsive style="background: #f5f5f5;" class="horizontal">
          <div v-for="item in items" :key="item.item_name">
            <ItemCard v-bind:itemDetails="item" />
          </div>
        </vue-horizontal>
    </div>
    <div class="q-pa-xl" style="padding-top: 0px; padding-bottom: 10px">
      <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Browse by Tags </h4>
      <h6 v-if="!loadTags"> Loading... </h6>
      <vue-horizontal v-if="loadTags" responsive style="background: #f5f5f5;" class="horizontal">
        <div v-for="(tag, index) in tags" :key="index">
          <tag-card v-bind:tag="tag"/>
        </div>
      </vue-horizontal>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onMounted, onBeforeMount } from 'vue'
import { useQuasar } from 'quasar'
import axios from 'axios'
import VueHorizontal from "vue-horizontal";
import ItemCard from "/src/components/ItemCard.vue"
import TagCard from "/src/components/TagCard.vue"

export default defineComponent({
  name: 'UserDefault',
  components: {
    VueHorizontal,
    ItemCard,
    TagCard
  },

  setup() {
    let items = ref([])
    let loadItems = ref(false)
    let loadTags = ref(false)
    const $q = useQuasar()
    let options = ref({})
    let tags = ref([])
    
    onBeforeMount(async () => {
      axios.get('/recommendations/from_user', { params: {
        token: $q.localStorage.getItem('token'),
        number_of_recs: 10
      }}).then ( async res => {
          let itemIds = res.data['item_ids']
          items.value = itemIds
          loadItems.value = true
        })
      axios.get('/all_tags', { params : {
        token: $q.localStorage.getItem('token')
      }}).then( async (res) => {
        tags.value = res.data['tags']
        loadTags.value = true
      })
    })

    return {
      items,
      options,
      tags, 
      loadItems,
      loadTags,
    }
  }
})

</script>
