<template>
  <div class="grid gap-4" :class="gridCols">
    <div v-for="kpi in items" :key="kpi.label"
      class="rounded-xl border px-4 py-3 transition-colors"
      :class="cardClass">
      <div class="flex items-center justify-between mb-1">
        <span class="text-[10px] font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ kpi.label }}</span>
        <span v-if="kpi.trend != null" class="text-[10px] font-bold" :class="kpi.trend >= 0 ? 'text-emerald-500' : 'text-red-500'">
          {{ kpi.trend >= 0 ? '+' : '' }}{{ kpi.trend }}%
        </span>
      </div>
      <div class="text-2xl font-bold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ kpi.value }}</div>
      <div v-if="kpi.sublabel" class="text-[10px] mt-0.5" :class="isDark ? 'text-slate-600' : 'text-slate-400'">{{ kpi.sublabel }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  items: {
    type: Array,
    required: true,
    default: () => []
  },
  cols: {
    type: Number,
    default: 4
  }
})

const gridCols = computed(() => {
  const map = {
    2: 'grid-cols-1 sm:grid-cols-2',
    3: 'grid-cols-1 sm:grid-cols-3',
    4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4',
    5: 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-5',
    6: 'grid-cols-2 sm:grid-cols-3 lg:grid-cols-6'
  }
  return map[props.cols] || map[4]
})

const cardClass = computed(() => {
  return isDark.value
    ? 'bg-slate-900/80 border-slate-800'
    : 'bg-white border-slate-200 shadow-sm'
})
</script>
