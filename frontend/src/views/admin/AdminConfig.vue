<template>
  <div class="space-y-6">
    <!-- Page header -->
    <APageHeader title="Configuration" subtitle="Manage system settings and parameters" :show-refresh="false" />

    <!-- Search bar -->
    <div class="relative">
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
      </svg>
      <input v-model="searchQuery" type="text" placeholder="Search by key or description..."
        class="w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm transition-colors outline-none"
        :class="isDark
          ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-500 focus:border-blue-500'
          : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400 focus:border-blue-500 shadow-sm'" />
    </div>

    <!-- Category tabs -->
    <ATabBar :tabs="categoryTabs" v-model="activeCategory" />

    <!-- Config cards -->
    <div class="space-y-3">
      <div v-for="cfg in filteredConfigs" :key="cfg.key"
        class="rounded-xl border p-4 transition-all"
        :class="[
          editingKey === cfg.key
            ? (isDark ? 'bg-slate-800/60 border-blue-500/40 ring-1 ring-blue-500/20' : 'bg-blue-50/30 border-blue-300 ring-1 ring-blue-200')
            : (isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'),
          cfg.readonly ? 'opacity-75' : ''
        ]">
        <!-- Card header -->
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-mono font-bold text-sm" :class="isDark ? 'text-white' : 'text-slate-900'">{{ cfg.key }}</span>
              <span class="text-[10px] font-medium px-2 py-0.5 rounded-full" :class="categoryBadgeClass(cfg.category)">{{ cfg.category }}</span>
              <span v-if="cfg.readonly" class="text-[10px] font-medium px-2 py-0.5 rounded-full"
                :class="isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-200 text-slate-500'">read-only</span>
            </div>
            <p class="text-xs mt-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ cfg.description }}</p>
          </div>

          <!-- Edit / Save / Cancel controls -->
          <div v-if="!cfg.readonly" class="flex items-center gap-2 flex-shrink-0">
            <template v-if="editingKey === cfg.key">
              <button @click="cancelEdit"
                class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
                :class="isDark ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                Cancel
              </button>
              <button @click="saveEdit(cfg)"
                :disabled="saving"
                class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors disabled:opacity-50"
                :class="isDark ? 'bg-blue-600 text-white hover:bg-blue-500' : 'bg-blue-600 text-white hover:bg-blue-700'">
                {{ saving ? 'Saving...' : 'Save' }}
              </button>
            </template>
            <template v-else>
              <button @click="startEdit(cfg)"
                class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
                :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                Edit
              </button>
            </template>
          </div>
        </div>

        <!-- Value display / edit area -->
        <div class="mt-3">
          <!-- Editing mode -->
          <template v-if="editingKey === cfg.key">
            <!-- Number input -->
            <input v-if="cfg.type === 'number'" v-model.number="editValue" type="number"
              :min="cfg.validation?.min" :max="cfg.validation?.max" :step="cfg.validation?.step || 1"
              class="w-full max-w-xs px-3 py-2 rounded-lg border text-sm font-mono outline-none transition-colors"
              :class="isDark
                ? 'bg-slate-800 border-slate-600 text-white focus:border-blue-500'
                : 'bg-white border-slate-300 text-slate-900 focus:border-blue-500'" />

            <!-- Boolean toggle -->
            <div v-else-if="cfg.type === 'boolean'" class="flex items-center gap-3">
              <button @click="editValue = !editValue"
                class="relative w-11 h-6 rounded-full transition-colors focus:outline-none"
                :class="editValue
                  ? 'bg-blue-600'
                  : (isDark ? 'bg-slate-600' : 'bg-slate-300')">
                <div class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white transition-transform shadow-sm"
                  :class="editValue ? 'translate-x-5' : 'translate-x-0'"></div>
              </button>
              <span class="text-sm font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ editValue ? 'true' : 'false' }}</span>
            </div>

            <!-- Select dropdown -->
            <select v-else-if="cfg.type === 'select'" v-model="editValue"
              class="px-3 py-2 rounded-lg border text-sm font-mono outline-none transition-colors appearance-none cursor-pointer"
              :class="isDark
                ? 'bg-slate-800 border-slate-600 text-white focus:border-blue-500'
                : 'bg-white border-slate-300 text-slate-900 focus:border-blue-500'">
              <option v-for="opt in cfg.options" :key="opt" :value="opt">{{ opt }}</option>
            </select>

            <!-- String input (default) -->
            <input v-else v-model="editValue" type="text"
              class="w-full max-w-md px-3 py-2 rounded-lg border text-sm font-mono outline-none transition-colors"
              :class="isDark
                ? 'bg-slate-800 border-slate-600 text-white focus:border-blue-500'
                : 'bg-white border-slate-300 text-slate-900 focus:border-blue-500'" />
          </template>

          <!-- Display mode -->
          <template v-else>
            <!-- Boolean display -->
            <div v-if="cfg.type === 'boolean'" class="flex items-center gap-3">
              <div class="relative w-11 h-6 rounded-full cursor-default"
                :class="cfg.value
                  ? (isDark ? 'bg-blue-600/60' : 'bg-blue-500/40')
                  : (isDark ? 'bg-slate-700' : 'bg-slate-200')">
                <div class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform"
                  :class="cfg.value ? 'translate-x-5' : 'translate-x-0'"></div>
              </div>
              <span class="text-sm font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ cfg.value ? 'true' : 'false' }}</span>
            </div>

            <!-- Other value display -->
            <span v-else class="text-sm font-mono px-2.5 py-1 rounded-lg inline-block"
              :class="isDark ? 'bg-slate-800 text-slate-300' : 'bg-slate-100 text-slate-700'">
              {{ cfg.value }}
            </span>
          </template>
        </div>

        <!-- Footer: updated info -->
        <div v-if="cfg.updated_at" class="mt-3 pt-3 border-t text-[11px] flex items-center gap-3"
          :class="isDark ? 'border-slate-700/50 text-slate-500' : 'border-slate-100 text-slate-400'">
          <span>Updated {{ formatTime(cfg.updated_at) }}</span>
          <span v-if="cfg.updated_by">by {{ cfg.updated_by }}</span>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="filteredConfigs.length === 0 && !loading"
      class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <AEmptyState
        :title="searchQuery ? 'No matching settings' : 'No configuration entries'"
        :description="searchQuery ? 'No settings match your search query. Try different keywords or clear the search.' : 'Configuration entries will be loaded from the backend. Check that the config API is available.'"
        :action-label="searchQuery ? 'Clear Search' : ''"
        @action="searchQuery = ''" />
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <div class="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Toast notification -->
    <Teleport to="body">
      <Transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-2" enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-2">
        <div v-if="toast.show" class="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl shadow-lg text-sm font-medium flex items-center gap-2"
          :class="toast.type === 'success'
            ? (isDark ? 'bg-emerald-600 text-white' : 'bg-emerald-600 text-white')
            : (isDark ? 'bg-red-600 text-white' : 'bg-red-600 text-white')">
          <svg v-if="toast.type === 'success'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
          {{ toast.message }}
        </div>
      </Transition>
    </Teleport>

    <!-- Confirmation dialog for safety configs -->
    <Teleport to="body">
      <Transition enter-active-class="transition ease-out duration-150" enter-from-class="opacity-0" enter-to-class="opacity-100"
        leave-active-class="transition ease-in duration-100" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="confirmDialog.show" class="fixed inset-0 z-50 flex items-center justify-center">
          <div class="absolute inset-0 bg-black/50" @click="confirmDialog.show = false"></div>
          <div class="relative rounded-2xl border p-6 max-w-md w-full mx-4 shadow-xl"
            :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
            <h3 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Confirm Safety Change</h3>
            <p class="text-sm mt-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              You are modifying a safety-critical configuration. Please review the change carefully.
            </p>
            <div class="mt-4 space-y-2">
              <div class="flex items-center gap-2 text-sm">
                <span class="font-mono font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ confirmDialog.key }}</span>
              </div>
              <div class="grid grid-cols-2 gap-3 mt-3">
                <div class="rounded-lg p-3 border"
                  :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-200'">
                  <div class="text-[10px] uppercase font-semibold mb-1" :class="isDark ? 'text-red-400' : 'text-red-600'">Old value</div>
                  <div class="text-sm font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ String(confirmDialog.oldValue) }}</div>
                </div>
                <div class="rounded-lg p-3 border"
                  :class="isDark ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-emerald-50 border-emerald-200'">
                  <div class="text-[10px] uppercase font-semibold mb-1" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">New value</div>
                  <div class="text-sm font-mono" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ String(confirmDialog.newValue) }}</div>
                </div>
              </div>
            </div>
            <div class="flex items-center justify-end gap-2 mt-6">
              <button @click="confirmDialog.show = false"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                Cancel
              </button>
              <button @click="confirmAndSave"
                :disabled="saving"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-colors bg-red-600 text-white hover:bg-red-700 disabled:opacity-50">
                {{ saving ? 'Saving...' : 'Confirm Change' }}
              </button>
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
import { getConfig, updateConfig } from '@/services/adminApi.js'
import APageHeader from '@/components/admin/APageHeader.vue'
import ATabBar from '@/components/admin/ATabBar.vue'
import AEmptyState from '@/components/admin/AEmptyState.vue'
import { relativeTime as sharedRelativeTime } from '@/components/admin/formatters.js'

const { isDark } = useTheme()

const configs = ref([])
const loading = ref(true)
const searchQuery = ref('')
const activeCategory = ref('all')
const editingKey = ref(null)
const editValue = ref(null)
const saving = ref(false)

const toast = ref({ show: false, message: '', type: 'success' })
const confirmDialog = ref({ show: false, key: '', oldValue: null, newValue: null, cfg: null })

const categories = ['all', 'diagnostics', 'safety', 'routing', 'export', 'system']

const categoryTabs = computed(() =>
  categories.map(cat => ({
    key: cat,
    label: cat.charAt(0).toUpperCase() + cat.slice(1),
    count: cat === 'all'
      ? configs.value.length
      : configs.value.filter(c => c.category === cat).length,
  }))
)

const filteredConfigs = computed(() => {
  let result = configs.value
  if (activeCategory.value !== 'all') {
    result = result.filter(c => c.category === activeCategory.value)
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(c =>
      c.key.toLowerCase().includes(q) || (c.description || '').toLowerCase().includes(q)
    )
  }
  return result
})

async function fetchConfig() {
  loading.value = true
  try {
    const data = await getConfig()
    configs.value = data.config || data.configs || (Array.isArray(data) ? data : [])
  } catch (e) {
    console.error('Failed to fetch config:', e)
    showToast('Failed to load configuration', 'error')
  } finally {
    loading.value = false
  }
}

function startEdit(cfg) {
  editingKey.value = cfg.key
  editValue.value = cfg.type === 'boolean' ? Boolean(cfg.value) : cfg.value
}

function cancelEdit() {
  editingKey.value = null
  editValue.value = null
}

async function saveEdit(cfg) {
  // Safety configs require confirmation
  if (cfg.category === 'safety') {
    confirmDialog.value = {
      show: true,
      key: cfg.key,
      oldValue: cfg.value,
      newValue: editValue.value,
      cfg,
    }
    return
  }
  await performSave(cfg)
}

async function confirmAndSave() {
  const cfg = confirmDialog.value.cfg
  confirmDialog.value.show = false
  await performSave(cfg)
}

async function performSave(cfg) {
  saving.value = true
  const newValue = editValue.value
  const oldValue = cfg.value
  try {
    await updateConfig(cfg.key, newValue)
    // Update local state
    const idx = configs.value.findIndex(c => c.key === cfg.key)
    if (idx !== -1) {
      configs.value[idx] = {
        ...configs.value[idx],
        value: newValue,
        updated_at: new Date().toISOString(),
        updated_by: 'admin',
      }
    }
    editingKey.value = null
    editValue.value = null
    showToast(`Updated ${cfg.key} successfully`, 'success')
  } catch (e) {
    console.error('Failed to update config:', e)
    // Revert
    const idx = configs.value.findIndex(c => c.key === cfg.key)
    if (idx !== -1) {
      configs.value[idx].value = oldValue
    }
    showToast(e.message || 'Failed to save configuration', 'error')
  } finally {
    saving.value = false
  }
}

function showToast(message, type = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => { toast.value.show = false }, 3000)
}

function categoryBadgeClass(category) {
  const map = {
    diagnostics: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-100 text-blue-700',
    safety: isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700',
    routing: isDark.value ? 'bg-purple-500/15 text-purple-400' : 'bg-purple-100 text-purple-700',
    export: isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-700',
    system: isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700',
  }
  return map[category] || (isDark.value ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-500')
}

function formatTime(ts) {
  if (!ts) return ''
  const rel = sharedRelativeTime(ts)
  return rel || ts
}

onMounted(() => fetchConfig())
</script>
