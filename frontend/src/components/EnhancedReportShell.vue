<template>
  <div v-if="enabled" class="enhanced-report-shell">
    <!-- Summary bar -->
    <div
      class="summary-bar flex items-center justify-between px-5 py-3 rounded-xl mb-6"
      :class="isDark
        ? 'bg-slate-800/70 border border-slate-700/50'
        : 'bg-white border border-slate-200 shadow-sm'"
    >
      <div class="flex items-center gap-3 min-w-0">
        <span
          class="font-semibold truncate"
          :class="isDark ? 'text-white' : 'text-slate-900'"
        >{{ diagnosis || 'Diagnosis' }}</span>

        <span
          v-if="confidence != null"
          class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold"
          :class="confidenceClass"
        >{{ confidence }}%</span>

        <span
          v-if="urgency"
          class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide"
          :class="urgencyClass"
        >{{ urgency }}</span>

        <span
          v-if="specialty"
          class="text-xs px-2 py-0.5 rounded-full"
          :class="isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-100 text-slate-600'"
        >{{ specialty }}</span>
      </div>

      <div
        class="text-xs flex-shrink-0 ml-4"
        :class="isDark ? 'text-slate-400' : 'text-slate-500'"
      >
        Powered by {{ provider || 'AI' }}
      </div>
    </div>

    <!-- Main layout -->
    <div class="flex gap-6">
      <div class="flex-1 min-w-0">
        <slot></slot>
      </div>
      <aside v-if="$slots.sidebar" class="w-72 flex-shrink-0 hidden lg:block">
        <slot name="sidebar"></slot>
      </aside>
    </div>

    <!-- Footer slot -->
    <slot name="footer"></slot>
  </div>

  <!-- Fallback: just render content as-is when flag is off -->
  <template v-else>
    <slot></slot>
  </template>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getFlag } from '@/services/featureFlags.js'

const props = defineProps({
  diagnosis: { type: String, default: '' },
  confidence: { type: Number, default: null },
  urgency: { type: String, default: '' },
  provider: { type: String, default: '' },
  specialty: { type: String, default: '' },
})

const { isDark } = useTheme()

const enabled = computed(() => getFlag('enhancedUI'))

const confidenceClass = computed(() => {
  const c = props.confidence
  if (c == null) return ''
  if (c >= 80) return isDark.value
    ? 'bg-emerald-500/15 text-emerald-400'
    : 'bg-emerald-100 text-emerald-700'
  if (c >= 50) return isDark.value
    ? 'bg-amber-500/15 text-amber-400'
    : 'bg-amber-100 text-amber-700'
  return isDark.value
    ? 'bg-red-500/15 text-red-400'
    : 'bg-red-100 text-red-700'
})

const urgencyClass = computed(() => {
  const u = (props.urgency || '').toLowerCase()
  if (u === 'emergency' || u === 'critical')
    return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
  if (u === 'high' || u === 'urgent')
    return isDark.value ? 'bg-orange-500/15 text-orange-400' : 'bg-orange-100 text-orange-700'
  if (u === 'moderate' || u === 'medium')
    return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-700'
  return isDark.value ? 'bg-slate-700 text-slate-300' : 'bg-slate-100 text-slate-600'
})
</script>
