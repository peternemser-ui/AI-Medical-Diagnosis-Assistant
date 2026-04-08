<template>
  <div>
    <!-- ── Header ── -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-[var(--text-primary)]">Food &amp; Lifestyle Interactions</h1>
      <p class="text-sm mt-1 text-[var(--text-secondary)]">Learn how food, alcohol, and lifestyle choices affect your medications</p>
    </div>

    <!-- ── Loading ── -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="rounded-2xl border p-5 animate-pulse"
        :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <div class="h-6 rounded w-1/3 mb-4" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-2/3 mb-2" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-1/2" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
      </div>
    </div>

    <!-- ── Empty state ── -->
    <div v-else-if="medications.length === 0" class="flex flex-col items-center text-center py-16">
      <div class="w-16 h-16 rounded-2xl flex items-center justify-center mb-5"
        :class="isDark ? 'bg-slate-800' : 'bg-purple-50'">
        <svg class="w-8 h-8" :class="isDark ? 'text-slate-600' : 'text-purple-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8.25v-1.5m0 1.5c-1.355 0-2.697.056-4.024.166C6.845 8.51 6 9.473 6 10.608v2.513m6-4.871c1.355 0 2.697.056 4.024.166C17.155 8.51 18 9.473 18 10.608v2.513M15 8.25v-1.5m-6 1.5v-1.5m12 9.75l-1.5.75a3.354 3.354 0 01-3 0 3.354 3.354 0 00-3 0 3.354 3.354 0 01-3 0 3.354 3.354 0 00-3 0 3.354 3.354 0 01-3 0L3 16.5m18-12.75v14.25"/>
        </svg>
      </div>
      <h3 class="text-lg font-bold mb-2 text-[var(--text-primary)]">No Medications Added</h3>
      <p class="text-sm mb-6 text-[var(--text-secondary)] max-w-sm">Add your current medications in your health profile to see food interactions, scheduling, side effects, and more.</p>
      <router-link to="/profile"
        class="inline-block px-5 py-2.5 rounded-xl text-sm font-semibold bg-indigo-700 hover:bg-indigo-800 text-white transition-all">
        Add Medications in Profile
      </router-link>
    </div>

    <!-- ── Medication cards ── -->
    <div v-else class="space-y-4">
      <div v-for="med in medications" :key="med.name"
        class="rounded-2xl border overflow-hidden transition-all"
        :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200'">
        <!-- Card header (clickable) -->
        <button @click="toggle(med.name)"
          class="w-full flex items-center justify-between p-5 text-left transition-colors"
          :class="isDark ? 'hover:bg-slate-800/40' : 'hover:bg-slate-50'">
          <div class="flex items-center gap-3">
            <!-- Drug initial avatar -->
            <div class="w-10 h-10 rounded-xl flex items-center justify-center text-sm font-bold flex-shrink-0"
              :class="isDark ? 'bg-purple-500/20 text-purple-400' : 'bg-purple-100 text-purple-700'">
              {{ med.name[0] }}
            </div>
            <div>
              <h3 class="font-bold text-[var(--text-primary)]">{{ med.name }}</h3>
              <span class="text-xs text-[var(--text-secondary)]">{{ med.dosage }}</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <span v-if="expanded[med.name]" class="text-xs font-medium" :class="isDark ? 'text-purple-400' : 'text-purple-600'">Hide details</span>
            <span v-else class="text-xs font-medium" :class="isDark ? 'text-slate-500' : 'text-slate-400'">View interactions</span>
            <svg class="w-4 h-4 transition-transform flex-shrink-0"
              :class="[expanded[med.name] ? 'rotate-180' : '', isDark ? 'text-slate-500' : 'text-slate-400']"
              fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
          </div>
        </button>

        <!-- Expanded content -->
        <Transition
          enter-active-class="transition-all duration-200 ease-out"
          enter-from-class="max-h-0 opacity-0"
          enter-to-class="max-h-[2000px] opacity-100"
          leave-active-class="transition-all duration-150 ease-in"
          leave-from-class="max-h-[2000px] opacity-100"
          leave-to-class="max-h-0 opacity-0">
          <div v-if="expanded[med.name]" class="overflow-hidden">
            <div class="border-t px-5 pt-4 pb-5" :class="isDark ? 'border-slate-800' : 'border-slate-100'">

              <!-- Quick severity overview row -->
              <div class="flex flex-wrap gap-2 mb-4">
                <div v-if="getInfo(med.name).avoid?.length" class="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600'">
                  <span class="w-2 h-2 rounded-full bg-red-500"></span>
                  {{ getInfo(med.name).avoid.length }} to avoid
                </div>
                <div v-if="getInfo(med.name).helpful?.length" class="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium"
                  :class="isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                  {{ getInfo(med.name).helpful.length }} beneficial
                </div>
              </div>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <!-- Foods to Avoid -->
                <div class="rounded-xl p-4 border-l-4 border-red-500"
                  :class="isDark ? 'bg-red-500/5 border border-red-500/20' : 'bg-red-50 border border-red-100'">
                  <h4 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2 mb-3"
                    :class="isDark ? 'text-red-400' : 'text-red-600'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"/>
                    </svg>
                    Foods to Avoid
                  </h4>
                  <ul class="space-y-1.5">
                    <li v-for="item in getInfo(med.name).avoid" :key="item"
                      class="flex items-start gap-2 text-xs"
                      :class="isDark ? 'text-red-300/80' : 'text-red-700'">
                      <span class="flex-shrink-0 mt-0.5 font-bold">&#10005;</span>
                      {{ item }}
                    </li>
                  </ul>
                </div>

                <!-- Foods that Help -->
                <div class="rounded-xl p-4 border-l-4 border-emerald-500"
                  :class="isDark ? 'bg-emerald-500/5 border border-emerald-500/20' : 'bg-emerald-50 border border-emerald-100'">
                  <h4 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2 mb-3"
                    :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Foods that Help
                  </h4>
                  <ul class="space-y-1.5">
                    <li v-for="item in getInfo(med.name).helpful" :key="item"
                      class="flex items-start gap-2 text-xs"
                      :class="isDark ? 'text-emerald-300/80' : 'text-emerald-700'">
                      <span class="flex-shrink-0 mt-0.5 font-bold">&#10003;</span>
                      {{ item }}
                    </li>
                  </ul>
                </div>

                <!-- Meal Timing -->
                <div class="rounded-xl p-4 border-l-4 border-sky-500"
                  :class="isDark ? 'bg-sky-500/5 border border-sky-500/20' : 'bg-sky-50 border border-sky-100'">
                  <h4 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2 mb-2"
                    :class="isDark ? 'text-sky-400' : 'text-sky-600'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Meal Timing
                  </h4>
                  <p class="text-xs leading-relaxed" :class="isDark ? 'text-sky-300/80' : 'text-sky-700'">{{ getInfo(med.name).timing }}</p>
                </div>

                <!-- Alcohol -->
                <div class="rounded-xl p-4 border-l-4 border-amber-500"
                  :class="isDark ? 'bg-amber-500/5 border border-amber-500/20' : 'bg-amber-50 border border-amber-100'">
                  <h4 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2 mb-2"
                    :class="isDark ? 'text-amber-400' : 'text-amber-600'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"/>
                    </svg>
                    Alcohol
                  </h4>
                  <p class="text-xs leading-relaxed" :class="isDark ? 'text-amber-300/80' : 'text-amber-700'">{{ getInfo(med.name).alcohol }}</p>
                </div>

                <!-- Supplements to Avoid -->
                <div class="rounded-xl p-4 border-l-4 border-orange-500"
                  :class="isDark ? 'bg-orange-500/5 border border-orange-500/20' : 'bg-orange-50 border border-orange-100'">
                  <h4 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2 mb-3"
                    :class="isDark ? 'text-orange-400' : 'text-orange-600'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.618 5.984A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                    </svg>
                    Supplements to Avoid
                  </h4>
                  <ul class="space-y-1.5">
                    <li v-for="item in getInfo(med.name).supplements" :key="item"
                      class="flex items-start gap-2 text-xs"
                      :class="isDark ? 'text-orange-300/80' : 'text-orange-700'">
                      <span class="flex-shrink-0 mt-0.5 font-bold">&#10005;</span>
                      {{ item }}
                    </li>
                  </ul>
                </div>

                <!-- Lifestyle Warnings -->
                <div class="rounded-xl p-4 border-l-4 border-purple-500"
                  :class="isDark ? 'bg-purple-500/5 border border-purple-500/20' : 'bg-purple-50 border border-purple-100'">
                  <h4 class="text-xs font-bold uppercase tracking-wide flex items-center gap-2 mb-3"
                    :class="isDark ? 'text-purple-400' : 'text-purple-600'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    Lifestyle Warnings
                  </h4>
                  <ul class="space-y-1.5">
                    <li v-for="item in getInfo(med.name).lifestyle" :key="item"
                      class="flex items-start gap-2 text-xs"
                      :class="isDark ? 'text-purple-300/80' : 'text-purple-700'">
                      <span class="flex-shrink-0 mt-0.5">&#9888;</span>
                      {{ item }}
                    </li>
                  </ul>
                </div>
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
import { getProfileMedications } from '@/services/profileMedications.js'

const { isDark } = useTheme()
const medications = ref([])
const loading = ref(true)
const expanded = reactive({})
const foodCache = reactive({})

const noProfileMeds = ref(false)

function buildFoodDataFromEnriched(enrichedMed) {
  if (!enrichedMed.foodInteractions) return null
  const fi = enrichedMed.foodInteractions
  return {
    avoid: fi.avoid || [],
    helpful: fi.helpful || [],
    timing: fi.mealTiming || 'No specific information available.',
    alcohol: fi.alcohol || 'Consult your doctor about alcohol use.',
    supplements: fi.supplements || [],
    lifestyle: fi.lifestyle || []
  }
}

function getInfo(name) {
  if (foodCache[name]) return foodCache[name]
  const fallback = { avoid: ['No data available'], helpful: ['Consult your pharmacist'], timing: 'No specific information available.', alcohol: 'Consult your doctor about alcohol use.', supplements: ['Consult your pharmacist'], lifestyle: ['Follow your doctor\'s instructions'] }
  return fallback
}

function toggle(name) {
  expanded[name] = !expanded[name]
}

onMounted(async () => {
  try {
    const data = await getMedications()
    medications.value = Array.isArray(data) ? data : data.medications || []
  } catch {
    // Fall back to user's profile medications
    const { medications: profileMeds, hasProfile } = getProfileMedications()
    if (hasProfile) {
      medications.value = profileMeds.map(m => ({ name: m.name, dosage: m.dosage }))
      // Populate food cache from the medication database
      for (const m of profileMeds) {
        const foodData = buildFoodDataFromEnriched(m)
        if (foodData) foodCache[m.name] = foodData
      }
    } else {
      medications.value = []
      noProfileMeds.value = true
    }
  }

  if (medications.value.length > 0) {
    try {
      const names = medications.value.map(m => m.name)
      const data = await getFoodInteractions(names)
      if (data && data.interactions) {
        for (const [name, info] of Object.entries(data.interactions)) {
          foodCache[name] = info
        }
      }
    } catch { /* use database data already in cache */ }
  }

  loading.value = false
})
</script>
