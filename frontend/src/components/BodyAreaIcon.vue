<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 64 64"
    fill="none"
    :stroke="color"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
    v-html="iconPath"
  />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  area: { type: String, default: 'body' },
  size: { type: [Number, String], default: 48 },
  color: { type: String, default: 'currentColor' },
})

// Clinical line-art SVG paths for body areas
const iconMap = {
  // HEAD / BRAIN — detailed brain with folds and neural connections
  head: `<path d="M32 6c-12 0-18 9-18 20 0 6 2 11 5 14l3 4v8h20v-8l3-4c3-3 5-8 5-14 0-11-6-20-18-20z"/>
         <path d="M22 24c2 4 6 6 10 6s8-2 10-6" opacity="0.4"/>
         <path d="M20 18c4-3 8-4 12-4s8 1 12 4" opacity="0.4"/>
         <path d="M32 16v10" opacity="0.3"/>
         <circle cx="26" cy="20" r="1.5" opacity="0.3"/>
         <circle cx="38" cy="20" r="1.5" opacity="0.3"/>`,
  brain: `<!-- Brain with neural network pattern -->
          <path d="M32 6c-12 0-18 9-18 20 0 6 2 11 5 14l3 4v8h20v-8l3-4c3-3 5-8 5-14 0-11-6-20-18-20z"/>
          <!-- Brain hemispheres -->
          <path d="M32 8v38" opacity="0.2" stroke-dasharray="2 2"/>
          <!-- Left hemisphere folds -->
          <path d="M18 22c4-1 8 1 10 4" opacity="0.5"/>
          <path d="M16 30c5 0 9 2 12 0" opacity="0.5"/>
          <path d="M20 18c3-1 6 0 8 2" opacity="0.4"/>
          <!-- Right hemisphere folds -->
          <path d="M46 22c-4-1-8 1-10 4" opacity="0.5"/>
          <path d="M48 30c-5 0-9 2-12 0" opacity="0.5"/>
          <path d="M44 18c-3-1-6 0-8 2" opacity="0.4"/>
          <!-- Neural nodes -->
          <circle cx="24" cy="20" r="2" opacity="0.35" fill="currentColor" stroke="none"/>
          <circle cx="40" cy="20" r="2" opacity="0.35" fill="currentColor" stroke="none"/>
          <circle cx="28" cy="30" r="1.5" opacity="0.3" fill="currentColor" stroke="none"/>
          <circle cx="36" cy="30" r="1.5" opacity="0.3" fill="currentColor" stroke="none"/>
          <circle cx="32" cy="24" r="2" opacity="0.4" fill="currentColor" stroke="none"/>
          <!-- Neural connections -->
          <path d="M24 20l8 4" opacity="0.2"/>
          <path d="M40 20l-8 4" opacity="0.2"/>
          <path d="M28 30l4-6" opacity="0.2"/>
          <path d="M36 30l-4-6" opacity="0.2"/>
          <!-- Brainstem -->
          <path d="M29 42c0-3 1-5 3-6 2 1 3 3 3 6" opacity="0.4"/>`,
  // NERVE / NEUROMUSCULAR — nerve pathway with synapses
  nerve: `<!-- Spinal cord -->
          <path d="M32 6v20" stroke-width="2.5"/>
          <!-- Main nerve branches -->
          <path d="M32 14l-14 12" opacity="0.8"/>
          <path d="M32 14l14 12" opacity="0.8"/>
          <path d="M32 22l-10 18" opacity="0.6"/>
          <path d="M32 22l10 18" opacity="0.6"/>
          <!-- Nerve endings -->
          <path d="M18 26l-6 4m0-2l-4 6" opacity="0.4"/>
          <path d="M46 26l6 4m0-2l4 6" opacity="0.4"/>
          <path d="M22 40l-6 8m-1-4l-4 4" opacity="0.4"/>
          <path d="M42 40l6 8m1-4l4 4" opacity="0.4"/>
          <!-- Synaptic nodes -->
          <circle cx="32" cy="10" r="3" opacity="0.5" fill="currentColor" stroke="none"/>
          <circle cx="32" cy="22" r="2.5" opacity="0.4" fill="currentColor" stroke="none"/>
          <circle cx="18" cy="26" r="2" opacity="0.35" fill="currentColor" stroke="none"/>
          <circle cx="46" cy="26" r="2" opacity="0.35" fill="currentColor" stroke="none"/>
          <circle cx="22" cy="40" r="2" opacity="0.3" fill="currentColor" stroke="none"/>
          <circle cx="42" cy="40" r="2" opacity="0.3" fill="currentColor" stroke="none"/>`,

  // LIPS / MOUTH — lips outline
  lips: `<path d="M16 32c0 0 4-6 16-6s16 6 16 6"/>
         <path d="M16 32c0 0 4 8 16 8s16-8 16-8"/>
         <path d="M32 26v0" stroke-width="0"/>
         <path d="M24 32c2-2 5-3 8-3s6 1 8 3" opacity="0.6"/>`,
  mouth: `<path d="M16 32c0 0 4-6 16-6s16 6 16 6"/>
          <path d="M16 32c0 0 4 8 16 8s16-8 16-8"/>
          <path d="M24 32c2-2 5-3 8-3s6 1 8 3" opacity="0.6"/>`,

  // EYE — eye with iris and pupil
  eye: `<path d="M8 32c0 0 8-14 24-14s24 14 24 14c0 0-8 14-24 14S8 32 8 32z"/>
        <circle cx="32" cy="32" r="8"/>
        <circle cx="32" cy="32" r="3.5" fill="currentColor" stroke="none"/>`,
  eyes: `<path d="M8 32c0 0 8-14 24-14s24 14 24 14c0 0-8 14-24 14S8 32 8 32z"/>
         <circle cx="32" cy="32" r="8"/>
         <circle cx="32" cy="32" r="3.5" fill="currentColor" stroke="none"/>`,

  // EAR — outer ear shape
  ear: `<path d="M36 12c8 0 14 6 14 14 0 6-3 10-6 14-2 3-4 6-4 10v4"/>
        <path d="M36 12c-4 0-8 4-8 10 0 4 2 7 5 9"/>
        <path d="M33 31c2 2 4 1 5-1s0-5-2-6"/>`,

  // NOSE — nose front view
  nose: `<path d="M32 10v20"/>
         <path d="M32 30c-4 4-10 6-12 4s0-6 4-8"/>
         <path d="M32 30c4 4 10 6 12 4s0-6-4-8"/>
         <circle cx="26" cy="38" r="2" opacity="0.4"/>
         <circle cx="38" cy="38" r="2" opacity="0.4"/>`,

  // THROAT / NECK — neck with throat indication
  throat: `<path d="M22 8h20v0c0 8-4 12-4 20v12c0 4-2 8-6 8s-6-4-6-8V28c0-8-4-12-4-20z"/>
           <path d="M28 20h8" opacity="0.5"/>
           <path d="M26 26h12" opacity="0.5"/>`,

  // TOOTH / DENTAL
  tooth: `<path d="M24 14c-4 0-8 4-8 10 0 4 2 8 4 14 1 4 3 8 4 12 1-4 3-8 4-12h0c1 4 3 8 4 12 1-4 3-8 4-12 2-6 4-10 4-14 0-6-4-10-8-10h-8z"/>
          <path d="M32 14v8" opacity="0.4"/>`,

  // CHEST / HEART — chest with heart
  chest: `<path d="M16 20h32v24c0 4-4 8-8 8H24c-4 0-8-4-8-8V20z"/>
          <path d="M16 20c0-6 4-10 8-10h16c4 0 8 4 8 10"/>
          <path d="M28 30c-4-4-8-2-8 2s4 6 12 12c8-6 12-8 12-12s-4-6-8-2l-4 4-4-4z" opacity="0.6"/>`,
  heart: `<path d="M28 30c-4-4-8-2-8 2s4 6 12 12c8-6 12-8 12-12s-4-6-8-2l-4 4-4-4z"/>
          <path d="M20 28v-8c0-4 4-8 8-8h8c4 0 8 4 8 8v8"/>`,

  // LUNGS — lung pair
  lungs: `<path d="M32 10v30"/>
          <path d="M32 18c-4 2-8 6-10 12-2 8-2 14 0 16 2 2 6 2 10-2"/>
          <path d="M32 18c4 2 8 6 10 12 2 8 2 14 0 16-2 2-6 2-10-2"/>
          <path d="M26 28c-1 2-2 5-2 8" opacity="0.4"/>
          <path d="M38 28c1 2 2 5 2 8" opacity="0.4"/>`,

  // STOMACH / DIGESTIVE
  stomach: `<path d="M24 10h8c2 0 4 2 4 4v6c0 6-4 10-4 16 0 4 2 8 6 10h-8c-8 0-14-6-14-14v-6c0-6-2-10 0-14 1-2 4-2 8-2z"/>
            <path d="M20 22h16" opacity="0.4"/>`,
  digestive: `<path d="M24 10h8c2 0 4 2 4 4v6c0 6-4 10-4 16 0 4 2 8 6 10h-8c-8 0-14-6-14-14v-6c0-6-2-10 0-14 1-2 4-2 8-2z"/>
              <path d="M20 22h16" opacity="0.4"/>`,

  // LIVER
  liver: `<path d="M14 22c0-4 4-8 10-8h12c6 0 12 4 12 10 0 8-6 16-16 20-4 2-8 2-10 0-4-4-8-12-8-22z"/>
          <path d="M32 14v20" opacity="0.4"/>`,

  // KIDNEY
  kidney: `<path d="M22 16c-6 0-10 6-10 14s4 16 10 18c4 2 8-2 8-8v-4c0-4 2-6 4-6s4 2 4 6v4c0 6 4 10 8 8 6-2 10-10 10-18s-4-14-10-14c-4 0-6 4-6 8v2c0 2-2 4-4 4h-4c-2 0-4-2-4-4v-2c0-4-2-8-6-8z"/>`,
  kidneys: `<path d="M22 16c-6 0-10 6-10 14s4 16 10 18c4 2 8-2 8-8v-4c0-4 2-6 4-6s4 2 4 6v4c0 6 4 10 8 8 6-2 10-10 10-18s-4-14-10-14c-4 0-6 4-6 8v2c0 2-2 4-4 4h-4c-2 0-4-2-4-4v-2c0-4-2-8-6-8z"/>`,

  // SKIN — arm with skin layers
  skin: `<path d="M20 12h24v40H20z" rx="4"/>
         <path d="M20 22h24" opacity="0.3"/>
         <path d="M20 32h24" opacity="0.3"/>
         <circle cx="28" cy="17" r="1.5" opacity="0.5"/>
         <circle cx="36" cy="27" r="1.5" opacity="0.5"/>
         <circle cx="30" cy="37" r="1.5" opacity="0.5"/>`,

  // MUSCLES / JOINTS — flexed arm
  muscles: `<path d="M18 48c0-8 4-12 8-16 2-2 2-6 0-8l-4-6c-2-4 0-8 4-8 2 0 4 2 6 4l8 10c2 4 6 6 10 6h2"/>
            <path d="M30 24c4-2 10 0 12 4 2 6-2 10-6 12"/>
            <path d="M22 40c2-2 6-2 8 0"/>`,
  joints: `<path d="M18 48c0-8 4-12 8-16 2-2 2-6 0-8l-4-6c-2-4 0-8 4-8 2 0 4 2 6 4l8 10c2 4 6 6 10 6h2"/>
           <path d="M30 24c4-2 10 0 12 4 2 6-2 10-6 12"/>`,

  // BONE / SKELETON
  bone: `<path d="M22 14c-4-4-10-2-10 4 0 4 4 6 6 6v16c-2 0-6 2-6 6 0 6 6 8 10 4 2-2 4-2 6 0h4c2 2 4 2 6 0 4 4 10 2 10-4 0-4-4-6-6-6V24c2 0 6-2 6-6 0-6-6-8-10-4-2 2-4 2-6 0h-4c-2-2-4-2-6 0z"/>`,

  // HAND
  hand: `<path d="M24 34V16c0-2 2-4 4-4s4 2 4 4v18"/>
         <path d="M32 34V14c0-2 2-4 4-4s4 2 4 4v14"/>
         <path d="M40 28V18c0-2 2-4 4-4s4 2 4 4v14c0 10-6 18-14 20"/>
         <path d="M24 34V22c0-2-2-4-4-4s-4 2-4 4v10c0 10 6 18 14 20"/>`,

  // FOOT
  foot: `<path d="M18 12v24c0 6 2 10 4 12h20c4 0 8-4 8-8 0-6-4-8-10-8h-4c-2 0-4-2-4-4V12c0-2-2-4-4-4h-6c-2 0-4 2-4 4z"/>
         <path d="M42 40h4" opacity="0.4"/>
         <path d="M42 44h2" opacity="0.4"/>`,

  // SPINE / BACK
  spine: `<path d="M32 8v48"/>
          <path d="M26 14h12" opacity="0.6"/>
          <path d="M24 22h16" opacity="0.6"/>
          <path d="M22 30h20" opacity="0.6"/>
          <path d="M24 38h16" opacity="0.6"/>
          <path d="M26 46h12" opacity="0.6"/>
          <circle cx="32" cy="14" r="2" opacity="0.3"/>
          <circle cx="32" cy="22" r="2.5" opacity="0.3"/>
          <circle cx="32" cy="30" r="3" opacity="0.3"/>
          <circle cx="32" cy="38" r="2.5" opacity="0.3"/>
          <circle cx="32" cy="46" r="2" opacity="0.3"/>`,

  // THYROID / ENDOCRINE
  thyroid: `<path d="M32 10v16"/>
            <path d="M32 26c-8 0-14 4-14 10s6 10 14 10 14-4 14-10-6-10-14-10z"/>
            <path d="M32 26c-2 0-4 2-4 6s2 8 4 8 4-4 4-8-2-6-4-6z" opacity="0.4"/>`,
  endocrine: `<path d="M32 10v16"/>
              <path d="M32 26c-8 0-14 4-14 10s6 10 14 10 14-4 14-10-6-10-14-10z"/>
              <path d="M32 26c-2 0-4 2-4 6s2 8 4 8 4-4 4-8-2-6-4-6z" opacity="0.4"/>`,

  // IMMUNE / SHIELD
  immune: `<path d="M32 6L12 16v12c0 14 8 22 20 28 12-6 20-14 20-28V16L32 6z"/>
           <path d="M24 32l6 6 12-12" stroke-width="2.5"/>`,

  // PELVIS / REPRODUCTIVE
  pelvis: `<path d="M16 20c0-4 4-8 8-8h16c4 0 8 4 8 8v8c0 8-4 16-16 20-12-4-16-12-16-20v-8z"/>
           <path d="M28 28h8" opacity="0.5"/>
           <path d="M32 24v8" opacity="0.5"/>`,

  // GENERIC BODY — full body outline
  body: `<circle cx="32" cy="12" r="6"/>
         <path d="M32 18v16"/>
         <path d="M20 24h24"/>
         <path d="M24 56l8-22 8 22"/>`,

  // FACE — front face
  face: `<path d="M18 28c0-10 6-18 14-18s14 8 14 18c0 8-4 16-14 20-10-4-14-12-14-20z"/>
         <circle cx="26" cy="26" r="2" fill="currentColor" stroke="none"/>
         <circle cx="38" cy="26" r="2" fill="currentColor" stroke="none"/>
         <path d="M28 36c2 2 4 2 8 0" opacity="0.6"/>`,

  // TONGUE
  tongue: `<path d="M20 18h24v4c0 12-4 24-12 28-8-4-12-16-12-28V18z"/>
           <path d="M32 18v24" opacity="0.4"/>`,

  // BREAST
  breast: `<path d="M16 18c0 12 6 22 16 28 10-6 16-16 16-28"/>
           <path d="M16 18h32"/>
           <circle cx="32" cy="32" r="3" opacity="0.4"/>`,

  // BLADDER / URINARY
  bladder: `<path d="M22 18c-4 4-6 10-6 16 0 8 6 16 16 16s16-8 16-16c0-6-2-12-6-16"/>
            <path d="M28 8v10c0 2 2 4 4 4s4-2 4-4V8"/>`,
  urinary: `<path d="M22 18c-4 4-6 10-6 16 0 8 6 16 16 16s16-8 16-16c0-6-2-12-6-16"/>
            <path d="M28 8v10c0 2 2 4 4 4s4-2 4-4V8"/>`,
}

// Keyword-to-icon mapping for auto-detection from diagnosis/specialty text
const keywordMap = {
  lip: 'lips', lips: 'lips', oral: 'lips', mouth: 'mouth', cheilitis: 'lips',
  eye: 'eye', eyes: 'eyes', vision: 'eye', ophthalm: 'eye', retina: 'eye', glaucoma: 'eye',
  ear: 'ear', hearing: 'ear', tinnitus: 'ear', otitis: 'ear',
  nose: 'nose', nasal: 'nose', sinus: 'nose', rhinitis: 'nose',
  throat: 'throat', laryn: 'throat', pharyn: 'throat', tonsil: 'throat', vocal: 'throat',
  head: 'head', brain: 'brain', neuro: 'nerve', migraine: 'head', headache: 'head', cognitive: 'brain',
  neuromuscular: 'nerve', neuropathy: 'nerve', nerve: 'nerve', peripheral: 'nerve', cmt: 'nerve', charcot: 'nerve', motor: 'nerve', sensory: 'nerve',
  tooth: 'tooth', dental: 'tooth', teeth: 'tooth', gum: 'tooth',
  tongue: 'tongue', glossitis: 'tongue',
  face: 'face', facial: 'face', acne: 'face',
  chest: 'chest', heart: 'heart', cardiac: 'heart', cardio: 'heart', coronary: 'heart', angina: 'heart',
  lung: 'lungs', pulmonary: 'lungs', respiratory: 'lungs', breath: 'lungs', asthma: 'lungs', bronch: 'lungs', pneumonia: 'lungs', cough: 'lungs',
  stomach: 'stomach', gastro: 'stomach', digest: 'digestive', bowel: 'digestive', abdominal: 'stomach', nausea: 'stomach', reflux: 'stomach', gerd: 'stomach', ulcer: 'stomach', esophag: 'stomach',
  liver: 'liver', hepat: 'liver', biliary: 'liver', gallbladder: 'liver', jaundice: 'liver',
  kidney: 'kidney', renal: 'kidney', urinary: 'urinary', bladder: 'bladder', urine: 'bladder',
  skin: 'skin', dermat: 'skin', rash: 'skin', eczema: 'skin', psoriasis: 'skin', lesion: 'skin', melanoma: 'skin', squamous: 'skin', basal: 'skin', carcinoma: 'skin',
  muscle: 'muscles', joint: 'joints', bone: 'bone', musculoskeletal: 'muscles', arthritis: 'joints', fracture: 'bone', orthop: 'bone', spine: 'spine', back: 'spine', spinal: 'spine', costochondritis: 'chest',
  thyroid: 'thyroid', endocrine: 'endocrine', diabetes: 'endocrine', hormone: 'endocrine', adrenal: 'endocrine',
  immune: 'immune', autoimmune: 'immune', allergy: 'immune', infection: 'immune',
  hand: 'hand', wrist: 'hand', finger: 'hand', carpal: 'hand',
  foot: 'foot', ankle: 'foot', heel: 'foot', plantar: 'foot', toe: 'foot',
  breast: 'breast', mammary: 'breast',
  pelvis: 'pelvis', reproductive: 'pelvis', uterus: 'pelvis', ovary: 'pelvis', prostate: 'pelvis',
}

const iconPath = computed(() => {
  // Direct area match
  const direct = iconMap[props.area?.toLowerCase()]
  if (direct) return direct

  // Try keyword matching
  const areaLower = (props.area || '').toLowerCase()
  for (const [keyword, icon] of Object.entries(keywordMap)) {
    if (areaLower.includes(keyword)) {
      return iconMap[icon] || iconMap.body
    }
  }

  return iconMap.body
})
</script>
