<script setup>
import MyVImg from '@/components/MyVImg.vue'
import defaultMemberLocation from '@images/pages/default-member-location.png'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import useInputImg from '@/hooks/useInputImg'
import { useMemberStore } from '@/stores/member'
import Swal from 'sweetalert2'

const formSchema = yup.object({
  image: yup.string().required(),
  name: yup.string().required().max(64),
})

const dialog = ref(false)
const submitBtnLoading = ref(false)
const myForm = ref(null)
const locationId = ref()
const locationName = ref()

const {
  refInputEl,
  imgModel,
  changeImg,
} = useInputImg()

const memberStore = useMemberStore()

const resetImgModel = () => {
  imgModel.value = undefined
}


const openDialog = location => {
  dialog.value = true
  nextTick(() => {
    myForm.value.resetForm()
    if (location) {
      locationId.value = location.id
      locationName.value = location.name
      imgModel.value = location.image
      myForm.value.setFieldValue('name', location.name)
      myForm.value.setFieldValue('image', imgModel.value)
    } else {
      locationId.value = undefined
      locationName.value = undefined
      imgModel.value = undefined
    }
  })
}

const submit = async () => {
  const validate = await myForm.value.validate()
  if (!validate.valid) {
    return
  }
  submitBtnLoading.value = true

  const payload = new FormData()
  if (refInputEl.value.files[0]) {
    payload.append('image', refInputEl.value.files[0])
  }
  if (locationId.value){
    payload.append('id', locationId.value)
  }
  payload.append('item', JSON.stringify({
    name: myForm.value.getValues().name,
  }))
  await memberStore.memberLocationCreateOrUpdate(payload)
  await memberStore.memberLocationList()
  submitBtnLoading.value = false
  dialog.value = false

  await Swal.fire({
    title: `${locationId ? '更新' : '新增'}地點成功!`,
    icon: 'success',
  })
}

const updateDialogEvent = async () => {
  myForm.value.resetForm()
}

const cancel = async () => {
  myForm.value.resetForm()
  dialog.value = false
}

defineExpose({
  resetImgModel,
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
                  src: imgModel,
                  lazySrc: imgModel,
                  defaultImg: defaultMemberLocation,
                  aspectRatio: 1.7,
                }"
              />
            </VCol>
            <VCol cols="12">
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
                  :hidden="true"
                  @change="changeImg"
                >
              </Field>

              <div class="text-center">
                <ErrorMessage
                  class="error-message "
                  name="image"
                />
              </div>
              <VBtn
                block
                @click="refInputEl?.click()"
              >
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
            type="submit"
            :loading="submitBtnLoading"
            @click="submit"
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
