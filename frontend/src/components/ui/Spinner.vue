<template>
  <div
    :class="[
      'inline-block animate-spin rounded-full border-solid border-current border-r-transparent motion-reduce:animate-[spin_1.5s_linear_infinite]',
      sizeClasses,
      colorClasses
    ]"
    role="status"
    :aria-label="label"
  >
    <span class="sr-only">{{ label }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'white', 'gray', 'success', 'danger'].includes(value)
  },
  label: {
    type: String,
    default: 'Loading...'
  }
})

const sizeClasses = computed(() => {
  const sizes = {
    xs: 'w-3 h-3 border',
    sm: 'w-4 h-4 border-2',
    md: 'w-6 h-6 border-2',
    lg: 'w-8 h-8 border-[3px]',
    xl: 'w-12 h-12 border-4'
  }
  return sizes[props.size]
})

const colorClasses = computed(() => {
  const colors = {
    primary: 'text-blue-600',
    white: 'text-white',
    gray: 'text-gray-400',
    success: 'text-green-600',
    danger: 'text-red-600'
  }
  return colors[props.color]
})
</script>
