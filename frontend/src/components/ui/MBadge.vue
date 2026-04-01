<template>
  <span :class="['badge', variantClass, sizeClass]">
    <span v-if="dot" class="w-1.5 h-1.5 rounded-full" :class="dotColor"></span>
    <slot />
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'neutral',
    validator: v => ['success', 'warning', 'danger', 'info', 'neutral', 'purple', 'brand',
                      'routine', 'moderate', 'urgent', 'emergency'].includes(v),
  },
  size: { type: String, default: 'md', validator: v => ['sm', 'md'].includes(v) },
  dot: Boolean,
})

const variantClass = computed(() => `badge-${props.variant}`)

const sizeClass = computed(() => props.size === 'sm' ? 'text-micro px-1.5 py-px' : '')

const dotColors = {
  success: 'bg-emerald-500', warning: 'bg-amber-500', danger: 'bg-red-500',
  info: 'bg-blue-500', neutral: 'bg-slate-500', purple: 'bg-purple-500',
  brand: 'bg-brand-500', routine: 'bg-emerald-500', moderate: 'bg-amber-500',
  urgent: 'bg-orange-500', emergency: 'bg-red-500',
}

const dotColor = computed(() => dotColors[props.variant] || 'bg-slate-500')
</script>
