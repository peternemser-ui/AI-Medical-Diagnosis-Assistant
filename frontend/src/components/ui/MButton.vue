<template>
  <component
    :is="tag"
    :class="[
      variantClasses[variant],
      sizes[size],
      loading && 'pointer-events-none opacity-70',
    ]"
    :disabled="disabled || loading"
  >
    <svg v-if="loading" class="animate-spin w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
    <slot />
  </component>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: v => ['primary', 'blue', 'secondary', 'ghost', 'danger', 'icon'].includes(v),
  },
  size: { type: String, default: 'md', validator: v => ['sm', 'md', 'lg'].includes(v) },
  tag: { type: String, default: 'button' },
  disabled: Boolean,
  loading: Boolean,
})

const variantClasses = {
  primary:   'btn-primary',
  blue:      'btn-blue',
  secondary: 'btn-secondary',
  ghost:     'btn-ghost',
  danger:    'btn-danger',
  icon:      'btn-icon',
}

const sizes = {
  sm: 'btn-sm',
  md: '',
  lg: 'btn-lg',
}
</script>
