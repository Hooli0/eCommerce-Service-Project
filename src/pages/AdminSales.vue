<template>
  <q-page class="q-pa-xl" style="background-color: aliceblue" view="lHh Lpr lFf">
    <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px; margin-bottom: 10px"> Sales Data</h4>
    <div class="row">
      <div class="column">
        <h6 style="font-weight: bold; font-family: Arial; margin-top: 5px; margin-bottom: 5px">Listings</h6>
        <h6 v-if="items.length == 0" style="font-weight: bold; font-family: Arial; margin-top: 5px;"> No Listings </h6>
        <div style="height: 55vh; overflow-y:auto;">
            <div class="q-pa-xs" style="background: #f5f5f5; max-width: 350px" v-for="(item, index) in items" :key="index">
              <div class="row justify-left" style="font-weight: bold; font-family: Arial; max-width: 200px; cursor: pointer" @click="displayGraph(index)">
                <div>{{ item.item_name }}</div>
              </div>
            </div>
        </div>
        <q-btn v-if="switchGraph" flat label="Gross Sales" style="float: left; margin-top: 10px;" @click="switchGraph = !switchGraph"/>
        <q-btn v-if="!switchGraph" flat label="Item Sales" style="float: left; margin-top: 10px;" @click="switchGraph = !switchGraph"/>
        <q-btn to="/Admin/Default" flat label="< Back" style="float: left; margin-top: 10px;"/>
      </div>
      <div v-if="switchGraph" style="margin-left: 150px">
        <h6 style="font-weight: bold; font-family: Arial; margin-top: 5px; margin-bottom: 0px"> {{ selectedItem }} </h6>
        <Chart
          :size="{ width: 1200, height: 550 }"
          :data="itemData"
          :margin="margin"
          :direction="direction">
          <template #layers>
            <Grid strokeDasharray="2,2" />
            <Bar :barStyle="{ fill: '#26a69a' }" :maxWidth="40" :dataKeys="['name', 'pl']" />
          </template>
        </Chart>
      </div>
      <div v-if="!switchGraph" style="margin-left: 150px">
        <h6 style="font-weight: bold; font-family: Arial; margin-top: 5px; margin-bottom: 0px"> Gross Sales </h6>
        <Chart
          :size="{ width: 1200, height: 550 }"
          :data="grossData"
          :margin="margin"
          :direction="direction">
          <template #layers>
            <Grid strokeDasharray="2,2" />
            <Bar :barStyle="{ fill: '#26a69a' }" :maxWidth="40" :dataKeys="['name', 'pl']" />
          </template>
        </Chart>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import axios from 'axios'
import { Chart, Grid, Bar } from 'vue3-charts'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'AdminSales',
  components: { Chart, Grid, Bar },

  setup() {
    const $q = useQuasar()
    let items = ref([])
    let selectedItem = ref('itemName')
    let itemData = ref([])
    let grossData = ref([])
    let switchGraph = ref(true)
    const direction = ref('horizontal')
    const margin = ref({
      left: 0,
      top: 20,
      right: 20,
      bottom: 0
    })
    axios.get('/admin/items', { params: {
      token: $q.localStorage.getItem('token')
    }}).then ( res => {
      items.value = JSON.parse(res.data['details'])
      selectedItem.value = items.value[0].item_name
      if (items.value.length == 0) {
        empty.value = true
      } else {
        axios.get('/admin/item/sales/history', { params: {
          token: $q.localStorage.getItem('token'),
          item_id: Number(items.value[0]['item_id'])
        }}).then( res => {
          let parseData = JSON.parse(res.data['details'])
          for (let i = 0; i < parseData.length; i++) {
            parseData[i]['name'] = parseData[i]['date']
            delete parseData[i]['date']
            parseData[i]['pl'] = parseData[i]['quantity_sold']
            delete parseData[i]['quantity_sold']
          }
          itemData.value = parseData
        })
      }
    })

    axios.get('/admin/sales/history', { params: {
      token: $q.localStorage.getItem('token'),
    }}).then( res => {
      let parseData = JSON.parse(res.data['details'])
      for (let i = 0; i < parseData.length; i++) {
        parseData[i]['name'] = parseData[i]['date']
        delete parseData[i]['date']
        parseData[i]['pl'] = parseData[i]['revenue']
        delete parseData[i]['revenue']
      }
      grossData.value = parseData
    })
      
    return {
      items,
      itemData,
      margin,
      direction,
      selectedItem,
      switchGraph,
      grossData,
      async displayGraph(index) {
        selectedItem.value = items.value[index]['item_name']
        await axios.get('/admin/item/sales/history', { params: {
          token: $q.localStorage.getItem('token'),
          item_id: Number(items.value[index]['item_id'])
        }}).then( res => {
          itemData.value = this.cleanData(res.data['details'])
        })
      },
      cleanData(data) {
        let parseData = JSON.parse(data)
        for (let i = 0; i < parseData.length; i++) {
          parseData[i]['name'] = parseData[i]['date']
          delete parseData[i]['date']
          parseData[i]['pl'] = parseData[i]['quantity_sold']
          delete parseData[i]['quantity_sold']
        }
        return parseData
      }
    }
  }

})
</script>

<style lang="scss" scoped>
  .imgWrap {
    max-width: 100%;
    max-height: 100%;
    object-fit: cover;
  }
  .imgBox {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  div::-webkit-scrollbar {
    display: none;
  }
</style>
