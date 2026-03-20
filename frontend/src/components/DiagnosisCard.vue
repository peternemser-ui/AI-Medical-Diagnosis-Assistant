<template>
  <div class="diagnosis-card rounded-xl border overflow-hidden transition-all duration-300 mb-3" :class="[borderClass, isDark ? '' : 'shadow-sm']">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between px-3 sm:px-4 py-2.5 sm:py-3 gap-2 sm:gap-0" :class="headerBg">
      <div class="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
        <div class="flex-shrink-0 w-8 h-8 sm:w-9 sm:h-9 rounded-lg flex items-center justify-center text-sm" :class="isDark ? 'bg-slate-700/50' : 'bg-slate-100'">
          <span>{{ specialtyIcon }}</span>
        </div>
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

    <!-- Research links -->
    <div class="px-4 pb-2 flex flex-wrap gap-1.5">
      <a :href="'https://scholar.google.com/scholar?q=' + encodeURIComponent(cause.cause)" target="_blank" rel="noopener" class="inline-flex items-center gap-1 text-[10px] px-2 py-1 rounded-md transition-colors" :class="isDark ? 'bg-blue-500/10 text-blue-400 hover:bg-blue-500/20' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
        Google Scholar
      </a>
      <a :href="'https://www.mayoclinic.org/search/search-results?q=' + encodeURIComponent(cause.cause)" target="_blank" rel="noopener" class="inline-flex items-center gap-1 text-[10px] px-2 py-1 rounded-md transition-colors" :class="isDark ? 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100'">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
        Mayo Clinic
      </a>
      <a :href="'https://medlineplus.gov/ency/article/' + encodeURIComponent(cause.cause) + '.htm'" target="_blank" rel="noopener" class="inline-flex items-center gap-1 text-[10px] px-2 py-1 rounded-md transition-colors" :class="isDark ? 'bg-purple-500/10 text-purple-400 hover:bg-purple-500/20' : 'bg-purple-50 text-purple-600 hover:bg-purple-100'">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
        MedlinePlus
      </a>
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

const specialtyIcon = computed(() => {
  const s = (props.cause.specialty || '').toLowerCase()
  if (s.includes('cardio') || s.includes('heart')) return '❤️'
  if (s.includes('neuro')) return '🧠'
  if (s.includes('dermat') || s.includes('skin')) return '🩹'
  if (s.includes('gastro') || s.includes('gi')) return '🫁'
  if (s.includes('pulmon') || s.includes('lung')) return '🫁'
  if (s.includes('ent') || s.includes('ear')) return '👂'
  if (s.includes('ortho') || s.includes('msk')) return '🦴'
  if (s.includes('psych') || s.includes('mental')) return '🧘'
  if (s.includes('oncol') || s.includes('cancer')) return '🔬'
  if (s.includes('allergy') || s.includes('immun')) return '🛡️'
  if (s.includes('endo') || s.includes('thyroid')) return '⚗️'
  if (s.includes('surgery') || s.includes('oral')) return '🏥'
  if (s.includes('primary') || s.includes('family') || s.includes('internal')) return '🩺'
  return '🩺'
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
