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
          <stop offset="0%" :stop-color="accentColor" stop-opacity="0.65" />
          <stop offset="70%" :stop-color="accentColor" stop-opacity="0.05" />
          <stop offset="100%" :stop-color="accentColor" stop-opacity="0" />
        </radialGradient>
      </defs>
      <circle cx="100" cy="100" r="95" fill="url(#ill-glow)" />

      <!-- Illustration paths -->
      <g :stroke="strokeColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
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
const strokeColor = computed(() => isDark.value ? '#94a3b8' : '#1e293b')

const containerClass = computed(() =>
  isDark.value ? 'opacity-80 hover:opacity-100 transition-opacity' : 'opacity-90 hover:opacity-100 transition-opacity'
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

// Detailed medical SVG illustrations (200x200 viewBox) — colored anatomical fills
const illustrations = {
  esophagus: `
    <!-- Esophagus tube with pink lining -->
    <path d="M88 25 C88 25 85 50 82 75 C80 90 78 110 80 125 L120 125 C122 110 120 90 118 75 C115 50 112 25 112 25z" fill="#F9A8D4" fill-opacity="0.4" stroke="#9D174D" stroke-width="2"/>
    <path d="M90 25 C90 25 87 50 84 75 C82 90 80 110 82 125" stroke="#EC4899" stroke-width="1.5" fill="none" opacity="0.7"/>
    <path d="M110 25 C110 25 113 50 116 75 C118 90 120 110 118 125" stroke="#EC4899" stroke-width="1.5" fill="none" opacity="0.7"/>
    <!-- Esophageal lining folds -->
    <path d="M90 35 C95 38 105 38 110 35" stroke="#BE185D" fill="none" opacity="0.6"/>
    <path d="M88 55 C94 58 106 58 112 55" stroke="#BE185D" fill="none" opacity="0.6"/>
    <path d="M86 75 C93 78 107 78 114 75" stroke="#BE185D" fill="none" opacity="0.6"/>
    <!-- Lower esophageal sphincter -->
    <ellipse cx="100" cy="120" rx="22" ry="8" fill="#F472B6" fill-opacity="0.3" stroke="#9D174D" stroke-width="2"/>
    <!-- Stomach -->
    <path d="M78 125 C60 130 48 150 50 170 C52 185 70 195 90 192 C100 190 110 185 115 175 C125 155 128 140 122 125" fill="#F9A8D4" fill-opacity="0.5" stroke="#9D174D" stroke-width="2"/>
    <!-- Stomach inner lining -->
    <path d="M82 130 C65 135 54 152 56 168 C58 180 72 188 88 186" fill="#EC4899" fill-opacity="0.25" stroke="none"/>
    <!-- Stomach rugae -->
    <path d="M65 150 C75 148 85 152 90 155" stroke="#BE185D" fill="none" opacity="0.7"/>
    <path d="M60 165 C72 162 82 166 88 170" stroke="#BE185D" fill="none" opacity="0.7"/>
    <!-- Acid reflux arrows (green) -->
    <path d="M95 110 L95 90" stroke="#84CC16" stroke-width="1.5" opacity="0.8" stroke-dasharray="4 3" fill="none"/>
    <path d="M95 90 L91 96 M95 90 L99 96" stroke="#84CC16" stroke-width="1.5" opacity="0.8" fill="none"/>
    <path d="M105 105 L105 85" stroke="#84CC16" stroke-width="1.5" opacity="0.8" stroke-dasharray="4 3" fill="none"/>
    <path d="M105 85 L101 91 M105 85 L109 91" stroke="#84CC16" stroke-width="1.5" opacity="0.8" fill="none"/>
    <!-- Gastric juice hint -->
    <circle cx="90" cy="70" r="2" fill="#84CC16" opacity="0.7" stroke="none"/>
    <circle cx="108" cy="65" r="2" fill="#84CC16" opacity="0.7" stroke="none"/>
    <circle cx="94" cy="50" r="1.5" fill="#84CC16" opacity="0.6" stroke="none"/>
    <!-- Diaphragm line -->
    <path d="M40 122 C60 115 80 118 100 120 C120 122 140 115 160 122" stroke="#6B7280" stroke-width="1" opacity="0.65" stroke-dasharray="6 4" fill="none"/>
  `,

  stomach: `
    <!-- Esophagus entry -->
    <path d="M90 20 L85 60 L108 60 L110 20" fill="#F9A8D4" fill-opacity="0.3" stroke="#9D174D" stroke-width="2"/>
    <!-- Stomach body -->
    <path d="M82 60 C55 70 40 100 42 135 C44 165 70 185 100 182 C120 180 138 165 140 140 C145 110 135 80 112 60" fill="#F9A8D4" fill-opacity="0.55" stroke="#9D174D" stroke-width="2"/>
    <!-- Inner lining -->
    <path d="M86 65 C62 74 48 102 50 132 C52 158 72 178 98 176 C116 174 132 162 134 138 C138 112 130 84 110 65" fill="#EC4899" fill-opacity="0.25" stroke="none"/>
    <!-- Gastric juice pool -->
    <path d="M58 145 C65 158 80 168 95 170 C80 165 68 155 60 142z" fill="#84CC16" fill-opacity="0.3" stroke="none"/>
    <!-- Greater curvature detail -->
    <path d="M55 90 C58 110 60 130 65 148" stroke="#BE185D" fill="none" opacity="0.6"/>
    <!-- Rugae folds -->
    <path d="M65 95 C80 92 95 97 105 100" stroke="#BE185D" fill="none" opacity="0.7"/>
    <path d="M58 115 C75 112 90 117 102 120" stroke="#BE185D" fill="none" opacity="0.7"/>
    <path d="M55 135 C72 132 88 137 98 140" stroke="#BE185D" fill="none" opacity="0.7"/>
    <!-- Pylorus -->
    <ellipse cx="115" cy="165" rx="12" ry="6" fill="#F472B6" fill-opacity="0.4" stroke="#9D174D" opacity="0.8"/>
    <!-- Gastric glands -->
    <circle cx="75" cy="105" r="2.5" fill="#EC4899" opacity="0.6" stroke="none"/>
    <circle cx="90" cy="125" r="2.5" fill="#EC4899" opacity="0.6" stroke="none"/>
    <circle cx="72" cy="145" r="2" fill="#EC4899" opacity="0.6" stroke="none"/>
  `,

  heart: `
    <!-- Aorta -->
    <path d="M100 45 C100 30 115 20 130 25 C145 30 145 45 140 60 L125 55 C128 44 125 34 118 30 C112 28 105 32 105 42z" fill="#EF4444" fill-opacity="0.5" stroke="#991B1B" stroke-width="2"/>
    <path d="M100 45 C100 30 85 20 70 25 C55 30 55 45 60 60 L75 55 C72 44 75 34 82 30 C88 28 95 32 95 42z" fill="#3B82F6" fill-opacity="0.4" stroke="#1E40AF" stroke-width="2"/>
    <!-- Heart body -->
    <path d="M60 60 C45 70 35 95 40 120 C45 145 65 170 100 185 C135 170 155 145 160 120 C165 95 155 70 140 60" fill="#DC2626" fill-opacity="0.5" stroke="#991B1B" stroke-width="2"/>
    <!-- Right side (blue deoxygenated) -->
    <path d="M60 60 C45 70 35 95 40 120 C45 145 65 170 100 185 L100 55z" fill="#3B82F6" fill-opacity="0.15" stroke="none"/>
    <!-- Left side (red oxygenated) -->
    <path d="M140 60 C155 70 165 95 160 120 C155 145 135 170 100 185 L100 55z" fill="#DC2626" fill-opacity="0.15" stroke="none"/>
    <!-- Septum -->
    <path d="M100 55 L100 170" stroke="#991B1B" opacity="0.7" stroke-dasharray="4 4" fill="none"/>
    <!-- Right atrium -->
    <path d="M70 80 C75 90 85 95 95 90" fill="#6366F1" fill-opacity="0.2" stroke="#4338CA" opacity="0.6"/>
    <!-- Left atrium -->
    <path d="M105 90 C115 95 125 90 130 80" fill="#DC2626" fill-opacity="0.2" stroke="#991B1B" opacity="0.6"/>
    <!-- Right ventricle -->
    <path d="M65 115 C75 125 90 128 95 120" fill="#6366F1" fill-opacity="0.25" stroke="#4338CA" opacity="0.6"/>
    <!-- Left ventricle -->
    <path d="M105 120 C110 128 125 125 135 115" fill="#991B1B" fill-opacity="0.25" stroke="#991B1B" opacity="0.6"/>
    <!-- Valves -->
    <ellipse cx="85" cy="100" rx="8" ry="3" fill="#F87171" fill-opacity="0.5" stroke="#991B1B" opacity="0.75" transform="rotate(-10 85 100)"/>
    <ellipse cx="115" cy="100" rx="8" ry="3" fill="#F87171" fill-opacity="0.5" stroke="#991B1B" opacity="0.75" transform="rotate(10 115 100)"/>
    <!-- Coronary arteries -->
    <path d="M75 70 C68 85 65 100 68 120" stroke="#EF4444" stroke-width="1.5" opacity="0.7" fill="none"/>
    <path d="M125 70 C132 85 135 100 132 120" stroke="#EF4444" stroke-width="1.5" opacity="0.7" fill="none"/>
    <!-- Heartbeat line -->
    <path d="M25 150 L55 150 L65 130 L75 165 L85 140 L90 150 L175 150" stroke="#EF4444" stroke-width="1.5" opacity="0.8" fill="none"/>
  `,

  ribcage: `
    <!-- Sternum -->
    <path d="M97 25 L97 130 L103 130 L103 25z" fill="#F5F5DC" fill-opacity="0.5" stroke="#78716C" stroke-width="2"/>
    <!-- Ribs - left -->
    <path d="M100 40 C85 38 65 45 50 60" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.8"/>
    <path d="M100 52 C83 50 60 58 45 75" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.8"/>
    <path d="M100 64 C82 62 58 72 42 90" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.75"/>
    <path d="M100 76 C82 75 58 85 45 105" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.7"/>
    <path d="M100 88 C84 87 62 96 50 115" stroke="#D6D3D1" stroke-width="2" fill="none" opacity="0.65"/>
    <path d="M100 100 C86 99 68 106 58 120" stroke="#D6D3D1" stroke-width="2" fill="none" opacity="0.8"/>
    <path d="M100 112 C90 111 78 115 70 125" stroke="#D6D3D1" stroke-width="2" fill="none" opacity="0.75"/>
    <!-- Ribs - right -->
    <path d="M100 40 C115 38 135 45 150 60" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.8"/>
    <path d="M100 52 C117 50 140 58 155 75" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.8"/>
    <path d="M100 64 C118 62 142 72 158 90" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.75"/>
    <path d="M100 76 C118 75 142 85 155 105" stroke="#D6D3D1" stroke-width="2.5" fill="none" opacity="0.7"/>
    <path d="M100 88 C116 87 138 96 150 115" stroke="#D6D3D1" stroke-width="2" fill="none" opacity="0.65"/>
    <path d="M100 100 C114 99 132 106 142 120" stroke="#D6D3D1" stroke-width="2" fill="none" opacity="0.8"/>
    <path d="M100 112 C110 111 122 115 130 125" stroke="#D6D3D1" stroke-width="2" fill="none" opacity="0.75"/>
    <!-- Costal cartilage highlight (costochondritis area) -->
    <circle cx="88" cy="55" r="6" fill="#EF4444" opacity="0.5" stroke="none"/>
    <circle cx="112" cy="55" r="6" fill="#EF4444" opacity="0.5" stroke="none"/>
    <!-- Inflammation marker -->
    <circle cx="88" cy="55" r="10" stroke="#EF4444" stroke-width="1" opacity="0.55" stroke-dasharray="3 3" fill="none"/>
    <circle cx="112" cy="55" r="10" stroke="#EF4444" stroke-width="1" opacity="0.55" stroke-dasharray="3 3" fill="none"/>
    <!-- Spine hint -->
    <path d="M100 130 L100 180" stroke="#A8A29E" stroke-width="2" opacity="0.6" fill="none"/>
    <path d="M94 145 L106 145" stroke="#A8A29E" opacity="0.65" fill="none"/>
    <path d="M94 160 L106 160" stroke="#A8A29E" opacity="0.65" fill="none"/>
  `,

  lungs: `
    <!-- Left lung fill -->
    <path d="M45 65 C30 75 20 100 22 130 C24 160 40 180 65 182 C80 183 90 175 95 160 L95 55 C85 58 60 62 45 65z" fill="#FCA5A5" fill-opacity="0.45" stroke="#991B1B" stroke-width="2"/>
    <!-- Right lung fill -->
    <path d="M155 65 C170 75 180 100 178 130 C176 160 160 180 135 182 C120 183 110 175 105 160 L105 55 C115 58 140 62 155 65z" fill="#FCA5A5" fill-opacity="0.45" stroke="#991B1B" stroke-width="2"/>
    <!-- Trachea -->
    <path d="M95 18 L95 55 L105 55 L105 18z" fill="#D1D5DB" fill-opacity="0.5" stroke="#6B7280" stroke-width="2"/>
    <!-- Tracheal rings -->
    <path d="M95 28 L105 28" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <path d="M95 36 L105 36" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <path d="M95 44 L105 44" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <!-- Bronchi -->
    <path d="M95 55 C85 60 70 65 60 75" stroke="#F87171" stroke-width="2" fill="none"/>
    <path d="M105 55 C115 60 130 65 140 75" stroke="#F87171" stroke-width="2" fill="none"/>
    <!-- Bronchial tree - left -->
    <path d="M60 75 C55 85 45 95 40 110" stroke="#F87171" opacity="0.6" fill="none"/>
    <path d="M60 75 C58 88 55 100 58 115" stroke="#F87171" opacity="0.6" fill="none"/>
    <path d="M70 70 C65 82 58 92 52 100" stroke="#F87171" opacity="0.7" fill="none"/>
    <!-- Bronchial tree - right -->
    <path d="M140 75 C145 85 155 95 160 110" stroke="#F87171" opacity="0.6" fill="none"/>
    <path d="M140 75 C142 88 145 100 142 115" stroke="#F87171" opacity="0.6" fill="none"/>
    <path d="M130 70 C135 82 142 92 148 100" stroke="#F87171" opacity="0.7" fill="none"/>
    <!-- Alveoli hints -->
    <circle cx="42" cy="130" r="5" fill="#FECACA" opacity="0.7" stroke="#F87171" stroke-width="0.5"/>
    <circle cx="55" cy="145" r="5" fill="#FECACA" opacity="0.7" stroke="#F87171" stroke-width="0.5"/>
    <circle cx="158" cy="130" r="5" fill="#FECACA" opacity="0.7" stroke="#F87171" stroke-width="0.5"/>
    <circle cx="145" cy="145" r="5" fill="#FECACA" opacity="0.7" stroke="#F87171" stroke-width="0.5"/>
  `,

  brain: `
    <!-- Brain fill -->
    <path d="M100 30 C60 30 35 55 35 90 C35 115 45 135 65 148 L72 155 L72 170 L128 170 L128 155 L135 148 C155 135 165 115 165 90 C165 55 140 30 100 30z" fill="#FDA4AF" fill-opacity="0.45" stroke="#9F1239" stroke-width="2"/>
    <!-- Hemisphere divide -->
    <path d="M100 32 L100 165" stroke="#BE123C" opacity="0.5" stroke-dasharray="4 4" fill="none"/>
    <!-- Left hemisphere gyri -->
    <path d="M55 60 C65 55 80 58 90 65" stroke="#BE123C" fill="none" opacity="0.65"/>
    <path d="M45 80 C58 75 72 78 88 85" stroke="#BE123C" fill="none" opacity="0.65"/>
    <path d="M42 100 C56 95 70 98 90 105" stroke="#BE123C" fill="none" opacity="0.6"/>
    <path d="M48 118 C60 114 74 117 88 122" stroke="#BE123C" fill="none" opacity="0.7"/>
    <!-- Right hemisphere gyri -->
    <path d="M145 60 C135 55 120 58 110 65" stroke="#BE123C" fill="none" opacity="0.65"/>
    <path d="M155 80 C142 75 128 78 112 85" stroke="#BE123C" fill="none" opacity="0.65"/>
    <path d="M158 100 C144 95 130 98 110 105" stroke="#BE123C" fill="none" opacity="0.6"/>
    <path d="M152 118 C140 114 126 117 112 122" stroke="#BE123C" fill="none" opacity="0.7"/>
    <!-- Cerebellum -->
    <path d="M75 148 C80 155 90 158 100 158 C110 158 120 155 125 148" fill="#FB7185" fill-opacity="0.3" stroke="#BE123C" opacity="0.7"/>
    <path d="M80 152 C88 158 112 158 120 152" stroke="#BE123C" fill="none" opacity="0.7"/>
    <!-- Brain stem -->
    <path d="M92 158 C92 162 95 168 100 170 C105 168 108 162 108 158" fill="#FDA4AF" fill-opacity="0.5" stroke="#9F1239" opacity="0.8"/>
    <!-- Neural activity nodes (blue) -->
    <circle cx="70" cy="70" r="4.5" fill="#3B82F6" opacity="0.6" stroke="#1E40AF" stroke-width="0.5"/>
    <circle cx="130" cy="70" r="4.5" fill="#3B82F6" opacity="0.6" stroke="#1E40AF" stroke-width="0.5"/>
    <circle cx="80" cy="100" r="4" fill="#3B82F6" opacity="0.7" stroke="#1E40AF" stroke-width="0.5"/>
    <circle cx="120" cy="100" r="4" fill="#3B82F6" opacity="0.7" stroke="#1E40AF" stroke-width="0.5"/>
    <!-- Neural connections -->
    <path d="M70 70 L80 100" stroke="#60A5FA" opacity="0.6" fill="none" stroke-width="1.5"/>
    <path d="M130 70 L120 100" stroke="#60A5FA" opacity="0.6" fill="none" stroke-width="1.5"/>
    <path d="M80 100 L100 90 L120 100" stroke="#60A5FA" opacity="0.55" fill="none" stroke-width="1.5"/>
  `,

  liver: `
    <!-- Liver body -->
    <path d="M35 80 C30 70 40 50 70 45 C100 40 150 45 170 60 C180 68 178 85 170 100 C155 130 120 150 90 155 C65 158 45 145 38 125 C32 110 32 95 35 80z" fill="#92400E" fill-opacity="0.5" stroke="#78350F" stroke-width="2"/>
    <!-- Right lobe (lighter) -->
    <path d="M105 48 C135 46 158 50 168 60 C176 67 175 82 168 96 C158 118 135 136 115 142 L100 100z" fill="#B45309" fill-opacity="0.3" stroke="none"/>
    <!-- Falciform ligament -->
    <path d="M105 45 L100 100" stroke="#78350F" stroke-width="1.5" opacity="0.7" fill="none"/>
    <!-- Hepatic lobes division -->
    <path d="M100 50 C98 70 95 90 90 110 C85 130 82 145 85 155" stroke="#78350F" fill="none" opacity="0.7"/>
    <!-- Portal vein -->
    <path d="M100 100 C90 105 80 115 75 130" stroke="#3B82F6" stroke-width="1.5" opacity="0.6" fill="none"/>
    <path d="M100 100 C110 108 120 115 130 118" stroke="#3B82F6" stroke-width="1.5" opacity="0.6" fill="none"/>
    <!-- Hepatic veins -->
    <path d="M100 70 L85 55" stroke="#EF4444" opacity="0.7" fill="none"/>
    <path d="M100 70 L120 55" stroke="#EF4444" opacity="0.7" fill="none"/>
    <!-- Gallbladder -->
    <path d="M110 130 C115 135 118 145 115 155 C112 162 108 162 105 155 C102 145 105 135 110 130z" fill="#22C55E" fill-opacity="0.55" stroke="#15803D" stroke-width="1.5"/>
    <!-- Surface texture -->
    <circle cx="65" cy="80" r="3" fill="#B45309" opacity="0.5" stroke="none"/>
    <circle cx="130" cy="75" r="3" fill="#B45309" opacity="0.5" stroke="none"/>
    <circle cx="80" cy="110" r="3" fill="#B45309" opacity="0.5" stroke="none"/>
  `,

  kidney: `
    <!-- Left kidney -->
    <path d="M70 55 C50 60 35 80 35 105 C35 135 50 160 70 165 C82 168 90 158 90 145 L90 120 C90 112 85 108 80 108 C75 108 70 112 70 120 L70 130 C70 138 65 142 60 140 C50 136 42 120 42 105 C42 85 52 68 70 55z" fill="#B91C1C" fill-opacity="0.4" stroke="#7F1D1D" stroke-width="2"/>
    <!-- Right kidney -->
    <path d="M130 55 C150 60 165 80 165 105 C165 135 150 160 130 165 C118 168 110 158 110 145 L110 120 C110 112 115 108 120 108 C125 108 130 112 130 120 L130 130 C130 138 135 142 140 140 C150 136 158 120 158 105 C158 85 148 68 130 55z" fill="#B91C1C" fill-opacity="0.4" stroke="#7F1D1D" stroke-width="2"/>
    <!-- Medulla zones (lighter red) -->
    <circle cx="62" cy="105" r="12" fill="#EF4444" opacity="0.5" stroke="none"/>
    <circle cx="138" cy="105" r="12" fill="#EF4444" opacity="0.5" stroke="none"/>
    <!-- Renal pelvis -->
    <path d="M78 108 C76 100 72 95 68 95 C64 95 60 100 60 108" fill="#FCA5A5" fill-opacity="0.4" stroke="none"/>
    <path d="M122 108 C124 100 128 95 132 95 C136 95 140 100 140 108" fill="#FCA5A5" fill-opacity="0.4" stroke="none"/>
    <!-- Ureters (yellow) -->
    <path d="M75 160 C78 175 85 185 95 190" stroke="#FDE68A" stroke-width="2.5" opacity="0.8" fill="none"/>
    <path d="M125 160 C122 175 115 185 105 190" stroke="#FDE68A" stroke-width="2.5" opacity="0.8" fill="none"/>
    <!-- Renal arteries -->
    <path d="M100 95 L78 100" stroke="#EF4444" stroke-width="1.5" opacity="0.7" fill="none"/>
    <path d="M100 95 L122 100" stroke="#EF4444" stroke-width="1.5" opacity="0.7" fill="none"/>
    <!-- Aorta hint -->
    <path d="M100 50 L100 140" stroke="#DC2626" stroke-width="2" opacity="0.5" fill="none"/>
  `,

  spine: `
    <!-- Vertebral column -->
    <path d="M98 15 L98 185 L102 185 L102 15z" fill="#E7E5E4" fill-opacity="0.4" stroke="#78716C" stroke-width="1.5"/>
    <!-- Cervical vertebrae -->
    <rect x="88" y="20" width="24" height="10" rx="4" fill="#F5F5DC" fill-opacity="0.6" stroke="#78716C" stroke-width="1.5"/>
    <rect x="86" y="34" width="28" height="10" rx="4" fill="#F5F5DC" fill-opacity="0.6" stroke="#78716C" stroke-width="1.5"/>
    <rect x="85" y="48" width="30" height="10" rx="4" fill="#F5F5DC" fill-opacity="0.55" stroke="#78716C" stroke-width="1.5"/>
    <!-- Thoracic vertebrae -->
    <rect x="83" y="64" width="34" height="11" rx="5" fill="#E7E5E4" fill-opacity="0.6" stroke="#78716C" stroke-width="1.5"/>
    <rect x="82" y="79" width="36" height="11" rx="5" fill="#E7E5E4" fill-opacity="0.65" stroke="#78716C" stroke-width="1.5"/>
    <rect x="82" y="94" width="36" height="11" rx="5" fill="#E7E5E4" fill-opacity="0.65" stroke="#78716C" stroke-width="1.5"/>
    <rect x="83" y="109" width="34" height="11" rx="5" fill="#E7E5E4" fill-opacity="0.6" stroke="#78716C" stroke-width="1.5"/>
    <!-- Lumbar vertebrae -->
    <rect x="81" y="126" width="38" height="12" rx="5" fill="#D6D3D1" fill-opacity="0.65" stroke="#78716C" stroke-width="1.5"/>
    <rect x="80" y="142" width="40" height="12" rx="5" fill="#D6D3D1" fill-opacity="0.65" stroke="#78716C" stroke-width="1.5"/>
    <rect x="81" y="158" width="38" height="12" rx="5" fill="#D6D3D1" fill-opacity="0.6" stroke="#78716C" stroke-width="1.5"/>
    <!-- Sacrum -->
    <path d="M85 175 L100 192 L115 175z" fill="#D6D3D1" fill-opacity="0.5" stroke="#78716C" stroke-width="1.5"/>
    <!-- Discs (blue) -->
    <ellipse cx="100" cy="31" rx="14" ry="2" fill="#60A5FA" opacity="0.6" stroke="none"/>
    <ellipse cx="100" cy="45" rx="15" ry="2" fill="#60A5FA" opacity="0.6" stroke="none"/>
    <ellipse cx="100" cy="61" rx="16" ry="2" fill="#60A5FA" opacity="0.6" stroke="none"/>
    <!-- Spinal cord (yellow) -->
    <path d="M99 18 L99 180" stroke="#FDE68A" stroke-width="2" opacity="0.5" fill="none"/>
    <!-- Spinal processes -->
    <path d="M88 25 L72 30" stroke="#A8A29E" opacity="0.7" fill="none"/>
    <path d="M112 25 L128 30" stroke="#A8A29E" opacity="0.7" fill="none"/>
    <path d="M82 85 L62 92" stroke="#A8A29E" opacity="0.7" fill="none"/>
    <path d="M118 85 L138 92" stroke="#A8A29E" opacity="0.7" fill="none"/>
    <path d="M80 148 L58 155" stroke="#A8A29E" opacity="0.7" fill="none"/>
    <path d="M120 148 L142 155" stroke="#A8A29E" opacity="0.7" fill="none"/>
  `,

  eye: `
    <!-- Eye outline (sclera white) -->
    <path d="M20 100 C20 100 50 50 100 50 C150 50 180 100 180 100 C180 100 150 150 100 150 C50 150 20 100 20 100z" fill="#FFFFFF" fill-opacity="0.85" stroke="#374151" stroke-width="2"/>
    <!-- Pink corners -->
    <path d="M20 100 C25 95 32 88 40 82 C32 92 28 98 25 100 C28 102 32 108 40 118 C32 112 25 105 20 100z" fill="#FDA4AF" fill-opacity="0.6" stroke="none"/>
    <path d="M180 100 C175 95 168 88 160 82 C168 92 172 98 175 100 C172 102 168 108 160 118 C168 112 175 105 180 100z" fill="#FDA4AF" fill-opacity="0.6" stroke="none"/>
    <!-- Iris -->
    <circle cx="100" cy="100" r="30" fill="#3B82F6" fill-opacity="0.45" stroke="#1E40AF" stroke-width="2"/>
    <!-- Iris detail rings -->
    <circle cx="100" cy="100" r="24" fill="none" stroke="#2563EB" stroke-width="0.5" opacity="0.5"/>
    <circle cx="100" cy="100" r="20" fill="none" stroke="#1D4ED8" stroke-width="0.5" opacity="0.4"/>
    <!-- Pupil -->
    <circle cx="100" cy="100" r="14" fill="#111827" opacity="0.85" stroke="none"/>
    <!-- Iris radial details -->
    <path d="M100 70 L100 74" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <path d="M100 126 L100 130" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <path d="M70 100 L74 100" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <path d="M126 100 L130 100" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <path d="M79 79 L82 82" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <path d="M118 118 L121 121" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <path d="M121 79 L118 82" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <path d="M82 118 L79 121" stroke="#1E40AF" opacity="0.55" fill="none"/>
    <!-- Light reflection -->
    <circle cx="108" cy="92" r="5" fill="white" opacity="0.8" stroke="none"/>
    <circle cx="94" cy="106" r="2" fill="white" opacity="0.5" stroke="none"/>
    <!-- Eyelid crease -->
    <path d="M30 85 C50 60 80 50 100 50 C120 50 150 60 170 85" stroke="#374151" opacity="0.5" fill="none"/>
  `,

  ear: `
    <!-- Outer ear fill -->
    <path d="M120 30 C150 35 165 60 165 90 C165 120 155 140 140 155 C130 165 120 170 115 180 L105 180 C108 170 115 162 125 152 C138 140 148 120 148 90 C148 65 138 45 120 40 L120 30z" fill="#FDBCB4" fill-opacity="0.4" stroke="#92400E" stroke-width="2"/>
    <!-- Helix -->
    <path d="M120 30 C100 28 80 38 70 55 C60 72 58 95 62 115 C65 130 75 140 85 145" fill="none" stroke="#92400E" stroke-width="2"/>
    <!-- Inner ear area fill -->
    <path d="M115 50 C105 55 95 68 92 85 C90 100 92 112 98 122 L120 115 C118 100 116 80 115 50z" fill="#F9A8D4" fill-opacity="0.25" stroke="none"/>
    <!-- Antihelix -->
    <path d="M115 50 C105 55 95 68 92 85 C90 100 92 112 98 122" stroke="#D97706" stroke-width="1.5" fill="none" opacity="0.7"/>
    <!-- Tragus -->
    <path d="M82 90 C78 88 75 92 78 98 C80 102 84 100 84 96" fill="#FDBCB4" fill-opacity="0.5" stroke="#92400E" stroke-width="1.5"/>
    <!-- Ear canal -->
    <ellipse cx="88" cy="95" rx="6" ry="8" fill="#374151" fill-opacity="0.35" stroke="#92400E" opacity="0.7"/>
    <!-- Earlobe -->
    <path d="M85 145 C82 155 88 168 100 170 C108 172 112 168 115 180" fill="none" stroke="#92400E" stroke-width="2" opacity="0.7"/>
    <!-- Inner ear hint -->
    <circle cx="88" cy="95" r="3" fill="#1F2937" opacity="0.6" stroke="none"/>
  `,

  skin: `
    <!-- Epidermis layer (skin tone) -->
    <path d="M25 40 C35 38 45 41 55 38 C65 35 75 39 85 37 C95 35 105 38 115 36 C125 34 135 38 145 36 C155 34 165 39 175 40 L175 60 L25 60z" fill="#FDBCB4" fill-opacity="0.6" stroke="#D97706" stroke-width="1.5"/>
    <path d="M25 60 L175 60" stroke="#92400E" stroke-width="2" fill="none"/>
    <!-- Wavy skin surface -->
    <path d="M25 40 C35 38 45 41 55 38 C65 35 75 39 85 37 C95 35 105 38 115 36 C125 34 135 38 145 36 C155 34 165 39 175 40" stroke="#D97706" stroke-width="1.5" fill="none"/>
    <!-- Dermis layer (pink) -->
    <path d="M25 60 L175 60 L175 100 L25 100z" fill="#F8A4A4" fill-opacity="0.4" stroke="none"/>
    <path d="M25 100 L175 100" stroke="#BE185D" stroke-width="1.5" fill="none" opacity="0.7"/>
    <!-- Subcutaneous/fat layer (yellow) -->
    <path d="M25 100 L175 100 L175 145 L25 145z" fill="#FDE68A" fill-opacity="0.35" stroke="none"/>
    <path d="M25 145 L175 145" stroke="#D97706" stroke-width="1" fill="none" opacity="0.55"/>
    <!-- Deep fat layer -->
    <path d="M25 145 L175 145 L175 185 L25 185z" fill="#FDE68A" fill-opacity="0.2" stroke="none"/>
    <!-- Hair follicles (brown) -->
    <path d="M60 60 L58 35 C57 28 62 25 63 30 L62 60" stroke="#92400E" stroke-width="1.5" fill="#92400E" fill-opacity="0.3"/>
    <path d="M120 60 L118 30 C117 22 122 20 123 26 L122 60" stroke="#92400E" stroke-width="1.5" fill="#92400E" fill-opacity="0.3"/>
    <!-- Hair shafts -->
    <path d="M59 35 C56 22 54 12 56 8" stroke="#92400E" stroke-width="1" fill="none" opacity="0.7"/>
    <path d="M119 30 C116 18 118 10 120 5" stroke="#92400E" stroke-width="1" fill="none" opacity="0.7"/>
    <!-- Sweat glands -->
    <path d="M85 80 C82 88 78 92 82 96 C86 100 90 96 88 90 C86 85 88 78 85 80z" fill="#F8A4A4" fill-opacity="0.3" stroke="#BE185D" opacity="0.6"/>
    <!-- Blood vessels (red) -->
    <path d="M40 110 C50 105 60 112 70 108 C80 104 90 110 100 106 C110 102 120 108 130 105 C140 102 150 108 160 110" stroke="#EF4444" stroke-width="1.5" opacity="0.7" fill="none"/>
    <!-- Capillaries -->
    <path d="M70 108 C72 115 68 120 70 125" stroke="#EF4444" stroke-width="0.8" opacity="0.5" fill="none"/>
    <path d="M130 105 C132 112 128 118 130 122" stroke="#EF4444" stroke-width="0.8" opacity="0.5" fill="none"/>
    <!-- Nerve endings -->
    <circle cx="75" cy="80" r="3" fill="#A855F7" opacity="0.5" stroke="#7C3AED" stroke-width="0.5"/>
    <circle cx="140" cy="78" r="3" fill="#A855F7" opacity="0.5" stroke="#7C3AED" stroke-width="0.5"/>
    <!-- Fat cells (yellow) -->
    <circle cx="60" cy="125" r="8" fill="#FDE68A" fill-opacity="0.5" stroke="#D97706" opacity="0.6"/>
    <circle cx="80" cy="128" r="7" fill="#FDE68A" fill-opacity="0.5" stroke="#D97706" opacity="0.6"/>
    <circle cx="100" cy="125" r="8" fill="#FDE68A" fill-opacity="0.5" stroke="#D97706" opacity="0.6"/>
    <circle cx="120" cy="128" r="7" fill="#FDE68A" fill-opacity="0.5" stroke="#D97706" opacity="0.6"/>
    <circle cx="140" cy="125" r="8" fill="#FDE68A" fill-opacity="0.5" stroke="#D97706" opacity="0.6"/>
  `,

  thyroid: `
    <!-- Trachea -->
    <path d="M95 30 L95 170 L105 170 L105 30z" fill="#E5E7EB" fill-opacity="0.35" stroke="#6B7280" stroke-width="1.5"/>
    <!-- Tracheal rings -->
    <path d="M95 45 L105 45" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <path d="M95 55 L105 55" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <path d="M95 65 L105 65" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <path d="M95 130 L105 130" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <path d="M95 140 L105 140" stroke="#9CA3AF" opacity="0.7" fill="none"/>
    <!-- Thyroid - left lobe -->
    <path d="M95 75 C75 78 58 90 55 110 C52 130 65 145 85 145 C92 145 95 140 95 130" fill="#C084FC" fill-opacity="0.35" stroke="#7C3AED" stroke-width="2"/>
    <!-- Thyroid - right lobe -->
    <path d="M105 75 C125 78 142 90 145 110 C148 130 135 145 115 145 C108 145 105 140 105 130" fill="#C084FC" fill-opacity="0.35" stroke="#7C3AED" stroke-width="2"/>
    <!-- Isthmus -->
    <path d="M95 102 L105 102 L105 108 L95 108z" fill="#C084FC" fill-opacity="0.4" stroke="#7C3AED" stroke-width="2"/>
    <!-- Follicles -->
    <circle cx="75" cy="108" r="5" fill="#DDD6FE" fill-opacity="0.5" stroke="#7C3AED" opacity="0.65"/>
    <circle cx="82" cy="125" r="4" fill="#DDD6FE" fill-opacity="0.5" stroke="#7C3AED" opacity="0.6"/>
    <circle cx="68" cy="120" r="4.5" fill="#DDD6FE" fill-opacity="0.5" stroke="#7C3AED" opacity="0.6"/>
    <circle cx="125" cy="108" r="5" fill="#DDD6FE" fill-opacity="0.5" stroke="#7C3AED" opacity="0.65"/>
    <circle cx="118" cy="125" r="4" fill="#DDD6FE" fill-opacity="0.5" stroke="#7C3AED" opacity="0.6"/>
    <circle cx="132" cy="120" r="4.5" fill="#DDD6FE" fill-opacity="0.5" stroke="#7C3AED" opacity="0.6"/>
    <!-- Blood supply -->
    <path d="M75 75 C70 82 66 92 65 100" stroke="#EF4444" stroke-width="1" opacity="0.6" fill="none"/>
    <path d="M125 75 C130 82 134 92 135 100" stroke="#EF4444" stroke-width="1" opacity="0.6" fill="none"/>
  `,

  joint: `
    <!-- Upper bone shaft (femur-like) -->
    <path d="M85 20 L85 80 L115 80 L115 20z" fill="#F5F5DC" fill-opacity="0.5" stroke="#78716C" stroke-width="2"/>
    <!-- Bone head -->
    <path d="M70 95 C65 100 62 110 65 118 C68 126 78 132 100 132 C122 132 132 126 135 118 C138 110 135 100 130 95 L120 95 C120 90 115 85 115 80 L85 80 C85 85 80 90 80 95z" fill="#F5F5DC" fill-opacity="0.55" stroke="#78716C" stroke-width="2"/>
    <!-- Cartilage (blue) -->
    <path d="M72 120 C80 125 90 128 100 128 C110 128 120 125 128 120" stroke="#60A5FA" stroke-width="3" opacity="0.6" fill="none" stroke-linecap="round"/>
    <!-- Joint space / synovial fluid (yellow) -->
    <path d="M68 132 L132 132" stroke="none" fill="none"/>
    <ellipse cx="100" cy="132" rx="28" ry="5" fill="#FDE68A" opacity="0.5" stroke="none"/>
    <!-- Lower bone (tibia-like) -->
    <path d="M72 138 C68 142 65 150 65 158 L65 162 C65 168 72 174 80 174 C88 174 92 168 92 162 L92 195" fill="#F5F5DC" fill-opacity="0.45" stroke="#78716C" stroke-width="2"/>
    <path d="M128 138 C132 142 135 150 135 158 L135 162 C135 168 128 174 120 174 C112 174 108 168 108 162 L108 195" fill="#F5F5DC" fill-opacity="0.45" stroke="#78716C" stroke-width="2"/>
    <!-- Ligaments -->
    <path d="M78 100 C82 115 85 125 88 135" stroke="#D97706" stroke-width="1.5" opacity="0.55" fill="none"/>
    <path d="M122 100 C118 115 115 125 112 135" stroke="#D97706" stroke-width="1.5" opacity="0.55" fill="none"/>
  `,

  intestine: `
    <!-- Large intestine frame (darker pink) -->
    <path d="M40 160 L40 50 C40 35 55 25 100 25 C145 25 160 35 160 50 L160 160 C160 175 145 180 100 180 C55 180 40 175 40 160z" fill="#F87171" fill-opacity="0.2" stroke="#B91C1C" stroke-width="2.5"/>
    <!-- Small intestine loops (lighter pink fill) -->
    <path d="M55 40 C55 40 145 40 145 55 C145 70 55 65 55 80 C55 95 145 90 145 105 C145 120 55 115 55 130 C55 145 145 140 145 155" fill="none" stroke="#FB7185" stroke-width="3" opacity="0.7" stroke-linecap="round"/>
    <!-- Small intestine fill areas -->
    <path d="M60 42 C80 42 120 42 140 48 C142 58 130 62 100 62 C70 62 58 66 56 72 C56 82 70 86 100 86 C130 86 142 90 142 98 C142 108 130 112 100 112 C70 112 58 116 56 122 C56 132 70 136 100 136 C130 136 142 140 142 150" fill="#FCA5A5" fill-opacity="0.25" stroke="none"/>
    <!-- Haustra marks on large intestine -->
    <path d="M35 70 L45 70" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <path d="M35 90 L45 90" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <path d="M35 110 L45 110" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <path d="M35 130 L45 130" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <path d="M155 70 L165 70" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <path d="M155 90 L165 90" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <path d="M155 110 L165 110" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <path d="M155 130 L165 130" stroke="#B91C1C" opacity="0.55" fill="none"/>
    <!-- Appendix -->
    <path d="M45 160 C42 170 38 178 35 182" stroke="#F87171" stroke-width="2" opacity="0.65" fill="none"/>
  `,

  throat: `
    <!-- Neck outline (skin tone) -->
    <path d="M70 20 C65 40 62 60 60 80 C58 100 56 120 55 140 C54 160 55 175 58 185 L142 185 C145 175 146 160 145 140 C144 120 142 100 140 80 C138 60 135 40 130 20z" fill="#FDBCB4" fill-opacity="0.15" stroke="#D97706" stroke-width="1.5" opacity="0.55"/>
    <!-- Pharynx -->
    <path d="M82 30 C78 40 76 55 78 70 L122 70 C124 55 122 40 118 30z" fill="#F9A8D4" fill-opacity="0.25" stroke="#BE185D" stroke-width="1.5" opacity="0.7"/>
    <!-- Larynx (voice box) -->
    <path d="M78 70 C75 75 74 82 76 90 C78 98 85 102 100 102 C115 102 122 98 124 90 C126 82 125 75 122 70" fill="#F9A8D4" fill-opacity="0.35" stroke="#9D174D" stroke-width="2"/>
    <!-- Vocal cords -->
    <path d="M84 85 L100 92 L116 85" stroke="#EC4899" stroke-width="1.5" fill="none" opacity="0.8"/>
    <!-- Epiglottis -->
    <path d="M92 68 C95 62 100 60 105 62 C108 64 108 68 105 70 L95 70 C92 68 92 66 92 68z" fill="#F472B6" fill-opacity="0.4" stroke="#9D174D" stroke-width="1.5"/>
    <!-- Trachea -->
    <path d="M92 102 L90 180 L110 180 L108 102z" fill="#E5E7EB" fill-opacity="0.3" stroke="#6B7280" stroke-width="1.5"/>
    <!-- Tracheal rings -->
    <path d="M92 115 L108 115" stroke="#9CA3AF" opacity="0.6" fill="none"/>
    <path d="M91 130 L109 130" stroke="#9CA3AF" opacity="0.6" fill="none"/>
    <path d="M91 145 L109 145" stroke="#9CA3AF" opacity="0.6" fill="none"/>
    <path d="M90 160 L110 160" stroke="#9CA3AF" opacity="0.6" fill="none"/>
    <!-- Thyroid gland hint -->
    <path d="M85 108 C78 112 75 120 78 128 C80 132 88 134 92 130" fill="#C084FC" fill-opacity="0.25" stroke="#7C3AED" opacity="0.6"/>
    <path d="M115 108 C122 112 125 120 122 128 C120 132 112 134 108 130" fill="#C084FC" fill-opacity="0.25" stroke="#7C3AED" opacity="0.6"/>
  `,

  pancreas: `
    <!-- Pancreas body -->
    <path d="M45 95 C50 85 65 80 85 82 C100 84 110 88 125 90 C140 92 155 90 165 95 C172 98 174 108 168 115 C160 124 145 125 130 122 C115 119 105 118 90 120 C75 122 60 120 50 115 C42 110 40 102 45 95z" fill="#FDE68A" fill-opacity="0.45" stroke="#92400E" stroke-width="2"/>
    <!-- Pancreatic duct -->
    <path d="M60 105 C80 102 100 103 120 105 C140 107 155 108 165 105" stroke="#D97706" stroke-width="1.5" fill="none" opacity="0.7"/>
    <!-- Head of pancreas (darker) -->
    <circle cx="55" cy="105" r="15" fill="#F59E0B" opacity="0.4" stroke="none"/>
    <!-- Islets of Langerhans (blue) -->
    <circle cx="80" cy="98" r="3.5" fill="#60A5FA" opacity="0.5" stroke="#3B82F6" stroke-width="0.5"/>
    <circle cx="105" cy="102" r="4" fill="#60A5FA" opacity="0.5" stroke="#3B82F6" stroke-width="0.5"/>
    <circle cx="130" cy="100" r="3.5" fill="#60A5FA" opacity="0.5" stroke="#3B82F6" stroke-width="0.5"/>
    <!-- Duodenum curve -->
    <path d="M45 80 C35 85 28 100 30 115 C32 130 40 140 50 142 C58 143 62 138 60 130 C58 120 52 112 50 105" fill="#FCA5A5" fill-opacity="0.25" stroke="#9D174D" stroke-width="1.5" opacity="0.65"/>
    <!-- Blood vessels -->
    <path d="M100 80 L100 70" stroke="#EF4444" stroke-width="1" opacity="0.6" fill="none"/>
    <path d="M100 125 L100 140" stroke="#EF4444" stroke-width="1" opacity="0.6" fill="none"/>
    <!-- Bile duct (green) -->
    <path d="M48 70 L50 90" stroke="#22C55E" stroke-width="1.5" opacity="0.6" fill="none"/>
  `,

  bladder: `
    <!-- Bladder body -->
    <path d="M60 70 C40 80 30 105 32 130 C34 155 50 175 75 180 C90 183 110 183 125 180 C150 175 166 155 168 130 C170 105 160 80 140 70" fill="#FBBF24" fill-opacity="0.2" stroke="#92400E" stroke-width="2"/>
    <!-- Inner bladder wall -->
    <path d="M68 78 C52 87 42 108 44 130 C46 150 58 168 78 174 C90 176 110 176 122 174 C142 168 154 150 156 130 C158 108 148 87 132 78" fill="#FDE68A" fill-opacity="0.2" stroke="none"/>
    <!-- Ureters -->
    <path d="M75 30 C72 45 68 55 65 70" stroke="#FDE68A" stroke-width="2.5" opacity="0.7" fill="none"/>
    <path d="M125 30 C128 45 132 55 135 70" stroke="#FDE68A" stroke-width="2.5" opacity="0.7" fill="none"/>
    <!-- Ureteral openings -->
    <circle cx="65" cy="72" r="3" fill="#F59E0B" fill-opacity="0.5" stroke="#92400E" opacity="0.6"/>
    <circle cx="135" cy="72" r="3" fill="#F59E0B" fill-opacity="0.5" stroke="#92400E" opacity="0.6"/>
    <!-- Internal folds -->
    <path d="M55 100 C70 95 90 98 100 100 C110 102 130 95 145 100" stroke="#D97706" fill="none" opacity="0.5"/>
    <path d="M50 125 C68 120 88 122 100 125 C112 128 132 120 150 125" stroke="#D97706" fill="none" opacity="0.5"/>
    <!-- Urethra -->
    <path d="M95 178 C96 185 98 190 100 195 C102 190 104 185 105 178" fill="#FDE68A" fill-opacity="0.3" stroke="#92400E" stroke-width="1.5" opacity="0.7"/>
    <!-- Trigone -->
    <path d="M65 72 L100 175 L135 72" stroke="#D97706" fill="#FBBF24" fill-opacity="0.1" opacity="0.4" stroke-dasharray="4 4"/>
    <!-- Detrusor muscle hint -->
    <path d="M45 95 C42 110 42 130 48 150" stroke="#B45309" opacity="0.45" fill="none"/>
    <path d="M155 95 C158 110 158 130 152 150" stroke="#B45309" opacity="0.45" fill="none"/>
  `,

  immune: `
    <!-- Shield fill -->
    <path d="M100 20 L50 50 L50 100 C50 145 70 170 100 185 C130 170 150 145 150 100 L150 50 L100 20z" fill="#DBEAFE" fill-opacity="0.35" stroke="#1E40AF" stroke-width="2"/>
    <!-- Inner shield glow -->
    <path d="M100 35 L60 58 L60 100 C60 138 76 160 100 172 C124 160 140 138 140 100 L140 58 L100 35z" fill="#3B82F6" fill-opacity="0.15" stroke="none"/>
    <!-- Cross/plus (red) -->
    <path d="M92 70 L92 140 L108 140 L108 70z" fill="#EF4444" fill-opacity="0.6" stroke="#B91C1C" stroke-width="1"/>
    <path d="M70 97 L130 97 L130 113 L70 113z" fill="#EF4444" fill-opacity="0.6" stroke="#B91C1C" stroke-width="1"/>
    <!-- Antibody shapes (white/blue) -->
    <path d="M65 65 L60 55 M65 65 L70 55 M65 65 L65 80" stroke="#60A5FA" stroke-width="1.5" fill="none" opacity="0.65"/>
    <path d="M135 65 L130 55 M135 65 L140 55 M135 65 L135 80" stroke="#60A5FA" stroke-width="1.5" fill="none" opacity="0.65"/>
    <!-- Cell markers (green = healthy) -->
    <circle cx="78" cy="82" r="5" fill="#22C55E" opacity="0.5" stroke="#15803D" stroke-width="0.5"/>
    <circle cx="122" cy="82" r="5" fill="#22C55E" opacity="0.5" stroke="#15803D" stroke-width="0.5"/>
    <circle cx="78" cy="132" r="5" fill="#22C55E" opacity="0.5" stroke="#15803D" stroke-width="0.5"/>
    <circle cx="122" cy="132" r="5" fill="#22C55E" opacity="0.5" stroke="#15803D" stroke-width="0.5"/>
  `,

  bone: `
    <!-- Long bone -->
    <path d="M80 30 C70 30 62 38 62 48 C62 55 68 60 72 62 L72 138 C68 140 62 145 62 152 C62 162 70 170 80 170 L120 170 C130 170 138 162 138 152 C138 145 132 140 128 138 L128 62 C132 60 138 55 138 48 C138 38 130 30 120 30 L80 30z" fill="#F5F5DC" fill-opacity="0.55" stroke="#78716C" stroke-width="2"/>
    <!-- Compact bone (outer) -->
    <path d="M72 62 L72 138" stroke="#A8A29E" stroke-width="3" fill="none" opacity="0.4"/>
    <path d="M128 62 L128 138" stroke="#A8A29E" stroke-width="3" fill="none" opacity="0.4"/>
    <!-- Epiphyseal line top -->
    <path d="M72 62 L128 62" stroke="#D97706" stroke-width="1.5" opacity="0.65" fill="none"/>
    <!-- Epiphyseal line bottom -->
    <path d="M72 138 L128 138" stroke="#D97706" stroke-width="1.5" opacity="0.65" fill="none"/>
    <!-- Medullary cavity (yellow marrow) -->
    <path d="M82 68 L82 132 L118 132 L118 68z" fill="#FDE68A" fill-opacity="0.35" stroke="none"/>
    <!-- Spongy bone hints (top) -->
    <path d="M75 42 C85 45 95 42 100 40 C105 42 115 45 125 42" stroke="#A8A29E" fill="none" opacity="0.65"/>
    <path d="M78 50 C88 52 98 50 108 48 C115 50 122 52 125 50" stroke="#A8A29E" fill="none" opacity="0.5"/>
    <!-- Spongy bone hints (bottom) -->
    <path d="M75 158 C85 155 95 158 100 160 C105 158 115 155 125 158" stroke="#A8A29E" fill="none" opacity="0.65"/>
    <path d="M78 152 C88 150 98 152 108 154 C115 152 122 150 125 152" stroke="#A8A29E" fill="none" opacity="0.5"/>
    <!-- Periosteum -->
    <path d="M70 70 L70 130" stroke="#D97706" stroke-width="1" opacity="0.5" stroke-dasharray="4 4" fill="none"/>
    <path d="M130 70 L130 130" stroke="#D97706" stroke-width="1" opacity="0.5" stroke-dasharray="4 4" fill="none"/>
    <!-- Bone marrow dots (red) -->
    <circle cx="90" cy="90" r="2.5" fill="#EF4444" opacity="0.5" stroke="none"/>
    <circle cx="110" cy="100" r="2.5" fill="#EF4444" opacity="0.5" stroke="none"/>
    <circle cx="95" cy="115" r="2.5" fill="#EF4444" opacity="0.5" stroke="none"/>
  `,

  head: `
    <!-- Skull outline -->
    <path d="M100 25 C60 25 40 55 40 85 C40 110 50 130 65 142 L72 148 L72 165 L128 165 L128 148 L135 142 C150 130 160 110 160 85 C160 55 140 25 100 25z" fill="#F5F5DC" fill-opacity="0.4" stroke="#78716C" stroke-width="2"/>
    <!-- Jaw -->
    <path d="M72 148 C78 158 88 165 100 165 C112 165 122 158 128 148" stroke="#A8A29E" fill="none" opacity="0.65"/>
    <!-- Eye sockets -->
    <ellipse cx="78" cy="90" rx="15" ry="12" fill="#374151" fill-opacity="0.15" stroke="#78716C" opacity="0.6"/>
    <ellipse cx="122" cy="90" rx="15" ry="12" fill="#374151" fill-opacity="0.15" stroke="#78716C" opacity="0.6"/>
    <!-- Nose -->
    <path d="M100 95 L95 115 L105 115 L100 95z" fill="#D6D3D1" fill-opacity="0.3" stroke="#78716C" opacity="0.6"/>
    <!-- Cranial sutures -->
    <path d="M100 25 L100 60" stroke="#A8A29E" opacity="0.65" stroke-dasharray="3 3" fill="none"/>
    <path d="M55 70 C70 65 85 62 100 60 C115 62 130 65 145 70" stroke="#A8A29E" opacity="0.65" stroke-dasharray="3 3" fill="none"/>
    <!-- Temporal region -->
    <path d="M45 80 C48 95 50 110 55 120" stroke="#A8A29E" opacity="0.5" fill="none"/>
    <path d="M155 80 C152 95 150 110 145 120" stroke="#A8A29E" opacity="0.5" fill="none"/>
    <!-- Brain hint through skull -->
    <path d="M60 60 C70 55 85 52 100 52 C115 52 130 55 140 60" fill="#FDA4AF" fill-opacity="0.15" stroke="none"/>
  `,

  body: `
    <!-- Head (skin tone) -->
    <circle cx="100" cy="35" r="18" fill="#FDBCB4" fill-opacity="0.5" stroke="#92400E" stroke-width="2"/>
    <!-- Neck -->
    <path d="M93 53 L93 65 L107 65 L107 53z" fill="#FDBCB4" fill-opacity="0.35" stroke="#92400E" stroke-width="1.5"/>
    <!-- Torso (blue clothing hint) -->
    <path d="M70 65 L65 130 L80 135 L100 140 L120 135 L135 130 L130 65z" fill="#DBEAFE" fill-opacity="0.35" stroke="#1E40AF" stroke-width="2"/>
    <!-- Shoulders -->
    <path d="M70 65 L50 72" stroke="#1E40AF" stroke-width="2" fill="none"/>
    <path d="M130 65 L150 72" stroke="#1E40AF" stroke-width="2" fill="none"/>
    <!-- Arms (skin tone) -->
    <path d="M50 72 L42 115 L38 145" stroke="#D4A188" stroke-width="3" opacity="0.7" fill="none" stroke-linecap="round"/>
    <path d="M150 72 L158 115 L162 145" stroke="#D4A188" stroke-width="3" opacity="0.7" fill="none" stroke-linecap="round"/>
    <!-- Hands -->
    <circle cx="38" cy="147" r="4" fill="#FDBCB4" fill-opacity="0.45" stroke="#D4A188" stroke-width="1"/>
    <circle cx="162" cy="147" r="4" fill="#FDBCB4" fill-opacity="0.45" stroke="#D4A188" stroke-width="1"/>
    <!-- Legs (skin tone) -->
    <path d="M85 135 L78 170 L75 195" stroke="#D4A188" stroke-width="3" opacity="0.7" fill="none" stroke-linecap="round"/>
    <path d="M115 135 L122 170 L125 195" stroke="#D4A188" stroke-width="3" opacity="0.7" fill="none" stroke-linecap="round"/>
    <!-- Spine center line -->
    <path d="M100 65 L100 140" stroke="#6B7280" opacity="0.4" stroke-dasharray="3 3" fill="none"/>
    <!-- Ribcage hint on torso -->
    <path d="M78 80 L100 85 L122 80" stroke="#93C5FD" opacity="0.5" fill="none"/>
    <path d="M75 95 L100 100 L125 95" stroke="#93C5FD" opacity="0.5" fill="none"/>
    <!-- Pelvis -->
    <path d="M80 130 C90 140 110 140 120 130" stroke="#93C5FD" opacity="0.4" fill="none"/>
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
