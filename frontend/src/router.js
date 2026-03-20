import { createRouter, createWebHistory } from 'vue-router'

// Eagerly loaded core views
import HomeView from '@/views/HomeView.vue'
import VoiceDiagnosis from '@/views/VoiceDiagnosis.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/setup',
    name: 'ApiKeySetup',
    component: () => import('@/views/ApiKeySetup.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileSetup.vue')
  },
  {
    path: '/consult',
    name: 'Consult',
    component: VoiceDiagnosis,
    beforeEnter: (to, from, next) => {
      const apiKeyConfigured = localStorage.getItem('api_key_configured')
      if (!apiKeyConfigured) {
        next('/setup')
      } else {
        next()
      }
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue')
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/ReportsView.vue')
  },
  {
    path: '/reports/:id',
    name: 'SessionDetail',
    component: () => import('@/views/SessionDetail.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/components/DiagnosisDashboard.vue')
  },
  // Legacy redirects
  { path: '/voice-diagnosis', redirect: '/consult' },
  { path: '/diagnose', redirect: '/consult' },
  { path: '/welcome', redirect: '/' },
  { path: '/dashboard-old', redirect: '/dashboard' },
  { path: '/chat', redirect: '/consult' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
