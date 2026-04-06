<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Cases</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Track diagnostic pipeline progress</p>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex items-center gap-1 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
      <button v-for="tab in tabs" :key="tab.key"
        @click="activeTab = tab.key"
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

    <!-- Cases table -->
    <div class="rounded-2xl border overflow-hidden" :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <table class="w-full text-sm">
        <thead>
          <tr :class="isDark ? 'border-b border-slate-800' : 'border-b border-slate-100'">
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Case ID</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Patient</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Chief Complaint</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Stage</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Urgency</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Duration</th>
            <th class="text-right px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in cases" :key="c.case_id"
            @click="openCase(c.case_id)"
            class="border-b transition-colors cursor-pointer"
            :class="isDark ? 'border-slate-800/50 hover:bg-slate-800/40' : 'border-slate-50 hover:bg-slate-50'">
            <td class="px-5 py-3 font-mono text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ c.case_id.slice(0, 10) }}</td>
            <td class="px-5 py-3 text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ c.age }}y {{ c.gender }}</td>
            <td class="px-5 py-3 text-xs truncate max-w-[200px]" :class="isDark ? 'text-white' : 'text-slate-900'">{{ c.symptoms?.slice(0, 60) }}{{ c.symptoms?.length > 60 ? '...' : '' }}</td>
            <td class="px-5 py-3">
              <span class="text-xs font-medium capitalize" :class="isDark ? 'text-blue-400' : 'text-blue-600'">{{ c.current_stage || '—' }}</span>
            </td>
            <td class="px-5 py-3">
              <span class="text-xs font-medium px-2 py-0.5 rounded-full" :class="urgencyClass(c.urgency)">{{ c.urgency || 'routine' }}</span>
            </td>
            <td class="px-5 py-3 tabular-nums text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ c.duration || '—' }}</td>
            <td class="px-5 py-3 text-right">
              <span class="text-xs font-medium px-2 py-0.5 rounded-full" :class="statusClass(c.status)">{{ c.status }}</span>
            </td>
          </tr>
          <tr v-if="cases.length === 0">
            <td colspan="7" class="px-5 py-12 text-center text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              No cases found. Run a diagnosis to see cases here.
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Case detail drawer -->
    <ASheet :open="!!selectedCase" :title="'Case ' + (selectedCase?.case_id || '').slice(0,10)" @close="selectedCase = null" width="lg">
      <template v-if="selectedCase">
        <!-- Case overview -->
        <div class="space-y-5">
          <!-- Status / Urgency row -->
          <div class="flex items-center gap-3 flex-wrap">
            <span class="text-xs font-medium px-2.5 py-1 rounded-full" :class="statusClass(selectedCase.status)">{{ selectedCase.status }}</span>
            <span class="text-xs font-medium px-2.5 py-1 rounded-full" :class="urgencyClass(selectedCase.urgency)">{{ selectedCase.urgency || 'routine' }}</span>
            <span v-if="selectedCase.current_stage" class="text-xs font-medium capitalize" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Stage: {{ selectedCase.current_stage }}</span>
          </div>

          <!-- Case ID -->
          <div>
            <label class="text-[10px] uppercase tracking-wider font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Case ID</label>
            <p class="font-mono text-xs mt-0.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ selectedCase.case_id }}</p>
          </div>

          <!-- Patient info -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-[10px] uppercase tracking-wider font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Age</label>
              <p class="text-sm mt-0.5" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ selectedCase.age ?? '—' }}</p>
            </div>
            <div>
              <label class="text-[10px] uppercase tracking-wider font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Gender</label>
              <p class="text-sm mt-0.5" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ selectedCase.gender ?? '—' }}</p>
            </div>
          </div>

          <!-- Symptoms -->
          <div>
            <label class="text-[10px] uppercase tracking-wider font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Symptoms</label>
            <p class="text-sm mt-1 leading-relaxed" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ selectedCase.symptoms || '—' }}</p>
          </div>

          <!-- Timestamps -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-[10px] uppercase tracking-wider font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Created</label>
              <p class="text-xs mt-0.5 tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ formatTimestamp(selectedCase.created_at) }}</p>
            </div>
            <div>
              <label class="text-[10px] uppercase tracking-wider font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Completed</label>
              <p class="text-xs mt-0.5 tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ formatTimestamp(selectedCase.completed_at) }}</p>
            </div>
          </div>

          <!-- Duration -->
          <div v-if="selectedCase.duration || selectedCase.duration_ms">
            <label class="text-[10px] uppercase tracking-wider font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Duration</label>
            <p class="text-sm mt-0.5 tabular-nums" :class="isDark ? 'text-slate-200' : 'text-slate-700'">
              {{ selectedCase.duration || ((selectedCase.duration_ms / 1000).toFixed(1) + 's') }}
            </p>
          </div>

          <!-- Pipeline Timeline -->
          <div>
            <label class="text-[10px] uppercase tracking-wider font-semibold mb-3 block" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Pipeline Timeline</label>
            <div v-if="selectedCase.timeline && selectedCase.timeline.length > 0" class="relative ml-3">
              <!-- Vertical line -->
              <div class="absolute left-[5px] top-2 bottom-2 w-px" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>
              <!-- Events -->
              <div v-for="(event, i) in selectedCase.timeline" :key="i" class="relative pl-6 pb-4 last:pb-0">
                <!-- Dot -->
                <div class="absolute left-0 top-1.5 w-[11px] h-[11px] rounded-full border-2"
                  :class="timelineDotClass(event.type || event.status)"></div>
                <!-- Content -->
                <div>
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-xs font-semibold capitalize" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ event.stage || event.event || event.agent || '—' }}</span>
                    <span v-if="event.duration_ms" class="text-[10px] tabular-nums px-1.5 py-0.5 rounded-full"
                      :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'">{{ (event.duration_ms / 1000).toFixed(2) }}s</span>
                    <span v-if="event.duration && !event.duration_ms" class="text-[10px] tabular-nums px-1.5 py-0.5 rounded-full"
                      :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'">{{ event.duration }}</span>
                  </div>
                  <p v-if="event.description || event.message || event.findings" class="text-xs mt-0.5 leading-relaxed"
                    :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ event.description || event.message || event.findings }}</p>
                  <p class="text-[10px] mt-0.5 tabular-nums" :class="isDark ? 'text-slate-600' : 'text-slate-400'">{{ formatTimestamp(event.timestamp) }}</p>
                </div>
              </div>
            </div>
            <p v-else class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No timeline data available.</p>
          </div>
        </div>
      </template>
    </ASheet>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getCases, getCaseCounts, getCase, getCaseTimeline } from '@/services/adminApi.js'
import ASheet from '@/components/admin/ASheet.vue'

const { isDark } = useTheme()
const activeTab = ref('all')
const cases = ref([])
const selectedCase = ref(null)
const tabCounts = ref({})

const tabs = computed(() => [
  { key: 'all', label: 'All', count: tabCounts.value.all ?? null },
  { key: 'active', label: 'Active', count: tabCounts.value.active ?? null },
  { key: 'completed', label: 'Completed', count: tabCounts.value.completed ?? null },
  { key: 'errored', label: 'Errored', count: tabCounts.value.errored ?? tabCounts.value.error ?? null },
])

async function fetchCases() {
  try {
    const data = await getCases({ status: activeTab.value === 'all' ? '' : activeTab.value, limit: 50 })
    cases.value = data.cases || data || []
  } catch (e) {
    console.error('Failed to fetch cases:', e)
  }
}

async function fetchCounts() {
  try {
    const counts = await getCaseCounts()
    tabCounts.value = counts
  } catch (e) {
    // counts are optional — silently ignore
  }
}

async function fetchData() {
  await Promise.all([fetchCases(), fetchCounts()])
}

// Re-fetch when tab changes
watch(activeTab, () => fetchCases())

async function openCase(caseId) {
  try {
    const [detail, timeline] = await Promise.all([
      getCase(caseId),
      getCaseTimeline(caseId)
    ])
    selectedCase.value = { ...detail, timeline: timeline?.events || timeline || [] }
  } catch (e) {
    console.error('Failed to load case:', e)
  }
}

const { start } = usePolling(fetchData, 15000)
onMounted(() => start())

function urgencyClass(u) {
  if (u === 'emergency') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
  if (u === 'urgent') return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-700'
  if (u === 'soon') return isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-100 text-blue-700'
  return isDark.value ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-500'
}

function statusClass(s) {
  if (s === 'completed') return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
  if (s === 'active' || s === 'running') return isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-100 text-blue-700'
  if (s === 'error' || s === 'failed') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700'
  return isDark.value ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-500'
}

function timelineDotClass(type) {
  if (type === 'completed' || type === 'complete' || type === 'success')
    return isDark.value ? 'border-emerald-500 bg-emerald-500/20' : 'border-emerald-500 bg-emerald-50'
  if (type === 'started' || type === 'start' || type === 'running' || type === 'active')
    return isDark.value ? 'border-blue-500 bg-blue-500/20' : 'border-blue-500 bg-blue-50'
  if (type === 'error' || type === 'failed')
    return isDark.value ? 'border-red-500 bg-red-500/20' : 'border-red-500 bg-red-50'
  return isDark.value ? 'border-slate-500 bg-slate-500/20' : 'border-slate-400 bg-slate-100'
}

function formatTimestamp(ts) {
  if (!ts) return '—'
  try {
    const d = new Date(ts)
    return d.toLocaleString()
  } catch (e) {
    return ts
  }
}
</script>
