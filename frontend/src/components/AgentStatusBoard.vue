<template>
  <div class="agent-status-board relative rounded-2xl overflow-hidden mx-4 my-3 border transition-colors"
    :class="isDark
      ? 'border-white/[0.06]'
      : 'border-slate-200 bg-white shadow-sm'"
    :style="{ background: isDark ? 'linear-gradient(145deg, #0a0f1c 0%, #070b16 50%, #05070d 100%)' : undefined }">
    <!-- Ambient background (dark only) -->
    <div v-if="isDark" class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute w-[250px] h-[250px] -top-[80px] -left-[60px] rounded-full blur-[100px] opacity-[0.04]"
        style="background: radial-gradient(circle, #8b5cf6, transparent)"></div>
      <div class="absolute w-[200px] h-[200px] -bottom-[60px] -right-[40px] rounded-full blur-[80px] opacity-[0.03]"
        style="background: radial-gradient(circle, #06b6d4, transparent)"></div>
      <svg class="absolute inset-0 w-full h-full opacity-[0.025]" xmlns="http://www.w3.org/2000/svg">
        <line x1="5%" y1="10%" x2="95%" y2="90%" stroke="#8b5cf6" stroke-width="0.3" stroke-dasharray="5 3" class="neural-drift n1" />
        <line x1="95%" y1="20%" x2="5%" y2="80%" stroke="#06b6d4" stroke-width="0.3" stroke-dasharray="5 3" class="neural-drift n2" />
      </svg>
    </div>

    <div class="relative z-10 p-5">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center border shadow-lg"
            :class="isDark ? 'bg-gradient-to-br from-violet-500/50 to-cyan-500/30 border-white/10 shadow-violet-500/10' : 'bg-gradient-to-br from-violet-500 to-cyan-500 border-violet-300 shadow-violet-200'">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
          <div>
            <h3 class="text-sm font-bold uppercase tracking-wider" :class="isDark ? 'text-white' : 'text-slate-800'">Agent Pipeline Status</h3>
            <p class="text-detail mt-0.5" :class="isDark ? 'text-white/30' : 'text-slate-400'">Real-time diagnostic processing</p>
          </div>
        </div>
        <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-full border"
          :class="isDark ? 'bg-white/[0.04] border-white/[0.08]' : 'bg-slate-100 border-slate-200'">
          <span class="text-detail font-semibold tabular-nums" :style="{ color: completedCount === agents.length ? '#22c55e' : '#3b82f6' }">
            {{ completedCount }}/{{ agents.length }}
          </span>
          <span class="text-detail" :class="isDark ? 'text-white/30' : 'text-slate-400'">complete</span>
        </div>
      </div>

      <!-- Agent rows -->
      <div class="space-y-2">
        <div
          v-for="agent in agents"
          :key="agent.key"
          class="agent-row group relative rounded-xl border transition-all duration-500 cursor-pointer overflow-hidden"
          :class="getRowClasses(agent)"
          @click="toggleExpand(agent.key)"
        >
          <!-- Active agent inner glow (dark only) -->
          <div v-if="isActive(agent.key) && isDark" class="absolute inset-0 pointer-events-none"
            :style="{ background: `radial-gradient(ellipse at 20% 50%, ${agent.color}10 0%, transparent 60%)` }"></div>

          <!-- Energy ring for active (dark only) -->
          <div v-if="isActive(agent.key) && isDark" class="absolute inset-0 rounded-xl pointer-events-none energy-ring"
            :style="energyRingStyle(agent.color)"></div>

          <div class="relative px-3.5 py-3 flex items-center gap-3">
            <!-- Status icon -->
            <div class="relative flex-shrink-0 w-7 h-7 flex items-center justify-center">
              <!-- Glow -->
              <div v-if="(isActive(agent.key) || isCompleted(agent.key)) && isDark" class="absolute inset-0 rounded-full blur-md -z-10"
                :style="{ background: hasError(agent.key) ? '#ef444430' : isCompleted(agent.key) ? '#22c55e20' : `${agent.color}25` }"
                :class="isActive(agent.key) ? 'glow-pulse' : ''"></div>
              <!-- Error -->
              <svg v-if="hasError(agent.key)" class="w-5 h-5 text-red-400 drop-shadow-[0_0_4px_rgba(239,68,68,0.5)]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <!-- Completed -->
              <svg v-else-if="isCompleted(agent.key)" class="w-5 h-5 text-emerald-400 drop-shadow-[0_0_4px_rgba(34,197,94,0.5)]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              <!-- Active spinner -->
              <div v-else-if="isActive(agent.key)" class="w-5 h-5 rounded-full border-2 border-t-transparent animate-spin"
                :style="{ borderColor: `${agent.color}70`, borderTopColor: 'transparent' }"></div>
              <!-- Waiting -->
              <div v-else class="w-4 h-4 rounded-full" :class="isDark ? 'bg-white/[0.04] border border-white/[0.08]' : 'bg-slate-200 border border-slate-300'"></div>
            </div>

            <!-- Agent icon -->
            <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 text-base transition-all duration-300"
              :class="isActive(agent.key) ? (isDark ? '' : 'bg-blue-50') : isCompleted(agent.key) ? (isDark ? '' : 'bg-emerald-50') : (isDark ? '' : 'bg-slate-100')"
              :style="isDark ? { background: isActive(agent.key) ? `${agent.color}15` : isCompleted(agent.key) ? 'rgba(34,197,94,0.08)' : 'rgba(255,255,255,0.03)' } : undefined">
              {{ agent.icon }}
            </div>

            <!-- Agent info -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between">
                <span class="text-sm font-semibold transition-colors duration-300"
                  :class="hasError(agent.key) ? (isDark ? 'text-red-400' : 'text-red-600') : isActive(agent.key) ? (isDark ? 'text-white' : 'text-blue-700') : isCompleted(agent.key) ? (isDark ? 'text-emerald-400/90' : 'text-emerald-700') : (isDark ? 'text-white/30' : 'text-slate-400')">
                  {{ agent.name }}
                </span>
                <span class="text-caption tabular-nums font-medium"
                  :class="[isActive(agent.key) ? 'animate-pulse' : '', isActive(agent.key) ? (isDark ? 'text-blue-400' : 'text-blue-600') : isCompleted(agent.key) ? (isDark ? 'text-emerald-500/50' : 'text-emerald-600') : (isDark ? 'text-white/15' : 'text-slate-400')]">
                  <template v-if="isActive(agent.key)">{{ liveTimer.toFixed(1) }}s</template>
                  <template v-else-if="agentTimings[agent.key]">{{ agentTimings[agent.key].toFixed(1) }}s</template>
                  <template v-else>&mdash;</template>
                </span>
              </div>
              <div class="text-caption mt-0.5 truncate transition-colors duration-300"
                :class="hasError(agent.key) ? (isDark ? 'text-red-400/70' : 'text-red-500') : isActive(agent.key) ? (isDark ? 'text-white/40' : 'text-blue-500') : isCompleted(agent.key) ? (isDark ? 'text-emerald-500/40' : 'text-emerald-600') : (isDark ? 'text-white/15' : 'text-slate-400')">
                <template v-if="hasError(agent.key)">Error: {{ errors[agent.key] }}</template>
                <template v-else-if="isCompleted(agent.key) && agentFindings[agent.key]">{{ agentFindings[agent.key] }}</template>
                <template v-else-if="isActive(agent.key)">{{ agent.activeLabel }}</template>
                <template v-else>Waiting</template>
              </div>
            </div>

            <!-- Expand arrow -->
            <div v-if="isCompleted(agent.key) && agentFindings[agent.key]" class="flex-shrink-0 ml-1">
              <svg class="w-4 h-4 transition-transform duration-200"
                :class="[expandedAgent === agent.key ? 'rotate-180' : '', isDark ? 'text-white/20' : 'text-slate-400']"
                fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>

          <!-- Expanded details -->
          <div class="expand-region" :class="expandedAgent === agent.key && isCompleted(agent.key) ? 'expand-open' : 'expand-closed'">
            <div class="px-3.5 pb-3.5">
              <div class="h-px w-full mb-3" :style="{ background: `linear-gradient(to right, transparent, ${agent.color}20, transparent)` }"></div>
              <p class="text-caption leading-relaxed" :class="isDark ? 'text-white/50' : 'text-slate-600'">{{ agentFindings[agent.key] || 'No details available' }}</p>
              <div v-if="agentTimings[agent.key]" class="mt-2 text-detail tabular-nums" :class="isDark ? 'text-white/25' : 'text-slate-400'">
                Completed in {{ agentTimings[agent.key].toFixed(2) }}s
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Progress bar -->
      <div class="mt-4 relative">
        <div class="h-1.5 rounded-full overflow-hidden" :class="isDark ? 'bg-white/[0.04]' : 'bg-slate-200'">
          <div
            class="h-full rounded-full transition-all duration-700 ease-out"
            :style="progressBarStyle"
          ></div>
        </div>
        <!-- Glow under progress bar (dark only) -->
        <div v-if="isDark" class="absolute top-0 left-0 h-1.5 rounded-full blur-sm transition-all duration-700"
          :style="{ width: progressPercent + '%', background: completedCount === agents.length ? '#22c55e40' : '#3b82f640' }"></div>
      </div>

      <!-- Footer stats -->
      <div class="mt-3 flex items-center justify-between text-detail">
        <span :class="isDark ? 'text-white/25' : 'text-slate-400'">Est. cost: <span class="font-semibold tabular-nums" :class="isDark ? 'text-white/40' : 'text-slate-500'">~${{ estimatedCost }}</span></span>
        <span :class="isDark ? 'text-white/20' : 'text-slate-400'">{{ currentModel }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  activeAgent: { type: String, default: null },
  completedAgents: { type: Array, default: () => [] },
  agentTimings: { type: Object, default: () => ({}) },
  agentFindings: { type: Object, default: () => ({}) },
  errors: { type: Object, default: () => ({}) }
})

const agents = [
  { key: 'triage', name: 'Triage Agent', icon: '\u{1F6A8}', color: '#3b82f6', activeLabel: 'Assessing urgency and red flags...' },
  { key: 'diagnostician', name: 'Diagnostician', icon: '\u{1FA7A}', color: '#8b5cf6', activeLabel: 'Generating differential diagnosis...' },
  { key: 'research', name: 'Research Agent', icon: '\u{1F4DA}', color: '#06b6d4', activeLabel: 'Searching clinical guidelines...' },
  { key: 'specialist', name: 'Specialist', icon: '\u{1F9D1}\u200D\u2695\uFE0F', color: '#6366f1', activeLabel: 'Deep specialty analysis...' },
  { key: 'treatment', name: 'Treatment Planner', icon: '\u{1F48A}', color: '#f59e0b', activeLabel: 'Creating treatment plan...' },
  { key: 'safety', name: 'Safety Reviewer', icon: '\u{1F6E1}\uFE0F', color: '#ef4444', activeLabel: 'Checking for safety concerns...' },
  { key: 'empathy', name: 'Empathy Agent', icon: '\u{1F49A}', color: '#ec4899', activeLabel: 'Writing patient-friendly summary...' }
]

// containerStyle removed — theme handled via :class and conditional :style in template

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

watch(() => props.activeAgent, (newAgent) => {
  if (liveTimerInterval) { clearInterval(liveTimerInterval); liveTimerInterval = null }
  if (newAgent) {
    liveTimerStart = Date.now()
    liveTimer.value = 0
    liveTimerInterval = setInterval(() => { liveTimer.value = (Date.now() - liveTimerStart) / 1000 }, 100)
  } else { liveTimer.value = 0 }
}, { immediate: true })

onUnmounted(() => { if (liveTimerInterval) clearInterval(liveTimerInterval) })

const completedCount = computed(() => props.completedAgents.length)

const progressPercent = computed(() => {
  const total = agents.length
  const done = props.completedAgents.length
  const activeBonus = props.activeAgent ? 0.5 : 0
  return Math.min(100, ((done + activeBonus) / total) * 100)
})

const progressBarStyle = computed(() => ({
  width: progressPercent.value + '%',
  background: completedCount.value === agents.length
    ? 'linear-gradient(90deg, #22c55e, #10b981)'
    : 'linear-gradient(90deg, #3b82f6, #8b5cf6)',
}))

function isActive(key) { return props.activeAgent === key }
function isCompleted(key) { return props.completedAgents.includes(key) }
function hasError(key) { return !!(props.errors && props.errors[key]) }
function toggleExpand(key) { expandedAgent.value = expandedAgent.value === key ? null : key }

function getRowClasses(agent) {
  if (hasError(agent.key)) return isDark.value ? 'border-red-500/25 bg-red-500/[0.04]' : 'border-red-300 bg-red-50'
  if (isActive(agent.key)) return isDark.value ? 'border-blue-500/30 bg-blue-500/[0.06] shadow-md shadow-blue-500/10' : 'border-blue-400 bg-blue-50 shadow-md shadow-blue-100'
  if (isCompleted(agent.key)) return isDark.value ? 'border-emerald-500/15 bg-emerald-500/[0.03]' : 'border-emerald-300 bg-emerald-50'
  return isDark.value ? 'border-white/[0.04] bg-white/[0.01]' : 'border-slate-200 bg-slate-50/50'
}

function energyRingStyle(color) {
  return {
    background: `conic-gradient(from var(--ring-angle, 0deg), transparent 0%, ${color}35 25%, transparent 50%, ${color}15 75%, transparent 100%)`,
    mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
    WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
    maskComposite: 'xor',
    WebkitMaskComposite: 'xor',
    padding: '1.5px',
  }
}
</script>

<style scoped>
.neural-drift {
  animation: drift 10s linear infinite;
}
.n1 { animation-delay: 0s; }
.n2 { animation-delay: -4s; }

@keyframes drift {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -40; }
}

.glow-pulse {
  animation: glowPulse 2s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.4); }
}

.energy-ring {
  animation: ringRotate 3s linear infinite;
}

@keyframes ringRotate {
  from { --ring-angle: 0deg; }
  to { --ring-angle: 360deg; }
}

@property --ring-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

/* Expand/collapse */
.expand-region {
  display: grid;
  transition: grid-template-rows 300ms cubic-bezier(0.4, 0, 0.2, 1), opacity 200ms ease;
}
.expand-closed { grid-template-rows: 0fr; opacity: 0; }
.expand-open { grid-template-rows: 1fr; opacity: 1; }
.expand-region > div { overflow: hidden; }
</style>
