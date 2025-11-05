/**
 * Theme Composable
 * Manages dark/light mode with localStorage persistence
 */

import { ref, watch, onMounted } from 'vue'

const isDark = ref(false)
const STORAGE_KEY = 'medical-app-theme'

export function useTheme() {
  // Initialize theme from localStorage or system preference
  const initializeTheme = () => {
    const savedTheme = localStorage.getItem(STORAGE_KEY)
    
    if (savedTheme) {
      isDark.value = savedTheme === 'dark'
    } else {
      // Check system preference
      isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    
    applyTheme()
  }
  
  // Apply theme to document
  const applyTheme = () => {
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      document.documentElement.setAttribute('data-theme', 'dark')
      document.documentElement.style.colorScheme = 'dark'
    } else {
      document.documentElement.classList.remove('dark')
      document.documentElement.setAttribute('data-theme', 'light')
      document.documentElement.style.colorScheme = 'light'
    }
  }
  
  // Toggle theme
  const toggleTheme = () => {
    isDark.value = !isDark.value
    localStorage.setItem(STORAGE_KEY, isDark.value ? 'dark' : 'light')
    applyTheme()
    
    console.log(`🌓 Theme toggled to: ${isDark.value ? 'dark' : 'light'}`)
  }
  
  // Set specific theme
  const setTheme = (theme) => {
    isDark.value = theme === 'dark'
    localStorage.setItem(STORAGE_KEY, theme)
    applyTheme()
  }
  
  // Watch for changes
  watch(isDark, () => {
    applyTheme()
  })
  
  return {
    isDark,
    toggleTheme,
    setTheme,
    initializeTheme
  }
}
