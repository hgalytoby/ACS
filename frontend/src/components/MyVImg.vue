<script setup>
import ImageLazyProgress from '@/components/ImageLazyProgress.vue'
import defaultAvatar from '@images/avatars/default-avatar.png'

const props = defineProps({
  imgObj: Object,
})

const imgObj = computed(() => {
  const data = JSON.parse(JSON.stringify(props.imgObj))

  data.src = data.src || props.imgObj.defaultImg || defaultAvatar
  data.lazySrc = data.lazySrc || props.imgObj.defaultImg || defaultAvatar

  return data
})
</script>

<template>
  <VImg v-bind="imgObj">
    <template #placeholder>
      <ImageLazyProgress />
    </template>
  </VImg>
</template>
