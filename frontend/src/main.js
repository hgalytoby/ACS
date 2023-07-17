import '@/@iconify/icons-bundle'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import { loadFonts } from '@/plugins/webfontloader'
import router from '@/router'
import '@core/scss/template/index.scss'
import '@layouts/styles/index.scss'
import '@styles/styles.scss'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import VueProgressBar from '@aacassandra/vue3-progressbar'
import 'animate.css'
import { progressbarOptions, toastificationOptions } from '@/utils/options'
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

loadFonts()

// Create vue app
export const app = createApp(App)

const pinia = createPinia()

pinia.use(({ store }) => {
  store.$router = markRaw(router)
})

// Use plugins
app.use(vuetify)
app.use(pinia)
app.use(router)
app.use(VueProgressBar, progressbarOptions)
app.use(Toast, toastificationOptions)

// Mount vue app
app.mount('#app')
