<template>
  <div class="diagnosis-card rounded-xl border overflow-hidden transition-all duration-300 mb-3" :class="[borderClass, isDark ? '' : 'shadow-sm']">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between px-3 sm:px-4 py-2.5 sm:py-3 gap-2 sm:gap-0" :class="headerBg">
      <div class="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
        <span class="text-base sm:text-lg flex-shrink-0">{{ rankEmoji }}</span>
        <div class="min-w-0">
          <h4 class="text-xs sm:text-sm font-bold truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ cause.cause }}</h4>
          <div class="flex items-center gap-2 mt-0.5 flex-wrap">
            <span class="text-[10px] font-semibold uppercase px-1.5 py-0.5 rounded" :class="urgencyBadge">
              {{ cause.urgency }}
            </span>
            <span class="text-[10px] text-slate-400">{{ cause.specialty }}</span>
          </div>
        </div>
      </div>
      <!-- Confidence -->
      <div class="flex-shrink-0 text-center ml-0 sm:ml-3">
        <div class="text-lg sm:text-xl font-black" :class="confidenceColor">{{ cause.value }}%</div>
        <div class="text-[9px] text-slate-500 uppercase tracking-wider">confidence</div>
      </div>
    </div>

    <!-- Confidence bar -->
    <div class="h-1" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'">
      <div class="h-full transition-all duration-700" :class="barColor" :style="{ width: cause.value + '%' }"></div>
    </div>

    <!-- Explanation -->
    <div v-if="cause.explanation" class="px-4 py-3 text-xs leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
      {{ cause.explanation }}
    </div>

    <!-- Expandable details -->
    <div v-if="recommendedTests.length > 0 || redFlags.length > 0">
      <button
        @click="expanded = !expanded"
        class="w-full px-4 py-2 text-[11px] flex items-center gap-1 transition-colors border-t"
        :class="isDark ? 'text-slate-400 hover:text-slate-300 border-slate-700/50' : 'text-slate-500 hover:text-slate-700 border-slate-200'"
      >
        <svg class="w-3 h-3 transition-transform" :class="{ 'rotate-90': expanded }" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
        </svg>
        Details &amp; Tests
      </button>

      <div v-if="expanded" class="px-4 pb-3 space-y-2">
        <!-- Red flags -->
        <div v-if="redFlags.length > 0">
          <div class="text-[10px] font-semibold text-red-400 uppercase mb-1">Warning Signs</div>
          <ul class="space-y-0.5">
            <li v-for="flag in redFlags" :key="flag" class="text-xs text-red-300 flex items-start gap-1.5">
              <span class="text-red-500 mt-0.5 flex-shrink-0">!</span>
              <span>{{ flag }}</span>
            </li>
          </ul>
        </div>
        <!-- Tests -->
        <div v-if="recommendedTests.length > 0">
          <div class="text-[10px] font-semibold text-blue-400 uppercase mb-1">Recommended Tests</div>
          <ul class="space-y-0.5">
            <li v-for="test in recommendedTests" :key="test" class="text-xs text-slate-400 flex items-start gap-1.5">
              <span class="text-blue-500 mt-0.5 flex-shrink-0">&bull;</span>
              <span>{{ test }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  cause: { type: Object, required: true },
  rank: { type: Number, default: 1 },
  redFlags: { type: Array, default: () => [] },
  recommendedTests: { type: Array, default: () => [] }
})

const expanded = ref(false)

const rankEmoji = computed(() => {
  if (props.rank === 1) return '#1'
  if (props.rank === 2) return '#2'
  return `#${props.rank}`
})

const borderClass = computed(() => {
  if (props.cause.urgency === 'urgent') return isDark.value ? 'border-red-500/30' : 'border-red-300'
  if (props.cause.urgency === 'soon') return isDark.value ? 'border-amber-500/30' : 'border-amber-300'
  return isDark.value ? 'border-slate-700/50' : 'border-slate-200'
})

const headerBg = computed(() => {
  return isDark.value ? 'bg-slate-800/80' : 'bg-slate-50'
})

const urgencyBadge = computed(() => {
  if (props.cause.urgency === 'urgent') return 'bg-red-500/20 text-red-300'
  if (props.cause.urgency === 'soon') return 'bg-amber-500/20 text-amber-300'
  return 'bg-blue-500/20 text-blue-300'
})

const confidenceColor = computed(() => {
  if (props.cause.value >= 70) return 'text-emerald-400'
  if (props.cause.value >= 40) return 'text-amber-400'
  return 'text-slate-400'
})

const barColor = computed(() => {
  if (props.cause.value >= 70) return 'bg-emerald-500'
  if (props.cause.value >= 40) return 'bg-amber-500'
  return 'bg-slate-500'
})
</script>
