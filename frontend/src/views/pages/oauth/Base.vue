<script setup>
import { useTheme } from 'vuetify'
import BaseAuth from '@/views/pages/auth/Base.vue'
import { useRoute } from 'vue-router'
import { useOAuthStore } from '@/stores/oauth'
import { authProviderItems } from '@/utils/oauth'

const route = useRoute()
const oauth = useOAuthStore()
const { global } = useTheme()

const icon = authProviderItems[route.params.providerName].icon

const color = global.name.value === 'dark' ?
  authProviderItems[route.params.providerName].colorInDark :
  authProviderItems[route.params.providerName].color
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
        <VIcon
          size="48"
          :icon="icon"
          :color="color"
        />
      </v-progress-circular>
    </template>
  </BaseAuth>
</template>


<style lang='scss'>
@use "@core/scss/pages/page-auth.scss";
</style>
