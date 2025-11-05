<template>
  <div class="error-boundary">
    <slot v-if="!hasError"></slot>

    <div v-else class="error-boundary-fallback" role="alert" aria-live="assertive">
      <div class="error-content">
        <div class="error-icon">
          <svg class="w-16 h-16 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z">
            </path>
          </svg>
        </div>

        <h2 class="error-title">{{ title }}</h2>
        <p class="error-message">{{ message }}</p>

        <div v-if="showDetails && errorDetails" class="error-details">
          <button
            @click="detailsExpanded = !detailsExpanded"
            class="error-details-toggle"
            :aria-expanded="detailsExpanded"
          >
            {{ detailsExpanded ? 'Hide' : 'Show' }} Error Details
            <svg
              class="w-4 h-4 ml-2 transition-transform"
              :class="{ 'rotate-180': detailsExpanded }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
          </button>

          <div v-if="detailsExpanded" class="error-details-content">
            <pre>{{ errorDetails }}</pre>
          </div>
        </div>

        <div class="error-actions">
          <button
            @click="handleRetry"
            class="btn btn-primary"
            :disabled="retrying"
          >
            <svg v-if="retrying" class="animate-spin w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ retrying ? 'Retrying...' : 'Try Again' }}
          </button>

          <button
            v-if="showReload"
            @click="handleReload"
            class="btn btn-secondary"
          >
            Reload Page
          </button>

          <button
            v-if="onReset"
            @click="handleReset"
            class="btn btn-secondary"
          >
            Reset Application
          </button>
        </div>

        <div v-if="showSupport" class="error-support">
          <p class="text-sm text-gray-400">
            If this problem persists, please
            <a href="https://github.com/anthropics/claude-code/issues" target="_blank" rel="noopener" class="text-blue-400 hover:text-blue-300">
              report this issue
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onErrorCaptured, computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Something went wrong'
  },
  message: {
    type: String,
    default: 'An unexpected error occurred. Please try again.'
  },
  showDetails: {
    type: Boolean,
    default: true
  },
  showReload: {
    type: Boolean,
    default: true
  },
  showSupport: {
    type: Boolean,
    default: true
  },
  onRetry: {
    type: Function,
    default: null
  },
  onReset: {
    type: Function,
    default: null
  },
  logErrors: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['error', 'retry', 'reset'])

const hasError = ref(false)
const error = ref(null)
const errorInfo = ref(null)
const detailsExpanded = ref(false)
const retrying = ref(false)

const errorDetails = computed(() => {
  if (!error.value) return null

  return {
    message: error.value.message,
    stack: error.value.stack,
    info: errorInfo.value,
    timestamp: new Date().toISOString()
  }
})

// Capture errors from child components
onErrorCaptured((err, instance, info) => {
  hasError.value = true
  error.value = err
  errorInfo.value = info

  if (props.logErrors) {
    console.error('❌ Error Boundary caught error:', err)
    console.error('Component:', instance)
    console.error('Error Info:', info)
  }

  emit('error', { error: err, instance, info })

  // Prevent error from propagating
  return false
})

// Also catch global unhandled errors
if (typeof window !== 'undefined') {
  const originalErrorHandler = window.onerror

  window.onerror = (message, source, lineno, colno, error) => {
    if (!hasError.value) {
      hasError.value = true
      error.value = error || new Error(message)
      errorInfo.value = { source, lineno, colno }

      if (props.logErrors) {
        console.error('❌ Global error caught:', message, error)
      }

      emit('error', { error: error.value })
    }

    // Call original handler if it exists
    if (originalErrorHandler) {
      return originalErrorHandler(message, source, lineno, colno, error)
    }

    return false
  }
}

async function handleRetry() {
  retrying.value = true

  try {
    if (props.onRetry) {
      await props.onRetry()
    }

    // Reset error state
    hasError.value = false
    error.value = null
    errorInfo.value = null
    detailsExpanded.value = false

    emit('retry')
  } catch (err) {
    console.error('❌ Retry failed:', err)
  } finally {
    retrying.value = false
  }
}

function handleReload() {
  window.location.reload()
}

function handleReset() {
  if (props.onReset) {
    props.onReset()
  }

  // Reset error state
  hasError.value = false
  error.value = null
  errorInfo.value = null
  detailsExpanded.value = false

  emit('reset')
}
</script>

<style scoped>
.error-boundary-fallback {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: linear-gradient(135deg, rgba(30, 30, 30, 0.95) 0%, rgba(20, 20, 20, 0.95) 100%);
  border-radius: 12px;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.error-content {
  max-width: 600px;
  text-align: center;
}

.error-icon {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
}

.error-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.75rem;
}

.error-message {
  color: #d1d5db;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.error-details {
  margin: 1.5rem 0;
  text-align: left;
}

.error-details-toggle {
  display: inline-flex;
  align-items: center;
  color: #60a5fa;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  font-size: 0.875rem;
  transition: color 0.2s;
}

.error-details-toggle:hover {
  color: #93c5fd;
}

.error-details-content {
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  max-height: 300px;
  overflow-y: auto;
}

.error-details-content pre {
  margin: 0;
  font-size: 0.75rem;
  color: #e5e7eb;
  white-space: pre-wrap;
  word-break: break-word;
}

.error-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.error-support {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.rotate-180 {
  transform: rotate(180deg);
}
</style>
