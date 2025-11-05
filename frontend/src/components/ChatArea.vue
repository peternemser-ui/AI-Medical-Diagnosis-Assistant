<template>
  <div class="flex-1 overflow-hidden flex flex-col" style="background-color: var(--chat-bg);">
    <!-- Conversation messages -->
    <div 
      ref="chatContainer"
      class="flex-1 overflow-y-auto p-4 space-y-4"
      :class="{ 'auto-scroll': autoScroll }"
    >
      <!-- Premium welcome message if no messages -->
      <div v-if="messages.length === 0" class="text-center py-8">
        <!-- State-of-the-art welcome card with glass morphism -->
        <div 
          class="premium-welcome-card"
          :style="{
            background: 'var(--glass-bg)',
            border: '1px solid var(--glass-border)',
            borderRadius: '24px',
            padding: '32px',
            maxWidth: '500px',
            margin: '0 auto',
            boxShadow: 'var(--glass-shadow)',
            backdropFilter: 'var(--glass-backdrop)',
            position: 'relative',
            overflow: 'hidden'
          }"
        >
          <!-- Premium glass overlay -->
          <div 
            class="glass-overlay"
            :style="{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'var(--gradient-glass)',
              opacity: 0.9,
              zIndex: 1,
              borderRadius: '24px'
            }"
          ></div>
          
          <!-- Content with proper z-index -->
          <div style="position: relative; z-index: 2;">
            <!-- Premium medical icon with gradient -->
            <div 
              class="premium-icon-container"
              :style="{
                background: 'var(--gradient-primary)',
                borderRadius: '20px',
                width: '60px',
                height: '60px',
                margin: '0 auto 20px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: 'var(--shadow-primary)'
              }"
            >
              <svg 
                class="w-8 h-8 text-white" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            
            <!-- Premium welcome text -->
            <h2 
              class="text-xl font-bold mb-3"
              :style="{ 
                color: 'var(--primary-700)',
                fontSize: '22px',
                fontWeight: '700',
                marginBottom: '12px'
              }"
            >
              AI Health Assistant
            </h2>
            
            <p 
              class="text-lg mb-4"
              :style="{ 
                color: 'var(--text)',
                fontSize: '16px',
                fontWeight: '500',
                marginBottom: '16px',
                lineHeight: '1.5'
              }"
            >
              Professional health guidance powered by advanced AI
            </p>
            
            <p 
              class="text-sm premium-subtitle"
              :style="{ 
                color: 'var(--text-subtle)',
                fontSize: '14px',
                fontWeight: '400',
                lineHeight: '1.6'
              }"
            >
              Let's start by discussing your symptoms. You can type or use voice input to describe how you're feeling.
            </p>
          </div>
        </div>
      </div>

      <!-- Message list -->
      <div 
        v-for="(message, index) in messages" 
        :key="message.id || index"
        class="flex"
        :class="{ 'justify-end': message.sender === 'user', 'justify-start': message.sender === 'assistant' }"
      >
        <div 
          class="max-w-[80%] relative"
          :class="getMessageContainerClasses(message)"
        >
          <!-- Thought bubble for assistant messages -->
          <div 
            v-if="message.sender === 'assistant'"
            class="assistant-message rounded-3xl p-4 shadow-lg relative"
          >
            <!-- Traditional thought bubble tail with properly positioned circles -->
            <div class="thought-bubble-tail">
              <div class="bubble-circle bubble-large"></div>
              <div class="bubble-circle bubble-medium"></div>
              <div class="bubble-circle bubble-small"></div>
            </div>
            
            <!-- Message header for assistant messages -->
            <div class="flex items-center mb-2">
              <div class="w-6 h-6 bg-gradient-to-br from-sky-500 to-cyan-500 rounded-full flex items-center justify-center mr-2">
                <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
              <span class="text-xs message-subtitle font-bold text-shadow">AI Health Assistant</span>
            </div>

            <!-- Message content -->
            <div class="message-content">
              <!-- Text content -->
              <div v-if="message.text" class="whitespace-pre-wrap" v-html="formatMessageText(message.text)"></div>
              
              <!-- Audio playback for voice messages -->
              <div v-if="message.audioUrl" class="mt-2">
                <audio :src="message.audioUrl" controls class="w-full"></audio>
              </div>

              <!-- Follow-up options -->
              <div v-if="message.followUpOptions && message.followUpOptions.length > 0" class="mt-3 space-y-2">
                <p class="text-sm text-gray-400 mb-2">You can ask me about:</p>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="option in message.followUpOptions"
                    :key="option"
                    @click="$emit('followup-selected', option)"
                    class="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-full transition-colors duration-200"
                  >
                    {{ option }}
                  </button>
                </div>
              </div>

              <!-- Diagnosis results -->
              <div v-if="message.diagnosis" class="mt-3 p-3 bg-gray-800 bg-opacity-50 rounded-lg border border-gray-600">
                <h4 class="font-semibold text-green-400 mb-2">Health Assessment Results</h4>
                
                <!-- Main diagnosis -->
                <div v-if="message.diagnosis.primary_diagnosis" class="mb-3">
                  <h5 class="text-sm font-medium text-gray-300 mb-1">Primary Assessment:</h5>
                  <p class="text-white">{{ message.diagnosis.primary_diagnosis }}</p>
                  <p v-if="message.diagnosis.confidence" class="text-xs text-gray-400 mt-1">
                    Confidence: {{ message.diagnosis.confidence }}%
                  </p>
                </div>

                <!-- Recommendations -->
                <div v-if="message.diagnosis.recommendations && message.diagnosis.recommendations.length > 0" class="mb-3">
                  <h5 class="text-sm font-medium text-gray-300 mb-2">Recommendations:</h5>
                  <ul class="text-sm text-gray-200 space-y-1">
                    <li v-for="rec in message.diagnosis.recommendations" :key="rec" class="flex items-start">
                      <span class="text-green-400 mr-2">•</span>
                      <span>{{ rec }}</span>
                    </li>
                  </ul>
                </div>

                <!-- Alternative diagnoses -->
                <div v-if="message.diagnosis && message.diagnosis.alternative_diagnoses && message.diagnosis.alternative_diagnoses.length > 0" class="mb-3">
                  <h5 class="text-sm font-medium text-gray-300 mb-2">Other Possible Conditions:</h5>
                  <div class="space-y-2">
                    <div v-for="(alt, index) in message.diagnosis.alternative_diagnoses" :key="index" class="flex justify-between items-center bg-gray-700 bg-opacity-50 rounded p-2">
                      <span class="text-gray-200">{{ alt.cause || alt.condition }}</span>
                      <span class="text-yellow-400 text-sm font-mono">{{ alt.value || alt.confidence }}%</span>
                    </div>
                  </div>
                </div>

                <!-- When to seek care -->
                <div v-if="message.diagnosis.urgency" class="mb-3">
                  <h5 class="text-sm font-medium text-gray-300 mb-1">When to Seek Care:</h5>
                  <p class="text-sm" :class="getUrgencyClass(message.diagnosis.urgency)">
                    {{ message.diagnosis.urgency }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Message footer with timestamp and replay button -->
            <div class="mt-2 flex items-center justify-between">
              <div class="text-xs text-gray-500">
                {{ formatTimestamp(message.timestamp) }}
              </div>
              
              <!-- Replay button - only show if sound is enabled -->
              <button
                v-if="soundEnabled"
                @click="$emit('replay-message', message.text)"
                class="flex items-center gap-1 text-xs text-gray-400 hover:text-blue-400 transition-colors duration-200 px-2 py-1 rounded hover:bg-gray-700/50"
                title="Replay this message"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                </svg>
                <span>Replay</span>
              </button>
            </div>
          </div>
          
          <!-- Speech bubble for user messages -->
          <div 
            v-else
            class="bg-gradient-to-br from-blue-600 to-purple-600 text-white rounded-3xl p-4 shadow-lg relative"
          >
            <!-- Speech bubble tail pointing left toward the AI doctor -->
            <div class="absolute -left-3 bottom-6 w-6 h-6">
              <div class="absolute w-0 h-0 border-t-8 border-b-8 border-r-8 border-t-transparent border-b-transparent border-r-blue-600"></div>
            </div>
            
            <!-- Message content -->
            <div class="message-content">
              <!-- Text content -->
              <div v-if="message.text" class="whitespace-pre-wrap" v-html="formatMessageText(message.text)"></div>
              
              <!-- Audio playback for voice messages -->
              <div v-if="message.audioUrl" class="mt-2">
                <audio :src="message.audioUrl" controls class="w-full"></audio>
              </div>
            </div>

            <!-- Message timestamp -->
            <div class="mt-2 text-xs text-blue-200 opacity-75">
              {{ formatTimestamp(message.timestamp) }}
              <span v-if="message.method" class="ml-2">
                ({{ message.method === 'voice' ? '🎤' : '⌨️' }})
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Enhanced Typing indicator -->
      <div v-if="isTyping" class="flex justify-start">
        <div class="bg-gradient-to-r from-gray-800 to-gray-700 rounded-lg p-4 max-w-[80%] shadow-lg border border-gray-600 animate-pulse-soft">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center animate-spin-slow shadow-lg">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="typing-indicator-enhanced">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
            <span class="text-sm text-blue-300 font-medium animate-pulse">AI Doctor is analyzing...</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  isTyping: {
    type: Boolean,
    default: false
  },
  autoScroll: {
    type: Boolean,
    default: true
  },
  soundEnabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['followup-selected', 'replay-message'])

const chatContainer = ref(null)

// Watch for new messages and scroll to bottom
watch(() => props.messages.length, () => {
  if (props.autoScroll) {
    nextTick(() => {
      scrollToBottom()
    })
  }
})

// Watch for typing indicator and scroll to bottom
watch(() => props.isTyping, (newVal) => {
  if (newVal && props.autoScroll) {
    nextTick(() => {
      scrollToBottom()
    })
  }
})

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const getMessageContainerClasses = (message) => {
  return {
    'mb-8': message.sender === 'assistant', // Extra spacing for thought bubbles
    'mb-4': message.sender === 'user', // Normal spacing for user messages
    'animate-fadeIn': true // Smooth appearance animation
  }
}

const getUrgencyClass = (urgency) => {
  const urgencyLower = urgency.toLowerCase()
  if (urgencyLower.includes('immediate') || urgencyLower.includes('urgent') || urgencyLower.includes('emergency')) {
    return 'text-red-400'
  } else if (urgencyLower.includes('soon') || urgencyLower.includes('within')) {
    return 'text-yellow-400'
  } else {
    return 'text-green-400'
  }
}

const formatMessageText = (text) => {
  // Convert URLs to clickable links
  const urlPattern = /(https?:\/\/[^\s]+)/g
  text = text.replace(urlPattern, '<a href="$1" target="_blank" class="text-blue-400 hover:text-blue-300 underline">$1</a>')
  
  // Convert **bold** to bold
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  
  // Convert *italic* to italic
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>')
  
  // Do NOT convert line breaks to <br> here — we rely on CSS (whitespace-pre-wrap) to preserve formatting
  // Collapse excessive blank lines (3 or more) into a single blank line to avoid huge vertical gaps
  text = text.replace(/(\n\s*){3,}/g, '\n\n')
  
  return text
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  
  if (diffMins < 1) {
    return 'Just now'
  } else if (diffMins < 60) {
    return `${diffMins}m ago`
  } else if (diffHours < 24) {
    return `${diffHours}h ago`
  } else {
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
}

// Expose scroll function for parent component
defineExpose({
  scrollToBottom
})
</script>

<style>
.auto-scroll {
  scroll-behavior: smooth;
}

.animate-fadeIn {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.message {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Thought bubble tail animations */
.group:hover .thought-tail {
  animation: bounce 0.3s ease-in-out;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.typing-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Enhanced Typing Indicator */
.typing-indicator-enhanced {
  display: flex;
  align-items: center;
  gap: 4px;
}

.typing-dot {
  height: 8px;
  width: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
  border-radius: 50%;
  display: inline-block;
  animation: typing-bounce 1.4s infinite ease-in-out;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
}

.typing-dot:nth-child(1) {
  animation-delay: 0s;
}

.typing-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing-bounce {
  0%, 60%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px) scale(1.2);
    opacity: 1;
  }
}

@keyframes spin-slow {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes pulse-soft {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.95;
  }
}

.animate-spin-slow {
  animation: spin-slow 3s linear infinite;
}

.animate-pulse-soft {
  animation: pulse-soft 2s ease-in-out infinite;
}

/* Legacy typing indicator (fallback) */
.typing-indicator span {
  height: 4px;
  width: 4px;
  background-color: #6b7280;
  border-radius: 50%;
  display: inline-block;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.32s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Hide scrollbar completely while keeping scroll functionality */
.overflow-y-auto {
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.overflow-y-auto::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

/* ====================================
   STATE-OF-THE-ART MESSAGE STYLING
   Premium glass morphism medical interface
   ==================================== */

/* Premium Light Mode - Assistant messages with sophisticated glass morphism */
.assistant-message {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: var(--text);
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.1), 0 4px 16px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(16px);
  position: relative;
  overflow: visible; /* Allow thought bubbles to extend outside */
  margin-bottom: 24px; /* Extra space for thought bubble tail */
}

/* Glass morphism overlay effect for light mode */
.assistant-message::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.8) 100%);
  opacity: 0.9;
  z-index: 1;
  border-radius: inherit;
}

/* Ensure content is above overlay */
.assistant-message > * {
  position: relative;
  z-index: 2;
}

/* Premium message subtitle with enhanced contrast - WHITE TEXT */
.message-subtitle {
  color: #ffffff !important;
  font-weight: 700 !important;
  font-size: 12px !important;
  letter-spacing: 0.5px !important;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6) !important;
}

/* Text shadow utility class */
.text-shadow {
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
}

/* ====================================
   THOUGHT BUBBLE STYLING
   Traditional comic-style thought bubble design
   ==================================== */

/* Thought bubble tail positioning and styling */
.thought-bubble-tail {
  position: absolute;
  bottom: -16px;
  left: 24px;
  display: flex;
  align-items: flex-end;
  gap: 4px;
  z-index: 10;
}

/* Individual bubble circles */
.bubble-circle {
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  border: 1px solid rgba(59, 130, 246, 0.2);
  animation: bubble-float 2s ease-in-out infinite;
}

.bubble-large {
  width: 16px;
  height: 16px;
  animation-delay: 0s;
}

.bubble-medium {
  width: 12px;
  height: 12px;
  animation-delay: 0.3s;
}

.bubble-small {
  width: 8px;
  height: 8px;
  animation-delay: 0.6s;
}

/* Floating animation for thought bubbles */
@keyframes bubble-float {
  0%, 100% {
    transform: translateY(0) scale(1);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-2px) scale(1.05);
    opacity: 1;
  }
}

/* Dark mode thought bubble styling */
[data-theme="dark"] .bubble-circle,
.dark .bubble-circle {
  background: linear-gradient(135deg, #22d3ee 0%, #0891b2 50%, #0e7490 100%) !important;
  border: 1px solid rgba(34, 211, 238, 0.4) !important;
  box-shadow: 0 2px 8px rgba(34, 211, 238, 0.4) !important;
}

/* ====================================
   ENHANCED MESSAGE BUBBLE STYLING
   ==================================== */

/* ====================================
   DARK MODE OVERRIDES
   Proper dark theme support with CSS variables
   ==================================== */

/* Dark Mode - Assistant messages with enhanced visibility */
[data-theme="dark"] .assistant-message {
  background: #1e293b !important;
  border: 2px solid #22d3ee !important;
  color: #ffffff !important;
  box-shadow: 0 8px 25px rgba(34, 211, 238, 0.15), 0 4px 10px rgba(0, 0, 0, 0.3) !important;
  backdrop-filter: none !important;
  overflow: visible !important; /* Allow thought bubbles to extend outside */
  margin-bottom: 24px !important; /* Extra space for thought bubble tail */
}

.dark .assistant-message {
  background: #1e293b !important;
  border: 2px solid #22d3ee !important;
  color: #ffffff !important;
  box-shadow: 0 8px 25px rgba(34, 211, 238, 0.15), 0 4px 10px rgba(0, 0, 0, 0.3) !important;
  backdrop-filter: none !important;
  overflow: visible !important; /* Allow thought bubbles to extend outside */
  margin-bottom: 24px !important; /* Extra space for thought bubble tail */
}

/* Disable glass morphism overlay in dark mode for better readability */
[data-theme="dark"] .assistant-message::before,
.dark .assistant-message::before {
  display: none !important;
}

[data-theme="dark"] .message-subtitle {
  color: #ffffff !important;
  font-weight: 800 !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8), 0 0 8px rgba(34, 211, 238, 0.5) !important;
  letter-spacing: 0.8px !important;
}

.dark .message-subtitle {
  color: #ffffff !important;
  font-weight: 800 !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8), 0 0 8px rgba(34, 211, 238, 0.5) !important;
  letter-spacing: 0.8px !important;
}

/* Dark mode timestamp styling */
[data-theme="dark"] .assistant-message .text-gray-500,
.dark .assistant-message .text-gray-500 {
  color: #ffffff !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6) !important;
}

[data-theme="dark"] .assistant-message .text-xs,
.dark .assistant-message .text-xs {
  color: #ffffff !important;
}

[data-theme="dark"] .bubble-tail {
  background: #22d3ee !important;
  border: 1px solid #0891b2 !important;
  box-shadow: 0 4px 8px rgba(34, 211, 238, 0.3) !important;
}

.dark .bubble-tail {
  background: #22d3ee !important;
  border: 1px solid #0891b2 !important;
  box-shadow: 0 4px 8px rgba(34, 211, 238, 0.3) !important;
}

/* Improve text contrast within assistant messages */
[data-theme="dark"] .assistant-message .message-content,
.dark .assistant-message .message-content {
  color: var(--text) !important;
}

[data-theme="dark"] .assistant-message p,
.dark .assistant-message p {
  color: var(--text) !important;
}

[data-theme="dark"] .assistant-message strong,
.dark .assistant-message strong {
  color: var(--primary) !important;
}

/* Fix all text elements in dark mode */
[data-theme="dark"] .assistant-message,
[data-theme="dark"] .assistant-message *,
.dark .assistant-message,
.dark .assistant-message * {
  color: var(--text) !important;
}

/* Keep strong elements with accent color */
[data-theme="dark"] .assistant-message strong,
.dark .assistant-message strong {
  color: #22d3ee !important;
  font-weight: 800 !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

/* ====================================
   WELCOME MESSAGE DARK MODE SUPPORT
   ====================================*/

/* Premium welcome card dark mode */
[data-theme="dark"] .premium-welcome-card,
.dark .premium-welcome-card {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--shadow-lg) !important;
  backdrop-filter: none !important;
}

/* Disable glass overlay in dark mode for welcome card */
[data-theme="dark"] .premium-welcome-card .glass-overlay,
.dark .premium-welcome-card .glass-overlay {
  display: none !important;
}

[data-theme="dark"] .premium-welcome-card h2,
.dark .premium-welcome-card h2 {
  color: var(--text) !important;
}

[data-theme="dark"] .premium-welcome-card p,
.dark .premium-welcome-card p {
  color: var(--text-muted) !important;
}

[data-theme="dark"] .premium-welcome-card .premium-subtitle,
.dark .premium-welcome-card .premium-subtitle {
  color: var(--text-muted) !important;
}

[data-theme="dark"] .assistant-message .message-content p,
[data-theme="dark"] .assistant-message .message-content div {
  color: #ffffff !important;
}

.dark .assistant-message .message-content p,
.dark .assistant-message .message-content div {
  color: #ffffff !important;
}

/* Light mode text styling for maximum contrast */
.assistant-message .message-content {
  color: #111827 !important;
  font-weight: 500 !important;
  line-height: 1.6 !important;
}

.assistant-message .message-content p,
.assistant-message .message-content div {
  color: #111827 !important;
  font-weight: 500 !important;
}

.assistant-message .message-content strong {
  color: #000000 !important;
  font-weight: 700 !important;
  text-shadow: none !important;
}

/* Dark mode text styling for maximum contrast */
[data-theme="dark"] .assistant-message .message-content,
.dark .assistant-message .message-content {
  color: #ffffff !important;
  font-weight: 500 !important;
  line-height: 1.6 !important;
}

[data-theme="dark"] .assistant-message .message-content p,
[data-theme="dark"] .assistant-message .message-content div,
.dark .assistant-message .message-content p,
.dark .assistant-message .message-content div {
  color: #ffffff !important;
  font-weight: 500 !important;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
}

[data-theme="dark"] .assistant-message .message-content strong,
.dark .assistant-message .message-content strong {
  color: #22d3ee !important;
  font-weight: 800 !important;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6) !important;
}
</style>
