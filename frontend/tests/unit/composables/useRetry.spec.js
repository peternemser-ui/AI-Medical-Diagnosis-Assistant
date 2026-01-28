import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useRetry } from '@/composables/useRetry'

describe('useRetry', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('executes function successfully on first try', async () => {
    const { execute } = useRetry()
    const fn = vi.fn().mockResolvedValue('success')
    const result = await execute(fn)
    expect(result).toBe('success')
    expect(fn).toHaveBeenCalledTimes(1)
  })

  it('retries on failure', async () => {
    const { execute } = useRetry({ maxRetries: 3 })
    const fn = vi.fn()
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValue('success')

    const promise = execute(fn)
    await vi.advanceTimersByTimeAsync(1000)
    const result = await promise

    expect(result).toBe('success')
    expect(fn).toHaveBeenCalledTimes(2)
  })

  it('uses exponential backoff', async () => {
    const { execute } = useRetry({ maxRetries: 3, baseDelay: 100 })
    const fn = vi.fn().mockRejectedValue(new Error('fail'))

    const promise = execute(fn).catch(() => {})

    await vi.advanceTimersByTimeAsync(100) // First retry
    await vi.advanceTimersByTimeAsync(200) // Second retry
    await vi.advanceTimersByTimeAsync(400) // Third retry

    await promise
    expect(fn.mock.calls.length).toBeGreaterThan(1)
  })

  it('throws after max retries', async () => {
    const { execute } = useRetry({ maxRetries: 2 })
    const fn = vi.fn().mockRejectedValue(new Error('persistent failure'))

    const promise = execute(fn)
    await vi.advanceTimersByTimeAsync(5000)

    await expect(promise).rejects.toThrow('persistent failure')
  })

  it('provides retry count', async () => {
    const { execute, retryCount } = useRetry({ maxRetries: 3 })
    const fn = vi.fn()
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValue('success')

    const promise = execute(fn)
    await vi.advanceTimersByTimeAsync(1000)
    await promise

    expect(retryCount.value).toBe(1)
  })

  it('indicates loading state', async () => {
    const { execute, isLoading } = useRetry()
    const fn = vi.fn().mockResolvedValue('success')

    expect(isLoading.value).toBe(false)
    const promise = execute(fn)
    expect(isLoading.value).toBe(true)
    await promise
    expect(isLoading.value).toBe(false)
  })

  it('can be cancelled', async () => {
    const { execute, cancel } = useRetry({ maxRetries: 5 })
    const fn = vi.fn().mockRejectedValue(new Error('fail'))

    const promise = execute(fn).catch(() => {})
    cancel()
    await vi.advanceTimersByTimeAsync(10000)
    await promise

    expect(fn.mock.calls.length).toBeLessThanOrEqual(2)
  })

  it('resets state', () => {
    const { reset, retryCount } = useRetry()
    reset()
    expect(retryCount.value).toBe(0)
  })
})
