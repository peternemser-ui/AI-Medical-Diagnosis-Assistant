<template>
  <div class="dial-chart-container" :style="{ width: size + 'px', height: size + 'px' }">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
      <!-- Background arc -->
      <path
        :d="backgroundArc"
        fill="none"
        :stroke="backgroundColor"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
      />
      
      <!-- Value arc -->
      <path
        :d="valueArc"
        fill="none"
        :stroke="color"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        class="value-arc"
      />
      
      <!-- Center text - 30% smaller and perfectly centered -->
      <text
        :x="size / 2"
        :y="size / 2"
        text-anchor="middle"
        dominant-baseline="central"
        :font-size="size * 0.175"
        font-weight="bold"
        :fill="color"
        class="value-text"
      >
        {{ value }}%
      </text>
      
      <!-- Label text - hidden as we show it outside the circle now -->
      <text
        v-if="label"
        :x="size / 2"
        :y="size / 2 + 25"
        text-anchor="middle"
        :font-size="size * 0.056"
        fill="#9CA3AF"
        class="label-text"
      >
        {{ label }}
      </text>
    </svg>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    required: true,
    default: 0
  },
  label: {
    type: String,
    default: ''
  },
  color: {
    type: String,
    default: '#3B82F6'
  },
  backgroundColor: {
    type: String,
    default: '#1F2937'
  },
  size: {
    type: Number,
    default: 200
  },
  strokeWidth: {
    type: Number,
    default: 20
  }
})

// Calculate arc paths
const radius = computed(() => (props.size - props.strokeWidth) / 2)
const centerX = computed(() => props.size / 2)
const centerY = computed(() => props.size / 2)

// Start angle (bottom left) and end angle (bottom right) for a gauge
const startAngle = computed(() => (3 / 4) * Math.PI) // 135 degrees
const endAngle = computed(() => (9 / 4) * Math.PI)   // 405 degrees (270 degree arc)

// Helper function to convert polar to cartesian coordinates
const polarToCartesian = (angle) => {
  return {
    x: centerX.value + radius.value * Math.cos(angle),
    y: centerY.value + radius.value * Math.sin(angle)
  }
}

// Background arc (full gauge)
const backgroundArc = computed(() => {
  const start = polarToCartesian(startAngle.value)
  const end = polarToCartesian(endAngle.value)
  
  return `M ${start.x} ${start.y} A ${radius.value} ${radius.value} 0 1 1 ${end.x} ${end.y}`
})

// Value arc (filled portion based on percentage)
const valueArc = computed(() => {
  if (props.value <= 0) {
    return '' // No arc if value is 0
  }
  
  const totalAngle = endAngle.value - startAngle.value // 1.5 * PI (270 degrees)
  const valueAngle = startAngle.value + (totalAngle * props.value / 100)
  
  const start = polarToCartesian(startAngle.value)
  const end = polarToCartesian(valueAngle)
  
  // Calculate if we need the large arc flag
  // Large arc flag should be 1 if the arc is more than 180 degrees
  const arcAngle = totalAngle * props.value / 100
  const largeArcFlag = arcAngle > Math.PI ? 1 : 0
  
  return `M ${start.x} ${start.y} A ${radius.value} ${radius.value} 0 ${largeArcFlag} 1 ${end.x} ${end.y}`
})
</script>

<style scoped>
.dial-chart-container {
  display: inline-block;
}

.value-arc {
  transition: stroke-dasharray 0.5s ease-out;
}

.value-text {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.label-text {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
</style>
