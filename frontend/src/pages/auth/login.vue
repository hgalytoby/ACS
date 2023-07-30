<script setup>
import BaseContent from '@/views/pages/auth/BaseContent.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'

const formSchema = yup.object({
  email: yup.string().required().email(),
  password: yup.string().required().min(8),
})

const router = useRouter()
const auth = useAuthStore()
const remember = ref(!!localStorage.getItem('REMEMBER'))
const email = ref(localStorage.getItem('EMAIL'))
const isPasswordVisible = ref(false)
const submitBtnLoading = ref(false)

async function submit({ email, password }) {
  submitBtnLoading.value = true
  await auth.login({
    username: email,
    password,
    remember: remember.value,
  })
  submitBtnLoading.value = false
}
</script>

<template>
  <BaseContent>
    <template #header>
      <h5 class="text-h5 font-weight-semibold mb-1">
        Welcome to Materio! 👋🏻
      </h5>
      <p class="mb-0">
        Please sign-in to your account and start the adventure
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
              v-model="email"
              name="email"
              type="email"
            >
              <VTextField
                v-bind="field"
                v-model="email"
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
            <div class="d-flex align-center justify-space-between flex-wrap mt-1 mb-4">
              <VCheckbox
                v-model="remember"
                label="Remember me"
              />
              <RouterLink
                class="ms-2 mb-1"
                :to="{name:'ForgotPassword'}"
              >
                Forgot Password?
              </RouterLink>
            </div>
            <VBtn
              block
              type="submit"
              :loading="submitBtnLoading"
            >
              Login
            </VBtn>
          </VCol>
          <VCol
            cols="12"
            class="text-center text-base"
          >
            <span>New on our platform?</span>
            <RouterLink
              class="text-primary ms-2"
              :to="{name:'Register'}"
            >
              Create an account
            </RouterLink>
          </VCol>
        </VRow>
      </Form>
    </template>
  </BaseContent>
</template>
