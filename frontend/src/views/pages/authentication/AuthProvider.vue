<script setup>
import { useTheme } from 'vuetify'
import { useOAuthStore } from '@/stores/oauth'
import { authProviders } from '@/utils/oauth'

const oauth = useOAuthStore()

const { global } = useTheme()

async function login(providerName) {
  await oauth.authorize(providerName)
}
</script>

<template>
  <VBtn
    v-for="link in authProviders"
    :key="link.icon"
    :icon="link.icon"
    variant="text"
    :color="global.name.value === 'dark' ? link.colorInDark : link.color"
    @click="login(link.name)"
  />
</template>
