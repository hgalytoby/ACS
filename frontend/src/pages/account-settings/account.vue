<script setup>
import { useUserStore } from '@/stores/user'
import defaultAvatar from '@images/avatars/default-avatar.png'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import AccountSettingsOAuth from '@/views/pages/account-settings/AccountSettingsOAuth.vue'
import ImageUpload from '@/components/ImageUpload.vue'

const formSchema = yup.object({
  username: yup.string().required().max(64),
})

const userStore = useUserStore()

const formValues = {
  username: userStore.meInfo.username,
}

const submitBtnLoading = ref(false)
const imageUploadRef = ref()
const showAvatar = computed(() => userStore.meInfo.avatar || defaultAvatar)

const submit = async ({ username }) => {
  submitBtnLoading.value = true

  const payload = new FormData()
  if (imageUploadRef.value.refInputEl.files[0]) {
    payload.append('avatar', imageUploadRef.value.refInputEl.files[0])
  }

  payload.append('item', JSON.stringify({ username }))
  await userStore.updateMeInfo(payload)
    .then(async () => {
      await userStore.me()
    })

  submitBtnLoading.value = false
}

const resetForm = setFieldValue => {
  setFieldValue('username', userStore.meInfo.username)
}


import Swal from 'sweetalert2'
import SweetalertIcon from 'vue-sweetalert-icons/src/components/icon.vue'

const test = () => {
  Swal.fire({
    icon: 'success',
    title: 'Signed in successfully',
  })
}
</script>

<template>
  <VRow>
    <SweetalertIcon icon="success" />
    <VCol cols="12">
      <VCard>
        <Form
          v-slot="{ setFieldValue }"
          :validation-schema="formSchema"
          :initial-values="formValues"
          @submit="submit"
        >
          <VCardText class="d-flex">
            <ImageUpload
              ref="imageUploadRef"
              :default-img="showAvatar"
            />
          </VCardText>
          <VCardText>
            <VIcon icon="mdi-shield-account" />
            Roles:
            <v-chip
              v-for="role in userStore.meInfo.roleList"
              :key="role.id"
              class="ms-2"
              color="primary"
            >
              {{ role.name }}
            </v-chip>
          </VCardText>
          <VDivider />
          <VCardText>
            <VRow>
              <VCol cols="12">
                <Field
                  v-slot="{ field }"
                  name="username"
                  type="text"
                >
                  <VTextField
                    v-bind="field"
                    v-model="formValues.username"
                    label="Username"
                    prepend-inner-icon="mdi-account"
                  />
                </Field>
                <ErrorMessage
                  class="error-message"
                  name="username"
                />
              </VCol>
              <VCol cols="12">
                <VTextField
                  v-model="userStore.meInfo.email"
                  label="E-mail"
                  readonly
                  prepend-inner-icon="mdi-email"
                />
              </VCol>
              <VCol cols="12">
                <VTextField
                  v-model="userStore.meInfo.createdAt"
                  label="Created-at"
                  readonly
                  prepend-inner-icon="mdi-calendar"
                />
              </VCol>
            </VRow>
          </VCardText>
          <VDivider />
          <VCardText>
            <AccountSettingsOAuth />
          </VCardText>
          <VDivider />
          <VCardText>
            <VRow>
              <VCol
                cols="12"
                class="d-flex flex-wrap gap-4"
              >
                <VBtn
                  type="submit"
                  :loading="submitBtnLoading"
                >
                  Save changes
                </VBtn>

                <VBtn
                  color="secondary"
                  variant="tonal"
                  type="reset"
                  @click.prevent="resetForm(setFieldValue)"
                >
                  Reset
                </VBtn>
              </VCol>
            </VRow>
          </VCardText>
        </Form>
      </VCard>
    </VCol>
  </VRow>
</template>

<style lang='scss' scoped>
.custom-image {
  border-radius: 4px;
}
</style>
