<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-blue-600/5' : 'bg-blue-400/10'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-slate-600/5' : 'bg-slate-400/8'"></div>
    </div>

    <!-- Nav bar -->
    <AppNav currentPage="second-opinion" />

    <!-- Main content -->
    <div class="relative z-10 max-w-5xl mx-auto px-4 py-6 space-y-6">

      <div>
        <h1 class="text-2xl font-bold text-[var(--text-primary)]">AI Second Opinion</h1>
        <p class="text-sm text-[var(--text-secondary)] mt-1">Run the same case through multiple AI models and review consensus.</p>
      </div>

      <!-- Step 1: Case Selection -->
      <div class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center gap-2 mb-4">
          <div class="w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold">1</div>
          <h2 class="text-sm font-semibold text-[var(--text-primary)]">Select Case</h2>
        </div>

        <!-- Load from history -->
        <div v-if="pastSessions.length > 0" class="space-y-2 mb-4">
          <p class="text-xs text-[var(--text-secondary)] mb-2">Select a past diagnosis or enter symptoms manually.</p>
          <button v-for="sess in pastSessions.slice(0, 5)" :key="sess.id"
            @click="selectSession(sess)"
            class="w-full text-left px-4 py-3 rounded-xl border text-sm transition-all"
            :class="selectedCase?.id === sess.id
              ? (isDark ? 'border-blue-500 bg-blue-500/10 text-blue-300' : 'border-blue-500 bg-blue-50 text-blue-700')
              : (isDark ? 'border-slate-600 hover:border-slate-500 text-slate-300 hover:bg-slate-700/50' : 'border-slate-200 hover:border-slate-300 text-slate-700 hover:bg-slate-50')">
            <div class="flex items-center justify-between">
              <div class="flex-1 min-w-0">
                <span class="font-medium truncate block">{{ sess.topDiagnosis }}</span>
                <span class="text-xs text-[var(--text-secondary)]">{{ sess.symptomsSummary }}</span>
              </div>
              <div class="text-right flex-shrink-0 ml-3">
                <span class="text-xs text-[var(--text-secondary)]">{{ formatDate(sess.timestamp) }}</span>
                <div v-if="sess.confidence" class="text-xs font-medium" :class="sess.confidence >= 70 ? 'text-emerald-500' : 'text-amber-500'">
                  {{ sess.confidence }}% conf.
                </div>
              </div>
            </div>
          </button>
        </div>

        <!-- Manual entry -->
        <div class="space-y-3">
          <p v-if="pastSessions.length === 0" class="text-xs text-[var(--text-secondary)] mb-2">No past diagnoses found. Enter symptoms manually.</p>
          <div>
            <label class="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">Symptoms</label>
            <textarea v-model="manualSymptoms" rows="3" placeholder="Describe symptoms, duration, severity..."
              class="w-full px-4 py-3 rounded-xl border text-sm outline-none transition-colors resize-none"
              :class="isDark
                ? 'bg-slate-900/60 border-slate-600 text-white placeholder-slate-500 focus:border-blue-500'
                : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400 focus:border-blue-500'"></textarea>
          </div>
          <div class="flex gap-3">
            <div class="w-28">
              <label class="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">Age</label>
              <input v-model.number="manualAge" type="number" min="1" max="120" placeholder="35"
                class="w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors"
                :class="isDark
                  ? 'bg-slate-900/60 border-slate-600 text-white focus:border-blue-500'
                  : 'bg-slate-50 border-slate-200 text-slate-900 focus:border-blue-500'" />
            </div>
            <div class="w-36">
              <label class="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">Gender</label>
              <select v-model="manualGender"
                class="w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors appearance-none cursor-pointer"
                :class="isDark
                  ? 'bg-slate-900/60 border-slate-600 text-white focus:border-blue-500'
                  : 'bg-slate-50 border-slate-200 text-slate-900 focus:border-blue-500'">
                <option value="female">Female</option>
                <option value="male">Male</option>
                <option value="other">Other</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Model Selection -->
      <div class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center gap-2 mb-4">
          <div class="w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold">2</div>
          <h2 class="text-sm font-semibold text-[var(--text-primary)]">Select Models</h2>
        </div>

        <p class="text-xs text-[var(--text-secondary)] mb-3">Choose 2 or more models to compare. More models give higher confidence in consensus.</p>

        <div class="space-y-2">
          <label v-for="model in availableModels" :key="model.id"
            class="flex items-center gap-3 px-4 py-3 rounded-xl border text-sm cursor-pointer transition-all"
            :class="selectedModels.includes(model.id)
              ? (isDark ? 'border-blue-500 bg-blue-500/10' : 'border-blue-500 bg-blue-50')
              : (isDark ? 'border-slate-600 hover:border-slate-500' : 'border-slate-200 hover:border-slate-300')">
            <input type="checkbox" :value="model.id" v-model="selectedModels"
              class="w-4 h-4 rounded border-2 accent-blue-500" />
            <div class="flex-1">
              <span class="font-medium text-[var(--text-primary)]">{{ model.name }}</span>
              <span class="text-xs ml-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ model.vendor }}</span>
            </div>
            <span class="text-xs font-mono px-2 py-0.5 rounded-md"
              :class="isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-100 text-slate-500'">
              ~{{ model.estimatedCost }}
            </span>
          </label>
        </div>

        <div class="mt-3 flex items-center justify-between text-xs">
          <span class="text-[var(--text-secondary)]">{{ selectedModels.length }} model{{ selectedModels.length !== 1 ? 's' : '' }} selected</span>
          <span v-if="selectedModels.length >= 2" class="font-medium" :class="isDark ? 'text-blue-400' : 'text-blue-600'">
            Est. total: {{ estimatedTotal }}
          </span>
        </div>
      </div>

      <!-- Get Second Opinion Button -->
      <div class="flex justify-center">
        <button @click="runComparison" :disabled="!canRun || running"
          class="px-8 py-3 rounded-2xl text-sm font-bold transition-all"
          :class="canRun && !running
            ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:shadow-lg hover:shadow-blue-500/25 hover:scale-[1.02]'
            : 'opacity-40 cursor-not-allowed ' + (isDark ? 'bg-slate-700 text-slate-500' : 'bg-slate-200 text-slate-400')">
          <span v-if="running" class="flex items-center gap-2">
            <span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            Running analysis...
          </span>
          <span v-else>Get Second Opinion</span>
        </button>
      </div>

      <!-- Progress -->
      <div v-if="running" class="rounded-2xl border p-5"
        :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
        <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4">Running Models...</h3>
        <div class="space-y-3">
          <div v-for="model in runningModels" :key="model.id" class="flex items-center gap-3">
            <div class="w-5 h-5 flex items-center justify-center">
              <span v-if="model.status === 'done'" class="text-emerald-500">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              </span>
              <span v-else-if="model.status === 'error'" class="text-amber-500">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
              </span>
              <span v-else class="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></span>
            </div>
            <span class="text-sm font-medium text-[var(--text-primary)]">{{ model.name }}</span>
            <span class="text-xs text-[var(--text-secondary)]">{{ model.status === 'done' ? model.time + 's' : model.status === 'error' ? 'Failed' : 'Running...' }}</span>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-if="results" class="space-y-6">

        <!-- Consensus Report -->
        <div class="rounded-2xl border p-6"
          :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h2 class="text-lg font-bold text-[var(--text-primary)] mb-1">Consensus Report</h2>
          <p class="text-xs text-[var(--text-secondary)] mb-5">{{ results.modelResults.length }} models analyzed</p>

          <!-- Consensus Banner -->
          <div class="rounded-xl px-5 py-4 mb-5"
            :class="consensusLevel === 'strong'
              ? (isDark ? 'bg-emerald-900/30 border border-emerald-700/50' : 'bg-emerald-50 border border-emerald-200')
              : consensusLevel === 'mixed'
                ? (isDark ? 'bg-amber-900/20 border border-amber-700/50' : 'bg-amber-50 border border-amber-200')
                : (isDark ? 'bg-purple-900/20 border border-purple-700/50' : 'bg-purple-50 border border-purple-200')">
            <div class="flex items-start gap-4">
              <div class="text-3xl">
                {{ consensusLevel === 'strong' ? '\u2705' : consensusLevel === 'mixed' ? '\u26A0\uFE0F' : '\uD83D\uDD0D' }}
              </div>
              <div>
                <h3 class="font-bold text-base"
                  :class="consensusLevel === 'strong'
                    ? (isDark ? 'text-emerald-300' : 'text-emerald-800')
                    : consensusLevel === 'mixed'
                      ? (isDark ? 'text-amber-300' : 'text-amber-800')
                      : (isDark ? 'text-purple-300' : 'text-purple-800')">
                  {{ consensusDiagnosis }}
                </h3>
                <p class="text-sm mt-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  {{ consensusSummary }}
                </p>
              </div>
            </div>
          </div>

          <!-- Agreement Matrix -->
          <div class="mb-5">
            <h3 class="text-xs font-semibold text-[var(--text-secondary)] uppercase tracking-wider mb-3">Agreement Matrix</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr>
                    <th class="text-left pb-2 text-xs font-medium text-[var(--text-secondary)]">Model</th>
                    <th class="text-left pb-2 text-xs font-medium text-[var(--text-secondary)]">Top Diagnosis</th>
                    <th class="text-center pb-2 text-xs font-medium text-[var(--text-secondary)]">Agrees</th>
                    <th class="text-right pb-2 text-xs font-medium text-[var(--text-secondary)]">Confidence</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="mr in results.modelResults" :key="mr.model" class="border-t" :style="{ borderColor: 'var(--clinical-border)' }">
                    <td class="py-2.5 font-medium text-[var(--text-primary)]">{{ mr.modelName }}</td>
                    <td class="py-2.5 text-[var(--text-secondary)]">{{ mr.topDiagnosis }}</td>
                    <td class="py-2.5 text-center">
                      <span v-if="mr.agreesWithConsensus" class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-500 text-xs font-bold">Y</span>
                      <span v-else class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-500/20 text-amber-500 text-xs font-bold">N</span>
                    </td>
                    <td class="py-2.5 text-right">
                      <span class="font-semibold" :class="mr.confidence >= 70 ? 'text-emerald-500' : mr.confidence >= 40 ? 'text-amber-500' : 'text-slate-400'">
                        {{ mr.confidence }}%
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Combined Confidence -->
          <div class="flex items-center gap-4 mb-5">
            <div class="text-center">
              <div class="text-3xl font-bold" :class="results.combinedConfidence >= 70 ? 'text-emerald-500' : results.combinedConfidence >= 40 ? 'text-amber-500' : 'text-slate-400'">
                {{ results.combinedConfidence }}%
              </div>
              <div class="text-xs text-[var(--text-secondary)]">Combined Confidence</div>
            </div>
            <div class="flex-1 h-3 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
              <div class="h-full rounded-full transition-all duration-1000"
                :class="results.combinedConfidence >= 70 ? 'bg-emerald-500' : results.combinedConfidence >= 40 ? 'bg-amber-500' : 'bg-slate-400'"
                :style="{ width: results.combinedConfidence + '%' }"></div>
            </div>
          </div>

          <!-- Recommended Action -->
          <div class="rounded-xl px-4 py-3"
            :class="isDark ? 'bg-slate-700/50' : 'bg-slate-50'">
            <p class="text-xs font-semibold text-[var(--text-secondary)] uppercase tracking-wider mb-1">Recommended Action</p>
            <p class="text-sm text-[var(--text-primary)]">{{ recommendedAction }}</p>
          </div>
        </div>

        <!-- Disagreements -->
        <div v-if="disagreements.length > 0" class="rounded-2xl border p-5"
          :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-3">Points of Disagreement</h3>
          <div class="space-y-3">
            <div v-for="(d, idx) in disagreements" :key="idx"
              class="rounded-xl border px-4 py-3"
              :class="isDark ? 'border-amber-800/40 bg-amber-900/10' : 'border-amber-200 bg-amber-50/50'">
              <p class="text-sm font-medium" :class="isDark ? 'text-amber-300' : 'text-amber-800'">
                {{ d.modelName }} suggests: {{ d.topDiagnosis }}
              </p>
              <p class="text-xs text-[var(--text-secondary)] mt-0.5">
                Confidence: {{ d.confidence }}% &mdash; {{ d.reasoning || 'Different weighting of presented symptoms.' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Side-by-Side Comparison Table -->
        <div class="rounded-2xl border p-5"
          :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4">Side-by-Side Comparison</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr>
                  <th class="text-left pb-3 text-xs font-medium text-[var(--text-secondary)] min-w-[100px]">Model</th>
                  <th class="text-left pb-3 text-xs font-medium text-[var(--text-secondary)] min-w-[140px]">Diagnosis</th>
                  <th class="text-center pb-3 text-xs font-medium text-[var(--text-secondary)]">Confidence</th>
                  <th class="text-left pb-3 text-xs font-medium text-[var(--text-secondary)] min-w-[160px]">Key Tests</th>
                  <th class="text-left pb-3 text-xs font-medium text-[var(--text-secondary)] min-w-[160px]">Treatment</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="mr in results.modelResults" :key="mr.model + '_cmp'" class="border-t" :style="{ borderColor: 'var(--clinical-border)' }">
                  <td class="py-3 font-medium text-[var(--text-primary)] align-top">{{ mr.modelName }}</td>
                  <td class="py-3 align-top">
                    <span class="px-2 py-0.5 rounded-md text-xs font-medium"
                      :class="mr.agreesWithConsensus
                        ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700')
                        : (isDark ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-700')">
                      {{ mr.topDiagnosis }}
                    </span>
                  </td>
                  <td class="py-3 text-center align-top">
                    <span class="font-semibold" :class="mr.confidence >= 70 ? 'text-emerald-500' : 'text-amber-500'">
                      {{ mr.confidence }}%
                    </span>
                  </td>
                  <td class="py-3 text-xs text-[var(--text-secondary)] align-top">{{ mr.tests || 'N/A' }}</td>
                  <td class="py-3 text-xs text-[var(--text-secondary)] align-top">{{ mr.treatment || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Disclaimer -->
        <div class="text-center">
          <p class="text-xs text-[var(--text-secondary)]">
            This multi-model analysis is for informational purposes only and does not constitute medical advice.
            Always consult a qualified healthcare provider for diagnosis and treatment.
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import AppNav from '@/components/AppNav.vue'
import { diagnose } from '@/services/api'
import { getSessionsAsync, getSessionAsync } from '@/services/historyService'

const { isDark } = useTheme()

// ── Past Sessions ─────────────────────────────────────────────
const pastSessions = ref([])
const selectedCase = ref(null)
const manualSymptoms = ref('')
const manualAge = ref(35)
const manualGender = ref('female')

onMounted(async () => {
  try {
    pastSessions.value = await getSessionsAsync()
  } catch {
    pastSessions.value = []
  }
})

async function selectSession(sess) {
  selectedCase.value = sess
  // Load full session to extract symptoms
  try {
    const full = await getSessionAsync(sess.id)
    if (full) {
      manualSymptoms.value = full.symptoms || sess.symptomsSummary || ''
      manualAge.value = parseInt(full.age) || 35
      manualGender.value = full.gender || 'female'
    }
  } catch {
    manualSymptoms.value = sess.symptomsSummary || ''
  }
}

// ── Model Selection ───────────────────────────────────────────
const availableModels = [
  { id: 'claude-sonnet', name: 'Claude Sonnet', vendor: 'Anthropic', estimatedCost: '$0.02' },
  { id: 'claude-haiku', name: 'Claude Haiku', vendor: 'Anthropic', estimatedCost: '$0.005' },
  { id: 'gpt-4o', name: 'GPT-4o', vendor: 'OpenAI', estimatedCost: '$0.03' },
  { id: 'gpt-4o-mini', name: 'GPT-4o Mini', vendor: 'OpenAI', estimatedCost: '$0.005' },
]

const selectedModels = ref(['claude-sonnet', 'gpt-4o'])

const estimatedTotal = computed(() => {
  const costs = { 'claude-sonnet': 0.02, 'claude-haiku': 0.005, 'gpt-4o': 0.03, 'gpt-4o-mini': 0.005 }
  const total = selectedModels.value.reduce((sum, id) => sum + (costs[id] || 0), 0)
  return '$' + total.toFixed(3)
})

const canRun = computed(() => {
  return selectedModels.value.length >= 2 && (manualSymptoms.value.trim().length > 5)
})

// ── Run Comparison ────────────────────────────────────────────
const running = ref(false)
const runningModels = ref([])
const results = ref(null)

async function runComparison() {
  if (!canRun.value || running.value) return
  running.value = true
  results.value = null

  const models = selectedModels.value.map(id => availableModels.find(m => m.id === id))
  runningModels.value = models.map(m => ({ id: m.id, name: m.name, status: 'running', time: null }))

  const modelResults = []

  // Run each model sequentially through the diagnose endpoint
  for (let i = 0; i < models.length; i++) {
    const model = models[i]
    const startTime = Date.now()
    try {
      const payload = {
        symptoms: manualSymptoms.value,
        age: manualAge.value,
        gender: manualGender.value,
        model_hint: model.id
      }
      const result = await diagnose(payload)
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)
      runningModels.value[i].status = 'done'
      runningModels.value[i].time = elapsed

      // Parse the result
      const causes = result.causes || []
      const topCause = causes[0] || {}
      const tests = (result.recommended_tests || []).slice(0, 3).join(', ')
      const treatment = (result.recommended_actions || result.recommendations || []).slice(0, 2).join(', ')

      modelResults.push({
        model: model.id,
        modelName: model.name,
        topDiagnosis: topCause.cause || topCause.condition || 'Unable to determine',
        confidence: topCause.value || topCause.confidence || 0,
        tests: tests || 'Standard workup',
        treatment: treatment || 'See full report',
        allCauses: causes,
        reasoning: topCause.reasoning || '',
        raw: result
      })
    } catch (err) {
      runningModels.value[i].status = 'error'
      modelResults.push({
        model: model.id,
        modelName: model.name,
        topDiagnosis: 'Error',
        confidence: 0,
        tests: 'N/A',
        treatment: 'N/A',
        allCauses: [],
        reasoning: err.message || 'Model unavailable',
        raw: null
      })
    }
  }

  // Build consensus
  const validResults = modelResults.filter(r => r.confidence > 0)

  // Find most common top diagnosis (case-insensitive)
  const diagCounts = {}
  validResults.forEach(r => {
    const key = r.topDiagnosis.toLowerCase().trim()
    diagCounts[key] = (diagCounts[key] || 0) + 1
  })
  const sortedDiags = Object.entries(diagCounts).sort((a, b) => b[1] - a[1])
  const topConsensus = sortedDiags[0] ? sortedDiags[0][0] : ''
  const topCount = sortedDiags[0] ? sortedDiags[0][1] : 0

  // Mark agreement
  modelResults.forEach(r => {
    r.agreesWithConsensus = r.topDiagnosis.toLowerCase().trim() === topConsensus
  })

  // Combined confidence
  const avgConfidence = validResults.length > 0
    ? Math.round(validResults.reduce((sum, r) => sum + r.confidence, 0) / validResults.length)
    : 0

  results.value = {
    modelResults,
    topConsensus: validResults.find(r => r.topDiagnosis.toLowerCase().trim() === topConsensus)?.topDiagnosis || 'Inconclusive',
    agreementCount: topCount,
    totalModels: modelResults.length,
    combinedConfidence: avgConfidence
  }

  running.value = false
}

// ── Consensus Computed ────────────────────────────────────────
const consensusLevel = computed(() => {
  if (!results.value) return ''
  const pct = results.value.agreementCount / results.value.totalModels
  if (pct >= 0.8) return 'strong'
  if (pct >= 0.5) return 'mixed'
  return 'disagree'
})

const consensusDiagnosis = computed(() => {
  if (!results.value) return ''
  if (consensusLevel.value === 'strong') {
    return `${results.value.agreementCount} of ${results.value.totalModels} models agree: ${results.value.topConsensus}`
  }
  if (consensusLevel.value === 'mixed') {
    return `Partial agreement: ${results.value.topConsensus}`
  }
  return 'Models disagree on primary diagnosis'
})

const consensusSummary = computed(() => {
  if (!results.value) return ''
  if (consensusLevel.value === 'strong') {
    return 'Strong consensus across AI models supports this diagnosis with high confidence.'
  }
  if (consensusLevel.value === 'mixed') {
    return 'Some models agree, but there are alternative possibilities worth discussing with your doctor.'
  }
  return 'The AI models produced different primary diagnoses. A specialist evaluation is recommended for clarity.'
})

const recommendedAction = computed(() => {
  if (!results.value) return ''
  if (consensusLevel.value === 'strong' && results.value.combinedConfidence >= 70) {
    return 'Your diagnosis is well-supported across multiple AI models. Discuss these findings with your healthcare provider for confirmation.'
  }
  if (consensusLevel.value === 'mixed') {
    return 'Consider discussing these possibilities with your doctor. The partial agreement suggests multiple viable diagnoses that clinical examination can help distinguish.'
  }
  return 'The AI models disagree significantly. We recommend a specialist evaluation to clarify the diagnosis. Bring these results to your appointment for discussion.'
})

const disagreements = computed(() => {
  if (!results.value) return []
  return results.value.modelResults.filter(r => !r.agreesWithConsensus && r.confidence > 0)
})

// ── Formatting ────────────────────────────────────────────────
function formatDate(iso) {
  try { return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) } catch { return iso }
}
</script>
