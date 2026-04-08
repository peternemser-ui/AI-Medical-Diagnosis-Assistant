<template>
  <div class="min-h-screen" :class="isDark ? 'bg-slate-950 text-slate-100' : 'bg-white text-slate-900'">
    <!-- Top nav bar -->
    <AppNav currentPage="help" />

    <div class="max-w-7xl mx-auto flex">
      <!-- Mobile TOC dropdown -->
      <div class="lg:hidden sticky top-14 z-10 w-full px-4 py-2"
        :class="isDark ? 'bg-slate-950/95' : 'bg-white/95'" style="backdrop-filter: blur(12px)">
        <button @click="showMobileToc = !showMobileToc"
          class="w-full flex items-center justify-between px-4 py-2.5 text-sm rounded-lg border transition-colors"
          :class="isDark
            ? 'bg-slate-900 border-slate-700 text-slate-300 hover:border-slate-600'
            : 'bg-slate-50 border-slate-200 text-slate-700 hover:border-slate-300'">
          <span>{{ activeSectionTitle || 'Table of Contents' }}</span>
          <svg class="w-4 h-4 transition-transform" :class="showMobileToc ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        <Transition
          enter-active-class="transition duration-200 ease-out"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2">
          <div v-if="showMobileToc"
            class="mt-1 rounded-lg border shadow-xl overflow-hidden"
            :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
            <nav class="py-2 max-h-64 overflow-y-auto">
              <a v-for="section in tocSections" :key="section.id"
                :href="'#' + section.id"
                @click.prevent="scrollToSection(section.id); showMobileToc = false"
                class="block px-4 py-2 text-sm transition-colors"
                :class="activeSection === section.id
                  ? (isDark ? 'bg-blue-500/10 text-blue-400 font-medium' : 'bg-blue-50 text-blue-600 font-medium')
                  : (isDark ? 'text-slate-400 hover:bg-slate-800 hover:text-slate-200' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900')">
                {{ section.title }}
              </a>
            </nav>
          </div>
        </Transition>
      </div>

      <!-- Sidebar TOC (desktop) -->
      <aside class="hidden lg:block w-64 flex-shrink-0 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto py-6 pr-6 pl-4">
        <p class="text-xs font-semibold uppercase tracking-wider mb-3"
          :class="isDark ? 'text-slate-500' : 'text-slate-400'">On this page</p>
        <nav class="space-y-0.5">
          <a v-for="section in tocSections" :key="section.id"
            :href="'#' + section.id"
            @click.prevent="scrollToSection(section.id)"
            class="block px-3 py-1.5 text-sm rounded-lg transition-colors"
            :class="activeSection === section.id
              ? (isDark ? 'bg-blue-500/10 text-blue-400 font-medium border-l-2 border-blue-500' : 'bg-blue-50 text-blue-600 font-medium border-l-2 border-blue-500')
              : (isDark ? 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50')">
            {{ section.title }}
          </a>
        </nav>
      </aside>

      <!-- Main content -->
      <main class="flex-1 min-w-0 py-8 px-4 sm:px-6 lg:px-12">
        <!-- Search results info -->
        <div v-if="searchQuery && searchResultCount !== null" class="mb-6 px-4 py-3 rounded-lg text-sm"
          :class="isDark ? 'bg-slate-800/50 text-slate-300' : 'bg-slate-100 text-slate-600'">
          <span v-if="searchResultCount > 0">Found <strong>{{ searchResultCount }}</strong> match{{ searchResultCount === 1 ? '' : 'es' }} for "<strong>{{ searchQuery }}</strong>"</span>
          <span v-else>No results found for "<strong>{{ searchQuery }}</strong>"</span>
        </div>

        <!-- Rendered markdown -->
        <div class="help-content prose prose-sm sm:prose max-w-none"
          :class="isDark ? 'prose-invert' : ''"
          v-html="renderedContent">
        </div>

        <!-- Disclaimer -->
        <div class="mt-12 pt-6 border-t text-center"
          :class="isDark ? 'border-slate-800' : 'border-slate-200'">
          <p class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
            MedDiagnose AI is an informational tool for educational purposes only. Always consult a qualified healthcare provider.
          </p>
        </div>
      </main>
    </div>

    <!-- Back to top -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-4">
      <button v-if="showBackToTop" @click="scrollToTop"
        class="fixed bottom-6 right-6 p-3 rounded-full shadow-lg z-30 transition-colors"
        :class="isDark
          ? 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'
          : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'"
        title="Back to top">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
        </svg>
      </button>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { useTheme } from '@/composables/useTheme.js'
import AppNav from '@/components/AppNav.vue'
import { HELP_CONTENT } from '@/data/helpContent.js'

const { isDark } = useTheme()

const searchQuery = ref('')
const activeSection = ref('')
const showBackToTop = ref(false)
const showMobileToc = ref(false)
const searchResultCount = ref(null)

// Parse TOC sections from the markdown headings
const tocSections = computed(() => {
  const sections = []
  const lines = HELP_CONTENT.split('\n')
  for (const line of lines) {
    const match = line.match(/^## (\d+)\. (.+)/)
    if (match) {
      const num = match[1]
      const title = match[2]
      const id = `${num}-${title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-$/, '')}`
      sections.push({ id, title: `${num}. ${title}` })
    }
  }
  return sections
})

const activeSectionTitle = computed(() => {
  const found = tocSections.value.find(s => s.id === activeSection.value)
  return found ? found.title : ''
})

// Configure marked for heading IDs
marked.use({
  renderer: {
    heading({ tokens, depth }) {
      const text = tokens.map(t => t.raw || t.text || '').join('')
      const cleanText = text.replace(/<[^>]*>/g, '')
      // Generate IDs matching the TOC pattern for h2 sections
      const match = cleanText.match(/^(\d+)\. (.+)/)
      let id
      if (match && depth === 2) {
        id = `${match[1]}-${match[2].toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-$/, '')}`
      } else {
        id = cleanText.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-$/, '')
      }
      return `<h${depth} id="${id}">${text}</h${depth}>\n`
    }
  }
})

// Render markdown content with optional search highlighting
const renderedContent = computed(() => {
  let content = HELP_CONTENT
  // Remove the embedded TOC (the numbered list at the top)
  content = content.replace(/## Table of Contents[\s\S]*?(?=\n---\n)/, '')

  const rawHtml = marked.parse(content)
  let sanitized = DOMPurify.sanitize(rawHtml, { ADD_ATTR: ['id'] })

  if (searchQuery.value && searchQuery.value.trim().length >= 2) {
    const query = searchQuery.value.trim()
    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    const regex = new RegExp(`(${escaped})`, 'gi')

    // Count matches in text content (not in tags)
    const textOnly = sanitized.replace(/<[^>]*>/g, '')
    const matches = textOnly.match(regex)
    searchResultCount.value = matches ? matches.length : 0

    // Highlight in HTML (avoid matching inside tags)
    sanitized = sanitized.replace(/(<[^>]*>)|(\b[^<]*)/g, (match, tag, text) => {
      if (tag) return tag
      if (text) return text.replace(regex, '<mark class="search-highlight">$1</mark>')
      return match
    })
  } else {
    searchResultCount.value = null
  }

  return sanitized
})

// Scroll to a section
function scrollToSection(id) {
  const el = document.getElementById(id)
  if (el) {
    const offset = 80 // account for sticky nav
    const top = el.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Track scroll position for active section and back-to-top
let observer = null

function setupIntersectionObserver() {
  if (observer) observer.disconnect()

  observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeSection.value = entry.target.id
        }
      }
    },
    { rootMargin: '-80px 0px -70% 0px', threshold: 0 }
  )

  for (const section of tocSections.value) {
    const el = document.getElementById(section.id)
    if (el) observer.observe(el)
  }
}

function handleScroll() {
  showBackToTop.value = window.scrollY > 400
}

// When search changes, scroll to first match
watch(searchQuery, async () => {
  await nextTick()
  if (searchQuery.value && searchQuery.value.trim().length >= 2) {
    const firstMark = document.querySelector('.search-highlight')
    if (firstMark) {
      const top = firstMark.getBoundingClientRect().top + window.scrollY - 120
      window.scrollTo({ top, behavior: 'smooth' })
    }
  }
})

onMounted(async () => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  await nextTick()
  setupIntersectionObserver()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.help-content :deep(h1) {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.help-content :deep(h2) {
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 3rem;
  margin-bottom: 1rem;
  padding-top: 1.5rem;
  letter-spacing: -0.01em;
}

.help-content :deep(h3) {
  font-size: 1.125rem;
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 0.75rem;
}

.help-content :deep(table) {
  font-size: 0.875rem;
  width: 100%;
  border-collapse: collapse;
}

.help-content :deep(th),
.help-content :deep(td) {
  padding: 0.5rem 0.75rem;
  text-align: left;
}

.help-content :deep(code) {
  font-size: 0.85em;
  padding: 0.15em 0.4em;
  border-radius: 4px;
}

.help-content :deep(hr) {
  margin: 2.5rem 0;
  opacity: 0.3;
}

.help-content :deep(.search-highlight) {
  background-color: rgba(250, 204, 21, 0.4);
  color: inherit;
  padding: 0.1em 0.15em;
  border-radius: 2px;
}

/* Dark mode search highlight */
.prose-invert :deep(.search-highlight) {
  background-color: rgba(250, 204, 21, 0.3);
}
</style>
