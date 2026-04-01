/**
 * User Service — HIPAA-compliant profile and preferences management.
 *
 * PHI (profile with medical data) is stored encrypted in localStorage
 * via encryptedStorage. Preferences (theme, language) are non-PHI
 * and stored as plaintext localStorage.
 *
 * The old "saved accounts" / passwordless login system has been removed.
 * All auth now goes through backend JWT (authService.js).
 */

import { isUnlocked } from './cryptoService.js'
import {
  getEncryptedProfile,
  saveEncryptedProfile,
  clearAllEncryptedData,
  getEncryptedHistory,
} from './encryptedStorage.js'

const PREFERENCES_KEY = 'user_preferences'

// ── Helpers ──────────────────────────────────────────────────

function generateUUID() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID()
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

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

// ── Profile (PHI — encrypted) ────────────────────────────────

/**
 * Get user profile. Returns encrypted profile if unlocked,
 * otherwise returns default (no PHI exposed).
 *
 * NOTE: This is now async because it reads from encrypted storage.
 * Callers that previously used getProfile() synchronously may need
 * to be updated. For backward compatibility, a sync fallback reads
 * from the auth_user cache (non-PHI fields only).
 */
export async function getProfileAsync() {
  if (isUnlocked()) {
    return await getEncryptedProfile()
  }
  // Fallback: return non-PHI fields from auth cache
  return _getAuthUserAsProfile()
}

/**
 * Synchronous profile getter — reads from plaintext localStorage
 * (user_profile or auth_user cache). Use getProfileAsync() for
 * full PHI-inclusive profile from encrypted storage.
 */
export function getProfile() {
  try {
    // Try full plaintext profile first (pre-migration or fallback)
    const raw = localStorage.getItem('user_profile')
    if (raw) return { ...defaultProfile(), ...JSON.parse(raw) }

    // Fallback: auth_user cache (non-PHI fields)
    const authRaw = localStorage.getItem('auth_user')
    if (authRaw) {
      const user = JSON.parse(authRaw)
      return { ...defaultProfile(), name: user.name || '', email: user.email || '', id: user.id || '' }
    }
  } catch { /* ignore */ }
  return defaultProfile()
}

/**
 * Save profile data. Uses encrypted storage when unlocked,
 * falls back to plaintext localStorage for backward compatibility.
 */
export async function saveProfile(data) {
  const defaultP = defaultProfile()

  if (isUnlocked()) {
    // HIPAA path: save full profile encrypted
    const current = await getEncryptedProfile()
    const merged = { ...current, ...data }
    await saveEncryptedProfile(merged)
    return merged
  }

  // Fallback: save to plaintext localStorage (will be migrated on next login)
  try {
    const raw = localStorage.getItem('user_profile')
    const current = raw ? { ...defaultP, ...JSON.parse(raw) } : defaultP
    const merged = { ...current, ...data }
    localStorage.setItem('user_profile', JSON.stringify(merged))

    // Also update auth_user cache with non-PHI fields
    _updateAuthUserCache(merged)

    return merged
  } catch {
    return null
  }
}

function _updateAuthUserCache(profile) {
  try {
    const raw = localStorage.getItem('auth_user')
    const authUser = raw ? JSON.parse(raw) : {}
    authUser.name = profile.name || authUser.name
    authUser.email = profile.email || authUser.email
    localStorage.setItem('auth_user', JSON.stringify(authUser))
  } catch { /* ignore */ }
}

// ── Preferences (non-PHI — plaintext) ────────────────────────

export function getPreferences() {
  try {
    const raw = localStorage.getItem(PREFERENCES_KEY)
    if (raw) return { ...defaultPreferences(), ...JSON.parse(raw) }
  } catch { /* ignore */ }
  return defaultPreferences()
}

export function savePreference(key, value) {
  try {
    const current = getPreferences()
    current[key] = value
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify(current))
    return current
  } catch { /* ignore */ }
}

export function savePreferences(data) {
  try {
    const current = getPreferences()
    const merged = { ...current, ...data }
    localStorage.setItem(PREFERENCES_KEY, JSON.stringify(merged))
    return merged
  } catch { /* ignore */ }
}

// ── Profile completeness check ───────────────────────────────

export function isProfileComplete() {
  const profile = getProfile()
  return !!(profile.name && profile.name.trim().length > 0)
}

// ── Data management ──────────────────────────────────────────

/**
 * Clear all local user data (encrypted PHI + preferences).
 */
export function clearUserData() {
  clearAllEncryptedData()
  localStorage.removeItem(PREFERENCES_KEY)
}

/**
 * Export all user data as JSON. Only works when session is unlocked.
 */
export async function exportAllData() {
  if (!isUnlocked()) {
    return { error: 'Session locked — log in to export data' }
  }

  const profile = await getEncryptedProfile()
  const preferences = getPreferences()
  const sessions = await getEncryptedHistory()

  return {
    profile,
    preferences,
    sessions,
    exportedAt: new Date().toISOString(),
  }
}
