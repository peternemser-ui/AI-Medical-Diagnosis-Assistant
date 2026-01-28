import { ref, readonly } from 'vue'

const notifications = ref([])
let notificationId = 0

export function useNotifications() {
  /**
   * Add a notification
   */
  function notify(options) {
    const id = ++notificationId
    const notification = {
      id,
      type: options.type || 'info',
      title: options.title || '',
      message: options.message,
      duration: options.duration ?? 5000,
      dismissible: options.dismissible ?? true,
      action: options.action || null,
      createdAt: Date.now()
    }

    notifications.value.push(notification)

    // Auto-dismiss after duration
    if (notification.duration > 0) {
      setTimeout(() => {
        dismiss(id)
      }, notification.duration)
    }

    return id
  }

  /**
   * Show success notification
   */
  function success(message, options = {}) {
    return notify({ ...options, type: 'success', message })
  }

  /**
   * Show error notification
   */
  function error(message, options = {}) {
    return notify({ ...options, type: 'error', message, duration: options.duration ?? 8000 })
  }

  /**
   * Show warning notification
   */
  function warning(message, options = {}) {
    return notify({ ...options, type: 'warning', message })
  }

  /**
   * Show info notification
   */
  function info(message, options = {}) {
    return notify({ ...options, type: 'info', message })
  }

  /**
   * Dismiss a notification by ID
   */
  function dismiss(id) {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index !== -1) {
      notifications.value.splice(index, 1)
    }
  }

  /**
   * Dismiss all notifications
   */
  function dismissAll() {
    notifications.value = []
  }

  /**
   * Show a promise-based notification
   */
  async function promise(asyncFn, options = {}) {
    const {
      loading = 'Loading...',
      success: successMsg = 'Success!',
      error: errorMsg = 'Something went wrong'
    } = options

    const id = notify({
      type: 'loading',
      message: loading,
      duration: 0,
      dismissible: false
    })

    try {
      const result = await asyncFn()
      dismiss(id)
      success(typeof successMsg === 'function' ? successMsg(result) : successMsg)
      return result
    } catch (err) {
      dismiss(id)
      error(typeof errorMsg === 'function' ? errorMsg(err) : errorMsg)
      throw err
    }
  }

  return {
    notifications: readonly(notifications),
    notify,
    success,
    error,
    warning,
    info,
    dismiss,
    dismissAll,
    promise
  }
}

// Global toast instance for use outside components
export const toast = {
  success: (msg, opts) => useNotifications().success(msg, opts),
  error: (msg, opts) => useNotifications().error(msg, opts),
  warning: (msg, opts) => useNotifications().warning(msg, opts),
  info: (msg, opts) => useNotifications().info(msg, opts)
}
