import { ref, onUnmounted } from 'vue'
import { useUser } from './useUser.js'
import { useToast } from './useToast.js'

const TIMEOUT_MS = 30 * 60 * 1000        // 30 minutes
const WARNING_BEFORE_MS = 2 * 60 * 1000  // warn 2 minutes before logout

const ACTIVITY_EVENTS = ['mousemove', 'keypress', 'click', 'touchstart', 'scroll']

// Shared state so multiple components don't create duplicate timers
let timeoutId = null
let warningId = null
let active = false

export function useSessionTimeout() {
  const { logout } = useUser()
  const toast = useToast()
  const isWarningVisible = ref(false)

  function onActivity() {
    if (!active) return
    resetTimer()
  }

  function startSessionTimer() {
    if (active) return // already running
    active = true
    ACTIVITY_EVENTS.forEach(evt => window.addEventListener(evt, onActivity, { passive: true }))
    scheduleTimers()
  }

  function scheduleTimers() {
    clearScheduled()

    // Warning fires 2 minutes before logout
    warningId = setTimeout(() => {
      isWarningVisible.value = true
      toast.warning(
        'Your session will expire in 2 minutes due to inactivity. Move your mouse or press a key to stay logged in.',
        0 // persistent — no auto-dismiss
      )
    }, TIMEOUT_MS - WARNING_BEFORE_MS)

    // Actual logout
    timeoutId = setTimeout(() => {
      isWarningVisible.value = false
      toast.info('You have been logged out due to inactivity.')
      logout()
    }, TIMEOUT_MS)
  }

  function resetTimer() {
    if (!active) return
    isWarningVisible.value = false
    scheduleTimers()
  }

  function stopTimer() {
    active = false
    clearScheduled()
    isWarningVisible.value = false
    ACTIVITY_EVENTS.forEach(evt => window.removeEventListener(evt, onActivity))
  }

  function clearScheduled() {
    if (timeoutId) { clearTimeout(timeoutId); timeoutId = null }
    if (warningId) { clearTimeout(warningId); warningId = null }
  }

  // Auto-cleanup if the component using this composable unmounts
  onUnmounted(() => {
    stopTimer()
  })

  return {
    startSessionTimer,
    resetTimer,
    stopTimer,
    isWarningVisible,
  }
}
