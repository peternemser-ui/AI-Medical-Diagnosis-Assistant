import { ref, watch } from 'vue'

const SIZES = ['small', 'medium', 'large', 'xlarge']
const SIZE_LABELS = { small: 'S', medium: 'M', large: 'L', xlarge: 'XL' }
const SIZE_SCALES = { small: '14px', medium: '16px', large: '18px', xlarge: '20px' }
const SIZE_DISPLAY = { small: 'Small', medium: 'Medium', large: 'Large', xlarge: 'Extra Large' }

const fontSize = ref(localStorage.getItem('font_size') || 'medium')

function applyFontSize(size) {
  if (typeof document !== 'undefined') {
    document.documentElement.style.fontSize = SIZE_SCALES[size] || '16px'
  }
}

// Apply immediately on import
applyFontSize(fontSize.value)

export function useFontSize() {
  function setFontSize(size) {
    if (!SIZES.includes(size)) return
    fontSize.value = size
    localStorage.setItem('font_size', size)
    applyFontSize(size)
  }

  function cycleFontSize() {
    const idx = SIZES.indexOf(fontSize.value)
    const next = SIZES[(idx + 1) % SIZES.length]
    setFontSize(next)
  }

  watch(fontSize, applyFontSize)

  return {
    fontSize,
    setFontSize,
    cycleFontSize,
    sizes: SIZES,
    sizeLabels: SIZE_LABELS,
    sizeDisplay: SIZE_DISPLAY,
    sizeScales: SIZE_SCALES,
  }
}
