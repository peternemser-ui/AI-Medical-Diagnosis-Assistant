<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="mx-auto w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mb-4">
          <Stethoscope class="w-8 h-8 text-white" />
        </div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ $t('app.title') || 'AI Medical Assistant' }}
        </h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          {{ $t('app.subtitle') || 'Your intelligent health companion' }}
        </p>
      </div>

      <!-- Auth Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg">
        <LoginForm
          v-if="currentView === 'login'"
          @success="handleSuccess"
          @forgot-password="currentView = 'forgot'"
          @switch-to-register="currentView = 'register'"
        />

        <RegisterForm
          v-else-if="currentView === 'register'"
          @success="handleSuccess"
          @switch-to-login="currentView = 'login'"
        />

        <ForgotPasswordForm
          v-else-if="currentView === 'forgot'"
          @back-to-login="currentView = 'login'"
        />
      </div>

      <!-- Footer -->
      <div class="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
        <p>{{ $t('auth.medicalDisclaimer') || 'This tool is for informational purposes only and does not replace professional medical advice.' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Stethoscope } from 'lucide-vue-next'
import LoginForm from '@/components/auth/LoginForm.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'
import ForgotPasswordForm from '@/components/auth/ForgotPasswordForm.vue'

const router = useRouter()
const route = useRoute()

const currentView = ref('login')

function handleSuccess() {
  const redirectTo = route.query.redirect || '/'
  router.push(redirectTo)
}
</script>
