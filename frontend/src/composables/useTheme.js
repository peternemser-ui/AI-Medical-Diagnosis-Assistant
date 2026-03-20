import { ref, watch, onMounted } from 'vue'

const theme = ref(localStorage.getItem('theme') || 'dark')

function applyTheme(t) {
  const root = document.documentElement
  if (t === 'dark') {
    root.classList.add('dark')
    root.classList.remove('light')
  } else {
    root.classList.add('light')
    root.classList.remove('dark')
  }
}

// Apply immediately on import (before any component mounts)
if (typeof document !== 'undefined') {
  applyTheme(theme.value)
}

export function useTheme() {
  function setTheme(t) {
    theme.value = t
    localStorage.setItem('theme', t)
    applyTheme(t)
  }

  function toggleTheme() {
    setTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  const isDark = ref(theme.value === 'dark')

  watch(theme, (t) => {
    isDark.value = t === 'dark'
  })

  onMounted(() => {
    applyTheme(theme.value)
  })

  return { theme, isDark, setTheme, toggleTheme }
}
