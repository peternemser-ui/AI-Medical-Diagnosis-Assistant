<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <AppNav currentPage="journal" />

    <div class="max-w-4xl mx-auto px-4 py-6 space-y-6">

      <!-- Page Header -->
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center flex-shrink-0 shadow-sm">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Health Journal</h1>
          <p class="text-sm mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Log your daily symptoms to track patterns and share with your doctor</p>
        </div>
      </div>

      <!-- ======= SECTION 1: Daily Check-in ======= -->
      <section class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-700 bg-indigo-900/10' : 'border-slate-200 bg-indigo-50/60'">
          <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">How are you feeling today?</h2>
            <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Log your symptoms and mood for daily tracking</p>
          </div>
        </div>

        <div class="p-6 space-y-6">

          <!-- Mood Selector -->
          <div>
            <label class="text-sm font-semibold block mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Mood</label>
            <div class="flex gap-3 justify-center">
              <button v-for="m in moods" :key="m.value" @click="checkin.mood = m.value"
                class="flex flex-col items-center gap-2 p-3 rounded-xl border-2 transition-all duration-200"
                :class="checkin.mood === m.value
                  ? isDark ? 'border-indigo-500 bg-indigo-900/20 scale-110 shadow-md' : 'border-indigo-500 bg-indigo-50 scale-110 shadow-md'
                  : isDark ? 'border-slate-700 hover:border-slate-600 hover:scale-105' : 'border-slate-200 hover:border-slate-300 hover:scale-105'">
                <span class="text-3xl leading-none">{{ m.emoji }}</span>
                <span class="text-[10px] font-medium"
                  :class="checkin.mood === m.value
                    ? isDark ? 'text-indigo-300' : 'text-indigo-700'
                    : isDark ? 'text-slate-400' : 'text-slate-500'">{{ m.label }}</span>
              </button>
            </div>
          </div>

          <!-- Symptom Tags -->
          <div>
            <label class="text-sm font-semibold block mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Symptoms</label>
            <div class="flex flex-wrap gap-2">
              <button v-for="s in symptomTags" :key="s.value" @click="toggleSymptom(s.value)"
                class="px-3 py-1.5 rounded-lg text-xs font-medium border transition-all duration-200"
                :class="checkin.symptoms.includes(s.value)
                  ? isDark ? 'bg-indigo-900/20 border-indigo-500 text-indigo-300' : 'bg-indigo-50 border-indigo-400 text-indigo-700'
                  : isDark ? 'border-slate-700 text-slate-400 hover:border-slate-600' : 'border-slate-200 text-slate-500 hover:border-slate-400'">
                {{ s.emoji }} {{ s.label }}
              </button>
            </div>
          </div>

          <!-- Severity Slider -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <label class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Overall Severity</label>
              <span class="text-sm font-bold" :class="severityColor">{{ checkin.severity }}/10</span>
            </div>
            <input type="range" min="1" max="10" v-model.number="checkin.severity"
              class="w-full h-2 rounded-full appearance-none cursor-pointer"
              :style="{ background: severityGradient }" />
            <div class="flex justify-between mt-1.5">
              <span class="text-[10px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Mild</span>
              <span class="text-[10px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Severe</span>
            </div>
          </div>

          <!-- Notes Textarea -->
          <div>
            <label class="text-sm font-semibold block mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Notes</label>
            <textarea v-model="checkin.notes" rows="3" placeholder="Any additional details about how you're feeling..."
              class="w-full px-4 py-3 rounded-xl border text-sm transition-colors resize-none"
              :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:border-indigo-500 outline-none' : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400 focus:border-indigo-500 outline-none'">
            </textarea>
          </div>

          <!-- Save Button -->
          <button @click="logEntry" :disabled="!checkin.mood"
            class="w-full py-3 rounded-xl text-sm font-semibold transition-all duration-200 bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm hover:shadow-md disabled:opacity-40 disabled:cursor-not-allowed">
            Save Entry
          </button>
        </div>
      </section>

      <!-- ======= SECTION 2: AI Pattern Detection ======= -->
      <section v-if="aiInsights.length > 0"
        class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-700 bg-amber-900/10' : 'border-slate-200 bg-amber-50/60'">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">AI Insights</h2>
            <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Patterns detected from your journal entries</p>
          </div>
        </div>
        <div class="p-6 space-y-3">
          <div v-for="(insight, idx) in aiInsights" :key="idx"
            class="flex gap-3 p-4 rounded-xl border"
            :class="isDark ? 'bg-slate-800/30 border-slate-700' : 'bg-amber-50/60 border-amber-100'">
            <div class="flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center text-xl"
              :class="isDark ? 'bg-amber-900/20' : 'bg-amber-100'">
              {{ insight.emoji }}
            </div>
            <div>
              <h4 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ insight.title }}</h4>
              <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ insight.description }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ======= SECTION 3: Trend Charts ======= -->
      <section v-if="entries.length >= 2"
        class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-700 bg-cyan-900/10' : 'border-slate-200 bg-cyan-50/60'">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Trends</h2>
            <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Severity and mood trends over time</p>
          </div>
        </div>
        <div class="p-6 space-y-6">
          <!-- Severity trend -->
          <div>
            <h3 class="text-sm font-semibold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Severity Over Time</h3>
            <div class="flex items-end gap-1 h-32">
              <div v-for="(entry, idx) in recentEntries" :key="idx" class="flex-1 flex flex-col items-center gap-1">
                <div class="w-full rounded-t-md transition-all duration-300 min-h-[4px]"
                  :class="entry.severity <= 3 ? 'bg-emerald-500' : entry.severity <= 6 ? 'bg-amber-500' : 'bg-red-500'"
                  :style="{ height: (entry.severity / 10 * 100) + '%' }"></div>
                <span class="text-[8px] truncate w-full text-center" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ formatShortDate(entry.date) }}</span>
              </div>
            </div>
          </div>
          <!-- Mood trend -->
          <div>
            <h3 class="text-sm font-semibold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Mood Trend</h3>
            <div class="flex items-center gap-1">
              <div v-for="(entry, idx) in recentEntries" :key="idx"
                class="flex-1 flex flex-col items-center gap-1 p-1 rounded-lg"
                :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
                <span class="text-lg">{{ getMoodEmoji(entry.mood) }}</span>
                <span class="text-[8px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ formatShortDate(entry.date) }}</span>
              </div>
            </div>
          </div>
          <!-- Symptom frequency -->
          <div>
            <h3 class="text-sm font-semibold mb-3" :class="isDark ? 'text-white' : 'text-slate-900'">Symptom Frequency</h3>
            <div class="space-y-2.5">
              <div v-for="(count, symptom) in symptomFrequency" :key="symptom" class="flex items-center gap-3">
                <span class="text-xs w-24 text-right capitalize" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ symptom }}</span>
                <div class="flex-1 h-2.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'">
                  <div class="h-full rounded-full bg-indigo-500 transition-all duration-500"
                    :style="{ width: (count / entries.length * 100) + '%' }"></div>
                </div>
                <span class="text-xs font-bold w-6 text-right" :class="isDark ? 'text-white' : 'text-slate-900'">{{ count }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ======= SECTION 4: Journal Timeline ======= -->
      <section class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <div class="px-6 py-4 border-b flex items-center justify-between"
          :class="isDark ? 'border-slate-700 bg-indigo-900/10' : 'border-slate-200 bg-indigo-50/60'">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <div>
              <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Journal Timeline</h2>
              <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ entries.length }} entries recorded</p>
            </div>
          </div>
          <!-- Filter -->
          <select v-if="entries.length > 0" v-model="symptomFilter"
            class="text-xs px-3 py-1.5 rounded-lg border transition-colors outline-none"
            :class="isDark ? 'bg-slate-800 border-slate-700 text-slate-300' : 'bg-white border-slate-200 text-slate-600'">
            <option value="">All symptoms</option>
            <option v-for="s in symptomTags" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>
        </div>

        <!-- Timeline entries -->
        <div v-if="filteredEntries.length > 0" class="p-6">
          <div class="relative">
            <!-- Vertical line -->
            <div class="absolute left-5 top-0 bottom-0 w-px" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>

            <div v-for="(entry, idx) in filteredEntries" :key="idx" class="relative pl-12 pb-5 last:pb-0">
              <!-- Severity dot -->
              <div class="absolute left-3.5 top-2 w-3 h-3 rounded-full border-2 z-10"
                :class="entry.severity <= 3
                  ? 'bg-emerald-500 border-emerald-300'
                  : entry.severity <= 6
                    ? 'bg-amber-500 border-amber-300'
                    : 'bg-red-500 border-red-300'"></div>

              <!-- Entry card -->
              <div class="rounded-xl border p-4 cursor-pointer transition-all duration-200 hover:shadow-sm"
                :class="isDark ? 'bg-slate-800/40 border-slate-700 hover:border-slate-600' : 'bg-white border-slate-200 hover:border-slate-300'"
                @click="toggleExpand(idx)">
                <div class="flex items-center justify-between mb-2.5">
                  <div class="flex items-center gap-2.5">
                    <span class="text-xl leading-none">{{ getMoodEmoji(entry.mood) }}</span>
                    <span class="text-xs font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ formatDate(entry.date) }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-bold px-2.5 py-0.5 rounded-lg"
                      :class="entry.severity <= 3
                        ? isDark ? 'bg-emerald-900/20 text-emerald-400' : 'bg-emerald-50 text-emerald-700'
                        : entry.severity <= 6
                          ? isDark ? 'bg-amber-900/20 text-amber-400' : 'bg-amber-50 text-amber-700'
                          : isDark ? 'bg-red-900/20 text-red-400' : 'bg-red-50 text-red-700'">
                      {{ entry.severity }}/10
                    </span>
                    <svg class="w-4 h-4 transition-transform" :class="[expandedEntries[idx] ? 'rotate-180' : '', isDark ? 'text-slate-500' : 'text-slate-400']"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </div>
                </div>

                <!-- Symptom tags -->
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="s in entry.symptoms" :key="s"
                    class="px-2.5 py-0.5 rounded-md text-[10px] font-medium capitalize border"
                    :class="isDark ? 'bg-indigo-900/20 text-indigo-300 border-indigo-800/40' : 'bg-indigo-50 text-indigo-600 border-indigo-100'">
                    {{ getSymptomLabel(s) }}
                  </span>
                  <span v-if="entry.symptoms.length === 0" class="text-[10px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No symptoms logged</span>
                </div>

                <!-- Expanded details -->
                <Transition enter-active-class="transition-all duration-200 ease-out" enter-from-class="max-h-0 opacity-0" enter-to-class="max-h-40 opacity-100" leave-active-class="transition-all duration-150 ease-in" leave-from-class="max-h-40 opacity-100" leave-to-class="max-h-0 opacity-0">
                  <div v-if="expandedEntries[idx]" class="overflow-hidden mt-3 pt-3 border-t"
                    :class="isDark ? 'border-slate-700' : 'border-slate-200'">
                    <p v-if="entry.notes" class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ entry.notes }}</p>
                    <p v-else class="text-xs italic" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No additional notes.</p>
                    <button @click.stop="deleteEntry(idx)" class="mt-2 text-[10px] text-red-500 hover:text-red-400 transition-colors">Delete entry</button>
                  </div>
                </Transition>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else class="p-12 text-center">
          <div class="w-20 h-20 mx-auto mb-5 rounded-2xl flex items-center justify-center"
            :class="isDark ? 'bg-slate-800' : 'bg-indigo-50'">
            <svg class="w-10 h-10" :class="isDark ? 'text-slate-600' : 'text-indigo-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
            </svg>
          </div>
          <h3 class="text-base font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Your health journal is empty</h3>
          <p class="text-sm max-w-sm mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Start logging your daily symptoms above to build a health timeline and unlock AI-powered insights.</p>
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
