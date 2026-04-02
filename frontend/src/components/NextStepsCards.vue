<template>
  <div class="space-y-3">
    <h3 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)] flex items-center gap-2">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      What To Do Next
    </h3>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <!-- Emergency card (if red flags or emergency urgency) -->
      <div v-if="showEmergency"
        class="rounded-card p-4 border-l-4 border-l-red-500 transition-all"
        :class="isDark ? 'bg-red-500/5 border border-red-500/20' : 'bg-red-50 border border-red-200'">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center mb-3"
          :class="isDark ? 'bg-red-500/15' : 'bg-red-100'">
          <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/>
          </svg>
        </div>
        <h4 class="text-body-sm font-bold text-red-500 mb-1">Seek Medical Attention</h4>
        <p class="text-detail leading-relaxed" :class="isDark ? 'text-red-300/80' : 'text-red-700'">
          Warning signs were detected. Contact a healthcare provider or visit urgent care as soon as possible.
        </p>
        <div v-if="redFlags.length" class="mt-2 space-y-1">
          <div v-for="flag in redFlags.slice(0, 3)" :key="flag" class="text-detail flex items-start gap-1.5"
            :class="isDark ? 'text-red-300/70' : 'text-red-600'">
            <span class="font-bold flex-shrink-0">!</span>
            <span>{{ typeof flag === 'object' ? flag.title || flag.message || JSON.stringify(flag) : flag }}</span>
          </div>
        </div>
      </div>

      <!-- See a Doctor card -->
      <div v-if="showSeeDoctor"
        class="rounded-card p-4 border-l-4 border-l-amber-500 transition-all"
        :class="isDark ? 'bg-amber-500/5 border border-amber-500/20' : 'bg-amber-50 border border-amber-200'">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center mb-3"
          :class="isDark ? 'bg-amber-500/15' : 'bg-amber-100'">
          <svg class="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
        <h4 class="text-body-sm font-bold text-amber-500 mb-1">Schedule an Appointment</h4>
        <p class="text-detail leading-relaxed" :class="isDark ? 'text-amber-300/80' : 'text-amber-700'">
          {{ specialistName ? `See a ${specialistName} within the next few days.` : 'Schedule a visit with your primary care doctor.' }}
        </p>
        <div v-if="recommendedTests.length" class="mt-2 text-detail" :class="isDark ? 'text-amber-300/60' : 'text-amber-600'">
          {{ recommendedTests.length }} test{{ recommendedTests.length > 1 ? 's' : '' }} recommended
        </div>
      </div>

      <!-- Self-care card (always shown) -->
      <div class="rounded-card p-4 border-l-4 border-l-emerald-500 transition-all"
        :class="isDark ? 'bg-emerald-500/5 border border-emerald-500/20' : 'bg-emerald-50 border border-emerald-200'">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center mb-3"
          :class="isDark ? 'bg-emerald-500/15' : 'bg-emerald-100'">
          <svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
          </svg>
        </div>
        <h4 class="text-body-sm font-bold text-emerald-500 mb-1">{{ showEmergency ? 'Meanwhile' : 'Self-Care at Home' }}</h4>
        <p class="text-detail leading-relaxed" :class="isDark ? 'text-emerald-300/80' : 'text-emerald-700'">
          {{ showEmergency ? 'While awaiting care, rest and stay hydrated. Monitor your symptoms closely.' : 'Monitor symptoms, rest, and follow the lifestyle recommendations below.' }}
        </p>
        <div v-if="actionCount > 0" class="mt-2 text-detail" :class="isDark ? 'text-emerald-300/60' : 'text-emerald-600'">
          {{ actionCount }} action item{{ actionCount > 1 ? 's' : '' }} to follow
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  urgency: { type: String, default: 'routine' },
  redFlags: { type: Array, default: () => [] },
  recommendedTests: { type: Array, default: () => [] },
  specialties: { type: Array, default: () => [] },
  actionCount: { type: Number, default: 0 },
})

const showEmergency = computed(() =>
  props.urgency === 'emergency' || props.urgency === 'urgent' || props.redFlags.length > 0
)

const showSeeDoctor = computed(() =>
  props.urgency !== 'routine' || props.recommendedTests.length > 0 || props.specialties.length > 0
)

const specialistName = computed(() => {
  if (!props.specialties.length) return ''
  return props.specialties[0].replace(/_/g, ' ')
})
</script>
