/**
 * Encrypted Storage Service
 *
 * Wraps localStorage with AES-256-GCM encryption for PHI data.
 * All Tier 2 (local PHI) data flows through this service.
 * Returns safe defaults when the crypto session is locked.
 */

import {
  encrypt,
  decrypt,
  getSessionKey,
  isUnlocked,
  generateSalt,
  deriveKey,
} from './cryptoService.js'

const ENC_PREFIX = 'enc_'
const SALT_KEY = 'encryption_salt'
const VERSION_KEY = 'encryption_version'
const CURRENT_VERSION = '1'

// Keys that contain PHI and must be encrypted
const PHI_KEYS = [
  'user_profile',
  'diagnosis_history',
  'latest_diagnosis_result',
  'finalDiagnosis',
  'chatHistory',
  'anthropic_api_key',
  'openai_api_key',
  'google_api_key',
]

// ── Core encrypted read/write ────────────────────────────────

/**
 * Read and decrypt a value from encrypted localStorage.
 * Returns null if locked, key doesn't exist, or decryption fails.
 */
export async function getEncrypted(key) {
  if (!isUnlocked()) return null

  const raw = localStorage.getItem(ENC_PREFIX + key)
  if (!raw) return null

  try {
    const parsed = JSON.parse(raw)
    if (!parsed.iv || !parsed.ct) return null
    const plaintext = await decrypt(parsed, getSessionKey())
    return JSON.parse(plaintext)
  } catch {
    // Decryption failed (wrong key, tampered data, or corrupt)
    return null
  }
}

/**
 * Encrypt and store a value in localStorage.
 * No-ops if the session is locked.
 */
export async function setEncrypted(key, data) {
  if (!isUnlocked()) return

  const plaintext = JSON.stringify(data)
  const encrypted = await encrypt(plaintext, getSessionKey())
  localStorage.setItem(ENC_PREFIX + key, JSON.stringify(encrypted))
}

/**
 * Remove an encrypted key from localStorage.
 */
export function removeEncrypted(key) {
  localStorage.removeItem(ENC_PREFIX + key)
}

// ── Profile ──────────────────────────────────────────────────

const DEFAULT_PROFILE = {
  id: '',
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
  createdAt: '',
}

export async function getEncryptedProfile() {
  const data = await getEncrypted('user_profile')
  return data ? { ...DEFAULT_PROFILE, ...data } : { ...DEFAULT_PROFILE }
}

export async function saveEncryptedProfile(profile) {
  await setEncrypted('user_profile', profile)
}

// ── Diagnosis History ────────────────────────────────────────

const MAX_SESSIONS = 20

export async function getEncryptedHistory() {
  const data = await getEncrypted('diagnosis_history')
  return Array.isArray(data) ? data : []
}

export async function saveEncryptedSession(session) {
  const history = await getEncryptedHistory()
  // Upsert by id
  const idx = history.findIndex(s => s.id === session.id)
  if (idx >= 0) {
    history[idx] = session
  } else {
    history.unshift(session)
  }
  // Cap at max sessions
  await setEncrypted('diagnosis_history', history.slice(0, MAX_SESSIONS))
}

export async function deleteEncryptedSession(id) {
  const history = await getEncryptedHistory()
  await setEncrypted('diagnosis_history', history.filter(s => s.id !== id))
}

export async function clearEncryptedHistory() {
  removeEncrypted('diagnosis_history')
}

// ── Latest Diagnosis ─────────────────────────────────────────

export async function getEncryptedLatestDiagnosis() {
  return await getEncrypted('latest_diagnosis_result')
}

export async function saveEncryptedLatestDiagnosis(result) {
  await setEncrypted('latest_diagnosis_result', result)
}

// ── API Keys ─────────────────────────────────────────────────

export async function getEncryptedApiKey(provider) {
  return await getEncrypted(`${provider}_api_key`)
}

export async function saveEncryptedApiKey(provider, key) {
  await setEncrypted(`${provider}_api_key`, key)
}

export async function removeEncryptedApiKey(provider) {
  removeEncrypted(`${provider}_api_key`)
}

/**
 * Get all API keys as an object. Used by api.js getAuthHeaders().
 */
export async function getAllEncryptedApiKeys() {
  const [anthropic, openai, google] = await Promise.all([
    getEncryptedApiKey('anthropic'),
    getEncryptedApiKey('openai'),
    getEncryptedApiKey('google'),
  ])
  return { anthropic, openai, google }
}

// ── Salt Management ──────────────────────────────────────────

/**
 * Get or create the encryption salt for this browser.
 */
export function getOrCreateSalt() {
  let salt = localStorage.getItem(SALT_KEY)
  if (!salt) {
    salt = generateSalt()
    localStorage.setItem(SALT_KEY, salt)
    localStorage.setItem(VERSION_KEY, CURRENT_VERSION)
  }
  return salt
}

// ── Clear All Encrypted Data ─────────────────────────────────

/**
 * Wipe all encrypted localStorage keys and the salt.
 * Called from Settings "Clear all local health data".
 */
export function clearAllEncryptedData() {
  for (const key of PHI_KEYS) {
    localStorage.removeItem(ENC_PREFIX + key)
  }
  // Also clear any other enc_ keys
  const toRemove = []
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i)
    if (k && k.startsWith(ENC_PREFIX)) toRemove.push(k)
  }
  toRemove.forEach(k => localStorage.removeItem(k))
  localStorage.removeItem(SALT_KEY)
  localStorage.removeItem(VERSION_KEY)
}

// ── Data Migration (one-time plaintext → encrypted) ──────────

/**
 * Migrate existing plaintext localStorage data to encrypted storage.
 * Called once after first login post-update.
 */
export async function migrateToEncryptedStorage() {
  if (!isUnlocked()) return

  let migrated = false

  for (const key of PHI_KEYS) {
    const plaintext = localStorage.getItem(key)
    const encrypted = localStorage.getItem(ENC_PREFIX + key)

    if (plaintext && !encrypted) {
      try {
        const data = JSON.parse(plaintext)
        await setEncrypted(key, data)
        localStorage.removeItem(key)
        migrated = true
      } catch {
        // Not valid JSON — just remove it
        localStorage.removeItem(key)
      }
    }
  }

  // Remove insecure saved accounts
  localStorage.removeItem('user_accounts')

  if (migrated) {
    console.info('[HIPAA] Migrated plaintext data to encrypted storage')
  }
}

// ── Re-encryption (password change) ──────────────────────────

/**
 * Re-encrypt all local PHI data with a new key.
 * Used during password change.
 * @param {CryptoKey} oldKey
 * @param {CryptoKey} newKey
 */
export async function reEncryptAll(oldKey, newKey) {
  const keysToReEncrypt = []

  // Collect all enc_ keys
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i)
    if (k && k.startsWith(ENC_PREFIX)) keysToReEncrypt.push(k)
  }

  // Decrypt with old, encrypt with new
  for (const fullKey of keysToReEncrypt) {
    const raw = localStorage.getItem(fullKey)
    if (!raw) continue

    try {
      const parsed = JSON.parse(raw)
      const plaintext = await decrypt(parsed, oldKey)
      const data = JSON.parse(plaintext)
      const reEncrypted = await encrypt(JSON.stringify(data), newKey)
      localStorage.setItem(fullKey, JSON.stringify(reEncrypted))
    } catch {
      // If decryption fails, skip this key (may already be re-encrypted)
    }
  }
}
