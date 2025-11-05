import { ref, onUnmounted } from 'vue'

/**
 * Voice Recognition and Speech Synthesis Composable
 * Handles voice input and text-to-speech functionality
 */
export function useVoice() {
  const isRecording = ref(false)
  const isSupported = ref(false)
  const isSpeaking = ref(false)
  const voiceEnabled = ref(true)
  const soundEnabled = ref(false)

  const speechRecognition = ref(null)
  const speechSynthesis = ref(null)
  const mediaRecorder = ref(null)
  const mediaStream = ref(null)
  const audioChunks = ref([])

  /**
   * Initialize voice capabilities
   */
  function initialize() {
    console.log('🔧 Initializing voice capabilities...')

    try {
      // Initialize Speech Recognition
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition
        speechRecognition.value = new SpeechRecognitionClass()

        speechRecognition.value.continuous = false
        speechRecognition.value.interimResults = false
        speechRecognition.value.lang = 'en-US'

        console.log('✅ Speech recognition initialized')
      } else {
        console.warn('⚠️ Speech recognition not supported')
        voiceEnabled.value = false
      }

      // Initialize Speech Synthesis
      if ('speechSynthesis' in window) {
        speechSynthesis.value = window.speechSynthesis

        // Load voices
        if (speechSynthesis.value.getVoices().length === 0) {
          speechSynthesis.value.addEventListener('voiceschanged', () => {
            console.log('🔊 Voices loaded:', speechSynthesis.value.getVoices().length)
          })
        } else {
          console.log('🔊 Voices available:', speechSynthesis.value.getVoices().length)
        }

        console.log('✅ Speech synthesis initialized')
      } else {
        console.warn('⚠️ Speech synthesis not supported')
      }

      // Check MediaRecorder support
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        isSupported.value = true
        console.log('✅ Media recording supported')
      } else {
        console.warn('⚠️ Media recording not supported')
        voiceEnabled.value = false
      }
    } catch (error) {
      console.error('❌ Error initializing voice capabilities:', error)
      voiceEnabled.value = false
      speechSynthesis.value = null
      speechRecognition.value = null
    }
  }

  /**
   * Start voice recording
   */
  async function startRecording(onResult, onError) {
    if (!speechRecognition.value) {
      onError?.('Speech recognition not available')
      return
    }

    try {
      isRecording.value = true

      speechRecognition.value.onresult = (event) => {
        try {
          const transcript = event.results[0][0].transcript
          console.log('🎤 Voice recognized:', transcript)
          isRecording.value = false
          onResult?.(transcript)
        } catch (err) {
          console.error('❌ Error processing voice result:', err)
          isRecording.value = false
          onError?.('Failed to process voice input')
        }
      }

      speechRecognition.value.onerror = (event) => {
        console.error('❌ Speech recognition error:', event.error)
        isRecording.value = false

        let errorMessage = 'Voice recognition failed'
        if (event.error === 'not-allowed' || event.error === 'permission-denied') {
          errorMessage = 'Microphone access denied. Please enable microphone permissions.'
        } else if (event.error === 'no-speech') {
          errorMessage = 'No speech detected. Please try again.'
        } else if (event.error === 'network') {
          errorMessage = 'Network error. Please check your connection.'
        }

        onError?.(errorMessage)
      }

      speechRecognition.value.onend = () => {
        isRecording.value = false
      }

      speechRecognition.value.start()
    } catch (error) {
      console.error('❌ Error starting recording:', error)
      isRecording.value = false
      onError?.('Failed to start voice recording')
    }
  }

  /**
   * Stop voice recording
   */
  function stopRecording() {
    if (speechRecognition.value && isRecording.value) {
      try {
        speechRecognition.value.stop()
        isRecording.value = false
        console.log('✅ Recording stopped')
      } catch (error) {
        console.error('❌ Error stopping recording:', error)
      }
    }
  }

  /**
   * Speak text using speech synthesis
   */
  function speak(text, options = {}) {
    if (!speechSynthesis.value || !soundEnabled.value) {
      console.log('🔇 Speech synthesis disabled or not available')
      return
    }

    try {
      // Cancel any ongoing speech
      speechSynthesis.value.cancel()

      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = options.rate || 1.2
      utterance.pitch = options.pitch || 1.0
      utterance.volume = options.volume || 0.8
      utterance.lang = options.lang || 'en-US'

      // Select voice if specified
      if (options.voice) {
        const voices = speechSynthesis.value.getVoices()
        const selectedVoice = voices.find(v => v.name === options.voice)
        if (selectedVoice) {
          utterance.voice = selectedVoice
        }
      }

      utterance.onstart = () => {
        isSpeaking.value = true
        console.log('🔊 Speaking:', text.substring(0, 50) + '...')
      }

      utterance.onend = () => {
        isSpeaking.value = false
        console.log('✅ Speech completed')
      }

      utterance.onerror = (error) => {
        isSpeaking.value = false
        console.error('❌ Speech synthesis error:', error)
      }

      speechSynthesis.value.speak(utterance)
    } catch (error) {
      console.error('❌ Error speaking text:', error)
      isSpeaking.value = false
    }
  }

  /**
   * Stop speaking
   */
  function stopSpeaking() {
    if (speechSynthesis.value) {
      speechSynthesis.value.cancel()
      isSpeaking.value = false
      console.log('🔇 Speech cancelled')
    }
  }

  /**
   * Toggle sound on/off
   */
  function toggleSound() {
    soundEnabled.value = !soundEnabled.value
    console.log('🔊 Sound toggled:', soundEnabled.value ? 'ON' : 'OFF')

    if (soundEnabled.value) {
      // Play test sound
      setTimeout(() => {
        speak('Voice enabled', { rate: 1.2, volume: 0.8 })
      }, 100)
    } else {
      stopSpeaking()
    }

    return soundEnabled.value
  }

  /**
   * Get available voices
   */
  function getAvailableVoices() {
    if (!speechSynthesis.value) return []
    return speechSynthesis.value.getVoices()
  }

  /**
   * Set language for voice recognition
   */
  function setLanguage(lang) {
    if (speechRecognition.value) {
      speechRecognition.value.lang = lang
      console.log('🌐 Language set to:', lang)
    }
  }

  /**
   * Cleanup resources
   */
  function cleanup() {
    stopRecording()
    stopSpeaking()

    if (mediaStream.value) {
      mediaStream.value.getTracks().forEach(track => track.stop())
      mediaStream.value = null
    }

    console.log('🧹 Voice resources cleaned up')
  }

  // Cleanup on unmount
  onUnmounted(() => {
    cleanup()
  })

  return {
    // State
    isRecording,
    isSupported,
    isSpeaking,
    voiceEnabled,
    soundEnabled,

    // Methods
    initialize,
    startRecording,
    stopRecording,
    speak,
    stopSpeaking,
    toggleSound,
    getAvailableVoices,
    setLanguage,
    cleanup
  }
}
