<template>
  <Transition name="handoff">
    <div v-if="visible" class="flex justify-center my-6 px-4">
      <div class="relative max-w-sm w-full rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-800/80 border-slate-700/50' : 'bg-white/90 border-slate-200'"
        :style="{ boxShadow: `0 8px 32px -4px ${specialist.accentHex}15, 0 4px 12px -2px rgba(0,0,0,0.08)` }">

        <!-- Accent top bar -->
        <div class="h-1 w-full bg-gradient-to-r" :class="specialist.bgClass"></div>

        <div class="p-5">
          <!-- Header label -->
          <div class="text-center mb-4">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-pill text-detail font-bold uppercase tracking-wider"
              :style="{ background: specialist.accentHex + '12', color: specialist.accentHex }">
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
              </svg>
              Specialist Referral
            </span>
          </div>

          <!-- PA → Specialist visual -->
          <div class="flex items-center justify-center gap-3 sm:gap-5">
            <!-- PA avatar -->
            <div class="flex flex-col items-center gap-1.5 transition-all duration-700 handoff-pa">
              <div class="w-14 h-14 rounded-full border-2 flex items-center justify-center text-2xl shadow-md transition-all"
                :class="isDark ? 'bg-slate-700 border-slate-500' : 'bg-amber-50 border-amber-200'">
                {{ paEmoji }}
              </div>
              <span class="text-caption font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ paName }}</span>
              <span class="text-micro uppercase tracking-wider" :class="isDark ? 'text-slate-600' : 'text-slate-400'">PA</span>
            </div>

            <!-- Animated connector -->
            <div class="flex items-center gap-1 handoff-arrow">
              <div class="w-6 sm:w-10 h-0.5 rounded-full" :style="{ background: specialist.accentHex + '60' }"></div>
              <div class="w-6 h-6 rounded-full flex items-center justify-center"
                :style="{ background: specialist.accentHex + '15' }">
                <svg class="w-3.5 h-3.5" :style="{ color: specialist.accentHex }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                </svg>
              </div>
              <div class="w-6 sm:w-10 h-0.5 rounded-full" :style="{ background: specialist.accentHex + '60' }"></div>
            </div>

            <!-- Specialist avatar -->
            <div class="flex flex-col items-center gap-1.5 transition-all duration-700 handoff-specialist">
              <div class="w-14 h-14 rounded-full border-2 flex items-center justify-center text-2xl shadow-lg ring-2 ring-offset-2 transition-all"
                :class="isDark ? 'ring-offset-slate-800' : 'ring-offset-white'"
                :style="{ borderColor: specialist.accentHex, background: specialist.accentHex + '10', '--tw-ring-color': specialist.accentHex + '30' }">
                {{ specialist.emoji }}
              </div>
              <span class="text-caption font-semibold" :style="{ color: specialist.accentHex }">{{ specialist.name.split(',')[0] }}</span>
              <span class="text-micro uppercase tracking-wider" :style="{ color: specialist.accentHex + 'cc' }">{{ formattedSpecialty }}</span>
            </div>
          </div>

          <!-- Referral reason -->
          <div v-if="reason" class="mt-4 text-center">
            <p class="text-detail leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              "{{ reason }}"
            </p>
          </div>

          <!-- Credentials bar -->
          <div class="mt-4 pt-3 border-t flex items-center justify-center gap-2"
            :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <div class="w-2 h-2 rounded-full animate-pulse" :style="{ background: specialist.accentHex }"></div>
            <span class="text-detail font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              {{ specialist.title }} · {{ specialist.credentials }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme'
import { PA_EMOJIS } from '@/data/specialistDoctors.js'

const { isDark } = useTheme()

const props = defineProps({
  paName: { type: String, default: 'Dr. Hopps' },
  paCharacter: { type: String, default: 'bunny' },
  specialist: { type: Object, required: true },
  specialty: { type: String, default: 'general_medicine' },
  reason: { type: String, default: '' },
  visible: { type: Boolean, default: false },
})

const paEmoji = computed(() => PA_EMOJIS[props.paCharacter] || '🐰')

const formattedSpecialty = computed(() =>
  props.specialty.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
)
</script>

<style scoped>
.handoff-enter-active {
  transition: all 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}
.handoff-enter-from {
  opacity: 0;
  transform: translateY(24px) scale(0.92);
}
.handoff-leave-active {
  transition: all 0.3s ease-in;
}
.handoff-leave-to {
  opacity: 0;
  transform: translateY(-12px) scale(0.96);
}

/* Staggered entrance for child elements */
.handoff-enter-active .handoff-pa {
  transition-delay: 0.1s;
}
.handoff-enter-active .handoff-arrow {
  transition-delay: 0.3s;
}
.handoff-enter-active .handoff-specialist {
  transition-delay: 0.5s;
}
.handoff-enter-from .handoff-pa,
.handoff-enter-from .handoff-arrow,
.handoff-enter-from .handoff-specialist {
  opacity: 0;
  transform: translateY(8px);
}
</style>
