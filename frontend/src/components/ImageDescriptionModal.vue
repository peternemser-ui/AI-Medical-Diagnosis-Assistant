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

              <!-- Annotation toolbar (hidden when zoomed) -->
              <div v-if="!isZoomed" class="flex items-center gap-1.5 flex-wrap mb-2">
                <button v-for="tool in annotationTools" :key="tool.id"
                  @click="setActiveTool(tool.id)"
                  class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium border transition-all duration-150 min-w-[44px] min-h-[44px] justify-center"
                  :class="activeTool === tool.id
                    ? 'bg-blue-600 text-white border-blue-600 shadow-md shadow-blue-500/25'
                    : (isDark
                      ? 'bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700 hover:border-slate-600'
                      : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50 hover:border-gray-300')">
                  <span v-html="tool.icon" class="w-4 h-4 flex items-center justify-center"></span>
                  <span class="hidden sm:inline">{{ tool.label }}</span>
                </button>
                <div class="w-px h-6 mx-1" :class="isDark ? 'bg-slate-700' : 'bg-gray-200'"></div>
                <button @click="undoAnnotation"
                  :disabled="annotations.length === 0"
                  class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium border transition-all duration-150 min-w-[44px] min-h-[44px] justify-center"
                  :class="annotations.length === 0
                    ? (isDark ? 'bg-slate-800/40 text-slate-600 border-slate-700/50 cursor-not-allowed' : 'bg-gray-50 text-gray-300 border-gray-100 cursor-not-allowed')
                    : (isDark ? 'bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700' : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50')">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a5 5 0 015 5v2M3 10l4-4M3 10l4 4"/></svg>
                  <span class="hidden sm:inline">Undo</span>
                </button>
                <button @click="clearAnnotations"
                  :disabled="annotations.length === 0"
                  class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium border transition-all duration-150 min-w-[44px] min-h-[44px] justify-center"
                  :class="annotations.length === 0
                    ? (isDark ? 'bg-slate-800/40 text-slate-600 border-slate-700/50 cursor-not-allowed' : 'bg-gray-50 text-gray-300 border-gray-100 cursor-not-allowed')
                    : (isDark ? 'bg-slate-800/80 text-red-400 border-slate-700 hover:bg-red-500/20' : 'bg-white text-red-500 border-gray-200 hover:bg-red-50')">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                  <span class="hidden sm:inline">Clear</span>
                </button>
                <span v-if="annotations.length > 0" class="text-xs ml-1" :class="isDark ? 'text-slate-500' : 'text-gray-400'">
                  {{ annotations.length }} mark{{ annotations.length !== 1 ? 's' : '' }}
                </span>
              </div>

              <!-- Image preview with annotation canvas -->
              <div class="relative rounded-xl overflow-hidden border"
                :class="isDark ? 'border-slate-700/60 bg-slate-800/50' : 'border-gray-200 bg-gray-50'">
                <div :class="isZoomed ? 'overflow-auto max-h-[60vh]' : 'flex items-center justify-center'"
                  class="relative"
                  @click="isZoomed && (isZoomed = false)">
                  <div ref="imageWrapperRef" class="relative inline-block" :class="isZoomed ? 'w-full' : ''">
                    <img ref="imageRef" :src="imageUrl" alt="Uploaded symptom image"
                      class="transition-all duration-300 block"
                      :class="[
                        isZoomed ? 'w-full h-auto cursor-zoom-out' : 'max-h-[40vh] object-contain cursor-crosshair',
                      ]"
                      :style="activeTool && !isZoomed ? { pointerEvents: 'none' } : {}"
                      @load="onImageLoad" />
                    <!-- Annotation canvas overlay -->
                    <canvas v-show="!isZoomed"
                      ref="annotationCanvas"
                      class="absolute top-0 left-0 w-full h-full"
                      :style="{ cursor: activeTool === 'text' ? 'text' : activeTool ? 'crosshair' : 'zoom-in', touchAction: 'none' }"
                      @mousedown="onCanvasMouseDown"
                      @mousemove="onCanvasMouseMove"
                      @mouseup="onCanvasMouseUp"
                      @mouseleave="onCanvasMouseUp"
                      @touchstart.prevent="onCanvasTouchStart"
                      @touchmove.prevent="onCanvasTouchMove"
                      @touchend.prevent="onCanvasTouchEnd"
                      @click="onCanvasClick"
                    ></canvas>
                  </div>
                </div>
                <!-- Text label input popup -->
                <div v-if="showTextInput" class="absolute z-10 flex items-center gap-1"
                  :style="{ left: textInputPos.x + 'px', top: textInputPos.y + 'px' }">
                  <input ref="textLabelInput" v-model="textLabelValue"
                    @keydown.enter="confirmTextLabel" @keydown.esc="cancelTextLabel"
                    placeholder="Label..."
                    class="px-2 py-1 rounded-lg text-sm border shadow-lg w-32 focus:outline-none focus:ring-2"
                    :class="isDark
                      ? 'bg-slate-800 text-white border-slate-600 focus:ring-blue-500/40'
                      : 'bg-white text-gray-900 border-gray-300 focus:ring-blue-500/30'" />
                  <button @click="confirmTextLabel"
                    class="p-1.5 rounded-lg text-white bg-blue-600 hover:bg-blue-700 shadow-lg">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
                  </button>
                  <button @click="cancelTextLabel"
                    class="p-1.5 rounded-lg shadow-lg"
                    :class="isDark ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                  </button>
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
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
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
const imageWrapperRef = ref(null)
const annotationCanvas = ref(null)
const textLabelInput = ref(null)

// --- Annotation state ---
const activeTool = ref(null)
const annotations = ref([])
const isDrawing = ref(false)
const drawStart = ref(null)
const currentPath = ref([])
const showTextInput = ref(false)
const textInputPos = ref({ x: 0, y: 0 })
const textInputCanvasPos = ref({ x: 0, y: 0 })
const textLabelValue = ref('')
let animFrameId = null

const STROKE_COLOR = '#EF4444'
const STROKE_WIDTH = 3

const annotationTools = [
  { id: 'circle', label: 'Circle', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/></svg>' },
  { id: 'arrow', label: 'Arrow', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 19L19 5M19 5h-6M19 5v6"/></svg>' },
  { id: 'freehand', label: 'Draw', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/></svg>' },
  { id: 'text', label: 'Text', icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7V4h16v3M9 20h6M12 4v16"/></svg>' },
]

function setActiveTool(toolId) {
  if (activeTool.value === toolId) {
    activeTool.value = null
  } else {
    activeTool.value = toolId
  }
  cancelTextLabel()
}

function getCanvasPos(e) {
  const canvas = annotationCanvas.value
  if (!canvas) return { x: 0, y: 0 }
  const rect = canvas.getBoundingClientRect()
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  return {
    x: clientX - rect.left,
    y: clientY - rect.top
  }
}

function onCanvasMouseDown(e) {
  if (!activeTool.value || activeTool.value === 'text' || isZoomed.value) return
  e.preventDefault()
  isDrawing.value = true
  drawStart.value = getCanvasPos(e)
  currentPath.value = [drawStart.value]
}

function onCanvasMouseMove(e) {
  if (!isDrawing.value || !activeTool.value) return
  e.preventDefault()
  const pos = getCanvasPos(e)
  if (activeTool.value === 'freehand') {
    currentPath.value.push(pos)
  }
  renderAll(pos)
}

function onCanvasMouseUp(e) {
  if (!isDrawing.value || !activeTool.value) return
  const pos = getCanvasPos(e)
  finishDrawing(pos)
}

function onCanvasTouchStart(e) {
  if (!activeTool.value || activeTool.value === 'text' || isZoomed.value) return
  isDrawing.value = true
  drawStart.value = getCanvasPos(e)
  currentPath.value = [drawStart.value]
}

function onCanvasTouchMove(e) {
  if (!isDrawing.value || !activeTool.value) return
  const pos = getCanvasPos(e)
  if (activeTool.value === 'freehand') {
    currentPath.value.push(pos)
  }
  renderAll(pos)
}

function onCanvasTouchEnd(e) {
  if (!isDrawing.value || !activeTool.value) return
  // Use last known position from the path or drawStart
  const pos = currentPath.value.length > 1 ? currentPath.value[currentPath.value.length - 1] : drawStart.value
  finishDrawing(pos)
}

function onCanvasClick(e) {
  if (activeTool.value !== 'text' || isZoomed.value) {
    // If no tool is active, toggle zoom
    if (!activeTool.value && !isDrawing.value) {
      isZoomed.value = !isZoomed.value
    }
    return
  }
  e.stopPropagation()
  const canvasPos = getCanvasPos(e)
  const canvas = annotationCanvas.value
  if (!canvas) return
  const rect = canvas.getBoundingClientRect()
  // Position the input popup relative to the image container
  textInputPos.value = {
    x: Math.min(canvasPos.x, rect.width - 160),
    y: Math.max(0, canvasPos.y - 36)
  }
  textInputCanvasPos.value = canvasPos
  textLabelValue.value = ''
  showTextInput.value = true
  nextTick(() => textLabelInput.value?.focus())
}

function confirmTextLabel() {
  if (!textLabelValue.value.trim()) {
    cancelTextLabel()
    return
  }
  annotations.value.push({
    type: 'text',
    x: textInputCanvasPos.value.x,
    y: textInputCanvasPos.value.y,
    text: textLabelValue.value.trim()
  })
  showTextInput.value = false
  textLabelValue.value = ''
  renderAll()
}

function cancelTextLabel() {
  showTextInput.value = false
  textLabelValue.value = ''
}

function finishDrawing(pos) {
  if (!drawStart.value) { isDrawing.value = false; return }

  if (activeTool.value === 'circle') {
    const dx = pos.x - drawStart.value.x
    const dy = pos.y - drawStart.value.y
    const radius = Math.sqrt(dx * dx + dy * dy)
    if (radius > 3) {
      annotations.value.push({ type: 'circle', cx: drawStart.value.x, cy: drawStart.value.y, radius })
    }
  } else if (activeTool.value === 'arrow') {
    const dx = pos.x - drawStart.value.x
    const dy = pos.y - drawStart.value.y
    if (Math.sqrt(dx * dx + dy * dy) > 5) {
      annotations.value.push({ type: 'arrow', x1: drawStart.value.x, y1: drawStart.value.y, x2: pos.x, y2: pos.y })
    }
  } else if (activeTool.value === 'freehand') {
    if (currentPath.value.length > 2) {
      annotations.value.push({ type: 'freehand', points: [...currentPath.value] })
    }
  }

  isDrawing.value = false
  drawStart.value = null
  currentPath.value = []
  renderAll()
}

function undoAnnotation() {
  annotations.value.pop()
  renderAll()
}

function clearAnnotations() {
  annotations.value = []
  renderAll()
}

// --- Canvas rendering ---
function renderAll(previewPos) {
  const canvas = annotationCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Draw saved annotations
  for (const ann of annotations.value) {
    drawAnnotation(ctx, ann)
  }

  // Draw live preview
  if (isDrawing.value && drawStart.value && previewPos) {
    ctx.globalAlpha = 0.6
    if (activeTool.value === 'circle') {
      const dx = previewPos.x - drawStart.value.x
      const dy = previewPos.y - drawStart.value.y
      const r = Math.sqrt(dx * dx + dy * dy)
      drawCircle(ctx, drawStart.value.x, drawStart.value.y, r)
    } else if (activeTool.value === 'arrow') {
      drawArrow(ctx, drawStart.value.x, drawStart.value.y, previewPos.x, previewPos.y)
    } else if (activeTool.value === 'freehand') {
      drawFreehand(ctx, currentPath.value)
    }
    ctx.globalAlpha = 1.0
  }
}

function drawAnnotation(ctx, ann) {
  if (ann.type === 'circle') {
    drawCircle(ctx, ann.cx, ann.cy, ann.radius)
  } else if (ann.type === 'arrow') {
    drawArrow(ctx, ann.x1, ann.y1, ann.x2, ann.y2)
  } else if (ann.type === 'freehand') {
    drawFreehand(ctx, ann.points)
  } else if (ann.type === 'text') {
    drawTextLabel(ctx, ann.x, ann.y, ann.text)
  }
}

function drawCircle(ctx, cx, cy, r) {
  ctx.beginPath()
  ctx.arc(cx, cy, r, 0, Math.PI * 2)
  ctx.strokeStyle = STROKE_COLOR
  ctx.lineWidth = STROKE_WIDTH
  ctx.stroke()
}

function drawArrow(ctx, x1, y1, x2, y2) {
  const headLen = 14
  const angle = Math.atan2(y2 - y1, x2 - x1)

  ctx.beginPath()
  ctx.moveTo(x1, y1)
  ctx.lineTo(x2, y2)
  ctx.strokeStyle = STROKE_COLOR
  ctx.lineWidth = STROKE_WIDTH
  ctx.stroke()

  // Arrowhead
  ctx.beginPath()
  ctx.moveTo(x2, y2)
  ctx.lineTo(x2 - headLen * Math.cos(angle - Math.PI / 6), y2 - headLen * Math.sin(angle - Math.PI / 6))
  ctx.moveTo(x2, y2)
  ctx.lineTo(x2 - headLen * Math.cos(angle + Math.PI / 6), y2 - headLen * Math.sin(angle + Math.PI / 6))
  ctx.strokeStyle = STROKE_COLOR
  ctx.lineWidth = STROKE_WIDTH
  ctx.stroke()
}

function drawFreehand(ctx, points) {
  if (points.length < 2) return
  ctx.beginPath()
  ctx.moveTo(points[0].x, points[0].y)
  for (let i = 1; i < points.length; i++) {
    ctx.lineTo(points[i].x, points[i].y)
  }
  ctx.strokeStyle = STROKE_COLOR
  ctx.lineWidth = STROKE_WIDTH
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  ctx.stroke()
}

function drawTextLabel(ctx, x, y, text) {
  const fontSize = 14
  ctx.font = `bold ${fontSize}px sans-serif`
  const metrics = ctx.measureText(text)
  const padding = 4
  const bgW = metrics.width + padding * 2
  const bgH = fontSize + padding * 2

  // Background pill
  ctx.fillStyle = 'rgba(0,0,0,0.65)'
  ctx.beginPath()
  ctx.roundRect(x - padding, y - fontSize - padding, bgW, bgH, 4)
  ctx.fill()

  // Text
  ctx.fillStyle = '#FFFFFF'
  ctx.fillText(text, x, y - padding)

  // Small red dot marker
  ctx.beginPath()
  ctx.arc(x, y + 4, 3, 0, Math.PI * 2)
  ctx.fillStyle = STROKE_COLOR
  ctx.fill()
}

function syncCanvasSize() {
  const canvas = annotationCanvas.value
  const img = imageRef.value
  if (!canvas || !img) return
  // Match canvas internal resolution to displayed image size
  const rect = img.getBoundingClientRect()
  canvas.width = rect.width
  canvas.height = rect.height
  canvas.style.width = rect.width + 'px'
  canvas.style.height = rect.height + 'px'
  renderAll()
}

function onImageLoad() {
  analyzeImage()
  nextTick(() => syncCanvasSize())
}

let resizeObserver = null

// handled in merged watcher below

onBeforeUnmount(() => {
  if (resizeObserver) {
    resizeObserver.disconnect()
  }
})

// --- Composite export ---
function getAnnotatedImageUrl() {
  const img = imageRef.value
  if (!img || annotations.value.length === 0) return props.imageUrl

  try {
    const composite = document.createElement('canvas')
    composite.width = img.naturalWidth
    composite.height = img.naturalHeight
    const ctx = composite.getContext('2d')
    ctx.drawImage(img, 0, 0)

    // Scale from display coords to natural coords
    const displayRect = img.getBoundingClientRect()
    const scaleX = img.naturalWidth / displayRect.width
    const scaleY = img.naturalHeight / displayRect.height
    ctx.save()
    ctx.scale(scaleX, scaleY)

    for (const ann of annotations.value) {
      drawAnnotation(ctx, ann)
    }
    ctx.restore()

    return composite.toDataURL('image/jpeg', 0.92)
  } catch (e) {
    // CORS or other error - return original
    console.warn('Could not composite annotations:', e)
    return props.imageUrl
  }
}

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

  // Annotation count
  if (annotations.value.length > 0) {
    parts.push(`Patient marked ${annotations.value.length} area${annotations.value.length !== 1 ? 's' : ''} of concern on the image`)
  }

  const fullDescription = parts.join('. ')

  // Use annotated composite image if annotations exist
  const finalImageUrl = getAnnotatedImageUrl()

  emit('submit', {
    imageUrl: finalImageUrl,
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
  activeTool.value = null
  annotations.value = []
  isDrawing.value = false
  drawStart.value = null
  currentPath.value = []
  showTextInput.value = false
  textLabelValue.value = ''
}

// Re-sync canvas after un-zooming
watch(isZoomed, (val) => {
  if (!val) {
    nextTick(() => syncCanvasSize())
  }
})

// Reset when modal closes, setup canvas when it opens
watch(() => props.visible, (val) => {
  if (!val) {
    resetState()
    if (resizeObserver) {
      resizeObserver.disconnect()
      resizeObserver = null
    }
  } else {
    nextTick(() => {
      // Don't auto-focus textarea on mobile (keyboard is annoying)
      if (window.innerWidth > 640) {
        textareaRef.value?.focus()
      }
      syncCanvasSize()
      // Watch for resizes
      if (imageRef.value && typeof ResizeObserver !== 'undefined') {
        resizeObserver = new ResizeObserver(() => syncCanvasSize())
        resizeObserver.observe(imageRef.value)
      }
    })
  }
})
</script>
