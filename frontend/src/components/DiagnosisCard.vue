<template>
  <div class="diagnosis-card rounded-xl overflow-hidden transition-all duration-300 mb-3 group hover:scale-[1.02] hover:shadow-2xl cursor-pointer" :class="[cardClass, isDark ? '' : 'shadow-md']" @click="$emit('open-detail', cause)"  role="button" tabindex="0" :aria-label="'View details for ' + cause.cause"  @keydown.enter="$emit('open-detail', cause)"  >
    <!-- Gradient top accent -->
    <div class="h-1" :class="accentGradient"></div>

    <!-- Header -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between px-3 sm:px-4 py-3 sm:py-4 gap-2 sm:gap-0" :class="headerBg">
      <div class="flex items-center gap-2 sm:gap-3 min-w-0 flex-1">
        <div class="flex-shrink-0 w-10 h-10 sm:w-11 sm:h-11 rounded-xl flex items-center justify-center text-lg shadow-lg" :class="iconBgClass">
          <span>{{ specialtyIcon }}</span>
        </div>
        <div class="min-w-0">
          <h4 class="text-sm sm:text-base font-bold truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ cause.cause }}</h4>
          <div class="flex items-center gap-2 mt-1 flex-wrap">
            <span class="text-detail font-bold uppercase px-2 py-0.5 rounded-full" :class="urgencyBadge">
              {{ cause.urgency }}
            </span>
            <span class="text-detail font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ cause.specialty }}</span>
          </div>
        </div>
      </div>
      <!-- Confidence -->
      <div class="flex-shrink-0 text-center ml-0 sm:ml-3">
        <div class="text-2xl sm:text-3xl font-black tabular-nums" :class="confidenceColor">{{ cause.value }}%</div>
        <div class="text-tiny uppercase tracking-widest font-semibold" :class="confidenceLabelColor">{{ confidenceLabel }}</div>
      </div>
    </div>

    <!-- Animated confidence bar -->
    <div class="h-1.5 relative" :class="isDark ? 'bg-slate-800/80' : 'bg-slate-200'">
      <div class="h-full transition-all duration-1000 ease-out relative overflow-hidden" :class="barGradient" :style="{ width: cause.value + '%' }">
        <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
      </div>
    </div>

    <!-- Key Clinical Indicators -->
    <div class="px-4 pt-3 pb-1 flex flex-wrap gap-1.5">
      <span class="inline-flex items-center gap-1 text-detail font-medium px-2 py-1 rounded-full" :class="isDark ? 'bg-slate-700/50 text-slate-300' : 'bg-slate-100 text-slate-600'">
        <span class="w-1.5 h-1.5 rounded-full" :class="confidenceDotColor"></span>
        {{ confidenceLabel }} {{ t('diagnosis.confidence') }}
      </span>
      <span v-if="cause.urgency === 'urgent'" class="inline-flex items-center gap-1 text-detail font-medium px-2 py-1 rounded-full bg-red-500/15 text-red-400">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
        {{ t('diagnosis.needsPromptAttention') }}
      </span>
      <span v-if="cause.urgency === 'soon'" class="inline-flex items-center gap-1 text-detail font-medium px-2 py-1 rounded-full bg-amber-500/15 text-amber-400">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        {{ t('diagnosis.scheduleSoon') }}
      </span>
      <span v-if="rank === 1" class="inline-flex items-center gap-1 text-detail font-medium px-2 py-1 rounded-full" :class="isDark ? 'bg-yellow-500/15 text-yellow-400' : 'bg-yellow-50 text-yellow-700'">
        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
        {{ t('diagnosis.mostLikely') }}
      </span>
    </div>

    <!-- Explanation -->
    <div v-if="cause.explanation" class="px-4 py-2.5 text-xs leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
      {{ cause.explanation }}
    </div>

    <!-- Red flags inline (always visible when present) -->
    <div v-if="redFlags.length > 0" class="mx-4 mb-2 p-2.5 rounded-lg border" :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-200'">
      <div class="flex items-center gap-1.5 mb-1.5">
        <svg class="w-3.5 h-3.5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
        <span class="text-detail font-bold text-red-400 uppercase tracking-wider">{{ t('diagnosis.warningSignsLabel') }}</span>
      </div>
      <ul class="space-y-1">
        <li v-for="flag in redFlags" :key="flag" class="text-caption flex items-start gap-1.5" :class="isDark ? 'text-red-300' : 'text-red-700'">
          <span class="text-red-500 mt-0.5 flex-shrink-0 font-bold">!</span>
          <span>{{ flag }}</span>
        </li>
      </ul>
    </div>

    <!-- Recommended Tests inline (always visible when present) -->
    <div v-if="recommendedTests.length > 0" class="mx-4 mb-2 p-2.5 rounded-lg border" :class="isDark ? 'bg-blue-500/5 border-blue-500/20' : 'bg-blue-50 border-blue-200'">
      <div class="flex items-center gap-1.5 mb-1.5">
        <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
        <span class="text-detail font-bold text-blue-400 uppercase tracking-wider">{{ t('diagnosis.recommendedTestsLabel') }}</span>
        <span class="text-tiny ml-auto px-1.5 py-0.5 rounded-full" :class="isDark ? 'bg-blue-500/20 text-blue-300' : 'bg-blue-100 text-blue-600'">{{ recommendedTests.length }}</span>
      </div>
      <ul class="space-y-1">
        <li v-for="test in recommendedTests.slice(0, showAllTests ? undefined : 3)" :key="test" class="text-caption flex items-start gap-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
          <svg class="w-3 h-3 mt-0.5 flex-shrink-0 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/></svg>
          <span>{{ test }}</span>
        </li>
      </ul>
      <button v-if="recommendedTests.length > 3" @click="showAllTests = !showAllTests" class="mt-1.5 text-detail font-medium transition-colors" :class="isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'">
        {{ showAllTests ? t('diagnosis.showLess') : t('diagnosis.showAllTests').replace('{n}', recommendedTests.length) }}
      </button>
    </div>

    <!-- Confidence Breakdown Mini -->
    <div class="mx-4 mb-2 p-2.5 rounded-lg" :class="isDark ? 'bg-slate-700/30' : 'bg-slate-50'">
      <div class="grid grid-cols-3 gap-2 text-center">
        <div>
          <div class="text-detail font-semibold uppercase tracking-wider mb-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ t('diagnosis.rank') }}</div>
          <div class="text-sm font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">#{{ rank }}</div>
        </div>
        <div>
          <div class="text-detail font-semibold uppercase tracking-wider mb-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ t('diagnosis.urgency') }}</div>
          <div class="text-sm font-bold capitalize" :class="urgencyTextColor">{{ cause.urgency || t('diagnosis.routine') }}</div>
        </div>
        <div>
          <div class="text-detail font-semibold uppercase tracking-wider mb-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ t('diagnosis.specialty') }}</div>
          <div class="text-caption font-bold truncate" :class="isDark ? 'text-blue-400' : 'text-blue-600'" :title="cause.specialty">{{ shortSpecialty }}</div>
        </div>
      </div>
    </div>

    <!-- Research links -->
    <div class="px-4 pb-3 flex flex-wrap gap-1.5">
      <a :href="'https://scholar.google.com/scholar?q=' + encodeURIComponent(cause.cause)" target="_blank" rel="noopener" class="inline-flex items-center gap-1 text-detail font-medium px-2.5 py-1.5 rounded-lg transition-all hover:scale-105" :class="isDark ? 'bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 hover:shadow-lg hover:shadow-blue-500/10' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
        Google Scholar
      </a>
      <a :href="'https://www.mayoclinic.org/search/search-results?q=' + encodeURIComponent(cause.cause)" target="_blank" rel="noopener" class="inline-flex items-center gap-1 text-detail font-medium px-2.5 py-1.5 rounded-lg transition-all hover:scale-105" :class="isDark ? 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 hover:shadow-lg hover:shadow-emerald-500/10' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100'">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
        Mayo Clinic
      </a>
      <a :href="'https://medlineplus.gov/ency/article/' + encodeURIComponent(cause.cause) + '.htm'" target="_blank" rel="noopener" class="inline-flex items-center gap-1 text-detail font-medium px-2.5 py-1.5 rounded-lg transition-all hover:scale-105" :class="isDark ? 'bg-purple-500/10 text-purple-400 hover:bg-purple-500/20 hover:shadow-lg hover:shadow-purple-500/10' : 'bg-purple-50 text-purple-600 hover:bg-purple-100'">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
        MedlinePlus
      </a>
      <a :href="'https://en.wikipedia.org/wiki/' + encodeURIComponent(cause.cause.replace(/ /g, '_'))" target="_blank" rel="noopener" class="inline-flex items-center gap-1 text-detail font-medium px-2.5 py-1.5 rounded-lg transition-all hover:scale-105" :class="isDark ? 'bg-slate-500/10 text-slate-400 hover:bg-slate-500/20' : 'bg-slate-50 text-slate-600 hover:bg-slate-100'">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
        Wikipedia
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'

const { isDark } = useTheme()
const { t } = useI18n()

const props = defineProps({
  cause: { type: Object, required: true },
  rank: { type: Number, default: 1 },
  redFlags: { type: Array, default: () => [] },
  recommendedTests: { type: Array, default: () => [] }
})
defineEmits(['open-detail'])

const showAllTests = ref(false)

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

const shortSpecialty = computed(() => {
  const s = props.cause.specialty || 'Primary Care'
  return s.length > 14 ? s.slice(0, 12) + '...' : s
})

const confidenceLabel = computed(() => {
  if (props.cause.value >= 70) return t('diagnosis.confidenceHigh')
  if (props.cause.value >= 40) return t('diagnosis.confidenceModerate')
  if (props.cause.value >= 20) return t('diagnosis.confidenceLow')
  return t('diagnosis.confidenceVeryLow')
})

const confidenceLabelColor = computed(() => {
  if (props.cause.value >= 70) return 'text-emerald-500'
  if (props.cause.value >= 40) return 'text-amber-500'
  return 'text-blue-500'
})

const confidenceDotColor = computed(() => {
  if (props.cause.value >= 70) return 'bg-emerald-400'
  if (props.cause.value >= 40) return 'bg-amber-400'
  return 'bg-blue-400'
})

const urgencyTextColor = computed(() => {
  if (props.cause.urgency === 'urgent') return isDark.value ? 'text-red-400' : 'text-red-600'
  if (props.cause.urgency === 'soon') return isDark.value ? 'text-amber-400' : 'text-amber-600'
  return isDark.value ? 'text-emerald-400' : 'text-emerald-600'
})

const cardClass = computed(() => {
  if (props.cause.urgency === 'urgent') return isDark.value ? 'border border-red-500/40 shadow-red-500/5' : 'border border-red-300 shadow-red-100'
  if (props.cause.urgency === 'soon') return isDark.value ? 'border border-amber-500/40 shadow-amber-500/5' : 'border border-amber-300 shadow-amber-100'
  return isDark.value ? 'border border-slate-700/60 hover:border-blue-500/30' : 'border border-slate-200 hover:border-blue-300'
})

const accentGradient = computed(() => {
  if (props.cause.value >= 70) return 'bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400'
  if (props.cause.value >= 40) return 'bg-gradient-to-r from-amber-500 via-orange-400 to-yellow-400'
  return 'bg-gradient-to-r from-slate-500 via-blue-400 to-indigo-400'
})

const iconBgClass = computed(() => {
  if (props.cause.value >= 70) return isDark.value ? 'bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30' : 'bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-200'
  if (props.cause.value >= 40) return isDark.value ? 'bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30' : 'bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200'
  return isDark.value ? 'bg-gradient-to-br from-blue-500/20 to-indigo-500/20 border border-blue-500/30' : 'bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200'
})

const headerBg = computed(() => {
  return isDark.value ? 'bg-slate-800/80' : 'bg-slate-50/80'
})

const urgencyBadge = computed(() => {
  if (props.cause.urgency === 'urgent') return 'bg-red-500/20 text-red-300 border border-red-500/30'
  if (props.cause.urgency === 'soon') return 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
  return 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
})

const confidenceColor = computed(() => {
  if (props.cause.value >= 70) return 'text-emerald-400 drop-shadow-[0_0_8px_rgba(52,211,153,0.3)]'
  if (props.cause.value >= 40) return 'text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.3)]'
  return 'text-blue-400 drop-shadow-[0_0_8px_rgba(96,165,250,0.3)]'
})

const barGradient = computed(() => {
  if (props.cause.value >= 70) return 'bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-400'
  if (props.cause.value >= 40) return 'bg-gradient-to-r from-amber-600 via-amber-500 to-yellow-400'
  return 'bg-gradient-to-r from-blue-600 via-blue-500 to-indigo-400'
})
</script>
