<script setup>
import AuthBase from '@/views/pages/auth/base.vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const forgotPasswordFormSchema = yup.object({
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
  <auth-base>
    <template #header>
      <p class="text-2xl font-weight-semibold text--primary mb-2">
        Forgot Password? 🔒
      </p>
      <p class="mb-2">
        Enter your email and we'll send you instructions to reset your password
      </p>
    </template>
    <template #content>
      <Form
        :validation-schema="forgotPasswordFormSchema"
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
              Login
              <template #loader>
                <v-progress-circular
                  indeterminate
                  color="primary"
                />
              </template>
            </VBtn>
          </VCol>
          <VCol
            cols="12"
            class="mx-n2"
          >
            <RouterLink
              class="d-flex align-center justify-center text-base"
              :to="{name:'Login'}"
            >
              <VIcon
                size="24px"
                color="#9155fd"
                icon="mdi-chevron-left"
              />
              Back to login
            </RouterLink>
          </VCol>
        </vrow>
      </Form>
    </template>
  </auth-base>
</template>
