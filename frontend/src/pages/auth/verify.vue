<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const toast = useToast()

const token = route.query.token

if (token) {
  auth.verify({ token })
} else {
  toast.warning('錯誤驗證!')
  router.push({ name: 'RequestVerifyToken' })
}
</script>

<template>
  <div class="text-center">
    <v-progress-circular
      :width="5"
      size="100"
      indeterminate
      color="primary"
    >
      驗證中
    </v-progress-circular>
  </div>
</template>

