<template>
  <router-link :to="helpTarget"
    class="group fixed bottom-6 right-6 w-12 h-12 rounded-full shadow-xl flex items-center justify-center z-40 transition-all hover:scale-110"
    :class="isDark ? 'bg-blue-600 text-white hover:bg-blue-500' : 'bg-blue-500 text-white hover:bg-blue-600'"
    title="Help & Documentation (press ?)">
    <span
      class="pointer-events-none absolute right-14 top-1/2 -translate-y-1/2 whitespace-nowrap rounded-lg px-3 py-1.5 text-xs font-medium shadow-lg opacity-0 transition-opacity group-hover:opacity-100"
      :class="isDark ? 'bg-slate-800 text-slate-200' : 'bg-slate-900 text-white'"
    >
      Help &amp; Documentation (press ?)
    </span>
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
    </svg>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
const route = useRoute()

const helpTarget = computed(() => {
  const sectionMap = {
    '/consult': '/help#starting-a-consultation',
    '/nutrition': '/help#nutrition-planner',
    '/mental-health': '/help#mental-health',
    '/journal': '/help#symptom-journal',
    '/medications': '/help#medications',
    '/reports': '/help#reports-history',
    '/settings': '/help#settings-preferences',
    '/profile': '/help#your-account',
    '/pricing': '/help#subscription-plans',
  }
  return sectionMap[route.path] || '/help'
})
</script>
