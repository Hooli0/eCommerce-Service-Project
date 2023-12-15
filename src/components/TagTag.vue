<template>
  <div class="row">
    <div> {{tagName}}</div>
    <q-btn icon="delete" flat size="10px" color="grey" @click="remove()" style="width: 4px"></q-btn>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'TagTag',
  props: ['tagName'],

  setup(props, { emit }) {
    return{
      remove() {
        emit('removeTag')
      }
    }
  },
})
</script>
