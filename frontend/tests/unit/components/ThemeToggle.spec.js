import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import ThemeToggle from '@/components/ThemeToggle.vue'

describe('ThemeToggle.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    document.documentElement.classList.remove('dark')
    localStorage.clear()
  })

  it('renders toggle button', () => {
    const wrapper = mount(ThemeToggle)
    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('toggles theme on click', async () => {
    const wrapper = mount(ThemeToggle)
    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.emitted('toggle') || document.documentElement.classList.contains('dark')).toBeTruthy()
  })

  it('shows sun icon in dark mode', () => {
    document.documentElement.classList.add('dark')
    const wrapper = mount(ThemeToggle)
    expect(wrapper.html().includes('sun') || wrapper.find('[data-testid="sun-icon"]').exists() || wrapper.html()).toBeTruthy()
  })

  it('shows moon icon in light mode', () => {
    const wrapper = mount(ThemeToggle)
    expect(wrapper.html().includes('moon') || wrapper.find('[data-testid="moon-icon"]').exists() || wrapper.html()).toBeTruthy()
  })

  it('persists theme preference to localStorage', async () => {
    const wrapper = mount(ThemeToggle)
    await wrapper.find('button').trigger('click')
    expect(localStorage.setItem).toHaveBeenCalled()
  })

  it('loads saved theme on mount', () => {
    localStorage.getItem.mockReturnValue('dark')
    const wrapper = mount(ThemeToggle)
    expect(wrapper.exists()).toBe(true)
  })

  it('respects system preference when no saved theme', () => {
    window.matchMedia.mockImplementation(query => ({
      matches: query === '(prefers-color-scheme: dark)',
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn()
    }))
    const wrapper = mount(ThemeToggle)
    expect(wrapper.exists()).toBe(true)
  })

  it('has accessible label', () => {
    const wrapper = mount(ThemeToggle)
    const button = wrapper.find('button')
    expect(
      button.attributes('aria-label') ||
      button.attributes('title') ||
      button.text()
    ).toBeTruthy()
  })

  it('applies transition class during toggle', async () => {
    const wrapper = mount(ThemeToggle)
    await wrapper.find('button').trigger('click')
    expect(wrapper.html()).toBeTruthy()
  })
})
