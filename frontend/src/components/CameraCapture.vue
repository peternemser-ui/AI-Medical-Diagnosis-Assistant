<template>
  <div class="relative w-full h-full min-h-[400px] flex flex-col bg-black rounded-2xl overflow-hidden">

    <!-- ══ PERMISSION DENIED STATE ══ -->
    <div v-if="camera.error.value && !camera.isActive.value" class="flex-1 flex flex-col items-center justify-center p-8 text-center">
      <div class="w-20 h-20 rounded-full bg-red-500/10 flex items-center justify-center mb-5">
        <svg class="w-10 h-10 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
        </svg>
      </div>
      <h3 class="text-lg font-semibold text-white mb-2">Camera Access Required</h3>
      <p class="text-sm text-slate-400 max-w-xs mb-6">{{ camera.error.value }}</p>
      <div class="space-y-2 text-left text-xs text-slate-500 max-w-xs">
        <p class="font-medium text-slate-400">How to enable camera:</p>
        <ol class="list-decimal list-inside space-y-1">
          <li>Click the camera icon in your browser's address bar</li>
          <li>Select "Allow" for camera access</li>
          <li>Reload the page and try again</li>
        </ol>
      </div>
      <div class="flex gap-3 mt-6">
        <button @click="retryCamera" class="px-5 py-2.5 rounded-xl text-sm font-semibold bg-blue-600 text-white hover:bg-blue-700 transition-colors">
          Try Again
        </button>
        <button @click="handleClose" class="px-5 py-2.5 rounded-xl text-sm font-semibold bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors">
          Close
        </button>
      </div>
    </div>

    <!-- ══ LOADING STATE ══ -->
    <div v-else-if="camera.isLoading.value" class="flex-1 flex flex-col items-center justify-center p-8">
      <div class="w-14 h-14 rounded-full border-3 border-slate-700 border-t-blue-500 animate-spin mb-5"></div>
      <h3 class="text-base font-semibold text-white mb-1">Starting camera...</h3>
      <p class="text-sm text-slate-500">Please allow camera access when prompted</p>
    </div>

    <!-- ══ CAPTURED PHOTO REVIEW ══ -->
    <div v-else-if="capturedPhoto" class="flex-1 flex flex-col">
      <!-- Photo preview -->
      <div class="flex-1 relative flex items-center justify-center bg-black">
        <img :src="capturedPhoto.dataUrl" alt="Captured photo" class="max-w-full max-h-full object-contain" />
      </div>

      <!-- Review toolbar -->
      <div class="p-4 flex items-center justify-center gap-4 bg-black/90 backdrop-blur-sm">
        <button @click="retakePhoto" class="flex items-center gap-2 px-5 py-3 rounded-xl text-sm font-semibold bg-slate-800 text-white hover:bg-slate-700 transition-colors">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Retake
        </button>
        <button @click="usePhoto" class="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-500 hover:to-teal-500 transition-all shadow-lg shadow-emerald-500/25">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          Use Photo
        </button>
      </div>
    </div>

    <!-- ══ LIVE CAMERA VIEW ══ -->
    <div v-else-if="camera.isActive.value" class="flex-1 flex flex-col">
      <!-- Video preview area -->
      <div class="flex-1 relative overflow-hidden bg-black">
        <video
          :ref="el => { if (el) camera.videoRef.value = el }"
          autoplay
          playsinline
          muted
          class="absolute inset-0 w-full h-full object-cover"
        ></video>

        <!-- Top bar: close + info -->
        <div class="absolute top-0 left-0 right-0 p-3 flex items-center justify-between z-20" style="background: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, transparent 100%)">
          <button @click="handleClose" class="w-9 h-9 rounded-full bg-black/50 backdrop-blur-sm flex items-center justify-center text-white hover:bg-black/70 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div class="flex items-center gap-2 text-xs text-white/70 bg-black/40 backdrop-blur-sm px-3 py-1.5 rounded-full">
            <div class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></div>
            <span>{{ camera.facingMode.value === 'user' ? 'Front' : 'Rear' }}</span>
          </div>
        </div>

        <!-- Overlay guide for prescription scanning -->
        <div v-if="showGuide && mode === 'prescription'" class="absolute inset-0 z-10 pointer-events-none flex items-center justify-center p-6">
          <div class="w-full max-w-sm aspect-[3/4] border-2 border-white/40 rounded-2xl relative">
            <div class="absolute top-0 left-0 w-8 h-8 border-t-3 border-l-3 border-white rounded-tl-xl"></div>
            <div class="absolute top-0 right-0 w-8 h-8 border-t-3 border-r-3 border-white rounded-tr-xl"></div>
            <div class="absolute bottom-0 left-0 w-8 h-8 border-b-3 border-l-3 border-white rounded-bl-xl"></div>
            <div class="absolute bottom-0 right-0 w-8 h-8 border-b-3 border-r-3 border-white rounded-br-xl"></div>
            <div class="absolute inset-x-0 bottom-0 translate-y-full pt-3 text-center">
              <span class="text-xs text-white/80 bg-black/50 backdrop-blur-sm px-3 py-1.5 rounded-full">Align prescription within the frame</span>
            </div>
          </div>
        </div>

        <!-- Overlay guide for pill identification -->
        <div v-if="showGuide && mode === 'pill'" class="absolute inset-0 z-10 pointer-events-none flex items-center justify-center">
          <div class="w-48 h-48 sm:w-56 sm:h-56 rounded-full border-2 border-white/40 relative">
            <div class="absolute -top-1 left-1/2 -translate-x-1/2 w-6 h-0.5 bg-white/60 rounded-full"></div>
            <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 w-6 h-0.5 bg-white/60 rounded-full"></div>
            <div class="absolute top-1/2 -left-1 -translate-y-1/2 w-0.5 h-6 bg-white/60 rounded-full"></div>
            <div class="absolute top-1/2 -right-1 -translate-y-1/2 w-0.5 h-6 bg-white/60 rounded-full"></div>
            <div class="absolute inset-x-0 bottom-0 translate-y-full pt-4 text-center">
              <span class="text-xs text-white/80 bg-black/50 backdrop-blur-sm px-3 py-1.5 rounded-full">Place pill in the center</span>
            </div>
          </div>
        </div>

        <!-- Overlay guide for wound -->
        <div v-if="showGuide && mode === 'wound'" class="absolute inset-0 z-10 pointer-events-none flex items-center justify-center p-8">
          <div class="w-full max-w-xs aspect-square border-2 border-white/30 rounded-3xl relative">
            <div class="absolute inset-x-0 bottom-0 translate-y-full pt-3 text-center">
              <span class="text-xs text-white/80 bg-black/50 backdrop-blur-sm px-3 py-1.5 rounded-full">Center the affected area</span>
            </div>
          </div>
        </div>

        <!-- Auto-capture countdown -->
        <div v-if="autoCaptureCountdown > 0" class="absolute inset-0 z-20 flex items-center justify-center pointer-events-none">
          <div class="w-24 h-24 rounded-full bg-black/60 backdrop-blur-sm flex items-center justify-center">
            <span class="text-4xl font-bold text-white">{{ autoCaptureCountdown }}</span>
          </div>
        </div>
      </div>

      <!-- Bottom toolbar -->
      <div class="p-4 pb-6 flex items-center justify-center gap-6 bg-black/90 backdrop-blur-sm">
        <!-- Flash toggle -->
        <button
          v-if="camera.hasFlashlight.value"
          @click="camera.toggleFlashlight()"
          class="w-11 h-11 rounded-full flex items-center justify-center transition-colors"
          :class="camera.isFlashlightOn.value ? 'bg-yellow-500 text-black' : 'bg-white/15 text-white hover:bg-white/25'"
          title="Toggle flash"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </button>
        <div v-else class="w-11"></div>

        <!-- Capture button -->
        <button
          @click="handleCapture"
          class="w-18 h-18 rounded-full border-4 border-white flex items-center justify-center transition-transform active:scale-90 hover:scale-105"
          title="Capture photo"
        >
          <div class="w-14 h-14 rounded-full bg-white hover:bg-slate-100 transition-colors"></div>
        </button>

        <!-- Switch camera -->
        <button
          v-if="camera.hasMultipleCameras.value"
          @click="camera.switchCamera()"
          class="w-11 h-11 rounded-full bg-white/15 text-white flex items-center justify-center hover:bg-white/25 transition-colors"
          title="Switch camera"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
        <div v-else class="w-11"></div>
      </div>
    </div>

    <!-- ══ NO CAMERA / FALLBACK ══ -->
    <div v-else class="flex-1 flex flex-col items-center justify-center p-8 text-center">
      <div class="w-20 h-20 rounded-full bg-slate-800 flex items-center justify-center mb-5">
        <svg class="w-10 h-10 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </div>
      <h3 class="text-base font-semibold text-white mb-1">Ready to capture</h3>
      <p class="text-sm text-slate-500 mb-5">Camera will start when opened</p>
      <button @click="retryCamera" class="px-5 py-2.5 rounded-xl text-sm font-semibold bg-blue-600 text-white hover:bg-blue-700 transition-colors">
        Start Camera
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useCamera } from '@/composables/useCamera.js'

const props = defineProps({
  mode: {
    type: String,
    default: 'general',
    validator: v => ['prescription', 'pill', 'general', 'wound'].includes(v),
  },
  showGuide: {
    type: Boolean,
    default: true,
  },
  autoCapture: {
    type: Number,
    default: 0, // 0 = disabled, otherwise seconds
  },
  quality: {
    type: Number,
    default: 0.92,
  },
})

const emit = defineEmits(['capture', 'close', 'error'])

const camera = useCamera()
const capturedPhoto = ref(null)
const autoCaptureCountdown = ref(0)
let autoCaptureTimer = null

// ── Start camera on mount ──
onMounted(async () => {
  const facingMode = props.mode === 'general' ? 'user' : 'environment'
  const ok = await camera.startCamera({ facingMode, resolution: 'hd' })
  if (!ok && camera.error.value) {
    emit('error', camera.error.value)
  }
  if (ok && props.autoCapture > 0) {
    startAutoCapture()
  }
})

onUnmounted(() => {
  clearAutoCaptureTimer()
  camera.stopCamera()
})

// ── Auto-capture timer ──
function startAutoCapture() {
  autoCaptureCountdown.value = props.autoCapture
  autoCaptureTimer = setInterval(() => {
    autoCaptureCountdown.value--
    if (autoCaptureCountdown.value <= 0) {
      clearAutoCaptureTimer()
      handleCapture()
    }
  }, 1000)
}

function clearAutoCaptureTimer() {
  if (autoCaptureTimer) {
    clearInterval(autoCaptureTimer)
    autoCaptureTimer = null
  }
  autoCaptureCountdown.value = 0
}

// ── Capture photo ──
function handleCapture() {
  clearAutoCaptureTimer()
  const photo = camera.capturePhoto(props.quality)
  if (photo) {
    capturedPhoto.value = photo
  }
}

// ── Retake ──
function retakePhoto() {
  capturedPhoto.value = null
  if (props.autoCapture > 0) {
    startAutoCapture()
  }
}

// ── Use photo — emit to parent ──
function usePhoto() {
  if (capturedPhoto.value) {
    emit('capture', {
      dataUrl: capturedPhoto.value.dataUrl,
      base64: capturedPhoto.value.base64,
      blob: capturedPhoto.value.blob,
    })
  }
  capturedPhoto.value = null
}

// ── Retry camera ──
async function retryCamera() {
  const facingMode = props.mode === 'general' ? 'user' : 'environment'
  const ok = await camera.startCamera({ facingMode, resolution: 'hd' })
  if (!ok && camera.error.value) {
    emit('error', camera.error.value)
  }
}

// ── Close ──
function handleClose() {
  camera.stopCamera()
  capturedPhoto.value = null
  emit('close')
}
</script>

<style scoped>
.w-18 {
  width: 4.5rem;
}
.h-18 {
  height: 4.5rem;
}
.border-3 {
  border-width: 3px;
}
</style>
