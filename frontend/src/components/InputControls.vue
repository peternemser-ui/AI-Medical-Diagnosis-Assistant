<template>
  <div class="border-t p-4 backdrop-blur-xl shadow-[0_-1px_3px_0_rgb(0_0_0/0.04)]" style="background: var(--clinical-surface); border-color: var(--clinical-border)">
    <div class="max-w-4xl mx-auto">

      <!-- ══ HANDS-FREE VOICE MODE (full takeover) ══ -->
      <div v-if="handsFreeMode" class="space-y-3">
        <!-- Waveform + transcript -->
        <div class="rounded-xl overflow-hidden border" :class="[isDark ? 'bg-slate-950/90' : 'bg-gray-50', isListening ? 'border-blue-500/40' : (isDark ? 'border-slate-700/30' : 'border-gray-300')]">
          <!-- Waveform canvas -->
          <div class="relative h-12 sm:h-16 flex items-center">
            <canvas ref="waveformCanvas" class="absolute inset-0 w-full h-full"></canvas>
            <div class="relative z-10 flex items-center justify-between w-full px-4">
              <div class="flex items-center gap-3">
                <div class="w-3 h-3 rounded-full shadow-lg" :class="isListening ? 'bg-blue-500 animate-pulse shadow-blue-500/50' : (isDark ? 'bg-slate-600' : 'bg-gray-400')"></div>
                <span class="text-sm font-medium" :class="isListening ? 'text-blue-400' : (isDark ? 'text-slate-500' : 'text-gray-500')">
                  {{ isListening ? t('input.listening') : (isProcessingSpeech ? t('input.processing') : t('input.paused')) }}
                </span>
                <span v-if="isListening" class="text-xs font-mono" :class="isDark ? 'text-slate-500' : 'text-gray-500'">{{ formatTime(listenTime) }}</span>
              </div>
              <button
                @click="exitHandsFree"
                class="text-xs font-semibold px-3 py-1.5 rounded-lg border transition-colors flex items-center gap-1.5"
                :class="isDark ? 'text-red-400 border-red-500/30 bg-red-500/10 hover:bg-red-500/20 hover:text-red-300' : 'text-red-600 border-red-300 bg-red-50 hover:bg-red-100'"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                {{ t('input.exitVoiceMode') }}
              </button>
            </div>
          </div>

          <!-- Live transcript -->
          <div v-if="liveTranscript || interimText" class="px-4 py-3 border-t" :class="isDark ? 'border-slate-800/50' : 'border-gray-200'">
            <div class="text-sm leading-relaxed" :class="isDark ? 'text-white' : 'text-gray-900'">
              <span>{{ liveTranscript }}</span>
              <span class="text-blue-400/60 italic">{{ interimText }}</span>
              <span v-if="isListening && !interimText" class="inline-block w-0.5 h-4 bg-blue-400 animate-pulse ml-0.5 align-middle"></span>
            </div>
            <div v-if="silenceCountdown > 0 && liveTranscript" class="mt-2 flex items-center gap-2">
              <div class="h-1 flex-1 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-gray-200'">
                <div class="h-full bg-blue-500 transition-all duration-1000 rounded-full" :style="{ width: ((3 - silenceCountdown) / 3 * 100) + '%' }"></div>
              </div>
              <span class="text-detail" :class="isDark ? 'text-slate-500' : 'text-gray-500'">{{ t('input.sendingIn').replace('{n}', silenceCountdown) }}</span>
            </div>
          </div>
        </div>

        <!-- Voice mode controls -->
        <div class="flex flex-wrap items-center gap-2">
          <!-- Mute/unmute (big toggle) -->
          <button
            @click="toggleMute"
            class="flex-1 py-2 sm:py-3 rounded-xl font-medium text-sm transition-all flex items-center justify-center gap-2"
            :class="isListening
              ? 'bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30'
              : 'bg-blue-600 text-white hover:bg-blue-700'"
          >
            <svg v-if="isListening" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            {{ isListening ? t('input.pauseMic') : t('input.resumeMic') }}
          </button>

          <!-- Send now -->
          <button
            @click="sendTranscript"
            :disabled="!liveTranscript.trim()"
            class="py-2 sm:py-3 px-4 sm:px-5 rounded-xl font-medium text-sm transition-all flex items-center gap-2"
            :class="liveTranscript.trim()
              ? 'bg-emerald-600 text-white hover:bg-emerald-700'
              : (isDark ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-gray-200 text-gray-400 cursor-not-allowed')"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
            {{ t('input.send') }}
          </button>

          <!-- Sound toggle -->
          <button
            @click="emit('sound-toggle')"
            class="p-2 sm:p-3 rounded-xl transition-colors"
            :class="soundEnabled ? 'bg-green-600/20 text-green-400 border border-green-500/30' : (isDark ? 'bg-slate-800 text-slate-500' : 'bg-gray-200 text-gray-500')"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            </svg>
          </button>
        </div>
      </div>

      <!-- ══ STANDARD INPUT MODE ══ -->
      <div v-else>
        <!-- Image preview above input -->
        <div v-if="imagePreview" class="mb-2 relative inline-block">
          <img :src="imagePreview" alt="Upload preview" class="h-20 rounded-lg border object-cover" :class="isDark ? 'border-slate-600/50' : 'border-gray-300'" />
          <button
            @click="removeImage"
            class="absolute -top-2 -right-2 w-5 h-5 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center text-xs leading-none transition-colors"
            title="Remove image"
          >&times;</button>
        </div>

        <div class="flex items-end space-x-2 sm:space-x-3" role="toolbar" aria-label="Message controls">
          <!-- Sound/TTS toggle -->
          <button
            @click="emit('sound-toggle')"
            :class="soundToggleClasses"
            class="flex-shrink-0 p-1.5 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
            :title="soundEnabled ? 'Sound ON' : 'Sound OFF'"
            :aria-label="soundEnabled ? 'Turn sound off' : 'Turn sound on'"
          >
            <svg v-if="soundEnabled" class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            </svg>
            <svg v-else class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
          </button>

          <!-- Avatar/Chat mode toggle -->
          <button
            @click="emit('avatar-toggle')"
            class="flex-shrink-0 p-1.5 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
            :class="avatarMode
              ? (isDark ? 'bg-blue-500/20 text-blue-400 ring-1 ring-blue-500/30' : 'bg-blue-100 text-blue-600 ring-1 ring-blue-300')
              : (isDark ? 'bg-slate-700 hover:bg-slate-600 text-slate-300' : 'bg-gray-200 hover:bg-gray-300 text-gray-600')"
            :title="avatarMode ? 'Switch to Chat mode' : 'Switch to Avatar mode'"
            :aria-label="avatarMode ? 'Switch to Chat mode' : 'Switch to Avatar mode'"
          >
            <svg v-if="!avatarMode" class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14c-4 0-7 2-7 4v1h14v-1c0-2-3-4-7-4z"/></svg>
            <svg v-else class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          </button>

          <!-- Hands-free voice mode button -->
          <button
            @click="enterHandsFree"
            :disabled="disabled || isProcessing"
            class="flex-shrink-0 p-1.5 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105 bg-blue-600 hover:bg-blue-700 text-white"
            :class="{ 'bg-gray-600 text-gray-400 cursor-not-allowed': disabled || isProcessing, 'bg-blue-600 hover:bg-blue-700 text-white': !(disabled || isProcessing) }"
            title="Enter hands-free voice mode"
            aria-label="Enter hands-free voice mode"
          >
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </button>

          <!-- Image/Camera button with dropdown -->
          <div class="relative flex-shrink-0">
            <button
              @click="toggleImageMenu"
              :disabled="disabled || isProcessing"
              class="p-1.5 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
              :class="imageBase64 ? 'bg-emerald-600 hover:bg-emerald-700 text-white' : (isDark ? 'bg-slate-700 hover:bg-slate-600 text-slate-300' : 'bg-gray-200 hover:bg-gray-300 text-gray-600')"
              title="Add image for visual diagnosis"
              aria-label="Add image for visual diagnosis"
            >
              <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>

            <!-- Dropdown menu -->
            <div
              v-if="showImageMenu"
              class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 rounded-xl border shadow-xl overflow-hidden z-50"
              :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'"
            >
              <button
                @click="openCameraCapture"
                class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors text-left"
                :class="isDark ? 'text-white hover:bg-slate-700' : 'text-slate-900 hover:bg-slate-50'"
              >
                <svg class="w-5 h-5 flex-shrink-0" :class="isDark ? 'text-blue-400' : 'text-blue-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {{ t('input.takePhoto') }}
              </button>
              <div class="h-px" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>
              <button
                @click="triggerImageUpload"
                class="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors text-left"
                :class="isDark ? 'text-white hover:bg-slate-700' : 'text-slate-900 hover:bg-slate-50'"
              >
                <svg class="w-5 h-5 flex-shrink-0" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {{ t('input.uploadImageBtn') }}
              </button>
            </div>
          </div>
          <input
            ref="fileInputRef"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleImageSelected"
          />

          <!-- Text input with autocomplete -->
          <div class="flex-1 relative">
            <SymptomAutocomplete
              ref="autocompleteRef"
              :query="currentMessage"
              :visible="showAutocomplete"
              @select="handleAutocompleteSelect"
            />
            <textarea
              ref="textareaRef"
              v-model="currentMessage"
              @keydown="handleKeydown"
              @input="adjustTextareaHeight"
              @focus="showAutocomplete = true"
              @blur="showAutocomplete = false"
              :disabled="disabled"
              :placeholder="placeholderText"
              aria-label="Type your message"
              class="input w-full rounded-input px-4 py-3.5 text-body-lg resize-none transition-all duration-200"
              :style="{ height: textareaHeight + 'px' }"
              rows="1"
            ></textarea>
            <!-- Keyboard hint -->
            <div v-if="currentMessage.length > 0 && !disabled" class="absolute right-2 bottom-1 text-tiny pointer-events-none" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
              <kbd class="px-1 py-0.5 rounded text-micro border" :class="isDark ? 'border-slate-700 bg-slate-800' : 'border-slate-300 bg-slate-100'">Enter</kbd> {{ t('input.enterSend') }}
            </div>
          </div>

          <!-- Send button -->
          <button
            @click="handleSend"
            :disabled="!canSend"
            class="flex-shrink-0 p-1.5 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
            :class="sendButtonClasses"
            title="Send message"
            aria-label="Send message"
          >
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import SymptomAutocomplete from '@/components/SymptomAutocomplete.vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'

const { isDark } = useTheme()
const { t } = useI18n()

const props = defineProps({
  disabled: { type: Boolean, default: false },
  isProcessing: { type: Boolean, default: false },
  isSpeaking: { type: Boolean, default: false },
  voiceEnabled: { type: Boolean, default: true },
  soundEnabled: { type: Boolean, default: false },
  avatarMode: { type: Boolean, default: false },
  quickActions: { type: Array, default: () => [] }
})

const emit = defineEmits([
  'send-message', 'start-recording', 'stop-recording',
  'voice-toggle', 'sound-toggle', 'avatar-toggle', 'quick-action', 'open-voice-settings',
  'open-camera'
])

// ── Standard input state ──
const currentMessage = ref('')
const textareaRef = ref(null)
const autocompleteRef = ref(null)
const showAutocomplete = ref(false)

function handleAutocompleteSelect(term) {
  currentMessage.value = term
  showAutocomplete.value = false
  nextTick(() => textareaRef.value?.focus())
}
const fileInputRef = ref(null)
const textareaHeight = ref(48)
const MIN_HEIGHT = 48
const MAX_HEIGHT = 120

// ── Image upload state ──
const imageBase64 = ref(null)
const imagePreview = ref(null)

// ── Hands-free voice state ──
const handsFreeMode = ref(false)
const isListening = ref(false)
const isProcessingSpeech = ref(false)
const liveTranscript = ref('')
const interimText = ref('')
const listenTime = ref(0)
const silenceCountdown = ref(0)
const waveformCanvas = ref(null)

let recognition = null
let listenTimer = null
let silenceTimer = null
let silenceInterval = null
let audioContext = null
let analyser = null
let micStream = null
let animationId = null
const SILENCE_DELAY = 3 // seconds of silence before auto-send

// ── Computed ──
const canSend = computed(() => !props.disabled && !props.isProcessing && (currentMessage.value.trim().length > 0 || imageBase64.value))

const placeholderText = computed(() => {
  if (props.disabled) return t('input.placeholderWait')
  if (props.isProcessing) return t('input.placeholderProcessing')
  return t('input.placeholder')
})

const soundToggleClasses = computed(() => ({
  'bg-green-600 hover:bg-green-700 text-white': props.soundEnabled,
  'bg-gray-600 hover:bg-gray-700 text-gray-300': !props.soundEnabled && isDark.value,
  'bg-gray-200 hover:bg-gray-300 text-gray-600': !props.soundEnabled && !isDark.value
}))

const sendButtonClasses = computed(() => ({
  'bg-blue-600 hover:bg-blue-700 text-white': canSend.value,
  'bg-gray-600 text-gray-400 cursor-not-allowed': !canSend.value && isDark.value,
  'bg-gray-200 text-gray-400 cursor-not-allowed': !canSend.value && !isDark.value
}))

// ── Image menu ──
const showImageMenu = ref(false)

function toggleImageMenu() {
  if (props.disabled || props.isProcessing) return
  showImageMenu.value = !showImageMenu.value
}

function openCameraCapture() {
  showImageMenu.value = false
  emit('open-camera')
}

// Close image menu when clicking outside
function handleDocumentClick(e) {
  if (showImageMenu.value) {
    showImageMenu.value = false
  }
}

// ── Image upload ──
function triggerImageUpload() {
  showImageMenu.value = false
  if (props.disabled || props.isProcessing) return
  fileInputRef.value?.click()
}

function handleImageSelected(event) {
  const file = event.target.files?.[0]
  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    const dataUrl = e.target.result
    imagePreview.value = dataUrl
    // Strip the data:image/...;base64, prefix to get raw base64
    imageBase64.value = dataUrl.split(',')[1]
  }
  reader.readAsDataURL(file)

  // Reset file input so the same file can be re-selected
  event.target.value = ''
}

function removeImage() {
  imageBase64.value = null
  imagePreview.value = null
}

// ── Standard input ──
const handleSend = () => {
  if (!canSend.value) return
  const msg = currentMessage.value.trim() || (imageBase64.value ? '[Image attached]' : '')
  emit('send-message', msg, imageBase64.value || null)
  currentMessage.value = ''
  imageBase64.value = null
  imagePreview.value = null
  textareaHeight.value = MIN_HEIGHT
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() }
}

const adjustTextareaHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
      textareaHeight.value = Math.min(Math.max(textareaRef.value.scrollHeight, MIN_HEIGHT), MAX_HEIGHT)
    }
  })
}

// ── Hands-free voice mode ──
function enterHandsFree() {
  if (props.disabled || props.isProcessing) return

  const SRC = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SRC) {
    alert('Voice input requires Google Chrome or Microsoft Edge.\n\nPlease open this app in Chrome for full voice features.')
    return
  }

  handsFreeMode.value = true
  liveTranscript.value = ''
  interimText.value = ''
  listenTime.value = 0
  silenceCountdown.value = 0

  // Init recognition
  recognition = new SRC()
  recognition.continuous = true
  recognition.interimResults = true
  const { lang: currentLang } = useI18n()
  const STT_LANGS = { en:'en-US', es:'es-ES', fr:'fr-FR', zh:'zh-CN', hi:'hi-IN', ar:'ar-SA', de:'de-DE', pt:'pt-BR', ja:'ja-JP', ko:'ko-KR', ru:'ru-RU', it:'it-IT' }
  recognition.lang = STT_LANGS[currentLang.value] || 'en-US'
  recognition.maxAlternatives = 1

  recognition.onresult = (event) => {
    let final = ''
    let interim = ''
    for (let i = 0; i < event.results.length; i++) {
      const t = event.results[i][0].transcript
      if (event.results[i].isFinal) {
        final += t + ' '
      } else {
        interim += t
      }
    }
    if (final.trim()) {
      liveTranscript.value = (liveTranscript.value + ' ' + final).trim()
      // Reset silence timer — user just spoke
      resetSilenceTimer()
    }
    interimText.value = interim
  }

  recognition.onerror = (event) => {
    if (event.error === 'no-speech') {
      // Normal — just means silence, keep listening
      return
    }
    if (event.error === 'aborted') return
    if (event.error === 'not-allowed') {
      handsFreeMode.value = false
      return
    }
  }

  recognition.onend = () => {
    // Auto-restart if still in hands-free mode and listening
    if (handsFreeMode.value && isListening.value) {
      try { recognition.start() } catch (_) {}
    }
  }

  startListening()
}

function startListening() {
  if (!recognition) return
  try { recognition.start() } catch (_) {}
  isListening.value = true
  listenTime.value = 0
  listenTimer = setInterval(() => { listenTime.value++ }, 1000)

  // Start waveform
  nextTick(() => startWaveform())
}

function stopListening() {
  isListening.value = false
  if (listenTimer) { clearInterval(listenTimer); listenTimer = null }
  try { recognition?.stop() } catch (_) {}
  stopWaveform()
  clearSilenceTimer()
}

function toggleMute() {
  if (isListening.value) {
    stopListening()
  } else {
    interimText.value = ''
    startListening()
  }
}

function resetSilenceTimer() {
  clearSilenceTimer()
  silenceCountdown.value = SILENCE_DELAY

  silenceInterval = setInterval(() => {
    silenceCountdown.value--
    if (silenceCountdown.value <= 0) {
      clearSilenceTimer()
      // Auto-send after silence
      if (liveTranscript.value.trim()) {
        sendTranscript()
      }
    }
  }, 1000)
}

function clearSilenceTimer() {
  if (silenceInterval) { clearInterval(silenceInterval); silenceInterval = null }
  silenceCountdown.value = 0
}

function sendTranscript() {
  const text = liveTranscript.value.trim()
  if (!text) return
  stopListening()
  clearSilenceTimer()
  isProcessingSpeech.value = true
  emit('send-message', text)

  // Reset and resume listening after a delay (wait for AI to respond)
  liveTranscript.value = ''
  interimText.value = ''

  // Don't resume immediately — wait for parent's isProcessing to go false
  // The watcher below handles resuming after the doctor finishes speaking
  isProcessingSpeech.value = false
}

function exitHandsFree() {
  stopListening()
  clearSilenceTimer()
  handsFreeMode.value = false
  isProcessingSpeech.value = false
  liveTranscript.value = ''
  interimText.value = ''
  if (recognition) { try { recognition.abort() } catch (_) {} recognition = null }
  stopWaveform()
}

// ── Waveform ──
async function startWaveform() {
  try {
    audioContext = new (window.AudioContext || window.webkitAudioContext)()
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const source = audioContext.createMediaStreamSource(micStream)
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 256
    analyser.smoothingTimeConstant = 0.7
    source.connect(analyser)
    drawWaveform()
  } catch (_) {}
}

function drawWaveform() {
  if (!analyser || !waveformCanvas.value) return
  const canvas = waveformCanvas.value
  const ctx = canvas.getContext('2d')
  const bufferLength = analyser.frequencyBinCount
  const dataArray = new Uint8Array(bufferLength)
  const rect = canvas.getBoundingClientRect()
  canvas.width = rect.width * window.devicePixelRatio
  canvas.height = rect.height * window.devicePixelRatio
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio)
  const W = rect.width, H = rect.height

  function render() {
    animationId = requestAnimationFrame(render)
    analyser.getByteFrequencyData(dataArray)
    ctx.clearRect(0, 0, W, H)
    const barCount = 80, gap = 1.5
    const barWidth = (W - gap * barCount) / barCount
    for (let i = 0; i < barCount; i++) {
      const dataIdx = Math.floor((i / barCount) * bufferLength)
      const value = dataArray[dataIdx] / 255
      const barHeight = Math.max(1.5, value * (H * 0.85))
      const r = Math.floor(80 + value * 120), g = Math.floor(120 + value * 80), b = Math.floor(220 + value * 35)
      ctx.fillStyle = `rgba(${r}, ${g}, ${b}, ${0.3 + value * 0.6})`
      const x = i * (barWidth + gap)
      ctx.beginPath()
      ctx.roundRect(x, H / 2 - barHeight / 2, barWidth, barHeight, 1)
      ctx.fill()
    }
  }
  render()
}

function stopWaveform() {
  if (animationId) { cancelAnimationFrame(animationId); animationId = null }
  if (micStream) { micStream.getTracks().forEach(t => t.stop()); micStream = null }
  if (audioContext && audioContext.state !== 'closed') { audioContext.close().catch(() => {}); audioContext = null }
  analyser = null
}

const formatTime = (s) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, '0')}`

watch(currentMessage, adjustTextareaHeight)

// Resume hands-free listening only when BOTH processing is done AND doctor is done speaking
watch(
  () => ({ processing: props.isProcessing, speaking: props.isSpeaking }),
  ({ processing, speaking }) => {
    if (!processing && !speaking && handsFreeMode.value && !isListening.value) {
      // Doctor finished speaking — safe to resume mic without picking up TTS
      setTimeout(() => {
        if (handsFreeMode.value && !props.isSpeaking) {
          liveTranscript.value = ''
          interimText.value = ''
          startListening()
        }
      }, 800) // Extra delay to ensure TTS audio fully fades
    }
  }
)

onMounted(() => {
  textareaRef.value?.focus()
  document.addEventListener('click', handleDocumentClick, true)
})
onUnmounted(() => {
  exitHandsFree()
  stopWaveform()
  document.removeEventListener('click', handleDocumentClick, true)
})

defineExpose({
  cleanup: () => { exitHandsFree() },
  focus: () => textareaRef.value?.focus()
})
</script>

<style scoped>
.input-gradient-focus:focus {
  border-color: transparent;
  outline: none;
  box-shadow: 0 0 0 1px #3b82f6, 0 0 0 3px rgba(139, 92, 246, 0.3);
}
</style>
