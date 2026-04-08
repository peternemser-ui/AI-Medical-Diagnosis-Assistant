import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import {
  trackPageView,
  trackEvent,
  getAnalyticsSummary,
  clearAnalytics,
} from '@/composables/useAnalytics.js'

// ── Helpers ──────────────────────────────────────────────────────────────────

const STORAGE_KEY = 'app_analytics'

function storedData() {
  const raw = localStorage.getItem(STORAGE_KEY)
  return raw ? JSON.parse(raw) : null
}

// ── Setup / Teardown ─────────────────────────────────────────────────────────

beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  localStorage.clear()
  vi.restoreAllMocks()
})

// ── trackPageView ─────────────────────────────────────────────────────────────

describe('trackPageView', () => {
  it('increments pageViews for a given path', () => {
    trackPageView('/dashboard')
    trackPageView('/dashboard')
    trackPageView('/dashboard')

    const data = storedData()
    expect(data.pageViews['/dashboard']).toBe(3)
  })

  it('tracks multiple paths independently', () => {
    trackPageView('/home')
    trackPageView('/settings')
    trackPageView('/home')

    const data = storedData()
    expect(data.pageViews['/home']).toBe(2)
    expect(data.pageViews['/settings']).toBe(1)
  })

  it('increments totalPageViews on each call', () => {
    trackPageView('/a')
    trackPageView('/b')
    trackPageView('/a')

    expect(storedData().totalPageViews).toBe(3)
  })

  it('does nothing when path is falsy', () => {
    trackPageView('')
    trackPageView(null)
    trackPageView(undefined)

    expect(storedData()).toBeNull()
  })

  it('persists data across separate calls', () => {
    trackPageView('/x')
    // simulate a second "session" read from storage
    trackPageView('/x')

    expect(storedData().pageViews['/x']).toBe(2)
  })
})

// ── trackEvent ────────────────────────────────────────────────────────────────

describe('trackEvent', () => {
  it('stores an event under category:action key', () => {
    trackEvent('consultation', 'started')

    const data = storedData()
    expect(data.events['consultation:started']).toBe(1)
  })

  it('increments the same event key on repeated calls', () => {
    trackEvent('report', 'generated')
    trackEvent('report', 'generated')
    trackEvent('report', 'generated')

    expect(storedData().events['report:generated']).toBe(3)
  })

  it('increments totalEvents on each call', () => {
    trackEvent('a', 'b')
    trackEvent('c', 'd')

    expect(storedData().totalEvents).toBe(2)
  })

  it('stores optional label in eventLabels', () => {
    trackEvent('feature', 'used', 'dark-mode')

    const data = storedData()
    expect(data.eventLabels['feature:used:dark-mode']).toBe(1)
  })

  it('does not write eventLabels when label is omitted', () => {
    trackEvent('x', 'y')

    const data = storedData()
    expect(Object.keys(data.eventLabels)).toHaveLength(0)
  })

  it('does nothing when category is falsy', () => {
    trackEvent('', 'action')
    trackEvent(null, 'action')

    expect(storedData()).toBeNull()
  })

  it('does nothing when action is falsy', () => {
    trackEvent('category', '')
    trackEvent('category', undefined)

    expect(storedData()).toBeNull()
  })
})

// ── getAnalyticsSummary ───────────────────────────────────────────────────────

describe('getAnalyticsSummary', () => {
  it('returns zero totals when no data has been tracked', () => {
    const summary = getAnalyticsSummary()

    expect(summary.totalPageViews).toBe(0)
    expect(summary.totalEvents).toBe(0)
    expect(summary.topPages).toHaveLength(0)
    expect(summary.recentEvents).toHaveLength(0)
  })

  it('returns correct totals after tracking', () => {
    trackPageView('/home')
    trackPageView('/home')
    trackEvent('report', 'generated')

    const summary = getAnalyticsSummary()
    expect(summary.totalPageViews).toBe(2)
    expect(summary.totalEvents).toBe(1)
  })

  it('topPages is sorted by count descending', () => {
    trackPageView('/a')
    trackPageView('/b')
    trackPageView('/b')
    trackPageView('/b')
    trackPageView('/a')

    const { topPages } = getAnalyticsSummary()
    expect(topPages[0].path).toBe('/b')
    expect(topPages[0].count).toBe(3)
    expect(topPages[1].path).toBe('/a')
  })

  it('recentEvents is sorted by count descending', () => {
    trackEvent('cat', 'rare')
    trackEvent('cat', 'common')
    trackEvent('cat', 'common')
    trackEvent('cat', 'common')

    const { recentEvents } = getAnalyticsSummary()
    expect(recentEvents[0].key).toBe('cat:common')
    expect(recentEvents[0].count).toBe(3)
  })

  it('maps known paths to friendly names', () => {
    trackPageView('/')
    trackPageView('/settings')

    const { topPages } = getAnalyticsSummary()
    const home = topPages.find(p => p.path === '/')
    const settings = topPages.find(p => p.path === '/settings')

    expect(home.name).toBe('Home')
    expect(settings.name).toBe('Settings')
  })

  it('leaves unknown paths as-is', () => {
    trackPageView('/unknown-feature')

    const { topPages } = getAnalyticsSummary()
    expect(topPages[0].name).toBe('/unknown-feature')
  })

  it('limits topPages to 5 entries', () => {
    for (let i = 0; i < 10; i++) trackPageView(`/page-${i}`)

    const { topPages } = getAnalyticsSummary()
    expect(topPages.length).toBeLessThanOrEqual(5)
  })
})

// ── clearAnalytics ────────────────────────────────────────────────────────────

describe('clearAnalytics', () => {
  it('removes all analytics data from localStorage', () => {
    trackPageView('/home')
    trackEvent('test', 'action')

    clearAnalytics()

    expect(storedData()).toBeNull()
  })

  it('after clearing, tracking starts fresh', () => {
    trackPageView('/home')
    trackPageView('/home')
    clearAnalytics()
    trackPageView('/home')

    expect(storedData().pageViews['/home']).toBe(1)
    expect(storedData().totalPageViews).toBe(1)
  })

  it('is idempotent — clearing when empty does not throw', () => {
    expect(() => clearAnalytics()).not.toThrow()
    expect(() => clearAnalytics()).not.toThrow()
  })
})
