<template>
  <div class="space-y-6">
    <!-- Page header -->
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Analytics</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Pipeline performance metrics and trends</p>
      </div>
      <div class="flex items-center gap-3">
        <!-- Period selector -->
        <div class="flex rounded-lg overflow-hidden border"
          :class="isDark ? 'border-slate-700' : 'border-slate-200'">
          <button v-for="p in periods" :key="p.value"
            @click="setPeriod(p.value)"
            class="px-3 py-1.5 text-xs font-medium transition-colors"
            :class="period === p.value
              ? (isDark ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-50 text-blue-700')
              : (isDark ? 'bg-slate-900 text-slate-400 hover:text-slate-200' : 'bg-white text-slate-500 hover:text-slate-700')">
            {{ p.label }}
          </button>
        </div>
        <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          Last updated: {{ lastUpdated }}
        </span>
        <button @click="refresh" class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
          :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          Refresh
        </button>
      </div>
    </div>

    <!-- Summary metrics row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="metric in summaryMetrics" :key="metric.label"
        class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center" :class="metric.iconBg">
            <span v-html="metric.icon" class="w-4 h-4"></span>
          </div>
        </div>
        <div class="text-2xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ metric.value }}</div>
        <div class="text-xs mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ metric.label }}</div>
      </div>
    </div>

    <!-- Charts grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

      <!-- Throughput -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Throughput</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Cases processed per time bucket</p>
        </div>
        <div class="p-5">
          <div v-if="throughput.length > 0" class="space-y-2">
            <div v-for="(bucket, i) in throughput" :key="i" class="flex items-center gap-3">
              <span class="text-[10px] tabular-nums w-14 text-right flex-shrink-0"
                :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ bucket.label }}</span>
              <div class="flex-1 h-5 rounded-md overflow-hidden"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <div class="h-full rounded-md bg-blue-500 transition-all duration-500"
                  :style="{ width: throughputBarWidth(bucket.count) }"></div>
              </div>
              <span class="text-[10px] tabular-nums w-8 flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ bucket.count }}</span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No throughput data available
          </div>
        </div>
      </div>

      <!-- Agent Latency -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Agent Latency</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Average processing time per agent</p>
        </div>
        <div class="p-5">
          <div v-if="agentLatency.length > 0" class="space-y-2.5">
            <div v-for="agent in agentLatency" :key="agent.name" class="flex items-center gap-3">
              <span class="text-[10px] font-medium capitalize w-20 text-right flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ agent.name }}</span>
              <div class="flex-1 h-5 rounded-md overflow-hidden"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <div class="h-full rounded-md transition-all duration-500"
                  :class="latencyBarColor(agent.avg_ms)"
                  :style="{ width: latencyBarWidth(agent.avg_ms) }"></div>
              </div>
              <span class="text-[10px] tabular-nums w-12 flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ (agent.avg_ms / 1000).toFixed(1) }}s</span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No latency data available
          </div>
        </div>
      </div>

      <!-- Error Rates by Agent -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Error Rates by Agent</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Percentage of failed executions per agent</p>
        </div>
        <div class="p-5">
          <div v-if="errorRates.length > 0" class="space-y-2.5">
            <div v-for="agent in errorRates" :key="agent.name" class="flex items-center gap-3">
              <span class="text-[10px] font-medium capitalize w-20 text-right flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ agent.name }}</span>
              <div class="flex-1 h-5 rounded-md overflow-hidden"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <div class="h-full rounded-md bg-red-500 transition-all duration-500"
                  :style="{ width: agent.rate + '%' }"></div>
              </div>
              <span class="text-[10px] tabular-nums w-10 flex-shrink-0"
                :class="agent.rate > 5 ? 'text-red-400 font-medium' : (isDark ? 'text-slate-300' : 'text-slate-600')">
                {{ agent.rate.toFixed(1) }}%
              </span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No error data available
          </div>
        </div>
      </div>

      <!-- Urgency Distribution -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Urgency Distribution</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Breakdown of case urgency levels</p>
        </div>
        <div class="p-5">
          <div v-if="urgencyTotal > 0">
            <!-- Stacked bar -->
            <div class="h-8 rounded-lg overflow-hidden flex">
              <div v-for="seg in urgencySegments" :key="seg.key"
                class="h-full transition-all duration-500 relative group"
                :class="seg.color"
                :style="{ width: seg.pct + '%' }">
                <div v-if="seg.pct > 4" class="absolute inset-0 flex items-center justify-center text-[9px] font-bold text-white">
                  {{ seg.pct.toFixed(0) }}%
                </div>
              </div>
            </div>
            <!-- Legend -->
            <div class="flex flex-wrap gap-4 mt-3">
              <div v-for="seg in urgencySegments" :key="seg.key" class="flex items-center gap-1.5">
                <div class="w-2.5 h-2.5 rounded-sm" :class="seg.color"></div>
                <span class="text-[10px] capitalize" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                  {{ seg.key }} ({{ seg.count }})
                </span>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No urgency data available
          </div>
        </div>
      </div>

      <!-- Confidence Distribution -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Confidence Distribution</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Histogram of diagnostic confidence scores</p>
        </div>
        <div class="p-5">
          <div v-if="confidenceBuckets.length > 0">
            <div class="flex items-end gap-1.5 h-32">
              <div v-for="bucket in confidenceBuckets" :key="bucket.label"
                class="flex-1 flex flex-col items-center gap-1">
                <span class="text-[9px] tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ bucket.count }}</span>
                <div class="w-full rounded-t-md transition-all duration-500"
                  :class="confidenceBarColor(bucket.rangeStart)"
                  :style="{ height: confidenceBarHeight(bucket.count) }"></div>
              </div>
            </div>
            <div class="flex gap-1.5 mt-1">
              <div v-for="bucket in confidenceBuckets" :key="bucket.label"
                class="flex-1 text-center text-[9px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                {{ bucket.label }}
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No confidence data available
          </div>
        </div>
      </div>

      <!-- Completion Funnel -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Completion Funnel</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">How many cases reach each pipeline stage</p>
        </div>
        <div class="p-5">
          <div v-if="completionFunnel.length > 0" class="space-y-2">
            <div v-for="(stage, i) in completionFunnel" :key="stage.name" class="flex items-center gap-3">
              <span class="text-[10px] font-medium capitalize w-20 text-right flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ stage.name }}</span>
              <div class="flex-1 h-5 rounded-md overflow-hidden"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <div class="h-full rounded-md transition-all duration-500"
                  :class="funnelBarColor(i)"
                  :style="{ width: funnelBarWidth(stage.count) }"></div>
              </div>
              <span class="text-[10px] tabular-nums w-10 flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ stage.count }}</span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No funnel data available
          </div>
        </div>
      </div>

      <!-- Top Failure Categories -->
      <div class="rounded-2xl border overflow-hidden lg:col-span-2"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Top Failure Categories</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Most common failure reasons ranked by occurrence</p>
        </div>
        <div class="p-5">
          <div v-if="failureCategories.length > 0" class="space-y-2">
            <div v-for="(cat, i) in failureCategories" :key="cat.category"
              class="flex items-center gap-3">
              <span class="text-[10px] font-bold w-5 text-right flex-shrink-0"
                :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ i + 1 }}</span>
              <span class="text-xs w-48 truncate flex-shrink-0"
                :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ cat.category }}</span>
              <div class="flex-1 h-4 rounded-md overflow-hidden"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <div class="h-full rounded-md bg-red-500/80 transition-all duration-500"
                  :style="{ width: failureBarWidth(cat.count) }"></div>
              </div>
              <span class="text-[10px] tabular-nums w-8 flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ cat.count }}</span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No failure data available
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getAnalytics } from '@/services/adminApi.js'

const { isDark } = useTheme()

const periods = [
  { label: 'Today', value: 'today' },
  { label: '24h', value: '24h' },
  { label: '7d', value: '7d' },
  { label: '30d', value: '30d' },
]
const period = ref('24h')
const lastUpdated = ref('--')

// Raw data
const throughput = ref([])
const turnaroundTrend = ref([])
const agentLatency = ref([])
const errorRates = ref([])
const urgencyDistribution = ref({})
const confidenceDistribution = ref({})
const reviewRate = ref(null)
const completionFunnel = ref([])
const failureCategories = ref([])

// Summary metrics
const summaryMetrics = computed(() => {
  const totalCases = throughput.value.reduce((sum, b) => sum + (b.count || 0), 0)

  const turnaroundValues = turnaroundTrend.value.map(t => t.avg_ms || t.value || 0).filter(v => v > 0)
  const avgTurnaround = turnaroundValues.length > 0
    ? (turnaroundValues.reduce((s, v) => s + v, 0) / turnaroundValues.length / 1000).toFixed(1) + 's'
    : '--'

  const errorTotal = errorRates.value.reduce((s, a) => s + (a.rate || 0), 0)
  const avgError = errorRates.value.length > 0
    ? (errorTotal / errorRates.value.length).toFixed(1) + '%'
    : '--'

  const rvRate = reviewRate.value != null
    ? (reviewRate.value * 100).toFixed(1) + '%'
    : '--'

  return [
    {
      label: 'Total Cases',
      value: totalCases,
      iconBg: 'bg-blue-500/10',
      icon: '<svg fill="none" stroke="#3b82f6" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08"/></svg>',
    },
    {
      label: 'Avg Turnaround',
      value: avgTurnaround,
      iconBg: 'bg-emerald-500/10',
      icon: '<svg fill="none" stroke="#10b981" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    },
    {
      label: 'Error Rate',
      value: avgError,
      iconBg: 'bg-red-500/10',
      icon: '<svg fill="none" stroke="#ef4444" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"/></svg>',
    },
    {
      label: 'Review Rate',
      value: rvRate,
      iconBg: 'bg-purple-500/10',
      icon: '<svg fill="none" stroke="#a855f7" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    },
  ]
})

// Throughput bar scaling
function throughputBarWidth(count) {
  const max = Math.max(...throughput.value.map(b => b.count), 1)
  return (count / max * 100) + '%'
}

// Latency helpers
function latencyBarWidth(ms) {
  const max = Math.max(...agentLatency.value.map(a => a.avg_ms), 1)
  return (ms / max * 100) + '%'
}

function latencyBarColor(ms) {
  if (ms < 3000) return 'bg-emerald-500'
  if (ms < 8000) return 'bg-amber-500'
  return 'bg-red-500'
}

// Urgency segments
const urgencyTotal = computed(() => {
  return Object.values(urgencyDistribution.value).reduce((s, v) => s + (v || 0), 0)
})

const urgencyColors = {
  emergency: 'bg-red-500',
  urgent: 'bg-amber-500',
  soon: 'bg-yellow-400',
  routine: 'bg-emerald-500',
}

const urgencySegments = computed(() => {
  const total = urgencyTotal.value
  if (total === 0) return []
  return ['emergency', 'urgent', 'soon', 'routine']
    .filter(key => (urgencyDistribution.value[key] || 0) > 0)
    .map(key => ({
      key,
      count: urgencyDistribution.value[key] || 0,
      pct: ((urgencyDistribution.value[key] || 0) / total) * 100,
      color: urgencyColors[key] || 'bg-slate-400',
    }))
})

// Confidence helpers
const confidenceBuckets = computed(() => {
  const raw = confidenceDistribution.value
  if (!raw || typeof raw !== 'object') return []
  const ranges = [
    { label: '0-20', rangeStart: 0 },
    { label: '20-40', rangeStart: 20 },
    { label: '40-60', rangeStart: 40 },
    { label: '60-80', rangeStart: 60 },
    { label: '80-100', rangeStart: 80 },
  ]
  return ranges.map(r => ({
    ...r,
    count: raw[r.label] || raw[r.rangeStart] || 0,
  }))
})

const maxConfidence = computed(() => Math.max(...confidenceBuckets.value.map(b => b.count), 1))

function confidenceBarHeight(count) {
  return Math.max((count / maxConfidence.value) * 100, 2) + '%'
}

function confidenceBarColor(rangeStart) {
  if (rangeStart < 20) return 'bg-red-400'
  if (rangeStart < 40) return 'bg-amber-400'
  if (rangeStart < 60) return 'bg-yellow-400'
  if (rangeStart < 80) return 'bg-blue-400'
  return 'bg-emerald-400'
}

// Funnel helpers
function funnelBarWidth(count) {
  const max = Math.max(...completionFunnel.value.map(s => s.count), 1)
  return (count / max * 100) + '%'
}

function funnelBarColor(index) {
  const colors = ['bg-blue-500', 'bg-blue-400', 'bg-cyan-500', 'bg-teal-500', 'bg-emerald-500', 'bg-green-500', 'bg-lime-500']
  return colors[index % colors.length]
}

// Failure bar scaling
function failureBarWidth(count) {
  const max = Math.max(...failureCategories.value.map(c => c.count), 1)
  return (count / max * 100) + '%'
}

// Data fetching
async function fetchData() {
  try {
    const data = await getAnalytics(period.value)

    throughput.value = (data.throughput || []).map(t => ({
      label: t.bucket || t.label || t.time || '',
      count: t.count || t.cases || 0,
    }))

    turnaroundTrend.value = data.turnaround_trend || []
    agentLatency.value = (data.agent_latency || []).map(a => ({
      name: a.name || a.agent || '',
      avg_ms: a.avg_ms || a.latency_ms || a.avg || 0,
    }))

    errorRates.value = (data.error_rates || []).map(a => ({
      name: a.name || a.agent || '',
      rate: a.rate || a.error_rate || 0,
    }))

    urgencyDistribution.value = data.urgency_distribution || {}
    confidenceDistribution.value = data.confidence_distribution || {}
    reviewRate.value = data.review_rate ?? null

    completionFunnel.value = (data.completion_funnel || []).map(s => ({
      name: s.stage || s.name || '',
      count: s.count || s.cases || 0,
    }))

    failureCategories.value = (data.top_failure_categories || []).map(c => ({
      category: c.category || c.reason || c.name || '',
      count: c.count || 0,
    }))

    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (e) {
    console.error('Failed to fetch analytics:', e)
  }
}

function setPeriod(p) {
  period.value = p
  fetchData()
}

function refresh() { fetchData() }

const { start } = usePolling(fetchData, 30000)
onMounted(() => start())
</script>
