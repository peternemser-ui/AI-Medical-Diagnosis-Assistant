<template>
  <div v-if="visible" class="flex flex-wrap gap-1.5 px-2">
    <button
      v-for="chip in chips"
      :key="chip"
      @click="$emit('select', chip)"
      class="text-xs px-3 py-1.5 rounded-full border transition-all duration-150 hover:-translate-y-0.5"
      :class="isDark
        ? 'bg-slate-800/60 border-slate-700/50 text-slate-300 hover:bg-blue-500/15 hover:border-blue-500/30 hover:text-blue-300'
        : 'bg-white border-slate-200 text-slate-600 hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700 shadow-sm'"
    >
      {{ chip }}
    </button>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'

const { isDark } = useTheme()
const { lang } = useI18n()

defineProps({
  visible: { type: Boolean, default: true }
})

defineEmits(['select'])

const chips = [
  'Headache', 'Chest pain', 'Fatigue', 'Fever',
  'Back pain', 'Cough', 'Nausea', 'Skin rash',
  'Dizziness', 'Joint pain'
]
</script>
