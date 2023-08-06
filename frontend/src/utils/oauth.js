import { it } from 'vuetify/locale'
import Microsoft from '@/views/pages/authentication/Microsoft.vue'

export const authProviders = [
  {
    icon: Microsoft,
    color: '',
    colorInDark: '',
    name: 'microsoft',
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

export const authProviderItems = {}

authProviders.forEach(item => authProviderItems[item.name] = item)
