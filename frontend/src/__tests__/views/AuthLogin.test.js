import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'

// ── Mocks ─────────────────────────────────────────────────────────────────────

const mockLogin = vi.fn()

vi.mock('@/services/authService', () => ({
  login: (...args) => mockLogin(...args),
}))

vi.mock('@/services/userService', () => ({
  saveProfile: vi.fn(() => Promise.resolve()),
}))

vi.mock('@/services/analytics', () => ({
  trackEvent: vi.fn(),
  EVENTS: { LOGIN: 'login' },
}))

vi.mock('@/composables/useTheme.js', () => ({
  useTheme: () => ({
    isDark: { value: false },
    theme: { value: 'light' },
    toggleTheme: vi.fn(),
  }),
}))

// ── Component import after mocks ──────────────────────────────────────────────

import AuthLogin from '@/views/AuthLogin.vue'

// ── Router factory ────────────────────────────────────────────────────────────

function makeRouter(initialPath = '/login') {
  const router = createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/login', component: AuthLogin },
      { path: '/consult', component: { template: '<div/>' } },
      { path: '/setup', component: { template: '<div/>' } },
      { path: '/signup', component: { template: '<div/>' } },
    ],
  })
  router.push(initialPath)
  return router
}

function mountLogin() {
  const router = makeRouter()
  return mount(AuthLogin, {
    global: {
      plugins: [router],
      stubs: {
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

describe('AuthLogin', () => {
  beforeEach(() => {
    mockLogin.mockReset()
    localStorage.clear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  // ── Rendering ──────────────────────────────────────────────────────────────

  describe('renders correctly', () => {
    it('mounts without error', () => {
      const wrapper = mountLogin()
      expect(wrapper.exists()).toBe(true)
    })

    it('renders the login form', () => {
      const wrapper = mountLogin()
      expect(wrapper.find('form').exists()).toBe(true)
    })

    it('renders email input with correct type', () => {
      const wrapper = mountLogin()
      const emailInput = wrapper.find('input[type="email"]')
      expect(emailInput.exists()).toBe(true)
    })

    it('renders email input with id="email"', () => {
      const wrapper = mountLogin()
      expect(wrapper.find('#email').exists()).toBe(true)
    })

    it('email label is associated with input via for attribute', () => {
      const wrapper = mountLogin()
      const label = wrapper.find('label[for="email"]')
      expect(label.exists()).toBe(true)
    })

    it('renders password input with id="password"', () => {
      const wrapper = mountLogin()
      expect(wrapper.find('#password').exists()).toBe(true)
    })

    it('password label is associated with input via for attribute', () => {
      const wrapper = mountLogin()
      const label = wrapper.find('label[for="password"]')
      expect(label.exists()).toBe(true)
    })

    it('renders a submit button', () => {
      const wrapper = mountLogin()
      const submit = wrapper.find('button[type="submit"]')
      expect(submit.exists()).toBe(true)
    })

    it('submit button initial text is "Sign In"', () => {
      const wrapper = mountLogin()
      const submit = wrapper.find('button[type="submit"]')
      expect(submit.text()).toContain('Sign In')
    })

    it('renders a link to signup page', () => {
      const wrapper = mountLogin()
      const links = wrapper.findAll('a')
      const hrefs = links.map(l => l.attributes('href'))
      expect(hrefs).toContain('/signup')
    })

    it('does not show error message initially', () => {
      const wrapper = mountLogin()
      // error div only renders when error ref is truthy
      const errorDiv = wrapper.find('.bg-red-500\\/10')
      expect(errorDiv.exists()).toBe(false)
    })
  })

  // ── Email validation ───────────────────────────────────────────────────────

  describe('email validation indicator', () => {
    it('shows validation hint when an invalid email is entered', async () => {
      const wrapper = mountLogin()
      const emailInput = wrapper.find('#email')
      await emailInput.setValue('notanemail')
      await wrapper.vm.$nextTick()
      // The error text appears when email is set but not valid (rendered as text-red-400)
      const hint = wrapper.find('#email-error')
      expect(hint.exists()).toBe(true)
    })

    it('hides validation hint when email is empty', async () => {
      const wrapper = mountLogin()
      const emailInput = wrapper.find('#email')
      await emailInput.setValue('')
      await wrapper.vm.$nextTick()
      const hint = wrapper.find('#email-error')
      expect(hint.exists()).toBe(false)
    })

    it('does not show invalid hint for a valid email', async () => {
      const wrapper = mountLogin()
      const emailInput = wrapper.find('#email')
      await emailInput.setValue('valid@example.com')
      await wrapper.vm.$nextTick()
      const hint = wrapper.find('#email-error')
      expect(hint.exists()).toBe(false)
    })
  })

  // ── Password toggle ────────────────────────────────────────────────────────

  describe('password visibility toggle', () => {
    it('password input starts as type="password"', () => {
      const wrapper = mountLogin()
      expect(wrapper.find('#password').attributes('type')).toBe('password')
    })

    it('clicking the toggle button reveals the password', async () => {
      const wrapper = mountLogin()
      const toggleBtn = wrapper.find('button[type="button"]')
      await toggleBtn.trigger('click')
      expect(wrapper.find('#password').attributes('type')).toBe('text')
    })
  })

  // ── Form submission ────────────────────────────────────────────────────────

  describe('form submission', () => {
    it('calls authLogin with email and password on submit', async () => {
      mockLogin.mockResolvedValue({ user: { email: 'a@b.com', name: 'A' } })
      const wrapper = mountLogin()

      await wrapper.find('#email').setValue('user@example.com')
      await wrapper.find('#password').setValue('secret123')
      await wrapper.find('form').trigger('submit')

      expect(mockLogin).toHaveBeenCalledWith('user@example.com', 'secret123')
    })

    it('shows error message when login throws', async () => {
      mockLogin.mockRejectedValue(new Error('Invalid credentials'))
      const wrapper = mountLogin()

      await wrapper.find('#email').setValue('bad@example.com')
      await wrapper.find('#password').setValue('wrong')
      await wrapper.find('form').trigger('submit')
      await wrapper.vm.$nextTick()
      await wrapper.vm.$nextTick()

      expect(wrapper.vm.error).toBe('Invalid credentials')
    })

    it('sets api_key_configured in localStorage on success', async () => {
      mockLogin.mockResolvedValue({ user: { email: 'a@b.com', name: 'A' } })
      const wrapper = mountLogin()

      await wrapper.find('#email').setValue('user@example.com')
      await wrapper.find('#password').setValue('pass')
      await wrapper.find('form').trigger('submit')
      await wrapper.vm.$nextTick()

      expect(localStorage.getItem('api_key_configured')).toBe('true')
    })

    it('submit button is disabled while loading', async () => {
      // Make login hang so we can inspect loading state
      let resolve
      mockLogin.mockReturnValue(new Promise(r => { resolve = r }))
      const wrapper = mountLogin()

      await wrapper.find('#email').setValue('u@e.com')
      await wrapper.find('#password').setValue('pass')
      wrapper.find('form').trigger('submit')
      await wrapper.vm.$nextTick()

      expect(wrapper.find('button[type="submit"]').attributes('disabled')).toBeDefined()
      resolve({ user: { email: 'u@e.com' } })
    })
  })

  // ── Accessibility ──────────────────────────────────────────────────────────

  describe('accessibility attributes', () => {
    it('email input has aria-invalid when email is invalid', async () => {
      const wrapper = mountLogin()
      await wrapper.find('#email').setValue('bad')
      await wrapper.vm.$nextTick()
      expect(wrapper.find('#email').attributes('aria-invalid')).toBe('true')
    })

    it('email input does not have aria-invalid when email is valid', async () => {
      const wrapper = mountLogin()
      await wrapper.find('#email').setValue('good@example.com')
      await wrapper.vm.$nextTick()
      const ariaInvalid = wrapper.find('#email').attributes('aria-invalid')
      expect(ariaInvalid).not.toBe('true')
    })

    it('email input has aria-describedby when invalid', async () => {
      const wrapper = mountLogin()
      await wrapper.find('#email').setValue('notvalid')
      await wrapper.vm.$nextTick()
      expect(wrapper.find('#email').attributes('aria-describedby')).toBeTruthy()
    })
  })
})
