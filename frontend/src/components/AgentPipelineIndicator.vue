<template>
  <div class="agent-pipeline relative rounded-2xl overflow-hidden mx-4 my-3 border transition-colors"
    :class="isDark
      ? 'border-white/[0.06]'
      : 'border-slate-200 shadow-sm'"
    :style="{ background: isDark ? 'linear-gradient(145deg, #0a0f1c 0%, #070b16 50%, #05070d 100%)' : undefined }">
    <!-- Ambient background (dark only) -->
    <div v-if="isDark" class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute w-[300px] h-[300px] -top-[120px] -right-[80px] rounded-full blur-[100px] opacity-[0.05]"
        style="background: radial-gradient(circle, #8b5cf6, transparent)"></div>
      <div class="absolute w-[200px] h-[200px] -bottom-[60px] -left-[40px] rounded-full blur-[80px] opacity-[0.04]"
        style="background: radial-gradient(circle, #06b6d4, transparent)"></div>
      <svg class="absolute inset-0 w-full h-full opacity-[0.03]" xmlns="http://www.w3.org/2000/svg">
        <line x1="0%" y1="50%" x2="100%" y2="50%" stroke="#8b5cf6" stroke-width="0.5" stroke-dasharray="6 3" class="neural-flow" />
        <line x1="10%" y1="20%" x2="90%" y2="80%" stroke="#06b6d4" stroke-width="0.3" stroke-dasharray="4 4" class="neural-flow n2" />
      </svg>
    </div>

    <div class="relative z-10 px-5 py-4">
      <!-- Header -->
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-7 h-7 rounded-lg flex items-center justify-center border"
            :class="isDark
              ? 'bg-gradient-to-br from-violet-500/60 to-cyan-500/40 border-white/10'
              : 'bg-gradient-to-br from-violet-500 to-cyan-500 border-violet-300'">
            <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
          <span class="text-caption font-bold uppercase tracking-wider"
            :class="isDark ? 'text-white/80' : 'text-slate-700'">{{ t('pipeline.title') }}</span>
        </div>
        <div class="flex items-center gap-2">
          <span v-if="totalTime > 0" class="text-detail font-semibold tabular-nums"
            :class="isDark ? 'text-white/40' : 'text-slate-400'">{{ totalTime.toFixed(1) }}s</span>
          <span v-else class="flex items-center gap-1.5 text-detail font-semibold">
            <span class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></span>
            <span class="text-blue-500">{{ t('pipeline.processing') }}</span>
          </span>
        </div>
      </div>

      <!-- Pipeline flow -->
      <div class="grid grid-cols-4 sm:flex sm:flex-wrap items-stretch gap-1.5">
        <div
          v-for="(agent, idx) in agents"
          :key="agent.key"
          class="flex items-center sm:flex-1 sm:min-w-[110px]"
        >
          <!-- Agent node -->
          <div
            class="agent-node relative flex items-center gap-1.5 sm:gap-2.5 px-2 sm:px-3 py-2 sm:py-2.5 rounded-xl border transition-all duration-500 flex-1 overflow-hidden"
            :class="getNodeClasses(agent.key)"
          >
            <!-- Inner glow overlay (dark only) -->
            <div
              v-if="isActive(agent.key) && isDark"
              class="absolute inset-0 pointer-events-none"
              :style="{ background: `radial-gradient(ellipse at center, ${agent.color}15 0%, transparent 70%)` }"
            ></div>

            <!-- Energy ring for active (dark only) -->
            <div
              v-if="isActive(agent.key) && isDark"
              class="absolute inset-0 rounded-xl pointer-events-none energy-ring"
              :style="energyRingStyle(agent.color)"
            ></div>

            <!-- Status icon -->
            <div class="relative flex-shrink-0 w-5 h-5 sm:w-6 sm:h-6 flex items-center justify-center">
              <div
                v-if="(isActive(agent.key) || isCompleted(agent.key)) && isDark"
                class="absolute inset-0 rounded-full blur-md -z-10"
                :style="{ background: isCompleted(agent.key) ? '#22c55e20' : `${agent.color}30` }"
                :class="isActive(agent.key) ? 'glow-pulse' : ''"
              ></div>
              <!-- Completed -->
              <svg v-if="isCompleted(agent.key)" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-emerald-500" :class="isDark ? 'drop-shadow-[0_0_4px_rgba(34,197,94,0.5)]' : ''" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <!-- Active spinner -->
              <div v-else-if="isActive(agent.key)" class="w-4 h-4 sm:w-5 sm:h-5 rounded-full border-2 border-t-transparent animate-spin"
                :style="{ borderColor: `${agent.color}80`, borderTopColor: 'transparent' }"></div>
              <!-- Waiting -->
              <div v-else class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full"
                :class="isDark ? 'bg-white/[0.06] border border-white/[0.1]' : 'bg-slate-200 border border-slate-300'"></div>
            </div>

            <!-- Agent info -->
            <div class="relative min-w-0 flex-1">
              <div class="text-tiny sm:text-caption font-semibold truncate transition-colors duration-300"
                :class="getTextClass(agent.key)">
                {{ agent.name }}
              </div>
              <div class="hidden sm:block text-tiny truncate transition-colors duration-300"
                :class="getSubtextClass(agent.key)">
                <template v-if="isActive(agent.key)">{{ agent.activeLabel }}</template>
                <template v-else-if="isCompleted(agent.key) && agentTimings[agent.key]">
                  <span class="tabular-nums">{{ agentTimings[agent.key].toFixed(1) }}s</span>
                </template>
                <template v-else>{{ agent.waitLabel }}</template>
              </div>
            </div>
          </div>

          <!-- Connector -->
          <div v-if="idx < agents.length - 1" class="flex-shrink-0 mx-0.5 hidden sm:flex items-center">
            <svg class="w-3.5 h-3.5 transition-colors duration-500" fill="currentColor" viewBox="0 0 20 20"
              :class="isCompleted(agent.key) ? 'text-emerald-500' : (isDark ? 'text-white/10' : 'text-slate-300')">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'
const { isDark } = useTheme()
const { t } = useI18n()

const props = defineProps({
  activeAgent: { type: String, default: null },
  completedAgents: { type: Array, default: () => [] },
  agentTimings: { type: Object, default: () => ({}) },
  totalTime: { type: Number, default: 0 }
})

const agents = computed(() => [
  { key: 'triage', name: t('agent.triage'), color: '#3b82f6', activeLabel: t('pipeline.triageActive'), waitLabel: t('pipeline.pending') },
  { key: 'diagnostician', name: t('agent.diagnostician'), color: '#8b5cf6', activeLabel: t('pipeline.diagnosisActive'), waitLabel: t('pipeline.pending') },
  { key: 'research', name: t('agent.researcher'), color: '#06b6d4', activeLabel: t('pipeline.researchActive'), waitLabel: t('pipeline.pending') },
  { key: 'specialist', name: t('agent.specialist'), color: '#6366f1', activeLabel: t('pipeline.specialistActive'), waitLabel: t('pipeline.pending') },
  { key: 'treatment', name: t('agent.treatment'), color: '#f59e0b', activeLabel: t('pipeline.treatmentActive'), waitLabel: t('pipeline.pending') },
  { key: 'safety', name: t('agent.safety'), color: '#ef4444', activeLabel: t('pipeline.safetyActive'), waitLabel: t('pipeline.pending') },
  { key: 'empathy', name: t('agent.empathy'), color: '#ec4899', activeLabel: t('pipeline.empathyActive'), waitLabel: t('pipeline.pending') }
])

function isActive(key) { return props.activeAgent === key }
function isCompleted(key) { return props.completedAgents.includes(key) }

function getNodeClasses(key) {
  if (isActive(key)) {
    return isDark.value
      ? 'border-blue-500/50 bg-blue-500/[0.08] shadow-md shadow-blue-500/10'
      : 'border-blue-400 bg-blue-50 shadow-md shadow-blue-100'
  }
  if (isCompleted(key)) {
    return isDark.value
      ? 'border-emerald-500/20 bg-emerald-500/[0.04]'
      : 'border-emerald-300 bg-emerald-50'
  }
  return isDark.value
    ? 'border-white/[0.06] bg-white/[0.02]'
    : 'border-slate-200 bg-slate-50'
}

function getTextClass(key) {
  if (isActive(key)) return isDark.value ? 'text-white' : 'text-blue-700'
  if (isCompleted(key)) return isDark.value ? 'text-emerald-400/90' : 'text-emerald-700'
  return isDark.value ? 'text-white/30' : 'text-slate-400'
}

function getSubtextClass(key) {
  if (isActive(key)) return isDark.value ? 'text-white/50' : 'text-blue-500'
  if (isCompleted(key)) return isDark.value ? 'text-emerald-500/50' : 'text-emerald-600'
  return isDark.value ? 'text-white/15' : 'text-slate-400'
}

function energyRingStyle(color) {
  return {
    background: `conic-gradient(from var(--ring-angle, 0deg), transparent 0%, ${color}40 25%, transparent 50%, ${color}20 75%, transparent 100%)`,
    mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
    WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
    maskComposite: 'xor',
    WebkitMaskComposite: 'xor',
    padding: '1.5px',
  }
}
</script>

<style scoped>
.neural-flow {
  animation: neuralFlow 8s linear infinite;
}
.neural-flow.n2 { animation-delay: -3s; }

@keyframes neuralFlow {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -40; }
}

.glow-pulse {
  animation: glowPulse 2s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.3); }
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
</style>
