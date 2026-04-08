<template>
  <div class="relative">
    <!-- Search icon -->
    <svg
      xmlns="http://www.w3.org/2000/svg"
      :class="[
        'absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none',
        isDark ? 'text-slate-500' : 'text-slate-400'
      ]"
      viewBox="0 0 20 20"
      fill="currentColor"
    >
      <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
    </svg>

    <!-- Input -->
    <input
      ref="inputRef"
      :value="localValue"
      type="text"
      :placeholder="placeholder"
      :class="[
        'w-full pl-9 pr-8 py-2 text-sm rounded-lg border outline-none transition-colors',
        isDark
          ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:border-slate-600'
          : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400 focus:border-slate-400'
      ]"
      @input="onInput"
    />

    <!-- Clear button -->
    <button
      v-if="localValue"
      :class="[
        'absolute right-2 top-1/2 -translate-y-1/2 p-0.5 rounded transition-colors',
        isDark
          ? 'text-slate-500 hover:text-slate-300 hover:bg-slate-700'
          : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'
      ]"
      @click="clear"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Search...'
  },
  debounceMs: {
    type: Number,
    default: 300
  }
})

const emit = defineEmits(['update:modelValue'])

const localValue = ref(props.modelValue)
const inputRef = ref(null)
let timer = null

watch(() => props.modelValue, (v) => {
  localValue.value = v
})

function onInput(e) {
  localValue.value = e.target.value
  clearTimeout(timer)
  timer = setTimeout(() => {
    emit('update:modelValue', localValue.value)
  }, props.debounceMs)
}

function clear() {
  localValue.value = ''
  clearTimeout(timer)
  emit('update:modelValue', '')
  inputRef.value?.focus()
}

onBeforeUnmount(() => {
  clearTimeout(timer)
})
</script>
