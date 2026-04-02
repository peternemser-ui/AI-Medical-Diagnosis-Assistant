<template>
  <div class="body-diagram-input w-full max-w-xs mx-auto">
    <div class="text-center mb-3">
      <h3 class="text-body-sm font-semibold text-[var(--text-primary)]">Or tap where it hurts</h3>
      <p class="text-detail text-[var(--text-tertiary)] mt-0.5">Select one or more areas</p>
    </div>

    <!-- SVG Body with clickable zones -->
    <div class="relative mx-auto" style="width: 180px; height: 340px">
      <svg viewBox="0 0 180 340" class="w-full h-full" xmlns="http://www.w3.org/2000/svg">
        <!-- Body outline (silhouette) -->
        <g :class="isDark ? 'text-slate-700' : 'text-slate-200'" fill="currentColor" opacity="0.4">
          <!-- Head -->
          <ellipse cx="90" cy="32" rx="22" ry="26"/>
          <!-- Neck -->
          <rect x="82" y="56" width="16" height="14" rx="4"/>
          <!-- Torso -->
          <path d="M58 70 Q56 68 50 75 L42 110 L40 150 L44 185 Q48 195 60 195 L120 195 Q132 195 136 185 L140 150 L138 110 L130 75 Q124 68 122 70 Z"/>
          <!-- Left arm -->
          <path d="M42 78 Q32 80 28 95 L22 140 L18 180 Q16 188 22 190 L30 188 L36 150 L42 115 Z"/>
          <!-- Right arm -->
          <path d="M138 78 Q148 80 152 95 L158 140 L162 180 Q164 188 158 190 L150 188 L144 150 L138 115 Z"/>
          <!-- Left leg -->
          <path d="M60 195 L56 240 L52 285 L48 320 Q46 332 54 334 L66 332 L68 318 L72 280 L76 240 L80 195 Z"/>
          <!-- Right leg -->
          <path d="M120 195 L124 240 L128 285 L132 320 Q134 332 126 334 L114 332 L112 318 L108 280 L104 240 L100 195 Z"/>
        </g>

        <!-- Clickable zones (invisible hit areas with hover/selected states) -->
        <g v-for="zone in bodyZones" :key="zone.id">
          <component
            :is="zone.shape"
            v-bind="zone.attrs"
            class="body-zone cursor-pointer transition-all duration-200"
            :class="selectedZones.includes(zone.id) ? 'selected' : 'idle'"
            :style="{
              fill: selectedZones.includes(zone.id) ? zone.color + '35' : 'transparent',
              stroke: selectedZones.includes(zone.id) ? zone.color : (hoverZone === zone.id ? zone.color + '60' : 'transparent'),
              strokeWidth: selectedZones.includes(zone.id) ? 2 : 1.5,
            }"
            @click="toggleZone(zone.id)"
            @mouseenter="hoverZone = zone.id"
            @mouseleave="hoverZone = null"
          />
          <!-- Zone label (shown on hover or selected) -->
          <text
            v-if="hoverZone === zone.id || selectedZones.includes(zone.id)"
            :x="zone.labelX" :y="zone.labelY"
            text-anchor="middle"
            class="text-[8px] font-semibold pointer-events-none select-none"
            :style="{ fill: selectedZones.includes(zone.id) ? zone.color : (isDark ? '#94a3b8' : '#64748b') }">
            {{ zone.label }}
          </text>
        </g>
      </svg>
    </div>

    <!-- Selected zones summary + go button -->
    <Transition name="slide-up">
      <div v-if="selectedZones.length > 0" class="mt-3 flex items-center gap-2">
        <div class="flex-1 flex flex-wrap gap-1">
          <span v-for="zoneId in selectedZones" :key="zoneId"
            class="inline-flex items-center gap-1 px-2 py-0.5 rounded-pill text-micro font-medium cursor-pointer transition-colors"
            :style="{ background: getZone(zoneId).color + '15', color: getZone(zoneId).color }"
            @click="toggleZone(zoneId)">
            {{ getZone(zoneId).label }}
            <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
          </span>
        </div>
        <button @click="startWithSelectedZones"
          class="flex-shrink-0 px-3 py-1.5 rounded-btn text-detail font-semibold text-white bg-blue-600 hover:bg-blue-500 transition-colors">
          Go
          <svg class="w-3 h-3 inline ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()
const emit = defineEmits(['select'])

const selectedZones = ref([])
const hoverZone = ref(null)

const bodyZones = [
  { id: 'head',      shape: 'ellipse', attrs: { cx: 90, cy: 32, rx: 24, ry: 28 },              label: 'Head',      labelX: 90,  labelY: 12,  color: '#a855f7', symptom: 'head pain, headache, or dizziness' },
  { id: 'throat',    shape: 'rect',    attrs: { x: 78, y: 56, width: 24, height: 16, rx: 6 },   label: 'Throat',    labelX: 90,  labelY: 54,  color: '#f59e0b', symptom: 'sore throat, difficulty swallowing, or neck pain' },
  { id: 'chest',     shape: 'rect',    attrs: { x: 56, y: 74, width: 68, height: 50, rx: 10 },  label: 'Chest',     labelX: 90,  labelY: 100, color: '#ef4444', symptom: 'chest pain, tightness, or breathing difficulty' },
  { id: 'abdomen',   shape: 'rect',    attrs: { x: 52, y: 126, width: 76, height: 45, rx: 8 },  label: 'Abdomen',   labelX: 90,  labelY: 150, color: '#f97316', symptom: 'stomach pain, nausea, or digestive issues' },
  { id: 'pelvis',    shape: 'rect',    attrs: { x: 56, y: 173, width: 68, height: 24, rx: 8 },  label: 'Pelvis',    labelX: 90,  labelY: 188, color: '#ec4899', symptom: 'pelvic pain or discomfort' },
  { id: 'left_arm',  shape: 'rect',    attrs: { x: 16, y: 82, width: 24, height: 100, rx: 10 }, label: 'L. Arm',    labelX: 28,  labelY: 78,  color: '#3b82f6', symptom: 'left arm pain, numbness, or weakness' },
  { id: 'right_arm', shape: 'rect',    attrs: { x: 140, y: 82, width: 24, height: 100, rx: 10 },label: 'R. Arm',    labelX: 152, labelY: 78,  color: '#3b82f6', symptom: 'right arm pain, numbness, or weakness' },
  { id: 'left_leg',  shape: 'rect',    attrs: { x: 48, y: 198, width: 32, height: 110, rx: 10 },label: 'L. Leg',    labelX: 64,  labelY: 260, color: '#06b6d4', symptom: 'left leg pain, swelling, or mobility issues' },
  { id: 'right_leg', shape: 'rect',    attrs: { x: 100, y: 198, width: 32, height: 110, rx: 10 },label: 'R. Leg',   labelX: 116, labelY: 260, color: '#06b6d4', symptom: 'right leg pain, swelling, or mobility issues' },
  { id: 'skin',      shape: 'rect',    attrs: { x: 0, y: 310, width: 180, height: 28, rx: 8 },  label: 'Skin (anywhere)', labelX: 90, labelY: 327, color: '#f43f5e', symptom: 'skin rash, itching, discoloration, or unusual marks' },
]

function getZone(id) {
  return bodyZones.find(z => z.id === id) || bodyZones[0]
}

function toggleZone(id) {
  const idx = selectedZones.value.indexOf(id)
  if (idx >= 0) {
    selectedZones.value.splice(idx, 1)
  } else {
    selectedZones.value.push(id)
  }
}

function startWithSelectedZones() {
  const symptoms = selectedZones.value
    .map(id => getZone(id).symptom)
    .join('; ')
  const text = `I'm experiencing: ${symptoms}`
  emit('select', text)
  selectedZones.value = []
}
</script>

<style scoped>
.body-zone.idle:hover {
  fill: rgba(59, 130, 246, 0.08);
}
.slide-up-enter-active { transition: all 0.3s ease-out; }
.slide-up-enter-from { opacity: 0; transform: translateY(8px); }
.slide-up-leave-active { transition: all 0.2s ease-in; }
.slide-up-leave-to { opacity: 0; transform: translateY(4px); }
</style>
