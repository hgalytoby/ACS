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
      click: unlinkEvent(item.name),
    }
    
    return acc
  }, {})

  userStore.me.oauthAccounts.forEach(item => {
    items[item.oauthName].message = `Unlink ${item.oauthName}`
    items[item.oauthName].click = linkEvent(item.oauthName)
  })

  return items
})

const linkEvent = providerName => {
  return async () => {
    await oauthStore.authorize(providerName)
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
      sm="3"
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

<style scoped lang='scss'>

</style>
