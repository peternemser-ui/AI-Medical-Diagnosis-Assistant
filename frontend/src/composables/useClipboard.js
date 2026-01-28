import { ref, readonly } from 'vue'

/**
 * Clipboard composable for copy/paste operations
 */
export function useClipboard(options = {}) {
  const { timeout = 2000 } = options

  const text = ref('')
  const copied = ref(false)
  const isSupported = ref(navigator && 'clipboard' in navigator)

  let timeoutId

  /**
   * Copy text to clipboard
   */
  async function copy(value) {
    if (!isSupported.value) {
      // Fallback for older browsers
      return fallbackCopy(value)
    }

    try {
      await navigator.clipboard.writeText(value)
      text.value = value
      copied.value = true

      // Reset copied state after timeout
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => {
        copied.value = false
      }, timeout)

      return true
    } catch (error) {
      console.error('Failed to copy:', error)
      return fallbackCopy(value)
    }
  }

  /**
   * Fallback copy using textarea
   */
  function fallbackCopy(value) {
    const textarea = document.createElement('textarea')
    textarea.value = value
    textarea.style.position = 'fixed'
    textarea.style.left = '-9999px'
    textarea.style.top = '-9999px'
    document.body.appendChild(textarea)
    textarea.focus()
    textarea.select()

    try {
      const successful = document.execCommand('copy')
      if (successful) {
        text.value = value
        copied.value = true

        clearTimeout(timeoutId)
        timeoutId = setTimeout(() => {
          copied.value = false
        }, timeout)
      }
      return successful
    } catch (error) {
      console.error('Fallback copy failed:', error)
      return false
    } finally {
      document.body.removeChild(textarea)
    }
  }

  /**
   * Read text from clipboard
   */
  async function paste() {
    if (!isSupported.value) {
      console.warn('Clipboard API not supported')
      return null
    }

    try {
      const clipboardText = await navigator.clipboard.readText()
      text.value = clipboardText
      return clipboardText
    } catch (error) {
      console.error('Failed to read clipboard:', error)
      return null
    }
  }

  return {
    text: readonly(text),
    copied: readonly(copied),
    isSupported: readonly(isSupported),
    copy,
    paste
  }
}

/**
 * Copy to clipboard helper function
 */
export async function copyToClipboard(text) {
  const { copy } = useClipboard()
  return await copy(text)
}
