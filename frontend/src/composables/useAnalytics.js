/**
 * useAnalytics — lightweight, privacy-respecting local analytics.
 * All data stays in localStorage. No external services, no tracking pixels.
 */

const STORAGE_KEY = 'app_analytics'

function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

function defaultData() {
  return {
    version: 1,
    startedAt: new Date().toISOString(),
    pageViews: {},        // { '/path': count }
    events: {},           // { 'category:action': count }
    eventLabels: {},      // { 'category:action:label': count }
    totalPageViews: 0,
    totalEvents: 0,
    lastUpdated: new Date().toISOString(),
  }
}

function saveData(data) {
  try {
    data.lastUpdated = new Date().toISOString()
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch {
    // localStorage might be full or unavailable — fail silently
  }
}

function getData() {
  return loadData() || defaultData()
}

// ── Public API ──────────────────────────────────────────────────────────────

/**
 * Track a page view for the given route path.
 * @param {string} path  e.g. '/dashboard', '/consultation'
 */
export function trackPageView(path) {
  if (!path) return
  const data = getData()
  data.pageViews[path] = (data.pageViews[path] || 0) + 1
  data.totalPageViews = (data.totalPageViews || 0) + 1
  saveData(data)
}

/**
 * Track a feature usage event.
 * @param {string} category  e.g. 'consultation', 'report', 'medication'
 * @param {string} action    e.g. 'started', 'generated', 'added'
 * @param {string} [label]   optional extra context
 */
export function trackEvent(category, action, label) {
  if (!category || !action) return
  const data = getData()
  const key = `${category}:${action}`
  data.events[key] = (data.events[key] || 0) + 1
  data.totalEvents = (data.totalEvents || 0) + 1
  if (label) {
    const labelKey = `${category}:${action}:${label}`
    data.eventLabels[labelKey] = (data.eventLabels[labelKey] || 0) + 1
  }
  saveData(data)
}

/**
 * Return a summary object suitable for display in the settings UI.
 */
export function getAnalyticsSummary() {
  const data = getData()

  // Sort pages by view count, most visited first
  const sortedPages = Object.entries(data.pageViews)
    .sort(([, a], [, b]) => b - a)
    .map(([path, count]) => ({ path, count }))

  // Sort events by count
  const sortedEvents = Object.entries(data.events)
    .sort(([, a], [, b]) => b - a)
    .map(([key, count]) => {
      const [category, action] = key.split(':')
      return { key, category, action, count }
    })

  const friendlyPageName = (path) => {
    const map = {
      '/': 'Home',
      '/consultation': 'Consultation',
      '/dashboard': 'Dashboard',
      '/settings': 'Settings',
      '/history': 'History',
      '/profile': 'Profile',
      '/help': 'Help',
      '/medications': 'Medications',
      '/admin': 'Admin',
    }
    return map[path] || path
  }

  return {
    totalPageViews: data.totalPageViews || 0,
    totalEvents: data.totalEvents || 0,
    startedAt: data.startedAt || null,
    lastUpdated: data.lastUpdated || null,
    topPages: sortedPages.slice(0, 5).map(p => ({
      ...p,
      name: friendlyPageName(p.path),
    })),
    recentEvents: sortedEvents.slice(0, 8),
  }
}

/**
 * Wipe all analytics data from localStorage.
 */
export function clearAnalytics() {
  localStorage.removeItem(STORAGE_KEY)
}

/**
 * Vue composable — call inside a component's setup() to get reactive helpers.
 */
export function useAnalytics() {
  return {
    trackPageView,
    trackEvent,
    getAnalyticsSummary,
    clearAnalytics,
  }
}
