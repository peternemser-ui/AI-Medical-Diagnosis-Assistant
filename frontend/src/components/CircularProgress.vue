<template>
  <div class="circular-progress" :style="{ width: size + 'px', height: size + 'px' }">
    <svg 
      :width="size" 
      :height="size" 
      :viewBox="`0 0 ${size} ${size}`"
      class="transform -rotate-90"
    >
      <!-- Background Circle -->
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        :stroke="backgroundColor"
        :stroke-width="strokeWidth"
        fill="transparent"
        class="transition-all duration-300"
      />
      
      <!-- Progress Circle -->
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        :stroke="color"
        :stroke-width="strokeWidth"
        fill="transparent"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="strokeDashoffset"
        :stroke-linecap="linecap"
        class="transition-all duration-1000 ease-in-out"
        :style="{ filter: glowEffect }"
      />
      
      <!-- Animated dots for enhanced visual appeal -->
      <circle
        v-if="showDots"
        :cx="size / 2 + radius * Math.cos(dotAngle)"
        :cy="size / 2 + radius * Math.sin(dotAngle)"
        :r="strokeWidth / 3"
        :fill="color"
        class="transition-all duration-1000"
      >
        <animateTransform
          attributeName="transform"
          attributeType="XML"
          type="rotate"
          :values="`0 ${size/2} ${size/2}; ${360 * (percentage / 100)} ${size/2} ${size/2}`"
          dur="1s"
          repeatCount="1"
        />
      </circle>
    </svg>
    
    <!-- Slot for custom content inside the circle -->
    <div v-if="$slots.default" class="absolute inset-0 flex items-center justify-center">
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const props = defineProps({
  percentage: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0 && value <= 100
  },
  size: {
    type: Number,
    default: 120
  },
  strokeWidth: {
    type: Number,
    default: 8
  },
  color: {
    type: String,
    default: '#3b82f6'
  },
  backgroundColor: {
    type: String,
    default: '#e5e7eb'
  },
  linecap: {
    type: String,
    default: 'round',
    validator: (value) => ['butt', 'round', 'square'].includes(value)
  },
  animated: {
    type: Boolean,
    default: true
  },
  showDots: {
    type: Boolean,
    default: false
  },
  glow: {
    type: Boolean,
    default: true
  }
})

const animatedPercentage = ref(0)

const radius = computed(() => (props.size - props.strokeWidth) / 2)
const circumference = computed(() => radius.value * 2 * Math.PI)

const strokeDashoffset = computed(() => {
  const percentage = props.animated ? animatedPercentage.value : props.percentage
  return circumference.value - (percentage / 100) * circumference.value
})

const dotAngle = computed(() => {
  const percentage = props.animated ? animatedPercentage.value : props.percentage
  return (percentage / 100) * 2 * Math.PI - Math.PI / 2
})

const glowEffect = computed(() => {
  if (!props.glow) return 'none'
  return `drop-shadow(0 0 6px ${props.color}40)`
})

// Animate percentage on mount
onMounted(() => {
  if (props.animated) {
    const duration = 1000 // 1 second
    const steps = 60 // 60fps
    const increment = props.percentage / steps
    const interval = duration / steps
    
    let current = 0
    const timer = setInterval(() => {
      current += increment
      if (current >= props.percentage) {
        current = props.percentage
        clearInterval(timer)
      }
      animatedPercentage.value = current
    }, interval)
  } else {
    animatedPercentage.value = props.percentage
  }
})
</script>

<style scoped>
.circular-progress {
  position: relative;
  display: inline-block;
}

svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

circle {
  transition: stroke-dashoffset 0.3s ease-in-out;
}
</style>
