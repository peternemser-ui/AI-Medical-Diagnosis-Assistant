import { ref, watch } from 'vue'

/**
 * Reactive localStorage composable
 */
export function useLocalStorage(key, defaultValue, options = {}) {
  const {
    serializer = JSON,
    onError = (e) => console.error('useLocalStorage error:', e)
  } = options

  // Read initial value
  const readValue = () => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? serializer.parse(item) : defaultValue
    } catch (error) {
      onError(error)
      return defaultValue
    }
  }

  const storedValue = ref(readValue())

  // Watch for changes and sync to localStorage
  watch(
    storedValue,
    (newValue) => {
      try {
        if (newValue === undefined || newValue === null) {
          window.localStorage.removeItem(key)
        } else {
          window.localStorage.setItem(key, serializer.stringify(newValue))
        }
      } catch (error) {
        onError(error)
      }
    },
    { deep: true }
  )

  // Listen for storage events from other tabs
  if (typeof window !== 'undefined') {
    window.addEventListener('storage', (e) => {
      if (e.key === key && e.newValue !== null) {
        try {
          storedValue.value = serializer.parse(e.newValue)
        } catch (error) {
          onError(error)
        }
      }
    })
  }

  // Remove value
  const remove = () => {
    storedValue.value = defaultValue
    window.localStorage.removeItem(key)
  }

  return {
    value: storedValue,
    remove
  }
}

/**
 * Reactive sessionStorage composable
 */
export function useSessionStorage(key, defaultValue, options = {}) {
  const {
    serializer = JSON,
    onError = (e) => console.error('useSessionStorage error:', e)
  } = options

  const readValue = () => {
    try {
      const item = window.sessionStorage.getItem(key)
      return item ? serializer.parse(item) : defaultValue
    } catch (error) {
      onError(error)
      return defaultValue
    }
  }

  const storedValue = ref(readValue())

  watch(
    storedValue,
    (newValue) => {
      try {
        if (newValue === undefined || newValue === null) {
          window.sessionStorage.removeItem(key)
        } else {
          window.sessionStorage.setItem(key, serializer.stringify(newValue))
        }
      } catch (error) {
        onError(error)
      }
    },
    { deep: true }
  )

  const remove = () => {
    storedValue.value = defaultValue
    window.sessionStorage.removeItem(key)
  }

  return {
    value: storedValue,
    remove
  }
}

/**
 * Check if localStorage is available
 */
export function isStorageAvailable(type = 'localStorage') {
  try {
    const storage = window[type]
    const testKey = '__storage_test__'
    storage.setItem(testKey, testKey)
    storage.removeItem(testKey)
    return true
  } catch (e) {
    return false
  }
}
