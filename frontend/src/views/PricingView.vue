<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/3 w-[500px] h-[500px] rounded-full blur-[120px]"
        :class="isDark ? 'bg-blue-600/5' : 'bg-blue-400/10'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-emerald-600/5' : 'bg-emerald-400/10'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="relative z-20 flex items-center justify-between px-6 py-3 border-b backdrop-blur-xl"
      style="background: color-mix(in srgb, var(--clinical-surface) 85%, transparent); border-color: var(--clinical-border)">
      <div class="flex items-center gap-4">
        <button @click="$router.back()" class="p-1.5 rounded-lg transition-colors"
          :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </button>
        <h1 class="text-lg font-bold text-[var(--text-primary)]">Pricing Plans</h1>
      </div>
      <ThemeLangControls />
    </nav>

    <!-- Main content -->
    <div class="relative z-10 px-4 py-10 sm:py-16">
      <!-- Header -->
      <div class="text-center max-w-2xl mx-auto mb-12">
        <h2 class="text-3xl sm:text-4xl font-extrabold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">
          Choose Your Plan
        </h2>
        <p class="text-base sm:text-lg" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
          Get AI-powered medical insights with the right plan for you. All plans include our core diagnostic engine.
        </p>
      </div>

      <!-- Billing toggle -->
      <div class="flex items-center justify-center gap-3 mb-10">
        <span class="text-sm font-medium" :class="!annual ? (isDark ? 'text-white' : 'text-slate-900') : (isDark ? 'text-slate-500' : 'text-slate-400')">Monthly</span>
        <button @click="annual = !annual" class="relative w-12 h-6 rounded-full transition-colors"
          :class="annual ? 'bg-emerald-500' : (isDark ? 'bg-slate-700' : 'bg-slate-300')">
          <span class="absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform"
            :class="annual ? 'translate-x-6' : 'translate-x-0'"></span>
        </button>
        <span class="text-sm font-medium" :class="annual ? (isDark ? 'text-white' : 'text-slate-900') : (isDark ? 'text-slate-500' : 'text-slate-400')">
          Annual <span class="text-emerald-500 font-semibold">Save 20%</span>
        </span>
      </div>

      <!-- Tier cards -->
      <div class="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div v-for="tier in tiers" :key="tier.tier_key"
          class="relative rounded-2xl border p-6 flex flex-col transition-all duration-200"
          :class="[
            tier.tier_key === 'pro'
              ? (isDark ? 'border-blue-500/40 bg-blue-500/5 shadow-xl shadow-blue-500/10 ring-1 ring-blue-500/20' : 'border-blue-400 bg-blue-50/50 shadow-xl shadow-blue-200/40 ring-1 ring-blue-300')
              : (isDark ? 'border-slate-800 bg-slate-900/60' : 'border-slate-200 bg-white'),
            tier.tier_key === currentTier ? 'ring-2 ring-emerald-500/50' : ''
          ]">
          <!-- Popular badge -->
          <div v-if="tier.tier_key === 'pro'" class="absolute -top-3 left-1/2 -translate-x-1/2">
            <span class="px-3 py-1 text-xs font-bold uppercase tracking-wider rounded-full bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg">
              Most Popular
            </span>
          </div>

          <!-- Current plan badge -->
          <div v-if="tier.tier_key === currentTier" class="absolute -top-3 right-4">
            <span class="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-emerald-500 text-white">
              Current Plan
            </span>
          </div>

          <!-- Tier icon -->
          <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4"
            :class="tierIconClass(tier.tier_key)">
            <svg v-if="tier.tier_key === 'free'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            <svg v-else-if="tier.tier_key === 'plus'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
            <svg v-else-if="tier.tier_key === 'pro'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>

          <!-- Tier name -->
          <h3 class="text-xl font-bold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">
            {{ tier.name }}
          </h3>

          <!-- Price -->
          <div class="mb-4">
            <span class="text-3xl font-extrabold" :class="isDark ? 'text-white' : 'text-slate-900'">
              {{ tier.price === 0 ? 'Free' : `$${displayPrice(tier.price)}` }}
            </span>
            <span v-if="tier.price > 0" class="text-sm ml-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              /{{ annual ? 'year' : 'month' }}
            </span>
          </div>

          <!-- Diagnoses limit -->
          <div class="text-sm mb-5 pb-5 border-b"
            :class="isDark ? 'text-slate-400 border-slate-800' : 'text-slate-500 border-slate-200'">
            <span class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-800'">
              {{ tier.diagnoses_per_month === -1 ? 'Unlimited' : tier.diagnoses_per_month }}
            </span>
            diagnoses per month
          </div>

          <!-- Features list -->
          <ul class="space-y-2.5 mb-6 flex-1">
            <li v-for="feature in tierFeatures(tier)" :key="feature.label"
              class="flex items-start gap-2.5 text-sm"
              :class="feature.included ? (isDark ? 'text-slate-300' : 'text-slate-700') : (isDark ? 'text-slate-600' : 'text-slate-400')">
              <svg v-if="feature.included" class="w-4 h-4 mt-0.5 flex-shrink-0 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <svg v-else class="w-4 h-4 mt-0.5 flex-shrink-0" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
              <span>{{ feature.label }}</span>
            </li>
          </ul>

          <!-- Models -->
          <div class="mb-5">
            <div class="text-xs font-semibold uppercase tracking-wider mb-2"
              :class="isDark ? 'text-slate-500' : 'text-slate-400'">AI Models</div>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="model in tier.models" :key="model"
                class="px-2 py-0.5 text-xs rounded-full border"
                :class="isDark ? 'bg-slate-800 border-slate-700 text-slate-400' : 'bg-slate-50 border-slate-200 text-slate-600'">
                {{ modelLabel(model) }}
              </span>
            </div>
          </div>

          <!-- CTA button -->
          <button
            @click="handleUpgrade(tier.tier_key)"
            :disabled="tier.tier_key === currentTier"
            class="w-full py-2.5 rounded-xl text-sm font-semibold transition-all"
            :class="ctaClass(tier)">
            {{ tier.tier_key === currentTier ? 'Current Plan' : (tier.price === 0 ? 'Get Started' : 'Upgrade Now') }}
          </button>
        </div>
      </div>

      <!-- Feature comparison table (desktop) -->
      <div class="max-w-6xl mx-auto mt-16 hidden lg:block">
        <h3 class="text-2xl font-bold text-center mb-8" :class="isDark ? 'text-white' : 'text-slate-900'">
          Feature Comparison
        </h3>
        <div class="rounded-2xl border overflow-hidden"
          :class="isDark ? 'border-slate-800 bg-slate-900/60' : 'border-slate-200 bg-white'">
          <table class="w-full text-sm">
            <thead>
              <tr :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
                <th class="text-left px-6 py-4 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Feature</th>
                <th v-for="tier in tiers" :key="tier.tier_key" class="text-center px-4 py-4 font-semibold"
                  :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  {{ tier.name }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in comparisonRows" :key="row.label"
                :class="i % 2 === 0 ? (isDark ? 'bg-slate-900/30' : 'bg-white') : (isDark ? 'bg-slate-800/20' : 'bg-slate-50/50')">
                <td class="px-6 py-3" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ row.label }}</td>
                <td v-for="tier in tiers" :key="tier.tier_key" class="text-center px-4 py-3">
                  <svg v-if="row.values[tier.tier_key] === true" class="w-5 h-5 mx-auto text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else-if="row.values[tier.tier_key] === false" class="w-5 h-5 mx-auto" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                  <span v-else :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ row.values[tier.tier_key] }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- FAQ section -->
      <div class="max-w-2xl mx-auto mt-16 mb-12">
        <h3 class="text-2xl font-bold text-center mb-8" :class="isDark ? 'text-white' : 'text-slate-900'">
          Frequently Asked Questions
        </h3>
        <div class="space-y-4">
          <div v-for="faq in faqs" :key="faq.q"
            class="rounded-xl border p-5"
            :class="isDark ? 'border-slate-800 bg-slate-900/60' : 'border-slate-200 bg-white'">
            <h4 class="font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">{{ faq.q }}</h4>
            <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ faq.a }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'
import ThemeLangControls from '@/components/ThemeLangControls.vue'

const router = useRouter()
const { isDark } = useTheme()

const annual = ref(false)
const currentTier = ref('free')
const loading = ref(false)

const tiers = ref([
  {
    tier_key: 'free', name: 'Free', price: 0, diagnoses_per_month: 2,
    models: ['ollama'],
    features: ['basic_report', 'body_map'],
    max_photos: 1, pdf_export: false, specialist_routing: false, family_members: 0,
  },
  {
    tier_key: 'plus', name: 'Plus', price: 9.99, diagnoses_per_month: 20,
    models: ['ollama', 'claude-haiku-4-5', 'claude-sonnet-4-6', 'gpt-4o-mini'],
    features: ['basic_report', 'body_map', 'pdf_export', 'photo_analysis', 'history'],
    max_photos: 5, pdf_export: true, specialist_routing: true, family_members: 0,
  },
  {
    tier_key: 'pro', name: 'Pro', price: 29.99, diagnoses_per_month: -1,
    models: ['ollama', 'claude-haiku-4-5', 'claude-sonnet-4-6', 'claude-opus-4-6', 'gpt-4o', 'gpt-4o-mini'],
    features: ['basic_report', 'body_map', 'pdf_export', 'photo_analysis', 'history', 'specialist_routing', 'priority_support', 'api_access'],
    max_photos: -1, pdf_export: true, specialist_routing: true, family_members: 0,
  },
  {
    tier_key: 'family', name: 'Family', price: 49.99, diagnoses_per_month: -1,
    models: ['ollama', 'claude-haiku-4-5', 'claude-sonnet-4-6', 'claude-opus-4-6', 'gpt-4o'],
    features: ['basic_report', 'body_map', 'pdf_export', 'photo_analysis', 'history', 'specialist_routing', 'family_profiles', 'pediatric_mode'],
    max_photos: -1, pdf_export: true, specialist_routing: true, family_members: 5,
  },
])

// All possible features for the comparison
const allFeatures = [
  { key: 'basic_report', label: 'Basic Diagnostic Reports' },
  { key: 'body_map', label: 'Interactive Body Map' },
  { key: 'pdf_export', label: 'PDF Export' },
  { key: 'photo_analysis', label: 'Photo / Image Analysis' },
  { key: 'history', label: 'Diagnosis History' },
  { key: 'specialist_routing', label: 'Specialist Routing' },
  { key: 'priority_support', label: 'Priority Support' },
  { key: 'api_access', label: 'API Access' },
  { key: 'family_profiles', label: 'Family Profiles (up to 5)' },
  { key: 'pediatric_mode', label: 'Pediatric Mode' },
]

const modelLabels = {
  'ollama': 'Ollama (Local)',
  'claude-haiku-4-5': 'Claude Haiku',
  'claude-sonnet-4-6': 'Claude Sonnet',
  'claude-opus-4-6': 'Claude Opus',
  'gpt-4o': 'GPT-4o',
  'gpt-4o-mini': 'GPT-4o Mini',
}

function modelLabel(m) {
  return modelLabels[m] || m
}

function displayPrice(price) {
  if (annual.value) {
    return (price * 12 * 0.8).toFixed(0)
  }
  return price.toFixed(2)
}

function tierFeatures(tier) {
  return allFeatures.map(f => ({
    label: f.label,
    included: tier.features.includes(f.key),
  }))
}

function tierIconClass(key) {
  const classes = {
    free: 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
    plus: 'bg-blue-100 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400',
    pro: 'bg-purple-100 text-purple-600 dark:bg-purple-500/10 dark:text-purple-400',
    family: 'bg-emerald-100 text-emerald-600 dark:bg-emerald-500/10 dark:text-emerald-400',
  }
  return classes[key] || classes.free
}

function ctaClass(tier) {
  if (tier.tier_key === currentTier.value) {
    return isDark.value
      ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
      : 'bg-slate-100 text-slate-400 cursor-not-allowed'
  }
  if (tier.tier_key === 'pro') {
    return 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600 shadow-lg shadow-blue-500/20'
  }
  if (tier.price === 0) {
    return isDark.value
      ? 'bg-slate-800 text-white hover:bg-slate-700 border border-slate-700'
      : 'bg-slate-100 text-slate-800 hover:bg-slate-200 border border-slate-200'
  }
  return isDark.value
    ? 'bg-blue-600 text-white hover:bg-blue-500'
    : 'bg-blue-500 text-white hover:bg-blue-600'
}

const comparisonRows = computed(() => {
  const rows = [
    { label: 'Diagnoses per month', values: {} },
    { label: 'Max photo uploads', values: {} },
    ...allFeatures.map(f => ({ label: f.label, values: {} })),
    { label: 'Family members', values: {} },
  ]

  for (const tier of tiers.value) {
    rows[0].values[tier.tier_key] = tier.diagnoses_per_month === -1 ? 'Unlimited' : String(tier.diagnoses_per_month)
    rows[1].values[tier.tier_key] = tier.max_photos === -1 ? 'Unlimited' : String(tier.max_photos)
    allFeatures.forEach((f, i) => {
      rows[i + 2].values[tier.tier_key] = tier.features.includes(f.key)
    })
    rows[rows.length - 1].values[tier.tier_key] = tier.family_members > 0 ? String(tier.family_members) : false
  }

  return rows
})

const faqs = [
  { q: 'Can I cancel anytime?', a: 'Yes. You can cancel or downgrade your subscription at any time. Your access continues until the end of the billing period.' },
  { q: 'What happens when I reach my diagnosis limit?', a: 'You\'ll see an upgrade prompt. You can upgrade instantly or wait for your monthly limit to reset on the 1st of each month.' },
  { q: 'Is Ollama really free and unlimited?', a: 'Yes. Ollama runs AI models locally on your device. It\'s free, private, and has no usage limits. All plans include Ollama access.' },
  { q: 'What AI models do I get access to?', a: 'Free plans use Ollama (local). Plus adds Claude Haiku, Sonnet, and GPT-4o Mini. Pro and Family unlock all models including Claude Opus and GPT-4o.' },
  { q: 'Is this a substitute for seeing a doctor?', a: 'No. Our AI provides preliminary assessments for informational purposes. Always consult a qualified healthcare provider for medical decisions.' },
]

async function handleUpgrade(tierKey) {
  if (tierKey === currentTier.value) return

  // For free tier, just redirect to signup/consult
  if (tierKey === 'free') {
    router.push('/consult')
    return
  }

  // Placeholder: in production, create a Stripe Checkout session
  // For now, call the upgrade endpoint directly
  loading.value = true
  try {
    const { getAccessToken } = await import('@/services/authService.js')
    const token = getAccessToken()
    if (!token) {
      router.push('/login')
      return
    }

    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
    const res = await fetch(`${API_BASE_URL}/api/subscription/upgrade`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ tier: tierKey }),
    })
    if (res.ok) {
      const data = await res.json()
      currentTier.value = data.tier?.tier_key || tierKey
    }
  } catch (e) {
    console.error('Upgrade failed:', e)
  } finally {
    loading.value = false
  }
}

// Load current tier on mount
onMounted(async () => {
  try {
    const { getAccessToken } = await import('@/services/authService.js')
    const token = getAccessToken()
    if (!token) return

    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
    const res = await fetch(`${API_BASE_URL}/api/subscription/status`, {
      headers: { 'Authorization': `Bearer ${token}` },
    })
    if (res.ok) {
      const data = await res.json()
      currentTier.value = data.usage?.tier || 'free'
    }
  } catch {
    // Not logged in or network error — default to free
  }

  // Also try to load tiers from the API (to stay in sync with backend definitions)
  try {
    const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
    const res = await fetch(`${API_BASE_URL}/api/subscription/tiers`)
    if (res.ok) {
      const data = await res.json()
      if (data.tiers && data.tiers.length > 0) {
        tiers.value = data.tiers
      }
    }
  } catch {
    // Use hardcoded tiers as fallback
  }
})
</script>
