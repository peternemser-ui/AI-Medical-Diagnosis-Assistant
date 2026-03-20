<template>
  <div class="min-h-screen flex flex-col transition-colors duration-300"
    :class="isDark
      ? 'bg-gradient-to-br from-slate-950 via-slate-900 to-gray-900 text-white'
      : 'bg-gradient-to-br from-slate-50 via-white to-slate-100 text-slate-900'"
  >
    <!-- Header -->
    <div class="backdrop-blur-xl border-b py-3 px-4 sm:px-6 flex justify-between items-center transition-colors duration-300"
      :class="isDark ? 'bg-slate-950/90 border-slate-800/50' : 'bg-white/90 border-slate-200'"
    >
      <!-- Left: Brand + Home link -->
      <div class="flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-md shadow-blue-500/15 group-hover:shadow-blue-500/25 transition-shadow">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
            </svg>
          </div>
          <span class="text-base font-semibold hidden sm:inline transition-colors" :class="isDark ? 'text-white group-hover:text-blue-300' : 'text-slate-900 group-hover:text-blue-600'">{{ t('nav.brand') }}</span>
        </router-link>

        <!-- Divider + Status (desktop) -->
        <div class="hidden sm:flex items-center gap-3">
          <div class="w-px h-5" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
          <router-link to="/settings" v-if="apiStatus === true" class="flex items-center text-xs bg-emerald-500/10 text-emerald-400 px-3 py-1 rounded-full border border-emerald-500/15 gap-1.5 hover:bg-emerald-500/20 transition-colors cursor-pointer" title="Click to change AI model">
            <div class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></div>
            {{ activeProvider === 'anthropic' ? 'Claude' : 'GPT-4o' }} {{ t('nav.connected') }}
            <svg class="w-3 h-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </router-link>
          <div v-else-if="apiStatus === false" class="flex items-center text-xs bg-amber-500/10 text-amber-400 px-3 py-1 rounded-full border border-amber-500/15 gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-amber-400"></div>
            {{ t('nav.basicMode') }}
          </div>
        </div>
      </div>

      <!-- Right: Labeled action buttons -->
      <div class="flex items-center gap-2">
        <!-- New consultation -->
        <button
          @click="handleStartOver"
          class="hidden sm:flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm transition-all"
          :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800/60' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-200/60'"
        >
          <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          <span>{{ t('nav.new') }}</span>
        </button>

        <button
          @click="showHistory = true"
          class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm transition-all"
          :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800/60' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-200/60'"
        >
          <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="hidden sm:inline">{{ t('nav.history') }}</span>
        </button>

        <button
          @click="avatarMode = !avatarMode"
          class="flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm transition-all"
          :class="avatarMode
            ? 'bg-blue-500/15 text-blue-400 border border-blue-500/20'
            : (isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800/60' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-200/60')"
        >
          <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          <span class="hidden sm:inline">{{ avatarMode ? t('nav.avatar') : t('nav.chat') }}</span>
        </button>

        <!-- Divider -->
        <div class="w-px h-6 mx-0.5" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>

        <ThemeLangControls />

        <button
          @click="goToApiSettings"
          class="p-2.5 rounded-lg transition-all"
          :class="isDark ? 'text-slate-500 hover:text-white hover:bg-slate-800/60' : 'text-slate-400 hover:text-slate-800 hover:bg-slate-200/60'"
          :title="t('nav.settings')"
          :aria-label="t('nav.settings')"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Agent Pipeline - shown during diagnosis -->
    <AgentPipelineIndicator
      v-if="conversationState === 'diagnosing'"
      :active-agent="activeAgent"
      :completed-agents="completedAgents"
      :agent-timings="agentTimings"
      :total-time="diagnosisElapsed"
    />

    <!-- Agent Status Board - detailed real-time status during diagnosis -->
    <AgentStatusBoard
      v-if="conversationState === 'diagnosing'"
      :active-agent="activeAgent"
      :completed-agents="completedAgents"
      :agent-timings="agentTimings"
      :agent-findings="agentFindings"
      :errors="agentErrors"
    />

    <!-- Progress Indicator - shown during gathering -->
    <ProgressIndicator
      v-if="conversationState === 'gathering' || conversationState === 'awaiting-confirmation'"
      :visible="true"
      :progress="progressPercentage"
      :current-step="currentStep"
      :steps="progressSteps"
      :title="getProgressTitle()"
      :message="getProgressMessage()"
    />

    <!-- ══════ AVATAR MODE ══════ -->
    <div v-if="avatarMode" class="flex-1 flex flex-col min-h-0 pb-28 relative overflow-hidden">
      <!-- Ambient glow -->
      <div class="absolute inset-0 flex items-center justify-center pointer-events-none" style="top: -10%">
        <div
          class="w-[600px] h-[600px] rounded-full blur-[150px] opacity-15 transition-colors duration-1000"
          :style="{ backgroundColor: doctorAvatar.bgColor }"
        ></div>
      </div>

      <!-- Top: Avatar area (reduced to give more room to chat) -->
      <div class="flex-[1.2] flex flex-col items-center justify-center relative z-10">
        <!-- Avatar (extra large) -->
        <div class="relative cursor-pointer" @click="showAvatarCustomizer = true" title="Click to customize">
          <DoctorAvatar :avatar="doctorAvatar" :speaking="isSpeakingAnimating" :size="avatarSize" :show-name="false" />
          <!-- Sound waves when speaking -->
          <div v-if="isSpeakingAnimating" class="absolute -left-8 top-1/2 -translate-y-1/2 flex flex-col gap-1.5">
            <div class="w-5 h-1.5 bg-blue-400/60 rounded-full animate-pulse" style="animation-delay:0s"></div>
            <div class="w-8 h-1.5 bg-blue-400/40 rounded-full animate-pulse" style="animation-delay:0.2s"></div>
            <div class="w-4 h-1.5 bg-blue-400/50 rounded-full animate-pulse" style="animation-delay:0.4s"></div>
          </div>
          <div v-if="isSpeakingAnimating" class="absolute -right-8 top-1/2 -translate-y-1/2 flex flex-col gap-1.5">
            <div class="w-4 h-1.5 bg-blue-400/50 rounded-full animate-pulse" style="animation-delay:0.1s"></div>
            <div class="w-8 h-1.5 bg-blue-400/40 rounded-full animate-pulse" style="animation-delay:0.3s"></div>
            <div class="w-5 h-1.5 bg-blue-400/60 rounded-full animate-pulse" style="animation-delay:0.5s"></div>
          </div>
        </div>
        <!-- Doctor name -->
        <div class="mt-2 text-center">
          <div class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ doctorAvatar.name }}</div>
          <div class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ doctorAvatar.specialty }}</div>
          <button @click="showAvatarCustomizer = true" class="mt-0.5 text-[10px] transition-colors" :class="isDark ? 'text-blue-400/50 hover:text-blue-300' : 'text-blue-500/60 hover:text-blue-600'">{{ t('customize') }}</button>
        </div>
      </div>

      <!-- Bottom: Chat subtitle area — larger, with expand button -->
      <div class="flex-[1.5] flex flex-col justify-start items-center relative z-10 px-4">
        <!-- Typing indicator -->
        <div v-if="showTyping" class="flex items-center justify-center gap-2 mb-2">
          <div class="flex gap-1">
            <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay:0s"></span>
            <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay:0.15s"></span>
            <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay:0.3s"></span>
          </div>
          <span class="text-xs text-slate-500">{{ t('thinking') }}</span>
        </div>

        <!-- User's last message -->
        <div v-if="lastUserText" class="mb-2 text-center">
          <span class="inline-block text-sm px-4 py-1.5 rounded-full border backdrop-blur-sm"
            :class="isDark ? 'bg-blue-600/20 text-blue-200 border-blue-500/15' : 'bg-blue-600 text-white border-blue-700'">
            {{ lastUserText }}
          </span>
        </div>

        <!-- Subtitle text — larger -->
        <div
          v-if="lastAssistantText"
          class="w-full max-w-3xl backdrop-blur-md rounded-xl px-6 py-5 text-center border shadow-2xl"
          :class="isDark ? 'bg-black/60 border-slate-700/20' : 'bg-slate-900 border-slate-800'"
        >
          <p class="text-white text-lg sm:text-xl leading-relaxed font-medium" v-html="formatSubtitle(lastAssistantText)"></p>
        </div>

        <!-- Expand to chat button -->
        <button
          @click="avatarMode = false; localStorage.setItem('avatar_mode', 'false')"
          class="mt-3 flex items-center gap-1.5 text-[11px] transition-colors"
          :class="isDark ? 'text-slate-500 hover:text-blue-400' : 'text-slate-600 hover:text-blue-600'"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          {{ t('nav.chat') === 'Chat' ? 'Open full chat' : t('nav.chat') }}
        </button>
      </div>
    </div>

    <!-- ══════ CHAT MODE (default) ══════ -->
    <div v-else class="flex-1 flex flex-col min-h-0 pb-28">
      <div class="flex-1 overflow-y-auto">
        <div class="max-w-4xl mx-auto px-2">
          <ChatArea
            ref="chatAreaRef"
            :messages="chatMessages"
            :is-typing="showTyping"
            :auto-scroll="autoScroll"
            :sound-enabled="soundEnabled"
            @followup-selected="handleQuickQuestion"
            @replay-message="speakMessage"
          />
        </div>
      </div>
    </div>

    <!-- Avatar Customizer Modal -->
    <AvatarCustomizer
      v-if="showAvatarCustomizer"
      :current-avatar="doctorAvatar"
      @close="showAvatarCustomizer = false"
      @save="saveDoctorAvatar"
    />

    <!-- Input Controls - Fixed at bottom -->
    <div class="fixed bottom-0 left-0 right-0 z-50">
      <InputControls
        ref="inputControlsRef"
        :disabled="isLoading"
        :is-processing="isLoading"
        :is-speaking="isTTSSpeaking"
        :voice-enabled="voiceEnabled"
        :sound-enabled="soundEnabled"
        :quick-actions="getQuickActions()"
        @send-message="handleSendMessage"
        @start-recording="startVoiceRecording"
        @stop-recording="stopVoiceRecording"
        @voice-input="handleVoiceResult"
        @voice-toggle="toggleVoiceEnabled"
        @sound-toggle="soundEnabled = !soundEnabled"
        @open-voice-settings="showAvatarCustomizer = true"
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

    <!-- History Drawer -->
    <HistoryDrawer
      v-model="showHistory"
      @view-session="handleViewHistorySession"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { diagnose, diagnoseStream, followup, healthCheck, ApiError } from '@/services/api.js'

// Import core components
import ChatArea from '@/components/ChatArea.vue'
import InputControls from '@/components/InputControls.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import AgentPipelineIndicator from '@/components/AgentPipelineIndicator.vue'
import AgentStatusBoard from '@/components/AgentStatusBoard.vue'
import QuickActions from '@/components/QuickActions.vue'
import HelpModal from '@/components/HelpModal.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'
import DoctorAvatar from '@/components/DoctorAvatar.vue'
import AvatarCustomizer from '@/components/AvatarCustomizer.vue'
import HistoryDrawer from '@/components/HistoryDrawer.vue'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import { saveSession } from '@/services/historyService.js'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'
import { useToast } from '@/composables/useToast.js'

const { isDark } = useTheme()
const { t, lang } = useI18n()
const toast = useToast()

// When language changes mid-conversation, update the greeting if it's the only message
watch(lang, () => {
  if (chatMessages.value.length === 1 && chatMessages.value[0].sender === 'assistant' && conversationState.value === 'gathering' && questionnaire.value.currentQuestionIndex === 0) {
    chatMessages.value[0].text = t('chat.greeting')
    chatMessages.value = [...chatMessages.value]
  }
})

// Medical Questionnaire Manager — Structured Clinical Interview
class MedicalQuestionnaireManager {
  constructor() {
    // Questions use i18n keys — translated at display time via t()
    this.questions = [
      { id: 'age', i18nKey: 'q.age', type: 'number', phase: 'demographics' },
      { id: 'gender', i18nKey: 'q.gender', type: 'open', phase: 'demographics' },
      { id: 'symptoms', i18nKey: 'q.symptoms', type: 'open', phase: 'chief_complaint' },
      { id: 'onset', i18nKey: 'q.onset', type: 'open', phase: 'hpi' },
      { id: 'character', i18nKey: 'q.character', type: 'open', phase: 'hpi' },
      { id: 'location_radiation', i18nKey: 'q.location', type: 'open', phase: 'hpi' },
      { id: 'severity', i18nKey: 'q.severity', type: 'scale', phase: 'hpi' },
      { id: 'timing_pattern', i18nKey: 'q.timing', type: 'open', phase: 'hpi' },
      { id: 'aggravating_alleviating', i18nKey: 'q.aggravating', type: 'open', phase: 'hpi' },
      { id: 'associated_symptoms', i18nKey: 'q.associated', type: 'open', phase: 'hpi' },
      { id: 'past_medical', i18nKey: 'q.pastMedical', type: 'open', phase: 'medical_history' },
      { id: 'medications', i18nKey: 'q.medications', type: 'open', phase: 'medical_history' },
      { id: 'allergies', i18nKey: 'q.allergies', type: 'open', phase: 'medical_history' },
      { id: 'family_history', i18nKey: 'q.familyHistory', type: 'open', phase: 'medical_history' },
      { id: 'lifestyle', i18nKey: 'q.lifestyle', type: 'open', phase: 'social' },
    ]
    this.currentQuestionIndex = 0
    this.userResponses = {}
    this.isComplete = false
  }

  getNextQuestion() {
    if (this.currentQuestionIndex < this.questions.length) {
      return this.questions[this.currentQuestionIndex].i18nKey
    }
    this.isComplete = true
    return null
  }

  addResponse(response) {
    if (this.currentQuestionIndex < this.questions.length) {
      const questionId = this.questions[this.currentQuestionIndex].id
      this.userResponses[questionId] = response
      this.currentQuestionIndex++
    }
  }

  getAllResponses() {
    return Object.values(this.userResponses).join('\n\n')
  }

  getProgress() {
    return {
      current: this.currentQuestionIndex,
      total: this.questions.length,
      percentage: Math.round((this.currentQuestionIndex / this.questions.length) * 100)
    }
  }

  reset() {
    this.currentQuestionIndex = 0
    this.userResponses = {}
    this.isComplete = false
  }
}

// Composables
const router = useRouter()

// === REACTIVE STATE ===
const currentInput = ref('')
const isLoading = ref(false)
const error = ref(null)
const pendingImageBase64 = ref(null) // Stored image for diagnosis request
const estimatedCost = ref(0.0)
const hasStarted = ref(false)
const chatMessages = ref([])
const chatAreaRef = ref(null)
const inputControlsRef = ref(null)
const showTyping = ref(false)
const showHelp = ref(false)
const showSettings = ref(false)
const showHistory = ref(false)
const viewingHistorySession = ref(false)
const apiStatus = ref(null) // null = checking, true = AI enabled, false = fallback mode

// Conversation management
const conversationState = ref('initial') // initial, gathering, diagnosing, diagnosed
const questionnaire = ref(new MedicalQuestionnaireManager())
const currentStep = ref(0)
const totalSteps = ref(8) // Progress bar steps: Demographics, Symptoms, HPI, Details, History, Lifestyle, AI Follow-up, Review

// Doctor avatar state
const avatarMode = ref(localStorage.getItem('avatar_mode') === 'true')
const showAvatarCustomizer = ref(false)
const defaultAvatar = {
  name: 'Dr. AI',
  specialty: 'General Practitioner',
  skinTone: '#F5CBA7',
  hairStyle: 'short',
  hairColor: '#3d2b1f',
  eyeColor: '#4A6FA5',
  coatColor: '#f0f0f0',
  glasses: true,
  bgColor: '#1e3a5f',
  lipColor: '#c9877a',
  accessoryColor: '#64748b',
  avatarStyle: 'illustrated',
  photoUrl: '',
}
const doctorAvatar = ref(JSON.parse(localStorage.getItem('doctor_avatar') || JSON.stringify(defaultAvatar)))

const lastAssistantMessage = computed(() => {
  const msgs = chatMessages.value.filter(m => m.sender === 'assistant')
  return msgs.length > 0 ? msgs[msgs.length - 1] : null
})
const lastAssistantText = computed(() => {
  const msg = lastAssistantMessage.value
  if (!msg) return ''
  return (msg.text || '').replace(/\*\*/g, '')
})
const lastUserText = computed(() => {
  const msgs = chatMessages.value.filter(m => m.sender === 'user')
  if (msgs.length === 0) return ''
  return (msgs[msgs.length - 1].text || '').substring(0, 100)
})
const isMobile = ref(window.innerWidth < 640)
const avatarSize = computed(() => isMobile.value ? 'xxl' : 'xxxl')
const isSpeakingAnimating = computed(() => {
  return isTTSSpeaking.value  // Only animate mouth when actually speaking via TTS
})
const progressSteps = computed(() => [
  t('step.demographics'), t('step.symptoms'), t('step.details'), t('step.character'),
  t('step.history'), t('step.lifestyle'), t('step.followup'), t('step.review')
])

function formatSubtitle(text) {
  if (!text) return ''
  // Extract the last meaningful block — find the last question or last 1-2 sentences
  let t = text.replace(/\*\*/g, '')

  // Split into sentences
  const sentences = t.split(/(?<=[.?!])\s+/).filter(s => s.trim())

  if (sentences.length === 0) return text

  // If there's a question, show from the last question onward
  const lastQuestionIdx = sentences.findLastIndex(s => s.includes('?'))
  if (lastQuestionIdx >= 0) {
    // Show the question and 1 sentence before it for context (max 2 sentences)
    const start = Math.max(lastQuestionIdx - 1, 0)
    t = sentences.slice(start).join(' ')
  } else {
    // No question — show last 2 sentences
    t = sentences.slice(-2).join(' ')
  }

  // Bold key terms
  t = t.replace(/\*\*(.*?)\*\*/g, '<strong class="text-blue-300">$1</strong>')
  return t
}

function saveDoctorAvatar(avatar) {
  doctorAvatar.value = avatar
  localStorage.setItem('doctor_avatar', JSON.stringify(avatar))
  showAvatarCustomizer.value = false
  toast.success('Avatar updated!')
}

watch(avatarMode, (val) => {
  localStorage.setItem('avatar_mode', val ? 'true' : 'false')
})

// Agent pipeline state
const activeAgent = ref(null)
const completedAgents = ref([])
const agentTimings = ref({})
const agentFindings = ref({})
const agentErrors = ref({})
const diagnosisElapsed = ref(0)
const agentSimTimer = ref(null)
const elapsedTimer = ref(null)
const activeProvider = ref(null)

// Voice recording
const voiceRecording = ref({
  isRecording: false,
  isSupported: false,
  mediaRecorder: null,
  stream: null,
  chunks: []
})

// Settings
const voiceEnabled = ref(true)
const autoScroll = ref(true)
const soundEnabled = ref(false) // Start with sound OFF by default

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

// Speech Recognition (if available)
const speechRecognition = ref(null)
const speechSynthesis = ref(null)

// Computed properties
const canSubmit = computed(() => {
  return currentInput.value.trim() && !isLoading.value
})

const progressPercentage = computed(() => {
  if (conversationState.value === 'initial') return 0
  if (conversationState.value === 'gathering') {
    const totalQs = questionnaire.value.questions.length + 3 // fixed + AI
    const current = questionnaire.value.getProgress().current
    return Math.round((current / totalQs) * 80)
  }
  if (conversationState.value === 'awaiting-confirmation') return 85
  if (conversationState.value === 'diagnosing') return 90
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
  if (newVal && speechSynthesis.value) {
    // When turning on, play a brief confirmation
    setTimeout(() => {
      const utterance = new SpeechSynthesisUtterance('Voice enabled')
      const voice = pickDoctorVoice()
      if (voice) utterance.voice = voice
      utterance.rate = 1.1
      utterance.volume = 0.8
      window.speechSynthesis.speak(utterance)
    }, 100)
  } else if (!newVal) {
    // When turning off, cancel everything and clean up
    if (speakAbort) speakAbort.cancelled = true
    if (speechSynthesis.value) speechSynthesis.value.cancel()
    isTTSSpeaking.value = false
    stopKeepAlive()
  }
})

// === LIFECYCLE ===
const handleResize = () => { isMobile.value = window.innerWidth < 640 }
onMounted(async () => {
  window.addEventListener('resize', handleResize)

  // Initialize voice capabilities FIRST
  setupVoiceCapabilities()
  
  // Check API status
  checkApiStatus()
  
  // Force complete reset
  chatMessages.value = []
  hasStarted.value = false
  conversationState.value = 'initial'
  isLoading.value = false
  showTyping.value = false
  questionnaire.value.reset()
  
  // Add only the initial AI greeting
  setTimeout(() => {
    chatMessages.value = [{
      id: Date.now(),
      sender: 'assistant',
      text: 'Hello! I\'m your AI medical assistant powered by 7 specialized agents.\n\nI\'ll conduct a thorough clinical interview to understand your situation — covering your symptoms, their characteristics, your medical history, and lifestyle factors. This takes about 15 questions so I can build a complete picture.\n\nThen our agent team (Triage, Diagnostician, Research, Specialist, Treatment, Safety, and Communication) will collaborate to analyze your case.\n\nLet\'s begin. **What is your age?**',
      timestamp: new Date()
    }]
    
    hasStarted.value = true
    conversationState.value = 'gathering'
    // Speak the initial greeting if sound is enabled
    if (soundEnabled.value && speechSynthesis.value) {
      setTimeout(() => {
        speakMessage('Hello! I\'m your AI medical assistant powered by 7 specialized agents. I\'ll assess your symptoms through a structured interview, then our agent team will collaborate to analyze your case. Let\'s start. What is your age?')
      }, 800)
    }
    
    // Focus input on initial load
    restoreInputFocus()
  }, 500)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  cleanup()
  // Clean up TTS
  if (speakAbort) speakAbort.cancelled = true
  if (speechSynthesis.value) speechSynthesis.value.cancel()
  stopKeepAlive()
})

// === INITIALIZATION ===
async function checkApiStatus() {
  try {
    const anthropicKey = localStorage.getItem('anthropic_api_key')
    const openaiKey = localStorage.getItem('openai_api_key')

    if (anthropicKey && anthropicKey.trim() && anthropicKey.startsWith('sk-ant-')) {
      apiStatus.value = true
      activeProvider.value = 'anthropic'
    } else if (openaiKey && openaiKey.trim() && openaiKey.startsWith('sk-')) {
      apiStatus.value = true
      activeProvider.value = 'openai'
    } else {
      apiStatus.value = false
      activeProvider.value = null
    }
  } catch (err) {
    console.error('API status check failed:', err)
    apiStatus.value = false
  }
}

async function initializeApp() {
  try {
    const isHealthy = await healthCheck()
    if (isHealthy) {
      // API connection successful
    } else {
      handleError('Backend API is not healthy. Please try again later.')
    }
  } catch (err) {
    console.error('❌ API connection failed:', err)
    handleError('Failed to connect to the backend API. Please check your network connection and try again.')
  }
}

function setupVoiceCapabilities() {
  try {
    // Check for speech recognition support (don't fully init — startVoiceRecording does that)
    const hasSpeechRecognition = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
    if (!hasSpeechRecognition) {
      voiceEnabled.value = false
    }
    voiceRecording.value.isSupported = hasSpeechRecognition

    // Speech synthesis for text-to-speech
    if ('speechSynthesis' in window) {
      speechSynthesis.value = window.speechSynthesis
      // Force voice list to load (Chrome loads them async)
      speechSynthesis.value.getVoices()
      speechSynthesis.value.addEventListener('voiceschanged', () => {
        // Voice list updated — pickDoctorVoice() reads fresh each time, so nothing else needed
      })
    }
  } catch (err) {
    voiceEnabled.value = false
    speechSynthesis.value = null
    speechRecognition.value = null
  }
}

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
      if (voiceRecording.value.isRecording) {
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
  if (voiceRecording.value.stream) {
    voiceRecording.value.stream.getTracks().forEach(track => track.stop())
  }
  
  if (speechRecognition.value) {
    speechRecognition.value.stop()
  }
  
  if (window.__voiceDiagnosisKeydownHandler) {
    document.removeEventListener('keydown', window.__voiceDiagnosisKeydownHandler)
  }
}

// === CORE FUNCTIONS ===

/**
 * Handles the start of the conversation
 */
function handleStart() {
  hasStarted.value = true
  conversationState.value = 'gathering'
  addMessage('assistant', t('chat.greeting'))
}

/**
 * Validates user input based on the current question type
 */
function validateInput(message, questionType) {
  const trimmed = message.trim()
  
  if (!trimmed) {
    return { valid: false, error: 'Please provide a response.' }
  }
  
  // Get current question
  const currentQ = questionnaire.value.questions[questionnaire.value.currentQuestionIndex]
  
  if (!currentQ) {
    return { valid: true } // No specific validation needed
  }
  
  // Validate based on question ID
  switch (currentQ.id) {
    case 'symptoms':
      if (trimmed.length < 5) {
        return { valid: false, error: 'Please provide more detail about your symptoms (at least 5 characters).' }
      }
      // Check if it's just gibberish or non-medical text
      if (/^[^a-zA-Z]*$/.test(trimmed) || /^(.)\1+$/.test(trimmed)) {
        return { valid: false, error: 'Please describe your symptoms using words.' }
      }
      break
      
    case 'duration':
      // Accept either free text or one of the options
      // No strict validation needed as any time description is acceptable
      break
      
    case 'severity':
      // Try to extract a number
      const severityMatch = trimmed.match(/\b(\d+)\b/)
      if (!severityMatch) {
        return { valid: false, error: 'Please provide a number between 1 and 10 to rate the severity.' }
      }
      const severity = parseInt(severityMatch[1])
      if (severity < 1 || severity > 10) {
        return { valid: false, error: 'Please provide a severity rating between 1 and 10.' }
      }
      break
      
    case 'age':
      const ageMatch = trimmed.match(/\b(\d+)\b/)
      if (!ageMatch) {
        return { valid: false, error: 'Please provide your age as a number (e.g., 25).' }
      }
      const age = parseInt(ageMatch[1])
      if (age < 1 || age > 120) {
        return { valid: false, error: 'Please provide a valid age between 1 and 120.' }
      }
      break
      
    case 'gender':
      const validGenders = ['male', 'female', 'man', 'woman', 'non-binary', 'nonbinary', 'other', 'prefer not to say']
      const genderLower = trimmed.toLowerCase()
      const isValidGender = validGenders.some(g => genderLower.includes(g))
      if (!isValidGender && trimmed.length < 3) {
        return { valid: false, error: 'Please specify your gender (e.g., male, female, non-binary, or prefer not to say).' }
      }
      break
  }
  
  return { valid: true }
}

/**
 * Handles sending a message from the user
 */
async function handleSendMessage(message, imageBase64Param = null) {
  // Store the image for later use in diagnosis request
  if (imageBase64Param) {
    pendingImageBase64.value = imageBase64Param
  }

  if (!message.trim() || isLoading.value) {
    return
  }

  // Validate input if in gathering state
  if (conversationState.value === 'gathering') {
    const validation = validateInput(message, 'current')
    if (!validation.valid) {
      // Show error message to user
      addMessage('assistant', `❌ ${validation.error}`)
      // Restore focus and wait for corrected input
      restoreInputFocus()
      return
    }
  }

  // Clear input and add user message
  currentInput.value = ''
  const imageUrl = imageBase64Param ? `data:image/jpeg;base64,${imageBase64Param}` : null
  addMessage('user', message, imageUrl ? { imageUrl } : {})
  
  // Restore focus to input immediately after clearing
  restoreInputFocus()
  
  // Show typing indicator
  showTyping.value = true
  isLoading.value = true
  
  try {
    if (conversationState.value === 'gathering') {
      // Store response in questionnaire for regular questions
      questionnaire.value.addResponse(message)
      await handleGatheringMessage()
    } else if (conversationState.value === 'awaiting-confirmation') {
      // Check if this is a "yes" response to proceed with diagnosis
      const isConfirmation = /^(yes|y|sure|ok|okay|proceed|go ahead|continue|let's go)$/i.test(message.trim())
      
      if (isConfirmation) {
        // User confirmed to proceed with diagnosis
        await handleProceedToDiagnosis()
      } else {
        // User declined or unclear response
        addMessage('assistant', "I understand. Would you like me to proceed with the health assessment analysis? Please respond with 'yes' when you're ready.")
        await waitForSpeech()
      }
    } else if (conversationState.value === 'diagnosed') {
      await handleFollowUpMessage(message)
    } else {
      // If state is initial, start the conversation
      handleStart()
      // Then handle the message
      questionnaire.value.addResponse(message)
      await handleGatheringMessage()
    }
  } catch (err) {
    console.error('❌ Message handling failed:', err)
    handleError(err instanceof ApiError ? err.message : 'An unexpected error occurred. Please try again.')
  } finally {
    showTyping.value = false

    // Wait for the doctor to finish speaking before re-enabling input
    // This prevents the user from sending while the doctor is mid-sentence
    if (soundEnabled.value && speechSynthesis.value) {
      await waitForSpeech()
    }

    isLoading.value = false
    restoreInputFocus()
  }
}

/**
 * Handles gathering medical information through questions
 */
async function handleGatheringMessage() {
  // Brief thinking pause
  await new Promise(resolve => setTimeout(resolve, 800))

  const currentIndex = questionnaire.value.currentQuestionIndex
  const fixedQuestionCount = questionnaire.value.questions.length // 15 structured questions

  // After all fixed questions, go straight to diagnosis — no AI follow-ups
  // The AI follow-up loop was causing 80+ repetitive questions
  if (currentIndex >= fixedQuestionCount) {
    addMessage('assistant', t('chat.analysisStart'))
    await waitForSpeech()
    currentStep.value = totalSteps.value
    // Auto-proceed to diagnosis without waiting for confirmation
    await handleProceedToDiagnosis()
    return
  }

  // Fixed structured questions — translate using i18n
  const nextQuestionKey = questionnaire.value.getNextQuestion()
  if (nextQuestionKey) {
    const currentQ = questionnaire.value.questions[currentIndex]
    const prevQ = currentIndex > 0 ? questionnaire.value.questions[currentIndex - 1] : null
    let prefix = ''
    if (currentQ.phase !== prevQ?.phase) {
      const phaseKeys = {
        'demographics': '',
        'chief_complaint': '',
        'hpi': 'q.phase.hpi',
        'medical_history': 'q.phase.medical',
        'social': 'q.phase.social',
      }
      const phaseKey = phaseKeys[currentQ.phase]
      prefix = phaseKey ? t(phaseKey) : ''
    }
    addMessage('assistant', prefix + t(nextQuestionKey))
    await waitForSpeech()
    currentStep.value = Math.min(currentIndex, totalSteps.value - 1)
  }
}

/**
 * Proceeds with medical diagnosis after questions are complete
 */
function startAgentSimulation() {
  const agentOrder = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']
  let idx = 0
  activeAgent.value = agentOrder[0]
  completedAgents.value = []
  agentTimings.value = {}
  diagnosisElapsed.value = 0

  // Elapsed timer
  const startTime = Date.now()
  elapsedTimer.value = setInterval(() => {
    diagnosisElapsed.value = (Date.now() - startTime) / 1000
  }, 200)

  // Simulate agent progression every ~2 seconds, with diagnostician+research in parallel
  agentSimTimer.value = setInterval(() => {
    if (idx < agentOrder.length - 1) {
      // Complete current agent(s)
      completedAgents.value = [...completedAgents.value, agentOrder[idx]]
      agentTimings.value = { ...agentTimings.value, [agentOrder[idx]]: 1.5 + Math.random() * 1.5 }
      idx++

      // Run diagnostician and research in parallel (both activate after triage)
      if (agentOrder[idx] === 'diagnostician' && idx + 1 < agentOrder.length && agentOrder[idx + 1] === 'research') {
        activeAgent.value = agentOrder[idx]
        // Complete both diagnostician and research together on next tick
        setTimeout(() => {
          completedAgents.value = [...completedAgents.value, 'diagnostician']
          agentTimings.value = { ...agentTimings.value, diagnostician: 1.5 + Math.random() * 1.5 }
          completedAgents.value = [...completedAgents.value, 'research']
          agentTimings.value = { ...agentTimings.value, research: 1.5 + Math.random() * 1.5 }
          idx = idx + 2 // skip past both
          if (idx < agentOrder.length) {
            activeAgent.value = agentOrder[idx]
          }
        }, 2000)
      } else {
        activeAgent.value = agentOrder[idx]
      }
    }
  }, 2000)
}

function stopAgentSimulation(realTimings) {
  clearInterval(agentSimTimer.value)
  clearInterval(elapsedTimer.value)
  agentSimTimer.value = null
  elapsedTimer.value = null

  if (realTimings) {
    agentTimings.value = realTimings
  }
  completedAgents.value = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']
  activeAgent.value = null
}

async function handleProceedToDiagnosis() {
  isLoading.value = true
  showTyping.value = true
  conversationState.value = 'diagnosing'

  // Scroll to top so user sees the agent pipeline status
  window.scrollTo({ top: 0, behavior: 'smooth' })

  // Reset agent pipeline state for real-time streaming
  activeAgent.value = 'triage'
  completedAgents.value = []
  agentTimings.value = {}
  agentFindings.value = {}
  agentErrors.value = {}
  diagnosisElapsed.value = 0

  // Start elapsed timer with timeout warning
  const diagStartTime = Date.now()
  let timeoutWarned = false
  elapsedTimer.value = setInterval(() => {
    diagnosisElapsed.value = (Date.now() - diagStartTime) / 1000
    if (diagnosisElapsed.value > 45 && !timeoutWarned) {
      timeoutWarned = true
      toast.warning('Analysis is taking longer than expected. Please wait...')
    }
  }, 200)

  // Agent order for determining the next active agent
  const agentOrder = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']

  // Add thinking message with helpful context
  addMessage('assistant', "Starting multi-agent analysis — 7 specialized AI agents will now analyze your case. This typically takes 15-30 seconds.\n\nAgents: Triage > Diagnostician + Research > Specialist > Treatment > Safety > Summary")

  try {
    // Extract all responses from questionnaire
    const responses = questionnaire.value.userResponses
    
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
    
    // Build comprehensive clinical summary from structured interview
    const symptomParts = [
      `Chief Complaint: ${responses.symptoms || 'Not specified'}`,
    ]
    if (responses.onset) symptomParts.push(`Onset: ${responses.onset}`)
    if (responses.character) symptomParts.push(`Character/Quality: ${responses.character}`)
    if (responses.location_radiation) symptomParts.push(`Location/Radiation: ${responses.location_radiation}`)
    symptomParts.push(`Severity: ${severity}/10`)
    if (responses.timing_pattern) symptomParts.push(`Timing/Pattern: ${responses.timing_pattern}`)
    if (responses.aggravating_alleviating) symptomParts.push(`Aggravating/Alleviating factors: ${responses.aggravating_alleviating}`)
    if (responses.associated_symptoms) symptomParts.push(`Associated Symptoms: ${responses.associated_symptoms}`)
    symptomParts.push(`Duration: ${duration}`)
    if (responses.past_medical) symptomParts.push(`Past Medical History: ${responses.past_medical}`)
    if (responses.medications) symptomParts.push(`Current Medications: ${responses.medications}`)
    if (responses.allergies) symptomParts.push(`Allergies: ${responses.allergies}`)
    if (responses.family_history) symptomParts.push(`Family History: ${responses.family_history}`)
    if (responses.lifestyle) symptomParts.push(`Social/Lifestyle: ${responses.lifestyle}`)

    // Include any AI follow-up responses
    Object.entries(responses).forEach(([key, val]) => {
      if (key.startsWith('ai_question_') && val) {
        symptomParts.push(`Follow-up: ${val}`)
      }
    })

    const symptomsText = symptomParts.join('\n\n')
    
    // Extract structured fields separately for richer backend context
    const diagnosisData = {
      symptoms: symptomsText,
      age: age,
      gender: gender,
      duration: duration,
      severity: severity,
      image_base64: pendingImageBase64.value || null,
      // Send structured fields separately so the backend can build a better clinical summary
      medical_history: responses.past_medical || null,
      current_medications: responses.medications || null,
      allergies: responses.allergies || null,
      family_history: responses.family_history || null,
      social_history: responses.lifestyle || null,
      // Model preference from settings
      model_preference: localStorage.getItem('model_preference') || 'auto',
    }

    // Clear the pending image after building the request
    pendingImageBase64.value = null

    // SSE streaming callback for real-time agent updates
    const agentLabels = {
      triage: 'Triage', diagnostician: 'Diagnostician', research: 'Research',
      specialist: 'Specialist', treatment: 'Treatment', safety: 'Safety', empathy: 'Summary'
    }

    const onAgentEvent = (event) => {
      if (event.event === 'agent_complete') {
        const agentName = event.agent

        // Update completed agents
        if (!completedAgents.value.includes(agentName)) {
          completedAgents.value = [...completedAgents.value, agentName]
        }

        // Update timings and findings
        agentTimings.value = { ...agentTimings.value, [agentName]: event.elapsed }
        agentFindings.value = { ...agentFindings.value, [agentName]: event.key_findings }

        // Determine next active agent
        const allCompleted = new Set(completedAgents.value)
        let nextActive = null
        for (const a of agentOrder) {
          if (!allCompleted.has(a)) {
            nextActive = a
            break
          }
        }
        activeAgent.value = nextActive

        // Update the thinking message in-place so user sees live progress
        const thinkingMsg = chatMessages.value.find(m => m.sender === 'assistant' && m.text.includes('multi-agent analysis'))
        if (thinkingMsg) {
          const done = completedAgents.value.length
          const total = agentOrder.length
          const completed = completedAgents.value.map(a => `${agentLabels[a] || a}`).join(', ')
          const next = nextActive ? agentLabels[nextActive] || nextActive : 'Finalizing'
          thinkingMsg.text = `Multi-agent analysis in progress (${done}/${total})...\n\nCompleted: ${completed}\nNow running: ${next}\n\nElapsed: ${diagnosisElapsed.value.toFixed(0)}s`
          chatMessages.value = [...chatMessages.value] // trigger reactivity
        }
      }
    }

    // Try streaming first, fall back to non-streaming
    let result
    try {
      result = await diagnoseStream(diagnosisData, onAgentEvent)
    } catch (streamErr) {
      console.warn('SSE streaming failed, falling back to standard request:', streamErr.message)
      // Fall back: use simulation + standard diagnose
      startAgentSimulation()
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Diagnosis request timed out after 90 seconds')), 90000)
      )
      result = await Promise.race([
        diagnose(diagnosisData),
        timeoutPromise
      ])
      stopAgentSimulation(result.agent_timings || null)
    }

    // Stop elapsed timer
    if (elapsedTimer.value) {
      clearInterval(elapsedTimer.value)
      elapsedTimer.value = null
    }

    estimatedCost.value += result.estimated_cost || 0.05

    // Finalize agent state
    completedAgents.value = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']
    activeAgent.value = null
    if (result.agent_timings) agentTimings.value = result.agent_timings
    if (result.total_time) diagnosisElapsed.value = result.total_time

    // Check if AI was used
    if (result.estimated_cost > 0 && result.causes && result.causes.length > 0) {
      apiStatus.value = true
    } else {
      apiStatus.value = false
    }

    // Remove thinking message and add structured diagnosis
    chatMessages.value.pop()

    const diagnosisText = result.answer || "I've analyzed your symptoms. Based on the information provided, I recommend consulting with a healthcare professional."

    // Add the diagnosis message with structured agent data
    chatMessages.value.push({
      id: Date.now() + Math.random(),
      sender: 'assistant',
      text: diagnosisText,
      timestamp: new Date(),
      // Structured multi-agent data
      causes: result.causes || [],
      redFlags: result.red_flags || [],
      recommendedTests: result.recommended_tests || [],
      additionalQuestions: result.additional_questions || [],
      confidenceScores: result.confidence_scores || {},
      agentDetails: result.agent_details || {},
      agentTimings: result.agent_timings || {},
      multiAgent: result.multi_agent || false,
      agentsUsed: result.agents_used || [],
      // Enhanced structured data
      patientSummary: result.patient_summary || '',
      actionChecklist: result.action_checklist || [],
      safetyStatus: result.safety_status || '',
      safetyWarnings: result.safety_warnings || [],
      medications: result.medications || [],
      lifestyleRecommendations: result.lifestyle_recommendations || [],
      warningSignsList: result.warning_signs || [],
      followUpTimeline: result.follow_up_timeline || '',
      totalTime: result.total_time || 0
    })

    conversationState.value = 'diagnosed'
    toast.success('Diagnosis complete! Your results are ready.')

    // Switch to chat mode so user can see the full structured results
    if (avatarMode.value) {
      avatarMode.value = false
      localStorage.setItem('avatar_mode', 'false')
    }

    // Store diagnosis data for dashboard immediately after diagnosis completes
    storeDiagnosisForDashboard()

    // Save full structured result to localStorage for the new dashboard
    try {
      const fullResult = {
        ...result,
        age: questionnaire.value.userResponses.age || '',
        gender: questionnaire.value.userResponses.gender || '',
        symptoms: questionnaire.value.userResponses.symptoms || '',
        date: new Date().toISOString()
      }
      localStorage.setItem('latest_diagnosis_result', JSON.stringify(fullResult))
    } catch (e) {
      console.error('Failed to store full diagnosis result:', e)
    }

    // Save to conversation history
    try {
      saveSession({
        symptoms: questionnaire.value.userResponses.symptoms || '',
        age: questionnaire.value.userResponses.age || '',
        gender: questionnaire.value.userResponses.gender || '',
        diagnosisResult: result,
        chatMessages: chatMessages.value.map(m => ({ sender: m.sender, text: m.text, timestamp: m.timestamp })),
        timestamp: new Date().toISOString()
      })
    } catch (e) {
      console.error('Failed to save session to history:', e)
    }

  } catch (err) {
    console.error('Diagnosis failed:', err)
    toast.error(`Diagnosis failed: ${err.message || 'Unknown error'}`)
    // Stop timers
    if (elapsedTimer.value) {
      clearInterval(elapsedTimer.value)
      elapsedTimer.value = null
    }
    stopAgentSimulation(null)

    // Remove thinking message
    if (chatMessages.value.length > 0 && chatMessages.value[chatMessages.value.length - 1].text.includes('Multi-agent')) {
      chatMessages.value.pop()
    }
    
    // Store basic diagnosis data for dashboard even when API fails
    const fallbackDiagnosis = [{
      condition: "Medical Assessment Needed",
      confidence: 75,
      explanation: `Based on your symptoms: ${questionnaire.value.getAllResponses().substring(0, 100)}..., I recommend consulting with a healthcare professional for proper evaluation and diagnosis.`,
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
    
    // Switch to chat mode so user can see the error message properly
    if (avatarMode.value) {
      avatarMode.value = false
      localStorage.setItem('avatar_mode', 'false')
    }

    // Add error message but still set state to diagnosed so user can access dashboard
    addMessage('assistant',
      "I apologize, but I'm having trouble processing your diagnosis right now. This could be due to a connection issue.\n\n**Please check:**\n1. Your API key is valid (Settings > API Keys)\n2. The backend server is running on port 8000\n3. Your internet connection is stable\n\nYou can try again by clicking '+ New' in the header."
    )

    conversationState.value = 'diagnosed'
  } finally {
    showTyping.value = false
    isLoading.value = false
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
      original_symptoms: questionnaire.value.userResponses.symptoms || ''
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
 * Handle viewing a past session from history drawer
 */
function handleViewHistorySession(session) {
  if (!session || !session.chatMessages) return
  viewingHistorySession.value = true
  // Load the session's chat messages into the current view as read-only
  chatMessages.value = session.chatMessages.map((m, i) => ({
    id: Date.now() + i,
    sender: m.sender || (m.role === 'user' ? 'user' : 'assistant'),
    text: m.text || m.content || '',
    timestamp: m.timestamp ? new Date(m.timestamp) : new Date()
  }))
  conversationState.value = 'diagnosed'
  hasStarted.value = true

  // If the session has a full diagnosis result, store it for dashboard access
  if (session.diagnosisResult) {
    try {
      localStorage.setItem('latest_diagnosis_result', JSON.stringify({
        ...session.diagnosisResult,
        age: session.age || '',
        gender: session.gender || '',
        symptoms: session.symptoms || '',
        date: session.timestamp || new Date().toISOString()
      }))
    } catch (e) {
      console.error('Failed to store history session result:', e)
    }
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
function handleQuickAction(action) {
  if (action.action === 'navigate' || action.action === 'manual-navigate') {
    // Always store diagnosis data before navigating
    storeDiagnosisForDashboard()
    
    if (action.action === 'manual-navigate') {
      // Force direct navigation for debug
      window.location.href = action.route
    } else {
      // Use Vue router
      router.push(action.route).catch(err => {
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
 * Stores current diagnosis data in localStorage for dashboard
 */
function storeDiagnosisForDashboard() {
  try {
    // Find the diagnosis message in chat (look for the main diagnosis response)
    // Check both chatMessages (live) and localStorage (for stored data)
    let diagnosisMessage = chatMessages.value.find(msg => 
      (msg.sender === 'assistant' || msg.role === 'assistant') && 
      (msg.text || msg.content) && 
      (msg.text?.length > 100 || msg.content?.length > 100) && 
      !msg.text?.includes('Analyzing') &&
      (msg.text?.includes('Differential diagnosis') || msg.content?.includes('Differential diagnosis'))
    )
    
    let dashboardData = []
    let treatmentSteps = []
    let holisticOptions = []
    
    // Get the text content from either msg.text or msg.content
    const text = diagnosisMessage?.text || diagnosisMessage?.content
    
    if (text) {
      // Look for "Differential diagnosis:" section - be more flexible with ending
      const diffDiagSection = text.match(/Differential diagnosis[s]?:([\s\S]*?)(?=Additional information|Suggested diagnostic|Clinical recommendations|Urgency:|Assessment summary:|$)/i)
      
      if (diffDiagSection) {
        const diagnosisText = diffDiagSection[1]
        
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
          
          dashboardData.push({
            condition,
            confidence,
            urgency,
            specialty,
            explanation
          })
        }
        
      }
      
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
    
    // Fallback if no diagnoses were parsed
    if (dashboardData.length === 0) {
      const symptoms = questionnaire.value.getAllResponses()
      dashboardData = [{
        condition: "Health Assessment Complete",
        confidence: 80,
        urgency: "routine",
        specialty: "Primary Care",
        explanation: `Based on your reported symptoms and medical history, a comprehensive evaluation by a healthcare professional is recommended for proper diagnosis and treatment planning.`
      }]
      
      treatmentSteps = [
        "Consult with your primary care physician or appropriate specialist",
        "Provide them with detailed symptom information",
        "Discuss duration, severity, and any triggering factors",
        "Follow recommended diagnostic tests or treatments",
        "Schedule follow-up appointments as needed"
      ]
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
  if (!enabled && voiceRecording.value.isRecording) {
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

  if (voiceRecording.value.isRecording) {
    stopVoiceRecording()
  } else {
    await startVoiceRecording()
  }
}

/**
 * Starts voice recording
 */
async function startVoiceRecording() {
  // Check if already recording
  if (voiceRecording.value.isRecording) return

  // Try to initialize speech recognition if not already done
  if (!speechRecognition.value) {
    const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition
    if (SpeechRecognitionClass) {
      try {
        speechRecognition.value = new SpeechRecognitionClass()
        speechRecognition.value.continuous = false
        speechRecognition.value.interimResults = true
        speechRecognition.value.lang = 'en-US'
        speechRecognition.value.maxAlternatives = 1

        speechRecognition.value.onresult = (event) => {
          // Build transcript from all results
          let transcript = ''
          for (let i = 0; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript
          }
          // If this is a final result, send the message
          if (event.results[event.results.length - 1].isFinal) {
            voiceRecording.value.isRecording = false
            if (transcript && transcript.trim()) {
              handleSendMessage(transcript.trim())
            }
          }
        }

        speechRecognition.value.onerror = (event) => {
          voiceRecording.value.isRecording = false
          if (event.error === 'not-allowed' || event.error === 'permission-denied') {
            handleError('Microphone permission denied. Please allow microphone access in your browser settings (click the lock icon in the address bar).')
            voiceEnabled.value = false
          } else if (event.error === 'no-speech') {
            handleError('No speech detected. Please try again and speak clearly into your microphone.')
          } else if (event.error === 'network') {
            handleError('Speech recognition needs an internet connection. Please check your network.')
          } else if (event.error === 'aborted') {
            // User cancelled — not an error
          } else {
            handleError(`Voice recognition error: ${event.error}. Please type your message instead.`)
          }
        }

        speechRecognition.value.onend = () => {
          voiceRecording.value.isRecording = false
        }
      } catch (initErr) {
        speechRecognition.value = null
      }
    }
  }

  if (!speechRecognition.value) {
    handleError(
      'Voice input is not supported in this browser. Please use Google Chrome for voice features, or type your message instead.'
    )
    voiceEnabled.value = false
    return
  }

  try {
    // Stop any existing session first
    try { speechRecognition.value.abort() } catch (_) {}

    speechRecognition.value.start()
    voiceRecording.value.isRecording = true
  } catch (err) {
    voiceRecording.value.isRecording = false
    if (err.message && err.message.includes('already')) {
      voiceRecording.value.isRecording = true
    } else {
      handleError('Could not start voice recording. Please try again or type your message.')
    }
  }
}

/**
 * Stops voice recording
 */
function stopVoiceRecording() {
  try {
    if (speechRecognition.value) {
      try { speechRecognition.value.stop() } catch (_) {}
    }

    if (voiceRecording.value.mediaRecorder) {
      try {
        if (voiceRecording.value.mediaRecorder.state !== 'inactive') {
          voiceRecording.value.mediaRecorder.stop()
        }
      } catch (_) {}
    }

    if (voiceRecording.value.stream) {
      try {
        voiceRecording.value.stream.getTracks().forEach(track => {
          track.stop()
        })
        voiceRecording.value.stream = null
      } catch (err) {
        console.warn('⚠️ Error stopping stream:', err)
      }
    }
    
    voiceRecording.value.isRecording = false
    voiceRecording.value.mediaRecorder = null
    voiceRecording.value.chunks = []
  } catch (err) {
    console.error('❌ Error stopping voice recording:', err)
    // Force reset state
    voiceRecording.value.isRecording = false
    voiceRecording.value.mediaRecorder = null
    voiceRecording.value.stream = null
    voiceRecording.value.chunks = []
  }
}

/**
 * Handles voice recognition result
 */
function handleVoiceResult(transcript) {
  currentInput.value = transcript
  voiceRecording.value.isRecording = false
}

// === UTILITY FUNCTIONS ===

/**
 * Gets quick actions for current state
 */
function getQuickActions() {
  if (conversationState.value === 'gathering' && !questionnaire.value.isComplete) {
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
      return `Gathering medical information (${questionnaire.value.getProgress().current}/${questionnaire.value.getProgress().total})`
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
// Resolves when the doctor finishes speaking (or immediately if sound off)
let currentSpeechPromise = null

function addMessage(role, content, additionalData = {}) {
  // Sanitize message content
  const sanitizeMessage = (txt) => {
    if (!txt || typeof txt !== 'string') return txt
    let t = txt.replace(/<br\s*\/?\>/gi, '\n')
    t = t.replace(/<[^>]+>/g, '')
    t = t.replace(/(\n\s*){3,}/g, '\n\n')
    return t.trim()
  }

  const cleanContent = sanitizeMessage(content)

  const message = {
    id: Date.now() + Math.random(),
    sender: role,
    text: cleanContent,
    timestamp: new Date(),
    ...additionalData
  }

  chatMessages.value.push(message)
  chatMessages.value = [...chatMessages.value]

  // Speak message if it's from assistant and speech synthesis is enabled
  if (role === 'assistant' && speechSynthesis.value && soundEnabled.value) {
    // Create a promise that resolves when speech finishes
    currentSpeechPromise = new Promise((resolve) => {
      setTimeout(async () => {
        await speakMessage(cleanContent)
        resolve()
      }, 300)
    })
  } else {
    currentSpeechPromise = Promise.resolve()
  }
}

/**
 * Waits for the doctor to finish speaking before continuing.
 * Returns immediately if sound is off.
 */
async function waitForSpeech() {
  if (currentSpeechPromise) {
    await currentSpeechPromise
    currentSpeechPromise = null
  }
}

/**
 * Speaks a message using text-to-speech
 */
// Track speaking state for avatar lip sync
const isTTSSpeaking = ref(false)

// Chrome workaround: speechSynthesis silently pauses after ~15s.
// Periodically call resume() to keep it alive.
let keepAliveInterval = null
function startKeepAlive() {
  stopKeepAlive()
  keepAliveInterval = setInterval(() => {
    if (speechSynthesis.value && speechSynthesis.value.speaking) {
      speechSynthesis.value.resume()
    }
  }, 5000)
}
function stopKeepAlive() {
  if (keepAliveInterval) { clearInterval(keepAliveInterval); keepAliveInterval = null }
}

/**
 * Find the best voice for the doctor avatar.
 * Always re-reads the voice list (never stale).
 */
function pickDoctorVoice() {
  if (!speechSynthesis.value) return null
  const voices = speechSynthesis.value.getVoices()
  if (voices.length === 0) return null

  // Check user preference first
  const preferredName = doctorAvatar.value.preferredVoice
  if (preferredName) {
    const match = voices.find(v => v.name === preferredName)
    if (match) return match
  }

  const gender = doctorAvatar.value.name || ''
  const femaleNames = ['sarah','maria','amara','emma','lisa','anna','jessica','rachel','emily']
  const preferFemale = femaleNames.some(n => gender.toLowerCase().includes(n))

  // Ranked voice preference — high-quality first
  const preferredNames = [
    preferFemale ? 'Google UK English Female' : 'Google UK English Male',
    preferFemale ? 'Google US English' : 'Google UK English Male',
    preferFemale ? 'Microsoft Zira' : 'Microsoft David',
    preferFemale ? 'Microsoft Jenny Online' : 'Microsoft Guy Online',
    preferFemale ? 'Microsoft Aria Online' : 'Microsoft Ryan Online',
    preferFemale ? 'Samantha' : 'Daniel',
    preferFemale ? 'Karen' : 'Alex',
    preferFemale ? 'Moira' : 'Tom',
    'Google UK English Female',
    'Google UK English Male',
  ]

  for (const name of preferredNames) {
    const v = voices.find(voice => voice.name.includes(name))
    if (v) return v
  }

  const enVoices = voices.filter(v => v.lang.startsWith('en'))
  const cloudVoice = enVoices.find(v => !v.localService)
  if (cloudVoice) return cloudVoice
  if (enVoices.length > 0) return enVoices[0]
  return voices[0] || null
}

/**
 * Sequentially speaks an array of text chunks using a promise chain.
 * Each chunk waits for the previous to finish before starting.
 */
let speakAbort = null // AbortController-like flag for cancellation

function speakChunk(text, voice, rate) {
  return new Promise((resolve) => {
    if (speakAbort?.cancelled) { resolve(); return }
    const utterance = new SpeechSynthesisUtterance(text)
    if (voice) utterance.voice = voice
    utterance.rate = rate
    utterance.pitch = 1.0
    utterance.volume = 0.85

    utterance.onstart = () => { isTTSSpeaking.value = true }
    utterance.onend = () => { resolve() }
    utterance.onerror = (e) => {
      // 'interrupted' and 'canceled' are expected when we cancel
      if (e.error !== 'interrupted' && e.error !== 'canceled') {
        console.warn('TTS chunk error:', e.error)
      }
      resolve()
    }

    speechSynthesis.value.speak(utterance)
  })
}

async function speakMessage(text) {
  if (!text || typeof text !== 'string' || text.trim().length === 0) return
  if (!speechSynthesis.value) return
  if (!soundEnabled.value) return

  // Cancel any in-progress speech
  if (speakAbort) speakAbort.cancelled = true
  speechSynthesis.value.cancel()
  isTTSSpeaking.value = false

  // Small delay after cancel — some browsers need this
  await new Promise(r => setTimeout(r, 50))

  const abort = { cancelled: false }
  speakAbort = abort

  try {
    // Clean text for speech
    let cleanText = text
      .replace(/<[^>]*>/g, '')       // HTML tags
      .replace(/\*\*/g, '')          // Bold markdown
      .replace(/[#`_~]/g, '')        // Other markdown
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Markdown links → just text
      .replace(/[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '') // Emoji
      .replace(/---+/g, '. ')
      .replace(/={2,}/g, '. ')
      .replace(/-{2,}/g, '. ')
      .replace(/\n+/g, '. ')
      .replace(/\.\s*\./g, '.')
      .replace(/\s+/g, ' ')
      .trim()

    if (!cleanText) return

    // Split into chunks — keep them shorter (200 chars) for reliability.
    // Shorter chunks recover faster from errors and feel more responsive.
    const maxLen = 200
    const chunks = []
    let remaining = cleanText
    while (remaining.length > 0) {
      if (remaining.length <= maxLen) {
        chunks.push(remaining)
        break
      }
      // Prefer breaking at sentence boundaries, then commas, then spaces
      let breakIdx = remaining.lastIndexOf('. ', maxLen)
      if (breakIdx < maxLen * 0.3) breakIdx = remaining.lastIndexOf(', ', maxLen)
      if (breakIdx < maxLen * 0.3) breakIdx = remaining.lastIndexOf(' ', maxLen)
      if (breakIdx < maxLen * 0.3) breakIdx = maxLen
      chunks.push(remaining.substring(0, breakIdx + 1))
      remaining = remaining.substring(breakIdx + 1).trim()
    }

    // Always pick voice fresh (respects user changes without page reload)
    const voice = pickDoctorVoice()
    const rate = doctorAvatar.value.voiceRate || 0.95

    // Start Chrome keep-alive workaround
    startKeepAlive()

    // Speak chunks sequentially
    for (const chunk of chunks) {
      if (abort.cancelled || !soundEnabled.value) break
      await speakChunk(chunk, voice, rate)
    }
  } catch (err) {
    console.warn('TTS error:', err)
  } finally {
    isTTSSpeaking.value = false
    stopKeepAlive()
    if (speakAbort === abort) speakAbort = null
  }
}

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
  const responses = Object.values(questionnaire.value.userResponses).join(' ')
  const ageMatch = responses.match(/\b(\d{1,3})\b/)
  return ageMatch ? parseInt(ageMatch[1]) : null
}

/**
 * Extracts gender from responses
 */
function extractGender() {
  const responses = Object.values(questionnaire.value.userResponses).join(' ').toLowerCase()
  if (responses.includes('male') && !responses.includes('female')) return 'male'
  if (responses.includes('female')) return 'female'
  return 'unknown'
}

/**
 * Extracts severity from responses
 */
function extractSeverity() {
  const responses = Object.values(questionnaire.value.userResponses).join(' ')
  const severityMatch = responses.match(/\b([1-9]|10)\b/)
  return severityMatch ? parseInt(severityMatch[1]) : null
}

/**
 * Handles errors by displaying them to the user
 */
function handleError(message) {
  // Use toast for network/minor errors, keep modal for critical ones
  const isCritical = message.includes('API') || message.includes('backend') || message.includes('connect')
  if (isCritical) {
    error.value = message
    setTimeout(() => { if (error.value === message) error.value = null }, 8000)
  } else {
    toast.error(message)
  }
  console.error('Error:', message)
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
  if (window.speechSynthesis) {
    const utterance = new SpeechSynthesisUtterance('Hello, I am your AI health assistant. I can speak to you.')
    utterance.rate = 1.0
    utterance.pitch = 1.0
    utterance.volume = 1.0
    window.speechSynthesis.speak(utterance)
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
  if (chatMessages.value.length > 0) {
    if (!confirm('Are you sure you want to start over? This will clear your current conversation.')) {
      return
    }
  }

  // Cancel any ongoing speech
  if (speakAbort) speakAbort.cancelled = true
  if (speechSynthesis.value) speechSynthesis.value.cancel()
  isTTSSpeaking.value = false
  stopKeepAlive()

  chatMessages.value = []
  currentInput.value = ''
  hasStarted.value = false
  conversationState.value = 'initial'
  questionnaire.value.reset()
  error.value = null
  currentStep.value = 0
  showTyping.value = false
  
  // Stop any ongoing voice recording
  if (voiceRecording.value.isRecording) {
    stopVoiceRecording()
  }

  toast.info('Conversation cleared. Ready for a new consultation.')
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