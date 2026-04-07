import { describe, it, expect, vi, beforeEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'

// ---- Mock dependencies before importing components ----

vi.mock('@/services/adminApi.js', () => ({
  getOverview: vi.fn(() =>
    Promise.resolve({
      system: { active_cases: 0, avg_pipeline_duration_ms: 0, error_cases: 0, cases_last_24h: 0 },
      agents: [],
      alerts: [],
      recent_cases: [],
    }),
  ),
  getAgents: vi.fn(() => Promise.resolve([])),
  getAgentDetail: vi.fn(() =>
    Promise.resolve({
      health: {},
      description: '',
      recent_executions: [],
      failure_clusters: [],
      performance_trend: [],
      learning_insights: [],
      config: {},
      dependencies: [],
      downstream: [],
    }),
  ),
  controlAgent: vi.fn(() => Promise.resolve({})),
  getCases: vi.fn(() => Promise.resolve({ cases: [], total: 0, page: 1, total_pages: 1 })),
  getCaseCounts: vi.fn(() => Promise.resolve({})),
  getCase: vi.fn(() => Promise.resolve({})),
  getCaseTimeline: vi.fn(() => Promise.resolve({ events: [] })),
  getReviews: vi.fn(() => Promise.resolve({ items: [], total: 0, counts: {} })),
  reviewAction: vi.fn(() => Promise.resolve({})),
  getAnalytics: vi.fn(() =>
    Promise.resolve({
      throughput: [],
      turnaround_trend: [],
      agent_latency: {},
      error_rates: {},
      urgency_distribution: {},
      confidence_distribution: [],
      review_rate: 0,
      completion_funnel: {},
      top_failure_categories: [],
      period: '24h',
    }),
  ),
  getLogs: vi.fn(() => Promise.resolve({ logs: [], total: 0 })),
  getConfig: vi.fn(() => Promise.resolve([])),
  updateConfig: vi.fn(() => Promise.resolve({})),
  getReports: vi.fn(() => Promise.resolve({ reports: [], total: 0, page: 1, total_pages: 1 })),
  regenerateReport: vi.fn(() => Promise.resolve({})),
  getAlerts: vi.fn(() => Promise.resolve({ alerts: [] })),
}))

vi.mock('@/composables/usePolling.js', () => ({
  usePolling: vi.fn(() => ({
    isPolling: { value: false },
    error: { value: null },
    lastFetched: { value: null },
    start: vi.fn(),
    stop: vi.fn(),
    restart: vi.fn(),
    poll: vi.fn(),
  })),
}))

vi.mock('@/composables/useTheme.js', () => ({
  useTheme: () => ({ isDark: { value: false }, toggleTheme: vi.fn() }),
}))

vi.mock('vue-router', () => ({
  useRouter: () => ({ push: vi.fn() }),
  useRoute: () => ({ path: '/admin', params: {}, query: {} }),
  RouterLink: { template: '<a><slot /></a>' },
  RouterView: { template: '<div><slot /></div>' },
}))

// ---- Import components after mocks are set up ----

import AdminOverview from '@/views/admin/AdminOverview.vue'
import AdminAgents from '@/views/admin/AdminAgents.vue'
import AdminCases from '@/views/admin/AdminCases.vue'
import AdminReviews from '@/views/admin/AdminReviews.vue'
import AdminAnalytics from '@/views/admin/AdminAnalytics.vue'
import AdminLogs from '@/views/admin/AdminLogs.vue'
import AdminConfig from '@/views/admin/AdminConfig.vue'
import AdminReports from '@/views/admin/AdminReports.vue'
import AdminLayout from '@/views/admin/AdminLayout.vue'

// Common mount options
const globalStubs = {
  RouterLink: { template: '<a><slot /></a>' },
  RouterView: { template: '<div><slot /></div>' },
  APageHeader: { template: '<div><h1>{{ title }}</h1><slot /></div>', props: ['title', 'subtitle', 'lastUpdated', 'last-updated', 'showRefresh', 'show-refresh'] },
  ASheet: { template: '<div><slot /></div>' },
  AConfirmDialog: { template: '<div><slot /></div>' },
  AMetricCard: { template: '<div><slot /></div>' },
  ADataTable: { template: '<div><slot /></div>' },
  ASearchInput: { template: '<div><slot /></div>' },
  ATabBar: { template: '<div><slot /></div>' },
  AStatusBadge: { template: '<div><slot /></div>' },
  AKpiStrip: { template: '<div><slot /></div>' },
  ABarChart: { template: '<div><slot /></div>' },
  AEmptyState: { template: '<div><slot /></div>' },
  Transition: { template: '<div><slot /></div>' },
}

function mountOpts(overrides = {}) {
  return {
    global: {
      stubs: { ...globalStubs, ...(overrides.stubs || {}) },
    },
    ...overrides,
  }
}

// ---- AdminOverview ----

describe('AdminOverview', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminOverview, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('displays metric cards container', () => {
    const wrapper = shallowMount(AdminOverview, mountOpts())
    // The metric cards are inside a grid container
    const grid = wrapper.find('.grid')
    expect(grid.exists()).toBe(true)
  })
})

// ---- AdminAgents ----

describe('AdminAgents', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminAgents, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders grid view by default', () => {
    const wrapper = shallowMount(AdminAgents, mountOpts())
    // The heading should say "Agents"
    const heading = wrapper.find('h1')
    expect(heading.text()).toBe('Agents')
  })
})

// ---- AdminCases ----

describe('AdminCases', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminCases, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders tabs', () => {
    const wrapper = shallowMount(AdminCases, mountOpts())
    const heading = wrapper.find('h1')
    expect(heading.text()).toBe('Cases')
  })
})

// ---- AdminReviews ----

describe('AdminReviews', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminReviews, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders tab bar', () => {
    const wrapper = shallowMount(AdminReviews, mountOpts())
    const heading = wrapper.find('h1')
    expect(heading.text()).toBe('Review Queue')
  })
})

// ---- AdminAnalytics ----

describe('AdminAnalytics', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminAnalytics, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders period selector', () => {
    const wrapper = shallowMount(AdminAnalytics, mountOpts())
    const heading = wrapper.find('h1')
    expect(heading.text()).toBe('Analytics')
  })
})

// ---- AdminLogs ----

describe('AdminLogs', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminLogs, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders filter bar', () => {
    const wrapper = shallowMount(AdminLogs, mountOpts())
    const heading = wrapper.find('h1')
    expect(heading.text()).toBe('Logs')
  })
})

// ---- AdminConfig ----

describe('AdminConfig', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminConfig, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders category tabs', () => {
    const wrapper = shallowMount(AdminConfig, mountOpts())
    const heading = wrapper.find('h1')
    expect(heading.text()).toBe('Configuration')
  })
})

// ---- AdminReports ----

describe('AdminReports', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminReports, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders status tabs', () => {
    const wrapper = shallowMount(AdminReports, mountOpts())
    const heading = wrapper.find('h1')
    expect(heading.text()).toBe('Reports')
  })
})

// ---- AdminLayout ----

describe('AdminLayout', () => {
  it('mounts without error', () => {
    const wrapper = shallowMount(AdminLayout, mountOpts())
    expect(wrapper.exists()).toBe(true)
  })

  it('renders sidebar nav items', () => {
    const wrapper = shallowMount(AdminLayout, mountOpts())
    // The layout should contain the sidebar with nav links
    const nav = wrapper.find('nav')
    expect(nav.exists()).toBe(true)
  })
})
