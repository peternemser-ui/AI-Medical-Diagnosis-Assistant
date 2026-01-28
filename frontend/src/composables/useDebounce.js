import { ref, watch, customRef } from 'vue'

/**
 * Debounce a value
 */
export function useDebounce(value, delay = 300) {
  const debouncedValue = ref(value.value)

  let timeout

  watch(value, (newValue) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      debouncedValue.value = newValue
    }, delay)
  })

  return debouncedValue
}

/**
 * Create a debounced ref
 */
export function useDebouncedRef(initialValue, delay = 300) {
  let timeout
  return customRef((track, trigger) => {
    return {
      get() {
        track()
        return initialValue
      },
      set(newValue) {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
          initialValue = newValue
          trigger()
        }, delay)
      }
    }
  })
}

/**
 * Debounce a function
 */
export function useDebounceFn(fn, delay = 300, options = {}) {
  const { leading = false, trailing = true, maxWait } = options

  let timeout
  let maxTimeout
  let lastCallTime
  let lastInvokeTime = 0
  let result

  const invokeFunc = (time) => {
    lastInvokeTime = time
    result = fn()
    return result
  }

  const leadingEdge = (time) => {
    lastInvokeTime = time
    if (maxWait !== undefined) {
      maxTimeout = setTimeout(timerExpired, maxWait)
    }
    return leading ? invokeFunc(time) : result
  }

  const remainingWait = (time) => {
    const timeSinceLastCall = time - lastCallTime
    const timeSinceLastInvoke = time - lastInvokeTime
    const timeWaiting = delay - timeSinceLastCall

    return maxWait !== undefined
      ? Math.min(timeWaiting, maxWait - timeSinceLastInvoke)
      : timeWaiting
  }

  const shouldInvoke = (time) => {
    const timeSinceLastCall = time - lastCallTime
    const timeSinceLastInvoke = time - lastInvokeTime

    return (
      lastCallTime === undefined ||
      timeSinceLastCall >= delay ||
      timeSinceLastCall < 0 ||
      (maxWait !== undefined && timeSinceLastInvoke >= maxWait)
    )
  }

  const timerExpired = () => {
    const time = Date.now()
    if (shouldInvoke(time)) {
      return trailingEdge(time)
    }
    timeout = setTimeout(timerExpired, remainingWait(time))
  }

  const trailingEdge = (time) => {
    timeout = undefined
    if (trailing && lastCallTime !== undefined) {
      return invokeFunc(time)
    }
    lastCallTime = undefined
    return result
  }

  const debounced = (...args) => {
    const time = Date.now()
    const isInvoking = shouldInvoke(time)

    lastCallTime = time

    if (isInvoking) {
      if (timeout === undefined) {
        return leadingEdge(time)
      }
      if (maxWait !== undefined) {
        timeout = setTimeout(timerExpired, delay)
        return invokeFunc(time)
      }
    }
    if (timeout === undefined) {
      timeout = setTimeout(timerExpired, delay)
    }
    return result
  }

  debounced.cancel = () => {
    if (timeout !== undefined) {
      clearTimeout(timeout)
    }
    if (maxTimeout !== undefined) {
      clearTimeout(maxTimeout)
    }
    lastInvokeTime = 0
    lastCallTime = undefined
    timeout = undefined
  }

  debounced.flush = () => {
    if (timeout !== undefined) {
      return trailingEdge(Date.now())
    }
    return result
  }

  debounced.pending = () => {
    return timeout !== undefined
  }

  return debounced
}

/**
 * Throttle a function
 */
export function useThrottleFn(fn, delay = 300, options = {}) {
  return useDebounceFn(fn, delay, {
    ...options,
    leading: true,
    trailing: true,
    maxWait: delay
  })
}
