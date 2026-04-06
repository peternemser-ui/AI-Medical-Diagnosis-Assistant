<template>
  <div class="space-y-6">
    <!-- Page header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">System Overview</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Real-time platform health and operations</p>
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

    <!-- Metric cards row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="metric in metrics" :key="metric.label"
        class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center" :class="metric.iconBg">
            <span v-html="metric.icon" class="w-4 h-4"></span>
          </div>
          <span v-if="metric.trend != null" class="text-xs font-medium px-2 py-0.5 rounded-full"
            :class="metric.trend >= 0
              ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600')
              : (isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600')">
            {{ metric.trend >= 0 ? '+' : '' }}{{ metric.trend }}%
          </span>
        </div>
        <div class="text-2xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ metric.value }}</div>
        <div class="text-xs mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ metric.label }}</div>
      </div>
    </div>

    <!-- Quick stats bar -->
    <div class="flex items-center gap-4 flex-wrap px-1">
      <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
        <span class="font-semibold" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ pendingReviews }}</span> pending reviews
      </span>
      <span class="w-px h-3" :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></span>
      <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
        <span class="font-semibold" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ activeCasesCount }}</span> active cases
      </span>
      <span class="w-px h-3" :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></span>
      <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
        <span class="font-semibold" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ errorsToday }}</span> errors today
      </span>
    </div>

    <!-- Middle row: Agent Health + Alerts -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Agent Health Grid (2/3) -->
      <div class="lg:col-span-2 rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b flex items-center justify-between"
          :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Agent Health</h2>
          <router-link to="/admin/agents" class="text-xs font-medium" :class="isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'">View all →</router-link>
        </div>
        <div class="p-4 grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-4 gap-3">
          <div v-for="agent in agents" :key="agent.name"
            @click="router.push('/admin/agents')"
            class="rounded-xl border p-3 transition-colors cursor-pointer"
            :class="isDark ? 'border-slate-700/50 hover:border-slate-600 bg-slate-800/40' : 'border-slate-200 hover:border-slate-300 bg-slate-50/50'">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold capitalize" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ agent.name }}</span>
              <span class="w-2 h-2 rounded-full" :class="statusDotClass(agent.status)"></span>
            </div>
            <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ agent.latency_p50 }}s</div>
            <div class="text-[10px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ agent.cases_24h }} cases today</div>
          </div>
        </div>
      </div>

      <!-- Alerts (1/3) -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b flex items-center justify-between" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Recent Alerts</h2>
          <span v-if="pendingReviews > 0" class="text-[10px] font-medium px-2 py-0.5 rounded-full"
            :class="isDark ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-50 text-amber-700'">
            {{ pendingReviews }} pending review{{ pendingReviews === 1 ? '' : 's' }}
          </span>
        </div>
        <div class="p-3 space-y-2 max-h-80 overflow-y-auto">
          <div v-for="alert in alerts" :key="alert.id"
            @click="onAlertClick(alert)"
            class="rounded-lg border p-3 text-xs cursor-pointer transition-colors"
            :class="[alertClass(alert.severity), isDark ? 'hover:bg-slate-800/60' : 'hover:bg-slate-100/80']">
            <div class="flex items-start gap-2">
              <span class="w-1.5 h-1.5 rounded-full mt-1 flex-shrink-0" :class="alertDotClass(alert.severity)"></span>
              <div class="flex-1 min-w-0">
                <p class="font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ alert.message }}</p>
                <p class="mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ formatTime(alert.timestamp) }}</p>
              </div>
              <span class="flex-shrink-0 text-[10px]" :class="isDark ? 'text-slate-600' : 'text-slate-400'">→</span>
            </div>
          </div>
          <div v-if="alerts.length === 0" class="text-center py-6 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No alerts — all systems nominal
          </div>
        </div>
      </div>
    </div>

    <!-- Pipeline snapshot -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b flex items-center justify-between"
        :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Active Pipelines</h2>
        <span class="text-xs px-2 py-0.5 rounded-full" :class="isDark ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-600'">{{ activePipelines.length }} running</span>
      </div>
      <div v-if="activePipelines.length > 0" class="p-4 space-y-3">
        <div v-for="pipeline in activePipelines" :key="pipeline.case_id"
          class="flex items-center gap-4 p-3 rounded-xl border"
          :class="isDark ? 'border-slate-700/40 bg-slate-800/30' : 'border-slate-100 bg-slate-50/50'">
          <div class="flex-shrink-0">
            <span class="text-xs font-mono" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ pipeline.case_id.slice(0, 8) }}</span>
          </div>
          <!-- Pipeline steps -->
          <div class="flex-1 flex items-center gap-1">
            <div v-for="(step, i) in pipelineSteps" :key="step"
              class="flex items-center gap-1">
              <div class="w-6 h-6 rounded-full flex items-center justify-center text-[9px] font-bold transition-colors"
                :class="getStepClass(pipeline.stage, step)">
                {{ i + 1 }}
              </div>
              <div v-if="i < pipelineSteps.length - 1" class="w-4 h-px" :class="isStepComplete(pipeline.stage, step) ? 'bg-emerald-500' : (isDark ? 'bg-slate-700' : 'bg-slate-200')"></div>
            </div>
          </div>
          <div class="flex-shrink-0 text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ pipeline.elapsed_s.toFixed(1) }}s</div>
        </div>
      </div>
      <div v-else class="p-8 text-center text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
        No active pipelines — system idle
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getOverview, getReviews } from '@/services/adminApi.js'

const { isDark } = useTheme()
const router = useRouter()

const metrics = ref([
  { label: 'Active Cases', value: '—', trend: null, iconBg: 'bg-blue-500/10', icon: '<svg fill="none" stroke="#3b82f6" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08"/></svg>' },
  { label: 'Avg Turnaround', value: '—', trend: null, iconBg: 'bg-emerald-500/10', icon: '<svg fill="none" stroke="#10b981" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' },
  { label: 'Error Rate (24h)', value: '—', trend: null, iconBg: 'bg-red-500/10', icon: '<svg fill="none" stroke="#ef4444" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"/></svg>' },
  { label: 'Agent Uptime', value: '—', trend: null, iconBg: 'bg-purple-500/10', icon: '<svg fill="none" stroke="#a855f7" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"/></svg>' },
])
const agents = ref([])
const alerts = ref([])
const activePipelines = ref([])
const lastUpdated = ref('—')
const pendingReviews = ref(0)
const activeCasesCount = ref(0)
const errorsToday = ref(0)

const pipelineSteps = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']

async function fetchData() {
  try {
    const data = await getOverview()
    const sys = data.system || {}
    metrics.value[0].value = sys.active_cases ?? 0
    metrics.value[1].value = ((sys.avg_pipeline_duration_ms ?? 0) / 1000).toFixed(1) + 's'
    metrics.value[2].value = sys.error_cases ?? 0
    metrics.value[3].value = sys.cases_last_24h ?? 0
    // No hardcoded trends — leave as null (real trend data not available)
    metrics.value[0].trend = null
    metrics.value[1].trend = null
    metrics.value[2].trend = null
    metrics.value[3].trend = null

    // Quick stats
    activeCasesCount.value = sys.active_cases ?? 0
    errorsToday.value = sys.error_cases ?? 0

    // Map agent data to match the template
    agents.value = (data.agents || []).map(a => ({
      name: a.name,
      status: a.status,
      latency_p50: (a.avg_latency_ms / 1000).toFixed(1),
      cases_24h: a.cases_processed,
      errors_24h: a.error_count,
      model: ''
    }))
    alerts.value = (data.recent_alerts || []).map(a => ({
      id: a.id || Math.random(),
      severity: a.severity,
      message: a.message,
      timestamp: a.timestamp,
      case_id: a.case_id || null
    }))
    activePipelines.value = (data.recent_cases || [])
      .filter(c => c.status === 'active' || c.status === 'running')
      .map(c => ({
        case_id: c.case_id,
        stage: c.current_stage || 'triage',
        elapsed_s: (c.duration_ms || 0) / 1000
      }))
    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (e) {
    console.error('Failed to fetch admin overview:', e)
  }

  // Fetch pending reviews count
  try {
    const reviews = await getReviews({ status: 'pending' })
    pendingReviews.value = reviews.total || reviews.items?.length || 0
  } catch (e) {
    // reviews endpoint may not exist yet — silently ignore
  }
}

function refresh() { fetchData() }

function onAlertClick(alert) {
  if (alert.case_id) {
    router.push(`/admin/cases?highlight=${alert.case_id}`)
  } else {
    router.push('/admin/cases')
  }
}

const { start } = usePolling(fetchData, 15000)
onMounted(() => start())

function statusDotClass(status) {
  if (status === 'healthy' || status === 'running') return 'bg-emerald-500'
  if (status === 'degraded') return 'bg-amber-500'
  if (status === 'error') return 'bg-red-500'
  if (status === 'paused') return 'bg-blue-500'
  return 'bg-slate-500'
}

function alertClass(severity) {
  if (severity === 'error' || severity === 'critical') return isDark.value ? 'border-red-500/20 bg-red-500/5' : 'border-red-200 bg-red-50'
  if (severity === 'warning') return isDark.value ? 'border-amber-500/20 bg-amber-500/5' : 'border-amber-200 bg-amber-50'
  return isDark.value ? 'border-slate-700/40 bg-slate-800/30' : 'border-slate-200 bg-slate-50'
}

function alertDotClass(severity) {
  if (severity === 'error' || severity === 'critical') return 'bg-red-500'
  if (severity === 'warning') return 'bg-amber-500'
  return 'bg-blue-500'
}

function formatTime(ts) {
  if (!ts) return ''
  try { return new Date(ts).toLocaleTimeString() } catch (e) { return ts }
}

function getStepClass(currentStage, step) {
  const stepIdx = pipelineSteps.indexOf(step)
  const currentIdx = pipelineSteps.indexOf(currentStage)
  if (stepIdx < currentIdx) return isDark.value ? 'bg-emerald-500/20 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
  if (stepIdx === currentIdx) return 'bg-blue-500 text-white animate-pulse'
  return isDark.value ? 'bg-slate-800 text-slate-500' : 'bg-slate-200 text-slate-400'
}

function isStepComplete(currentStage, step) {
  return pipelineSteps.indexOf(step) < pipelineSteps.indexOf(currentStage)
}
</script>
