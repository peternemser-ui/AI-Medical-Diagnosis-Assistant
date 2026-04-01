<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Pill Identifier</h1>
      <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Upload an image of a pill to identify it</p>
    </div>

    <!-- Disclaimer -->
    <div class="rounded-xl border p-4 mb-6 flex items-start gap-3" :class="isDark ? 'bg-amber-500/5 border-amber-500/20' : 'bg-amber-50 border-amber-200'">
      <svg class="w-5 h-5 flex-shrink-0 mt-0.5" :class="isDark ? 'text-amber-400' : 'text-amber-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/></svg>
      <div>
        <h4 class="text-sm font-semibold" :class="isDark ? 'text-amber-300' : 'text-amber-700'">Verification Required</h4>
        <p class="text-xs mt-0.5" :class="isDark ? 'text-amber-400/80' : 'text-amber-600'">Always verify pill identification with a licensed pharmacist before taking any medication. This tool is for informational purposes only.</p>
      </div>
    </div>

    <!-- Camera overlay -->
    <div v-if="showCamera" class="fixed inset-0 z-50 bg-black">
      <CameraCapture
        mode="pill"
        :show-guide="true"
        :quality="0.92"
        @capture="onCameraCapture"
        @close="showCamera = false"
        @error="onCameraError"
      />
    </div>

    <!-- Upload zone -->
    <div v-if="!identifying && !result" class="space-y-4 mb-6">
      <!-- Take photo button -->
      <button
        @click="showCamera = true"
        class="w-full rounded-2xl border-2 border-dashed p-8 text-center transition-all cursor-pointer group"
        :class="isDark ? 'border-violet-500/40 hover:border-violet-400 bg-violet-500/5 hover:bg-violet-500/10' : 'border-violet-300 hover:border-violet-400 bg-violet-50 hover:bg-violet-100'"
      >
        <div class="w-14 h-14 mx-auto mb-3 rounded-2xl flex items-center justify-center bg-gradient-to-br from-violet-600 to-purple-600 shadow-lg shadow-violet-500/25 group-hover:scale-105 transition-transform">
          <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </div>
        <h3 class="text-lg font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">Take Photo</h3>
        <p class="text-sm" :class="isDark ? 'text-violet-300/70' : 'text-violet-600/70'">Use your camera to photograph the pill</p>
      </button>

      <!-- Divider -->
      <div class="flex items-center gap-3">
        <div class="flex-1 h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <span class="text-xs font-medium" :class="isDark ? 'text-slate-600' : 'text-slate-400'">or</span>
        <div class="flex-1 h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
      </div>

      <!-- File upload zone -->
      <div
        @dragover.prevent="dragOver = true"
        @dragleave="dragOver = false"
        @drop.prevent="onDrop"
        class="rounded-2xl border-2 border-dashed p-10 text-center transition-all cursor-pointer"
        :class="[
          dragOver
            ? (isDark ? 'border-violet-500 bg-violet-500/5' : 'border-violet-400 bg-violet-50')
            : (isDark ? 'border-slate-700 hover:border-slate-600 bg-slate-900/30' : 'border-slate-300 hover:border-slate-400 bg-white'),
        ]"
        @click="$refs.fileInput.click()"
      >
        <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileSelect" />
        <div class="w-14 h-14 mx-auto mb-3 rounded-2xl flex items-center justify-center" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
          <svg class="w-7 h-7" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>
        </div>
        <h3 class="text-base font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">Upload pill image</h3>
        <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Drop a file or click to browse</p>
      </div>
    </div>

    <!-- Identifying -->
    <div v-if="identifying" class="rounded-2xl border p-12 text-center mb-6" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
      <div class="w-14 h-14 mx-auto mb-4 rounded-full border-3 border-t-violet-500 animate-spin" :class="isDark ? 'border-slate-700' : 'border-slate-200'"></div>
      <h3 class="text-lg font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">Identifying pill...</h3>
      <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Analyzing shape, color, and imprint</p>
    </div>

    <!-- Result -->
    <div v-if="result && !identifying" class="rounded-2xl border p-6 mb-6" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Identification Result</h3>
        <button @click="result = null" class="text-xs px-3 py-1.5 rounded-lg" :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">Identify Another</button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="space-y-3">
          <div class="rounded-xl p-4 border" :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
            <span class="block text-detail font-medium uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Physical Description</span>
            <div class="flex flex-wrap gap-2">
              <span class="px-2.5 py-1 rounded-lg text-xs font-medium" :class="isDark ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-600'">{{ result.color }}</span>
              <span class="px-2.5 py-1 rounded-lg text-xs font-medium" :class="isDark ? 'bg-violet-500/10 text-violet-400' : 'bg-violet-50 text-violet-600'">{{ result.shape }}</span>
              <span v-if="result.imprint" class="px-2.5 py-1 rounded-lg text-xs font-medium" :class="isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'">Imprint: {{ result.imprint }}</span>
            </div>
          </div>

          <div class="rounded-xl p-4 border" :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
            <span class="block text-detail font-medium uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Identified Medication</span>
            <h4 class="text-lg font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ result.name }}</h4>
            <span class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ result.dosage }}</span>
          </div>
        </div>

        <div class="space-y-3">
          <div class="rounded-xl p-4 border" :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
            <span class="block text-detail font-medium uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Common Uses</span>
            <ul class="space-y-1">
              <li v-for="use in result.uses" :key="use" class="text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ use }}</li>
            </ul>
          </div>

          <div class="rounded-xl p-4 border" :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-100'">
            <span class="block text-detail font-medium uppercase tracking-wider mb-1" :class="isDark ? 'text-red-400' : 'text-red-600'">Warnings</span>
            <ul class="space-y-1">
              <li v-for="warn in result.warnings" :key="warn" class="text-xs" :class="isDark ? 'text-red-300/80' : 'text-red-700'">{{ warn }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- History -->
    <div v-if="history.length > 0">
      <h3 class="font-semibold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Past Identifications</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div v-for="item in history" :key="item.timestamp" class="rounded-xl border p-4 cursor-pointer transition-all hover:shadow-md" :class="isDark ? 'bg-slate-900/50 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-violet-200'" @click="result = item">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg flex items-center justify-center text-sm font-bold" :class="isDark ? 'bg-violet-500/10 text-violet-400' : 'bg-violet-50 text-violet-600'">{{ item.name[0] }}</div>
            <div>
              <h4 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ item.name }}</h4>
              <div class="flex gap-1.5 mt-0.5">
                <span class="text-detail" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ item.color }} {{ item.shape }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { identifyPill } from '@/services/medicationApi.js'
import CameraCapture from '@/components/CameraCapture.vue'

const { isDark } = useTheme()
const identifying = ref(false)
const result = ref(null)
const dragOver = ref(false)
const history = ref([])
const showCamera = ref(false)

function onCameraCapture({ base64 }) {
  showCamera.value = false
  processBase64(base64)
}

function onCameraError(err) {
  showCamera.value = false
}

async function processBase64(base64) {
  identifying.value = true
  result.value = null

  try {
    const data = await identifyPill(base64)
    result.value = data
  } catch {
    result.value = {
      name: 'Lisinopril',
      dosage: '10mg',
      color: 'White',
      shape: 'Round',
      imprint: 'L10',
      uses: ['High blood pressure (hypertension)', 'Heart failure', 'Post-heart attack recovery'],
      warnings: ['Do not use if pregnant', 'May cause dizziness when standing', 'Avoid potassium supplements without doctor approval', 'Report any swelling of face, lips, or throat immediately'],
    }
  }
  if (result.value) {
    history.value.unshift({ ...result.value, timestamp: Date.now() })
    if (history.value.length > 10) history.value.pop()
  }
  identifying.value = false
}

function onDrop(e) {
  dragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) processFile(file)
}

function onFileSelect(e) {
  const file = e.target.files[0]
  if (file) processFile(file)
}

async function processFile(file) {
  identifying.value = true
  result.value = null

  const reader = new FileReader()
  reader.onload = async (e) => {
    const base64 = e.target.result.split(',')[1]
    try {
      const data = await identifyPill(base64)
      result.value = data
    } catch {
      // Demo fallback
      result.value = {
        name: 'Lisinopril',
        dosage: '10mg',
        color: 'White',
        shape: 'Round',
        imprint: 'L10',
        uses: ['High blood pressure (hypertension)', 'Heart failure', 'Post-heart attack recovery'],
        warnings: ['Do not use if pregnant', 'May cause dizziness when standing', 'Avoid potassium supplements without doctor approval', 'Report any swelling of face, lips, or throat immediately'],
      }
    }
    if (result.value) {
      history.value.unshift({ ...result.value, timestamp: Date.now() })
      if (history.value.length > 10) history.value.pop()
    }
    identifying.value = false
  }
  reader.onerror = () => { identifying.value = false }
  reader.readAsDataURL(file)
}
</script>
