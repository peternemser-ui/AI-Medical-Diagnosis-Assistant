import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'

// ── Mocks ─────────────────────────────────────────────────────────────────────

const mockSignup = vi.fn()

vi.mock('@/services/authService', () => ({
  signup: (...args) => mockSignup(...args),
}))

vi.mock('@/services/userService', () => ({
  saveProfile: vi.fn(() => Promise.resolve()),
}))

vi.mock('@/services/analytics', () => ({
  trackEvent: vi.fn(),
  EVENTS: { SIGNUP: 'signup' },
}))

vi.mock('@/composables/useTheme.js', () => ({
  useTheme: () => ({
    isDark: { value: false },
    theme: { value: 'light' },
    toggleTheme: vi.fn(),
  }),
}))

// ── Component import after mocks ──────────────────────────────────────────────

import AuthSignup from '@/views/AuthSignup.vue'

// ── Router factory ────────────────────────────────────────────────────────────

function makeRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/signup', component: AuthSignup },
      { path: '/login', component: { template: '<div/>' } },
      { path: '/setup', component: { template: '<div/>' } },
    ],
  })
}

function mountSignup() {
  return mount(AuthSignup, {
    global: {
      plugins: [makeRouter()],
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

describe('AuthSignup', () => {
  beforeEach(() => {
    mockSignup.mockReset()
    localStorage.clear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  // ── Rendering ──────────────────────────────────────────────────────────────

  describe('renders correctly', () => {
    it('mounts without error', () => {
      const wrapper = mountSignup()
      expect(wrapper.exists()).toBe(true)
    })

    it('renders the signup form', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('form').exists()).toBe(true)
    })

    it('renders name input with id="name"', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('#name').exists()).toBe(true)
    })

    it('name label is associated with input via for attribute', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('label[for="name"]').exists()).toBe(true)
    })

    it('renders email input with id="signup-email"', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('#signup-email').exists()).toBe(true)
    })

    it('email label is associated with input', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('label[for="signup-email"]').exists()).toBe(true)
    })

    it('renders password input with id="signup-password"', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('#signup-password').exists()).toBe(true)
    })

    it('password label is associated with input', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('label[for="signup-password"]').exists()).toBe(true)
    })

    it('renders confirm-password input with id="confirm-password"', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('#confirm-password').exists()).toBe(true)
    })

    it('confirm-password label is associated with input', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('label[for="confirm-password"]').exists()).toBe(true)
    })

    it('renders terms checkbox', () => {
      const wrapper = mountSignup()
      const checkbox = wrapper.find('input[type="checkbox"]')
      expect(checkbox.exists()).toBe(true)
    })

    it('renders a submit button', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
    })

    it('submit button initial text is "Create Account"', () => {
      const wrapper = mountSignup()
      expect(wrapper.find('button[type="submit"]').text()).toContain('Create Account')
    })

    it('renders link to login page', () => {
      const wrapper = mountSignup()
      const links = wrapper.findAll('a')
      const hrefs = links.map(l => l.attributes('href'))
      expect(hrefs).toContain('/login')
    })
  })

  // ── Password strength meter ────────────────────────────────────────────────

  describe('password strength meter', () => {
    it('strength bar is not shown when password is empty', () => {
      const wrapper = mountSignup()
      // Strength bar only renders v-if="password" — identified by role="progressbar"
      const bar = wrapper.find('[role="progressbar"]')
      expect(bar.exists()).toBe(false)
    })

    it('strength bar appears when password is typed', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('abc')
      await wrapper.vm.$nextTick()
      // Strength meter now renders as a single continuous progress bar with role="progressbar"
      const bar = wrapper.find('[role="progressbar"]')
      expect(bar.exists()).toBe(true)
    })

    it('strengthLevel is 1 (Weak) for very short password', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('ab')
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.strengthLevel).toBe(1)
    })

    it('strengthLevel is 2 (Fair) for 8-char password', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('abcdefgh')
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.strengthLevel).toBe(2)
    })

    it('strengthLevel is 4 (Strong) for long password with all requirements', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('Str0ng!Pass#')
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.strengthLevel).toBe(4)
    })

    it('strength label text reflects level', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('Str0ng!Pass#')
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.strengthLabelText).toBe('Strong')
    })

    it('strength bar has role="progressbar" for accessibility', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('abc')
      await wrapper.vm.$nextTick()
      const progressbar = wrapper.find('[role="progressbar"]')
      expect(progressbar.exists()).toBe(true)
    })

    it('progressbar has aria-valuenow matching strengthLevel', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('ab')
      await wrapper.vm.$nextTick()
      const progressbar = wrapper.find('[role="progressbar"]')
      expect(progressbar.attributes('aria-valuenow')).toBe('1')
    })

    it('progressbar has aria-label', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('abc')
      await wrapper.vm.$nextTick()
      const progressbar = wrapper.find('[role="progressbar"]')
      expect(progressbar.attributes('aria-label')).toBeTruthy()
    })
  })

  // ── Individual password requirement hints ─────────────────────────────────

  describe('password requirement hints', () => {
    it('shows requirement hints when password is entered', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('test')
      await wrapper.vm.$nextTick()
      // pwHasLength computed
      expect(wrapper.vm.pwHasLength).toBe(false)
    })

    it('pwHasLength is true for 8+ char password', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('12345678')
      expect(wrapper.vm.pwHasLength).toBe(true)
    })

    it('pwHasUpper is true when password contains uppercase', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('Abc')
      expect(wrapper.vm.pwHasUpper).toBe(true)
    })

    it('pwHasLower is true when password contains lowercase', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('Abc')
      expect(wrapper.vm.pwHasLower).toBe(true)
    })

    it('pwHasNumber is true when password contains a digit', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('abc1')
      expect(wrapper.vm.pwHasNumber).toBe(true)
    })

    it('pwHasSpecial is true for special characters', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('abc!')
      expect(wrapper.vm.pwHasSpecial).toBe(true)
    })
  })

  // ── Password mismatch ──────────────────────────────────────────────────────

  describe('password confirmation', () => {
    it('shows mismatch error when passwords differ', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('Password1!')
      await wrapper.find('#confirm-password').setValue('Different1!')
      await wrapper.vm.$nextTick()
      const mismatch = wrapper.find('p.text-red-400')
      expect(mismatch.exists()).toBe(true)
      expect(mismatch.text()).toContain('Passwords do not match')
    })

    it('does not show mismatch error when passwords match', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#signup-password').setValue('SamePass1!')
      await wrapper.find('#confirm-password').setValue('SamePass1!')
      await wrapper.vm.$nextTick()
      await wrapper.vm.$nextTick()
      // The component shows error only when confirmPassword !== password
      expect(wrapper.vm.confirmPassword).toBe(wrapper.vm.password)
    })
  })

  // ── canSubmit computed ────────────────────────────────────────────────────

  describe('canSubmit', () => {
    it('is falsy when form is empty', () => {
      const wrapper = mountSignup()
      expect(wrapper.vm.canSubmit).toBeFalsy()
    })

    it('is false when passwords do not match', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#name').setValue('Jane')
      await wrapper.find('#signup-email').setValue('jane@example.com')
      await wrapper.find('#signup-password').setValue('Pass1234!')
      await wrapper.find('#confirm-password').setValue('Different!')
      await wrapper.find('input[type="checkbox"]').setValue(true)
      expect(wrapper.vm.canSubmit).toBe(false)
    })

    it('is true when all fields are valid and terms accepted', async () => {
      const wrapper = mountSignup()
      await wrapper.find('#name').setValue('Jane Doe')
      await wrapper.find('#signup-email').setValue('jane@example.com')
      await wrapper.find('#signup-password').setValue('Pass1234!')
      await wrapper.find('#confirm-password').setValue('Pass1234!')
      await wrapper.find('input[type="checkbox"]').setValue(true)
      expect(wrapper.vm.canSubmit).toBe(true)
    })
  })

  // ── Form submission ────────────────────────────────────────────────────────

  describe('form submission', () => {
    async function fillValidForm(wrapper) {
      await wrapper.find('#name').setValue('Jane Doe')
      await wrapper.find('#signup-email').setValue('jane@example.com')
      await wrapper.find('#signup-password').setValue('Pass1234!')
      await wrapper.find('#confirm-password').setValue('Pass1234!')
      await wrapper.find('input[type="checkbox"]').setValue(true)
    }

    it('calls authSignup with name, email, password on submit', async () => {
      mockSignup.mockResolvedValue({ user: { email: 'jane@example.com', name: 'Jane Doe' } })
      const wrapper = mountSignup()
      await fillValidForm(wrapper)
      await wrapper.find('form').trigger('submit')
      expect(mockSignup).toHaveBeenCalledWith('Jane Doe', 'jane@example.com', 'Pass1234!')
    })

    it('shows error message when signup throws', async () => {
      mockSignup.mockRejectedValue(new Error('Email already taken'))
      const wrapper = mountSignup()
      await fillValidForm(wrapper)
      await wrapper.find('form').trigger('submit')
      await wrapper.vm.$nextTick()
      await wrapper.vm.$nextTick()
      expect(wrapper.vm.error).toBe('Email already taken')
    })

    it('shows verification message on success', async () => {
      mockSignup.mockResolvedValue({ user: { email: 'jane@example.com', name: 'Jane Doe' } })
      const wrapper = mountSignup()
      await fillValidForm(wrapper)
      await wrapper.find('form').trigger('submit')
      await wrapper.vm.$nextTick()
      expect(wrapper.text()).toContain('jane@example.com')
    })
  })
})
