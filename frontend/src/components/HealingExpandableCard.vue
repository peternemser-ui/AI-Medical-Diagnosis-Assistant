<template>
  <div
    class="healing-card group relative rounded-2xl border transition-all duration-300 overflow-hidden cursor-pointer"
    :class="[
      isExpanded
        ? 'border-transparent'
        : 'hover:-translate-y-1',
      focused ? 'ring-2 ring-offset-0' : ''
    ]"
    :style="cardOuterStyle"
    role="region"
    :aria-label="title"
    @keydown.enter="toggle"
    @keydown.space.prevent="toggle"
  >
    <!-- Glow border overlay -->
    <div
      class="absolute inset-0 rounded-2xl pointer-events-none transition-opacity duration-500"
      :style="glowBorderStyle"
      :class="isExpanded || hovered ? 'opacity-100' : 'opacity-30'"
    ></div>

    <!-- Ambient gradient blob behind card -->
    <div
      class="absolute -top-20 -right-20 w-48 h-48 rounded-full blur-[80px] pointer-events-none transition-opacity duration-500"
      :style="{ background: `radial-gradient(circle, ${accentColor}20, transparent)` }"
      :class="hovered || isExpanded ? 'opacity-100' : 'opacity-0'"
    ></div>

    <!-- Card inner content -->
    <div class="relative z-10">
      <!-- Collapsed header (always visible) -->
      <button
        class="w-full flex items-center gap-4 p-5 text-left outline-none"
        :aria-expanded="isExpanded"
        :aria-controls="`card-content-${cardId}`"
        @click="toggle"
        @mouseenter="hovered = true"
        @mouseleave="hovered = false"
        @focus="focused = true"
        @blur="focused = false"
      >
        <!-- Icon container with glow -->
        <div class="relative flex-shrink-0">
          <div
            class="w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300"
            :style="iconContainerStyle"
          >
            <span class="text-xl">{{ icon }}</span>
          </div>
          <!-- Icon pulse glow -->
          <div
            class="absolute inset-0 rounded-xl blur-md transition-opacity duration-300 -z-10"
            :style="{ background: `${accentColor}30` }"
            :class="hovered || isExpanded ? 'opacity-100 scale-110' : 'opacity-40'"
          ></div>
        </div>

        <!-- Title area -->
        <div class="flex-1 min-w-0">
          <h3 class="text-sm font-bold uppercase tracking-wider transition-colors duration-300" :class="isDark ? 'text-white' : 'text-slate-800'">
            {{ title }}
          </h3>
          <p class="text-caption mt-0.5 line-clamp-1" :class="isDark ? 'text-white/40' : 'text-slate-500'">{{ subtitle }}</p>
        </div>

        <!-- Arrow indicator -->
        <div
          class="w-8 h-8 rounded-lg flex items-center justify-center transition-all duration-300 flex-shrink-0"
          :class="isExpanded ? 'rotate-90' : 'group-hover:translate-x-0.5'"
          :style="{ background: `${accentColor}15` }"
        >
          <svg class="w-4 h-4 transition-colors" :class="isDark ? 'text-white/60' : 'text-slate-400'" :style="isExpanded ? { color: accentColor } : {}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </button>

      <!-- Expanded content -->
      <div
        :id="`card-content-${cardId}`"
        class="expand-region"
        :class="isExpanded ? 'expand-open' : 'expand-closed'"
      >
        <div class="px-5 pb-5 space-y-6" ref="contentRef">
          <!-- Divider -->
          <div class="h-px w-full" :style="{ background: `linear-gradient(to right, transparent, ${accentColor}30, transparent)` }"></div>

          <!-- Content blocks with staggered animation -->
          <div
            v-for="(section, sIdx) in sections"
            :key="sIdx"
            class="content-block"
            :style="{ transitionDelay: isExpanded ? `${sIdx * 80}ms` : '0ms' }"
          >
            <!-- Section header -->
            <div class="flex items-center gap-2.5 mb-3">
              <span class="text-base">{{ section.icon }}</span>
              <span
                class="text-detail font-bold uppercase tracking-[0.15em]"
                :style="{ color: accentColor }"
              >
                {{ section.category }}
              </span>
            </div>

            <!-- Recommendation items -->
            <div class="space-y-2.5 ml-1">
              <div
                v-for="(rec, rIdx) in section.recommendations"
                :key="rIdx"
                class="flex items-start gap-3 p-2.5 rounded-xl transition-colors duration-200 group/item"
                style="background: rgba(255,255,255,0.02)"
                @mouseenter="$event.currentTarget.style.background = `${accentColor}08`"
                @mouseleave="$event.currentTarget.style.background = 'rgba(255,255,255,0.02)'"
              >
                <!-- Bullet glow dot -->
                <div class="flex-shrink-0 mt-1">
                  <div class="w-1.5 h-1.5 rounded-full" :style="{ backgroundColor: accentColor, boxShadow: `0 0 6px ${accentColor}60` }"></div>
                </div>
                <!-- Text with bold key term -->
                <span class="text-xs leading-relaxed" :class="isDark ? 'text-white/70' : 'text-slate-600'" v-html="highlightKeyTerm(rec)"></span>
              </div>
            </div>

            <!-- Evidence level meter -->
            <div v-if="section.evidence" class="flex items-center gap-2 mt-3 ml-1">
              <span class="text-tiny font-semibold uppercase tracking-wider" :class="isDark ? 'text-white/30' : 'text-slate-400'">Evidence</span>
              <div class="flex gap-0.5">
                <div
                  v-for="dot in 5"
                  :key="dot"
                  class="w-2 h-2 rounded-full transition-colors"
                  :style="{ backgroundColor: dot <= section.evidence ? accentColor : 'rgba(255,255,255,0.08)' }"
                ></div>
              </div>
            </div>
          </div>

          <!-- "Why It Works" section -->
          <div v-if="whyItWorks" class="rounded-xl p-4 border" :style="whyBlockStyle">
            <div class="flex items-center gap-2 mb-2">
              <svg class="w-3.5 h-3.5" :style="{ color: accentColor }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="text-detail font-bold uppercase tracking-wider" :class="isDark ? 'text-white/50' : 'text-slate-500'">Why It Works</span>
            </div>
            <p class="text-caption leading-relaxed" :class="isDark ? 'text-white/50' : 'text-slate-500'">{{ whyItWorks }}</p>
          </div>

          <!-- AI Insight panel -->
          <div v-if="aiInsight" class="ai-insight-panel relative rounded-xl p-4 overflow-hidden" :style="aiPanelStyle">
            <!-- Left accent border -->
            <div class="absolute left-0 top-2 bottom-2 w-0.5 rounded-full" :style="{ backgroundColor: accentColor, boxShadow: `0 0 8px ${accentColor}60` }"></div>

            <div class="flex items-start gap-3 ml-2">
              <!-- Brain icon -->
              <div class="flex-shrink-0 w-7 h-7 rounded-lg flex items-center justify-center" :style="{ background: `${accentColor}15` }">
                <svg class="w-3.5 h-3.5" :style="{ color: accentColor }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <span class="text-detail font-bold uppercase tracking-wider" :style="{ color: accentColor }">AI Insight</span>
                <p class="text-caption leading-relaxed mt-1" :class="isDark ? 'text-white/60' : 'text-slate-600'">{{ aiInsight }}</p>
              </div>
            </div>

            <!-- Subtle particles -->
            <div class="absolute top-0 right-0 w-24 h-24 pointer-events-none opacity-30">
              <div class="absolute w-1 h-1 rounded-full ai-particle p-1" :style="{ backgroundColor: accentColor, top: '20%', right: '30%' }"></div>
              <div class="absolute w-0.5 h-0.5 rounded-full ai-particle p-2" :style="{ backgroundColor: accentColor, top: '60%', right: '15%' }"></div>
              <div class="absolute w-1 h-1 rounded-full ai-particle p-3" :style="{ backgroundColor: accentColor, top: '40%', right: '50%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  cardId: { type: String, required: true },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  icon: { type: String, default: '' },
  accentColor: { type: String, default: '#3b82f6' },
  sections: { type: Array, default: () => [] },
  whyItWorks: { type: String, default: '' },
  aiInsight: { type: String, default: '' },
  isDark: { type: Boolean, default: true },
})

const isExpanded = ref(false)
const hovered = ref(false)
const focused = ref(false)

function toggle() {
  isExpanded.value = !isExpanded.value
}

const cardOuterStyle = computed(() => {
  if (!props.isDark) {
    return {
      background: isExpanded.value ? `${props.accentColor}05` : '#ffffff',
      borderColor: hovered.value || isExpanded.value ? `${props.accentColor}40` : '#e2e8f0',
      boxShadow: hovered.value || isExpanded.value ? `0 4px 20px ${props.accentColor}08` : '0 1px 2px rgba(0,0,0,0.04)',
    }
  }
  return {
    background: isExpanded.value
      ? `linear-gradient(145deg, ${props.accentColor}08 0%, rgba(10,15,28,0.95) 40%, rgba(5,7,13,0.98) 100%)`
      : 'rgba(10, 15, 28, 0.7)',
    borderColor: hovered.value || isExpanded.value ? `${props.accentColor}30` : 'rgba(255,255,255,0.06)',
    boxShadow: hovered.value || isExpanded.value ? `0 8px 40px ${props.accentColor}10, 0 0 0 1px ${props.accentColor}15` : 'none',
  }
})

const glowBorderStyle = computed(() => ({
  boxShadow: `inset 0 0 30px ${props.accentColor}08`,
}))

const iconContainerStyle = computed(() => ({
  background: `linear-gradient(135deg, ${props.accentColor}20, ${props.accentColor}08)`,
  border: `1px solid ${props.accentColor}25`,
}))

const whyBlockStyle = computed(() => ({
  background: `${props.accentColor}05`,
  borderColor: `${props.accentColor}15`,
}))

const aiPanelStyle = computed(() => ({
  background: `linear-gradient(135deg, ${props.accentColor}08 0%, rgba(255,255,255,0.02) 100%)`,
  border: `1px solid ${props.accentColor}12`,
}))

function highlightKeyTerm(text) {
  const strongClass = props.isDark ? 'text-white/90' : 'text-slate-800'
  const dashClass = props.isDark ? 'text-white/30' : 'text-slate-400'
  const dashMatch = text.match(/^(.+?)\s*[—–]\s*(.+)$/)
  if (dashMatch) {
    return `<strong class="${strongClass} font-medium">${dashMatch[1]}</strong> <span class="${dashClass}">—</span> ${dashMatch[2]}`
  }
  const colonMatch = text.match(/^(.+?):\s*(.+)$/)
  if (colonMatch) {
    return `<strong class="${strongClass} font-medium">${colonMatch[1]}</strong>: ${colonMatch[2]}`
  }
  return text
}
</script>

<style scoped>
/* Expand/collapse animation */
.expand-region {
  display: grid;
  transition: grid-template-rows 400ms cubic-bezier(0.4, 0, 0.2, 1), opacity 300ms ease;
}

.expand-closed {
  grid-template-rows: 0fr;
  opacity: 0;
}

.expand-open {
  grid-template-rows: 1fr;
  opacity: 1;
}

.expand-region > div {
  overflow: hidden;
}

/* Content block stagger animation */
.content-block {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 300ms ease, transform 300ms ease;
}

.expand-open .content-block {
  opacity: 1;
  transform: translateY(0);
}

/* AI insight particles */
.ai-particle {
  animation: particleFloat 3s ease-in-out infinite;
}

.ai-particle.p-1 { animation-delay: 0s; }
.ai-particle.p-2 { animation-delay: 1s; }
.ai-particle.p-3 { animation-delay: 2s; }

@keyframes particleFloat {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
  50% { transform: translateY(-6px) scale(1.5); opacity: 0.7; }
}

/* Focus visible */
.healing-card:focus-within {
  outline: none;
}
</style>
