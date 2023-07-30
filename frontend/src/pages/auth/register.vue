<script setup>
import BaseContent from '@/views/pages/auth/BaseContent.vue'
import { useAuthStore } from '@/stores/auth'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import { debounce } from 'lodash'

const { errors, handleSubmit, defineInputBinds } = useForm({
  validationSchema: yup.object({
    email: yup.string().email().required().test({
      name: 'exists-email',
      message: 'email already exists!',
      test: async value => {
        await checkEmail(value)

        return true
      },
    }),
    username: yup.string().required().max(64),
    password: yup.string().min(6).required(),
    confirmPassword: yup
      .string()
      .required()
      .oneOf([yup.ref('password')], 'Passwords do not match'),
    privacyPolicy: yup.boolean().required().test({
      name: 'is-true',
      message: '值必須為 true',
      test: value => value === true,
    }),
  }),
})

const authStore = useAuthStore()
const cache = reactive({})
const emailSchema = yup.string().email()



const email = defineInputBinds('email', {
  validateOnInput: true,
})

const username = defineInputBinds('username', {
  validateOnInput: true,
})

const password = defineInputBinds('password', {
  validateOnInput: true,
})

const confirmPassword = defineInputBinds('confirmPassword', {
  validateOnInput: true,
})

const privacyPolicy = defineInputBinds('privacyPolicy', {
  validateOnInput: true,
})

const showEmailFailMsg = ref('')
const isPasswordVisible = ref(false)
const isConfirmPasswordVisible = ref(false)
const submitBtnLoading = ref(false)

const submit = handleSubmit(async ({ email, username, password }) => {
  submitBtnLoading.value = true
  await authStore.register({ email, username, password })
  submitBtnLoading.value = false
})

const checkEmail = debounce(async value => {
  try {
    await emailSchema.validate(value)
    if (cache[value] === undefined) {
      cache[value] = await authStore.emailExists(value)
    }
  } catch (e){
  }
}, 2000)

watch(errors, (nV, _) => {
  if (cache[email.value.value] === false){
    showEmailFailMsg.value = 'email already exists!'
  } else {
    showEmailFailMsg.value = nV.email
  }
})
watch(cache, (nV, _) => {
  if (!nV[email.value.value]) {
    showEmailFailMsg.value = 'email already exists!'
  } else {
    showEmailFailMsg.value = ''
  }
})
</script>

<template>
  <BaseContent>
    <template #header>
      <h5 class="text-h5 font-weight-semibold mb-1">
        Adventure starts here 🚀
      </h5>
      <p class="mb-0">
        Make your app management easy and fun!
      </p>
    </template>
    <template #content>
      <form @submit="submit">
        <VRow>
          <VCol cols="12">
            <VTextField
              v-bind="email"
              label="Email"
              type="email"
              prepend-inner-icon="mdi-email"
            />
            <div class="error-message">
              {{ showEmailFailMsg }}
            </div>
          </VCol>
          <VCol cols="12">
            <VTextField
              v-bind="username"
              label="Username"
              prepend-inner-icon="mdi-account"
            />
            <div class="error-message">
              {{ errors.username }}
            </div>
          </VCol>
          <VCol cols="12">
            <VTextField
              v-bind="password"
              label="Password"
              :type="isPasswordVisible ? 'text' : 'password'"
              :append-inner-icon="isPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
              prepend-inner-icon="mdi-lock-question"
              @click:append-inner="isPasswordVisible = !isPasswordVisible"
            />
            <div class="error-message">
              {{ errors.password }}
            </div>
          </VCol>
          <VCol cols="12">
            <VTextField
              v-bind="confirmPassword"
              label="ConfirmPassword"
              :type="isConfirmPasswordVisible ? 'text' : 'password'"
              :append-inner-icon="isConfirmPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
              prepend-inner-icon="mdi-lock-question"
              @click:append-inner="isConfirmPasswordVisible = !isConfirmPasswordVisible"
            />
            <div class="error-message">
              {{ errors.confirmPassword }}
            </div>
          </VCol>
          <VCol cols="12">
            <div class="d-flex align-center mt-n5">
              <VCheckbox
                id="privacy-policy"
                v-bind="privacyPolicy"
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
            <VBtn
              block
              type="submit"
              :loading="submitBtnLoading"
            >
              Sign up
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
      </form>
    </template>
  </BaseContent>
</template>
