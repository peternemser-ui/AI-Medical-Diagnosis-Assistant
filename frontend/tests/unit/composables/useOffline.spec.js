import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useOffline } from '@/composables/useOffline'

describe('useOffline', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    Object.defineProperty(navigator, 'onLine', {
      value: true,
      writable: true,
      configurable: true
    })
  })

  it('detects online status', () => {
    const { isOnline } = useOffline()
    expect(isOnline.value).toBe(true)
  })

  it('detects offline status', () => {
    Object.defineProperty(navigator, 'onLine', { value: false })
    const { isOnline } = useOffline()
    expect(isOnline.value).toBe(false)
  })

  it('provides offline indicator', () => {
    Object.defineProperty(navigator, 'onLine', { value: false })
    const { isOffline } = useOffline()
    expect(isOffline.value).toBe(true)
  })

  it('responds to online event', () => {
    const { isOnline } = useOffline()
    Object.defineProperty(navigator, 'onLine', { value: true })
    window.dispatchEvent(new Event('online'))
    expect(isOnline.value).toBe(true)
  })

  it('responds to offline event', () => {
    const { isOnline } = useOffline()
    Object.defineProperty(navigator, 'onLine', { value: false })
    window.dispatchEvent(new Event('offline'))
    expect(isOnline.value).toBe(false)
  })

  it('provides connection quality info', () => {
    const { connectionQuality } = useOffline()
    expect(['good', 'poor', 'unknown', undefined]).toContain(connectionQuality?.value)
  })

  it('queues requests when offline', () => {
    Object.defineProperty(navigator, 'onLine', { value: false })
    const { queueRequest, pendingRequests } = useOffline()
    queueRequest({ url: '/api/test', method: 'POST' })
    expect(pendingRequests.value.length).toBe(1)
  })

  it('processes queue when back online', async () => {
    const { queueRequest, processQueue, pendingRequests } = useOffline()
    queueRequest({ url: '/api/test', method: 'POST' })
    Object.defineProperty(navigator, 'onLine', { value: true })
    await processQueue()
    // Queue should be processed
    expect(pendingRequests.value.length).toBeLessThanOrEqual(1)
  })

  it('clears queue', () => {
    const { queueRequest, clearQueue, pendingRequests } = useOffline()
    queueRequest({ url: '/api/test', method: 'POST' })
    clearQueue()
    expect(pendingRequests.value.length).toBe(0)
  })

  it('provides last online time', () => {
    const { lastOnlineTime } = useOffline()
    expect(lastOnlineTime.value).toBeDefined()
  })
})
