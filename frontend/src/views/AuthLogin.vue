<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden p-4 transition-colors duration-300"
    :class="isDark ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'">

    <!-- Minimal background accent — no heavy blobs -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
      <div class="absolute top-0 right-0 w-[480px] h-[480px] opacity-[0.06] rounded-full"
        style="background: radial-gradient(circle at center, #4f46e5, transparent 70%); transform: translate(30%, -30%);"></div>
    </div>

    <div class="relative z-10 w-full max-w-[940px] grid grid-cols-1 lg:grid-cols-[40%_1fr] rounded-2xl shadow-2xl overflow-hidden border"
      :class="isDark ? 'shadow-black/70 border-slate-800' : 'shadow-slate-200/80 shadow-xl border-slate-200'">

      <!-- ── Left branding panel ── -->
      <div class="hidden lg:flex relative items-center justify-center p-8 rounded-l-2xl"
        :class="isDark ? 'bg-slate-900 border-r border-slate-800' : 'bg-slate-900 border-r border-slate-800'">
        <!-- Subtle grid overlay on panel -->
        <div class="absolute inset-0 rounded-l-2xl overflow-hidden opacity-[0.04]"
          style="background-image: linear-gradient(rgba(255,255,255,0.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.6) 1px,transparent 1px); background-size: 48px 48px;"></div>

        <div class="relative z-10 max-w-xs w-full">
          <!-- Logo -->
          <div class="inline-flex p-3.5 rounded-2xl bg-indigo-700 shadow-2xl shadow-indigo-700/40 mb-8">
            <svg class="w-10 h-10 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>

          <h1 class="text-3xl font-extrabold text-white tracking-tight leading-tight mb-2">Your AI<br/>Medical Team</h1>
          <p class="text-slate-400 text-sm leading-relaxed mb-8">
            Clinical-grade intelligence available around the clock.
          </p>

          <!-- Value props -->
          <div class="space-y-4">
            <div v-for="vp in valueProps" :key="vp.title" class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                :style="{ background: vp.bg, border: `1px solid ${vp.border}` }">
                <svg class="w-4 h-4" :style="{ color: vp.iconColor }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="vp.icon" />
                </svg>
              </div>
              <div>
                <div class="text-sm font-semibold text-slate-200">{{ vp.title }}</div>
                <div class="text-xs text-slate-500 mt-0.5">{{ vp.desc }}</div>
              </div>
            </div>
          </div>

          <!-- Trust signals -->
          <div class="mt-8 pt-6 border-t border-slate-800 flex flex-col gap-2">
            <div class="flex items-center gap-2 text-xs text-slate-500">
              <svg class="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              HIPAA-aware design &amp; AES-256 encryption
            </div>
            <div class="flex items-center gap-2 text-xs text-slate-500">
              <svg class="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
              Data stays on your device — no server storage
            </div>
          </div>
        </div>
      </div>

      <!-- ── Right login panel ── -->
      <div class="p-7 sm:p-9 lg:rounded-r-2xl"
        :class="isDark ? 'bg-slate-900' : 'bg-white'">

        <!-- Mobile logo -->
        <div class="lg:hidden text-center mb-7">
          <div class="inline-flex p-3 rounded-2xl bg-indigo-700 shadow-xl shadow-indigo-700/30 mb-4">
            <svg class="w-9 h-9 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <h1 class="text-xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Medical Diagnosis AI</h1>
        </div>

        <h2 class="text-2xl font-bold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">Welcome back</h2>
        <p class="text-sm mb-7" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Sign in to access your diagnosis history</p>

        <!-- Email verified success banner -->
        <Transition name="fade">
          <div v-if="showVerifiedBanner" class="mb-5 p-3.5 bg-emerald-500/10 border border-emerald-500/25 rounded-xl text-emerald-400 text-sm flex items-start gap-2.5">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>Email verified! You can now sign in.</span>
          </div>
        </Transition>

        <!-- Email verification failed banner -->
        <Transition name="fade">
          <div v-if="showVerifiedFailed" class="mb-5 p-3.5 bg-amber-500/10 border border-amber-500/25 rounded-xl text-amber-400 text-sm flex items-start gap-2.5">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
            <span>Verification link is invalid or has expired. Enter your email below and use the resend button.</span>
          </div>
        </Transition>

        <!-- Email not verified warning -->
        <Transition name="fade">
          <div v-if="showUnverifiedWarning" class="mb-5 p-3.5 bg-amber-500/10 border border-amber-500/25 rounded-xl text-amber-400 text-sm">
            <div class="flex items-start gap-2.5 mb-3">
              <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              <span>Please verify your email address before signing in. Check your inbox for the verification link.</span>
            </div>
            <button
              type="button"
              :disabled="resendLoading || resendSent"
              @click="handleResend"
              class="w-full py-2 px-3 text-xs font-semibold rounded-lg border transition-all disabled:opacity-60 disabled:cursor-not-allowed"
              :class="isDark
                ? 'border-amber-500/40 text-amber-400 hover:bg-amber-500/10'
                : 'border-amber-400/50 text-amber-600 hover:bg-amber-50'"
            >
              <span v-if="resendSent">Verification email sent — check your inbox</span>
              <span v-else-if="resendLoading">Sending...</span>
              <span v-else>Resend verification email</span>
            </button>
          </div>
        </Transition>

        <!-- Error display -->
        <Transition name="fade">
          <div v-if="error" id="login-error" role="alert" class="mb-5 p-3.5 bg-red-500/10 border border-red-500/25 rounded-xl text-red-400 text-sm flex items-start gap-2.5">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
            <span>{{ error }}</span>
          </div>
        </Transition>

        <form @submit.prevent="handleLogin" class="space-y-5" novalidate>
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium mb-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Email address</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="w-4.5 h-4.5 text-slate-400" width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/></svg>
              </div>
              <input
                id="email"
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="you@example.com"
                :aria-invalid="email && !isValidEmail ? 'true' : undefined"
                :aria-describedby="email && !isValidEmail ? 'email-error' : undefined"
                class="w-full pl-10 pr-10 py-3 rounded-xl text-sm focus:outline-none focus:ring-2 transition-all"
                :class="[
                  isDark
                    ? 'bg-slate-800/70 border border-slate-700 text-white placeholder:text-slate-600 focus:ring-indigo-500/40 focus:border-indigo-500/50'
                    : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 focus:ring-indigo-400/40 focus:border-indigo-400/60',
                  email && !isValidEmail ? 'border-red-500/60 focus:ring-red-400/30' : ''
                ]"
              />
              <div v-if="email" class="absolute inset-y-0 right-0 pr-3.5 flex items-center pointer-events-none">
                <svg v-if="isValidEmail" class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                <svg v-else class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
              </div>
            </div>
            <p v-if="email && !isValidEmail" id="email-error" role="alert" class="text-xs mt-1.5 text-red-400">Please enter a valid email address</p>
          </div>

          <!-- Password -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label for="password" class="block text-sm font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Password</label>
              <a href="mailto:support@meddiagnosisai.com?subject=Password%20Reset%20Request"
                class="text-xs transition-colors"
                :class="isDark ? 'text-slate-500 hover:text-indigo-400' : 'text-slate-400 hover:text-indigo-600'"
                title="Contact support to reset your password">
                Forgot password?
              </a>
            </div>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="w-4.5 h-4.5 text-slate-400" width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              </div>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                placeholder="Enter your password"
                class="w-full pl-10 pr-12 py-3 rounded-xl text-sm focus:outline-none focus:ring-2 transition-all"
                :class="isDark
                  ? 'bg-slate-800/70 border border-slate-700 text-white placeholder:text-slate-600 focus:ring-indigo-500/40 focus:border-indigo-500/50'
                  : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 focus:ring-indigo-400/40 focus:border-indigo-400/60'"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Hide password' : 'Show password'"
                class="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-300 transition-colors"
              >
                <svg v-if="!showPassword" class="w-4.5 h-4.5" width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                <svg v-else class="w-4.5 h-4.5" width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
              </button>
            </div>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3.5 px-4 bg-indigo-700 hover:bg-indigo-600 text-white font-semibold rounded-xl shadow-lg shadow-indigo-700/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm mt-1"
          >
            <svg v-if="loading" class="w-4.5 h-4.5 animate-spin" width="18" height="18" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center gap-3">
          <div class="flex-1 h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
          <span class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">New here?</span>
          <div class="flex-1 h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        </div>

        <!-- Signup link -->
        <router-link
          to="/signup"
          class="w-full block text-center py-3 px-4 text-sm font-medium rounded-xl border transition-all"
          :class="isDark
            ? 'bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 hover:text-white border-slate-700'
            : 'bg-slate-50 hover:bg-slate-100 text-slate-600 hover:text-slate-900 border-slate-200'"
        >
          Create an account
        </router-link>

        <!-- Skip link -->
        <div class="mt-4 text-center">
          <router-link to="/setup" class="text-xs transition-colors" :class="isDark ? 'text-slate-600 hover:text-slate-400' : 'text-slate-400 hover:text-slate-600'">
            Continue without an account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { login as authLogin, resendVerification } from '@/services/authService'
import { saveProfile } from '@/services/userService'
import { trackEvent, EVENTS } from '@/services/analytics'
import { useTheme } from '@/composables/useTheme.js'

const router = useRouter()
const route = useRoute()
const { isDark } = useTheme()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

// Email verification banners
const showVerifiedBanner = ref(false)
const showVerifiedFailed = ref(false)
const showUnverifiedWarning = ref(false)
const resendLoading = ref(false)
const resendSent = ref(false)

const isValidEmail = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))

onMounted(() => {
  // Read ?verified=true|false from the URL (set by the backend verify-email redirect)
  const verified = route.query.verified
  if (verified === 'true') {
    showVerifiedBanner.value = true
  } else if (verified === 'false') {
    showVerifiedFailed.value = true
  }
  // Clean up the query param without adding to browser history
  if (verified) {
    router.replace({ path: route.path })
  }
})

// Left panel value propositions
const valueProps = [
  {
    title: 'Multi-Agent Diagnosis',
    desc: '7 AI specialists collaborate on every consultation',
    icon: 'M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
    bg: 'rgba(79,70,229,0.12)',
    border: 'rgba(79,70,229,0.25)',
    iconColor: '#818cf8',
  },
  {
    title: 'Medication Safety',
    desc: 'Drug interactions, dosage checks, contraindications',
    icon: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
    bg: 'rgba(16,185,129,0.10)',
    border: 'rgba(16,185,129,0.25)',
    iconColor: '#34d399',
  },
  {
    title: 'Nutrition Planning',
    desc: 'AI meal plans, dietary advice, supplement guidance',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    bg: 'rgba(5,150,105,0.10)',
    border: 'rgba(5,150,105,0.25)',
    iconColor: '#10b981',
  },
]

async function handleLogin() {
  error.value = ''
  showUnverifiedWarning.value = false
  loading.value = true

  try {
    const data = await authLogin(email.value, password.value)

    // Check if the account is unverified (server may return this flag)
    if (data.user && data.user.email_verified === false) {
      showUnverifiedWarning.value = true
      loading.value = false
      return
    }

    // Merge auth user data into existing profile (preserve gender, DOB, etc.)
    if (data.user) {
      await saveProfile({
        email: data.user.email,
        name: data.user.name || data.user.email.split('@')[0],
        ...(data.user.profile_data || {}),
      })
    }
    // Mark API key as configured so the consult guard passes
    localStorage.setItem('api_key_configured', 'true')
    trackEvent(EVENTS.LOGIN, { method: 'email' })
    router.push('/consult')
  } catch (e) {
    // Server returns 403 for unverified accounts
    if (e.message && e.message.toLowerCase().includes('verify')) {
      showUnverifiedWarning.value = true
    } else {
      error.value = e.message || 'Login failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}

async function handleResend() {
  if (!email.value || resendLoading.value || resendSent.value) return
  resendLoading.value = true
  await resendVerification(email.value)
  resendLoading.value = false
  resendSent.value = true
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
