<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-violet-600/8' : 'bg-violet-400/12'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-indigo-600/6' : 'bg-indigo-400/10'"></div>
      <div class="absolute top-2/3 left-1/2 w-64 h-64 rounded-full blur-[100px]"
        :class="isDark ? 'bg-blue-600/4' : 'bg-blue-400/8'"></div>
    </div>

    <!-- Nav bar -->
    <AppNav currentPage="journal" />

    <!-- Main content -->
    <div class="relative z-10 max-w-4xl mx-auto px-4 py-6 space-y-6">

      <!-- ======= SECTION 1: Daily Check-in ======= -->
      <section class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-800 bg-violet-500/5' : 'border-slate-200 bg-violet-50/50'">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-[var(--text-primary)]">How are you feeling today?</h2>
            <p class="text-xs text-[var(--text-secondary)]">Log your symptoms and mood for daily tracking</p>
          </div>
        </div>
        <div class="p-6 space-y-5">
          <!-- Mood selector -->
          <div>
            <label class="text-sm font-semibold text-[var(--text-primary)] mb-3 block">Mood</label>
            <div class="flex gap-3 justify-center">
              <button v-for="m in moods" :key="m.value" @click="checkin.mood = m.value"
                class="flex flex-col items-center gap-1 p-3 rounded-xl border transition-all duration-200"
                :class="checkin.mood === m.value
                  ? 'border-violet-500 shadow-lg shadow-violet-500/20 scale-110 ' + (isDark ? 'bg-violet-500/15' : 'bg-violet-50')
                  : isDark ? 'border-slate-700 hover:border-slate-600 hover:bg-slate-800/50' : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'">
                <span class="text-3xl">{{ m.emoji }}</span>
                <span class="text-[10px] font-medium text-[var(--text-secondary)]">{{ m.label }}</span>
              </button>
            </div>
          </div>

          <!-- Symptom tags -->
          <div>
            <label class="text-sm font-semibold text-[var(--text-primary)] mb-2 block">Symptoms</label>
            <div class="flex flex-wrap gap-2">
              <button v-for="s in symptomTags" :key="s.value" @click="toggleSymptom(s.value)"
                class="px-3 py-1.5 rounded-lg text-xs font-medium border transition-all duration-200"
                :class="checkin.symptoms.includes(s.value)
                  ? isDark ? 'bg-indigo-500/20 border-indigo-500/50 text-indigo-300' : 'bg-indigo-50 border-indigo-300 text-indigo-700'
                  : isDark ? 'border-slate-700 text-slate-400 hover:border-slate-600' : 'border-slate-300 text-slate-500 hover:border-slate-400'">
                {{ s.emoji }} {{ s.label }}
              </button>
            </div>
          </div>

          <!-- Severity slider -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-sm font-semibold text-[var(--text-primary)]">Severity</label>
              <span class="text-sm font-bold" :class="severityColor">{{ checkin.severity }}/10</span>
            </div>
            <input type="range" min="1" max="10" v-model.number="checkin.severity"
              class="w-full h-2 rounded-full appearance-none cursor-pointer"
              :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"
              :style="{ background: severityGradient }" />
            <div class="flex justify-between mt-1">
              <span class="text-[10px] text-[var(--text-secondary)]">Mild</span>
              <span class="text-[10px] text-[var(--text-secondary)]">Severe</span>
            </div>
          </div>

          <!-- Notes -->
          <div>
            <label class="text-sm font-semibold text-[var(--text-primary)] mb-2 block">Notes</label>
            <textarea v-model="checkin.notes" rows="3" placeholder="Any additional details about how you're feeling..."
              class="w-full px-4 py-3 rounded-xl border text-sm transition-colors resize-none"
              :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:border-violet-500' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400 focus:border-violet-500'"
              style="outline: none"></textarea>
          </div>

          <!-- Log button -->
          <button @click="logEntry" :disabled="!checkin.mood"
            class="w-full py-3 rounded-xl text-sm font-semibold transition-all duration-200 bg-gradient-to-r from-violet-500 to-purple-600 text-white shadow-lg shadow-violet-500/20 hover:shadow-xl disabled:opacity-40 disabled:cursor-not-allowed">
            Log Entry
          </button>
        </div>
      </section>

      <!-- ======= SECTION 2: AI Pattern Detection ======= -->
      <section v-if="aiInsights.length > 0"
        class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-800 bg-amber-500/5' : 'border-slate-200 bg-amber-50/50'">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-[var(--text-primary)]">AI Insights</h2>
            <p class="text-xs text-[var(--text-secondary)]">Patterns detected from your journal entries</p>
          </div>
        </div>
        <div class="p-6 space-y-3">
          <div v-for="(insight, idx) in aiInsights" :key="idx"
            class="flex gap-3 p-4 rounded-xl border"
            :class="isDark ? 'bg-slate-800/30 border-slate-700' : 'bg-amber-50/50 border-amber-100'">
            <div class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center text-lg"
              :class="isDark ? 'bg-amber-500/10' : 'bg-amber-100'">
              {{ insight.emoji }}
            </div>
            <div>
              <h4 class="text-sm font-semibold text-[var(--text-primary)]">{{ insight.title }}</h4>
              <p class="text-xs mt-0.5 text-[var(--text-secondary)]">{{ insight.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ======= SECTION 3: Trend Charts ======= -->
      <section v-if="entries.length >= 2"
        class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-800 bg-cyan-500/5' : 'border-slate-200 bg-cyan-50/50'">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-[var(--text-primary)]">Trends</h2>
            <p class="text-xs text-[var(--text-secondary)]">Severity and mood trends over time</p>
          </div>
        </div>
        <div class="p-6 space-y-6">
          <!-- Severity trend chart (CSS-based) -->
          <div>
            <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-3">Severity Over Time</h3>
            <div class="flex items-end gap-1 h-32">
              <div v-for="(entry, idx) in recentEntries" :key="idx" class="flex-1 flex flex-col items-center gap-1">
                <div class="w-full rounded-t-md transition-all duration-300 min-h-[4px]"
                  :class="entry.severity <= 3 ? 'bg-emerald-500' : entry.severity <= 6 ? 'bg-amber-500' : 'bg-red-500'"
                  :style="{ height: (entry.severity / 10 * 100) + '%' }"></div>
                <span class="text-[8px] text-[var(--text-secondary)] truncate w-full text-center">{{ formatShortDate(entry.date) }}</span>
              </div>
            </div>
          </div>

          <!-- Mood trend -->
          <div>
            <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-3">Mood Trend</h3>
            <div class="flex items-center gap-1">
              <div v-for="(entry, idx) in recentEntries" :key="idx"
                class="flex-1 flex flex-col items-center gap-1 p-1 rounded-lg"
                :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
                <span class="text-lg">{{ getMoodEmoji(entry.mood) }}</span>
                <span class="text-[8px] text-[var(--text-secondary)]">{{ formatShortDate(entry.date) }}</span>
              </div>
            </div>
          </div>

          <!-- Symptom frequency -->
          <div>
            <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-3">Symptom Frequency</h3>
            <div class="space-y-2">
              <div v-for="(count, symptom) in symptomFrequency" :key="symptom" class="flex items-center gap-3">
                <span class="text-xs w-20 text-right text-[var(--text-secondary)] capitalize">{{ symptom }}</span>
                <div class="flex-1 h-3 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'">
                  <div class="h-full rounded-full bg-gradient-to-r from-violet-500 to-purple-500 transition-all duration-500"
                    :style="{ width: (count / entries.length * 100) + '%' }"></div>
                </div>
                <span class="text-xs font-bold text-[var(--text-primary)] w-6 text-right">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ======= SECTION 4: Journal Timeline ======= -->
      <section class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center justify-between"
          :class="isDark ? 'border-slate-800 bg-indigo-500/5' : 'border-slate-200 bg-indigo-50/50'">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-[var(--text-primary)]">Journal Timeline</h2>
              <p class="text-xs text-[var(--text-secondary)]">{{ entries.length }} entries recorded</p>
            </div>
          </div>
          <!-- Filter dropdown -->
          <select v-if="entries.length > 0" v-model="symptomFilter"
            class="text-xs px-3 py-1.5 rounded-lg border transition-colors"
            :class="isDark ? 'bg-slate-800 border-slate-700 text-slate-300' : 'bg-white border-slate-300 text-slate-600'"
            style="outline: none">
            <option value="">All symptoms</option>
            <option v-for="s in symptomTags" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>
        </div>

        <!-- Timeline entries -->
        <div v-if="filteredEntries.length > 0" class="p-6">
          <div class="relative">
            <!-- Vertical timeline line -->
            <div class="absolute left-5 top-0 bottom-0 w-px"
              :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>

            <div v-for="(entry, idx) in filteredEntries" :key="idx" class="relative pl-12 pb-6 last:pb-0">
              <!-- Timeline dot -->
              <div class="absolute left-3.5 top-1 w-3 h-3 rounded-full border-2 z-10"
                :class="entry.severity <= 3
                  ? 'bg-emerald-500 border-emerald-300'
                  : entry.severity <= 6
                    ? 'bg-amber-500 border-amber-300'
                    : 'bg-red-500 border-red-300'"></div>

              <!-- Entry card -->
              <div class="rounded-xl border p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
                :class="isDark ? 'bg-slate-800/40 border-slate-700 hover:border-slate-600' : 'bg-white border-slate-200 hover:border-slate-300'"
                @click="toggleExpand(idx)">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="text-lg">{{ getMoodEmoji(entry.mood) }}</span>
                    <span class="text-xs font-medium text-[var(--text-secondary)]">{{ formatDate(entry.date) }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-bold px-2 py-0.5 rounded-md"
                      :class="entry.severity <= 3
                        ? isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-600'
                        : entry.severity <= 6
                          ? isDark ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600'
                          : isDark ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600'">
                      {{ entry.severity }}/10
                    </span>
                    <svg class="w-4 h-4 transition-transform text-[var(--text-secondary)]"
                      :class="{ 'rotate-180': expandedEntries[idx] }"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </div>
                </div>
                <!-- Symptom tags -->
                <div class="flex flex-wrap gap-1">
                  <span v-for="s in entry.symptoms" :key="s"
                    class="px-2 py-0.5 rounded-md text-[10px] font-medium capitalize"
                    :class="isDark ? 'bg-indigo-500/10 text-indigo-300 border border-indigo-500/20' : 'bg-indigo-50 text-indigo-600 border border-indigo-100'">
                    {{ getSymptomLabel(s) }}
                  </span>
                </div>
                <!-- Expanded details -->
                <Transition enter-active-class="transition-all duration-200 ease-out" enter-from-class="max-h-0 opacity-0" enter-to-class="max-h-40 opacity-100" leave-active-class="transition-all duration-150 ease-in" leave-from-class="max-h-40 opacity-100" leave-to-class="max-h-0 opacity-0">
                  <div v-if="expandedEntries[idx]" class="overflow-hidden mt-3 pt-3 border-t"
                    :class="isDark ? 'border-slate-700' : 'border-slate-200'">
                    <p v-if="entry.notes" class="text-xs text-[var(--text-secondary)]">{{ entry.notes }}</p>
                    <p v-else class="text-xs italic text-[var(--text-secondary)]">No additional notes.</p>
                    <button @click.stop="deleteEntry(idx)"
                      class="mt-2 text-[10px] text-red-400 hover:text-red-300 transition-colors">Delete entry</button>
                  </div>
                </Transition>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else class="p-12 text-center">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center"
            :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
            <span class="text-3xl">&#x1F4D3;</span>
          </div>
          <h3 class="text-lg font-semibold mb-2 text-[var(--text-primary)]">No Journal Entries</h3>
          <p class="text-sm text-[var(--text-secondary)] max-w-sm mx-auto">Start logging your daily symptoms above to build a health timeline and unlock AI-powered insights.</p>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import AppNav from '@/components/AppNav.vue'

const { isDark } = useTheme()

// ── Mood definitions ──
const moods = [
  { value: 1, emoji: '\u{1F62B}', label: 'Awful' },
  { value: 2, emoji: '\u{1F615}', label: 'Poor' },
  { value: 3, emoji: '\u{1F610}', label: 'Okay' },
  { value: 4, emoji: '\u{1F642}', label: 'Good' },
  { value: 5, emoji: '\u{1F60A}', label: 'Great' },
]

function getMoodEmoji(val) {
  const m = moods.find(m => m.value === val)
  return m ? m.emoji : '\u{1F610}'
}

// ── Symptom tags ──
const symptomTags = [
  { value: 'pain', label: 'Pain', emoji: '\u{1FA79}' },
  { value: 'fatigue', label: 'Fatigue', emoji: '\u{1F634}' },
  { value: 'nausea', label: 'Nausea', emoji: '\u{1F922}' },
  { value: 'headache', label: 'Headache', emoji: '\u{1F915}' },
  { value: 'anxiety', label: 'Anxiety', emoji: '\u{1F630}' },
  { value: 'insomnia', label: 'Insomnia', emoji: '\u{1F4A4}' },
  { value: 'dizziness', label: 'Dizziness', emoji: '\u{1F4AB}' },
  { value: 'cough', label: 'Cough', emoji: '\u{1F637}' },
  { value: 'fever', label: 'Fever', emoji: '\u{1F321}\uFE0F' },
  { value: 'appetite_loss', label: 'Appetite Loss', emoji: '\u{1F37D}\uFE0F' },
  { value: 'muscle_ache', label: 'Muscle Ache', emoji: '\u{1F4AA}' },
  { value: 'brain_fog', label: 'Brain Fog', emoji: '\u{1F32B}\uFE0F' },
]

function getSymptomLabel(val) {
  const s = symptomTags.find(s => s.value === val)
  return s ? s.label : val
}

// ── Check-in state ──
const checkin = reactive({
  mood: null,
  symptoms: [],
  severity: 5,
  notes: '',
})

function toggleSymptom(val) {
  const idx = checkin.symptoms.indexOf(val)
  if (idx >= 0) checkin.symptoms.splice(idx, 1)
  else checkin.symptoms.push(val)
}

const severityColor = computed(() => {
  if (checkin.severity <= 3) return 'text-emerald-500'
  if (checkin.severity <= 6) return 'text-amber-500'
  return 'text-red-500'
})

const severityGradient = computed(() => {
  const pct = ((checkin.severity - 1) / 9) * 100
  return `linear-gradient(to right, #10b981 0%, #f59e0b 50%, #ef4444 100%)`
})

// ── Journal entries ──
const entries = ref([])
const STORAGE_KEY = 'symptom_journal'

onMounted(() => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) entries.value = JSON.parse(raw)
  } catch (_e) { /* ignore */ }
})

function saveEntries() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries.value))
}

function logEntry() {
  if (!checkin.mood) return

  const entry = {
    date: new Date().toISOString(),
    mood: checkin.mood,
    symptoms: [...checkin.symptoms],
    severity: checkin.severity,
    notes: checkin.notes,
  }
  entries.value.unshift(entry)
  saveEntries()

  // Reset form
  checkin.mood = null
  checkin.symptoms = []
  checkin.severity = 5
  checkin.notes = ''
}

function deleteEntry(idx) {
  // Map from filtered index to actual index
  const filtered = filteredEntries.value
  const entry = filtered[idx]
  const realIdx = entries.value.indexOf(entry)
  if (realIdx >= 0) {
    entries.value.splice(realIdx, 1)
    saveEntries()
  }
}

// ── Filter ──
const symptomFilter = ref('')

const filteredEntries = computed(() => {
  if (!symptomFilter.value) return entries.value
  return entries.value.filter(e => e.symptoms.includes(symptomFilter.value))
})

// ── Expanded entries ──
const expandedEntries = reactive({})

function toggleExpand(idx) {
  expandedEntries[idx] = !expandedEntries[idx]
}

// ── Recent entries for charts ──
const recentEntries = computed(() => {
  return [...entries.value].reverse().slice(-14)
})

// ── Symptom frequency ──
const symptomFrequency = computed(() => {
  const freq = {}
  entries.value.forEach(e => {
    e.symptoms.forEach(s => {
      freq[s] = (freq[s] || 0) + 1
    })
  })
  // Sort by frequency descending, take top 8
  const sorted = Object.entries(freq).sort((a, b) => b[1] - a[1]).slice(0, 8)
  return Object.fromEntries(sorted)
})

// ── AI Insights ──
const aiInsights = computed(() => {
  if (entries.value.length < 5) return []

  const insights = []

  // Trend detection: severity going up or down
  const recent5 = entries.value.slice(0, 5)
  const older5 = entries.value.slice(5, 10)
  if (older5.length >= 3) {
    const recentAvg = recent5.reduce((s, e) => s + e.severity, 0) / recent5.length
    const olderAvg = older5.reduce((s, e) => s + e.severity, 0) / older5.length
    if (recentAvg < olderAvg - 1) {
      insights.push({
        emoji: '\u{1F4C9}',
        title: 'Severity Trending Down',
        description: `Your average severity dropped from ${olderAvg.toFixed(1)} to ${recentAvg.toFixed(1)} recently. Your treatment may be working.`,
      })
    } else if (recentAvg > olderAvg + 1) {
      insights.push({
        emoji: '\u{1F4C8}',
        title: 'Severity Trending Up',
        description: `Your average severity increased from ${olderAvg.toFixed(1)} to ${recentAvg.toFixed(1)}. Consider discussing this with your doctor.`,
      })
    }
  }

  // Day-of-week pattern
  const dayMap = {}
  entries.value.forEach(e => {
    const day = new Date(e.date).toLocaleDateString('en-US', { weekday: 'long' })
    if (!dayMap[day]) dayMap[day] = { total: 0, count: 0 }
    dayMap[day].total += e.severity
    dayMap[day].count++
  })
  let worstDay = null
  let worstAvg = 0
  Object.entries(dayMap).forEach(([day, data]) => {
    if (data.count >= 2) {
      const avg = data.total / data.count
      if (avg > worstAvg) {
        worstAvg = avg
        worstDay = day
      }
    }
  })
  if (worstDay && worstAvg > 5) {
    insights.push({
      emoji: '\u{1F4C5}',
      title: `${worstDay}s are Harder`,
      description: `Your symptoms tend to be worse on ${worstDay}s (avg severity ${worstAvg.toFixed(1)}). This could be related to weekly patterns in stress or activity.`,
    })
  }

  // Most common symptom co-occurrence
  if (entries.value.length >= 5) {
    const pairs = {}
    entries.value.forEach(e => {
      for (let i = 0; i < e.symptoms.length; i++) {
        for (let j = i + 1; j < e.symptoms.length; j++) {
          const key = [e.symptoms[i], e.symptoms[j]].sort().join('+')
          pairs[key] = (pairs[key] || 0) + 1
        }
      }
    })
    const topPair = Object.entries(pairs).sort((a, b) => b[1] - a[1])[0]
    if (topPair && topPair[1] >= 3) {
      const [s1, s2] = topPair[0].split('+')
      insights.push({
        emoji: '\u{1F517}',
        title: 'Symptom Correlation',
        description: `${getSymptomLabel(s1)} and ${getSymptomLabel(s2)} appear together in ${topPair[1]} entries. They may be related.`,
      })
    }
  }

  // Mood improvement
  if (recent5.length >= 3 && older5.length >= 3) {
    const recentMoodAvg = recent5.reduce((s, e) => s + e.mood, 0) / recent5.length
    const olderMoodAvg = older5.reduce((s, e) => s + e.mood, 0) / older5.length
    if (recentMoodAvg > olderMoodAvg + 0.5) {
      insights.push({
        emoji: '\u{2728}',
        title: 'Mood Improving',
        description: 'Your overall mood has been trending upward recently. Keep up the positive habits!',
      })
    }
  }

  return insights
})

// ── Date formatting ──
function formatDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function formatShortDate(dateStr) {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>
