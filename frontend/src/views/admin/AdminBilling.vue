<template>
  <div class="space-y-6">
    <!-- Page header -->
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Billing & Revenue</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Subscription metrics, usage tracking, and revenue analytics</p>
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

    <!-- Stripe Configuration Section -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b flex items-center justify-between" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <div class="flex items-center gap-3">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Stripe Configuration</h2>
          <span class="px-2 py-0.5 rounded-full text-[10px] font-semibold"
            :class="stripeStatus.configured
              ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-600')
              : (isDark ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600')">
            {{ stripeStatus.configured ? 'Stripe Connected' : 'Demo Mode' }}
          </span>
          <span v-if="stripeStatus.configured" class="px-2 py-0.5 rounded-full text-[10px] font-medium"
            :class="stripeStatus.mode === 'live'
              ? (isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600')
              : (isDark ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-600')">
            {{ stripeStatus.mode === 'live' ? 'Live' : 'Test' }}
          </span>
        </div>
        <button @click="showStripeConfig = !showStripeConfig" class="text-xs font-medium transition-colors px-3 py-1.5 rounded-lg"
          :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          {{ showStripeConfig ? 'Hide' : 'Configure' }}
        </button>
      </div>
      <div v-if="showStripeConfig" class="p-5 space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="space-y-1.5">
            <label class="text-xs font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Stripe Secret Key</label>
            <input v-model="stripeSecretKey" type="password" placeholder="sk_test_..." autocomplete="off"
              class="w-full px-3 py-2 rounded-lg text-sm border outline-none transition-colors"
              :class="isDark ? 'bg-slate-800 border-slate-700 text-slate-200 placeholder-slate-500 focus:border-blue-500' : 'bg-white border-slate-300 text-slate-800 placeholder-slate-400 focus:border-blue-500'" />
          </div>
          <div class="space-y-1.5">
            <label class="text-xs font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Webhook Secret</label>
            <input v-model="stripeWebhookSecret" type="password" placeholder="whsec_..." autocomplete="off"
              class="w-full px-3 py-2 rounded-lg text-sm border outline-none transition-colors"
              :class="isDark ? 'bg-slate-800 border-slate-700 text-slate-200 placeholder-slate-500 focus:border-blue-500' : 'bg-white border-slate-300 text-slate-800 placeholder-slate-400 focus:border-blue-500'" />
          </div>
        </div>
        <div class="flex items-center gap-3">
          <button @click="saveStripe" :disabled="stripeSaving" class="px-4 py-2 rounded-lg text-xs font-semibold text-white transition-colors"
            :class="stripeSaving ? 'bg-blue-400 cursor-wait' : 'bg-blue-600 hover:bg-blue-500'">
            {{ stripeSaving ? 'Saving...' : 'Save Keys' }}
          </button>
          <button @click="testStripe" :disabled="stripeTesting" class="px-4 py-2 rounded-lg text-xs font-semibold transition-colors border"
            :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-300 text-slate-600 hover:bg-slate-50'">
            {{ stripeTesting ? 'Testing...' : 'Test Connection' }}
          </button>
          <span v-if="stripeMessage" class="text-xs font-medium" :class="stripeMessageError ? 'text-red-500' : 'text-emerald-500'">
            {{ stripeMessage }}
          </span>
        </div>
        <p class="text-[11px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          In demo mode, upgrades happen instantly without payment. Configure Stripe to enable real payment processing.
        </p>
      </div>
    </div>

    <!-- Revenue Dashboard -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Revenue Dashboard</h2>
        <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Revenue breakdown by source</p>
      </div>
      <div class="p-5">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="rev in revenueSources" :key="rev.label" class="p-4 rounded-xl border"
            :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-slate-50 border-slate-200'">
            <div class="text-[11px] font-medium mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ rev.label }}</div>
            <div class="text-lg font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">${{ rev.value.toLocaleString() }}</div>
            <div class="mt-2 h-1.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
              <div class="h-full rounded-full transition-all duration-500" :class="rev.barClass"
                :style="{ width: rev.pct + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Subscription Overview -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Subscription Overview</h2>
        <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Subscribers by tier and estimated MRR</p>
      </div>
      <div class="p-5">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="sub in subscriptionTiers" :key="sub.name" class="p-4 rounded-xl border text-center"
            :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-slate-50 border-slate-200'">
            <div class="w-8 h-8 mx-auto rounded-full flex items-center justify-center mb-2" :class="sub.iconBg">
              <span class="text-sm">{{ sub.icon }}</span>
            </div>
            <div class="text-xs font-semibold capitalize mb-1" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ sub.name }}</div>
            <div class="text-xl font-bold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ sub.count }}</div>
            <div class="text-[10px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              ${{ sub.mrr }}/mo MRR
            </div>
          </div>
        </div>
        <div class="mt-4 pt-4 border-t flex items-center justify-between"
          :class="isDark ? 'border-slate-700' : 'border-slate-200'">
          <span class="text-xs font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Total Estimated MRR</span>
          <span class="text-lg font-bold tabular-nums" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">
            ${{ totalSubscriptionMRR.toLocaleString() }}
          </span>
        </div>
      </div>
    </div>

    <!-- Revenue metric cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="metric in revenueMetrics" :key="metric.label"
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

    <!-- Middle row: Usage chart + Tier distribution -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Daily usage chart (2/3) -->
      <div class="lg:col-span-2 rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Daily Diagnoses</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Diagnoses processed per day (last 15 days)</p>
        </div>
        <div class="p-5">
          <div v-if="dailyUsage.length > 0" class="space-y-2">
            <div v-for="(day, i) in dailyUsage" :key="i" class="flex items-center gap-3">
              <span class="text-[10px] tabular-nums w-16 text-right flex-shrink-0"
                :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ formatDay(day.date) }}</span>
              <div class="flex-1 h-5 rounded-md overflow-hidden"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <div class="h-full rounded-md bg-emerald-500 transition-all duration-500"
                  :style="{ width: barWidth(day.diagnoses) }"></div>
              </div>
              <span class="text-[10px] tabular-nums w-8 flex-shrink-0"
                :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ day.diagnoses }}</span>
            </div>
          </div>
          <div v-else class="text-center py-8 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            No usage data available
          </div>
        </div>
      </div>

      <!-- Tier distribution (1/3) -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Tier Distribution</h2>
        </div>
        <div class="p-5 space-y-4">
          <div v-for="tier in tierData" :key="tier.name" class="space-y-1.5">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full" :class="tier.dotClass"></span>
                <span class="text-xs font-medium capitalize" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ tier.name }}</span>
              </div>
              <span class="text-xs tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ tier.count }} users</span>
            </div>
            <div class="w-full h-2 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
              <div class="h-full rounded-full transition-all duration-500" :class="tier.barClass"
                :style="{ width: tierBarWidth(tier.count) }"></div>
            </div>
          </div>

          <!-- Quick stats -->
          <div class="pt-3 mt-3 border-t space-y-2" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
            <div class="flex justify-between text-xs">
              <span :class="isDark ? 'text-slate-400' : 'text-slate-500'">Churn Rate</span>
              <span class="font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ data?.churn_rate || 0 }}%</span>
            </div>
            <div class="flex justify-between text-xs">
              <span :class="isDark ? 'text-slate-400' : 'text-slate-500'">Growth Rate</span>
              <span class="font-medium text-emerald-500">+{{ data?.growth_rate || 0 }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Transactions table -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b flex items-center justify-between" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Recent Transactions</h2>
        <span class="text-[10px] font-medium px-2 py-0.5 rounded-full"
          :class="isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-100 text-slate-600'">
          {{ transactions.length }} records
        </span>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Invoice</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">User</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Tier</th>
              <th class="text-right px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Amount</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Status</th>
              <th class="text-left px-5 py-3 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tx in transactions" :key="tx.invoice_id"
              class="border-t transition-colors"
              :class="isDark ? 'border-slate-800 hover:bg-slate-800/40' : 'border-slate-100 hover:bg-slate-50'">
              <td class="px-5 py-3 font-mono tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ tx.invoice_id?.slice(0, 12) }}</td>
              <td class="px-5 py-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ tx.user_id }}</td>
              <td class="px-5 py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium capitalize"
                  :class="tierBadgeClass(tx.tier)">{{ tx.tier }}</span>
              </td>
              <td class="px-5 py-3 text-right tabular-nums font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">${{ tx.amount }}</td>
              <td class="px-5 py-3">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-medium"
                  :class="statusBadgeClass(tx.status)">{{ tx.status }}</span>
              </td>
              <td class="px-5 py-3 tabular-nums" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ formatDate(tx.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { usePolling } from '@/composables/usePolling.js'
import { getBillingSummary, getStripeStatus, saveStripeConfig } from '@/services/adminApi.js'

const { isDark } = useTheme()
const data = ref(null)

// Stripe configuration state
const showStripeConfig = ref(false)
const stripeSecretKey = ref('')
const stripeWebhookSecret = ref('')
const stripeSaving = ref(false)
const stripeTesting = ref(false)
const stripeMessage = ref('')
const stripeMessageError = ref(false)
const stripeStatus = ref({ configured: false, mode: 'demo' })

async function fetchStripeStatus() {
  try {
    stripeStatus.value = await getStripeStatus()
  } catch (e) {
    stripeStatus.value = { configured: false, mode: 'demo' }
  }
}

async function saveStripe() {
  stripeSaving.value = true
  stripeMessage.value = ''
  try {
    await saveStripeConfig(stripeSecretKey.value, stripeWebhookSecret.value)
    stripeMessage.value = 'Keys saved successfully'
    stripeMessageError.value = false
    await fetchStripeStatus()
  } catch (e) {
    stripeMessage.value = e.message || 'Failed to save'
    stripeMessageError.value = true
  } finally {
    stripeSaving.value = false
  }
}

async function testStripe() {
  stripeTesting.value = true
  stripeMessage.value = ''
  try {
    if (!stripeSecretKey.value || !stripeSecretKey.value.startsWith('sk_')) {
      stripeMessage.value = 'Invalid key format. Must start with sk_test_ or sk_live_'
      stripeMessageError.value = true
      return
    }
    await saveStripeConfig(stripeSecretKey.value, stripeWebhookSecret.value)
    await fetchStripeStatus()
    if (stripeStatus.value.configured) {
      stripeMessage.value = 'Connection successful (' + stripeStatus.value.mode + ' mode)'
      stripeMessageError.value = false
    } else {
      stripeMessage.value = 'Key saved but not recognized as valid Stripe key'
      stripeMessageError.value = true
    }
  } catch (e) {
    stripeMessage.value = e.message || 'Connection failed'
    stripeMessageError.value = true
  } finally {
    stripeTesting.value = false
  }
}

async function fetchData() {
  data.value = await getBillingSummary()
}

const { lastFetched, start: startPolling } = usePolling(fetchData, 15000)
onMounted(() => {
  startPolling()
  fetchStripeStatus()
})

const lastUpdated = computed(() => lastFetched.value ? lastFetched.value.toLocaleTimeString() : '--')

function refresh() { fetchData() }

// Subscription Overview
const tierPrices = { free: 0, starter: 19, pro: 49, enterprise: 199 }
const subscriptionTiers = computed(() => {
  const dist = data.value?.tier_distribution || {}
  const tiers = [
    { name: 'Free', key: 'free', icon: '\u2014', iconBg: 'bg-slate-200 dark:bg-slate-700' },
    { name: 'Plus', key: 'starter', icon: '+', iconBg: 'bg-blue-100 dark:bg-blue-500/20' },
    { name: 'Pro', key: 'pro', icon: 'P', iconBg: 'bg-violet-100 dark:bg-violet-500/20' },
    { name: 'Family', key: 'enterprise', icon: 'F', iconBg: 'bg-emerald-100 dark:bg-emerald-500/20' },
  ]
  return tiers.map(t => ({
    ...t,
    count: dist[t.key] || 0,
    mrr: ((dist[t.key] || 0) * (tierPrices[t.key] || 0)),
  }))
})

const totalSubscriptionMRR = computed(() => subscriptionTiers.value.reduce((sum, t) => sum + t.mrr, 0))

// Revenue Dashboard
const revenueSources = computed(() => {
  const mrr = data.value?.mrr || 0
  const subRev = totalSubscriptionMRR.value
  const apiRev = Math.round(mrr * 0.15)  // estimated 15% from API keys
  const referralRev = Math.round(mrr * 0.05)  // estimated 5% from referrals
  const total = subRev + apiRev + referralRev
  const maxVal = Math.max(subRev, apiRev, referralRev, 1)
  return [
    { label: 'Subscription Revenue', value: subRev, barClass: 'bg-violet-500', pct: (subRev / maxVal) * 100 },
    { label: 'API Revenue', value: apiRev, barClass: 'bg-blue-500', pct: (apiRev / maxVal) * 100 },
    { label: 'Referral Revenue', value: referralRev, barClass: 'bg-amber-500', pct: (referralRev / maxVal) * 100 },
    { label: 'Total MRR', value: total, barClass: 'bg-emerald-500', pct: 100 },
  ]
})

// Revenue metric cards
const revenueMetrics = computed(() => {
  if (!data.value) return []
  const d = data.value
  return [
    {
      label: 'Monthly Recurring Revenue',
      value: `$${(d.mrr || 0).toLocaleString()}`,
      trend: d.growth_rate || null,
      iconBg: 'bg-emerald-500/10',
      icon: '<svg fill="none" stroke="rgb(16,185,129)" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
    },
    {
      label: 'Total Users',
      value: d.total_users || 0,
      trend: null,
      iconBg: 'bg-blue-500/10',
      icon: '<svg fill="none" stroke="rgb(59,130,246)" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z"/></svg>',
    },
    {
      label: 'Paid Users',
      value: d.paid_users || 0,
      trend: null,
      iconBg: 'bg-violet-500/10',
      icon: '<svg fill="none" stroke="rgb(139,92,246)" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z"/></svg>',
    },
    {
      label: 'ARPU',
      value: `$${d.arpu || 0}`,
      trend: null,
      iconBg: 'bg-amber-500/10',
      icon: '<svg fill="none" stroke="rgb(245,158,11)" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"/></svg>',
    },
  ]
})

// Daily usage chart
const dailyUsage = computed(() => data.value?.daily_usage || [])
const maxDailyDiagnoses = computed(() => Math.max(...dailyUsage.value.map(d => d.diagnoses), 1))
function barWidth(count) { return `${Math.max(2, (count / maxDailyDiagnoses.value) * 100)}%` }

function formatDay(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr + 'T00:00:00')
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

// Tier distribution
const tierData = computed(() => {
  const dist = data.value?.tier_distribution || {}
  const tiers = [
    { name: 'free', dotClass: 'bg-slate-400', barClass: 'bg-slate-400' },
    { name: 'starter', dotClass: 'bg-blue-500', barClass: 'bg-blue-500' },
    { name: 'pro', dotClass: 'bg-violet-500', barClass: 'bg-violet-500' },
    { name: 'enterprise', dotClass: 'bg-emerald-500', barClass: 'bg-emerald-500' },
  ]
  return tiers.map(t => ({ ...t, count: dist[t.name] || 0 }))
})
const maxTierCount = computed(() => Math.max(...tierData.value.map(t => t.count), 1))
function tierBarWidth(count) { return `${Math.max(2, (count / maxTierCount.value) * 100)}%` }

// Transactions
const transactions = computed(() => data.value?.recent_transactions || [])

function formatDate(iso) {
  if (!iso) return '--'
  return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function tierBadgeClass(tier) {
  const map = {
    free: isDark.value ? 'bg-slate-700 text-slate-300' : 'bg-slate-100 text-slate-600',
    starter: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-700',
    pro: isDark.value ? 'bg-violet-500/15 text-violet-400' : 'bg-violet-50 text-violet-700',
    enterprise: isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700',
  }
  return map[tier] || map.free
}

function statusBadgeClass(status) {
  if (status === 'paid') return isDark.value ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'
  if (status === 'pending') return isDark.value ? 'bg-amber-500/10 text-amber-400' : 'bg-amber-50 text-amber-600'
  return isDark.value ? 'bg-red-500/10 text-red-400' : 'bg-red-50 text-red-600'
}
</script>
