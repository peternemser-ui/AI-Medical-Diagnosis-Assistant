<template>
  <div class="min-h-screen relative overflow-hidden transition-colors duration-300"
    :class="isDark ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'">

    <!-- ═══════ BACKGROUND LAYER (z-0) ═══════ -->
    <!-- Animated gradient color fields -->
    <canvas ref="bgCanvas" class="fixed inset-0 w-full h-full pointer-events-none" style="z-index:0"></canvas>

    <!-- Subtle grid overlay for texture -->
    <div class="fixed inset-0 pointer-events-none" style="z-index:1"
      :class="isDark ? 'opacity-[0.03]' : 'opacity-[0.04]'">
      <div class="w-full h-full" style="background-image: radial-gradient(circle, currentColor 0.5px, transparent 0.5px); background-size: 24px 24px;"></div>
    </div>

    <!-- Noise texture layer -->
    <div class="fixed inset-0 pointer-events-none mix-blend-overlay" style="z-index:1"
      :class="isDark ? 'opacity-[0.015]' : 'opacity-[0.02]'">
      <svg width="100%" height="100%"><filter id="noiseFilter"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#noiseFilter)"/></svg>
    </div>

    <!-- ═══════ MIDGROUND LAYER (z-10) ═══════ -->
    <!-- Frosted panels that sit between background and foreground -->

    <!-- Navigation -->
    <nav class="relative flex items-center justify-between px-6 sm:px-10 py-5" style="z-index:30">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
          </svg>
        </div>
        <span class="text-base font-semibold tracking-tight" :class="isDark ? 'text-white' : 'text-slate-900'">{{ t('nav.brand') }}</span>
      </div>
      <div class="flex items-center gap-2">
        <router-link to="/reports" class="text-sm transition-colors px-3 py-1.5 hidden sm:inline" :class="isDark ? 'text-slate-400 hover:text-white' : 'text-slate-500 hover:text-slate-900'">
          Reports
        </router-link>
        <ThemeLangControls />
        <!-- User menu -->
        <div class="relative" ref="userMenuRef">
          <button @click="showUserMenu = !showUserMenu" class="flex items-center gap-1.5 px-2 py-1.5 rounded-lg transition-all" :class="isDark ? 'hover:bg-slate-800/60 text-slate-400 hover:text-white' : 'hover:bg-slate-200/60 text-slate-500 hover:text-slate-900'">
            <div class="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-[10px] font-bold text-white">
              {{ userInitials || '?' }}
            </div>
            <svg class="w-3 h-3 hidden sm:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <Transition enter-active-class="transition duration-150 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
            <div v-if="showUserMenu" class="absolute right-0 top-full mt-1 w-48 rounded-lg shadow-xl border z-50 overflow-hidden py-1" :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-slate-200'">
              <div v-if="userName" class="px-3 py-2 border-b" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
                <div class="text-xs font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ userName }}</div>
                <div class="text-[10px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ userEmail || 'No email set' }}</div>
              </div>
              <router-link to="/profile" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                Profile
              </router-link>
              <router-link to="/settings" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                Settings
              </router-link>
              <router-link to="/reports" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                Reports
              </router-link>
              <router-link to="/setup" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
                API Keys
              </router-link>
            </div>
          </Transition>
        </div>
      </div>
    </nav>

    <!-- ═══════ FOREGROUND LAYER (z-20) ═══════ -->
    <!-- Hero — highest visual prominence -->
    <div class="relative flex flex-col items-center text-center px-6 pt-6 sm:pt-12 pb-8" style="z-index:20">
      <!-- Badge -->
      <div class="inline-flex items-center gap-2 rounded-full px-4 py-1.5 mb-6 border backdrop-blur-md"
        :class="isDark ? 'bg-blue-500/10 border-blue-500/20' : 'bg-white/60 border-blue-200'">
        <div class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></div>
        <span class="text-xs font-medium" :class="isDark ? 'text-blue-300' : 'text-blue-600'">{{ t('hero.badge') }}</span>
      </div>

      <!-- Headline -->
      <h1 class="font-headline text-4xl sm:text-5xl lg:text-[3.6rem] font-bold max-w-4xl my-8" style="letter-spacing:0.1em; line-height:1.1">
        <span :class="isDark ? 'bg-gradient-to-r from-white via-white to-slate-400 bg-clip-text text-transparent' : 'text-slate-900'">{{ t('hero.title1') }}</span>
        <br />
        <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent italic">{{ t('hero.title2') }}</span>
      </h1>

      <!-- Avatar showcase -->
      <div class="mt-8 mb-4 relative">
        <!-- Avatar glow — sits behind the avatar, inside foreground layer -->
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div class="w-64 h-64 sm:w-80 sm:h-80 rounded-full blur-[80px] transition-colors duration-1000"
            :class="isDark ? 'opacity-25' : 'opacity-15'"
            :style="{ backgroundColor: heroAvatar.bgColor }"></div>
        </div>
        <div class="relative hero-avatar-float">
          <DoctorAvatar :avatar="heroAvatar" :speaking="heroSpeaking" :waving="heroWaving" size="xxl" :show-name="false" />
        </div>
        <div class="mt-3 text-center">
          <div class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ heroAvatar.name }}</div>
          <div class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ heroAvatar.specialty }}</div>
          <!-- Sound toggle -->
          <button
            @click="toggleSound"
            class="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 border"
            :class="soundOn
              ? (isDark ? 'bg-blue-500/15 border-blue-500/30 text-blue-300 hover:bg-blue-500/25' : 'bg-blue-50 border-blue-300 text-blue-600 hover:bg-blue-100')
              : (isDark ? 'bg-slate-800/60 border-slate-700/50 text-slate-400 hover:text-slate-200 hover:bg-slate-800' : 'bg-slate-100 border-slate-300 text-slate-500 hover:text-slate-700 hover:bg-slate-200')"
          >
            <!-- Speaker icon -->
            <svg v-if="soundOn" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
            </svg>
            <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"/>
            </svg>
            {{ soundOn ? 'Listening' : 'Tap to hear me' }}
            <!-- Animated sound waves when speaking -->
            <span v-if="soundOn && heroSpeaking" class="flex items-center gap-0.5 ml-0.5">
              <span class="w-0.5 h-2 rounded-full animate-pulse" :class="isDark ? 'bg-blue-400' : 'bg-blue-500'" style="animation-delay:0s"></span>
              <span class="w-0.5 h-3 rounded-full animate-pulse" :class="isDark ? 'bg-blue-400' : 'bg-blue-500'" style="animation-delay:0.15s"></span>
              <span class="w-0.5 h-2 rounded-full animate-pulse" :class="isDark ? 'bg-blue-400' : 'bg-blue-500'" style="animation-delay:0.3s"></span>
            </span>
          </button>
        </div>
      </div>

      <p class="mt-4 text-base sm:text-lg max-w-xl leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
        {{ t('hero.subtitle') }}
      </p>

      <!-- CTA Buttons -->
      <div class="mt-8 flex flex-col sm:flex-row items-center gap-4">
        <button
          @click="startConsultation"
          class="group relative bg-blue-600 hover:bg-blue-500 text-white font-semibold text-base px-8 py-3.5 rounded-xl shadow-lg shadow-blue-600/25 transition-all duration-200 hover:shadow-xl hover:shadow-blue-500/30 hover:-translate-y-0.5 flex items-center gap-2.5"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
          {{ t('hero.startBtn') }}
          <svg class="w-4 h-4 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </button>
        <router-link
          to="/dashboard"
          class="font-medium text-sm px-6 py-3.5 rounded-xl border backdrop-blur-sm transition-all duration-200 flex items-center gap-2"
          :class="isDark
            ? 'text-slate-400 hover:text-white border-slate-700/50 hover:border-slate-600 bg-slate-900/30 hover:bg-slate-800/50'
            : 'text-slate-600 hover:text-slate-900 border-slate-300 hover:border-slate-400 bg-white/40 hover:bg-white/70'"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          {{ t('hero.reportBtn') }}
        </router-link>
      </div>
    </div>

    <!-- ═══════ MIDGROUND — Agent Pipeline ═══════ -->
    <div class="relative max-w-4xl mx-auto px-6 mt-6 sm:mt-10" style="z-index:10">
      <!-- Frosted panel -->
      <div class="rounded-2xl p-6 sm:p-8 backdrop-blur-lg border"
        :class="isDark
          ? 'bg-slate-900/40 border-slate-700/30'
          : 'bg-white/50 border-white/60 shadow-lg shadow-slate-200/50'">
        <div class="text-center mb-6">
          <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ t('hero.howItWorks') }}</h2>
          <p class="text-sm mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-500'">{{ t('hero.howItWorksDesc') }}</p>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
          <div
            v-for="(agent, i) in agents" :key="agent.key"
            class="group relative rounded-xl p-3 text-center transition-all duration-300 border"
            :class="isDark
              ? 'bg-slate-800/50 border-slate-700/40 hover:border-slate-600/60 hover:bg-slate-800/70'
              : 'bg-white/70 border-slate-200/80 hover:border-slate-300 hover:bg-white shadow-sm'"
          >
            <div class="absolute -top-2 -left-1 w-5 h-5 rounded-full flex items-center justify-center border"
              :class="isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-slate-300 shadow-sm'">
              <span class="text-[9px] font-bold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ i + 1 }}</span>
            </div>
            <div class="text-xl mb-1.5">{{ agent.icon }}</div>
            <div class="text-xs font-semibold" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ t(agent.nameKey) }}</div>
            <div class="text-[10px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ t(agent.descKey) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════ MIDGROUND — Feature Cards ═══════ -->
    <div class="relative max-w-5xl mx-auto px-6 mt-10 sm:mt-16 pb-20" style="z-index:10">
      <div class="grid sm:grid-cols-3 gap-4">
        <div v-for="feat in features" :key="feat.titleKey"
          class="rounded-xl p-5 transition-all duration-300 border backdrop-blur-lg"
          :class="isDark
            ? 'bg-slate-900/40 border-slate-700/30 hover:border-slate-600/50 hover:bg-slate-900/60'
            : 'bg-white/50 border-white/60 hover:bg-white/70 shadow-lg shadow-slate-200/40 hover:shadow-slate-300/50'"
        >
          <div class="w-10 h-10 rounded-lg flex items-center justify-center mb-3" :class="feat.iconBg">
            <svg class="w-5 h-5" :class="feat.iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="feat.iconPath"/>
            </svg>
          </div>
          <h3 class="text-sm font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-800'">{{ t(feat.titleKey) }}</h3>
          <p class="text-xs leading-relaxed" :class="isDark ? 'text-slate-500' : 'text-slate-500'">{{ t(feat.descKey) }}</p>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="relative border-t py-6 px-6 text-center" style="z-index:10"
      :class="isDark ? 'border-slate-800/50' : 'border-slate-200'">
      <p class="text-[11px] max-w-lg mx-auto leading-relaxed" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
        {{ t('hero.disclaimer') }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import DoctorAvatar from '@/components/DoctorAvatar.vue'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'

const router = useRouter()
const { isDark } = useTheme()
const { t } = useI18n()

// User menu
const showUserMenu = ref(false)
const userMenuRef = ref(null)
const userProfile = JSON.parse(localStorage.getItem('user_profile') || '{}')
const userName = ref(userProfile.name || '')
const userEmail = ref(userProfile.email || '')
const userInitials = ref(
  userName.value
    ? userName.value.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
    : ''
)

function onClickOutsideUserMenu(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) showUserMenu.value = false
}
onMounted(() => document.addEventListener('click', onClickOutsideUserMenu))
onUnmounted(() => document.removeEventListener('click', onClickOutsideUserMenu))

// ─── Animated background ───
const bgCanvas = ref(null)
let animId = null
let blobs = []
let mouseX = -1
let mouseY = -1

const darkPalette = [
  [20, 60, 160],   // vivid blue
  [90, 30, 140],   // rich purple
  [10, 100, 110],  // teal
  [60, 15, 120],   // deep indigo
  [140, 40, 100],  // magenta
  [15, 80, 140],   // ocean blue
  [30, 50, 100],   // steel blue
  [80, 20, 160],   // electric violet
  [5, 110, 90],    // emerald teal
  [110, 30, 70],   // berry
]
const lightPalette = [
  [50, 100, 255],  // electric blue
  [140, 60, 255],  // vivid purple
  [0, 200, 200],   // cyan
  [255, 60, 130],  // hot pink
  [255, 120, 0],   // tangerine orange
  [0, 180, 255],   // azure
  [180, 0, 255],   // violet
  [0, 220, 120],   // emerald
  [255, 80, 80],   // coral red
  [80, 60, 255],   // indigo
]

function initBlobs(w, h) {
  const palette = isDark.value ? darkPalette : lightPalette
  // Dark: slower, more subtle drift. Light: moderate, visible but calm.
  const speedMult = isDark.value ? 0.4 : 0.8
  blobs = Array.from({ length: 10 }, (_, i) => ({
    x: Math.random() * w,
    y: Math.random() * h,
    r: (isDark.value ? 180 : 140) + Math.random() * (isDark.value ? 320 : 260),
    vx: (Math.random() - 0.5) * 0.35 * speedMult,
    vy: (Math.random() - 0.5) * 0.25 * speedMult,
    color: palette[i % palette.length],
    targetColor: palette[i % palette.length],
    phase: Math.random() * Math.PI * 2,
    pulseSpeed: (0.001 + Math.random() * 0.003) * speedMult,
    orbitRadius: (15 + Math.random() * 40) * (isDark.value ? 1 : 1.2),
    orbitSpeed: (0.0002 + Math.random() * 0.0005) * speedMult,
    orbitPhase: Math.random() * Math.PI * 2,
  }))
}

function lerpColor(a, b, t) {
  return [
    a[0] + (b[0] - a[0]) * t,
    a[1] + (b[1] - a[1]) * t,
    a[2] + (b[2] - a[2]) * t,
  ]
}

function renderBackground(time) {
  const canvas = bgCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width
  const h = canvas.height

  // Base fill — light mode uses pure white so screen-blended colors pop
  ctx.fillStyle = isDark.value ? '#020617' : '#ffffff'
  ctx.fillRect(0, 0, w, h)

  // Dark: screen blend makes colors glow. Light: normal blend paints color directly.
  ctx.globalCompositeOperation = isDark.value ? 'screen' : 'source-over'

  const baseOpacity = isDark.value ? 0.3 : 0.25

  for (const blob of blobs) {
    // Orbital drift on top of linear movement
    const ox = Math.sin(time * blob.orbitSpeed + blob.orbitPhase) * blob.orbitRadius
    const oy = Math.cos(time * blob.orbitSpeed * 1.3 + blob.orbitPhase) * blob.orbitRadius * 0.7

    blob.x += blob.vx
    blob.y += blob.vy

    const drawX = blob.x + ox
    const drawY = blob.y + oy

    // Pulse
    const pulse = Math.sin(time * blob.pulseSpeed + blob.phase) * 0.25 + 1
    const r = blob.r * pulse

    // Bounce
    if (blob.x < -100) blob.vx = Math.abs(blob.vx)
    if (blob.x > w + 100) blob.vx = -Math.abs(blob.vx)
    if (blob.y < -100) blob.vy = Math.abs(blob.vy)
    if (blob.y > h + 100) blob.vy = -Math.abs(blob.vy)

    // Lerp color toward target for smooth theme transitions
    blob.color = lerpColor(blob.color, blob.targetColor, 0.02)

    // Mouse interaction: very gentle push
    if (mouseX >= 0) {
      const dx = drawX - mouseX
      const dy = drawY - mouseY
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < 300) {
        const force = (300 - dist) / 300 * 0.04
        blob.vx += (dx / dist) * force
        blob.vy += (dy / dist) * force
      }
    }

    // Dampen velocity — keeps blobs from accelerating over time
    blob.vx *= 0.997
    blob.vy *= 0.997

    // Draw blob with multiple gradient layers for richness
    const [cr, cg, cb] = blob.color
    const grad = ctx.createRadialGradient(drawX, drawY, 0, drawX, drawY, r)
    grad.addColorStop(0, `rgba(${cr|0}, ${cg|0}, ${cb|0}, ${baseOpacity})`)
    grad.addColorStop(0.3, `rgba(${cr|0}, ${cg|0}, ${cb|0}, ${baseOpacity * 0.6})`)
    grad.addColorStop(0.6, `rgba(${cr|0}, ${cg|0}, ${cb|0}, ${baseOpacity * 0.2})`)
    grad.addColorStop(1, `rgba(${cr|0}, ${cg|0}, ${cb|0}, 0)`)
    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.arc(drawX, drawY, r, 0, Math.PI * 2)
    ctx.fill()

    // Inner glow for hotspot — much brighter in light mode
    const glowMult = isDark.value ? 0.5 : 1.2
    const innerR = r * (isDark.value ? 0.35 : 0.5)
    const grad2 = ctx.createRadialGradient(drawX, drawY, 0, drawX, drawY, innerR)
    grad2.addColorStop(0, `rgba(${Math.min(255, (cr|0)+80)}, ${Math.min(255, (cg|0)+80)}, ${Math.min(255, (cb|0)+80)}, ${baseOpacity * glowMult})`)
    grad2.addColorStop(1, `rgba(${cr|0}, ${cg|0}, ${cb|0}, 0)`)
    ctx.fillStyle = grad2
    ctx.beginPath()
    ctx.arc(drawX, drawY, innerR, 0, Math.PI * 2)
    ctx.fill()
  }

  // Aurora streaks (horizontal light bands)
  ctx.globalCompositeOperation = isDark.value ? 'screen' : 'source-over'
  const streakCount = isDark.value ? 2 : 5
  for (let i = 0; i < streakCount; i++) {
    const yBase = isDark.value ? (0.25 + i * 0.4) : (0.1 + i * 0.18)
    const y = h * yBase + Math.sin(time * 0.0003 + i * 2) * h * 0.05
    const thickness = isDark.value ? 50 : 100
    const streakGrad = ctx.createLinearGradient(0, y - thickness, 0, y + thickness)
    const hue = (time * 0.008 + i * 50) % 360
    const alpha = isDark.value ? 0.04 : 0.12
    const sat = isDark.value ? 60 : 90
    const lum = isDark.value ? 45 : 60
    streakGrad.addColorStop(0, `hsla(${hue}, ${sat}%, ${lum}%, 0)`)
    streakGrad.addColorStop(0.5, `hsla(${hue}, ${sat}%, ${lum}%, ${alpha})`)
    streakGrad.addColorStop(1, `hsla(${hue}, ${sat}%, ${lum}%, 0)`)
    ctx.fillStyle = streakGrad
    ctx.fillRect(0, y - thickness, w, thickness * 2)
  }

  ctx.globalCompositeOperation = 'source-over'

  // ── Radiating lines — white rays emanating from a focal point with crescendo thickness ──
  ctx.lineCap = 'round'

  // Focal point: slightly above center, drifts slowly
  const focalX = w * 0.5 + Math.sin(time * 0.00008) * w * 0.05
  const focalY = h * 0.35 + Math.cos(time * 0.00006) * h * 0.03

  if (!isDark.value) {
    const rayCount = 60
    for (let i = 0; i < rayCount; i++) {
      const progress = i / (rayCount - 1)
      // Angle spread: full circle but weighted toward bottom half
      const angle = (i / rayCount) * Math.PI * 2 + time * 0.00003
      // Thickness crescendo as rays fan out
      const thickness = 0.3 + progress * progress * 6
      // Alpha: thin rays ghostly, thick rays bolder
      const alpha = 0.03 + Math.sin(progress * Math.PI) * 0.2
      // Ray length: extends well beyond screen
      const rayLen = Math.max(w, h) * 1.2

      const endX = focalX + Math.cos(angle) * rayLen
      const endY = focalY + Math.sin(angle) * rayLen

      ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`
      ctx.lineWidth = thickness
      ctx.beginPath()
      ctx.moveTo(focalX, focalY)
      ctx.lineTo(endX, endY)
      ctx.stroke()
    }
  } else {
    // Dark mode: fewer, subtler radiating rays
    const rayCount = 30
    for (let i = 0; i < rayCount; i++) {
      const progress = i / (rayCount - 1)
      const angle = (i / rayCount) * Math.PI * 2 + time * 0.00002
      const thickness = 0.2 + progress * progress * 1.8
      const alpha = 0.01 + Math.sin(progress * Math.PI) * 0.04
      const rayLen = Math.max(w, h) * 1.2

      const endX = focalX + Math.cos(angle) * rayLen
      const endY = focalY + Math.sin(angle) * rayLen

      ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`
      ctx.lineWidth = thickness
      ctx.beginPath()
      ctx.moveTo(focalX, focalY)
      ctx.lineTo(endX, endY)
      ctx.stroke()
    }
  }

  animId = requestAnimationFrame(renderBackground)
}

function onMouseMove(e) {
  mouseX = e.clientX
  mouseY = e.clientY
}

function resizeCanvas() {
  const canvas = bgCanvas.value
  if (!canvas) return
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
  initBlobs(canvas.width, canvas.height)
}

// Watch theme changes to smoothly transition blob colors
watch(isDark, () => {
  const palette = isDark.value ? darkPalette : lightPalette
  blobs.forEach((blob, i) => {
    blob.targetColor = palette[i % palette.length]
  })
})

onMounted(() => {
  resizeCanvas()
  animId = requestAnimationFrame(renderBackground)
  window.addEventListener('resize', resizeCanvas)
  window.addEventListener('mousemove', onMouseMove)
})

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
  window.removeEventListener('resize', resizeCanvas)
  window.removeEventListener('mousemove', onMouseMove)
  if (speakInterval) clearInterval(speakInterval)
  if (waveInterval) clearInterval(waveInterval)
  if (keepAliveInterval) clearInterval(keepAliveInterval)
  if (window.speechSynthesis) window.speechSynthesis.cancel()
})

// ─── Avatar ───
const defaultHeroAvatar = {
  name: 'Dr. AI', specialty: 'General Practitioner',
  skinTone: '#F5CBA7', hairStyle: 'short', hairColor: '#3d2b1f', eyeColor: '#4A6FA5',
  coatColor: '#f0f0f0', glasses: true, bgColor: '#1e3a5f', lipColor: '#c9877a',
  accessoryColor: '#64748b', avatarStyle: 'realistic', photoUrl: '',
}
const saved = localStorage.getItem('doctor_avatar')
const heroAvatar = ref(saved ? { ...defaultHeroAvatar, ...JSON.parse(saved) } : defaultHeroAvatar)

const heroSpeaking = ref(false)
const heroWaving = ref(false)
const soundOn = ref(false)
let speakInterval = null
let keepAliveInterval = null
let waveInterval = null

// Greeting messages per language
const greetings = {
  en: `Hello! I'm ${heroAvatar.value.name}, your AI ${heroAvatar.value.specialty}. I'm here to help you understand your symptoms. Just click Start Consultation and describe how you're feeling. I'll guide you through a thorough assessment.`,
  zh: `\u4F60\u597D\uFF01\u6211\u662F${heroAvatar.value.name}\uFF0C\u60A8\u7684AI${heroAvatar.value.specialty}\u3002\u6211\u5728\u8FD9\u91CC\u5E2E\u52A9\u60A8\u4E86\u89E3\u60A8\u7684\u75C7\u72B6\u3002\u70B9\u51FB\u5F00\u59CB\u54A8\u8BE2\uFF0C\u63CF\u8FF0\u60A8\u7684\u611F\u53D7\u3002`,
  es: `\u00A1Hola! Soy ${heroAvatar.value.name}, su ${heroAvatar.value.specialty} con IA. Estoy aqu\u00ED para ayudarle a entender sus s\u00EDntomas. Haga clic en Iniciar Consulta y describa c\u00F3mo se siente.`,
  hi: `\u0928\u092E\u0938\u094D\u0924\u0947! \u092E\u0948\u0902 ${heroAvatar.value.name} \u0939\u0942\u0901\u0964 \u092E\u0948\u0902 \u0906\u092A\u0915\u0947 \u0932\u0915\u094D\u0937\u0923\u094B\u0902 \u0915\u094B \u0938\u092E\u091D\u0928\u0947 \u092E\u0947\u0902 \u0906\u092A\u0915\u0940 \u092E\u0926\u0926 \u0915\u0947 \u0932\u093F\u090F \u092F\u0939\u093E\u0901 \u0939\u0942\u0901\u0964 \u092A\u0930\u093E\u092E\u0930\u094D\u0936 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902 \u092A\u0930 \u0915\u094D\u0932\u093F\u0915 \u0915\u0930\u0947\u0902\u0964`,
  fr: `Bonjour ! Je suis ${heroAvatar.value.name}, votre ${heroAvatar.value.specialty} IA. Je suis l\u00E0 pour vous aider \u00E0 comprendre vos sympt\u00F4mes. Cliquez sur Commencer la Consultation et d\u00E9crivez comment vous vous sentez.`,
}

function pickVoice() {
  if (!window.speechSynthesis) return null
  const voices = window.speechSynthesis.getVoices()
  if (!voices.length) return null

  const preferredName = heroAvatar.value.preferredVoice
  if (preferredName) {
    const match = voices.find(v => v.name === preferredName)
    if (match) return match
  }

  const name = (heroAvatar.value.name || '').toLowerCase()
  const femaleNames = ['sarah','maria','amara','emma','lisa','anna','jessica','rachel','emily']
  const preferFemale = femaleNames.some(n => name.includes(n))

  const ranked = [
    preferFemale ? 'Google UK English Female' : 'Google UK English Male',
    preferFemale ? 'Microsoft Zira' : 'Microsoft David',
    preferFemale ? 'Microsoft Jenny Online' : 'Microsoft Guy Online',
    preferFemale ? 'Samantha' : 'Daniel',
  ]
  for (const n of ranked) {
    const v = voices.find(voice => voice.name.includes(n))
    if (v) return v
  }
  const en = voices.filter(v => v.lang.startsWith('en'))
  return en.find(v => !v.localService) || en[0] || voices[0]
}

function speakGreeting() {
  if (!window.speechSynthesis) return
  window.speechSynthesis.cancel()

  const { lang: currentLang } = useI18n()
  const text = greetings[currentLang.value] || greetings.en

  // Split into chunks for reliability
  const chunks = []
  let remaining = text
  while (remaining.length > 0) {
    if (remaining.length <= 200) { chunks.push(remaining); break }
    let idx = remaining.lastIndexOf('. ', 200)
    if (idx < 60) idx = remaining.lastIndexOf(', ', 200)
    if (idx < 60) idx = remaining.lastIndexOf(' ', 200)
    if (idx < 60) idx = 200
    chunks.push(remaining.substring(0, idx + 1))
    remaining = remaining.substring(idx + 1).trim()
  }

  const voice = pickVoice()
  const rate = heroAvatar.value.voiceRate || 0.95

  // Chrome keep-alive
  keepAliveInterval = setInterval(() => {
    if (window.speechSynthesis.speaking) window.speechSynthesis.resume()
  }, 5000)

  heroSpeaking.value = true

  function speakNext(i) {
    if (i >= chunks.length || !soundOn.value) {
      heroSpeaking.value = false
      if (keepAliveInterval) { clearInterval(keepAliveInterval); keepAliveInterval = null }
      return
    }
    const utt = new SpeechSynthesisUtterance(chunks[i])
    if (voice) utt.voice = voice
    utt.rate = rate
    utt.pitch = 1.0
    utt.volume = 0.85
    utt.onend = () => speakNext(i + 1)
    utt.onerror = () => speakNext(i + 1)
    window.speechSynthesis.speak(utt)
  }

  // Small delay after cancel
  setTimeout(() => speakNext(0), 80)
}

function toggleSound() {
  soundOn.value = !soundOn.value
  if (soundOn.value) {
    speakGreeting()
  } else {
    if (window.speechSynthesis) window.speechSynthesis.cancel()
    heroSpeaking.value = false
    if (keepAliveInterval) { clearInterval(keepAliveInterval); keepAliveInterval = null }
  }
}

// Idle animations — mouth + wave
onMounted(() => {
  speakInterval = setInterval(() => {
    if (!soundOn.value) {
      heroSpeaking.value = true
      setTimeout(() => { heroSpeaking.value = false }, 2500)
    }
  }, 8000)
  // Initial wave on page load
  heroWaving.value = true
  setTimeout(() => { heroWaving.value = false }, 4000)
  // Wave periodically
  waveInterval = setInterval(() => {
    if (!heroSpeaking.value && !soundOn.value) {
      heroWaving.value = true
      setTimeout(() => { heroWaving.value = false }, 3500)
    }
  }, 12000)
  // Initial idle mouth animation
  if (!soundOn.value) {
    setTimeout(() => { heroSpeaking.value = true }, 1500)
    setTimeout(() => { heroSpeaking.value = false }, 4000)
  }
  // Preload voices
  if (window.speechSynthesis) {
    window.speechSynthesis.getVoices()
    window.speechSynthesis.addEventListener('voiceschanged', () => {})
  }
})

// ─── Data ───
const agents = [
  { key: 'triage', icon: '🚨', nameKey: 'agent.triage', descKey: 'agent.triage.desc' },
  { key: 'diagnostician', icon: '🔬', nameKey: 'agent.diagnostician', descKey: 'agent.diagnostician.desc' },
  { key: 'researcher', icon: '📚', nameKey: 'agent.researcher', descKey: 'agent.researcher.desc' },
  { key: 'specialist', icon: '🏥', nameKey: 'agent.specialist', descKey: 'agent.specialist.desc' },
  { key: 'treatment', icon: '💊', nameKey: 'agent.treatment', descKey: 'agent.treatment.desc' },
  { key: 'safety', icon: '🛡️', nameKey: 'agent.safety', descKey: 'agent.safety.desc' },
  { key: 'empathy', icon: '💬', nameKey: 'agent.empathy', descKey: 'agent.empathy.desc' },
]

const features = [
  {
    titleKey: 'feature.voice.title', descKey: 'feature.voice.desc',
    iconBg: 'bg-blue-500/10', iconColor: 'text-blue-400',
    iconPath: 'M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z',
  },
  {
    titleKey: 'feature.clinical.title', descKey: 'feature.clinical.desc',
    iconBg: 'bg-purple-500/10', iconColor: 'text-purple-400',
    iconPath: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01',
  },
  {
    titleKey: 'feature.safety.title', descKey: 'feature.safety.desc',
    iconBg: 'bg-emerald-500/10', iconColor: 'text-emerald-400',
    iconPath: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  },
]

function startConsultation() {
  const hasKey = localStorage.getItem('api_key_configured')
  router.push(hasKey ? '/consult' : '/setup')
}
</script>

<style scoped>
.font-headline {
  font-family: 'Libre Bodoni', 'Bodoni Moda', 'Playfair Display', Georgia, 'Times New Roman', serif;
}
.hero-avatar-float {
  animation: float 6s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
