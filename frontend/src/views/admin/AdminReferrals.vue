<template>
  <div class="space-y-6">
    <APageHeader title="Referral Analytics" subtitle="Track specialist referral clicks and revenue from 'Call Office' and 'Get Directions' actions" :showRefresh="false" />

    <!-- Period selector -->
    <div class="flex gap-2">
      <button v-for="p in periods" :key="p.days"
        @click="selectedDays = p.days; fetchStats()"
        class="px-3 py-1.5 text-xs font-semibold rounded-lg border transition-all"
        :class="selectedDays === p.days
          ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-400'
          : isDark
            ? 'bg-slate-800/60 border-slate-700/50 text-slate-400 hover:border-slate-600'
            : 'bg-slate-50 border-slate-200 text-slate-600 hover:border-slate-300'">
        {{ p.label }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-16">
      <div class="w-8 h-8 border-2 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin"></div>
    </div>

    <template v-else>
      <AKpiStrip :items="referralKpiItems" :cols="4" />

      <!-- Breakdown grids -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- By Specialty -->
        <div class="rounded-xl border p-6"
          :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
          <h2 class="text-lg font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">By Specialty</h2>
          <AEmptyState v-if="Object.keys(stats.by_specialty || {}).length === 0"
            title="No specialty data"
            description="No referral data yet. Referrals are tracked when patients click 'Call Office' or 'Get Directions' on specialist recommendations."
          />
          <div v-else class="space-y-3">
            <div v-for="(count, specialty) in sortedSpecialties" :key="specialty" class="flex items-center gap-3">
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-sm font-medium truncate" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ specialty }}</span>
                  <span class="text-xs font-mono" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ count }}</span>
                </div>
                <div class="h-2 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                  <div class="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all"
                    :style="{ width: Math.max((count / maxSpecialtyCount) * 100, 4) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- By Action Type -->
        <div class="rounded-xl border p-6"
          :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
          <h2 class="text-lg font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">By Action Type</h2>
          <AEmptyState v-if="Object.keys(stats.by_action || {}).length === 0"
            title="No action data"
            description="No referral actions tracked yet."
          />
          <div v-else class="space-y-4">
            <div v-for="(count, action) in stats.by_action" :key="action"
              class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
                :class="actionIconClass(action)">
                <svg v-if="action === 'call'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                </svg>
                <svg v-else-if="action === 'directions'" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9"/>
                </svg>
              </div>
              <div class="flex-1">
                <p class="text-sm font-semibold capitalize" :class="isDark ? 'text-white' : 'text-slate-900'">{{ action }}</p>
                <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ count }} clicks</p>
              </div>
              <span class="text-lg font-bold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                {{ Math.round((count / (stats.total_clicks || 1)) * 100) }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top referred doctors -->
      <div class="rounded-xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
          <h2 class="text-lg font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Top Referred Doctors</h2>
        </div>
        <AEmptyState v-if="!stats.top_doctors || stats.top_doctors.length === 0"
          title="No referral data yet"
          description="No referral data yet. Referrals are tracked when patients click 'Call Office' or 'Get Directions' on specialist recommendations."
        />
        <table v-else class="w-full text-sm">
          <thead>
            <tr :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
              <th class="text-left px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Doctor</th>
              <th class="text-left px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Specialty</th>
              <th class="text-left px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">NPI</th>
              <th class="text-right px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Clicks</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in stats.top_doctors" :key="doc.npi"
              class="border-t" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
              <td class="px-6 py-3 font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ doc.name }}</td>
              <td class="px-6 py-3" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">{{ doc.specialty }}</td>
              <td class="px-6 py-3 font-mono text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ doc.npi }}</td>
              <td class="px-6 py-3 text-right font-bold" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ doc.clicks }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import APageHeader from '@/components/admin/APageHeader.vue'
import AKpiStrip from '@/components/admin/AKpiStrip.vue'
import AEmptyState from '@/components/admin/AEmptyState.vue'

const { isDark } = useTheme()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const loading = ref(true)
const stats = ref({})
const selectedDays = ref(30)

const periods = [
  { label: '7 days', days: 7 },
  { label: '30 days', days: 30 },
  { label: '90 days', days: 90 },
]

const statsCards = computed(() => [
  {
    label: 'Total Clicks',
    value: (stats.value.total_clicks || 0).toLocaleString(),
  },
  {
    label: 'Qualified Referrals',
    value: (stats.value.qualified_referrals || 0).toLocaleString(),
    sub: 'Unique user+doctor per day',
  },
  {
    label: 'Est. Revenue',
    value: '$' + (stats.value.estimated_revenue || 0).toLocaleString(),
    color: isDark.value ? 'text-emerald-400' : 'text-emerald-600',
  },
  {
    label: 'Avg per Referral',
    value: '$' + (stats.value.avg_revenue_per_referral || 0).toFixed(2),
    sub: '$5-$25 range by specialty',
  },
])

const referralKpiItems = computed(() =>
  statsCards.value.map(s => ({
    label: s.label,
    value: s.value,
    sublabel: s.sub || undefined,
  }))
)

const sortedSpecialties = computed(() => {
  const entries = Object.entries(stats.value.by_specialty || {})
  entries.sort((a, b) => b[1] - a[1])
  return Object.fromEntries(entries)
})

const maxSpecialtyCount = computed(() => {
  const vals = Object.values(stats.value.by_specialty || {})
  return Math.max(...vals, 1)
})

function actionIconClass(action) {
  const map = {
    call: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-600',
    directions: isDark.value ? 'bg-purple-500/15 text-purple-400' : 'bg-purple-50 text-purple-600',
    website: isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600',
  }
  return map[action] || map.call
}

async function fetchStats() {
  loading.value = true
  try {
    const resp = await fetch(`${API_BASE_URL}/api/admin/referrals/stats?days=${selectedDays.value}`)
    if (resp.ok) {
      stats.value = await resp.json()
    }
  } catch (e) {
    console.error('Failed to fetch referral stats:', e)
  }
  loading.value = false
}

onMounted(() => fetchStats())
</script>
