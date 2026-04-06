<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4" :class="iconBgClass">
      <slot name="icon">
        <svg class="w-6 h-6" :class="iconColorClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
      </slot>
    </div>
    <h3 class="text-sm font-semibold mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ title }}</h3>
    <p class="text-xs max-w-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ description }}</p>
    <slot name="action">
      <button v-if="actionLabel" @click="$emit('action')" class="mt-4 text-xs font-medium px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition-colors">
        {{ actionLabel }}
      </button>
    </slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  title: {
    type: String,
    default: 'No data yet'
  },
  description: {
    type: String,
    default: ''
  },
  actionLabel: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: v => ['default', 'info', 'warning'].includes(v)
  }
})

defineEmits(['action'])

const iconBgClass = computed(() => {
  const map = {
    default: isDark.value ? 'bg-slate-800' : 'bg-slate-100',
    info: isDark.value ? 'bg-blue-500/10' : 'bg-blue-50',
    warning: isDark.value ? 'bg-amber-500/10' : 'bg-amber-50'
  }
  return map[props.variant] || map.default
})

const iconColorClass = computed(() => {
  const map = {
    default: isDark.value ? 'text-slate-500' : 'text-slate-400',
    info: isDark.value ? 'text-blue-400' : 'text-blue-500',
    warning: isDark.value ? 'text-amber-400' : 'text-amber-500'
  }
  return map[props.variant] || map.default
})
</script>
