import { createRouter, createWebHistory } from 'vue-router'

// Core application components
import HomeView from '@/views/HomeView.vue'
import VoiceDiagnosis from '@/views/VoiceDiagnosis.vue'
import DiagnosisDashboard from '@/components/DiagnosisDashboard.vue'
import ApiKeySetup from '@/views/ApiKeySetup.vue'

const routes = [
  {
    path: '/setup',
    name: 'ApiKeySetup',
    component: ApiKeySetup
  },
  { 
    path: '/', 
    name: 'Home',
    component: VoiceDiagnosis, // Main chat interface as homepage
    beforeEnter: (to, from, next) => {
      // Check if API key is configured
      const apiKeyConfigured = localStorage.getItem('api_key_configured')
      if (!apiKeyConfigured) {
        next('/setup')
      } else {
        next()
      }
    }
  },
  {
    path: '/welcome',
    name: 'Welcome', 
    component: HomeView // Welcome page moved to /welcome
  },
  {
    path: '/voice-diagnosis',
    redirect: '/' // Redirect to main interface
  },
  { 
    path: '/dashboard', 
    name: 'Dashboard', 
    component: DiagnosisDashboard 
  },
  // Redirect old routes
  { path: '/diagnose', redirect: '/' },
  { path: '/dashboard-old', redirect: '/dashboard' },
  { path: '/chat', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
