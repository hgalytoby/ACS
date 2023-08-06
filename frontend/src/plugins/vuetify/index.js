import { createVuetify } from 'vuetify'
import { VBtn } from 'vuetify/components/VBtn'
import defaults from './defaults'
import { icons } from './icons'
import theme from './theme'
import { VDataTable, VDataTableServer } from 'vuetify/labs/VDataTable'

// Styles
import '@core/scss/template/libs/vuetify/index.scss'
import 'vuetify/styles'

export default createVuetify({
  aliases: {
    IconBtn: VBtn,
  },
  components: {
    VDataTable,
    VDataTableServer,
  },
  defaults,
  icons,
  theme,
})
