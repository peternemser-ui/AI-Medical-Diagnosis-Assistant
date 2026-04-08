import { describe, it, expect, vi, beforeEach } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'

// ── Mocks (must precede component import) ─────────────────────────────────────

vi.mock('@/composables/useTheme.js', () => ({
  useTheme: () => ({
    isDark: { value: false },
    theme: { value: 'light' },
    setTheme: vi.fn(),
    toggleTheme: vi.fn(),
  }),
}))

vi.mock('@/composables/useI18n.js', () => ({
  useI18n: () => ({
    t: (key) => key,
    lang: { value: 'en' },
    setLang: vi.fn(),
    languages: [],
    currentLanguage: { value: { code: 'en', label: 'English' } },
  }),
}))

vi.mock('@/composables/useUser.js', () => ({
  useUser: () => ({
    profile: { value: { name: 'Test User', email: 'test@example.com' } },
    isLoggedIn: { value: false },
    logout: vi.fn(),
  }),
}))

// ── Component import after mocks ──────────────────────────────────────────────

import AppNav from '@/components/AppNav.vue'

// ── Router factory ────────────────────────────────────────────────────────────

function makeRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: { template: '<div/>' } },
      { path: '/consult', component: { template: '<div/>' } },
      { path: '/reports', component: { template: '<div/>' } },
      { path: '/medications', component: { template: '<div/>' } },
      { path: '/login', component: { template: '<div/>' } },
      { path: '/profile', component: { template: '<div/>' } },
    ],
  })
}

function mountNav(props = {}) {
  const router = makeRouter()
  return shallowMount(AppNav, {
    props,
    global: {
      plugins: [router],
      stubs: {
        ThemeLangControls: { template: '<div data-testid="theme-lang-controls" />' },
        RouterLink: {
          template: '<a :href="to"><slot /></a>',
          props: ['to'],
        },
      },
    },
  })
}

// ── Tests ─────────────────────────────────────────────────────────────────────

describe('AppNav', () => {
  describe('basic render', () => {
    it('mounts without error', () => {
      const wrapper = mountNav()
      expect(wrapper.exists()).toBe(true)
    })

    it('renders a <nav> element', () => {
      const wrapper = mountNav()
      expect(wrapper.find('nav').exists()).toBe(true)
    })

    it('nav element has role="navigation"', () => {
      const wrapper = mountNav()
      const nav = wrapper.find('nav')
      expect(nav.attributes('role')).toBe('navigation')
    })

    it('nav element has aria-label', () => {
      const wrapper = mountNav()
      const nav = wrapper.find('nav')
      expect(nav.attributes('aria-label')).toBeTruthy()
    })
  })

  describe('navigation links', () => {
    it('renders Consult link', () => {
      const wrapper = mountNav()
      const links = wrapper.findAll('a')
      const hrefs = links.map(l => l.attributes('href'))
      expect(hrefs).toContain('/consult')
    })

    it('renders Reports link', () => {
      const wrapper = mountNav()
      const links = wrapper.findAll('a')
      const hrefs = links.map(l => l.attributes('href'))
      expect(hrefs).toContain('/reports')
    })

    it('renders Medications link', () => {
      const wrapper = mountNav()
      const links = wrapper.findAll('a')
      const hrefs = links.map(l => l.attributes('href'))
      expect(hrefs).toContain('/medications')
    })

    it('renders a home / brand link pointing to /', () => {
      const wrapper = mountNav()
      const links = wrapper.findAll('a[href="/"]')
      expect(links.length).toBeGreaterThan(0)
    })
  })

  describe('mobile menu toggle', () => {
    it('mobile menu is hidden initially', () => {
      const wrapper = mountNav()
      // The mobile dropdown is conditionally rendered with v-if="showMobileMenu"
      const mobileMenu = wrapper.find('.absolute.top-full.left-0.right-0')
      expect(mobileMenu.exists()).toBe(false)
    })

    it('mobile hamburger button has aria-label', () => {
      const wrapper = mountNav()
      const buttons = wrapper.findAll('button')
      const hamburger = buttons.find(b => b.attributes('aria-label') === 'Toggle navigation menu')
      expect(hamburger).toBeDefined()
    })

    it('mobile hamburger button has aria-expanded="false" initially', () => {
      const wrapper = mountNav()
      const buttons = wrapper.findAll('button')
      const hamburger = buttons.find(b => b.attributes('aria-label') === 'Toggle navigation menu')
      expect(hamburger?.attributes('aria-expanded')).toBe('false')
    })

    it('clicking hamburger shows mobile menu', async () => {
      const wrapper = mountNav()
      const buttons = wrapper.findAll('button')
      const hamburger = buttons.find(b => b.attributes('aria-label') === 'Toggle navigation menu')
      await hamburger.trigger('click')
      const mobileMenu = wrapper.find('.absolute.top-full.left-0.right-0')
      expect(mobileMenu.exists()).toBe(true)
    })

    it('aria-expanded becomes true after clicking hamburger', async () => {
      const wrapper = mountNav()
      const buttons = wrapper.findAll('button')
      const hamburger = buttons.find(b => b.attributes('aria-label') === 'Toggle navigation menu')
      await hamburger.trigger('click')
      expect(hamburger.attributes('aria-expanded')).toBe('true')
    })

    it('clicking hamburger twice hides the menu again', async () => {
      const wrapper = mountNav()
      const buttons = wrapper.findAll('button')
      const hamburger = buttons.find(b => b.attributes('aria-label') === 'Toggle navigation menu')
      await hamburger.trigger('click')
      await hamburger.trigger('click')
      const mobileMenu = wrapper.find('.absolute.top-full.left-0.right-0')
      expect(mobileMenu.exists()).toBe(false)
    })
  })

  describe('"More" dropdown', () => {
    it('More button has aria-label', () => {
      const wrapper = mountNav()
      const moreBtn = wrapper.find('button[aria-label="More navigation options"]')
      expect(moreBtn.exists()).toBe(true)
    })

    it('More button has aria-expanded="false" initially', () => {
      const wrapper = mountNav()
      const moreBtn = wrapper.find('button[aria-label="More navigation options"]')
      expect(moreBtn.attributes('aria-expanded')).toBe('false')
    })

    it('clicking More button toggles aria-expanded', async () => {
      const wrapper = mountNav()
      const moreBtn = wrapper.find('button[aria-label="More navigation options"]')
      await moreBtn.trigger('click')
      expect(moreBtn.attributes('aria-expanded')).toBe('true')
    })
  })

  describe('theme lang controls', () => {
    it('renders ThemeLangControls component', () => {
      const wrapper = mountNav()
      expect(wrapper.find('[data-testid="theme-lang-controls"]').exists()).toBe(true)
    })
  })

  describe('currentPage prop', () => {
    it('accepts currentPage prop without error', () => {
      const wrapper = mountNav({ currentPage: 'consult' })
      expect(wrapper.exists()).toBe(true)
    })
  })
})
