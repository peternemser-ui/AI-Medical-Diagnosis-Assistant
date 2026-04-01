<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-950 via-slate-900 to-gray-900 text-white relative overflow-hidden p-4">
    <!-- Background blobs -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute rounded-full blur-[80px] opacity-40"
        style="width: 700px; height: 700px; top: -200px; right: -200px; background: radial-gradient(circle, #3b82f6, #8b5cf6)"></div>
      <div class="absolute rounded-full blur-[80px] opacity-30"
        style="width: 600px; height: 600px; bottom: -100px; left: -150px; background: radial-gradient(circle, #10b981, #3b82f6)"></div>
    </div>

    <div class="relative z-10 w-full max-w-[960px] grid grid-cols-1 lg:grid-cols-[38%_1fr] rounded-2xl shadow-2xl shadow-black/60 border border-slate-700/50 overflow-hidden">

      <!-- Left branding panel -->
      <div class="hidden lg:flex relative items-center justify-center p-6 bg-slate-950 rounded-l-2xl">
        <div class="relative z-10 max-w-sm">
          <div class="inline-flex p-4 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-2xl shadow-emerald-500/25 mb-8">
            <svg class="w-12 h-12 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <h1 class="text-4xl font-extrabold text-white tracking-tight leading-tight">Medical<br/>Diagnosis AI</h1>
          <p class="text-slate-400 mt-4 text-base leading-relaxed">Multi-agent clinical analysis powered by 7 specialized AI agents working together.</p>

          <!-- Pipeline preview -->
          <div class="mt-10 space-y-3">
            <div class="text-detail text-slate-500 uppercase tracking-widest font-bold">Diagnostic Pipeline</div>
            <div class="grid grid-cols-2 gap-2">
              <div v-for="agent in agents" :key="agent.name" class="flex items-center gap-2.5 bg-slate-800/40 rounded-lg px-3 py-2 border border-slate-800/60">
                <span class="text-sm">{{ agent.icon }}</span>
                <div>
                  <div class="text-caption font-semibold text-slate-300">{{ agent.name }}</div>
                  <div class="text-tiny text-slate-600">{{ agent.desc }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Trust signals -->
          <div class="mt-8 flex items-center gap-4 text-detail text-slate-600">
            <div class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              HIPAA-grade encryption
            </div>
            <div class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
              Encrypted at rest
            </div>
          </div>
        </div>
      </div>

      <!-- Right login panel -->
      <div class="bg-slate-900 p-6 sm:p-8 lg:rounded-r-2xl">
        <!-- Mobile logo -->
        <div class="lg:hidden text-center mb-6">
          <div class="inline-flex p-3 rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-600 shadow-xl shadow-emerald-500/20 mb-4">
            <svg class="w-9 h-9 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-white">Medical Diagnosis AI</h1>
        </div>

        <h2 class="text-xl font-bold text-white mb-1">Welcome back</h2>
        <p class="text-sm text-slate-400 mb-6">Sign in to access your diagnosis history</p>

        <!-- Error display -->
        <Transition name="fade">
          <div v-if="error" class="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm flex items-start gap-2">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
            <span>{{ error }}</span>
          </div>
        </Transition>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-slate-300 mb-1.5">Email address</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/></svg>
              </div>
              <input
                id="email"
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="you@example.com"
                class="w-full pl-10 pr-4 py-3 bg-slate-800/60 border border-slate-700/60 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-slate-300 mb-1.5">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              </div>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="current-password"
                placeholder="Enter your password"
                class="w-full pl-10 pr-12 py-3 bg-slate-800/60 border border-slate-700/60 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-500 hover:text-slate-300 transition-colors"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
              </button>
            </div>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-4 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-semibold rounded-xl shadow-lg shadow-emerald-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center gap-3">
          <div class="flex-1 h-px bg-slate-800"></div>
          <span class="text-xs text-slate-600">New here?</span>
          <div class="flex-1 h-px bg-slate-800"></div>
        </div>

        <!-- Signup link -->
        <router-link
          to="/signup"
          class="w-full block text-center py-3 px-4 bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 hover:text-white font-medium rounded-xl border border-slate-700/50 transition-all"
        >
          Create an account
        </router-link>

        <!-- Skip link -->
        <div class="mt-4 text-center">
          <router-link to="/setup" class="text-xs text-slate-600 hover:text-slate-400 transition-colors">
            Continue without an account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login as authLogin } from '@/services/authService'
import { saveProfile } from '@/services/userService'

const router = useRouter()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

const agents = [
  { icon: '\u{1F6A8}', name: 'Triage', desc: 'Urgency assessment' },
  { icon: '\u{1FA7A}', name: 'Diagnostician', desc: 'Differential diagnosis' },
  { icon: '\u{1F52C}', name: 'Research', desc: 'Evidence-based analysis' },
  { icon: '\u{1F3AF}', name: 'Specialist', desc: 'Domain-specific analysis' },
  { icon: '\u{1F48A}', name: 'Treatment', desc: 'Treatment planning' },
  { icon: '\u{1F6E1}\uFE0F', name: 'Safety', desc: 'Contraindication checks' },
]

async function handleLogin() {
  error.value = ''
  loading.value = true

  try {
    const data = await authLogin(email.value, password.value)
    // Reset and sync user_profile with the authenticated user
    localStorage.removeItem('user_profile')
    if (data.user) {
      saveProfile({
        email: data.user.email,
        name: data.user.name || data.user.email.split('@')[0],
        ...(data.user.profile_data || {}),
      })
    }
    // Mark API key as configured so the consult guard passes
    localStorage.setItem('api_key_configured', 'true')
    router.push('/consult')
  } catch (e) {
    error.value = e.message || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
