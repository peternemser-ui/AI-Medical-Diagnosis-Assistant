import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'

// Mock the composable dependencies before importing
vi.mock('../useUser.js', () => ({
  useUser: () => ({ logout: vi.fn() })
}))

vi.mock('../useToast.js', () => ({
  useToast: () => ({
    warning: vi.fn(),
    info: vi.fn(),
  })
}))

// Mock onUnmounted since we're not in a component setup context
vi.mock('vue', async () => {
  const actual = await vi.importActual('vue')
  return {
    ...actual,
    onUnmounted: vi.fn(),
  }
})

import { useSessionTimeout } from '../useSessionTimeout.js'

describe('useSessionTimeout', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    localStorage.clear()
  })

  afterEach(() => {
    // Stop any active timer to reset module-level state
    const { stopTimer } = useSessionTimeout()
    stopTimer()
    vi.useRealTimers()
  })

  it('starts a timer and the warning becomes visible before timeout', () => {
    const { startSessionTimer, isWarningVisible } = useSessionTimeout()
    startSessionTimer()

    expect(isWarningVisible.value).toBe(false)

    // Advance to just past the warning threshold (28 minutes)
    vi.advanceTimersByTime(28 * 60 * 1000 + 100)
    expect(isWarningVisible.value).toBe(true)
  })

  it('stopTimer clears scheduled timers and hides warning', () => {
    const { startSessionTimer, stopTimer, isWarningVisible } = useSessionTimeout()
    startSessionTimer()

    // Advance past warning
    vi.advanceTimersByTime(28 * 60 * 1000 + 100)
    expect(isWarningVisible.value).toBe(true)

    stopTimer()
    expect(isWarningVisible.value).toBe(false)
  })

  it('resetTimer clears the warning and reschedules', () => {
    const { startSessionTimer, resetTimer, isWarningVisible } = useSessionTimeout()
    startSessionTimer()

    // Advance past warning threshold
    vi.advanceTimersByTime(28 * 60 * 1000 + 100)
    expect(isWarningVisible.value).toBe(true)

    // Reset should hide warning and reschedule
    resetTimer()
    expect(isWarningVisible.value).toBe(false)

    // After another 28 minutes the warning should appear again
    vi.advanceTimersByTime(28 * 60 * 1000 + 100)
    expect(isWarningVisible.value).toBe(true)
  })

  it('does not start duplicate timers if called twice', () => {
    const { startSessionTimer, isWarningVisible } = useSessionTimeout()
    startSessionTimer()
    startSessionTimer() // second call should be no-op

    vi.advanceTimersByTime(28 * 60 * 1000 + 100)
    expect(isWarningVisible.value).toBe(true)
  })
})
