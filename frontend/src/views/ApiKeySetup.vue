<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
    <div class="max-w-2xl w-full space-y-8">
      <!-- Header -->
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="p-4 bg-white/10 rounded-2xl backdrop-blur-sm">
            <svg class="w-16 h-16 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"></path>
            </svg>
          </div>
        </div>
        <h1 class="text-4xl font-bold text-white mb-4">{{ $t('apiSetup.title') }}</h1>
        <p class="text-xl text-blue-200 mb-8">{{ $t('apiSetup.subtitle') }}</p>
      </div>

      <!-- API Key Setup Card -->
      <div class="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
        <div class="space-y-6">
          <div>
            <h2 class="text-2xl font-semibold text-white mb-2">{{ $t('apiSetup.configTitle') }}</h2>
            <p class="text-blue-200">
              {{ $t('apiSetup.configSubtitle') }}
            </p>
          </div>

          <!-- API Key Input -->
          <div class="space-y-4">
            <div>
              <label for="apiKey" class="block text-sm font-medium text-blue-200 mb-2">
                {{ $t('apiSetup.apiKeyLabel') }}
              </label>
              <div class="relative">
                <input
                  id="apiKey"
                  v-model="apiKey"
                  :type="showApiKey ? 'text' : 'password'"
                  :placeholder="$t('apiSetup.apiKeyPlaceholder')"
                  class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent backdrop-blur-sm"
                  @keyup.enter="saveAndContinue"
                />
                <button
                  type="button"
                  @click="showApiKey = !showApiKey"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center"
                >
                  <svg v-if="showApiKey" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                  </svg>
                  <svg v-else class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.543 7-1.275 4.057-5.065 7-9.543 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="error" class="p-4 bg-red-500/20 border border-red-500/30 rounded-lg">
              <p class="text-red-200 text-sm">{{ error }}</p>
            </div>

            <!-- Success Message -->
            <div v-if="success" class="p-4 bg-green-500/20 border border-green-500/30 rounded-lg">
              <p class="text-green-200 text-sm">{{ success }}</p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-4">
            <button
              @click="saveAndContinue"
              :disabled="!apiKey.trim() || isLoading"
              class="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200 flex items-center justify-center"
            >
              <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isLoading ? $t('apiSetup.validating') : $t('apiSetup.saveAndContinue') }}
            </button>
            
            <button
              @click="skipSetup"
              class="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
            >
              {{ $t('apiSetup.skipForNow') }}
            </button>
          </div>

          <!-- Help Text -->
          <div class="bg-blue-500/20 border border-blue-500/30 rounded-lg p-4">
            <h4 class="text-blue-200 font-semibold mb-2">{{ $t('apiSetup.needKeyTitle') }}</h4>
            <p class="text-blue-200 text-sm mb-3">
              {{ $t('apiSetup.needKeySubtitle') }}
            </p>
            <ol class="text-blue-200 text-sm space-y-1 ml-4 list-decimal">
              <li><a href="https://platform.openai.com/api-keys" target="_blank" class="text-blue-300 hover:text-blue-100 underline">{{ $t('apiSetup.steps.step1') }}</a></li>
              <li>{{ $t('apiSetup.steps.step2') }}</li>
              <li>{{ $t('apiSetup.steps.step3') }}</li>
              <li>{{ $t('apiSetup.steps.step4') }}</li>
            </ol>
            <p class="text-blue-300 text-xs mt-3">
              ⚠️ {{ $t('apiSetup.securityNote') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center">
        <p class="text-blue-300 text-sm">
          {{ $t('apiSetup.footer') }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

export default {
  name: 'ApiKeySetup',
  setup() {
    const router = useRouter()
    const { t } = useI18n()
    const apiKey = ref(localStorage.getItem('openai_api_key') || '')
    const showApiKey = ref(false)
    const isLoading = ref(false)
    const error = ref('')
    const success = ref('')

    const validateApiKey = (key) => {
      if (!key.trim()) {
        return t('apiSetup.errors.required')
      }
      if (!key.startsWith('sk-')) {
        return t('apiSetup.errors.invalidFormat')
      }
      if (key.length < 20) {
        return t('apiSetup.errors.tooShort')
      }
      return null
    }

    const saveAndContinue = async () => {
      error.value = ''
      success.value = ''

      const validationError = validateApiKey(apiKey.value)
      if (validationError) {
        error.value = validationError
        return
      }

      isLoading.value = true

      try {
        // Save to localStorage
        localStorage.setItem('openai_api_key', apiKey.value.trim())
        localStorage.setItem('api_key_configured', 'true')

        success.value = t('apiSetup.success')

        // Redirect to main app after a brief delay
        setTimeout(() => {
          router.push('/')
        }, 1000)

      } catch (err) {
        error.value = t('apiSetup.errors.saveFailed')
        console.error('Error saving API key:', err)
      } finally {
        isLoading.value = false
      }
    }

    const skipSetup = () => {
      localStorage.setItem('api_key_configured', 'skipped')
      router.push('/')
    }

    return {
      apiKey,
      showApiKey,
      isLoading,
      error,
      success,
      saveAndContinue,
      skipSetup
    }
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>