import { ref, computed } from 'vue'
import {
  getProfile,
  saveProfile,
  getPreferences,
  savePreference as savePreferenceSvc,
  clearUserData,
} from '../services/userService.js'
import { isAuthenticated, getCurrentUser } from '../services/authService.js'

// Initialize from sync sources: auth_user cache + preferences
const profile = ref(_loadInitialProfile())
const preferences = ref(getPreferences())

function _loadInitialProfile() {
  // First try auth_user (backend-provided, always has name/email)
  const authUser = getCurrentUser()
  const localProfile = getProfile()

  if (authUser && authUser.name) {
    return { ...localProfile, ...authUser }
  }
  return localProfile
}

export function useUser() {
  const isLoggedIn = computed(() => {
    // Check backend JWT auth first, then fall back to profile name
    if (isAuthenticated()) return true
    return !!(profile.value.name && profile.value.name.trim().length > 0)
  })

  function updateProfile(data) {
    // Update in-memory reactive profile immediately
    profile.value = { ...profile.value, ...data }
    // Persist (async — fires and forgets for now)
    saveProfile(data)
  }

  function setProfile(data) {
    profile.value = { ...data }
  }

  /** Refresh profile from storage (call after login/key derivation) */
  function refreshProfile() {
    profile.value = _loadInitialProfile()
  }

  function updatePreference(key, value) {
    const merged = savePreferenceSvc(key, value)
    preferences.value = { ...merged }
  }

  function logout() {
    clearUserData()
    profile.value = getProfile()
    preferences.value = getPreferences()
  }

  return { profile, preferences, isLoggedIn, updateProfile, setProfile, refreshProfile, updatePreference, logout }
}
