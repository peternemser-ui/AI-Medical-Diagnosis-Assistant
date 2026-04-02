<template>
  <div class="flex-1 overflow-hidden flex flex-col relative">
    <!-- Conversation messages -->
    <div
      ref="chatContainer"
      role="log"
      aria-live="polite"
      class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4"
      :class="{ 'auto-scroll': autoScroll }"
    >
      <!-- Welcome screen if no messages -->
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
        <!-- Skeleton loading state for welcome screen -->
        <div v-if="welcomeLoading" class="w-full max-w-2xl space-y-6 animate-fadeIn">
          <div class="flex flex-col items-center">
            <SkeletonLoader type="chat-message" />
          </div>
          <SkeletonLoader type="card" count="3" />
        </div>

        <!-- Actual welcome content -->
        <template v-else>
          <!-- Logo -->
          <div class="w-14 h-14 rounded-panel bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 mb-5">
            <svg class="w-7 h-7 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <!-- Title -->
          <h2 class="text-display font-bold mb-2 text-[var(--text-primary)]">{{ t('chat.welcomeTitle') }}</h2>
          <p class="text-body mb-3 text-[var(--text-secondary)]">{{ t('chat.welcomeSubtitle') }}</p>

          <!-- Clinical intelligence note -->
          <div class="flex items-center gap-2 mb-8 px-3 py-2 rounded-pill text-detail"
            :class="isDark ? 'bg-purple-500/10 text-purple-300 border border-purple-500/15' : 'bg-purple-50 text-purple-600 border border-purple-200'">
            <span class="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse"></span>
            {{ t('hero.sevenAgents') }} — {{ t('hero.subtitle') }}
          </div>

          <!-- Example prompt cards -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full max-w-2xl">
            <button
              v-for="prompt in examplePrompts"
              :key="prompt"
              @click="$emit('followup-selected', prompt)"
              class="card-interactive rounded-card px-4 py-3.5 text-left text-body-sm group"
            >
              <span class="text-[var(--text-secondary)] group-hover:text-[var(--text-primary)] transition-colors">{{ prompt }}</span>
            </button>
          </div>
        </template>
      </div>

      <!-- Message list -->
      <div role="list" aria-label="Chat messages">
      <div
        v-for="(message, index) in messages"
        :key="message.id || index"
        role="listitem"
        :aria-label="message.sender === 'user' ? 'Your message' : 'Doctor message'"
        class="flex"
        :class="{ 'justify-end': message.sender === 'user', 'justify-start': message.sender === 'assistant' }"
      >
        <div
          class="max-w-[95%] sm:max-w-[80%] lg:max-w-[70%] relative"
          :class="getMessageContainerClasses(message)"
        >
          <!-- Assistant messages -->
          <div
            v-if="message.sender === 'assistant'"
            class="rounded-card rounded-tl-sm p-4 sm:p-5 border-l-3 surface-card"
            :class="[
              message.causes && message.causes.length ? 'border-l-blue-500' : 'border-l-[var(--clinical-border)]'
            ]"
            :style="specialistMode && message.specialistMessage && activeSpecialist ? { borderLeftColor: activeSpecialist.accentHex } : {}"
          >
            <!-- Message header -->
            <div class="flex items-center mb-3 gap-2">
              <!-- Specialist Avatar (during handoff) -->
              <div v-if="specialistMode && message.specialistMessage && activeSpecialist"
                class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-lg shadow-md border-2 ring-1 ring-offset-1 transition-all"
                :style="{ borderColor: activeSpecialist.accentHex, background: activeSpecialist.accentHex + '10', '--tw-ring-color': activeSpecialist.accentHex + '25' }"
                :class="isDark ? 'ring-offset-slate-800' : 'ring-offset-white'">
                {{ activeSpecialist.emoji }}
              </div>
              <!-- PA Character Avatar -->
              <div v-else-if="paMode && !message.causes" class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-lg shadow-sm border"
                :class="isDark ? 'bg-slate-700 border-slate-600' : 'bg-amber-50 border-amber-200'">
                {{ paCharacter === 'cat' ? '🐱' : paCharacter === 'dog' ? '🐶' : paCharacter === 'human' ? '👨‍⚕️' : '🐰' }}
              </div>
              <!-- Medical AI Avatar (for diagnosis results) -->
              <div v-else class="w-7 h-7 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center flex-shrink-0">
                <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
                </svg>
              </div>
              <span class="text-xs font-medium" :style="specialistMode && message.specialistMessage && activeSpecialist ? { color: activeSpecialist.accentHex } : {}" :class="!(specialistMode && message.specialistMessage) ? (isDark ? 'text-slate-400' : 'text-slate-500') : ''">
                {{ specialistMode && message.specialistMessage && activeSpecialist
                  ? activeSpecialist.name + ', ' + activeSpecialist.credentials
                  : paMode && !message.causes
                    ? paAvatarName + ', PA'
                    : t('chat.medicalAI') }}
              </span>
              <span v-if="message.multiAgent" class="text-tiny font-semibold tracking-wide px-2 py-0.5 rounded-full inline-flex items-center gap-1" style="background: rgba(139,92,246,0.1); color: #a78bfa; border: 1px solid rgba(139,92,246,0.15)">
                <span class="w-1 h-1 rounded-full bg-violet-400 animate-pulse" style="box-shadow: 0 0 4px rgba(139,92,246,0.5)"></span>
                {{ t('chat.multiAgent') }}
              </span>
            </div>

            <!-- Message content -->
            <div class="message-content">
              <!-- Structured diagnosis cards (when multi-agent data present) -->
              <div v-if="message.causes && message.causes.length > 0" class="space-y-3">
                <!-- Agent summary banner -->
                <div v-if="message.totalTime" class="flex items-center gap-2.5 text-detail sm:text-caption rounded-xl px-3 py-2 mb-3 border" style="background: linear-gradient(135deg, rgba(139,92,246,0.06), rgba(6,182,212,0.04)); border-color: rgba(139,92,246,0.1)">
                  <div class="w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0" style="background: rgba(139,92,246,0.15)">
                    <svg class="w-3 h-3" style="color: #a78bfa" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                  </div>
                  <span style="color: rgba(255,255,255,0.5)">{{ t('chat.analyzedBy') }} <strong class="font-semibold" style="color: rgba(255,255,255,0.7)">{{ (message.agentsUsed || []).length }} {{ t('chat.agentsWord') }}</strong> in <strong class="font-semibold tabular-nums" style="color: #a78bfa">{{ message.totalTime.toFixed(1) }}s</strong></span>
                </div>

                <!-- Red flags alert -->
                <div v-if="message.redFlags && message.redFlags.length > 0" class="bg-red-500/10 border border-red-500/30 rounded-lg p-2 sm:p-3 mb-3">
                  <div class="text-xs font-bold text-red-400 uppercase mb-1.5">{{ t('chat.warningSignsDetected') }}</div>
                  <ul class="space-y-1">
                    <li v-for="flag in message.redFlags" :key="flag" class="text-xs text-red-300 flex items-start gap-1.5">
                      <span class="text-red-500 font-bold flex-shrink-0">!</span>
                      <span>{{ typeof flag === 'object' ? (flag.title || flag.message || flag.issue || JSON.stringify(flag)) : flag }}</span>
                    </li>
                  </ul>
                </div>

                <!-- Diagnosis cards -->
                <DiagnosisCard
                  v-for="(cause, ci) in message.causes"
                  :key="ci"
                  :cause="cause"
                  :rank="ci + 1"
                  :red-flags="ci === 0 ? (message.redFlags || []) : []"
                  :recommended-tests="ci === 0 ? (message.recommendedTests || []) : []"
                />

                <!-- Patient Summary (from Empathy Agent) -->
                <div v-if="message.patientSummary" class="bg-blue-500/5 border border-blue-500/20 rounded-lg p-2 sm:p-3 mt-3">
                  <div class="text-detail font-semibold text-blue-400 uppercase mb-1.5">{{ t('chat.patientSummary') }}</div>
                  <p class="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">{{ message.patientSummary }}</p>
                </div>

                <!-- Action Checklist -->
                <div v-if="message.actionChecklist && message.actionChecklist.length > 0" class="bg-emerald-500/5 border border-emerald-500/20 rounded-lg p-3 mt-2">
                  <div class="text-detail font-semibold text-emerald-400 uppercase mb-1.5">{{ t('chat.actionChecklist') }}</div>
                  <ol class="space-y-1">
                    <li v-for="(item, i) in message.actionChecklist" :key="i" class="text-xs text-slate-300 flex gap-2">
                      <span class="text-emerald-400 font-bold flex-shrink-0">{{ i + 1 }}.</span>
                      <span>{{ typeof item === 'string' ? item : item.action || JSON.stringify(item) }}</span>
                    </li>
                  </ol>
                </div>

                <!-- Safety Review -->
                <div v-if="message.safetyWarnings && message.safetyWarnings.length > 0" class="bg-amber-500/5 border border-amber-500/20 rounded-lg p-3 mt-2">
                  <div class="flex items-center gap-2 mb-1.5">
                    <div class="text-detail font-semibold text-amber-400 uppercase">{{ t('chat.safetyReview') }}</div>
                    <span class="text-tiny px-1.5 py-0.5 rounded" :class="message.safetyStatus === 'PASS' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'">
                      {{ message.safetyStatus || 'REVIEWED' }}
                    </span>
                  </div>
                  <ul class="space-y-0.5">
                    <li v-for="w in message.safetyWarnings" :key="w" class="text-xs text-amber-200 flex items-start gap-1.5">
                      <span class="text-amber-500 flex-shrink-0">&#9888;</span>
                      <span>{{ w }}</span>
                    </li>
                  </ul>
                </div>

                <!-- Warning Signs -->
                <div v-if="message.warningSignsList && message.warningSignsList.length > 0" class="bg-red-500/5 border border-red-500/20 rounded-lg p-3 mt-2">
                  <div class="text-detail font-semibold text-red-400 uppercase mb-1.5">{{ t('chat.seekImmediateCare') }}</div>
                  <ul class="space-y-0.5">
                    <li v-for="s in message.warningSignsList" :key="s" class="text-xs text-red-300 flex items-start gap-1.5">
                      <span class="text-red-500 flex-shrink-0">&bull;</span>
                      <span>{{ typeof s === 'string' ? s : JSON.stringify(s) }}</span>
                    </li>
                  </ul>
                </div>

                <!-- Recommended Tests -->
                <div v-if="message.recommendedTests && message.recommendedTests.length > 0" class="rounded-lg p-3 mt-2 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-gray-50 border-gray-200'">
                  <div class="text-detail font-semibold uppercase mb-1.5" :class="isDark ? 'text-slate-400' : 'text-gray-500'">{{ t('chat.recommendedTests') }}</div>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="t in message.recommendedTests" :key="t" class="text-caption px-2 py-0.5 rounded" :class="isDark ? 'text-slate-300 bg-slate-700/50' : 'text-gray-700 bg-gray-200'">
                      {{ t }}
                    </span>
                  </div>
                </div>

                <!-- Additional questions -->
                <div v-if="message.additionalQuestions && message.additionalQuestions.length > 0" class="mt-3">
                  <div class="text-detail font-semibold uppercase mb-2" :class="isDark ? 'text-slate-400' : 'text-gray-500'">{{ t('chat.askFollowup') }}</div>
                  <div class="flex flex-wrap gap-1.5">
                    <button
                      v-for="q in message.additionalQuestions"
                      :key="q"
                      @click="$emit('followup-selected', q)"
                      class="text-caption bg-blue-500/10 hover:bg-blue-500/20 text-blue-300 px-2.5 py-1 rounded-lg border border-blue-500/20 transition-colors"
                    >
                      {{ q }}
                    </button>
                  </div>
                </div>

                <!-- Actions: Dashboard + PDF -->
                <div class="mt-3 pt-3 border-t flex flex-wrap gap-2" :class="isDark ? 'border-slate-700/40' : 'border-gray-200'">
                  <router-link
                    to="/dashboard"
                    class="flex items-center gap-2 text-xs font-medium bg-blue-600 hover:bg-blue-500 text-white px-4 py-2.5 rounded-lg transition-colors shadow-sm"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                    </svg>
                    {{ t('chat.viewDashboard') }}
                  </router-link>
                  <button
                    @click="generatePDF(message)"
                    class="flex items-center gap-2 text-xs px-3 py-2.5 rounded-lg border transition-colors"
                    :class="isDark ? 'bg-slate-800/50 border-slate-700/40 text-slate-300 hover:bg-slate-700' : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    {{ t('chat.exportPdf') }}
                  </button>
                </div>
              </div>

              <!-- Plain text content (non-diagnosis messages) -->
              <div v-else>
                <div v-if="message.text" class="whitespace-pre-wrap text-base leading-relaxed" v-html="formatMessageText(message.text)"></div>
              </div>

              <!-- Audio playback -->
              <div v-if="message.audioUrl" class="mt-2">
                <audio :src="message.audioUrl" controls class="w-full"></audio>
              </div>

              <!-- Follow-up options (legacy) -->
              <div v-if="message.followUpOptions && message.followUpOptions.length > 0" class="mt-3">
                <p class="text-xs mb-2" :class="isDark ? 'text-slate-500' : 'text-gray-500'">{{ t('chat.youCanAsk') }}</p>
                <div class="flex flex-wrap gap-1.5">
                  <button
                    v-for="option in message.followUpOptions"
                    :key="option"
                    @click="$emit('followup-selected', option)"
                    class="text-caption bg-blue-500/10 hover:bg-blue-500/20 text-blue-300 px-2.5 py-1 rounded-lg border border-blue-500/20 transition-colors"
                  >
                    {{ option }}
                  </button>
                </div>
              </div>

            </div>

            <!-- Message footer -->
            <div class="mt-2 flex items-center justify-between">
              <div class="text-xs mt-1" :class="isDark ? 'text-slate-600' : 'text-gray-400'">{{ formatTimestamp(message.timestamp) }}</div>
              <button
                v-if="soundEnabled"
                @click="$emit('replay-message', message.text)"
                class="flex items-center gap-1 text-detail transition-colors px-1.5 py-0.5 rounded"
                :class="isDark ? 'text-slate-500 hover:text-blue-400 hover:bg-slate-700/50' : 'text-gray-400 hover:text-blue-500 hover:bg-gray-100'"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                </svg>
                {{ t('chat.replay') }}
              </button>
            </div>
          </div>

          <!-- User messages -->
          <div
            v-else
            class="rounded-xl rounded-br-sm px-4 sm:px-5 py-3 sm:py-4 shadow-lg"
            :class="isDark ? 'bg-blue-600 text-white' : 'bg-blue-500 text-white'"
          >
            <div v-if="message.text" class="whitespace-pre-wrap text-base" v-html="formatMessageText(message.text)"></div>
            <img v-if="message.imageUrl" :src="message.imageUrl" class="mt-2 max-w-xs rounded-lg border border-blue-400/30" alt="Uploaded image" />
            <div v-if="message.audioUrl" class="mt-2">
              <audio :src="message.audioUrl" controls class="w-full"></audio>
            </div>
            <div class="mt-2 text-xs text-blue-200/60">{{ formatTimestamp(message.timestamp) }}</div>
          </div>
        </div>
      </div>

      </div>

      <!-- Typing indicator -->
      <div v-if="isTyping" class="flex justify-start">
        <div class="rounded-xl p-4 max-w-[80%] border" :class="isDark ? 'bg-slate-800/80 border-slate-700/50' : 'bg-white border-gray-200'">
          <div class="flex items-center space-x-2">
            <div v-if="paMode" class="w-6 h-6 rounded-full flex items-center justify-center text-sm"
              :class="isDark ? 'bg-slate-700' : 'bg-amber-50'">
              {{ paCharacter === 'cat' ? '🐱' : paCharacter === 'dog' ? '🐶' : paCharacter === 'human' ? '👨‍⚕️' : '🐰' }}
            </div>
            <div v-else class="w-5 h-5 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
              <svg class="w-2.5 h-2.5 text-white" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
              </svg>
            </div>
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span class="text-caption" :class="isDark ? 'text-slate-500' : 'text-gray-500'">{{ t('chat.agentsAnalyzing') }}</span>
          </div>
          <!-- Skeleton preview of upcoming response -->
          <div v-if="messages.length > 0" class="mt-3 pt-3 border-t" :class="isDark ? 'border-slate-700/40' : 'border-gray-200'">
            <SkeletonLoader type="card" />
          </div>
        </div>
      </div>

    <!-- (Avatar mode button removed — Dr. Buddy is shown in avatar mode automatically) -->
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, createApp, h, onMounted } from 'vue'
import DOMPurify from 'dompurify'
import DiagnosisCard from '@/components/DiagnosisCard.vue'
import DiagnosisReport from '@/components/DiagnosisReport.vue'
import SkeletonLoader from '@/components/SkeletonLoader.vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'

const { isDark } = useTheme()
const { t } = useI18n()

// Brief skeleton loading state for welcome screen
const welcomeLoading = ref(true)
onMounted(() => {
  setTimeout(() => {
    welcomeLoading.value = false
  }, 600)
})

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
  },
  paMode: {
    type: Boolean,
    default: false
  },
  paCharacter: {
    type: String,
    default: 'dog'
  },
  specialistMode: {
    type: Boolean,
    default: false
  },
  activeSpecialist: {
    type: Object,
    default: null
  }
})

const paAvatarName = computed(() => {
  const names = { bunny: 'Dr. Hopps', cat: 'Dr. Whiskers', dog: 'Dr. Buddy', human: 'Dr. AI' }
  return names[props.paCharacter] || 'Dr. Hopps'
})

const emit = defineEmits(['followup-selected', 'replay-message', 'toggle-avatar'])

const chatContainer = ref(null)

const examplePrompts = [
  'I have a persistent headache',
  'I\'ve been experiencing chest pain',
  'I have a skin rash that won\'t go away'
]

// Watch for new messages — always scroll to bottom so user sees latest
watch(() => props.messages.length, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

// Watch for typing indicator
watch(() => props.isTyping, (newVal) => {
  if (newVal) {
    nextTick(() => {
      scrollToBottom()
    })
  }
})

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTo({
      top: chatContainer.value.scrollHeight,
      behavior: 'smooth'
    })
  }
}

const getMessageContainerClasses = (message) => {
  return {
    'mb-1': true,
    'animate-fadeIn': true
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

  // Collapse excessive blank lines
  text = text.replace(/(\n\s*){3,}/g, '\n\n')

  // Sanitize to prevent XSS — only allow safe formatting tags
  return DOMPurify.sanitize(text, {
    ALLOWED_TAGS: ['a', 'strong', 'em', 'br', 'p', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'target', 'class', 'rel'],
  })
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  
  if (diffMins < 1) {
    return t('chat.justNow')
  } else if (diffMins < 60) {
    return t('chat.minutesAgo').replace('{n}', diffMins)
  } else if (diffHours < 24) {
    return t('chat.hoursAgo').replace('{n}', diffHours)
  } else {
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
}

// ── PDF Report Generation ──
async function generatePDF(message) {
  const html2pdf = (await import('html2pdf.js')).default

  // Create a temporary container
  const container = document.createElement('div')
  container.style.position = 'absolute'
  container.style.left = '-9999px'
  container.style.top = '0'
  document.body.appendChild(container)

  // Mount DiagnosisReport into the container
  const app = createApp({
    render() {
      return h(DiagnosisReport, {
        diagnosisData: message,
        patientInfo: {
          age: message.agentDetails?.diagnosis?.patient_age || '',
          gender: message.agentDetails?.diagnosis?.patient_gender || '',
          symptoms: message.text ? message.text.substring(0, 200) : ''
        }
      })
    }
  })
  app.mount(container)

  // Wait for render
  await nextTick()
  await new Promise(r => setTimeout(r, 200))

  const opt = {
    margin: 10,
    filename: 'medical-report.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }

  try {
    await html2pdf().set(opt).from(container).save()
  } finally {
    app.unmount()
    document.body.removeChild(container)
  }
}

// Expose scroll function for parent component
defineExpose({
  scrollToBottom
})
</script>

<style scoped>
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

/* Custom scrollbar */
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
</style>
