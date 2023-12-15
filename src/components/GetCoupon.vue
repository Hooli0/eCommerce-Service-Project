// This file was adapted from the Quasar website under the Dialog subheading 
<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 40%;">
      <div class="row justify-between q-pa-sm" style="align-items: center; justify-content-center">
        <div class="imgBox q-pa-md">
          <q-img 
            class="imgWrap q-pa-md"
            style="align-items: center; justify-content-center"
            src="~assets\coupon.png"
          />
        </div>
        <div class="column">
          <h4 class="q-pa-sm" style="margin-top: 10px; margin-bottom: 10px;">Coupon Aquired!</h4>
          <h6 class="q-pa-sm" style="margin-top: 0px; margin-bottom: 0px;"> {{ couponDeal }} </h6>
        </div>
      </div>
      <q-card-actions align="right">
        <q-btn color="secondary" label="OK" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { useDialogPluginComponent, useQuasar } from 'quasar'
import axios from 'axios'

export default {
  props: [
    'couponDeal'
  ],

  emits: [
    // REQUIRED; need to specify some events that your
    // component will emit through useDialogPluginComponent()
    ...useDialogPluginComponent.emits
  ],

  setup () {
    const $q = useQuasar()
    axios.post('/user/check_for_daily_reward', {
      token: $q.localStorage.getItem('token'),
    }).then( () => {
      axios.post('/user/claim_coupons', {
        token: $q.localStorage.getItem('token'),
      })
    })
    // REQUIRED; must be called inside of setup()
    const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()
    // dialogRef      - Vue ref to be applied to QDialog
    // onDialogHide   - Function to be used as handler for @hide on QDialog
    // onDialogOK     - Function to call to settle dialog with "ok" outcome
    //                    example: onDialogOK() - no payload
    //                    example: onDialogOK({ /*.../* }) - with payload
    // onDialogCancel - Function to call to settle dialog with "cancel" outcome

    return {
      // This is REQUIRED;
      // Need to inject these (from useDialogPluginComponent() call)
      // into the vue scope for the vue html template
      dialogRef,
      onDialogHide,

      // other methods that we used in our vue html template;
      // these are part of our example (so not required)
      onOKClick () {
        // on OK, it is REQUIRED to
        // call onDialogOK (with optional payload)
        onDialogOK()
        // or with payload: onDialogOK({ ... })
        // ...and it will also hide the dialog automatically
      },

      // we can passthrough onDialogCancel directly
      onCancelClick: onDialogCancel
    }
  }
}
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
