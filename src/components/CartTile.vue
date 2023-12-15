<template>
  <q-item class="column" style="height: 200px; background: white">
    <div class="row justify-center"> 
      <div>
        <div class="imgBox">
          <q-img 
            :src="itemImg"
            class="imgWrap"
          />
        </div>
      </div>
      <div class="justify-top q-pa-md" style="font-size: 20px; position: relative">
        <div class="row justify-between" style="font-size:28px"> 
          <div style="overflow: hidden; white-space: nowrap; text-overflow: ellipsis;"> {{ itemDetails.item_name }} </div>
          <q-btn  v-if="editable" @click="deleteItem()" icon="delete" flat style="width: 20px;" />
        </div> 
        <div style="font-size:16px" > Description: {{ itemDetails.description }} </div> 
        <div class="row align-right">
          <q-btn v-if="editable" @click="editQuantity()" icon="edit" flat style="width: 20px; position: absolute;bottom: 0; right: 100px;" />
          <div class="column" style="position: absolute;bottom: 0; right: 0;"> 
            <div style="font-size:16px"> Price: ${{ itemDetails.price }} </div>
            <div style="font-size:16px"> Quantity: {{ itemDetails.amount }} </div>
          </div> 
        </div>
      </div>
    </div>
  </q-item>
</template>

<script>
import { defineComponent } from 'vue'
import { useQuasar } from 'quasar'

export default defineComponent({
  name: 'CartTile',
  props: ['itemDetails', 'editable'],

  setup(props, { emit } ) {
    const $q = useQuasar()
    const itemImg = 'http://127.0.0.1:2434/static/itemphotos/' + props.itemDetails.item_id + '.jpg'

    return {
      itemImg,
      deleteItem() {
        emit('deleteItem')
      },
      editQuantity() {
        emit('editQuantity')
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
