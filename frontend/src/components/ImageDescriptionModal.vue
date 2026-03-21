<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click.self="$emit('close')">
      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

      <!-- Modal -->
      <div class="relative w-full max-w-lg rounded-2xl shadow-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-gray-200'">

        <!-- Header -->
        <div class="flex items-center justify-between px-5 py-4 border-b"
          :class="isDark ? 'border-slate-700/50' : 'border-gray-200'">
          <h3 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-gray-900'">
            Describe Your Symptom Image
          </h3>
          <button @click="$emit('close')"
            class="p-1.5 rounded-lg transition-colors"
            :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-gray-100 text-gray-500 hover:text-gray-900'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Body -->
        <div class="px-5 py-4 space-y-4 max-h-[70vh] overflow-y-auto">
          <!-- Image preview -->
          <div class="flex justify-center">
            <img :src="imageUrl" alt="Uploaded symptom image"
              class="max-h-48 rounded-xl border object-contain"
              :class="isDark ? 'border-slate-700' : 'border-gray-300'" />
          </div>

          <!-- Instruction -->
          <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-gray-600'">
            Please describe what you see in this image (e.g., rash location, color, size, shape, texture).
            This description will be included with your symptoms for a more accurate assessment.
          </p>

          <!-- Quick suggestion buttons -->
          <div class="flex flex-wrap gap-2">
            <button v-for="tag in suggestionTags" :key="tag"
              @click="addTag(tag)"
              class="px-3 py-1.5 rounded-full text-xs font-medium border transition-all"
              :class="selectedTags.includes(tag)
                ? 'bg-blue-600 text-white border-blue-600'
                : (isDark
                  ? 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700 hover:border-slate-600'
                  : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200 hover:border-gray-400')">
              {{ tag }}
            </button>
          </div>

          <!-- Description text area -->
          <textarea
            ref="textareaRef"
            v-model="description"
            rows="3"
            placeholder="Describe the appearance, location, size, and any changes you've noticed..."
            class="w-full rounded-xl px-4 py-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/50 border transition-colors"
            :class="isDark
              ? 'bg-slate-800 text-white border-slate-700 placeholder-slate-500'
              : 'bg-gray-50 text-gray-900 border-gray-300 placeholder-gray-400'"
          ></textarea>
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-end gap-3 px-5 py-4 border-t"
          :class="isDark ? 'border-slate-700/50' : 'border-gray-200'">
          <button @click="$emit('close')"
            class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
            :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'">
            Cancel
          </button>
          <button @click="handleSubmit"
            :disabled="!canSubmit"
            class="px-5 py-2 rounded-xl text-sm font-semibold transition-all"
            :class="canSubmit
              ? 'bg-blue-600 hover:bg-blue-700 text-white'
              : (isDark ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-gray-200 text-gray-400 cursor-not-allowed')">
            Add to Consultation
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const props = defineProps({
  visible: { type: Boolean, default: false },
  imageUrl: { type: String, default: '' }
})

const emit = defineEmits(['close', 'submit'])

const description = ref('')
const selectedTags = ref([])
const textareaRef = ref(null)

const suggestionTags = [
  'Red rash',
  'Swelling',
  'Bruise',
  'Wound/Cut',
  'Skin discoloration',
  'Bump/Lump',
  'Blisters',
  'Dry/Flaky skin',
  'Itchy area',
  'Burning sensation'
]

const canSubmit = computed(() => {
  return description.value.trim().length > 0 || selectedTags.value.length > 0
})

function addTag(tag) {
  const idx = selectedTags.value.indexOf(tag)
  if (idx >= 0) {
    selectedTags.value.splice(idx, 1)
  } else {
    selectedTags.value.push(tag)
  }
}

function handleSubmit() {
  if (!canSubmit.value) return

  const parts = []
  if (selectedTags.value.length > 0) {
    parts.push('Visual symptoms: ' + selectedTags.value.join(', '))
  }
  if (description.value.trim()) {
    parts.push(description.value.trim())
  }

  const fullDescription = parts.join('. ')

  emit('submit', {
    imageUrl: props.imageUrl,
    description: fullDescription
  })

  // Reset state
  description.value = ''
  selectedTags.value = []
}

onMounted(() => {
  nextTick(() => textareaRef.value?.focus())
})
</script>
