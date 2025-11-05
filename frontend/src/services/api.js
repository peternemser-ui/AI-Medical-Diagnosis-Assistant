// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

/**
 * API Error Class
 */
class ApiError extends Error {
  constructor(message, status, details, isRetryable = false) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
    this.isRetryable = isRetryable
    this.timestamp = new Date().toISOString()
  }
}

/**
 * Rate Limiter Class
 */
class RateLimiter {
  constructor(maxRequests = 10, windowMs = 60000) {
    this.maxRequests = maxRequests
    this.windowMs = windowMs
    this.requests = []
  }

  canMakeRequest() {
    const now = Date.now()

    // Remove old requests outside the window
    this.requests = this.requests.filter(time => now - time < this.windowMs)

    return this.requests.length < this.maxRequests
  }

  recordRequest() {
    this.requests.push(Date.now())
  }

  getRemainingRequests() {
    const now = Date.now()
    this.requests = this.requests.filter(time => now - time < this.windowMs)
    return Math.max(0, this.maxRequests - this.requests.length)
  }

  getResetTime() {
    if (this.requests.length === 0) return 0
    const oldest = Math.min(...this.requests)
    return Math.max(0, this.windowMs - (Date.now() - oldest))
  }
}

// Global rate limiter instance
const rateLimiter = new RateLimiter(20, 60000) // 20 requests per minute

/**
 * Sleep helper
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

/**
 * Determine if error is retryable
 */
function isRetryableError(status, error) {
  // Retry on network errors
  if (!status || status === 0) return true

  // Retry on server errors (5xx)
  if (status >= 500 && status < 600) return true

  // Retry on rate limit (429)
  if (status === 429) return true

  // Retry on timeout
  if (error?.name === 'AbortError') return true

  return false
}

/**
 * Enhanced fetch with retry logic and rate limiting
 */
async function fetchWithErrorHandling(url, options = {}) {
  const {
    retries = 3,
    retryDelay = 1000,
    timeout = 30000,
    ...fetchOptions
  } = options

  // Check rate limit
  if (!rateLimiter.canMakeRequest()) {
    const resetTime = rateLimiter.getResetTime()
    throw new ApiError(
      `Rate limit exceeded. Please wait ${Math.ceil(resetTime / 1000)} seconds.`,
      429,
      { resetTime },
      false
    )
  }

  let lastError = null

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      // Create abort controller for timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), timeout)

      // Record request for rate limiting
      rateLimiter.recordRequest()

      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...fetchOptions.headers
        },
        signal: controller.signal,
        ...fetchOptions
      })

      clearTimeout(timeoutId)

      if (!response.ok) {
        let errorMessage = `Request failed with status ${response.status}`
        let errorDetails = null

        try {
          const errorData = await response.json()
          errorMessage = errorData.message || errorData.detail || errorMessage
          errorDetails = errorData
        } catch {
          errorMessage = response.statusText || errorMessage
        }

        const isRetryable = isRetryableError(response.status)
        const error = new ApiError(errorMessage, response.status, errorDetails, isRetryable)

        // If this is the last attempt or error is not retryable, throw
        if (attempt === retries || !isRetryable) {
          throw error
        }

        lastError = error
        console.warn(`⚠️ Request failed (attempt ${attempt + 1}/${retries + 1}):`, errorMessage)

        // Calculate delay with exponential backoff
        const delay = retryDelay * Math.pow(2, attempt)
        const jitter = Math.random() * 0.3 * delay
        await sleep(delay + jitter)
        continue
      }

      return await response.json()

    } catch (error) {
      if (error instanceof ApiError) {
        if (attempt === retries || !error.isRetryable) {
          throw error
        }
        lastError = error
      } else {
        // Network or other errors
        const isRetryable = error.name === 'AbortError' || error.message.includes('fetch')
        const apiError = new ApiError(
          error.name === 'AbortError'
            ? 'Request timeout - please try again'
            : error.message.includes('fetch')
              ? 'Network error - check your connection and ensure the backend is running'
              : error.message,
          0,
          { originalError: error.message },
          isRetryable
        )

        if (attempt === retries || !isRetryable) {
          throw apiError
        }

        lastError = apiError
      }

      console.warn(`⚠️ Request error (attempt ${attempt + 1}/${retries + 1}):`, error.message)

      // Wait before retry
      const delay = retryDelay * Math.pow(2, attempt)
      const jitter = Math.random() * 0.3 * delay
      await sleep(delay + jitter)
    }
  }

  // If we exhausted all retries, throw the last error
  throw lastError || new ApiError('Request failed after maximum retries', 0, null, false)
}

/**
 * Get API headers with authentication
 */
function getApiHeaders() {
  const headers = {
    'Content-Type': 'application/json'
  }

  // Try encrypted key first, fallback to unencrypted
  const apiKey = localStorage.getItem('_encrypted_api_key')
    ? null // Will be decrypted by encryption utility
    : localStorage.getItem('openai_api_key')

  if (apiKey) {
    headers['X-OpenAI-API-Key'] = apiKey
  }

  return headers
}

export async function diagnose(data, options = {}) {
  console.log('🩺 Sending diagnosis request:', data)

  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/diagnose`, {
    method: 'POST',
    headers: getApiHeaders(),
    body: JSON.stringify(data),
    timeout: 45000, // Longer timeout for AI processing
    retries: 2,
    ...options
  })

  console.log('✅ Diagnosis response received')
  return result
}

export async function generateQuestion(data, options = {}) {
  console.log('❓ Generating AI question based on:', data)

  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/generate-question`, {
    method: 'POST',
    headers: getApiHeaders(),
    body: JSON.stringify(data),
    timeout: 30000,
    retries: 2,
    ...options
  })

  console.log('✅ AI question generated')
  return result
}

export async function followup(data, options = {}) {
  console.log('💬 Sending followup request:', data)

  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/followup`, {
    method: 'POST',
    headers: getApiHeaders(),
    body: JSON.stringify(data),
    timeout: 30000,
    retries: 2,
    ...options
  })

  console.log('✅ Followup response received')
  return result
}

export async function healthCheck() {
  try {
    await fetchWithErrorHandling(`${API_BASE_URL}/health`, {
      timeout: 5000,
      retries: 1
    })
    return true
  } catch (error) {
    console.warn('⚠️ Health check failed:', error.message)
    return false
  }
}

/**
 * Get rate limit status
 */
export function getRateLimitStatus() {
  return {
    remaining: rateLimiter.getRemainingRequests(),
    resetTime: rateLimiter.getResetTime(),
    canMakeRequest: rateLimiter.canMakeRequest()
  }
}

/**
 * Reset rate limiter (useful for testing)
 */
export function resetRateLimit() {
  rateLimiter.requests = []
  console.log('✅ Rate limiter reset')
}

// Export classes and utilities
export { ApiError, RateLimiter }