<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useUserStore } from '@/stores/user'

const formSchema = yup.object({
  oldPassword: yup.string().required().min(8),
  newPassword: yup.string().required().min(8),
  confirmPassword: yup
    .string()
    .required()
    .oneOf([yup.ref('newPassword')], 'Passwords do not match'),
})

const userStore = useUserStore()

const isCurrentPasswordVisible = ref(false)
const isNewPasswordVisible = ref(false)
const isConfirmPasswordVisible = ref(false)
const submitBtnLoading = ref(false)

async function submit({ oldPassword, newPassword }) {
  submitBtnLoading.value = true
  await userStore.updateMePassword({
    oldPassword,
    newPassword,
  })
  submitBtnLoading.value = false
}
</script>

<template>
  <VRow>
    <VCol cols="12">
      <VCard title="Update Password">
        <Form
          :validation-schema="formSchema"
          @submit="submit"
        >
          <VCardText>
            <VRow class="mb-3">
              <VCol
                cols="12"
                md="6"
              >
                <Field
                  v-slot="{ field }"
                  name="oldPassword"
                  type="password"
                >
                  <VTextField
                    v-bind="field"
                    :type="isCurrentPasswordVisible ? 'text' : 'password'"
                    :append-inner-icon="isCurrentPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                    prepend-inner-icon="mdi-lock-question"
                    label="Old Password"
                    @click:append-inner="isCurrentPasswordVisible = !isCurrentPasswordVisible"
                  />
                </Field>
                <ErrorMessage
                  class="error-message"
                  name="oldPassword"
                />
              </VCol>
            </VRow>
            <VRow>
              <VCol
                cols="12"
                md="6"
              >
                <Field
                  v-slot="{ field }"
                  name="newPassword"
                  type="password"
                >
                  <VTextField
                    v-bind="field"
                    :type="isNewPasswordVisible ? 'text' : 'password'"
                    :append-inner-icon="isNewPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                    prepend-inner-icon="mdi-lock-question"
                    label="New Password"
                    @click:append-inner="isNewPasswordVisible = !isNewPasswordVisible"
                  />
                </Field>
                <ErrorMessage
                  class="error-message"
                  name="newPassword"
                />
              </VCol>

              <VCol
                cols="12"
                md="6"
              >
                <Field
                  v-slot="{ field }"
                  name="confirmPassword"
                  type="password"
                >
                  <VTextField
                    v-bind="field"
                    :type="isConfirmPasswordVisible ? 'text' : 'password'"
                    :append-inner-icon="isConfirmPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                    prepend-inner-icon="mdi-lock-question"
                    label="Confirm New Password"
                    @click:append-inner="isConfirmPasswordVisible = !isConfirmPasswordVisible"
                  />
                </Field>
                <ErrorMessage
                  class="error-message"
                  name="confirmPassword"
                />
              </VCol>
            </VRow>
          </VCardText>
          <VCardText class="d-flex flex-wrap gap-4">
            <VBtn
              type="submit"
              :loading="submitBtnLoading"
            >
              Save changes
            </VBtn>
            <VBtn
              type="reset"
              color="secondary"
              variant="tonal"
            >
              Reset
            </VBtn>
          </VCardText>
        </Form>
      </VCard>
    </VCol>
  </VRow>
</template>
