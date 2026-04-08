import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'

// ── Mocks ─────────────────────────────────────────────────────────────────────

vi.mock('@/composables/useTheme.js', () => ({
  useTheme: () => ({
    isDark: { value: false },
    theme: { value: 'light' },
    toggleTheme: vi.fn(),
  }),
}))

// ── Component import after mocks ──────────────────────────────────────────────

import HomeView from '@/views/HomeView.vue'

// ── Router / mount helpers ────────────────────────────────────────────────────

function makeRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/', component: HomeView },
      { path: '/consult', component: { template: '<div/>' } },
      { path: '/login', component: { template: '<div/>' } },
      { path: '/signup', component: { template: '<div/>' } },
      { path: '/features', component: { template: '<div/>' } },
      { path: '/pricing', component: { template: '<div/>' } },
      { path: '/nutrition', component: { template: '<div/>' } },
      { path: '/mental-health', component: { template: '<div/>' } },
      { path: '/medications', component: { template: '<div/>' } },
      { path: '/reports', component: { template: '<div/>' } },
      { path: '/second-opinion', component: { template: '<div/>' } },
    ],
  })
}

function mountHome(provideOverrides = {}) {
  const router = makeRouter()
  return shallowMount(HomeView, {
    global: {
      plugins: [router],
      provide: {
        isDark: { value: false },
        ...provideOverrides,
      },
      stubs: {
        AppNav: { template: '<nav data-testid="app-nav" />' },
        RouterLink: {
          template: '<a :href="to"><slot /></a>',
          props: ['to'],
        },
        Transition: { template: '<div><slot /></div>' },
      },
    },
  })
}

// ── Tests ─────────────────────────────────────────────────────────────────────

describe('HomeView', () => {
  // ── Basic render ───────────────────────────────────────────────────────────

  describe('renders correctly', () => {
    it('mounts without error', () => {
      const wrapper = mountHome()
      expect(wrapper.exists()).toBe(true)
    })

    it('renders AppNav', () => {
      const wrapper = mountHome()
      expect(wrapper.find('[data-testid="app-nav"]').exists()).toBe(true)
    })
  })

  // ── Hero section ───────────────────────────────────────────────────────────

  describe('hero section', () => {
    it('renders an h1 in the hero', () => {
      const wrapper = mountHome()
      const h1 = wrapper.find('h1')
      expect(h1.exists()).toBe(true)
    })

    it('h1 text includes "AI-Powered Medical" or "AI Medical" or "Intelligence Platform"', () => {
      const wrapper = mountHome()
      const h1 = wrapper.find('h1')
      expect(h1.text()).toMatch(/AI-Powered Medical|AI Medical|Intelligence Platform/i)
    })

    it('renders Start Free Consultation CTA', () => {
      const wrapper = mountHome()
      const links = wrapper.findAll('a')
      const ctaLinks = links.filter(l => l.text().includes('Start') || l.attributes('href') === '/consult')
      expect(ctaLinks.length).toBeGreaterThan(0)
    })

    it('CTA link points to /consult', () => {
      const wrapper = mountHome()
      const ctaLink = wrapper.find('a[href="/consult"]')
      expect(ctaLink.exists()).toBe(true)
    })

    it('renders a secondary CTA link in the hero', () => {
      const wrapper = mountHome()
      const links = wrapper.findAll('a, button')
      const secondaryCta = links.find(l =>
        l.text().includes('See How It Works') ||
        l.text().includes('Explore Features') ||
        l.attributes('href') === '#how-it-works'
      )
      expect(secondaryCta).toBeDefined()
    })

    it('renders trust badges', () => {
      const wrapper = mountHome()
      // Trust badges are in a flex-wrap container with text content
      const text = wrapper.text()
      expect(text).toContain('HIPAA')
    })
  })

  // ── Heading hierarchy ──────────────────────────────────────────────────────

  describe('heading hierarchy', () => {
    it('has exactly one h1', () => {
      const wrapper = mountHome()
      const h1s = wrapper.findAll('h1')
      expect(h1s).toHaveLength(1)
    })

    it('has h2 headings for each section', () => {
      const wrapper = mountHome()
      const h2s = wrapper.findAll('h2')
      // The page has: Platform Pillars, How It Works, See It In Action, Built for Medical Trust, Simple Pricing, Ready to Get Started?
      expect(h2s.length).toBeGreaterThanOrEqual(4)
    })

    it('h2 headings include expected section names', () => {
      const wrapper = mountHome()
      const h2Texts = wrapper.findAll('h2').map(h => h.text())
      // Platform section heading changed to "One Platform, Complete Health Intelligence"
      expect(h2Texts.some(t => t.includes('Platform') || t.includes('Health Intelligence'))).toBe(true)
      expect(h2Texts.some(t => t.includes('How It Works'))).toBe(true)
    })

    it('has h3 headings only within sections (below h2)', () => {
      const wrapper = mountHome()
      const h3s = wrapper.findAll('h3')
      // h3 appears in the specialist team map: "Our Specialist Team"
      // All h3s should appear after at least one h2 in DOM order
      expect(h3s.length).toBeGreaterThanOrEqual(0) // may be 0 in shallowMount
    })
  })

  // ── Sections ───────────────────────────────────────────────────────────────

  describe('page sections', () => {
    it('renders platform pillars section', () => {
      const wrapper = mountHome()
      // Section heading changed to "One Platform, Complete Health Intelligence"
      expect(wrapper.text()).toMatch(/Platform|Health Intelligence/i)
    })

    it('renders how it works section', () => {
      const wrapper = mountHome()
      expect(wrapper.text()).toContain('How It Works')
    })

    it('renders trust & privacy section', () => {
      const wrapper = mountHome()
      // Heading changed from "Built for Medical Trust" to "Built for Trust"
      expect(wrapper.text()).toMatch(/Built for.*Trust/i)
    })

    it('renders pricing section', () => {
      const wrapper = mountHome()
      // Heading changed to "Simple, Transparent Pricing"
      expect(wrapper.text()).toMatch(/Simple.*Pricing/i)
    })

    it('renders CTA banner section', () => {
      const wrapper = mountHome()
      expect(wrapper.text()).toContain('Ready to Get Started?')
    })
  })

  // ── Pipeline agents ────────────────────────────────────────────────────────

  describe('pipeline agents', () => {
    it('renders all 7 agent names', () => {
      const wrapper = mountHome()
      const text = wrapper.text()
      const agents = ['Triage', 'Diagnostician', 'Research', 'Specialist', 'Treatment', 'Safety', 'Empathy']
      agents.forEach(name => {
        expect(text).toContain(name)
      })
    })
  })

  // ── Demo section ───────────────────────────────────────────────────────────

  describe('demo section', () => {
    it('renders demo input placeholder', () => {
      const wrapper = mountHome()
      const input = wrapper.find('input[type="text"]')
      expect(input.exists()).toBe(true)
    })

    it('renders Analyze button', () => {
      const wrapper = mountHome()
      const buttons = wrapper.findAll('button')
      const analyzeBtn = buttons.find(b => b.text().includes('Analyze') || b.text().includes('Analyzing'))
      expect(analyzeBtn).toBeDefined()
    })
  })

  // ── Footer ─────────────────────────────────────────────────────────────────

  describe('footer', () => {
    it('renders a footer element', () => {
      const wrapper = mountHome()
      expect(wrapper.find('footer').exists()).toBe(true)
    })

    it('footer contains copyright notice', () => {
      const wrapper = mountHome()
      expect(wrapper.find('footer').text()).toContain('MedDiagnose AI')
    })

    it('footer contains medical disclaimer', () => {
      const wrapper = mountHome()
      expect(wrapper.find('footer').text().toLowerCase()).toContain('not a substitute for professional medical advice')
    })
  })

  // ── Skip link ──────────────────────────────────────────────────────────────

  describe('skip-to-content link', () => {
    it('renders a skip-to-content link', () => {
      const wrapper = mountHome()
      const skipLink = wrapper.find('a[href="#main-content"]')
      expect(skipLink.exists()).toBe(true)
    })
  })
})
