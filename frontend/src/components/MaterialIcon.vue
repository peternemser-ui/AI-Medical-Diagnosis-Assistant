<template>
  <span class="material-symbols-outlined" :class="sizeClass" :style="customStyle">
    {{ icon }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'md' // xs, sm, md, lg, xl, 2xl, 3xl
  },
  fill: {
    type: Boolean,
    default: false
  },
  weight: {
    type: Number,
    default: 400,
    validator: (value) => value >= 100 && value <= 700
  }
})

const sizeClass = computed(() => {
  const sizes = {
    'xs': 'text-xs',
    'sm': 'text-sm',
    'md': 'text-base',
    'lg': 'text-lg',
    'xl': 'text-xl',
    '2xl': 'text-2xl',
    '3xl': 'text-3xl'
  }
  return sizes[props.size] || sizes.md
})

const customStyle = computed(() => ({
  fontVariationSettings: `'FILL' ${props.fill ? 1 : 0}, 'wght' ${props.weight}`
}))
</script>

<style scoped>
.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  user-select: none;
}
</style>
