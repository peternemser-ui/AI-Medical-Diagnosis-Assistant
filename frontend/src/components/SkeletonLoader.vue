<template>
  <div class="skeleton-loader">
    <!-- Text type: renders lines of varying widths -->
    <div v-if="type === 'text'" class="space-y-2.5">
      <div
        v-for="(w, i) in textLineWidths"
        :key="i"
        class="h-3 rounded-lg animate-pulse"
        :class="skeletonBg"
        :style="{ width: w }"
      />
    </div>

    <!-- Circle type: renders a circular avatar placeholder -->
    <div
      v-else-if="type === 'circle'"
      class="rounded-full animate-pulse"
      :class="skeletonBg"
      :style="{ width: resolvedWidth, height: resolvedWidth }"
    />

    <!-- Card type: header bar + 3 text lines -->
    <div v-else-if="type === 'card'" class="space-y-3">
      <div
        class="h-5 rounded-lg animate-pulse"
        :class="skeletonBg"
        style="width: 45%"
      />
      <div class="space-y-2.5">
        <div
          class="h-3 rounded-lg animate-pulse"
          :class="skeletonBg"
          style="width: 100%"
        />
        <div
          class="h-3 rounded-lg animate-pulse"
          :class="skeletonBg"
          style="width: 85%"
        />
        <div
          class="h-3 rounded-lg animate-pulse"
          :class="skeletonBg"
          style="width: 70%"
        />
      </div>
    </div>

    <!-- Chart type: 5 horizontal bars of varying lengths -->
    <div v-else-if="type === 'chart'" class="space-y-2">
      <div
        v-for="(w, i) in chartBarWidths"
        :key="i"
        class="h-4 rounded-lg animate-pulse"
        :class="skeletonBg"
        :style="{ width: w }"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  type: {
    type: String,
    default: 'text',
    validator: (v) => ['text', 'circle', 'card', 'chart'].includes(v)
  },
  lines: {
    type: Number,
    default: 3
  },
  width: {
    type: String,
    default: 'full'
  }
})

const skeletonBg = computed(() =>
  isDark.value ? 'bg-slate-700/30' : 'bg-slate-200'
)

const resolvedWidth = computed(() => {
  if (props.width === 'full') return '100%'
  return props.width
})

// Cycle through 100%, 85%, 70% for text lines
const widthCycle = ['100%', '85%', '70%']

const textLineWidths = computed(() =>
  Array.from({ length: props.lines }, (_, i) => widthCycle[i % widthCycle.length])
)

const chartBarWidths = ['90%', '65%', '80%', '50%', '75%']
</script>
