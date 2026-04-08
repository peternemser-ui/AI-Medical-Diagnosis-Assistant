<template>
  <div>
    <!-- ── Header ── -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-[var(--text-primary)]">Schedule &amp; Reminders</h1>
        <p class="text-sm mt-1 text-[var(--text-secondary)]">Your daily medication timeline and reminders</p>
      </div>
      <button @click="showReminderModal = true"
        class="flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-semibold bg-indigo-700 hover:bg-indigo-800 text-white transition-all shadow-lg shadow-indigo-700/20">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
        Add Reminder
      </button>
    </div>

    <!-- ── Daily Timeline — Time Slots ── -->
    <div class="mb-8">
      <div class="flex items-center gap-2 mb-4">
        <svg class="w-4 h-4" :class="isDark ? 'text-purple-400' : 'text-purple-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Today's Schedule</h2>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="slot in timeSlots" :key="slot.label"
          class="rounded-2xl border overflow-hidden transition-all hover:shadow-md"
          :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200'">
          <!-- Slot header -->
          <div class="px-4 py-3 border-b flex items-center gap-2.5"
            :class="[slot.headerBg, isDark ? 'border-slate-800' : 'border-slate-100']">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center text-base flex-shrink-0" :class="slot.iconBg">
              {{ slot.emoji }}
            </div>
            <div>
              <h3 class="text-sm font-bold" :class="slot.titleColor">{{ slot.label }}</h3>
              <span class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ slot.time }}</span>
            </div>
          </div>

          <!-- Slot meds -->
          <div class="p-3">
            <div v-if="slot.meds.length === 0" class="flex items-center justify-center py-4">
              <span class="text-xs" :class="isDark ? 'text-slate-600' : 'text-slate-400'">No medications</span>
            </div>

            <div v-else class="space-y-2">
              <div v-for="med in slot.meds" :key="med.name + slot.label"
                class="rounded-xl p-3 border transition-all"
                :class="medStatusClass(med)">
                <!-- Med name + status -->
                <div class="flex items-start justify-between gap-2 mb-1.5">
                  <span class="text-sm font-semibold leading-tight text-[var(--text-primary)]">{{ med.name }}</span>
                  <span class="flex-shrink-0 text-xs px-1.5 py-0.5 rounded-full font-medium" :class="statusBadge(med.status)">{{ med.status }}</span>
                </div>
                <!-- Dosage -->
                <div class="text-xs mb-2.5 px-2 py-0.5 rounded-full inline-block font-medium"
                  :class="isDark ? 'bg-purple-500/10 text-purple-400' : 'bg-purple-50 text-purple-700'">
                  {{ med.dosage }}
                </div>
                <!-- Actions -->
                <div v-if="med.status === 'pending'" class="flex gap-1.5">
                  <button @click="markTaken(med, slot.label)"
                    class="flex-1 py-1.5 rounded-lg text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-white transition-colors">
                    Take
                  </button>
                  <button @click="markSkipped(med, slot.label)"
                    class="flex-1 py-1.5 rounded-lg text-xs font-semibold transition-colors"
                    :class="isDark ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                    Skip
                  </button>
                </div>
                <!-- Completed state indicator -->
                <div v-else class="flex items-center gap-1.5 text-xs"
                  :class="med.status === 'taken' ? (isDark ? 'text-emerald-400' : 'text-emerald-600') : (isDark ? 'text-red-400' : 'text-red-600')">
                  <svg v-if="med.status === 'taken'" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M4.5 12.75l6 6 9-13.5"/>
                  </svg>
                  <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                  {{ med.status === 'taken' ? 'Taken' : 'Skipped' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Weekly Calendar ── -->
    <div class="rounded-2xl border overflow-hidden mb-8"
      :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200'">
      <div class="px-5 py-3.5 border-b flex items-center gap-2"
        :class="isDark ? 'border-slate-800' : 'border-slate-200'">
        <svg class="w-4 h-4" :class="isDark ? 'text-purple-400' : 'text-purple-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
        </svg>
        <h3 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Weekly Overview</h3>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead>
            <tr>
              <th class="p-3 text-left font-semibold sticky left-0 z-10"
                :class="isDark ? 'bg-slate-900 text-slate-400 border-b border-slate-800' : 'bg-slate-50 text-slate-600 border-b border-slate-200'">
                Medication
              </th>
              <th v-for="day in weekDays" :key="day"
                class="p-3 text-center font-semibold border-b"
                :class="[
                  isDark ? 'bg-slate-900 border-slate-800' : 'bg-slate-50 border-slate-200',
                  day === todayName
                    ? (isDark ? 'text-purple-400' : 'text-purple-700')
                    : (isDark ? 'text-slate-400' : 'text-slate-600')
                ]">
                <div class="flex flex-col items-center">
                  <span>{{ day }}</span>
                  <div v-if="day === todayName" class="w-1.5 h-1.5 rounded-full mt-1"
                    :class="isDark ? 'bg-purple-400' : 'bg-purple-600'"></div>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="med in allMeds" :key="med.name" class="border-t"
              :class="isDark ? 'border-slate-800 hover:bg-slate-800/30' : 'border-slate-200 hover:bg-slate-50'">
              <td class="p-3 font-medium sticky left-0 z-10 whitespace-nowrap"
                :class="isDark ? 'bg-slate-900 text-slate-300' : 'bg-white text-slate-700'">
                {{ med.name }}
              </td>
              <td v-for="day in weekDays" :key="day" class="p-3 text-center"
                :class="isDark ? 'bg-slate-900/50' : 'bg-white'">
                <div class="w-7 h-7 rounded-lg mx-auto flex items-center justify-center transition-colors"
                  :class="weekCellClass(med.name, day)">
                  <svg v-if="getWeekStatus(med.name, day) === 'taken'" class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <svg v-else-if="getWeekStatus(med.name, day) === 'skipped'" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                  </svg>
                  <div v-else class="w-2 h-2 rounded-full" :class="isDark ? 'bg-slate-600' : 'bg-slate-300'"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Active Reminders ── -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-white border-slate-200'">
      <div class="px-5 py-3.5 border-b flex items-center justify-between"
        :class="isDark ? 'border-slate-800' : 'border-slate-200'">
        <div class="flex items-center gap-2">
          <svg class="w-4 h-4" :class="isDark ? 'text-purple-400' : 'text-purple-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
          <h3 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Active Reminders</h3>
        </div>
        <span class="text-xs px-2 py-0.5 rounded-full font-medium"
          :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'">
          {{ reminders.length }} set
        </span>
      </div>
      <div class="p-4">
        <div v-if="reminders.length === 0" class="flex flex-col items-center text-center py-8">
          <svg class="w-8 h-8 mb-3" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
          </svg>
          <span class="text-sm text-[var(--text-secondary)]">No reminders set.</span>
          <button @click="showReminderModal = true" class="mt-3 text-xs font-semibold"
            :class="isDark ? 'text-purple-400 hover:text-purple-300' : 'text-purple-600 hover:text-purple-800'">
            Add your first reminder
          </button>
        </div>
        <div v-else class="space-y-2">
          <div v-for="rem in reminders" :key="rem.id"
            class="flex items-center justify-between p-3.5 rounded-xl border transition-colors"
            :class="isDark ? 'border-slate-800 hover:bg-slate-800/40' : 'border-slate-100 hover:bg-slate-50'">
            <div class="flex items-center gap-3">
              <!-- Toggle -->
              <button @click="rem.enabled = !rem.enabled"
                class="relative w-9 h-5 rounded-full transition-colors flex-shrink-0"
                :class="rem.enabled ? 'bg-purple-500' : (isDark ? 'bg-slate-700' : 'bg-slate-300')">
                <div class="absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform"
                  :class="rem.enabled ? 'translate-x-4' : 'translate-x-0.5'"></div>
              </button>
              <div>
                <span class="text-sm font-semibold text-[var(--text-primary)]">{{ rem.medication }}</span>
                <div class="flex items-center gap-2 mt-0.5">
                  <span class="text-xs font-medium" :class="isDark ? 'text-purple-400' : 'text-purple-600'">{{ rem.time }}</span>
                  <span class="text-xs text-[var(--text-secondary)]">&mdash; {{ rem.days.join(', ') }}</span>
                </div>
              </div>
            </div>
            <button @click="removeReminder(rem.id)"
              class="p-1.5 rounded-lg transition-colors text-red-400 hover:bg-red-500/10">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ── Add Reminder Modal ── -->
    <Teleport to="body">
      <div v-if="showReminderModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showReminderModal = false"></div>
        <div class="relative w-full max-w-md rounded-2xl border shadow-2xl p-6"
          :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
          <h2 class="text-lg font-bold mb-5 text-[var(--text-primary)]">Add Reminder</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Medication</label>
              <select v-model="reminderForm.medication"
                class="w-full px-3 py-2.5 rounded-xl border text-sm focus:outline-none"
                :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'">
                <option value="">Select…</option>
                <option v-for="med in allMeds" :key="med.name" :value="med.name">{{ med.name }}</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Time</label>
              <input v-model="reminderForm.time" type="time"
                class="w-full px-3 py-2.5 rounded-xl border text-sm focus:outline-none"
                :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-slate-50 border-slate-200 text-slate-900'" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Days</label>
              <div class="flex flex-wrap gap-2">
                <label v-for="day in allDays" :key="day"
                  class="flex items-center gap-1 px-3 py-1.5 rounded-lg border cursor-pointer text-xs transition-colors"
                  :class="reminderForm.days.includes(day)
                    ? (isDark ? 'bg-purple-500/15 border-purple-500/30 text-purple-300' : 'bg-purple-50 border-purple-200 text-purple-700')
                    : (isDark ? 'border-slate-700 text-slate-400 hover:border-slate-600' : 'border-slate-200 text-slate-600 hover:border-slate-300')">
                  <input type="checkbox" :value="day" v-model="reminderForm.days" class="hidden" />
                  {{ day }}
                </label>
              </div>
            </div>
          </div>
          <div class="flex gap-3 mt-6">
            <button @click="showReminderModal = false"
              class="flex-1 px-4 py-2.5 rounded-xl text-sm font-medium border transition-colors"
              :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-200 text-slate-700 hover:bg-slate-50'">
              Cancel
            </button>
            <button @click="saveReminder" :disabled="!reminderForm.medication || !reminderForm.time"
              class="flex-1 px-4 py-2.5 rounded-xl text-sm font-semibold bg-indigo-700 hover:bg-indigo-800 text-white transition-all disabled:opacity-50">
              Save Reminder
            </button>
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
import { getProfileMedications } from '@/services/profileMedications.js'

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
    {
      label: 'Morning',
      time: '6:00 – 12:00',
      emoji: '\u2600\uFE0F',
      range: [6, 12],
      headerBg: isDark.value ? 'bg-amber-500/5' : 'bg-amber-50',
      iconBg: isDark.value ? 'bg-amber-500/15' : 'bg-amber-100',
      titleColor: isDark.value ? 'text-amber-400' : 'text-amber-700',
    },
    {
      label: 'Afternoon',
      time: '12:00 – 17:00',
      emoji: '\u26C5',
      range: [12, 17],
      headerBg: isDark.value ? 'bg-sky-500/5' : 'bg-sky-50',
      iconBg: isDark.value ? 'bg-sky-500/15' : 'bg-sky-100',
      titleColor: isDark.value ? 'text-sky-400' : 'text-sky-700',
    },
    {
      label: 'Evening',
      time: '17:00 – 21:00',
      emoji: '\uD83C\uDF05',
      range: [17, 21],
      headerBg: isDark.value ? 'bg-orange-500/5' : 'bg-orange-50',
      iconBg: isDark.value ? 'bg-orange-500/15' : 'bg-orange-100',
      titleColor: isDark.value ? 'text-orange-400' : 'text-orange-700',
    },
    {
      label: 'Bedtime',
      time: '21:00+',
      emoji: '\uD83C\uDF19',
      range: [21, 24],
      headerBg: isDark.value ? 'bg-violet-500/5' : 'bg-violet-50',
      iconBg: isDark.value ? 'bg-violet-500/15' : 'bg-violet-100',
      titleColor: isDark.value ? 'text-violet-400' : 'text-violet-700',
    },
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
    default: return isDark.value ? 'bg-slate-800 text-slate-600' : 'bg-slate-100 text-slate-400'
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
    // Fall back to user's profile medications
    const { medications: profileMeds, hasProfile } = getProfileMedications()
    if (hasProfile) {
      const expanded = []
      for (const m of profileMeds) {
        expanded.push({ name: m.name, dosage: m.dosage, scheduleHour: m.scheduleHour || 8 })
        // If twice daily, add a PM dose
        if (m.frequency === 'Twice daily') {
          expanded.push({ name: `${m.name} (PM)`, dosage: m.dosage, scheduleHour: 18 })
        }
      }
      allMeds.value = expanded
    } else {
      allMeds.value = []
    }
  }

  try {
    const data = await getReminders()
    reminders.value = Array.isArray(data) ? data : data.reminders || []
  } catch {
    reminders.value = []
  }
})
</script>
