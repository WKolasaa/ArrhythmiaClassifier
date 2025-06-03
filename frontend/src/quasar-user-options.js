import 'quasar/src/css/index.sass'
import '@quasar/extras/material-icons/material-icons.css'
import iconSet from 'quasar/icon-set/material-icons.js'
import lang from 'quasar/lang/en-US.js'
import { Notify, Dialog, Dark } from 'quasar'
import '@quasar/extras/material-icons/material-icons.css'


Dark.set(true) // Start in dark mode 
export default {
  config: {},
  plugins: {
    Notify,
    Dialog,
    Dark
  },
  lang: lang,
  iconSet: iconSet
}
