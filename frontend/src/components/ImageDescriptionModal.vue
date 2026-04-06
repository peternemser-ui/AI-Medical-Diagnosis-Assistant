<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="visible" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center" @click.self="$emit('close')">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/70 backdrop-blur-sm" @click="$emit('close')"></div>

        <!-- Modal -->
        <Transition
          enter-active-class="transition duration-300 ease-out"
          enter-from-class="opacity-0 translate-y-8 sm:translate-y-0 sm:scale-95"
          enter-to-class="opacity-100 translate-y-0 sm:scale-100"
          leave-active-class="transition duration-200 ease-in"
          leave-from-class="opacity-100 translate-y-0 sm:scale-100"
          leave-to-class="opacity-0 translate-y-8 sm:translate-y-0 sm:scale-95"
          appear
        >
          <div
            v-if="visible"
            class="relative w-full max-w-2xl sm:rounded-2xl shadow-2xl border overflow-hidden flex flex-col
                   h-full sm:h-auto sm:min-h-[60vh] sm:max-h-[90vh]
                   rounded-t-2xl sm:rounded-2xl"
            :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-gray-200'"
          >
            <!-- Header -->
            <div class="flex items-center justify-between px-5 py-4 border-b shrink-0"
              :class="isDark ? 'border-slate-700/50' : 'border-gray-200'">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl flex items-center justify-center"
                  :class="isDark ? 'bg-blue-500/20' : 'bg-blue-50'">
                  <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                      d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <circle cx="12" cy="13" r="3" stroke-width="1.5" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold leading-tight" :class="isDark ? 'text-white' : 'text-gray-900'">
                    Describe Your Symptom
                  </h3>
                  <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-gray-400'">
                    Help our AI understand what you see
                  </p>
                </div>
              </div>
              <button @click="$emit('close')"
                class="p-2 rounded-xl transition-colors"
                :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-gray-100 text-gray-500 hover:text-gray-900'">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- Scrollable body -->
            <div class="flex-1 overflow-y-auto px-5 py-4 space-y-5 overscroll-contain">

              <!-- Image quality warning -->
              <div v-if="imageWarning" class="flex items-center gap-2.5 px-4 py-3 rounded-xl text-sm font-medium"
                :class="isDark ? 'bg-amber-500/15 text-amber-300 border border-amber-500/30' : 'bg-amber-50 text-amber-700 border border-amber-200'">
                <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                {{ imageWarning }}
              </div>

              <!-- Image preview -->
              <div class="relative rounded-xl overflow-hidden border"
                :class="isDark ? 'border-slate-700/60 bg-slate-800/50' : 'border-gray-200 bg-gray-50'">
                <div :class="isZoomed ? 'overflow-auto max-h-[60vh]' : 'flex items-center justify-center'"
                  @click="isZoomed = !isZoomed" class="cursor-zoom-in">
                  <img ref="imageRef" :src="imageUrl" alt="Uploaded symptom image"
                    class="transition-all duration-300"
                    :class="[
                      isZoomed ? 'w-full h-auto cursor-zoom-out' : 'max-h-[40vh] object-contain cursor-zoom-in',
                    ]"
                    @load="analyzeImage" />
                </div>
                <!-- Zoom toggle -->
                <button @click.stop="isZoomed = !isZoomed"
                  class="absolute top-3 right-3 p-2 rounded-lg backdrop-blur-sm transition-colors"
                  :class="isDark
                    ? 'bg-black/50 text-white/80 hover:bg-black/70 hover:text-white'
                    : 'bg-white/70 text-gray-700 hover:bg-white/90 hover:text-gray-900'">
                  <svg v-if="!isZoomed" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                  </svg>
                  <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10H7" />
                  </svg>
                </button>
              </div>

              <!-- Body location selector -->
              <div>
                <label class="block text-sm font-semibold mb-2.5" :class="isDark ? 'text-slate-300' : 'text-gray-700'">
                  Where is this located?
                </label>
                <div class="flex flex-wrap gap-2">
                  <button v-for="loc in bodyLocations" :key="loc.label"
                    @click="toggleLocation(loc.label)"
                    class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-sm font-medium border transition-all duration-150"
                    :class="selectedLocation === loc.label
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-500/25'
                      : (isDark
                        ? 'bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700 hover:border-slate-600'
                        : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50 hover:border-gray-300')">
                    <span class="text-base leading-none">{{ loc.icon }}</span>
                    <span>{{ loc.label }}</span>
                  </button>
                </div>
              </div>

              <!-- Selected context chips -->
              <div v-if="selectedLocation || selectedTags.length > 0" class="flex flex-wrap gap-2">
                <span v-if="selectedLocation"
                  class="inline-flex items-center gap-1.5 pl-3 pr-2 py-1.5 rounded-full text-xs font-semibold"
                  :class="isDark ? 'bg-indigo-500/20 text-indigo-300' : 'bg-indigo-50 text-indigo-700'">
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
                  </svg>
                  {{ selectedLocation }}
                  <button @click="selectedLocation = ''" class="p-0.5 rounded-full hover:bg-black/10">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </span>
                <span v-for="tag in selectedTags" :key="'chip-' + tag"
                  class="inline-flex items-center gap-1 pl-2.5 pr-1.5 py-1.5 rounded-full text-xs font-semibold"
                  :class="isDark ? 'bg-blue-500/20 text-blue-300' : 'bg-blue-50 text-blue-700'">
                  {{ tag }}
                  <button @click="removeTag(tag)" class="p-0.5 rounded-full hover:bg-black/10">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </span>
              </div>

              <!-- Symptom tag groups -->
              <div class="space-y-4">
                <div v-for="group in tagGroups" :key="group.label">
                  <label class="block text-xs font-semibold uppercase tracking-wider mb-2"
                    :class="isDark ? 'text-slate-500' : 'text-gray-400'">
                    {{ group.label }}
                  </label>
                  <div class="flex flex-wrap gap-2">
                    <button v-for="tag in group.tags" :key="tag.label"
                      @click="toggleTag(tag.label)"
                      class="flex items-center gap-2 px-3.5 py-2.5 rounded-xl text-sm font-medium border transition-all duration-150"
                      :class="selectedTags.includes(tag.label)
                        ? 'bg-blue-600 text-white border-blue-600 shadow-md shadow-blue-500/25'
                        : (isDark
                          ? 'bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700 hover:border-slate-600'
                          : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50 hover:border-gray-300')">
                      <span class="text-base leading-none">{{ tag.icon }}</span>
                      <span>{{ tag.label }}</span>
                      <svg v-if="selectedTags.includes(tag.label)" class="w-4 h-4 ml-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>

              <!-- Duration quick-select -->
              <div>
                <label class="block text-sm font-semibold mb-2.5" :class="isDark ? 'text-slate-300' : 'text-gray-700'">
                  How long has this been present?
                </label>
                <div class="flex flex-wrap gap-2">
                  <button v-for="dur in durations" :key="dur"
                    @click="toggleDuration(dur)"
                    class="px-4 py-2.5 rounded-xl text-sm font-medium border transition-all duration-150"
                    :class="selectedDuration === dur
                      ? 'bg-emerald-600 text-white border-emerald-600 shadow-md shadow-emerald-500/25'
                      : (isDark
                        ? 'bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700 hover:border-slate-600'
                        : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50 hover:border-gray-300')">
                    {{ dur }}
                  </button>
                </div>
              </div>

              <!-- Description textarea -->
              <div>
                <label class="block text-sm font-semibold mb-2.5" :class="isDark ? 'text-slate-300' : 'text-gray-700'">
                  Additional details
                </label>
                <textarea
                  ref="textareaRef"
                  v-model="description"
                  rows="4"
                  placeholder="Describe what you see: size, color, texture, how long it's been there, if it's spreading..."
                  class="w-full rounded-xl px-4 py-3 text-sm resize-none focus:outline-none focus:ring-2 transition-colors border"
                  :class="isDark
                    ? 'bg-slate-800 text-white border-slate-700 placeholder-slate-500 focus:ring-blue-500/40 focus:border-blue-500/50'
                    : 'bg-gray-50 text-gray-900 border-gray-200 placeholder-gray-400 focus:ring-blue-500/30 focus:border-blue-400'"
                ></textarea>
              </div>

              <!-- Spacer so content isn't hidden behind sticky footer -->
              <div class="h-2"></div>
            </div>

            <!-- Sticky footer -->
            <div class="sticky bottom-0 flex items-center justify-between gap-3 px-5 py-4 border-t shrink-0"
              :class="isDark ? 'border-slate-700/50 bg-slate-900/95 backdrop-blur-sm' : 'border-gray-200 bg-white/95 backdrop-blur-sm'">
              <div class="text-xs" :class="isDark ? 'text-slate-500' : 'text-gray-400'">
                <span v-if="selectionCount > 0">{{ selectionCount }} detail{{ selectionCount > 1 ? 's' : '' }} selected</span>
                <span v-else>Select symptoms or type a description</span>
              </div>
              <div class="flex items-center gap-3">
                <button @click="$emit('close')"
                  class="px-4 py-2.5 rounded-xl text-sm font-medium transition-colors"
                  :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'">
                  Cancel
                </button>
                <button @click="handleSubmit"
                  :disabled="!canSubmit"
                  class="px-6 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200"
                  :class="canSubmit
                    ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg shadow-blue-600/25 hover:shadow-blue-600/40 active:scale-[0.97]'
                    : (isDark ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-gray-100 text-gray-400 cursor-not-allowed')">
                  Add to Consultation
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  visible: { type: Boolean, default: false },
  imageUrl: { type: String, default: '' }
})

const emit = defineEmits(['close', 'submit'])

const description = ref('')
const selectedTags = ref([])
const selectedLocation = ref('')
const selectedDuration = ref('')
const isZoomed = ref(false)
const imageWarning = ref('')
const imageRef = ref(null)
const textareaRef = ref(null)

// Body locations
const bodyLocations = [
  { label: 'Head/Face', icon: '🧠' },
  { label: 'Neck', icon: '🦴' },
  { label: 'Chest', icon: '🫁' },
  { label: 'Abdomen', icon: '🫃' },
  { label: 'Back', icon: '🔙' },
  { label: 'Arms', icon: '💪' },
  { label: 'Hands', icon: '🖐️' },
  { label: 'Legs', icon: '🦵' },
  { label: 'Feet', icon: '🦶' },
  { label: 'Skin (general)', icon: '🩹' },
]

// Categorized symptom tags
const tagGroups = [
  {
    label: 'Skin & Surface',
    tags: [
      { label: 'Red rash', icon: '🔴' },
      { label: 'Swelling', icon: '🫧' },
      { label: 'Bruise', icon: '🟣' },
      { label: 'Dry/Flaky skin', icon: '🌵' },
      { label: 'Blisters', icon: '💧' },
      { label: 'Skin discoloration', icon: '🎨' },
    ]
  },
  {
    label: 'Pain & Sensation',
    tags: [
      { label: 'Burning sensation', icon: '🔥' },
      { label: 'Itchy area', icon: '😣' },
      { label: 'Tender to touch', icon: '👆' },
      { label: 'Numbness', icon: '🧊' },
    ]
  },
  {
    label: 'Wounds',
    tags: [
      { label: 'Wound/Cut', icon: '🩸' },
      { label: 'Bump/Lump', icon: '⬤' },
      { label: 'Sore/Ulcer', icon: '🩹' },
      { label: 'Bleeding', icon: '💉' },
    ]
  }
]

// Duration options
const durations = ['Today', 'Few days', '1-2 weeks', '1+ month', 'Ongoing']

const selectionCount = computed(() => {
  let count = selectedTags.value.length
  if (selectedLocation.value) count++
  if (selectedDuration.value) count++
  return count
})

const canSubmit = computed(() => {
  return description.value.trim().length > 0 || selectedTags.value.length > 0 || selectedLocation.value || selectedDuration.value
})

function toggleLocation(loc) {
  selectedLocation.value = selectedLocation.value === loc ? '' : loc
}

function toggleTag(tag) {
  const idx = selectedTags.value.indexOf(tag)
  if (idx >= 0) {
    selectedTags.value.splice(idx, 1)
  } else {
    selectedTags.value.push(tag)
  }
}

function removeTag(tag) {
  const idx = selectedTags.value.indexOf(tag)
  if (idx >= 0) selectedTags.value.splice(idx, 1)
}

function toggleDuration(dur) {
  selectedDuration.value = selectedDuration.value === dur ? '' : dur
}

// Image quality analysis
function analyzeImage() {
  const img = imageRef.value
  if (!img) return
  imageWarning.value = ''

  try {
    // Check resolution
    if (img.naturalWidth < 200 || img.naturalHeight < 200) {
      imageWarning.value = 'Image resolution is very low — a higher quality photo will improve analysis accuracy.'
      return
    }

    // Check brightness via canvas sampling
    const canvas = document.createElement('canvas')
    const size = 64
    canvas.width = size
    canvas.height = size
    const ctx = canvas.getContext('2d')
    ctx.drawImage(img, 0, 0, size, size)
    const data = ctx.getImageData(0, 0, size, size).data

    let totalLuminance = 0
    const pixelCount = size * size
    for (let i = 0; i < data.length; i += 4) {
      // Perceived luminance formula
      totalLuminance += (0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2])
    }
    const avgLuminance = totalLuminance / pixelCount

    if (avgLuminance < 40) {
      imageWarning.value = 'This image appears too dark — try retaking with better lighting for a more accurate analysis.'
    } else if (avgLuminance > 240) {
      imageWarning.value = 'This image appears overexposed — try retaking in softer lighting.'
    }
  } catch (e) {
    // Canvas CORS or other error — skip silently
  }
}

function handleSubmit() {
  if (!canSubmit.value) return

  const parts = []

  // Build location + tags sentence
  if (selectedTags.value.length > 0) {
    let tagSentence = 'Visual symptoms'
    if (selectedLocation.value) {
      tagSentence += ` on ${selectedLocation.value.toLowerCase()}`
    }
    tagSentence += ': ' + selectedTags.value.join(', ')
    parts.push(tagSentence)
  } else if (selectedLocation.value) {
    parts.push(`Symptom located on ${selectedLocation.value.toLowerCase()}`)
  }

  // Duration
  if (selectedDuration.value) {
    const durMap = {
      'Today': 'since today',
      'Few days': 'for a few days',
      '1-2 weeks': 'for 1-2 weeks',
      '1+ month': 'for over a month',
      'Ongoing': 'ongoing/chronic'
    }
    parts.push(`Present ${durMap[selectedDuration.value] || selectedDuration.value}`)
  }

  // Free text
  if (description.value.trim()) {
    parts.push(`Additional details: ${description.value.trim()}`)
  }

  const fullDescription = parts.join('. ')

  emit('submit', {
    imageUrl: props.imageUrl,
    description: fullDescription
  })

  // Reset state
  resetState()
}

function resetState() {
  description.value = ''
  selectedTags.value = []
  selectedLocation.value = ''
  selectedDuration.value = ''
  isZoomed.value = false
  imageWarning.value = ''
}

// Reset when modal closes
watch(() => props.visible, (val) => {
  if (!val) {
    resetState()
  } else {
    nextTick(() => {
      // Don't auto-focus textarea on mobile (keyboard is annoying)
      if (window.innerWidth > 640) {
        textareaRef.value?.focus()
      }
    })
  }
})
</script>
