

<script setup>
import AuthBase from '@/views/pages/auth/base.vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useAuthStore } from '@/stores/auth'
</script>

<template>
  <AuthBase>
    <template #header>
      <h5 class="text-h5 font-weight-semibold mb-1">
        Forgot Password? 🔒
      </h5>
      <p class="mb-0">
        Enter your email and we'll send you instructions to reset your password
      </p>
    </template>
    <template #content>
      <Form>
        <VRow />
      </Form>
    </template>
  </AuthBase>
</template>
