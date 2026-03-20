<template>
  <Teleport to="body">
    <!-- Backdrop -->
    <Transition name="fade">
      <div
        v-if="modelValue"
        class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
        @click="close"
      ></div>
    </Transition>

    <!-- Drawer Panel -->
    <Transition name="slide-right">
      <div
        v-if="modelValue"
        class="fixed top-0 right-0 h-full w-full max-w-md bg-slate-900 border-l border-slate-700 shadow-2xl z-50 flex flex-col"
      >
        <!-- Header -->
        <div class="flex items-center justify-between px-5 py-4 border-b border-slate-700/50 bg-slate-900/95">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <h2 class="text-lg font-bold text-white">Consultation History</h2>
          </div>
          <button
            @click="close"
            class="p-1.5 rounded-lg hover:bg-slate-700/60 text-slate-400 hover:text-white transition-colors"
            title="Close"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- Session List -->
        <div class="flex-1 overflow-y-auto px-4 py-3 space-y-2">
          <!-- Empty state -->
          <div v-if="sessions.length === 0" class="flex flex-col items-center justify-center h-full text-center px-6">
            <svg class="w-16 h-16 text-slate-700 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <p class="text-slate-400 text-sm font-medium">No past consultations yet</p>
            <p class="text-slate-500 text-xs mt-1">Your diagnosis history will appear here</p>
          </div>

          <!-- Session cards -->
          <div
            v-for="session in sessions"
            :key="session.id"
            class="group bg-slate-800/60 border border-slate-700/50 rounded-xl p-3.5 hover:bg-slate-800 hover:border-slate-600/50 transition-all cursor-pointer"
            @click="viewSession(session.id)"
          >
            <div class="flex items-start justify-between gap-2 mb-2">
              <div class="flex items-center gap-2 min-w-0">
                <!-- Urgency dot -->
                <div
                  class="w-2.5 h-2.5 rounded-full flex-shrink-0"
                  :class="urgencyDotClass(session.urgency)"
                ></div>
                <span class="text-xs text-slate-400">{{ formatRelativeTime(session.timestamp) }}</span>
              </div>
              <!-- Delete button -->
              <button
                @click.stop="confirmDelete(session.id)"
                class="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-500/20 text-slate-500 hover:text-red-400 transition-all"
                title="Delete session"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>

            <!-- Symptoms summary -->
            <p class="text-sm text-slate-300 mb-2 leading-snug">{{ session.symptomsSummary || 'No symptoms recorded' }}</p>

            <!-- Top diagnosis -->
            <div class="flex items-center justify-between gap-2">
              <span class="text-xs text-slate-400 truncate">{{ session.topDiagnosis }}</span>
              <span
                v-if="session.confidence"
                class="text-[10px] font-bold px-2 py-0.5 rounded-full flex-shrink-0"
                :class="confidenceBadgeClass(session.confidence)"
              >
                {{ session.confidence }}%
              </span>
            </div>

            <!-- Patient info -->
            <div v-if="session.age || session.gender" class="flex items-center gap-2 mt-2 text-[10px] text-slate-500">
              <span v-if="session.age">Age: {{ session.age }}</span>
              <span v-if="session.age && session.gender" class="text-slate-700">|</span>
              <span v-if="session.gender">{{ session.gender }}</span>
            </div>

            <!-- Action buttons -->
            <div class="flex gap-2 mt-2.5">
              <button
                @click.stop="viewDashboard(session.id)"
                class="flex-1 flex items-center justify-center gap-1.5 text-[10px] font-medium py-1.5 rounded-lg bg-blue-500/15 text-blue-400 hover:bg-blue-500/25 border border-blue-500/20 transition-colors"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                Dashboard
              </button>
              <button
                @click.stop="viewReport(session.id)"
                class="flex-1 flex items-center justify-center gap-1.5 text-[10px] font-medium py-1.5 rounded-lg bg-slate-700/50 text-slate-400 hover:text-white hover:bg-slate-700 border border-slate-600/30 transition-colors"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                Details
              </button>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div v-if="sessions.length > 0" class="px-4 py-3 border-t border-slate-700/50 bg-slate-900/95 space-y-2">
          <a href="/reports" @click="close" class="block w-full text-center text-xs font-medium text-blue-400 hover:text-blue-300 py-2 rounded-lg hover:bg-blue-500/10 transition-colors">
            View All Reports
          </a>
          <button
            @click="confirmClearAll"
            class="w-full text-center text-xs text-slate-500 hover:text-red-400 py-2 rounded-lg hover:bg-red-500/10 transition-colors"
          >
            Clear All History
          </button>
        </div>

        <!-- Confirm dialog overlay -->
        <Transition name="fade">
          <div
            v-if="confirmAction"
            class="absolute inset-0 bg-black/60 flex items-center justify-center z-10 p-6"
          >
            <div class="bg-slate-800 border border-slate-600 rounded-xl p-5 max-w-sm w-full shadow-2xl">
              <p class="text-sm text-white mb-4">{{ confirmMessage }}</p>
              <div class="flex gap-3 justify-end">
                <button
                  @click="cancelConfirm"
                  class="px-4 py-2 text-xs text-slate-400 hover:text-white rounded-lg hover:bg-slate-700 transition-colors"
                >
                  Cancel
                </button>
                <button
                  @click="executeConfirm"
                  class="px-4 py-2 text-xs text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { getSessions, getSession, deleteSession, clearHistory } from '@/services/historyService.js'

const props = defineProps({
  modelValue: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'view-session'])

const sessions = ref([])
const confirmAction = ref(null)
const confirmMessage = ref('')
const pendingDeleteId = ref(null)

// Reload sessions whenever the drawer opens
watch(() => props.modelValue, (open) => {
  if (open) {
    sessions.value = getSessions()
  }
})

function close() {
  emit('update:modelValue', false)
}

function viewSession(id) {
  const session = getSession(id)
  if (session) {
    emit('view-session', session)
    close()
  }
}

function viewDashboard(id) {
  // Store the session's diagnosis result so the dashboard can load it
  const session = getSession(id)
  if (session && session.diagnosisResult) {
    localStorage.setItem('latest_diagnosis_result', JSON.stringify({
      ...session.diagnosisResult,
      age: session.age,
      gender: session.gender,
      date: session.timestamp,
    }))
  }
  close()
  // Navigate to dashboard
  import('vue-router').then(() => {
    window.location.href = '/dashboard'
  })
}

function viewReport(id) {
  close()
  window.location.href = `/reports/${id}`
}

function confirmDelete(id) {
  pendingDeleteId.value = id
  confirmMessage.value = 'Are you sure you want to delete this consultation?'
  confirmAction.value = 'delete'
}

function confirmClearAll() {
  confirmMessage.value = 'Are you sure you want to clear all consultation history? This cannot be undone.'
  confirmAction.value = 'clearAll'
}

function cancelConfirm() {
  confirmAction.value = null
  pendingDeleteId.value = null
}

function executeConfirm() {
  if (confirmAction.value === 'delete' && pendingDeleteId.value) {
    deleteSession(pendingDeleteId.value)
  } else if (confirmAction.value === 'clearAll') {
    clearHistory()
  }
  sessions.value = getSessions()
  confirmAction.value = null
  pendingDeleteId.value = null
}

function urgencyDotClass(urgency) {
  if (urgency === 'urgent' || urgency === 'emergency') return 'bg-red-500'
  if (urgency === 'soon') return 'bg-amber-500'
  return 'bg-emerald-500'
}

function confidenceBadgeClass(confidence) {
  if (confidence >= 70) return 'bg-emerald-500/20 text-emerald-400'
  if (confidence >= 40) return 'bg-amber-500/20 text-amber-400'
  return 'bg-slate-600/30 text-slate-400'
}

function formatRelativeTime(timestamp) {
  if (!timestamp) return ''
  const now = new Date()
  const date = new Date(timestamp)
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return 'Just now'
  if (diffMins < 60) return `${diffMins} min ago`
  if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) > 1 ? 's' : ''} ago`
  return date.toLocaleDateString()
}
</script>

<style scoped>
/* Slide from right */
.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.3s ease;
}
.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
}

/* Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(100, 116, 139, 0.3);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 116, 139, 0.5);
}
</style>
