<template>
  <span
    :class="[
      'inline-flex items-center font-medium rounded-full',
      variantClasses,
      sizeClasses
    ]"
  >
    <!-- Dot indicator -->
    <span
      v-if="dot"
      :class="[
        'rounded-full mr-1.5',
        dotClasses
      ]"
    />

    <!-- Icon (left) -->
    <component
      v-if="icon && iconPosition === 'left'"
      :is="icon"
      :class="['mr-1', iconSizeClasses]"
    />

    <!-- Content -->
    <slot>{{ label }}</slot>

    <!-- Icon (right) -->
    <component
      v-if="icon && iconPosition === 'right'"
      :is="icon"
      :class="['ml-1', iconSizeClasses]"
    />

    <!-- Remove button -->
    <button
      v-if="removable"
      type="button"
      @click="$emit('remove')"
      :class="[
        'ml-1 hover:opacity-75 focus:outline-none',
        removeButtonClasses
      ]"
      aria-label="Remove"
    >
      <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'primary', 'success', 'warning', 'danger', 'info'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  dot: {
    type: Boolean,
    default: false
  },
  icon: {
    type: [Object, Function],
    default: null
  },
  iconPosition: {
    type: String,
    default: 'left'
  },
  removable: {
    type: Boolean,
    default: false
  }
})

defineEmits(['remove'])

const variantClasses = computed(() => {
  const variants = {
    default: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    primary: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    success: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    danger: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    info: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400'
  }
  return variants[props.variant]
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-sm',
    lg: 'px-3 py-1 text-sm'
  }
  return sizes[props.size]
})

const dotClasses = computed(() => {
  const sizes = {
    sm: 'w-1.5 h-1.5',
    md: 'w-2 h-2',
    lg: 'w-2.5 h-2.5'
  }
  const colors = {
    default: 'bg-gray-500',
    primary: 'bg-blue-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    danger: 'bg-red-500',
    info: 'bg-purple-500'
  }
  return `${sizes[props.size]} ${colors[props.variant]}`
})

const iconSizeClasses = computed(() => {
  const sizes = {
    sm: 'w-3 h-3',
    md: 'w-3.5 h-3.5',
    lg: 'w-4 h-4'
  }
  return sizes[props.size]
})

const removeButtonClasses = computed(() => {
  return 'rounded-full'
})
</script>
