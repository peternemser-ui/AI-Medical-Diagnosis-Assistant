<template>
  <div class="medical-illustration" :class="containerClass">
    <svg
      :width="size"
      :height="size"
      viewBox="0 0 200 200"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <!-- Background glow -->
      <defs>
        <radialGradient id="ill-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" :stop-color="accentColor" stop-opacity="0.08" />
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0" />
        </radialGradient>
      </defs>
      <circle cx="100" cy="100" r="95" fill="url(#ill-glow)" />

      <!-- Illustration paths -->
      <g :stroke="strokeColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
         v-html="illustrationSvg" />
    </svg>
    <div v-if="label" class="mt-2 text-center">
      <span class="text-detail font-semibold uppercase tracking-widest"
        :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ label }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  condition: { type: String, default: '' },
  specialty: { type: String, default: '' },
  size: { type: [Number, String], default: 180 },
})

const accentColor = computed(() => isDark.value ? '#60a5fa' : '#3b82f6')
const strokeColor = computed(() => isDark.value ? '#94a3b8' : '#64748b')

const containerClass = computed(() =>
  isDark.value ? 'opacity-70 hover:opacity-90 transition-opacity' : 'opacity-60 hover:opacity-80 transition-opacity'
)

// Map condition/specialty text to illustration key
const illustrationKey = computed(() => {
  const text = ((props.condition || '') + ' ' + (props.specialty || '')).toLowerCase()

  const mappings = [
    { keys: ['gerd', 'reflux', 'esophag', 'gastroesophageal'], icon: 'esophagus' },
    { keys: ['stomach', 'gastritis', 'peptic', 'ulcer', 'gastro', 'dyspepsia'], icon: 'stomach' },
    { keys: ['heart', 'cardiac', 'cardio', 'coronary', 'angina', 'pectoris', 'myocard'], icon: 'heart' },
    { keys: ['costochondritis', 'chest wall', 'sternum', 'rib'], icon: 'ribcage' },
    { keys: ['lung', 'pulmonary', 'pneumonia', 'bronch', 'asthma', 'respiratory', 'copd'], icon: 'lungs' },
    { keys: ['anxiety', 'depression', 'mental', 'psychiatric', 'psych', 'panic', 'phq'], icon: 'brain' },
    { keys: ['head', 'migraine', 'headache', 'cephalgia'], icon: 'head' },
    { keys: ['liver', 'hepat', 'biliary', 'gallbladder', 'cirrhosis'], icon: 'liver' },
    { keys: ['kidney', 'renal', 'nephro'], icon: 'kidney' },
    { keys: ['skin', 'dermat', 'rash', 'eczema', 'psoriasis'], icon: 'skin' },
    { keys: ['thyroid', 'endocrine', 'hormone'], icon: 'thyroid' },
    { keys: ['spine', 'back', 'spinal', 'vertebr', 'disc', 'lumbar', 'cervical'], icon: 'spine' },
    { keys: ['joint', 'arthritis', 'musculoskeletal', 'osteo'], icon: 'joint' },
    { keys: ['bone', 'fracture', 'orthop'], icon: 'bone' },
    { keys: ['eye', 'vision', 'ophthalm', 'retina', 'glaucoma'], icon: 'eye' },
    { keys: ['ear', 'hearing', 'tinnitus', 'otitis'], icon: 'ear' },
    { keys: ['bladder', 'urinary', 'urin', 'cystitis'], icon: 'bladder' },
    { keys: ['intestin', 'bowel', 'colon', 'ibs', 'crohn', 'colitis', 'digest'], icon: 'intestine' },
    { keys: ['throat', 'laryn', 'pharyn', 'tonsil'], icon: 'throat' },
    { keys: ['diabetes', 'pancrea', 'insulin'], icon: 'pancreas' },
    { keys: ['immune', 'autoimmune', 'allergy'], icon: 'immune' },
  ]

  for (const mapping of mappings) {
    if (mapping.keys.some(k => text.includes(k))) {
      return mapping.icon
    }
  }
  return 'body'
})

const label = computed(() => {
  const labels = {
    esophagus: 'Esophagus & Stomach',
    stomach: 'Stomach',
    heart: 'Cardiovascular',
    ribcage: 'Chest Wall',
    lungs: 'Respiratory System',
    brain: 'Neurological',
    head: 'Cranial',
    liver: 'Hepatic System',
    kidney: 'Renal System',
    skin: 'Integumentary',
    thyroid: 'Endocrine',
    spine: 'Spinal Column',
    joint: 'Musculoskeletal',
    bone: 'Skeletal System',
    eye: 'Ophthalmic',
    ear: 'Auditory',
    bladder: 'Urinary System',
    intestine: 'Gastrointestinal',
    throat: 'Upper Airway',
    pancreas: 'Pancreatic',
    immune: 'Immune System',
    body: 'Anatomical Reference',
  }
  return labels[illustrationKey.value] || 'Anatomical Reference'
})

// Detailed medical SVG illustrations (200x200 viewBox)
const illustrations = {
  esophagus: `
    <!-- Esophagus tube -->
    <path d="M88 25 C88 25 85 50 82 75 C80 90 78 110 80 125" stroke-width="2" opacity="0.8"/>
    <path d="M112 25 C112 25 115 50 118 75 C120 90 122 110 120 125" stroke-width="2" opacity="0.8"/>
    <!-- Esophageal lining -->
    <path d="M90 35 C95 38 105 38 110 35" opacity="0.3"/>
    <path d="M88 55 C94 58 106 58 112 55" opacity="0.3"/>
    <path d="M86 75 C93 78 107 78 114 75" opacity="0.3"/>
    <!-- Lower esophageal sphincter -->
    <ellipse cx="100" cy="120" rx="22" ry="8" stroke-width="2" opacity="0.6"/>
    <!-- Stomach -->
    <path d="M78 125 C60 130 48 150 50 170 C52 185 70 195 90 192 C100 190 110 185 115 175 C125 155 128 140 122 125" stroke-width="2"/>
    <!-- Stomach rugae -->
    <path d="M65 150 C75 148 85 152 90 155" opacity="0.25"/>
    <path d="M60 165 C72 162 82 166 88 170" opacity="0.25"/>
    <!-- Acid reflux arrows -->
    <path d="M95 110 L95 90" stroke-width="1.5" opacity="0.5" stroke-dasharray="4 3"/>
    <path d="M95 90 L91 96 M95 90 L99 96" stroke-width="1.5" opacity="0.5"/>
    <path d="M105 105 L105 85" stroke-width="1.5" opacity="0.5" stroke-dasharray="4 3"/>
    <path d="M105 85 L101 91 M105 85 L109 91" stroke-width="1.5" opacity="0.5"/>
    <!-- Irritation markers -->
    <circle cx="90" cy="70" r="2" fill="currentColor" opacity="0.15" stroke="none"/>
    <circle cx="108" cy="65" r="2" fill="currentColor" opacity="0.15" stroke="none"/>
    <circle cx="94" cy="50" r="1.5" fill="currentColor" opacity="0.12" stroke="none"/>
    <!-- Diaphragm line -->
    <path d="M40 122 C60 115 80 118 100 120 C120 122 140 115 160 122" stroke-width="1" opacity="0.2" stroke-dasharray="6 4"/>
  `,

  stomach: `
    <!-- Esophagus entry -->
    <path d="M90 20 L85 60" stroke-width="2" opacity="0.6"/>
    <path d="M110 20 L108 60" stroke-width="2" opacity="0.6"/>
    <!-- Stomach body -->
    <path d="M82 60 C55 70 40 100 42 135 C44 165 70 185 100 182 C120 180 138 165 140 140 C145 110 135 80 112 60" stroke-width="2"/>
    <!-- Greater curvature detail -->
    <path d="M55 90 C58 110 60 130 65 148" opacity="0.3"/>
    <!-- Rugae folds -->
    <path d="M65 95 C80 92 95 97 105 100" opacity="0.25"/>
    <path d="M58 115 C75 112 90 117 102 120" opacity="0.25"/>
    <path d="M55 135 C72 132 88 137 98 140" opacity="0.25"/>
    <!-- Pylorus -->
    <ellipse cx="115" cy="165" rx="12" ry="6" opacity="0.5"/>
    <!-- Gastric glands -->
    <circle cx="75" cy="105" r="2.5" fill="currentColor" opacity="0.1" stroke="none"/>
    <circle cx="90" cy="125" r="2.5" fill="currentColor" opacity="0.1" stroke="none"/>
    <circle cx="72" cy="145" r="2" fill="currentColor" opacity="0.1" stroke="none"/>
  `,

  heart: `
    <!-- Aorta -->
    <path d="M100 45 C100 30 115 20 130 25 C145 30 145 45 140 60" stroke-width="2" opacity="0.7"/>
    <path d="M100 45 C100 30 85 20 70 25 C55 30 55 45 60 60" stroke-width="2" opacity="0.7"/>
    <!-- Heart body -->
    <path d="M60 60 C45 70 35 95 40 120 C45 145 65 170 100 185 C135 170 155 145 160 120 C165 95 155 70 140 60" stroke-width="2"/>
    <!-- Septum -->
    <path d="M100 55 L100 170" opacity="0.2" stroke-dasharray="4 4"/>
    <!-- Chambers -->
    <path d="M70 80 C75 90 85 95 95 90" opacity="0.3"/>
    <path d="M105 90 C115 95 125 90 130 80" opacity="0.3"/>
    <path d="M65 115 C75 125 90 128 95 120" opacity="0.3"/>
    <path d="M105 120 C110 128 125 125 135 115" opacity="0.3"/>
    <!-- Valves -->
    <ellipse cx="85" cy="100" rx="8" ry="3" opacity="0.4" transform="rotate(-10 85 100)"/>
    <ellipse cx="115" cy="100" rx="8" ry="3" opacity="0.4" transform="rotate(10 115 100)"/>
    <!-- Coronary arteries -->
    <path d="M75 70 C68 85 65 100 68 120" stroke-width="1" opacity="0.35"/>
    <path d="M125 70 C132 85 135 100 132 120" stroke-width="1" opacity="0.35"/>
    <!-- Heartbeat line -->
    <path d="M25 150 L55 150 L65 130 L75 165 L85 140 L90 150 L175 150" stroke-width="1.5" opacity="0.25"/>
  `,

  ribcage: `
    <!-- Sternum -->
    <path d="M100 25 L100 130" stroke-width="2.5"/>
    <!-- Ribs - left -->
    <path d="M100 40 C85 38 65 45 50 60" stroke-width="1.5" opacity="0.7"/>
    <path d="M100 52 C83 50 60 58 45 75" stroke-width="1.5" opacity="0.7"/>
    <path d="M100 64 C82 62 58 72 42 90" stroke-width="1.5" opacity="0.65"/>
    <path d="M100 76 C82 75 58 85 45 105" stroke-width="1.5" opacity="0.6"/>
    <path d="M100 88 C84 87 62 96 50 115" stroke-width="1.5" opacity="0.55"/>
    <path d="M100 100 C86 99 68 106 58 120" stroke-width="1.5" opacity="0.5"/>
    <path d="M100 112 C90 111 78 115 70 125" stroke-width="1.5" opacity="0.45"/>
    <!-- Ribs - right -->
    <path d="M100 40 C115 38 135 45 150 60" stroke-width="1.5" opacity="0.7"/>
    <path d="M100 52 C117 50 140 58 155 75" stroke-width="1.5" opacity="0.7"/>
    <path d="M100 64 C118 62 142 72 158 90" stroke-width="1.5" opacity="0.65"/>
    <path d="M100 76 C118 75 142 85 155 105" stroke-width="1.5" opacity="0.6"/>
    <path d="M100 88 C116 87 138 96 150 115" stroke-width="1.5" opacity="0.55"/>
    <path d="M100 100 C114 99 132 106 142 120" stroke-width="1.5" opacity="0.5"/>
    <path d="M100 112 C110 111 122 115 130 125" stroke-width="1.5" opacity="0.45"/>
    <!-- Costal cartilage highlight (costochondritis area) -->
    <circle cx="88" cy="55" r="6" fill="currentColor" opacity="0.08" stroke="none"/>
    <circle cx="112" cy="55" r="6" fill="currentColor" opacity="0.08" stroke="none"/>
    <!-- Inflammation marker -->
    <circle cx="88" cy="55" r="10" stroke-width="1" opacity="0.3" stroke-dasharray="3 3"/>
    <circle cx="112" cy="55" r="10" stroke-width="1" opacity="0.3" stroke-dasharray="3 3"/>
    <!-- Spine hint -->
    <path d="M100 130 L100 180" stroke-width="2" opacity="0.3"/>
    <path d="M94 145 L106 145" opacity="0.2"/>
    <path d="M94 160 L106 160" opacity="0.2"/>
  `,

  lungs: `
    <!-- Trachea -->
    <path d="M95 18 L95 55" stroke-width="2"/>
    <path d="M105 18 L105 55" stroke-width="2"/>
    <!-- Tracheal rings -->
    <path d="M95 28 L105 28" opacity="0.3"/>
    <path d="M95 36 L105 36" opacity="0.3"/>
    <path d="M95 44 L105 44" opacity="0.3"/>
    <!-- Bronchi -->
    <path d="M95 55 C85 60 70 65 60 75" stroke-width="1.8"/>
    <path d="M105 55 C115 60 130 65 140 75" stroke-width="1.8"/>
    <!-- Left lung -->
    <path d="M45 65 C30 75 20 100 22 130 C24 160 40 180 65 182 C80 183 90 175 95 160 L95 55 C85 58 60 62 45 65z" stroke-width="2"/>
    <!-- Right lung -->
    <path d="M155 65 C170 75 180 100 178 130 C176 160 160 180 135 182 C120 183 110 175 105 160 L105 55 C115 58 140 62 155 65z" stroke-width="2"/>
    <!-- Bronchial tree - left -->
    <path d="M60 75 C55 85 45 95 40 110" opacity="0.3"/>
    <path d="M60 75 C58 88 55 100 58 115" opacity="0.3"/>
    <path d="M70 70 C65 82 58 92 52 100" opacity="0.25"/>
    <!-- Bronchial tree - right -->
    <path d="M140 75 C145 85 155 95 160 110" opacity="0.3"/>
    <path d="M140 75 C142 88 145 100 142 115" opacity="0.3"/>
    <path d="M130 70 C135 82 142 92 148 100" opacity="0.25"/>
    <!-- Alveoli hints -->
    <circle cx="42" cy="130" r="4" opacity="0.12" fill="currentColor" stroke="none"/>
    <circle cx="55" cy="145" r="4" opacity="0.12" fill="currentColor" stroke="none"/>
    <circle cx="158" cy="130" r="4" opacity="0.12" fill="currentColor" stroke="none"/>
    <circle cx="145" cy="145" r="4" opacity="0.12" fill="currentColor" stroke="none"/>
  `,

  brain: `
    <!-- Brain outline -->
    <path d="M100 30 C60 30 35 55 35 90 C35 115 45 135 65 148 L72 155 L72 170 L128 170 L128 155 L135 148 C155 135 165 115 165 90 C165 55 140 30 100 30z" stroke-width="2"/>
    <!-- Hemisphere divide -->
    <path d="M100 32 L100 165" opacity="0.15" stroke-dasharray="4 4"/>
    <!-- Left hemisphere gyri -->
    <path d="M55 60 C65 55 80 58 90 65" opacity="0.35"/>
    <path d="M45 80 C58 75 72 78 88 85" opacity="0.35"/>
    <path d="M42 100 C56 95 70 98 90 105" opacity="0.3"/>
    <path d="M48 118 C60 114 74 117 88 122" opacity="0.25"/>
    <!-- Right hemisphere gyri -->
    <path d="M145 60 C135 55 120 58 110 65" opacity="0.35"/>
    <path d="M155 80 C142 75 128 78 112 85" opacity="0.35"/>
    <path d="M158 100 C144 95 130 98 110 105" opacity="0.3"/>
    <path d="M152 118 C140 114 126 117 112 122" opacity="0.25"/>
    <!-- Cerebellum -->
    <path d="M75 148 C80 155 90 158 100 158 C110 158 120 155 125 148" opacity="0.4"/>
    <path d="M80 152 C88 158 112 158 120 152" opacity="0.25"/>
    <!-- Brain stem -->
    <path d="M92 158 C92 162 95 168 100 170 C105 168 108 162 108 158" opacity="0.5"/>
    <!-- Neural activity nodes -->
    <circle cx="70" cy="70" r="4" fill="currentColor" opacity="0.1" stroke="none"/>
    <circle cx="130" cy="70" r="4" fill="currentColor" opacity="0.1" stroke="none"/>
    <circle cx="80" cy="100" r="3.5" fill="currentColor" opacity="0.08" stroke="none"/>
    <circle cx="120" cy="100" r="3.5" fill="currentColor" opacity="0.08" stroke="none"/>
    <!-- Neural connections -->
    <path d="M70 70 L80 100" opacity="0.12"/>
    <path d="M130 70 L120 100" opacity="0.12"/>
    <path d="M80 100 L100 90 L120 100" opacity="0.1"/>
  `,

  liver: `
    <!-- Liver body -->
    <path d="M35 80 C30 70 40 50 70 45 C100 40 150 45 170 60 C180 68 178 85 170 100 C155 130 120 150 90 155 C65 158 45 145 38 125 C32 110 32 95 35 80z" stroke-width="2"/>
    <!-- Falciform ligament -->
    <path d="M105 45 L100 100" stroke-width="1.5" opacity="0.4"/>
    <!-- Hepatic lobes division -->
    <path d="M100 50 C98 70 95 90 90 110 C85 130 82 145 85 155" opacity="0.25"/>
    <!-- Portal vein -->
    <path d="M100 100 C90 105 80 115 75 130" stroke-width="1.5" opacity="0.35"/>
    <path d="M100 100 C110 108 120 115 130 118" stroke-width="1.5" opacity="0.35"/>
    <!-- Hepatic veins -->
    <path d="M100 70 L85 55" opacity="0.25"/>
    <path d="M100 70 L120 55" opacity="0.25"/>
    <!-- Gallbladder -->
    <path d="M110 130 C115 135 118 145 115 155 C112 162 108 162 105 155 C102 145 105 135 110 130z" stroke-width="1.5" opacity="0.6"/>
    <!-- Surface texture -->
    <circle cx="65" cy="80" r="3" fill="currentColor" opacity="0.06" stroke="none"/>
    <circle cx="130" cy="75" r="3" fill="currentColor" opacity="0.06" stroke="none"/>
    <circle cx="80" cy="110" r="3" fill="currentColor" opacity="0.06" stroke="none"/>
  `,

  kidney: `
    <!-- Left kidney -->
    <path d="M70 55 C50 60 35 80 35 105 C35 135 50 160 70 165 C82 168 90 158 90 145 L90 120 C90 112 85 108 80 108 C75 108 70 112 70 120 L70 130 C70 138 65 142 60 140 C50 136 42 120 42 105 C42 85 52 68 70 55z" stroke-width="2"/>
    <!-- Right kidney -->
    <path d="M130 55 C150 60 165 80 165 105 C165 135 150 160 130 165 C118 168 110 158 110 145 L110 120 C110 112 115 108 120 108 C125 108 130 112 130 120 L130 130 C130 138 135 142 140 140 C150 136 158 120 158 105 C158 85 148 68 130 55z" stroke-width="2"/>
    <!-- Ureters -->
    <path d="M75 160 C78 175 85 185 95 190" stroke-width="1.5" opacity="0.5"/>
    <path d="M125 160 C122 175 115 185 105 190" stroke-width="1.5" opacity="0.5"/>
    <!-- Renal arteries -->
    <path d="M100 95 L78 100" stroke-width="1.5" opacity="0.4"/>
    <path d="M100 95 L122 100" stroke-width="1.5" opacity="0.4"/>
    <!-- Aorta hint -->
    <path d="M100 50 L100 140" stroke-width="1.5" opacity="0.2"/>
    <!-- Cortex/medulla zones -->
    <circle cx="62" cy="105" r="12" fill="currentColor" opacity="0.06" stroke="none"/>
    <circle cx="138" cy="105" r="12" fill="currentColor" opacity="0.06" stroke="none"/>
  `,

  spine: `
    <!-- Vertebral column -->
    <path d="M100 15 L100 185" stroke-width="2.5" opacity="0.4"/>
    <!-- Cervical vertebrae -->
    <rect x="88" y="20" width="24" height="10" rx="4" opacity="0.6"/>
    <rect x="86" y="34" width="28" height="10" rx="4" opacity="0.6"/>
    <rect x="85" y="48" width="30" height="10" rx="4" opacity="0.55"/>
    <!-- Thoracic vertebrae -->
    <rect x="83" y="64" width="34" height="11" rx="5" opacity="0.55"/>
    <rect x="82" y="79" width="36" height="11" rx="5" opacity="0.5"/>
    <rect x="82" y="94" width="36" height="11" rx="5" opacity="0.5"/>
    <rect x="83" y="109" width="34" height="11" rx="5" opacity="0.45"/>
    <!-- Lumbar vertebrae -->
    <rect x="81" y="126" width="38" height="12" rx="5" opacity="0.5"/>
    <rect x="80" y="142" width="40" height="12" rx="5" opacity="0.5"/>
    <rect x="81" y="158" width="38" height="12" rx="5" opacity="0.45"/>
    <!-- Sacrum -->
    <path d="M85 175 L100 192 L115 175z" opacity="0.4"/>
    <!-- Discs -->
    <ellipse cx="100" cy="31" rx="14" ry="2" fill="currentColor" opacity="0.08" stroke="none"/>
    <ellipse cx="100" cy="45" rx="15" ry="2" fill="currentColor" opacity="0.08" stroke="none"/>
    <ellipse cx="100" cy="61" rx="16" ry="2" fill="currentColor" opacity="0.08" stroke="none"/>
    <!-- Spinal processes -->
    <path d="M88 25 L72 30" opacity="0.25"/>
    <path d="M112 25 L128 30" opacity="0.25"/>
    <path d="M82 85 L62 92" opacity="0.25"/>
    <path d="M118 85 L138 92" opacity="0.25"/>
    <path d="M80 148 L58 155" opacity="0.25"/>
    <path d="M120 148 L142 155" opacity="0.25"/>
  `,

  eye: `
    <!-- Eye outline -->
    <path d="M20 100 C20 100 50 50 100 50 C150 50 180 100 180 100 C180 100 150 150 100 150 C50 150 20 100 20 100z" stroke-width="2"/>
    <!-- Iris -->
    <circle cx="100" cy="100" r="30" stroke-width="2"/>
    <!-- Pupil -->
    <circle cx="100" cy="100" r="14" fill="currentColor" opacity="0.6" stroke="none"/>
    <!-- Iris detail -->
    <path d="M100 70 L100 74" opacity="0.3"/>
    <path d="M100 126 L100 130" opacity="0.3"/>
    <path d="M70 100 L74 100" opacity="0.3"/>
    <path d="M126 100 L130 100" opacity="0.3"/>
    <path d="M79 79 L82 82" opacity="0.3"/>
    <path d="M118 118 L121 121" opacity="0.3"/>
    <path d="M121 79 L118 82" opacity="0.3"/>
    <path d="M82 118 L79 121" opacity="0.3"/>
    <!-- Light reflection -->
    <circle cx="110" cy="90" r="5" fill="white" opacity="0.3" stroke="none"/>
    <!-- Eyelid crease -->
    <path d="M30 85 C50 60 80 50 100 50 C120 50 150 60 170 85" opacity="0.2"/>
  `,

  ear: `
    <!-- Outer ear -->
    <path d="M120 30 C150 35 165 60 165 90 C165 120 155 140 140 155 C130 165 120 170 115 180 L105 180 C108 170 115 162 125 152 C138 140 148 120 148 90 C148 65 138 45 120 40" stroke-width="2"/>
    <!-- Helix -->
    <path d="M120 30 C100 28 80 38 70 55 C60 72 58 95 62 115 C65 130 75 140 85 145" stroke-width="2"/>
    <!-- Antihelix -->
    <path d="M115 50 C105 55 95 68 92 85 C90 100 92 112 98 122" stroke-width="1.5" opacity="0.6"/>
    <!-- Tragus -->
    <path d="M82 90 C78 88 75 92 78 98 C80 102 84 100 84 96" stroke-width="1.5" opacity="0.7"/>
    <!-- Ear canal -->
    <ellipse cx="88" cy="95" rx="6" ry="8" opacity="0.4"/>
    <!-- Earlobe -->
    <path d="M85 145 C82 155 88 168 100 170 C108 172 112 168 115 180" stroke-width="2" opacity="0.7"/>
    <!-- Inner ear hint -->
    <circle cx="88" cy="95" r="3" fill="currentColor" opacity="0.15" stroke="none"/>
  `,

  skin: `
    <!-- Epidermis layer -->
    <path d="M25 60 L175 60" stroke-width="2"/>
    <path d="M25 60 C35 55 45 58 55 55 C65 52 75 56 85 54 C95 52 105 55 115 53 C125 51 135 55 145 53 C155 51 165 56 175 60" stroke-width="1.5" opacity="0.6"/>
    <!-- Dermis layer -->
    <path d="M25 100 L175 100" stroke-width="1.5" opacity="0.5"/>
    <!-- Subcutaneous layer -->
    <path d="M25 145 L175 145" stroke-width="1" opacity="0.3"/>
    <!-- Hair follicles -->
    <path d="M60 60 L58 35 C57 28 62 25 63 30 L62 60" opacity="0.4"/>
    <path d="M120 60 L118 30 C117 22 122 20 123 26 L122 60" opacity="0.4"/>
    <!-- Sweat glands -->
    <path d="M85 80 C82 88 78 92 82 96 C86 100 90 96 88 90 C86 85 88 78 85 80z" opacity="0.35"/>
    <!-- Blood vessels -->
    <path d="M40 110 C50 105 60 112 70 108 C80 104 90 110 100 106 C110 102 120 108 130 105 C140 102 150 108 160 110" stroke-width="1" opacity="0.25"/>
    <!-- Nerve endings -->
    <circle cx="75" cy="80" r="3" fill="currentColor" opacity="0.08" stroke="none"/>
    <circle cx="140" cy="78" r="3" fill="currentColor" opacity="0.08" stroke="none"/>
    <!-- Layer labels area -->
    <circle cx="50" cy="75" r="2" fill="currentColor" opacity="0.12" stroke="none"/>
    <circle cx="50" cy="120" r="2" fill="currentColor" opacity="0.12" stroke="none"/>
    <circle cx="50" cy="160" r="2" fill="currentColor" opacity="0.12" stroke="none"/>
    <!-- Fat cells -->
    <circle cx="60" cy="125" r="8" opacity="0.1"/>
    <circle cx="80" cy="128" r="7" opacity="0.1"/>
    <circle cx="100" cy="125" r="8" opacity="0.1"/>
    <circle cx="120" cy="128" r="7" opacity="0.1"/>
    <circle cx="140" cy="125" r="8" opacity="0.1"/>
  `,

  thyroid: `
    <!-- Trachea -->
    <path d="M95 30 L95 170" stroke-width="2" opacity="0.5"/>
    <path d="M105 30 L105 170" stroke-width="2" opacity="0.5"/>
    <!-- Tracheal rings -->
    <path d="M95 45 L105 45" opacity="0.25"/>
    <path d="M95 55 L105 55" opacity="0.25"/>
    <path d="M95 65 L105 65" opacity="0.25"/>
    <path d="M95 130 L105 130" opacity="0.25"/>
    <path d="M95 140 L105 140" opacity="0.25"/>
    <!-- Thyroid - left lobe -->
    <path d="M95 75 C75 78 58 90 55 110 C52 130 65 145 85 145 C92 145 95 140 95 130" stroke-width="2"/>
    <!-- Thyroid - right lobe -->
    <path d="M105 75 C125 78 142 90 145 110 C148 130 135 145 115 145 C108 145 105 140 105 130" stroke-width="2"/>
    <!-- Isthmus -->
    <path d="M95 105 L105 105" stroke-width="2.5"/>
    <!-- Follicles -->
    <circle cx="75" cy="108" r="5" opacity="0.15"/>
    <circle cx="82" cy="125" r="4" opacity="0.12"/>
    <circle cx="68" cy="120" r="4.5" opacity="0.12"/>
    <circle cx="125" cy="108" r="5" opacity="0.15"/>
    <circle cx="118" cy="125" r="4" opacity="0.12"/>
    <circle cx="132" cy="120" r="4.5" opacity="0.12"/>
    <!-- Blood supply -->
    <path d="M75 75 C70 82 66 92 65 100" stroke-width="1" opacity="0.25"/>
    <path d="M125 75 C130 82 134 92 135 100" stroke-width="1" opacity="0.25"/>
  `,

  joint: `
    <!-- Upper bone (femur-like) -->
    <path d="M85 20 L85 80 C85 85 80 90 80 95" stroke-width="3" opacity="0.7"/>
    <path d="M115 20 L115 80 C115 85 120 90 120 95" stroke-width="3" opacity="0.7"/>
    <!-- Bone head -->
    <path d="M70 95 C65 100 62 110 65 118 C68 126 78 132 100 132 C122 132 132 126 135 118 C138 110 135 100 130 95" stroke-width="2"/>
    <!-- Cartilage -->
    <path d="M72 120 C80 125 90 128 100 128 C110 128 120 125 128 120" stroke-width="2" opacity="0.5" stroke-dasharray="4 3"/>
    <!-- Joint space -->
    <path d="M68 132 L132 132" stroke-width="1" opacity="0.3" stroke-dasharray="3 3"/>
    <!-- Lower bone (tibia-like) -->
    <path d="M72 138 C68 142 65 150 65 158 L65 162 C65 168 72 174 80 174 C88 174 92 168 92 162" stroke-width="2" opacity="0.7"/>
    <path d="M128 138 C132 142 135 150 135 158 L135 162 C135 168 128 174 120 174 C112 174 108 168 108 162" stroke-width="2" opacity="0.7"/>
    <path d="M92 162 L92 195" stroke-width="3" opacity="0.6"/>
    <path d="M108 162 L108 195" stroke-width="3" opacity="0.6"/>
    <!-- Synovial fluid -->
    <ellipse cx="100" cy="132" rx="25" ry="5" fill="currentColor" opacity="0.06" stroke="none"/>
    <!-- Ligaments -->
    <path d="M78 100 C82 115 85 125 88 135" stroke-width="1" opacity="0.3"/>
    <path d="M122 100 C118 115 115 125 112 135" stroke-width="1" opacity="0.3"/>
  `,

  intestine: `
    <!-- Small intestine loops -->
    <path d="M55 40 C55 40 145 40 145 55 C145 70 55 65 55 80 C55 95 145 90 145 105 C145 120 55 115 55 130 C55 145 145 140 145 155" stroke-width="2" opacity="0.6"/>
    <!-- Large intestine frame -->
    <path d="M40 160 L40 50 C40 35 55 30 65 35" stroke-width="2.5" opacity="0.5"/>
    <path d="M40 50 C40 35 55 25 100 25 C145 25 160 35 160 50 L160 160" stroke-width="2.5" opacity="0.5"/>
    <path d="M160 160 C160 175 145 180 100 180 C55 180 40 175 40 160" stroke-width="2.5" opacity="0.5"/>
    <!-- Haustra -->
    <path d="M35 70 L45 70" opacity="0.3"/>
    <path d="M35 90 L45 90" opacity="0.3"/>
    <path d="M35 110 L45 110" opacity="0.3"/>
    <path d="M35 130 L45 130" opacity="0.3"/>
    <path d="M155 70 L165 70" opacity="0.3"/>
    <path d="M155 90 L165 90" opacity="0.3"/>
    <path d="M155 110 L165 110" opacity="0.3"/>
    <path d="M155 130 L165 130" opacity="0.3"/>
    <!-- Appendix -->
    <path d="M45 160 C42 170 38 178 35 182" stroke-width="1.5" opacity="0.4"/>
  `,

  throat: `
    <!-- Neck outline -->
    <path d="M70 20 C65 40 62 60 60 80 C58 100 56 120 55 140 C54 160 55 175 58 185" stroke-width="1.5" opacity="0.3"/>
    <path d="M130 20 C135 40 138 60 140 80 C142 100 144 120 145 140 C146 160 145 175 142 185" stroke-width="1.5" opacity="0.3"/>
    <!-- Pharynx -->
    <path d="M82 30 C78 40 76 55 78 70" stroke-width="2" opacity="0.6"/>
    <path d="M118 30 C122 40 124 55 122 70" stroke-width="2" opacity="0.6"/>
    <!-- Larynx (voice box) -->
    <path d="M78 70 C75 75 74 82 76 90 C78 98 85 102 100 102 C115 102 122 98 124 90 C126 82 125 75 122 70" stroke-width="2"/>
    <!-- Vocal cords -->
    <path d="M84 85 L100 92 L116 85" stroke-width="1.5" opacity="0.5"/>
    <!-- Epiglottis -->
    <path d="M92 68 C95 62 100 60 105 62 C108 64 108 68 105 70 L95 70 C92 68 92 66 92 68z" stroke-width="1.5" opacity="0.6"/>
    <!-- Trachea -->
    <path d="M92 102 L90 180" stroke-width="2" opacity="0.5"/>
    <path d="M108 102 L110 180" stroke-width="2" opacity="0.5"/>
    <!-- Tracheal rings -->
    <path d="M92 115 L108 115" opacity="0.3"/>
    <path d="M91 130 L109 130" opacity="0.3"/>
    <path d="M91 145 L109 145" opacity="0.3"/>
    <path d="M90 160 L110 160" opacity="0.3"/>
    <!-- Thyroid gland hint -->
    <path d="M85 108 C78 112 75 120 78 128 C80 132 88 134 92 130" opacity="0.3"/>
    <path d="M115 108 C122 112 125 120 122 128 C120 132 112 134 108 130" opacity="0.3"/>
  `,

  pancreas: `
    <!-- Pancreas body -->
    <path d="M45 95 C50 85 65 80 85 82 C100 84 110 88 125 90 C140 92 155 90 165 95 C172 98 174 108 168 115 C160 124 145 125 130 122 C115 119 105 118 90 120 C75 122 60 120 50 115 C42 110 40 102 45 95z" stroke-width="2"/>
    <!-- Pancreatic duct -->
    <path d="M60 105 C80 102 100 103 120 105 C140 107 155 108 165 105" stroke-width="1.5" opacity="0.4"/>
    <!-- Head of pancreas -->
    <circle cx="55" cy="105" r="15" opacity="0.15" fill="currentColor" stroke="none"/>
    <!-- Islets of Langerhans -->
    <circle cx="80" cy="98" r="3" opacity="0.12" fill="currentColor" stroke="none"/>
    <circle cx="105" cy="102" r="3.5" opacity="0.12" fill="currentColor" stroke="none"/>
    <circle cx="130" cy="100" r="3" opacity="0.12" fill="currentColor" stroke="none"/>
    <!-- Duodenum curve -->
    <path d="M45 80 C35 85 28 100 30 115 C32 130 40 140 50 142 C58 143 62 138 60 130 C58 120 52 112 50 105" stroke-width="1.5" opacity="0.4"/>
    <!-- Blood vessels -->
    <path d="M100 80 L100 70" stroke-width="1" opacity="0.25"/>
    <path d="M100 125 L100 140" stroke-width="1" opacity="0.25"/>
    <!-- Bile duct -->
    <path d="M48 70 L50 90" stroke-width="1" opacity="0.3"/>
  `,

  bladder: `
    <!-- Bladder body -->
    <path d="M60 70 C40 80 30 105 32 130 C34 155 50 175 75 180 C90 183 110 183 125 180 C150 175 166 155 168 130 C170 105 160 80 140 70" stroke-width="2"/>
    <!-- Ureters -->
    <path d="M75 30 C72 45 68 55 65 70" stroke-width="1.5" opacity="0.5"/>
    <path d="M125 30 C128 45 132 55 135 70" stroke-width="1.5" opacity="0.5"/>
    <!-- Ureteral openings -->
    <circle cx="65" cy="72" r="3" opacity="0.3"/>
    <circle cx="135" cy="72" r="3" opacity="0.3"/>
    <!-- Internal folds -->
    <path d="M55 100 C70 95 90 98 100 100 C110 102 130 95 145 100" opacity="0.2"/>
    <path d="M50 125 C68 120 88 122 100 125 C112 128 132 120 150 125" opacity="0.2"/>
    <!-- Urethra -->
    <path d="M95 178 C96 185 98 190 100 195" stroke-width="1.5" opacity="0.5"/>
    <path d="M105 178 C104 185 102 190 100 195" stroke-width="1.5" opacity="0.5"/>
    <!-- Trigone -->
    <path d="M65 72 L100 175 L135 72" opacity="0.1" stroke-dasharray="4 4"/>
    <!-- Detrusor muscle hint -->
    <path d="M45 95 C42 110 42 130 48 150" opacity="0.15"/>
    <path d="M155 95 C158 110 158 130 152 150" opacity="0.15"/>
  `,

  immune: `
    <!-- Shield outline -->
    <path d="M100 20 L50 50 L50 100 C50 145 70 170 100 185 C130 170 150 145 150 100 L150 50 L100 20z" stroke-width="2"/>
    <!-- Cross/plus -->
    <path d="M100 70 L100 140" stroke-width="3" opacity="0.5"/>
    <path d="M70 105 L130 105" stroke-width="3" opacity="0.5"/>
    <!-- Antibody shapes -->
    <path d="M65 65 L60 55 M65 65 L70 55 M65 65 L65 80" stroke-width="1.5" opacity="0.3"/>
    <path d="M135 65 L130 55 M135 65 L140 55 M135 65 L135 80" stroke-width="1.5" opacity="0.3"/>
    <!-- Cell markers -->
    <circle cx="80" cy="85" r="5" opacity="0.15" fill="currentColor" stroke="none"/>
    <circle cx="120" cy="85" r="5" opacity="0.15" fill="currentColor" stroke="none"/>
    <circle cx="80" cy="130" r="5" opacity="0.15" fill="currentColor" stroke="none"/>
    <circle cx="120" cy="130" r="5" opacity="0.15" fill="currentColor" stroke="none"/>
    <!-- Shield glow -->
    <path d="M100 35 L60 58 L60 100 C60 138 76 160 100 172 C124 160 140 138 140 100 L140 58 L100 35z" opacity="0.08" fill="currentColor" stroke="none"/>
  `,

  bone: `
    <!-- Long bone -->
    <path d="M80 30 C70 30 62 38 62 48 C62 55 68 60 72 62 L72 138 C68 140 62 145 62 152 C62 162 70 170 80 170 L120 170 C130 170 138 162 138 152 C138 145 132 140 128 138 L128 62 C132 60 138 55 138 48 C138 38 130 30 120 30 L80 30z" stroke-width="2"/>
    <!-- Epiphyseal line top -->
    <path d="M72 62 L128 62" stroke-width="1.5" opacity="0.4"/>
    <!-- Epiphyseal line bottom -->
    <path d="M72 138 L128 138" stroke-width="1.5" opacity="0.4"/>
    <!-- Medullary cavity -->
    <path d="M82 72 L82 128" stroke-width="1" opacity="0.2"/>
    <path d="M118 72 L118 128" stroke-width="1" opacity="0.2"/>
    <!-- Trabecular bone hints -->
    <path d="M75 42 C85 45 95 42 100 40 C105 42 115 45 125 42" opacity="0.2"/>
    <path d="M75 158 C85 155 95 158 100 160 C105 158 115 155 125 158" opacity="0.2"/>
    <!-- Periosteum -->
    <path d="M70 70 L70 130" stroke-width="1" opacity="0.15" stroke-dasharray="4 4"/>
    <path d="M130 70 L130 130" stroke-width="1" opacity="0.15" stroke-dasharray="4 4"/>
    <!-- Bone marrow dots -->
    <circle cx="90" cy="90" r="2" fill="currentColor" opacity="0.08" stroke="none"/>
    <circle cx="110" cy="100" r="2" fill="currentColor" opacity="0.08" stroke="none"/>
    <circle cx="95" cy="115" r="2" fill="currentColor" opacity="0.08" stroke="none"/>
  `,

  head: `
    <!-- Skull outline -->
    <path d="M100 25 C60 25 40 55 40 85 C40 110 50 130 65 142 L72 148 L72 165 L128 165 L128 148 L135 142 C150 130 160 110 160 85 C160 55 140 25 100 25z" stroke-width="2"/>
    <!-- Jaw -->
    <path d="M72 148 C78 158 88 165 100 165 C112 165 122 158 128 148" opacity="0.4"/>
    <!-- Eye sockets -->
    <ellipse cx="78" cy="90" rx="15" ry="12" opacity="0.3"/>
    <ellipse cx="122" cy="90" rx="15" ry="12" opacity="0.3"/>
    <!-- Nose -->
    <path d="M100 95 L95 115 L105 115 L100 95z" opacity="0.3"/>
    <!-- Cranial sutures -->
    <path d="M100 25 L100 60" opacity="0.15" stroke-dasharray="3 3"/>
    <path d="M55 70 C70 65 85 62 100 60 C115 62 130 65 145 70" opacity="0.15" stroke-dasharray="3 3"/>
    <!-- Temporal region -->
    <path d="M45 80 C48 95 50 110 55 120" opacity="0.2"/>
    <path d="M155 80 C152 95 150 110 145 120" opacity="0.2"/>
  `,

  body: `
    <!-- Head -->
    <circle cx="100" cy="35" r="18" stroke-width="2"/>
    <!-- Neck -->
    <path d="M93 53 L93 65" stroke-width="1.5"/>
    <path d="M107 53 L107 65" stroke-width="1.5"/>
    <!-- Torso -->
    <path d="M70 65 L65 130 L80 135 L100 140 L120 135 L135 130 L130 65z" stroke-width="2"/>
    <!-- Shoulders -->
    <path d="M70 65 L50 72" stroke-width="2"/>
    <path d="M130 65 L150 72" stroke-width="2"/>
    <!-- Arms -->
    <path d="M50 72 L42 115 L38 145" stroke-width="1.8" opacity="0.7"/>
    <path d="M150 72 L158 115 L162 145" stroke-width="1.8" opacity="0.7"/>
    <!-- Legs -->
    <path d="M85 135 L78 170 L75 195" stroke-width="2" opacity="0.7"/>
    <path d="M115 135 L122 170 L125 195" stroke-width="2" opacity="0.7"/>
    <!-- Spine center line -->
    <path d="M100 65 L100 140" opacity="0.15" stroke-dasharray="3 3"/>
    <!-- Ribcage hint -->
    <path d="M78 80 L100 85 L122 80" opacity="0.15"/>
    <path d="M75 95 L100 100 L125 95" opacity="0.15"/>
    <!-- Pelvis -->
    <path d="M80 130 C90 140 110 140 120 130" opacity="0.3"/>
  `,
}

const illustrationSvg = computed(() => {
  return illustrations[illustrationKey.value] || illustrations.body
})
</script>

<style scoped>
.medical-illustration {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
