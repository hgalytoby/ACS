<script setup>
import BaseOAuth from '@/views/pages/oauth/Base.vue'
import { useRoute } from 'vue-router'
import { useOAuthStore } from '@/stores/oauth'

const route = useRoute()
const oauth = useOAuthStore()

onMounted(() => {
  oauth.associateCallback(
    {
      providerName: route.params.providerName,
      query: route.query,
    },
  )
})
</script>

<template>
  <BaseOAuth />
</template>

