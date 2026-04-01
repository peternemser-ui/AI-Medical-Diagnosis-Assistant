<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Food & Lifestyle Interactions</h1>
      <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Learn how food, alcohol, and lifestyle affect your medications</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="rounded-2xl border p-5 animate-pulse" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <div class="h-6 rounded w-1/3 mb-4" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-2/3 mb-2" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-1/2" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="medications.length === 0" class="text-center py-20">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
        <svg class="w-10 h-10" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8.25v-1.5m0 1.5c-1.355 0-2.697.056-4.024.166C6.845 8.51 6 9.473 6 10.608v2.513m6-4.871c1.355 0 2.697.056 4.024.166C17.155 8.51 18 9.473 18 10.608v2.513"/></svg>
      </div>
      <h3 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">No medications found</h3>
      <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Add medications first to see food and lifestyle interactions.</p>
    </div>

    <!-- Medication cards -->
    <div v-else class="space-y-4">
      <div v-for="med in medications" :key="med.name" class="rounded-2xl border overflow-hidden" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <!-- Header (clickable) -->
        <button @click="toggle(med.name)" class="w-full flex items-center justify-between p-5 text-left transition-colors" :class="isDark ? 'hover:bg-slate-800/50' : 'hover:bg-slate-50'">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-br from-emerald-500 to-teal-600 text-white text-sm font-bold">{{ med.name[0] }}</div>
            <div>
              <h3 class="font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ med.name }}</h3>
              <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ med.dosage }}</span>
            </div>
          </div>
          <svg class="w-5 h-5 transition-transform" :class="[expanded[med.name] ? 'rotate-180' : '', isDark ? 'text-slate-500' : 'text-slate-400']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </button>

        <!-- Expanded content -->
        <Transition enter-active-class="transition-all duration-200 ease-out" enter-from-class="max-h-0 opacity-0" enter-to-class="max-h-[2000px] opacity-100" leave-active-class="transition-all duration-150 ease-in" leave-from-class="max-h-[2000px] opacity-100" leave-to-class="max-h-0 opacity-0">
          <div v-if="expanded[med.name]" class="overflow-hidden">
            <div class="px-5 pb-5 grid grid-cols-1 sm:grid-cols-2 gap-3">
              <!-- Foods to Avoid -->
              <div class="rounded-xl p-4 border" :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-100'">
                <h4 class="text-sm font-semibold flex items-center gap-2 mb-2" :class="isDark ? 'text-red-400' : 'text-red-600'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/></svg>
                  Foods to Avoid
                </h4>
                <ul class="space-y-1">
                  <li v-for="item in getInfo(med.name).avoid" :key="item" class="text-xs" :class="isDark ? 'text-red-300/80' : 'text-red-700'">{{ item }}</li>
                </ul>
              </div>

              <!-- Foods that Help -->
              <div class="rounded-xl p-4 border" :class="isDark ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-emerald-50 border-emerald-100'">
                <h4 class="text-sm font-semibold flex items-center gap-2 mb-2" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  Foods that Help
                </h4>
                <ul class="space-y-1">
                  <li v-for="item in getInfo(med.name).helpful" :key="item" class="text-xs" :class="isDark ? 'text-emerald-300/80' : 'text-emerald-700'">{{ item }}</li>
                </ul>
              </div>

              <!-- Meal Timing -->
              <div class="rounded-xl p-4 border" :class="isDark ? 'bg-blue-500/5 border-blue-500/20' : 'bg-blue-50 border-blue-100'">
                <h4 class="text-sm font-semibold flex items-center gap-2 mb-2" :class="isDark ? 'text-blue-400' : 'text-blue-600'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  Meal Timing
                </h4>
                <p class="text-xs" :class="isDark ? 'text-blue-300/80' : 'text-blue-700'">{{ getInfo(med.name).timing }}</p>
              </div>

              <!-- Alcohol -->
              <div class="rounded-xl p-4 border" :class="isDark ? 'bg-amber-500/5 border-amber-500/20' : 'bg-amber-50 border-amber-100'">
                <h4 class="text-sm font-semibold flex items-center gap-2 mb-2" :class="isDark ? 'text-amber-400' : 'text-amber-600'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"/></svg>
                  Alcohol
                </h4>
                <p class="text-xs" :class="isDark ? 'text-amber-300/80' : 'text-amber-700'">{{ getInfo(med.name).alcohol }}</p>
              </div>

              <!-- Supplements to Avoid -->
              <div class="rounded-xl p-4 border" :class="isDark ? 'bg-orange-500/5 border-orange-500/20' : 'bg-orange-50 border-orange-100'">
                <h4 class="text-sm font-semibold flex items-center gap-2 mb-2" :class="isDark ? 'text-orange-400' : 'text-orange-600'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                  Supplements to Avoid
                </h4>
                <ul class="space-y-1">
                  <li v-for="item in getInfo(med.name).supplements" :key="item" class="text-xs" :class="isDark ? 'text-orange-300/80' : 'text-orange-700'">{{ item }}</li>
                </ul>
              </div>

              <!-- Lifestyle Warnings -->
              <div class="rounded-xl p-4 border" :class="isDark ? 'bg-purple-500/5 border-purple-500/20' : 'bg-purple-50 border-purple-100'">
                <h4 class="text-sm font-semibold flex items-center gap-2 mb-2" :class="isDark ? 'text-purple-400' : 'text-purple-600'">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  Lifestyle Warnings
                </h4>
                <ul class="space-y-1">
                  <li v-for="item in getInfo(med.name).lifestyle" :key="item" class="text-xs" :class="isDark ? 'text-purple-300/80' : 'text-purple-700'">{{ item }}</li>
                </ul>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getMedications, getFoodInteractions } from '@/services/medicationApi.js'

const { isDark } = useTheme()
const medications = ref([])
const loading = ref(true)
const expanded = reactive({})
const foodCache = reactive({})

const demoFoodData = {
  'Lisinopril': { avoid: ['High-potassium foods (bananas, oranges, potatoes) in excess', 'Salt substitutes containing potassium'], helpful: ['Low-sodium diet improves effectiveness', 'Balanced potassium from varied sources'], timing: 'Can be taken with or without food. Take at the same time each day.', alcohol: 'Limit alcohol. It can lower blood pressure further, causing dizziness.', supplements: ['Potassium supplements (risk of hyperkalemia)', 'NSAIDs like ibuprofen (reduce effectiveness)'], lifestyle: ['Rise slowly from sitting to avoid dizziness', 'Stay hydrated, especially in hot weather', 'Avoid heavy exercise until you know how it affects you'] },
  'Metformin': { avoid: ['Excessive sugar and refined carbohydrates', 'Heavy meals high in fat (slows absorption)'], helpful: ['High-fiber foods help blood sugar control', 'Balanced meals with protein and complex carbs'], timing: 'Take with meals to reduce stomach upset. Best taken with the largest meals.', alcohol: 'Avoid or strictly limit alcohol. Increases risk of lactic acidosis.', supplements: ['Vitamin B12 absorption may be reduced (monitor levels)', 'Chromium supplements (unpredictable glucose effects)'], lifestyle: ['Maintain regular exercise routine', 'Monitor blood sugar regularly', 'Stay well hydrated'] },
  'Atorvastatin': { avoid: ['Grapefruit and grapefruit juice (increases drug levels)', 'Excessive alcohol (liver strain)'], helpful: ['Oat bran and soluble fiber (complement cholesterol reduction)', 'Fish rich in omega-3 fatty acids'], timing: 'Take at bedtime for best effectiveness. Can be taken with or without food.', alcohol: 'Limit to moderate amounts. Heavy drinking increases liver damage risk.', supplements: ['St. John\'s Wort (reduces effectiveness)', 'Red yeast rice (contains natural statins, additive risk)'], lifestyle: ['Report any unexplained muscle pain or weakness immediately', 'Regular liver function tests recommended', 'Maintain heart-healthy diet and exercise'] },
  'Albuterol': { avoid: ['Caffeine in excess (may increase heart rate)', 'Foods that trigger your asthma/allergies'], helpful: ['Anti-inflammatory foods (berries, leafy greens, fatty fish)', 'Adequate hydration thins mucus'], timing: 'Use as needed. No specific meal timing requirements.', alcohol: 'Moderate alcohol is usually fine. Avoid if it triggers breathing issues.', supplements: ['Ephedra / ma huang (additive stimulant effects)', 'High-dose caffeine supplements'], lifestyle: ['Rinse mouth after use to prevent irritation', 'Track triggers and avoid them', 'Keep rescue inhaler accessible at all times'] },
}

function getInfo(name) {
  return foodCache[name] || demoFoodData[name] || { avoid: ['No data available'], helpful: ['Consult your pharmacist'], timing: 'No specific information available.', alcohol: 'Consult your doctor about alcohol use.', supplements: ['Consult your pharmacist'], lifestyle: ['Follow your doctor\'s instructions'] }
}

function toggle(name) {
  expanded[name] = !expanded[name]
}

onMounted(async () => {
  try {
    const data = await getMedications()
    medications.value = Array.isArray(data) ? data : data.medications || []
  } catch {
    medications.value = [
      { name: 'Lisinopril', dosage: '10mg' },
      { name: 'Metformin', dosage: '500mg' },
      { name: 'Atorvastatin', dosage: '20mg' },
      { name: 'Albuterol', dosage: '90mcg' },
    ]
  }

  try {
    const names = medications.value.map(m => m.name)
    const data = await getFoodInteractions(names)
    if (data && data.interactions) {
      for (const [name, info] of Object.entries(data.interactions)) {
        foodCache[name] = info
      }
    }
  } catch { /* use demo data */ }

  loading.value = false
})
</script>
