<template>
  <div class="natural-healing-section relative rounded-2xl overflow-hidden" :style="containerStyle">
    <!-- Ambient background (dark only) -->
    <div v-if="isDark" class="absolute inset-0 pointer-events-none overflow-hidden">
      <!-- Faint gradient blobs -->
      <div class="absolute w-[350px] h-[350px] -top-[120px] -left-[100px] rounded-full blur-[120px] opacity-[0.04]"
        style="background: radial-gradient(circle, #ef4444, transparent)"></div>
      <div class="absolute w-[300px] h-[300px] top-1/3 -right-[80px] rounded-full blur-[100px] opacity-[0.03]"
        style="background: radial-gradient(circle, #f59e0b, transparent)"></div>
      <div class="absolute w-[250px] h-[250px] -bottom-[80px] left-1/3 rounded-full blur-[100px] opacity-[0.04]"
        style="background: radial-gradient(circle, #22c55e, transparent)"></div>

      <!-- Subtle neural lines -->
      <svg class="absolute inset-0 w-full h-full opacity-[0.03]" xmlns="http://www.w3.org/2000/svg">
        <line x1="5%" y1="30%" x2="95%" y2="70%" stroke="#f59e0b" stroke-width="0.3" stroke-dasharray="6 3" class="neural-drift n1" />
        <line x1="10%" y1="80%" x2="90%" y2="20%" stroke="#22c55e" stroke-width="0.3" stroke-dasharray="6 3" class="neural-drift n2" />
        <line x1="50%" y1="5%" x2="50%" y2="95%" stroke="#ef4444" stroke-width="0.2" stroke-dasharray="4 4" class="neural-drift n3" />
      </svg>
    </div>

    <!-- Top summary bar -->
    <div class="relative z-10 px-6 pt-6 pb-4">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <div class="flex items-center gap-3 mb-1.5">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-500/60 to-emerald-500/40 flex items-center justify-center shadow-lg shadow-amber-500/10 border border-white/10">
              <span class="text-base">&#127807;</span>
            </div>
            <h2 class="text-sm font-bold uppercase tracking-wider" :class="isDark ? 'text-white' : 'text-slate-800'">Natural & Holistic Healing Options</h2>
          </div>
          <p class="text-caption ml-12" :class="isDark ? 'text-white/35' : 'text-slate-500'">Evidence-informed complementary approaches tailored to your condition</p>
        </div>

        <!-- Dynamic badges -->
        <div class="flex items-center gap-2 ml-12 sm:ml-0 flex-wrap">
          <span class="badge-pill" style="--badge-color: #22c55e">
            <span class="w-1.5 h-1.5 rounded-full inline-block" style="background: #22c55e; box-shadow: 0 0 4px #22c55e60"></span>
            Low Risk
          </span>
          <span class="badge-pill" style="--badge-color: #f59e0b">
            <span class="w-1.5 h-1.5 rounded-full inline-block" style="background: #f59e0b; box-shadow: 0 0 4px #f59e0b60"></span>
            Moderate Evidence
          </span>
          <span class="badge-pill" style="--badge-color: #3b82f6">
            <span class="w-1.5 h-1.5 rounded-full inline-block" style="background: #3b82f6; box-shadow: 0 0 4px #3b82f660"></span>
            Adjunct Therapy
          </span>
        </div>
      </div>
    </div>

    <!-- Divider -->
    <div class="relative z-10 mx-6 h-px" :class="isDark ? 'bg-gradient-to-r from-transparent via-white/10 to-transparent' : 'bg-slate-200'"></div>

    <!-- Cards -->
    <div class="relative z-10 p-6 space-y-4">
      <!-- TCM Card -->
      <HealingExpandableCard
        card-id="tcm"
        title="Traditional Chinese Medicine"
        subtitle="Acupuncture, herbal formulas, and energy-based healing"
        icon="&#127982;"
        accent-color="#ef4444"
        :sections="tcmSections"
        why-it-works="Traditional Chinese Medicine views the body as an interconnected system of energy meridians. By targeting specific acupuncture points and using herbal formulas, TCM aims to restore the natural flow of Qi, addressing root imbalances rather than just symptoms."
        :ai-insight="tcmInsight"
        :is-dark="isDark"
      />

      <!-- Ayurvedic Card -->
      <HealingExpandableCard
        card-id="ayurveda"
        title="Ayurvedic Medicine"
        subtitle="Ancient Indian healing through herbs, diet, and daily practices"
        icon="&#129463;"
        accent-color="#f59e0b"
        :sections="ayurvedaSections"
        why-it-works="Ayurveda identifies three fundamental bio-energies (doshas) governing bodily functions. Treatments are personalized to your constitutional type, using herbs, dietary adjustments, and lifestyle practices to restore doshic balance and promote self-healing."
        :ai-insight="ayurvedaInsight"
        :is-dark="isDark"
      />

      <!-- Naturopathic Card -->
      <HealingExpandableCard
        card-id="naturopathic"
        title="Naturopathic & Holistic"
        subtitle="Evidence-based supplements, mind-body therapies, and bodywork"
        icon="&#127807;"
        accent-color="#22c55e"
        :sections="naturopathicSections"
        why-it-works="Naturopathic medicine combines evidence-based nutritional supplementation with mind-body therapies. These approaches support the body's innate healing capacity by reducing inflammation, optimizing nutrient levels, and regulating the nervous system."
        :ai-insight="naturopathicInsight"
        :is-dark="isDark"
      />
    </div>

    <!-- Collapsible disclaimer footer -->
    <div class="relative z-10 px-6 pb-4">
      <button
        @click="disclaimerOpen = !disclaimerOpen"
        class="flex items-center gap-2 text-detail transition-colors py-1.5 outline-none"
        :class="isDark ? 'text-white/25 hover:text-white/40 focus:text-white/40' : 'text-slate-400 hover:text-slate-600 focus:text-slate-600'"
        :aria-expanded="disclaimerOpen"
        aria-controls="healing-disclaimer"
      >
        <svg class="w-3 h-3 transition-transform duration-200" :class="disclaimerOpen ? 'rotate-90' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        Important Disclaimer
      </button>
      <div
        id="healing-disclaimer"
        class="disclaimer-expand"
        :class="disclaimerOpen ? 'disclaimer-open' : 'disclaimer-closed'"
      >
        <div class="rounded-xl px-4 py-3 mt-2 border" style="background: rgba(245,158,11,0.04); border-color: rgba(245,158,11,0.12)">
          <p class="text-detail leading-relaxed text-amber-400/50">
            <span class="font-bold text-amber-400/70">Disclaimer:</span> Alternative and holistic treatments are presented for informational purposes only. They are not a substitute for conventional medical care. Always consult your primary healthcare provider before starting any alternative therapy, especially if you are taking medications, as interactions may occur. Evidence levels vary across these modalities.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import HealingExpandableCard from './HealingExpandableCard.vue'

const { isDark } = useTheme()

const props = defineProps({
  tcmRecommendations: { type: Array, default: () => [] },
  ayurvedicRecommendations: { type: Array, default: () => [] },
  holisticRecommendations: { type: Array, default: () => [] },
})

const disclaimerOpen = ref(false)

const containerStyle = computed(() =>
  isDark.value
    ? { background: 'linear-gradient(145deg, #0a0f1c 0%, #070b16 50%, #05070d 100%)', border: '1px solid rgba(255,255,255,0.06)' }
    : { background: '#ffffff', border: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.06)' }
)

// Evidence levels per category
const evidenceMap = {
  'Acupuncture Points': 4,
  'Herbal Formulas': 3,
  'Movement Therapy': 4,
  'Herbal Remedies': 3,
  'Dietary Principles': 3,
  'Daily Practices (Dinacharya)': 2,
  'Supplements & Herbs': 4,
  'Mind-Body Therapies': 4,
  'Bodywork & Energy': 3,
}

function addEvidence(sections) {
  return sections.map(s => ({
    ...s,
    evidence: evidenceMap[s.category] || 2,
  }))
}

const tcmSections = computed(() => addEvidence(props.tcmRecommendations))
const ayurvedaSections = computed(() => addEvidence(props.ayurvedicRecommendations))
const naturopathicSections = computed(() => addEvidence(props.holisticRecommendations))

// Dynamic AI insights based on content
const tcmInsight = computed(() => {
  const hasAcu = props.tcmRecommendations.some(s => s.category === 'Acupuncture Points')
  const hasHerbs = props.tcmRecommendations.some(s => s.category === 'Herbal Formulas')
  if (hasAcu && hasHerbs) {
    return 'Combining acupuncture with herbal formulas may provide synergistic benefits. Acupuncture addresses acute symptoms through meridian stimulation, while herbal support offers sustained therapeutic effects over time.'
  }
  return 'These TCM approaches target the underlying constitutional imbalance associated with your condition, potentially reducing reliance on symptomatic treatments when used as complementary therapy.'
})

const ayurvedaInsight = computed(() => {
  const hasDiet = props.ayurvedicRecommendations.some(s => s.category === 'Dietary Principles')
  if (hasDiet) {
    return 'Ayurvedic dietary modifications work by reducing aggravating factors specific to your condition type. When combined with herbal support and daily practices, this comprehensive approach may help address both symptoms and underlying imbalances.'
  }
  return 'These Ayurvedic recommendations are tailored to address the doshic imbalance most likely associated with your symptoms, supporting the body\'s natural healing processes through a multi-modal approach.'
})

const naturopathicInsight = computed(() => {
  const hasSupps = props.holisticRecommendations.some(s => s.category === 'Supplements & Herbs')
  const hasMindBody = props.holisticRecommendations.some(s => s.category === 'Mind-Body Therapies')
  if (hasSupps && hasMindBody) {
    return 'The recommended supplements target specific biochemical pathways involved in your condition, while mind-body therapies address the neurological and stress-related components. This dual approach may enhance outcomes when combined with conventional care.'
  }
  return 'These evidence-based naturopathic approaches complement conventional treatment by supporting immune function, reducing inflammation, and optimizing the body\'s healing capacity through nutritional and lifestyle interventions.'
})
</script>

<style scoped>
.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.05em;
  padding: 4px 10px;
  border-radius: 9999px;
  background: color-mix(in srgb, var(--badge-color) 8%, transparent);
  border: 1px solid color-mix(in srgb, var(--badge-color) 15%, transparent);
  color: color-mix(in srgb, var(--badge-color) 80%, white);
}

/* Neural line drift */
.neural-drift {
  stroke-dashoffset: 0;
  animation: drift 12s linear infinite;
}
.n1 { animation-delay: 0s; }
.n2 { animation-delay: -4s; }
.n3 { animation-delay: -8s; }

@keyframes drift {
  0% { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -36; }
}

/* Disclaimer expand */
.disclaimer-expand {
  display: grid;
  transition: grid-template-rows 300ms ease, opacity 200ms ease;
}
.disclaimer-closed {
  grid-template-rows: 0fr;
  opacity: 0;
}
.disclaimer-open {
  grid-template-rows: 1fr;
  opacity: 1;
}
.disclaimer-expand > div {
  overflow: hidden;
}
</style>
