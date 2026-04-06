/**
 * Authentication service — JWT-based auth with refresh tokens.
 *
 * Tokens are stored in localStorage:
 *   access_token  — short-lived JWT (15 min)
 *   refresh_token — long-lived JWT (7 days), hashed server-side
 *
 * HIPAA: On login/signup, a PBKDF2-derived AES key is created from
 * the password and held in memory only. All PHI in localStorage is
 * encrypted with this key. On logout the key is cleared.
 */

import { deriveKey, setSessionKey, clearSessionKey } from './cryptoService.js'
import { getOrCreateSalt, migrateToEncryptedStorage } from './encryptedStorage.js'
import { loadApiKeysToCache, clearApiKeyCache } from './api.js'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

// ---------------------------------------------------------------------------
// Token storage
// ---------------------------------------------------------------------------

export function getAccessToken() {
  return localStorage.getItem('access_token')
}

export function getRefreshTokenValue() {
  return localStorage.getItem('refresh_token')
}

function storeTokens(access, refresh) {
  localStorage.setItem('access_token', access)
  if (refresh) localStorage.setItem('refresh_token', refresh)
}

function clearTokens() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('auth_user')
}

// ---------------------------------------------------------------------------
// JWT decode (no verification — that's server-side)
// ---------------------------------------------------------------------------

function decodeJWT(token) {
  try {
    const payload = token.split('.')[1]
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')))
  } catch {
    return null
  }
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Sign up a new account.
 */
export async function signup(name, email, password) {
  const res = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password }),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    const detail = err.detail
    const msg = typeof detail === 'string' ? detail
      : Array.isArray(detail) ? detail.map(d => d.msg || d.message || JSON.stringify(d)).join('; ')
      : `Signup failed (${res.status})`
    throw new Error(msg)
  }

  const data = await res.json()
  storeTokens(data.access_token, data.refresh_token)

  // Store only non-PHI user info
  const { id, email: userEmail, name: userName, role } = data.user || {}
  localStorage.setItem('auth_user', JSON.stringify({ id, email: userEmail, name: userName, role }))

  // HIPAA: Derive encryption key from password for local PHI storage
  const salt = getOrCreateSalt()
  const cryptoKey = await deriveKey(password, salt)
  setSessionKey(cryptoKey)
  await loadApiKeysToCache()

  return data
}

/**
 * Log in with email + password.
 */
export async function login(email, password) {
  const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Login failed (${res.status})`)
  }

  const data = await res.json()
  storeTokens(data.access_token, data.refresh_token)

  // Store only non-PHI user info
  const { id, email: userEmail, name: userName, role } = data.user || {}
  localStorage.setItem('auth_user', JSON.stringify({ id, email: userEmail, name: userName, role }))

  // HIPAA: Derive encryption key from password for local PHI storage
  const salt = getOrCreateSalt()
  const cryptoKey = await deriveKey(password, salt)
  setSessionKey(cryptoKey)

  // Migrate any existing plaintext data to encrypted storage
  await migrateToEncryptedStorage()
  await loadApiKeysToCache()

  return data
}

/**
 * Refresh the access token using the stored refresh token.
 * Returns the new access token or null on failure.
 */
export async function refreshToken() {
  const refresh = getRefreshTokenValue()
  if (!refresh) return null

  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refresh }),
    })

    if (!res.ok) {
      clearTokens()
      return null
    }

    const data = await res.json()
    localStorage.setItem('access_token', data.access_token)
    return data.access_token
  } catch {
    clearTokens()
    return null
  }
}

/**
 * Log out — revoke server session and clear local tokens.
 */
export async function logout() {
  // HIPAA: Clear encryption key and cached API keys from memory
  clearSessionKey()
  clearApiKeyCache()

  const token = getAccessToken()
  if (token) {
    try {
      await fetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      })
    } catch {
      // Best-effort server logout
    }
  }
  clearTokens()
}

/**
 * Check if the user is currently authenticated (has a non-expired access token).
 */
export function isAuthenticated() {
  const token = getAccessToken()
  if (!token) return false

  const payload = decodeJWT(token)
  if (!payload || !payload.exp) return false

  // Check expiry with 30-second buffer
  return payload.exp * 1000 > Date.now() - 30000
}

/**
 * Get the current user from the stored JWT (decoded client-side).
 * For a verified user object, call fetchCurrentUser().
 */
export function getCurrentUser() {
  try {
    const stored = localStorage.getItem('auth_user')
    if (stored) return JSON.parse(stored)
  } catch { /* ignore */ }

  const token = getAccessToken()
  if (!token) return null

  const payload = decodeJWT(token)
  if (!payload) return null

  return { id: payload.sub, role: payload.role }
}

/**
 * Fetch the verified current user profile from the server.
 */
export async function fetchCurrentUser() {
  const token = getAccessToken()
  if (!token) return null

  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    })
    if (!res.ok) return null
    const data = await res.json()
    localStorage.setItem('auth_user', JSON.stringify(data.user))
    return data.user
  } catch {
    return null
  }
}
