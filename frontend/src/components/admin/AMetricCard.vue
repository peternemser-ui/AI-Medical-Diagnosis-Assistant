<template>
  <div
    :class="[
      'rounded-2xl border p-5 relative overflow-hidden',
      isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200'
    ]"
  >
    <!-- Icon top-left -->
    <div class="flex items-start justify-between mb-3">
      <div
        v-if="$slots.icon"
        :class="[
          'w-10 h-10 rounded-xl flex items-center justify-center',
          isDark ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-600'
        ]"
      >
        <slot name="icon" />
      </div>

      <!-- Trend badge top-right -->
      <span
        v-if="trend !== undefined && trend !== null"
        :class="[
          'inline-flex items-center gap-0.5 text-xs font-semibold px-2 py-0.5 rounded-full',
          trend >= 0
            ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600')
            : (isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600')
        ]"
      >
        <svg
          v-if="trend >= 0"
          xmlns="http://www.w3.org/2000/svg"
          class="w-3 h-3"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path fill-rule="evenodd" d="M5.293 9.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L11 7.414V15a1 1 0 11-2 0V7.414L6.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="w-3 h-3"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path fill-rule="evenodd" d="M14.707 10.293a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 111.414-1.414L9 12.586V5a1 1 0 012 0v7.586l2.293-2.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
        {{ Math.abs(trend) }}%
      </span>
    </div>

    <!-- Value -->
    <div
      :class="[
        'text-3xl font-bold tracking-tight',
        isDark ? 'text-white' : 'text-slate-900'
      ]"
    >
      {{ value }}
    </div>

    <!-- Label -->
    <div
      :class="[
        'text-sm mt-1',
        isDark ? 'text-slate-400' : 'text-slate-500'
      ]"
    >
      {{ label }}
    </div>

    <!-- Sublabel -->
    <div
      v-if="sublabel"
      :class="[
        'text-xs mt-0.5',
        isDark ? 'text-slate-500' : 'text-slate-400'
      ]"
    >
      {{ sublabel }}
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  trend: {
    type: Number,
    default: null
  },
  sublabel: {
    type: String,
    default: ''
  }
})
</script>
