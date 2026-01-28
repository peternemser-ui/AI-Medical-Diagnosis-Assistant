/**
 * Utility functions for formatting data
 */

/**
 * Format a date to a human-readable string
 */
export function formatDate(date, options = {}) {
  const d = new Date(date)
  const { format = 'medium', locale = 'en-US' } = options

  const formats = {
    short: { month: 'short', day: 'numeric' },
    medium: { month: 'short', day: 'numeric', year: 'numeric' },
    long: { month: 'long', day: 'numeric', year: 'numeric' },
    full: { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }
  }

  return d.toLocaleDateString(locale, formats[format] || formats.medium)
}

/**
 * Format a date to relative time (e.g., "2 hours ago")
 */
export function formatRelativeTime(date) {
  const now = new Date()
  const d = new Date(date)
  const diff = now - d
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (seconds < 60) return 'just now'
  if (minutes < 60) return `${minutes} minute${minutes !== 1 ? 's' : ''} ago`
  if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''} ago`

  return formatDate(date, { format: 'medium' })
}

/**
 * Format a number with thousands separators
 */
export function formatNumber(num, options = {}) {
  const { locale = 'en-US', decimals = 0 } = options
  return new Intl.NumberFormat(locale, {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(num)
}

/**
 * Format a percentage
 */
export function formatPercent(value, decimals = 0) {
  return `${formatNumber(value, { decimals })}%`
}

/**
 * Format bytes to human-readable size
 */
export function formatBytes(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i]
}

/**
 * Format phone number
 */
export function formatPhone(phone) {
  const cleaned = ('' + phone).replace(/\D/g, '')
  const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/)
  if (match) return '(' + match[1] + ') ' + match[2] + '-' + match[3]
  return phone
}

/**
 * Truncate text with ellipsis
 */
export function truncate(text, length = 100, suffix = '...') {
  if (!text || text.length <= length) return text
  return text.substring(0, length).trim() + suffix
}

/**
 * Capitalize first letter
 */
export function capitalize(str) {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

/**
 * Convert string to title case
 */
export function titleCase(str) {
  if (!str) return ''
  return str.toLowerCase().split(' ').map(word => capitalize(word)).join(' ')
}

/**
 * Format duration in milliseconds to human-readable
 */
export function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)

  if (hours > 0) return `${hours}h ${minutes % 60}m`
  if (minutes > 0) return `${minutes}m ${seconds % 60}s`
  return `${seconds}s`
}

/**
 * Format urgency level with color
 */
export function formatUrgency(level) {
  const levels = {
    routine: { label: 'Routine', color: 'green' },
    soon: { label: 'Soon', color: 'yellow' },
    urgent: { label: 'Urgent', color: 'orange' },
    emergency: { label: 'Emergency', color: 'red' }
  }
  return levels[level] || levels.routine
}
