<template>
  <div :class="['inline-flex items-center justify-center rounded-full overflow-hidden', sizeClasses, colorClasses]">
    <img v-if="src && !imageError" :src="src" :alt="alt" class="w-full h-full object-cover" @error="imageError = true" />
    <span v-else-if="initials" :class="['font-medium', textSizeClasses]">{{ initials }}</span>
    <svg v-else class="text-gray-400" :class="iconSizeClasses" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
    </svg>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  src: { type: String, default: '' },
  alt: { type: String, default: '' },
  name: { type: String, default: '' },
  size: { type: String, default: 'md', validator: v => ['xs', 'sm', 'md', 'lg', 'xl'].includes(v) },
  color: { type: String, default: 'gray' }
})

const imageError = ref(false)

const initials = computed(() => {
  if (!props.name) return ''
  return props.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})

const sizeClasses = computed(() => {
  const sizes = { xs: 'w-6 h-6', sm: 'w-8 h-8', md: 'w-10 h-10', lg: 'w-12 h-12', xl: 'w-16 h-16' }
  return sizes[props.size]
})

const textSizeClasses = computed(() => {
  const sizes = { xs: 'text-xs', sm: 'text-xs', md: 'text-sm', lg: 'text-base', xl: 'text-lg' }
  return sizes[props.size]
})

const iconSizeClasses = computed(() => {
  const sizes = { xs: 'w-4 h-4', sm: 'w-5 h-5', md: 'w-6 h-6', lg: 'w-8 h-8', xl: 'w-10 h-10' }
  return sizes[props.size]
})

const colorClasses = computed(() => {
  const colors = {
    gray: 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-300',
    blue: 'bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300',
    green: 'bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-300',
    red: 'bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-300',
    yellow: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-600 dark:text-yellow-300',
    purple: 'bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-300'
  }
  return colors[props.color] || colors.gray
})
</script>
