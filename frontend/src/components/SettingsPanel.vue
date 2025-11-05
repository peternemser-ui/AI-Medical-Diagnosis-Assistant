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
      <div class="bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-700">
          <h2 class="text-xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Settings
          </h2>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-white transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Content -->
        <div class="p-6 space-y-6">
          <!-- Voice Settings -->
          <div>
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
              Voice Settings
            </h3>
            
            <div class="space-y-4">
              <!-- Enable Voice Input -->
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-white font-medium">Voice Input</label>
                  <p class="text-gray-400 text-sm">Enable microphone for voice recording</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    v-model="settings.voiceInput" 
                    @change="updateSetting('voiceInput', $event.target.checked)"
                    class="sr-only peer"
                  >
                  <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <!-- Enable Audio Responses -->
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-white font-medium">Audio Responses</label>
                  <p class="text-gray-400 text-sm">Play AI responses as audio</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    v-model="settings.audioResponses" 
                    @change="updateSetting('audioResponses', $event.target.checked)"
                    class="sr-only peer"
                  >
                  <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <!-- Speech Rate -->
              <div v-if="settings.audioResponses">
                <label class="block text-white font-medium mb-2">Speech Rate</label>
                <div class="flex items-center space-x-4">
                  <span class="text-gray-400 text-sm">Slow</span>
                  <input 
                    type="range" 
                    v-model="settings.speechRate" 
                    @input="updateSetting('speechRate', $event.target.value)"
                    min="0.5" 
                    max="2" 
                    step="0.1" 
                    class="flex-1 h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
                  >
                  <span class="text-gray-400 text-sm">Fast</span>
                </div>
                <p class="text-gray-400 text-xs mt-1">Current: {{ settings.speechRate }}x</p>
              </div>
            </div>
          </div>

          <!-- Interface Settings -->
          <div>
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Interface
            </h3>
            
            <div class="space-y-4">
              <!-- Auto-scroll -->
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-white font-medium">Auto-scroll Chat</label>
                  <p class="text-gray-400 text-sm">Automatically scroll to new messages</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    v-model="settings.autoScroll" 
                    @change="updateSetting('autoScroll', $event.target.checked)"
                    class="sr-only peer"
                  >
                  <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <!-- Sound Effects -->
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-white font-medium">Sound Effects</label>
                  <p class="text-gray-400 text-sm">Play sounds for notifications</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    v-model="settings.soundEffects" 
                    @change="updateSetting('soundEffects', $event.target.checked)"
                    class="sr-only peer"
                  >
                  <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>

              <!-- Show Timestamps -->
              <div class="flex items-center justify-between">
                <div>
                  <label class="text-white font-medium">Show Timestamps</label>
                  <p class="text-gray-400 text-sm">Display message timestamps</p>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                  <input 
                    type="checkbox" 
                    v-model="settings.showTimestamps" 
                    @change="updateSetting('showTimestamps', $event.target.checked)"
                    class="sr-only peer"
                  >
                  <div class="w-11 h-6 bg-gray-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
          </div>

          <!-- Privacy Settings -->
          <div>
            <h3 class="text-lg font-semibold text-white mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Privacy
            </h3>
            
            <div class="space-y-4">
              <!-- Clear Conversation -->
              <div>
                <button
                  @click="clearConversation"
                  class="w-full bg-yellow-600 hover:bg-yellow-700 text-white py-2 px-4 rounded-lg text-sm font-medium transition-colors duration-200 flex items-center justify-center"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Clear Conversation History
                </button>
                <p class="text-gray-400 text-xs mt-1">Remove all messages from this session</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="border-t border-gray-700 p-4 bg-gray-900 rounded-b-lg">
          <div class="flex justify-between items-center">
            <div class="text-sm text-gray-400">
              Settings saved automatically
            </div>
            <button
              @click="$emit('close')"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors duration-200"
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  initialSettings: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['close', 'settings-changed', 'clear-conversation'])

// Default settings
const defaultSettings = {
  voiceInput: true,
  audioResponses: false,
  speechRate: 1.0,
  autoScroll: true,
  soundEffects: true,
  showTimestamps: true
}

// Merge initial settings with defaults
const settings = ref({
  ...defaultSettings,
  ...props.initialSettings
})

// Update setting and emit change
const updateSetting = (key, value) => {
  settings.value[key] = value
  emit('settings-changed', { [key]: value })
}

// Clear conversation
const clearConversation = () => {
  emit('clear-conversation')
}

// Watch for changes in initial settings
watch(() => props.initialSettings, (newSettings) => {
  settings.value = {
    ...defaultSettings,
    ...newSettings
  }
}, { deep: true })
</script>

<style scoped>
/* Custom slider styling */
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.slider::-webkit-slider-track {
  height: 8px;
  -webkit-appearance: none;
  background: #4b5563;
  border-radius: 4px;
}

.slider::-moz-range-thumb {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-track {
  height: 8px;
  background: #4b5563;
  border-radius: 4px;
  border: none;
}

/* Toggle switch styling */
.peer:checked ~ div {
  background-color: #3b82f6;
}

.peer:focus ~ div {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
</style>
