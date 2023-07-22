<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'

const auth = useAuthStore()
const route = useRoute()

onMounted(() => {
  auth.verify({ token: route.query.token })
})
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

