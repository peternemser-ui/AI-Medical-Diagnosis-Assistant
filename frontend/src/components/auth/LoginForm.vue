<template>
  <div class="login-form">
    <h2 class="text-2xl font-bold text-center mb-6 dark:text-white">
      {{ $t('auth.login') || 'Sign In' }}
    </h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {{ $t('auth.email') || 'Email' }}
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          autocomplete="email"
          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          :class="{ 'border-red-500': errors.email }"
          :placeholder="$t('auth.emailPlaceholder') || 'Enter your email'"
        />
        <p v-if="errors.email" class="mt-1 text-sm text-red-500">{{ errors.email }}</p>
      </div>

      <!-- Password -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {{ $t('auth.password') || 'Password' }}
        </label>
        <div class="relative">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            required
            autocomplete="current-password"
            class="w-full px-4 py-2 pr-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            :class="{ 'border-red-500': errors.password }"
            :placeholder="$t('auth.passwordPlaceholder') || 'Enter your password'"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700 dark:text-gray-400"
          >
            <component :is="showPassword ? 'EyeOff' : 'Eye'" class="w-5 h-5" />
          </button>
        </div>
        <p v-if="errors.password" class="mt-1 text-sm text-red-500">{{ errors.password }}</p>
      </div>

      <!-- Remember me & Forgot password -->
      <div class="flex items-center justify-between">
        <label class="flex items-center">
          <input
            v-model="form.rememberMe"
            type="checkbox"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">
            {{ $t('auth.rememberMe') || 'Remember me' }}
          </span>
        </label>
        <button
          type="button"
          @click="$emit('forgot-password')"
          class="text-sm text-blue-600 hover:text-blue-500 dark:text-blue-400"
        >
          {{ $t('auth.forgotPassword') || 'Forgot password?' }}
        </button>
      </div>

      <!-- Error message -->
      <div v-if="authError" class="p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
        {{ authError }}
      </div>

      <!-- Submit button -->
      <button
        type="submit"
        :disabled="isLoading"
        class="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="isLoading" class="flex items-center justify-center">
          <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ $t('auth.signingIn') || 'Signing in...' }}
        </span>
        <span v-else>{{ $t('auth.signIn') || 'Sign In' }}</span>
      </button>

      <!-- Register link -->
      <p class="text-center text-sm text-gray-600 dark:text-gray-400">
        {{ $t('auth.noAccount') || "Don't have an account?" }}
        <button
          type="button"
          @click="$emit('switch-to-register')"
          class="text-blue-600 hover:text-blue-500 dark:text-blue-400 font-medium"
        >
          {{ $t('auth.signUp') || 'Sign up' }}
        </button>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { Eye, EyeOff } from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'

const emit = defineEmits(['success', 'forgot-password', 'switch-to-register'])

const { login, isLoading, error: authError, clearError } = useAuth()

const form = reactive({
  email: '',
  password: '',
  rememberMe: false
})

const errors = reactive({
  email: '',
  password: ''
})

const showPassword = ref(false)

function validate() {
  let isValid = true
  errors.email = ''
  errors.password = ''

  if (!form.email) {
    errors.email = 'Email is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email'
    isValid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  clearError()

  if (!validate()) return

  try {
    await login(form.email, form.password)
    emit('success')
  } catch (err) {
    console.error('Login failed:', err)
  }
}
</script>

<style scoped>
.login-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
