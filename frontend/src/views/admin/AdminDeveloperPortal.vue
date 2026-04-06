<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Developer Portal</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Manage API keys for external developers using the 7-agent pipeline
        </p>
      </div>
      <button @click="showCreateModal = true"
        class="px-4 py-2.5 text-sm font-semibold rounded-xl bg-gradient-to-r from-blue-600 to-indigo-500 text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30 transition-all">
        + Create New Key
      </button>
    </div>

    <!-- Stats cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="stat in statsCards" :key="stat.label"
        class="rounded-xl border p-4"
        :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <p class="text-xs font-medium uppercase tracking-wider" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          {{ stat.label }}
        </p>
        <p class="text-2xl font-bold mt-1" :class="isDark ? 'text-white' : 'text-slate-900'">
          {{ stat.value }}
        </p>
      </div>
    </div>

    <!-- Usage chart (simple bar chart) -->
    <div class="rounded-xl border p-6"
      :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
      <h2 class="text-lg font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Calls Per Day (Last 14 Days)</h2>
      <div class="flex items-end gap-1 h-40">
        <div v-for="(bar, idx) in chartBars" :key="idx"
          class="flex-1 rounded-t-md transition-all"
          :class="isDark ? 'bg-blue-500/60' : 'bg-blue-400'"
          :style="{ height: bar.height + '%' }"
          :title="bar.date + ': ' + bar.count + ' calls'">
        </div>
      </div>
      <div class="flex justify-between mt-2 text-[10px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
        <span>{{ chartBars[0]?.date || '' }}</span>
        <span>{{ chartBars[chartBars.length - 1]?.date || '' }}</span>
      </div>
    </div>

    <!-- Pricing tiers -->
    <div class="rounded-xl border p-6"
      :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
      <h2 class="text-lg font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Pricing Tiers</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="(plan, key) in plans" :key="key"
          class="rounded-xl border p-4 text-center"
          :class="isDark ? 'bg-slate-800/50 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
          <p class="text-xs font-bold uppercase tracking-wider" :class="isDark ? 'text-blue-400' : 'text-blue-600'">
            {{ key }}
          </p>
          <p class="text-xl font-bold mt-2" :class="isDark ? 'text-white' : 'text-slate-900'">
            {{ plan.price ? '$' + plan.price + '/mo' : '$' + plan.price_per_call + '/call' }}
          </p>
          <p class="text-xs mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            {{ plan.limit ? plan.limit.toLocaleString() + ' calls/mo' : 'Unlimited' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Keys table -->
    <div class="rounded-xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
      <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
        <h2 class="text-lg font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">API Keys</h2>
      </div>

      <div v-if="loading" class="p-8 text-center">
        <div class="w-8 h-8 border-2 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mx-auto"></div>
      </div>

      <div v-else-if="keys.length === 0" class="p-8 text-center text-sm"
        :class="isDark ? 'text-slate-500' : 'text-slate-400'">
        No API keys created yet. Click "Create New Key" to get started.
      </div>

      <table v-else class="w-full text-sm">
        <thead>
          <tr :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
            <th class="text-left px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Key</th>
            <th class="text-left px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Developer</th>
            <th class="text-left px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Plan</th>
            <th class="text-right px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">This Month</th>
            <th class="text-right px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Total</th>
            <th class="text-center px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Status</th>
            <th class="text-center px-6 py-3 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="k in keys" :key="k.key"
            class="border-t" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <td class="px-6 py-3 font-mono text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
              {{ k.key.slice(0, 12) }}...
            </td>
            <td class="px-6 py-3">
              <p class="font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ k.developer }}</p>
              <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ k.email }}</p>
            </td>
            <td class="px-6 py-3">
              <span class="px-2 py-0.5 text-xs font-bold uppercase rounded-full"
                :class="planBadgeClass(k.plan)">
                {{ k.plan }}
              </span>
            </td>
            <td class="px-6 py-3 text-right font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
              {{ k.calls_this_month?.toLocaleString() || 0 }}
            </td>
            <td class="px-6 py-3 text-right font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
              {{ k.total_calls?.toLocaleString() || 0 }}
            </td>
            <td class="px-6 py-3 text-center">
              <span class="px-2 py-0.5 text-[10px] font-bold uppercase rounded-full"
                :class="k.active
                  ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700')
                  : (isDark ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-700')">
                {{ k.active ? 'Active' : 'Revoked' }}
              </span>
            </td>
            <td class="px-6 py-3 text-center">
              <button v-if="k.active" @click="revokeKey(k.key)"
                class="text-xs font-medium px-3 py-1 rounded-lg transition-colors"
                :class="isDark ? 'text-red-400 hover:bg-red-500/15' : 'text-red-600 hover:bg-red-50'">
                Revoke
              </button>
              <span v-else class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-300'">--</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create Key Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showCreateModal" class="fixed inset-0 z-[9999] flex items-center justify-center p-4" @click.self="showCreateModal = false">
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
          <div class="relative w-full max-w-md rounded-2xl border shadow-2xl p-6"
            :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-slate-200'">
            <h3 class="text-lg font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Create API Key</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-xs font-semibold mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Developer Name</label>
                <input v-model="newKey.developer_name" type="text" placeholder="Acme Health"
                  class="w-full px-3 py-2 text-sm rounded-xl border"
                  :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
              </div>
              <div>
                <label class="block text-xs font-semibold mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Email</label>
                <input v-model="newKey.email" type="email" placeholder="dev@acmehealth.com"
                  class="w-full px-3 py-2 text-sm rounded-xl border"
                  :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
              </div>
              <div>
                <label class="block text-xs font-semibold mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Plan</label>
                <select v-model="newKey.plan"
                  class="w-full px-3 py-2 text-sm rounded-xl border"
                  :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'">
                  <option value="starter">Starter ($49/mo - 1K calls)</option>
                  <option value="growth">Growth ($299/mo - 10K calls)</option>
                  <option value="enterprise">Enterprise ($1,999/mo - 100K calls)</option>
                  <option value="payg">Pay-as-you-go ($1.50/call)</option>
                </select>
              </div>
            </div>
            <div class="flex gap-3 mt-6">
              <button @click="showCreateModal = false"
                class="flex-1 px-4 py-2 text-sm font-medium rounded-xl border transition-colors"
                :class="isDark ? 'border-slate-700 text-slate-400 hover:bg-slate-800' : 'border-slate-200 text-slate-600 hover:bg-slate-50'">
                Cancel
              </button>
              <button @click="createKey"
                :disabled="!newKey.developer_name || !newKey.email"
                class="flex-1 px-4 py-2 text-sm font-semibold rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition-colors disabled:opacity-50">
                Create Key
              </button>
            </div>
            <!-- Show created key -->
            <div v-if="createdKey" class="mt-4 p-3 rounded-xl border"
              :class="isDark ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-emerald-50 border-emerald-200'">
              <p class="text-xs font-semibold mb-1" :class="isDark ? 'text-emerald-400' : 'text-emerald-700'">Key created! Copy it now -- it won't be shown again in full.</p>
              <code class="block text-xs font-mono break-all" :class="isDark ? 'text-emerald-300' : 'text-emerald-800'">{{ createdKey }}</code>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const loading = ref(true)
const keys = ref([])
const usageStats = ref({})
const dailyUsage = ref({})
const showCreateModal = ref(false)
const createdKey = ref('')
const newKey = ref({ developer_name: '', email: '', plan: 'starter' })

const plans = {
  starter: { limit: 1000, price: 49 },
  growth: { limit: 10000, price: 299 },
  enterprise: { limit: 100000, price: 1999 },
  payg: { limit: null, price_per_call: 1.50 },
}

const statsCards = computed(() => [
  { label: 'Active Keys', value: usageStats.value.active_keys || 0 },
  { label: 'Total Calls', value: (usageStats.value.total_calls || 0).toLocaleString() },
  { label: 'Monthly Revenue', value: '$' + (usageStats.value.estimated_monthly_revenue || 0).toLocaleString() },
  { label: 'Inactive Keys', value: usageStats.value.inactive_keys || 0 },
])

const chartBars = computed(() => {
  // Aggregate daily usage across all keys for last 14 days
  const days = []
  const now = new Date()
  for (let i = 13; i >= 0; i--) {
    const d = new Date(now)
    d.setDate(d.getDate() - i)
    const key = d.toISOString().split('T')[0]
    let count = 0
    for (const keyUsage of Object.values(dailyUsage.value || {})) {
      count += keyUsage[key] || 0
    }
    days.push({ date: key.slice(5), count })
  }
  const max = Math.max(...days.map(d => d.count), 1)
  return days.map(d => ({ ...d, height: Math.max((d.count / max) * 100, 2) }))
})

function planBadgeClass(plan) {
  const map = {
    starter: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-700',
    growth: isDark.value ? 'bg-purple-500/15 text-purple-400' : 'bg-purple-50 text-purple-700',
    enterprise: isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-700',
    payg: isDark.value ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-600',
  }
  return map[plan] || map.starter
}

async function fetchKeys() {
  loading.value = true
  try {
    const resp = await fetch(`${API_BASE_URL}/api/developer/keys`)
    if (resp.ok) {
      const data = await resp.json()
      keys.value = data.keys || []
    }
  } catch (e) { console.error('Failed to fetch keys:', e) }
  loading.value = false
}

async function fetchUsage() {
  try {
    const resp = await fetch(`${API_BASE_URL}/api/developer/usage`)
    if (resp.ok) {
      const data = await resp.json()
      usageStats.value = data
      dailyUsage.value = data.daily_usage || {}
    }
  } catch (e) { console.error('Failed to fetch usage:', e) }
}

async function createKey() {
  try {
    const resp = await fetch(`${API_BASE_URL}/api/developer/keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newKey.value),
    })
    if (resp.ok) {
      const data = await resp.json()
      createdKey.value = data.key
      newKey.value = { developer_name: '', email: '', plan: 'starter' }
      await fetchKeys()
      await fetchUsage()
    }
  } catch (e) { console.error('Failed to create key:', e) }
}

async function revokeKey(key) {
  if (!confirm('Are you sure you want to revoke this API key?')) return
  try {
    await fetch(`${API_BASE_URL}/api/developer/keys/${key}`, { method: 'DELETE' })
    await fetchKeys()
    await fetchUsage()
  } catch (e) { console.error('Failed to revoke key:', e) }
}

onMounted(() => {
  fetchKeys()
  fetchUsage()
})
</script>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 0.2s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
