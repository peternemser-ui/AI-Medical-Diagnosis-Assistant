/**
 * Authentication composable for Vue components
 */

import { ref, computed, readonly } from 'vue'
import { authService } from '@/services/auth'

// Reactive state
const user = ref(null)
const isLoading = ref(false)
const error = ref(null)

// Initialize from localStorage
const initAuth = () => {
  const storedUser = authService.getUser()
  if (storedUser && authService.isAuthenticated()) {
    user.value = storedUser
  }
}

initAuth()

/**
 * Authentication composable
 * @returns {Object} Auth methods and state
 */
export function useAuth() {
  // Computed properties
  const isAuthenticated = computed(() => !!user.value && authService.isAuthenticated())
  const isAdmin = computed(() => user.value?.is_admin || false)
  const userName = computed(() => user.value?.name || '')
  const userEmail = computed(() => user.value?.email || '')

  /**
   * Register a new user
   * @param {Object} userData - Registration data
   */
  async function register(userData) {
    isLoading.value = true
    error.value = null

    try {
      await authService.register(userData)
      // Auto-login after registration
      await login(userData.email, userData.password)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Login user
   * @param {string} email - User email
   * @param {string} password - User password
   */
  async function login(email, password) {
    isLoading.value = true
    error.value = null

    try {
      await authService.login(email, password)
      user.value = authService.getUser()
    } catch (err) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Logout current user
   */
  async function logout() {
    isLoading.value = true
    error.value = null

    try {
      await authService.logout()
      user.value = null
    } catch (err) {
      error.value = err.response?.data?.detail || 'Logout failed'
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Refresh user data
   */
  async function refreshUser() {
    if (!authService.isAuthenticated()) return

    try {
      const userData = await authService.getCurrentUser()
      user.value = userData
      authService.setUser(userData)
    } catch (err) {
      console.error('Failed to refresh user:', err)
    }
  }

  /**
   * Change password
   * @param {string} currentPassword - Current password
   * @param {string} newPassword - New password
   */
  async function changePassword(currentPassword, newPassword) {
    isLoading.value = true
    error.value = null

    try {
      await authService.changePassword(currentPassword, newPassword)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Password change failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Request password reset
   * @param {string} email - User email
   */
  async function forgotPassword(email) {
    isLoading.value = true
    error.value = null

    try {
      await authService.forgotPassword(email)
    } catch (err) {
      error.value = err.response?.data?.detail || 'Password reset request failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Clear any auth errors
   */
  function clearError() {
    error.value = null
  }

  return {
    // State (readonly)
    user: readonly(user),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Computed
    isAuthenticated,
    isAdmin,
    userName,
    userEmail,

    // Methods
    register,
    login,
    logout,
    refreshUser,
    changePassword,
    forgotPassword,
    clearError
  }
}

export default useAuth
