<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950 text-white' : 'bg-white text-slate-900'">
    <AppNav />
    <div class="flex flex-col items-center justify-center px-4 py-32 text-center">
      <div class="text-8xl font-bold mb-4" :class="isDark ? 'text-slate-700' : 'text-slate-200'">404</div>
      <h1 class="text-2xl font-bold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Page Not Found</h1>
      <p class="text-base mb-8 max-w-md" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <div class="flex flex-col sm:flex-row gap-3">
        <router-link
          to="/"
          class="px-6 py-2.5 rounded-xl text-sm font-semibold border transition-all"
          :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-300 text-slate-700 hover:bg-slate-50'"
        >
          Go Home
        </router-link>
        <router-link
          to="/consult"
          class="px-6 py-2.5 rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 shadow-lg shadow-emerald-500/20 transition-all"
        >
          Start Consultation
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import AppNav from '@/components/AppNav.vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
</script>
