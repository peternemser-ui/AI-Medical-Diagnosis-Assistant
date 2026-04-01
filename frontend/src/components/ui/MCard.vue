<template>
  <component
    :is="tag"
    :class="[
      'rounded-card transition-colors duration-200',
      variants[variant],
      interactive && 'cursor-pointer',
      interactive && (isDark
        ? 'hover:border-slate-600 hover:shadow-elevated-dark'
        : 'hover:border-slate-300 hover:shadow-elevated'),
      padding && paddingSizes[padding],
      $attrs.class,
    ]"
  >
    <slot />
  </component>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

defineProps({
  variant: {
    type: String,
    default: 'default',
    validator: v => ['default', 'elevated', 'soft', 'clinical', 'ghost'].includes(v),
  },
  padding: {
    type: String,
    default: 'md',
    validator: v => ['none', 'sm', 'md', 'lg'].includes(v),
  },
  interactive: Boolean,
  tag: { type: String, default: 'div' },
})

const variants = {
  default:  'surface-card',
  elevated: 'surface-elevated',
  soft:     'surface-soft',
  clinical: 'card-clinical',
  ghost:    'border border-transparent',
}

const paddingSizes = {
  none: '',
  sm:   'p-3',
  md:   'p-card-px',
  lg:   'p-6',
}
</script>
