<template>
  <div v-if="visible" class="p-3 shadow-lg progress-indicator-bar premium-progress-container" 
    :style="{
      background: 'var(--progress-bg)',
      borderBottom: '1px solid var(--border-accent)',
      boxShadow: 'var(--shadow-lg)',
      backdropFilter: 'var(--glass-backdrop)',
      borderRadius: '0 0 16px 16px'
    }"
  >
    <div class="max-w-4xl mx-auto">
      <!-- Premium progress header - High contrast dark mode -->
      <div class="flex items-center justify-between mb-3">
        <h3 
          class="text-sm font-bold tracking-wide premium-progress-title"
          :style="{ 
            color: '#ffffff',
            fontSize: '14px',
            fontWeight: '700',
            letterSpacing: '0.5px'
          }"
        >
          {{ title }}
        </h3>
        <span 
          class="text-xs premium-percentage"
          :style="{ 
            color: '#22d3ee',
            fontSize: '12px',
            fontWeight: '600',
            background: 'rgba(34, 211, 238, 0.1)',
            padding: '4px 8px',
            borderRadius: '8px',
            border: '1px solid #22d3ee'
          }"
        >
          {{ Math.round(progress) }}% Complete
        </span>
      </div>
      
      <!-- Premium progress bar - High contrast dark mode -->
      <div 
        class="w-full rounded-full h-3 mb-3 premium-progress-track"
        :style="{ 
          background: '#334155',
          border: '1px solid #475569',
          boxShadow: 'inset 0 2px 4px rgba(0, 0, 0, 0.3)',
          height: '12px'
        }"
      >
        <div
          class="h-full rounded-full transition-all duration-700 ease-out premium-progress-fill"
          :style="{ 
            background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 50%, #0e7490 100%)',
            width: progress + '%',
            boxShadow: '0 4px 14px rgba(6, 182, 212, 0.3)',
            borderRadius: '6px'
          }"
        ></div>
      </div>
      
      <!-- Step indicators -->
      <div v-if="steps.length > 0" class="flex justify-between items-center">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="flex items-center text-xs"
        >
          <div class="flex items-center">
            <!-- Step icon -->
            <div class="w-4 h-4 mr-1 flex items-center justify-center">
              <!-- Completed step -->
              <svg v-if="currentStep > index" class="w-3 h-3" style="color: var(--primary) !important;" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <!-- Current step -->
              <div v-else-if="currentStep === index" class="w-2 h-2 rounded-full animate-pulse" style="background-color: var(--warning) !important;"></div>
              <!-- Future step -->
              <div v-else class="w-2 h-2 rounded-full" style="background-color: #94a3b8 !important;"></div>
            </div>
            <span
              class="hidden sm:inline premium-step-label"
              :style="{
                color: currentStep > index ? '#22d3ee' : currentStep === index ? '#f59e0b' : '#94a3b8',
                fontSize: '11px',
                fontWeight: '500'
              }"
            >{{ step }}</span>
          </div>
        </div>
      </div>
      
      <!-- Progress message -->
      <p v-if="message" class="text-xs mt-1" style="color: var(--text-accent) !important;">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  progress: {
    type: Number,
    default: 0,
    validator: (value) => value >= 0 && value <= 100
  },
  title: {
    type: String,
    default: 'Processing...'
  },
  message: {
    type: String,
    default: 'Please wait while we process your request.'
  },
  steps: {
    type: Array,
    default: () => []
  },
  currentStep: {
    type: Number,
    default: 0
  },
  estimatedTime: {
    type: String,
    default: ''
  },
  showCancel: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['cancel'])

// Computed properties for progress circle
const circumference = computed(() => 2 * Math.PI * 40) // radius = 40

const strokeDashoffset = computed(() => {
  const offset = circumference.value - (props.progress / 100) * circumference.value
  return offset
})

// Get classes for step items - using inline styles instead
const getStepClasses = (index) => {
  if (props.currentStep > index) {
    return '' // Completed - styled inline with #1565c0
  } else if (props.currentStep === index) {
    return '' // Current - styled inline with #1976d2
  } else {
    return '' // Future - styled inline with #90caf9
  }
}
</script>

<style>
/* Light mode - progress indicator background */
.progress-indicator-bar {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e5e7eb;
}

/* Dark mode - progress indicator background (darker blue - darker than body area) */
[data-theme="dark"] .progress-indicator-bar {
  background-color: #0f172a !important;
  border-bottom: 1px solid #1e293b !important;
}

.dark .progress-indicator-bar {
  background-color: #0f172a !important;
  border-bottom: 1px solid #1e293b !important;
}

/* Animation for the progress circle */
circle {
  transition: stroke-dashoffset 0.5s ease-in-out;
}

/* Pulse animation for current step */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
