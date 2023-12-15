<template>
  <q-page style="background-color: aliceblue;" view="lHh Lpr lFf">
    <q-tabs
      v-model="tab"
      dense
      class="text-black bg-primary"
      active-color="secondary"
      align="justify"
      style="background: $primary;"
    >
      <q-tab name="general" label="General"/>
      <q-tab name="address" label="Shipping Details"/>
      <q-tab name="history" label="Purchase History"/>
    </q-tabs>
    <q-tab-panels v-model="tab" class="q-pa-md" style="background-color: transparent">
      <q-tab-panel name="general" class="q-pl-xl q-pr-xl q-pb-xl">
        <credential-edit />
        <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Avalible Coupons </h4>
        <div class="row justify-between" style="align-items: center">
          <div class="row" style="align-items: center">
            <div class="q-pa-md imgBoxCoupon">
              <q-img 
                class="imgWrap"
                src="~assets\coupon.png"
              />
            </div>
            <h3 style="padding-left: 50px">Next coupon avalible in: </h3>
          </div>
          <div v-if="!canClaim" style="font-size: 37px; margin-right: 50px"> {{ displayTime }} </div>
          <q-btn v-if="canClaim" size="28px" label="Claim!" style="background: #ffcf33; margin-right: 50px" flat @click="claimCoupon()" />
        </div>
        <div class="row">
          <div v-if="coupons.length == 0">No coupons :(</div>
          <div v-for="(coupon, index) in coupons" :key="index" class="column">
            <coupon-tile class="q-pa-md" v-bind:couponDeal="coupon" v-bind:readOnly="true" />
          </div>
        </div>
      </q-tab-panel>
      <q-tab-panel name="address" class="column justify-between q-pl-xl q-pr-xl q-pb-sm">
        <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Shipping Details</h4>
        <div style="font-weight: bold; font-family: Arial">StreetAddress</div>
        <q-input filled v-model="streetAddress" placeholder="" dense />
        <div style="font-weight: bold; font-family: Arial">City</div>
        <q-input filled v-model="city" placeholder="" dense />
        <div style="font-weight: bold; font-family: Arial">State/Region/Province</div>
        <q-input filled v-model="state" placeholder="" dense />
        <div style="font-weight: bold; font-family: Arial">Postcode</div>
        <q-input filled v-model="postcode" placeholder="" dense />
        <div> 
          <q-btn @click="saveShipping()" style="float: right; background: #ffcf33; margin-top: 50px;" label="Confirm" flat/>
        </div>
      </q-tab-panel>
      <q-tab-panel name="history" class="column q-pl-xl q-pr-xl q-pb-xl">
        <h4 style="font-weight: bold; font-family: Arial; margin-top: 5px"> Purchase History</h4>
        <div v-if="history.length == 0"> Buy something!</div>
        <div v-for="(cart, index) in history" :key="cart.cart_id" class="q-pa-md" style="margin-bottom: 20px">
          <div style="font-weight:bold; font-size: 21px">{{ cart.date }}</div>
          <div class="column" style="align-items: center;">
            <div style="width: 600px" v-for="item in cart.items" :key="item">
              <cart-tile v-bind:itemDetails="item" v-bind:editable="false" />
            </div>
          </div>
          <div class="row justify-between q-pa-md" style="width: 250px">
            <ShareNetwork
              network="facebook"
              :url="urls[index]"
              title="SM Func"
              description="TestDesc"
            >
              <q-img 
                src="~assets\facebookShare.png"
                class="imgBox"
              />
            </ShareNetwork>
            <ShareNetwork
              network="twitter"
              :url="urls[index]"
              title="SM Func"
              description="TestDesc"
            >
              <q-img 
                src="~assets\twitterShare.png"
                class="imgBox"
              />
            </ShareNetwork>
          </div>
        </div>
      </q-tab-panel>
    </q-tab-panels>
    <div style="padding-left: 50px; padding-bottom: 50px">
      <q-btn to="/User/Default" style="float: left;" label="Back" flat/>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, onBeforeUnmount } from 'vue'
import { Notify, useQuasar } from 'quasar'
import axios from 'axios'
import CredentialEdit from 'src/components/CredentialEdit.vue'
import CartTile from 'src/components/CartTile.vue'
import { ShareNetwork } from 'vue-social-sharing'
import CouponTile from 'src/components/CouponTile.vue'

export default defineComponent({
  name: 'UserProfile',
  components: {
    CredentialEdit,
    CartTile,
    ShareNetwork,
    CouponTile
  },

  setup() {
    const $q = useQuasar()
    let tab = ref('general')
    let username = ref('')
    let password = ref('')
    let streetAddress = ref('')
    let city = ref('')
    let state = ref('')
    let postcode = ref('')
    let history = ref([])
    let urls = ref([])
    let coupons = ref([])
    let timeRemaining = ref('999')
    let displayTime = ref('')
    let canClaim = ref(false)

    axios.get('/user/history', { params: {
      token: $q.localStorage.getItem('token'),
    }}).then( async res => {
      let userId = 0
      await axios.get('/user/user_id', { params: {
        token: $q.localStorage.getItem('token'),
      }}).then( res => {
        userId = res.data
      })
      let tempHist = res.data['history']
      for (let i = 0; i < tempHist.length; i++) {
        urls.value.push('http://127.0.0.1:8080/User/Cart?cart_id=' + tempHist[i].cart_id + '&' + 'user_id=' + userId)
        for (let k = 0; k < tempHist[i].items.length; k++) {
          tempHist[i].items[k].item.amount = tempHist[i].items[k].count
          delete tempHist[i].items[k].item.count
          tempHist[i].items[k] = tempHist[i].items[k].item
        }
      }
      history.value = tempHist
      history.value.reverse()
    })

    axios.get('/user/details', { params: {
      token: $q.localStorage.getItem('token')
    }}).then( res => {
      let address =  JSON.parse(res.data.details)
      let realAddress = address['address']
        streetAddress.value = realAddress['address']
        city.value = realAddress['city']
        state.value = realAddress['state']
        postcode.value = realAddress['post_code']
    })

    axios.post('/user/check_for_daily_reward', {
      token: $q.localStorage.getItem('token'),
    }).then( () => {
      axios.get('/user/coupons', { params: {
        token: $q.localStorage.getItem('token')
      }}).then( res => {
        coupons.value = res.data
      })
      axios.get('/user/coupon_timer', { params: {
        token: $q.localStorage.getItem('token')
      }}).then( res => {
        timeRemaining.value = Math.round(Number(res.data['coupon_timer']))
      })
    })

    let intervalId = setInterval(() => {
      timeRemaining.value -= 1
      let seconds = timeRemaining.value % 60
      let minutes = Math.floor(timeRemaining.value / 60)
      displayTime.value = String(minutes) + ':' + String(seconds)
      if (timeRemaining.value <= 0) {
        canClaim.value = true
      }
    }, 1000)

    onBeforeUnmount(() => {
      clearInterval(intervalId)
    })

    return {
      username,
      password,
      tab,
      streetAddress,
      city,
      state,
      postcode,
      history,
      urls,
      coupons,
      displayTime,
      canClaim,
      async saveShipping() {
        await axios.post('/user/change_address', {
          token: $q.localStorage.getItem('token'),
          address: streetAddress.value,
          city: city.value,
          suburb: "Fix Later",
          state: state.value,
          post_code: postcode.value,
        }).then( res => { 
          if (res.data['success'] == true) {
            Notify.create('Address changed')
          }
        })
      },
      async claimCoupon() {
        await axios.post('/user/check_for_daily_reward', {
          token: $q.localStorage.getItem('token'),
        })
        await axios.post('/user/claim_coupons', {
          token: $q.localStorage.getItem('token'),
        }).then( async (res) => {
          if (res.data.success == false) {
            Notify.create(res.data.message)
          }
          await axios.get('/user/coupon_timer', { params: {
            token: $q.localStorage.getItem('token')
          }}).then( res => {
            timeRemaining.value = Math.round(Number(res.data['coupon_timer']))
          })
          axios.get('/user/coupons', { params: {
            token: $q.localStorage.getItem('token')
          }}).then( res => {
            coupons.value = res.data
          })
        })
        canClaim.value = false
      },
      async hasClaimable() {
        await axios.post('/user/check_for_daily_reward', {
          token: $q.localStorage.getItem('token'),
        })
        axios.get('/user/has_claimable_coupon', { params: {
          token: $q.localStorage.getItem('token')
        }})
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
    width: 100px;
    height: 30px;
    display: flex;
    justify-content: center;
  }
  .imgBoxCoupon {
    width: 180px;
    height: 180px;
    display: flex;
    justify-content: center;
  }
</style>
