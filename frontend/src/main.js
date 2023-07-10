import '@/@iconify/icons-bundle'
import App from '@/App.vue'
import vuetify from '@/plugins/vuetify'
import {loadFonts} from '@/plugins/webfontloader'
import router from '@/router'
import '@core/scss/template/index.scss'
import '@layouts/styles/index.scss'
import '@styles/styles.scss'
import {createPinia} from 'pinia'
import {createApp} from 'vue'
import VueProgressBar from '@aacassandra/vue3-progressbar'
import 'animate.css'

loadFonts()

// Create vue app
export const app = createApp(App)


// Use plugins
app.use(vuetify)
app.use(createPinia())
app.use(router)
app.use(VueProgressBar, {
    color: '#48e3d1',
    failedColor: '#ff0202',
    thickness: '2px',
    transition: {
        speed: '0.2s',
        opacity: '0.6s',
        termination: 300,
    },
    autoRevert: false,
    location: 'top',
    inverse: false,
})

// Mount vue app
app.mount('#app')
