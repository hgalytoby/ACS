<script setup>
import MyVImg from '@/components/MyVImg.vue'
import defaultMemberLocation from '@images/pages/default-member-location.png'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'

const formSchema = yup.object({
  image: yup.string().required(),
  name: yup.string().required().max(64),
})

const image = ref()
const dialog = ref(false)
const submitBtnLoading = ref(false)
const myForm = ref(null)
const locationId = ref()
const locationName = ref()
const locationImage = ref()

const openDialog = location => {
  if (location) {
    locationId.value = location.id
    locationName.value = location.name
    locationImage.value = location.image
    myForm.value.setFieldValue('name', location.name)
  } else {
    locationId.value = undefined
    locationName.value = undefined
    locationImage.value = undefined
  }

  dialog.value = true
}

const updateLocationData = ({ id, name, image }) => {
  locationId.value = id
  locationName.value = name
  locationImage.value = image
}

const submit = async () => {
  submitBtnLoading.value = true

  submitBtnLoading.value = false
}

const updateDialogEvent = () => {
}

const cancel = () => {
  dialog.value = false
}

defineExpose({
  updateLocationData,
  openDialog,
})
</script>

<template>
  <Form
    ref="myForm"
    :validation-schema="formSchema"
    @submit="submit"
  >
    <VDialog
      v-model="dialog"
      width="500"
      @update:model-value="updateDialogEvent"
    >
      <VCard>
        <VCardTitle>
          <VRow>
            <VCol cols="12">
              <MyVImg
                :img-obj="{
                  src: locationImage,
                  lazySrc: locationImage,
                  defaultImg: defaultMemberLocation,
                  aspectRatio: 1.7,
                }"
              />
            </VCol>
            <VCol cols="12">
              <input
                type="file"
                accept=".jpeg,.png,.jpg,GIF"
                :hidden="true"
              >
              <VBtn block>
                上傳圖片
              </VBtn>
            </VCol>
            <VCol cols="12">
              <Field
                v-slot="{ field }"
                name="name"
                type="text"
              >
                <VTextField
                  v-bind="field"
                  v-model="locationName"
                  label="地點名稱"
                  type="text"
                  density="compact"
                  prepend-inner-icon="mdi-map-marker-outline"
                />
                <ErrorMessage
                  class="error-message"
                  name="name"
                />
              </Field>
            </VCol>
          </VRow>
        </VCardTitle>
        <VCardActions class="justify-center">
          <VBtn
            class="mx-2"
            variant="elevated"
          >
            儲存
          </VBtn>
          <VBtn
            class="mx-2"
            color="error"
            variant="outlined"
            @click="cancel"
          >
            取消
          </VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </Form>
</template>
