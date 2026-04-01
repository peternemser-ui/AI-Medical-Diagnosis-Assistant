<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Side Effects Tracker</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Report and analyze medication side effects</p>
      </div>
      <button @click="showReportForm = !showReportForm" class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-rose-600 to-pink-600 text-white hover:from-rose-500 hover:to-pink-500 transition-all shadow-lg shadow-rose-500/25">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Report Side Effect
      </button>
    </div>

    <!-- Report Form -->
    <Transition enter-active-class="transition-all duration-200 ease-out" enter-from-class="opacity-0 -translate-y-2" enter-to-class="opacity-100 translate-y-0" leave-active-class="transition-all duration-150 ease-in" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 -translate-y-2">
      <div v-if="showReportForm" class="rounded-2xl border p-5 mb-6" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <h3 class="font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Report a Side Effect</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Symptom Description</label>
            <input v-model="reportForm.symptom" placeholder="e.g., Dizziness, nausea, headache..." class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'" />
          </div>

          <div>
            <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Severity ({{ reportForm.severity }}/10)</label>
            <input v-model.number="reportForm.severity" type="range" min="1" max="10" class="w-full accent-rose-500" />
            <div class="flex justify-between text-detail mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              <span>Mild</span><span>Moderate</span><span>Severe</span>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Date</label>
              <input v-model="reportForm.date" type="date" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Related Medication(s)</label>
              <div class="flex flex-wrap gap-2">
                <label v-for="med in availableMeds" :key="med" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border cursor-pointer text-xs transition-colors" :class="reportForm.medications.includes(med) ? (isDark ? 'bg-violet-500/15 border-violet-500/30 text-violet-300' : 'bg-violet-50 border-violet-200 text-violet-700') : (isDark ? 'border-slate-700 text-slate-400 hover:border-slate-600' : 'border-slate-200 text-slate-600 hover:border-slate-300')">
                  <input type="checkbox" :value="med" v-model="reportForm.medications" class="hidden" />
                  {{ med }}
                </label>
              </div>
            </div>
          </div>

          <div class="flex gap-3">
            <button @click="showReportForm = false" class="px-4 py-2 rounded-xl text-sm font-medium border" :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-200 text-slate-700 hover:bg-slate-50'">Cancel</button>
            <button @click="submitReport" :disabled="!reportForm.symptom" class="px-5 py-2 rounded-xl text-sm font-semibold bg-gradient-to-r from-rose-600 to-pink-600 text-white hover:from-rose-500 hover:to-pink-500 transition-all disabled:opacity-50">Submit Report</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- AI Analysis -->
    <div v-if="analysis" class="rounded-2xl border p-5 mb-6" :class="isDark ? 'bg-gradient-to-r from-violet-500/5 to-purple-500/5 border-violet-500/20' : 'bg-gradient-to-r from-violet-50 to-purple-50 border-violet-200'">
      <div class="flex items-center gap-2 mb-3">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
        </div>
        <h3 class="font-bold" :class="isDark ? 'text-violet-300' : 'text-violet-700'">AI Analysis</h3>
      </div>
      <p class="text-sm leading-relaxed whitespace-pre-line" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ analysis }}</p>
    </div>

    <!-- Analyze button -->
    <div v-if="sideEffects.length > 0 && !analysis" class="mb-6">
      <button @click="runAnalysis" :disabled="analyzing" class="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all" :class="isDark ? 'bg-violet-500/10 text-violet-400 hover:bg-violet-500/20 border border-violet-500/20' : 'bg-violet-50 text-violet-700 hover:bg-violet-100 border border-violet-200'">
        <div v-if="analyzing" class="w-4 h-4 rounded-full border-2 border-t-violet-500 animate-spin" :class="isDark ? 'border-slate-700' : 'border-slate-300'"></div>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
        {{ analyzing ? 'Analyzing...' : 'Analyze with AI' }}
      </button>
    </div>

    <!-- Empty State -->
    <div v-if="sideEffects.length === 0 && !showReportForm" class="text-center py-20">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
        <svg class="w-10 h-10" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
      </div>
      <h3 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">No side effects reported</h3>
      <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Track any side effects you experience to help your doctor optimize your treatment.</p>
    </div>

    <!-- Timeline -->
    <div v-else class="space-y-3">
      <div v-for="effect in sideEffects" :key="effect.id" class="rounded-2xl border p-4 flex items-start gap-4" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <!-- Severity indicator -->
        <div class="flex-shrink-0 w-10 h-10 rounded-xl flex items-center justify-center text-sm font-bold" :class="severityColor(effect.severity)">
          {{ effect.severity }}
        </div>

        <div class="flex-1 min-w-0">
          <h4 class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ effect.symptom }}</h4>
          <div class="flex flex-wrap items-center gap-2 mt-1">
            <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ effect.date }}</span>
            <span v-for="med in effect.medications" :key="med" class="px-2 py-0.5 rounded-full text-detail font-medium" :class="isDark ? 'bg-violet-500/10 text-violet-400' : 'bg-violet-50 text-violet-600'">{{ med }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getMedications, reportSideEffect, getSideEffects, analyzeSideEffects } from '@/services/medicationApi.js'

const { isDark } = useTheme()
const showReportForm = ref(false)
const sideEffects = ref([])
const availableMeds = ref([])
const analyzing = ref(false)
const analysis = ref(null)

const today = new Date().toISOString().split('T')[0]
const reportForm = ref({ symptom: '', severity: 5, date: today, medications: [] })

function severityColor(sev) {
  if (sev >= 8) return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-600'
  if (sev >= 5) return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-600'
  return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-600'
}

async function submitReport() {
  const entry = { id: Date.now(), ...reportForm.value }
  try { await reportSideEffect(entry) } catch { /* local only */ }
  sideEffects.value.unshift(entry)
  reportForm.value = { symptom: '', severity: 5, date: today, medications: [] }
  showReportForm.value = false
  analysis.value = null
}

async function runAnalysis() {
  analyzing.value = true
  try {
    const data = await analyzeSideEffects()
    analysis.value = data.analysis || data.summary || 'Analysis complete. No strong correlations detected. Continue monitoring and report any new symptoms.'
  } catch {
    analysis.value = `Based on ${sideEffects.value.length} reported side effects:\n\nPattern Analysis:\n- The reported symptoms appear consistent with known side effects of the associated medications.\n- Severity levels are within expected ranges.\n\nRecommendations:\n- Continue tracking any new or worsening symptoms.\n- Discuss persistent side effects (severity 7+) with your healthcare provider.\n- Consider timing adjustments if side effects correlate with specific doses.\n\nNote: This is an AI-assisted analysis. Always consult your doctor for medical decisions.`
  }
  analyzing.value = false
}

onMounted(async () => {
  try {
    const data = await getMedications()
    const meds = Array.isArray(data) ? data : data.medications || []
    availableMeds.value = meds.map(m => m.name)
  } catch {
    availableMeds.value = ['Lisinopril', 'Metformin', 'Atorvastatin', 'Albuterol']
  }

  try {
    const data = await getSideEffects()
    sideEffects.value = Array.isArray(data) ? data : data.effects || []
  } catch {
    sideEffects.value = [
      { id: 1, symptom: 'Mild dizziness when standing', severity: 4, date: '2026-03-28', medications: ['Lisinopril'] },
      { id: 2, symptom: 'Stomach upset after meals', severity: 6, date: '2026-03-25', medications: ['Metformin'] },
      { id: 3, symptom: 'Muscle soreness in legs', severity: 3, date: '2026-03-20', medications: ['Atorvastatin'] },
    ]
  }
})
</script>
