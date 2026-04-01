<template>
  <div class="space-y-4 py-4">
    <!-- Elapsed timer -->
    <div class="flex items-center justify-between px-1">
      <div class="flex items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
        <span class="text-xs font-medium" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Analyzing your case...</span>
      </div>
      <span class="text-xs tabular-nums font-mono" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ elapsed.toFixed(1) }}s</span>
    </div>

    <!-- Mini pipeline tracker -->
    <div class="flex items-center gap-1 px-1">
      <div v-for="(step, i) in pipelineSteps" :key="step.key" class="flex items-center gap-1">
        <div class="w-6 h-6 rounded-full flex items-center justify-center text-tiny font-bold transition-all duration-500"
          :class="getStepClass(step.key)"
          :title="step.name">
          <svg v-if="isCompleted(step.key)" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
          <div v-else-if="isActive(step.key)" class="w-1.5 h-1.5 rounded-full bg-current animate-pulse"></div>
          <span v-else>{{ i + 1 }}</span>
        </div>
        <div v-if="i < pipelineSteps.length - 1" class="w-3 h-px transition-colors duration-500"
          :class="isCompleted(step.key) ? 'bg-emerald-500' : (isDark ? 'bg-slate-700' : 'bg-slate-200')"></div>
      </div>
      <span class="ml-2 text-detail tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ completedCount }}/7</span>
    </div>

    <!-- Live agent result cards -->
    <div class="space-y-3">
      <TransitionGroup name="agent-card">
        <div v-for="result in results" :key="result.agent"
          class="rounded-xl border p-4 transition-all duration-300"
          :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">

          <!-- Card header -->
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded-lg flex items-center justify-center" :style="{ backgroundColor: getAgentColor(result.agent) + '15' }">
                <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: getAgentColor(result.agent) }"></div>
              </div>
              <span class="text-sm font-semibold capitalize" :class="isDark ? 'text-white' : 'text-slate-900'">{{ getAgentLabel(result.agent) }}</span>
            </div>
            <span class="text-detail tabular-nums px-2 py-0.5 rounded-full"
              :class="isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-100 text-slate-500'">{{ result.elapsed.toFixed(1) }}s</span>
          </div>

          <!-- Agent-specific content -->
          <!-- TRIAGE -->
          <div v-if="result.agent === 'triage'" class="space-y-2">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold uppercase px-2 py-0.5 rounded-full" :class="urgencyClass(result.highlights?.urgency)">
                {{ result.highlights?.urgency || 'routine' }}
              </span>
              <span v-if="result.highlights?.red_flags_count" class="text-xs" :class="isDark ? 'text-amber-400' : 'text-amber-600'">
                {{ result.highlights.red_flags_count }} red flag{{ result.highlights.red_flags_count > 1 ? 's' : '' }} detected
              </span>
            </div>
            <p v-if="result.highlights?.domains?.length" class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              Domains: {{ result.highlights.domains.join(', ') }}
            </p>
          </div>

          <!-- DIAGNOSTICIAN -->
          <div v-else-if="result.agent === 'diagnostician'" class="space-y-2">
            <div v-for="dx in (result.highlights?.top_diagnoses || []).slice(0, 3)" :key="dx.name" class="flex items-center gap-2">
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-0.5">
                  <span class="text-xs font-medium truncate" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ dx.name }}</span>
                  <span class="text-detail font-bold tabular-nums ml-2" :class="dx.confidence >= 70 ? 'text-emerald-500' : dx.confidence >= 40 ? 'text-amber-500' : (isDark ? 'text-slate-400' : 'text-slate-500')">{{ dx.confidence }}%</span>
                </div>
                <div class="h-1.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
                  <div class="h-full rounded-full transition-all duration-1000 ease-out"
                    :class="dx.confidence >= 70 ? 'bg-emerald-500' : dx.confidence >= 40 ? 'bg-amber-500' : 'bg-blue-500'"
                    :style="{ width: dx.confidence + '%' }"></div>
                </div>
              </div>
            </div>
            <p v-if="result.highlights?.tests_count" class="text-detail" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              {{ result.highlights.tests_count }} diagnostic tests recommended
            </p>
          </div>

          <!-- RESEARCH -->
          <div v-else-if="result.agent === 'research'">
            <p class="text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
              {{ result.highlights?.evidence_summary_preview || result.findings || 'Evidence review complete' }}
            </p>
            <p v-if="result.highlights?.guidelines_count" class="text-detail mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              {{ result.highlights.guidelines_count }} clinical guidelines referenced
            </p>
          </div>

          <!-- SPECIALIST -->
          <div v-else-if="result.agent === 'specialist'" class="space-y-1">
            <div class="flex items-center gap-2">
              <span v-if="result.highlights?.specialty_consulted" class="text-xs font-medium px-2 py-0.5 rounded-full"
                :class="isDark ? 'bg-purple-500/10 text-purple-400' : 'bg-purple-50 text-purple-600'">
                {{ result.highlights.specialty_consulted }}
              </span>
              <span v-if="result.highlights?.risk_level" class="text-xs font-medium px-2 py-0.5 rounded-full"
                :class="riskClass(result.highlights.risk_level)">
                {{ result.highlights.risk_level }} risk
              </span>
            </div>
            <p v-if="result.highlights?.criteria_applied" class="text-detail" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              Applied: {{ result.highlights.criteria_applied }}
            </p>
          </div>

          <!-- TREATMENT -->
          <div v-else-if="result.agent === 'treatment'" class="flex items-center gap-3">
            <div v-if="result.highlights?.medications_count" class="text-center">
              <div class="text-lg font-bold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ result.highlights.medications_count }}</div>
              <div class="text-tiny uppercase" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Medications</div>
            </div>
            <div v-if="result.highlights?.lifestyle_recs_count" class="text-center">
              <div class="text-lg font-bold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ result.highlights.lifestyle_recs_count }}</div>
              <div class="text-tiny uppercase" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Lifestyle</div>
            </div>
            <span v-if="result.highlights?.has_immediate_actions" class="text-xs font-medium px-2 py-0.5 rounded-full"
              :class="isDark ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-50 text-amber-600'">
              Immediate actions required
            </span>
          </div>

          <!-- SAFETY -->
          <div v-else-if="result.agent === 'safety'" class="flex items-center gap-3">
            <span class="text-xs font-bold uppercase px-3 py-1 rounded-full"
              :class="safetyClass(result.highlights?.status)">
              {{ result.highlights?.status || 'REVIEWED' }}
            </span>
            <span v-if="result.highlights?.warnings_count" class="text-xs" :class="isDark ? 'text-amber-400' : 'text-amber-600'">
              {{ result.highlights.warnings_count }} warning{{ result.highlights.warnings_count > 1 ? 's' : '' }}
            </span>
            <span v-else class="text-xs" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">No safety concerns</span>
          </div>

          <!-- EMPATHY -->
          <div v-else-if="result.agent === 'empathy'">
            <p class="text-xs leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
              {{ (result.highlights?.summary_preview || result.findings || '').slice(0, 150) }}{{ (result.highlights?.summary_preview || '').length > 150 ? '...' : '' }}
            </p>
            <p v-if="result.highlights?.action_items_count" class="text-detail mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              {{ result.highlights.action_items_count }} action items for you
            </p>
          </div>

          <!-- GENERIC FALLBACK -->
          <div v-else>
            <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ result.findings || 'Analysis complete' }}</p>
          </div>
        </div>
      </TransitionGroup>
    </div>

    <!-- Waiting indicator for next agent -->
    <div v-if="completedCount < 7" class="flex items-center gap-2 px-1">
      <div class="flex gap-1">
        <div class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-bounce" style="animation-delay: 0ms"></div>
        <div class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-bounce" style="animation-delay: 150ms"></div>
        <div class="w-1.5 h-1.5 rounded-full bg-blue-500 animate-bounce" style="animation-delay: 300ms"></div>
      </div>
      <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
        {{ activeAgentLabel }}...
      </span>
    </div>

    <!-- Completion message -->
    <div v-else class="flex items-center gap-2 px-1">
      <svg class="w-4 h-4 text-emerald-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
      <span class="text-xs font-medium" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">All 7 agents complete — preparing your report...</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  results: { type: Array, default: () => [] },
  activeAgent: { type: String, default: null },
  completedAgents: { type: Array, default: () => [] },
  elapsed: { type: Number, default: 0 },
})

const pipelineSteps = [
  { key: 'triage', name: 'Triage' },
  { key: 'diagnostician', name: 'Diagnosis' },
  { key: 'research', name: 'Research' },
  { key: 'specialist', name: 'Specialist' },
  { key: 'treatment', name: 'Treatment' },
  { key: 'safety', name: 'Safety' },
  { key: 'empathy', name: 'Summary' },
]

const agentLabels = {
  triage: 'Triage', diagnostician: 'Diagnostician', research: 'Research',
  specialist: 'Specialist', treatment: 'Treatment', safety: 'Safety', empathy: 'Communication',
}

const agentColors = {
  triage: '#3b82f6', diagnostician: '#8b5cf6', research: '#06b6d4',
  specialist: '#6366f1', treatment: '#f59e0b', safety: '#ef4444', empathy: '#ec4899',
}

const completedCount = computed(() => props.completedAgents.length)
const activeAgentLabel = computed(() => {
  if (!props.activeAgent) return 'Processing'
  return agentLabels[props.activeAgent] || props.activeAgent
})

function isActive(key) { return props.activeAgent === key }
function isCompleted(key) { return props.completedAgents.includes(key) }
function getAgentLabel(key) { return agentLabels[key] || key }
function getAgentColor(key) { return agentColors[key] || '#64748b' }

function getStepClass(key) {
  if (isCompleted(key)) return isDark.value ? 'bg-emerald-500/20 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
  if (isActive(key)) return 'bg-blue-500 text-white'
  return isDark.value ? 'bg-slate-800 text-slate-500' : 'bg-slate-200 text-slate-400'
}

function urgencyClass(u) {
  if (u === 'emergency') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
  if (u === 'urgent' || u === 'emergent') return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-700'
  if (u === 'soon') return isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-100 text-blue-700'
  return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
}

function riskClass(level) {
  const l = (level || '').toLowerCase()
  if (l === 'high' || l === 'critical') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
  if (l === 'moderate') return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-700'
  return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
}

function safetyClass(status) {
  const s = (status || '').toLowerCase()
  if (s.includes('fail') || s.includes('alert') || s.includes('critical')) return isDark.value ? 'bg-red-500/20 text-red-300' : 'bg-red-100 text-red-700'
  if (s.includes('caution') || s.includes('warn')) return isDark.value ? 'bg-amber-500/20 text-amber-300' : 'bg-amber-100 text-amber-700'
  return isDark.value ? 'bg-emerald-500/20 text-emerald-300' : 'bg-emerald-100 text-emerald-700'
}
</script>

<style scoped>
.agent-card-enter-active {
  transition: all 0.4s ease-out;
}
.agent-card-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.agent-card-leave-active {
  transition: all 0.2s ease-in;
}
.agent-card-leave-to {
  opacity: 0;
}
</style>
