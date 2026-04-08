import { onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export function useKeyboardShortcuts() {
  const router = useRouter()

  function handleKeydown(e) {
    // Only trigger if not in an input/textarea
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return

    if (e.key === '?' && !e.ctrlKey) {
      e.preventDefault()
      router.push('/help')
    }
    if (e.key === 'n' && e.ctrlKey) {
      e.preventDefault()
      router.push('/consult')
    }
  }

  onMounted(() => document.addEventListener('keydown', handleKeydown))
  onUnmounted(() => document.removeEventListener('keydown', handleKeydown))
}
