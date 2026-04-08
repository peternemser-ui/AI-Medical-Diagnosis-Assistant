import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import {
  getOverview,
  getAgents,
  getAgent,
  controlAgent,
  getCases,
  getCase,
  getCaseCounts,
  getCaseTimeline,
  getAgentDetail,
  getAgentExecutions,
  getLogs,
  getConfig,
  updateConfig,
  getReports,
  regenerateReport,
  getReviews,
  reviewAction,
  getAnalytics,
  getAlerts,
} from '@/services/adminApi.js'

describe('adminApi service', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({}),
        }),
      ),
    )
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  // ---- Simple GET endpoints ----

  it('getOverview calls correct URL', async () => {
    await getOverview()
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/overview',
      expect.objectContaining({ headers: expect.objectContaining({ 'Content-Type': 'application/json' }) }),
    )
  })

  it('getAgents calls correct URL', async () => {
    await getAgents()
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/agents',
      expect.objectContaining({ headers: expect.any(Object) }),
    )
  })

  it('getAgent calls correct URL with name param', async () => {
    await getAgent('triage')
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/agents/triage',
      expect.objectContaining({ headers: expect.any(Object) }),
    )
  })

  it('controlAgent sends POST with action body', async () => {
    await controlAgent('triage', 'restart')
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/agents/triage/control',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ action: 'restart' }),
      }),
    )
  })

  // ---- Cases ----

  it('getCases passes query params correctly', async () => {
    await getCases({ status: 'active', page: '2' })
    const url = fetch.mock.calls[0][0]
    expect(url).toContain('/api/admin/cases')
    expect(url).toContain('status=active')
    expect(url).toContain('page=2')
  })

  it('getCases filters empty params', async () => {
    await getCases({ status: '', page: '' })
    const url = fetch.mock.calls[0][0]
    expect(url).toBe('/api/admin/cases')
  })

  it('getCase calls correct URL with ID', async () => {
    await getCase('abc-123')
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/cases/abc-123',
      expect.objectContaining({ headers: expect.any(Object) }),
    )
  })

  it('getCaseCounts calls correct URL', async () => {
    await getCaseCounts()
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/cases/counts',
      expect.objectContaining({ headers: expect.any(Object) }),
    )
  })

  it('getCaseTimeline calls correct URL', async () => {
    await getCaseTimeline('abc-123')
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/cases/abc-123/timeline',
      expect.objectContaining({ headers: expect.any(Object) }),
    )
  })

  // ---- Agent detail / executions ----

  it('getAgentDetail calls correct URL', async () => {
    await getAgentDetail('diagnostician')
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/agents/diagnostician/detail',
      expect.objectContaining({ headers: expect.any(Object) }),
    )
  })

  it('getAgentExecutions calls correct URL with limit', async () => {
    await getAgentExecutions('diagnostician', 25)
    const url = fetch.mock.calls[0][0]
    expect(url).toBe('/api/admin/agents/diagnostician/executions?limit=25')
  })

  // ---- Logs ----

  it('getLogs passes filter params', async () => {
    await getLogs({ level: 'error', agent: 'triage', search: 'timeout' })
    const url = fetch.mock.calls[0][0]
    expect(url).toContain('/api/admin/logs')
    expect(url).toContain('level=error')
    expect(url).toContain('agent=triage')
    expect(url).toContain('search=timeout')
  })

  it('getLogs filters null/empty params', async () => {
    await getLogs({ level: null, agent: '', search: 'test' })
    const url = fetch.mock.calls[0][0]
    expect(url).toContain('search=test')
    expect(url).not.toContain('level')
    expect(url).not.toContain('agent')
  })

  // ---- Config ----

  it('getConfig calls correct URL', async () => {
    await getConfig()
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/config',
      expect.objectContaining({ headers: expect.any(Object) }),
    )
  })

  it('updateConfig sends PUT with value body', async () => {
    await updateConfig('max_tokens', 4096)
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/config/max_tokens',
      expect.objectContaining({
        method: 'PUT',
        body: JSON.stringify({ value: 4096 }),
      }),
    )
  })

  // ---- Reports ----

  it('getReports passes query params', async () => {
    await getReports({ status: 'completed', page: '1' })
    const url = fetch.mock.calls[0][0]
    expect(url).toContain('/api/admin/reports')
    expect(url).toContain('status=completed')
    expect(url).toContain('page=1')
  })

  it('regenerateReport sends POST', async () => {
    await regenerateReport('rpt-42')
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/reports/rpt-42/regenerate',
      expect.objectContaining({ method: 'POST' }),
    )
  })

  // ---- Reviews ----

  it('getReviews passes filter params', async () => {
    await getReviews({ status: 'pending', priority: 'high' })
    const url = fetch.mock.calls[0][0]
    expect(url).toContain('/api/admin/reviews')
    expect(url).toContain('status=pending')
    expect(url).toContain('priority=high')
  })

  it('reviewAction sends POST with action and notes', async () => {
    await reviewAction('rev-1', 'approve', 'Looks good')
    expect(fetch).toHaveBeenCalledWith(
      '/api/admin/reviews/rev-1/action',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify({ action: 'approve', notes: 'Looks good' }),
      }),
    )
  })

  // ---- Analytics ----

  it('getAnalytics passes period param', async () => {
    await getAnalytics('7d')
    const url = fetch.mock.calls[0][0]
    expect(url).toBe('/api/admin/analytics?period=7d')
  })

  // ---- Alerts ----

  it('getAlerts passes limit param', async () => {
    await getAlerts(10)
    const url = fetch.mock.calls[0][0]
    expect(url).toBe('/api/admin/alerts?limit=10')
  })

  // ---- Error handling ----

  it('throws on non-ok response', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
      json: () => Promise.reject(new Error('parse fail')),
    })

    await expect(getOverview()).rejects.toThrow('Internal Server Error')
  })

  it('parses detail from error response', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 403,
      statusText: 'Forbidden',
      json: () => Promise.resolve({ detail: 'Access denied' }),
    })

    await expect(getOverview()).rejects.toThrow('Access denied')
  })
})
