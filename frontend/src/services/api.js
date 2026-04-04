import { getAccessToken, refreshToken as doRefresh } from './authService'
import { isUnlocked } from './cryptoService.js'
import { getEncryptedApiKey } from './encryptedStorage.js'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

// In-memory cache of decrypted API keys (cleared on logout with session key)
let _keyCache = { anthropic: null, openai: null, google: null, _loaded: false }

/**
 * Pre-load decrypted API keys into memory cache.
 * Called after login/key derivation so getAuthHeaders() can stay synchronous.
 */
export async function loadApiKeysToCache() {
  if (!isUnlocked()) return
  const [anthropic, openai, google] = await Promise.all([
    getEncryptedApiKey('anthropic'),
    getEncryptedApiKey('openai'),
    getEncryptedApiKey('google'),
  ])
  _keyCache = { anthropic, openai, google, _loaded: true }
}

/** Clear the in-memory API key cache (called on logout). */
export function clearApiKeyCache() {
  _keyCache = { anthropic: null, openai: null, google: null, _loaded: false }
}

class ApiError extends Error {
  constructor(message, status, details) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

function getAuthHeaders() {
  const headers = { 'Content-Type': 'application/json' }

  // JWT auth token
  const accessToken = getAccessToken()
  if (accessToken) {
    headers['Authorization'] = `Bearer ${accessToken}`
  }

  // Always send ALL available API keys so the backend can pick the right one
  // Try encrypted cache first, then plaintext localStorage fallback
  const anthropicKey = _keyCache.anthropic || localStorage.getItem('anthropic_api_key') || ''
  const openaiKey = _keyCache.openai || localStorage.getItem('openai_api_key') || ''
  const googleKey = _keyCache.google || localStorage.getItem('google_api_key') || ''

  if (anthropicKey) headers['X-Anthropic-API-Key'] = anthropicKey
  if (openaiKey) headers['X-OpenAI-API-Key'] = openaiKey
  if (googleKey) headers['X-Google-API-Key'] = googleKey

  // Debug: log when no keys are being sent (helps diagnose routing issues)
  if (!anthropicKey && !openaiKey && !googleKey) {
    console.warn('[API] No API keys available in headers — backend will fall back to Ollama or return error')
  }

  return headers
}

async function fetchWithErrorHandling(url, options = {}, _retried = false) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    })

    // Auto-refresh on 401 and retry once
    if (response.status === 401 && !_retried) {
      const newToken = await doRefresh()
      if (newToken) {
        const retryHeaders = { ...options.headers }
        retryHeaders['Authorization'] = `Bearer ${newToken}`
        return fetchWithErrorHandling(url, { ...options, headers: retryHeaders }, true)
      }
    }

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

      throw new ApiError(errorMessage, response.status, errorDetails)
    }

    return await response.json()
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }

    throw new ApiError(
      error.message.includes('fetch') ? 'Network error - check if backend is running' : error.message,
      0,
      { originalError: error.message }
    )
  }
}

export async function validateApiKeys() {
  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/validate-key`, {
    method: 'POST',
    headers: getAuthHeaders(),
  })
  return result
}

export async function diagnose(data) {
  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/diagnose`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  })

  return result
}

export async function diagnoseStream(data, onEvent) {
  const headers = getAuthHeaders()

  const response = await fetch(`${API_BASE_URL}/api/diagnose/stream`, {
    method: 'POST',
    headers,
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`
    try {
      const errorData = await response.json()
      errorMessage = errorData.message || errorData.detail || errorMessage
    } catch {
      errorMessage = response.statusText || errorMessage
    }
    throw new ApiError(errorMessage, response.status)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  let finalResult = null

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })

    // Parse SSE events from buffer
    const lines = buffer.split('\n')
    buffer = ''

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]

      if (line.startsWith('data: ')) {
        const jsonStr = line.slice(6).trim()
        if (!jsonStr) continue

        try {
          const parsed = JSON.parse(jsonStr)
          onEvent(parsed)

          if (parsed.event === 'complete') {
            finalResult = parsed.result
          } else if (parsed.event === 'error') {
            throw new ApiError(parsed.message || 'Diagnosis pipeline error', 0)
          }
        } catch (e) {
          if (e instanceof ApiError) throw e
          // Incomplete JSON - put it back into buffer
          buffer = lines.slice(i).join('\n')
          break
        }
      } else if (line !== '') {
        // Non-data line or partial line, keep in buffer
        buffer += line + '\n'
      }
    }
  }

  if (!finalResult) {
    throw new ApiError('Stream ended without a complete event', 0)
  }

  return finalResult
}

export async function interview(data) {
  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/interview`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  })
  return result
}

export async function generateQuestion(data) {
  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/generate-question`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  })

  return result
}

export async function followup(data) {
  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/followup`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  })

  return result
}

export async function getAgentInfo() {
  return await fetchWithErrorHandling(`${API_BASE_URL}/api/agents`)
}

export async function healthCheck() {
  try {
    await fetchWithErrorHandling(`${API_BASE_URL}/health`)
    return true
  } catch {
    return false
  }
}

export { ApiError, API_BASE_URL }
