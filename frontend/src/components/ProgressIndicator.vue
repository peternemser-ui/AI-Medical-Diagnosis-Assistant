<template>
  <div v-if="visible" class="border-b backdrop-blur-xl" :class="isDark ? 'bg-slate-900/90 border-slate-800/80' : 'bg-white/90 border-gray-200'">
    <div class="max-w-5xl mx-auto px-4 py-2.5">
      <!-- Compact single row: title + steps + percentage -->
      <div class="flex items-center gap-4">
        <!-- Steps as pills -->
        <div class="flex-1 flex items-center gap-1 overflow-x-auto no-scrollbar">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="flex items-center gap-1 flex-shrink-0"
          >
            <!-- Step pill -->
            <div
              class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-full text-xs font-medium transition-all duration-300 whitespace-nowrap"
              :class="getStepPillClass(index)"
            >
              <!-- Check for completed -->
              <svg v-if="currentStep > index" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
              <!-- Pulse for current -->
              <div v-else-if="currentStep === index" class="w-1.5 h-1.5 rounded-full bg-current animate-pulse"></div>
              <span class="hidden sm:inline">{{ step }}</span>
              <span class="sm:hidden">{{ index + 1 }}</span>
            </div>
            <!-- Connector -->
            <svg v-if="index < steps.length - 1" class="w-3 h-3 flex-shrink-0" :class="currentStep > index ? (isDark ? 'text-emerald-500' : 'text-emerald-600') : (isDark ? 'text-slate-700' : 'text-gray-400')" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>

        <!-- Percentage badge -->
        <div class="flex-shrink-0 text-xs font-bold px-2.5 py-1 rounded-full"
          :class="progress >= 80 ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700') : (isDark ? 'bg-slate-800 text-slate-400' : 'bg-gray-200 text-gray-600')"
        >
          {{ Math.round(progress) }}%
        </div>
      </div>

      <!-- Thin progress bar -->
      <div class="mt-2 h-1 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-gray-200'">
        <div
          class="h-full rounded-full transition-all duration-700 ease-out"
          :class="progress >= 80 ? 'bg-emerald-500' : 'bg-blue-500'"
          :style="{ width: progress + '%' }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  visible: { type: Boolean, default: false },
  progress: { type: Number, default: 0 },
  title: { type: String, default: 'Processing...' },
  message: { type: String, default: '' },
  steps: { type: Array, default: () => [] },
  currentStep: { type: Number, default: 0 },
})

function getStepPillClass(index) {
  if (props.currentStep > index) {
    return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700 font-semibold'
  }
  if (props.currentStep === index) {
    return isDark.value ? 'bg-blue-500/15 text-blue-400 ring-1 ring-blue-500/30' : 'bg-blue-100 text-blue-700 ring-1 ring-blue-300 font-semibold'
  }
  return isDark.value ? 'bg-slate-800/50 text-slate-500' : 'bg-gray-100 text-gray-500'
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>
