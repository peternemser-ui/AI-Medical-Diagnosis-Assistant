<template>
  <div class="language-switcher">
    <button
      @click.stop="showDropdown = !showDropdown"
      class="language-button p-2 hover:bg-white/10 rounded-lg transition-colors duration-200 group relative"
      title="Language"
    >
      <div class="flex items-center gap-2">
        <svg class="w-6 h-6 text-gray-300 group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>
        </svg>
        <span class="text-sm font-semibold text-gray-300 group-hover:text-white transition-colors">
          {{ currentLanguageFlag }}
        </span>
      </div>
    </button>

    <!-- Dropdown Menu -->
    <transition name="dropdown">
      <div
        v-if="showDropdown"
        @click.stop
        class="language-dropdown absolute top-full right-0 mt-2 bg-gray-900 border border-white/20 rounded-xl shadow-2xl overflow-hidden z-50 min-w-[200px]"
      >
        <div class="p-2">
          <button
            v-for="lang in languages"
            :key="lang.code"
            @click="changeLanguage(lang.code)"
            class="language-option w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-white/10 transition-all duration-200 text-left"
            :class="{ 'bg-purple-600/30 border border-purple-500/50': locale === lang.code }"
          >
            <span class="text-2xl">{{ lang.flag }}</span>
            <div class="flex-1">
              <div class="text-white font-semibold">{{ lang.name }}</div>
              <div class="text-xs text-gray-400">{{ lang.nativeName }}</div>
            </div>
            <svg
              v-if="locale === lang.code"
              class="w-5 h-5 text-purple-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale, t } = useI18n()
const showDropdown = ref(false)

const languages = [
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸' },
  { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷' },
  { code: 'zh', name: 'Chinese', nativeName: '中文', flag: '🇨🇳' }
]

const currentLanguageFlag = computed(() => {
  const lang = languages.find(l => l.code === locale.value)
  return lang ? lang.flag : '🇺🇸'
})

function changeLanguage(langCode) {
  locale.value = langCode
  localStorage.setItem('app-language', langCode)
  showDropdown.value = false
}

function closeDropdown() {
  showDropdown.value = false
}

// Handle click outside
function handleClickOutside(event) {
  const dropdown = document.querySelector('.language-dropdown')
  const button = document.querySelector('.language-button')
  
  if (dropdown && button && !dropdown.contains(event.target) && !button.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.language-switcher {
  position: relative;
}

.language-dropdown {
  animation: dropdown-enter 0.2s ease-out;
}

@keyframes dropdown-enter {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-enter-active {
  animation: dropdown-enter 0.2s ease-out;
}

.dropdown-leave-active {
  animation: dropdown-enter 0.15s ease-in reverse;
}

.language-option {
  cursor: pointer;
}

.language-option:active {
  transform: scale(0.98);
}
</style>
