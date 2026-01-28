<template>
  <label class="inline-flex items-start cursor-pointer" :class="{ 'opacity-50 cursor-not-allowed': disabled }">
    <input
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      :class="[
        'rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500 dark:bg-gray-700',
        sizeClasses
      ]"
      @change="$emit('update:modelValue', $event.target.checked)"
    />
    <span v-if="label || $slots.default" :class="['ml-2 text-gray-700 dark:text-gray-300', labelSizeClasses]">
      <slot>{{ label }}</slot>
    </span>
  </label>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  label: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  size: { type: String, default: 'md' }
})

defineEmits(['update:modelValue'])

const sizeClasses = computed(() => {
  const sizes = { sm: 'w-3.5 h-3.5', md: 'w-4 h-4', lg: 'w-5 h-5' }
  return sizes[props.size]
})

const labelSizeClasses = computed(() => {
  const sizes = { sm: 'text-xs', md: 'text-sm', lg: 'text-base' }
  return sizes[props.size]
})
</script>
