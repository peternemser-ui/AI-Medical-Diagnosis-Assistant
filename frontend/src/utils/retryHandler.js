/**
 * Retry Handler Utility
 *
 * Wraps async operations with configurable retry logic.
 * Non-intrusive — used by wrapping existing calls, not replacing them.
 */

export async function withRetry(fn, options = {}) {
  const { maxRetries = 3, baseDelay = 1000, backoffFactor = 2, onRetry = null } = options

  let lastError
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn()
    } catch (err) {
      lastError = err
      if (attempt < maxRetries) {
        const delay = baseDelay * Math.pow(backoffFactor, attempt)
        if (onRetry) onRetry(attempt + 1, maxRetries, delay, err)
        await new Promise(r => setTimeout(r, delay))
      }
    }
  }
  throw lastError
}

export function createRetryWrapper(fn, options = {}) {
  return (...args) => withRetry(() => fn(...args), options)
}
