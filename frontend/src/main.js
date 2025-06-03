import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { Quasar, Dark, Notify, Dialog } from 'quasar'
import quasarLang from 'quasar/lang/en-US'
import quasarIconSet from 'quasar/icon-set/material-icons'
import 'quasar/src/css/index.sass'

createApp(App).use(Quasar, {
  plugins: { Dark, Notify, Dialog },
  lang: quasarLang,
  iconSet: quasarIconSet,
}).use(router).mount('#app')
