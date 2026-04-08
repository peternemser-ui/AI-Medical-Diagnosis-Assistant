<template>
  <span class="inline-flex items-center gap-1.5">
    <span
      :class="[
        'rounded-full inline-block flex-shrink-0',
        dotSizeClass,
        colorClasses.dot,
        (pulse && (status === 'healthy' || status === 'running')) || status === 'retrying' ? 'animate-pulse' : ''
      ]"
    />
    <span
      v-if="displayLabel"
      :class="[
        'font-medium capitalize',
        textSizeClass,
        colorClasses.text
      ]"
    >
      {{ displayLabel }}
    </span>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: v => ['healthy', 'degraded', 'error', 'idle', 'paused', 'running', 'retrying'].includes(v)
  },
  label: {
    type: String,
    default: ''
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md'].includes(v)
  },
  pulse: {
    type: Boolean,
    default: false
  }
})

const displayLabel = computed(() => props.label || props.status)

const dotSizeClass = computed(() => props.size === 'sm' ? 'w-1.5 h-1.5' : 'w-2.5 h-2.5')
const textSizeClass = computed(() => props.size === 'sm' ? 'text-xs' : 'text-sm')

const colorClasses = computed(() => {
  const map = {
    healthy: { dot: 'bg-emerald-500', text: isDark.value ? 'text-emerald-400' : 'text-emerald-600' },
    running: { dot: 'bg-emerald-500', text: isDark.value ? 'text-emerald-400' : 'text-emerald-600' },
    degraded: { dot: 'bg-amber-500', text: isDark.value ? 'text-amber-400' : 'text-amber-600' },
    error: { dot: 'bg-red-500', text: isDark.value ? 'text-red-400' : 'text-red-600' },
    idle: { dot: isDark.value ? 'bg-slate-500' : 'bg-slate-400', text: isDark.value ? 'text-slate-400' : 'text-slate-500' },
    paused: { dot: 'bg-purple-500', text: isDark.value ? 'text-purple-400' : 'text-purple-600' },
    retrying: { dot: 'bg-yellow-500', text: isDark.value ? 'text-yellow-400' : 'text-yellow-600' }
  }
  return map[props.status] || map.idle
})
</script>
