<template>
  <q-item class="column" style="background: #f5f5f6; margin-left: 5px; margin-right: 5px;">
    <div @click="toTag()" style="cursor: pointer;"> 
      <div class="imgBox row justify-center">
        <q-img 
          class="imgWrap"
          :src="tagImg"
        />
      </div>
      <div class="justify-top" style="font-size: 20px; width: 280px; position: relative">
        <div class="row justify-between" style="font-size:28px"> 
          <div> {{ tag.tag }} </div>
        </div> 
      </div>
    </div>
  </q-item>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'TagCard',
  props: ['tag'],

  setup(props) {
    const tagImg = ref(props.tag['image_url'])

    return {
      tagImg,
      toTag() {
        this.$router.push('/User/PostSearch/'+'tag/'+props.tag.tag)
      }
    }
  }
})
</script>

<style lang="scss" scoped>
.imgBox {
  width: 200px;
  height: 200px;
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
