<script setup>
import AuthBase from '@/views/pages/auth/base.vue'
import AuthProvider from '@/views/pages/authentication/AuthProvider.vue'
import {useRouter} from 'vue-router'
import {useAuthStore} from '@/stores/auth'
import {Form, Field, ErrorMessage} from 'vee-validate'
import * as yup from 'yup'

const router = useRouter()

const loginFormSchema = yup.object({
  email: yup.string().required().email(),
  password: yup.string().required().min(6),
})

const remember = ref(!!localStorage.getItem('README'))
const email = ref(localStorage.getItem('EMAIL'))

const isPasswordVisible = ref(false)

const user = useAuthStore()

async function submit({email, password}) {
  await user.login({username: email, password}).then(() => {
    if (remember.value) {
      localStorage.setItem('README', '1')
      localStorage.setItem('EMAIL', email)
      router.push('/')
    } else {
      localStorage.removeItem('README')
      localStorage.removeItem('EMAIL')
    }
  })
}
</script>

<template>
  <AuthBase>
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
        :validation-schema="loginFormSchema"
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
              />
            </Field>
            <ErrorMessage name="email"/>
          </VCol>
          <VCol cols="12">
            <Field
              v-slot="{ field }"
              name="password"
              type="string"
            >
              <VTextField
                v-bind="field"
                label="Password"
                :type="isPasswordVisible ? 'text' : 'password'"
                :append-inner-icon="isPasswordVisible ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
                @click:append-inner="isPasswordVisible = !isPasswordVisible"
              />
            </Field>
            <ErrorMessage name="password"/>
            <div class="d-flex align-center justify-space-between flex-wrap mt-1 mb-4">
              <VCheckbox
                v-model="remember"
                label="Remember me"
              />

              <a
                class="ms-2 mb-1"
                href="javascript:void(0)"
              >
                Forgot Password?
              </a>
            </div>
            <VBtn
              block
              type="submit"
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
    <template #footer>
      <VRow>
        <VCol
          cols="12"
          class="d-flex align-center"
        >
          <VDivider/>
          <span class="mx-4">or</span>
          <VDivider/>
        </VCol>
        <VCol
          cols="12"
          class="text-center"
        >
          <AuthProvider/>
        </VCol>
      </VRow>
    </template>
  </AuthBase>
</template>
