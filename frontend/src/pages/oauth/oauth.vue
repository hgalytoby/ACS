<script setup>
import BaseAuth from '@/views/pages/auth/Base.vue'
import { useRoute } from 'vue-router'
import { useOAuthStore } from '@/stores/oauth'

const route = useRoute()
const oauth = useOAuthStore()

onMounted(() => {
  oauth.callback({ name: route.params.name, query: route.query })
})
</script>

<template>
  <BaseAuth>
    <template #content>
      <v-progress-circular
        :width="5"
        size="100"
        indeterminate
        color="primary"
      >
        驗證中
      </v-progress-circular>
    </template>
  </BaseAuth>
</template>


<style lang='scss'>
@use "@core/scss/pages/page-auth.scss";
</style>
