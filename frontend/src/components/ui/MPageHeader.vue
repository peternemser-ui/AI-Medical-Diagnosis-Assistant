<template>
  <div class="backdrop-blur-xl border-b py-3 px-6 transition-colors sticky top-0 z-50"
    :class="isDark
      ? 'bg-slate-900/95 border-slate-700/50 shadow-panel-dark'
      : 'bg-white/95 border-slate-200 shadow-subtle'">
    <!-- Subtle gradient accent -->
    <div v-if="accent" class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500"></div>

    <div class="max-w-7xl mx-auto flex items-center justify-between gap-4">
      <!-- Left: icon + title -->
      <div class="flex items-center gap-3 min-w-0">
        <div v-if="icon" class="w-9 h-9 rounded-btn bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg flex-shrink-0">
          <slot name="icon">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="icon"/>
            </svg>
          </slot>
        </div>
        <div class="min-w-0">
          <h1 class="text-title font-bold leading-tight truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ title }}</h1>
          <p v-if="subtitle" class="text-caption" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ subtitle }}</p>
        </div>
      </div>

      <!-- Center: metadata pills -->
      <div v-if="$slots.meta" class="hidden md:flex items-center gap-3">
        <slot name="meta" />
      </div>

      <!-- Right: actions -->
      <div class="flex items-center gap-2 flex-shrink-0">
        <slot name="actions" />
      </div>
    </div>
  </div>

  <!-- Mobile meta bar -->
  <div v-if="$slots['mobile-meta']" class="md:hidden flex items-center justify-between gap-2 px-4 py-2 border-b text-body-sm"
    :class="isDark ? 'bg-slate-800/50 border-slate-700/30 text-slate-400' : 'bg-slate-50 border-slate-200 text-slate-500'">
    <slot name="mobile-meta" />
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'
const { isDark } = useTheme()

defineProps({
  title: { type: String, required: true },
  subtitle: String,
  icon: String,
  accent: { type: Boolean, default: false },
})
</script>
