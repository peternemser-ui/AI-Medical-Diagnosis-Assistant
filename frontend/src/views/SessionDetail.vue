<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-gradient-to-br from-slate-950 via-slate-900 to-gray-900 text-white' : 'bg-gradient-to-br from-slate-50 via-white to-slate-100 text-slate-900'">
    <!-- Nav -->
    <div class="backdrop-blur-xl border-b py-3 px-6 transition-colors" :class="isDark ? 'bg-slate-950/90 border-slate-800/50' : 'bg-white/90 border-slate-200'">
      <div class="max-w-5xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <router-link to="/reports" class="flex items-center gap-2 text-sm transition-colors" :class="isDark ? 'text-slate-400 hover:text-white' : 'text-slate-500 hover:text-slate-900'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
            Back to Reports
          </router-link>
        </div>
        <div class="flex items-center gap-2">
          <ThemeLangControls />
          <button @click="exportPdf" :disabled="isExporting" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-50 transition-colors">
            <svg v-if="!isExporting" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <svg v-else class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
            {{ isExporting ? 'Exporting...' : 'Export PDF' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-5xl mx-auto px-4 py-6" ref="reportContent">
      <!-- Not found -->
      <div v-if="!session" class="flex flex-col items-center text-center py-20 px-4">
        <div class="w-14 h-14 rounded-2xl flex items-center justify-center mb-5" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
          <svg class="w-7 h-7" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <h2 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Session Not Found</h2>
        <p class="text-sm mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">This consultation may have been deleted or the link is invalid.</p>
        <p class="text-xs mb-6" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Consultations are stored locally on your device and may be cleared if browser data is deleted.</p>
        <div class="flex gap-3">
          <router-link to="/reports" class="px-4 py-2 rounded-lg text-xs font-medium transition-colors" :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">View All Reports</router-link>
          <router-link to="/consult" class="px-4 py-2 rounded-lg text-xs font-medium bg-blue-600 text-white hover:bg-blue-500 transition-colors">Start New Consultation</router-link>
        </div>
      </div>

      <template v-else>
        <!-- Session header -->
        <div class="mb-6">
          <div class="flex items-start justify-between flex-wrap gap-3">
            <div>
              <h1 class="text-xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Consultation Report</h1>
              <div class="flex items-center gap-3 mt-1 text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                <span>{{ formatDate(session.timestamp) }}</span>
                <span v-if="session.age">Age: {{ session.age }}</span>
                <span v-if="session.gender" class="capitalize">{{ session.gender }}</span>
              </div>
            </div>
            <span v-if="topUrgency" class="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider" :class="urgencyClass">{{ topUrgency }}</span>
          </div>

          <!-- Symptoms summary -->
          <div v-if="session.symptoms" class="mt-4 p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-slate-50 border-slate-200'">
            <div class="text-[10px] uppercase font-semibold mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Chief Complaint</div>
            <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ session.symptoms }}</p>
          </div>
        </div>

        <!-- Confidence Chart -->
        <div v-if="causes.length > 0" class="mb-6 p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-white border-slate-200 shadow-sm'">
          <h2 class="text-xs font-bold uppercase tracking-wide mb-4" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Diagnosis Confidence</h2>
          <div class="space-y-3">
            <div v-for="(cause, i) in causes" :key="'chart-'+i" class="flex items-center gap-3">
              <div class="w-6 text-right text-[10px] font-bold flex-shrink-0" :class="isDark ? 'text-slate-500' : 'text-slate-400'">#{{ i+1 }}</div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-xs font-medium truncate pr-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ cause.cause }}</span>
                  <span class="text-xs font-bold flex-shrink-0" :class="cause.value >= 50 ? 'text-emerald-500' : cause.value >= 20 ? 'text-amber-500' : (isDark ? 'text-slate-400' : 'text-slate-500')">{{ cause.value }}%</span>
                </div>
                <div class="w-full h-2.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700/50' : 'bg-slate-100'">
                  <div class="h-full rounded-full transition-all duration-1000 ease-out" :style="{ width: cause.value + '%' }" :class="cause.value >= 50 ? 'bg-emerald-500' : cause.value >= 20 ? 'bg-amber-500' : (isDark ? 'bg-slate-500' : 'bg-slate-300')"></div>
                </div>
              </div>
              <span class="text-[9px] font-semibold uppercase px-1.5 py-0.5 rounded flex-shrink-0" :class="cause.urgency === 'urgent' || cause.urgency === 'emergency' ? (isDark ? 'bg-red-500/20 text-red-400' : 'bg-red-50 text-red-600') : (isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-100 text-slate-500')">{{ cause.urgency }}</span>
            </div>
          </div>
        </div>

        <!-- Agent Performance (if available) -->
        <div v-if="session.diagnosisResult && session.diagnosisResult.agent_timings" class="mb-6 p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-white border-slate-200 shadow-sm'">
          <h2 class="text-xs font-bold uppercase tracking-wide mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Agent Performance</h2>
          <div class="space-y-2">
            <div v-for="(time, agent) in session.diagnosisResult.agent_timings" :key="agent" class="flex items-center justify-between text-xs">
              <span class="capitalize" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ agent.replace(/_/g, ' ') }}</span>
              <span class="font-mono font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ typeof time === 'number' ? time.toFixed(1) + 's' : time }}</span>
            </div>
            <div class="pt-2 border-t flex items-center justify-between text-xs font-bold" :class="isDark ? 'border-slate-700 text-white' : 'border-slate-200 text-slate-900'">
              <span>Total</span>
              <span>{{ session.diagnosisResult.total_time ? session.diagnosisResult.total_time.toFixed(1) + 's' : '—' }}</span>
            </div>
          </div>
        </div>

        <!-- Diagnoses -->
        <div v-if="causes.length > 0" class="mb-6">
          <h2 class="text-sm font-bold uppercase tracking-wide mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Differential Diagnoses</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <DiagnosisCard
              v-for="(cause, i) in causes" :key="i"
              :cause="cause" :rank="i + 1"
              :red-flags="i === 0 ? redFlags : []"
              :recommended-tests="i === 0 ? recommendedTests : []"
            />
          </div>
        </div>

        <!-- Tests & Actions -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div v-if="recommendedTests.length" class="p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-white border-slate-200 shadow-sm'">
            <h3 class="text-xs font-bold uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Recommended Tests</h3>
            <ul class="space-y-1">
              <li v-for="test in recommendedTests" :key="test" class="text-xs flex items-start gap-2" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
                <span class="text-blue-400 mt-0.5">&#8226;</span>{{ test }}
              </li>
            </ul>
          </div>
          <div v-if="actionChecklist.length" class="p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-white border-slate-200 shadow-sm'">
            <h3 class="text-xs font-bold uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Action Items</h3>
            <ul class="space-y-1">
              <li v-for="item in actionChecklist" :key="item" class="text-xs flex items-start gap-2" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
                <span class="text-amber-400 mt-0.5">&#9744;</span>{{ item }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Red Flags -->
        <div v-if="redFlags.length" class="mb-6 p-4 rounded-xl border" :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-200'">
          <h3 class="text-xs font-bold uppercase tracking-wide mb-2 text-red-400">Red Flags</h3>
          <ul class="space-y-1">
            <li v-for="flag in redFlags" :key="flag" class="text-xs flex items-start gap-2 text-red-300">
              <span class="text-red-500 mt-0.5">!</span>{{ flag }}
            </li>
          </ul>
        </div>

        <!-- Treatment Plan -->
        <div v-if="treatments.length || medications.length || lifestyleRecs.length" class="mb-6 p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-xs font-bold uppercase tracking-wide mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
            <span class="inline-flex items-center gap-1.5">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
              Treatment Plan
            </span>
          </h3>
          <div class="space-y-3">
            <div v-if="medications.length">
              <div class="text-[10px] font-semibold uppercase mb-1.5" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Medications</div>
              <ul class="space-y-1">
                <li v-for="med in medications" :key="typeof med === 'string' ? med : med.name" class="text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  <span class="font-medium">{{ typeof med === 'string' ? med : med.name }}</span>
                  <span v-if="med.dose" class="text-slate-400"> — {{ med.dose }}</span>
                  <span v-if="med.warnings" class="text-amber-400 text-[10px]"> ({{ med.warnings }})</span>
                </li>
              </ul>
            </div>
            <div v-if="lifestyleRecs.length">
              <div class="text-[10px] font-semibold uppercase mb-1.5" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Lifestyle Recommendations</div>
              <ul class="space-y-1">
                <li v-for="rec in lifestyleRecs" :key="rec" class="text-xs flex items-start gap-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  <span class="text-emerald-400 mt-0.5">&#10003;</span>{{ rec }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Find a Doctor -->
        <div v-if="causes.length > 0" class="mb-6 p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-xs font-bold uppercase tracking-wide mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
            <span class="inline-flex items-center gap-1.5">
              <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              Find Nearby Specialists
            </span>
          </h3>
          <p class="text-xs mb-3" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Search for specialists related to your diagnosis:</p>
          <div class="flex flex-wrap gap-2">
            <a v-for="cause in causes.slice(0, 3)" :key="'doc-'+cause.cause"
              :href="'https://www.google.com/maps/search/' + encodeURIComponent((cause.specialty || 'doctor') + ' near me')"
              target="_blank" rel="noopener"
              class="inline-flex items-center gap-1.5 text-xs px-3 py-2 rounded-lg border transition-colors"
              :class="isDark ? 'bg-slate-700/50 border-slate-600/50 text-slate-300 hover:bg-slate-700 hover:text-white' : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700'"
            >
              <svg class="w-3.5 h-3.5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              Find {{ cause.specialty || 'Doctor' }} near me
            </a>
          </div>
          <p class="text-[10px] mt-3" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Opens Google Maps to find specialists in your area. Always verify credentials and check with your insurance provider.</p>
        </div>

        <!-- Chat transcript -->
        <div v-if="session.chatMessages && session.chatMessages.length" class="mb-6">
          <h2 class="text-sm font-bold uppercase tracking-wide mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Conversation Transcript</h2>
          <div class="space-y-2 max-h-[500px] overflow-y-auto pr-2">
            <div v-for="(msg, i) in session.chatMessages" :key="i"
              class="p-3 rounded-lg text-xs leading-relaxed"
              :class="msg.sender === 'user'
                ? (isDark ? 'bg-blue-500/10 border border-blue-500/20 text-blue-200 ml-8' : 'bg-blue-50 border border-blue-200 text-blue-800 ml-8')
                : (isDark ? 'bg-slate-800/60 border border-slate-700/40 text-slate-300 mr-8' : 'bg-slate-50 border border-slate-200 text-slate-600 mr-8')"
            >
              <div class="text-[10px] font-semibold uppercase mb-1" :class="msg.sender === 'user' ? 'text-blue-400' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                {{ msg.sender === 'user' ? 'You' : 'Dr. AI' }}
              </div>
              {{ msg.text }}
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getSession } from '@/services/historyService.js'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import DiagnosisCard from '@/components/DiagnosisCard.vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
const route = useRoute()
const session = ref(null)
const isExporting = ref(false)
const reportContent = ref(null)

onMounted(() => {
  const id = route.params.id
  if (id) session.value = getSession(id)
})

const causes = computed(() => session.value?.diagnosisResult?.causes || [])
const redFlags = computed(() => session.value?.diagnosisResult?.red_flags || session.value?.diagnosisResult?.redFlags || [])
const recommendedTests = computed(() => session.value?.diagnosisResult?.recommended_tests || session.value?.diagnosisResult?.recommendedTests || [])
const actionChecklist = computed(() => session.value?.diagnosisResult?.action_checklist || session.value?.diagnosisResult?.actionChecklist || [])
const medications = computed(() => session.value?.diagnosisResult?.medications || [])
const lifestyleRecs = computed(() => session.value?.diagnosisResult?.lifestyle_recommendations || session.value?.diagnosisResult?.lifestyleRecommendations || [])
const treatments = computed(() => session.value?.diagnosisResult?.treatment_plans || [])

const topUrgency = computed(() => {
  if (!causes.value.length) return ''
  const u = causes.value.map(c => c.urgency || 'routine')
  if (u.includes('emergency')) return 'emergency'
  if (u.includes('urgent')) return 'urgent'
  if (u.includes('soon')) return 'soon'
  return 'routine'
})

const urgencyClass = computed(() => {
  const u = topUrgency.value
  if (u === 'emergency') return 'bg-red-500/20 text-red-300 border border-red-500/30'
  if (u === 'urgent') return 'bg-red-500/15 text-red-400 border border-red-500/20'
  if (u === 'soon') return 'bg-amber-500/15 text-amber-400 border border-amber-500/20'
  return 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20'
})

function formatDate(ts) {
  try { return new Date(ts).toLocaleString() } catch { return ts }
}

async function exportPdf() {
  if (isExporting.value || !reportContent.value) return
  isExporting.value = true
  try {
    const html2pdf = (await import('html2pdf.js')).default
    await html2pdf().set({
      margin: [10, 10, 10, 10],
      filename: `consultation-${route.params.id}.pdf`,
      image: { type: 'jpeg', quality: 0.95 },
      html2canvas: { scale: 2, backgroundColor: isDark.value ? '#0f172a' : '#ffffff' },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }).from(reportContent.value).save()
  } catch (err) {
    console.error('PDF export failed:', err)
  } finally {
    isExporting.value = false
  }
}
</script>
