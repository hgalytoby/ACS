<script setup>
import AuthBase from '@/views/pages/auth/base.vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const registerFormSchema = yup.object({
  email: yup.string().required().email(),
  username: yup.string().required().max(64),
  password: yup.string().required().min(8),
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

const isPasswordVisible = ref(false)
const isConfirmPasswordVisible = ref(false)
const submitBtnLoading = ref(false)
const privacyPolicy = ref(false)

async function submit({ email, username, password }) {
  submitBtnLoading.value = true
  await auth.register({ email, username, password })
  submitBtnLoading.value = false

}
</script>

<template>
  <AuthBase>
    <template #header>
      <h5 class="text-h5 font-weight-semibold mb-1">
        Adventure starts here 🚀
      </h5>
      <p class="mb-0">
        Make your app management easy and fun!
      </p>
    </template>
    <template #content>
      <Form
        v-slot="{ errors }"
        :validation-schema="registerFormSchema"
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
            <Field
              v-slot="{ field }"
              name="username"
              type="string"
            >
              <VTextField
                v-bind="field"
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
          </VCol>
          <VCol cols="12">
            <Field
              v-slot="{ field }"
              name="privacyPolicy"
              type="checkbox"
              :value="true"
            >
              <div class="d-flex align-center mt-n5">
                <VCheckbox
                  id="privacy-policy"
                  v-bind="field"
                  v-model="privacyPolicy"
                  name="privacyPolicy"
                />
                <VLabel
                  :class="{
                    'animate__animated animate__headShake' : errors.privacyPolicy
                  }"
                  :style="{'color': errors.privacyPolicy ? 'red' : ''}"
                  for="privacy-policy"
                  style="opacity: 1;"
                >
                  <span class="me-1">I agree to</span>
                  <a
                    href="javascript:void(0)"
                    class="text-primary"
                  >privacy policy & terms</a>
                </VLabel>
              </div>
            </Field>
            <VBtn
              block
              type="submit"
            >
              Sign up
            </VBtn>
          </VCol>
          <VCol
            cols="12"
            class="text-center text-base"
          >
            <span>Already have an account?</span>
            <RouterLink
              class="text-primary ms-2"
              to="login"
            >
              Sign in instead
            </RouterLink>
          </VCol>
        </VRow>
      </Form>
    </template>
  </AuthBase>
</template>

<style lang='scss'>
@use "@core/scss/pages/page-auth.scss";
</style>
