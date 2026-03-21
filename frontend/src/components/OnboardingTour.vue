<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="visible" class="fixed inset-0 z-[9999] flex items-center justify-center p-4" @click.self="handleSkip">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

        <!-- Modal -->
        <div
          class="relative w-full max-w-lg rounded-2xl border shadow-2xl overflow-hidden transition-colors duration-300"
          :class="isDark
            ? 'bg-slate-900/80 border-slate-700/50 backdrop-blur-xl'
            : 'bg-white/80 border-slate-200/60 backdrop-blur-xl'"
        >
          <!-- Progress bar -->
          <div class="h-1 w-full" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
            <div
              class="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500 ease-out"
              :style="{ width: `${((currentStep + 1) / steps.length) * 100}%` }"
            ></div>
          </div>

          <!-- Content area -->
          <div class="p-8">
            <!-- Step icon -->
            <div class="flex justify-center mb-6">
              <div
                class="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl"
                :class="isDark ? 'bg-blue-500/15' : 'bg-blue-50'"
              >
                {{ steps[currentStep].icon }}
              </div>
            </div>

            <!-- Title -->
            <h2 class="text-2xl font-bold text-center mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">
              {{ steps[currentStep].title }}
            </h2>

            <!-- Subtitle -->
            <p class="text-sm text-center mb-6" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              Step {{ currentStep + 1 }} of {{ steps.length }}
            </p>

            <!-- Step 1: Agent pipeline -->
            <div v-if="currentStep === 0" class="space-y-4">
              <p class="text-center leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                Your symptoms are analyzed by <span class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">7 specialized AI agents</span> working together for a thorough assessment.
              </p>
              <div class="grid grid-cols-4 sm:grid-cols-7 gap-2 mt-4">
                <div
                  v-for="agent in agents"
                  :key="agent.name"
                  class="flex flex-col items-center gap-1.5 p-2 rounded-xl transition-colors"
                  :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'"
                >
                  <span class="text-xl">{{ agent.icon }}</span>
                  <span class="text-[10px] font-medium leading-tight text-center" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ agent.name }}</span>
                </div>
              </div>
            </div>

            <!-- Step 2: How it works -->
            <div v-if="currentStep === 1" class="space-y-4">
              <div class="flex flex-col gap-3">
                <div
                  v-for="(item, i) in howItWorks"
                  :key="i"
                  class="flex items-start gap-3 p-3 rounded-xl transition-colors"
                  :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'"
                >
                  <div
                    class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0"
                    :class="isDark ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-100 text-blue-600'"
                  >
                    {{ i + 1 }}
                  </div>
                  <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ item }}</p>
                </div>
              </div>
            </div>

            <!-- Step 3: Reports -->
            <div v-if="currentStep === 2" class="space-y-4">
              <div class="flex flex-col gap-3">
                <div
                  v-for="(item, i) in reportFeatures"
                  :key="i"
                  class="flex items-start gap-3 p-3 rounded-xl transition-colors"
                  :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'"
                >
                  <span class="text-lg flex-shrink-0">{{ item.icon }}</span>
                  <div>
                    <p class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ item.title }}</p>
                    <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ item.desc }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Step 4: Privacy -->
            <div v-if="currentStep === 3" class="space-y-4">
              <div class="flex justify-center mb-2">
                <div
                  class="w-20 h-20 rounded-full flex items-center justify-center"
                  :class="isDark ? 'bg-emerald-500/10' : 'bg-emerald-50'"
                >
                  <svg class="w-10 h-10" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" />
                  </svg>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <div
                  v-for="(item, i) in privacyPoints"
                  :key="i"
                  class="flex items-center gap-2.5 p-2.5 rounded-lg"
                  :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'"
                >
                  <svg class="w-4 h-4 flex-shrink-0" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                  </svg>
                  <span class="text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ item }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer with buttons and dots -->
          <div
            class="px-8 pb-6 flex items-center justify-between"
          >
            <!-- Back / Skip -->
            <div class="w-24">
              <button
                v-if="currentStep > 0"
                @click="prevStep"
                class="text-sm font-medium px-3 py-1.5 rounded-lg transition-colors"
                :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'"
              >
                Back
              </button>
              <button
                v-else
                @click="handleSkip"
                class="text-sm font-medium px-3 py-1.5 rounded-lg transition-colors"
                :class="isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-400 hover:text-slate-600'"
              >
                Skip
              </button>
            </div>

            <!-- Dot indicators -->
            <div class="flex items-center gap-2">
              <button
                v-for="(_, i) in steps"
                :key="i"
                @click="currentStep = i"
                class="w-2 h-2 rounded-full transition-all duration-300"
                :class="i === currentStep
                  ? 'bg-blue-500 w-6'
                  : (isDark ? 'bg-slate-600 hover:bg-slate-500' : 'bg-slate-300 hover:bg-slate-400')"
              ></button>
            </div>

            <!-- Next / Get Started -->
            <div class="w-24 flex justify-end">
              <button
                v-if="currentStep < steps.length - 1"
                @click="nextStep"
                class="text-sm font-semibold px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-500 transition-colors shadow-lg shadow-blue-500/25"
              >
                Next
              </button>
              <button
                v-else
                @click="handleComplete"
                class="text-sm font-semibold px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-500 hover:to-purple-500 transition-all shadow-lg shadow-blue-500/25"
              >
                Get Started
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const { isDark } = useTheme()
const currentStep = ref(0)

const agents = [
  { name: 'Triage', icon: '🚦' },
  { name: 'Diagnostician', icon: '🔬' },
  { name: 'Research', icon: '📚' },
  { name: 'Specialist', icon: '🏥' },
  { name: 'Treatment', icon: '💊' },
  { name: 'Safety', icon: '🛡️' },
  { name: 'Empathy', icon: '💙' },
]

const steps = [
  { title: 'Welcome to Your AI Medical Team', icon: '👋' },
  { title: 'How It Works', icon: '⚡' },
  { title: 'Your Reports', icon: '📋' },
  { title: 'Privacy First', icon: '🔒' },
]

const howItWorks = [
  'Answer about 15 clinical questions so we can understand your symptoms in detail.',
  'Our 7 AI agents analyze your responses in parallel using evidence-based reasoning.',
  'Receive a comprehensive diagnosis with confidence scores, recommended tests, and next steps.',
]

const reportFeatures = [
  { icon: '💾', title: 'Saved Locally', desc: 'All reports are stored in your browser. Access them anytime from the Reports page.' },
  { icon: '📄', title: 'Export as PDF', desc: 'Download professional medical reports to share with your healthcare provider.' },
  { icon: '🗺️', title: 'Find a Specialist', desc: 'Use the built-in specialist finder to locate relevant doctors near you.' },
]

const privacyPoints = [
  'All data stays on your device — nothing is stored on our servers.',
  'Your API key is saved in your browser only, never transmitted elsewhere.',
  'Conversation history is stored locally and you can delete it anytime.',
  'You are in full control of your medical information.',
]

function nextStep() {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

function prevStep() {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

function handleSkip() {
  localStorage.setItem('onboarding_complete', 'true')
  emit('close')
}

function handleComplete() {
  localStorage.setItem('onboarding_complete', 'true')
  emit('close')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
