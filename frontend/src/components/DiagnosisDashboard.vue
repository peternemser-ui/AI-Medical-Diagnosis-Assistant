<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-gradient-to-br from-slate-950 via-slate-900 to-gray-900 text-white' : 'bg-gradient-to-br from-slate-50 via-white to-slate-100 text-slate-900'">
    <!-- Header -->
    <div class="backdrop-blur-xl border-b py-3 px-6 shadow-xl transition-colors" :class="isDark ? 'bg-slate-900/95 border-slate-700/50' : 'bg-white/95 border-slate-200'">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
          </div>
          <div>
            <h1 class="text-lg font-bold leading-tight" :class="isDark ? 'text-white' : 'text-slate-900'">Diagnosis Dashboard</h1>
            <p class="text-[11px]" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Comprehensive Analysis</p>
          </div>
        </div>

        <!-- Patient Info Bar -->
        <div class="hidden md:flex items-center gap-4 text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
          <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-slate-100 border-slate-200'">
            <svg class="w-3.5 h-3.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            <span v-if="patientAge">Age: {{ patientAge }}</span>
            <span v-if="patientGender" class="ml-1 capitalize">{{ patientGender }}</span>
          </div>
          <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-slate-100 border-slate-200'">
            <svg class="w-3.5 h-3.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            <span>{{ formattedDate }}</span>
          </div>
          <!-- Urgency badge -->
          <span class="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider"
                :class="urgencyBadgeClass">
            {{ overallUrgency }}
          </span>
        </div>

        <div class="flex items-center gap-2">
          <ThemeLangControls />
          <!-- Back button -->
          <router-link to="/consult" class="flex items-center gap-2 px-4 py-2 text-xs rounded-lg border transition-colors" :class="isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-slate-100 hover:bg-slate-200 border-slate-200 hover:border-slate-300 text-slate-700'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
            Back to Chat
          </router-link>
        </div>
      </div>
    </div>

    <!-- Mobile patient bar -->
    <div class="md:hidden flex items-center justify-between gap-2 px-4 py-2 border-b text-xs" :class="isDark ? 'bg-slate-800/50 border-slate-700/30 text-slate-400' : 'bg-slate-50 border-slate-200 text-slate-500'">
      <div class="flex items-center gap-3">
        <span v-if="patientAge">Age: {{ patientAge }}</span>
        <span v-if="patientGender" class="capitalize">{{ patientGender }}</span>
        <span>{{ formattedDate }}</span>
      </div>
      <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase" :class="urgencyBadgeClass">{{ overallUrgency }}</span>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 py-6 space-y-6">

      <!-- Row 1: Confidence Chart + Agent Performance -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Confidence Chart (2/3) -->
        <div class="lg:col-span-2 bg-slate-800/60 border border-slate-700/50 rounded-xl overflow-hidden">
          <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Differential Diagnoses Confidence</h2>
          </div>
          <div class="p-5">
            <div v-if="causes.length > 0" style="height: 250px; position: relative;">
              <Bar :data="chartData" :options="chartOptions" />
            </div>
            <div v-else class="text-center py-10 text-slate-500 text-sm">No diagnosis data available</div>
          </div>
        </div>

        <!-- Agent Performance Panel (1/3) -->
        <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
          <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
            <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Agent Performance</h2>
          </div>
          <div class="p-4 space-y-2.5">
            <div v-for="agent in agentList" :key="agent.name"
                 class="flex items-center gap-3 text-xs">
              <div class="w-2 h-2 rounded-full flex-shrink-0" :style="{ backgroundColor: agent.color }"></div>
              <span class="flex-1 truncate" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ agent.name }}</span>
              <div class="w-20 rounded-full h-1.5" :class="isDark ? 'bg-slate-700/50' : 'bg-slate-200'">
                <div class="h-1.5 rounded-full transition-all" :style="{ width: agent.barWidth + '%', backgroundColor: agent.color }"></div>
              </div>
              <span class="text-slate-500 w-12 text-right tabular-nums">{{ agent.timeStr }}</span>
            </div>
            <div class="border-t pt-2 mt-3 flex items-center justify-between text-xs" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
              <span class="font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Total Pipeline</span>
              <span class="font-bold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ formatTime(totalPipelineTime) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Row 2: Diagnosis Cards -->
      <div>
        <div class="flex items-center gap-2 mb-3">
          <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Detailed Diagnoses</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          <DiagnosisCard
            v-for="(cause, index) in causes"
            :key="index"
            :cause="cause"
            :rank="index + 1"
            :red-flags="index === 0 ? redFlags : []"
            :recommended-tests="index === 0 ? recommendedTests : []"
          />
        </div>
        <div v-if="causes.length === 0" class="text-center py-8 text-slate-500 text-sm">No diagnoses available.</div>
      </div>

      <!-- Row 3: Recommended Tests + Body System Indicators -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Recommended Tests -->
        <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
          <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
            <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Recommended Tests</h2>
          </div>
          <div class="p-4">
            <div v-if="recommendedTests.length > 0" class="space-y-2">
              <label
                v-for="(test, i) in recommendedTests"
                :key="i"
                class="flex items-start gap-3 p-2.5 rounded-lg cursor-pointer transition-colors group" :class="isDark ? 'hover:bg-slate-700/30' : 'hover:bg-slate-50'"
              >
                <input
                  type="checkbox"
                  v-model="testChecked[i]"
                  class="mt-0.5 rounded border-slate-600 bg-slate-700 text-blue-500 focus:ring-blue-500/50 focus:ring-offset-0"
                />
                <span class="text-xs leading-relaxed" :class="testChecked[i] ? 'line-through text-slate-400' : (isDark ? 'text-slate-300 group-hover:text-slate-200' : 'text-slate-600 group-hover:text-slate-900')">{{ test }}</span>
              </label>
            </div>
            <div v-else class="text-center py-6 text-slate-500 text-sm">No tests recommended</div>
          </div>
        </div>

        <!-- Body System Indicators -->
        <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
          <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
            <svg class="w-4 h-4 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Body Systems</h2>
          </div>
          <div class="p-4">
            <div class="grid grid-cols-3 sm:grid-cols-4 gap-3">
              <div
                v-for="system in bodySystems"
                :key="system.name"
                class="flex flex-col items-center gap-1.5 p-3 rounded-xl border transition-all"
                :class="system.active
                  ? (isDark ? 'bg-blue-500/10 border-blue-500/30 text-blue-300' : 'bg-blue-50 border-blue-300 text-blue-600')
                  : (isDark ? 'bg-slate-800/30 border-slate-700/30 text-slate-500' : 'bg-slate-50 border-slate-200 text-slate-400')"
              >
                <span class="text-2xl">{{ system.icon }}</span>
                <span class="text-[10px] font-medium text-center leading-tight">{{ system.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Row 4: Action Items + Safety Review -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Action Items -->
        <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
          <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
            <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Action Items</h2>
          </div>
          <div class="p-4">
            <div v-if="actionChecklist.length > 0" class="space-y-2">
              <label
                v-for="(item, i) in actionChecklist"
                :key="i"
                class="flex items-start gap-3 p-2.5 rounded-lg cursor-pointer transition-colors group" :class="isDark ? 'hover:bg-slate-700/30' : 'hover:bg-slate-50'"
              >
                <input
                  type="checkbox"
                  v-model="actionChecked[i]"
                  class="mt-0.5 rounded border-slate-600 bg-slate-700 text-amber-500 focus:ring-amber-500/50 focus:ring-offset-0"
                />
                <span class="text-xs leading-relaxed" :class="actionChecked[i] ? 'line-through text-slate-400' : (isDark ? 'text-slate-300 group-hover:text-slate-200' : 'text-slate-600 group-hover:text-slate-900')">{{ item }}</span>
              </label>
            </div>
            <div v-else class="text-center py-6 text-slate-500 text-sm">No action items</div>
          </div>
        </div>

        <!-- Safety Review -->
        <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
          <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
            <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Safety Review</h2>
          </div>
          <div class="p-4">
            <!-- Status badge -->
            <div class="flex items-center gap-2 mb-4">
              <span class="text-xs font-bold uppercase px-3 py-1.5 rounded-full"
                    :class="safetyStatusClass">
                {{ safetyStatusLabel }}
              </span>
            </div>
            <!-- Warnings -->
            <div v-if="safetyWarnings.length > 0" class="space-y-2">
              <div
                v-for="(warning, i) in safetyWarnings"
                :key="i"
                class="flex items-start gap-2.5 p-2.5 bg-red-500/5 border border-red-500/10 rounded-lg"
              >
                <svg class="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                <span class="text-xs text-red-300 leading-relaxed">{{ warning }}</span>
              </div>
            </div>
            <div v-if="redFlags.length > 0" class="mt-3 space-y-2">
              <div class="text-[10px] font-semibold text-red-400 uppercase mb-1">Red Flags</div>
              <div
                v-for="(flag, i) in redFlags"
                :key="'rf-' + i"
                class="flex items-start gap-2 text-xs text-red-300"
              >
                <span class="text-red-500 mt-0.5 flex-shrink-0">!</span>
                <span>{{ flag }}</span>
              </div>
            </div>
            <div v-if="safetyWarnings.length === 0 && redFlags.length === 0" class="text-center py-4 text-slate-500 text-sm">
              No safety concerns identified
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Actions -->
      <div class="flex justify-center gap-4 flex-wrap py-4">
        <button
          @click="downloadReport"
          :disabled="isExporting"
          class="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:opacity-60 disabled:cursor-wait rounded-xl text-sm font-semibold text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30 transition-all"
        >
          <svg v-if="isExporting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          {{ isExporting ? 'Exporting...' : 'Download PDF' }}
        </button>
        <router-link
          to="/consult"
          class="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold border transition-all"
          :class="isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-white hover:bg-slate-50 border-slate-300 hover:border-slate-400 text-slate-700'"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          New Assessment
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import DiagnosisCard from './DiagnosisCard.vue'
import ThemeLangControls from './ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const { isDark } = useTheme()

// Data
const diagnosisData = ref(null)
const reportRef = ref(null)
const isExporting = ref(false)

onMounted(() => {
  loadData()
})

function loadData() {
  try {
    // Primary source: latest_diagnosis_result (full structured response)
    const raw = localStorage.getItem('latest_diagnosis_result')
    if (raw) {
      diagnosisData.value = JSON.parse(raw)
      return
    }
    // Fallback: legacy finalDiagnosis format
    const legacy = localStorage.getItem('finalDiagnosis')
    if (legacy) {
      const parsed = JSON.parse(legacy)
      diagnosisData.value = {
        causes: Array.isArray(parsed) ? parsed.map(d => ({
          cause: d.condition || 'Unknown',
          value: d.confidence || 0,
          urgency: d.urgency || 'routine',
          specialty: d.specialty || 'Primary Care',
          explanation: d.explanation || ''
        })) : [],
        agent_timings: {},
        recommended_tests: [],
        red_flags: [],
        action_checklist: [],
        safety_status: '',
        safety_warnings: []
      }
      return
    }
  } catch (e) {
    console.error('Failed to load diagnosis data:', e)
  }

  // No saved data — load realistic sample case
  diagnosisData.value = getSampleData()
}

function getSampleData() {
  return {
    age: 42,
    gender: 'female',
    date: new Date().toISOString(),
    causes: [
      {
        cause: 'Gastroesophageal Reflux Disease (GERD)',
        value: 78,
        urgency: 'soon',
        specialty: 'Gastroenterology',
        explanation: 'Recurrent substernal burning pain worsening after meals and when lying down, with acid regurgitation. Duration of 3 weeks and response pattern consistent with acid-mediated injury. GERD accounts for ~60% of non-cardiac chest pain presentations in this demographic.'
      },
      {
        cause: 'Costochondritis',
        value: 52,
        urgency: 'routine',
        specialty: 'Rheumatology',
        explanation: 'Reproducible chest wall tenderness on palpation, worsened by deep breathing and certain movements. Common musculoskeletal cause of chest pain in younger patients. Tietze syndrome variant possible given localized swelling reported.'
      },
      {
        cause: 'Anxiety Disorder with Somatic Symptoms',
        value: 41,
        urgency: 'routine',
        specialty: 'Psychiatry',
        explanation: 'Patient reports recent work-related stress, sleep disturbance, and episodes of chest tightness with palpitations not correlated with exertion. PHQ-9 screening suggests moderate anxiety. Somatic symptom disorder should be considered after organic causes are excluded.'
      },
      {
        cause: 'Peptic Ulcer Disease',
        value: 28,
        urgency: 'soon',
        specialty: 'Gastroenterology',
        explanation: 'Epigastric pain with nocturnal symptoms and NSAID use (ibuprofen for back pain). H. pylori prevalence in this population is ~30%. Ulcer cannot be excluded without endoscopy. Alarm features absent but duration warrants investigation.'
      },
      {
        cause: 'Stable Angina Pectoris',
        value: 15,
        urgency: 'urgent',
        specialty: 'Cardiology',
        explanation: 'Low pre-test probability given age, sex, and atypical features (non-exertional, postprandial). However, family history of premature CAD (father, age 55) and dyslipidemia elevate baseline risk. HEART score: 3 (low risk). Cannot be fully excluded without stress testing.'
      }
    ],
    agent_timings: {
      'Symptom Analyzer': 1.2,
      'Medical Diagnostician': 3.8,
      'Specialist Consultant': 2.9,
      'Test Recommender': 1.5,
      'Treatment Planner': 2.1,
      'Safety Checker': 0.8,
      'Empathy Agent': 1.1,
    },
    total_time: 13.4,
    recommended_tests: [
      'Complete Blood Count (CBC) with differential',
      'Comprehensive Metabolic Panel (CMP) including liver function',
      'Lipid panel (total cholesterol, LDL, HDL, triglycerides)',
      'H. pylori stool antigen test or urea breath test',
      'Troponin I — to rule out acute coronary syndrome',
      'ECG (12-lead electrocardiogram) at rest',
      'Upper GI endoscopy (EGD) if symptoms persist beyond 4 weeks',
      'Exercise stress test if cardiac risk factors warrant',
      'Chest X-ray (PA and lateral) to exclude pulmonary pathology',
    ],
    red_flags: [
      'Family history of premature coronary artery disease (father, MI at age 55)',
      'Unintentional weight loss of 4 lbs over 3 weeks — warrants monitoring',
      'Nocturnal symptoms disrupting sleep — possible Barrett\'s esophagus risk',
    ],
    action_checklist: [
      'Schedule appointment with primary care physician within 1 week',
      'Begin empiric PPI trial (omeprazole 20mg daily x 8 weeks) — discuss with physician first',
      'Avoid NSAIDs (ibuprofen) — switch to acetaminophen for back pain',
      'Elevate head of bed 6-8 inches; avoid eating within 3 hours of bedtime',
      'Reduce caffeine, alcohol, and spicy food intake',
      'Track symptoms in a food/symptom diary for 2 weeks',
      'Schedule fasting lipid panel and CBC lab work',
      'If chest pain occurs with exertion, shortness of breath, or radiation to arm/jaw — seek emergency care immediately',
      'Follow up with gastroenterologist if PPI trial does not resolve symptoms',
      'Consider stress management techniques — CBT referral if anxiety persists',
    ],
    safety_status: 'caution',
    safety_warnings: [
      'Cardiac causes not fully excluded — patient should seek immediate emergency care if symptoms change in character (exertional, radiating, associated with dyspnea or diaphoresis)',
      'NSAID use with possible peptic ulcer disease increases GI bleeding risk — discontinue ibuprofen and switch to acetaminophen',
      'PPI therapy should be time-limited (8 weeks) and reassessed — long-term use associated with magnesium deficiency and increased fracture risk',
    ],
  }
}

// Computed
const causes = computed(() => {
  if (!diagnosisData.value) return []
  return diagnosisData.value.causes || []
})

const patientAge = computed(() => diagnosisData.value?.age || diagnosisData.value?.patientAge || '')
const patientGender = computed(() => diagnosisData.value?.gender || diagnosisData.value?.patientGender || '')

const formattedDate = computed(() => {
  const d = diagnosisData.value?.date || diagnosisData.value?.timestamp
  if (d) {
    try { return new Date(d).toLocaleDateString() } catch { /* ignore */ }
  }
  return new Date().toLocaleDateString()
})

const overallUrgency = computed(() => {
  const c = causes.value
  if (c.length === 0) return 'routine'
  const urgencies = c.map(x => x.urgency || 'routine')
  if (urgencies.includes('emergency')) return 'emergency'
  if (urgencies.includes('urgent')) return 'urgent'
  if (urgencies.includes('soon')) return 'soon'
  return 'routine'
})

const urgencyBadgeClass = computed(() => {
  const u = overallUrgency.value
  if (u === 'emergency') return 'bg-red-500/20 text-red-300 border border-red-500/30'
  if (u === 'urgent') return 'bg-red-500/15 text-red-400 border border-red-500/20'
  if (u === 'soon') return 'bg-amber-500/15 text-amber-400 border border-amber-500/20'
  return 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20'
})

const recommendedTests = computed(() => diagnosisData.value?.recommended_tests || diagnosisData.value?.recommendedTests || [])
const redFlags = computed(() => diagnosisData.value?.red_flags || diagnosisData.value?.redFlags || [])
const actionChecklist = computed(() => diagnosisData.value?.action_checklist || diagnosisData.value?.actionChecklist || [])
const safetyWarnings = computed(() => diagnosisData.value?.safety_warnings || diagnosisData.value?.safetyWarnings || [])

const safetyStatus = computed(() => diagnosisData.value?.safety_status || diagnosisData.value?.safetyStatus || '')

const safetyStatusLabel = computed(() => {
  const s = safetyStatus.value.toLowerCase()
  if (s.includes('pass') || s.includes('safe') || s.includes('clear')) return 'PASS'
  if (s.includes('fail') || s.includes('danger') || s.includes('critical')) return 'FAIL'
  if (s.includes('warn') || s.includes('caution')) return 'CAUTION'
  if (safetyWarnings.value.length > 0 || redFlags.value.length > 0) return 'CAUTION'
  return 'PASS'
})

const safetyStatusClass = computed(() => {
  const label = safetyStatusLabel.value
  if (label === 'FAIL') return 'bg-red-500/20 text-red-300'
  if (label === 'CAUTION') return 'bg-amber-500/20 text-amber-300'
  return 'bg-emerald-500/20 text-emerald-300'
})

// Agent timings
const agentTimingsData = computed(() => diagnosisData.value?.agent_timings || diagnosisData.value?.agentTimings || {})

const totalPipelineTime = computed(() => {
  return diagnosisData.value?.total_time || diagnosisData.value?.totalTime || 0
})

const agentColors = {
  'Symptom Analyzer': '#3b82f6',
  'Medical Diagnostician': '#8b5cf6',
  'Specialist Consultant': '#6366f1',
  'Test Recommender': '#10b981',
  'Treatment Planner': '#f59e0b',
  'Safety Checker': '#ef4444',
  'Empathy Agent': '#06b6d4',
}

const agentList = computed(() => {
  const timings = agentTimingsData.value
  const entries = Object.entries(timings)
  if (entries.length === 0) {
    // Default agent list if no timings
    return Object.keys(agentColors).map(name => ({
      name,
      time: 0,
      timeStr: '--',
      barWidth: 0,
      color: agentColors[name] || '#64748b'
    }))
  }

  const maxTime = Math.max(...entries.map(([, t]) => t), 1)

  return entries.map(([name, time]) => ({
    name,
    time,
    timeStr: formatTime(time),
    barWidth: Math.round((time / maxTime) * 100),
    color: agentColors[name] || '#64748b'
  }))
})

function formatTime(seconds) {
  if (!seconds || seconds === 0) return '--'
  if (seconds < 1) return (seconds * 1000).toFixed(0) + 'ms'
  return seconds.toFixed(1) + 's'
}

// Chart data
const chartData = computed(() => {
  const labels = causes.value.map(c => c.cause || c.condition || 'Unknown')
  const values = causes.value.map(c => c.value || c.confidence || 0)
  const colors = values.map(v => {
    if (v >= 70) return 'rgba(16, 185, 129, 0.8)'
    if (v >= 40) return 'rgba(245, 158, 11, 0.8)'
    return 'rgba(100, 116, 139, 0.8)'
  })
  const borderColors = values.map(v => {
    if (v >= 70) return 'rgba(16, 185, 129, 1)'
    if (v >= 40) return 'rgba(245, 158, 11, 1)'
    return 'rgba(100, 116, 139, 1)'
  })

  return {
    labels,
    datasets: [{
      label: 'Confidence %',
      data: values,
      backgroundColor: colors,
      borderColor: borderColors,
      borderWidth: 1,
      borderRadius: 6,
      barThickness: 28
    }]
  }
})

const chartOptions = computed(() => ({
  indexAxis: 'y',
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: isDark.value ? '#1e293b' : '#ffffff',
      titleColor: isDark.value ? '#e2e8f0' : '#1e293b',
      bodyColor: isDark.value ? '#cbd5e1' : '#475569',
      borderColor: isDark.value ? '#334155' : '#e2e8f0',
      borderWidth: 1,
      padding: 10,
      cornerRadius: 8,
      callbacks: {
        label: (ctx) => `Confidence: ${ctx.parsed.x}%`
      }
    }
  },
  scales: {
    x: {
      min: 0,
      max: 100,
      grid: { color: isDark.value ? 'rgba(51, 65, 85, 0.3)' : 'rgba(203, 213, 225, 0.5)' },
      ticks: { color: isDark.value ? '#94a3b8' : '#64748b', callback: (v) => v + '%' }
    },
    y: {
      grid: { display: false },
      ticks: {
        color: isDark.value ? '#cbd5e1' : '#334155',
        font: { size: 11 },
        callback: function(value) {
          const label = this.getLabelForValue(value)
          return label.length > 30 ? label.substring(0, 28) + '...' : label
        }
      }
    }
  }
}))

// Local checkbox state
const testChecked = reactive({})
const actionChecked = reactive({})

// Body systems
const allBodySystems = [
  { name: 'Heart', icon: '\u2764\uFE0F', keywords: ['heart', 'cardiac', 'cardio', 'chest pain', 'palpitation', 'cardiovascular'] },
  { name: 'Brain', icon: '\uD83E\uDDE0', keywords: ['brain', 'neuro', 'headache', 'migraine', 'dizzy', 'cognitive', 'mental'] },
  { name: 'Lungs', icon: '\uD83E\uDEC1', keywords: ['lung', 'respiratory', 'breath', 'cough', 'pulmonary', 'asthma'] },
  { name: 'GI Tract', icon: '\uD83E\uDE79', keywords: ['stomach', 'digest', 'gastro', 'bowel', 'abdominal', 'nausea', 'gi'] },
  { name: 'MSK', icon: '\uD83E\uDDB4', keywords: ['muscle', 'joint', 'bone', 'musculoskeletal', 'back', 'arthritis', 'pain'] },
  { name: 'Skin', icon: '\uD83E\uDE7A', keywords: ['skin', 'dermat', 'rash', 'itch', 'eczema', 'psoriasis'] },
  { name: 'Kidneys', icon: '\uD83E\uDEC0', keywords: ['kidney', 'renal', 'urinary', 'bladder'] },
  { name: 'Liver', icon: '\uD83E\uDEDB', keywords: ['liver', 'hepat', 'biliary', 'gallbladder'] },
  { name: 'Endocrine', icon: '\uD83E\uDDEA', keywords: ['thyroid', 'diabetes', 'hormone', 'endocrine', 'adrenal'] },
  { name: 'Immune', icon: '\uD83D\uDEE1\uFE0F', keywords: ['immune', 'autoimmune', 'allergy', 'infection', 'virus', 'bacteria', 'fungal'] },
  { name: 'Eyes', icon: '\uD83D\uDC41\uFE0F', keywords: ['eye', 'vision', 'ophthalm', 'retina'] },
  { name: 'ENT', icon: '\uD83D\uDC42', keywords: ['ear', 'nose', 'throat', 'sinus', 'tonsil'] },
]

const bodySystems = computed(() => {
  // Determine which systems are relevant based on diagnosis content
  const allText = causes.value.map(c =>
    ((c.cause || '') + ' ' + (c.explanation || '') + ' ' + (c.specialty || '')).toLowerCase()
  ).join(' ')

  // Also include recommended tests text
  const testsText = recommendedTests.value.join(' ').toLowerCase()
  const fullText = allText + ' ' + testsText

  return allBodySystems.map(system => ({
    ...system,
    active: system.keywords.some(kw => fullText.includes(kw))
  }))
})

async function downloadReport() {
  if (isExporting.value) return
  isExporting.value = true

  try {
    const html2pdf = (await import('html2pdf.js')).default
    const { buildPrintReport } = await import('@/services/pdfReport.js')

    const reportHtml = buildPrintReport({
      causes: causes.value,
      redFlags: redFlags.value,
      recommendedTests: recommendedTests.value,
      actionChecklist: actionChecklist.value,
      safetyWarnings: safetyWarnings.value,
      safetyStatusLabel: safetyStatusLabel.value,
      agentList: agentList.value,
      totalPipelineTime: totalPipelineTime.value,
      formatTime,
      patientAge: patientAge.value,
      patientGender: patientGender.value,
      formattedDate: formattedDate.value,
      overallUrgency: overallUrgency.value,
    })

    const container = document.createElement('div')
    container.innerHTML = reportHtml
    document.body.appendChild(container)

    const filename = 'diagnosis-report-' + new Date().toISOString().slice(0, 10) + '.pdf'

    await html2pdf().set({
      margin: [12, 12, 12, 12],
      filename,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true, backgroundColor: '#ffffff', logging: false },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }).from(container.firstChild).save()

    document.body.removeChild(container)
  } catch (err) {
    console.error('PDF export failed:', err)
    alert('PDF export failed. Please try again.')
  } finally {
    isExporting.value = false
  }
}

</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.5);
}
::-webkit-scrollbar-thumb {
  background: rgba(71, 85, 105, 0.6);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(100, 116, 139, 0.7);
}
</style>
