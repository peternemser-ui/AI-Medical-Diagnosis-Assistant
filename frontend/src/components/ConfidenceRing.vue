<template>
  <div class="relative inline-flex items-center justify-center" :style="{ width: size + 'px', height: size + 'px' }">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" class="transform -rotate-90">
      <!-- Background ring -->
      <circle
        :cx="center" :cy="center" :r="radius"
        fill="none"
        :stroke="isDark ? '#334155' : '#e2e8f0'"
        :stroke-width="strokeWidth"
      />
      <!-- Progress ring -->
      <circle
        :cx="center" :cy="center" :r="radius"
        fill="none"
        :stroke="ringColor"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        class="transition-all duration-1000 ease-out"
      />
    </svg>
    <!-- Center value -->
    <div class="absolute inset-0 flex items-center justify-center">
      <span class="font-bold tabular-nums" :class="textClass" :style="{ fontSize: (size * 0.28) + 'px', color: ringColor }">
        {{ value }}%
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  value: { type: Number, required: true, default: 0 },
  size: { type: Number, default: 48 },
  strokeWidth: { type: Number, default: 4 },
})

const center = computed(() => props.size / 2)
const radius = computed(() => (props.size - props.strokeWidth) / 2 - 1)
const circumference = computed(() => 2 * Math.PI * radius.value)
const clampedValue = computed(() => Math.max(0, Math.min(100, props.value)))
const dashOffset = computed(() => circumference.value * (1 - clampedValue.value / 100))

const ringColor = computed(() => {
  if (clampedValue.value >= 70) return '#10b981'
  if (clampedValue.value >= 50) return '#3b82f6'
  if (clampedValue.value >= 25) return '#f59e0b'
  return '#ef4444'
})

const textClass = computed(() => '')
</script>
