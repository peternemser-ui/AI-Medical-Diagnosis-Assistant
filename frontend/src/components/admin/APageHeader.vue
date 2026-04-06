<template>
  <div class="flex items-center justify-between mb-6">
    <div>
      <h1 class="text-xl font-bold tracking-tight" :class="isDark ? 'text-white' : 'text-slate-900'">
        <slot name="title">{{ title }}</slot>
      </h1>
      <p v-if="subtitle" class="text-sm mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ subtitle }}</p>
    </div>
    <div class="flex items-center gap-3">
      <span v-if="lastUpdated" class="text-xs tabular-nums" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
        {{ lastUpdated }}
      </span>
      <slot name="actions">
        <button v-if="showRefresh" @click="$emit('refresh')" class="text-xs font-medium px-3 py-1.5 rounded-lg transition-colors" :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
          Refresh
        </button>
      </slot>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  lastUpdated: {
    type: String,
    default: ''
  },
  showRefresh: {
    type: Boolean,
    default: true
  }
})

defineEmits(['refresh'])
</script>
