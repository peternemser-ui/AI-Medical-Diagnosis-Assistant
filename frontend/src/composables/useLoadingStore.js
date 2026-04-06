/**
 * Global Loading State Manager
 *
 * Provides centralized loading/error state for the entire app.
 * Components can check if ANY async operation is in progress.
 */
import { ref, computed } from 'vue'

const _operations = ref(new Map())  // operationId -> { label, startTime }
const _errors = ref([])             // { id, message, timestamp, dismissed }

export function useLoadingStore() {
  const isLoading = computed(() => _operations.value.size > 0)
  const activeOperations = computed(() => Array.from(_operations.value.entries()).map(([id, op]) => ({ id, ...op })))
  const errors = computed(() => _errors.value.filter(e => !e.dismissed))

  function startOperation(id, label = 'Loading...') {
    const map = new Map(_operations.value)
    map.set(id, { label, startTime: Date.now() })
    _operations.value = map
  }

  function endOperation(id) {
    const map = new Map(_operations.value)
    map.delete(id)
    _operations.value = map
  }

  function addError(message, details = null) {
    _errors.value = [..._errors.value, {
      id: Date.now() + Math.random(),
      message,
      details,
      timestamp: new Date().toISOString(),
      dismissed: false,
    }]
  }

  function dismissError(id) {
    _errors.value = _errors.value.map(e => e.id === id ? { ...e, dismissed: true } : e)
  }

  function clearErrors() {
    _errors.value = []
  }

  return { isLoading, activeOperations, errors, startOperation, endOperation, addError, dismissError, clearErrors }
}
