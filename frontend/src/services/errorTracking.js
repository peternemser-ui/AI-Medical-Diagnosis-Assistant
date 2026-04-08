/**
 * Client-side error tracking service.
 *
 * Captures uncaught JavaScript errors and unhandled promise rejections,
 * stores the last 50 events in localStorage, and exposes helpers for
 * retrieving and clearing the log.
 *
 * No data is sent to a third-party service — everything stays local.
 * This makes it easy to debug production issues by asking users to share
 * their error log (e.g., via a support form or admin panel).
 *
 * Usage (wired in main.js):
 *   import { initErrorTracking } from '@/services/errorTracking'
 *   initErrorTracking()
 *
 * Retrieve the log anywhere:
 *   import { getErrorLog, clearErrorLog } from '@/services/errorTracking'
 *   const errors = getErrorLog()   // Array of error objects
 *   clearErrorLog()                // Wipe stored errors
 */

const STORAGE_KEY = 'meddiagnose_error_log'
const MAX_ERRORS = 50

// ── Internal helpers ──────────────────────────────────────────────────────────

/**
 * Load the current error log from localStorage.
 * Returns an empty array if the key is absent or the stored value is corrupt.
 *
 * @returns {Array<Object>} Stored error entries.
 */
function _loadLog() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

/**
 * Persist the error log to localStorage.
 * Silently ignores QuotaExceededError and similar storage failures.
 *
 * @param {Array<Object>} log - The array to persist.
 */
function _saveLog(log) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(log))
  } catch {
    // Storage full or unavailable — fail silently so tracking never breaks the app.
  }
}

/**
 * Append one error entry to the log, capping the total at MAX_ERRORS.
 * Newest entries are added to the front of the array.
 *
 * @param {Object} entry - Error entry to record.
 */
function _record(entry) {
  const log = _loadLog()
  log.unshift(entry)              // newest first
  if (log.length > MAX_ERRORS) {
    log.splice(MAX_ERRORS)        // discard oldest
  }
  _saveLog(log)
}

/**
 * Safely truncate a string to avoid bloating localStorage with huge stack traces.
 *
 * @param {string|null|undefined} str
 * @param {number} [maxLen=2000]
 * @returns {string}
 */
function _truncate(str, maxLen = 2000) {
  if (!str) return ''
  return str.length > maxLen ? str.slice(0, maxLen) + '…' : str
}

// ── Public API ────────────────────────────────────────────────────────────────

/**
 * Manually capture an error or message.
 * Call this from try/catch blocks or Vue's errorHandler to record
 * caught exceptions alongside the automatically captured ones.
 *
 * @param {Error|string} error - The error to capture.
 * @param {Object} [context={}] - Optional key/value metadata (e.g. component name).
 */
export function captureError(error, context = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    type: 'manual',
    message: _truncate(error instanceof Error ? error.message : String(error)),
    stack: _truncate(error instanceof Error ? error.stack : ''),
    context,
    url: window.location.href,
    userAgent: navigator.userAgent,
  }
  _record(entry)

  // In development, also log to the console for immediate visibility.
  if (import.meta.env.DEV) {
    console.error('[ErrorTracking] Captured error:', entry)
  }
}

/**
 * Retrieve all stored error log entries.
 * Entries are ordered newest-first.
 *
 * @returns {Array<Object>} Up to MAX_ERRORS error entries.
 */
export function getErrorLog() {
  return _loadLog()
}

/**
 * Clear all stored error log entries.
 */
export function clearErrorLog() {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    // Ignore storage errors
  }
}

/**
 * Initialize the global error tracking hooks.
 * Call once at application startup (before mounting the Vue app).
 *
 * Registers:
 *  - window.onerror       — catches synchronous runtime errors
 *  - window.onunhandledrejection — catches unhandled Promise rejections
 */
export function initErrorTracking() {
  // ── Synchronous errors ────────────────────────────────────────────────────
  const _previousOnError = window.onerror

  window.onerror = function (message, source, lineno, colno, error) {
    _record({
      timestamp: new Date().toISOString(),
      type: 'uncaught_error',
      message: _truncate(String(message)),
      stack: _truncate(error instanceof Error ? error.stack : ''),
      source: _truncate(source),
      lineno,
      colno,
      url: window.location.href,
      userAgent: navigator.userAgent,
    })

    // Chain to any previously assigned handler (e.g. from another library).
    if (typeof _previousOnError === 'function') {
      return _previousOnError(message, source, lineno, colno, error)
    }
    // Return false to let the browser's default error handling continue.
    return false
  }

  // ── Unhandled promise rejections ──────────────────────────────────────────
  const _previousOnUnhandledRejection = window.onunhandledrejection

  window.onunhandledrejection = function (event) {
    const reason = event.reason
    _record({
      timestamp: new Date().toISOString(),
      type: 'unhandled_rejection',
      message: _truncate(
        reason instanceof Error
          ? reason.message
          : String(reason ?? 'Unhandled promise rejection'),
      ),
      stack: _truncate(reason instanceof Error ? reason.stack : ''),
      url: window.location.href,
      userAgent: navigator.userAgent,
    })

    // Chain to any previously assigned handler.
    if (typeof _previousOnUnhandledRejection === 'function') {
      return _previousOnUnhandledRejection(event)
    }
  }

  if (import.meta.env.DEV) {
    console.info(
      `[ErrorTracking] Initialized. Storing up to ${MAX_ERRORS} errors in localStorage key "${STORAGE_KEY}".`,
    )
  }
}
