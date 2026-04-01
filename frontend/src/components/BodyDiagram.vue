<template>
  <div class="rounded-xl overflow-hidden border transition-colors relative" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-md'">
    <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-pink-500 via-rose-500 to-red-500"></div>

    <!-- Header -->
    <div class="px-4 py-2.5 border-b flex items-center justify-between" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
      <div class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-pink-500 to-rose-500 flex items-center justify-center shadow-md shadow-pink-500/20">
          <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
        </div>
        <h2 class="text-xs font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Affected Areas</h2>
      </div>
      <span v-if="activeRegions.length > 0" class="text-detail font-semibold px-2 py-0.5 rounded-full" :class="isDark ? 'bg-pink-500/15 text-pink-400' : 'bg-pink-50 text-pink-600'">
        {{ activeRegions.length }}
      </span>
    </div>

    <div class="p-4">
      <!-- Affected areas list -->
      <div v-if="activeRegions.length > 0" class="space-y-2">
        <div
          v-for="region in activeRegions"
          :key="region.id"
          class="flex items-center gap-3 p-2.5 rounded-lg border transition-all"
          :class="isDark
            ? 'bg-slate-700/20 border-slate-700/30 hover:bg-slate-700/40'
            : 'bg-slate-50 border-slate-200 hover:bg-slate-100'"
        >
          <!-- Priority indicator bar -->
          <div class="w-1 h-8 rounded-full flex-shrink-0"
            :class="region.priority === 'primary' ? 'bg-red-500' : region.priority === 'secondary' ? 'bg-amber-500' : 'bg-blue-500'"></div>

          <!-- Icon -->
          <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
            :class="region.priority === 'primary'
              ? (isDark ? 'bg-red-500/15' : 'bg-red-50')
              : region.priority === 'secondary'
                ? (isDark ? 'bg-amber-500/15' : 'bg-amber-50')
                : (isDark ? 'bg-blue-500/15' : 'bg-blue-50')">
            <svg class="w-4 h-4"
              :class="region.priority === 'primary' ? 'text-red-400' : region.priority === 'secondary' ? 'text-amber-400' : 'text-blue-400'"
              fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="region.id === 'head'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              <path v-else-if="region.id === 'mouth'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/>
              <path v-else-if="region.id === 'eyes'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              <path v-else-if="region.id === 'throat'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"/>
              <path v-else-if="region.id === 'chest'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              <path v-else-if="region.id === 'lungs'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"/>
              <path v-else-if="region.id === 'abdomen'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
              <path v-else-if="region.id === 'skin_arm'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a6 6 0 00-6-6h-2"/>
              <path v-else-if="region.id === 'muscles'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              <path v-else-if="region.id === 'immune'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>

          <!-- Name + priority -->
          <div class="flex-1 min-w-0">
            <div class="text-xs font-semibold truncate" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ region.name }}</div>
          </div>

          <!-- Priority badge -->
          <span class="text-tiny font-bold uppercase tracking-wide px-2 py-0.5 rounded-full flex-shrink-0"
            :class="region.priority === 'primary'
              ? (isDark ? 'bg-red-500/15 text-red-400 ring-1 ring-red-500/20' : 'bg-red-50 text-red-600 ring-1 ring-red-200')
              : region.priority === 'secondary'
                ? (isDark ? 'bg-amber-500/15 text-amber-400 ring-1 ring-amber-500/20' : 'bg-amber-50 text-amber-600 ring-1 ring-amber-200')
                : (isDark ? 'bg-blue-500/15 text-blue-400 ring-1 ring-blue-500/20' : 'bg-blue-50 text-blue-600 ring-1 ring-blue-200')">
            {{ region.priority }}
          </span>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-6">
        <svg class="w-8 h-8 mx-auto mb-2" :class="isDark ? 'text-slate-600' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
        <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No affected areas detected</p>
      </div>

      <!-- Legend -->
      <div v-if="activeRegions.length > 0" class="flex items-center justify-center gap-5 mt-3 pt-3 border-t text-detail font-medium" :class="isDark ? 'border-slate-700/30 text-slate-500' : 'border-slate-200 text-slate-400'">
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-red-500 inline-block"></span>Primary</span>
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500 inline-block"></span>Secondary</span>
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-blue-500 inline-block"></span>Monitor</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  causes: { type: Array, default: () => [] },
  bodySystems: { type: Array, default: () => [] },
  recommendedTests: { type: Array, default: () => [] },
  redFlags: { type: Array, default: () => [] },
  gender: { type: String, default: '' },
  compact: { type: Boolean, default: false },
})

// Build full text for matching
const fullText = computed(() => {
  const causesText = props.causes.map(c =>
    ((c.cause || '') + ' ' + (c.explanation || '') + ' ' + (c.specialty || '')).toLowerCase()
  ).join(' ')
  const testsText = props.recommendedTests.join(' ').toLowerCase()
  const flagsText = props.redFlags.join(' ').toLowerCase()
  return causesText + ' ' + testsText + ' ' + flagsText
})

const regionDefs = {
  head: { name: 'Brain & Nervous System', keywords: ['brain', 'neuro', 'headache', 'migraine', 'dizzy', 'cognitive', 'mental', 'anxiety', 'depression', 'psychiatric', 'psych', 'seizure'] },
  mouth: { name: 'Mouth, Lips & Oral', keywords: ['lip', 'lips', 'oral', 'mouth', 'chapped', 'cheilitis', 'lichen planus', 'mucosa', 'tongue', 'gum', 'dental', 'stomatitis', 'canker', 'cold sore', 'angular'] },
  eyes: { name: 'Eyes & Vision', keywords: ['eye', 'vision', 'ophthalm', 'retina', 'glaucoma', 'cataract'] },
  throat: { name: 'Ear, Nose & Throat', keywords: ['ear', 'nose', 'throat', 'sinus', 'tonsil', 'ent', 'laryn', 'pharyn', 'vocal'] },
  chest: { name: 'Heart & Cardiovascular', keywords: ['heart', 'cardiac', 'cardio', 'chest pain', 'palpitation', 'cardiovascular', 'angina', 'coronary', 'hypertension', 'arrhythmia', 'ecg', 'troponin'] },
  lungs: { name: 'Lungs & Respiratory', keywords: ['lung', 'respiratory', 'breath', 'cough', 'pulmonary', 'asthma', 'bronch', 'pneumonia', 'copd'] },
  abdomen: { name: 'Digestive System', keywords: ['stomach', 'digest', 'gastro', 'bowel', 'abdominal', 'nausea', 'gi', 'reflux', 'gerd', 'ulcer', 'esophag', 'colon', 'intestin', 'pancrea', 'gallbladder', 'h. pylori', 'endoscop'] },
  liver: { name: 'Liver & Biliary', keywords: ['liver', 'hepat', 'biliary', 'gallbladder', 'cirrhosis', 'jaundice'] },
  kidneys: { name: 'Kidneys & Urinary', keywords: ['kidney', 'renal', 'urinary', 'bladder', 'urine', 'creatinine'] },
  skin_arm: { name: 'Skin & Integumentary', keywords: ['skin', 'dermat', 'rash', 'itch', 'eczema', 'psoriasis', 'atopic', 'chapped', 'lichen', 'hives', 'acne', 'wound', 'lesion', 'biopsy', 'lip', 'dry skin', 'flaking'] },
  muscles: { name: 'Muscles & Joints', keywords: ['muscle', 'joint', 'bone', 'musculoskeletal', 'back', 'arthritis', 'pain', 'costochondritis', 'fibromyalgia', 'sprain', 'fracture', 'ortho'] },
  endocrine: { name: 'Endocrine System', keywords: ['thyroid', 'diabetes', 'hormone', 'endocrine', 'adrenal', 'insulin', 'cortisol', 'pituitary'] },
  immune: { name: 'Immune System', keywords: ['immune', 'autoimmune', 'allergy', 'infection', 'virus', 'bacteria', 'fungal', 'inflammation', 'deficiency', 'vitamin', 'b12', 'anemia'] },
}

function getRegionPriority(regionId) {
  const def = regionDefs[regionId]
  if (!def) return null
  const text = fullText.value
  const matchCount = def.keywords.filter(kw => text.includes(kw)).length
  const topCause = props.causes[0]
  const topText = topCause ? ((topCause.cause || '') + ' ' + (topCause.specialty || '') + ' ' + (topCause.explanation || '')).toLowerCase() : ''
  const topMatch = def.keywords.some(kw => topText.includes(kw))
  if (topMatch && matchCount >= 2) return 'primary'
  if (matchCount >= 2 || topMatch) return 'secondary'
  if (matchCount >= 1) return 'monitor'
  return null
}

const activeRegions = computed(() => {
  const regions = []
  for (const [id, def] of Object.entries(regionDefs)) {
    const priority = getRegionPriority(id)
    if (!priority) continue
    regions.push({ id, name: def.name, priority })
  }
  const order = { primary: 0, secondary: 1, monitor: 2 }
  regions.sort((a, b) => order[a.priority] - order[b.priority])
  return regions
})
</script>
