import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated, getCurrentUser } from '@/services/authService'

// Eagerly loaded core views
import HomeView from '@/views/HomeView.vue'
import VoiceDiagnosis from '@/views/VoiceDiagnosis.vue'

// Auth guard for protected routes
function requireAuth(to, from, next) {
  if (!isAuthenticated()) {
    next('/login')
  } else {
    next()
  }
}

// Admin guard — requires authentication + admin role
function requireAdmin(to, from, next) {
  if (!isAuthenticated()) {
    next('/login')
  } else {
    const user = getCurrentUser()
    if (user && user.role === 'admin') {
      next()
    } else {
      next('/consult') // non-admin users redirected to consult
    }
  }
}

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/AuthLogin.vue')
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('@/views/AuthSignup.vue')
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
      if (!isAuthenticated()) {
        next('/login')
      } else {
        const apiKeyConfigured = localStorage.getItem('api_key_configured')
        if (!apiKeyConfigured) {
          next('/setup')
        } else {
          next()
        }
      }
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/SettingsView.vue'),
    beforeEnter: requireAuth
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/ReportsView.vue'),
    beforeEnter: requireAuth
  },
  {
    path: '/reports/:id',
    name: 'SessionDetail',
    component: () => import('@/views/SessionDetail.vue'),
  },
  {
    path: '/compare',
    name: 'Compare',
    component: () => import('@/views/CompareView.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/components/DiagnosisDashboard.vue'),
  },
  // Admin Dashboard (nested layout)
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    beforeEnter: requireAdmin,
    children: [
      {
        path: '',
        name: 'admin-overview',
        component: () => import('@/views/admin/AdminOverview.vue'),
      },
      {
        path: 'agents',
        name: 'admin-agents',
        component: () => import('@/views/admin/AdminAgents.vue'),
      },
      {
        path: 'cases',
        name: 'admin-cases',
        component: () => import('@/views/admin/AdminCases.vue'),
      },
      {
        path: 'reviews',
        name: 'admin-reviews',
        component: () => import('@/views/admin/AdminReviews.vue'),
      },
      {
        path: 'analytics',
        name: 'admin-analytics',
        component: () => import('@/views/admin/AdminAnalytics.vue'),
      },
      {
        path: 'logs',
        name: 'admin-logs',
        component: () => import('@/views/admin/AdminLogs.vue'),
      },
      {
        path: 'config',
        name: 'admin-config',
        component: () => import('@/views/admin/AdminConfig.vue'),
      },
      {
        path: 'reports',
        name: 'admin-reports',
        component: () => import('@/views/admin/AdminReports.vue'),
      },
      {
        path: 'models',
        name: 'admin-models',
        component: () => import('@/views/admin/AdminModelCompare.vue'),
      },
      {
        path: 'billing',
        name: 'admin-billing',
        component: () => import('@/views/admin/AdminBilling.vue'),
      },
      {
        path: 'seo',
        name: 'admin-seo',
        component: () => import('@/views/admin/AdminSEO.vue'),
      },
    ]
  },
  // Medication Management (nested layout)
  {
    path: '/medications',
    component: () => import('@/views/MedicationLayout.vue'),
    beforeEnter: requireAuth,
    children: [
      {
        path: '',
        name: 'med-list',
        component: () => import('@/views/medications/MedList.vue'),
      },
      {
        path: 'interactions',
        name: 'med-interactions',
        component: () => import('@/views/medications/MedInteractions.vue'),
      },
      {
        path: 'food',
        name: 'med-food',
        component: () => import('@/views/medications/MedFoodInteractions.vue'),
      },
      {
        path: 'side-effects',
        name: 'med-side-effects',
        component: () => import('@/views/medications/MedSideEffects.vue'),
      },
      {
        path: 'schedule',
        name: 'med-schedule',
        component: () => import('@/views/medications/MedSchedule.vue'),
      },
      {
        path: 'scan',
        name: 'med-scan',
        component: () => import('@/views/medications/MedScanPrescription.vue'),
      },
      {
        path: 'refills',
        name: 'med-refills',
        component: () => import('@/views/medications/MedRefills.vue'),
      },
      {
        path: 'identify',
        name: 'med-identify',
        component: () => import('@/views/medications/MedPillIdentifier.vue'),
      },
    ]
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
