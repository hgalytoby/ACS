import { it } from 'vuetify/locale'
import Microsoft from '@/views/pages/authentication/Microsoft.vue'
import Google from '@/views/pages/authentication/Google.vue'
import Github from '@/views/pages/authentication/Github.vue'

export const authProviders = [
  {
    icon: Microsoft,
    color: '#272727',
    colorInDark: '#fff',
    name: 'microsoft',
  },
  {
    icon: Github,
    color: '#272727',
    colorInDark: '#fff',
    name: 'github',
  },
  {
    icon: Google,
    color: '#272727',
    colorInDark: '#fff',
    name: 'google',
  },
]

export const authProviderItems = {}

authProviders.forEach(item => authProviderItems[item.name] = item)
