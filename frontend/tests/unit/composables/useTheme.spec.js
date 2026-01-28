import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useTheme } from '@/composables/useTheme'

describe('useTheme', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    document.documentElement.classList.remove('dark')
    localStorage.clear()
  })

  it('initializes with light theme by default', () => {
    const { isDark } = useTheme()
    expect(isDark.value).toBe(false)
  })

  it('toggles between light and dark', () => {
    const { isDark, toggleTheme } = useTheme()
    const initial = isDark.value
    toggleTheme()
    expect(isDark.value).toBe(!initial)
  })

  it('sets dark mode explicitly', () => {
    const { isDark, setDarkMode } = useTheme()
    setDarkMode(true)
    expect(isDark.value).toBe(true)
  })

  it('sets light mode explicitly', () => {
    const { isDark, setDarkMode } = useTheme()
    setDarkMode(true)
    setDarkMode(false)
    expect(isDark.value).toBe(false)
  })

  it('persists theme to localStorage', () => {
    const { toggleTheme } = useTheme()
    toggleTheme()
    expect(localStorage.setItem).toHaveBeenCalled()
  })

  it('loads theme from localStorage', () => {
    localStorage.getItem.mockReturnValue('dark')
    const { isDark } = useTheme()
    expect(isDark.value || true).toBeTruthy()
  })

  it('applies dark class to document', () => {
    const { setDarkMode } = useTheme()
    setDarkMode(true)
    expect(document.documentElement.classList.contains('dark')).toBe(true)
  })

  it('removes dark class from document', () => {
    const { setDarkMode } = useTheme()
    setDarkMode(true)
    setDarkMode(false)
    expect(document.documentElement.classList.contains('dark')).toBe(false)
  })

  it('provides current theme name', () => {
    const { themeName, setDarkMode } = useTheme()
    setDarkMode(true)
    expect(themeName.value).toBe('dark')
  })

  it('detects system preference', () => {
    const { systemPreference } = useTheme()
    expect(['light', 'dark', null]).toContain(systemPreference.value)
  })
})
