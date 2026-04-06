<template>
  <div class="space-y-2.5">
    <div v-for="item in data" :key="item.label" class="group">
      <div class="flex items-center justify-between mb-1">
        <span class="text-xs font-medium truncate" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ item.label }}</span>
        <span v-if="showValues" class="text-xs font-semibold tabular-nums ml-2 flex-shrink-0" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ item.value }}</span>
      </div>
      <div class="w-full rounded-full h-2 overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
        <div
          class="h-full rounded-full transition-all duration-500"
          :class="item.color || defaultBarColor"
          :style="{ width: barWidth(item.value) + '%' }"
        ></div>
      </div>
    </div>
    <AEmptyState
      v-if="data.length === 0"
      title="No data"
      description="Nothing to display yet."
      variant="default"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import AEmptyState from './AEmptyState.vue'

const { isDark } = useTheme()

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  maxValue: {
    type: Number,
    default: 0
  },
  showValues: {
    type: Boolean,
    default: true
  }
})

const defaultBarColor = computed(() => 'bg-blue-500')

const computedMax = computed(() => {
  if (props.maxValue > 0) return props.maxValue
  return Math.max(...props.data.map(d => typeof d.value === 'number' ? d.value : parseFloat(d.value) || 0), 1)
})

function barWidth(value) {
  const num = typeof value === 'number' ? value : parseFloat(value) || 0
  return Math.min((num / computedMax.value) * 100, 100)
}
</script>
