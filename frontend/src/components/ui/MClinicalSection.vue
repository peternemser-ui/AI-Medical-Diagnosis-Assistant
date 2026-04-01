<template>
  <section class="rounded-card overflow-hidden border transition-colors relative" :class="sectionClass">
    <!-- Top accent line -->
    <div v-if="accent" class="absolute top-0 left-0 right-0 h-0.5" :class="accentGradients[accent]"></div>

    <!-- Header -->
    <div v-if="title" class="px-5 py-3 border-b flex items-center gap-2.5"
      :class="isDark ? 'border-slate-700/30' : 'border-slate-200'"
      :role="collapsible ? 'button' : undefined"
      :tabindex="collapsible ? 0 : undefined"
      @click="collapsible && toggle()"
      @keydown.enter="collapsible && toggle()">
      <div v-if="icon" class="w-7 h-7 rounded-btn flex items-center justify-center shadow-sm"
        :class="iconGradients[iconColor] || iconGradients.blue">
        <slot name="icon">
          <span class="text-sm">{{ icon }}</span>
        </slot>
      </div>
      <div class="flex-1 min-w-0">
        <h2 class="text-body-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ title }}</h2>
        <p v-if="subtitle" class="text-detail mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ subtitle }}</p>
      </div>
      <slot name="header-right" />
      <span v-if="count !== null" class="text-detail font-semibold px-2 py-0.5 rounded-pill"
        :class="countBadgeClasses[iconColor] || countBadgeClasses.blue">{{ count }}</span>
      <svg v-if="collapsible" class="w-4 h-4 transition-transform flex-shrink-0"
        :class="[expanded ? 'rotate-180' : '', isDark ? 'text-slate-400' : 'text-slate-500']"
        fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
      </svg>
    </div>

    <!-- Body -->
    <div v-if="!collapsible || expanded" :class="noPadding ? '' : 'p-4'">
      <slot />
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  title: String,
  subtitle: String,
  icon: String,
  iconColor: { type: String, default: 'blue' },
  accent: String, // 'blue', 'cyan', 'amber', 'red', 'emerald', 'purple'
  count: { type: [Number, String], default: null },
  collapsible: Boolean,
  defaultExpanded: { type: Boolean, default: true },
  noPadding: Boolean,
})

const expanded = ref(props.defaultExpanded)
function toggle() { expanded.value = !expanded.value }

const sectionClass = computed(() =>
  isDark.value
    ? 'bg-slate-800/60 border-slate-700/50'
    : 'bg-white border-slate-200 shadow-card'
)

const accentGradients = {
  blue:    'bg-gradient-to-r from-blue-500 to-indigo-500',
  cyan:    'bg-gradient-to-r from-cyan-500 to-blue-500',
  amber:   'bg-gradient-to-r from-amber-500 to-orange-500',
  red:     'bg-gradient-to-r from-red-500 to-pink-500',
  emerald: 'bg-gradient-to-r from-emerald-500 to-teal-500',
  purple:  'bg-gradient-to-r from-violet-500 to-purple-500',
  brand:   'bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500',
}

const iconGradients = {
  blue:    'bg-gradient-to-br from-blue-500 to-indigo-500 shadow-blue-500/20',
  cyan:    'bg-gradient-to-br from-cyan-500 to-blue-500 shadow-cyan-500/20',
  amber:   'bg-gradient-to-br from-amber-500 to-orange-500 shadow-amber-500/20',
  red:     'bg-gradient-to-br from-red-500 to-pink-500 shadow-red-500/20',
  emerald: 'bg-gradient-to-br from-emerald-500 to-teal-500 shadow-emerald-500/20',
  purple:  'bg-gradient-to-br from-violet-500 to-purple-500 shadow-violet-500/20',
  indigo:  'bg-gradient-to-br from-indigo-500 to-blue-500 shadow-indigo-500/20',
}

const countBadgeClasses = {
  blue:    'bg-blue-500/15 text-blue-300',
  cyan:    'bg-cyan-500/15 text-cyan-300',
  amber:   'bg-amber-500/15 text-amber-300',
  red:     'bg-red-500/15 text-red-300',
  emerald: 'bg-emerald-500/15 text-emerald-300',
  purple:  'bg-purple-500/15 text-purple-300',
  indigo:  'bg-indigo-500/15 text-indigo-300',
}
</script>
