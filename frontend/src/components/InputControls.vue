<template>
  <div class="input-controls-bar p-4" style="background-color: var(--controls-bg); border-top: 1px solid var(--border);">
    <div class="max-w-4xl mx-auto">
      <!-- Voice recording indicator -->
      <div v-if="isRecording" class="mb-4 p-3 bg-red-900 bg-opacity-50 border border-red-600 rounded-lg">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
            <span class="text-red-400 font-medium">Recording...</span>
            <span class="text-gray-400 text-sm">{{ formatRecordingTime(recordingTime) }}</span>
          </div>
          <button
            @click="stopRecording"
            class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
          >
            Stop Recording
          </button>
        </div>
        <div class="mt-2">
          <div class="w-full bg-gray-700 rounded-full h-1">
            <div class="bg-red-500 h-1 rounded-full transition-all duration-500" :style="{ width: recordingProgress + '%' }"></div>
          </div>
        </div>
      </div>

      <!-- Main input area -->
      <div class="flex items-end space-x-3">
        <!-- Sound/TTS toggle button -->
        <button
          @click="toggleSoundEnabled"
          :class="soundToggleClasses"
          class="flex-shrink-0 p-3 rounded-full transition-all duration-200 transform hover:scale-105"
          :title="soundEnabled ? 'Sound ON - AI will speak questions' : 'Sound OFF - Text only'"
        >
          <!-- Speaker icon when sound is on -->
          <svg v-if="soundEnabled" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          </svg>
          <!-- Muted speaker icon when sound is off -->
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" clip-rule="evenodd" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
          </svg>
        </button>

        <!-- Voice recording button -->
        <button
          @click="toggleRecording"
          :disabled="disabled || isProcessing"
          class="flex-shrink-0 p-3 rounded-full transition-all duration-200 transform hover:scale-105"
          :class="voiceButtonClasses"
          :title="isRecording ? 'Stop recording' : 'Start voice recording'"
        >
          <svg v-if="!isRecording" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9h6v6H9z" />
          </svg>
        </button>

        <!-- Text input -->
        <div class="flex-1 relative">
          <textarea
            ref="textareaRef"
            v-model="currentMessage"
            @keydown="handleKeydown"
            @input="adjustTextareaHeight"
            :disabled="disabled || isRecording"
            :placeholder="placeholderText"
            class="input-textarea bg-bg text-text border-border w-full rounded-2xl px-4 py-3 pr-12 resize-none focus:outline-none focus:ring-2 focus:ring-primary transition-all duration-200"
            :style="{ height: textareaHeight + 'px' }"
            rows="1"
          ></textarea>
          
          <!-- Send button -->
          <button
            @click="handleSend"
            :disabled="!canSend"
            class="absolute right-2 bottom-2 p-2 rounded-full transition-all duration-200 transform hover:scale-105"
            :class="sendButtonClasses"
            :title="canSend ? 'Send message' : 'Enter a message to send'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Quick actions -->
      <div v-if="quickActions && quickActions.length > 0" class="mt-3 flex flex-wrap gap-2">
        <button
          v-for="action in quickActions"
          :key="action"
          @click="$emit('quick-action', action)"
          :disabled="disabled"
          class="text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white px-3 py-1 rounded-full transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ action }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps({
  disabled: {
    type: Boolean,
    default: false
  },
  isProcessing: {
    type: Boolean,
    default: false
  },
  voiceEnabled: {
    type: Boolean,
    default: true
  },
  soundEnabled: {
    type: Boolean,
    default: false
  },
  quickActions: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'send-message',
  'start-recording', 
  'stop-recording',
  'voice-toggle',
  'sound-toggle',
  'quick-action'
])

// Reactive state
const currentMessage = ref('')
const isRecording = ref(false)
const recordingTime = ref(0)
const recordingProgress = ref(0)
const textareaRef = ref(null)
const textareaHeight = ref(48)

// Constants
const MIN_HEIGHT = 48
const MAX_HEIGHT = 120
const MAX_RECORDING_TIME = 60 // seconds

// Computed properties
const canSend = computed(() => {
  return !props.disabled && !props.isProcessing && currentMessage.value.trim().length > 0
})

const placeholderText = computed(() => {
  if (props.disabled) return t('common.loading')
  if (props.isProcessing) return t('common.loading')
  if (isRecording.value) return t('diagnosis.analyzing')
  return t('diagnosis.voiceInputPlaceholder')
})

const soundToggleClasses = computed(() => ({
  'bg-slate-600 hover:bg-slate-700 text-white': props.soundEnabled,
  'bg-slate-700 hover:bg-slate-600 text-slate-400': !props.soundEnabled
}))

const voiceToggleClasses = computed(() => ({
  'bg-cyan-500 hover:bg-cyan-600 text-white': props.voiceEnabled,
  'bg-slate-700 hover:bg-slate-600 text-slate-400': !props.voiceEnabled
}))

const voiceButtonClasses = computed(() => ({
  'bg-cyan-500 hover:bg-cyan-600 text-white': !isRecording.value && !props.disabled && props.voiceEnabled,
  'bg-red-600 hover:bg-red-700 text-white animate-pulse': isRecording.value,
  'bg-slate-700 text-slate-500 cursor-not-allowed': props.disabled || !props.voiceEnabled
}))

const sendButtonClasses = computed(() => ({
  'bg-cyan-500 hover:bg-cyan-600 text-white': canSend.value,
  'bg-slate-700 text-slate-500 cursor-not-allowed': !canSend.value
}))

// Methods
const toggleSoundEnabled = () => {
  emit('sound-toggle')
}

const toggleVoiceEnabled = () => {
  if (isRecording.value) {
    stopRecording()
  }
  emit('voice-toggle')
}

const toggleRecording = () => {
  if (!props.voiceEnabled) {
    // Enable voice first if it's disabled
    emit('voice-toggle')
    return
  }
  
  if (isRecording.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

const startRecording = () => {
  if (props.disabled || !props.voiceEnabled) return
  
  isRecording.value = true
  recordingTime.value = 0
  recordingProgress.value = 0
  
  emit('start-recording')
  
  // Start recording timer
  const timer = setInterval(() => {
    recordingTime.value += 1
    recordingProgress.value = (recordingTime.value / MAX_RECORDING_TIME) * 100
    
    if (recordingTime.value >= MAX_RECORDING_TIME) {
      clearInterval(timer)
      stopRecording()
    }
  }, 1000)
  
  // Store timer to clear if stopped manually
  window.recordingTimer = timer
}

const stopRecording = () => {
  isRecording.value = false
  
  if (window.recordingTimer) {
    clearInterval(window.recordingTimer)
    window.recordingTimer = null
  }
  
  emit('stop-recording')
}

const handleSend = () => {
  if (!canSend.value) return
  
  const message = currentMessage.value.trim()
  if (message) {
    emit('send-message', message)
    currentMessage.value = ''
    resetTextareaHeight()
  }
}

const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}

const adjustTextareaHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      // Reset height to auto to get the correct scrollHeight
      textareaRef.value.style.height = 'auto'
      
      // Calculate new height based on content
      const newHeight = Math.min(
        Math.max(textareaRef.value.scrollHeight, MIN_HEIGHT),
        MAX_HEIGHT
      )
      
      textareaHeight.value = newHeight
    }
  })
}

const resetTextareaHeight = () => {
  textareaHeight.value = MIN_HEIGHT
}

const formatRecordingTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
}

// Watch for message changes to adjust height
watch(currentMessage, adjustTextareaHeight)

// Focus textarea on mount
onMounted(() => {
  if (textareaRef.value) {
    textareaRef.value.focus()
  }
})

// Cleanup on unmount
const cleanup = () => {
  if (window.recordingTimer) {
    clearInterval(window.recordingTimer)
    window.recordingTimer = null
  }
}

// Expose cleanup for parent component
defineExpose({
  cleanup,
  focus: () => textareaRef.value?.focus()
})
</script>

<style>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

/* Input controls bar styling */
.input-controls-bar {
  position: relative;
  background: linear-gradient(to bottom, rgba(248, 250, 252, 0.9), rgba(241, 245, 249, 0.95));
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(226, 232, 240, 0.6);
}

/* Dark mode - darker with fade effect */
[data-theme="dark"] .input-controls-bar {
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.98)) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-top: 1px solid rgba(51, 65, 85, 0.5) !important;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.3);
}

.dark .input-controls-bar {
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.98)) !important;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-top: 1px solid rgba(51, 65, 85, 0.5) !important;
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.3);
}

/* Textarea styling */
.input-textarea {
  overflow: hidden;
  background-color: #f8f9fa;
  color: #1f2937;
  border: 1px solid #d1d5db;
}

.input-textarea::placeholder {
  color: #9ca3af;
}

.input-textarea:focus {
  outline: none;
  box-shadow: 0 0 0 2px #3b82f6;
  border-color: #3b82f6;
}

/* Dark mode textarea */
[data-theme="dark"] .input-textarea {
  background-color: #1e293b !important;
  color: #f1f5f9 !important;
  border: 1px solid #475569 !important;
}

.dark .input-textarea {
  background-color: #1e293b !important;
  color: #f1f5f9 !important;
  border: 1px solid #475569 !important;
}

[data-theme="dark"] .input-textarea::placeholder {
  color: #64748b !important;
}

.dark .input-textarea::placeholder {
  color: #64748b !important;
}
</style>