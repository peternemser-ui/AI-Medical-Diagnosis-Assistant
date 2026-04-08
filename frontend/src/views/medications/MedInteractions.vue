<template>
  <div>
    <!-- ── Header ── -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-[var(--text-primary)]">Drug Interactions</h1>
        <p class="text-sm mt-1 text-[var(--text-secondary)]">Safety matrix — check how your medications interact</p>
      </div>
    </div>

    <!-- ── Summary bar ── -->
    <div v-if="medications.length >= 2 && !loading" class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
      <div class="rounded-xl p-3.5 border-l-4 border-red-500"
        :class="isDark ? 'bg-slate-900 border border-slate-800' : 'bg-white border border-slate-200'">
        <div class="flex items-center gap-2 mb-0.5">
          <div class="w-2.5 h-2.5 rounded-full bg-red-500 flex-shrink-0"></div>
          <span class="text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Major</span>
        </div>
        <div class="text-xl font-bold" :class="isDark ? 'text-red-400' : 'text-red-600'">{{ counts.major }}</div>
        <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">dangerous pairs</div>
      </div>
      <div class="rounded-xl p-3.5 border-l-4 border-orange-500"
        :class="isDark ? 'bg-slate-900 border border-slate-800' : 'bg-white border border-slate-200'">
        <div class="flex items-center gap-2 mb-0.5">
          <div class="w-2.5 h-2.5 rounded-full bg-orange-500 flex-shrink-0"></div>
          <span class="text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Moderate</span>
        </div>
        <div class="text-xl font-bold" :class="isDark ? 'text-orange-400' : 'text-orange-600'">{{ counts.moderate }}</div>
        <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">caution pairs</div>
      </div>
      <div class="rounded-xl p-3.5 border-l-4 border-amber-400"
        :class="isDark ? 'bg-slate-900 border border-slate-800' : 'bg-white border border-slate-200'">
        <div class="flex items-center gap-2 mb-0.5">
          <div class="w-2.5 h-2.5 rounded-full bg-amber-400 flex-shrink-0"></div>
          <span class="text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Minor</span>
        </div>
        <div class="text-xl font-bold" :class="isDark ? 'text-amber-400' : 'text-amber-600'">{{ counts.minor }}</div>
        <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">watch pairs</div>
      </div>
      <div class="rounded-xl p-3.5 border-l-4 border-emerald-500"
        :class="isDark ? 'bg-slate-900 border border-slate-800' : 'bg-white border border-slate-200'">
        <div class="flex items-center gap-2 mb-0.5">
          <div class="w-2.5 h-2.5 rounded-full bg-emerald-500 flex-shrink-0"></div>
          <span class="text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Safe</span>
        </div>
        <div class="text-xl font-bold" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">{{ counts.safe }}</div>
        <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">no issues</div>
      </div>
    </div>

    <!-- ── Legend ── -->
    <div v-if="medications.length >= 2 && !loading"
      class="flex flex-wrap items-center gap-4 mb-5 p-3.5 rounded-xl border"
      :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-slate-50 border-slate-200'">
      <span class="text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Severity Legend:</span>
      <div class="flex flex-wrap gap-3">
        <div v-for="leg in legend" :key="leg.label" class="flex items-center gap-1.5">
          <div class="w-6 h-6 rounded flex items-center justify-center text-xs font-bold" :class="leg.cellClass">{{ leg.icon }}</div>
          <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ leg.label }}</span>
        </div>
      </div>
    </div>

    <!-- ── Add temporary med ── -->
    <div class="mb-6 flex flex-col sm:flex-row gap-3">
      <input v-model="tempMed" placeholder="Add a temporary medication to check interactions…"
        class="flex-1 px-4 py-2.5 rounded-xl border text-sm focus:outline-none focus:ring-2"
        :class="isDark
          ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-500 focus:ring-purple-500/20'
          : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400 focus:ring-purple-400/20'"
        @keyup.enter="addTempMed" />
      <button @click="addTempMed" :disabled="!tempMed"
        class="px-5 py-2.5 rounded-xl text-sm font-semibold transition-all disabled:opacity-50 border border-slate-300 bg-white text-slate-700 hover:bg-slate-50"
        :class="isDark ? 'border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700' : ''">
        Test Drug Addition
      </button>
    </div>

    <!-- ── Loading ── -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-3">
        <div class="w-10 h-10 rounded-full border-2 border-t-purple-500 animate-spin" :class="isDark ? 'border-slate-700' : 'border-slate-200'"></div>
        <span class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Analyzing interactions…</span>
      </div>
    </div>

    <!-- ── Empty state ── -->
    <div v-else-if="medications.length < 2" class="flex flex-col items-center text-center py-16">
      <div class="w-16 h-16 rounded-2xl flex items-center justify-center mb-5"
        :class="isDark ? 'bg-slate-800' : 'bg-amber-50'">
        <svg class="w-8 h-8" :class="isDark ? 'text-slate-600' : 'text-amber-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/>
        </svg>
      </div>
      <h3 class="text-lg font-bold mb-2 text-[var(--text-primary)]">{{ medications.length === 0 ? 'No Medications Added' : 'Not Enough Medications' }}</h3>
      <p class="text-sm mb-6 text-[var(--text-secondary)] max-w-sm">{{ medications.length === 0 ? 'Add your current medications to check for drug interactions.' : 'Add at least 2 medications to check for interactions.' }}</p>
      <router-link v-if="medications.length === 0" to="/profile"
        class="inline-block px-5 py-2.5 rounded-xl text-sm font-semibold bg-indigo-700 hover:bg-indigo-800 text-white transition-all">
        Add Medications in Profile
      </router-link>
    </div>

    <!-- ── Interaction Matrix ── -->
    <div v-else>
      <div class="overflow-x-auto rounded-2xl border"
        :class="isDark ? 'border-slate-800' : 'border-slate-200'">
        <table class="w-full text-sm">
          <thead>
            <tr>
              <!-- Corner cell -->
              <th class="p-3 text-left font-semibold sticky left-0 z-10 min-w-[120px]"
                :class="isDark ? 'bg-slate-900 text-slate-500 border-b border-slate-800' : 'bg-slate-50 text-slate-400 border-b border-slate-200'">
                <span class="text-xs">Drug &rarr;</span>
              </th>
              <th v-for="med in medications" :key="'h-' + med"
                class="p-3 text-center font-semibold whitespace-nowrap border-b"
                :class="isDark ? 'bg-slate-900 text-slate-300 border-slate-800' : 'bg-slate-50 text-slate-700 border-slate-200'">
                <div class="flex flex-col items-center gap-1">
                  <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold"
                    :class="isDark ? 'bg-purple-500/20 text-purple-400' : 'bg-purple-100 text-purple-700'">
                    {{ med[0]?.toUpperCase() }}
                  </div>
                  <span class="text-xs max-w-[80px] truncate">{{ med }}</span>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, ri) in medications" :key="'r-' + row" class="border-t"
              :class="isDark ? 'border-slate-800 hover:bg-slate-800/30' : 'border-slate-200 hover:bg-slate-50'">
              <!-- Row label -->
              <td class="p-3 font-semibold whitespace-nowrap sticky left-0 z-10"
                :class="isDark ? 'bg-slate-900 text-slate-300' : 'bg-slate-50 text-slate-700'">
                <div class="flex items-center gap-2">
                  <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0"
                    :class="isDark ? 'bg-purple-500/20 text-purple-400' : 'bg-purple-100 text-purple-700'">
                    {{ row[0]?.toUpperCase() }}
                  </div>
                  <span class="text-xs max-w-[80px] truncate">{{ row }}</span>
                </div>
              </td>
              <!-- Cells -->
              <td v-for="(col, ci) in medications" :key="'c-' + col" class="p-2 text-center">
                <!-- Same drug diagonal -->
                <div v-if="ri === ci" class="w-11 h-11 rounded-xl mx-auto flex items-center justify-center"
                  :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                  <svg class="w-4 h-4" :class="isDark ? 'text-slate-600' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4"/>
                  </svg>
                </div>
                <!-- Interaction cell -->
                <button v-else @click="showDetail(row, col)"
                  class="w-11 h-11 rounded-xl mx-auto flex items-center justify-center transition-all hover:scale-110 hover:shadow-lg cursor-pointer group"
                  :class="cellClass(ri, ci)"
                  :title="`${row} + ${col}: ${getInteraction(row, col).severity}`">
                  <!-- Severity icon -->
                  <svg v-if="getInteraction(medications[ri], medications[ci]).severity === 'Safe'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4.5 12.75l6 6 9-13.5"/>
                  </svg>
                  <svg v-else-if="getInteraction(medications[ri], medications[ci]).severity === 'Major'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/>
                  </svg>
                  <span v-else class="text-xs font-bold leading-none">{{ cellLabel(ri, ci) }}</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Matrix help text -->
      <p class="text-xs mt-3 text-center" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
        Click any cell to see detailed interaction information
      </p>
    </div>

    <!-- ── Detail slide-out ── -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="selectedPair" class="fixed inset-0 z-[100] flex justify-end">
          <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="selectedPair = null"></div>
          <div class="relative w-full max-w-md h-full overflow-y-auto border-l shadow-2xl"
            :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
            <!-- Panel header -->
            <div class="sticky top-0 z-10 p-5 border-b backdrop-blur-xl"
              :class="isDark ? 'bg-slate-900/95 border-slate-800' : 'bg-white/95 border-slate-200'">
              <button @click="selectedPair = null" class="absolute top-4 right-4 p-1.5 rounded-lg transition-colors"
                :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
              <div class="pr-10">
                <h3 class="text-base font-bold text-[var(--text-primary)]">{{ selectedPair.med1 }} + {{ selectedPair.med2 }}</h3>
                <div class="flex items-center gap-2 mt-2">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold" :class="severityBadge(selectedPair.severity)">
                    <span class="w-2 h-2 rounded-full" :class="severityDot(selectedPair.severity)"></span>
                    {{ selectedPair.severity }} Interaction
                  </span>
                </div>
              </div>
            </div>

            <!-- Panel content -->
            <div class="p-5 space-y-5">
              <div class="space-y-4">
                <div class="p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
                  <h4 class="text-xs font-bold uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Description</h4>
                  <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ selectedPair.description }}</p>
                </div>
                <div class="p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
                  <h4 class="text-xs font-bold uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Clinical Significance</h4>
                  <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ selectedPair.significance }}</p>
                </div>
                <div class="p-4 rounded-xl border-l-4"
                  :class="selectedPair.severity === 'Major'
                    ? (isDark ? 'bg-red-500/5 border-red-500' : 'bg-red-50 border-red-500')
                    : selectedPair.severity === 'Moderate'
                    ? (isDark ? 'bg-orange-500/5 border-orange-500' : 'bg-orange-50 border-orange-500')
                    : (isDark ? 'bg-slate-800/50 border-slate-600' : 'bg-slate-50 border-slate-400')">
                  <h4 class="text-xs font-bold uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Recommendation</h4>
                  <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ selectedPair.recommendation }}</p>
                </div>
              </div>

              <p class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
                Always consult your pharmacist or physician before changing your medications.
              </p>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getMedications, checkInteractions } from '@/services/medicationApi.js'
import { getProfileMedicationNames } from '@/services/profileMedications.js'

const { isDark } = useTheme()
const medications = ref([])
const interactions = ref({})
const loading = ref(true)
const tempMed = ref('')
const selectedPair = ref(null)

const legend = computed(() => [
  { label: 'Safe', icon: '✓', cellClass: isDark.value ? 'bg-emerald-500/20 text-emerald-400' : 'bg-emerald-100 text-emerald-700' },
  { label: 'Minor', icon: '!', cellClass: isDark.value ? 'bg-amber-400/20 text-amber-400' : 'bg-amber-100 text-amber-700' },
  { label: 'Moderate', icon: '!!', cellClass: isDark.value ? 'bg-orange-500/20 text-orange-400' : 'bg-orange-100 text-orange-700' },
  { label: 'Major', icon: '▲', cellClass: isDark.value ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-700' },
])

const demoInteractions = {
  'Lisinopril|Metformin': { severity: 'Minor', description: 'Lisinopril may slightly increase the blood sugar-lowering effect of Metformin.', significance: 'This interaction is generally not clinically significant. No dose adjustment is typically needed.', recommendation: 'Monitor blood sugar as usual. Report any unusual hypoglycemic episodes.' },
  'Lisinopril|Atorvastatin': { severity: 'Safe', description: 'No clinically significant interaction between Lisinopril and Atorvastatin.', significance: 'These medications are commonly prescribed together for cardiovascular risk reduction.', recommendation: 'No special precautions needed. Continue as prescribed.' },
  'Lisinopril|Albuterol': { severity: 'Safe', description: 'No significant interaction between these medications.', significance: 'These medications work on different systems and do not interfere with each other.', recommendation: 'No action needed.' },
  'Metformin|Atorvastatin': { severity: 'Moderate', description: 'Atorvastatin may slightly increase blood glucose levels, potentially reducing Metformin effectiveness.', significance: 'Monitor HbA1c and fasting glucose regularly. Statins can have a small effect on glucose metabolism.', recommendation: 'Continue both medications but monitor blood sugar more closely. Discuss with your doctor if glucose control worsens.' },
  'Metformin|Albuterol': { severity: 'Moderate', description: 'Albuterol can raise blood sugar levels, potentially counteracting Metformin.', significance: 'Beta-2 agonists can cause hyperglycemia through glycogenolysis stimulation.', recommendation: 'Monitor blood sugar after using Albuterol. Contact your doctor if significant blood sugar spikes occur.' },
  'Atorvastatin|Albuterol': { severity: 'Safe', description: 'No clinically significant interaction.', significance: 'These medications do not interact.', recommendation: 'No precautions needed.' },
}

function getKey(a, b) {
  return [a, b].sort().join('|')
}

function getInteraction(a, b) {
  const key = getKey(a, b)
  return interactions.value[key] || demoInteractions[key] || { severity: 'Unknown', description: 'No interaction data available.', significance: 'Consult your pharmacist or doctor.', recommendation: 'Discuss with your healthcare provider.' }
}

const counts = computed(() => {
  let major = 0, moderate = 0, minor = 0, safe = 0
  for (let i = 0; i < medications.value.length; i++) {
    for (let j = i + 1; j < medications.value.length; j++) {
      const inter = getInteraction(medications.value[i], medications.value[j])
      if (inter.severity === 'Major') major++
      else if (inter.severity === 'Moderate') moderate++
      else if (inter.severity === 'Minor') minor++
      else safe++
    }
  }
  return { major, moderate, minor, safe }
})

function cellClass(ri, ci) {
  const inter = getInteraction(medications.value[ri], medications.value[ci])
  switch (inter.severity) {
    case 'Major': return isDark.value ? 'bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30' : 'bg-red-100 text-red-700 border border-red-200 hover:bg-red-200'
    case 'Moderate': return isDark.value ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30 hover:bg-orange-500/30' : 'bg-orange-100 text-orange-700 border border-orange-200 hover:bg-orange-200'
    case 'Minor': return isDark.value ? 'bg-amber-400/20 text-amber-400 border border-amber-400/30 hover:bg-amber-400/30' : 'bg-amber-100 text-amber-700 border border-amber-200 hover:bg-amber-200'
    case 'Safe': return isDark.value ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/30' : 'bg-emerald-100 text-emerald-700 border border-emerald-200 hover:bg-emerald-200'
    default: return isDark.value ? 'bg-slate-800 text-slate-500 border border-slate-700' : 'bg-slate-100 text-slate-400 border border-slate-200'
  }
}

function cellLabel(ri, ci) {
  const inter = getInteraction(medications.value[ri], medications.value[ci])
  switch (inter.severity) {
    case 'Major': return '!!!'
    case 'Moderate': return '!!'
    case 'Minor': return '!'
    case 'Safe': return 'OK'
    default: return '?'
  }
}

function severityBadge(severity) {
  switch (severity) {
    case 'Major': return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
    case 'Moderate': return isDark.value ? 'bg-orange-500/15 text-orange-400' : 'bg-orange-100 text-orange-700'
    case 'Minor': return isDark.value ? 'bg-amber-400/15 text-amber-400' : 'bg-amber-100 text-amber-700'
    case 'Safe': return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
    default: return isDark.value ? 'bg-slate-700 text-slate-400' : 'bg-slate-200 text-slate-600'
  }
}

function severityDot(severity) {
  switch (severity) {
    case 'Major': return 'bg-red-500'
    case 'Moderate': return 'bg-orange-500'
    case 'Minor': return 'bg-amber-400'
    case 'Safe': return 'bg-emerald-500'
    default: return 'bg-slate-500'
  }
}

function showDetail(med1, med2) {
  const inter = getInteraction(med1, med2)
  selectedPair.value = { med1, med2, ...inter }
}

function addTempMed() {
  if (tempMed.value && !medications.value.includes(tempMed.value)) {
    medications.value.push(tempMed.value)
    tempMed.value = ''
    fetchInteractions()
  }
}

async function fetchInteractions() {
  if (medications.value.length < 2) return
  loading.value = true
  try {
    const data = await checkInteractions(medications.value)
    if (data && data.interactions) {
      for (const inter of data.interactions) {
        const key = getKey(inter.med1, inter.med2)
        interactions.value[key] = inter
      }
    }
  } catch { /* use demo data */ }
  loading.value = false
}

onMounted(async () => {
  try {
    const data = await getMedications()
    const meds = Array.isArray(data) ? data : data.medications || []
    medications.value = meds.map(m => m.name)
  } catch {
    // Fall back to user's profile medications
    medications.value = getProfileMedicationNames()
  }
  await fetchInteractions()
})
</script>
