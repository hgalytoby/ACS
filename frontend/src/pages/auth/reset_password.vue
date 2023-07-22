<script setup>
import AuthBase from '@/views/pages/auth/Base.vue'
import BackToLogin from '@/views/pages/auth/BackToLogin.vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const toast = useToast()

const resetPasswordFormSchema = yup.object({
  confirmPassword: yup
    .string()
    .required()
    .oneOf([yup.ref('password')], 'Passwords do not match'),
  privacyPolicy: yup.boolean().required().test({
    name: 'is-true',
    message: '值必須為 true',
    test: value => value === true,
  }),
})

const token = route.query.token

if (!token) {
  toast.warning('錯誤驗證!')
  router.push({ name: 'RequestVerifyToken' })
}

const isPasswordVisible = ref(false)
const isConfirmPasswordVisible = ref(false)
const submitBtnLoading = ref(false)


async function submit(payload) {
  submitBtnLoading.value = true
  await auth.resetPassword(payload)
  submitBtnLoading.value = false
}
</script>

<template>
  <AuthBase>
    <template #header>
      <p class="text-h5 font-weight-semibold mb-1">
        Reset Password 🔒
      </p>
      <p class="mb-0">
        Your new password must be different from previously used passwords
      </p>
    </template>
    <template #content>
      <Form
        :validation-schema="resetPasswordFormSchema"
        @submit="submit"
      >
        <VRow>
          <VCol cols="12">
            <Field
              v-slot="{ field }"
              name="password"
              type="password"
            >
              <VTextField
                v-bind="field"
                label="Password"
                :type="isPasswordVisible ? 'text' : 'password'"
                :append-inner-icon="isPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                prepend-inner-icon="mdi-lock-question"
                @click:append-inner="isPasswordVisible = !isPasswordVisible"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="password"
            />
          </VCol>
          <VCol cols="12">
            <Field
              v-slot="{ field }"
              name="confirmPassword"
              type="password"
            >
              <VTextField
                v-bind="field"
                label="ConfirmPassword"
                :type="isConfirmPasswordVisible ? 'text' : 'password'"
                :append-inner-icon="isConfirmPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                prepend-inner-icon="mdi-lock-question"
                @click:append-inner="isConfirmPasswordVisible = !isConfirmPasswordVisible"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="confirmPassword"
            />
            <VBtn
              class="mt-6"
              block
              type="submit"
            >
              Set New Password
            </VBtn>
          </VCol>
          <VCol
            cols="12"
            class="mx-n2"
          >
            <BackToLogin />
          </VCol>
        </vrow>
      </Form>
    </template>
  </AuthBase>
</template>
