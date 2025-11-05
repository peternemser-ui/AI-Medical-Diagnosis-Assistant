import { ref } from 'vue'

/**
 * Retry Logic Composable
 * Implements exponential backoff retry strategy
 */
export function useRetry() {
  const retryCount = ref(0)
  const maxRetries = ref(3)
  const isRetrying = ref(false)
  const lastError = ref(null)

  /**
   * Execute function with exponential backoff retry
   * @param {Function} fn - Function to execute
   * @param {Object} options - Retry options
   * @returns {Promise} - Result of function execution
   */
  async function withRetry(fn, options = {}) {
    const {
      maxAttempts = maxRetries.value,
      baseDelay = 1000,
      maxDelay = 30000,
      backoffMultiplier = 2,
      shouldRetry = (error) => true,
      onRetry = (attempt, error) => {},
      onSuccess = (result) => {},
      onFailure = (error) => {}
    } = options

    retryCount.value = 0
    isRetrying.value = true
    lastError.value = null

    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        console.log(`🔄 Attempt ${attempt}/${maxAttempts}`)

        const result = await fn()

        // Success
        retryCount.value = attempt
        isRetrying.value = false
        lastError.value = null

        console.log(`✅ Success on attempt ${attempt}`)
        onSuccess(result)

        return result
      } catch (error) {
        retryCount.value = attempt
        lastError.value = error

        console.error(`❌ Attempt ${attempt} failed:`, error.message)

        // Check if we should retry
        if (attempt === maxAttempts || !shouldRetry(error)) {
          isRetrying.value = false
          console.error(`💥 All retry attempts exhausted`)
          onFailure(error)
          throw error
        }

        // Calculate delay with exponential backoff
        const delay = Math.min(
          baseDelay * Math.pow(backoffMultiplier, attempt - 1),
          maxDelay
        )

        // Add jitter (randomness) to prevent thundering herd
        const jitter = Math.random() * 0.3 * delay
        const totalDelay = delay + jitter

        console.log(`⏳ Waiting ${Math.round(totalDelay)}ms before retry...`)

        // Call retry callback
        onRetry(attempt, error)

        // Wait before next attempt
        await sleep(totalDelay)
      }
    }
  }

  /**
   * Execute with simple retry (no exponential backoff)
   */
  async function withSimpleRetry(fn, attempts = 3, delay = 1000) {
    return withRetry(fn, {
      maxAttempts: attempts,
      baseDelay: delay,
      backoffMultiplier: 1
    })
  }

  /**
   * Execute with aggressive retry (fast retries)
   */
  async function withAggressiveRetry(fn, attempts = 5) {
    return withRetry(fn, {
      maxAttempts: attempts,
      baseDelay: 500,
      maxDelay: 5000,
      backoffMultiplier: 1.5
    })
  }

  /**
   * Execute with conservative retry (slow retries)
   */
  async function withConservativeRetry(fn, attempts = 3) {
    return withRetry(fn, {
      maxAttempts: attempts,
      baseDelay: 3000,
      maxDelay: 60000,
      backoffMultiplier: 3
    })
  }

  /**
   * Reset retry state
   */
  function reset() {
    retryCount.value = 0
    isRetrying.value = false
    lastError.value = null
  }

  return {
    // State
    retryCount,
    maxRetries,
    isRetrying,
    lastError,

    // Methods
    withRetry,
    withSimpleRetry,
    withAggressiveRetry,
    withConservativeRetry,
    reset
  }
}

/**
 * Helper: Sleep function
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Retry strategies for common error types
 */
export const RetryStrategies = {
  // Network errors - retry aggressively
  NETWORK: {
    shouldRetry: (error) => {
      return error.message?.includes('network') ||
             error.message?.includes('fetch') ||
             error.code === 'ECONNREFUSED'
    },
    maxAttempts: 5,
    baseDelay: 500,
    backoffMultiplier: 2
  },

  // Timeout errors - retry conservatively
  TIMEOUT: {
    shouldRetry: (error) => {
      return error.message?.includes('timeout') ||
             error.code === 'ETIMEDOUT'
    },
    maxAttempts: 3,
    baseDelay: 3000,
    backoffMultiplier: 2
  },

  // Rate limit errors - retry with backoff
  RATE_LIMIT: {
    shouldRetry: (error) => {
      return error.status === 429 ||
             error.message?.includes('rate limit')
    },
    maxAttempts: 4,
    baseDelay: 5000,
    backoffMultiplier: 3
  },

  // Server errors (5xx) - retry moderately
  SERVER_ERROR: {
    shouldRetry: (error) => {
      return error.status >= 500 && error.status < 600
    },
    maxAttempts: 3,
    baseDelay: 2000,
    backoffMultiplier: 2
  },

  // Don't retry client errors (4xx except 429)
  NO_RETRY: {
    shouldRetry: () => false,
    maxAttempts: 1
  }
}
