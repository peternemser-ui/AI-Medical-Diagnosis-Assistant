<template>
  <div
    :class="[
      'bg-white dark:bg-gray-800 rounded-xl overflow-hidden',
      shadow && shadowClasses,
      bordered && 'border border-gray-200 dark:border-gray-700',
      hoverable && 'hover:shadow-lg transition-shadow cursor-pointer',
      padding && paddingClasses
    ]"
  >
    <!-- Header -->
    <div
      v-if="$slots.header || title"
      :class="[
        'border-b border-gray-200 dark:border-gray-700',
        headerPadding
      ]"
    >
      <slot name="header">
        <div class="flex items-center justify-between">
          <div>
            <h3 v-if="title" class="text-lg font-semibold text-gray-900 dark:text-white">
              {{ title }}
            </h3>
            <p v-if="subtitle" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {{ subtitle }}
            </p>
          </div>
          <slot name="header-actions" />
        </div>
      </slot>
    </div>

    <!-- Body -->
    <div :class="bodyPadding">
      <slot />
    </div>

    <!-- Footer -->
    <div
      v-if="$slots.footer"
      :class="[
        'border-t border-gray-200 dark:border-gray-700',
        footerPadding
      ]"
    >
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  subtitle: {
    type: String,
    default: ''
  },
  shadow: {
    type: [Boolean, String],
    default: 'md',
    validator: (value) => typeof value === 'boolean' || ['sm', 'md', 'lg', 'xl', 'none'].includes(value)
  },
  bordered: {
    type: Boolean,
    default: false
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  padding: {
    type: [Boolean, String],
    default: true
  }
})

const shadowClasses = computed(() => {
  if (props.shadow === false || props.shadow === 'none') return ''
  const shadows = {
    sm: 'shadow-sm',
    md: 'shadow',
    lg: 'shadow-lg',
    xl: 'shadow-xl'
  }
  return props.shadow === true ? 'shadow' : shadows[props.shadow]
})

const paddingClasses = computed(() => {
  if (props.padding === false) return ''
  const paddings = {
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6'
  }
  return props.padding === true ? '' : paddings[props.padding]
})

const headerPadding = computed(() => {
  return props.padding === false ? 'p-4' : 'px-4 py-3'
})

const bodyPadding = computed(() => {
  if (props.padding === false) return ''
  if (props.padding === true) return 'p-4'
  const paddings = { sm: 'p-3', md: 'p-4', lg: 'p-6' }
  return paddings[props.padding] || 'p-4'
})

const footerPadding = computed(() => {
  return props.padding === false ? 'p-4' : 'px-4 py-3'
})
</script>
