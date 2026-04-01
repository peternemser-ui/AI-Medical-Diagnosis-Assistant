<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Schedule & Reminders</h1>
        <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Track your daily medication schedule</p>
      </div>
      <button @click="showReminderModal = true" class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-blue-600 to-cyan-600 text-white hover:from-blue-500 hover:to-cyan-500 transition-all shadow-lg shadow-blue-500/25">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Add Reminder
      </button>
    </div>

    <!-- Daily Timeline -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div v-for="slot in timeSlots" :key="slot.label" class="rounded-2xl border p-4" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
        <div class="flex items-center gap-2 mb-3">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" :class="slot.bgClass">
            <span class="text-sm">{{ slot.emoji }}</span>
          </div>
          <div>
            <h3 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ slot.label }}</h3>
            <span class="text-detail" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ slot.time }}</span>
          </div>
        </div>

        <div v-if="slot.meds.length === 0" class="text-center py-4">
          <span class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">No medications</span>
        </div>

        <div v-else class="space-y-2">
          <div v-for="med in slot.meds" :key="med.name + slot.label" class="rounded-xl p-3 border transition-all" :class="medStatusClass(med)">
            <div class="flex items-center justify-between mb-1">
              <span class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ med.name }}</span>
              <span class="text-detail px-1.5 py-0.5 rounded-full font-medium" :class="statusBadge(med.status)">{{ med.status }}</span>
            </div>
            <div class="text-xs mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ med.dosage }}</div>
            <div v-if="med.status === 'pending'" class="flex gap-2">
              <button @click="markTaken(med, slot.label)" class="flex-1 text-caption py-1.5 rounded-lg font-semibold bg-emerald-500 text-white hover:bg-emerald-400 transition-colors">Take</button>
              <button @click="markSkipped(med, slot.label)" class="flex-1 text-caption py-1.5 rounded-lg font-semibold transition-colors" :class="isDark ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">Skip</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Weekly Calendar -->
    <div class="rounded-2xl border overflow-hidden mb-8" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
      <div class="p-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
        <h3 class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Weekly Overview</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr>
              <th class="p-3 text-left font-semibold sticky left-0 z-10" :class="isDark ? 'bg-slate-900 text-slate-400' : 'bg-slate-50 text-slate-600'">Medication</th>
              <th v-for="day in weekDays" :key="day" class="p-3 text-center font-semibold" :class="[isDark ? 'bg-slate-900 text-slate-400' : 'bg-slate-50 text-slate-600', day === todayName ? (isDark ? 'text-violet-400' : 'text-violet-600') : '']">
                {{ day }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="med in allMeds" :key="med.name" class="border-t" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
              <td class="p-3 font-medium sticky left-0 z-10 whitespace-nowrap" :class="isDark ? 'bg-slate-900 text-slate-300' : 'bg-white text-slate-700'">{{ med.name }}</td>
              <td v-for="day in weekDays" :key="day" class="p-3 text-center" :class="isDark ? 'bg-slate-900/50' : 'bg-white'">
                <div class="w-6 h-6 rounded-full mx-auto flex items-center justify-center" :class="weekCellClass(med.name, day)">
                  <svg v-if="getWeekStatus(med.name, day) === 'taken'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
                  <svg v-else-if="getWeekStatus(med.name, day) === 'skipped'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
                  <div v-else class="w-2 h-2 rounded-full" :class="isDark ? 'bg-slate-600' : 'bg-slate-300'"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Active Reminders -->
    <div class="rounded-2xl border p-5" :class="isDark ? 'bg-slate-900/50 border-slate-800' : 'bg-white border-slate-200'">
      <h3 class="font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Active Reminders</h3>
      <div v-if="reminders.length === 0" class="text-center py-8">
        <span class="text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No reminders set. Add one to stay on track.</span>
      </div>
      <div v-else class="space-y-2">
        <div v-for="rem in reminders" :key="rem.id" class="flex items-center justify-between p-3 rounded-xl border" :class="isDark ? 'border-slate-800 hover:bg-slate-800/50' : 'border-slate-100 hover:bg-slate-50'">
          <div class="flex items-center gap-3">
            <button @click="rem.enabled = !rem.enabled" class="relative w-10 h-5 rounded-full transition-colors" :class="rem.enabled ? 'bg-blue-500' : (isDark ? 'bg-slate-700' : 'bg-slate-300')">
              <div class="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform" :class="rem.enabled ? 'translate-x-5' : 'translate-x-0.5'"></div>
            </button>
            <div>
              <span class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ rem.medication }}</span>
              <span class="text-xs ml-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ rem.time }} - {{ rem.days.join(', ') }}</span>
            </div>
          </div>
          <button @click="removeReminder(rem.id)" class="p-1.5 rounded-lg transition-colors text-red-400 hover:bg-red-500/10">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Add Reminder Modal -->
    <Teleport to="body">
      <div v-if="showReminderModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showReminderModal = false"></div>
        <div class="relative w-full max-w-md rounded-2xl border shadow-2xl p-6" :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
          <h2 class="text-lg font-bold mb-5" :class="isDark ? 'text-white' : 'text-slate-900'">Add Reminder</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Medication</label>
              <select v-model="reminderForm.medication" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'">
                <option value="">Select...</option>
                <option v-for="med in allMeds" :key="med.name" :value="med.name">{{ med.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Time</label>
              <input v-model="reminderForm.time" type="time" class="w-full px-3 py-2.5 rounded-xl border text-sm" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Days</label>
              <div class="flex flex-wrap gap-2">
                <label v-for="day in allDays" :key="day" class="flex items-center gap-1 px-3 py-1.5 rounded-lg border cursor-pointer text-xs transition-colors" :class="reminderForm.days.includes(day) ? (isDark ? 'bg-blue-500/15 border-blue-500/30 text-blue-300' : 'bg-blue-50 border-blue-200 text-blue-700') : (isDark ? 'border-slate-700 text-slate-400' : 'border-slate-200 text-slate-600')">
                  <input type="checkbox" :value="day" v-model="reminderForm.days" class="hidden" />
                  {{ day }}
                </label>
              </div>
            </div>
          </div>
          <div class="flex gap-3 mt-6">
            <button @click="showReminderModal = false" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-medium border" :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-200 text-slate-700 hover:bg-slate-50'">Cancel</button>
            <button @click="saveReminder" :disabled="!reminderForm.medication || !reminderForm.time" class="flex-1 px-4 py-2.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-blue-600 to-cyan-600 text-white hover:from-blue-500 hover:to-cyan-500 transition-all disabled:opacity-50">Save</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getMedications, getReminders, addReminder, deleteReminder, logAdherence } from '@/services/medicationApi.js'

const { isDark } = useTheme()
const allMeds = ref([])
const reminders = ref([])
const showReminderModal = ref(false)
const adherenceLog = ref({})

const allDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
const weekDays = allDays
const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const todayName = dayNames[new Date().getDay()]

const reminderForm = ref({ medication: '', time: '08:00', days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] })

const timeSlots = computed(() => {
  const slots = [
    { label: 'Morning', time: '6:00 - 12:00', emoji: '\u2600\uFE0F', bgClass: isDark.value ? 'bg-amber-500/15' : 'bg-amber-50', range: [6, 12] },
    { label: 'Afternoon', time: '12:00 - 17:00', emoji: '\u26C5', bgClass: isDark.value ? 'bg-blue-500/15' : 'bg-blue-50', range: [12, 17] },
    { label: 'Evening', time: '17:00 - 21:00', emoji: '\uD83C\uDF05', bgClass: isDark.value ? 'bg-orange-500/15' : 'bg-orange-50', range: [17, 21] },
    { label: 'Bedtime', time: '21:00+', emoji: '\uD83C\uDF19', bgClass: isDark.value ? 'bg-violet-500/15' : 'bg-violet-50', range: [21, 24] },
  ]
  return slots.map(s => ({
    ...s,
    meds: allMeds.value.filter(m => {
      const h = m.scheduleHour || 8
      return h >= s.range[0] && h < s.range[1]
    }).map(m => ({
      ...m,
      status: adherenceLog.value[m.name + '_' + s.label] || 'pending'
    }))
  }))
})

function medStatusClass(med) {
  switch (med.status) {
    case 'taken': return isDark.value ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-emerald-200 bg-emerald-50'
    case 'skipped': return isDark.value ? 'border-red-500/30 bg-red-500/5' : 'border-red-200 bg-red-50'
    case 'late': return isDark.value ? 'border-amber-500/30 bg-amber-500/5' : 'border-amber-200 bg-amber-50'
    default: return isDark.value ? 'border-slate-700 bg-slate-800/50' : 'border-slate-200 bg-slate-50'
  }
}

function statusBadge(status) {
  switch (status) {
    case 'taken': return isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-600'
    case 'skipped': return isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-600'
    case 'late': return isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-100 text-amber-600'
    default: return isDark.value ? 'bg-slate-700 text-slate-400' : 'bg-slate-200 text-slate-500'
  }
}

function markTaken(med, slot) {
  adherenceLog.value[med.name + '_' + slot] = 'taken'
  try { logAdherence({ medication: med.name, slot, status: 'taken', date: new Date().toISOString() }) } catch { /* local */ }
}

function markSkipped(med, slot) {
  adherenceLog.value[med.name + '_' + slot] = 'skipped'
  try { logAdherence({ medication: med.name, slot, status: 'skipped', date: new Date().toISOString() }) } catch { /* local */ }
}

function getWeekStatus(medName, day) {
  if (day === todayName) return adherenceLog.value[medName + '_Morning'] || adherenceLog.value[medName + '_Afternoon'] || 'pending'
  // Random demo data for past days
  const dayIndex = allDays.indexOf(day)
  const todayIndex = allDays.indexOf(todayName)
  if (dayIndex < todayIndex) {
    const hash = (medName.length * 7 + dayIndex * 13) % 10
    return hash > 2 ? 'taken' : 'skipped'
  }
  return 'pending'
}

function weekCellClass(medName, day) {
  const status = getWeekStatus(medName, day)
  switch (status) {
    case 'taken': return isDark.value ? 'bg-emerald-500/20 text-emerald-400' : 'bg-emerald-100 text-emerald-600'
    case 'skipped': return isDark.value ? 'bg-red-500/20 text-red-400' : 'bg-red-100 text-red-600'
    default: return isDark.value ? 'bg-slate-800' : 'bg-slate-100'
  }
}

async function saveReminder() {
  const rem = { id: Date.now(), ...reminderForm.value, enabled: true }
  try { await addReminder(rem) } catch { /* local */ }
  reminders.value.push(rem)
  showReminderModal.value = false
  reminderForm.value = { medication: '', time: '08:00', days: [...allDays] }
}

async function removeReminder(id) {
  try { await deleteReminder(id) } catch { /* local */ }
  reminders.value = reminders.value.filter(r => r.id !== id)
}

onMounted(async () => {
  try {
    const data = await getMedications()
    const meds = Array.isArray(data) ? data : data.medications || []
    allMeds.value = meds.map(m => ({ ...m, scheduleHour: m.scheduleHour || (m.frequency === 'Twice daily' ? 8 : m.frequency === 'Once daily' ? 8 : 8) }))
  } catch {
    allMeds.value = [
      { name: 'Lisinopril', dosage: '10mg', scheduleHour: 8 },
      { name: 'Metformin', dosage: '500mg', scheduleHour: 8 },
      { name: 'Metformin (PM)', dosage: '500mg', scheduleHour: 18 },
      { name: 'Atorvastatin', dosage: '20mg', scheduleHour: 21 },
    ]
  }

  try {
    const data = await getReminders()
    reminders.value = Array.isArray(data) ? data : data.reminders || []
  } catch {
    reminders.value = [
      { id: 1, medication: 'Lisinopril', time: '08:00', days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], enabled: true },
      { id: 2, medication: 'Metformin', time: '08:00', days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], enabled: true },
      { id: 3, medication: 'Atorvastatin', time: '21:00', days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], enabled: true },
    ]
  }
})
</script>
