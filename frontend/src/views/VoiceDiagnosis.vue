<template>
  <div 
    class="min-h-screen flex flex-col voice-diagnosis-container relative overflow-x-hidden" 
    :style="{ background: 'var(--bg)', color: 'var(--text)' }"
  >
    <!-- === FEATURE #10: EMERGENCY ALERT BANNER === -->
    <div v-if="showEmergency" class="emergency-alert-banner bg-red-600 bg-opacity-95 backdrop-blur-sm py-4 px-6 shadow-2xl border-b-4 border-red-800 animate-pulse-emergency">
      <div class="max-w-4xl mx-auto flex items-start gap-4">
        <div class="flex-shrink-0">
          <svg class="w-10 h-10 text-white animate-pulse" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
        </div>
        <div class="flex-1">
          <h3 class="text-xl font-bold mb-2 text-white flex items-center gap-2">
            ⚠️ {{ emergencyType }}
          </h3>
          <p class="text-white text-base leading-relaxed mb-3">{{ emergencyMessage }}</p>
          <div class="flex gap-3">
            <a href="tel:911" class="inline-flex items-center gap-2 bg-white text-red-600 px-4 py-2 rounded-lg font-bold hover:bg-red-50 transition-colors shadow-lg">
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
              </svg>
              CALL 911 NOW
            </a>
            <button @click="dismissEmergency" class="text-white underline hover:text-red-100 px-3">
              I understand (dismiss)
            </button>
          </div>
        </div>
        <button @click="dismissEmergency" class="flex-shrink-0 text-white hover:text-red-100 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- API Status Indicator - Small Tab -->
    <div v-if="apiStatus === true" class="absolute top-0 left-1/2 transform -translate-x-1/2 z-50">
      <div class="bg-green-600 text-white text-xs px-4 py-1 rounded-b-lg shadow-lg flex items-center gap-1">
        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        <span class="font-medium">AI Active</span>
      </div>
    </div>
    
    <!-- Header with Premium Light Background -->
    <div
      class="backdrop-blur-sm py-4 px-6 flex justify-between items-center header-bar"
      style="background-color: var(--header-bg); border-bottom: 1px solid var(--border);"
    >
      <div>
        <h1 class="text-2xl font-bold header-title" :style="{ color: '#ffffff', fontWeight: '800' }">🩺 AI Health Assistant</h1>
        <p class="header-subtitle text-sm" :style="{ color: '#e2e8f0', fontSize: '14px' }">Professional health guidance powered by AI</p>
      </div>
      <div class="text-right space-y-1 flex items-center gap-4">
        <div class="space-y-1">
          <div class="flex items-center justify-end gap-2">
            <div class="text-sm status-success">● Online</div>
            <div v-if="apiStatus === true" class="flex items-center text-xs status-success px-2 py-1 rounded-full border">
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
              </svg>
              AI Active
            </div>
            <div v-else-if="apiStatus === false" class="flex items-center text-xs status-warning px-2 py-1 rounded-full border">
              <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              Basic Mode
            </div>
          </div>
          <div class="text-xs" :style="{ color: '#e2e8f0', fontSize: '12px' }">Estimated Cost: ${{ estimatedCost.toFixed(4) }}</div>
        </div>

        <!-- Theme Toggle -->
        <ThemeToggle />

        <!-- === FEATURE #7: LANGUAGE SWITCHER === -->
        <LanguageSwitcher />

        <!-- Settings Button -->
        <button
          @click="goToApiSettings"
          class="p-2 hover-overlay rounded-lg transition-colors duration-200 group settings-btn"
          title="Configure API Key"
        >
          <svg class="w-6 h-6 text-secondary group-hover:text-primary group-hover:rotate-90 transition-all duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Progress Indicator - Fixed at top -->
    <ProgressIndicator 
      v-if="conversationState !== 'initial'"
      :visible="conversationState !== 'initial'"
      :progress="progressPercentage"
      :current-step="currentStep"
      :steps="['Start', 'Symptoms', 'Duration', 'Severity', 'Details', 'Analysis']"
      :title="getProgressTitle()"
      :message="getProgressMessage()"
    />

    <!-- Chat Interface - Always visible -->
    <div class="flex-1 flex flex-col min-h-0 pb-32">
      <div class="flex-1 overflow-hidden">
        <div class="max-w-4xl mx-auto h-full flex flex-col">
          <!-- Chat Area -->
          <ChatArea
            ref="chatAreaRef"
            :messages="chatMessages"
            :is-typing="showTyping"
            :auto-scroll="autoScroll"
            :sound-enabled="soundEnabled"
            @followup-selected="handleQuickQuestion"
            @replay-message="(text) => voice.speak(text)"
          />
          
          <!-- Body Diagram Section (shown during symptom gathering) -->
          <div 
            v-if="conversationState === 'gathering' && showBodyDiagram" 
            class="max-w-4xl mx-auto px-4 py-4 bg-surface-2 bg-opacity-90 backdrop-blur-sm rounded-lg border border-border mb-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <MaterialIcon icon="accessibility_new" size="lg" :fill="true" class="text-purple-400" />
                <h3 class="text-lg font-semibold">Select Symptom Locations</h3>
              </div>
              <button 
                @click="showBodyDiagram = false"
                class="text-gray-400 hover:text-white transition-colors"
              >
                <MaterialIcon icon="close" size="sm" />
              </button>
            </div>
            <BodyDiagram
              v-model="selectedBodyAreas"
              :disabled="isLoading"
              @areas-changed="handleBodyAreasChanged"
            />
          </div>

          <!-- Image Upload Section (shown during symptom gathering) -->
          <div 
            v-if="conversationState === 'gathering' && showImageUpload" 
            class="max-w-4xl mx-auto px-4 py-4 bg-surface-2 bg-opacity-90 backdrop-blur-sm rounded-lg border border-border mb-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <MaterialIcon icon="photo_camera" size="lg" :fill="true" class="text-blue-400" />
                <h3 class="text-lg font-semibold">Add Photos (Optional)</h3>
              </div>
              <button 
                @click="showImageUpload = false"
                class="text-gray-400 hover:text-white transition-colors"
              >
                <MaterialIcon icon="close" size="sm" />
              </button>
            </div>
            <p class="text-sm text-gray-400 mb-4">Upload photos of your symptoms to help with diagnosis</p>
            <ImageUpload
              ref="imageUploadRef"
              :disabled="isLoading"
              :max-images="5"
              @images-updated="handleImagesUpdated"
              @analysis-complete="handleImageAnalysisComplete"
            />
          </div>

          <!-- Severity Slider Section (shown when asking about severity) -->
          <div 
            v-if="conversationState === 'gathering' && showSeveritySlider" 
            class="max-w-4xl mx-auto px-4 py-4 bg-surface-2 bg-opacity-90 backdrop-blur-sm rounded-lg border border-border mb-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <MaterialIcon icon="monitor_heart" size="lg" :fill="true" class="text-red-400" />
                <h3 class="text-lg font-semibold">Rate Your Symptom Severity</h3>
              </div>
              <button 
                @click="handleSeveritySubmit"
                class="px-4 py-2 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 rounded-lg font-semibold transition-all duration-200 flex items-center gap-2"
              >
                <MaterialIcon icon="check" size="sm" />
                Submit
              </button>
            </div>
            <p class="text-sm text-gray-400 mb-4">Use the slider below to indicate how severe your symptoms are</p>
            <SeveritySlider
              v-model="severityValue"
              label="Symptom Severity Level"
            />
          </div>
          
          <!-- Quick Actions -->
          <QuickActions 
            v-if="conversationState === 'diagnosed'"
            :actions="diagnosisActions"
            @action-selected="handleQuickAction"
          />
        </div>
      </div>
    </div>

    <!-- Body Diagram Toggle Button (floating) -->
    <button
      v-if="conversationState === 'gathering' && !showBodyDiagram"
      @click="toggleBodyDiagram"
      class="fixed bottom-40 right-6 z-20 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110"
      title="Select body areas"
    >
      <MaterialIcon icon="accessibility_new" size="lg" :fill="true" />
    </button>

    <!-- Image Upload Toggle Button (floating) -->
    <button
      v-if="conversationState === 'gathering' && !showImageUpload"
      @click="toggleImageUpload"
      class="fixed bottom-24 right-6 z-20 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110"
      title="Upload symptom photos"
    >
      <MaterialIcon icon="add_photo_alternate" size="lg" :fill="true" />
    </button>

    <!-- === FEATURE #9: DRUG LOOKUP BUTTON (floating) === -->
    <button
      v-if="conversationState !== 'initial'"
      @click="showDrugLookup = true"
      class="fixed top-24 right-6 z-20 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-4 py-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110 flex items-center gap-2"
      title="Drug Information & Interactions"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
      </svg>
      <span class="text-sm font-semibold">💊 Drugs</span>
    </button>

    <!-- Drug Lookup Modal -->
    <div 
      v-if="showDrugLookup"
      class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
      @click.self="showDrugLookup = false"
    >
      <div 
        class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-y-auto border border-white/10"
        @click.stop
      >
        <div class="p-6">
          <DrugLookup @close="showDrugLookup = false" />
        </div>
      </div>
    </div>

    <!-- Input Controls - Fixed at bottom -->
    <div class="fixed bottom-0 left-0 right-0 z-50">
      <InputControls
        ref="inputControlsRef"
        :disabled="isLoading"
        :is-processing="isLoading"
        :voice-enabled="voiceEnabled"
        :sound-enabled="soundEnabled"
        :quick-actions="getQuickActions()"
        @send-message="handleSendMessage"
        @start-recording="startVoiceRecording"
        @stop-recording="stopVoiceRecording"
        @voice-input="handleVoiceResult"
        @voice-toggle="toggleVoiceEnabled"
        @sound-toggle="soundEnabled = !soundEnabled"
      />
    </div>

    <!-- Error Message -->
    <ErrorMessage 
      :visible="!!error"
      :message="error || ''"
      :show-retry="true"
      @close="clearError"
      @retry="clearError"
    />
    
    <!-- Help Modal -->
    <HelpModal v-if="showHelp" @close="showHelp = false" />
    
    <!-- Settings Panel -->
    <SettingsPanel 
      v-if="showSettings" 
      :visible="showSettings"
      :initial-settings="{ voiceInput: voiceEnabled, autoScroll: autoScroll, soundEffects: soundEnabled }"
      @close="showSettings = false"
      @settings-changed="handleSettingsChange"
      @clear-conversation="handleStartOver"
    />
  </div>
</template>

<script setup>
console.log('🔥 VoiceDiagnosis component script starting...')
console.log('🌍 Window location:', window.location.href)
console.log('📁 Current route should be VoiceDiagnosis')

import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { diagnose, followup, healthCheck, ApiError } from '@/services/api.js'

// Import composables
import { useQuestionnaire } from '@/composables/useQuestionnaire'
import { useChat } from '@/composables/useChat'
import { useVoice } from '@/composables/useVoice'
import { useEmergency } from '@/composables/useEmergency'

// Import core components
import ChatArea from '@/components/ChatArea.vue'
import InputControls from '@/components/InputControls.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import QuickActions from '@/components/QuickActions.vue'
import HelpModal from '@/components/HelpModal.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'
import ImageUpload from '@/components/ImageUpload.vue'
import BodyDiagram from '@/components/BodyDiagram.vue'
import MaterialIcon from '@/components/MaterialIcon.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import SeveritySlider from '@/components/SeveritySlider.vue'
import DrugLookup from '@/components/DrugLookup.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'

// Composables
const router = useRouter()
const { t } = useI18n()

// Initialize composables
const questionnaire = useQuestionnaire()
const chat = useChat()
const voice = useVoice()
const emergency = useEmergency()

// === REACTIVE STATE ===
const currentInput = ref('')
const isLoading = ref(false)
const error = ref(null)
const estimatedCost = ref(0.0)
const hasStarted = ref(false)

// Use chat from composable
const chatMessages = chat.messages
console.log('📝 Chat messages initialized from composable:', chatMessages.value)
const chatAreaRef = ref(null)
const inputControlsRef = ref(null)

// Use typing indicator from composable
const showTyping = chat.isTyping
const showHelp = ref(false)
const showSettings = ref(false)
const apiStatus = ref(null) // null = checking, true = AI enabled, false = fallback mode

// Conversation management - questionnaire now from composable
const conversationState = ref('initial') // initial, gathering, diagnosing, diagnosed
const currentStep = ref(0)
const totalSteps = ref(13) // Total questions: 3 fixed (age, gender, symptoms) + 10 AI-generated follow-ups

// Body diagram
const showBodyDiagram = ref(false)
const selectedBodyAreas = ref([])

// Image upload
const showImageUpload = ref(false)
const imageUploadRef = ref(null)
const uploadedImages = ref([])
const imageAnalysisResults = ref([])

// Severity slider
const showSeveritySlider = ref(false)
const severityValue = ref(5)

// === FEATURE #10: EMERGENCY DETECTION - now from composable ===
const showEmergency = emergency.showEmergency
const emergencyMessage = emergency.emergencyMessage
const emergencyType = emergency.emergencyType

// === FEATURE #9: DRUG LOOKUP ===
const showDrugLookup = ref(false)

// Voice - now from composable
const voiceEnabled = voice.voiceEnabled
const soundEnabled = voice.soundEnabled

// Settings
const autoScroll = chat.autoScroll

// Diagnosis completion actions
const diagnosisActions = ref([
  {
    id: 'view-dashboard',
    text: 'View Detailed Dashboard',
    category: 'results',
    description: 'See comprehensive analysis with charts and recommendations',
    icon: 'dashboard',
    action: 'navigate',
    route: '/dashboard'
  },
  {
    id: 'manual-dashboard',
    text: 'Go to Dashboard (Direct)',
    category: 'debug',
    description: 'Direct navigation to dashboard for testing',
    icon: 'build',
    action: 'manual-navigate',
    route: '/dashboard'
  },
  {
    id: 'when-doctor',
    text: 'When should I see a doctor?',
    category: 'care',
    description: 'Get guidance on when to seek medical attention',
    icon: 'person',
    action: 'question'
  },
  {
    id: 'home-remedies',
    text: 'What can I do at home?',
    category: 'treatment',
    description: 'Learn about home care options',
    icon: 'home',
    action: 'question'
  },
  {
    id: 'medications',
    text: 'Can I take over-the-counter medications?',
    category: 'treatment',
    description: 'Ask about medication options',
    icon: 'medication',
    action: 'question'
  },
  {
    id: 'symptoms-worse',
    text: 'Are my symptoms getting worse?',
    category: 'severity',
    description: 'Ask about symptom progression',
    icon: 'trending_down',
    action: 'question'
  }
])

// Speech Recognition refs removed - now handled by voice composable

// Computed properties
const canSubmit = computed(() => {
  return currentInput.value.trim() && !isLoading.value
})

const progressPercentage = computed(() => {
  if (conversationState.value === 'initial') return 0
  if (conversationState.value === 'gathering') {
    return Math.round((questionnaire.progress.value.current / questionnaire.progress.value.total) * 70)
  }
  if (conversationState.value === 'diagnosing') return 85
  if (conversationState.value === 'diagnosed') return 100
  return 0
})

// === WATCHERS ===
watch(chatMessages, async () => {
  if (autoScroll.value) {
    await nextTick()
    scrollToBottom()
  }
}, { deep: true })

watch(conversationState, (newState) => {
  console.log(`🔄 Conversation state changed to: ${newState}`)
})

// === HELPER FUNCTIONS ===
function restoreInputFocus() {
  nextTick(() => {
    setTimeout(() => {
      if (inputControlsRef.value && inputControlsRef.value.focus) {
        inputControlsRef.value.focus()
      }
    }, 100)
  })
}

// === WATCHERS ===
watch(soundEnabled, (newVal) => {
  console.log('🔊 Sound toggled:', newVal ? 'ON' : 'OFF')

  // Voice composable handles test sound in its toggleSound method
  // When turning on, play a test message
  if (newVal) {
    setTimeout(() => {
      voice.speak('Voice enabled', { rate: 1.2, volume: 0.8 })
    }, 100)
  } else {
    // When turning off, stop any ongoing speech
    voice.stopSpeaking()
  }
})

// === LIFECYCLE ===
onMounted(async () => {
  console.log('🔄 Component mounted - FRESH START')
  console.log('🔊 Initial soundEnabled state:', soundEnabled.value)
  console.log('🔊 Speech synthesis available:', !!window.speechSynthesis)
  
  // Initialize voice capabilities FIRST
  voice.initialize()
  console.log('🔊 After setup - voice initialized')
  
  // Check API status
  checkApiStatus()
  
  // Force complete reset
  chat.clearMessages()
  hasStarted.value = false
  conversationState.value = 'initial'
  isLoading.value = false
  chat.isTyping.value = false
  questionnaire.reset()

  // Add only the initial AI greeting
  setTimeout(() => {
    chat.addAssistantMessage('Hello, I\'m your AI health assistant. I\'m here to help assess your **human health** symptoms and provide guidance.\n\n**Important:** This service is for human health only. If you need help with a pet (dog, cat, fish, bird, etc.), please consult a veterinarian. 🐾\n\nBefore we begin, I need to collect some basic information. **What is your age?**')
    
    hasStarted.value = true
    conversationState.value = 'gathering'
    console.log('✅ Fresh conversation started')
    
    // Speak the initial greeting if sound is enabled
    if (soundEnabled.value) {
      console.log('🔊 Will speak initial greeting in 800ms')
      setTimeout(() => {
        console.log('🔊 Now speaking initial greeting')
        voice.speak('Hello, I\'m your AI health assistant. I\'m here to help assess your symptoms and provide guidance. Before we begin, I need to collect some basic information. What is your age?')
      }, 800)
    } else {
      console.log('❌ NOT speaking initial greeting - sound disabled')
    }
    
    // Focus input on initial load
    restoreInputFocus()
  }, 500)
})

onUnmounted(() => {
  cleanup()
})

// === INITIALIZATION ===
async function checkApiStatus() {
  try {
    // Check if API key is configured in localStorage
    const apiKey = localStorage.getItem('openai_api_key')
    
    if (apiKey && apiKey.trim() && apiKey.startsWith('sk-')) {
      console.log('✅ OpenAI API key found - AI Enhanced Mode enabled')
      apiStatus.value = true // AI Enhanced Mode
    } else {
      console.log('⚠️ No valid API key found - Running in Basic Mode')
      apiStatus.value = false // Basic Mode
    }
  } catch (err) {
    console.error('❌ API status check failed:', err)
    apiStatus.value = false
  }
}

async function initializeApp() {
  try {
    console.log('🔍 Testing API connection...')
    const isHealthy = await healthCheck()
    if (isHealthy) {
      console.log('✅ API connection successful')
    } else {
      handleError('Backend API is not healthy. Please try again later.')
    }
  } catch (err) {
    console.error('❌ API connection failed:', err)
    handleError('Failed to connect to the backend API. Please check your network connection and try again.')
  }
}

// setupVoiceCapabilities removed - now using voice.initialize() from composable

function setupKeyboardShortcuts() {
  const handleKeydown = (event) => {
    // Ctrl/Cmd + Enter to send message
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      if (canSubmit.value) {
        handleSendMessage(currentInput.value)
      }
    }
    
    // ESC to cancel/clear
    if (event.key === 'Escape') {
      if (voice.isRecording.value) {
        stopVoiceRecording()
      } else {
        currentInput.value = ''
      }
    }
    
    // F1 for help
    if (event.key === 'F1') {
      event.preventDefault()
      showHelp.value = !showHelp.value
    }
  }
  
  document.addEventListener('keydown', handleKeydown)
  
  // Store cleanup function
  window.__voiceDiagnosisKeydownHandler = handleKeydown
}

function cleanup() {
  // Voice composable handles its own cleanup
  voice.cleanup()

  if (window.__voiceDiagnosisKeydownHandler) {
    document.removeEventListener('keydown', window.__voiceDiagnosisKeydownHandler)
  }
}

// === CORE FUNCTIONS ===

/**
 * Handles the start of the conversation
 */
function handleStart() {
  console.log('🚀 handleStart called - simplified version')
  
  hasStarted.value = true
  conversationState.value = 'gathering'
  
  // Simple direct message addition
  chat.addAssistantMessage('Hello, I\'m your AI health assistant. What brings you here today?')

  console.log('✅ Message added via chat composable')
}

// Note: validateInput function removed - now using questionnaire.validateResponse() from composable

// detectEmergency and showEmergencyAlert functions removed - now using emergency composable

/**
 * Dismisses emergency alert
 */
function dismissEmergency() {
  emergency.dismissAlert()
}

/**
 * Handles sending a message from the user
 */
async function handleSendMessage(message) {
  console.log('📨 handleSendMessage called with:', message)
  console.log('🔍 Current state:', {
    message: message.trim(),
    isLoading: isLoading.value,
    conversationState: conversationState.value
  })
  
  if (!message.trim() || isLoading.value) {
    console.log('❌ Message rejected:', { isEmpty: !message.trim(), isLoading: isLoading.value })
    return
  }

  // Validate input if in gathering state using the composable's validation
  if (conversationState.value === 'gathering') {
    const validation = questionnaire.validateResponse(message)
    if (!validation.valid) {
      console.log('❌ Validation failed:', validation.error)
      // Show error message to user
      addMessage('assistant', `❌ ${validation.error}`)
      // Restore focus and wait for corrected input
      restoreInputFocus()
      return
    }
  }

  // Clear input and add user message
  currentInput.value = ''
  console.log('👤 Adding user message...')
  addMessage('user', message)
  
  // === FEATURE #10: EMERGENCY DETECTION ===
  const emergencyDetected = emergency.detectEmergency(message)
  if (emergencyDetected) {
    emergency.showAlert(emergencyDetected)
    // Still continue with normal flow but user has been warned
  }
  
  // Restore focus to input immediately after clearing
  restoreInputFocus()
  
  // Show typing indicator
  showTyping.value = true
  isLoading.value = true
  
  console.log('🤖 Processing message for state:', conversationState.value)

  try {
    if (conversationState.value === 'gathering') {
      console.log('📝 Handling gathering message...')
      // Store response in questionnaire for regular questions
      questionnaire.addResponse(message)
      await handleGatheringMessage()
    } else if (conversationState.value === 'awaiting-confirmation') {
      console.log('✅ Handling confirmation...')
      // Check if this is a "yes" response to proceed with diagnosis
      const isConfirmation = /^(yes|y|sure|ok|okay|proceed|go ahead|continue|let's go)$/i.test(message.trim())
      
      if (isConfirmation) {
        // User confirmed to proceed with diagnosis
        await handleProceedToDiagnosis()
      } else {
        // User declined or unclear response
        addMessage('assistant', "I understand. Would you like me to proceed with the health assessment analysis? Please respond with 'yes' when you're ready.")
      }
    } else if (conversationState.value === 'diagnosed') {
      console.log('💬 Handling follow-up message...')
      await handleFollowUpMessage(message)
    } else {
      console.log('🚨 Unknown state, treating as initial message')
      // If state is initial, start the conversation
      handleStart()
      // Then handle the message
      questionnaire.addResponse(message)
      await handleGatheringMessage()
    }
  } catch (err) {
    console.error('❌ Message handling failed:', err)
    handleError(err instanceof ApiError ? err.message : 'An unexpected error occurred. Please try again.')
  } finally {
    showTyping.value = false
    isLoading.value = false
    console.log('✅ Message handling complete')
    // Restore focus after assistant responds
    restoreInputFocus()
  }
}

/**
 * Handles gathering medical information through questions
 */
async function handleGatheringMessage() {
  // Wait a bit to simulate thinking
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  console.log('📋 Current question index:', questionnaire.currentQuestionIndex.value)
  console.log('📋 Total questions:', questionnaire.progress.value.total)

  const currentIndex = questionnaire.currentQuestionIndex.value
  const totalQuestions = questionnaire.progress.value.total
  
  // Check if we've completed all questionnaire questions
  if (questionnaire.isComplete.value || currentIndex >= totalQuestions) {
    // All questions completed - change state to awaiting confirmation
    conversationState.value = 'awaiting-confirmation'
    addMessage('assistant', 
      "Perfect! I now have all the information I need to provide you with a comprehensive health assessment.\n\n✅ **Medical interview completed**\n\nWould you like me to proceed with analyzing your symptoms and providing my assessment?"
    )
    currentStep.value = totalSteps.value
    return
  }
  
  // Get the next question from the composable
  const nextQuestion = questionnaire.getNextQuestion()
  if (nextQuestion) {
    console.log('❓ Asking question #' + currentIndex + ':', nextQuestion)
    
    // Check if this is the severity question
    const currentQuestion = questionnaire.currentQuestion.value
    if (currentQuestion && currentQuestion.id === 'severity') {
      // Show severity slider instead of regular input
      addMessage('assistant', nextQuestion)
      showSeveritySlider.value = true
      console.log('📊 Showing severity slider')
    } else {
      addMessage('assistant', nextQuestion)
    }
    
    currentStep.value = questionnaire.progress.value.current
  } else {
    // No more questions - this shouldn't happen but handle it
    console.warn('⚠️ Unexpected state: no question available but not complete')
    conversationState.value = 'awaiting-confirmation'
    addMessage('assistant', 
      "Thank you for providing that information. I have enough details to analyze your symptoms.\n\nWould you like me to proceed with the assessment?"
    )
  }
}

/**
 * Proceeds with medical diagnosis after questions are complete
 */
async function handleProceedToDiagnosis() {
  console.log('🩺 Starting diagnosis process...')
  isLoading.value = true
  showTyping.value = true
  conversationState.value = 'diagnosing'

  // Add thinking message
  addMessage('assistant', "🔍 Analyzing your symptoms and medical information...")

  try {
    // Extract all responses from questionnaire
    const responses = questionnaire.userResponses
    console.log('📋 Raw responses:', responses)
    
    // Parse age - extract number from response text
    let age = 30
    if (responses.age) {
      const ageMatch = responses.age.match(/\d+/)
      age = ageMatch ? parseInt(ageMatch[0]) : 30
    }
    
    const gender = responses.gender || 'unknown'
    const duration = responses.duration || 'recent'
    
    // Parse severity - extract number from response text
    let severity = 5
    if (responses.severity) {
      const severityMatch = responses.severity.match(/\d+/)
      severity = severityMatch ? parseInt(severityMatch[0]) : 5
    }
    
    // Build comprehensive symptoms description
    // Add body areas if selected
    let locationInfo = ''
    if (selectedBodyAreas.value.length > 0) {
      const areaNames = selectedBodyAreas.value
        .map(area => area.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '))
        .join(', ')
      locationInfo = `\n\nAffected Body Areas: ${areaNames}`
    }
    
    // Add image analysis if available
    let imageInfo = ''
    if (imageAnalysisResults.value.length > 0) {
      imageInfo = '\n\nImage Analysis:\n' + imageAnalysisResults.value
        .map((img, idx) => `Image ${idx + 1}: ${img.analysis}`)
        .join('\n')
    }
    
    // Build comprehensive symptom description including ALL conversation history
    const conversationSummary = chatMessages.value
      .filter(msg => msg.role === 'user' || msg.role === 'assistant')
      .map(msg => `${msg.role === 'user' ? 'Patient' : 'Doctor'}: ${msg.content}`)
      .join('\n\n')
    
    const symptomsText = [
      `Main Symptoms: ${responses.symptoms || 'Not specified'}`,
      `Duration: ${duration}`,
      `Severity: ${severity}/10`,
      `Medical History: ${responses.medical_history || 'None provided'}${locationInfo}${imageInfo}`,
      `\n--- COMPLETE MEDICAL INTERVIEW ---\n${conversationSummary}\n--- END INTERVIEW ---`
    ].join('\n\n')
    
    const diagnosisData = {
      symptoms: symptomsText,
      age: age,
      gender: gender,
      duration: duration,
      severity: severity,
      body_areas: selectedBodyAreas.value,
      has_images: imageAnalysisResults.value.length > 0,
      conversation_history: conversationSummary // Send full conversation for better diagnosis
    }

    console.log('🩺 Sending diagnosis request:', diagnosisData)
    console.log('📊 Extracted values - Age:', age, 'Gender:', gender, 'Severity:', severity)

    // Add timeout to prevent infinite waiting
    const timeoutPromise = new Promise((_, reject) => 
      setTimeout(() => reject(new Error('Diagnosis request timed out')), 30000)
    )

    const result = await Promise.race([
      diagnose(diagnosisData),
      timeoutPromise
    ])

    console.log('🩺 Diagnosis result received:', result)
    estimatedCost.value += result.estimated_cost || 0.05

    // Check if AI was used (estimated_cost > 0 means API key was used)
    if (result.estimated_cost > 0 && result.causes && result.causes.length > 0) {
      apiStatus.value = true // AI Enhanced Mode
    } else {
      apiStatus.value = false // Fallback Mode
    }

    // Remove thinking message and add diagnosis
    chatMessages.value.pop()
    
    const diagnosisMessage = result.answer || "I've analyzed your symptoms. Based on the information provided, I recommend consulting with a healthcare professional for proper evaluation."

    // Add the diagnosis message
    addMessage('assistant', diagnosisMessage)

    conversationState.value = 'diagnosed'
    
    // Store diagnosis data for dashboard immediately after diagnosis completes
    // Pass the structured data directly from the API response
    storeDiagnosisForDashboard(result)
    
    // Auto-redirect to dashboard after a brief delay to show diagnosis was received
    setTimeout(() => {
      console.log('🚀 Auto-redirecting to dashboard...')
      router.push('/dashboard').catch(err => {
        console.error('❌ Auto-redirect failed:', err)
      })
    }, 2000) // 2 second delay to let user see the diagnosis was completed

  } catch (err) {
    console.error('❌ Diagnosis failed:', err)
    
    // Remove thinking message
    if (chatMessages.value.length > 0 && chatMessages.value[chatMessages.value.length - 1].text.includes('Analyzing')) {
      chatMessages.value.pop()
    }
    
    // Store basic diagnosis data for dashboard even when API fails
    const fallbackDiagnosis = [{
      condition: "Medical Assessment Needed",
      confidence: 75,
      explanation: `Based on your symptoms: ${questionnaire.getAllResponses().substring(0, 100)}..., I recommend consulting with a healthcare professional for proper evaluation and diagnosis.`,
      finalPlan: {
        content: `1. Schedule an appointment with your primary care physician\n2. Bring a list of all symptoms and their duration\n3. Mention any medications or treatments you've tried\n4. Ask about any tests that might be needed`
      }
    }]
    localStorage.setItem('finalDiagnosis', JSON.stringify(fallbackDiagnosis))
    
    // Store conversation history
    const chatHistory = chatMessages.value.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text
    }))
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory))
    
    // Add error message but still set state to diagnosed so user can access dashboard
    addMessage('assistant', 
      "I apologize, but I'm having trouble processing your diagnosis right now. This could be due to a connection issue. However, I've prepared a basic assessment for you based on the information provided.\n\n**I recommend consulting with a healthcare professional for proper evaluation.** You can view your assessment summary below."
    )
    
    conversationState.value = 'diagnosed'
    
    // Auto-redirect to dashboard even on error so user can see basic assessment
    setTimeout(() => {
      console.log('🚀 Auto-redirecting to dashboard (fallback mode)...')
      router.push('/dashboard').catch(err => {
        console.error('❌ Auto-redirect failed:', err)
      })
    }, 2000)
  } finally {
    showTyping.value = false
    isLoading.value = false
    console.log('🩺 Diagnosis process completed')
    // Restore focus after diagnosis completes
    restoreInputFocus()
  }
}

/**
 * Handles follow-up questions after diagnosis
 */
async function handleFollowUpMessage(message) {
  // Wait a bit to simulate thinking
  await new Promise(resolve => setTimeout(resolve, 800))
  
  try {
    const result = await followup({
      question: message,
      previous_messages: chatMessages.value.slice(-10),
      original_symptoms: questionnaire.userResponses.symptoms || ''
    })

    estimatedCost.value += result.estimated_cost || 0.02
    addMessage('assistant', result.answer)
    
    // Play notification sound if enabled
    if (soundEnabled.value) {
      playNotificationSound()
    }
  } catch (err) {
    console.error('❌ Follow-up failed:', err)
    handleError(err instanceof ApiError ? err.message : 'Failed to process follow-up question. Please try again.')
  }
}

/**
 * Handles quick questions from predefined options
 */
function handleQuickQuestion(question) {
  currentInput.value = question
  handleSendMessage(question)
}

/**
 * Handles quick actions including navigation and questions
 */
/**
 * Handle image upload updates
 */
function handleImagesUpdated(images) {
  uploadedImages.value = images
  console.log('📸 Images updated:', images.length)
}

/**
 * Handle image analysis completion
 */
function handleImageAnalysisComplete(images) {
  console.log('✅ Image analysis complete for', images.length, 'images')
  
  // Store analysis results
  imageAnalysisResults.value = images
    .filter(img => img.analysis)
    .map(img => ({
      name: img.name,
      analysis: img.analysis
    }))
  
  // Add image analysis to chat
  if (imageAnalysisResults.value.length > 0) {
    const analysisText = imageAnalysisResults.value
      .map((result, index) => `📸 **Image ${index + 1} Analysis:**\n${result.analysis}`)
      .join('\n\n')
    
    addMessage('assistant', `I've analyzed your ${imageAnalysisResults.value.length} image(s):\n\n${analysisText}\n\nThis visual information will be included in your diagnosis.`)
  }
}

/**
 * Toggle body diagram visibility
 */
function toggleBodyDiagram() {
  showBodyDiagram.value = !showBodyDiagram.value
  
  if (showBodyDiagram.value) {
    addMessage('assistant', '👤 Please click on the body diagram to show me where your symptoms are located. You can select multiple areas.')
  }
}

/**
 * Handle body area selection changes
 */
function handleBodyAreasChanged(areas) {
  console.log('📍 Selected body areas:', areas)
  
  if (areas.length > 0) {
    const areaList = areas
      .map(area => area.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '))
      .join(', ')
    
    addMessage('assistant', `✅ Got it! You've indicated symptoms in: **${areaList}**. This will help me provide a more targeted diagnosis.`)
  }
}

/**
 * Toggle image upload visibility
 */
function toggleImageUpload() {
  showImageUpload.value = !showImageUpload.value
  
  if (showImageUpload.value) {
    addMessage('assistant', '📸 You can now upload photos of your symptoms. This will help me provide a more accurate diagnosis.')
  }
}

/**
 * Handle severity slider submission
 */
async function handleSeveritySubmit() {
  console.log('📊 Severity value submitted:', severityValue.value)
  
  showSeveritySlider.value = false
  
  // Add user message showing selected severity
  addMessage('user', `${severityValue.value}/10`)
  
  // Store the severity value
  questionnaire.addResponse(severityValue.value.toString())
  
  // Acknowledge the severity rating
  const severityText = severityValue.value <= 3 ? 'mild' : severityValue.value <= 5 ? 'moderate' : severityValue.value <= 7 ? 'significant' : severityValue.value <= 9 ? 'severe' : 'critical'
  addMessage('assistant', `✅ Thank you. I've noted your symptoms are at a **${severityText}** level (${severityValue.value}/10). This helps me understand the urgency of your situation.`)
  
  // Continue with next question
  await new Promise(resolve => setTimeout(resolve, 800))
  await handleGatheringMessage()
}

function handleQuickAction(action) {
  if (action.action === 'navigate' || action.action === 'manual-navigate') {
    // Always store diagnosis data before navigating
    storeDiagnosisForDashboard()
    
    console.log('🚀 Navigating to:', action.route)
    
    if (action.action === 'manual-navigate') {
      // Force direct navigation for debug
      window.location.href = action.route
    } else {
      // Use Vue router
      router.push(action.route).then(() => {
        console.log('✅ Navigation successful')
      }).catch(err => {
        console.error('❌ Navigation failed:', err)
        handleError('Failed to navigate to dashboard. Please try refreshing the page.')
      })
    }
  } else if (action.action === 'question') {
    // Handle as a regular question
    currentInput.value = action.text
    handleSendMessage(action.text)
  } else {
    // Default behavior - treat as question
    handleQuickQuestion(action.text || action.id)
  }
}

/**
 * Generate comprehensive holistic and alternative treatment options
 */
function generateHolisticOptions(diagnosis) {
  const condition = (diagnosis.condition || '').toLowerCase()
  const options = []
  
  // Dermatology conditions (rashes, itching, skin issues)
  if (condition.includes('dermatitis') || condition.includes('rash') || condition.includes('itch') || 
      condition.includes('eczema') || condition.includes('psoriasis')) {
    options.push('Skin examination: Visual assessment for signs of rash, redness, or fungal infection')
    options.push('Patch testing: If contact dermatitis is suspected, to identify potential allergens')
    options.push('KOH test: Microscopic examination to rule out fungal infection if tinea cruris is considered')
    options.push('Natural remedies: Apply aloe vera gel or coconut oil to soothe irritated skin')
    options.push('Oatmeal baths: Colloidal oatmeal soaks can reduce inflammation and itching')
    options.push('Tea tree oil: Diluted tea tree oil (5%) has antifungal and antibacterial properties')
    options.push('Dietary changes: Increase omega-3 fatty acids (fish, flaxseed) to reduce inflammation')
    options.push('Cotton clothing: Wear loose, breathable cotton underwear to reduce friction')
    options.push('Probiotics: Consider probiotic supplements to support skin health from within')
    options.push('Avoid irritants: Stop using scented soaps, detergents, or harsh chemicals on affected area')
  }
  
  // Eye conditions
  else if (condition.includes('eye') || condition.includes('vision') || condition.includes('vitreous') || 
           condition.includes('retina') || condition.includes('hemorrhage')) {
    options.push('Comprehensive eye examination: Including visual acuity, intraocular pressure, and fundoscopy')
    options.push('Optical coherence tomography (OCT): To assess retinal structure and detect bleeding')
    options.push('Fluorescein angiography: If retinal vascular issues are suspected')
    options.push('Bilberry extract: Rich in anthocyanins, may support retinal health and circulation')
    options.push('Lutein and zeaxanthin: Antioxidant supplements that protect eye tissues')
    options.push('Ginkgo biloba: May improve blood flow to the eyes (consult doctor first)')
    options.push('Vitamin A: Essential for eye health; found in carrots, sweet potatoes, and leafy greens')
    options.push('Rest eyes regularly: Follow 20-20-20 rule (every 20 min, look 20 feet away for 20 seconds)')
    options.push('Reduce eye strain: Adjust screen brightness, use proper lighting, take frequent breaks')
    options.push('Cold compress: Apply to closed eyes to reduce any inflammation or discomfort')
  }
  
  // Headache/Migraine
  else if (condition.includes('migraine') || condition.includes('headache')) {
    options.push('Neurological examination: To assess sensory and motor function')
    options.push('MRI or CT scan: If new onset or unusual symptoms, to rule out structural causes')
    options.push('Magnesium supplementation: 400-500mg daily may reduce migraine frequency')
    options.push('Feverfew herb: Traditional remedy for migraine prevention (75-100mg twice daily)')
    options.push('Butterbur extract: May reduce migraine frequency (use PA-free forms only)')
    options.push('Riboflavin (Vitamin B2): 400mg daily has shown benefit in migraine prevention')
    options.push('Coenzyme Q10: 100mg three times daily may help prevent migraines')
    options.push('Acupuncture: Evidence supports effectiveness for migraine prevention')
    options.push('Mindfulness meditation: Stress reduction can decrease migraine triggers')
    options.push('Identify triggers: Keep headache diary to track food, stress, sleep patterns')
  }
  
  // Joint/Knee conditions
  else if (condition.includes('arthritis') || condition.includes('joint') || condition.includes('knee')) {
    options.push('X-ray imaging: To assess joint space narrowing and bone changes')
    options.push('MRI: If soft tissue injury or early arthritis needs evaluation')
    options.push('Joint aspiration: Analysis of synovial fluid if infection or gout is suspected')
    options.push('Glucosamine and chondroitin: Joint support supplements (1500mg/1200mg daily)')
    options.push('Turmeric/Curcumin: Natural anti-inflammatory (500-1000mg with black pepper)')
    options.push('Omega-3 fatty acids: Fish oil reduces joint inflammation (2-3g EPA/DHA daily)')
    options.push('Gentle exercise: Swimming, tai chi, or yoga to maintain joint mobility')
    options.push('Weight management: Reduce stress on weight-bearing joints')
    options.push('Hot/cold therapy: Alternate to reduce pain and stiffness')
    options.push('Ginger tea: Natural anti-inflammatory that may reduce joint pain')
  }
  
  // Digestive/Abdominal issues
  else if (condition.includes('gastro') || condition.includes('abdom') || condition.includes('digest') ||
           condition.includes('stomach') || condition.includes('intestin')) {
    options.push('Stool analysis: To check for infections, parasites, or inflammation markers')
    options.push('Endoscopy: If persistent symptoms or alarm features present')
    options.push('Food sensitivity testing: To identify potential dietary triggers')
    options.push('Probiotics: Multi-strain supplement to restore gut flora balance')
    options.push('Peppermint oil: Enteric-coated capsules for IBS symptoms')
    options.push('Ginger: Natural remedy for nausea and digestive discomfort')
    options.push('Chamomile tea: Soothing for digestive upset and inflammation')
    options.push('Elimination diet: Temporarily remove common triggers (dairy, gluten, etc.)')
    options.push('Fiber supplementation: Psyllium husk or ground flaxseed for regularity')
    options.push('Stress management: Yoga, meditation, or breathing exercises for gut-brain connection')
  }
  
  // Respiratory conditions
  else if (condition.includes('respiratory') || condition.includes('lung') || condition.includes('breath') ||
           condition.includes('asthma') || condition.includes('bronch')) {
    options.push('Chest X-ray: To evaluate lung fields and rule out infection or structural issues')
    options.push('Pulmonary function tests: To assess lung capacity and airflow')
    options.push('Peak flow monitoring: Daily tracking of breathing capacity')
    options.push('Steam inhalation: With eucalyptus oil to open airways and reduce congestion')
    options.push('Breathing exercises: Pursed-lip breathing and diaphragmatic breathing techniques')
    options.push('N-acetylcysteine (NAC): Mucolytic supplement that thins mucus (600mg twice daily)')
    options.push('Vitamin D: Adequate levels support immune function (test and supplement if low)')
    options.push('Honey and lemon: Natural remedy for cough and throat irritation')
    options.push('Air quality: Use HEPA filter, avoid smoke and allergens')
    options.push('Hydration: Drink plenty of fluids to thin mucus and support respiratory function')
  }
  
  // General/Fallback options
  else {
    options.push('Comprehensive physical examination: To assess overall health status')
    options.push('Blood work: Complete blood count, metabolic panel, and relevant markers')
    options.push('Adequate sleep: Aim for 7-9 hours nightly to support healing and immune function')
    options.push('Balanced nutrition: Focus on whole foods, fruits, vegetables, and lean proteins')
    options.push('Hydration: Drink 8-10 glasses of water daily for optimal body function')
    options.push('Stress reduction: Practice meditation, deep breathing, or progressive muscle relaxation')
    options.push('Regular exercise: 30 minutes of moderate activity most days of the week')
    options.push('Vitamin D3: Supplement if deficient (2000-4000 IU daily)')
    options.push('Quality multivitamin: Fill nutritional gaps with a comprehensive daily supplement')
    options.push('Mind-body practices: Consider yoga, tai chi, or qigong for overall wellness')
  }
  
  return options
}

/**
 * Stores current diagnosis data in localStorage for dashboard
 */
function storeDiagnosisForDashboard(apiResult = null) {
  try {
    console.log('💾 Storing diagnosis for dashboard with API result:', apiResult ? 'YES' : 'NO')
    
    let dashboardData = []
    let treatmentSteps = []
    let holisticOptions = []
    
    // If we have structured API result, use it directly (preferred method)
    if (apiResult && apiResult.causes && apiResult.causes.length > 0) {
      console.log('✅ Using structured API data - causes count:', apiResult.causes.length)
      
      // Convert API causes to dashboard format
      dashboardData = apiResult.causes.map(cause => ({
        condition: cause.cause || cause.condition || 'Unknown Condition',
        confidence: cause.value || cause.confidence || 0,
        urgency: cause.urgency || 'routine',
        specialty: cause.specialty || 'Primary Care',
        explanation: cause.explanation || 'Assessment based on clinical symptoms and patient history.'
      }))
      
      // Extract treatment steps from additional_questions or red_flags
      if (apiResult.red_flags && apiResult.red_flags.length > 0) {
        treatmentSteps.push('⚠️ Warning Signs:')
        treatmentSteps.push(...apiResult.red_flags)
      }
      
      // Extract diagnostic tests as holistic options
      if (apiResult.recommended_tests && apiResult.recommended_tests.length > 0) {
        holisticOptions = apiResult.recommended_tests
      }
      
      console.log('📊 Dashboard data from API:', dashboardData.length, 'diagnoses')
    } 
    // Fallback: Try to parse from diagnosis message text
    else {
      console.log('⚠️ No API result, falling back to text parsing')
      
      // Find the diagnosis message in chat
      let diagnosisMessage = chatMessages.value.find(msg => 
        (msg.sender === 'assistant' || msg.role === 'assistant') && 
        (msg.text || msg.content) && 
        (msg.text?.length > 100 || msg.content?.length > 100) && 
        !msg.text?.includes('Analyzing') &&
        (msg.text?.includes('Differential diagnosis') || msg.content?.includes('Differential diagnosis'))
      )
      
      console.log('🔍 Found diagnosis message:', diagnosisMessage ? 'YES' : 'NO')
      
      // Get the text content from either msg.text or msg.content
      const text = diagnosisMessage?.text || diagnosisMessage?.content
      
      if (text) {
        console.log('📝 Diagnosis text length:', text.length)
        console.log('📝 First 500 chars:', text.substring(0, 500))
        
        // Look for "Differential diagnosis:" section - be more flexible with ending
        const diffDiagSection = text.match(/Differential diagnosis[s]?:([\s\S]*?)(?=Additional information|Suggested diagnostic|Clinical recommendations|Urgency:|Assessment summary:|$)/i)
      
      if (diffDiagSection) {
        console.log('✅ Found Differential diagnosis section')
        const diagnosisText = diffDiagSection[1]
        console.log('📝 Diagnosis section text (first 500):', diagnosisText.substring(0, 500))
        
        // Use regex to match complete diagnosis entries including multiline clinical reasoning
        // Pattern: 1. Name — Confidence: 85% — Urgency: routine — Specialty: Primary Care
        //             Clinical reasoning: ...text...
        const diagnosisPattern = /(\d+)\.\s+([^\n—]+?)\s*—\s*Confidence:\s*(\d+)%\s*—\s*Urgency:\s*(\w+)\s*—\s*Specialty:\s*([^\n]+?)(?:\n\s*Clinical reasoning:\s*([^\n]+(?:\n(?!\d+\.)[^\n]+)*))?/gi
        
        let match
        while ((match = diagnosisPattern.exec(diagnosisText)) !== null) {
          const condition = match[2].trim()
          const confidence = parseInt(match[3])
          const urgency = match[4].trim()
          const specialty = match[5].trim()
          const explanation = match[6] ? match[6].trim() : 'Assessment based on clinical symptoms and patient history.'
          
          console.log('✅ Matched diagnosis:', condition, confidence + '%', urgency, specialty)
          
          dashboardData.push({
            condition,
            confidence,
            urgency,
            specialty,
            explanation
          })
        }
        
          console.log('📊 Total matched:', dashboardData.length)
        } else {
          console.log('❌ Could not find Differential diagnosis section')
        }
        
        console.log('📊 Parsed diagnoses count:', dashboardData.length)
        
        // Extract treatment recommendations
        const recommendationsMatch = text.match(/Clinical recommendations:([\s\S]*?)(?=\n\n|Urgency:|$)/i)
        if (recommendationsMatch) {
          const recs = recommendationsMatch[1].match(/- (.+?)(?=\n|$)/g)
          if (recs) {
            treatmentSteps = recs.map(r => r.replace(/^-\s*/, '').trim())
          }
        }
        
        // Extract diagnostic tests as holistic options
        const testsMatch = text.match(/Suggested diagnostic tests:([\s\S]*?)(?=\n\n|Clinical recommendations:|$)/i)
        if (testsMatch) {
          const tests = testsMatch[1].match(/- (.+?)(?=\n|$)/g)
          if (tests) {
            holisticOptions = tests.map(t => t.replace(/^-\s*/, '').trim())
          }
        }
      }
    } // End of fallback else block
    
    // Generate comprehensive holistic options if none exist
    if (holisticOptions.length === 0 && dashboardData.length > 0) {
      holisticOptions = generateHolisticOptions(dashboardData[0])
    }
    
    // Fallback if no diagnoses were parsed
    if (dashboardData.length === 0) {
      const symptoms = questionnaire.getAllResponses()
      dashboardData = [{
        condition: "Health Assessment Complete",
        confidence: 80,
        urgency: "routine",
        specialty: "Primary Care",
        explanation: `Based on your reported symptoms and medical history, a comprehensive evaluation by a healthcare professional is recommended for proper diagnosis and treatment planning.`
      }]
      
      treatmentSteps = [
        "1. Schedule an appointment with your primary care physician",
        "2. Bring a list of all symptoms and their duration",
        "3. Mention any medications or treatments you've tried",
        "4. Ask about any tests that might be needed"
      ]
    }
    
    // Generate treatment plan based on top diagnosis if not already set
    if (treatmentSteps.length === 0 && dashboardData.length > 0) {
      const topDiagnosis = dashboardData[0]
      const urgency = topDiagnosis.urgency || 'routine'
      const specialty = topDiagnosis.specialty || 'Primary Care'
      
      treatmentSteps = []
      
      // Step 1: Urgency-based first action
      if (urgency === 'urgent') {
        treatmentSteps.push('1. Seek immediate medical attention at an emergency room or urgent care facility')
      } else if (urgency === 'soon') {
        treatmentSteps.push('1. Schedule an appointment with your healthcare provider within 24-48 hours')
      } else {
        treatmentSteps.push('1. Schedule an appointment with your primary care physician or ' + specialty + ' specialist')
      }
      
      // Step 2: Documentation
      treatmentSteps.push('2. Document all symptoms with dates, severity, and any patterns or triggers')
       
      // Step 3: Information to bring
      treatmentSteps.push('3. Bring a complete list of current medications, supplements, and allergies')
      
      // Step 4: Diagnosis-specific advice
      if (apiResult && apiResult.recommended_tests && apiResult.recommended_tests.length > 0) {
        treatmentSteps.push('4. Ask your doctor about recommended diagnostic tests: ' + apiResult.recommended_tests[0])
      } else {
        treatmentSteps.push('4. Ask about diagnostic tests or examinations that could confirm the diagnosis')
      }
      
      // Step 5: Monitoring
      treatmentSteps.push('5. Monitor your symptoms closely and seek care sooner if they worsen')
    }
    
    // Add treatment and holistic options to first diagnosis item
    if (dashboardData.length > 0) {
      dashboardData[0].finalPlan = {
        content: treatmentSteps.join('\n')
      }
      dashboardData[0].holisticOptions = holisticOptions
    }
    
    // Sanitize any HTML-like content in finalPlan before storing to avoid many <br> tags
    const sanitizeHtmlToText = (html) => {
      if (!html || typeof html !== 'string') return html
      let txt = html
      // Remove <style> blocks entirely (and any CSS inside)
      txt = txt.replace(/<style[\s\S]*?<\/style>/gi, '')
      // Remove link tags that may reference stylesheets
      txt = txt.replace(/<link[^>]*>/gi, '')
      // Replace <br> tags with newlines
      txt = txt.replace(/<br\s*\/?\>/gi, '\n')
      // Strip remaining HTML tags
      txt = txt.replace(/<[^>]+>/g, '')
      // Collapse 3+ blank lines into two newlines
      txt = txt.replace(/(\n\s*){3,}/g, '\n\n')
      // Trim trailing/leading whitespace
      return txt.trim()
    }

    // Apply sanitization to all string fields in each diagnosis item to remove CSS and HTML
    const sanitizeItem = (item) => {
      const out = { ...item }
      if (out.condition && typeof out.condition === 'string') {
        out.condition = sanitizeHtmlToText(out.condition)
      }
      if (out.explanation && typeof out.explanation === 'string') {
        out.explanation = sanitizeHtmlToText(out.explanation)
      }
      if (out.finalPlan && out.finalPlan.content && typeof out.finalPlan.content === 'string') {
        out.finalPlan = { ...out.finalPlan, content: sanitizeHtmlToText(out.finalPlan.content) }
      }
      return out
    }

    dashboardData = dashboardData.map(sanitizeItem)

    // Store in localStorage
    localStorage.setItem('finalDiagnosis', JSON.stringify(dashboardData))
    
    // Also store chat history
    const chatHistory = chatMessages.value.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text
    }))
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory))

    // Store patient information directly for dashboard
    const responses = questionnaire.userResponses
    const patientInfo = {
      age: responses.age || '30',
      gender: responses.gender || 'unknown',
      symptoms: responses.symptoms || 'Not specified',
      duration: responses.duration || 'recent',
      severity: responses.severity || '5/10',
      medicalHistory: responses.medical_history || 'None provided'
    }
    localStorage.setItem('patientInfo', JSON.stringify(patientInfo))
    console.log('👤 Saved patient info:', patientInfo)

    // Store selected body areas for pain location diagram
    if (selectedBodyAreas.value && selectedBodyAreas.value.length > 0) {
      localStorage.setItem('selectedBodyAreas', JSON.stringify(selectedBodyAreas.value))
      console.log('🗺️ Saved body areas:', selectedBodyAreas.value)
    }
    
    // === FEATURE #3: HEALTH HISTORY TIMELINE ===
    // Store this diagnosis in the history timeline
    const diagnosisRecord = {
      timestamp: new Date().toISOString(),
      diagnoses: dashboardData,
      symptoms: questionnaire.getAllResponses(),
      age: questionnaire.userResponses.age || 'Not specified',
      gender: questionnaire.userResponses.gender || 'Not specified',
      urgency: dashboardData[0]?.urgency || 'routine',
      chatHistory: chatHistory
    }
    
    // Load existing history and add new diagnosis
    let diagnosisHistory = []
    try {
      const existingHistory = localStorage.getItem('diagnosisHistory')
      if (existingHistory) {
        diagnosisHistory = JSON.parse(existingHistory)
      }
    } catch (e) {
      console.error('❌ Error loading diagnosis history:', e)
    }
    
    // Add new diagnosis at the beginning (newest first)
    diagnosisHistory.unshift(diagnosisRecord)
    
    // Keep only last 50 diagnoses to prevent localStorage from growing too large
    if (diagnosisHistory.length > 50) {
      diagnosisHistory = diagnosisHistory.slice(0, 50)
    }
    
    // Save updated history
    localStorage.setItem('diagnosisHistory', JSON.stringify(diagnosisHistory))
    console.log('📊 Diagnosis data stored for dashboard:', dashboardData)
    console.log('📈 Diagnosis history updated. Total records:', diagnosisHistory.length)
    
  } catch (error) {
    console.error('❌ Error storing diagnosis data:', error)
  }
}

// === VOICE FUNCTIONS ===

/**
 * Toggles voice recording enabled/disabled
 */
function toggleVoiceEnabled(enabled) {
  voiceEnabled.value = enabled
  if (!enabled && voice.isRecording.value) {
    stopVoiceRecording()
  }
}

/**
 * Toggles voice recording
 */
async function toggleVoiceRecording() {
  if (!voiceEnabled.value) {
    handleError('Voice recording is disabled. Please enable it in settings.')
    return
  }

  if (voice.isRecording.value) {
    stopVoiceRecording()
  } else {
    await startVoiceRecording()
  }
}

/**
 * Starts voice recording
 */
async function startVoiceRecording() {
  console.log('🎙️ Starting voice recording...')

  if (!voice.isSupported.value) {
    console.warn('⚠️ Voice recording not supported')
    handleError('Voice recording is not supported in your browser.')
    voice.voiceEnabled.value = false
    return
  }

  // Check if already recording
  if (voice.isRecording.value) {
    console.warn('⚠️ Already recording')
    return
  }

  // Use voice composable's startRecording with callbacks
  await voice.startRecording(
    // onResult callback - called when speech is recognized
    (transcript) => {
      console.log('✅ Voice recognized:', transcript)
      if (transcript && transcript.trim()) {
        handleSendMessage(transcript.trim())
      }
    },
    // onError callback - called on error
    (errorMessage) => {
      console.error('❌ Voice recording error:', errorMessage)
      handleError(errorMessage)
    }
  )
}

/**
 * Stops voice recording
 */
function stopVoiceRecording() {
  console.log('⏹️ Stopping voice recording...')
  // Voice composable handles all cleanup internally
  voice.stopRecording()
  console.log('✅ Voice recording stopped via composable')
}

/**
 * Handles voice recognition result
 */
function handleVoiceResult(transcript) {
  currentInput.value = transcript
  voice.isRecording.value = false
}

// === UTILITY FUNCTIONS ===

/**
 * Gets quick actions for current state
 */
function getQuickActions() {
  if (conversationState.value === 'gathering' && !questionnaire.isComplete) {
    return []
  }
  return []
}

/**
 * Handles settings changes from settings panel
 */
function handleSettingsChange(settings) {
  if (settings.voiceInput !== undefined) {
    voiceEnabled.value = settings.voiceInput
  }
  if (settings.autoScroll !== undefined) {
    autoScroll.value = settings.autoScroll
  }
  if (settings.soundEffects !== undefined) {
    soundEnabled.value = settings.soundEffects
  }
}

/**
 * Gets progress title based on current state
 */
function getProgressTitle() {
  switch (conversationState.value) {
    case 'gathering':
      return 'Collecting Information'
    case 'diagnosing':
      return 'Analyzing Symptoms'
    case 'diagnosed':
      return 'Assessment Complete'
    default:
      return 'Getting Started'
  }
}

/**
 * Gets progress message based on current state
 */
function getProgressMessage() {
  switch (conversationState.value) {
    case 'gathering':
      return `Gathering medical information (${questionnaire.progress.value.current}/${questionnaire.progress.value.total})`
    case 'diagnosing':
      return 'Processing your symptoms and generating health insights...'
    case 'diagnosed':
      return 'Your health assessment is ready. Feel free to ask follow-up questions.'
    default:
      return 'Ready to begin your health assessment'
  }
}

/**
 * Adds a message to the chat
 */
function addMessage(role, content, additionalData = {}) {
  console.log('💬 addMessage called:', { role, content, additionalData })
  console.log('📊 Current chatMessages length before:', chatMessages.value.length)
  // Sanitize message content to remove HTML <br> tags and collapse excessive blank lines
  const sanitizeMessage = (txt) => {
    if (!txt || typeof txt !== 'string') return txt
    // Replace <br> with newlines
    let t = txt.replace(/<br\s*\/?\>/gi, '\n')
    // Remove other HTML tags
    t = t.replace(/<[^>]+>/g, '')
    // Collapse 3+ blank lines to two
    t = t.replace(/(\n\s*){3,}/g, '\n\n')
    return t.trim()
  }

  const cleanContent = sanitizeMessage(content)

  // Use chat composable to add message
  const message = chat.addMessage(cleanContent, role, additionalData)
  console.log('📊 Message added via composable:', message)
  console.log('📊 Total messages now:', chat.messages.value.length)
  
  // Speak message if it's from assistant and sound is enabled
  if (role === 'assistant' && soundEnabled.value) {
    console.log('🔊 Attempting to speak message, soundEnabled:', soundEnabled.value)
    // Small delay to ensure message is rendered
    setTimeout(() => {
      voice.speak(cleanContent) // Use cleaned content
    }, 300) // Increased delay for better reliability
  } else {
    console.log('🔇 Not speaking:', {
      isAssistant: role === 'assistant',
      soundEnabled: soundEnabled.value,
      role: role
    })
  }
}

// speakMessage function removed - now using voice.speak() from composable

/**
 * Plays a notification sound
 */
function playNotificationSound() {
  // Create a simple notification sound
  const audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const oscillator = audioContext.createOscillator()
  const gainNode = audioContext.createGain()
  
  oscillator.connect(gainNode)
  gainNode.connect(audioContext.destination)
  
  oscillator.frequency.setValueAtTime(800, audioContext.currentTime)
  oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1)
  
  gainNode.gain.setValueAtTime(0, audioContext.currentTime)
  gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.01)
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2)
  
  oscillator.start(audioContext.currentTime)
  oscillator.stop(audioContext.currentTime + 0.2)
}

/**
 * Scrolls chat to bottom
 */
function scrollToBottom() {
  if (chatAreaRef.value && chatAreaRef.value.scrollToBottom) {
    chatAreaRef.value.scrollToBottom()
  }
}

/**
 * Extracts age from responses
 */
function extractAge() {
  const responses = Object.values(questionnaire.userResponses).join(' ')
  const ageMatch = responses.match(/\b(\d{1,3})\b/)
  return ageMatch ? parseInt(ageMatch[1]) : null
}

/**
 * Extracts gender from responses
 */
function extractGender() {
  const responses = Object.values(questionnaire.userResponses).join(' ').toLowerCase()
  if (responses.includes('male') && !responses.includes('female')) return 'male'
  if (responses.includes('female')) return 'female'
  return 'unknown'
}

/**
 * Extracts severity from responses
 */
function extractSeverity() {
  const responses = Object.values(questionnaire.userResponses).join(' ')
  const severityMatch = responses.match(/\b([1-9]|10)\b/)
  return severityMatch ? parseInt(severityMatch[1]) : null
}

/**
 * Handles errors by displaying them to the user
 */
function handleError(message) {
  error.value = message
  console.error('❌ Error:', message)
  
  // Auto-clear error after 8 seconds
  setTimeout(() => {
    if (error.value === message) {
      error.value = null
    }
  }, 8000)
}

/**
 * Clears the current error
 */
function clearError() {
  error.value = null
}

/**
 * Navigate to API key setup page
 */
function goToApiSettings() {
  router.push('/setup')
}

/**
 * Test speech synthesis
 */
function testSpeech() {
  console.log('🔊 Testing speech synthesis...')
  if (window.speechSynthesis) {
    const utterance = new SpeechSynthesisUtterance('Hello, I am your AI health assistant. I can speak to you.')
    utterance.rate = 1.0
    utterance.pitch = 1.0
    utterance.volume = 1.0
    window.speechSynthesis.speak(utterance)
    console.log('🔊 Test speech triggered')
  } else {
    console.error('❌ Speech synthesis not available')
  }
}

// Make test function available globally for debugging
if (import.meta.env.DEV) {
  window.testSpeech = testSpeech
}

/**
 * Resets the entire conversation
 */
function handleStartOver() {
  // Confirm if user really wants to start over
  if (chatMessages.value.length > 0) {
    if (!confirm('Are you sure you want to start over? This will clear your current conversation.')) {
      return
    }
  }
  
  chatMessages.value = []
  currentInput.value = ''
  hasStarted.value = false
  conversationState.value = 'initial'
  questionnaire.reset()
  error.value = null
  currentStep.value = 0
  showTyping.value = false
  
  // Stop any ongoing voice recording
  if (voice.isRecording.value) {
    stopVoiceRecording()
  }
  
  console.log('🔄 Conversation reset')
}

// Export for debugging
if (import.meta.env.DEV) {
  window.voiceDiagnosisDebug = {
    questionnaire,
    chatMessages,
    conversationState,
    handleStartOver,
    handleError
  }
}
</script>

<style scoped>
/* ====================================
   VOICE DIAGNOSIS - ACCESSIBLE THEME STYLES
   ==================================== */

/* Light Mode - LIGHT 2 Design */
/* ====================================
   MAIN CONTAINER - THEME AWARE
   ==================================== */

.voice-diagnosis-container {
  background: var(--bg) !important;
  color: var(--text) !important;
  transition: background 0.3s ease, color 0.3s ease;
}

/* Dark Mode - Explicit styling */
:root[data-theme="dark"] .voice-diagnosis-container,
.dark .voice-diagnosis-container {
  background: var(--bg) !important;
  color: var(--text) !important;
}

/* Header Styles - Light Mode (LIGHT 2) */
.header-bar {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  box-shadow: var(--shadow-sm);
}

.header-title {
  color: #212529;
}

/* ====================================
   HEADER STYLES - MAXIMUM VISIBILITY
   ==================================== */

.header-title {
  color: #ffffff !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8) !important;
}

.header-subtitle {
  color: #e2e8f0 !important;
}

/* Header Bar - Maximum visibility */
.header-bar {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
  border-bottom: 1px solid #475569 !important;
  color: #ffffff !important;
}

/* Force maximum contrast in dark mode */
:root[data-theme="dark"] .header-bar,
.dark .header-bar {
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
  border-bottom: 1px solid #475569 !important;
  color: #ffffff !important;
}

:root[data-theme="dark"] .header-title,
.dark .header-title {
  color: #ffffff !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8) !important;
}

:root[data-theme="dark"] .header-subtitle,
.dark .header-subtitle {
  color: #e2e8f0 !important;
}

/* Force all header text to be bright */
:root[data-theme="dark"] .header-bar *,
.dark .header-bar * {
  color: #ffffff !important;
}

:root[data-theme="dark"] .header-bar .text-xs,
.dark .header-bar .text-xs {
  color: #e2e8f0 !important;
}

/* ====================================
   DARK MODE TEXT ELEMENTS - CSS VARIABLES
   ==================================== */

/* Dark mode - All header text elements using CSS variables */
:root[data-theme="dark"] .header-bar .status-success,
:root[data-theme="dark"] .header-bar .status-warning,
:root[data-theme="dark"] .header-bar .text-muted,
.dark .header-bar .status-success,
.dark .header-bar .status-warning,
.dark .header-bar .text-muted {
  color: var(--text-muted) !important;
}

:root[data-theme="dark"] .header-bar .text-secondary,
.dark .header-bar .text-secondary {
  color: var(--text-muted) !important;
}

:root[data-theme="dark"] .header-bar svg,
.dark .header-bar svg {
  color: var(--text) !important;
}

/* Global text-muted class */
.text-muted {
  color: var(--text-muted) !important;
}

/* ====================================
   COMPREHENSIVE DARK MODE SUPPORT
   ==================================== */

/* Ensure all text is visible in dark mode */
:root[data-theme="dark"],
.dark {
  color: var(--text) !important;
}

:root[data-theme="dark"] *,
.dark * {
  color: inherit;
}

/* Force important text visibility in dark mode */
:root[data-theme="dark"] h1,
:root[data-theme="dark"] h2,
:root[data-theme="dark"] h3,
:root[data-theme="dark"] p,
:root[data-theme="dark"] span,
:root[data-theme="dark"] div,
.dark h1,
.dark h2,
.dark h3,
.dark p,
.dark span,
.dark div {
  color: var(--text) !important;
}

/* Ensure status indicators are visible */
:root[data-theme="dark"] .status-success,
.dark .status-success {
  color: var(--success) !important;
}

:root[data-theme="dark"] .status-warning,
.dark .status-warning {
  color: var(--warning) !important;
}

.settings-btn {
  background: rgba(255, 255, 255, 0.1);
}

:root[data-theme="dark"] .settings-btn {
  background: var(--surface-2);
}

.settings-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

:root[data-theme="dark"] .settings-btn:hover {
  background: var(--surface);
}

/* ====================================
   EMERGENCY ALERT - ACCESSIBLE COLORS
   ==================================== */
.emergency-alert-banner {
  animation: slide-down 0.4s ease-out, pulse-emergency 2s ease-in-out infinite;
  box-shadow: var(--shadow-xl), 0 0 30px rgba(220, 38, 38, 0.4);
}

/* Light mode emergency banner */
.emergency-alert-banner {
  background-color: #c62828 !important; /* WCAG AAA compliant red */
  border-color: #8e0000 !important;
}

/* Dark mode emergency banner */
:root[data-theme="dark"] .emergency-alert-banner {
  background-color: #b71c1c !important;
  border-color: #7f0000 !important;
}

@keyframes slide-down {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes pulse-emergency {
  0%, 100% {
    box-shadow: 0 10px 40px rgba(220, 38, 38, 0.5);
  }
  50% {
    box-shadow: 0 10px 60px rgba(220, 38, 38, 0.8);
  }
}

.animate-pulse-emergency {
  animation: pulse-emergency 2s ease-in-out infinite;
}

/* ====================================
   RESPONSIVE & ACCESSIBILITY
   ==================================== */

/* Focus visible for keyboard navigation */
:global(*:focus-visible) {
  outline: 2px solid var(--color-focus-ring);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .voice-diagnosis-container {
    border: 2px solid var(--color-border-strong);
  }
}
</style>