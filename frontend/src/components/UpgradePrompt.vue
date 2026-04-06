<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="visible" class="fixed inset-0 z-[200] flex items-center justify-center p-4" @click.self="close">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm"></div>

        <!-- Modal -->
        <div class="relative w-full max-w-lg rounded-2xl border shadow-2xl overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-slate-200'">
          <!-- Header with gradient -->
          <div class="px-6 pt-6 pb-4 text-center"
            :class="isDark ? 'bg-gradient-to-b from-blue-500/10 to-transparent' : 'bg-gradient-to-b from-blue-50 to-transparent'">
            <!-- Close button -->
            <button @click="close" class="absolute top-3 right-3 p-1.5 rounded-lg transition-colors"
              :class="isDark ? 'text-slate-500 hover:text-white hover:bg-slate-800' : 'text-slate-400 hover:text-slate-900 hover:bg-slate-100'">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>

            <!-- Warning icon -->
            <div class="w-14 h-14 mx-auto rounded-full flex items-center justify-center mb-4"
              :class="isDark ? 'bg-amber-500/10' : 'bg-amber-50'">
              <svg class="w-7 h-7 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>

            <h2 class="text-xl font-bold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">
              {{ title }}
            </h2>
            <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
              {{ subtitle }}
            </p>
          </div>

          <!-- Usage bar -->
          <div v-if="used !== null && limit !== null" class="px-6 py-4">
            <div class="flex justify-between text-xs font-medium mb-2"
              :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              <span>{{ used }} of {{ limit }} diagnoses used</span>
              <span class="text-amber-500 font-semibold">{{ Math.round((used / limit) * 100) }}%</span>
            </div>
            <div class="h-2.5 rounded-full overflow-hidden"
              :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
              <div class="h-full rounded-full transition-all duration-500 bg-gradient-to-r from-amber-500 to-red-500"
                :style="{ width: `${Math.min(100, (used / limit) * 100)}%` }"></div>
            </div>
          </div>

          <!-- Tier comparison -->
          <div class="px-6 py-4">
            <div class="text-xs font-semibold uppercase tracking-wider mb-3"
              :class="isDark ? 'text-slate-500' : 'text-slate-400'">What you're missing</div>
            <div class="grid grid-cols-2 gap-2">
              <div v-for="feature in missingFeatures" :key="feature"
                class="flex items-center gap-2 text-sm px-3 py-2 rounded-lg"
                :class="isDark ? 'bg-slate-800/60' : 'bg-slate-50'">
                <svg class="w-4 h-4 text-blue-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
                <span :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ feature }}</span>
              </div>
            </div>
          </div>

          <!-- CTAs -->
          <div class="px-6 pb-6 space-y-3">
            <button @click="goToPricing"
              class="w-full py-3 rounded-xl text-sm font-semibold bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:from-blue-600 hover:to-purple-600 shadow-lg shadow-blue-500/20 transition-all">
              Upgrade to {{ suggestedTierName }}
              <span v-if="suggestedPrice" class="opacity-80 ml-1">- ${{ suggestedPrice }}/mo</span>
            </button>

            <button @click="continueWithOllama"
              class="w-full py-2.5 rounded-xl text-sm font-medium transition-colors border"
              :class="isDark
                ? 'border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800'
                : 'border-slate-200 text-slate-500 hover:text-slate-800 hover:bg-slate-50'">
              Continue with Ollama (local, free)
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'

const router = useRouter()
const { isDark } = useTheme()

const props = defineProps({
  visible: { type: Boolean, default: false },
  used: { type: Number, default: null },
  limit: { type: Number, default: null },
  currentTier: { type: String, default: 'free' },
  blockedFeature: { type: String, default: null },
  suggestedTierName: { type: String, default: 'Plus' },
  suggestedPrice: { type: Number, default: 9.99 },
})

const emit = defineEmits(['close', 'continue-ollama'])

const title = computed(() => {
  if (props.used !== null && props.limit !== null) {
    return `You've used ${props.used}/${props.limit} free diagnoses`
  }
  if (props.blockedFeature) {
    return `${props.blockedFeature} requires an upgrade`
  }
  return 'Upgrade your plan'
})

const subtitle = computed(() => {
  if (props.used !== null && props.limit !== null && props.used >= props.limit) {
    return 'Your monthly limit resets on the 1st. Upgrade now for more diagnoses and premium AI models.'
  }
  return 'Unlock premium features and unlimited AI-powered diagnostics.'
})

const featureLabels = {
  pdf_export: 'PDF Export',
  photo_analysis: 'Photo Analysis',
  history: 'Diagnosis History',
  specialist_routing: 'Specialist Routing',
  priority_support: 'Priority Support',
  api_access: 'API Access',
  family_profiles: 'Family Profiles',
  pediatric_mode: 'Pediatric Mode',
}

const missingFeatures = computed(() => {
  // Features the user doesn't have but would get with an upgrade
  const freeFeatures = ['basic_report', 'body_map']
  const plusFeatures = ['pdf_export', 'photo_analysis', 'history', 'specialist_routing']

  if (props.currentTier === 'free') {
    return plusFeatures.map(f => featureLabels[f] || f)
  }
  if (props.currentTier === 'plus') {
    return ['priority_support', 'api_access'].map(f => featureLabels[f] || f)
  }
  return ['family_profiles', 'pediatric_mode'].map(f => featureLabels[f] || f)
})

function close() {
  emit('close')
}

function goToPricing() {
  emit('close')
  router.push('/pricing')
}

function continueWithOllama() {
  emit('continue-ollama')
  emit('close')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
