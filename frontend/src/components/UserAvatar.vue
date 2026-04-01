<template>
  <div
    :class="[sizeClass, baseClass]"
    :title="name"
  >
    <img
      v-if="avatarUrl"
      :src="avatarUrl"
      :alt="name"
      class="w-full h-full object-cover rounded-full"
    />
    <span v-else :class="textClass">{{ initials }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '../composables/useTheme.js'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  name: {
    type: String,
    default: '',
  },
  avatarUrl: {
    type: String,
    default: '',
  },
})

const { isDark } = useTheme()

const initials = computed(() => {
  if (!props.name) return '?'
  return props.name
    .trim()
    .split(/\s+/)
    .map((w) => w[0])
    .filter(Boolean)
    .slice(0, 2)
    .join('')
    .toUpperCase()
})

const sizeClass = computed(() => {
  const map = {
    sm: 'w-7 h-7',
    md: 'w-9 h-9',
    lg: 'w-12 h-12',
  }
  return map[props.size] || map.md
})

const textClass = computed(() => {
  const map = {
    sm: 'text-detail',
    md: 'text-xs',
    lg: 'text-sm',
  }
  return map[props.size] || map.md
})

const baseClass = computed(() => {
  const common = 'rounded-full flex items-center justify-center overflow-hidden select-none font-semibold'
  if (props.avatarUrl) {
    return common
  }
  return `${common} bg-gradient-to-br from-blue-500 to-purple-600 text-white`
})
</script>
