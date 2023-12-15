<template>
  <q-page style="background-color: aliceblue;" view="lHh Lpr lFf">
    <div class="column justify-between" style="padding-left: 10%; padding-right: 10%; padding-top: 0%; padding-bottom: 5%;">
      <h2 style="font-weight: bold; font-family: Arial"> Edit Listing </h2>
      <h6 style="margin-top: 10px; margin-bottom: 10px"> Name </h6>
      <q-input v-model="name" />
      <h6 style="margin-top: 50px; margin-bottom: 10px"> Product Description </h6>
      <q-input
        v-model="description"
        filled
        type="textarea"
      />
      <h6 style="margin-top: 50px; margin-bottom: 10px"> Tags </h6>
      <q-input v-model="newTags" @keyup.enter="addTag()" />
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
        <q-btn @click="goBack()" style="float: right; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="back" flat/>
        <q-btn @click="handleEditListing()" style="float: right; background: #ffcf33; margin-top: 50px; margin-bottom: 50px" label="Confirm" flat/>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { Notify, useQuasar } from 'quasar'
import axios from 'axios'
import TagTag from 'src/components/TagTag.vue'
import { useRoute } from 'vue-router'

export default defineComponent({
  name: 'AdminEditListing',
  components: {
    TagTag,
  },

  setup() {
    const $q = useQuasar()
    const $router = useRoute()
    let itemId = $router.params.itemId
    let name = ref('')
    let description = ref('')
    let price = ref()
    let tags = ref([])
    let stock = ref()
    let newTags = ref('')
    let tagList = ref([])
    let imgURL = ref('')

    axios.get('/admin/item/details', { params: {
      token: $q.localStorage.getItem('token'),
      item_id: Number(itemId),
    }}).then( res => {
      name.value = res.data['details']['item_name']
      description.value = res.data['details']['description']
      tags.value = res.data['details']['tags']
      price.value = res.data['details']['price']
      stock.value = res.data['details']['stock']
      imgURL.value = res.data['details']['image_url']
      Object.values(tags.value).forEach(val => tagList.value.push(val));
    })

    return {
      name,
      description,
      price,
      stock,
      tagList,
      newTags,
      imgURL,
      addTag() {
        tagList.value.push(newTags.value)
        newTags.value = ''
      },
      removeTag(index) {
        tagList.value.splice(index, 1)
      },
      async handleEditListing() {
        let fail = false
        await axios.put('/item/upload_image', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          image_url: imgURL.value
        }).then( res => {
          if (res.data.success == false) {
            Notify.create(res.data['message'])
            fail = true
            return
          }
        })
        if (fail == true) return

        await axios.put('/admin/item/edit/name', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          item_name: name.value
        })
        await axios.put('/admin/item/edit/desc', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          description: description.value
        })
        await axios.put('/admin/item/edit/tags', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          tags: tagList.value
        })
        await axios.put('/admin/item/edit/price', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          price: Number(price.value)
        })
        await axios.put('/admin/item/edit/stock', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          stock: Number(stock.value)
        })
        this.$router.push('/Admin/Default')
      },
      goBack() {
        this.$router.push('/Admin/Default')
      }
    }
  }
})
</script>
