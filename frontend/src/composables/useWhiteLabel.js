/**
 * White-Label composable -- loads config from backend and provides
 * reactive brand values that components can use instead of hardcoded strings.
 */

import { ref, readonly, onMounted } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const config = ref({
  brand_name: 'MedDiagnose AI',
  tagline: 'Multi-agent clinical analysis',
  logo_url: null,
  primary_color: '#3b82f6',
  accent_color: '#8b5cf6',
  contact_email: '',
  contact_phone: '',
  disclaimer: 'This AI-generated assessment is for informational purposes only.',
  powered_by: true,
})

const loaded = ref(false)
const error = ref(null)

async function fetchConfig() {
  try {
    const resp = await fetch(`${API_BASE_URL}/api/whitelabel/config`)
    if (resp.ok) {
      const data = await resp.json()
      config.value = { ...config.value, ...data }
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loaded.value = true
  }
}

// Fetch once on first import
let initPromise = null

export function useWhiteLabel() {
  if (!initPromise) {
    initPromise = fetchConfig()
  }

  // Allow re-fetch (e.g. after admin saves new config)
  async function refresh() {
    await fetchConfig()
  }

  return {
    brandName: readonly(ref(config.value.brand_name)),
    config: readonly(config),
    loaded: readonly(loaded),
    error: readonly(error),
    refresh,
  }
}
