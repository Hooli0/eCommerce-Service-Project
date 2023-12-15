<template>
  <div class="column q-pa-xs" style="align-items: center; justify-content-center">
    <div v-if="!readOnly" class="q-gutter-sm">
      <q-checkbox v-model="useCoupon" color="secondary" @update:model-value="handleClick()"/>
    </div>
    <div class="imgBox">
      <q-img 
        class="imgWrap"
        style="align-items: center; justify-content-center"
        src="~assets\coupon.png"
      />
    </div>
    <div> {{ couponPercentage }}% off!</div>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'CouponTile',
  props: ['couponDeal', 'readOnly'],

  setup(props, { emit }) {
    let useCoupon = ref(false)
    let couponPercentage = Number(props.couponDeal.discount_value) * 100
    return{
      useCoupon,
      couponPercentage,
      handleClick() {
        if (useCoupon.value == false) {
          emit('remove')
        } else if (useCoupon.value == true) {
          emit('add')
        }
      }
    }
  },
})
</script>

<style lang="scss" scoped>
.imgWrap {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}
.imgBox {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
