<template>
  <q-page view="lHh Lpr lFf">
    <div v-if="itemLoad" class="row q-pa-lg">
      <div class="column q-pa-md" style="width: 43%; height: 90%;">
        <div class="imgBox">
          <q-img :src="itemImg" class="imgWrap"/>
        </div>
      </div>
      <div class="column" style="width: 50%">
        <h1 style="margin-bottom: 0px"> {{ itemData.item_name }} </h1>
        <star-rating v-if="loadReview" v-bind:star-size="50" v-bind:rating="rating" :increment="0.01" read-only></star-rating>
        <h6 style="margin-bottom: 0px; margin-top: 10px"> Description </h6>
        <div> {{ itemData.description }} </div>
        <div style="margin-bottom: 10px; margin-top:10px"> Tags: {{ itemData.tags.toString() }} </div>
        <h6 style="margin-bottom: 0px; text-align: right"> ${{ itemData.price }} </h6>
        <h6 style="margin-top: 10px; text-align: right"> Remaining Stock: {{ itemData.stock }} </h6>
        <div v-if="loadCart" class="row" style="margin-left: auto; margin-right: 0;">
          <div v-if="!alreadyIn" class="row">
          <q-btn @click="addToCart()" label="Add to Cart" text-color="black" flat style="background: #ffcf33; height: 37px; margin-right: 20px"/>
          <q-input
            v-model.number="quantity"
            type="number"
            filled
            dense
            :rules="[ val => (val > 0 && val <= itemData.stock) || 'Invalid Quantity']"
          >
          </q-input>
          </div>
          <div v-if="alreadyIn">
            <h6 style="margin-top: 20px;">Item in Cart</h6>
          </div>
        </div>
      </div>
    </div>
    <div v-if="loadReview" class="q-pa-lg" style="margin-left: 5%; margin-right: 6%">
      <h5 style="margin-bottom: 0px; margin-top: 10px"> Reviews </h5>
      <q-toggle label="Write a review" v-model="reviewOpen" color="secondary"></q-toggle>
      <q-slide-transition>
        <div v-show="reviewOpen" class="row justify-between">
          <q-input
          v-model="userReview"
          filled
          type="textarea"
          style="width: 85%"
          />
          <div class="column justify-between">
            <star-rating v-bind:rating="userRating" @update:rating ="setRating" v-bind:star-size="30" :show-rating="false"/>
            <q-btn @click="addReview()" text-color="black" flat style="background: #ffcf33;" label="Add review" />
          </div>
        </div>
      </q-slide-transition>
      <div v-if="reviews.length == 0">There are currently no reviews</div>
      <div v-for="(review, index) in reviews" :key="index">
        <div class="row">
          <div style="font-weight: bold">{{ review.username}}</div>
          <div style="padding-left: 10px">{{ review.date }}</div>
        </div>
        <star-rating v-bind:rating="review.rating" read-only v-bind:star-size="20" :show-rating="false"/>
        <div> {{ review.review }} </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Notify, useQuasar } from 'quasar'
import axios from 'axios'
import StarRating from 'vue-star-rating'

export default defineComponent({
  name: 'UserItem',
  components: {
    StarRating
  },
  watch: {
    $route(to) {
      let routeList = to.fullPath.split('/')
      console.log(routeList)
      if (routeList[2] == 'Item') {
        this.reloadItem(routeList[3])
      }
    }
  },
  
  setup() {
    const $router = useRoute()
    const $q = useQuasar()
    let itemId = $router.params.itemId
    let itemLoad = ref(false)
    let loadCart = ref(false)
    let loadReview = ref(false)
    let alreadyIn = ref(false)
    let quantity = ref(1)
    let rating = ref(0)
    let reviews = ref([])
    let userReview = ref('')
    let userRating = ref(0)
    let reviewOpen = ref(false)
    let itemImg = 'http://127.0.0.1:2434/static/itemphotos/' + $router.params.itemId + '.jpg'
    let itemData = ref({
      item_id: Number,
      item_name: String,
      description: String,
      tags: [],
      price: Number,
      stock: Number
    })

    axios.get('item/getCart',{ params: {
      token: $q.localStorage.getItem('token'),
    }}).then(res => {
      loadCart.value = true
      for (let i = 0; i < res.data['cart'].length; i++) {
        if (res.data['cart'][i]['item']['item_id'] == itemId) {
          alreadyIn.value = true
        }
      }
    })

    axios.get('user/item/details', { params: { 
      token: $q.localStorage.getItem('token'),
      item_id: Number(itemId)
    }}).then( res => {
      itemData.value = res.data['details']
      itemLoad.value = true
    })

    axios.get('/item/get_reviews', { params: {
      token: $q.localStorage.getItem('token'),
      item_id: Number(itemId)
    }}).then( res => {
      rating.value = res.data['avg_rating']
      reviews.value = res.data['reviews']
      loadReview.value = true
    })

    return {
      itemId,
      itemData,
      itemLoad,
      quantity,
      loadCart,
      loadReview,
      alreadyIn,
      rating,
      reviews,
      userReview,
      userRating,
      reviewOpen,
      itemImg,
      async addToCart() {
        await axios.post('/item/cart/add', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          amount: quantity.value
        }).then( res => {
          if (res.data.success) {
            alreadyIn.value = true
          } else {
            Notify.create(res.data.message)
          }
        })
      },
      async handlePurchase() {
        await axios.post('/checkout/buy_now', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          return_url: 'http://localhost:8080/User/PostPurchase'
        }).then( res => {
          window.location.assign(res.data['redirect_url'])
        })
      },
      async reloadItem(item_id) {
        itemId = item_id
        axios.get('user/item/details', { params: { 
          token: $q.localStorage.getItem('token'),
          item_id: Number(item_id)
        }}).then( (res) => {
          itemData.value = res.data['details']
        })
        axios.get('/item/get_reviews', { params: {
        token: $q.localStorage.getItem('token'),
        item_id: Number(item_id)
        }}).then( res => {
          rating.value = res.data['avg_rating']
          reviews.value = res.data['reviews']
        })
      },
      async addReview() {
        await axios.post('/item/create_review', {
          token: $q.localStorage.getItem('token'),
          item_id: Number(itemId),
          rating: Number(userRating.value),
          review: userReview.value
        }).then( (res) => {
          if (res.data['success'] == true) {
            Notify.create('Review Added')
          } else {
            Notify.create(res.data['message'])
          }
          userReview.value = ''
          userRating.value = 0
          reviewOpen.value = false
        })
        axios.get('/item/get_reviews', { params: {
        token: $q.localStorage.getItem('token'),
        item_id: Number(itemId)
        }}).then( res => {
          rating.value = res.data['avg_rating']
          reviews.value = res.data['reviews']
        })
      },
      setRating(rating) {
        userRating.value = rating
      }
    }
  }
})

</script>

<style lang="scss" scoped>
.imgBox {
  width: 100%;
  height: 100%;
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