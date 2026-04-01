<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Refill Tracker</h1>
      <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Track prescription refill dates and remaining refills</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="rounded-2xl border p-5 animate-pulse" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <div class="h-5 rounded w-1/3 mb-3" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-1/2" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="refills.length === 0" class="text-center py-20">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
        <svg class="w-10 h-10" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182M21.015 4.356v4.992"/></svg>
      </div>
      <h3 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">No refill data</h3>
      <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Add refill dates to your medications to track upcoming refills.</p>
    </div>

    <!-- Refill list sorted by urgency -->
    <div v-else class="space-y-3">
      <div v-for="refill in sortedRefills" :key="refill.id" class="rounded-2xl border-l-4 border p-5 transition-all hover:shadow-md" :class="[refillCardClass(refill), isDark ? 'bg-slate-900/50' : 'bg-white']">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <h3 class="font-bold text-lg" :class="isDark ? 'text-white' : 'text-slate-900'">{{ refill.name }}</h3>
              <span class="px-2.5 py-0.5 rounded-full text-caption font-semibold" :class="urgencyBadge(refill)">{{ urgencyLabel(refill) }}</span>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
              <div>
                <span class="block text-detail font-medium uppercase tracking-wider mb-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Last Filled</span>
                <span :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ refill.lastFilled || 'Unknown' }}</span>
              </div>
              <div>
                <span class="block text-detail font-medium uppercase tracking-wider mb-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Next Refill</span>
                <span class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ refill.nextRefill || 'Not set' }}</span>
              </div>
              <div>
                <span class="block text-detail font-medium uppercase tracking-wider mb-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Refills Left</span>
                <span :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ refill.refillsRemaining != null ? refill.refillsRemaining : 'N/A' }}</span>
              </div>
              <div>
                <span class="block text-detail font-medium uppercase tracking-wider mb-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Pharmacy</span>
                <span :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ refill.pharmacy || 'Not specified' }}</span>
              </div>
            </div>
          </div>
          <div class="flex sm:flex-col gap-2">
            <button @click="updateRefill(refill)" class="px-4 py-2 rounded-xl text-xs font-semibold transition-colors" :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'">
              Update Refill
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Update Refill Modal -->
    <Teleport to="body">
      <div v-if="editingRefill" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="editingRefill = null"></div>
        <div class="relative w-full max-w-sm rounded-2xl border shadow-2xl p-6" :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
          <h2 class="text-lg font-bold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Update Refill - {{ editingRefill.name }}</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Last Filled Date</label>
              <input v-model="editingRefill.lastFilled" type="date" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Refills Remaining</label>
              <input v-model.number="editingRefill.refillsRemaining" type="number" min="0" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
            </div>
          </div>
          <div class="flex gap-3 mt-5">
            <button @click="editingRefill = null" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-medium border" :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-200 text-slate-700 hover:bg-slate-50'">Cancel</button>
            <button @click="saveRefill" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500 transition-all">Save</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getMedications, getUpcomingRefills } from '@/services/medicationApi.js'

const { isDark } = useTheme()
const refills = ref([])
const loading = ref(true)
const editingRefill = ref(null)

function daysUntil(dateStr) {
  if (!dateStr) return Infinity
  const diff = new Date(dateStr) - new Date()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
}

const sortedRefills = computed(() => {
  return [...refills.value].sort((a, b) => daysUntil(a.nextRefill) - daysUntil(b.nextRefill))
})

function refillCardClass(refill) {
  const days = daysUntil(refill.nextRefill)
  if (days < 3) return isDark.value ? 'border-red-500 border-r-slate-800 border-t-slate-800 border-b-slate-800' : 'border-red-500 border-r-slate-200 border-t-slate-200 border-b-slate-200'
  if (days < 7) return isDark.value ? 'border-amber-500 border-r-slate-800 border-t-slate-800 border-b-slate-800' : 'border-amber-500 border-r-slate-200 border-t-slate-200 border-b-slate-200'
  return isDark.value ? 'border-emerald-500 border-r-slate-800 border-t-slate-800 border-b-slate-800' : 'border-emerald-500 border-r-slate-200 border-t-slate-200 border-b-slate-200'
}

function urgencyBadge(refill) {
  const days = daysUntil(refill.nextRefill)
  if (days < 3) return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-600'
  if (days < 7) return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-600'
  return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-600'
}

function urgencyLabel(refill) {
  const days = daysUntil(refill.nextRefill)
  if (days < 0) return 'Overdue'
  if (days === 0) return 'Today'
  if (days < 3) return `${days}d left`
  if (days < 7) return `${days}d left`
  if (days === Infinity) return 'No date'
  return `${days}d left`
}

function updateRefill(refill) {
  editingRefill.value = { ...refill }
}

function saveRefill() {
  const idx = refills.value.findIndex(r => r.id === editingRefill.value.id)
  if (idx >= 0) {
    // Recalculate next refill (30 day supply assumed)
    if (editingRefill.value.lastFilled) {
      const lastDate = new Date(editingRefill.value.lastFilled)
      lastDate.setDate(lastDate.getDate() + 30)
      editingRefill.value.nextRefill = lastDate.toISOString().split('T')[0]
    }
    refills.value[idx] = { ...editingRefill.value }
  }
  editingRefill.value = null
}

onMounted(async () => {
  try {
    const data = await getUpcomingRefills()
    refills.value = Array.isArray(data) ? data : data.refills || []
  } catch {
    refills.value = [
      { id: 1, name: 'Lisinopril', lastFilled: '2026-03-05', nextRefill: '2026-04-04', refillsRemaining: 3, pharmacy: 'CVS Pharmacy' },
      { id: 2, name: 'Metformin', lastFilled: '2026-03-20', nextRefill: '2026-04-01', refillsRemaining: 5, pharmacy: 'Walgreens' },
      { id: 3, name: 'Atorvastatin', lastFilled: '2026-02-15', nextRefill: '2026-03-17', refillsRemaining: 1, pharmacy: 'CVS Pharmacy' },
      { id: 4, name: 'Albuterol', lastFilled: '2026-01-10', nextRefill: '2026-04-10', refillsRemaining: 2, pharmacy: 'Rite Aid' },
    ]
  }
  loading.value = false
})
</script>
