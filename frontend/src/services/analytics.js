/**
 * Analytics Event Tracking
 *
 * Tracks user funnel: landing -> signup -> first diagnosis -> upgrade
 * Uses a simple localStorage-based system (replace with Mixpanel/Amplitude later)
 */

const EVENTS_KEY = 'analytics_events'

export function trackEvent(name, properties = {}) {
  const event = {
    name,
    properties,
    timestamp: new Date().toISOString(),
    sessionId: getSessionId(),
    userId: getUserId(),
  }

  // Store locally
  const events = JSON.parse(localStorage.getItem(EVENTS_KEY) || '[]')
  events.push(event)
  // Keep last 500 events
  if (events.length > 500) events.splice(0, events.length - 500)
  localStorage.setItem(EVENTS_KEY, JSON.stringify(events))

  // Log for development
  console.debug('[Analytics]', name, properties)

  // TODO: Send to backend analytics endpoint
  // fetch('/api/analytics/track', { method: 'POST', body: JSON.stringify(event) })
}

function getSessionId() {
  let id = sessionStorage.getItem('session_id')
  if (!id) {
    id = Math.random().toString(36).substr(2, 9)
    sessionStorage.setItem('session_id', id)
  }
  return id
}

function getUserId() {
  try {
    const auth = JSON.parse(localStorage.getItem('auth_user') || '{}')
    return auth.id || 'anonymous'
  } catch { return 'anonymous' }
}

export function getEvents() {
  return JSON.parse(localStorage.getItem(EVENTS_KEY) || '[]')
}

// Pre-defined event names
export const EVENTS = {
  PAGE_VIEW: 'page_view',
  SIGNUP: 'signup',
  LOGIN: 'login',
  FIRST_DIAGNOSIS: 'first_diagnosis',
  DIAGNOSIS_COMPLETE: 'diagnosis_complete',
  PHOTO_UPLOAD: 'photo_upload',
  PDF_DOWNLOAD: 'pdf_download',
  SPECIALIST_REFERRAL: 'specialist_referral',
  UPGRADE_PROMPT_SHOWN: 'upgrade_prompt_shown',
  UPGRADE_CLICKED: 'upgrade_clicked',
  PRICING_VIEWED: 'pricing_viewed',
}
