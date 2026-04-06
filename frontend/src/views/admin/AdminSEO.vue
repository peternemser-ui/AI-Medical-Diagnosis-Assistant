<template>
  <div class="space-y-6">
    <!-- Page header -->
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">SEO & Marketing</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">SEO health, content ideas, and marketing insights</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          Last updated: {{ lastUpdated }}
        </span>
        <button @click="refresh" class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
          :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          Refresh
        </button>
      </div>
    </div>

    <!-- SEO Score + Quick Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- SEO Score card -->
      <div class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center" :class="scoreIconBg">
            <svg class="w-4 h-4" :class="scoreIconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <span class="text-lg font-bold" :class="gradeColor">{{ audit?.grade || '--' }}</span>
        </div>
        <div class="text-2xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ audit?.overall_score || 0 }}/100</div>
        <div class="text-xs mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">SEO Health Score</div>
      </div>

      <!-- Issues -->
      <div class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center bg-red-500/10">
            <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/>
            </svg>
          </div>
        </div>
        <div class="text-2xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ audit?.total_issues || 0 }}</div>
        <div class="text-xs mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Total Issues</div>
      </div>

      <!-- Pages indexed -->
      <div class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center bg-blue-500/10">
            <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/>
            </svg>
          </div>
        </div>
        <div class="text-2xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ audit?.metrics?.pages_indexed || 0 }}</div>
        <div class="text-xs mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Pages Indexed</div>
      </div>

      <!-- Load time -->
      <div class="rounded-2xl border p-5 transition-colors"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-center justify-between mb-3">
          <div class="w-9 h-9 rounded-xl flex items-center justify-center bg-amber-500/10">
            <svg class="w-4 h-4 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
        <div class="text-2xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ (audit?.metrics?.average_load_time_ms || 0) / 1000 }}s</div>
        <div class="text-xs mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Avg Load Time</div>
      </div>
    </div>

    <!-- Middle row: Page audit + Recommendations -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Page Scores -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Page Audit Scores</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">SEO score per page with issue indicators</p>
        </div>
        <div class="p-4 space-y-3">
          <div v-for="page in (audit?.pages_audited || [])" :key="page.page"
            class="flex items-center gap-3 rounded-xl border p-3 transition-colors"
            :class="isDark ? 'border-slate-700/50 bg-slate-800/40' : 'border-slate-200 bg-slate-50/50'">
            <div class="flex-1 min-w-0">
              <div class="text-xs font-mono font-medium truncate" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ page.page }}</div>
              <div class="flex items-center gap-2 mt-1.5">
                <span class="text-[10px] px-1.5 py-0.5 rounded-full font-medium"
                  :class="page.title_ok ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600') : (isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600')">
                  Title
                </span>
                <span class="text-[10px] px-1.5 py-0.5 rounded-full font-medium"
                  :class="page.desc_ok ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600') : (isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600')">
                  Desc
                </span>
                <span class="text-[10px] px-1.5 py-0.5 rounded-full font-medium"
                  :class="page.h1_ok ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600') : (isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600')">
                  H1
                </span>
                <span class="text-[10px] px-1.5 py-0.5 rounded-full font-medium"
                  :class="page.og_ok ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600') : (isDark ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600')">
                  OG
                </span>
              </div>
            </div>
            <div class="text-right flex-shrink-0">
              <div class="text-sm font-semibold tabular-nums" :class="pageScoreColor(page.score)">{{ page.score }}</div>
              <div class="text-[10px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">/100</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Recommendations</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Prioritized actions to improve SEO</p>
        </div>
        <div class="p-4 space-y-3">
          <div v-for="(rec, i) in (audit?.recommendations || [])" :key="i"
            class="rounded-xl border p-3 transition-colors"
            :class="isDark ? 'border-slate-700/50 bg-slate-800/40' : 'border-slate-200 bg-slate-50/50'">
            <div class="flex items-start gap-2">
              <span class="text-[10px] font-bold px-1.5 py-0.5 rounded-full mt-0.5 flex-shrink-0 uppercase"
                :class="priorityBadge(rec.priority)">{{ rec.priority }}</span>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ rec.action }}</div>
                <div class="text-[11px] mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ rec.impact }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Blog Ideas -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b flex items-center justify-between" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <div>
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Blog Content Ideas</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">AI-generated content suggestions based on common conditions</p>
        </div>
        <button @click="refreshBlogIdeas" class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
          :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          Generate New Ideas
        </button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Title</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Category</th>
              <th class="text-right px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Est. Traffic</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Difficulty</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">SEO Score</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="idea in blogIdeas" :key="idea.id"
              class="border-t transition-colors"
              :class="isDark ? 'border-slate-800 hover:bg-slate-800/40' : 'border-slate-100 hover:bg-slate-50'">
              <td class="px-5 py-3 max-w-xs truncate" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ idea.title }}</td>
              <td class="px-5 py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium"
                  :class="isDark ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-700'">{{ idea.category }}</span>
              </td>
              <td class="px-5 py-3 text-right tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ (idea.estimated_monthly_traffic || 0).toLocaleString() }}/mo</td>
              <td class="px-5 py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium"
                  :class="difficultyBadge(idea.difficulty)">{{ idea.difficulty }}</span>
              </td>
              <td class="px-5 py-3 tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ idea.seo_score }}/100</td>
              <td class="px-5 py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium capitalize"
                  :class="statusClass(idea.status)">{{ idea.status }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Social share preview -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Site Features</h2>
      </div>
      <div class="p-5 grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div v-for="feature in siteFeatures" :key="feature.label"
          class="flex items-center gap-2 text-xs">
          <span class="w-2 h-2 rounded-full flex-shrink-0" :class="feature.ok ? 'bg-emerald-500' : 'bg-red-500'"></span>
          <span :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ feature.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getSeoAudit, getBlogIdeas } from '@/services/adminApi.js'

const { isDark } = useTheme()
const audit = ref(null)
const blogIdeas = ref([])

async function fetchData() {
  const [auditData, blogData] = await Promise.all([
    getSeoAudit(),
    getBlogIdeas(),
  ])
  audit.value = auditData
  blogIdeas.value = blogData.suggestions || []
}

async function refreshBlogIdeas() {
  const blogData = await getBlogIdeas()
  blogIdeas.value = blogData.suggestions || []
}

const { lastFetched, start: startPolling } = usePolling(fetchData, 30000)
onMounted(() => startPolling())

const lastUpdated = computed(() => lastFetched.value ? lastFetched.value.toLocaleTimeString() : '--')

function refresh() { fetchData() }

// Score styling
const scoreIconBg = computed(() => {
  const score = audit.value?.overall_score || 0
  if (score >= 80) return 'bg-emerald-500/10'
  if (score >= 60) return 'bg-amber-500/10'
  return 'bg-red-500/10'
})
const scoreIconColor = computed(() => {
  const score = audit.value?.overall_score || 0
  if (score >= 80) return 'text-emerald-500'
  if (score >= 60) return 'text-amber-500'
  return 'text-red-500'
})
const gradeColor = computed(() => {
  const grade = audit.value?.grade || 'D'
  const colors = { A: 'text-emerald-500', B: 'text-blue-500', C: 'text-amber-500', D: 'text-red-500' }
  return colors[grade] || 'text-red-500'
})

function pageScoreColor(score) {
  if (score >= 80) return isDark.value ? 'text-emerald-400' : 'text-emerald-600'
  if (score >= 60) return isDark.value ? 'text-amber-400' : 'text-amber-600'
  return isDark.value ? 'text-red-400' : 'text-red-600'
}

function priorityBadge(priority) {
  const map = {
    high: isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600',
    medium: isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600',
    low: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-600',
  }
  return map[priority] || map.low
}

function difficultyBadge(difficulty) {
  const map = {
    easy: isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-600',
    medium: isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600',
    hard: isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600',
  }
  return map[difficulty] || map.medium
}

function statusClass(status) {
  const map = {
    idea: isDark.value ? 'bg-slate-700 text-slate-300' : 'bg-slate-100 text-slate-600',
    draft: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-700',
    published: isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700',
  }
  return map[status] || map.idea
}

const siteFeatures = computed(() => {
  const m = audit.value?.metrics || {}
  return [
    { label: 'SSL Enabled', ok: m.ssl_enabled ?? false },
    { label: 'Mobile Friendly', ok: m.mobile_friendly ?? false },
    { label: 'Sitemap Present', ok: m.sitemap_present ?? false },
    { label: 'robots.txt', ok: m.robots_txt_present ?? false },
  ]
})
</script>
