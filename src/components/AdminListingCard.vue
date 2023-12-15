<template>
  <q-item class="column" style="height: 200px; background: white">
    <div class="row justify-left"> 
      <div class="imgBox">
        <q-img 
          class="imgWrap"
          :src="itemImg"
        />
      </div>
      <div class="justify-top q-pa-md" style="font-size: 20px; width: 280px; position: relative">
        <div class="row justify-between" style="font-size:28px"> 
          <div style="width:180px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis;"> {{ itemDetails.item_name }} </div>
          <div>
            <q-btn @click="editItem()" icon="edit" flat style="width: 20px;" />
            <q-btn @click="deleteItem()" icon="delete" flat style="width: 20px;" />
          </div>
        </div> 
        <div style="font-size:16px"> Tags: {{ itemDetails.tags.toString() }} </div> 
        <div style="font-size:16px" > Description: {{ itemDetails.description }} </div> 
        <div class="column" style="position: absolute;bottom: 0; right: 0;"> 
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
  name: 'AdminListingCard',
  props: ['itemDetails'],
  emits: ['deleteItem', 'editItem'],

  setup(props, { emit }) {
    const $q = useQuasar()
    const itemImg = 'http://127.0.0.1:2434/static/itemphotos/' + props.itemDetails.item_id + '.jpg'

    return {
      itemImg,
      async deleteItem() {
        await axios.delete('/admin/item/remove', { data: {
          token: $q.localStorage.getItem('token'),
          item_id: props.itemDetails.item_id
          }
        })
        emit('deleteItem')
      },
      async editItem() {
        this.$router.push('/Admin/EditItem/'+props.itemDetails.item_id)
      },
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
  width: 200px;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
