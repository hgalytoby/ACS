<script setup>
import BaseContent from '@/views/pages/auth/BaseContent.vue'
import BackToLogin from '@/views/pages/auth/BackToLogin.vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const formSchema = yup.object({
  email: yup.string().required().email(),
})

const submitBtnLoading = ref(false)

async function submit(payload) {
  submitBtnLoading.value = true
  await auth.forgotPassword(payload)
  submitBtnLoading.value = false
}
</script>

<template>
  <BaseContent>
    <template #header>
      <p class="text-h5 font-weight-semibold mb-1">
        Forgot Password? 🔒
      </p>
      <p class="mb-0">
        Enter your email and we'll send you instructions to reset your password
      </p>
    </template>
    <template #content>
      <Form
        :validation-schema="formSchema"
        @submit="submit"
      >
        <VRow>
          <VCol cols="12">
            <Field
              v-slot="{ field }"
              name="email"
              type="email"
            >
              <VTextField
                v-bind="field"
                label="Email"
                type="email"
                prepend-inner-icon="mdi-email"
              />
            </Field>
            <ErrorMessage
              class="error-message"
              name="email"
            />
          </VCol>
          <VCol cols="12">
            <VBtn
              block
              type="submit"
              :loading="submitBtnLoading"
            >
              Send reset link
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
  </BaseContent>
</template>
