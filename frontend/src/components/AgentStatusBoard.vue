<template>
  <div class="agent-status-board bg-slate-900/80 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 mx-4 my-3">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-sm font-semibold text-slate-300 uppercase tracking-wider">Agent Pipeline Status</h3>
      <span class="text-xs text-slate-500">{{ completedCount }}/{{ agents.length }} complete</span>
    </div>

    <div class="space-y-1.5">
      <div
        v-for="agent in agents"
        :key="agent.key"
        class="agent-row rounded-lg border px-3 py-2.5 transition-all duration-500 cursor-pointer"
        :class="getRowClasses(agent.key)"
        @click="toggleExpand(agent.key)"
      >
        <div class="flex items-center gap-3">
          <!-- Status icon -->
          <div class="flex-shrink-0 w-6 h-6 flex items-center justify-center">
            <!-- Error -->
            <svg v-if="hasError(agent.key)" class="w-5 h-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <!-- Completed -->
            <svg v-else-if="isCompleted(agent.key)" class="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <!-- Active spinner -->
            <div v-else-if="isActive(agent.key)" class="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
            <!-- Waiting -->
            <div v-else class="w-4 h-4 rounded-full bg-slate-700 border border-slate-600"></div>
          </div>

          <!-- Agent icon -->
          <span class="text-base flex-shrink-0">{{ agent.icon }}</span>

          <!-- Agent info -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium" :class="getNameClass(agent.key)">{{ agent.name }}</span>
              <span class="text-xs tabular-nums" :class="getTimingClass(agent.key)">
                <template v-if="isActive(agent.key)">{{ liveTimer.toFixed(1) }}s</template>
                <template v-else-if="agentTimings[agent.key]">{{ agentTimings[agent.key].toFixed(1) }}s</template>
                <template v-else>&mdash;</template>
              </span>
            </div>
            <div class="text-xs mt-0.5 truncate" :class="getStatusClass(agent.key)">
              <template v-if="hasError(agent.key)">Error: {{ errors[agent.key] }}</template>
              <template v-else-if="isCompleted(agent.key) && agentFindings[agent.key]">{{ agentFindings[agent.key] }}</template>
              <template v-else-if="isActive(agent.key)">{{ agent.activeLabel }}</template>
              <template v-else>Waiting</template>
            </div>
          </div>

          <!-- Expand arrow -->
          <div v-if="isCompleted(agent.key) && agentFindings[agent.key]" class="flex-shrink-0 ml-1">
            <svg
              class="w-4 h-4 text-slate-500 transition-transform duration-200"
              :class="{ 'rotate-180': expandedAgent === agent.key }"
              fill="currentColor" viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>

        <!-- Expanded details -->
        <transition name="expand">
          <div v-if="expandedAgent === agent.key && isCompleted(agent.key)" class="mt-2 pt-2 border-t border-slate-700/50">
            <p class="text-xs text-slate-400 leading-relaxed">{{ agentFindings[agent.key] || 'No details available' }}</p>
            <div v-if="agentTimings[agent.key]" class="mt-1 text-[10px] text-slate-500">
              Completed in {{ agentTimings[agent.key].toFixed(2) }} seconds
            </div>
          </div>
        </transition>
      </div>
    </div>

    <!-- Progress bar -->
    <div class="mt-3 h-1.5 bg-slate-800 rounded-full overflow-hidden">
      <div
        class="h-full rounded-full transition-all duration-700 ease-out"
        :class="progressBarClass"
        :style="{ width: progressPercent + '%' }"
      ></div>
    </div>

    <!-- Estimated cost -->
    <div class="mt-2.5 flex items-center justify-between text-[10px] text-slate-500">
      <span>Est. cost: ~${{ estimatedCost }}</span>
      <span>{{ currentModel }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'

const props = defineProps({
  activeAgent: { type: String, default: null },
  completedAgents: { type: Array, default: () => [] },
  agentTimings: { type: Object, default: () => ({}) },
  agentFindings: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) }
})

const agents = [
  { key: 'triage', name: 'Triage Agent', icon: '\u{1F6A8}', activeLabel: 'Assessing urgency and red flags...' },
  { key: 'diagnostician', name: 'Diagnostician', icon: '\u{1FA7A}', activeLabel: 'Generating differential diagnosis...' },
  { key: 'research', name: 'Research Agent', icon: '\u{1F4DA}', activeLabel: 'Searching clinical guidelines...' },
  { key: 'specialist', name: 'Specialist', icon: '\u{1F9D1}\u200D\u2695\uFE0F', activeLabel: 'Deep specialty analysis...' },
  { key: 'treatment', name: 'Treatment Planner', icon: '\u{1F48A}', activeLabel: 'Creating treatment plan...' },
  { key: 'safety', name: 'Safety Reviewer', icon: '\u{1F6E1}\uFE0F', activeLabel: 'Checking for safety concerns...' },
  { key: 'empathy', name: 'Empathy Agent', icon: '\u{1F49A}', activeLabel: 'Writing patient-friendly summary...' }
]

// Model and cost estimation
const modelPref = localStorage.getItem('model_preference') || 'auto'
const modelCosts = {
  'auto': { perAgent: 0.015, name: 'Claude Sonnet (auto)' },
  'opus': { perAgent: 0.075, name: 'Claude Opus 4.6' },
  'sonnet': { perAgent: 0.015, name: 'Claude Sonnet 4.6' },
  'haiku': { perAgent: 0.005, name: 'Claude Haiku 4.5' },
  'gpt-4o': { perAgent: 0.025, name: 'GPT-4o' },
  'gpt-4o-mini': { perAgent: 0.003, name: 'GPT-4o Mini' },
  'o3': { perAgent: 0.10, name: 'OpenAI o3' },
  'gemini-2.5-pro': { perAgent: 0.02, name: 'Gemini 2.5 Pro' },
  'gemini-2.5-flash': { perAgent: 0.005, name: 'Gemini 2.5 Flash' },
}
const modelInfo = modelCosts[modelPref] || modelCosts['auto']
const currentModel = modelInfo.name

const estimatedCost = computed(() => {
  const completed = props.completedAgents.length
  const total = agents.length
  const costSoFar = completed * modelInfo.perAgent
  const projected = total * modelInfo.perAgent
  if (completed === total) return costSoFar.toFixed(3)
  return `${costSoFar.toFixed(3)} / ~${projected.toFixed(2)}`
})

const expandedAgent = ref(null)
const liveTimer = ref(0)
let liveTimerInterval = null
let liveTimerStart = null

// Live timer for currently active agent
watch(() => props.activeAgent, (newAgent) => {
  if (liveTimerInterval) {
    clearInterval(liveTimerInterval)
    liveTimerInterval = null
  }
  if (newAgent) {
    liveTimerStart = Date.now()
    liveTimer.value = 0
    liveTimerInterval = setInterval(() => {
      liveTimer.value = (Date.now() - liveTimerStart) / 1000
    }, 100)
  } else {
    liveTimer.value = 0
  }
}, { immediate: true })

onUnmounted(() => {
  if (liveTimerInterval) clearInterval(liveTimerInterval)
})

const completedCount = computed(() => props.completedAgents.length)

const progressPercent = computed(() => {
  const total = agents.length
  const done = props.completedAgents.length
  const activeBonus = props.activeAgent ? 0.5 : 0
  return Math.min(100, ((done + activeBonus) / total) * 100)
})

const progressBarClass = computed(() => {
  if (props.completedAgents.length === agents.length) return 'bg-emerald-500'
  return 'bg-gradient-to-r from-blue-500 to-blue-400'
})

function isActive(key) {
  return props.activeAgent === key
}

function isCompleted(key) {
  return props.completedAgents.includes(key)
}

function hasError(key) {
  return !!(props.errors && props.errors[key])
}

function toggleExpand(key) {
  expandedAgent.value = expandedAgent.value === key ? null : key
}

function getRowClasses(key) {
  if (hasError(key)) return 'border-red-500/40 bg-red-500/5'
  if (isActive(key)) return 'border-blue-500/50 bg-blue-500/10 shadow-md shadow-blue-500/5'
  if (isCompleted(key)) return 'border-emerald-500/30 bg-emerald-500/5'
  return 'border-slate-700/30 bg-slate-800/20'
}

function getNameClass(key) {
  if (hasError(key)) return 'text-red-300'
  if (isActive(key)) return 'text-blue-200'
  if (isCompleted(key)) return 'text-emerald-300'
  return 'text-slate-500'
}

function getTimingClass(key) {
  if (isActive(key)) return 'text-blue-400 animate-pulse'
  if (isCompleted(key)) return 'text-emerald-500/70'
  return 'text-slate-600'
}

function getStatusClass(key) {
  if (hasError(key)) return 'text-red-400/80'
  if (isCompleted(key)) return 'text-emerald-400/70'
  if (isActive(key)) return 'text-blue-400/70'
  return 'text-slate-600'
}
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  margin-top: 0;
  padding-top: 0;
}
.expand-enter-to,
.expand-leave-from {
  max-height: 100px;
  opacity: 1;
}
</style>
