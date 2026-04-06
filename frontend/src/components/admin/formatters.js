/**
 * Shared formatting utilities for the admin UI.
 */

/**
 * Returns a human-readable relative time string (e.g. "3m ago", "2h ago").
 * @param {string|number|Date} ts - Timestamp
 * @returns {string}
 */
export function relativeTime(ts) {
  if (!ts) return ''
  const now = Date.now()
  const then = new Date(ts).getTime()
  const diffMs = now - then
  if (isNaN(diffMs)) return String(ts)

  const seconds = Math.floor(diffMs / 1000)
  if (seconds < 5) return 'just now'
  if (seconds < 60) return `${seconds}s ago`

  const minutes = Math.floor(seconds / 60)
  if (minutes < 60) return `${minutes}m ago`

  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}h ago`

  const days = Math.floor(hours / 24)
  if (days < 30) return `${days}d ago`

  const months = Math.floor(days / 30)
  return `${months}mo ago`
}

/**
 * Format milliseconds into a readable duration string.
 * @param {number} ms
 * @returns {string}
 */
export function formatDuration(ms) {
  if (ms == null || isNaN(ms)) return '--'
  if (ms < 1000) return `${Math.round(ms)}ms`
  const seconds = ms / 1000
  if (seconds < 60) return `${seconds.toFixed(1)}s`
  const minutes = Math.floor(seconds / 60)
  const remainSec = Math.round(seconds % 60)
  return `${minutes}m ${remainSec}s`
}

/**
 * Format bytes into human-readable size (KB, MB, GB).
 * @param {number} bytes
 * @returns {string}
 */
export function formatBytes(bytes) {
  if (bytes == null || isNaN(bytes)) return '--'
  if (bytes === 0) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  const value = bytes / Math.pow(1024, i)
  return `${value.toFixed(i === 0 ? 0 : 1)} ${units[i]}`
}

/**
 * Format a number with commas (e.g. 1,234,567).
 * @param {number} n
 * @returns {string}
 */
export function formatNumber(n) {
  if (n == null || isNaN(n)) return '--'
  return Number(n).toLocaleString('en-US')
}

/**
 * Format a number as USD currency.
 * @param {number} n
 * @returns {string}
 */
export function formatCurrency(n) {
  if (n == null || isNaN(n)) return '--'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}
