<script setup>
import defaultAvatar from '@images/avatars/default-avatar.png'
import { Field, ErrorMessage } from 'vee-validate'
import useInputImg from '@/hooks/useInputImg'
import MyVImg from '@/components/MyVImg.vue'

const props = defineProps({
  resetCallback: {
    type: Function,
    required: false,
  },
  defaultImg: {
    type: String,
    required: false,
    default: defaultAvatar,
  },
})

const {
  refInputEl,
  imgModel,
  changeImg,
  resetImgModel,
} = useInputImg(props.resetCallback)

imgModel.value = props.defaultImg


defineExpose({
  refInputEl,
  resetImgModel,
})
</script>

<template>
  <MyVImg
    :img-obj="{
      src: imgModel,
      lazySrc: imgModel,
      class: 'me-6 custom-image',
      width: '100',
      maxWidth: '120',
    }"
  />
  <div class="d-flex flex-column justify-center gap-5">
    <div class="d-flex flex-wrap gap-2">
      <VBtn
        color="primary"
        @click="refInputEl?.click()"
      >
        <VIcon
          icon="mdi-cloud-upload-outline"
          class="d-sm-none"
        />
        <span class="d-none d-sm-block">Upload new photo</span>
      </VBtn>

      <Field
        v-slot="{ field }"
        name="image"
        type="file"
      >
        <input
          v-bind="field"
          ref="refInputEl"
          type="file"
          name="file"
          accept=".jpeg,.png,.jpg,GIF"
          hidden
          @change="changeImg"
        >
      </Field>
      <VBtn
        color="error"
        variant="outlined"
        @click="resetImgModel"
      >
        <span class="d-none d-sm-block">Reset</span>
        <VIcon
          icon="mdi-refresh"
          class="d-sm-none"
        />
      </VBtn>
    </div>
    <ErrorMessage
      class="error-message"
      name="image"
    />
    <p class="text-body-1 mb-0">
      Allowed JPG, GIF or PNG. Max size of 800K
    </p>
  </div>
</template>
