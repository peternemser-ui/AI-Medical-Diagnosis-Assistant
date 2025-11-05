import { ref, onMounted, onUnmounted } from 'vue'

/**
 * Offline Detection Composable
 * Detects network connectivity and provides graceful degradation
 */
export function useOffline() {
  const isOnline = ref(navigator.onLine)
  const wasOffline = ref(false)
  const offlineSince = ref(null)
  const reconnectedAt = ref(null)

  /**
   * Handle online event
   */
  function handleOnline() {
    const wasActuallyOffline = !isOnline.value

    isOnline.value = true
    reconnectedAt.value = new Date()

    if (wasActuallyOffline) {
      console.log('✅ Connection restored')

      // Calculate offline duration
      if (offlineSince.value) {
        const duration = Math.floor((reconnectedAt.value - offlineSince.value) / 1000)
        console.log(`📶 Was offline for ${duration} seconds`)
      }

      wasOffline.value = true
      offlineSince.value = null
    }
  }

  /**
   * Handle offline event
   */
  function handleOffline() {
    isOnline.value = false
    offlineSince.value = new Date()
    console.warn('⚠️ Connection lost')
  }

  /**
   * Initialize listeners
   */
  function initialize() {
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)

    console.log('🌐 Offline detection initialized')
    console.log(`📶 Current status: ${isOnline.value ? 'Online' : 'Offline'}`)
  }

  /**
   * Cleanup listeners
   */
  function cleanup() {
    window.removeEventListener('online', handleOnline)
    window.removeEventListener('offline', handleOffline)
    console.log('🧹 Offline detection cleaned up')
  }

  /**
   * Check connectivity by making a request
   */
  async function checkConnectivity(url = 'https://www.google.com/favicon.ico') {
    try {
      const response = await fetch(url, {
        method: 'HEAD',
        mode: 'no-cors',
        cache: 'no-cache'
      })
      isOnline.value = true
      return true
    } catch (error) {
      isOnline.value = false
      return false
    }
  }

  /**
   * Get offline duration in seconds
   */
  function getOfflineDuration() {
    if (!offlineSince.value) return 0
    return Math.floor((new Date() - offlineSince.value) / 1000)
  }

  // Auto-initialize on mount
  onMounted(() => {
    initialize()
  })

  // Cleanup on unmount
  onUnmounted(() => {
    cleanup()
  })

  return {
    // State
    isOnline,
    wasOffline,
    offlineSince,
    reconnectedAt,

    // Methods
    initialize,
    cleanup,
    checkConnectivity,
    getOfflineDuration
  }
}
