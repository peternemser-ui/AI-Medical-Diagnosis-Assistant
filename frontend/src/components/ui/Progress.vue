<template>
  <div>
    <div v-if="showLabel" class="flex justify-between mb-1">
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ label }}</span>
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{{ value }}%</span>
    </div>
    <div :class="['w-full rounded-full overflow-hidden', heightClasses, 'bg-gray-200 dark:bg-gray-700']">
      <div
        :class="['rounded-full transition-all duration-300', colorClasses, heightClasses, striped && 'bg-stripes', animated && 'animate-stripes']"
        :style="{ width: `${Math.min(Math.max(value, 0), 100)}%` }"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, default: 0 },
  label: { type: String, default: '' },
  showLabel: { type: Boolean, default: false },
  size: { type: String, default: 'md' },
  color: { type: String, default: 'blue' },
  striped: { type: Boolean, default: false },
  animated: { type: Boolean, default: false }
})

const heightClasses = computed(() => {
  const heights = { sm: 'h-1', md: 'h-2', lg: 'h-3', xl: 'h-4' }
  return heights[props.size] || heights.md
})

const colorClasses = computed(() => {
  const colors = {
    blue: 'bg-blue-600', green: 'bg-green-600', red: 'bg-red-600',
    yellow: 'bg-yellow-500', purple: 'bg-purple-600', gray: 'bg-gray-600'
  }
  return colors[props.color] || colors.blue
})
</script>

<style scoped>
.bg-stripes {
  background-image: linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%, transparent);
  background-size: 1rem 1rem;
}
.animate-stripes { animation: stripes 1s linear infinite; }
@keyframes stripes { from { background-position: 1rem 0; } to { background-position: 0 0; } }
</style>
