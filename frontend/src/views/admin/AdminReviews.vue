<template>
  <div class="space-y-6">
    <!-- Page header -->
    <APageHeader title="Review Queue" subtitle="Triage and resolve flagged cases" :last-updated="lastUpdated" @refresh="refresh" />

    <!-- Tabs -->
    <ATabBar :tabs="tabs" :model-value="activeTab" @update:model-value="switchTab" />

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
              <span class="text-xs font-medium px-2 py-0.5 rounded-full capitalize" :class="sharedPriorityClass(item.priority)">{{ item.priority }}</span>
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
              {{ sharedRelativeTime(item.created_at) }}
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
            <td colspan="7">
              <AEmptyState
                title="No reviews in queue — all caught up!"
                description="Flagged cases from the safety agent or manual escalations will appear here for triage and resolution."
                variant="info" />
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
import APageHeader from '@/components/admin/APageHeader.vue'
import ATabBar from '@/components/admin/ATabBar.vue'
import AEmptyState from '@/components/admin/AEmptyState.vue'
import { getPriorityColor, getStatusColor } from '@/components/admin/statusClasses.js'
import { relativeTime as sharedRelativeTime } from '@/components/admin/formatters.js'

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

function sharedPriorityClass(priority) {
  const c = getPriorityColor(priority || 'low')
  return `${c.bg} ${c.text}`
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

// relativeTime replaced by sharedRelativeTime from formatters.js
</script>
