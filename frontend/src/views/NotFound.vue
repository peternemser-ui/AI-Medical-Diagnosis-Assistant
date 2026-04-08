<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'">
    <AppNav />

    <main class="flex flex-col items-center justify-center px-4 py-24 sm:py-32 text-center">

      <!-- Large 404 display number -->
      <div class="relative mb-8 select-none" aria-hidden="true">
        <!-- Background number (decorative) -->
        <div class="text-[10rem] sm:text-[14rem] font-extrabold leading-none tracking-tighter tabular-nums"
          :class="isDark ? 'text-slate-800/80' : 'text-slate-200'">
          404
        </div>
        <!-- Foreground medical cross icon, centered over the 0 -->
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="w-20 h-20 sm:w-28 sm:h-28 rounded-3xl flex items-center justify-center shadow-2xl"
            :class="isDark ? 'bg-indigo-700 shadow-indigo-700/40' : 'bg-indigo-600 shadow-indigo-600/30'">
            <svg class="w-10 h-10 sm:w-14 sm:h-14 text-white" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Heading -->
      <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3"
        :class="isDark ? 'text-white' : 'text-slate-900'">
        Page Not Found
      </h1>

      <!-- Subtext -->
      <p class="text-base sm:text-lg max-w-md mb-10 leading-relaxed"
        :class="isDark ? 'text-slate-400' : 'text-slate-500'">
        The page you're looking for doesn't exist or has been moved. Don't worry — your health insights are still just one click away.
      </p>

      <!-- Divider decoration -->
      <div class="flex items-center gap-4 mb-10">
        <div class="h-px w-16" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="w-2 h-2 rounded-full" :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
        <div class="h-px w-16" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
      </div>

      <!-- Action buttons -->
      <div class="flex flex-col sm:flex-row gap-3">
        <router-link
          to="/"
          class="btn-secondary px-8 py-3 text-sm font-semibold"
          :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-300 text-slate-700 hover:bg-white hover:shadow-sm'"
        >
          <svg class="w-4 h-4 inline-block mr-1.5 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
          Go Home
        </router-link>
        <router-link
          to="/consult"
          class="btn-primary px-8 py-3 text-sm font-semibold bg-indigo-700 hover:bg-indigo-600 text-white shadow-lg shadow-indigo-700/30"
        >
          <svg class="w-4 h-4 inline-block mr-1.5 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
          Start Consultation
        </router-link>
      </div>

      <!-- Helpful links -->
      <div class="mt-14 flex flex-wrap justify-center gap-x-6 gap-y-2">
        <span class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Looking for:</span>
        <router-link to="/nutrition" class="text-xs transition-colors" :class="isDark ? 'text-slate-500 hover:text-indigo-400' : 'text-slate-500 hover:text-indigo-600'">Nutrition</router-link>
        <router-link to="/mental-health" class="text-xs transition-colors" :class="isDark ? 'text-slate-500 hover:text-indigo-400' : 'text-slate-500 hover:text-indigo-600'">Mental Health</router-link>
        <router-link to="/medications" class="text-xs transition-colors" :class="isDark ? 'text-slate-500 hover:text-indigo-400' : 'text-slate-500 hover:text-indigo-600'">Medications</router-link>
        <router-link to="/reports" class="text-xs transition-colors" :class="isDark ? 'text-slate-500 hover:text-indigo-400' : 'text-slate-500 hover:text-indigo-600'">Reports</router-link>
      </div>

    </main>
  </div>
</template>

<script setup>
import AppNav from '@/components/AppNav.vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
</script>
