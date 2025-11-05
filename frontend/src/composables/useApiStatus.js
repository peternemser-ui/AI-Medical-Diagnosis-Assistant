import { ref, computed } from 'vue'
import { healthCheck } from '@/services/api.js'

/**
 * API Status Composable
 * Manages API connection status and health checks
 */
export function useApiStatus() {
  const apiStatus = ref(null) // null = checking, true = connected, false = disconnected
  const isChecking = ref(false)
  const lastCheckTime = ref(null)
  const hasApiKey = ref(false)
  const apiMode = ref('basic') // 'basic' | 'enhanced'
  const errorCount = ref(0)
  const checkInterval = ref(null)

  /**
   * Check if API key is configured
   */
  function checkApiKey() {
    try {
      const apiKey = localStorage.getItem('openai_api_key')

      if (apiKey && apiKey.trim() && apiKey.startsWith('sk-')) {
        hasApiKey.value = true
        apiMode.value = 'enhanced'
        console.log('✅ OpenAI API key found - Enhanced Mode')
        return true
      } else {
        hasApiKey.value = false
        apiMode.value = 'basic'
        console.log('⚠️ No valid API key - Basic Mode')
        return false
      }
    } catch (error) {
      console.error('❌ Error checking API key:', error)
      hasApiKey.value = false
      apiMode.value = 'basic'
      return false
    }
  }

  /**
   * Check API health
   */
  async function checkHealth() {
    if (isChecking.value) {
      console.log('⏳ Health check already in progress')
      return apiStatus.value
    }

    isChecking.value = true

    try {
      console.log('🔍 Checking API health...')
      const isHealthy = await healthCheck()

      if (isHealthy) {
        apiStatus.value = true
        errorCount.value = 0
        console.log('✅ API health check passed')
      } else {
        apiStatus.value = false
        errorCount.value++
        console.warn('⚠️ API health check failed')
      }

      lastCheckTime.value = new Date()
      return apiStatus.value
    } catch (error) {
      console.error('❌ API health check error:', error)
      apiStatus.value = false
      errorCount.value++
      lastCheckTime.value = new Date()
      return false
    } finally {
      isChecking.value = false
    }
  }

  /**
   * Initialize API status
   */
  async function initialize() {
    console.log('🚀 Initializing API status...')

    // Check API key first
    checkApiKey()

    // Then check health
    await checkHealth()

    return {
      hasKey: hasApiKey.value,
      isHealthy: apiStatus.value,
      mode: apiMode.value
    }
  }

  /**
   * Start periodic health checks
   */
  function startPeriodicChecks(intervalMs = 60000) {
    // Clear existing interval
    stopPeriodicChecks()

    console.log(`⏰ Starting periodic health checks (every ${intervalMs}ms)`)

    checkInterval.value = setInterval(async () => {
      await checkHealth()
    }, intervalMs)
  }

  /**
   * Stop periodic health checks
   */
  function stopPeriodicChecks() {
    if (checkInterval.value) {
      clearInterval(checkInterval.value)
      checkInterval.value = null
      console.log('⏹️ Stopped periodic health checks')
    }
  }

  /**
   * Force refresh status
   */
  async function refresh() {
    console.log('🔄 Forcing API status refresh...')
    checkApiKey()
    return await checkHealth()
  }

  /**
   * Update API key
   */
  function updateApiKey(newKey) {
    try {
      if (newKey && newKey.trim()) {
        localStorage.setItem('openai_api_key', newKey.trim())
        console.log('✅ API key updated')
      } else {
        localStorage.removeItem('openai_api_key')
        console.log('🗑️ API key removed')
      }

      checkApiKey()
      return true
    } catch (error) {
      console.error('❌ Error updating API key:', error)
      return false
    }
  }

  /**
   * Remove API key
   */
  function removeApiKey() {
    return updateApiKey('')
  }

  /**
   * Get status message
   */
  const statusMessage = computed(() => {
    if (isChecking.value) {
      return 'Checking connection...'
    }

    if (apiStatus.value === null) {
      return 'Connection status unknown'
    }

    if (!hasApiKey.value) {
      return 'Basic Mode - Add API key for AI features'
    }

    if (apiStatus.value) {
      return 'AI Enhanced Mode - Connected'
    }

    return 'Connection error - Retrying...'
  })

  /**
   * Get status color
   */
  const statusColor = computed(() => {
    if (isChecking.value) return 'yellow'
    if (apiStatus.value === null) return 'gray'
    if (!hasApiKey.value) return 'yellow'
    return apiStatus.value ? 'green' : 'red'
  })

  /**
   * Check if enhanced mode is available
   */
  const isEnhancedMode = computed(() => {
    return hasApiKey.value && apiStatus.value === true
  })

  /**
   * Get time since last check
   */
  const timeSinceLastCheck = computed(() => {
    if (!lastCheckTime.value) return null

    const now = new Date()
    const diff = Math.floor((now - lastCheckTime.value) / 1000) // seconds

    if (diff < 60) return `${diff}s ago`
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
    return `${Math.floor(diff / 3600)}h ago`
  })

  return {
    // State
    apiStatus,
    isChecking,
    lastCheckTime,
    hasApiKey,
    apiMode,
    errorCount,

    // Computed
    statusMessage,
    statusColor,
    isEnhancedMode,
    timeSinceLastCheck,

    // Methods
    initialize,
    checkApiKey,
    checkHealth,
    startPeriodicChecks,
    stopPeriodicChecks,
    refresh,
    updateApiKey,
    removeApiKey
  }
}
