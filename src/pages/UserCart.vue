<template>
  <q-page class="q-pa-md" view="lHh Lpr lFf" style="margin-left: 100px; margin-right: 100px;">
    <div class="row justify-between">

      <div class="q-pa-lg">
        <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Cart </h4>
        <div style="height: 60vh; overflow-y:auto;">
          <h6 v-if="items.length == 0" style="font-weight: bold; font-family: Arial; margin-top: 5px"> Cart is empty! </h6>
          <div class="q-pa-md" style="background: #f5f5f5;" v-for="(item, index) in items" :key="item.item_name">
            <cart-tile v-on:deleteItem="deleteItem(index)" v-on:editQuantity="editQuantity(index)" v-bind:itemDetails="item" v-bind:editable="true"/>
          </div>
        </div>
        <h4 v-if="activeCoupons.length == 0" style="font-weight: bold; font-family: Arial; margin-top: 50px; margin-bottom: 0px; text-align: right"> Total: ${{ originalPrice }} </h4>
        <h4 v-if="activeCoupons.length != 0" style="font-weight: bold; font-family: Arial; margin-top: 50px; margin-bottom: 0px; text-align: right; text-decoration: line-through"> Total: ${{ originalPrice }} </h4>
        <h4 v-if="activeCoupons.length != 0" style="font-weight: bold; font-family: Arial; margin-top: 50px; margin-bottom: 0px; text-align: right"> Total: ${{ discountedPrice }} </h4>
        <div class="row" style="max-width: 600px">
          <div v-if="coupons.length == 0">No coupons :(</div>
          <div v-for="(coupon, index) in coupons" :key="index" class="column">
            <coupon-tile v-bind:couponDeal="coupon" v-bind:readOnly="false" v-on:add="addCoupon(index)" v-on:remove="removeCoupon(index)" />
          </div>
        </div>
        <!-- <div>
          {{ activeCoupons }}
        </div> -->
      </div>

      <div class="column q-pa-lg" style="margin-left: 20px; margin-right: 70px; width: 35vw;">
        <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Confirm Details</h4>
        <div class="q-pa-sm" style="background: #f5f5f5; margin: 10px 10px 10px 10px;">
          <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Shipping Details</h4>
          <div style="font-weight: bold; font-family: Arial">StreetAddress: {{ streetAddress }} </div>
          <div style="font-weight: bold; font-family: Arial">City: {{ city }} </div>
          <div style="font-weight: bold; font-family: Arial">State/Region/Province: {{ state }} </div>
          <div style="font-weight: bold; font-family: Arial">Postcode: {{ postcode }} </div>
          <q-btn label="Edit" style="float: right" flat to="/User/Profile"/>
        </div>
        <div class="q-pa-sm" style="margin-left: auto; margin-right:10">
          <q-btn @click="purchase()" label="Confirm Purchase" style="background: #ffcf33;" flat/>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRoute } from 'vue-router'
import { Notify, useQuasar } from 'quasar'
import axios from 'axios'
import CartTile from '/src/components/CartTile.vue'
import CouponTile from 'src/components/CouponTile.vue'

export default defineComponent({
  name: 'UserCart',
  components: {
    CartTile,
    CouponTile
  },
  setup() {

    let $q = useQuasar()
    let $router = useRoute()
    let items = ref([])
    let loadCart = ref(false)
    let originalPrice = ref()
    let discountedPrice = ref()
  
    let streetAddress = ref('')
    let city = ref('')
    let state = ref('')
    let postcode = ref('')

    let coupons = ref([])
    let activeCoupons = ref([])

    axios.post('/user/check_for_daily_reward', {
      token: $q.localStorage.getItem('token'),
    }).then( () => {
      axios.get('/user/coupons', { params: {
        token: $q.localStorage.getItem('token')
      }}).then( res => {
        coupons.value = res.data
      })
    })

    if ($router.query['cart_id'] != null && $router.query['user_id'] != null) {
      axios.post('/share/item_cart', {
        token: $q.localStorage.getItem('token'),
        user_id: Number($router.query['user_id']),
        cart_id: Number($router.query['cart_id'])
      }).then( res => {
        for (let i = 0; i < res.data['item_list'].length; i++) {
          let parseDict = res.data['item_list'][i]['item']
          parseDict['amount'] = res.data['item_list'][i]['count']
          console.log(parseDict)
          items.value.push(parseDict)
        }
        Notify.create(res.data['message'])
        axios.get('/item/cart/get/totalprice', { params: {
          token: $q.localStorage.getItem('token'),
          coupon_list: JSON.stringify([])
        }}).then( res => {
          console.log(res.data)
          originalPrice.value = res.data['original_price']
          discountedPrice.value = Number(res.data['discounted_price']).toFixed(2)
        })
      })
    } else {
      axios.get('item/getCart',{ params: {
        token: $q.localStorage.getItem('token'),
      }}).then(res => {
        console.log(res.data['cart'])
        loadCart.value = true
        for (let i = 0; i < res.data['cart'].length; i++) {
          let parseDict = res.data['cart'][i]['item']
          parseDict['amount'] = res.data['cart'][i]['count']
          console.log(parseDict)
          items.value.push(parseDict)
        }
        axios.get('/item/cart/get/totalprice', { params: {
          token: $q.localStorage.getItem('token'),
          coupon_list: JSON.stringify([])
        }}).then( res => {
          console.log(res.data)
          originalPrice.value = res.data['original_price']
          discountedPrice.value = Number(res.data['discounted_price']).toFixed(2)
        })
      })
    }
    
    axios.get('/user/details', { params: {
      token: $q.localStorage.getItem('token')
    }}).then( res => {
      console.log(res.data.details)
      let address =  JSON.parse(res.data.details)
      let realAddress = address['address']
      console.log(realAddress)
        streetAddress.value = realAddress['address']
        city.value = realAddress['city']
        state.value = realAddress['state']
        postcode.value = realAddress['post_code']
    })

    return {
      items,
      originalPrice,
      discountedPrice,
      streetAddress,
      city,
      state,
      postcode,
      coupons,
      activeCoupons,
      async purchase() {
        console.log('buy init')
        if (items.value.length == 0) {
          Notify.create("can't buy nothing")
          return
        }
        if (streetAddress.value == '' || city.value == '' || state.value == '' || postcode.value == '') {
          Notify.create("Enter a shipping address")
          return
        }
        await axios.post('/checkout/cart', {
          token: $q.localStorage.getItem('token'),
          return_url: 'http://localhost:8080/User/PostPurchase',
          original_price: Number(originalPrice.value),
          discounted_price: Number(discountedPrice.value),
          used_coupons: activeCoupons.value
        }).then( res => {
          $q.localStorage.set('order_id', res.data['order_id'])
          window.location.assign(res.data['redirect_url'])
          // this.$router.push(res.data['redirect_url'])
          for (let i = 0; i < items.value.length; i++) {
            axios.put('/recommendations/record_click', {
              token: $q.localStorage.getItem('token'),
              item_id: Number(items.value[i]['item_id'])
            })
          }
        })
      },
      getTotal() {
        axios.get('/item/cart/get/totalprice', { params: {
          token: $q.localStorage.getItem('token'),
          coupon_list: JSON.stringify(activeCoupons.value)
        }}).then( res => {
          console.log(res.data)
          originalPrice.value = res.data['original_price']
          discountedPrice.value = Number(res.data['discounted_price']).toFixed(2)
        })
      },
      deleteItem(index) {
        axios.delete('/item/cart/remove/item', { data: {
          token: $q.localStorage.getItem('token'),
          item_id: items.value[index]['item_id']
        }}).then( res => {
          console.log(res.data)
          items.value.splice(index, 1)
          this.getTotal()
        })
        this.getTotal()
      },
      editQuantity(index) {
        $q.dialog({
          message: 'Enter new quantity',
          prompt: {
            model: '',
            type: 'number'
          },
          ok: {
            color: 'secondary'
          },
        }).onOk( async (model) => {
          console.log(model)
          await axios.put('/item/cart/set/count', {
            token: $q.localStorage.getItem('token'),
            item_id: items.value[index]['item_id'],
            new_count: Number(model)
          }).then( res => {
            if (res.data['success']) {
              items.value[index]['amount'] = Number(model)
              this.getTotal()
            } else {
              $q.notify('Unacceptable quantity')
            }
          })
          this.getTotal()
        }).onCancel(() => {
          // console.log('Cancel')
        }).onDismiss(() => {
          // console.log('I am triggered on both OK and Cancel')
        })
      },
      addCoupon(index) {
        activeCoupons.value.push(coupons.value[index])
        this.getTotal()
      },
      removeCoupon(index) {
        for (let i = 0; i < activeCoupons.value.length; i++) {
          if (activeCoupons.value[i].id == coupons.value[index].id) {
            activeCoupons.value.splice(i, 1)
          }
        }
        this.getTotal()
      }
    }
  }

})

</script>

<style lang="scss" scoped>
div::-webkit-scrollbar {
  display: none;
}
</style>