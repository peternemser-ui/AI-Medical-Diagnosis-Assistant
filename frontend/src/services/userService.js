const PROFILE_KEY = 'user_profile'
const PREFERENCES_KEY = 'user_preferences'
const HISTORY_KEY = 'diagnosis_history'

/**
 * Generate a UUID using crypto.randomUUID() with fallback
 */
function generateUUID() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  // Fallback for older browsers
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

/**
 * Returns default profile shape
 */
function defaultProfile() {
  return {
    id: generateUUID(),
    name: '',
    email: '',
    avatarUrl: '',
    dateOfBirth: '',
    gender: '',
    bloodType: '',
    allergies: [],
    medications: [],
    emergencyContact: '',
    createdAt: new Date().toISOString(),
  }
}

/**
 * Returns default preferences shape
 */
function defaultPreferences() {
  return {
    theme: 'dark',
    language: 'en',
    voiceInput: true,
    audioResponses: false,
    speechRate: 0.95,
    autoScroll: true,
    soundEffects: true,
    notifications: false,
  }
}

/**
 * Get user profile from localStorage, creating a default if none exists.
 * @returns {Object} The user profile object
 */
export function getProfile() {
  try {
    const raw = localStorage.getItem(PROFILE_KEY)
    if (raw) {
      return { ...defaultProfile(), ...JSON.parse(raw) }
    }
  } catch (e) {
    console.error('Failed to read user profile:', e)
  }
  return defaultProfile()
}

/**
 * Merge data into the existing profile and save to localStorage.
 * @param {Object} data - Partial profile fields to merge
 */
export function saveProfile(data) {
  try {
    const current = getProfile()
    const merged = { ...current, ...data }
    localStorage.setItem(PROFILE_KEY, JSON.stringify(merged))
    return merged
  } catch (e) {
    console.error('Failed to save user profile:', e)
  }
}

/**
 * Get user preferences from localStorage, creating defaults if none exist.
 * @returns {Object} The preferences object
 */
export function getPreferences() {
  try {
    const raw = localStorage.getItem(PREFERENCES_KEY)
    if (raw) {
      return { ...defaultPreferences(), ...JSON.parse(raw) }
    }
  } catch (e) {
    console.error('Failed to read user preferences:', e)
  }
  return defaultPreferences()
}

/**
 * Save a single preference by key.
 * @param {string} key - Preference key
 * @param {*} value - Preference value
 */
export function savePreference(key, value) {
  try {
    const current = getPreferences()
    current[key] = value
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify(current))
    return current
  } catch (e) {
    console.error('Failed to save preference:', e)
  }
}

/**
 * Merge multiple preferences and save.
 * @param {Object} data - Partial preferences to merge
 */
export function savePreferences(data) {
  try {
    const current = getPreferences()
    const merged = { ...current, ...data }
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify(merged))
    return merged
  } catch (e) {
    console.error('Failed to save preferences:', e)
  }
}

/**
 * Check if the user profile is considered complete.
 * @returns {boolean} True if name is set
 */
export function isProfileComplete() {
  const profile = getProfile()
  return !!(profile.name && profile.name.trim().length > 0)
}

/**
 * Remove all user data (profile and preferences) from localStorage.
 */
export function clearUserData() {
  try {
    localStorage.removeItem(PROFILE_KEY)
    localStorage.removeItem(PREFERENCES_KEY)
  } catch (e) {
    console.error('Failed to clear user data:', e)
  }
}

/**
 * Export all user data as a JSON object (profile, preferences, and session history).
 * @returns {Object} Combined data export
 */
export function exportAllData() {
  const profile = getProfile()
  const preferences = getPreferences()

  let sessions = []
  try {
    const raw = localStorage.getItem(HISTORY_KEY)
    if (raw) {
      sessions = JSON.parse(raw)
    }
  } catch (e) {
    console.error('Failed to read session history for export:', e)
  }

  return {
    profile,
    preferences,
    sessions,
    exportedAt: new Date().toISOString(),
  }
}
