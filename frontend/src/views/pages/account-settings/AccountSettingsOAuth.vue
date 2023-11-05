<script setup>
import { authProviders } from '@/utils/oauth'
import { useOAuthStore } from '@/stores/oauth'
import { useTheme } from 'vuetify'
import { useUserStore } from '@/stores/user'

const oauthStore = useOAuthStore()
const userStore = useUserStore()
const { global } = useTheme()

const currentOAuthAccounts = computed(() => {
  const items = authProviders.reduce((acc, item) => {
    acc[item.name] = {
      icon: item.icon,
      color: global.name.value === 'dark' ? item.colorInDark : item.color,
      message: `Link ${item.name}`,
      click: linkEvent(item.name),
    }

    return acc
  }, {})

  userStore.meInfo.oauthAccounts.forEach(item => {
    items[item.oauthName].message = `Unlink ${item.oauthName}`
    items[item.oauthName].click = unlinkEvent(item.oauthName)
  })

  return items
})

const linkEvent = providerName => {
  return async () => {
    await oauthStore.associateAuthorize(providerName)
  }
}

const unlinkEvent = providerName => {
  return async () => {
    await userStore.unlinkOauthAccount(providerName)
  }
}
</script>

<template>
  <VRow>
    <VCol
      v-for="oauth in currentOAuthAccounts"
      :key="oauth.icon"
      cols="12"
      sm="auto"
    >
      <VBtn
        block
        :prepend-icon="oauth.icon"
        variant="outlined"
        :color="oauth.color"
        @click="oauth.click"
      >
        {{ oauth.message }}
      </VBtn>
    </VCol>
  </VRow>
</template>

