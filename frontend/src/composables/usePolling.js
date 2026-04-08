import { ref, onUnmounted } from 'vue'

/**
 * Composable for polling data at regular intervals with auto-cleanup.
 * @param {Function} fetchFn - Async function to call on each interval
 * @param {number} intervalMs - Polling interval in milliseconds (default 10000)
 */
export function usePolling(fetchFn, intervalMs = 10000) {
  const isPolling = ref(false)
  const error = ref(null)
  const lastFetched = ref(null)
  let timer = null

  async function poll() {
    try {
      error.value = null
      await fetchFn()
      lastFetched.value = new Date()
    } catch (e) {
      error.value = e.message || 'Polling failed'
      console.error('Polling error:', e)
    }
  }

  function start() {
    if (isPolling.value) return
    isPolling.value = true
    poll() // Immediate first fetch
    timer = setInterval(poll, intervalMs)
  }

  function stop() {
    isPolling.value = false
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  function restart() {
    stop()
    start()
  }

  // Auto-cleanup on component unmount
  onUnmounted(() => stop())

  return { isPolling, error, lastFetched, start, stop, restart, poll }
}
