<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950' : 'bg-white'">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-blue-600/5' : 'bg-blue-400/10'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-purple-600/5' : 'bg-purple-400/10'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="relative z-20 flex items-center justify-between px-6 py-3 border-b"
      :class="isDark ? 'border-slate-800 bg-slate-950/80 backdrop-blur-xl' : 'border-slate-200 bg-white/80 backdrop-blur-xl'">
      <div class="flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
            </svg>
          </div>
          <span class="text-sm font-semibold hidden sm:inline" :class="isDark ? 'text-white' : 'text-slate-900'">Medical AI</span>
        </router-link>
        <div class="w-px h-5 hidden sm:block" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <span class="text-sm font-medium hidden sm:inline" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Reports</span>
      </div>
      <div class="flex items-center gap-2">
        <ThemeLangControls />
        <router-link to="/" class="p-1.5 rounded-lg transition-colors"
          :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </router-link>
      </div>
    </nav>

    <!-- Main content -->
    <div class="relative z-10 max-w-5xl mx-auto px-4 py-6">
      <!-- Header with stats -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Consultation Reports</h1>
          <div class="flex items-center gap-4 mt-1">
            <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              {{ allSessions.length }} total consultation{{ allSessions.length !== 1 ? 's' : '' }}
            </span>
            <span v-if="allSessions.length > 0" class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
              Latest: {{ formatDate(allSessions[0]?.timestamp) }}
            </span>
          </div>
        </div>
        <button v-if="allSessions.length > 0" @click="exportAllJson"
          class="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-medium border transition-colors self-start"
          :class="isDark
            ? 'border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800'
            : 'border-slate-300 text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
          </svg>
          Export All as JSON
        </button>
      </div>

      <!-- Search bar -->
      <div class="mb-5">
        <div class="relative">
          <svg class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            placeholder="Search consultations..."
            class="w-full rounded-xl pl-10 pr-4 py-3 text-sm border focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
            :class="isDark
              ? 'bg-slate-900/80 border-slate-800 text-white placeholder-slate-600'
              : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400'"
          />
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="filteredSessions.length === 0" class="flex flex-col items-center justify-center py-20 text-center">
        <svg class="w-16 h-16 mb-4" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <h2 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">
          {{ allSessions.length === 0 ? 'No consultations yet' : 'No matching results' }}
        </h2>
        <p class="text-sm mb-6" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          {{ allSessions.length === 0 ? 'Start your first consultation to see reports here.' : 'Try adjusting your search term.' }}
        </p>
        <router-link v-if="allSessions.length === 0" to="/consult"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium bg-blue-600 hover:bg-blue-500 text-white transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          Start First Consultation
        </router-link>
      </div>

      <!-- Session cards -->
      <div v-else class="space-y-3">
        <div
          v-for="session in filteredSessions"
          :key="session.id"
          class="group backdrop-blur-xl rounded-2xl border p-4 transition-all duration-200 cursor-pointer"
          :class="isDark
            ? 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/80'
            : 'bg-white/80 border-slate-200 hover:border-slate-300 shadow-sm hover:shadow'"
          @click="$router.push(`/reports/${session.id}`)"
        >
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1 min-w-0">
              <!-- Date + Urgency badge + Message count -->
              <div class="flex items-center gap-2 mb-1.5 flex-wrap">
                <span class="text-xs font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                  {{ formatDate(session.timestamp) }}
                </span>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wide"
                  :class="urgencyClass(session.urgency)">
                  {{ session.urgency }}
                </span>
                <span v-if="getMessageCount(session.id)" class="text-[10px] px-1.5 py-0.5 rounded-full"
                  :class="isDark ? 'bg-slate-800 text-slate-500' : 'bg-slate-100 text-slate-400'">
                  {{ getMessageCount(session.id) }} messages
                </span>
              </div>

              <!-- Summary (first user message truncated to ~80 chars) -->
              <p class="text-sm font-medium mb-1 leading-snug" :class="isDark ? 'text-white' : 'text-slate-900'">
                {{ getSessionSummary(session.id) }}
              </p>

              <!-- Top diagnosis -->
              <div class="flex items-center gap-3 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                <span>{{ session.topDiagnosis }}</span>
                <span v-if="session.confidence" class="font-medium"
                  :class="session.confidence >= 70 ? 'text-emerald-400' : session.confidence >= 40 ? 'text-amber-400' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                  {{ session.confidence }}%
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2 flex-shrink-0">
              <router-link :to="`/reports/${session.id}`"
                @click.stop
                class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
                :class="isDark
                  ? 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900'">
                View Details
              </router-link>
              <button
                @click.stop="handleDelete(session.id)"
                class="p-1.5 rounded-lg transition-all opacity-0 group-hover:opacity-100"
                :class="isDark
                  ? 'text-slate-600 hover:text-red-400 hover:bg-red-500/10'
                  : 'text-slate-400 hover:text-red-500 hover:bg-red-50'"
                title="Delete consultation"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm Dialog -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="confirmDialog.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
        <div class="rounded-2xl border shadow-2xl max-w-sm w-full p-6"
          :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
          <p class="text-sm mb-5" :class="isDark ? 'text-white' : 'text-slate-900'">{{ confirmDialog.message }}</p>
          <div class="flex gap-3 justify-end">
            <button @click="confirmDialog.show = false"
              class="px-4 py-2 text-xs rounded-lg transition-colors"
              :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
              Cancel
            </button>
            <button @click="confirmDialog.action(); confirmDialog.show = false"
              class="px-4 py-2 text-xs text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors">
              Delete
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'
import { getSessions, getSession, deleteSession } from '@/services/historyService.js'

const { isDark } = useTheme()
const searchQuery = ref('')
const allSessions = ref(getSessions())

// Cache for full session data (message counts, summaries)
const sessionCache = {}

function loadFullSession(id) {
  if (!sessionCache[id]) {
    sessionCache[id] = getSession(id)
  }
  return sessionCache[id]
}

function getMessageCount(id) {
  const full = loadFullSession(id)
  return full?.chatMessages?.length || 0
}

function getSessionSummary(id) {
  const full = loadFullSession(id)
  if (full?.chatMessages?.length > 0) {
    const firstUserMsg = full.chatMessages.find(m => m.role === 'user' || m.sender === 'user')
    if (firstUserMsg) {
      const text = firstUserMsg.content || firstUserMsg.text || firstUserMsg.message || ''
      return text.length > 80 ? text.substring(0, 80) + '...' : text
    }
  }
  // Fallback to symptoms summary
  const session = allSessions.value.find(s => s.id === id)
  return session?.symptomsSummary || 'No description available'
}

const filteredSessions = computed(() => {
  if (!searchQuery.value.trim()) return allSessions.value
  const q = searchQuery.value.toLowerCase()
  return allSessions.value.filter(s => {
    const summary = getSessionSummary(s.id).toLowerCase()
    return summary.includes(q) ||
      (s.symptomsSummary || '').toLowerCase().includes(q) ||
      (s.topDiagnosis || '').toLowerCase().includes(q)
  })
})

const confirmDialog = reactive({
  show: false,
  message: '',
  action: () => {},
})

function urgencyClass(urgency) {
  if (urgency === 'emergency') return 'bg-red-500/20 text-red-300'
  if (urgency === 'urgent') return 'bg-red-500/15 text-red-400'
  if (urgency === 'soon') return 'bg-amber-500/15 text-amber-400'
  return 'bg-emerald-500/15 text-emerald-400'
}

function formatDate(timestamp) {
  if (!timestamp) return ''
  try {
    const d = new Date(timestamp)
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return timestamp
  }
}

function handleDelete(id) {
  confirmDialog.message = 'Are you sure you want to delete this consultation? This cannot be undone.'
  confirmDialog.action = () => {
    deleteSession(id)
    delete sessionCache[id]
    allSessions.value = getSessions()
  }
  confirmDialog.show = true
}

function exportAllJson() {
  const data = {
    sessions: allSessions.value,
    exportedAt: new Date().toISOString(),
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `consultations-export-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
}
</script>
