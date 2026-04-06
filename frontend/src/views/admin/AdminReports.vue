<template>
  <div class="space-y-6">
    <APageHeader title="Reports" subtitle="Generated diagnosis reports and PDFs" lastUpdated="Auto-refreshes every 15s" @refresh="refresh" />

    <!-- Summary stats -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div v-for="stat in summaryStats" :key="stat.label"
        class="rounded-2xl border p-4 transition-colors"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center gap-2 mb-1">
          <span class="w-2 h-2 rounded-full" :class="stat.dotClass"></span>
          <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ stat.label }}</span>
        </div>
        <div class="text-xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ stat.value }}</div>
      </div>
    </div>

    <ATabBar :tabs="tabs" v-model="activeTab" @update:modelValue="switchTab" />

    <!-- Reports table -->
    <div class="rounded-2xl border overflow-hidden" :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <table class="w-full text-sm">
        <thead>
          <tr :class="isDark ? 'border-b border-slate-800' : 'border-b border-slate-100'">
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Report ID</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Case ID</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Type</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Status</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Patient</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Symptoms</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Created</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Size</th>
            <th class="text-right px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reports" :key="r.report_id"
            class="border-b transition-colors"
            :class="isDark ? 'border-slate-800/50 hover:bg-slate-800/40' : 'border-slate-50 hover:bg-slate-50'">
            <td class="px-5 py-3 font-mono text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ (r.report_id || '').slice(0, 10) }}</td>
            <td class="px-5 py-3 font-mono text-xs">
              <router-link v-if="r.case_id" :to="`/admin/cases/${r.case_id}`"
                class="hover:underline" :class="isDark ? 'text-blue-400' : 'text-blue-600'">
                {{ r.case_id.slice(0, 10) }}
              </router-link>
              <span v-else :class="isDark ? 'text-slate-500' : 'text-slate-400'">--</span>
            </td>
            <td class="px-5 py-3 text-xs capitalize" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ r.type || 'diagnosis' }}</td>
            <td class="px-5 py-3">
              <span class="inline-flex items-center gap-1.5 text-xs font-medium px-2 py-0.5 rounded-full" :class="statusClass(r.status)">
                <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(r.status)"></span>
                {{ r.status }}
              </span>
            </td>
            <td class="px-5 py-3 text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
              {{ r.age ? `${r.age}y` : '' }}{{ r.age && r.gender ? ' ' : '' }}{{ r.gender || '' }}
              <span v-if="!r.age && !r.gender" :class="isDark ? 'text-slate-500' : 'text-slate-400'">--</span>
            </td>
            <td class="px-5 py-3 text-xs truncate max-w-[180px]" :class="isDark ? 'text-white' : 'text-slate-900'">
              {{ truncate(r.symptoms, 50) }}
            </td>
            <td class="px-5 py-3 text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ relativeTime(r.created_at) }}</td>
            <td class="px-5 py-3 text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ formatSize(r.file_size) }}</td>
            <td class="px-5 py-3 text-right">
              <div class="flex items-center justify-end gap-2">
                <button v-if="r.status === 'generated' || r.status === 'failed'"
                  @click="handleRegenerate(r.report_id)"
                  :disabled="regeneratingIds.has(r.report_id)"
                  class="px-2.5 py-1 rounded-lg text-xs font-medium transition-colors"
                  :class="regeneratingIds.has(r.report_id)
                    ? (isDark ? 'bg-slate-800 text-slate-500 cursor-wait' : 'bg-slate-100 text-slate-400 cursor-wait')
                    : (isDark ? 'bg-blue-500/15 text-blue-400 hover:bg-blue-500/25' : 'bg-blue-50 text-blue-600 hover:bg-blue-100')">
                  {{ regeneratingIds.has(r.report_id) ? 'Regenerating...' : 'Regenerate' }}
                </button>
                <router-link v-if="r.case_id" :to="`/admin/cases/${r.case_id}`"
                  class="px-2.5 py-1 rounded-lg text-xs font-medium transition-colors"
                  :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                  View Case
                </router-link>
              </div>
            </td>
          </tr>
          <tr v-if="reports.length === 0">
            <td colspan="9">
              <AEmptyState title="No reports found" description="No reports found. Reports are generated after each completed diagnosis." />
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex items-center justify-between">
      <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
        Page {{ currentPage }} of {{ totalPages }} ({{ totalReports }} total)
      </span>
      <div class="flex items-center gap-1">
        <button @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1"
          class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-40"
          :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          Prev
        </button>
        <button @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages"
          class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-40"
          :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getReports, regenerateReport } from '@/services/adminApi.js'
import APageHeader from '@/components/admin/APageHeader.vue'
import ATabBar from '@/components/admin/ATabBar.vue'
import AEmptyState from '@/components/admin/AEmptyState.vue'
import { relativeTime as sharedRelativeTime, formatBytes } from '@/components/admin/formatters.js'

const { isDark } = useTheme()

const activeTab = ref('all')
const reports = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalReports = ref(0)
const regeneratingIds = reactive(new Set())
const limit = 25

const tabs = ref([
  { key: 'all', label: 'All', count: null },
  { key: 'generated', label: 'Generated', count: null },
  { key: 'failed', label: 'Failed', count: null },
  { key: 'pending', label: 'Pending', count: null },
  { key: 'regenerating', label: 'Regenerating', count: null },
])

const summaryStats = ref([
  { label: 'Total Reports', value: 0, dotClass: 'bg-slate-400' },
  { label: 'Generated', value: 0, dotClass: 'bg-emerald-500' },
  { label: 'Failed', value: 0, dotClass: 'bg-red-500' },
  { label: 'Avg Generation', value: '--', dotClass: 'bg-blue-500' },
])

async function fetchReports() {
  try {
    const params = { page: currentPage.value, limit }
    if (activeTab.value !== 'all') {
      params.status = activeTab.value
    }
    const data = await getReports(params)
    reports.value = data.reports || data || []
    totalReports.value = data.total || reports.value.length
    totalPages.value = data.total_pages || 1
    currentPage.value = data.page || currentPage.value

    // Update summary stats from the full list (when on 'all' tab)
    if (activeTab.value === 'all') {
      const all = reports.value
      summaryStats.value[0].value = totalReports.value
      summaryStats.value[1].value = all.filter(r => r.status === 'generated').length
      summaryStats.value[2].value = all.filter(r => r.status === 'failed').length

      const withDuration = all.filter(r => r.generation_time_ms)
      if (withDuration.length > 0) {
        const avg = withDuration.reduce((sum, r) => sum + r.generation_time_ms, 0) / withDuration.length
        summaryStats.value[3].value = (avg / 1000).toFixed(1) + 's'
      } else {
        summaryStats.value[3].value = '--'
      }
    }

    // Update tab counts if data provides them
    if (data.counts) {
      tabs.value.find(t => t.key === 'all').count = data.counts.total || null
      tabs.value.find(t => t.key === 'generated').count = data.counts.generated || null
      tabs.value.find(t => t.key === 'failed').count = data.counts.failed || null
      tabs.value.find(t => t.key === 'pending').count = data.counts.pending || null
      tabs.value.find(t => t.key === 'regenerating').count = data.counts.regenerating || null
    }
  } catch (e) {
    console.error('Failed to fetch reports:', e)
  }
}

function switchTab(key) {
  activeTab.value = key
  currentPage.value = 1
  fetchReports()
}

function goToPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
  fetchReports()
}

async function handleRegenerate(reportId) {
  if (regeneratingIds.has(reportId)) return
  regeneratingIds.add(reportId)
  try {
    await regenerateReport(reportId)
    await fetchReports()
  } catch (e) {
    console.error('Failed to regenerate report:', e)
  } finally {
    regeneratingIds.delete(reportId)
  }
}

function refresh() { fetchReports() }

const { start } = usePolling(fetchReports, 15000)
onMounted(() => start())

// Helpers

function statusClass(status) {
  if (status === 'generated') return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
  if (status === 'failed') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
  if (status === 'pending') return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-700'
  if (status === 'regenerating') return isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-100 text-blue-700'
  return isDark.value ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-500'
}

function statusDotClass(status) {
  if (status === 'generated') return 'bg-emerald-500'
  if (status === 'failed') return 'bg-red-500'
  if (status === 'pending') return 'bg-amber-500'
  if (status === 'regenerating') return 'bg-blue-500'
  return 'bg-slate-400'
}

function truncate(text, max) {
  if (!text) return '--'
  return text.length > max ? text.slice(0, max) + '...' : text
}

function relativeTime(ts) {
  return sharedRelativeTime(ts) || '--'
}

function formatSize(bytes) {
  return formatBytes(bytes)
}
</script>
