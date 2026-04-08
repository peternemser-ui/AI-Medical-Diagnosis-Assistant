/**
 * Medication Management API service — fetch wrappers for /api/medications/* endpoints
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

function getApiKeyHeaders() {
  const headers = {}
  const anthropicKey = localStorage.getItem('anthropic_api_key')
  const openaiKey = localStorage.getItem('openai_api_key')
  const googleKey = localStorage.getItem('google_api_key')
  if (anthropicKey) headers['X-Anthropic-API-Key'] = anthropicKey
  if (openaiKey) headers['X-OpenAI-API-Key'] = openaiKey
  if (googleKey) headers['X-Google-API-Key'] = googleKey
  return headers
}

async function medFetch(url, options = {}) {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    headers: { 'Content-Type': 'application/json', ...getApiKeyHeaders(), ...options.headers },
    ...options,
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(error.detail || `Request failed: ${response.status}`)
  }
  return response.json()
}

// Medications CRUD
export const getMedications = () => medFetch('/api/medications')
export const addMedication = (data) => medFetch('/api/medications', { method: 'POST', body: JSON.stringify(data) })
export const updateMedication = (id, data) => medFetch(`/api/medications/${id}`, { method: 'PUT', body: JSON.stringify(data) })
export const deleteMedication = (id) => medFetch(`/api/medications/${id}`, { method: 'DELETE' })

// Interactions
export const checkInteractions = (medications) => medFetch('/api/medications/interactions', { method: 'POST', body: JSON.stringify({ medications }) })
export const getFoodInteractions = (medications) => medFetch('/api/medications/food-interactions', { method: 'POST', body: JSON.stringify({ medications }) })

// Medication Guide
export const getMedicationGuide = (id) => medFetch(`/api/medications/${id}/guide`)

// Prescription scanning
export const scanPrescription = (imageBase64) => medFetch('/api/medications/scan-prescription', { method: 'POST', body: JSON.stringify({ image: imageBase64 }) })

// Adherence tracking
export const logAdherence = (data) => medFetch('/api/medications/adherence', { method: 'POST', body: JSON.stringify(data) })
export const getAdherenceHistory = () => medFetch('/api/medications/adherence')

// Side effects
export const reportSideEffect = (data) => medFetch('/api/medications/side-effects', { method: 'POST', body: JSON.stringify(data) })
export const getSideEffects = () => medFetch('/api/medications/side-effects')
export const analyzeSideEffects = () => medFetch('/api/medications/side-effects/analyze', { method: 'POST' })

// Schedule & Reminders
export const getSchedule = () => medFetch('/api/medications/schedule')
export const getReminders = () => medFetch('/api/medications/reminders')
export const addReminder = (data) => medFetch('/api/medications/reminders', { method: 'POST', body: JSON.stringify(data) })
export const deleteReminder = (id) => medFetch(`/api/medications/reminders/${id}`, { method: 'DELETE' })

// Pill Identifier
export const identifyPill = (imageBase64) => medFetch('/api/medications/identify-pill', { method: 'POST', body: JSON.stringify({ image: imageBase64 }) })

// Search & Refills
export const searchMedications = (query) => medFetch(`/api/medications/search?q=${encodeURIComponent(query)}`)
export const getUpcomingRefills = () => medFetch('/api/medications/refills')
