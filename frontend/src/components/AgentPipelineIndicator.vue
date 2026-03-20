<template>
  <div class="agent-pipeline px-4 py-3">
    <div class="flex items-center justify-between mb-2">
      <span class="text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">7-Agent Analysis Pipeline</span>
      <span v-if="totalTime > 0" class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ totalTime.toFixed(1) }}s</span>
      <span v-else class="text-xs text-blue-500 animate-pulse">Processing...</span>
    </div>

    <div class="grid grid-cols-4 sm:flex sm:flex-wrap items-center gap-1">
      <div
        v-for="(agent, idx) in agents"
        :key="agent.key"
        class="flex items-center"
        :class="{ 'sm:flex-1 sm:min-w-[100px]': true }"
      >
        <!-- Agent node -->
        <div
          class="relative flex items-center gap-1 sm:gap-2 px-1.5 sm:px-3 py-1.5 sm:py-2 rounded-lg border transition-all duration-500 flex-1"
          :class="getNodeClasses(agent.key)"
        >
          <!-- Status icon -->
          <div class="flex-shrink-0 w-4 h-4 sm:w-5 sm:h-5 flex items-center justify-center">
            <!-- Completed -->
            <svg v-if="isCompleted(agent.key)" class="w-3 h-3 sm:w-4 sm:h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
            </svg>
            <!-- Active spinner -->
            <div v-else-if="isActive(agent.key)" class="w-3 h-3 sm:w-4 sm:h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
            <!-- Waiting -->
            <div v-else class="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full" :class="isDark ? 'bg-slate-600' : 'bg-slate-300'"></div>
          </div>

          <!-- Agent info -->
          <div class="min-w-0 flex-1">
            <div class="text-[9px] sm:text-xs font-medium truncate" :class="getTextClass(agent.key)">
              {{ agent.name }}
            </div>
            <div class="hidden sm:block text-[10px] truncate" :class="getSubtextClass(agent.key)">
              <template v-if="isActive(agent.key)">{{ agent.activeLabel }}</template>
              <template v-else-if="isCompleted(agent.key) && agentTimings[agent.key]">{{ agentTimings[agent.key].toFixed(1) }}s</template>
              <template v-else>{{ agent.waitLabel }}</template>
            </div>
          </div>
        </div>

        <!-- Connector arrow -->
        <div v-if="idx < agents.length - 1" class="flex-shrink-0 mx-0.5 hidden sm:block">
          <svg class="w-3 h-3" :class="isCompleted(agent.key) ? 'text-emerald-500' : (isDark ? 'text-slate-700' : 'text-slate-300')" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme.js'
const { isDark } = useTheme()

const props = defineProps({
  activeAgent: { type: String, default: null },
  completedAgents: { type: Array, default: () => [] },
  agentTimings: { type: Object, default: () => ({}) },
  totalTime: { type: Number, default: 0 }
})

const agents = [
  { key: 'triage', name: 'Triage', activeLabel: 'Assessing urgency...', waitLabel: 'Pending' },
  { key: 'diagnostician', name: 'Diagnosis', activeLabel: 'Analyzing symptoms...', waitLabel: 'Pending' },
  { key: 'research', name: 'Research', activeLabel: 'Checking evidence...', waitLabel: 'Pending' },
  { key: 'specialist', name: 'Specialist', activeLabel: 'Deep analysis...', waitLabel: 'Pending' },
  { key: 'treatment', name: 'Treatment', activeLabel: 'Planning care...', waitLabel: 'Pending' },
  { key: 'safety', name: 'Safety', activeLabel: 'Safety review...', waitLabel: 'Pending' },
  { key: 'empathy', name: 'Summary', activeLabel: 'Writing summary...', waitLabel: 'Pending' }
]

function isActive(key) {
  return props.activeAgent === key
}

function isCompleted(key) {
  return props.completedAgents.includes(key)
}

function getNodeClasses(key) {
  if (isActive(key)) return isDark.value ? 'border-blue-500/60 bg-blue-500/10 shadow-md shadow-blue-500/10' : 'border-blue-400 bg-blue-50 shadow-md shadow-blue-100'
  if (isCompleted(key)) return isDark.value ? 'border-emerald-500/40 bg-emerald-500/5' : 'border-emerald-300 bg-emerald-50'
  return isDark.value ? 'border-slate-700/50 bg-slate-800/30' : 'border-slate-200 bg-slate-50'
}

function getTextClass(key) {
  if (isActive(key)) return isDark.value ? 'text-blue-300' : 'text-blue-700'
  if (isCompleted(key)) return isDark.value ? 'text-emerald-300' : 'text-emerald-700'
  return isDark.value ? 'text-slate-500' : 'text-slate-400'
}

function getSubtextClass(key) {
  if (isActive(key)) return isDark.value ? 'text-blue-400/70' : 'text-blue-600'
  if (isCompleted(key)) return isDark.value ? 'text-emerald-500/60' : 'text-emerald-600'
  return isDark.value ? 'text-slate-600' : 'text-slate-400'
}
</script>
