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
          <p class="text-slate-400 mt-4 text-base leading-relaxed">Create your secure account to save diagnosis history and get personalized health insights.</p>

          <div class="mt-10 space-y-4">
            <div class="text-detail text-slate-500 uppercase tracking-widest font-bold">Why create an account?</div>
            <div class="space-y-3">
              <div class="flex items-start gap-3">
                <div class="w-8 h-8 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                </div>
                <div>
                  <div class="text-sm font-medium text-slate-200">Diagnosis History</div>
                  <div class="text-xs text-slate-500">Access all your past consultations securely</div>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <div class="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
                </div>
                <div>
                  <div class="text-sm font-medium text-slate-200">HIPAA-Grade Security</div>
                  <div class="text-xs text-slate-500">Field-level encryption for all patient data</div>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <div class="w-8 h-8 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                </div>
                <div>
                  <div class="text-sm font-medium text-slate-200">Health Trends</div>
                  <div class="text-xs text-slate-500">Track and compare diagnoses over time</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right signup panel -->
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

        <h2 class="text-xl font-bold text-white mb-1">Create your account</h2>
        <p class="text-sm text-slate-400 mb-6">Secure, encrypted, HIPAA-compliant</p>

        <!-- Error display -->
        <Transition name="fade">
          <div v-if="error" class="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm flex items-start gap-2">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
            <span>{{ error }}</span>
          </div>
        </Transition>

        <form @submit.prevent="handleSignup" class="space-y-4">
          <!-- Name -->
          <div>
            <label for="name" class="block text-sm font-medium text-slate-300 mb-1.5">Full name</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              </div>
              <input
                id="name"
                v-model="name"
                type="text"
                required
                autocomplete="name"
                placeholder="Jane Doe"
                class="w-full pl-10 pr-4 py-3 bg-slate-800/60 border border-slate-700/60 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="signup-email" class="block text-sm font-medium text-slate-300 mb-1.5">Email address</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/></svg>
              </div>
              <input
                id="signup-email"
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
            <label for="signup-password" class="block text-sm font-medium text-slate-300 mb-1.5">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              </div>
              <input
                id="signup-password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="new-password"
                placeholder="Minimum 8 characters"
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

            <!-- Password strength indicator -->
            <div class="mt-2 space-y-1.5">
              <div class="flex gap-1">
                <div v-for="i in 4" :key="i" class="h-1 flex-1 rounded-full transition-all duration-300"
                  :class="i <= passwordStrength ? strengthColors[passwordStrength] : 'bg-slate-800'"></div>
              </div>
              <p class="text-caption transition-colors" :class="passwordStrengthLabel.color">
                {{ passwordStrengthLabel.text }}
              </p>
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirm-password" class="block text-sm font-medium text-slate-300 mb-1.5">Confirm password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="w-5 h-5 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
              <input
                id="confirm-password"
                v-model="confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="new-password"
                placeholder="Re-enter your password"
                class="w-full pl-10 pr-4 py-3 bg-slate-800/60 border border-slate-700/60 rounded-xl text-white placeholder:text-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500/50 transition-all"
                :class="confirmPassword && confirmPassword !== password ? 'border-red-500/50 focus:ring-red-500/50' : ''"
              />
            </div>
            <p v-if="confirmPassword && confirmPassword !== password" class="text-caption text-red-400 mt-1">
              Passwords do not match
            </p>
          </div>

          <!-- Terms -->
          <label class="flex items-start gap-3 cursor-pointer group">
            <input
              v-model="acceptTerms"
              type="checkbox"
              required
              class="mt-1 w-4 h-4 rounded border-slate-600 bg-slate-800 text-emerald-500 focus:ring-emerald-500/30 focus:ring-2 cursor-pointer"
            />
            <span class="text-xs text-slate-400 group-hover:text-slate-300 transition-colors leading-relaxed">
              I agree to the Terms of Service and acknowledge that my health information will be encrypted (AES-256) and stored locally on this device only. No medical data is sent to or stored on our servers. I consent to this under HIPAA guidelines.
            </span>
          </label>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading || !canSubmit"
            class="w-full py-3 px-4 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-semibold rounded-xl shadow-lg shadow-emerald-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center gap-3">
          <div class="flex-1 h-px bg-slate-800"></div>
          <span class="text-xs text-slate-600">Already have an account?</span>
          <div class="flex-1 h-px bg-slate-800"></div>
        </div>

        <!-- Login link -->
        <router-link
          to="/login"
          class="w-full block text-center py-3 px-4 bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 hover:text-white font-medium rounded-xl border border-slate-700/50 transition-all"
        >
          Sign in instead
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { signup as authSignup } from '@/services/authService'
import { saveProfile } from '@/services/userService'

const router = useRouter()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const acceptTerms = ref(false)
const loading = ref(false)
const error = ref('')

const strengthColors = {
  1: 'bg-red-500',
  2: 'bg-orange-500',
  3: 'bg-yellow-500',
  4: 'bg-emerald-500',
}

const passwordStrength = computed(() => {
  const p = password.value
  if (!p) return 0
  let score = 0
  if (p.length >= 8) score++
  if (/[A-Z]/.test(p) && /[a-z]/.test(p)) score++
  if (/\d/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  return score
})

const passwordStrengthLabel = computed(() => {
  const labels = [
    { text: '', color: 'text-slate-600' },
    { text: 'Weak — add uppercase, numbers, or symbols', color: 'text-red-400' },
    { text: 'Fair — consider adding more variety', color: 'text-orange-400' },
    { text: 'Good — almost there', color: 'text-yellow-400' },
    { text: 'Strong password', color: 'text-emerald-400' },
  ]
  return labels[passwordStrength.value]
})

const canSubmit = computed(() => {
  return (
    name.value.trim() &&
    email.value.trim() &&
    password.value.length >= 8 &&
    password.value === confirmPassword.value &&
    acceptTerms.value
  )
})

async function handleSignup() {
  if (!canSubmit.value) return

  error.value = ''
  loading.value = true

  try {
    const data = await authSignup(name.value.trim(), email.value.trim(), password.value)
    // Reset user_profile for the new account (clear old profile data)
    localStorage.removeItem('user_profile')
    await saveProfile({
      name: name.value.trim(),
      email: email.value.trim(),
      ...(data.user?.profile_data || {}),
    })
    localStorage.setItem('api_key_configured', 'true')
    router.push('/setup')
  } catch (e) {
    error.value = e.message || 'Signup failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
