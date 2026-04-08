import { createRouter, createWebHistory } from 'vue-router'
import { isAuthenticated, getCurrentUser, refreshToken } from '@/services/authService'
import { trackEvent, EVENTS } from '@/services/analytics'
import { setSEO } from '@/composables/useSEO'

// Eagerly loaded core views
import HomeView from '@/views/HomeView.vue'
import VoiceDiagnosis from '@/views/VoiceDiagnosis.vue'

// Auth guard for protected routes — tries token refresh before redirecting to login
async function requireAuth(to, from, next) {
  if (isAuthenticated()) {
    next()
  } else {
    const newToken = await refreshToken()
    if (newToken) {
      next()
    } else {
      next('/login')
    }
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
    component: HomeView,
    meta: {
      title: 'Home',
      description: 'AI-powered medical diagnosis assistant with 7 specialized agents. Get comprehensive clinical analysis, differential diagnosis, and treatment recommendations.',
      keywords: 'AI medical diagnosis, symptom checker, health AI, medical assistant, clinical analysis, telemedicine',
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/AuthLogin.vue'),
    meta: {
      title: 'Log In',
      description: 'Sign in to MedAssist AI to access your diagnosis history and personalized health consultations.',
      keywords: 'login, sign in, medical AI account',
    }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import('@/views/AuthSignup.vue'),
    meta: {
      title: 'Sign Up',
      description: 'Create a free MedAssist AI account to start AI-powered medical consultations and track your health.',
      keywords: 'sign up, register, medical AI, free account',
    }
  },
  {
    path: '/setup',
    name: 'ApiKeySetup',
    component: () => import('@/views/ApiKeySetup.vue'),
    meta: {
      title: 'API Key Setup',
      description: 'Configure your Anthropic or OpenAI API key to power your personal AI medical diagnosis sessions.',
      keywords: 'API key setup, Anthropic, OpenAI, configuration',
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileSetup.vue'),
    meta: {
      title: 'Profile',
      description: 'Manage your personal health profile including age, medical history, and medication information.',
      keywords: 'profile, health profile, medical history, personal information',
    }
  },
  {
    path: '/consult',
    name: 'Consult',
    component: VoiceDiagnosis,
    meta: {
      title: 'Consultation',
      description: 'Start an AI medical consultation. Describe your symptoms and receive a comprehensive differential diagnosis from 7 specialized AI agents.',
      keywords: 'medical consultation, symptom analysis, AI diagnosis, differential diagnosis',
    },
    beforeEnter: async (to, from, next) => {
      let authed = isAuthenticated()
      if (!authed) {
        const newToken = await refreshToken()
        authed = !!newToken
      }
      if (!authed) {
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
    meta: {
      title: 'Settings',
      description: 'Manage your MedAssist AI account settings, API keys, language preferences, and notification options.',
      keywords: 'settings, account, preferences, API keys, language',
    },
    beforeEnter: requireAuth
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('@/views/ReportsView.vue'),
    meta: {
      title: 'Reports',
      description: 'Review your past AI medical consultation reports and track your health history over time.',
      keywords: 'medical reports, diagnosis history, health records, consultation history',
    },
    beforeEnter: requireAuth
  },
  {
    path: '/reports/:id',
    name: 'SessionDetail',
    component: () => import('@/views/SessionDetail.vue'),
    meta: {
      title: 'Report Detail',
      description: 'View detailed results from a past AI medical consultation including diagnosis, treatment plan, and safety review.',
      keywords: 'diagnosis report, consultation detail, medical report',
    },
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: () => import('@/views/PricingView.vue'),
    meta: {
      title: 'Pricing',
      description: 'Transparent, pay-per-diagnosis pricing for MedAssist AI. Bring your own API key for full control.',
      keywords: 'pricing, cost, plans, API key, pay per use',
    }
  },
  {
    path: '/compare',
    name: 'Compare',
    component: () => import('@/views/CompareView.vue'),
    meta: {
      title: 'Compare Plans',
      description: 'Compare MedAssist AI plans and features to find the best fit for your health needs.',
      keywords: 'compare plans, features comparison, MedAssist AI plans',
    }
  },
  {
    path: '/features',
    name: 'Features',
    component: () => import('@/views/FeaturesShowcase.vue'),
    meta: {
      title: 'Features',
      description: 'Explore all features of MedAssist AI: 7-agent pipeline, voice input, image diagnosis, safety checks, and more.',
      keywords: 'features, AI agents, voice diagnosis, image analysis, safety review',
    }
  },
  {
    path: '/nutrition',
    name: 'Nutrition',
    component: () => import('@/views/NutritionPlanner.vue'),
    meta: {
      title: 'Nutrition Planner',
      description: 'Get AI-powered personalized nutrition recommendations based on your health profile and medical history.',
      keywords: 'nutrition planner, diet recommendations, health nutrition, AI nutrition',
    }
  },
  {
    path: '/mental-health',
    name: 'MentalHealth',
    component: () => import('@/views/MentalHealth.vue'),
    meta: {
      title: 'Mental Health',
      description: 'AI-supported mental health resources, PHQ-9 screening, and personalized wellness guidance.',
      keywords: 'mental health, PHQ-9, depression screening, anxiety, wellness, AI mental health',
    }
  },
  {
    path: '/journal',
    name: 'SymptomJournal',
    component: () => import('@/views/SymptomJournal.vue'),
    meta: {
      title: 'Symptom Journal',
      description: 'Track and log your symptoms over time to identify patterns and share with your healthcare provider.',
      keywords: 'symptom journal, symptom tracker, health log, daily symptoms',
    }
  },
  {
    path: '/second-opinion',
    name: 'SecondOpinion',
    component: () => import('@/views/SecondOpinion.vue'),
    meta: {
      title: 'Second Opinion',
      description: 'Get an AI second opinion on an existing diagnosis. Upload your report and receive independent clinical analysis.',
      keywords: 'second opinion, AI second opinion, diagnosis review, medical second opinion',
    }
  },
  {
    path: '/help',
    name: 'HelpCenter',
    component: () => import('@/views/HelpCenter.vue'),
    meta: {
      title: 'Help Center',
      description: 'Find answers to common questions about MedAssist AI, how it works, privacy, and getting support.',
      keywords: 'help center, FAQ, support, how it works, privacy',
    }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/components/DiagnosisDashboard.vue'),
    meta: {
      title: 'Dashboard',
      description: 'Your personal health dashboard: overview of diagnoses, trends, medications, and recommended actions.',
      keywords: 'health dashboard, diagnosis overview, health trends, medical summary',
    },
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
      {
        path: 'improve',
        name: 'admin-improve',
        component: () => import('@/views/admin/AdminImprove.vue'),
      },
      {
        path: 'developer',
        name: 'admin-developer',
        component: () => import('@/views/admin/AdminDeveloperPortal.vue'),
      },
      {
        path: 'referrals',
        name: 'admin-referrals',
        component: () => import('@/views/admin/AdminReferrals.vue'),
      },
      {
        path: 'system',
        name: 'AdminSystem',
        component: () => import('@/views/admin/SystemInsightDashboard.vue'),
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
  { path: '/chat', redirect: '/consult' },
  // 404 catch-all (must be last)
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '404 Not Found — MedDiagnose AI' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Set document title, SEO meta tags, and track page views
router.afterEach((to) => {
  const { title, description, keywords } = to.meta || {}
  setSEO({
    title: title || undefined,
    description: description || undefined,
    keywords: keywords || undefined,
    canonical: `https://medassist.ai${to.path}`,
  })
  trackEvent(EVENTS.PAGE_VIEW, { path: to.path, name: to.name || '' })
})

export default router
