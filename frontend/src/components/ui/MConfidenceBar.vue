<template>
  <div class="flex items-center gap-2">
    <div class="confidence-bar flex-1">
      <div
        class="h-full rounded-full transition-all duration-500 ease-out"
        :class="barColor"
        :style="{ width: `${clampedValue}%` }"
      />
    </div>
    <span v-if="showLabel" class="text-detail font-semibold tabular-nums" :class="labelColor">
      {{ clampedValue }}%
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  showLabel: { type: Boolean, default: true },
})

const clampedValue = computed(() => Math.max(0, Math.min(100, Math.round(props.value))))

const barColor = computed(() => {
  if (clampedValue.value >= 75) return 'bg-emerald-500'
  if (clampedValue.value >= 50) return 'bg-blue-500'
  if (clampedValue.value >= 25) return 'bg-amber-500'
  return 'bg-red-500'
})

const labelColor = computed(() => {
  if (clampedValue.value >= 75) return 'text-emerald-600 dark:text-emerald-400'
  if (clampedValue.value >= 50) return 'text-blue-600 dark:text-blue-400'
  if (clampedValue.value >= 25) return 'text-amber-600 dark:text-amber-400'
  return 'text-red-600 dark:text-red-400'
})
</script>
