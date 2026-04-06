<template>
  <div class="space-y-6">
    <!-- Page header + Hero Button -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Improvement Dashboard</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Run quality audits and track system improvement opportunities</p>
      </div>
      <button
        @click="runAudit"
        :disabled="loading"
        class="px-6 py-3 rounded-xl text-sm font-bold transition-all flex items-center gap-2 shadow-lg"
        :class="loading
          ? (isDark ? 'bg-slate-700 text-slate-400 cursor-not-allowed' : 'bg-slate-200 text-slate-400 cursor-not-allowed')
          : 'bg-gradient-to-r from-violet-600 to-indigo-600 text-white hover:from-violet-500 hover:to-indigo-500 hover:shadow-xl hover:scale-[1.02]'"
      >
        <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
        <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
        {{ loading ? 'Running Audit...' : 'Run Quality Audit' }}
      </button>
    </div>

    <!-- Error banner -->
    <div v-if="error" class="rounded-xl border px-4 py-3 text-sm flex items-center gap-2"
      :class="isDark ? 'bg-red-500/10 border-red-500/20 text-red-400' : 'bg-red-50 border-red-200 text-red-600'">
      <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
      {{ error }}
    </div>

    <!-- Empty state -->
    <div v-if="!audit && !loading" class="rounded-2xl border p-16 text-center"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-violet-500/20 to-indigo-500/20 flex items-center justify-center mb-4">
        <svg class="w-8 h-8" :class="isDark ? 'text-violet-400' : 'text-violet-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
      </div>
      <h3 class="text-lg font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">No Audit Data</h3>
      <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Click "Run Quality Audit" to analyze recent cases and generate improvement recommendations.</p>
    </div>

    <!-- Audit Results -->
    <template v-if="audit">
      <!-- Quality Score Summary -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <!-- Overall Score -->
        <div class="rounded-2xl border p-6 col-span-1 md:col-span-2 flex items-center gap-6"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
          <div class="relative w-24 h-24 flex-shrink-0">
            <svg class="w-24 h-24 -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="42" fill="none" stroke-width="8" :stroke="isDark ? '#1e293b' : '#e2e8f0'" />
              <circle cx="50" cy="50" r="42" fill="none" stroke-width="8" stroke-linecap="round"
                :stroke="scoreColor(audit.overall_score)"
                :stroke-dasharray="`${audit.overall_score * 2.64} 264`" />
            </svg>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-2xl font-black tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ audit.overall_score }}</span>
            </div>
          </div>
          <div>
            <div class="text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Overall Quality Score</div>
            <div class="flex items-center gap-2 mt-1">
              <span class="text-3xl font-black tabular-nums" :style="{ color: scoreColor(audit.overall_score) }">{{ audit.overall_score }}/100</span>
              <span class="px-2.5 py-1 rounded-lg text-xs font-bold" :style="{ backgroundColor: scoreColor(audit.grade_value || audit.overall_score) + '20', color: scoreColor(audit.grade_value || audit.overall_score) }">
                Grade {{ audit.grade }}
              </span>
            </div>
            <div class="text-xs mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Based on {{ audit.cases_audited }} audited cases</div>
          </div>
        </div>

        <!-- Cases Audited -->
        <div class="rounded-2xl border p-6"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
          <div class="text-xs font-medium uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Cases Audited</div>
          <div class="text-3xl font-black mt-2 tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ audit.cases_audited }}</div>
          <div class="text-xs mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Recent consultations</div>
        </div>

        <!-- Grade Distribution -->
        <div class="rounded-2xl border p-6"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
          <div class="text-xs font-medium uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Grade Distribution</div>
          <div class="flex items-end gap-1.5 h-16">
            <div v-for="g in gradeLabels" :key="g" class="flex-1 flex flex-col items-center gap-1">
              <div class="w-full rounded-t transition-all" :style="{ height: gradeBarHeight(g), backgroundColor: gradeColor(g) }"></div>
              <span class="text-[10px] font-bold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ g }}</span>
            </div>
          </div>
          <div class="flex justify-between mt-1">
            <span v-for="g in gradeLabels" :key="g" class="flex-1 text-center text-[10px] tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ gradeCount(g) }}</span>
          </div>
        </div>
      </div>

      <!-- Recommendations Panel -->
      <div v-if="audit.recommendations && audit.recommendations.length">
        <h2 class="text-lg font-bold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Recommendations</h2>
        <div class="space-y-3">
          <div v-for="(rec, i) in audit.recommendations" :key="i"
            class="rounded-2xl border p-5 space-y-3"
            :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
            <div class="flex items-center gap-2 flex-wrap">
              <!-- Priority -->
              <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full"
                :class="priorityClass(rec.priority)">{{ rec.priority }}</span>
              <!-- Category -->
              <span class="text-[10px] font-medium px-2 py-0.5 rounded-full"
                :class="isDark ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-600'">{{ rec.category }}</span>
            </div>
            <div class="font-semibold text-sm" :class="isDark ? 'text-white' : 'text-slate-900'">{{ rec.title }}</div>
            <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ rec.description }}</p>
            <!-- Suggested Action -->
            <div v-if="rec.suggested_action" class="rounded-xl px-4 py-3 text-sm"
              :class="isDark ? 'bg-indigo-500/10 border border-indigo-500/20 text-indigo-300' : 'bg-indigo-50 border border-indigo-100 text-indigo-700'">
              <span class="font-semibold">Suggested Action:</span> {{ rec.suggested_action }}
            </div>
            <!-- Expected Impact -->
            <div v-if="rec.expected_impact" class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              Expected Impact: <span class="font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ rec.expected_impact }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Issue Patterns -->
      <div v-if="audit.issue_patterns && audit.issue_patterns.length">
        <h2 class="text-lg font-bold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Issue Patterns</h2>
        <div class="rounded-2xl border overflow-hidden" :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
          <table class="w-full text-sm">
            <thead>
              <tr :class="isDark ? 'border-b border-slate-800' : 'border-b border-slate-100'">
                <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Pattern</th>
                <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Count</th>
                <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Most Affected Agent</th>
                <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Trend</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(pattern, i) in audit.issue_patterns" :key="i"
                class="border-b transition-colors"
                :class="isDark ? 'border-slate-800/50 hover:bg-slate-800/40' : 'border-slate-50 hover:bg-slate-50'">
                <td class="px-5 py-3 font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ pattern.name }}</td>
                <td class="px-5 py-3 tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ pattern.count }}</td>
                <td class="px-5 py-3">
                  <span class="text-xs font-mono px-2 py-0.5 rounded-md" :class="isDark ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-600'">{{ pattern.affected_agent }}</span>
                </td>
                <td class="px-5 py-3">
                  <span class="text-xs font-medium" :class="trendClass(pattern.trend)">
                    {{ trendIcon(pattern.trend) }} {{ pattern.trend || 'stable' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Agent Health Scorecard -->
      <div v-if="audit.agent_health && audit.agent_health.length">
        <h2 class="text-lg font-bold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Agent Health Scorecard</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          <div v-for="agent in audit.agent_health" :key="agent.name"
            class="rounded-2xl border p-4 flex items-center gap-3"
            :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
            <div class="w-3 h-3 rounded-full flex-shrink-0" :class="agentStatusClass(agent.issues)"></div>
            <div class="min-w-0">
              <div class="text-sm font-semibold truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ agent.name }}</div>
              <div class="text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ agent.issues }} issue{{ agent.issues !== 1 ? 's' : '' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Case Audits -->
      <div v-if="audit.recent_audits && audit.recent_audits.length">
        <h2 class="text-lg font-bold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Recent Case Audits</h2>
        <div class="space-y-2">
          <div v-for="(c, i) in audit.recent_audits" :key="i"
            class="rounded-2xl border overflow-hidden"
            :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
            <!-- Header (clickable) -->
            <button @click="toggleCase(i)" class="w-full flex items-center justify-between px-5 py-3.5 text-left transition-colors"
              :class="isDark ? 'hover:bg-slate-800/40' : 'hover:bg-slate-50'">
              <div class="flex items-center gap-3 min-w-0">
                <span class="text-sm font-semibold truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ c.diagnosis || 'Unknown' }}</span>
                <span class="text-xs font-bold tabular-nums px-2 py-0.5 rounded-lg" :style="{ backgroundColor: scoreColor(c.score) + '20', color: scoreColor(c.score) }">
                  {{ c.score }}/100
                </span>
                <span class="text-[10px] font-bold px-1.5 py-0.5 rounded" :style="{ backgroundColor: scoreColor(gradeToScore(c.grade)) + '15', color: scoreColor(gradeToScore(c.grade)) }">
                  {{ c.grade }}
                </span>
              </div>
              <div class="flex items-center gap-3 flex-shrink-0">
                <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ formatTime(c.timestamp) }}</span>
                <svg class="w-4 h-4 transition-transform" :class="[expandedCases.has(i) ? 'rotate-180' : '', isDark ? 'text-slate-500' : 'text-slate-400']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
              </div>
            </button>
            <!-- Expanded content -->
            <div v-if="expandedCases.has(i)" class="px-5 pb-4 border-t" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
              <div v-if="c.issues && c.issues.length" class="mt-3 space-y-1.5">
                <div v-for="(issue, j) in c.issues" :key="j" class="flex items-start gap-2 text-sm">
                  <svg class="w-4 h-4 mt-0.5 flex-shrink-0 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
                  <span :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ issue }}</span>
                </div>
              </div>
              <div v-else class="mt-3 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No issues detected.</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { runQualityAudit, getLatestAudit } from '@/services/adminApi.js'

const { isDark } = useTheme()

const loading = ref(false)
const error = ref(null)
const audit = ref(null)
const expandedCases = reactive(new Set())
const gradeLabels = ['A', 'B', 'C', 'D', 'F']

onMounted(async () => {
  try {
    const data = await getLatestAudit()
    if (data && data.overall_score != null) audit.value = data
  } catch {
    // No previous audit — that's fine
  }
})

async function runAudit() {
  loading.value = true
  error.value = null
  try {
    const data = await runQualityAudit()
    audit.value = data
  } catch (e) {
    error.value = e.message || 'Failed to run audit'
  } finally {
    loading.value = false
  }
}

function toggleCase(index) {
  if (expandedCases.has(index)) expandedCases.delete(index)
  else expandedCases.add(index)
}

function scoreColor(score) {
  if (score >= 80) return '#10b981'
  if (score >= 60) return '#f59e0b'
  return '#ef4444'
}

function gradeColor(grade) {
  const map = { A: '#10b981', B: '#3b82f6', C: '#f59e0b', D: '#f97316', F: '#ef4444' }
  return map[grade] || '#64748b'
}

function gradeCount(grade) {
  return audit.value?.grade_distribution?.[grade] ?? 0
}

function gradeBarHeight(grade) {
  const count = gradeCount(grade)
  const max = Math.max(1, ...gradeLabels.map(g => gradeCount(g)))
  return `${Math.max(4, (count / max) * 56)}px`
}

function gradeToScore(grade) {
  const map = { A: 90, B: 75, C: 60, D: 45, F: 25 }
  return map[grade] || 50
}

function priorityClass(priority) {
  const p = (priority || '').toLowerCase()
  if (p === 'high') return 'bg-red-500/15 text-red-500'
  if (p === 'medium') return 'bg-amber-500/15 text-amber-500'
  return 'bg-blue-500/15 text-blue-500'
}

function trendClass(trend) {
  const t = (trend || '').toLowerCase()
  if (t === 'up') return 'text-red-500'
  if (t === 'down') return 'text-emerald-500'
  return isDark.value ? 'text-slate-400' : 'text-slate-500'
}

function trendIcon(trend) {
  const t = (trend || '').toLowerCase()
  if (t === 'up') return '\u2191'
  if (t === 'down') return '\u2193'
  return '\u2194'
}

function agentStatusClass(issues) {
  if (issues === 0) return 'bg-emerald-500'
  if (issues <= 2) return 'bg-amber-500'
  return 'bg-red-500'
}

function formatTime(ts) {
  if (!ts) return '--'
  try {
    return new Date(ts).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch { return ts }
}
</script>
