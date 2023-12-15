<template>
  <q-item class="column" style="height: 200px; background: white">
    <div class="row justify-center" @click="toItem()" style="cursor: pointer;"> 
      <div>
        <div class="imgBox">
          <q-img 
            :src="itemImg"
            class="imgWrap"
          />
        </div>
      </div>
      <div class="justify-top q-pa-md" style="font-size: 20px; width: 280px; position: relative">
        <div class="row justify-between" style="font-size:28px"> 
          <div style="overflow: hidden; white-space: nowrap; text-overflow: ellipsis;"> {{ itemDetails.item_name }} </div>
        </div> 
        <div style="font-size:16px"> Tags: {{ itemDetails.tags.toString() }} </div> 
        <div style="font-size:16px" > Description: {{ itemDetails.description }} </div> 
        <div class="column" style="float: right"> 
          <div style="font-size:16px"> Price: ${{ itemDetails.price }} </div>
          <div style="font-size:16px"> Stock: {{ itemDetails.stock }} </div>
        </div> 
      </div>
    </div>
  </q-item>
</template>

<script>
import { defineComponent } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'ItemTile',
  props: ['itemDetails'],

  setup(props) {
    const $q = useQuasar()
    const itemImg = 'http://127.0.0.1:2434/static/itemphotos/' + props.itemDetails.item_id + '.jpg'
    return {
      itemImg,
      toItem() {
        axios.put('/recommendations/record_click', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(props.itemDetails['item_id'])
        })
        this.$router.push('/User/Item/'+props.itemDetails.item_id)
      }
    }
  }
})
</script>

<style lang="scss" scoped>
.imgBox {
  width: 200px;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.imgWrap {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}
</style>
