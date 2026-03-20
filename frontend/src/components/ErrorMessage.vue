<template>
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="transform opacity-0 scale-95"
    enter-to-class="transform opacity-100 scale-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="transform opacity-100 scale-100"
    leave-to-class="transform opacity-0 scale-95"
  >
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
      <div class="rounded-lg shadow-xl max-w-md w-full" :class="isDark ? 'bg-gray-800' : 'bg-white'">
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b" :class="isDark ? 'border-gray-700' : 'border-gray-200'">
          <div class="flex items-center space-x-2">
            <div class="p-2 rounded-full" :class="iconClasses">
              <component :is="iconComponent" class="w-5 h-5" />
            </div>
            <h3 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-gray-900'">{{ title }}</h3>
          </div>
          <button
            @click="$emit('close')"
            class="transition-colors duration-200"
            :class="isDark ? 'text-gray-400 hover:text-white' : 'text-gray-400 hover:text-gray-700'"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Content -->
        <div class="p-4">
          <p class="leading-relaxed" :class="isDark ? 'text-gray-300' : 'text-gray-600'">{{ message }}</p>
          
          <!-- Additional details -->
          <div v-if="details" class="mt-3 p-3 bg-opacity-50 rounded-lg" :class="isDark ? 'bg-gray-700' : 'bg-gray-100'">
            <p class="text-sm" :class="isDark ? 'text-gray-400' : 'text-gray-500'">{{ details }}</p>
          </div>

          <!-- Error code -->
          <div v-if="errorCode" class="mt-3 text-xs" :class="isDark ? 'text-gray-500' : 'text-gray-400'">
            Error Code: {{ errorCode }}
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end space-x-3 p-4 border-t" :class="isDark ? 'border-gray-700' : 'border-gray-200'">
          <button
            v-if="showRetry"
            @click="$emit('retry')"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors duration-200"
          >
            Try Again
          </button>
          <button
            @click="$emit('close')"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
            :class="isDark ? 'bg-gray-600 hover:bg-gray-700 text-white' : 'bg-gray-200 hover:bg-gray-300 text-gray-700'"
          >
            {{ showRetry ? 'Cancel' : 'OK' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'error',
    validator: (value) => ['error', 'warning', 'info', 'success'].includes(value)
  },
  title: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    required: true
  },
  details: {
    type: String,
    default: ''
  },
  errorCode: {
    type: String,
    default: ''
  },
  showRetry: {
    type: Boolean,
    default: false
  },
  autoClose: {
    type: Boolean,
    default: false
  },
  autoCloseDelay: {
    type: Number,
    default: 5000
  }
})

const emit = defineEmits(['close', 'retry'])

// Computed properties for styling based on type
const iconClasses = computed(() => {
  switch (props.type) {
    case 'error':
      return 'bg-red-500 text-white'
    case 'warning':
      return 'bg-yellow-500 text-white'
    case 'success':
      return 'bg-green-500 text-white'
    case 'info':
    default:
      return 'bg-blue-500 text-white'
  }
})

const iconComponent = computed(() => {
  switch (props.type) {
    case 'error':
      return 'ExclamationTriangleIcon'
    case 'warning':
      return 'ExclamationTriangleIcon'
    case 'success':
      return 'CheckCircleIcon'
    case 'info':
    default:
      return 'InformationCircleIcon'
  }
})

const computedTitle = computed(() => {
  if (props.title) return props.title
  
  switch (props.type) {
    case 'error':
      return 'Error'
    case 'warning':
      return 'Warning'
    case 'success':
      return 'Success'
    case 'info':
    default:
      return 'Information'
  }
})

// Auto-close functionality
if (props.autoClose && props.visible) {
  setTimeout(() => {
    emit('close')
  }, props.autoCloseDelay)
}
</script>

<script>
// Define icon components
const ExclamationTriangleIcon = {
  name: 'ExclamationTriangleIcon',
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
    </svg>
  `
}

const CheckCircleIcon = {
  name: 'CheckCircleIcon',
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
}

const InformationCircleIcon = {
  name: 'InformationCircleIcon',
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
}

export default {
  components: {
    ExclamationTriangleIcon,
    CheckCircleIcon,
    InformationCircleIcon
  }
}
</script>
