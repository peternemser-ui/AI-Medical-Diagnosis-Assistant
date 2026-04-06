/**
 * Admin API service — fetch wrappers for /api/admin/* endpoints
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

async function adminFetch(url, options = {}) {
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

// Existing
export const getOverview = () => adminFetch('/api/admin/overview')
export const getAgents = () => adminFetch('/api/admin/agents')
export const getAgent = (name) => adminFetch(`/api/admin/agents/${name}`)
export const controlAgent = (name, action) => adminFetch(`/api/admin/agents/${name}/control`, { method: 'POST', body: JSON.stringify({ action }) })
export const getCases = (params = {}) => { const q = new URLSearchParams(Object.entries(params).filter(([,v]) => v)).toString(); return adminFetch(`/api/admin/cases${q ? '?' + q : ''}`) }
export const getCase = (caseId) => adminFetch(`/api/admin/cases/${caseId}`)
export const getAlerts = (limit = 50) => adminFetch(`/api/admin/alerts?limit=${limit}`)

// NEW endpoints
export const getCaseCounts = () => adminFetch('/api/admin/cases/counts')
export const getCaseTimeline = (caseId) => adminFetch(`/api/admin/cases/${caseId}/timeline`)

export const getAgentDetail = (name) => adminFetch(`/api/admin/agents/${name}/detail`)
export const getAgentExecutions = (name, limit = 50) => adminFetch(`/api/admin/agents/${name}/executions?limit=${limit}`)

export const getLogs = (params = {}) => { const q = new URLSearchParams(Object.entries(params).filter(([,v]) => v != null && v !== '')).toString(); return adminFetch(`/api/admin/logs${q ? '?' + q : ''}`) }

export const getConfig = () => adminFetch('/api/admin/config')
export const updateConfig = (key, value) => adminFetch(`/api/admin/config/${key}`, { method: 'PUT', body: JSON.stringify({ value }) })

export const getReports = (params = {}) => { const q = new URLSearchParams(Object.entries(params).filter(([,v]) => v != null && v !== '')).toString(); return adminFetch(`/api/admin/reports${q ? '?' + q : ''}`) }
export const regenerateReport = (reportId) => adminFetch(`/api/admin/reports/${reportId}/regenerate`, { method: 'POST' })

export const getReviews = (params = {}) => { const q = new URLSearchParams(Object.entries(params).filter(([,v]) => v != null && v !== '')).toString(); return adminFetch(`/api/admin/reviews${q ? '?' + q : ''}`) }
export const reviewAction = (reviewId, action, notes = null) => adminFetch(`/api/admin/reviews/${reviewId}/action`, { method: 'POST', body: JSON.stringify({ action, notes }) })

export const getAnalytics = (period = '24h') => adminFetch(`/api/admin/analytics?period=${period}`)

// SEO & Marketing
export const getSeoAudit = () => adminFetch('/api/admin/seo/audit')
export const getSeoMeta = (page) => adminFetch(`/api/admin/seo/meta/${page}`)
export const getBlogIdeas = () => adminFetch('/api/admin/seo/blog-ideas', { method: 'POST' })
export const getSocialShare = (data) => adminFetch('/api/admin/seo/social-share', { method: 'POST', body: JSON.stringify(data) })
export const getLandingPageCopy = (specialty) => adminFetch(`/api/admin/seo/landing/${specialty}`)

// Billing (Admin)
export const getBillingSummary = () => adminFetch('/api/admin/billing/summary')
export const getBillingUsage = () => adminFetch('/api/admin/billing/usage')

// Billing (Public)
export const getPlans = () => fetch(`${API_BASE_URL}/api/billing/plans`).then(r => r.json())
export const getUserUsage = (userId = 'user-001') => fetch(`${API_BASE_URL}/api/billing/usage?user_id=${userId}`).then(r => r.json())
export const createCheckout = (userId, tier) => fetch(`${API_BASE_URL}/api/billing/checkout`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ user_id: userId, tier }) }).then(r => r.json())

// Model Comparison
export const getAvailableModels = () => adminFetch('/api/admin/models')
export const runModelComparison = (data) => adminFetch('/api/admin/compare', { method: 'POST', body: JSON.stringify(data) })
export const getComparisons = (limit = 20) => adminFetch(`/api/admin/comparisons?limit=${limit}`)
export const getComparison = (id) => adminFetch(`/api/admin/comparisons/${id}`)

// Quality Audit / Improve
export const runQualityAudit = () => adminFetch('/api/admin/audit', { method: 'POST' })
export const getLatestAudit = () => adminFetch('/api/admin/audit/latest')

// Stripe Configuration
export const getStripeStatus = () => adminFetch('/api/admin/stripe/status')
export const saveStripeConfig = (secretKey, webhookSecret) => adminFetch('/api/admin/stripe/config', { method: 'POST', body: JSON.stringify({ secret_key: secretKey, webhook_secret: webhookSecret }) })
export const testStripeConnection = (secretKey) => adminFetch('/api/admin/stripe/config', { method: 'POST', body: JSON.stringify({ secret_key: secretKey, webhook_secret: '' }) })
