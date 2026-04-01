/**
 * HIPAA-Compliant Crypto Service
 *
 * Provides AES-256-GCM encryption/decryption with PBKDF2 key derivation
 * using the native Web Crypto API. Zero external dependencies.
 *
 * The session key lives only in module-scoped memory — never persisted.
 * On logout or tab close, the key is cleared and localStorage PHI
 * remains encrypted at rest.
 */

const PBKDF2_ITERATIONS = 600_000 // OWASP 2023 recommendation
const SALT_BYTES = 16
const IV_BYTES = 12 // AES-GCM standard
const KEY_ALGO = 'AES-GCM'
const KEY_LENGTH = 256

// ── Module-scoped session key (never persisted) ──────────────
let _sessionKey = null

/**
 * Generate a cryptographically random salt.
 * @returns {string} Base64-encoded 16-byte salt
 */
export function generateSalt() {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_BYTES))
  return _arrayToBase64(salt)
}

/**
 * Derive an AES-256-GCM CryptoKey from a password + salt using PBKDF2.
 * @param {string} password - User's plaintext password (only available at login time)
 * @param {string} saltB64 - Base64-encoded salt from localStorage
 * @returns {Promise<CryptoKey>}
 */
export async function deriveKey(password, saltB64) {
  const encoder = new TextEncoder()
  const salt = _base64ToArray(saltB64)

  // Import password as raw key material
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    encoder.encode(password),
    'PBKDF2',
    false,
    ['deriveKey']
  )

  // Derive AES-GCM key
  return crypto.subtle.deriveKey(
    {
      name: 'PBKDF2',
      salt,
      iterations: PBKDF2_ITERATIONS,
      hash: 'SHA-256',
    },
    keyMaterial,
    { name: KEY_ALGO, length: KEY_LENGTH },
    false, // not extractable
    ['encrypt', 'decrypt']
  )
}

/**
 * Encrypt plaintext string with AES-256-GCM.
 * @param {string} plaintext
 * @param {CryptoKey} key
 * @returns {Promise<{iv: string, ct: string}>} Base64-encoded IV and ciphertext
 */
export async function encrypt(plaintext, key) {
  const encoder = new TextEncoder()
  const iv = crypto.getRandomValues(new Uint8Array(IV_BYTES))

  const ciphertext = await crypto.subtle.encrypt(
    { name: KEY_ALGO, iv },
    key,
    encoder.encode(plaintext)
  )

  return {
    iv: _arrayToBase64(iv),
    ct: _arrayToBase64(new Uint8Array(ciphertext)),
  }
}

/**
 * Decrypt AES-256-GCM ciphertext.
 * @param {{iv: string, ct: string}} encrypted - Base64-encoded IV and ciphertext
 * @param {CryptoKey} key
 * @returns {Promise<string>} Decrypted plaintext
 * @throws {Error} If key is wrong or data is tampered (GCM auth tag fails)
 */
export async function decrypt(encrypted, key) {
  const iv = _base64ToArray(encrypted.iv)
  const ct = _base64ToArray(encrypted.ct)

  const plaintext = await crypto.subtle.decrypt(
    { name: KEY_ALGO, iv },
    key,
    ct
  )

  return new TextDecoder().decode(plaintext)
}

// ── Session key management ───────────────────────────────────

/** Store the derived key in memory for this session. */
export function setSessionKey(key) {
  _sessionKey = key
}

/** Get the current session key (null if not logged in). */
export function getSessionKey() {
  return _sessionKey
}

/** Clear the session key from memory (called on logout). */
export function clearSessionKey() {
  _sessionKey = null
}

/** Check if a session key is available (user is logged in and key derived). */
export function isUnlocked() {
  return _sessionKey !== null
}

// ── Helpers ──────────────────────────────────────────────────

function _arrayToBase64(arr) {
  return btoa(String.fromCharCode(...arr))
}

function _base64ToArray(b64) {
  const bin = atob(b64)
  const arr = new Uint8Array(bin.length)
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i)
  return arr
}
