/**
 * Shared status, priority, and log-level color constants for the admin UI.
 * All values are Tailwind CSS classes.
 */

export const STATUS_COLORS = {
  healthy: { bg: 'bg-emerald-500/10', text: 'text-emerald-500', dot: 'bg-emerald-500', border: 'border-emerald-500/20' },
  running: { bg: 'bg-emerald-500/10', text: 'text-emerald-500', dot: 'bg-emerald-500', border: 'border-emerald-500/20' },
  degraded: { bg: 'bg-amber-500/10', text: 'text-amber-500', dot: 'bg-amber-500', border: 'border-amber-500/20' },
  error: { bg: 'bg-red-500/10', text: 'text-red-500', dot: 'bg-red-500', border: 'border-red-500/20' },
  failing: { bg: 'bg-red-500/10', text: 'text-red-500', dot: 'bg-red-500', border: 'border-red-500/20' },
  idle: { bg: 'bg-slate-500/10', text: 'text-slate-500', dot: 'bg-slate-500', border: 'border-slate-500/20' },
  paused: { bg: 'bg-purple-500/10', text: 'text-purple-500', dot: 'bg-purple-500', border: 'border-purple-500/20' },
  retrying: { bg: 'bg-yellow-500/10', text: 'text-yellow-500', dot: 'bg-yellow-500', border: 'border-yellow-500/20' },
  unknown: { bg: 'bg-slate-500/10', text: 'text-slate-400', dot: 'bg-slate-400', border: 'border-slate-500/20' }
}

export const PRIORITY_COLORS = {
  critical: { bg: 'bg-red-500/10', text: 'text-red-500', dot: 'bg-red-500', border: 'border-red-500/20' },
  high: { bg: 'bg-orange-500/10', text: 'text-orange-500', dot: 'bg-orange-500', border: 'border-orange-500/20' },
  medium: { bg: 'bg-amber-500/10', text: 'text-amber-500', dot: 'bg-amber-500', border: 'border-amber-500/20' },
  low: { bg: 'bg-blue-500/10', text: 'text-blue-500', dot: 'bg-blue-500', border: 'border-blue-500/20' }
}

export const LOG_LEVEL_COLORS = {
  debug: { bg: 'bg-slate-500/10', text: 'text-slate-400', dot: 'bg-slate-400' },
  info: { bg: 'bg-blue-500/10', text: 'text-blue-500', dot: 'bg-blue-500' },
  warning: { bg: 'bg-amber-500/10', text: 'text-amber-500', dot: 'bg-amber-500' },
  error: { bg: 'bg-red-500/10', text: 'text-red-500', dot: 'bg-red-500' }
}

/**
 * Get color classes for a status string.
 * Falls back to 'unknown' if status not recognized.
 */
export function getStatusColor(status) {
  return STATUS_COLORS[status] || STATUS_COLORS.unknown
}

/**
 * Get color classes for a priority string.
 * Falls back to 'low'.
 */
export function getPriorityColor(priority) {
  return PRIORITY_COLORS[priority] || PRIORITY_COLORS.low
}

/**
 * Get color classes for a log level.
 * Falls back to 'info'.
 */
export function getLogLevelColor(level) {
  return LOG_LEVEL_COLORS[level] || LOG_LEVEL_COLORS.info
}

/**
 * Derive agent health status from error count.
 * 0 errors = healthy, 1-2 = degraded, 3+ = failing.
 */
export function deriveAgentHealth(errorCount) {
  if (errorCount === 0) return 'healthy'
  if (errorCount <= 2) return 'degraded'
  return 'failing'
}
