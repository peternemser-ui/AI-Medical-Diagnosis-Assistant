<template>
  <div>
    <!-- ── Header ── -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-[var(--text-primary)]">My Medications</h1>
        <p class="text-sm mt-1 text-[var(--text-secondary)]">Manage your active and past medications</p>
      </div>
      <button @click="showAddModal = true"
        class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-indigo-700 hover:bg-indigo-800 text-white transition-all shadow-lg shadow-indigo-700/20">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Add Medication
      </button>
    </div>

    <!-- Medications Disclaimer Banner -->
    <div class="flex items-start gap-2.5 rounded-lg p-3 border mb-4"
      :class="isDark ? 'bg-purple-900/15 border-purple-700/40 text-purple-300' : 'bg-purple-50 border-purple-200 text-purple-800'">
      <svg class="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p class="text-xs leading-relaxed">Medication information is for reference only. Always follow your prescribing physician's instructions. Report side effects to your healthcare provider.</p>
    </div>

    <!-- ── Search / Filter bar ── -->
    <div class="flex flex-col sm:flex-row gap-3 mb-6">
      <div class="relative flex-1">
        <svg class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none"
          :class="isDark ? 'text-slate-500' : 'text-slate-400'"
          fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
        <input v-model="searchQuery" placeholder="Search medications…"
          class="w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm transition-colors focus:outline-none focus:ring-2"
          :class="isDark
            ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-500 focus:border-purple-500 focus:ring-purple-500/20'
            : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400 focus:border-purple-400 focus:ring-purple-400/20'" />
      </div>
      <select v-model="filterStatus"
        class="px-4 py-2.5 rounded-xl border text-sm focus:outline-none"
        :class="isDark ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-900'">
        <option value="all">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>

    <!-- ── Loading State ── -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="rounded-2xl p-5 animate-pulse surface-card">
        <div class="h-5 rounded w-2/3 mb-3" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-1/2 mb-2" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-1/3" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
      </div>
    </div>

    <!-- ── Empty State ── -->
    <div v-else-if="filteredMeds.length === 0 && !loading" class="flex flex-col items-center text-center py-16">
      <div class="w-16 h-16 rounded-2xl flex items-center justify-center mb-5"
        :class="isDark ? 'bg-slate-800' : 'bg-purple-50'">
        <svg class="w-8 h-8" :class="isDark ? 'text-slate-600' : 'text-purple-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/>
        </svg>
      </div>
      <h3 class="text-lg font-bold mb-2 text-[var(--text-primary)]">No Medications Added</h3>
      <p class="text-sm mb-6 text-[var(--text-secondary)] max-w-sm">Add your current medications to see food interactions, scheduling, side effects, and more.</p>
      <div class="flex flex-col sm:flex-row items-center justify-center gap-3">
        <router-link to="/profile"
          class="px-5 py-2.5 rounded-xl text-sm font-semibold border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 transition-all"
          :class="isDark ? 'border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700' : ''">
          Add via Profile
        </router-link>
        <button @click="showAddModal = true"
          class="px-5 py-2.5 rounded-xl text-sm font-semibold bg-indigo-700 hover:bg-indigo-800 text-white transition-all">
          Add Manually
        </button>
      </div>
    </div>

    <!-- ── Medication Grid ── -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="med in filteredMeds" :key="med.id"
        class="group relative rounded-2xl border transition-all hover:shadow-lg overflow-hidden"
        :class="[
          !med.active && 'opacity-60',
          isDark ? 'bg-slate-900 border-slate-800 hover:border-slate-700' : 'bg-white border-slate-200 hover:border-slate-300'
        ]">
        <!-- Status stripe top -->
        <div class="h-1 w-full" :class="med.active ? 'bg-emerald-500' : 'bg-slate-400'"></div>

        <div class="p-5">
          <!-- Top row: drug info + toggle -->
          <div class="flex items-start gap-3 mb-4">
            <!-- Adherence ring -->
            <div class="relative w-11 h-11 flex-shrink-0">
              <svg class="w-11 h-11 -rotate-90" viewBox="0 0 36 36">
                <circle cx="18" cy="18" r="15.915" fill="none" :stroke="isDark ? '#334155' : '#e2e8f0'" stroke-width="3"/>
                <circle cx="18" cy="18" r="15.915" fill="none" stroke="url(#adherenceGrad)" stroke-width="3" stroke-linecap="round" :stroke-dasharray="`${(med.adherence || 0)} 100`"/>
                <defs><linearGradient id="adherenceGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#a855f7"/></linearGradient></defs>
              </svg>
              <span class="absolute inset-0 flex items-center justify-center text-[10px] font-bold text-[var(--text-primary)]">{{ med.adherence || 0 }}%</span>
            </div>

            <!-- Name + dosage -->
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-base truncate text-[var(--text-primary)]">{{ med.name }}</h3>
              <div class="flex flex-wrap items-center gap-1.5 mt-1.5">
                <!-- Dosage badge -->
                <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold"
                  :class="isDark ? 'bg-purple-500/15 text-purple-400' : 'bg-purple-50 text-purple-700 border border-purple-200'">
                  {{ med.dosage }}
                </span>
              </div>
            </div>

            <!-- Active toggle -->
            <button @click="toggleActive(med)"
              class="flex-shrink-0 relative w-9 h-5 rounded-full transition-colors"
              :class="med.active ? 'bg-emerald-500' : (isDark ? 'bg-slate-700' : 'bg-slate-300')"
              :title="med.active ? 'Active — click to pause' : 'Paused — click to activate'">
              <div class="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform"
                :class="med.active ? 'translate-x-4' : 'translate-x-0.5'"></div>
            </button>
          </div>

          <!-- Tags row -->
          <div class="flex flex-wrap gap-1.5 mb-3">
            <!-- Frequency -->
            <span v-if="med.frequency" class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
              :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-600'">
              {{ med.frequency }}
            </span>
            <!-- Route -->
            <span v-if="med.route" class="inline-flex items-center text-xs"
              :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              &bull; {{ med.route }}
            </span>
            <!-- Status dot -->
            <span class="inline-flex items-center gap-1 text-xs ml-auto"
              :class="med.active ? (isDark ? 'text-emerald-400' : 'text-emerald-600') : (isDark ? 'text-amber-400' : 'text-amber-600')">
              <span class="w-1.5 h-1.5 rounded-full" :class="med.active ? 'bg-emerald-500' : 'bg-amber-500'"></span>
              {{ med.active ? 'Active' : 'Paused' }}
            </span>
          </div>

          <!-- Prescriber -->
          <div v-if="med.prescriber" class="text-xs mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            Prescribed by {{ med.prescriber }}
          </div>

          <!-- Actions (appear on hover) -->
          <div class="flex gap-2 pt-3 border-t transition-opacity"
            :class="[isDark ? 'border-slate-800' : 'border-slate-100']">
            <button @click="editMed(med)"
              class="flex-1 text-xs py-1.5 rounded-lg font-medium transition-colors border"
              :class="isDark
                ? 'border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800 hover:border-slate-600'
                : 'border-slate-200 text-slate-500 hover:text-slate-900 hover:bg-slate-50'">
              Edit
            </button>
            <button @click="confirmDelete(med)"
              class="flex-1 text-xs py-1.5 rounded-lg font-medium transition-colors border border-transparent text-red-400 hover:bg-red-500/10 hover:border-red-500/20">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Add/Edit Modal ── -->
    <Teleport to="body">
      <div v-if="showAddModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="closeModal"></div>
        <div class="relative w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-2xl shadow-2xl p-6 surface-card">
          <h2 class="text-lg font-bold mb-5 text-[var(--text-primary)]">{{ editingMed ? 'Edit Medication' : 'Add Medication' }}</h2>

          <div class="space-y-4">
            <!-- Name with autocomplete -->
            <div class="relative">
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Medication Name</label>
              <input v-model="form.name" @input="onNameInput" placeholder="e.g., Lisinopril" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'" />
              <div v-if="suggestions.length" class="absolute left-0 right-0 top-full mt-1 rounded-xl border shadow-lg overflow-hidden z-10 max-h-40 overflow-y-auto" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'">
                <button v-for="s in suggestions" :key="s" @click="selectSuggestion(s)" class="w-full text-left px-3 py-2 text-sm transition-colors" :class="isDark ? 'hover:bg-slate-700 text-slate-300' : 'hover:bg-slate-50 text-slate-700'">{{ s }}</button>
              </div>
            </div>

            <!-- Drug Interaction Warnings -->
            <div v-if="interactionWarnings.length > 0" class="rounded-xl border-l-4 p-3 space-y-2"
              :class="interactionWarnings.some(w => w.severity === 'high')
                ? (isDark ? 'bg-red-500/10 border-red-500' : 'bg-red-50 border-red-500')
                : (isDark ? 'bg-amber-500/10 border-amber-500' : 'bg-amber-50 border-amber-500')">
              <div class="flex items-center gap-2 text-sm font-semibold"
                :class="interactionWarnings.some(w => w.severity === 'high') ? 'text-red-500' : 'text-amber-500'">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
                Drug Interaction Warning
              </div>
              <div v-for="(w, idx) in interactionWarnings" :key="idx" class="text-xs leading-relaxed"
                :class="w.severity === 'high' ? 'text-red-400' : (isDark ? 'text-amber-300' : 'text-amber-700')">
                <span class="font-bold uppercase text-[10px] px-1.5 py-0.5 rounded mr-1"
                  :class="w.severity === 'high' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-500'">{{ w.severity }}</span>
                <strong>{{ form.name }}</strong> + <strong>{{ w.existingMed }}</strong>: {{ w.description }}
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Dosage</label>
                <input v-model="form.dosage" placeholder="e.g., 10mg" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'" />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Frequency</label>
                <select v-model="form.frequency" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'">
                  <option value="">Select...</option>
                  <option v-for="f in frequencies" :key="f" :value="f">{{ f }}</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Route</label>
                <select v-model="form.route" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'">
                  <option value="">Select...</option>
                  <option v-for="r in routes" :key="r" :value="r">{{ r }}</option>
                </select>
              </div>
              <div>
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Start Date</label>
                <input v-model="form.startDate" type="date" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Prescriber</label>
                <input v-model="form.prescriber" placeholder="Dr. name" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'" />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Pharmacy</label>
                <input v-model="form.pharmacy" placeholder="Pharmacy name" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'" />
              </div>
            </div>

            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Notes</label>
              <textarea v-model="form.notes" rows="2" placeholder="Any special instructions..." class="w-full px-3 py-2.5 rounded-xl border text-sm resize-none" :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'"></textarea>
            </div>
          </div>

          <div class="flex gap-3 mt-6">
            <button @click="closeModal" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-medium border transition-colors" :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-200 text-slate-700 hover:bg-slate-50'">Cancel</button>
            <button @click="saveMedication" :disabled="!form.name" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-semibold bg-indigo-700 hover:bg-indigo-800 text-white transition-all disabled:opacity-50 disabled:cursor-not-allowed">
              {{ editingMed ? 'Update' : 'Add' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Delete confirmation -->
    <Teleport to="body">
      <div v-if="deletingMed" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="deletingMed = null"></div>
        <div class="relative w-full max-w-sm rounded-2xl shadow-2xl p-6 surface-card">
          <h3 class="text-lg font-bold mb-2 text-[var(--text-primary)]">Delete Medication?</h3>
          <p class="text-sm mb-5 text-[var(--text-secondary)]">Remove <strong>{{ deletingMed.name }}</strong> from your list? This cannot be undone.</p>
          <div class="flex gap-3">
            <button @click="deletingMed = null" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-medium border" :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-200 text-slate-700 hover:bg-slate-50'">Cancel</button>
            <button @click="doDelete" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-semibold bg-red-600 text-white hover:bg-red-500 transition-colors">Delete</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Footer Disclaimer -->
    <p class="text-xs text-slate-400 text-center py-4">For informational purposes only. Not a substitute for professional medical advice.</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getMedications, addMedication, updateMedication, deleteMedication, searchMedications } from '@/services/medicationApi.js'
import { getProfileMedications } from '@/services/profileMedications.js'
import { getAllMedicationNames, checkDrugInteractions } from '@/data/medicationDatabase.js'

const { isDark } = useTheme()
const medications = ref([])
const loading = ref(true)
const searchQuery = ref('')
const filterStatus = ref('all')
const showAddModal = ref(false)
const editingMed = ref(null)
const deletingMed = ref(null)
const suggestions = ref([])
const interactionWarnings = ref([])
let searchTimeout = null

const frequencies = ['Once daily', 'Twice daily', 'Three times daily', 'Four times daily', 'Every 6 hours', 'Every 8 hours', 'Every 12 hours', 'As needed', 'Weekly']
const routes = ['Oral', 'Topical', 'Injection', 'Inhaled', 'Sublingual', 'Rectal', 'Ophthalmic']

const defaultForm = { name: '', dosage: '', frequency: '', route: '', startDate: '', prescriber: '', pharmacy: '', notes: '' }
const form = ref({ ...defaultForm })

const filteredMeds = computed(() => {
  let list = medications.value
  if (filterStatus.value === 'active') list = list.filter(m => m.active)
  else if (filterStatus.value === 'inactive') list = list.filter(m => !m.active)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(m => m.name.toLowerCase().includes(q) || (m.prescriber || '').toLowerCase().includes(q))
  }
  return list
})

async function fetchMedications() {
  loading.value = true
  try {
    const data = await getMedications()
    medications.value = Array.isArray(data) ? data : data.medications || []
  } catch {
    // Use profile medications instead of hardcoded demo data
    const { medications: profileMeds } = getProfileMedications()
    medications.value = profileMeds
  }
  loading.value = false
}

function onNameInput() {
  clearTimeout(searchTimeout)
  checkInteractions()
  if (form.value.name.length < 2) { suggestions.value = []; return }
  searchTimeout = setTimeout(async () => {
    try {
      const data = await searchMedications(form.value.name)
      suggestions.value = (Array.isArray(data) ? data : data.results || []).slice(0, 5)
    } catch {
      suggestions.value = getAllMedicationNames().filter(s => s.toLowerCase().includes(form.value.name.toLowerCase())).slice(0, 5)
    }
  }, 300)
}

function selectSuggestion(s) {
  form.value.name = s
  suggestions.value = []
  checkInteractions()
}

function checkInteractions() {
  if (!form.value.name || form.value.name.length < 2) {
    interactionWarnings.value = []
    return
  }
  const existingMeds = medications.value.filter(m => {
    // Don't check against the medication being edited
    if (editingMed.value && m.id === editingMed.value.id) return false
    return m.active
  })
  interactionWarnings.value = checkDrugInteractions(form.value.name, existingMeds)
}

function editMed(med) {
  editingMed.value = med
  form.value = { name: med.name, dosage: med.dosage, frequency: med.frequency, route: med.route, startDate: med.startDate || '', prescriber: med.prescriber || '', pharmacy: med.pharmacy || '', notes: med.notes || '' }
  showAddModal.value = true
}

function closeModal() {
  showAddModal.value = false
  editingMed.value = null
  form.value = { ...defaultForm }
  suggestions.value = []
  interactionWarnings.value = []
}

async function saveMedication() {
  try {
    if (editingMed.value) {
      await updateMedication(editingMed.value.id, form.value)
      Object.assign(editingMed.value, form.value)
    } else {
      const newMed = { ...form.value, id: Date.now(), active: true, adherence: 0 }
      try { await addMedication(form.value) } catch { /* use local */ }
      medications.value.push(newMed)
    }
  } catch {
    const newMed = { ...form.value, id: Date.now(), active: true, adherence: 0 }
    medications.value.push(newMed)
  }
  closeModal()
}

function toggleActive(med) {
  med.active = !med.active
  try { updateMedication(med.id, { active: med.active }) } catch { /* ignore */ }
}

function confirmDelete(med) { deletingMed.value = med }

async function doDelete() {
  const med = deletingMed.value
  try { await deleteMedication(med.id) } catch { /* ignore */ }
  medications.value = medications.value.filter(m => m.id !== med.id)
  deletingMed.value = null
}

onMounted(fetchMedications)
</script>
