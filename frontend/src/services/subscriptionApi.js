/**
 * Subscription API service — communicates with the subscription endpoints.
 */

import { getAccessToken } from './authService'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

function authHeaders() {
  const headers = { 'Content-Type': 'application/json' }
  const token = getAccessToken()
  if (token) headers['Authorization'] = `Bearer ${token}`
  return headers
}

/** Get current subscription status (tier + usage). */
export async function getSubscriptionStatus() {
  const res = await fetch(`${API_BASE_URL}/api/subscription/status`, {
    headers: authHeaders(),
  })
  if (!res.ok) throw new Error(`Subscription status failed: ${res.status}`)
  return res.json()
}

/** Check if the user can use a feature or model. */
export async function checkSubscription({ feature, model } = {}) {
  const res = await fetch(`${API_BASE_URL}/api/subscription/check`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({ feature, model }),
  })
  if (!res.ok) throw new Error(`Subscription check failed: ${res.status}`)
  return res.json()
}

/** Get all available tiers (public). */
export async function getTiers() {
  const res = await fetch(`${API_BASE_URL}/api/subscription/tiers`)
  if (!res.ok) throw new Error(`Fetching tiers failed: ${res.status}`)
  return res.json()
}

/** Upgrade to a new tier. */
export async function upgradeTier(tier) {
  const res = await fetch(`${API_BASE_URL}/api/subscription/upgrade`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({ tier }),
  })
  if (!res.ok) throw new Error(`Upgrade failed: ${res.status}`)
  return res.json()
}
