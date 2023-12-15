<template>
  <q-page class="q-pa-xl" style="background-color: aliceblue;" view="lHh Lpr lFf">
    <credential-edit />
    <div style="padding-left: 50px; padding-bottom: 30px">
      <q-btn to="/Admin/Default" style="float: left;" label="Back" flat/>
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import CredentialEdit from 'src/components/CredentialEdit.vue'

export default defineComponent({
  name: 'AdminProfile',
  components: {
    CredentialEdit
  },
})
</script>
