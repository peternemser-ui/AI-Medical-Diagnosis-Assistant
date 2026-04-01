<template>
  <button
    :class="[
      'body-system-card group relative flex flex-col items-center gap-3 p-5 rounded-2xl border transition-all duration-300 ease-out cursor-pointer outline-none',
      'backdrop-blur-md',
      active
        ? 'is-active border-transparent scale-[1.03]'
        : 'border-white/[0.08] hover:-translate-y-1'
    ]"
    :style="cardStyle"
    :aria-label="`${system.name} — ${active ? 'Active' : 'Inactive'}. Analyze conditions related to ${system.name}`"
    :aria-pressed="active"
    tabindex="0"
    @mouseenter="hovered = true"
    @mouseleave="hovered = false"
    @focus="focused = true"
    @blur="focused = false"
  >
    <!-- Animated energy ring for active state -->
    <div v-if="active" class="energy-ring absolute inset-0 rounded-2xl pointer-events-none" :style="energyRingStyle"></div>

    <!-- Outer glow shadow (hover + active) -->
    <div
      class="absolute inset-0 rounded-2xl pointer-events-none transition-opacity duration-300"
      :style="outerGlowStyle"
      :class="hovered || active ? 'opacity-100' : 'opacity-0'"
    ></div>

    <!-- Focus ring for accessibility -->
    <div
      v-if="focused"
      class="absolute inset-0 rounded-2xl pointer-events-none ring-2 ring-offset-2 ring-offset-transparent"
      :style="{ '--tw-ring-color': glowColor }"
    ></div>

    <!-- Glow container with pulsing radial gradient -->
    <div class="relative w-14 h-14 flex items-center justify-center">
      <!-- Radial glow behind icon -->
      <div
        class="absolute inset-0 rounded-full blur-xl transition-all duration-300"
        :class="[
          active ? 'glow-pulse-active' : 'glow-pulse-idle',
          hovered ? 'scale-125' : ''
        ]"
        :style="{ background: `radial-gradient(circle, ${glowColor}40 0%, transparent 70%)`, animationDelay: `${animDelay}ms` }"
      ></div>

      <!-- Secondary inner glow -->
      <div
        class="absolute inset-1 rounded-full blur-md transition-opacity duration-300"
        :style="{ background: `radial-gradient(circle, ${glowColor}30 0%, transparent 60%)` }"
        :class="hovered || active ? 'opacity-100' : 'opacity-50'"
      ></div>

      <!-- Subtle particles (3 tiny dots orbiting) -->
      <div v-if="hovered || active" class="absolute inset-0 pointer-events-none">
        <span
          v-for="i in 3"
          :key="i"
          class="particle absolute w-1 h-1 rounded-full"
          :style="{
            backgroundColor: glowColor,
            animationDelay: `${(i - 1) * 0.8}s`,
            opacity: 0.6
          }"
        ></span>
      </div>

      <!-- Icon -->
      <div class="relative z-10 flex items-center justify-center">
        <svg
          v-if="system.svg"
          class="w-7 h-7 transition-all duration-300 drop-shadow-lg"
          :class="active ? (isDark ? 'text-white' : 'text-slate-900') + ' scale-110' : hovered ? (isDark ? 'text-white/90' : 'text-slate-700') : (isDark ? 'text-white/70' : 'text-slate-500')"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          viewBox="0 0 24 24"
          v-html="system.svg"
        ></svg>
        <span v-else class="text-3xl transition-transform duration-300" :class="active || hovered ? 'scale-110' : ''">{{ system.icon }}</span>
      </div>
    </div>

    <!-- Label -->
    <span
      class="text-xs font-medium tracking-wide text-center leading-tight transition-colors duration-300 uppercase"
      :class="active ? (isDark ? 'text-white' : 'text-slate-900') : hovered ? (isDark ? 'text-white/90' : 'text-slate-700') : (isDark ? 'text-white/60' : 'text-slate-500')"
    >
      {{ system.name }}
    </span>

    <!-- Active indicator dot -->
    <div
      v-if="active"
      class="absolute top-2.5 right-2.5 w-2 h-2 rounded-full active-dot"
      :style="{ backgroundColor: glowColor, boxShadow: `0 0 6px ${glowColor}` }"
    ></div>

    <!-- Tooltip -->
    <div
      class="tooltip absolute -bottom-10 left-1/2 -translate-x-1/2 whitespace-nowrap px-3 py-1.5 rounded-lg text-detail font-medium text-white/90 bg-black/80 backdrop-blur-sm border border-white/10 pointer-events-none transition-all duration-200 z-20"
      :class="hovered ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-1'"
    >
      Analyze conditions related to {{ system.name }}
    </div>
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  system: { type: Object, required: true },
  active: { type: Boolean, default: false },
  glowColor: { type: String, default: '#3b82f6' },
  animDelay: { type: Number, default: 0 },
  isDark: { type: Boolean, default: true },
})

const hovered = ref(false)
const focused = ref(false)

const cardStyle = computed(() => {
  if (!props.isDark) {
    // Light mode
    const base = {
      background: props.active ? `${props.glowColor}08` : '#ffffff',
      borderColor: props.active ? `${props.glowColor}30` : '#e2e8f0',
    }
    if (hovered.value && !props.active) {
      base.background = '#f8fafc'
      base.borderColor = `${props.glowColor}40`
    }
    return base
  }
  // Dark mode
  const base = {
    background: props.active
      ? `linear-gradient(135deg, ${props.glowColor}15 0%, ${props.glowColor}08 50%, rgba(10,15,28,0.9) 100%)`
      : 'rgba(10, 15, 28, 0.6)',
  }
  if (hovered.value && !props.active) {
    base.background = `linear-gradient(135deg, ${props.glowColor}10 0%, rgba(10,15,28,0.7) 100%)`
    base.borderColor = `${props.glowColor}40`
  }
  return base
})

const outerGlowStyle = computed(() => ({
  boxShadow: `0 0 30px ${props.glowColor}20, 0 0 60px ${props.glowColor}10`,
}))

const energyRingStyle = computed(() => ({
  background: `conic-gradient(from var(--ring-angle, 0deg), transparent 0%, ${props.glowColor}50 25%, transparent 50%, ${props.glowColor}30 75%, transparent 100%)`,
  mask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
  WebkitMask: 'linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0)',
  maskComposite: 'xor',
  WebkitMaskComposite: 'xor',
  padding: '2px',
}))
</script>

<style scoped>
/* Idle pulse animation */
.glow-pulse-idle {
  animation: glowPulseIdle 2.5s ease-in-out infinite;
}

@keyframes glowPulseIdle {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.08); opacity: 0.8; }
}

/* Active pulse animation (stronger) */
.glow-pulse-active {
  animation: glowPulseActive 2s ease-in-out infinite;
}

@keyframes glowPulseActive {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.15); opacity: 1; }
}

/* Energy ring rotation */
.energy-ring {
  animation: ringRotate 3s linear infinite;
}

@keyframes ringRotate {
  from { --ring-angle: 0deg; }
  to { --ring-angle: 360deg; }
}

@property --ring-angle {
  syntax: '<angle>';
  initial-value: 0deg;
  inherits: false;
}

/* Active indicator dot pulse */
.active-dot {
  animation: dotPulse 1.5s ease-in-out infinite;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.3); }
}

/* Particle orbiting animation */
.particle:nth-child(1) {
  animation: orbit1 3s linear infinite;
}
.particle:nth-child(2) {
  animation: orbit2 3.5s linear infinite;
}
.particle:nth-child(3) {
  animation: orbit3 4s linear infinite;
}

@keyframes orbit1 {
  0% { top: 50%; left: 0; }
  25% { top: 0; left: 50%; }
  50% { top: 50%; left: 100%; }
  75% { top: 100%; left: 50%; }
  100% { top: 50%; left: 0; }
}

@keyframes orbit2 {
  0% { top: 0; left: 30%; }
  25% { top: 30%; left: 100%; }
  50% { top: 100%; left: 70%; }
  75% { top: 70%; left: 0; }
  100% { top: 0; left: 30%; }
}

@keyframes orbit3 {
  0% { top: 100%; left: 50%; }
  25% { top: 50%; left: 0; }
  50% { top: 0; left: 50%; }
  75% { top: 50%; left: 100%; }
  100% { top: 100%; left: 50%; }
}

/* Focus visible */
.body-system-card:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
}
</style>
