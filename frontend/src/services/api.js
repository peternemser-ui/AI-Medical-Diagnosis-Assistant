const API_BASE_URL = 'http://localhost:8002'

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

  // Send ALL available vendor keys — the backend resolves which to use
  const anthropicKey = localStorage.getItem('anthropic_api_key')
  const openaiKey = localStorage.getItem('openai_api_key')
  const googleKey = localStorage.getItem('google_api_key')

  if (anthropicKey) headers['X-Anthropic-API-Key'] = anthropicKey
  if (openaiKey) headers['X-OpenAI-API-Key'] = openaiKey
  if (googleKey) headers['X-Google-API-Key'] = googleKey

  // Primary key for backward compatibility
  if (anthropicKey) {
    headers['X-Anthropic-API-Key'] = anthropicKey
  } else if (openaiKey) {
    headers['X-OpenAI-API-Key'] = openaiKey
  }

  return headers
}

async function fetchWithErrorHandling(url, options = {}) {
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    })

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
  console.log('Sending multi-agent diagnosis request:', data)

  const result = await fetchWithErrorHandling(`${API_BASE_URL}/api/diagnose`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data)
  })

  console.log('Multi-agent diagnosis complete:', {
    agents: result.agents_used,
    time: result.total_time,
    multiAgent: result.multi_agent
  })
  return result
}

export async function diagnoseStream(data, onEvent) {
  console.log('Starting SSE streaming diagnosis request:', data)

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
          }
        } catch (e) {
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

  console.log('SSE streaming diagnosis complete:', {
    agents: finalResult.agents_used,
    time: finalResult.total_time,
    multiAgent: finalResult.multi_agent
  })

  return finalResult
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
  } catch (error) {
    console.warn('Health check failed:', error.message)
    return false
  }
}

export { ApiError }
