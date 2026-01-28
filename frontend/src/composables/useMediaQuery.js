import { ref, onMounted, onUnmounted } from 'vue'

/**
 * Media query composable
 */
export function useMediaQuery(query) {
  const matches = ref(false)
  let mediaQueryList = null

  const updateMatch = (e) => {
    matches.value = e.matches
  }

  onMounted(() => {
    if (typeof window !== 'undefined') {
      mediaQueryList = window.matchMedia(query)
      matches.value = mediaQueryList.matches

      // Modern browsers
      if (mediaQueryList.addEventListener) {
        mediaQueryList.addEventListener('change', updateMatch)
      } else {
        // Fallback for older browsers
        mediaQueryList.addListener(updateMatch)
      }
    }
  })

  onUnmounted(() => {
    if (mediaQueryList) {
      if (mediaQueryList.removeEventListener) {
        mediaQueryList.removeEventListener('change', updateMatch)
      } else {
        mediaQueryList.removeListener(updateMatch)
      }
    }
  })

  return matches
}

/**
 * Breakpoint composables using Tailwind defaults
 */
export function useBreakpoints() {
  const breakpoints = {
    sm: '(min-width: 640px)',
    md: '(min-width: 768px)',
    lg: '(min-width: 1024px)',
    xl: '(min-width: 1280px)',
    '2xl': '(min-width: 1536px)'
  }

  const isSm = useMediaQuery(breakpoints.sm)
  const isMd = useMediaQuery(breakpoints.md)
  const isLg = useMediaQuery(breakpoints.lg)
  const isXl = useMediaQuery(breakpoints.xl)
  const is2Xl = useMediaQuery(breakpoints['2xl'])

  const isMobile = useMediaQuery('(max-width: 639px)')
  const isTablet = useMediaQuery('(min-width: 640px) and (max-width: 1023px)')
  const isDesktop = useMediaQuery('(min-width: 1024px)')

  return {
    isSm,
    isMd,
    isLg,
    isXl,
    is2Xl,
    isMobile,
    isTablet,
    isDesktop
  }
}

/**
 * Preferred color scheme
 */
export function usePreferredColorScheme() {
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')
  const prefersLight = useMediaQuery('(prefers-color-scheme: light)')

  return {
    prefersDark,
    prefersLight
  }
}

/**
 * Reduced motion preference
 */
export function usePreferredReducedMotion() {
  return useMediaQuery('(prefers-reduced-motion: reduce)')
}

/**
 * Print media query
 */
export function usePrint() {
  return useMediaQuery('print')
}
