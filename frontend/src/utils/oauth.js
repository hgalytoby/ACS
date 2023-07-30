import { it } from 'vuetify/locale'

export const authProviders = [
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

export const authProviderItems = {}

authProviders.forEach(item => authProviderItems[item.name] = item)
