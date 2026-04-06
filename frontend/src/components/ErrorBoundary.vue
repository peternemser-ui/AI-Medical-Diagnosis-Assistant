<!--
  Error Boundary Wrapper Component

  Catches rendering errors in child components and shows a recovery UI
  instead of crashing the entire app. Does NOT replace any existing error handling.
-->
<template>
  <div>
    <div v-if="hasError" class="rounded-xl border p-6 text-center" :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-200'">
      <svg class="w-10 h-10 mx-auto mb-3 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
      </svg>
      <h3 class="text-sm font-bold mb-1" :class="isDark ? 'text-red-300' : 'text-red-700'">Something went wrong</h3>
      <p class="text-xs mb-3" :class="isDark ? 'text-red-400' : 'text-red-600'">{{ errorMessage }}</p>
      <button @click="recover" class="px-4 py-2 text-xs font-medium rounded-lg bg-red-500 text-white hover:bg-red-600 transition-colors">
        Try Again
      </button>
    </div>
    <slot v-else></slot>
  </div>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
const hasError = ref(false)
const errorMessage = ref('')

onErrorCaptured((err) => {
  hasError.value = true
  errorMessage.value = err.message || 'An unexpected error occurred'
  console.error('[ErrorBoundary]', err)
  return false  // Prevent propagation
})

function recover() {
  hasError.value = false
  errorMessage.value = ''
}
</script>
