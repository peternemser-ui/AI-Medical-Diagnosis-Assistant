<template>
  <div class="body-diagram-container">
    <div class="diagram-header">
      <h3 class="text-lg font-semibold mb-2 flex items-center gap-2">
        <MaterialIcon icon="accessibility_new" size="lg" :fill="true" />
        Where are your symptoms?
      </h3>
      <p class="text-sm text-gray-400 mb-4">Click on body areas to select symptom locations</p>
    </div>

    <!-- View Toggle -->
    <div class="view-toggle">
      <button
        @click="currentView = 'front'"
        :class="['view-btn', { active: currentView === 'front' }]"
      >
        <MaterialIcon icon="person" size="sm" />
        <span class="ml-1">Front</span>
      </button>
      <button
        @click="currentView = 'back'"
        :class="['view-btn', { active: currentView === 'back' }]"
      >
        <MaterialIcon icon="person" size="sm" />
        <span class="ml-1">Back</span>
      </button>
    </div>

    <!-- Body Diagram SVG -->
    <div class="diagram-wrapper">
      <svg 
        viewBox="0 0 400 800" 
        class="body-svg"
        @click="handleBackgroundClick"
      >
        <!-- Front View -->
        <g v-if="currentView === 'front'" id="front-view">
          <!-- Head -->
          <ellipse
            cx="200" cy="60" rx="50" ry="60"
            :class="getAreaClass('head')"
            @click.stop="toggleArea('head')"
          />
          <text x="200" y="65" class="area-label">Head</text>

          <!-- Eyes (separate clickable area) -->
          <g class="eyes-group" @click.stop="toggleArea('eyes')" style="cursor: pointer;">
            <ellipse
              cx="185" cy="55" rx="10" ry="7"
              :class="getAreaClass('eyes')"
              style="pointer-events: none;"
            />
            <ellipse
              cx="215" cy="55" rx="10" ry="7"
              :class="getAreaClass('eyes')"
              style="pointer-events: none;"
            />
            <text x="200" y="50" class="area-label-tiny" style="pointer-events: none;">Eyes</text>
          </g>

          <!-- Neck -->
          <rect
            x="180" y="110" width="40" height="30"
            :class="getAreaClass('neck')"
            @click.stop="toggleArea('neck')"
          />
          <text x="200" y="128" class="area-label-small">Neck</text>

          <!-- Chest -->
          <ellipse
            cx="200" cy="180" rx="70" ry="45"
            :class="getAreaClass('chest')"
            @click.stop="toggleArea('chest')"
          />
          <text x="200" y="185" class="area-label">Chest</text>

          <!-- Abdomen -->
          <ellipse
            cx="200" cy="260" rx="65" ry="50"
            :class="getAreaClass('abdomen')"
            @click.stop="toggleArea('abdomen')"
          />
          <text x="200" y="265" class="area-label">Abdomen</text>

          <!-- Groin -->
          <ellipse
            cx="200" cy="330" rx="50" ry="30"
            :class="getAreaClass('groin')"
            @click.stop="toggleArea('groin')"
          />
          <text x="200" y="335" class="area-label-small">Groin</text>

          <!-- Left Shoulder -->
          <circle
            cx="130" cy="150" r="25"
            :class="getAreaClass('left_shoulder')"
            @click.stop="toggleArea('left_shoulder')"
          />
          <text x="130" y="155" class="area-label-tiny">L Shoulder</text>

          <!-- Right Shoulder -->
          <circle
            cx="270" cy="150" r="25"
            :class="getAreaClass('right_shoulder')"
            @click.stop="toggleArea('right_shoulder')"
          />
          <text x="270" y="155" class="area-label-tiny">R Shoulder</text>

          <!-- Left Arm -->
          <rect
            x="85" y="175" width="30" height="120" rx="15"
            :class="getAreaClass('left_arm')"
            @click.stop="toggleArea('left_arm')"
          />
          <text x="100" y="240" class="area-label-small">L Arm</text>

          <!-- Right Arm -->
          <rect
            x="285" y="175" width="30" height="120" rx="15"
            :class="getAreaClass('right_arm')"
            @click.stop="toggleArea('right_arm')"
          />
          <text x="300" y="240" class="area-label-small">R Arm</text>

          <!-- Left Hand -->
          <ellipse
            cx="100" cy="315" rx="18" ry="25"
            :class="getAreaClass('left_hand')"
            @click.stop="toggleArea('left_hand')"
          />
          <text x="100" y="320" class="area-label-tiny">L Hand</text>

          <!-- Right Hand -->
          <ellipse
            cx="300" cy="315" rx="18" ry="25"
            :class="getAreaClass('right_hand')"
            @click.stop="toggleArea('right_hand')"
          />
          <text x="300" y="320" class="area-label-tiny">R Hand</text>

          <!-- Left Thigh -->
          <rect
            x="160" y="360" width="35" height="140" rx="15"
            :class="getAreaClass('left_thigh')"
            @click.stop="toggleArea('left_thigh')"
          />
          <text x="177" y="435" class="area-label-small">L Thigh</text>

          <!-- Right Thigh -->
          <rect
            x="205" y="360" width="35" height="140" rx="15"
            :class="getAreaClass('right_thigh')"
            @click.stop="toggleArea('right_thigh')"
          />
          <text x="222" y="435" class="area-label-small">R Thigh</text>

          <!-- Left Knee -->
          <circle
            cx="177" cy="520" r="20"
            :class="getAreaClass('left_knee')"
            @click.stop="toggleArea('left_knee')"
          />
          <text x="177" y="525" class="area-label-tiny">L Knee</text>

          <!-- Right Knee -->
          <circle
            cx="222" cy="520" r="20"
            :class="getAreaClass('right_knee')"
            @click.stop="toggleArea('right_knee')"
          />
          <text x="222" y="525" class="area-label-tiny">R Knee</text>

          <!-- Left Leg -->
          <rect
            x="165" y="540" width="30" height="150" rx="12"
            :class="getAreaClass('left_leg')"
            @click.stop="toggleArea('left_leg')"
          />
          <text x="180" y="620" class="area-label-small">L Leg</text>

          <!-- Right Leg -->
          <rect
            x="205" y="540" width="30" height="150" rx="12"
            :class="getAreaClass('right_leg')"
            @click.stop="toggleArea('right_leg')"
          />
          <text x="220" y="620" class="area-label-small">R Leg</text>

          <!-- Left Foot -->
          <ellipse
            cx="180" cy="710" rx="22" ry="30"
            :class="getAreaClass('left_foot')"
            @click.stop="toggleArea('left_foot')"
          />
          <text x="180" y="715" class="area-label-tiny">L Foot</text>

          <!-- Right Foot -->
          <ellipse
            cx="220" cy="710" rx="22" ry="30"
            :class="getAreaClass('right_foot')"
            @click.stop="toggleArea('right_foot')"
          />
          <text x="220" y="715" class="area-label-tiny">R Foot</text>
        </g>

        <!-- Back View -->
        <g v-if="currentView === 'back'" id="back-view">
          <!-- Head (back) -->
          <ellipse
            cx="200" cy="60" rx="50" ry="60"
            :class="getAreaClass('head_back')"
            @click.stop="toggleArea('head_back')"
          />
          <text x="200" y="65" class="area-label">Head</text>

          <!-- Neck (back) -->
          <rect
            x="180" y="110" width="40" height="30"
            :class="getAreaClass('neck_back')"
            @click.stop="toggleArea('neck_back')"
          />
          <text x="200" y="128" class="area-label-small">Neck</text>

          <!-- Upper Back -->
          <rect
            x="140" y="145" width="120" height="80" rx="20"
            :class="getAreaClass('upper_back')"
            @click.stop="toggleArea('upper_back')"
          />
          <text x="200" y="190" class="area-label">Upper Back</text>

          <!-- Lower Back -->
          <rect
            x="145" y="230" width="110" height="90" rx="20"
            :class="getAreaClass('lower_back')"
            @click.stop="toggleArea('lower_back')"
          />
          <text x="200" y="280" class="area-label">Lower Back</text>

          <!-- Buttocks -->
          <ellipse
            cx="200" cy="350" rx="55" ry="40"
            :class="getAreaClass('buttocks')"
            @click.stop="toggleArea('buttocks')"
          />
          <text x="200" y="355" class="area-label">Buttocks</text>

          <!-- Left Shoulder (back) -->
          <circle
            cx="130" cy="155" r="28"
            :class="getAreaClass('left_shoulder_back')"
            @click.stop="toggleArea('left_shoulder_back')"
          />
          <text x="130" y="160" class="area-label-tiny">L Shoulder</text>

          <!-- Right Shoulder (back) -->
          <circle
            cx="270" cy="155" r="28"
            :class="getAreaClass('right_shoulder_back')"
            @click.stop="toggleArea('right_shoulder_back')"
          />
          <text x="270" y="160" class="area-label-tiny">R Shoulder</text>

          <!-- Left Arm (back) -->
          <rect
            x="85" y="185" width="30" height="120" rx="15"
            :class="getAreaClass('left_arm_back')"
            @click.stop="toggleArea('left_arm_back')"
          />
          <text x="100" y="250" class="area-label-small">L Arm</text>

          <!-- Right Arm (back) -->
          <rect
            x="285" y="185" width="30" height="120" rx="15"
            :class="getAreaClass('right_arm_back')"
            @click.stop="toggleArea('right_arm_back')"
          />
          <text x="300" y="250" class="area-label-small">R Arm</text>

          <!-- Back of Left Thigh -->
          <rect
            x="160" y="390" width="35" height="130" rx="15"
            :class="getAreaClass('left_thigh_back')"
            @click.stop="toggleArea('left_thigh_back')"
          />
          <text x="177" y="460" class="area-label-small">L Thigh</text>

          <!-- Back of Right Thigh -->
          <rect
            x="205" y="390" width="35" height="130" rx="15"
            :class="getAreaClass('right_thigh_back')"
            @click.stop="toggleArea('right_thigh_back')"
          />
          <text x="222" y="460" class="area-label-small">R Thigh</text>

          <!-- Back of Left Leg (Calf) -->
          <rect
            x="165" y="540" width="30" height="150" rx="12"
            :class="getAreaClass('left_calf')"
            @click.stop="toggleArea('left_calf')"
          />
          <text x="180" y="620" class="area-label-small">L Calf</text>

          <!-- Back of Right Leg (Calf) -->
          <rect
            x="205" y="540" width="30" height="150" rx="12"
            :class="getAreaClass('right_calf')"
            @click.stop="toggleArea('right_calf')"
          />
          <text x="220" y="620" class="area-label-small">R Calf</text>

          <!-- Left Heel -->
          <ellipse
            cx="180" cy="710" rx="22" ry="30"
            :class="getAreaClass('left_heel')"
            @click.stop="toggleArea('left_heel')"
          />
          <text x="180" y="715" class="area-label-tiny">L Heel</text>

          <!-- Right Heel -->
          <ellipse
            cx="220" cy="710" rx="22" ry="30"
            :class="getAreaClass('right_heel')"
            @click.stop="toggleArea('right_heel')"
          />
          <text x="220" y="715" class="area-label-tiny">R Heel</text>
        </g>
      </svg>
    </div>

    <!-- Selected Areas Display -->
    <div v-if="selectedAreas.length > 0" class="selected-areas">
      <h4 class="text-sm font-semibold mb-2 flex items-center gap-2">
        <MaterialIcon icon="check_circle" size="sm" class="text-green-400" />
        Selected Areas ({{ selectedAreas.length }})
      </h4>
      <div class="area-chips">
        <div
          v-for="area in selectedAreas"
          :key="area"
          class="area-chip"
        >
          <span>{{ formatAreaName(area) }}</span>
          <button
            @click="toggleArea(area)"
            class="remove-chip-btn"
            title="Remove"
          >
            <MaterialIcon icon="close" size="xs" />
          </button>
        </div>
      </div>
      <button @click="clearAllAreas" class="clear-all-btn">
        <MaterialIcon icon="clear_all" size="sm" />
        <span class="ml-1">Clear All</span>
      </button>
    </div>

    <!-- Helper Text -->
    <div class="helper-text">
      <MaterialIcon icon="info" size="sm" class="text-blue-400" />
      <span class="text-xs text-gray-400 ml-2">
        Select multiple areas if symptoms are in different locations
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import MaterialIcon from './MaterialIcon.vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'areas-changed'])

const currentView = ref('front')
const selectedAreas = ref([...props.modelValue])

// Watch for external changes
watch(() => props.modelValue, (newVal) => {
  selectedAreas.value = [...newVal]
})

// Watch for internal changes
watch(selectedAreas, (newVal) => {
  emit('update:modelValue', newVal)
  emit('areas-changed', newVal)
}, { deep: true })

const toggleArea = (area) => {
  if (props.disabled) return
  
  const index = selectedAreas.value.indexOf(area)
  if (index > -1) {
    selectedAreas.value.splice(index, 1)
  } else {
    selectedAreas.value.push(area)
  }
}

const clearAllAreas = () => {
  if (props.disabled) return
  selectedAreas.value = []
}

const handleBackgroundClick = () => {
  // Optional: could implement deselect all on background click
}

const getAreaClass = (area) => {
  const isSelected = selectedAreas.value.includes(area)
  return {
    'body-area': true,
    'selected': isSelected,
    'disabled': props.disabled
  }
}

const formatAreaName = (area) => {
  return area
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}
</script>

<style scoped>
.body-diagram-container {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.diagram-header {
  text-align: center;
  margin-bottom: 1rem;
}

.view-toggle {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.view-btn {
  flex: 1;
  max-width: 150px;
  padding: 0.625rem 1rem;
  background: rgba(55, 65, 81, 0.5);
  border: 2px solid rgba(75, 85, 99, 0.5);
  border-radius: 8px;
  color: #9CA3AF;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view-btn:hover:not(.active) {
  background: rgba(75, 85, 99, 0.5);
  border-color: rgba(107, 114, 128, 0.7);
}

.view-btn.active {
  background: linear-gradient(135deg, #3B82F6, #8B5CF6);
  border-color: #3B82F6;
  color: white;
}

.diagram-wrapper {
  background: rgba(31, 41, 55, 0.8);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(75, 85, 99, 0.5);
  margin-bottom: 1.5rem;
}

.body-svg {
  width: 100%;
  height: auto;
  max-height: 600px;
}

.body-area {
  fill: rgba(96, 165, 250, 0.15);
  stroke: rgba(96, 165, 250, 0.5);
  stroke-width: 2;
  cursor: pointer;
  transition: all 0.2s;
}

.body-area:hover:not(.disabled) {
  fill: rgba(96, 165, 250, 0.3);
  stroke: rgba(96, 165, 250, 0.8);
  stroke-width: 3;
}

.body-area.selected {
  fill: rgba(59, 130, 246, 0.5);
  stroke: rgba(59, 130, 246, 1);
  stroke-width: 3;
  animation: pulse 2s ease-in-out infinite;
}

.body-area.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

.area-label {
  fill: white;
  font-size: 14px;
  font-weight: 600;
  text-anchor: middle;
  pointer-events: none;
  opacity: 0.9;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
}

.area-label-small {
  fill: white;
  font-size: 11px;
  font-weight: 600;
  text-anchor: middle;
  pointer-events: none;
  opacity: 0.85;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
}

.area-label-tiny {
  fill: white;
  font-size: 9px;
  font-weight: 600;
  text-anchor: middle;
  pointer-events: none;
  opacity: 0.8;
  text-shadow: 0 0 4px rgba(0, 0, 0, 0.8);
}

.selected-areas {
  background: rgba(59, 130, 246, 0.1);
  border: 1px solid rgba(59, 130, 246, 0.3);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.area-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.area-chip {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(59, 130, 246, 0.2);
  border: 1px solid rgba(59, 130, 246, 0.4);
  padding: 0.375rem 0.75rem;
  border-radius: 20px;
  font-size: 0.875rem;
  color: #93C5FD;
  font-weight: 500;
}

.remove-chip-btn {
  background: none;
  border: none;
  color: #93C5FD;
  cursor: pointer;
  display: flex;
  align-items: center;
  padding: 0.125rem;
  border-radius: 50%;
  transition: all 0.2s;
}

.remove-chip-btn:hover {
  background: rgba(239, 68, 68, 0.3);
  color: #FCA5A5;
}

.clear-all-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.5rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  color: #FCA5A5;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-all-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
}

.helper-text {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  background: rgba(59, 130, 246, 0.05);
  border-radius: 8px;
}
</style>
