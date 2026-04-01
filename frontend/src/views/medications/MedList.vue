<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-[var(--text-primary)]">My Medications</h1>
        <p class="text-sm mt-1 text-[var(--text-secondary)]">Manage your active and past medications</p>
      </div>
      <button @click="showAddModal = true" class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500 transition-all shadow-lg shadow-violet-500/25">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Add Medication
      </button>
    </div>

    <!-- Search / Filter bar -->
    <div class="flex flex-col sm:flex-row gap-3 mb-6">
      <div class="relative flex-1">
        <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input v-model="searchQuery" placeholder="Search medications..." class="w-full pl-10 pr-4 py-2.5 rounded-xl border text-sm transition-colors" :class="isDark ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-500 focus:border-violet-500' : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400 focus:border-violet-500'" />
      </div>
      <select v-model="filterStatus" class="px-4 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-900 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-900'">
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="rounded-2xl p-5 animate-pulse surface-card">
        <div class="h-5 rounded w-2/3 mb-3" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-1/2 mb-2" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
        <div class="h-4 rounded w-1/3" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredMeds.length === 0 && !loading" class="text-center py-20">
      <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center surface-soft">
        <svg class="w-10 h-10" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/></svg>
      </div>
      <h3 class="text-lg font-semibold mb-2 text-[var(--text-primary)]">No medications yet</h3>
      <p class="text-sm mb-6 text-[var(--text-secondary)]">Add your first medication to start tracking dosages, interactions, and reminders.</p>
      <button @click="showAddModal = true" class="px-5 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500 transition-all">
        Add Your First Medication
      </button>
    </div>

    <!-- Medication Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="med in filteredMeds" :key="med.id" class="rounded-2xl p-5 transition-all hover:shadow-lg group relative surface-card" :class="[!med.active && 'opacity-60']">
        <!-- Active toggle -->
        <div class="absolute top-4 right-4 flex items-center gap-2">
          <button @click="toggleActive(med)" class="relative w-10 h-5 rounded-full transition-colors" :class="med.active ? 'bg-violet-500' : (isDark ? 'bg-slate-700' : 'bg-slate-300')">
            <div class="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform" :class="med.active ? 'translate-x-5' : 'translate-x-0.5'"></div>
          </button>
        </div>

        <!-- Content -->
        <div class="flex items-start gap-3 mb-3">
          <!-- Adherence ring -->
          <div class="relative w-12 h-12 flex-shrink-0">
            <svg class="w-12 h-12 -rotate-90" viewBox="0 0 36 36">
              <circle cx="18" cy="18" r="15.915" fill="none" :stroke="isDark ? '#334155' : '#e2e8f0'" stroke-width="3"/>
              <circle cx="18" cy="18" r="15.915" fill="none" stroke="url(#adherenceGrad)" stroke-width="3" stroke-linecap="round" :stroke-dasharray="`${(med.adherence || 0)} 100`"/>
              <defs><linearGradient id="adherenceGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#8b5cf6"/><stop offset="100%" stop-color="#a855f7"/></linearGradient></defs>
            </svg>
            <span class="absolute inset-0 flex items-center justify-center text-detail font-bold text-[var(--text-primary)]">{{ med.adherence || 0 }}%</span>
          </div>
          <div class="min-w-0">
            <h3 class="font-bold text-base truncate text-[var(--text-primary)]">{{ med.name }}</h3>
            <span class="inline-block px-2 py-0.5 rounded-full text-caption font-semibold mt-1" :class="isDark ? 'bg-violet-500/15 text-violet-300' : 'bg-violet-100 text-violet-700'">{{ med.dosage }}</span>
          </div>
        </div>

        <div class="flex flex-wrap gap-1.5 mb-3">
          <span class="px-2 py-0.5 rounded-full text-caption font-medium" :class="isDark ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-600'">{{ med.frequency }}</span>
          <span class="px-2 py-0.5 rounded-full text-caption font-medium" :class="isDark ? 'bg-emerald-500/10 text-emerald-400' : 'bg-emerald-50 text-emerald-600'">{{ med.route }}</span>
        </div>

        <div v-if="med.prescriber" class="text-xs mb-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          Prescribed by {{ med.prescriber }}
        </div>

        <!-- Actions -->
        <div class="flex gap-2 pt-2 border-t" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <button @click="editMed(med)" class="flex-1 text-xs py-1.5 rounded-lg font-medium transition-colors" :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">Edit</button>
          <button @click="confirmDelete(med)" class="flex-1 text-xs py-1.5 rounded-lg font-medium transition-colors text-red-400 hover:bg-red-500/10">Delete</button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
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
            <button @click="saveMedication" :disabled="!form.name" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-violet-600 to-purple-600 text-white hover:from-violet-500 hover:to-purple-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getMedications, addMedication, updateMedication, deleteMedication, searchMedications } from '@/services/medicationApi.js'

const { isDark } = useTheme()
const medications = ref([])
const loading = ref(true)
const searchQuery = ref('')
const filterStatus = ref('all')
const showAddModal = ref(false)
const editingMed = ref(null)
const deletingMed = ref(null)
const suggestions = ref([])
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
    // Use demo data if API not available
    medications.value = [
      { id: 1, name: 'Lisinopril', dosage: '10mg', frequency: 'Once daily', route: 'Oral', prescriber: 'Dr. Smith', pharmacy: 'CVS Pharmacy', active: true, adherence: 92, startDate: '2025-01-15', notes: '' },
      { id: 2, name: 'Metformin', dosage: '500mg', frequency: 'Twice daily', route: 'Oral', prescriber: 'Dr. Johnson', pharmacy: 'Walgreens', active: true, adherence: 78, startDate: '2024-11-01', notes: 'Take with food' },
      { id: 3, name: 'Atorvastatin', dosage: '20mg', frequency: 'Once daily', route: 'Oral', prescriber: 'Dr. Smith', pharmacy: 'CVS Pharmacy', active: true, adherence: 95, startDate: '2024-06-15', notes: 'Take at bedtime' },
      { id: 4, name: 'Albuterol', dosage: '90mcg', frequency: 'As needed', route: 'Inhaled', prescriber: 'Dr. Patel', pharmacy: 'Rite Aid', active: false, adherence: 45, startDate: '2024-03-20', notes: '' },
    ]
  }
  loading.value = false
}

function onNameInput() {
  clearTimeout(searchTimeout)
  if (form.value.name.length < 2) { suggestions.value = []; return }
  searchTimeout = setTimeout(async () => {
    try {
      const data = await searchMedications(form.value.name)
      suggestions.value = (Array.isArray(data) ? data : data.results || []).slice(0, 5)
    } catch {
      suggestions.value = ['Lisinopril', 'Losartan', 'Lipitor', 'Levothyroxine', 'Lexapro'].filter(s => s.toLowerCase().includes(form.value.name.toLowerCase()))
    }
  }, 300)
}

function selectSuggestion(s) {
  form.value.name = s
  suggestions.value = []
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
