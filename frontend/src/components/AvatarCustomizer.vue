<template>
  <div class="fixed inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-sm" @click.self="$emit('close')">
    <div class="bg-slate-900 border border-slate-700/50 rounded-none sm:rounded-2xl w-full max-w-none sm:max-w-lg mx-0 sm:mx-4 h-full sm:h-auto max-h-full sm:max-h-[90vh] overflow-y-auto shadow-2xl">
      <!-- Header -->
      <div class="flex items-center justify-between px-5 py-4 border-b border-slate-700/50">
        <h2 class="text-lg font-bold text-white">Customize Your AI Doctor</h2>
        <button @click="$emit('close')" class="text-slate-400 hover:text-white transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <div class="p-5 space-y-5">
        <!-- Live Preview -->
        <div class="flex justify-center py-4 bg-slate-800/50 rounded-xl">
          <DoctorAvatar :avatar="localAvatar" :speaking="previewSpeaking" size="xl" />
        </div>

        <!-- Avatar Style Toggle -->
        <div>
          <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Avatar Style</label>
          <div class="flex gap-2">
            <button
              v-for="s in avatarStyles" :key="s.id"
              @click="localAvatar.avatarStyle = s.id"
              class="flex-1 flex flex-col items-center gap-1.5 px-3 py-2.5 rounded-lg text-xs font-medium border transition-all"
              :class="localAvatar.avatarStyle === s.id
                ? 'bg-blue-500/20 border-blue-500/50 text-blue-300'
                : 'bg-slate-800 border-slate-700/50 text-slate-400 hover:text-white'"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="s.id === 'illustrated'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path v-else-if="s.id === 'realistic'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ s.label }}
            </button>
          </div>
        </div>

        <!-- Photo Upload (only in photo mode) -->
        <div v-if="localAvatar.avatarStyle === 'photo'" class="space-y-3">
          <div class="flex flex-col items-center gap-3 p-4 bg-slate-800/50 rounded-xl border border-dashed border-slate-600/50">
            <div v-if="localAvatar.photoUrl" class="w-24 h-24 rounded-full overflow-hidden border-2 border-slate-600">
              <img :src="localAvatar.photoUrl" alt="Uploaded photo" class="w-full h-full object-cover" />
            </div>
            <div v-else class="w-24 h-24 rounded-full bg-slate-700 flex items-center justify-center">
              <svg class="w-10 h-10 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <div class="flex gap-2">
              <button
                @click="photoFileRef.click()"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-xs font-medium transition-colors"
              >
                {{ localAvatar.photoUrl ? 'Change Photo' : 'Upload Photo' }}
              </button>
              <button
                v-if="localAvatar.photoUrl"
                @click="localAvatar.photoUrl = ''"
                class="bg-slate-700 hover:bg-slate-600 text-slate-300 px-4 py-2 rounded-lg text-xs font-medium transition-colors"
              >
                Remove
              </button>
            </div>
            <p class="text-[10px] text-slate-500 text-center">Upload a photo for a realistic avatar. Square images work best.</p>
          </div>
          <input ref="photoFileRef" type="file" accept="image/*" class="hidden" @change="handlePhotoUpload" />
        </div>

        <!-- Appearance options (hidden in photo mode) -->
        <template v-if="localAvatar.avatarStyle !== 'photo'">
          <!-- Name & Specialty -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-[11px] text-slate-400 uppercase font-semibold mb-1 block">Name</label>
              <input v-model="localAvatar.name" class="w-full bg-slate-800 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500" />
            </div>
            <div>
              <label class="text-[11px] text-slate-400 uppercase font-semibold mb-1 block">Specialty</label>
              <select v-model="localAvatar.specialty" class="w-full bg-slate-800 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500">
                <option>General Practitioner</option>
                <option>Internal Medicine</option>
                <option>Family Medicine</option>
                <option>Emergency Medicine</option>
                <option>Pediatrician</option>
                <option>Cardiologist</option>
                <option>Neurologist</option>
                <option>Dermatologist</option>
                <option>Psychiatrist</option>
                <option>Oncologist</option>
              </select>
            </div>
          </div>

          <!-- Skin Tone -->
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Skin Tone</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tone in skinTones" :key="tone"
                @click="localAvatar.skinTone = tone"
                class="w-9 h-9 rounded-full border-2 transition-all hover:scale-110"
                :class="localAvatar.skinTone === tone ? 'border-blue-400 scale-110 ring-2 ring-blue-400/30' : 'border-slate-600'"
                :style="{ backgroundColor: tone }"
              ></button>
            </div>
          </div>

          <!-- Hair Style -->
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Hair Style</label>
            <div class="flex gap-2 flex-wrap">
              <button
                v-for="style in hairStyles" :key="style.id"
                @click="localAvatar.hairStyle = style.id"
                class="px-3 py-1.5 rounded-lg text-xs font-medium border transition-all"
                :class="localAvatar.hairStyle === style.id
                  ? 'bg-blue-500/20 border-blue-500/50 text-blue-300'
                  : 'bg-slate-800 border-slate-700/50 text-slate-400 hover:text-white'"
              >{{ style.label }}</button>
            </div>
          </div>

          <!-- Hair Color -->
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Hair Color</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="color in hairColors" :key="color"
                @click="localAvatar.hairColor = color"
                class="w-8 h-8 rounded-full border-2 transition-all hover:scale-110"
                :class="localAvatar.hairColor === color ? 'border-blue-400 scale-110' : 'border-slate-600'"
                :style="{ backgroundColor: color }"
              ></button>
            </div>
          </div>

          <!-- Eye Color -->
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Eye Color</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="color in eyeColors" :key="color"
                @click="localAvatar.eyeColor = color"
                class="w-8 h-8 rounded-full border-2 transition-all hover:scale-110"
                :class="localAvatar.eyeColor === color ? 'border-blue-400 scale-110' : 'border-slate-600'"
                :style="{ backgroundColor: color }"
              ></button>
            </div>
          </div>

          <!-- Coat Color -->
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Coat Color</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="color in coatColors" :key="color.value"
                @click="localAvatar.coatColor = color.value"
                class="px-3 py-1.5 rounded-lg text-xs font-medium border transition-all"
                :class="localAvatar.coatColor === color.value
                  ? 'bg-blue-500/20 border-blue-500/50 text-blue-300'
                  : 'bg-slate-800 border-slate-700/50 text-slate-400 hover:text-white'"
              >{{ color.label }}</button>
            </div>
          </div>

          <!-- Accessories -->
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Accessories</label>
            <div class="flex gap-3">
              <label class="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" v-model="localAvatar.glasses" class="rounded bg-slate-800 border-slate-600 text-blue-500 focus:ring-blue-500" />
                <span class="text-sm text-slate-300">Glasses</span>
              </label>
            </div>
          </div>

          <!-- Background Color -->
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Background</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="bg in bgColors" :key="bg"
                @click="localAvatar.bgColor = bg"
                class="w-8 h-8 rounded-full border-2 transition-all hover:scale-110"
                :class="localAvatar.bgColor === bg ? 'border-blue-400 scale-110' : 'border-slate-600'"
                :style="{ backgroundColor: bg }"
              ></button>
            </div>
          </div>
        </template>

        <!-- Name & Specialty (photo mode - still needed) -->
        <div v-if="localAvatar.avatarStyle === 'photo'" class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-1 block">Name</label>
            <input v-model="localAvatar.name" class="w-full bg-slate-800 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500" />
          </div>
          <div>
            <label class="text-[11px] text-slate-400 uppercase font-semibold mb-1 block">Specialty</label>
            <select v-model="localAvatar.specialty" class="w-full bg-slate-800 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500">
              <option>General Practitioner</option>
              <option>Internal Medicine</option>
              <option>Family Medicine</option>
              <option>Emergency Medicine</option>
              <option>Pediatrician</option>
              <option>Cardiologist</option>
              <option>Neurologist</option>
              <option>Dermatologist</option>
              <option>Psychiatrist</option>
              <option>Oncologist</option>
            </select>
          </div>
        </div>

        <!-- Voice Settings -->
        <div>
          <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Doctor's Voice</label>
          <div class="space-y-2">
            <select
              v-model="localAvatar.preferredVoice"
              class="w-full bg-slate-800 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="">Auto (match doctor name)</option>
              <option v-for="v in availableVoices" :key="v.name" :value="v.name">
                {{ v.name }} ({{ v.lang }}){{ v.localService ? '' : ' - HD' }}
              </option>
            </select>
            <div class="flex gap-2">
              <button
                @click="previewVoice"
                class="flex-1 bg-slate-800 hover:bg-slate-700 border border-slate-700/50 text-slate-300 hover:text-white px-3 py-1.5 rounded-lg text-xs font-medium transition-colors flex items-center justify-center gap-1.5"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                </svg>
                Preview Voice
              </button>
              <div class="flex items-center gap-2 flex-1">
                <span class="text-[10px] text-slate-500 whitespace-nowrap">Speed</span>
                <input
                  type="range" min="0.7" max="1.3" step="0.05"
                  v-model.number="localAvatar.voiceRate"
                  class="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
                />
                <span class="text-[10px] text-slate-400 w-8">{{ (localAvatar.voiceRate || 0.95).toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Presets (not in photo mode) -->
        <div v-if="localAvatar.avatarStyle !== 'photo'">
          <label class="text-[11px] text-slate-400 uppercase font-semibold mb-2 block">Quick Presets</label>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
            <button
              v-for="preset in presets" :key="preset.name"
              @click="applyPreset(preset)"
              class="bg-slate-800 hover:bg-slate-700 border border-slate-700/50 rounded-lg p-2 text-center transition-colors"
            >
              <div class="text-xs font-medium text-white">{{ preset.name }}</div>
              <div class="text-[10px] text-slate-500">{{ preset.specialty }}</div>
            </button>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-5 py-4 border-t border-slate-700/50 flex gap-3">
        <button @click="$emit('close')" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2.5 rounded-lg text-sm font-medium transition-colors">
          Cancel
        </button>
        <button @click="save" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg text-sm font-medium transition-colors">
          Save Doctor
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import DoctorAvatar from './DoctorAvatar.vue'

const props = defineProps({
  currentAvatar: { type: Object, required: true }
})

const emit = defineEmits(['close', 'save'])

const localAvatar = reactive({
  preferredVoice: '',
  voiceRate: 0.95,
  avatarStyle: 'illustrated',
  photoUrl: '',
  ...props.currentAvatar,
})
const previewSpeaking = ref(false)
const availableVoices = ref([])
const photoFileRef = ref(null)

const avatarStyles = [
  { id: 'illustrated', label: 'Illustrated' },
  { id: 'realistic', label: 'Realistic' },
  { id: 'photo', label: 'Photo' },
]

onMounted(() => {
  setInterval(() => { previewSpeaking.value = !previewSpeaking.value }, 2000)

  const loadVoices = () => {
    if ('speechSynthesis' in window) {
      const voices = window.speechSynthesis.getVoices()
      availableVoices.value = voices.filter(v => v.lang.startsWith('en'))
      availableVoices.value.sort((a, b) => {
        if (a.localService !== b.localService) return a.localService ? 1 : -1
        return a.name.localeCompare(b.name)
      })
    }
  }
  loadVoices()
  if ('speechSynthesis' in window) {
    window.speechSynthesis.addEventListener('voiceschanged', loadVoices)
  }
})

function handlePhotoUpload(event) {
  const file = event.target.files?.[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (e) => {
    // Resize to reasonable dimensions to avoid huge localStorage entries
    const img = new Image()
    img.onload = () => {
      const canvas = document.createElement('canvas')
      const size = 256
      canvas.width = size
      canvas.height = size
      const ctx = canvas.getContext('2d')
      // Center-crop to square
      const s = Math.min(img.width, img.height)
      const sx = (img.width - s) / 2
      const sy = (img.height - s) / 2
      ctx.drawImage(img, sx, sy, s, s, 0, 0, size, size)
      localAvatar.photoUrl = canvas.toDataURL('image/jpeg', 0.85)
    }
    img.src = e.target.result
  }
  reader.readAsDataURL(file)
  event.target.value = ''
}

function previewVoice() {
  if (!('speechSynthesis' in window)) return
  window.speechSynthesis.cancel()

  const text = `Hello, I'm ${localAvatar.name}. I'm your ${localAvatar.specialty} and I'll be taking care of you today. How are you feeling?`
  const utterance = new SpeechSynthesisUtterance(text)

  const voices = window.speechSynthesis.getVoices()
  if (localAvatar.preferredVoice) {
    const v = voices.find(voice => voice.name === localAvatar.preferredVoice)
    if (v) utterance.voice = v
  } else {
    const femaleNames = ['sarah','maria','amara','emma','lisa','anna','jessica','rachel','emily']
    const isFemale = femaleNames.some(n => localAvatar.name.toLowerCase().includes(n))
    const preferred = isFemale
      ? ['Google UK English Female', 'Microsoft Zira', 'Samantha', 'Karen']
      : ['Google UK English Male', 'Microsoft David', 'Daniel', 'Alex']
    for (const name of preferred) {
      const v = voices.find(voice => voice.name.includes(name))
      if (v) { utterance.voice = v; break }
    }
  }

  utterance.rate = localAvatar.voiceRate || 0.95
  utterance.pitch = 1.0
  utterance.volume = 0.85

  previewSpeaking.value = true
  utterance.onend = () => { previewSpeaking.value = false }
  utterance.onerror = () => { previewSpeaking.value = false }

  window.speechSynthesis.speak(utterance)
}

const skinTones = ['#FDEBD0', '#F5CBA7', '#E0AC69', '#C68642', '#8D5524', '#5C3D2E']
const hairStyles = [
  { id: 'short', label: 'Short' },
  { id: 'long', label: 'Long' },
  { id: 'curly', label: 'Curly' },
  { id: 'ponytail', label: 'Ponytail' },
  { id: 'bald', label: 'Bald' },
]
const hairColors = ['#1a1a2e', '#3d2b1f', '#8B4513', '#B8860B', '#D4A574', '#C0C0C0', '#FF6347']
const eyeColors = ['#4A3728', '#2E5A3E', '#4A6FA5', '#6B7B8D', '#8B6914']
const coatColors = [
  { value: '#f0f0f0', label: 'White' },
  { value: '#2563eb', label: 'Blue' },
  { value: '#0d9488', label: 'Teal' },
  { value: '#7c3aed', label: 'Purple' },
  { value: '#1e293b', label: 'Navy' },
]
const bgColors = ['#1e293b', '#1e3a5f', '#1a3c34', '#3b1f4a', '#3f1f1f', '#2d3748']

const presets = [
  {
    name: 'Dr. Sarah',
    specialty: 'Family Medicine',
    skinTone: '#F5CBA7', hairStyle: 'long', hairColor: '#3d2b1f', eyeColor: '#4A6FA5',
    coatColor: '#f0f0f0', glasses: false, bgColor: '#1e3a5f',
    lipColor: '#d4756b', accessoryColor: '#64748b',
  },
  {
    name: 'Dr. James',
    specialty: 'Internal Medicine',
    skinTone: '#E0AC69', hairStyle: 'short', hairColor: '#1a1a2e', eyeColor: '#4A3728',
    coatColor: '#2563eb', glasses: true, bgColor: '#1e293b',
    lipColor: '#b87070', accessoryColor: '#475569',
  },
  {
    name: 'Dr. Amara',
    specialty: 'Cardiologist',
    skinTone: '#8D5524', hairStyle: 'curly', hairColor: '#1a1a2e', eyeColor: '#4A3728',
    coatColor: '#0d9488', glasses: false, bgColor: '#1a3c34',
    lipColor: '#c47070', accessoryColor: '#64748b',
  },
  {
    name: 'Dr. Wei',
    specialty: 'Neurologist',
    skinTone: '#FDEBD0', hairStyle: 'short', hairColor: '#1a1a2e', eyeColor: '#4A3728',
    coatColor: '#f0f0f0', glasses: true, bgColor: '#3b1f4a',
    lipColor: '#c9877a', accessoryColor: '#374151',
  },
  {
    name: 'Dr. Maria',
    specialty: 'Pediatrician',
    skinTone: '#C68642', hairStyle: 'ponytail', hairColor: '#3d2b1f', eyeColor: '#2E5A3E',
    coatColor: '#7c3aed', glasses: false, bgColor: '#3b1f4a',
    lipColor: '#d4756b', accessoryColor: '#64748b',
  },
  {
    name: 'Dr. Patel',
    specialty: 'Emergency Medicine',
    skinTone: '#C68642', hairStyle: 'short', hairColor: '#1a1a2e', eyeColor: '#4A3728',
    coatColor: '#1e293b', glasses: false, bgColor: '#3f1f1f',
    lipColor: '#b87070', accessoryColor: '#dc2626',
  },
]

function applyPreset(preset) {
  Object.assign(localAvatar, preset)
}

function save() {
  emit('save', { ...localAvatar })
}
</script>
