import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useApiStatus } from '@/composables/useApiStatus'

vi.mock('axios', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('useApiStatus', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes with unknown status', () => {
    const { status } = useApiStatus()
    expect(['unknown', 'checking', 'online']).toContain(status.value)
  })

  it('checks API health', async () => {
    const axios = await import('axios')
    axios.default.get.mockResolvedValue({ status: 200 })

    const { checkHealth, status } = useApiStatus()
    await checkHealth()
    expect(status.value).toBe('online')
  })

  it('detects API offline', async () => {
    const axios = await import('axios')
    axios.default.get.mockRejectedValue(new Error('Network error'))

    const { checkHealth, status } = useApiStatus()
    await checkHealth()
    expect(status.value).toBe('offline')
  })

  it('provides isHealthy computed', async () => {
    const axios = await import('axios')
    axios.default.get.mockResolvedValue({ status: 200 })

    const { checkHealth, isHealthy } = useApiStatus()
    await checkHealth()
    expect(isHealthy.value).toBe(true)
  })

  it('tracks response time', async () => {
    const axios = await import('axios')
    axios.default.get.mockResolvedValue({ status: 200 })

    const { checkHealth, responseTime } = useApiStatus()
    await checkHealth()
    expect(responseTime.value).toBeGreaterThanOrEqual(0)
  })

  it('provides error message when offline', async () => {
    const axios = await import('axios')
    axios.default.get.mockRejectedValue(new Error('Connection refused'))

    const { checkHealth, error } = useApiStatus()
    await checkHealth()
    expect(error.value).toBeTruthy()
  })

  it('auto-checks at interval', async () => {
    vi.useFakeTimers()
    const axios = await import('axios')
    axios.default.get.mockResolvedValue({ status: 200 })

    const { startAutoCheck, stopAutoCheck } = useApiStatus()
    startAutoCheck(1000)

    await vi.advanceTimersByTimeAsync(3000)
    expect(axios.default.get.mock.calls.length).toBeGreaterThan(1)

    stopAutoCheck()
    vi.useRealTimers()
  })

  it('provides last check time', async () => {
    const axios = await import('axios')
    axios.default.get.mockResolvedValue({ status: 200 })

    const { checkHealth, lastCheckTime } = useApiStatus()
    await checkHealth()
    expect(lastCheckTime.value).toBeDefined()
  })

  it('handles timeout', async () => {
    const axios = await import('axios')
    axios.default.get.mockImplementation(() => new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Timeout')), 10000)
    }))

    const { checkHealth, status } = useApiStatus()
    vi.useFakeTimers()
    const promise = checkHealth()
    await vi.advanceTimersByTimeAsync(10000)
    await promise
    expect(['offline', 'timeout']).toContain(status.value)
    vi.useRealTimers()
  })
})
