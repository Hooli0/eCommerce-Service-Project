<template>
  <q-page style="background-color: aliceblue;" view="lHh Lpr lFf">
    <div class="column justify-between" style="padding-left: 10%; padding-right: 10%; padding-top: 0%; padding-bottom: 5%;">
      <h2 style="font-weight: bold; font-family: Arial"> Add New Listing </h2>
      <h6 style="margin-top: 10px; margin-bottom: 10px"> Name </h6>
      <q-input v-model="name" />
      <h6 style="margin-top: 50px; margin-bottom: 10px"> Product Description </h6>
      <q-input
        v-model="description"
        filled
        type="textarea"
      />
      <h6 style="margin-top: 50px; margin-bottom: 10px"> Tags </h6>
      <q-input v-model="tags" @keyup.enter="addTag()" />
      <div class="row">
        <div style="margin-right: 10px"> {{ 'Tags:  ' }} </div>
        <div v-for="(tasdsdg, index) in tagList" :key="index">
          <tag-tag v-bind:tagName="tasdsdg" v-on:removeTag="removeTag(index)" />
        </div>
      </div>
      <h6 style="margin-top: 50px; margin-bottom: 10px"> Price </h6>
      <q-input type="number" v-model="price" :rules="[ val => (val > 0) || 'Invalid price']"/>
      <h6 style="margin-top: 50px; margin-bottom: 10px"> Available stock </h6>
      <q-input type="number" v-model="stock" :rules="[ val => (val > 0) || 'Invalid stock']"/>
      <h6 style="margin-top: 50px; margin-bottom: 10px"> Image URL </h6>
      <q-input v-model="imgURL" />
      <div class="row justify-between">
        <q-btn to="/Admin/Default" style="float: left; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="Back" flat/>
        <q-btn @click="handleAddListing()" style="float: right; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="Add Listing" flat/>
      </div>

    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { Notify, useQuasar } from 'quasar'
import TagTag from 'src/components/TagTag.vue'
import axios from 'axios'

export default defineComponent({
  name: 'AdminListingCard',
  components: {
    TagTag,
  },

  setup() {
    const $q = useQuasar()
    let name = ref('')
    let description = ref('')
    let tags = ref('')
    let price = ref()
    let stock = ref()
    let tagList = ref([])
    let imgURL = ref('')

    return {
      name,
      description,
      tags,
      price,
      stock,
      tagList,
      imgURL,
      addTag() {
        tagList.value.push(tags.value)
        tags.value = ''
      },
      removeTag(index) {
        tagList.value.splice(index, 1)
      },
      async handleAddListing() {
        await axios.post('/admin/item/add', {
          token: $q.localStorage.getItem('token'),
          item_name: name.value,
          description: description.value,
          tags: tagList.value, 
          price: Number(price.value),
          stock: Number(stock.value),
          image_url: imgURL.value
        }).then( async (res) => {
          if (res.data['success'] == false) {
            Notify.create('failed because of: ' + res.data['message'])
          } else {
            this.$router.push('/Admin/Default')
          }
        })
      }
    }
  }
})
</script>
