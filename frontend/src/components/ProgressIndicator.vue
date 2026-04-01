<template>
  <div v-if="visible" class="relative overflow-hidden" :style="containerStyle">
    <!-- Ambient glow -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
      <div class="absolute w-[200px] h-[200px] -top-[80px] -right-[60px] rounded-full blur-[80px] opacity-[0.04]"
        style="background: radial-gradient(circle, #3b82f6, transparent)"></div>
      <div class="absolute w-[150px] h-[150px] -bottom-[50px] -left-[30px] rounded-full blur-[60px] opacity-[0.03]"
        style="background: radial-gradient(circle, #22c55e, transparent)"></div>
    </div>

    <div class="relative z-10 max-w-5xl mx-auto px-4 py-2.5" aria-label="Interview progress">
      <!-- Steps + percentage -->
      <div class="flex items-center gap-4">
        <!-- Steps as pills (hidden on mobile) -->
        <div class="flex-1 hidden sm:flex items-center gap-1 overflow-x-auto no-scrollbar" role="navigation" aria-label="Interview steps">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="flex items-center gap-1 flex-shrink-0"
          >
            <!-- Step pill -->
            <div
              class="step-pill flex items-center gap-1.5 px-2.5 py-1.5 rounded-full text-caption font-medium transition-all duration-300 whitespace-nowrap border"
              :style="getStepPillStyle(index)"
            >
              <!-- Check for completed -->
              <svg v-if="currentStep > index" class="w-3 h-3 text-emerald-400 drop-shadow-[0_0_3px_rgba(34,197,94,0.4)]" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <!-- Pulse for current -->
              <div v-else-if="currentStep === index" class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse" style="box-shadow: 0 0 6px rgba(59,130,246,0.5)"></div>
              <span class="hidden sm:inline">{{ step }}</span>
              <span class="sm:hidden">{{ index + 1 }}</span>
            </div>
            <!-- Connector -->
            <div v-if="index < steps.length - 1" class="flex-shrink-0 mx-0.5 relative">
              <svg class="w-3 h-3 transition-colors duration-300" fill="currentColor" viewBox="0 0 20 20"
                :style="{ color: currentStep > index ? '#22c55e' : 'rgba(255,255,255,0.1)' }">
                <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- Percentage badge -->
        <div class="flex-shrink-0 text-caption font-bold px-3 py-1.5 rounded-full border tabular-nums"
          :style="progress >= 80
            ? { background: 'rgba(34,197,94,0.1)', color: '#22c55e', borderColor: 'rgba(34,197,94,0.2)', boxShadow: '0 0 10px rgba(34,197,94,0.1)' }
            : { background: 'rgba(255,255,255,0.04)', color: 'rgba(255,255,255,0.5)', borderColor: 'rgba(255,255,255,0.08)' }
          ">
          {{ Math.round(progress) }}%
        </div>
      </div>

      <!-- Progress bar with glow -->
      <div class="mt-2.5 relative">
        <div class="h-1 rounded-full overflow-hidden bg-white/[0.04]">
          <div
            role="progressbar"
            :aria-valuenow="Math.round(progress)"
            aria-valuemin="0"
            aria-valuemax="100"
            :aria-label="'Interview progress: ' + Math.round(progress) + '%'"
            class="h-full rounded-full transition-all duration-700 ease-out"
            :style="progressBarStyle"
          ></div>
        </div>
        <!-- Glow trail -->
        <div class="absolute top-0 left-0 h-1 rounded-full blur-sm transition-all duration-700"
          :style="{ width: progress + '%', background: progress >= 80 ? '#22c55e30' : '#3b82f630' }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  progress: { type: Number, default: 0 },
  title: { type: String, default: 'Processing...' },
  message: { type: String, default: '' },
  steps: { type: Array, default: () => [] },
  currentStep: { type: Number, default: 0 },
})

const containerStyle = {
  background: 'linear-gradient(145deg, #0a0f1c 0%, #070b16 60%, #05070d 100%)',
  borderBottom: '1px solid rgba(255,255,255,0.06)',
}

const progressBarStyle = computed(() => ({
  width: props.progress + '%',
  background: props.progress >= 80
    ? 'linear-gradient(90deg, #22c55e, #10b981)'
    : 'linear-gradient(90deg, #3b82f6, #8b5cf6)',
}))

function getStepPillStyle(index) {
  if (props.currentStep > index) {
    return { background: 'rgba(34,197,94,0.08)', color: '#22c55e', borderColor: 'rgba(34,197,94,0.15)' }
  }
  if (props.currentStep === index) {
    return { background: 'rgba(59,130,246,0.1)', color: '#60a5fa', borderColor: 'rgba(59,130,246,0.25)', boxShadow: '0 0 8px rgba(59,130,246,0.1)' }
  }
  return { background: 'rgba(255,255,255,0.02)', color: 'rgba(255,255,255,0.3)', borderColor: 'rgba(255,255,255,0.06)' }
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
