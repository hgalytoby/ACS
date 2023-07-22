<script setup>
import { useTheme } from 'vuetify'
import { useOAuthStore } from '@/stores/oauth'

const oauth = useOAuthStore()

const { global } = useTheme()

const authProviders = [
  {
    icon: 'mdi-facebook',
    color: '#4267b2',
    colorInDark: '#4267b2',
    name: 'facebook',
  },
  {
    icon: 'mdi-github',
    color: '#272727',
    colorInDark: '#fff',
    name: 'github',
  },
  {
    icon: 'mdi-google',
    color: '#db4437',
    colorInDark: '#db4437',
    name: 'google',
  },
]

async function login(name){
  await oauth.authorize(name)
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
