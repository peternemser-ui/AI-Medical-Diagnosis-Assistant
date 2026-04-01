<template>
  <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-pill border text-body-sm"
    :class="isDark
      ? 'bg-slate-800/60 border-slate-700/50 text-slate-300'
      : 'bg-slate-100 border-slate-200 text-slate-600'">
    <slot name="icon" />
    <slot />
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'
const { isDark } = useTheme()
</script>
