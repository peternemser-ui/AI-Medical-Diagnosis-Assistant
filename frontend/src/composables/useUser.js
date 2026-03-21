import { ref, computed } from 'vue'
import {
  getProfile,
  saveProfile,
  getPreferences,
  savePreference as savePreferenceSvc,
  clearUserData,
} from '../services/userService.js'

const profile = ref(getProfile())
const preferences = ref(getPreferences())

export function useUser() {
  const isLoggedIn = computed(() => {
    return !!(profile.value.name && profile.value.name.trim().length > 0)
  })

  function updateProfile(data) {
    const merged = saveProfile(data)
    profile.value = { ...merged }
  }

  function setProfile(data) {
    profile.value = { ...data }
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

  return { profile, preferences, isLoggedIn, updateProfile, setProfile, updatePreference, logout }
}
