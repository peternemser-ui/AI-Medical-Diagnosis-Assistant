<template>
  <div class="neural-body-systems relative rounded-2xl overflow-hidden" :style="containerStyle">
    <!-- Ambient animated background (dark only) -->
    <div v-if="isDark" class="absolute inset-0 pointer-events-none overflow-hidden">
      <!-- Neural line network -->
      <svg class="absolute inset-0 w-full h-full opacity-[0.04]" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="neural-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#7c3aed" stop-opacity="0.5" />
            <stop offset="50%" stop-color="#3b82f6" stop-opacity="0.3" />
            <stop offset="100%" stop-color="#06b6d4" stop-opacity="0.5" />
          </linearGradient>
        </defs>
        <!-- Animated neural lines -->
        <line x1="10%" y1="20%" x2="40%" y2="50%" stroke="url(#neural-grad-1)" stroke-width="0.5" class="neural-line line-1" />
        <line x1="60%" y1="10%" x2="30%" y2="80%" stroke="url(#neural-grad-1)" stroke-width="0.5" class="neural-line line-2" />
        <line x1="80%" y1="30%" x2="50%" y2="90%" stroke="url(#neural-grad-1)" stroke-width="0.5" class="neural-line line-3" />
        <line x1="20%" y1="70%" x2="90%" y2="40%" stroke="url(#neural-grad-1)" stroke-width="0.5" class="neural-line line-4" />
        <line x1="5%" y1="50%" x2="95%" y2="60%" stroke="url(#neural-grad-1)" stroke-width="0.3" class="neural-line line-5" />
        <line x1="45%" y1="5%" x2="55%" y2="95%" stroke="url(#neural-grad-1)" stroke-width="0.3" class="neural-line line-6" />
        <!-- Junction dots -->
        <circle cx="30%" cy="50%" r="1.5" fill="#7c3aed" opacity="0.15" class="neural-dot dot-1" />
        <circle cx="50%" cy="40%" r="1.5" fill="#3b82f6" opacity="0.15" class="neural-dot dot-2" />
        <circle cx="70%" cy="60%" r="1.5" fill="#06b6d4" opacity="0.15" class="neural-dot dot-3" />
        <circle cx="40%" cy="80%" r="1.5" fill="#22c55e" opacity="0.12" class="neural-dot dot-4" />
        <circle cx="60%" cy="20%" r="1.5" fill="#ec4899" opacity="0.12" class="neural-dot dot-5" />
      </svg>

      <!-- Gradient blobs -->
      <div class="absolute w-[300px] h-[300px] -top-[100px] -right-[80px] rounded-full blur-[100px] opacity-[0.06] blob-drift-1"
        style="background: radial-gradient(circle, #7c3aed, transparent)"></div>
      <div class="absolute w-[250px] h-[250px] -bottom-[80px] -left-[60px] rounded-full blur-[100px] opacity-[0.05] blob-drift-2"
        style="background: radial-gradient(circle, #06b6d4, transparent)"></div>
      <div class="absolute w-[200px] h-[200px] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full blur-[80px] opacity-[0.04] blob-drift-3"
        style="background: radial-gradient(circle, #3b82f6, transparent)"></div>
    </div>

    <!-- Header -->
    <div class="relative z-10 px-5 pt-5 pb-3 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-rose-500/80 to-pink-600/80 flex items-center justify-center shadow-lg shadow-rose-500/20 backdrop-blur-sm border border-white/10">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor"><path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" /></svg>
        </div>
        <div>
          <h2 class="text-sm font-bold uppercase tracking-wider" :class="isDark ? 'text-white' : 'text-slate-800'">Body Systems</h2>
          <p class="text-detail mt-0.5" :class="isDark ? 'text-white/40' : 'text-slate-500'">Neural diagnostic mapping</p>
        </div>
      </div>
      <div v-if="activeCount > 0" class="flex items-center gap-1.5 px-2.5 py-1 rounded-full border backdrop-blur-sm"
        :class="isDark ? 'bg-white/[0.06] border-white/[0.08]' : 'bg-emerald-50 border-emerald-200'">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-detail font-semibold text-emerald-400">{{ activeCount }} active</span>
      </div>
    </div>

    <!-- Divider -->
    <div class="relative z-10 mx-5 h-px" :class="isDark ? 'bg-gradient-to-r from-transparent via-white/10 to-transparent' : 'bg-slate-200'"></div>

    <!-- Systems Grid -->
    <div class="relative z-10 p-5">
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4" role="group" aria-label="Body systems diagnostic grid">
        <BodySystemCard
          v-for="(system, index) in systemsWithGlow"
          :key="system.name"
          :system="system"
          :active="system.active"
          :glow-color="system.glowColor"
          :anim-delay="index * 200"
          :is-dark="isDark"
        />
      </div>
    </div>

    <!-- Legend -->
    <div v-if="activeCount > 0" class="relative z-10 px-5 pb-4">
      <div class="flex items-center justify-center gap-6 pt-3 border-t text-detail font-medium"
        :class="isDark ? 'border-white/[0.06] text-white/40' : 'border-slate-200 text-slate-500'">
        <span class="flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full border-2 border-white/20 bg-transparent inline-block"></span>
          Inactive
        </span>
        <span class="flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full bg-blue-500 shadow-[0_0_6px_rgba(59,130,246,0.5)] inline-block"></span>
          Active
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import BodySystemCard from './BodySystemCard.vue'

const { isDark } = useTheme()

const props = defineProps({
  bodySystems: { type: Array, required: true },
})

// Map system names to specific glow colors and SVG icons
const systemGlowMap = {
  'Brain':               { color: '#7c3aed', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>' },
  'Heart':               { color: '#ef4444', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>' },
  'Lungs':               { color: '#06b6d4', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>' },
  'Digestive':           { color: '#22c55e', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>' },
  'Muscles & Joints':    { color: '#f59e0b', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>' },
  'Skin':                { color: '#ec4899', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a6 6 0 00-6-6h-2"/>' },
  'Kidneys':             { color: '#8b5cf6', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>' },
  'Liver':               { color: '#d97706', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>' },
  'Endocrine':           { color: '#14b8a6', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>' },
  'Immune':              { color: '#3b82f6', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>' },
  'Eyes':                { color: '#a78bfa', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>' },
  'Ear, Nose & Throat':  { color: '#f472b6', svg: '<path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>' },
}

const systemsWithGlow = computed(() =>
  props.bodySystems.map(system => ({
    ...system,
    glowColor: systemGlowMap[system.name]?.color || '#3b82f6',
    svg: systemGlowMap[system.name]?.svg || null,
  }))
)

const activeCount = computed(() => props.bodySystems.filter(s => s.active).length)

const containerStyle = computed(() =>
  isDark.value
    ? { background: 'linear-gradient(145deg, #0a0f1c 0%, #070b16 50%, #05070d 100%)', border: '1px solid rgba(255,255,255,0.06)' }
    : { background: '#ffffff', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.06)' }
)
</script>

<style scoped>
/* Neural line animations */
.neural-line {
  stroke-dasharray: 8 4;
  animation: neuralFlow 8s linear infinite;
}
.line-1 { animation-delay: 0s; }
.line-2 { animation-delay: -1.5s; }
.line-3 { animation-delay: -3s; }
.line-4 { animation-delay: -4.5s; }
.line-5 { animation-delay: -2s; }
.line-6 { animation-delay: -5s; }

@keyframes neuralFlow {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -48; }
}

/* Neural junction dot pulse */
.neural-dot {
  animation: dotGlow 3s ease-in-out infinite;
}
.dot-1 { animation-delay: 0s; }
.dot-2 { animation-delay: 0.6s; }
.dot-3 { animation-delay: 1.2s; }
.dot-4 { animation-delay: 1.8s; }
.dot-5 { animation-delay: 2.4s; }

@keyframes dotGlow {
  0%, 100% { r: 1.5; opacity: 0.1; }
  50% { r: 3; opacity: 0.3; }
}

/* Blob drifting animations */
.blob-drift-1 {
  animation: blobDrift1 20s ease-in-out infinite;
}
.blob-drift-2 {
  animation: blobDrift2 25s ease-in-out infinite;
}
.blob-drift-3 {
  animation: blobDrift3 18s ease-in-out infinite;
}

@keyframes blobDrift1 {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(-30px, 20px); }
  66% { transform: translate(20px, -15px); }
}

@keyframes blobDrift2 {
  0%, 100% { transform: translate(0, 0); }
  33% { transform: translate(25px, -20px); }
  66% { transform: translate(-15px, 25px); }
}

@keyframes blobDrift3 {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.2); }
}
</style>
