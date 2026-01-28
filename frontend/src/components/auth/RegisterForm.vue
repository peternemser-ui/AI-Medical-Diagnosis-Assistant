<template>
  <div class="register-form">
    <h2 class="text-2xl font-bold text-center mb-6 dark:text-white">
      {{ $t('auth.createAccount') || 'Create Account' }}
    </h2>

    <form @submit.prevent="handleSubmit" class="space-y-4">
      <!-- Name -->
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {{ $t('auth.fullName') || 'Full Name' }}
        </label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          required
          autocomplete="name"
          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          :class="{ 'border-red-500': errors.name }"
          :placeholder="$t('auth.namePlaceholder') || 'Enter your full name'"
        />
        <p v-if="errors.name" class="mt-1 text-sm text-red-500">{{ errors.name }}</p>
      </div>

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
            autocomplete="new-password"
            class="w-full px-4 py-2 pr-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            :class="{ 'border-red-500': errors.password }"
            :placeholder="$t('auth.passwordPlaceholder') || 'Create a password'"
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

        <!-- Password strength indicator -->
        <div class="mt-2">
          <div class="flex gap-1">
            <div
              v-for="i in 4"
              :key="i"
              class="h-1 flex-1 rounded"
              :class="passwordStrengthColor(i)"
            ></div>
          </div>
          <p class="text-xs text-gray-500 mt-1">
            {{ passwordStrengthText }}
          </p>
        </div>
      </div>

      <!-- Confirm Password -->
      <div>
        <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
          {{ $t('auth.confirmPassword') || 'Confirm Password' }}
        </label>
        <input
          id="confirmPassword"
          v-model="form.confirmPassword"
          :type="showPassword ? 'text' : 'password'"
          required
          autocomplete="new-password"
          class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          :class="{ 'border-red-500': errors.confirmPassword }"
          :placeholder="$t('auth.confirmPasswordPlaceholder') || 'Confirm your password'"
        />
        <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-500">{{ errors.confirmPassword }}</p>
      </div>

      <!-- Terms -->
      <div class="flex items-start">
        <input
          id="terms"
          v-model="form.acceptTerms"
          type="checkbox"
          required
          class="w-4 h-4 mt-1 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
        />
        <label for="terms" class="ml-2 text-sm text-gray-600 dark:text-gray-400">
          {{ $t('auth.agreeToTerms') || 'I agree to the' }}
          <a href="#" class="text-blue-600 hover:text-blue-500">{{ $t('auth.termsOfService') || 'Terms of Service' }}</a>
          {{ $t('auth.and') || 'and' }}
          <a href="#" class="text-blue-600 hover:text-blue-500">{{ $t('auth.privacyPolicy') || 'Privacy Policy' }}</a>
        </label>
      </div>
      <p v-if="errors.terms" class="text-sm text-red-500">{{ errors.terms }}</p>

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
          {{ $t('auth.creatingAccount') || 'Creating account...' }}
        </span>
        <span v-else>{{ $t('auth.createAccount') || 'Create Account' }}</span>
      </button>

      <!-- Login link -->
      <p class="text-center text-sm text-gray-600 dark:text-gray-400">
        {{ $t('auth.haveAccount') || 'Already have an account?' }}
        <button
          type="button"
          @click="$emit('switch-to-login')"
          class="text-blue-600 hover:text-blue-500 dark:text-blue-400 font-medium"
        >
          {{ $t('auth.signIn') || 'Sign in' }}
        </button>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Eye, EyeOff } from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'

const emit = defineEmits(['success', 'switch-to-login'])

const { register, isLoading, error: authError, clearError } = useAuth()

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  acceptTerms: false
})

const errors = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  terms: ''
})

const showPassword = ref(false)

const passwordStrength = computed(() => {
  const password = form.password
  let strength = 0

  if (password.length >= 8) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++

  return strength
})

const passwordStrengthText = computed(() => {
  const texts = ['Very weak', 'Weak', 'Fair', 'Strong', 'Very strong']
  return texts[passwordStrength.value] || ''
})

function passwordStrengthColor(index) {
  if (index <= passwordStrength.value) {
    const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500']
    return colors[passwordStrength.value - 1] || 'bg-gray-200'
  }
  return 'bg-gray-200 dark:bg-gray-600'
}

function validate() {
  let isValid = true
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.name || form.name.length < 2) {
    errors.name = 'Name must be at least 2 characters'
    isValid = false
  }

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
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
    isValid = false
  } else if (passwordStrength.value < 3) {
    errors.password = 'Password is too weak'
    isValid = false
  }

  if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    isValid = false
  }

  if (!form.acceptTerms) {
    errors.terms = 'You must accept the terms and conditions'
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  clearError()

  if (!validate()) return

  try {
    await register({
      name: form.name,
      email: form.email,
      password: form.password
    })
    emit('success')
  } catch (err) {
    console.error('Registration failed:', err)
  }
}
</script>

<style scoped>
.register-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
