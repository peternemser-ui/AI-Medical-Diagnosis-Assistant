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
                class="w-16 h-16 rounded-2xl flex items-center justify-center text-3xl transition-all duration-300"
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

            <!-- Step 1: Welcome + 7-agent system -->
            <div v-if="currentStep === 0" class="space-y-4">
              <p class="text-center leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                Welcome to your personal AI medical team. Your symptoms are analyzed by
                <span class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">7 specialized AI agents</span>
                working together for a thorough, evidence-based assessment.
              </p>
              <div class="grid grid-cols-4 sm:grid-cols-7 gap-2 mt-4">
                <div
                  v-for="agent in agents"
                  :key="agent.name"
                  class="flex flex-col items-center gap-1.5 p-2 rounded-xl transition-colors"
                  :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'"
                >
                  <span class="text-xl">{{ agent.icon }}</span>
                  <span class="text-detail font-medium leading-tight text-center" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ agent.name }}</span>
                </div>
              </div>
              <p class="text-xs text-center mt-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                Triage, Diagnostician, and Research run in parallel for faster results.
              </p>
            </div>

            <!-- Step 2: API Key Setup -->
            <div v-if="currentStep === 1" class="space-y-4">
              <p class="text-center leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                To power the AI agents, you need an API key from Anthropic (Claude) or OpenAI. Your key stays in your browser and is never sent to our servers.
              </p>
              <div class="flex flex-col gap-3">
                <div
                  v-for="(item, i) in apiKeyPoints"
                  :key="i"
                  class="flex items-center gap-2.5 p-2.5 rounded-lg"
                  :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'"
                >
                  <svg class="w-4 h-4 flex-shrink-0" :class="isDark ? 'text-blue-400' : 'text-blue-600'" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                  </svg>
                  <span class="text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ item }}</span>
                </div>
              </div>
              <div class="flex justify-center mt-4">
                <button
                  @click="navigateTo('/setup')"
                  class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium bg-blue-600 hover:bg-blue-500 text-white transition-colors shadow-lg shadow-blue-500/25"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z"/>
                  </svg>
                  Configure API Key
                </button>
              </div>
              <p v-if="hasApiKey" class="text-xs text-center text-emerald-500 font-medium mt-1">
                API key already configured
              </p>
            </div>

            <!-- Step 3: Profile Setup -->
            <div v-if="currentStep === 2" class="space-y-4">
              <p class="text-center leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                Setting up your profile helps the AI agents provide more personalized and accurate assessments based on your age, gender, and medical history.
              </p>
              <div class="flex flex-col gap-3">
                <div
                  v-for="(item, i) in profilePoints"
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
              <div class="flex justify-center mt-4">
                <button
                  @click="navigateTo('/profile')"
                  class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium bg-purple-600 hover:bg-purple-500 text-white transition-colors shadow-lg shadow-purple-500/25"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"/>
                  </svg>
                  Complete Profile
                </button>
              </div>
              <p v-if="hasProfile" class="text-xs text-center text-emerald-500 font-medium mt-1">
                Profile already set up
              </p>
            </div>

            <!-- Step 4: Start Consultation -->
            <div v-if="currentStep === 3" class="space-y-4">
              <div class="flex justify-center mb-2">
                <div
                  class="w-20 h-20 rounded-full flex items-center justify-center"
                  :class="isDark ? 'bg-emerald-500/10' : 'bg-emerald-50'"
                >
                  <svg class="w-10 h-10" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <p class="text-center leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                You're all set! Start your first consultation and let the 7 AI agents analyze your symptoms with evidence-based medical reasoning.
              </p>
              <div class="flex flex-col gap-2">
                <div
                  v-for="(item, i) in readyPoints"
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

            <!-- Next / Begin Consultation -->
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
                class="text-sm font-semibold px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-500 hover:to-teal-500 transition-all shadow-lg shadow-emerald-500/25 whitespace-nowrap"
              >
                Begin Consultation
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])

const router = useRouter()
const { isDark } = useTheme()
const currentStep = ref(0)

const hasApiKey = computed(() => {
  return !!(localStorage.getItem('api_key_configured') || localStorage.getItem('anthropic_api_key') || localStorage.getItem('openai_api_key'))
})

const hasProfile = computed(() => {
  return !!(localStorage.getItem('user_profile') || localStorage.getItem('patient_age'))
})

const agents = [
  { name: 'Triage', icon: '\u{1F6A6}' },
  { name: 'Diagnostician', icon: '\u{1F52C}' },
  { name: 'Research', icon: '\u{1F4DA}' },
  { name: 'Specialist', icon: '\u{1F3E5}' },
  { name: 'Treatment', icon: '\u{1F48A}' },
  { name: 'Safety', icon: '\u{1F6E1}\uFE0F' },
  { name: 'Empathy', icon: '\u{1F499}' },
]

const steps = [
  { title: 'Welcome to Your AI Medical Team', icon: '\u{1F44B}' },
  { title: 'Set Up Your API Key', icon: '\u{1F511}' },
  { title: 'Complete Your Profile', icon: '\u{1F464}' },
  { title: 'Ready to Begin', icon: '\u{1F680}' },
]

const apiKeyPoints = [
  'Get a free API key from Anthropic (Claude) or OpenAI',
  'Your key is stored locally in your browser only',
  'Powers all 7 AI agents for accurate diagnosis',
]

const profilePoints = [
  { icon: '\u{1F9EC}', title: 'Age & Gender', desc: 'Helps narrow down age-specific and gender-specific conditions.' },
  { icon: '\u{1FA7A}', title: 'Medical History', desc: 'Existing conditions and medications inform safer recommendations.' },
  { icon: '\u{26A0}\uFE0F', title: 'Allergies', desc: 'The Safety Agent uses this to flag contraindications.' },
]

const readyPoints = [
  'Describe your symptoms in natural language',
  'Answer follow-up questions from the AI agents',
  'Receive a comprehensive diagnosis with confidence scores',
  'Export your report as PDF to share with your doctor',
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
  router.push('/consult')
}

function navigateTo(path) {
  localStorage.setItem('onboarding_complete', 'true')
  emit('close')
  router.push(path)
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
