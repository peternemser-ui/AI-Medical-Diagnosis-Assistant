<template>
  <div v-if="!flagEnabled" class="text-center py-20">
    <p :class="isDark ? 'text-slate-400' : 'text-slate-500'">System Dashboard is disabled via feature flags.</p>
  </div>

  <div v-else class="space-y-8">
    <!-- Page header -->
    <div>
      <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">System Insight Dashboard</h1>
      <p class="mt-1 text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Agent pipeline, system health, processing metrics, and feature flag management.</p>
    </div>

    <!-- ===== Section 1: Agent Pipeline Visualization ===== -->
    <section>
      <h2 class="text-lg font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Agent Pipeline</h2>
      <div class="flex flex-wrap items-center gap-2">
        <div
          v-for="(agent, idx) in pipelineAgents"
          :key="agent.name"
          class="flex items-center gap-2"
        >
          <div
            class="relative px-4 py-3 rounded-xl border text-sm font-medium min-w-[120px] text-center"
            :class="agentNodeClass(agent)"
          >
            <div class="font-semibold">{{ agent.name }}</div>
            <div class="text-[10px] mt-0.5 opacity-70">{{ agent.model }}</div>
            <div class="flex items-center justify-center gap-1 mt-1">
              <span
                class="w-1.5 h-1.5 rounded-full"
                :class="statusDotClass(agent.status)"
              ></span>
              <span class="text-[10px] capitalize">{{ agent.status }}</span>
            </div>
            <div v-if="agent.lastTime != null" class="text-[10px] mt-0.5 opacity-60">{{ agent.lastTime }}ms</div>
            <!-- Parallel indicator for Diagnostician+Research -->
            <div
              v-if="agent.parallel"
              class="absolute -top-2 -right-2 text-[9px] px-1.5 py-0.5 rounded-full font-bold"
              :class="isDark ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-100 text-blue-700'"
            >parallel</div>
          </div>
          <!-- Arrow between nodes -->
          <svg v-if="idx < pipelineAgents.length - 1" class="w-5 h-5 flex-shrink-0" :class="isDark ? 'text-slate-600' : 'text-slate-300'" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
          </svg>
        </div>
      </div>
    </section>

    <!-- ===== Section 2: Real-Time System Status ===== -->
    <section>
      <h2 class="text-lg font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">System Status</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Backend health -->
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Backend Health</div>
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full" :class="health.ok ? 'bg-emerald-500' : 'bg-red-500'"></span>
            <span class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ health.ok ? 'Healthy' : 'Unreachable' }}</span>
          </div>
          <div v-if="health.version" class="text-xs mt-1 opacity-60">v{{ health.version }}</div>
        </div>

        <!-- Active model -->
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Active Model</div>
          <div class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ health.model || 'Unknown' }}</div>
        </div>

        <!-- Ollama status -->
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Ollama</div>
          <div class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">
            {{ health.ollama ? health.ollama : 'Not detected' }}
          </div>
        </div>

        <!-- API key status -->
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">API Keys</div>
          <div class="space-y-1">
            <div v-for="k in apiKeyStatuses" :key="k.name" class="flex items-center gap-2 text-sm">
              <span class="w-1.5 h-1.5 rounded-full" :class="k.valid ? 'bg-emerald-500' : 'bg-slate-500'"></span>
              <span :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ k.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== Section 3: Processing Metrics ===== -->
    <section>
      <h2 class="text-lg font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Processing Metrics</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Avg Pipeline Time</div>
          <div class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ metrics.avgTime }}ms</div>
        </div>
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Agent Success Rate</div>
          <div class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ metrics.successRate }}%</div>
        </div>
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Common Failures</div>
          <div class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ metrics.commonFailure || 'None' }}</div>
        </div>
        <div class="rounded-xl border p-4" :class="cardClass">
          <div class="text-xs uppercase tracking-wide mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Model Distribution</div>
          <div class="space-y-1 mt-1">
            <div v-for="m in metrics.modelDist" :key="m.model" class="flex items-center justify-between text-xs">
              <span :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ m.model }}</span>
              <span class="font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ m.count }}</span>
            </div>
            <div v-if="!metrics.modelDist.length" class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No data</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== Section 4: Feature Flags Panel ===== -->
    <section>
      <h2 class="text-lg font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Feature Flags</h2>
      <div class="rounded-xl border overflow-hidden" :class="cardClass">
        <div
          v-for="(val, key) in flags"
          :key="key"
          class="flex items-center justify-between px-5 py-3 border-b last:border-b-0"
          :class="isDark ? 'border-slate-700/50' : 'border-slate-100'"
        >
          <div>
            <span class="font-medium text-sm" :class="isDark ? 'text-white' : 'text-slate-900'">{{ key }}</span>
            <span
              v-if="FLAG_DEFAULTS[key] !== undefined"
              class="ml-2 text-[10px] opacity-50"
            >(default: {{ FLAG_DEFAULTS[key] ? 'on' : 'off' }})</span>
          </div>
          <button
            @click="toggleFlag(key)"
            class="relative w-11 h-6 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            :class="val
              ? 'bg-emerald-500'
              : (isDark ? 'bg-slate-600' : 'bg-slate-300')"
          >
            <span
              class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow transition-transform"
              :class="val ? 'translate-x-5' : 'translate-x-0'"
            ></span>
          </button>
        </div>
      </div>
      <div class="mt-3 flex justify-end">
        <button
          @click="doResetFlags"
          class="text-xs px-3 py-1.5 rounded-lg transition-colors"
          :class="isDark
            ? 'text-slate-400 hover:text-white hover:bg-slate-800'
            : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'"
        >Reset to defaults</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getFlag, getAllFlags, setFlag, resetFlags, FLAG_DEFAULTS } from '@/services/featureFlags.js'

const { isDark } = useTheme()

const flagEnabled = computed(() => getFlag('systemDashboard'))

// ── Cards styling ──
const cardClass = computed(() =>
  isDark.value
    ? 'bg-slate-800/50 border-slate-700/50'
    : 'bg-white border-slate-200 shadow-sm'
)

// ── Agent Pipeline ──
const pipelineAgents = ref([
  { name: 'Triage',        model: 'Claude Sonnet', status: 'idle', lastTime: null, parallel: false },
  { name: 'Diagnostician', model: 'Claude Sonnet', status: 'idle', lastTime: null, parallel: true },
  { name: 'Research',      model: 'Claude Sonnet', status: 'idle', lastTime: null, parallel: true },
  { name: 'Specialist',    model: 'Claude Sonnet', status: 'idle', lastTime: null, parallel: false },
  { name: 'Treatment',     model: 'Claude Sonnet', status: 'idle', lastTime: null, parallel: false },
  { name: 'Safety',        model: 'Claude Sonnet', status: 'idle', lastTime: null, parallel: false },
  { name: 'Empathy',       model: 'Claude Sonnet', status: 'idle', lastTime: null, parallel: false },
])

function agentNodeClass(agent) {
  if (isDark.value) {
    if (agent.status === 'complete') return 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
    if (agent.status === 'running') return 'bg-blue-500/10 border-blue-500/30 text-blue-400'
    if (agent.status === 'error') return 'bg-red-500/10 border-red-500/30 text-red-400'
    return 'bg-slate-800/50 border-slate-700/50 text-slate-400'
  }
  if (agent.status === 'complete') return 'bg-emerald-50 border-emerald-200 text-emerald-700'
  if (agent.status === 'running') return 'bg-blue-50 border-blue-200 text-blue-700'
  if (agent.status === 'error') return 'bg-red-50 border-red-200 text-red-700'
  return 'bg-white border-slate-200 text-slate-500'
}

function statusDotClass(status) {
  if (status === 'complete') return 'bg-emerald-500'
  if (status === 'running') return 'bg-blue-500 animate-pulse'
  if (status === 'error') return 'bg-red-500'
  return isDark.value ? 'bg-slate-600' : 'bg-slate-300'
}

// ── System Health ──
const health = reactive({ ok: false, version: '', model: '', ollama: '' })

const apiKeyStatuses = computed(() => [
  { name: 'Anthropic', valid: !!localStorage.getItem('anthropic_api_key') },
  { name: 'OpenAI', valid: !!localStorage.getItem('openai_api_key') },
  { name: 'Google', valid: !!localStorage.getItem('google_api_key') },
])

async function fetchHealth() {
  try {
    const res = await fetch('/health')
    if (!res.ok) throw new Error('unhealthy')
    const data = await res.json()
    health.ok = data.status === 'healthy'
    health.version = data.architecture || ''
    health.model = data.api_key_configured ? 'Configured' : 'No API key'
    health.ollama = data.ollama_available ? `Available (${(data.ollama_models || []).join(', ')})` : 'Not available'
  } catch {
    health.ok = false
  }
}

// ── Processing Metrics ──
const metrics = reactive({
  avgTime: '—',
  successRate: '—',
  commonFailure: '',
  modelDist: [],
})

async function fetchMetrics() {
  try {
    const res = await fetch('/api/admin/audit/latest')
    if (!res.ok) return
    const data = await res.json()

    // The audit endpoint returns { stats, recommendations, recent_cases }
    const stats = data.stats || {}
    const cases = data.recent_cases || []

    if (stats.average_score !== undefined) {
      metrics.successRate = Math.round(stats.average_score)
    }

    if (cases.length) {
      // Compute average pipeline time from case audits
      const times = cases.map(c => c.total_time).filter(Boolean)
      if (times.length) {
        metrics.avgTime = Math.round(times.reduce((a, b) => a + b, 0) / times.length * 1000)
      }
    }

    // Common failure from recommendations
    const recs = data.recommendations || []
    if (recs.length) {
      metrics.commonFailure = recs[0].title || ''
    }

    // Skip the old parsing — the data structure is different
    return
  } catch {
    return
  }
}

// Legacy parsing placeholder — kept for compatibility
function _legacyParsing() {
    const items = []
    if (!items.length) return
    const failures = items.filter(i => i.error || i.status === 'error')
    if (failures.length) {
      const agents = failures.map(f => f.failed_agent || f.agent || 'unknown')
      const counts = {}
      agents.forEach(a => { counts[a] = (counts[a] || 0) + 1 })
      metrics.commonFailure = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] || 'None'
    }

    // Model distribution
    const modelCounts = {}
    items.forEach(i => {
      const m = i.model || i.provider || 'unknown'
      modelCounts[m] = (modelCounts[m] || 0) + 1
    })
    metrics.modelDist = Object.entries(modelCounts).map(([model, count]) => ({ model, count }))

    // Update pipeline agent timings from latest entry
    const latest = items[0]
    if (latest?.agent_timings) {
      const nameMap = {
        triage: 'Triage', diagnostician: 'Diagnostician', research: 'Research',
        specialist: 'Specialist', treatment: 'Treatment', safety: 'Safety', empathy: 'Empathy'
      }
      for (const [key, ms] of Object.entries(latest.agent_timings)) {
        const agent = pipelineAgents.value.find(a => a.name === nameMap[key])
        if (agent) {
          agent.lastTime = typeof ms === 'number' ? Math.round(ms) : ms
          agent.status = 'complete'
        }
      }
    }
  } catch {
    // audit endpoint may not exist yet — that's fine
  }
}

// ── Feature Flags ──
const flags = ref(getAllFlags())

function toggleFlag(key) {
  const newVal = !flags.value[key]
  setFlag(key, newVal)
  flags.value = getAllFlags()
}

function doResetFlags() {
  resetFlags()
  flags.value = getAllFlags()
}

// ── Init ──
onMounted(() => {
  fetchHealth()
  fetchMetrics()
})
</script>
