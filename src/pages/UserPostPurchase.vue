<template>
  <q-page class="column justify-top" style="margin: 0px 100px 0px 100px;" view="lHh Lpr lFf">
    <div style="margin-bottom: 50px">
      <h1 class="row justify-center" style="font-family: Arial; font-weight: bold"> Order Placed! </h1>
      <div class="column justify-top q-pa-md" style="background: #f5f5f5">
        <h4 class="row justify-center" style="font-family: Arial; font-weight: bold"> Share your order! </h4>
        <div class="row justify-between" style="margin: 0px 300px 0px 300px">
          <ShareNetwork
            network="facebook"
            :url="shareURL"
            title="SM Func"
            description="TestDesc"
          >
            <div class="imgBox" style="cursor: pointer;">
              <q-img src="~assets\facebook.png" class="imgWrap"/>
            </div>
          </ShareNetwork>
          <ShareNetwork
            network="twitter"
            :url="shareURL"
            title="SM Func"
            description="TestDesc"
          >
            <div class="imgBox" style="cursor: pointer;">
              <q-img src="~assets\twitter.png" class="imgWrap"/>
            </div>
          </ShareNetwork>
        </div>
      </div>
    </div>
    <q-btn label="Back to Shopping" to="/User/Default" style="background: #ffcf33"/>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useQuasar } from 'quasar'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ShareNetwork } from 'vue-social-sharing'

export default defineComponent({
  name: 'UserPostPurchase',
  components: {
    ShareNetwork
  },
  
  setup() {
    const $q = useQuasar()
    const $router = useRoute()
    let shareURL = ref('')
    let userId = 0

    axios.get('/user/user_id', { params: {
      token: $q.localStorage.getItem('token'),
    }}).then( res => {
      userId = res.data
      axios.get('/user/history', { params: {
        token: $q.localStorage.getItem('token'),
      }}).then( res => {
        let tempHist = res.data['history']
        shareURL.value = 'http://127.0.0.1:8080/User/Cart?cart_id='+ tempHist[tempHist.length - 1]['cart_id'] + '&' + 'user_id=' + userId
      })
    })

    axios.post('/checkout/capture', {
      token: $q.localStorage.getItem('token'),
      order_id: $q.localStorage.getItem('order_id')
    }).then( res => {
      $q.localStorage.set('order_id', 'NOID')
    })

    return {
      shareURL
    }
  }
})
</script>

<style lang="scss" scoped>
.imgBox {
  width: 200px;
  height: 180px;
  justify-content: center;
}
.imgWrap {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}
</style>