/**
 * Central Feature Flags — controls all new features.
 * All new features MUST be toggleable via this config.
 * Reads from localStorage for runtime toggling, falls back to defaults.
 */

const DEFAULTS = {
  enhancedUI: true,           // Enhanced report shell with visual hierarchy
  systemDashboard: true,      // System insight dashboard in admin
  agentOrchestration: true,   // Agent orchestration wrapper with structured output
  adminV2: true,              // V2 admin modules (analytics, logs, reports, config)
  enhancedPrompt: true,       // V2 diagnosis prompts with structured sections
  globalLoadingSystem: true,  // Global loading store + error boundaries
}

const STORAGE_KEY = 'meddiagnose_feature_flags'

function loadFlags() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) return { ...DEFAULTS, ...JSON.parse(stored) }
  } catch {}
  return { ...DEFAULTS }
}

let _flags = loadFlags()

export function getFlag(name) {
  return _flags[name] ?? DEFAULTS[name] ?? false
}

export function setFlag(name, value) {
  _flags[name] = value
  localStorage.setItem(STORAGE_KEY, JSON.stringify(_flags))
}

export function getAllFlags() {
  return { ..._flags }
}

export function resetFlags() {
  _flags = { ...DEFAULTS }
  localStorage.removeItem(STORAGE_KEY)
}

export { DEFAULTS as FLAG_DEFAULTS }
