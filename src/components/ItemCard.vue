<template>
  <q-item class="column" style="background: #f5f5f5; margin-left: 5px; margin-right: 5px">
    <div @click="recordAndNavigate()" style="cursor: pointer;"> 
      <div class="imgBox row justify-center">
        <q-img
          class="imgWrap" 
          :src="itemImg"
        />
      </div>
      <div class="justify-top" style="font-size: 21px; width: 280px; position: relative">
          <div style="overflow: hidden; white-space: nowrap; text-overflow: ellipsis;"> {{ itemDetails.item_name }} </div>
          <div style="font-size:16px;"> ${{ itemDetails.price }} </div>
      </div>
    </div>
  </q-item>
</template>

<script>
import { defineComponent } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'ItemCard',
  props: ['itemDetails'],

  setup(props) {
    const $q = useQuasar()
    const itemImg = 'http://127.0.0.1:2434/static/itemphotos/' + props.itemDetails.item_id + '.jpg'
    return {
      itemImg,
      async recordAndNavigate() {
        await axios.put('/recommendations/record_click', {
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
.imgWrap {
  max-width: 100%;
  max-height: 100%;
}

.imgBox {
  width: 200px;
  height: 180px;
  justify-content: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
