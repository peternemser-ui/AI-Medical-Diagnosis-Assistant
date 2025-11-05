<template>
  <div class="severity-slider">
    <!-- Label -->
    <div class="slider-header">
      <label :for="id" class="slider-label">
        {{ label }}
      </label>
      <div class="severity-value" :style="{ color: getSeverityColor(modelValue) }">
        <span class="value-number">{{ modelValue }}</span>
        <span class="value-text">{{ getSeverityText(modelValue) }}</span>
      </div>
    </div>
    
    <!-- Slider Track -->
    <div class="slider-container">
      <input
        :id="id"
        type="range"
        :min="min"
        :max="max"
        :step="step"
        :value="modelValue"
        @input="handleInput"
        class="slider-input"
        :style="getSliderStyle()"
      />
      
      <!-- Visual markers -->
      <div class="slider-markers">
        <div
          v-for="n in markerCount"
          :key="n"
          class="marker"
          :class="{ 'active': n <= modelValue }"
          :style="{ left: `${((n - 1) / (max - min)) * 100}%` }"
        >
          <div class="marker-dot"></div>
          <div class="marker-label">{{ n }}</div>
        </div>
      </div>
    </div>
    
    <!-- Description -->
    <div class="slider-description">
      <div class="description-item">
        <span class="emoji">😊</span>
        <span>Mild</span>
      </div>
      <div class="description-item">
        <span class="emoji">😐</span>
        <span>Moderate</span>
      </div>
      <div class="description-item">
        <span class="emoji">😣</span>
        <span>Severe</span>
      </div>
      <div class="description-item">
        <span class="emoji">😰</span>
        <span>Critical</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 5
  },
  label: {
    type: String,
    default: 'Symptom Severity'
  },
  min: {
    type: Number,
    default: 1
  },
  max: {
    type: Number,
    default: 10
  },
  step: {
    type: Number,
    default: 1
  },
  id: {
    type: String,
    default: () => `severity-${Math.random().toString(36).substr(2, 9)}`
  }
})

const emit = defineEmits(['update:modelValue'])

const markerCount = computed(() => props.max - props.min + 1)

const handleInput = (event) => {
  emit('update:modelValue', parseInt(event.target.value))
}

const getSeverityColor = (value) => {
  if (value <= 3) return '#10b981' // Green - Mild
  if (value <= 5) return '#f59e0b' // Orange - Moderate
  if (value <= 7) return '#f97316' // Deep Orange - Significant
  if (value <= 9) return '#ef4444' // Red - Severe
  return '#dc2626' // Dark Red - Critical
}

const getSeverityText = (value) => {
  if (value <= 3) return 'Mild'
  if (value <= 5) return 'Moderate'
  if (value <= 7) return 'Significant'
  if (value <= 9) return 'Severe'
  return 'Critical'
}

const getSliderStyle = () => {
  const percentage = ((props.modelValue - props.min) / (props.max - props.min)) * 100
  const color = getSeverityColor(props.modelValue)
  
  return {
    background: `linear-gradient(to right, ${color} 0%, ${color} ${percentage}%, #e5e7eb ${percentage}%, #e5e7eb 100%)`
  }
}
</script>

<style scoped>
.severity-slider {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.slider-label {
  font-size: 1rem;
  font-weight: 600;
  color: #f1f5f9;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.severity-value {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  font-weight: 700;
}

.value-number {
  font-size: 1.5rem;
  line-height: 1;
}

.value-text {
  font-size: 0.875rem;
  opacity: 0.9;
}

/* Slider Container */
.slider-container {
  position: relative;
  padding: 1.5rem 0;
  margin-bottom: 1rem;
}

/* Slider Input */
.slider-input {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* Slider Track - WebKit */
.slider-input::-webkit-slider-runnable-track {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: transparent;
}

/* Slider Track - Firefox */
.slider-input::-moz-range-track {
  width: 100%;
  height: 8px;
  border-radius: 4px;
  background: #e5e7eb;
}

/* Slider Thumb - WebKit */
.slider-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  border: 3px solid currentColor;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.slider-input::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.slider-input::-webkit-slider-thumb:active {
  transform: scale(1.1);
}

/* Slider Thumb - Firefox */
.slider-input::-moz-range-thumb {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  border: 3px solid currentColor;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.slider-input::-moz-range-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.slider-input::-moz-range-thumb:active {
  transform: scale(1.1);
}

/* Visual Markers */
.slider-markers {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.marker {
  position: absolute;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.3s ease;
}

.marker-dot {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}

.marker.active .marker-dot {
  background: rgba(255, 255, 255, 0.8);
  width: 6px;
  height: 6px;
  box-shadow: 0 0 8px currentColor;
}

.marker-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 600;
  transition: all 0.3s ease;
}

.marker.active .marker-label {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 700;
}

/* Description */
.slider-description {
  display: flex;
  justify-content: space-between;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.description-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.7);
}

.emoji {
  font-size: 1.25rem;
}

/* Dark Mode Adjustments */
:root[data-theme="dark"] .severity-slider {
  background: rgba(30, 41, 59, 0.5);
  border-color: rgba(148, 163, 184, 0.2);
}

:root[data-theme="dark"] .slider-input::-moz-range-track {
  background: #334155;
}

/* Responsive */
@media (max-width: 640px) {
  .severity-slider {
    padding: 0.75rem;
  }
  
  .slider-label {
    font-size: 0.875rem;
  }
  
  .value-number {
    font-size: 1.25rem;
  }
  
  .value-text {
    font-size: 0.75rem;
  }
  
  .marker-label {
    font-size: 0.625rem;
  }
  
  .description-item {
    font-size: 0.625rem;
  }
  
  .emoji {
    font-size: 1rem;
  }
}

/* Animation for value change */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.severity-value {
  animation: pulse 0.3s ease;
}
</style>
