import { ref, computed } from 'vue'
import { translations, languages } from '@/i18n/translations.js'

const currentLang = ref(localStorage.getItem('lang') || 'en')

export function useI18n() {
  function setLang(code) {
    currentLang.value = code
    localStorage.setItem('lang', code)
    // Update document lang attribute
    document.documentElement.lang = code
  }

  function t(key) {
    const dict = translations[currentLang.value] || translations.en
    return dict[key] || translations.en[key] || key
  }

  const lang = computed(() => currentLang.value)
  const currentLanguage = computed(() => languages.find(l => l.code === currentLang.value) || languages[0])

  return { t, lang, currentLang, currentLanguage, setLang, languages }
}
