<template>
  <button
    type="button"
    role="switch"
    :aria-checked="modelValue"
    :disabled="disabled"
    :class="[
      'relative inline-flex flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
      modelValue ? 'bg-blue-600' : 'bg-gray-200 dark:bg-gray-600',
      sizeClasses,
      { 'opacity-50 cursor-not-allowed': disabled }
    ]"
    @click="toggle"
  >
    <span
      :class="[
        'pointer-events-none inline-block transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
        modelValue ? translateClasses : 'translate-x-0',
        dotSizeClasses
      ]"
    />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  size: { type: String, default: 'md' }
})

const emit = defineEmits(['update:modelValue'])

function toggle() {
  if (!props.disabled) {
    emit('update:modelValue', !props.modelValue)
  }
}

const sizeClasses = computed(() => {
  const sizes = { sm: 'h-5 w-9', md: 'h-6 w-11', lg: 'h-7 w-14' }
  return sizes[props.size]
})

const dotSizeClasses = computed(() => {
  const sizes = { sm: 'h-4 w-4', md: 'h-5 w-5', lg: 'h-6 w-6' }
  return sizes[props.size]
})

const translateClasses = computed(() => {
  const translates = { sm: 'translate-x-4', md: 'translate-x-5', lg: 'translate-x-7' }
  return translates[props.size]
})
</script>
