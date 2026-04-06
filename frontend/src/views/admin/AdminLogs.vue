<template>
  <div class="space-y-0">
    <!-- Page header -->
    <APageHeader title="Logs" subtitle="Structured system and agent logs" :show-refresh="false">
      <template #actions>
        <div class="flex items-center gap-3">
          <!-- Live indicator -->
          <div v-if="autoRefreshActive" class="flex items-center gap-1.5">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="text-[10px] font-medium" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Live</span>
          </div>
          <!-- Download -->
          <button @click="copyLogsToClipboard" class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
            :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
            {{ copyLabel }}
          </button>
        </div>
      </template>
    </APageHeader>

    <!-- Sticky filter bar -->
    <div class="sticky top-0 z-10 -mx-1 px-1 py-3 backdrop-blur-sm"
      :class="isDark ? 'bg-slate-950/80' : 'bg-slate-50/80'">
      <div class="flex flex-wrap items-center gap-2">
        <!-- Search -->
        <input v-model="filters.search" type="text" placeholder="Search messages..."
          class="flex-1 min-w-[180px] px-3 py-1.5 rounded-lg text-xs border outline-none transition-colors font-mono"
          :class="isDark
            ? 'bg-slate-900 border-slate-700 text-slate-200 placeholder-slate-500 focus:border-slate-600'
            : 'bg-white border-slate-200 text-slate-800 placeholder-slate-400 focus:border-slate-300'"
          @input="onFilterChange" />

        <!-- Level dropdown -->
        <select v-model="filters.level"
          class="px-3 py-1.5 rounded-lg text-xs border outline-none transition-colors appearance-none cursor-pointer"
          :class="isDark
            ? 'bg-slate-900 border-slate-700 text-slate-200'
            : 'bg-white border-slate-200 text-slate-800'"
          @change="onFilterChange">
          <option value="">All Levels</option>
          <option value="debug">Debug</option>
          <option value="info">Info</option>
          <option value="warning">Warning</option>
          <option value="error">Error</option>
        </select>

        <!-- Source dropdown -->
        <select v-model="filters.source"
          class="px-3 py-1.5 rounded-lg text-xs border outline-none transition-colors appearance-none cursor-pointer"
          :class="isDark
            ? 'bg-slate-900 border-slate-700 text-slate-200'
            : 'bg-white border-slate-200 text-slate-800'"
          @change="onFilterChange">
          <option value="">All Sources</option>
          <option v-for="s in sources" :key="s" :value="s.toLowerCase()">{{ s }}</option>
        </select>

        <!-- Case ID -->
        <input v-model="filters.case_id" type="text" placeholder="Case ID..."
          class="w-[120px] px-3 py-1.5 rounded-lg text-xs border outline-none transition-colors font-mono"
          :class="isDark
            ? 'bg-slate-900 border-slate-700 text-slate-200 placeholder-slate-500 focus:border-slate-600'
            : 'bg-white border-slate-200 text-slate-800 placeholder-slate-400 focus:border-slate-300'"
          @input="onFilterChange" />

        <!-- Clear filters -->
        <button v-if="hasActiveFilters" @click="clearFilters"
          class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
          :class="isDark ? 'bg-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-700' : 'bg-slate-100 text-slate-500 hover:text-slate-700 hover:bg-slate-200'">
          Clear
        </button>

        <!-- Log count -->
        <span class="text-[10px] tabular-nums ml-auto" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          {{ logs.length }}{{ total > logs.length ? ` / ${total}` : '' }} entries
        </span>
      </div>
    </div>

    <!-- Logs table -->
    <div class="rounded-2xl border overflow-hidden" :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <table class="w-full text-xs">
        <thead>
          <tr :class="isDark ? 'border-b border-slate-800' : 'border-b border-slate-100'">
            <th class="text-left px-3 py-2.5 text-[10px] font-semibold uppercase tracking-wider w-[140px]"
              :class="isDark ? 'text-slate-400' : 'text-slate-500'">Timestamp</th>
            <th class="text-left px-3 py-2.5 text-[10px] font-semibold uppercase tracking-wider w-[70px]"
              :class="isDark ? 'text-slate-400' : 'text-slate-500'">Level</th>
            <th class="text-left px-3 py-2.5 text-[10px] font-semibold uppercase tracking-wider w-[100px]"
              :class="isDark ? 'text-slate-400' : 'text-slate-500'">Source</th>
            <th class="text-left px-3 py-2.5 text-[10px] font-semibold uppercase tracking-wider"
              :class="isDark ? 'text-slate-400' : 'text-slate-500'">Message</th>
            <th class="text-left px-3 py-2.5 text-[10px] font-semibold uppercase tracking-wider w-[90px]"
              :class="isDark ? 'text-slate-400' : 'text-slate-500'">Case</th>
            <th class="w-8 px-2 py-2.5"></th>
          </tr>
        </thead>
        <tbody>
          <template v-for="(log, idx) in logs" :key="log.id || idx">
            <!-- Main row -->
            <tr @click="toggleExpand(idx)"
              class="border-b transition-colors cursor-pointer"
              :class="[
                isDark
                  ? 'border-slate-800/50 hover:bg-slate-800/40'
                  : 'border-slate-50 hover:bg-slate-50',
                idx % 2 === 1 ? (isDark ? 'bg-slate-900/40' : 'bg-slate-25') : ''
              ]">
              <td class="px-3 py-1.5 font-mono tabular-nums whitespace-nowrap" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                {{ formatTimestamp(log.timestamp) }}
              </td>
              <td class="px-3 py-1.5">
                <span class="text-[10px] font-semibold px-1.5 py-0.5 rounded uppercase" :class="sharedLevelClass(log.level)">
                  {{ log.level }}
                </span>
              </td>
              <td class="px-3 py-1.5 capitalize" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                {{ log.source || log.agent || '—' }}
              </td>
              <td class="px-3 py-1.5 truncate max-w-[400px]" :class="isDark ? 'text-slate-200' : 'text-slate-800'">
                {{ truncate(log.message, 120) }}
              </td>
              <td class="px-3 py-1.5 font-mono" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                {{ log.case_id ? log.case_id.slice(0, 8) : '—' }}
              </td>
              <td class="px-2 py-1.5 text-center">
                <svg class="w-3.5 h-3.5 transition-transform inline-block" :class="[
                  expandedIdx === idx ? 'rotate-90' : '',
                  isDark ? 'text-slate-500' : 'text-slate-400'
                ]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </td>
            </tr>
            <!-- Expanded detail row -->
            <tr v-if="expandedIdx === idx">
              <td colspan="6" class="px-0 py-0">
                <div class="px-5 py-4 border-b space-y-3"
                  :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-slate-50 border-slate-100'">
                  <!-- Full message -->
                  <div>
                    <div class="text-[10px] uppercase font-semibold mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Full Message</div>
                    <p class="text-xs whitespace-pre-wrap font-mono" :class="isDark ? 'text-slate-200' : 'text-slate-800'">{{ log.message }}</p>
                  </div>

                  <!-- Trace ID -->
                  <div v-if="log.trace_id">
                    <div class="text-[10px] uppercase font-semibold mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Trace ID</div>
                    <span class="text-xs font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ log.trace_id }}</span>
                  </div>

                  <!-- Details JSON -->
                  <div v-if="log.details && Object.keys(log.details).length > 0">
                    <div class="text-[10px] uppercase font-semibold mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Details</div>
                    <pre class="text-[11px] font-mono p-3 rounded-lg overflow-x-auto max-h-60"
                      :class="isDark ? 'bg-slate-900 text-slate-300' : 'bg-white text-slate-700 border border-slate-200'">{{ JSON.stringify(log.details, null, 2) }}</pre>
                  </div>

                  <!-- Links -->
                  <div class="flex items-center gap-3 pt-1">
                    <router-link v-if="log.case_id" :to="`/admin/cases`"
                      class="text-[11px] font-medium"
                      :class="isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'">
                      View Case &rarr;
                    </router-link>
                    <router-link v-if="log.agent || log.source" :to="`/admin/agents`"
                      class="text-[11px] font-medium"
                      :class="isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'">
                      View Agent &rarr;
                    </router-link>
                  </div>
                </div>
              </td>
            </tr>
          </template>
          <!-- Empty state -->
          <tr v-if="logs.length === 0 && !loading">
            <td colspan="6">
              <AEmptyState
                :title="hasActiveFilters ? 'No logs match your filters' : 'No log entries yet'"
                :description="hasActiveFilters ? 'Try broadening your search or clearing filters to see all entries.' : 'Log entries are recorded as agents process diagnoses. Run a diagnosis to generate log data.'"
                :action-label="hasActiveFilters ? 'Clear Filters' : ''"
                @action="clearFilters" />
            </td>
          </tr>
          <!-- Loading skeleton -->
          <tr v-if="loading && logs.length === 0">
            <td colspan="6" class="px-5 py-12 text-center text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              Loading logs...
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Load More -->
    <div v-if="logs.length < total" class="flex justify-center pt-4 pb-2">
      <button @click="loadMore" :disabled="loadingMore"
        class="px-5 py-2 rounded-xl text-xs font-medium transition-colors"
        :class="isDark
          ? 'bg-slate-800 text-slate-300 hover:bg-slate-700 disabled:opacity-50'
          : 'bg-slate-100 text-slate-600 hover:bg-slate-200 disabled:opacity-50'">
        {{ loadingMore ? 'Loading...' : `Load More (${total - logs.length} remaining)` }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getLogs } from '@/services/adminApi.js'
import APageHeader from '@/components/admin/APageHeader.vue'
import AEmptyState from '@/components/admin/AEmptyState.vue'
import { getLogLevelColor } from '@/components/admin/statusClasses.js'
import { relativeTime as sharedRelativeTime } from '@/components/admin/formatters.js'

const { isDark } = useTheme()

const sources = ['System', 'Triage', 'Diagnostician', 'Research', 'Specialist', 'Treatment', 'Safety', 'Empathy', 'Config', 'Export']

const filters = ref({
  search: '',
  level: '',
  source: '',
  case_id: '',
})

const logs = ref([])
const total = ref(0)
const loading = ref(false)
const loadingMore = ref(false)
const expandedIdx = ref(null)
const copyLabel = ref('Copy JSON')
const userInteracted = ref(false)
let filterDebounce = null

const PAGE_SIZE = 100

const hasActiveFilters = computed(() =>
  filters.value.search || filters.value.level || filters.value.source || filters.value.case_id
)

const autoRefreshActive = computed(() => isPolling.value && !userInteracted.value)

async function fetchLogs(append = false) {
  if (!append) loading.value = true
  try {
    const params = {
      limit: PAGE_SIZE,
      offset: append ? logs.value.length : 0,
    }
    if (filters.value.level) params.level = filters.value.level
    if (filters.value.source) params.source = filters.value.source
    if (filters.value.case_id) params.case_id = filters.value.case_id
    if (filters.value.search) params.search = filters.value.search

    const data = await getLogs(params)
    const fetched = data.logs || data || []
    const fetchedTotal = data.total ?? fetched.length

    if (append) {
      logs.value = [...logs.value, ...fetched]
    } else {
      logs.value = fetched
    }
    total.value = fetchedTotal
  } catch (e) {
    console.error('Failed to fetch logs:', e)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

async function pollLogs() {
  if (userInteracted.value) return
  await fetchLogs(false)
}

const { isPolling, start, stop } = usePolling(pollLogs, 10000)
onMounted(() => start())

function onFilterChange() {
  userInteracted.value = true
  expandedIdx.value = null
  clearTimeout(filterDebounce)
  filterDebounce = setTimeout(() => {
    fetchLogs(false)
  }, 300)
}

function clearFilters() {
  filters.value = { search: '', level: '', source: '', case_id: '' }
  userInteracted.value = false
  expandedIdx.value = null
  fetchLogs(false)
}

function loadMore() {
  loadingMore.value = true
  fetchLogs(true)
}

function toggleExpand(idx) {
  userInteracted.value = true
  expandedIdx.value = expandedIdx.value === idx ? null : idx
}

function formatTimestamp(ts) {
  if (!ts) return '—'
  try {
    const d = new Date(ts)
    const now = new Date()
    const isToday = d.toDateString() === now.toDateString()
    if (isToday) {
      const h = String(d.getHours()).padStart(2, '0')
      const m = String(d.getMinutes()).padStart(2, '0')
      const s = String(d.getSeconds()).padStart(2, '0')
      const ms = String(d.getMilliseconds()).padStart(3, '0')
      return `${h}:${m}:${s}.${ms}`
    }
    return d.toLocaleString(undefined, {
      month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit',
    })
  } catch (e) {
    return ts
  }
}

function sharedLevelClass(level) {
  const l = (level || '').toLowerCase()
  const mapped = l === 'warn' ? 'warning' : l
  const c = getLogLevelColor(mapped)
  return `${c.bg} ${c.text}`
}

function truncate(str, max) {
  if (!str) return '—'
  return str.length > max ? str.slice(0, max) + '...' : str
}

async function copyLogsToClipboard() {
  try {
    const payload = JSON.stringify(logs.value, null, 2)
    await navigator.clipboard.writeText(payload)
    copyLabel.value = 'Copied!'
    setTimeout(() => { copyLabel.value = 'Copy JSON' }, 2000)
  } catch (e) {
    copyLabel.value = 'Failed'
    setTimeout(() => { copyLabel.value = 'Copy JSON' }, 2000)
  }
}
</script>
