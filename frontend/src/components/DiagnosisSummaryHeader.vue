<template>
  <section id="section-summary" ref="rootRef" class="print-section">
    <div class="rounded-2xl overflow-hidden border transition-colors relative"
      :class="isDark
        ? 'bg-gradient-to-br from-slate-800/90 via-slate-800/70 to-slate-900/90 border-slate-700/40 shadow-2xl'
        : 'bg-white border-slate-200 shadow-xl shadow-slate-200/60'">

      <!-- Top accent bar -->
      <div class="h-1" :class="urgencyAccentClass"></div>

      <div class="p-6 sm:p-8 lg:p-10">
        <!-- Row 1: Primary Diagnosis + Confidence + Urgency -->
        <div class="flex flex-col lg:flex-row lg:items-start gap-6 lg:gap-10">

          <!-- Left: Diagnosis content -->
          <div class="flex-1 min-w-0 space-y-5">

            <!-- Urgency banner (if urgent/emergent) -->
            <div v-if="isUrgent" class="flex items-center gap-3 px-4 py-3 rounded-xl border"
              :class="isDark
                ? 'bg-red-500/10 border-red-500/25'
                : 'bg-red-50 border-red-200'">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="isDark ? 'bg-red-500/20' : 'bg-red-100'">
                <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
                </svg>
              </div>
              <div>
                <p class="text-sm font-semibold" :class="isDark ? 'text-red-300' : 'text-red-700'">Urgent medical attention may be needed</p>
                <p class="text-xs mt-0.5" :class="isDark ? 'text-red-400/70' : 'text-red-600/80'">
                  Based on the symptoms analyzed, we recommend consulting a healthcare professional promptly.
                </p>
              </div>
            </div>

            <!-- Overline label -->
            <div class="flex items-center gap-2">
              <span class="text-caption font-semibold uppercase tracking-widest"
                :class="isDark ? 'text-blue-400' : 'text-blue-600'">Primary Assessment</span>
              <span class="px-2.5 py-0.5 rounded-full text-detail font-bold uppercase tracking-wider"
                :class="urgencyBadgeClass">{{ urgency }}</span>
            </div>

            <!-- Primary diagnosis name -->
            <h2 class="text-2xl sm:text-3xl lg:text-[2.1rem] font-extrabold leading-tight tracking-tight"
              :class="isDark ? 'text-white' : 'text-slate-900'">
              {{ topCause.cause || 'Awaiting Analysis' }}
            </h2>

            <!-- Specialty tag -->
            <div v-if="topCause.specialty" class="flex items-center gap-2">
              <svg class="w-4 h-4" :class="isDark ? 'text-slate-400' : 'text-slate-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
              </svg>
              <span class="text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ topCause.specialty }}</span>
            </div>

            <!-- Plain-language explanation -->
            <p v-if="explanation" class="text-[15px] sm:text-base leading-relaxed max-w-2xl"
              :class="isDark ? 'text-slate-300' : 'text-[#334155]'"
              style="line-height: 1.7">
              {{ explanation }}
            </p>

            <!-- Chief complaint callout -->
            <div v-if="chiefComplaint" class="flex items-start gap-3 px-4 py-3 rounded-xl border-l-4 border-blue-500"
              :class="isDark ? 'bg-slate-700/30' : 'bg-blue-50/60'">
              <svg class="w-4 h-4 mt-0.5 flex-shrink-0 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
              </svg>
              <div>
                <div class="text-detail font-bold uppercase tracking-widest mb-1"
                  :class="isDark ? 'text-slate-400' : 'text-slate-600'">Presenting Complaint</div>
                <p class="text-sm font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ chiefComplaint }}</p>
              </div>
            </div>
          </div>

          <!-- Right: Confidence + Illustration + Stats -->
          <div class="flex flex-row lg:flex-col items-start lg:items-center gap-5 flex-shrink-0">

            <!-- Confidence ring + Illustration side by side -->
            <div class="flex flex-row items-start gap-5">
              <!-- Confidence ring + differential bars -->
              <div v-if="topCause.value" class="relative flex flex-col items-center">
                <div class="w-28 h-28 rounded-full flex items-center justify-center relative"
                  :style="confidenceRingStyle">
                  <div class="text-center">
                    <div class="text-3xl font-black tabular-nums" :style="{ color: confidenceColor }">
                      {{ topCause.value }}%
                    </div>
                    <div class="text-tiny font-bold uppercase tracking-widest mt-0.5"
                      :class="isDark ? 'text-slate-400' : 'text-slate-600'">confidence</div>
                  </div>
                </div>
                <!-- Primary diagnosis name + confidence label -->
                <div class="mt-3 text-center">
                  <div class="text-xs font-bold truncate max-w-[180px]" :class="isDark ? 'text-white' : 'text-slate-900'">{{ topCause.cause || 'Awaiting Analysis' }}</div>
                  <span class="text-caption font-semibold"
                    :style="{ color: confidenceColor }">{{ confidenceLabel }}</span>
                </div>

                <!-- Separator -->
                <div class="w-full my-4 border-t" :class="isDark ? 'border-slate-700/60' : 'border-slate-200'"></div>

                <!-- Mini differential chart -->
                <div v-if="otherCauses.length > 0" class="w-full space-y-1.5">
                  <div v-for="c in otherCauses" :key="c.cause" class="flex items-center gap-2">
                    <div class="flex-1 min-w-0">
                      <div class="flex items-center justify-between mb-0.5">
                        <span class="text-tiny font-medium truncate" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ c.cause.length > 22 ? c.cause.slice(0, 22) + '...' : c.cause }}</span>
                        <span class="text-tiny font-bold tabular-nums ml-1" :style="{ color: miniBarColor(c.value) }">{{ c.value }}%</span>
                      </div>
                      <div class="h-1.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700/60' : 'bg-slate-200'">
                        <div class="h-full rounded-full transition-all duration-700" :style="{ width: c.value + '%', background: miniBarColor(c.value) }"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Medical Illustration -->
              <div v-if="topCause.cause" class="hidden lg:block">
                <MedicalIllustration
                  :condition="topCause.cause || ''"
                  :specialty="topCause.specialty || ''"
                  :size="180"
                />
              </div>
            </div>

            <!-- Stat pills -->
            <div class="flex flex-row lg:flex-col gap-2">
              <div class="flex items-center gap-1.5 text-xs px-3 py-2 rounded-xl border"
                :class="isDark ? 'bg-slate-700/40 border-slate-600/40 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-600'">
                <svg class="w-3.5 h-3.5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                <span class="font-semibold">{{ causesCount }}</span> conditions
              </div>
              <div v-if="testsCount > 0" class="flex items-center gap-1.5 text-xs px-3 py-2 rounded-xl border"
                :class="isDark ? 'bg-slate-700/40 border-slate-600/40 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-600'">
                <svg class="w-3.5 h-3.5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
                <span class="font-semibold">{{ testsCount }}</span> tests
              </div>
              <div v-if="flagsCount > 0" class="flex items-center gap-1.5 text-xs px-3 py-2 rounded-xl border"
                :class="isDark ? 'bg-red-500/10 border-red-500/20 text-red-300' : 'bg-red-50 border-red-200 text-red-600'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                <span class="font-semibold">{{ flagsCount }}</span> {{ flagsCount === 1 ? 'flag' : 'flags' }}
              </div>
            </div>
          </div>
        </div>

        <!-- Divider -->
        <div class="my-6 h-px" :class="isDark ? 'bg-slate-700/40' : 'bg-slate-200'"></div>

        <!-- Row 2: Immediate Recommended Action -->
        <div class="rounded-xl p-5 border"
          :class="isDark
            ? 'bg-slate-700/25 border-slate-600/30'
            : 'bg-slate-50 border-slate-200'">
          <div class="flex items-center gap-2 mb-3">
            <svg class="w-5 h-5" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
            <h3 class="text-sm font-bold uppercase tracking-wider"
              :class="isDark ? 'text-slate-200' : 'text-slate-700'">Recommended Next Steps</h3>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <!-- Self-care -->
            <div class="flex items-start gap-3 p-3 rounded-lg"
              :class="isDark ? 'bg-slate-700/30' : 'bg-white border border-slate-200'">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="isDark ? 'bg-blue-500/15' : 'bg-blue-50'">
                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
                </svg>
              </div>
              <div>
                <div class="text-xs font-semibold mb-0.5" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Self-Care</div>
                <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Monitor symptoms and follow recommended lifestyle guidance below.</p>
              </div>
            </div>
            <!-- See a doctor -->
            <div class="flex items-start gap-3 p-3 rounded-lg"
              :class="isDark ? 'bg-slate-700/30' : 'bg-white border border-slate-200'">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="isDark ? 'bg-amber-500/15' : 'bg-amber-50'">
                <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
              <div>
                <div class="text-xs font-semibold mb-0.5" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Schedule a Visit</div>
                <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
                  {{ topCause.specialty ? `Consult a ${topCause.specialty} specialist` : 'See your primary care physician' }} for clinical evaluation.
                </p>
              </div>
            </div>
            <!-- Urgent care -->
            <div class="flex items-start gap-3 p-3 rounded-lg"
              :class="isDark ? 'bg-slate-700/30' : 'bg-white border border-slate-200'">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :class="isDark ? 'bg-red-500/15' : 'bg-red-50'">
                <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <div class="text-xs font-semibold mb-0.5" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Seek Urgent Care If</div>
                <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Symptoms worsen rapidly, new concerning symptoms appear, or you experience severe pain.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Row 3: Quick actions -->
        <div class="flex flex-wrap items-center gap-3 mt-6">
          <button @click="$emit('download-pdf')" :disabled="exporting"
            class="flex items-center gap-2 px-5 py-2.5 text-sm font-semibold rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 hover:to-blue-600 text-white shadow-lg shadow-blue-500/20 transition-all disabled:opacity-60">
            <svg v-if="exporting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            {{ exporting ? 'Exporting...' : 'Download Report' }}
          </button>
          <button @click="$emit('email')"
            class="flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-xl border transition-colors"
            :class="isDark ? 'bg-slate-700/40 hover:bg-slate-700 border-slate-600/40 text-slate-200' : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            Send to Doctor
          </button>
          <button @click="$emit('copy-summary')"
            class="flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-xl border transition-colors"
            :class="copiedSummary
              ? 'bg-emerald-500/15 border-emerald-500/30 text-emerald-400'
              : (isDark ? 'bg-slate-700/40 hover:bg-slate-700 border-slate-600/40 text-slate-200' : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700')">
            <svg v-if="copiedSummary" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
            {{ copiedSummary ? 'Copied!' : 'Copy Summary' }}
          </button>
          <router-link to="/consult"
            class="flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-xl border transition-colors"
            :class="isDark ? 'bg-slate-700/40 hover:bg-slate-700 border-slate-600/40 text-slate-200' : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            New Assessment
          </router-link>
          <button @click="$emit('find-specialists')"
            class="flex items-center gap-2 px-4 py-2.5 text-sm font-medium rounded-xl border transition-colors"
            :class="isDark ? 'bg-emerald-500/10 hover:bg-emerald-500/20 border-emerald-500/30 text-emerald-400' : 'bg-emerald-50 hover:bg-emerald-100 border-emerald-200 text-emerald-700'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            Find Specialists
          </button>
        </div>

        <!-- Disclaimer -->
        <p class="text-caption mt-5 pt-4 border-t leading-relaxed"
          :class="isDark ? 'text-slate-500 border-slate-700/30' : 'text-[#64748B] border-slate-200'"
          style="line-height: 1.6">
          This AI-generated clinical assessment is for informational purposes only and does not constitute medical advice, diagnosis, or treatment.
          Always seek the guidance of a qualified healthcare professional with any questions regarding a medical condition.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import BodyAreaIcon from './BodyAreaIcon.vue'
import MedicalIllustration from './MedicalIllustration.vue'

const { isDark } = useTheme()

const props = defineProps({
  causes: { type: Array, default: () => [] },
  urgency: { type: String, default: 'Unknown' },
  urgencyBadgeClass: { type: String, default: '' },
  chiefComplaint: { type: String, default: '' },
  patientSummary: { type: String, default: '' },
  causesCount: { type: Number, default: 0 },
  testsCount: { type: Number, default: 0 },
  flagsCount: { type: Number, default: 0 },
  exporting: { type: Boolean, default: false },
  copiedSummary: { type: Boolean, default: false },
})

defineEmits(['download-pdf', 'email', 'copy-summary', 'find-specialists'])

const topCause = computed(() => props.causes[0] || {})
const otherCauses = computed(() => props.causes.slice(1, 5))

const barColors = ['#8b5cf6', '#3b82f6', '#06b6d4', '#f59e0b', '#ef4444']
function miniBarColor(value) {
  if (value >= 60) return '#10b981'
  if (value >= 40) return '#f59e0b'
  if (value >= 20) return '#3b82f6'
  return '#8b5cf6'
}

const explanation = computed(() =>
  topCause.value.explanation || props.patientSummary || ''
)

// Derive body area from diagnosis name + specialty for icon display
const bodyAreaKey = computed(() => {
  const text = ((topCause.value.cause || '') + ' ' + (topCause.value.specialty || '')).toLowerCase()
  return text
})

const isUrgent = computed(() => {
  const u = props.urgency?.toLowerCase() || ''
  return u.includes('urgent') || u.includes('emergent') || u.includes('emergency')
})

const confidenceColor = computed(() => {
  const v = topCause.value.value || 0
  if (v >= 70) return '#22c55e'
  if (v >= 40) return '#f59e0b'
  return '#3b82f6'
})

const confidenceLabel = computed(() => {
  const v = topCause.value.value || 0
  if (v >= 80) return 'High Confidence'
  if (v >= 60) return 'Moderate-High'
  if (v >= 40) return 'Moderate'
  if (v >= 20) return 'Low-Moderate'
  return 'Preliminary'
})

const confidenceRingStyle = computed(() => {
  const color = confidenceColor.value
  return isDark.value
    ? { background: `${color}12`, boxShadow: `inset 0 0 0 4px ${color}30, 0 0 20px ${color}10` }
    : { background: `${color}08`, boxShadow: `inset 0 0 0 4px ${color}25` }
})

const urgencyAccentClass = computed(() => {
  const u = props.urgency?.toLowerCase() || ''
  if (u.includes('urgent') || u.includes('emergent') || u.includes('emergency')) return 'bg-gradient-to-r from-red-500 via-red-400 to-orange-400'
  if (u.includes('soon') || u.includes('moderate')) return 'bg-gradient-to-r from-amber-500 via-amber-400 to-yellow-400'
  return 'bg-gradient-to-r from-blue-500 via-blue-400 to-cyan-400'
})
</script>
