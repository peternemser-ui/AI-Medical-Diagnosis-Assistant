<template>
  <div class="min-h-screen flex items-center justify-center relative overflow-hidden p-4 transition-colors duration-300"
    :class="isDark ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'">

    <!-- Minimal background accent -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden" aria-hidden="true">
      <div class="absolute top-0 right-0 w-[480px] h-[480px] opacity-[0.05] rounded-full"
        style="background: radial-gradient(circle at center, #4f46e5, transparent 70%); transform: translate(30%, -30%);"></div>
    </div>

    <div class="relative z-10 w-full max-w-[940px] grid grid-cols-1 lg:grid-cols-[40%_1fr] rounded-2xl shadow-2xl overflow-hidden border"
      :class="isDark ? 'shadow-black/70 border-slate-800' : 'shadow-slate-200/80 shadow-xl border-slate-200'">

      <!-- ── Left branding panel ── -->
      <div class="hidden lg:flex relative items-center justify-center p-8 rounded-l-2xl"
        :class="isDark ? 'bg-slate-900 border-r border-slate-800' : 'bg-slate-900 border-r border-slate-800'">
        <!-- Subtle grid overlay -->
        <div class="absolute inset-0 rounded-l-2xl overflow-hidden opacity-[0.04]"
          style="background-image: linear-gradient(rgba(255,255,255,0.6) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.6) 1px,transparent 1px); background-size: 48px 48px;"></div>

        <div class="relative z-10 max-w-xs w-full">
          <!-- Logo -->
          <div class="inline-flex p-3.5 rounded-2xl bg-indigo-700 shadow-2xl shadow-indigo-700/40 mb-8">
            <svg class="w-10 h-10 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>

          <h1 class="text-3xl font-extrabold text-white tracking-tight leading-tight mb-2">Join Your AI<br/>Medical Team</h1>
          <p class="text-slate-400 text-sm leading-relaxed mb-8">
            Create your secure account and get started in under a minute.
          </p>

          <!-- Why create an account -->
          <div class="space-y-4 mb-8">
            <div class="text-[10px] font-bold uppercase tracking-widest text-slate-500">Why create an account?</div>
            <div v-for="benefit in accountBenefits" :key="benefit.title" class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5"
                :style="{ background: benefit.bg, border: `1px solid ${benefit.border}` }">
                <svg class="w-4 h-4" :style="{ color: benefit.iconColor }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="benefit.icon" />
                </svg>
              </div>
              <div>
                <div class="text-sm font-semibold text-slate-200">{{ benefit.title }}</div>
                <div class="text-xs text-slate-500 mt-0.5">{{ benefit.desc }}</div>
              </div>
            </div>
          </div>

          <!-- Trust signals -->
          <div class="pt-6 border-t border-slate-800 flex flex-col gap-2">
            <div class="flex items-center gap-2 text-xs text-slate-500">
              <svg class="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              AES-256 field-level encryption
            </div>
            <div class="flex items-center gap-2 text-xs text-slate-500">
              <svg class="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
              HIPAA-compliant design
            </div>
          </div>
        </div>
      </div>

      <!-- ── Right signup panel ── -->
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

        <h2 class="text-2xl font-bold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">Create your account</h2>
        <p class="text-sm mb-7" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Secure, encrypted, HIPAA-compliant</p>

        <!-- Check your email — shown after successful signup -->
        <Transition name="fade">
          <div v-if="signupSuccess" class="space-y-4">
            <div class="p-7 rounded-2xl border text-center"
              :class="isDark ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-emerald-50 border-emerald-200'">
              <!-- Animated email icon -->
              <div class="w-16 h-16 mx-auto mb-5 rounded-2xl bg-emerald-500/15 border border-emerald-500/20 flex items-center justify-center">
                <svg class="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              </div>
              <h3 class="text-lg font-bold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Check your email</h3>
              <p class="text-sm mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">We sent a verification link to</p>
              <p class="text-sm font-semibold text-emerald-500 mb-4">{{ signupEmail }}</p>
              <p class="text-xs leading-relaxed" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                Click the link in the email to verify your address, then sign in to start your first consultation.
              </p>
            </div>
            <router-link
              to="/login"
              class="w-full block text-center py-3 px-4 text-sm font-semibold rounded-xl bg-indigo-700 hover:bg-indigo-600 text-white shadow-lg shadow-indigo-700/25 transition-all"
            >
              Go to sign in
            </router-link>
          </div>
        </Transition>

        <!-- Error display -->
        <Transition name="fade">
          <div v-if="error && !signupSuccess" id="signup-error" role="alert" class="mb-5 p-3.5 bg-red-500/10 border border-red-500/25 rounded-xl text-red-400 text-sm flex items-start gap-2.5">
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
            <span>{{ error }}</span>
          </div>
        </Transition>

        <form v-if="!signupSuccess" @submit.prevent="handleSignup" class="space-y-4" novalidate>
          <!-- Name -->
          <div>
            <label for="name" class="block text-sm font-medium mb-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Full name</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              </div>
              <input
                id="name"
                v-model="name"
                type="text"
                required
                autocomplete="name"
                placeholder="Jane Doe"
                class="w-full pl-10 pr-4 py-3 rounded-xl text-sm focus:outline-none focus:ring-2 transition-all"
                :class="isDark
                  ? 'bg-slate-800/70 border border-slate-700 text-white placeholder:text-slate-600 focus:ring-indigo-500/40 focus:border-indigo-500/50'
                  : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 focus:ring-indigo-400/40 focus:border-indigo-400/60'"
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="signup-email" class="block text-sm font-medium mb-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Email address</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"/></svg>
              </div>
              <input
                id="signup-email"
                v-model="email"
                type="email"
                required
                autocomplete="email"
                placeholder="you@example.com"
                :aria-invalid="email && !isValidEmail ? 'true' : undefined"
                :aria-describedby="email && !isValidEmail ? 'signup-email-error' : undefined"
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
            <p v-if="email && !isValidEmail" id="signup-email-error" role="alert" class="text-xs mt-1.5 text-red-400">Please enter a valid email address</p>
          </div>

          <!-- Password -->
          <div>
            <label for="signup-password" class="block text-sm font-medium mb-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              </div>
              <input
                id="signup-password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="new-password"
                placeholder="Minimum 8 characters"
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
                <svg v-if="!showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/></svg>
              </button>
            </div>

            <!-- Password strength — proper progress bar -->
            <div v-if="password" class="mt-2.5 space-y-1.5">
              <!-- Single continuous progress bar -->
              <div class="relative h-2 rounded-full overflow-hidden"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"
                role="progressbar"
                :aria-valuenow="strengthLevel"
                aria-valuemin="0"
                aria-valuemax="4"
                :aria-label="`Password strength: ${strengthLabelText}`">
                <div class="absolute inset-y-0 left-0 rounded-full transition-all duration-500"
                  :style="{ width: `${(strengthLevel / 4) * 100}%` }"
                  :class="strengthBarColor"></div>
              </div>
              <p class="text-xs font-semibold transition-colors" :class="strengthLabelColor" aria-live="polite">
                {{ strengthLabelText }}
              </p>
            </div>

            <!-- Password requirement hints -->
            <div v-if="password" class="mt-2 grid grid-cols-2 gap-x-4 gap-y-1">
              <div class="flex items-center gap-1.5 text-xs" :class="pwHasLength ? 'text-emerald-500' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                <svg v-if="pwHasLength" class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                <svg v-else class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>
                8+ characters
              </div>
              <div class="flex items-center gap-1.5 text-xs" :class="pwHasUpper ? 'text-emerald-500' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                <svg v-if="pwHasUpper" class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                <svg v-else class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>
                Uppercase
              </div>
              <div class="flex items-center gap-1.5 text-xs" :class="pwHasLower ? 'text-emerald-500' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                <svg v-if="pwHasLower" class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                <svg v-else class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>
                Lowercase
              </div>
              <div class="flex items-center gap-1.5 text-xs" :class="pwHasNumber ? 'text-emerald-500' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                <svg v-if="pwHasNumber" class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                <svg v-else class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>
                Number
              </div>
              <div class="flex items-center gap-1.5 text-xs col-span-2" :class="pwHasSpecial ? 'text-emerald-500' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                <svg v-if="pwHasSpecial" class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                <svg v-else class="w-3 h-3 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/></svg>
                Special character (!@#$...)
              </div>
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirm-password" class="block text-sm font-medium mb-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Confirm password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
                <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              </div>
              <input
                id="confirm-password"
                v-model="confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                required
                autocomplete="new-password"
                placeholder="Re-enter your password"
                class="w-full pl-10 pr-4 py-3 rounded-xl text-sm focus:outline-none focus:ring-2 transition-all"
                :class="[
                  isDark
                    ? 'bg-slate-800/70 border border-slate-700 text-white placeholder:text-slate-600 focus:ring-indigo-500/40 focus:border-indigo-500/50'
                    : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder:text-slate-400 focus:ring-indigo-400/40 focus:border-indigo-400/60',
                  confirmPassword && confirmPassword !== password ? 'border-red-500/60 focus:ring-red-400/30' : ''
                ]"
              />
            </div>
            <p v-if="confirmPassword && confirmPassword !== password" class="text-xs text-red-400 mt-1.5">
              Passwords do not match
            </p>
          </div>

          <!-- Terms -->
          <label class="flex items-start gap-3 cursor-pointer group">
            <input
              v-model="acceptTerms"
              type="checkbox"
              required
              class="mt-0.5 w-4 h-4 rounded border-slate-600 bg-slate-800 text-indigo-500 focus:ring-indigo-500/30 focus:ring-2 cursor-pointer flex-shrink-0"
            />
            <span class="text-xs leading-relaxed transition-colors" :class="isDark ? 'text-slate-400 group-hover:text-slate-300' : 'text-slate-500 group-hover:text-slate-700'">
              I agree to the Terms of Service and acknowledge that my health information will be encrypted (AES-256) and stored locally on this device only. No medical data is sent to or stored on our servers. I consent to this under HIPAA guidelines.
            </span>
          </label>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading || !canSubmit"
            class="w-full py-3.5 px-4 bg-indigo-700 hover:bg-indigo-600 text-white font-semibold rounded-xl shadow-lg shadow-indigo-700/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
          >
            <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>
        </form>

        <!-- Divider + login link (hidden once signup succeeds) -->
        <template v-if="!signupSuccess">
          <div class="my-5 flex items-center gap-3">
            <div class="flex-1 h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
            <span class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Already have an account?</span>
            <div class="flex-1 h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
          </div>

          <router-link
            to="/login"
            class="w-full block text-center py-3 px-4 text-sm font-medium rounded-xl border transition-all"
            :class="isDark
              ? 'bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 hover:text-white border-slate-700'
              : 'bg-slate-50 hover:bg-slate-100 text-slate-600 hover:text-slate-900 border-slate-200'"
          >
            Sign in instead
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { signup as authSignup } from '@/services/authService'
import { saveProfile } from '@/services/userService'
import { trackEvent, EVENTS } from '@/services/analytics'
import { useTheme } from '@/composables/useTheme.js'

const router = useRouter()
const { isDark } = useTheme()

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const acceptTerms = ref(false)
const loading = ref(false)
const error = ref('')

// After successful signup — show "check your email" instead of redirecting
const signupSuccess = ref(false)
const signupEmail = ref('')

const isValidEmail = computed(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value))

// Individual password requirement checks
const pwHasLength = computed(() => password.value.length >= 8)
const pwHasUpper = computed(() => /[A-Z]/.test(password.value))
const pwHasLower = computed(() => /[a-z]/.test(password.value))
const pwHasNumber = computed(() => /\d/.test(password.value))
const pwHasSpecial = computed(() => /[^A-Za-z0-9]/.test(password.value))

// Password strength: Weak(1) <8 chars, Fair(2) 8-11 missing reqs, Good(3) 12+ some reqs, Strong(4) 12+ all reqs
const strengthLevel = computed(() => {
  const p = password.value
  if (!p) return 0
  const allReqs = pwHasUpper.value && pwHasLower.value && pwHasNumber.value && pwHasSpecial.value
  if (p.length >= 12 && allReqs) return 4
  if (p.length >= 12) return 3
  if (p.length >= 8) return 2
  return 1
})

const strengthBarColor = computed(() => {
  const colors = { 1: 'bg-red-500', 2: 'bg-amber-500', 3: 'bg-emerald-400', 4: 'bg-emerald-600' }
  return colors[strengthLevel.value] || ''
})

const strengthLabelText = computed(() => {
  const labels = { 0: '', 1: 'Weak', 2: 'Fair', 3: 'Good', 4: 'Strong' }
  return labels[strengthLevel.value]
})

const strengthLabelColor = computed(() => {
  const colors = { 0: 'text-slate-600', 1: 'text-red-400', 2: 'text-amber-400', 3: 'text-emerald-400', 4: 'text-emerald-500' }
  return colors[strengthLevel.value]
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

// Left panel account benefits
const accountBenefits = [
  {
    title: 'Diagnosis History',
    desc: 'Access all your past consultations securely',
    icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    bg: 'rgba(79,70,229,0.12)',
    border: 'rgba(79,70,229,0.25)',
    iconColor: '#818cf8',
  },
  {
    title: 'HIPAA-Grade Security',
    desc: 'Field-level encryption for all patient data',
    icon: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z',
    bg: 'rgba(16,185,129,0.10)',
    border: 'rgba(16,185,129,0.25)',
    iconColor: '#34d399',
  },
  {
    title: 'Health Trends',
    desc: 'Track and compare diagnoses over time',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    bg: 'rgba(147,51,234,0.10)',
    border: 'rgba(147,51,234,0.25)',
    iconColor: '#c084fc',
  },
]

async function handleSignup() {
  if (!canSubmit.value) return

  error.value = ''
  loading.value = true

  try {
    const trimmedEmail = email.value.trim()
    const data = await authSignup(name.value.trim(), trimmedEmail, password.value)

    trackEvent(EVENTS.SIGNUP, { method: 'email' })

    // Show the "check your email" state instead of auto-redirecting
    signupEmail.value = trimmedEmail
    signupSuccess.value = true
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
