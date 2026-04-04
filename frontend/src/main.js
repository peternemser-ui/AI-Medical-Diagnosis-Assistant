import { createApp } from 'vue'
import './index.css'
import App from './App.vue'
import router from './router.js'

// Apply theme class before mount to prevent flash
const savedTheme = localStorage.getItem('theme') || 'dark'
document.documentElement.classList.add(savedTheme)
document.documentElement.lang = localStorage.getItem('lang') || 'en'

createApp(App).use(router).mount('#app')

// Register service worker for PWA offline support
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((err) => {
      console.warn('SW registration failed:', err)
    })
  })
}
