<template>
  <div
    :class="[
      'flex gap-1 border-b',
      isDark ? 'border-slate-800' : 'border-slate-200'
    ]"
  >
    <button
      v-for="tab in tabs"
      :key="tab.key"
      :class="[
        'relative px-4 py-2.5 text-sm font-medium transition-colors whitespace-nowrap',
        modelValue === tab.key
          ? (isDark ? 'text-white' : 'text-slate-900')
          : (isDark ? 'text-slate-400 hover:text-slate-200' : 'text-slate-500 hover:text-slate-700')
      ]"
      @click="$emit('update:modelValue', tab.key)"
    >
      <span class="inline-flex items-center gap-2">
        {{ tab.label }}
        <span
          v-if="tab.count != null"
          :class="[
            'text-xs font-semibold px-1.5 py-0.5 rounded-full min-w-[20px] text-center',
            modelValue === tab.key
              ? (isDark ? 'bg-slate-700 text-slate-200' : 'bg-slate-200 text-slate-700')
              : (isDark ? 'bg-slate-800 text-slate-500' : 'bg-slate-100 text-slate-400')
          ]"
        >
          {{ tab.count }}
        </span>
      </span>

      <!-- Active underline -->
      <span
        v-if="modelValue === tab.key"
        :class="[
          'absolute bottom-0 left-0 right-0 h-0.5 rounded-t',
          isDark ? 'bg-blue-500' : 'bg-blue-600'
        ]"
      />
    </button>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

defineProps({
  tabs: {
    type: Array,
    required: true
  },
  modelValue: {
    type: String,
    required: true
  }
})

defineEmits(['update:modelValue'])
</script>
