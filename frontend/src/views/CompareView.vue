<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-blue-600/5' : 'bg-blue-400/10'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-purple-600/5' : 'bg-purple-400/10'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="relative z-20 flex items-center justify-between px-6 py-3 border-b"
      :class="isDark ? 'border-slate-800 bg-slate-950/80 backdrop-blur-xl' : 'border-slate-200 bg-white/80 backdrop-blur-xl'">
      <div class="flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <span class="text-sm font-semibold hidden sm:inline" :class="isDark ? 'text-white' : 'text-slate-900'">Medical AI</span>
        </router-link>
        <div class="w-px h-5 hidden sm:block" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <span class="text-sm font-medium hidden sm:inline" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Compare Sessions</span>
      </div>
      <div class="flex items-center gap-2">
        <ThemeLangControls />
        <router-link to="/reports" class="p-1.5 rounded-lg transition-colors flex items-center gap-1.5 text-xs font-medium"
          :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
          <span class="hidden sm:inline">Back to Reports</span>
        </router-link>
      </div>
    </nav>

    <!-- Main content -->
    <div class="relative z-10 max-w-6xl mx-auto px-4 py-6">
      <h1 class="text-2xl font-bold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">Compare Diagnoses</h1>
      <p class="text-xs mb-6" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
        Select two past sessions to compare side by side.
      </p>

      <!-- Session selectors -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div v-for="(side, idx) in ['A', 'B']" :key="side">
          <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            Session {{ side }}
          </label>
          <select
            :value="idx === 0 ? selectedA : selectedB"
            @change="idx === 0 ? (selectedA = $event.target.value) : (selectedB = $event.target.value)"
            class="w-full rounded-xl px-4 py-3 text-sm border focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all appearance-none cursor-pointer"
            :class="isDark
              ? 'bg-slate-900/80 border-slate-800 text-white'
              : 'bg-white border-slate-200 text-slate-900'"
          >
            <option value="">-- Select a session --</option>
            <option
              v-for="s in sessions"
              :key="s.id"
              :value="s.id"
              :disabled="(idx === 0 ? selectedB : selectedA) === s.id"
            >
              {{ formatDate(s.timestamp) }} — {{ s.topDiagnosis }} ({{ s.confidence }}%)
            </option>
          </select>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="sessions.length < 2" class="flex flex-col items-center justify-center py-20 text-center">
        <svg class="w-16 h-16 mb-4" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <h2 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">
          Need at least 2 sessions
        </h2>
        <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Complete more consultations to compare diagnoses.
        </p>
      </div>

      <!-- Comparison content -->
      <div v-else-if="sessionA && sessionB">
        <!-- Side by side: Date & Chief Complaint -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div v-for="(session, idx) in [sessionA, sessionB]" :key="idx"
            class="rounded-2xl border p-4"
            :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white/80 border-slate-200 shadow-sm'">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-detail font-bold uppercase tracking-wider px-2 py-0.5 rounded-full"
                :class="idx === 0
                  ? (isDark ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-100 text-blue-600')
                  : (isDark ? 'bg-purple-500/20 text-purple-400' : 'bg-purple-100 text-purple-600')">
                Session {{ idx === 0 ? 'A' : 'B' }}
              </span>
              <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                {{ formatDate(session.timestamp) }}
              </span>
            </div>
            <p class="text-sm font-medium leading-snug" :class="isDark ? 'text-white' : 'text-slate-900'">
              {{ session.symptoms || 'No symptoms recorded' }}
            </p>
            <div class="flex items-center gap-3 mt-2 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              <span v-if="session.age">Age: {{ session.age }}</span>
              <span v-if="session.gender">{{ session.gender }}</span>
            </div>
          </div>
        </div>

        <!-- Severity Comparison -->
        <div class="rounded-2xl border p-4 mb-6"
          :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white/80 border-slate-200 shadow-sm'">
          <h3 class="text-sm font-bold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Severity Comparison</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="(data, idx) in [causesA, causesB]" :key="idx">
              <div class="text-detail font-bold uppercase tracking-wider mb-2"
                :class="idx === 0
                  ? (isDark ? 'text-blue-400' : 'text-blue-600')
                  : (isDark ? 'text-purple-400' : 'text-purple-600')">
                Session {{ idx === 0 ? 'A' : 'B' }}
              </div>
              <div class="flex items-center gap-2">
                <span class="px-2 py-0.5 rounded-full text-detail font-bold uppercase tracking-wide"
                  :class="urgencyClass(getTopUrgency(data))">
                  {{ getTopUrgency(data) }}
                </span>
                <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                  Top confidence: {{ data.length > 0 ? (data[0].value || data[0].confidence || 0) : 0 }}%
                </span>
              </div>
            </div>
          </div>
          <!-- Severity arrow -->
          <div class="mt-3 pt-3 border-t" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <div class="flex items-center gap-2 text-xs font-medium"
              :class="severityDelta > 0
                ? (isDark ? 'text-red-400' : 'text-red-500')
                : severityDelta < 0
                  ? (isDark ? 'text-emerald-400' : 'text-emerald-500')
                  : (isDark ? 'text-slate-400' : 'text-slate-500')">
              <svg v-if="severityDelta > 0" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"/>
              </svg>
              <svg v-else-if="severityDelta < 0" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14"/>
              </svg>
              <span>
                {{ severityDelta > 0 ? 'Session B is more severe' : severityDelta < 0 ? 'Session B is less severe' : 'Similar severity' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Confidence Bars Side by Side -->
        <div class="rounded-2xl border p-4 mb-6"
          :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white/80 border-slate-200 shadow-sm'">
          <h3 class="text-sm font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Diagnosis Confidence</h3>
          <div class="space-y-3">
            <div v-for="condition in allConditions" :key="condition" class="space-y-1">
              <div class="text-xs font-medium flex items-center gap-2"
                :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                <span>{{ condition }}</span>
                <span v-if="isSharedCondition(condition)" class="text-tiny px-1.5 py-0.5 rounded-full"
                  :class="isDark ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-600'">
                  both
                </span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                <!-- Session A bar -->
                <div class="flex items-center gap-2">
                  <span class="text-detail w-5 font-bold" :class="isDark ? 'text-blue-400' : 'text-blue-600'">A</span>
                  <div class="flex-1 h-3 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'">
                    <div class="h-full rounded-full transition-all duration-700"
                      :class="isDark ? 'bg-blue-500' : 'bg-blue-500'"
                      :style="{ width: getConditionConfidence(causesA, condition) + '%' }"></div>
                  </div>
                  <span class="text-detail w-8 text-right font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    {{ getConditionConfidence(causesA, condition) }}%
                  </span>
                </div>
                <!-- Session B bar -->
                <div class="flex items-center gap-2">
                  <span class="text-detail w-5 font-bold" :class="isDark ? 'text-purple-400' : 'text-purple-600'">B</span>
                  <div class="flex-1 h-3 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'">
                    <div class="h-full rounded-full transition-all duration-700"
                      :class="isDark ? 'bg-purple-500' : 'bg-purple-500'"
                      :style="{ width: getConditionConfidence(causesB, condition) + '%' }"></div>
                  </div>
                  <span class="text-detail w-8 text-right font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    {{ getConditionConfidence(causesB, condition) }}%
                  </span>
                </div>
              </div>
            </div>
            <div v-if="allConditions.length === 0" class="text-xs text-center py-4"
              :class="isDark ? 'text-slate-600' : 'text-slate-400'">
              No diagnosis conditions found in selected sessions.
            </div>
          </div>
        </div>

        <!-- Recommended Tests Comparison -->
        <div class="rounded-2xl border p-4 mb-6"
          :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white/80 border-slate-200 shadow-sm'">
          <h3 class="text-sm font-bold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Recommended Tests</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="(tests, idx) in [testsA, testsB]" :key="idx">
              <div class="text-detail font-bold uppercase tracking-wider mb-2"
                :class="idx === 0
                  ? (isDark ? 'text-blue-400' : 'text-blue-600')
                  : (isDark ? 'text-purple-400' : 'text-purple-600')">
                Session {{ idx === 0 ? 'A' : 'B' }}
              </div>
              <div v-if="tests.length > 0" class="space-y-1">
                <div v-for="test in tests" :key="test"
                  class="flex items-center gap-2 text-xs px-2.5 py-1.5 rounded-lg"
                  :class="[
                    isDark ? 'bg-slate-800/50 text-slate-300' : 'bg-slate-50 text-slate-600',
                    isSharedTest(test) ? (isDark ? 'ring-1 ring-amber-500/30' : 'ring-1 ring-amber-300') : ''
                  ]">
                  <svg class="w-3 h-3 flex-shrink-0" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  <span>{{ test }}</span>
                </div>
              </div>
              <p v-else class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">No tests recommended.</p>
            </div>
          </div>
        </div>

        <!-- Changes Summary -->
        <div class="rounded-2xl border p-4"
          :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white/80 border-slate-200 shadow-sm'">
          <h3 class="text-sm font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Changes Summary</h3>

          <!-- New Conditions (in B but not A) -->
          <div class="mb-4" v-if="newConditions.length > 0">
            <h4 class="text-detail font-bold uppercase tracking-wider mb-2"
              :class="isDark ? 'text-red-400' : 'text-red-500'">
              New Conditions (in B, not in A)
            </h4>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="c in newConditions" :key="c"
                class="text-xs px-2.5 py-1 rounded-lg"
                :class="isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600'">
                {{ c }}
              </span>
            </div>
          </div>

          <!-- Resolved Conditions (in A but not B) -->
          <div class="mb-4" v-if="resolvedConditions.length > 0">
            <h4 class="text-detail font-bold uppercase tracking-wider mb-2"
              :class="isDark ? 'text-emerald-400' : 'text-emerald-500'">
              Resolved Conditions (in A, not in B)
            </h4>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="c in resolvedConditions" :key="c"
                class="text-xs px-2.5 py-1 rounded-lg"
                :class="isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'">
                {{ c }}
              </span>
            </div>
          </div>

          <!-- Changed Confidence -->
          <div class="mb-2" v-if="changedConfidence.length > 0">
            <h4 class="text-detail font-bold uppercase tracking-wider mb-2"
              :class="isDark ? 'text-amber-400' : 'text-amber-500'">
              Changed Confidence
            </h4>
            <div class="space-y-1.5">
              <div v-for="c in changedConfidence" :key="c.condition"
                class="flex items-center gap-2 text-xs"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                <span class="font-medium">{{ c.condition }}</span>
                <span :class="isDark ? 'text-slate-600' : 'text-slate-400'">{{ c.confA }}%</span>
                <svg class="w-3 h-3" :class="c.delta > 0 ? (isDark ? 'text-red-400' : 'text-red-500') : (isDark ? 'text-emerald-400' : 'text-emerald-500')" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                </svg>
                <span :class="c.delta > 0 ? (isDark ? 'text-red-400' : 'text-red-500') : (isDark ? 'text-emerald-400' : 'text-emerald-500')" class="font-medium">
                  {{ c.confB }}% ({{ c.delta > 0 ? '+' : '' }}{{ c.delta }}%)
                </span>
              </div>
            </div>
          </div>

          <!-- No changes -->
          <div v-if="newConditions.length === 0 && resolvedConditions.length === 0 && changedConfidence.length === 0"
            class="text-xs text-center py-4"
            :class="isDark ? 'text-slate-600' : 'text-slate-400'">
            No significant changes detected between these sessions.
          </div>
        </div>
      </div>

      <!-- Prompt to select -->
      <div v-else-if="sessions.length >= 2 && (!selectedA || !selectedB)"
        class="flex flex-col items-center justify-center py-20 text-center">
        <svg class="w-16 h-16 mb-4" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>
        </svg>
        <h2 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">
          Select Two Sessions
        </h2>
        <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Pick a session from each dropdown above to compare.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'
import { getSessions, getSession } from '@/services/historyService.js'

const { isDark } = useTheme()

const sessions = ref(getSessions())
const selectedA = ref('')
const selectedB = ref('')

const sessionA = computed(() => selectedA.value ? getSession(selectedA.value) : null)
const sessionB = computed(() => selectedB.value ? getSession(selectedB.value) : null)

function extractCauses(session) {
  if (!session?.diagnosisResult?.causes) return []
  return session.diagnosisResult.causes
}

function extractTests(session) {
  if (!session?.diagnosisResult?.recommended_tests) return []
  const tests = session.diagnosisResult.recommended_tests
  if (Array.isArray(tests)) return tests.map(t => typeof t === 'string' ? t : t.test || t.name || String(t))
  return []
}

const causesA = computed(() => extractCauses(sessionA.value))
const causesB = computed(() => extractCauses(sessionB.value))
const testsA = computed(() => extractTests(sessionA.value))
const testsB = computed(() => extractTests(sessionB.value))

function getConditionName(cause) {
  return (cause.cause || cause.condition || '').toLowerCase().trim()
}

function getConditionDisplay(cause) {
  return cause.cause || cause.condition || 'Unknown'
}

function getConfidence(cause) {
  return cause.value || cause.confidence || 0
}

const conditionNamesA = computed(() => new Set(causesA.value.map(getConditionName)))
const conditionNamesB = computed(() => new Set(causesB.value.map(getConditionName)))

const allConditions = computed(() => {
  const seen = new Set()
  const result = []
  for (const c of [...causesA.value, ...causesB.value]) {
    const name = getConditionDisplay(c)
    const key = getConditionName(c)
    if (!seen.has(key) && key) {
      seen.add(key)
      result.push(name)
    }
  }
  return result
})

function isSharedCondition(conditionDisplay) {
  const key = conditionDisplay.toLowerCase().trim()
  return conditionNamesA.value.has(key) && conditionNamesB.value.has(key)
}

function getConditionConfidence(causes, conditionDisplay) {
  const key = conditionDisplay.toLowerCase().trim()
  const match = causes.find(c => getConditionName(c) === key)
  return match ? getConfidence(match) : 0
}

function getTopUrgency(causes) {
  if (causes.length === 0) return 'routine'
  const order = ['emergency', 'urgent', 'soon', 'routine']
  for (const level of order) {
    if (causes.some(c => (c.urgency || 'routine') === level)) return level
  }
  return 'routine'
}

const severityDelta = computed(() => {
  const urgencyScore = { emergency: 4, urgent: 3, soon: 2, routine: 1 }
  const scoreA = urgencyScore[getTopUrgency(causesA.value)] || 1
  const scoreB = urgencyScore[getTopUrgency(causesB.value)] || 1
  return scoreB - scoreA
})

const testsASet = computed(() => new Set(testsA.value.map(t => t.toLowerCase().trim())))
const testsBSet = computed(() => new Set(testsB.value.map(t => t.toLowerCase().trim())))

function isSharedTest(test) {
  const key = test.toLowerCase().trim()
  return testsASet.value.has(key) && testsBSet.value.has(key)
}

const newConditions = computed(() => {
  return causesB.value
    .filter(c => !conditionNamesA.value.has(getConditionName(c)))
    .map(getConditionDisplay)
})

const resolvedConditions = computed(() => {
  return causesA.value
    .filter(c => !conditionNamesB.value.has(getConditionName(c)))
    .map(getConditionDisplay)
})

const changedConfidence = computed(() => {
  const result = []
  for (const cB of causesB.value) {
    const key = getConditionName(cB)
    const matchA = causesA.value.find(c => getConditionName(c) === key)
    if (matchA) {
      const confA = getConfidence(matchA)
      const confB = getConfidence(cB)
      if (confA !== confB) {
        result.push({
          condition: getConditionDisplay(cB),
          confA,
          confB,
          delta: confB - confA,
        })
      }
    }
  }
  return result
})

function urgencyClass(urgency) {
  if (urgency === 'emergency') return 'bg-red-500/20 text-red-300'
  if (urgency === 'urgent') return 'bg-red-500/15 text-red-400'
  if (urgency === 'soon') return 'bg-amber-500/15 text-amber-400'
  return 'bg-emerald-500/15 text-emerald-400'
}

function formatDate(timestamp) {
  if (!timestamp) return ''
  try {
    const d = new Date(timestamp)
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return timestamp
  }
}
</script>
