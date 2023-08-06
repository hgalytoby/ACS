<script setup>
import { useUserStore } from '@/stores/user'
import defaultAvatar from '@images/avatars/default-avatar.png'
import ImageLazyProgress from '@/components/ImageLazyProgress.vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'

const userStore = useUserStore()

const formSchema = yup.object({
  username: yup.string().required().max(64),
})

const formValues = {
  username: userStore.me.username,
}

const refInputEl = ref()
const avatar = ref()
const submitBtnLoading = ref(false)

const showAvatar = computed(() => userStore.me.avatar || defaultAvatar)

const changeAvatar = file => {
  const fileReader = new FileReader()
  const { files } = file.target
  if (files && files.length) {
    fileReader.readAsDataURL(files[0])
    fileReader.onload = () => {
      if (typeof fileReader.result === 'string')
        avatar.value = fileReader.result
    }
  }
}

async function submit({ username }) {
  submitBtnLoading.value = true

  const payload = new FormData()

  if (refInputEl.value.files[0]) {
    payload.append('avatar', refInputEl.value.files[0])
  }
  
  payload.append('item', JSON.stringify({ username }))
  
  await userStore.updateUserInfo(payload)
    .then(async () => {
      await userStore.userInfo()
    })
  
  submitBtnLoading.value = false
}

const resetForm = setFieldValue => {
  setFieldValue('username', userStore.me.username)
}

const resetAvatar = () => {
  avatar.value = undefined
}
</script>

<template>
  <VRow>
    <VCol cols="12">
      <VCard>
        <Form
          v-slot="{ setFieldValue }"
          :validation-schema="formSchema"
          :initial-values="formValues"
          @submit="submit"
        >
          <VCardText class="d-flex">
            <VImg
              class="me-6 custom-image"
              width="100"
              max-width="200"
              :src="avatar || showAvatar"
              :lazy-src="avatar || showAvatar"
            >
              <template #placeholder>
                <image-lazy-progress />
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

                <input
                  ref="refInputEl"
                  type="file"
                  name="file"
                  accept=".jpeg,.png,.jpg,GIF"
                  hidden
                  @input="changeAvatar"
                >

                <VBtn
                  type="reset"
                  color="error"
                  variant="tonal"
                  @click="resetAvatar"
                >
                  <span class="d-none d-sm-block">Reset</span>
                  <VIcon
                    icon="mdi-refresh"
                    class="d-sm-none"
                  />
                </VBtn>
              </div>

              <p class="text-body-1 mb-0">
                Allowed JPG, GIF or PNG. Max size of 800K
              </p>
            </div>
          </VCardText>
          <VCardText>
            <VIcon icon="mdi-shield-account" />
            Roles:
            <v-chip
              v-for="role in userStore.me.roleIds"
              :key="role.id"
              class="ms-2"
              color="primary"
            >
              {{ role.name }}
            </v-chip>
          </VCardText>
          <VDivider />
          <VCardText>
            <!-- 👉 Form -->
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
                  v-model="userStore.me.email"
                  label="E-mail"
                  readonly
                  prepend-inner-icon="mdi-email"
                />
              </VCol>
              <VCol cols="12">
                <VTextField
                  v-model="userStore.me.createdAt"
                  label="Created-at"
                  readonly
                  prepend-inner-icon="mdi-calendar"
                />
              </VCol>
              <!-- 👉 Form Actions -->
              <VCol
                cols="12"
                class="d-flex flex-wrap gap-4"
              >
                <VBtn type="submit">
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

<style lang="scss" scoped>
.custom-image {
  border-radius: 4px;
}
</style>