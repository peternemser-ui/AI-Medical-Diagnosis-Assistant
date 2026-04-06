<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Agents</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Monitor and control all AI agents</p>
      </div>
      <div class="flex items-center gap-2">
        <button @click="viewMode = 'grid'" class="p-2 rounded-lg transition-colors" :class="viewMode === 'grid' ? (isDark ? 'bg-slate-800 text-white' : 'bg-slate-200 text-slate-900') : (isDark ? 'text-slate-500' : 'text-slate-400')">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z"/></svg>
        </button>
        <button @click="viewMode = 'table'" class="p-2 rounded-lg transition-colors" :class="viewMode === 'table' ? (isDark ? 'bg-slate-800 text-white' : 'bg-slate-200 text-slate-900') : (isDark ? 'text-slate-500' : 'text-slate-400')">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z"/></svg>
        </button>
      </div>
    </div>

    <!-- Error toast -->
    <Transition name="toast">
      <div v-if="controlError" class="flex items-center gap-3 px-4 py-3 rounded-xl border"
        :class="isDark ? 'bg-red-500/10 border-red-500/20 text-red-400' : 'bg-red-50 border-red-200 text-red-600'">
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"/></svg>
        <span class="text-sm flex-1">{{ controlError }}</span>
        <button @click="controlError = ''" class="p-1 rounded-lg hover:bg-red-500/10">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </Transition>

    <!-- Grid view -->
    <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <div v-for="agent in agents" :key="agent.name"
        class="rounded-2xl border p-5 transition-all cursor-pointer hover:shadow-lg"
        :class="isDark ? 'bg-slate-900/80 border-slate-800 hover:border-slate-600' : 'bg-white border-slate-200 hover:border-slate-300 shadow-sm'"
        @click="openDetail(agent.name)">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-bold capitalize" :class="isDark ? 'text-white' : 'text-slate-900'">{{ agent.name }}</h3>
          <span class="flex items-center gap-1.5 text-xs font-medium px-2 py-0.5 rounded-full"
            :class="statusClass(agent.status)">
            <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(agent.status)"></span>
            {{ agent.status }}
          </span>
        </div>

        <div class="grid grid-cols-2 gap-3 mb-4">
          <div>
            <div class="text-[10px] uppercase tracking-wider" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Latency</div>
            <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ agent.latency_p50 }}s</div>
          </div>
          <div>
            <div class="text-[10px] uppercase tracking-wider" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Cases (24h)</div>
            <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ agent.cases_24h }}</div>
          </div>
          <div>
            <div class="text-[10px] uppercase tracking-wider" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Errors</div>
            <div class="text-lg font-semibold tabular-nums" :class="agent.errors_24h > 0 ? 'text-red-400' : (isDark ? 'text-emerald-400' : 'text-emerald-600')">{{ agent.errors_24h }}</div>
          </div>
          <div>
            <div class="text-[10px] uppercase tracking-wider" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Model</div>
            <div class="text-xs font-mono truncate" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ agent.model || '---' }}</div>
          </div>
        </div>

        <div class="flex items-center gap-2 pt-3 border-t" :class="isDark ? 'border-slate-700/40' : 'border-slate-100'"
          @click.stop>
          <button class="flex-1 text-xs font-medium py-1.5 rounded-lg transition-colors"
            :class="agent.status === 'paused'
              ? (isDark ? 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100')
              : (isDark ? 'bg-amber-500/10 text-amber-400 hover:bg-amber-500/20' : 'bg-amber-50 text-amber-600 hover:bg-amber-100')"
            :disabled="controlLoading"
            @click="handleControl(agent.name, agent.status === 'paused' ? 'resume' : 'pause')">
            {{ agent.status === 'paused' ? 'Resume' : 'Pause' }}
          </button>
          <button class="text-xs font-medium py-1.5 px-3 rounded-lg transition-colors"
            :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
            :disabled="controlLoading"
            @click="promptRestart(agent.name)">
            Restart
          </button>
        </div>
      </div>
    </div>

    <!-- Table view -->
    <div v-else class="rounded-2xl border overflow-hidden" :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <table class="w-full text-sm">
        <thead>
          <tr :class="isDark ? 'border-b border-slate-800' : 'border-b border-slate-100'">
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Agent</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Status</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Latency</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Cases</th>
            <th class="text-left px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Errors</th>
            <th class="text-right px-5 py-3 text-xs font-semibold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="agent in agents" :key="agent.name"
            class="border-b transition-colors cursor-pointer"
            :class="isDark ? 'border-slate-800/50 hover:bg-slate-800/40' : 'border-slate-50 hover:bg-slate-50'"
            @click="openDetail(agent.name)">
            <td class="px-5 py-3 font-semibold capitalize" :class="isDark ? 'text-white' : 'text-slate-900'">{{ agent.name }}</td>
            <td class="px-5 py-3">
              <span class="flex items-center gap-1.5 text-xs font-medium"><span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(agent.status)"></span>{{ agent.status }}</span>
            </td>
            <td class="px-5 py-3 tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ agent.latency_p50 }}s</td>
            <td class="px-5 py-3 tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ agent.cases_24h }}</td>
            <td class="px-5 py-3 tabular-nums" :class="agent.errors_24h > 0 ? 'text-red-400' : (isDark ? 'text-slate-500' : 'text-slate-400')">{{ agent.errors_24h }}</td>
            <td class="px-5 py-3 text-right" @click.stop>
              <div class="flex items-center justify-end gap-1">
                <button class="text-xs px-2 py-1 rounded-lg"
                  :class="isDark ? 'text-slate-400 hover:bg-slate-800' : 'text-slate-500 hover:bg-slate-100'"
                  @click="openDetail(agent.name)">
                  Details
                </button>
                <button class="text-xs px-2 py-1 rounded-lg"
                  :class="agent.status === 'paused'
                    ? (isDark ? 'text-emerald-400 hover:bg-emerald-500/10' : 'text-emerald-600 hover:bg-emerald-50')
                    : (isDark ? 'text-amber-400 hover:bg-amber-500/10' : 'text-amber-600 hover:bg-amber-50')"
                  :disabled="controlLoading"
                  @click="handleControl(agent.name, agent.status === 'paused' ? 'resume' : 'pause')">
                  {{ agent.status === 'paused' ? 'Resume' : 'Pause' }}
                </button>
                <button class="text-xs px-2 py-1 rounded-lg"
                  :class="isDark ? 'text-slate-400 hover:bg-slate-800' : 'text-slate-500 hover:bg-slate-100'"
                  :disabled="controlLoading"
                  @click="promptRestart(agent.name)">
                  Restart
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Agent detail drawer -->
    <ASheet :open="drawerOpen" :title="detailData?.name ? detailData.name.charAt(0).toUpperCase() + detailData.name.slice(1) + ' Agent' : 'Agent Detail'" width="lg" @close="drawerOpen = false">
      <div v-if="detailLoading" class="flex items-center justify-center py-20">
        <div class="w-6 h-6 border-2 border-current border-t-transparent rounded-full animate-spin" :class="isDark ? 'text-slate-500' : 'text-slate-400'"></div>
      </div>

      <div v-else-if="detailData" class="space-y-6">
        <!-- Status & description -->
        <div>
          <div class="flex items-center gap-3 mb-2">
            <span class="flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full"
              :class="statusClass(detailData.status)">
              <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(detailData.status)"></span>
              {{ detailData.status }}
            </span>
            <span v-if="detailData.model" class="text-xs font-mono px-2 py-1 rounded-lg"
              :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'">
              {{ detailData.model }}
            </span>
          </div>
          <p v-if="detailData.description" class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ detailData.description }}</p>
        </div>

        <!-- Performance metrics -->
        <div>
          <h4 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Performance Metrics</h4>
          <div class="grid grid-cols-3 gap-3">
            <div class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Avg Latency</div>
              <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ formatMs(detailData.avg_latency_ms) }}</div>
            </div>
            <div class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">P95 Latency</div>
              <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ formatMs(detailData.p95_latency_ms) }}</div>
            </div>
            <div class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Cases Processed</div>
              <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ detailData.cases_processed ?? 0 }}</div>
            </div>
            <div class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Error Count</div>
              <div class="text-lg font-semibold tabular-nums" :class="(detailData.error_count || 0) > 0 ? 'text-red-400' : (isDark ? 'text-emerald-400' : 'text-emerald-600')">{{ detailData.error_count ?? 0 }}</div>
            </div>
            <div class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Success Rate</div>
              <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ detailData.success_rate != null ? (detailData.success_rate * 100).toFixed(1) + '%' : '---' }}</div>
            </div>
            <div class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Uptime</div>
              <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ detailData.uptime || '---' }}</div>
            </div>
          </div>
        </div>

        <!-- Recent executions -->
        <div v-if="detailData.recent_executions && detailData.recent_executions.length">
          <h4 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Recent Executions</h4>
          <div class="rounded-xl border overflow-hidden" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <table class="w-full text-xs">
              <thead>
                <tr :class="isDark ? 'bg-slate-800/50 border-b border-slate-700/50' : 'bg-slate-50 border-b border-slate-200'">
                  <th class="text-left px-3 py-2 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Case ID</th>
                  <th class="text-left px-3 py-2 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Timestamp</th>
                  <th class="text-left px-3 py-2 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Latency</th>
                  <th class="text-left px-3 py-2 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Result</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="exec in detailData.recent_executions.slice(0, 10)" :key="exec.case_id || exec.timestamp"
                  class="border-b" :class="isDark ? 'border-slate-800/50' : 'border-slate-100'">
                  <td class="px-3 py-2 font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ exec.case_id || '---' }}</td>
                  <td class="px-3 py-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ formatTimestamp(exec.timestamp) }}</td>
                  <td class="px-3 py-2 tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ formatMs(exec.latency_ms) }}</td>
                  <td class="px-3 py-2">
                    <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium"
                      :class="exec.success !== false
                        ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600')
                        : (isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600')">
                      {{ exec.success !== false ? 'success' : 'error' }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Failure clusters -->
        <div v-if="detailData.failure_clusters && detailData.failure_clusters.length">
          <h4 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Failure Clusters</h4>
          <div class="space-y-2">
            <div v-for="cluster in detailData.failure_clusters" :key="cluster.category"
              class="flex items-center justify-between rounded-xl p-3 border"
              :class="isDark ? 'bg-red-500/5 border-red-500/10' : 'bg-red-50/50 border-red-100'">
              <div>
                <div class="text-sm font-medium" :class="isDark ? 'text-red-300' : 'text-red-700'">{{ cluster.category }}</div>
                <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Last seen: {{ formatTimestamp(cluster.last_seen) }}</div>
              </div>
              <span class="text-sm font-semibold tabular-nums px-2.5 py-1 rounded-lg"
                :class="isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-100 text-red-600'">
                {{ cluster.count }}
              </span>
            </div>
          </div>
        </div>

        <!-- Learning insights -->
        <div v-if="detailData.learning_insights && detailData.learning_insights.length">
          <h4 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Learning Insights</h4>
          <div class="space-y-2">
            <div v-for="(insight, idx) in detailData.learning_insights" :key="idx"
              class="rounded-xl p-3 border"
              :class="isDark ? 'bg-indigo-500/5 border-indigo-500/10' : 'bg-indigo-50/50 border-indigo-100'">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-semibold uppercase tracking-wider"
                  :class="isDark ? 'text-indigo-400' : 'text-indigo-600'">{{ insight.category }}</span>
                <span v-if="insight.frequency" class="text-[10px] tabular-nums px-2 py-0.5 rounded-full"
                  :class="isDark ? 'bg-indigo-500/10 text-indigo-400' : 'bg-indigo-100 text-indigo-600'">
                  {{ insight.frequency }}x
                </span>
              </div>
              <p class="text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ insight.description }}</p>
              <p v-if="insight.suggestion" class="text-xs mt-1.5 italic" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                Suggestion: {{ insight.suggestion }}
              </p>
            </div>
          </div>
        </div>

        <!-- Dependencies -->
        <div v-if="detailData.dependencies || detailData.downstream">
          <h4 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Dependencies</h4>
          <div class="grid grid-cols-2 gap-3">
            <div v-if="detailData.dependencies && detailData.dependencies.length"
              class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Upstream</div>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="dep in detailData.dependencies" :key="dep"
                  class="text-xs font-medium px-2 py-0.5 rounded-lg capitalize"
                  :class="isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-600'">
                  {{ dep }}
                </span>
              </div>
            </div>
            <div v-if="detailData.downstream && detailData.downstream.length"
              class="rounded-xl p-3 border" :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
              <div class="text-[10px] uppercase tracking-wider mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Downstream</div>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="dep in detailData.downstream" :key="dep"
                  class="text-xs font-medium px-2 py-0.5 rounded-lg capitalize"
                  :class="isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-600'">
                  {{ dep }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Agent config -->
        <div v-if="detailData.config && Object.keys(detailData.config).length">
          <h4 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Configuration</h4>
          <div class="rounded-xl border overflow-hidden" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <div v-for="(val, key) in detailData.config" :key="key"
              class="flex items-center justify-between px-3 py-2 text-xs border-b last:border-b-0"
              :class="isDark ? 'border-slate-800/50' : 'border-slate-100'">
              <span class="font-mono" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ key }}</span>
              <span class="font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ val }}</span>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <div v-if="detailData" class="flex items-center gap-2">
          <button class="flex-1 text-sm font-medium py-2 rounded-lg transition-colors"
            :class="detailData.status === 'paused'
              ? (isDark ? 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100')
              : (isDark ? 'bg-amber-500/10 text-amber-400 hover:bg-amber-500/20' : 'bg-amber-50 text-amber-600 hover:bg-amber-100')"
            :disabled="controlLoading"
            @click="handleControl(detailData.name, detailData.status === 'paused' ? 'resume' : 'pause')">
            {{ detailData.status === 'paused' ? 'Resume' : 'Pause' }}
          </button>
          <button class="text-sm font-medium py-2 px-4 rounded-lg transition-colors"
            :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
            :disabled="controlLoading"
            @click="promptRestart(detailData.name)">
            Restart
          </button>
        </div>
      </template>
    </ASheet>

    <!-- Confirm restart dialog -->
    <AConfirmDialog
      :open="confirmRestart"
      title="Restart Agent"
      :message="`Are you sure you want to restart ${selectedAgent}? This will temporarily interrupt any in-progress cases handled by this agent.`"
      confirm-label="Restart"
      variant="warning"
      @confirm="doRestart"
      @cancel="confirmRestart = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getAgents, controlAgent, getAgentDetail } from '@/services/adminApi.js'
import ASheet from '@/components/admin/ASheet.vue'
import AConfirmDialog from '@/components/admin/AConfirmDialog.vue'

const { isDark } = useTheme()
const viewMode = ref('grid')
const agents = ref([])

// Control state
const controlLoading = ref(false)
const controlError = ref('')
let errorTimeout = null

// Drawer state
const drawerOpen = ref(false)
const detailLoading = ref(false)
const detailData = ref(null)

// Restart confirmation state
const confirmRestart = ref(false)
const selectedAgent = ref('')

async function fetchAgents() {
  try {
    const data = await getAgents()
    agents.value = (data || []).map(a => ({
      name: a.name || a.display_name,
      status: a.status,
      latency_p50: ((a.avg_latency_ms || 0) / 1000).toFixed(1),
      cases_24h: a.cases_processed || 0,
      errors_24h: a.error_count || 0,
      model: a.model || 'claude-sonnet',
    }))
  } catch (e) {
    console.error('Failed to fetch agents:', e)
  }
}

const { start } = usePolling(fetchAgents, 10000)
onMounted(() => start())

// --- Control actions ---

function showError(msg) {
  controlError.value = msg
  if (errorTimeout) clearTimeout(errorTimeout)
  errorTimeout = setTimeout(() => { controlError.value = '' }, 5000)
}

async function handleControl(agentName, action) {
  controlLoading.value = true
  try {
    await controlAgent(agentName, action)
    await fetchAgents()
    // If drawer is open for this agent, refresh detail too
    if (drawerOpen.value && detailData.value?.name === agentName) {
      await loadDetail(agentName)
    }
  } catch (e) {
    showError(`Failed to ${action} ${agentName}: ${e.message}`)
  } finally {
    controlLoading.value = false
  }
}

function promptRestart(agentName) {
  selectedAgent.value = agentName
  confirmRestart.value = true
}

async function doRestart() {
  confirmRestart.value = false
  await handleControl(selectedAgent.value, 'restart')
}

// --- Detail drawer ---

async function openDetail(agentName) {
  drawerOpen.value = true
  await loadDetail(agentName)
}

async function loadDetail(agentName) {
  detailLoading.value = true
  detailData.value = null
  try {
    const data = await getAgentDetail(agentName)
    detailData.value = data
  } catch (e) {
    showError(`Failed to load agent detail: ${e.message}`)
    drawerOpen.value = false
  } finally {
    detailLoading.value = false
  }
}

// --- Formatting helpers ---

function formatMs(ms) {
  if (ms == null) return '---'
  if (ms < 1000) return ms.toFixed(0) + 'ms'
  return (ms / 1000).toFixed(1) + 's'
}

function formatTimestamp(ts) {
  if (!ts) return '---'
  try {
    const d = new Date(ts)
    return d.toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
  } catch (e) {
    return ts
  }
}

// --- Status classes (extended) ---

function statusClass(s) {
  if (s === 'healthy') return isDark.value ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'
  if (s === 'running') return isDark.value ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-600'
  if (s === 'degraded') return isDark.value ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-50 text-amber-600'
  if (s === 'error') return isDark.value ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600'
  if (s === 'paused') return isDark.value ? 'bg-purple-500/10 text-purple-400' : 'bg-purple-50 text-purple-600'
  if (s === 'retrying') return isDark.value ? 'bg-yellow-500/10 text-yellow-400' : 'bg-yellow-50 text-yellow-600'
  if (s === 'idle') return isDark.value ? 'bg-slate-500/10 text-slate-400' : 'bg-slate-100 text-slate-500'
  return isDark.value ? 'bg-slate-500/10 text-slate-400' : 'bg-slate-100 text-slate-500'
}

function statusDotClass(s) {
  if (s === 'healthy') return 'bg-emerald-500'
  if (s === 'running') return 'bg-blue-500'
  if (s === 'degraded') return 'bg-amber-500'
  if (s === 'error') return 'bg-red-500'
  if (s === 'paused') return 'bg-purple-500'
  if (s === 'retrying') return 'bg-yellow-500 animate-pulse'
  if (s === 'idle') return isDark.value ? 'bg-slate-500' : 'bg-slate-400'
  return 'bg-slate-500'
}
</script>

<style scoped>
.toast-enter-active {
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-leave-active {
  transition: all 0.2s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
