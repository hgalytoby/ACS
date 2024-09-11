<script setup>
import { useMemberStore } from '@/stores/member'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { bloodTypeSelectItem } from '@/utils/filter-select-item'
import DatePicker from 'vue-datepicker-next'
import ImageUpload from '@/components/ImageUpload.vue'

const props = defineProps({
  memberInfo: {
    type: Object,
    required: false,
    default: null,
  },
})

const { memberInfo } = toRefs(props)

const formSchema = yup.object({
  image: yup.string().required(),
  name: yup.string().required().max(32),
  bloodType: yup.string().required(),
  birthday: yup.string().required(),
  phone: yup.string().required().test({
    name: 'phone',
    message: '格式錯誤! 範例: 091234578',
    test: value => value.match(/^09[0-9]{8}$/),
  }),
  company: yup.string().required().max(32),
  jobTitle: yup.string().required().max(32),
})

const memberStore = useMemberStore()
const submitBtnLoading = ref(false)
const memberForm = reactive({})
const myForm = ref(null)
const imageUploadRef = ref()

onMounted(() => {
  if (memberInfo.value?.id) {
    Object.assign(memberForm, memberInfo.value)
    myForm.value.setFieldValue('image', memberInfo.value.image)
    myForm.value.setFieldValue('name', memberInfo.value.name)
    myForm.value.setFieldValue('birthday', memberInfo.value.birthday)
    myForm.value.setFieldValue('bloodType', memberInfo.value.bloodType)
    myForm.value.setFieldValue('phone', memberInfo.value.phone)
    myForm.value.setFieldValue('company', memberInfo.value.company)
    myForm.value.setFieldValue('jobTitle', memberInfo.value.jobTitle)
  }
})

const resetFormImg = (refInputEl, imgModel) => {
  if (memberInfo.value?.id){
    myForm.value.setFieldValue('image', memberInfo.value.image)
  } else {
    myForm.value.setFieldValue('image', null)
  }
  imgModel.value = memberInfo.value.image
}

const submit = async ({ image, ...payload }) => {
  submitBtnLoading.value = true

  const data = new FormData()

  if (imageUploadRef.value.refInputEl.files[0]) {
    data.append('image', imageUploadRef.value.refInputEl.files[0])
  }

  if (memberInfo.value?.id){
    data.append('id', memberInfo.value.id)
  }

  data.append('item', JSON.stringify(payload))
  await memberStore.memberCreateOrUpdate(data)
  submitBtnLoading.value = false
}
</script>

<template>
  <VCard class="pa-3">
    <Form
      ref="myForm"
      :validation-schema="formSchema"
      @submit="submit"
    >
      <VCardText class="d-flex">
        <ImageUpload
          ref="imageUploadRef"
          :reset-callback="resetFormImg"
          :default-img="memberInfo?.image"
        />
      </VCardText>
      <VCardText>
        <v-row>
          <VCol
            cols="12"
            sm="6"
          >
            <Field
              v-slot="{ field }"
              name="name"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="memberForm.name"
                label="Name"
                type="text"
                density="compact"
                prepend-inner-icon="mdi-account-outline"
              />
              <ErrorMessage
                class="error-message"
                name="name"
              />
            </Field>
          </VCol>
          <VCol
            cols="12"
            sm="6"
          >
            <Field
              v-slot="{ field }"
              name="bloodType"
              type="text"
            >
              <VSelect
                v-bind="field"
                v-model="memberForm.bloodType"
                label="BloodType"
                :items="bloodTypeSelectItem"
                item-title="name"
                item-value="value"
                type="text"
                placeholder="BloodType"
                density="compact"
                prepend-inner-icon="mdi-ab-testing"
              />
              <ErrorMessage
                class="error-message"
                name="bloodType"
              />
            </Field>
          </VCol>
          <VCol
            cols="12"
            sm="6"
          >
            <Field
              v-slot="{ field }"
              name="birthday"
              type="text"
            >
              <DatePicker
                v-model:value="memberForm.birthday"
                class="w-100"
                v-bind="field"
                type="date"
                value-type="format"
              >
                <template #input>
                  <VTextField
                    v-model="memberForm.birthday"
                    label="Birthday"
                    hide-details
                    density="compact"
                    readonly
                    placeholder="生日"
                    prepend-inner-icon="mdi-calendar-outline"
                  />
                </template>
                <template #icon-calendar />
              </DatePicker>
            </Field>
            <ErrorMessage
              class="error-message"
              name="birthday"
            />
          </VCol>
          <VCol
            cols="12"
            sm="6"
          >
            <Field
              v-slot="{ field }"
              name="phone"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="memberForm.phone"
                label="Phone"
                type="text"
                density="compact"
                prepend-inner-icon="mdi-phone-outline"
              />
              <ErrorMessage
                class="error-message"
                name="phone"
              />
            </Field>
          </VCol>
          <VCol
            cols="12"
            sm="6"
          >
            <Field
              v-slot="{ field }"
              name="company"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="memberForm.company"
                label="Company"
                type="text"
                density="compact"
                prepend-inner-icon="mdi-domain"
              />
              <ErrorMessage
                class="error-message"
                name="company"
              />
            </Field>
          </VCol>
          <VCol
            cols="12"
            sm="6"
          >
            <Field
              v-slot="{ field }"
              name="jobTitle"
              type="text"
            >
              <VTextField
                v-bind="field"
                v-model="memberForm.jobTitle"
                label="JobTitle"
                type="text"
                density="compact"
                prepend-inner-icon="mdi-card-account-details-outline"
              />
              <ErrorMessage
                class="error-message"
                name="jobTitle"
              />
            </Field>
          </VCol>
          <VCol cols="12">
            <VBtn
              color="primary"
              type="submit"
            >
              儲存
            </VBtn>
            <VBtn
              class="mx-3"
              color="error"
              variant="outlined"
              type="reset"
              @click="imageUploadRef?.resetImgModel"
            >
              重置
            </VBtn>
          </VCol>
        </v-row>
      </VCardText>
    </Form>
  </VCard>
</template>

<style lang='scss' scoped>
.custom-image {
  border-radius: 4px;
}
</style>
