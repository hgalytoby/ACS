<script setup>
import { useMemberStore } from '@/stores/member'
import defaultAvatar from '@images/avatars/default-avatar.png'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { bloodTypeSelectItem } from '@/utils/filter-select-item'
import DatePicker from 'vue-datepicker-next'
import ImageLazyProgress from '@/components/ImageLazyProgress.vue'

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
const birthday = ref()
const refInputEl = ref()
const fileModel = ref()
const myForm = ref(null)
const test = ref(true)

const imageChange = file => {
  const fileReader = new FileReader()
  const { files } = file.target

  if (files && files.length) {
    fileReader.readAsDataURL(files[0])
    fileReader.onload = () => {
      if (typeof fileReader.result === 'string')
        fileModel.value = fileReader.result
    }
  }
}

const resetFile = () => {
  refInputEl.value.value = null
  fileModel.value = undefined
}

const submit = async ({ image, ...payload }) => {
  submitBtnLoading.value = true

  const data = new FormData()

  data.append('image', refInputEl.value.files[0])
  data.append('item', JSON.stringify(payload))
  await memberStore.memberCreateOrUpdate(data)
  submitBtnLoading.value = false
}
</script>

<template>
  <Form
    ref="myForm"
    :validation-schema="formSchema"
    @submit="submit"
  >
    <VCard
      flat
      class="pa-3"
    >
      <VCardText class="d-flex">
        <!--        <UploadFile /> -->
        <VImg
          class="me-6 custom-image"
          width="100"
          max-width="120"
          :src="fileModel || defaultAvatar"
          :lazy-src="fileModel || defaultAvatar"
        >
          <template #placeholder>
            <ImageLazyProgress />
          </template>
        </VImg>
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
                @change="imageChange"
              >
            </Field>
            <VBtn
              color="error"
              variant="outlined"
              @click="resetFile"
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
        <!--        <div> -->
        <!--          <VBtn -->
        <!--            color="primary" -->
        <!--            class="me-3 my-5" -->
        <!--            @click="refInputEl?.click()" -->
        <!--          > -->
        <!--            <VIcon -->
        <!--              class="d-sm-none" -->
        <!--              icon="mdi-cloud-upload-outline" -->
        <!--            /> -->
        <!--            <span class="d-none d-sm-block">Upload new photo</span> -->
        <!--          </VBtn> -->
        <!--          <Field -->
        <!--            v-slot="{ field }" -->
        <!--            v-model="image" -->
        <!--            name="image" -->
        <!--            type="file" -->
        <!--          > -->
        <!--            <input -->
        <!--              v-bind="field" -->
        <!--              ref="refInputEl" -->
        <!--              type="file" -->
        <!--              name="file" -->
        <!--              accept=".jpeg,.png,.jpg,GIF" -->
        <!--              hidden -->
        <!--              @change="imageChange" -->
        <!--            > -->
        <!--          </Field> -->

        <!--          <VBtn -->
        <!--            color="error" -->
        <!--            variant="outlined" -->
        <!--            class="mx-3 my-5" -->
        <!--            @click="resetImage" -->
        <!--          > -->
        <!--            <span class="d-none d-sm-block">Reset</span> -->
        <!--            <VIcon -->
        <!--              icon="mdi-refresh" -->
        <!--              class="d-sm-none" -->
        <!--            /> -->
        <!--          </VBtn> -->
        <!--          <br> -->
        <!--          <ErrorMessage -->
        <!--            class="error-message" -->
        <!--            name="image" -->
        <!--          /> -->
        <!--          <p class="text-sm"> -->
        <!--            Allowed JPG, GIF or PNG. Max size of 800K -->
        <!--          </p> -->
        <!--        </div> -->
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
                v-model:value="birthday"
                class="w-100"
                v-bind="field"
                type="date"
                value-type="format"
              >
                <template #input>
                  <VTextField
                    v-model="birthday"
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
              @click="resetFile"
            >
              重置
            </VBtn>
          </VCol>
        </v-row>
      </VCardText>
    </VCard>
  </Form>
</template>

<style lang='scss' scoped>
.custom-image {
  border-radius: 4px;
}
</style>
