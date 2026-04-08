import { createApp } from 'vue'
import './index.css'
import './assets/designSystem.css'
import App from './App.vue'
import router from './router.js'
import { initErrorTracking, captureError } from '@/services/errorTracking'

// ── Error tracking — must run before the app mounts ──────────────────────────
initErrorTracking()

// Apply theme class before mount to prevent flash
const savedTheme = localStorage.getItem('theme') || 'dark'
document.documentElement.classList.add(savedTheme)
document.documentElement.lang = localStorage.getItem('lang') || 'en'

const app = createApp(App)

// Vue-level error handler — catches errors inside components and lifecycle hooks
app.config.errorHandler = (err, instance, info) => {
  captureError(err, {
    vueComponent: instance?.$options?.name ?? 'unknown',
    vueLifecycleHook: info,
  })
  // Re-throw in development so the browser DevTools still surface it
  if (import.meta.env.DEV) throw err
}

app.use(router).mount('#app')

// Register service worker for PWA offline support
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch((err) => {
      console.warn('SW registration failed:', err)
    })
  })
}
