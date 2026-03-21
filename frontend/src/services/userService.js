const PROFILE_KEY = 'user_profile'
const PREFERENCES_KEY = 'user_preferences'
const HISTORY_KEY = 'diagnosis_history'
const ACCOUNTS_KEY = 'user_accounts'

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
    city: '',
    stateRegion: '',
    zipCode: '',
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
    // Keep accounts list in sync
    if (merged.name && merged.email) {
      saveAccountToList(merged)
    }
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
 * Get all saved accounts from localStorage.
 * @returns {Array} List of saved account profiles
 */
export function getSavedAccounts() {
  try {
    const raw = localStorage.getItem(ACCOUNTS_KEY)
    if (raw) return JSON.parse(raw)
  } catch (e) {
    console.error('Failed to read saved accounts:', e)
  }
  return []
}

/**
 * Save or update an account in the accounts list.
 * @param {Object} profile - The profile to save
 */
export function saveAccountToList(profile) {
  try {
    const accounts = getSavedAccounts()
    const idx = accounts.findIndex(a => a.email && a.email === profile.email)
    if (idx >= 0) {
      accounts[idx] = { ...accounts[idx], ...profile }
    } else {
      accounts.push(profile)
    }
    localStorage.setItem(ACCOUNTS_KEY, JSON.stringify(accounts))
  } catch (e) {
    console.error('Failed to save account to list:', e)
  }
}

/**
 * Remove an account from the saved accounts list.
 * @param {string} email - The email of the account to remove
 */
export function removeAccount(email) {
  try {
    const accounts = getSavedAccounts().filter(a => a.email !== email)
    localStorage.setItem(ACCOUNTS_KEY, JSON.stringify(accounts))
  } catch (e) {
    console.error('Failed to remove account:', e)
  }
}

/**
 * Log in with an existing saved account by email.
 * @param {string} email - The email to log in with
 * @returns {Object|null} The profile if found, null otherwise
 */
export function loginWithEmail(email) {
  const accounts = getSavedAccounts()
  const account = accounts.find(a => a.email && a.email.toLowerCase() === email.toLowerCase())
  if (account) {
    localStorage.setItem(PROFILE_KEY, JSON.stringify(account))
    return account
  }
  return null
}

/**
 * Remove active session (profile and preferences) but keep saved accounts.
 */
export function clearUserData() {
  try {
    // Save current profile to accounts list before clearing
    const profile = getProfile()
    if (profile.name && profile.email) {
      saveAccountToList(profile)
    }
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
