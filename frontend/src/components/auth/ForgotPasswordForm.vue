<template>
  <div class="forgot-password-form">
    <h2 class="text-2xl font-bold text-center mb-2 dark:text-white">
      {{ $t('auth.resetPassword') || 'Reset Password' }}
    </h2>
    <p class="text-center text-gray-600 dark:text-gray-400 mb-6">
      {{ $t('auth.resetPasswordDescription') || "Enter your email and we'll send you a link to reset your password." }}
    </p>

    <form v-if="!submitted" @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {{ $t('auth.email') || 'Email' }}
        </label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          autocomplete="email"
          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          :class="{ 'border-red-500': error }"
          :placeholder="$t('auth.emailPlaceholder') || 'Enter your email'"
        />
        <p v-if="error" class="mt-1 text-sm text-red-500">{{ error }}</p>
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
          {{ $t('auth.sending') || 'Sending...' }}
        </span>
        <span v-else>{{ $t('auth.sendResetLink') || 'Send Reset Link' }}</span>
      </button>

      <!-- Back to login -->
      <button
        type="button"
        @click="$emit('back-to-login')"
        class="w-full py-2 px-4 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
      >
        {{ $t('auth.backToLogin') || 'Back to Login' }}
      </button>
    </form>

    <!-- Success message -->
    <div v-else class="text-center">
      <div class="w-16 h-16 mx-auto mb-4 bg-green-100 rounded-full flex items-center justify-center">
        <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
        {{ $t('auth.checkYourEmail') || 'Check your email' }}
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        {{ $t('auth.resetEmailSent') || "We've sent a password reset link to" }}
        <span class="font-medium">{{ email }}</span>
      </p>
      <button
        @click="$emit('back-to-login')"
        class="text-blue-600 hover:text-blue-500 dark:text-blue-400 font-medium"
      >
        {{ $t('auth.backToLogin') || 'Back to Login' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuth } from '@/composables/useAuth'

const emit = defineEmits(['back-to-login'])

const { forgotPassword, isLoading } = useAuth()

const email = ref('')
const error = ref('')
const submitted = ref(false)

async function handleSubmit() {
  error.value = ''

  if (!email.value) {
    error.value = 'Email is required'
    return
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    error.value = 'Please enter a valid email'
    return
  }

  try {
    await forgotPassword(email.value)
    submitted.value = true
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to send reset email'
  }
}
</script>

<style scoped>
.forgot-password-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
