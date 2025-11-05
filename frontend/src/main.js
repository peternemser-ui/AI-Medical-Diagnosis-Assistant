import { createApp } from 'vue'
import './index.css'
import App from './App.vue'
import router from './router.js'
import i18n from './i18n'

createApp(App)
  .use(router)
  .use(i18n)
  .mount('#app')
