import { ref, onUnmounted, computed } from 'vue'

/**
 * Vue 3 composable for camera/webcam access.
 * Handles MediaStream lifecycle, photo capture, camera switching,
 * flashlight toggle, zoom, and autofocus.
 *
 * Usage:
 *   const { videoRef, startCamera, capturePhoto, stopCamera, ... } = useCamera()
 *   // bind videoRef to a <video> element via ref="videoRef"
 */
export function useCamera() {
  // ── Reactive state ──
  const isActive = ref(false)
  const isLoading = ref(false)
  const error = ref(null)
  const hasPermission = ref(false)
  const stream = ref(null)
  const videoRef = ref(null)
  const facingMode = ref('environment')
  const hasMultipleCameras = ref(false)
  const hasFlashlight = ref(false)
  const isFlashlightOn = ref(false)
  const zoomLevel = ref(1.0)
  const capabilities = ref({
    cameras: [],
    flashSupported: false,
    zoomSupported: false,
    zoomMin: 1,
    zoomMax: 1,
    focusSupported: false,
  })

  // ── Internal ──
  let currentTrack = null

  const isMobile = computed(() => {
    if (typeof navigator === 'undefined') return false
    return /Android|iPhone|iPad|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
  })

  const resolutionMap = {
    hd: { width: 1280, height: 720 },
    fhd: { width: 1920, height: 1080 },
    '4k': { width: 3840, height: 2160 },
  }

  // ── Get available video input devices ──
  async function getDevices() {
    try {
      const devices = await navigator.mediaDevices.enumerateDevices()
      const videoDevices = devices.filter(d => d.kind === 'videoinput')
      capabilities.value.cameras = videoDevices
      hasMultipleCameras.value = videoDevices.length > 1
      return videoDevices
    } catch (e) {
      return []
    }
  }

  // ── Detect track capabilities (flash, zoom, focus) ──
  function detectCapabilities(track) {
    if (!track) return
    try {
      const caps = track.getCapabilities ? track.getCapabilities() : {}

      // Flash / torch
      const torchSupported = caps.torch === true || (Array.isArray(caps.torch) && caps.torch.includes(true))
      capabilities.value.flashSupported = torchSupported
      hasFlashlight.value = torchSupported

      // Zoom
      if (caps.zoom) {
        capabilities.value.zoomSupported = true
        capabilities.value.zoomMin = caps.zoom.min || 1
        capabilities.value.zoomMax = caps.zoom.max || 1
      } else {
        capabilities.value.zoomSupported = false
      }

      // Focus
      capabilities.value.focusSupported = !!(caps.focusMode && caps.focusMode.length > 0)
    } catch (e) {
      // Some browsers don't support getCapabilities
    }
  }

  // ── Start camera ──
  async function startCamera(options = {}) {
    const {
      facingMode: requestedFacing = 'environment',
      resolution = 'hd',
      mirror = false,
    } = options

    error.value = null
    isLoading.value = true
    facingMode.value = requestedFacing

    // Check for camera API
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      error.value = 'Camera not supported in this browser. Please use a modern browser like Chrome or Safari.'
      isLoading.value = false
      return false
    }

    // Stop any existing stream
    stopCamera()

    const res = resolutionMap[resolution] || resolutionMap.hd

    const constraints = {
      video: {
        facingMode: requestedFacing,
        width: { ideal: res.width },
        height: { ideal: res.height },
      },
      audio: false,
    }

    // On mobile, prefer facingMode; on desktop with only one camera, just request video
    if (!isMobile.value) {
      delete constraints.video.facingMode
    }

    try {
      // Add timeout to prevent hanging if permission dialog is ignored
      const mediaStream = await Promise.race([
        navigator.mediaDevices.getUserMedia(constraints),
        new Promise((_, reject) => setTimeout(() => reject(new Error('Camera request timed out. Please allow camera access and try again.')), 15000)),
      ])
      stream.value = mediaStream
      hasPermission.value = true
      isActive.value = true

      currentTrack = mediaStream.getVideoTracks()[0] || null
      detectCapabilities(currentTrack)
      await getDevices()

      // Bind to video element
      if (videoRef.value) {
        videoRef.value.srcObject = mediaStream
        videoRef.value.style.transform = mirror ? 'scaleX(-1)' : 'none'
        try {
          await videoRef.value.play()
        } catch (e) {
          // autoplay may be blocked; user interaction will fix it
        }
      }

      isLoading.value = false
      return true
    } catch (e) {
      isLoading.value = false
      hasPermission.value = false

      if (e.name === 'NotAllowedError' || e.name === 'PermissionDeniedError') {
        error.value = 'Camera permission was denied. Please allow camera access in your browser settings and try again.'
      } else if (e.name === 'NotFoundError' || e.name === 'DevicesNotFoundError') {
        error.value = 'No camera was found on this device. Please connect a camera and try again.'
      } else if (e.name === 'NotReadableError' || e.name === 'TrackStartError') {
        error.value = 'Camera is already in use by another application. Please close other apps using the camera and try again.'
      } else if (e.name === 'OverconstrainedError') {
        // Retry with simpler constraints
        try {
          const fallbackStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
          stream.value = fallbackStream
          hasPermission.value = true
          isActive.value = true
          currentTrack = fallbackStream.getVideoTracks()[0] || null
          detectCapabilities(currentTrack)
          await getDevices()
          if (videoRef.value) {
            videoRef.value.srcObject = fallbackStream
            try { await videoRef.value.play() } catch (_) {}
          }
          isLoading.value = false
          return true
        } catch (_) {
          error.value = 'Could not start the camera with the requested settings. Please try again.'
        }
      } else {
        error.value = `Camera error: ${e.message || 'Unknown error occurred'}. Please try again.`
      }

      return false
    }
  }

  // ── Stop camera ──
  function stopCamera() {
    if (stream.value) {
      stream.value.getTracks().forEach(track => track.stop())
      stream.value = null
    }
    if (videoRef.value) {
      videoRef.value.srcObject = null
    }
    currentTrack = null
    isActive.value = false
    isFlashlightOn.value = false
    zoomLevel.value = 1.0
  }

  // ── Capture photo ──
  function capturePhoto(quality = 0.92) {
    if (!videoRef.value || !isActive.value) {
      return null
    }

    const video = videoRef.value
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    const ctx = canvas.getContext('2d')
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    const dataUrl = canvas.toDataURL('image/jpeg', quality)
    const base64 = dataUrl.split(',')[1]

    // Convert to blob
    const byteString = atob(base64)
    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i)
    }
    const blob = new Blob([ab], { type: 'image/jpeg' })

    return {
      dataUrl,
      base64,
      blob,
      width: canvas.width,
      height: canvas.height,
    }
  }

  // ── Switch between front and rear cameras ──
  async function switchCamera() {
    const newFacing = facingMode.value === 'environment' ? 'user' : 'environment'
    const mirror = newFacing === 'user'
    return await startCamera({ facingMode: newFacing, mirror })
  }

  // ── Toggle flashlight (torch) ──
  async function toggleFlashlight() {
    if (!currentTrack || !hasFlashlight.value) return false

    try {
      const newState = !isFlashlightOn.value
      await currentTrack.applyConstraints({
        advanced: [{ torch: newState }],
      })
      isFlashlightOn.value = newState
      return true
    } catch (e) {
      return false
    }
  }

  // ── Set zoom level ──
  async function setZoom(level) {
    if (!currentTrack || !capabilities.value.zoomSupported) return false

    const clamped = Math.max(capabilities.value.zoomMin, Math.min(level, capabilities.value.zoomMax))
    try {
      await currentTrack.applyConstraints({
        advanced: [{ zoom: clamped }],
      })
      zoomLevel.value = clamped
      return true
    } catch (e) {
      return false
    }
  }

  // ── Trigger autofocus ──
  async function autoFocus() {
    if (!currentTrack || !capabilities.value.focusSupported) return false

    try {
      await currentTrack.applyConstraints({
        advanced: [{ focusMode: 'continuous' }],
      })
      return true
    } catch (e) {
      return false
    }
  }

  // ── Auto-cleanup on component unmount ──
  onUnmounted(() => {
    stopCamera()
  })

  return {
    // Reactive state
    isActive,
    isLoading,
    error,
    hasPermission,
    stream,
    videoRef,
    capabilities,
    facingMode,
    hasMultipleCameras,
    hasFlashlight,
    isFlashlightOn,
    zoomLevel,
    isMobile,

    // Methods
    startCamera,
    stopCamera,
    capturePhoto,
    switchCamera,
    toggleFlashlight,
    setZoom,
    autoFocus,
    getDevices,
  }
}
