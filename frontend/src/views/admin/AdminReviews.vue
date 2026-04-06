<template>
  <div class="space-y-6">
    <!-- Page header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Review Queue</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Triage and resolve flagged cases</p>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          Last updated: {{ lastUpdated }}
        </span>
        <button @click="refresh" class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
          :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          Refresh
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex items-center gap-1 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
      <button v-for="tab in tabs" :key="tab.key"
        @click="switchTab(tab.key)"
        class="px-4 py-2.5 text-sm font-medium transition-colors relative"
        :class="activeTab === tab.key
          ? (isDark ? 'text-white' : 'text-slate-900')
          : (isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-500 hover:text-slate-700')">
        {{ tab.label }}
        <span v-if="tab.count != null" class="ml-1.5 text-[10px] px-1.5 py-0.5 rounded-full"
          :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'">{{ tab.count }}</span>
        <div v-if="activeTab === tab.key" class="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500 rounded-full"></div>
      </button>
    </div>

    <!-- Reviews table -->
    <div class="rounded-2xl border overflow-hidden" :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <table class="w-full text-sm">
        <thead>
          <tr :class="isDark ? 'border-b border-slate-800' : 'border-b border-slate-100'">
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Priority</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Type</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Summary</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Case ID</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Status</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Created</th>
            <th class="text-right px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in reviews" :key="item.id"
            class="border-b transition-colors"
            :class="isDark ? 'border-slate-800/50 hover:bg-slate-800/40' : 'border-slate-50 hover:bg-slate-50'">
            <!-- Priority -->
            <td class="px-5 py-3">
              <span class="text-xs font-medium px-2 py-0.5 rounded-full" :class="priorityClass(item.priority)">{{ item.priority }}</span>
            </td>
            <!-- Type -->
            <td class="px-5 py-3">
              <span class="text-xs font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ formatType(item.type) }}</span>
            </td>
            <!-- Summary -->
            <td class="px-5 py-3 max-w-[260px]">
              <span class="text-xs truncate block" :class="isDark ? 'text-white' : 'text-slate-900'">{{ item.summary }}</span>
            </td>
            <!-- Case ID -->
            <td class="px-5 py-3">
              <router-link v-if="item.case_id" :to="`/admin/cases/${item.case_id}`"
                class="text-xs font-mono hover:underline"
                :class="isDark ? 'text-blue-400' : 'text-blue-600'">
                {{ item.case_id.slice(0, 10) }}
              </router-link>
              <span v-else class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">--</span>
            </td>
            <!-- Status -->
            <td class="px-5 py-3">
              <span class="inline-flex items-center gap-1.5 text-xs font-medium">
                <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(item.status)"></span>
                <span :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ item.status }}</span>
              </span>
            </td>
            <!-- Created -->
            <td class="px-5 py-3 tabular-nums text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              {{ relativeTime(item.created_at) }}
            </td>
            <!-- Actions -->
            <td class="px-5 py-3 text-right">
              <div class="flex items-center justify-end gap-1.5">
                <button v-if="item.status === 'pending'"
                  @click="handleAction(item, 'claim')"
                  class="px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors"
                  :class="isDark ? 'bg-blue-500/15 text-blue-400 hover:bg-blue-500/25' : 'bg-blue-50 text-blue-700 hover:bg-blue-100'"
                  :disabled="actionLoading === item.id">
                  Claim
                </button>
                <button v-if="item.status === 'claimed'"
                  @click="openNoteAction(item, 'resolve')"
                  class="px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors"
                  :class="isDark ? 'bg-emerald-500/15 text-emerald-400 hover:bg-emerald-500/25' : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'"
                  :disabled="actionLoading === item.id">
                  Resolve
                </button>
                <button v-if="item.status === 'pending' || item.status === 'claimed'"
                  @click="handleAction(item, 'escalate')"
                  class="px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors"
                  :class="isDark ? 'bg-amber-500/15 text-amber-400 hover:bg-amber-500/25' : 'bg-amber-50 text-amber-700 hover:bg-amber-100'"
                  :disabled="actionLoading === item.id">
                  Escalate
                </button>
                <button
                  @click="openNoteAction(item, 'add_note')"
                  class="px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors"
                  :class="isDark ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
                  :disabled="actionLoading === item.id">
                  Note
                </button>
              </div>
            </td>
          </tr>

          <!-- Inline note/resolve expansion row -->
          <tr v-if="noteAction && reviews.some(r => r.id === noteAction.item.id)"
            :class="isDark ? 'border-slate-800/50' : 'border-slate-50'">
            <td colspan="7" class="px-5 py-4">
              <div class="rounded-xl border p-4 max-w-xl"
                :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-slate-50 border-slate-200'">
                <div class="text-xs font-semibold mb-2" :class="isDark ? 'text-slate-200' : 'text-slate-700'">
                  {{ noteAction.action === 'resolve' ? 'Resolve with notes' : 'Add a note' }}
                </div>
                <textarea
                  v-model="noteText"
                  rows="3"
                  class="w-full rounded-lg border px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                  :class="isDark ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-500' : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400'"
                  :placeholder="noteAction.action === 'resolve' ? 'Resolution notes (required)...' : 'Add a note...'"
                ></textarea>
                <div class="flex items-center justify-end gap-2 mt-3">
                  <button @click="closeNoteAction"
                    class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
                    :class="isDark ? 'text-slate-400 hover:text-slate-200' : 'text-slate-500 hover:text-slate-700'">
                    Cancel
                  </button>
                  <button @click="submitNoteAction"
                    :disabled="noteAction.action === 'resolve' && !noteText.trim()"
                    class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-40"
                    :class="noteAction.action === 'resolve'
                      ? (isDark ? 'bg-emerald-600 text-white hover:bg-emerald-500' : 'bg-emerald-600 text-white hover:bg-emerald-700')
                      : (isDark ? 'bg-blue-600 text-white hover:bg-blue-500' : 'bg-blue-600 text-white hover:bg-blue-700')">
                    {{ noteAction.action === 'resolve' ? 'Resolve' : 'Save Note' }}
                  </button>
                </div>
              </div>
            </td>
          </tr>

          <!-- Empty state -->
          <tr v-if="reviews.length === 0">
            <td colspan="7" class="px-5 py-16 text-center">
              <div class="flex flex-col items-center gap-2">
                <svg class="w-10 h-10" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">No reviews in queue</p>
                <p class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Flagged cases will appear here for triage</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getReviews, reviewAction } from '@/services/adminApi.js'

const { isDark } = useTheme()

const activeTab = ref('all')
const reviews = ref([])
const counts = ref({ pending: 0, claimed: 0, resolved: 0, escalated: 0 })
const lastUpdated = ref('--')
const actionLoading = ref(null)

// Note / resolve inline action state
const noteAction = ref(null)
const noteText = ref('')

const tabs = ref([
  { key: 'all', label: 'All', count: null },
  { key: 'pending', label: 'Pending', count: null },
  { key: 'claimed', label: 'Claimed', count: null },
  { key: 'resolved', label: 'Resolved', count: null },
  { key: 'escalated', label: 'Escalated', count: null },
])

function updateTabCounts() {
  const total = (counts.value.pending || 0) + (counts.value.claimed || 0) + (counts.value.resolved || 0) + (counts.value.escalated || 0)
  tabs.value[0].count = total || null
  tabs.value[1].count = counts.value.pending || null
  tabs.value[2].count = counts.value.claimed || null
  tabs.value[3].count = counts.value.resolved || null
  tabs.value[4].count = counts.value.escalated || null
}

async function fetchData() {
  try {
    const params = {}
    if (activeTab.value !== 'all') params.status = activeTab.value
    const data = await getReviews(params)
    reviews.value = data.items || []
    if (data.counts) {
      counts.value = data.counts
      updateTabCounts()
    }
    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (e) {
    console.error('Failed to fetch reviews:', e)
  }
}

function switchTab(key) {
  activeTab.value = key
  closeNoteAction()
  fetchData()
}

function refresh() { fetchData() }

const { start } = usePolling(fetchData, 15000)
onMounted(() => start())

// --- Actions ---

async function handleAction(item, action) {
  actionLoading.value = item.id
  try {
    await reviewAction(item.id, action)
    await fetchData()
  } catch (e) {
    console.error(`Action ${action} failed:`, e)
  } finally {
    actionLoading.value = null
  }
}

function openNoteAction(item, action) {
  noteAction.value = { item, action }
  noteText.value = ''
}

function closeNoteAction() {
  noteAction.value = null
  noteText.value = ''
}

async function submitNoteAction() {
  if (!noteAction.value) return
  const { item, action } = noteAction.value
  actionLoading.value = item.id
  try {
    await reviewAction(item.id, action, noteText.value.trim() || null)
    closeNoteAction()
    await fetchData()
  } catch (e) {
    console.error(`Action ${action} failed:`, e)
  } finally {
    actionLoading.value = null
  }
}

// --- Formatting helpers ---

function priorityClass(priority) {
  if (priority === 'critical') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
  if (priority === 'high') return isDark.value ? 'bg-orange-500/15 text-orange-400' : 'bg-orange-100 text-orange-700'
  if (priority === 'medium') return isDark.value ? 'bg-yellow-500/15 text-yellow-400' : 'bg-yellow-100 text-yellow-700'
  return isDark.value ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-500'
}

function statusDotClass(status) {
  if (status === 'pending') return 'bg-amber-500'
  if (status === 'claimed') return 'bg-blue-500'
  if (status === 'resolved') return 'bg-emerald-500'
  if (status === 'escalated') return 'bg-red-500'
  return 'bg-slate-500'
}

function formatType(type) {
  if (!type) return '--'
  return type.replace(/_/g, ' ')
}

function relativeTime(timestamp) {
  if (!timestamp) return '--'
  try {
    const now = Date.now()
    const then = new Date(timestamp).getTime()
    const diff = now - then
    const seconds = Math.floor(diff / 1000)
    if (seconds < 60) return 'just now'
    const minutes = Math.floor(seconds / 60)
    if (minutes < 60) return `${minutes}m ago`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours}h ago`
    const days = Math.floor(hours / 24)
    if (days < 7) return `${days}d ago`
    return new Date(timestamp).toLocaleDateString()
  } catch (e) {
    return timestamp
  }
}
</script>
