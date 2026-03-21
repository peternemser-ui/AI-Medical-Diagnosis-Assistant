<template>
  <div class="border-t p-4 backdrop-blur-xl" :class="isDark ? 'bg-slate-900/95 border-slate-700/50' : 'bg-white/95 border-gray-200'">
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
                  {{ isListening ? 'Listening...' : (isProcessingSpeech ? 'Processing...' : 'Paused') }}
                </span>
                <span v-if="isListening" class="text-xs font-mono" :class="isDark ? 'text-slate-500' : 'text-gray-500'">{{ formatTime(listenTime) }}</span>
              </div>
              <button
                @click="exitHandsFree"
                class="text-xs px-2 py-1 rounded transition-colors"
                :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-gray-500 hover:text-gray-900 hover:bg-gray-200'"
              >
                Exit voice mode
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
              <span class="text-[10px]" :class="isDark ? 'text-slate-500' : 'text-gray-500'">Sending in {{ silenceCountdown }}s...</span>
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
            {{ isListening ? 'Pause mic' : 'Resume mic' }}
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
            Send
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

        <div class="flex items-end space-x-3">
          <!-- Sound/TTS toggle -->
          <button
            @click="emit('sound-toggle')"
            :class="soundToggleClasses"
            class="flex-shrink-0 p-2 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
            :title="soundEnabled ? 'Sound ON' : 'Sound OFF'"
          >
            <svg v-if="soundEnabled" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
            </svg>
          </button>

          <!-- Voice settings button -->
          <button
            @click="emit('open-voice-settings')"
            class="flex-shrink-0 p-2 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
            :class="isDark ? 'bg-slate-700 hover:bg-slate-600 text-slate-300' : 'bg-gray-200 hover:bg-gray-300 text-gray-600'"
            title="Voice &amp; avatar settings"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>

          <!-- Hands-free voice mode button -->
          <button
            @click="enterHandsFree"
            :disabled="disabled || isProcessing"
            class="flex-shrink-0 p-2 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105 bg-blue-600 hover:bg-blue-700 text-white"
            :class="{ 'bg-gray-600 text-gray-400 cursor-not-allowed': disabled || isProcessing, 'bg-blue-600 hover:bg-blue-700 text-white': !(disabled || isProcessing) }"
            title="Enter hands-free voice mode"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </button>

          <!-- Image upload button -->
          <button
            @click="triggerImageUpload"
            :disabled="disabled || isProcessing"
            class="flex-shrink-0 p-2 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
            :class="imageBase64 ? 'bg-emerald-600 hover:bg-emerald-700 text-white' : (isDark ? 'bg-slate-700 hover:bg-slate-600 text-slate-300' : 'bg-gray-200 hover:bg-gray-300 text-gray-600')"
            title="Upload an image for visual diagnosis"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
          <input
            ref="fileInputRef"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleImageSelected"
          />

          <!-- Text input -->
          <div class="flex-1 relative">
            <textarea
              ref="textareaRef"
              v-model="currentMessage"
              @keydown="handleKeydown"
              @input="adjustTextareaHeight"
              :disabled="disabled"
              :placeholder="placeholderText"
              aria-label="Message input"
              class="w-full rounded-xl px-4 py-3.5 text-base resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/50 border focus:border-transparent transition-all duration-200 input-gradient-focus"
              :class="isDark ? 'bg-slate-800 text-white border-slate-700/50 placeholder-slate-500' : 'bg-gray-100 text-gray-900 border-gray-300 placeholder-gray-400'"
              :style="{ height: textareaHeight + 'px' }"
              rows="1"
            ></textarea>
            <!-- Keyboard hint -->
            <div v-if="currentMessage.length > 0 && !disabled" class="absolute right-2 bottom-1 text-[9px] pointer-events-none" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
              <kbd class="px-1 py-0.5 rounded text-[8px] border" :class="isDark ? 'border-slate-700 bg-slate-800' : 'border-slate-300 bg-slate-100'">Enter</kbd> send
            </div>
          </div>

          <!-- Send button -->
          <button
            @click="handleSend"
            :disabled="!canSend"
            class="flex-shrink-0 p-2 sm:p-3 rounded-full transition-all duration-200 transform hover:scale-105"
            :class="sendButtonClasses"
            title="Send message"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  disabled: { type: Boolean, default: false },
  isProcessing: { type: Boolean, default: false },
  isSpeaking: { type: Boolean, default: false },
  voiceEnabled: { type: Boolean, default: true },
  soundEnabled: { type: Boolean, default: false },
  quickActions: { type: Array, default: () => [] }
})

const emit = defineEmits([
  'send-message', 'start-recording', 'stop-recording',
  'voice-toggle', 'sound-toggle', 'quick-action', 'open-voice-settings'
])

// ── Standard input state ──
const currentMessage = ref('')
const textareaRef = ref(null)
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
  if (props.disabled) return 'Please wait...'
  if (props.isProcessing) return 'Agents are analyzing your case...'
  return 'Type or click the mic for voice mode...'
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

// ── Image upload ──
function triggerImageUpload() {
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
    emit('send-message', '') // trigger error in parent
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
  recognition.lang = 'en-US'
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

onMounted(() => { textareaRef.value?.focus() })
onUnmounted(() => { exitHandsFree(); stopWaveform() })

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
