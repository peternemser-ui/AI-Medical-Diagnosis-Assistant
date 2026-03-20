<template>
  <div class="flex items-center gap-1.5">
    <!-- Theme toggle -->
    <button
      @click="toggleTheme"
      class="p-2 rounded-lg transition-all duration-200"
      :class="isDark
        ? 'text-slate-400 hover:text-yellow-300 hover:bg-slate-800/60'
        : 'text-slate-500 hover:text-slate-800 hover:bg-slate-200/60'"
      :title="isDark ? t('theme.light') : t('theme.dark')"
    >
      <!-- Sun icon (show in dark mode → click for light) -->
      <svg v-if="isDark" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
      </svg>
      <!-- Moon icon (show in light mode → click for dark) -->
      <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
      </svg>
    </button>

    <!-- Language selector -->
    <div ref="langDropdownRef">
      <button
        ref="langBtnRef"
        @click="toggleLangMenu"
        class="flex items-center gap-1 px-2 py-1.5 rounded-lg text-xs font-medium transition-all duration-200"
        :class="isDark
          ? 'text-slate-400 hover:text-white hover:bg-slate-800/60'
          : 'text-slate-500 hover:text-slate-800 hover:bg-slate-200/60'"
      >
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span>{{ currentLanguage.flag }}</span>
        <svg class="w-3 h-3 transition-transform" :class="showLangMenu ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>

      <!-- Dropdown via Teleport — renders at body level, always on top -->
      <Teleport to="body">
        <Transition
          enter-active-class="transition duration-150 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div
            v-if="showLangMenu"
            class="fixed min-w-[140px] rounded-lg shadow-2xl border overflow-hidden"
            :style="dropdownStyle"
            style="z-index: 99999"
            :class="isDark
              ? 'bg-slate-900 border-slate-700/50'
              : 'bg-white border-slate-200 shadow-lg'"
          >
            <button
              v-for="l in languages" :key="l.code"
              @click="selectLang(l.code)"
              class="w-full flex items-center gap-2.5 px-3 py-2 text-xs transition-colors"
              :class="[
                currentLang === l.code
                  ? (isDark ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-600')
                  : (isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50')
              ]"
            >
              <span class="font-mono text-[10px] w-5 text-center opacity-60">{{ l.flag }}</span>
              <span>{{ l.name }}</span>
              <svg v-if="currentLang === l.code" class="w-3 h-3 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'

const { isDark, toggleTheme } = useTheme()
const { t, currentLang, currentLanguage, setLang, languages } = useI18n()

const showLangMenu = ref(false)
const langDropdownRef = ref(null)
const langBtnRef = ref(null)
const dropdownStyle = ref({})

function toggleLangMenu() {
  showLangMenu.value = !showLangMenu.value
  if (showLangMenu.value && langBtnRef.value) {
    const rect = langBtnRef.value.getBoundingClientRect()
    dropdownStyle.value = {
      top: `${rect.bottom + 4}px`,
      right: `${window.innerWidth - rect.right}px`,
    }
  }
}

function selectLang(code) {
  setLang(code)
  showLangMenu.value = false
}

function onClickOutside(e) {
  if (langDropdownRef.value && !langDropdownRef.value.contains(e.target)) {
    showLangMenu.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onUnmounted(() => document.removeEventListener('click', onClickOutside))
</script>
