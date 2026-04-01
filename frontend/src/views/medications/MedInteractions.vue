<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Drug Interactions</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Check how your medications interact with each other</p>
      </div>
    </div>

    <!-- Summary bar -->
    <div v-if="medications.length >= 2 && !loading" class="flex flex-wrap gap-3 mb-6">
      <div class="px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2" :class="isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600'">
        <div class="w-2.5 h-2.5 rounded-full bg-red-500"></div>
        {{ counts.major }} Major
      </div>
      <div class="px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2" :class="isDark ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-50 text-amber-600'">
        <div class="w-2.5 h-2.5 rounded-full bg-amber-500"></div>
        {{ counts.moderate }} Moderate
      </div>
      <div class="px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2" :class="isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'">
        <div class="w-2.5 h-2.5 rounded-full bg-emerald-500"></div>
        {{ counts.minor }} Minor / Safe
      </div>
    </div>

    <!-- Add temporary med -->
    <div class="mb-6 flex flex-col sm:flex-row gap-3">
      <input v-model="tempMed" placeholder="Add a temporary medication to check..." class="flex-1 px-4 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-500' : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400'" @keyup.enter="addTempMed" />
      <button @click="addTempMed" :disabled="!tempMed" class="px-5 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-amber-500 to-orange-500 text-white hover:from-amber-400 hover:to-orange-400 transition-all disabled:opacity-50">
        Test Addition
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="flex flex-col items-center gap-3">
        <div class="w-10 h-10 rounded-full border-2 border-t-violet-500 animate-spin" :class="isDark ? 'border-slate-700' : 'border-slate-200'"></div>
        <span class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Analyzing interactions...</span>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="medications.length < 2" class="text-center py-20">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
        <svg class="w-10 h-10" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126z"/></svg>
      </div>
      <h3 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Not enough medications</h3>
      <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Add at least 2 medications to check for interactions.</p>
    </div>

    <!-- Interaction Matrix -->
    <div v-else class="overflow-x-auto rounded-2xl border" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
      <table class="w-full text-sm">
        <thead>
          <tr>
            <th class="p-3 text-left font-semibold sticky left-0 z-10" :class="isDark ? 'bg-slate-900 text-slate-400' : 'bg-slate-50 text-slate-600'"></th>
            <th v-for="med in medications" :key="'h-' + med" class="p-3 text-center font-semibold whitespace-nowrap" :class="isDark ? 'bg-slate-900 text-slate-300' : 'bg-slate-50 text-slate-700'">
              {{ med }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, ri) in medications" :key="'r-' + row" class="border-t" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <td class="p-3 font-semibold whitespace-nowrap sticky left-0 z-10" :class="isDark ? 'bg-slate-900 text-slate-300' : 'bg-slate-50 text-slate-700'">{{ row }}</td>
            <td v-for="(col, ci) in medications" :key="'c-' + col" class="p-2 text-center">
              <button v-if="ri !== ci" @click="showDetail(row, col)" class="w-10 h-10 rounded-lg mx-auto flex items-center justify-center transition-transform hover:scale-110 cursor-pointer" :class="cellClass(ri, ci)">
                <span class="text-xs font-bold">{{ cellLabel(ri, ci) }}</span>
              </button>
              <div v-else class="w-10 h-10 rounded-lg mx-auto flex items-center justify-center" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <span class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">--</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail slide-out -->
    <Teleport to="body">
      <Transition enter-active-class="transition duration-200 ease-out" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition duration-150 ease-in" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="selectedPair" class="fixed inset-0 z-[100] flex justify-end">
          <div class="absolute inset-0 bg-black/50" @click="selectedPair = null"></div>
          <div class="relative w-full max-w-md h-full overflow-y-auto border-l shadow-2xl p-6" :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
            <button @click="selectedPair = null" class="absolute top-4 right-4 p-1 rounded-lg" :class="isDark ? 'text-slate-400 hover:text-white' : 'text-slate-500 hover:text-slate-900'">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
            <h3 class="text-lg font-bold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">{{ selectedPair.med1 }} + {{ selectedPair.med2 }}</h3>
            <div class="inline-block px-2.5 py-1 rounded-full text-xs font-semibold mb-4" :class="severityBadge(selectedPair.severity)">{{ selectedPair.severity }} interaction</div>
            <div class="space-y-4">
              <div>
                <h4 class="text-sm font-semibold mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Description</h4>
                <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ selectedPair.description }}</p>
              </div>
              <div>
                <h4 class="text-sm font-semibold mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Clinical Significance</h4>
                <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ selectedPair.significance }}</p>
              </div>
              <div>
                <h4 class="text-sm font-semibold mb-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Recommendation</h4>
                <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ selectedPair.recommendation }}</p>
              </div>
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

const { isDark } = useTheme()
const medications = ref([])
const interactions = ref({})
const loading = ref(true)
const tempMed = ref('')
const selectedPair = ref(null)

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
  let major = 0, moderate = 0, minor = 0
  for (let i = 0; i < medications.value.length; i++) {
    for (let j = i + 1; j < medications.value.length; j++) {
      const inter = getInteraction(medications.value[i], medications.value[j])
      if (inter.severity === 'Major') major++
      else if (inter.severity === 'Moderate') moderate++
      else minor++
    }
  }
  return { major, moderate, minor }
})

function cellClass(ri, ci) {
  const inter = getInteraction(medications.value[ri], medications.value[ci])
  switch (inter.severity) {
    case 'Major': return isDark.value ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-700'
    case 'Moderate': return isDark.value ? 'bg-amber-500/20 text-amber-400' : 'bg-amber-100 text-amber-700'
    case 'Minor': return isDark.value ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-100 text-blue-700'
    case 'Safe': return isDark.value ? 'bg-emerald-500/20 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
    default: return isDark.value ? 'bg-slate-800 text-slate-500' : 'bg-slate-100 text-slate-400'
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
    case 'Moderate': return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-700'
    case 'Minor': return isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-100 text-blue-700'
    case 'Safe': return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
    default: return isDark.value ? 'bg-slate-700 text-slate-400' : 'bg-slate-200 text-slate-600'
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
    medications.value = ['Lisinopril', 'Metformin', 'Atorvastatin', 'Albuterol']
  }
  await fetchInteractions()
})
</script>
