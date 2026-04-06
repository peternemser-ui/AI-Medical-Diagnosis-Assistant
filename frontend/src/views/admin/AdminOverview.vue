<template>
  <div class="space-y-6">
    <!-- Page header -->
    <APageHeader
      title="Mission Control"
      subtitle="Real-time platform health and operations"
      :lastUpdated="lastUpdated"
      @refresh="refresh"
    />

    <!-- KPI Strip -->
    <AKpiStrip :items="kpiItems" :cols="4" />

    <!-- Needs Attention + Alerts row -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Needs Attention (2/3) -->
      <div class="lg:col-span-2 rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b flex items-center justify-between"
          :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Needs Attention</h2>
          <span v-if="attentionItems.length > 0" class="text-[10px] font-bold px-2 py-0.5 rounded-full"
            :class="isDark ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-50 text-amber-700'">
            {{ attentionItems.length }} item{{ attentionItems.length === 1 ? '' : 's' }}
          </span>
        </div>
        <div v-if="attentionItems.length > 0" class="p-3 space-y-2 max-h-72 overflow-y-auto">
          <div v-for="item in attentionItems" :key="item.id"
            @click="onAttentionClick(item)"
            class="flex items-center gap-3 rounded-xl border p-3 text-xs cursor-pointer transition-colors"
            :class="[attentionCardClass(item.priority), isDark ? 'hover:bg-slate-800/60' : 'hover:bg-slate-50']">
            <span class="flex-shrink-0 w-5 h-5 rounded-md flex items-center justify-center text-[9px] font-bold"
              :class="priorityBadgeClass(item.priority)">
              {{ item.priority === 'critical' ? '!' : item.priority === 'high' ? '!!' : '--' }}
            </span>
            <div class="flex-1 min-w-0">
              <p class="font-medium truncate" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ item.message }}</p>
              <p class="mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ item.sublabel }}</p>
            </div>
            <span class="text-[10px] flex-shrink-0" :class="isDark ? 'text-slate-600' : 'text-slate-400'">{{ item.time }}</span>
          </div>
        </div>
        <AEmptyState
          v-else
          title="All clear"
          description="No pending reviews, errors, or critical alerts right now."
          variant="default"
        />
      </div>

      <!-- Alerts (1/3) -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b flex items-center justify-between" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Alerts</h2>
        </div>
        <div v-if="alerts.length > 0" class="p-3 space-y-2 max-h-80 overflow-y-auto">
          <div v-for="alert in alerts" :key="alert.id"
            @click="onAlertClick(alert)"
            class="rounded-lg border p-3 text-xs cursor-pointer transition-colors"
            :class="[alertClass(alert.severity), isDark ? 'hover:bg-slate-800/60' : 'hover:bg-slate-100/80']">
            <div class="flex items-start gap-2">
              <span class="flex-shrink-0 mt-0.5 text-[9px] font-bold uppercase px-1.5 py-0.5 rounded"
                :class="severityBadgeClass(alert.severity)">
                {{ alert.severity }}
              </span>
              <div class="flex-1 min-w-0">
                <p class="font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ alert.message }}</p>
                <p class="mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ formatTime(alert.timestamp) }}</p>
              </div>
            </div>
          </div>
        </div>
        <AEmptyState
          v-else
          title="No alerts"
          description="All systems nominal."
          variant="default"
        />
      </div>
    </div>

    <!-- Agent Pipeline Health -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b flex items-center justify-between"
        :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Agent Pipeline Health</h2>
        <router-link to="/admin/agents" class="text-xs font-medium" :class="isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'">View all</router-link>
      </div>
      <div v-if="agents.length > 0" class="p-4">
        <div class="flex items-stretch gap-3 overflow-x-auto pb-1">
          <div v-for="agent in agents" :key="agent.name"
            @click="router.push('/admin/agents')"
            class="flex-shrink-0 w-36 rounded-xl border p-3 transition-colors cursor-pointer"
            :class="[agentCardBorder(agent.health), isDark ? 'bg-slate-800/40' : 'bg-slate-50/50']">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold capitalize truncate" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ agent.name }}</span>
              <AStatusBadge :status="agent.health === 'failing' ? 'error' : agent.health" :label="''" size="sm" :pulse="agent.health === 'healthy'" />
            </div>
            <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ agent.latency_p50 }}s</div>
            <div class="text-[10px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ agent.cases_24h }} cases / {{ agent.errors_24h }} err</div>
            <div class="mt-2 w-full rounded-full h-1 overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
              <div class="h-full rounded-full transition-all duration-500"
                :class="agent.health === 'healthy' ? 'bg-emerald-500' : agent.health === 'degraded' ? 'bg-amber-500' : 'bg-red-500'"
                :style="{ width: agentHealthPercent(agent) + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
      <AEmptyState
        v-else
        title="No agents reporting"
        description="Agent health data will appear once the pipeline processes cases."
        variant="info"
      />
    </div>

    <!-- Recent Activity -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b flex items-center justify-between"
        :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Recent Activity</h2>
        <router-link to="/admin/cases" class="text-xs font-medium" :class="isDark ? 'text-blue-400 hover:text-blue-300' : 'text-blue-600 hover:text-blue-700'">All cases</router-link>
      </div>
      <div v-if="recentCases.length > 0" class="divide-y" :class="isDark ? 'divide-slate-800' : 'divide-slate-100'">
        <div v-for="c in recentCases" :key="c.case_id"
          @click="router.push(`/admin/cases?highlight=${c.case_id}`)"
          class="flex items-center gap-4 px-5 py-3 cursor-pointer transition-colors"
          :class="isDark ? 'hover:bg-slate-800/40' : 'hover:bg-slate-50'">
          <span class="text-xs font-mono flex-shrink-0 w-20 truncate" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ c.case_id.slice(0, 8) }}</span>
          <span class="flex-shrink-0">
            <span class="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded"
              :class="caseStatusClass(c.status)">{{ c.status }}</span>
          </span>
          <span class="flex-1 text-xs truncate" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ c.diagnosis || 'Processing...' }}</span>
          <span class="text-xs tabular-nums flex-shrink-0" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ c.duration }}</span>
        </div>
      </div>
      <AEmptyState
        v-else
        title="No recent cases"
        description="Cases will appear here as they are processed through the pipeline."
        variant="default"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getOverview, getReviews } from '@/services/adminApi.js'
import { deriveAgentHealth, getStatusColor, getPriorityColor } from '@/components/admin/statusClasses.js'
import { relativeTime, formatDuration } from '@/components/admin/formatters.js'
import APageHeader from '@/components/admin/APageHeader.vue'
import AKpiStrip from '@/components/admin/AKpiStrip.vue'
import AEmptyState from '@/components/admin/AEmptyState.vue'
import AStatusBadge from '@/components/admin/AStatusBadge.vue'

const { isDark } = useTheme()
const router = useRouter()

// --- State ---
const agents = ref([])
const alerts = ref([])
const recentCases = ref([])
const lastUpdated = ref('--')
const pendingReviews = ref(0)
const activeCasesCount = ref(0)
const errorsToday = ref(0)
const avgTurnaround = ref('--')
const qualityScore = ref('--')

// --- KPI strip (computed from state) ---
const kpiItems = computed(() => [
  { label: 'Active Cases', value: activeCasesCount.value, sublabel: 'Currently in pipeline' },
  { label: 'Avg Turnaround', value: avgTurnaround.value, sublabel: 'Pipeline duration' },
  { label: 'Error Rate (24h)', value: errorsToday.value, sublabel: 'Failures today' },
  { label: 'Quality Score', value: qualityScore.value, sublabel: 'Based on reviews' },
])

// --- Needs Attention (merged, sorted by priority) ---
const attentionItems = computed(() => {
  const items = []
  const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 }

  // Pending reviews
  if (pendingReviews.value > 0) {
    items.push({
      id: 'pending-reviews',
      priority: pendingReviews.value >= 5 ? 'high' : 'medium',
      message: `${pendingReviews.value} pending review${pendingReviews.value === 1 ? '' : 's'}`,
      sublabel: 'Awaiting clinician review',
      time: '',
      route: '/admin/reviews'
    })
  }

  // Critical/error alerts
  alerts.value
    .filter(a => a.severity === 'critical' || a.severity === 'error')
    .slice(0, 5)
    .forEach(a => {
      items.push({
        id: `alert-${a.id}`,
        priority: a.severity === 'critical' ? 'critical' : 'high',
        message: a.message,
        sublabel: 'Alert',
        time: formatTime(a.timestamp),
        route: a.case_id ? `/admin/cases?highlight=${a.case_id}` : '/admin/cases'
      })
    })

  // Failing agents
  agents.value
    .filter(a => a.health === 'failing')
    .forEach(a => {
      items.push({
        id: `agent-failing-${a.name}`,
        priority: 'critical',
        message: `Agent "${a.name}" is failing (${a.errors_24h} errors)`,
        sublabel: 'Agent health',
        time: '',
        route: '/admin/agents'
      })
    })

  items.sort((a, b) => (priorityOrder[a.priority] ?? 99) - (priorityOrder[b.priority] ?? 99))
  return items
})

// --- Data fetching (preserved from original) ---
async function fetchData() {
  try {
    const data = await getOverview()
    const sys = data.system || {}

    activeCasesCount.value = sys.active_cases ?? 0
    errorsToday.value = sys.error_cases ?? 0
    avgTurnaround.value = formatDuration(sys.avg_pipeline_duration_ms ?? 0)
    // Quality score: derive from review data or system data if available
    qualityScore.value = sys.quality_score != null ? `${sys.quality_score}%` : '--'

    // Map agent data with derived health
    agents.value = (data.agents || []).map(a => ({
      name: a.name,
      status: a.status,
      health: deriveAgentHealth(a.error_count || 0),
      latency_p50: (a.avg_latency_ms / 1000).toFixed(1),
      cases_24h: a.cases_processed,
      errors_24h: a.error_count || 0,
    }))

    alerts.value = (data.recent_alerts || []).map(a => ({
      id: a.id || Math.random(),
      severity: a.severity,
      message: a.message,
      timestamp: a.timestamp,
      case_id: a.case_id || null
    }))

    // Recent cases (last 5)
    recentCases.value = (data.recent_cases || []).slice(0, 5).map(c => ({
      case_id: c.case_id,
      status: c.status || 'unknown',
      diagnosis: c.primary_diagnosis || c.diagnosis || '',
      duration: formatDuration(c.duration_ms || 0),
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
    // reviews endpoint may not exist yet
  }
}

function refresh() { fetchData() }

const { start } = usePolling(fetchData, 15000)
onMounted(() => start())

// --- UI helpers ---
function formatTime(ts) {
  if (!ts) return ''
  try { return relativeTime(ts) } catch (e) { return String(ts) }
}

function onAlertClick(alert) {
  if (alert.case_id) {
    router.push(`/admin/cases?highlight=${alert.case_id}`)
  } else {
    router.push('/admin/cases')
  }
}

function onAttentionClick(item) {
  if (item.route) router.push(item.route)
}

function alertClass(severity) {
  if (severity === 'error' || severity === 'critical') return isDark.value ? 'border-red-500/20 bg-red-500/5' : 'border-red-200 bg-red-50'
  if (severity === 'warning') return isDark.value ? 'border-amber-500/20 bg-amber-500/5' : 'border-amber-200 bg-amber-50'
  return isDark.value ? 'border-slate-700/40 bg-slate-800/30' : 'border-slate-200 bg-slate-50'
}

function severityBadgeClass(severity) {
  if (severity === 'critical') return isDark.value ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-700'
  if (severity === 'error') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600'
  if (severity === 'warning') return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-700'
  return isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-600'
}

function attentionCardClass(priority) {
  if (priority === 'critical') return isDark.value ? 'border-red-500/20 bg-red-500/5' : 'border-red-200 bg-red-50/50'
  if (priority === 'high') return isDark.value ? 'border-orange-500/20 bg-orange-500/5' : 'border-orange-200 bg-orange-50/50'
  return isDark.value ? 'border-slate-700/40 bg-slate-800/30' : 'border-slate-200 bg-slate-50/50'
}

function priorityBadgeClass(priority) {
  if (priority === 'critical') return isDark.value ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-600'
  if (priority === 'high') return isDark.value ? 'bg-orange-500/20 text-orange-400' : 'bg-orange-100 text-orange-600'
  return isDark.value ? 'bg-slate-700 text-slate-400' : 'bg-slate-200 text-slate-500'
}

function agentCardBorder(health) {
  if (health === 'healthy') return isDark.value ? 'border-emerald-500/20' : 'border-emerald-200'
  if (health === 'degraded') return isDark.value ? 'border-amber-500/20' : 'border-amber-200'
  return isDark.value ? 'border-red-500/20' : 'border-red-200'
}

function agentHealthPercent(agent) {
  // Visual indicator: healthy=100, degraded=60, failing=20
  if (agent.health === 'healthy') return 100
  if (agent.health === 'degraded') return 60
  return 20
}

function caseStatusClass(status) {
  if (status === 'completed' || status === 'complete') return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700'
  if (status === 'active' || status === 'running') return isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-700'
  if (status === 'error' || status === 'failed') return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600'
  return isDark.value ? 'bg-slate-700 text-slate-400' : 'bg-slate-100 text-slate-500'
}
</script>
