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
      <div class="bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-hidden">
        <!-- Header -->
        <div class="flex items-center justify-between p-6 border-b border-gray-700">
          <h2 class="text-2xl font-bold text-white flex items-center">
            <svg class="w-6 h-6 mr-2 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Help & Guide
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
        <div class="overflow-y-auto max-h-[70vh]">
          <!-- Tab Navigation -->
          <div class="flex border-b border-gray-700 bg-gray-900">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="px-6 py-3 text-sm font-medium transition-colors duration-200"
              :class="activeTab === tab.id 
                ? 'text-blue-400 border-b-2 border-blue-500 bg-gray-800' 
                : 'text-gray-400 hover:text-white hover:bg-gray-800'"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- Tab Content -->
          <div class="p-6">
            <!-- Getting Started Tab -->
            <div v-if="activeTab === 'getting-started'" class="space-y-6">
              <div>
                <h3 class="text-lg font-semibold text-white mb-3">Welcome to AI Health Assistant</h3>
                <p class="text-gray-300 leading-relaxed mb-4">
                  This AI-powered health assistant helps you understand your symptoms and provides personalized health guidance. 
                  Here's how to get the most out of your experience:
                </p>
                
                <div class="space-y-4">
                  <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span class="text-white font-semibold text-sm">1</span>
                    </div>
                    <div>
                      <h4 class="font-medium text-white mb-1">Start the Conversation</h4>
                      <p class="text-gray-400 text-sm">Describe your symptoms in detail using voice or text input.</p>
                    </div>
                  </div>
                  
                  <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span class="text-white font-semibold text-sm">2</span>
                    </div>
                    <div>
                      <h4 class="font-medium text-white mb-1">Answer Questions</h4>
                      <p class="text-gray-400 text-sm">The AI will ask follow-up questions to better understand your condition.</p>
                    </div>
                  </div>
                  
                  <div class="flex items-start space-x-3">
                    <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                      <span class="text-white font-semibold text-sm">3</span>
                    </div>
                    <div>
                      <h4 class="font-medium text-white mb-1">Get Insights</h4>
                      <p class="text-gray-400 text-sm">Receive personalized health insights and recommendations.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Voice Features Tab -->
            <div v-else-if="activeTab === 'voice-features'" class="space-y-6">
              <div>
                <h3 class="text-lg font-semibold text-white mb-3">Voice Features</h3>
                <p class="text-gray-300 leading-relaxed mb-4">
                  Take advantage of advanced voice capabilities for a hands-free experience:
                </p>
                
                <div class="space-y-4">
                  <div class="bg-gray-700 bg-opacity-50 rounded-lg p-4">
                    <h4 class="font-medium text-white mb-2 flex items-center">
                      <svg class="w-5 h-5 mr-2 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                      </svg>
                      Voice Recording
                    </h4>
                    <p class="text-gray-400 text-sm mb-2">Click the microphone button to record your voice input.</p>
                    <ul class="text-gray-400 text-sm space-y-1 ml-4">
                      <li>• Maximum recording time: 60 seconds</li>
                      <li>• Automatically processed when you stop recording</li>
                      <li>• Clear speech in a quiet environment works best</li>
                    </ul>
                  </div>
                  
                  <div class="bg-gray-700 bg-opacity-50 rounded-lg p-4">
                    <h4 class="font-medium text-white mb-2 flex items-center">
                      <svg class="w-5 h-5 mr-2 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 14.142M13 12a1 1 0 11-2 0 1 1 0 012 0z" />
                      </svg>
                      Audio Responses
                    </h4>
                    <p class="text-gray-400 text-sm mb-2">AI responses can be played back as audio.</p>
                    <ul class="text-gray-400 text-sm space-y-1 ml-4">
                      <li>• Toggle audio playback in settings</li>
                      <li>• Adjust playback speed if needed</li>
                      <li>• Audio controls available for each response</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- FAQ Tab -->
            <div v-else-if="activeTab === 'faq'" class="space-y-4">
              <h3 class="text-lg font-semibold text-white mb-3">Frequently Asked Questions</h3>
              
              <div class="space-y-3">
                <div v-for="faq in faqs" :key="faq.id" class="bg-gray-700 bg-opacity-50 rounded-lg">
                  <button
                    @click="toggleFaq(faq.id)"
                    class="w-full text-left p-4 flex justify-between items-center hover:bg-gray-600 hover:bg-opacity-50 transition-colors duration-200"
                  >
                    <span class="font-medium text-white">{{ faq.question }}</span>
                    <svg 
                      class="w-5 h-5 text-gray-400 transition-transform duration-200"
                      :class="{ 'rotate-180': faq.open }"
                      fill="none" 
                      stroke="currentColor" 
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  <div v-if="faq.open" class="px-4 pb-4">
                    <p class="text-gray-300 text-sm leading-relaxed">{{ faq.answer }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Privacy & Security Tab -->
            <div v-else-if="activeTab === 'privacy'" class="space-y-6">
              <div>
                <h3 class="text-lg font-semibold text-white mb-3">Privacy & Security</h3>
                
                <div class="space-y-4">
                  <div class="bg-green-900 bg-opacity-30 border border-green-600 rounded-lg p-4">
                    <h4 class="font-medium text-green-400 mb-2 flex items-center">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                      Your Data is Protected
                    </h4>
                    <ul class="text-green-200 text-sm space-y-1">
                      <li>• Conversations are not stored permanently</li>
                      <li>• Voice recordings are processed securely</li>
                      <li>• No personal health data is saved to external databases</li>
                      <li>• All data transmission is encrypted</li>
                    </ul>
                  </div>
                  
                  <div class="bg-yellow-900 bg-opacity-30 border border-yellow-600 rounded-lg p-4">
                    <h4 class="font-medium text-yellow-400 mb-2 flex items-center">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                      </svg>
                      Important Medical Disclaimer
                    </h4>
                    <p class="text-yellow-200 text-sm leading-relaxed">
                      This AI assistant provides general health information only. It is not a substitute for professional medical advice, 
                      diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="border-t border-gray-700 p-4 bg-gray-900">
          <div class="flex justify-between items-center">
            <div class="text-sm text-gray-400">
              Need more help? Contact support
            </div>
            <button
              @click="$emit('close')"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors duration-200"
            >
              Got it
            </button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const activeTab = ref('getting-started')

const tabs = [
  { id: 'getting-started', label: 'Getting Started' },
  { id: 'voice-features', label: 'Voice Features' },
  { id: 'faq', label: 'FAQ' },
  { id: 'privacy', label: 'Privacy & Security' }
]

const faqs = ref([
  {
    id: 1,
    question: 'How accurate is the AI diagnosis?',
    answer: 'The AI provides general health insights based on common symptom patterns. It is not a replacement for professional medical diagnosis and should be used as a guide only. Always consult healthcare professionals for accurate diagnosis.',
    open: false
  },
  {
    id: 2,
    question: 'Can I use this for emergency situations?',
    answer: 'No, this tool is not designed for medical emergencies. If you are experiencing a medical emergency, call emergency services immediately or go to the nearest emergency room.',
    open: false
  },
  {
    id: 3,
    question: 'Is my voice data stored?',
    answer: 'Voice recordings are processed for speech recognition and then discarded. No audio data is permanently stored on our servers.',
    open: false
  },
  {
    id: 4,
    question: 'What if the AI doesn\'t understand my symptoms?',
    answer: 'Try describing your symptoms in different ways, use simpler language, or break down complex symptoms into smaller parts. You can also use text input if voice recognition is having difficulties.',
    open: false
  },
  {
    id: 5,
    question: 'Can I share my results with my doctor?',
    answer: 'While the conversation is not permanently stored, you can take screenshots or notes of the recommendations to discuss with your healthcare provider.',
    open: false
  }
])

const toggleFaq = (id) => {
  const faq = faqs.value.find(f => f.id === id)
  if (faq) {
    faq.open = !faq.open
  }
}
</script>

<style scoped>
/* Custom scrollbar for content area */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(75, 85, 99, 0.2);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(75, 85, 99, 0.6);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(75, 85, 99, 0.8);
}

/* Smooth rotation for FAQ arrows */
.rotate-180 {
  transform: rotate(180deg);
}
</style>
