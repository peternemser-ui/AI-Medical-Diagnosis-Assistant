<template>
  <div id="app">
    <ErrorBoundary
      title="Something went wrong"
      message="The application encountered an unexpected error. Please try refreshing the page."
      :show-reload="true"
      :show-support="true"
    >
      <router-view />
    </ErrorBoundary>
  </div>
</template>

<script setup>
import ErrorBoundary from './components/ErrorBoundary.vue'
import { useTheme } from './composables/useTheme'

// Initialize theme IMMEDIATELY during setup (before rendering)
const { initializeTheme } = useTheme()
initializeTheme()
console.log('🎨 Theme initialized in App.vue')
</script>

<style>
/* Global styles */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

/* Remove any default styling that might interfere */
* {
  box-sizing: border-box;
}
</style>
