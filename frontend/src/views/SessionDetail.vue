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
            <h1 class="text-lg font-bold leading-tight" :class="isDark ? 'text-white' : 'text-slate-900'">Consultation Report</h1>
            <p class="text-[11px]" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Comprehensive Analysis</p>
          </div>
        </div>

        <!-- Patient Info Bar -->
        <div class="hidden md:flex items-center gap-4 text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'" v-if="session">
          <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-slate-100 border-slate-200'">
            <svg class="w-3.5 h-3.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            <span v-if="session.age">Age: {{ session.age }}</span>
            <span v-if="session.gender" class="ml-1 capitalize">{{ session.gender }}</span>
          </div>
          <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-slate-100 border-slate-200'">
            <svg class="w-3.5 h-3.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            <span>{{ formatDate(session.timestamp) }}</span>
          </div>
          <span v-if="topUrgency" class="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-wider" :class="urgencyClass">{{ topUrgency }}</span>
        </div>

        <div class="flex items-center gap-2">
          <ThemeLangControls />
          <router-link to="/reports" class="flex items-center gap-2 px-4 py-2 text-xs rounded-lg border transition-colors" :class="isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-slate-100 hover:bg-slate-200 border-slate-200 hover:border-slate-300 text-slate-700'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
            Back to Reports
          </router-link>
        </div>
      </div>
    </div>

    <!-- Mobile patient bar -->
    <div v-if="session" class="md:hidden flex items-center justify-between gap-2 px-4 py-2 border-b text-xs" :class="isDark ? 'bg-slate-800/50 border-slate-700/30 text-slate-400' : 'bg-slate-50 border-slate-200 text-slate-500'">
      <div class="flex items-center gap-3">
        <span v-if="session.age">Age: {{ session.age }}</span>
        <span v-if="session.gender" class="capitalize">{{ session.gender }}</span>
        <span>{{ formatDate(session.timestamp) }}</span>
      </div>
      <span v-if="topUrgency" class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase" :class="urgencyClass">{{ topUrgency }}</span>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto px-4 py-6 space-y-6" ref="reportContent">
      <!-- Not found -->
      <div v-if="!session" class="flex flex-col items-center text-center py-20 px-4">
        <div class="w-14 h-14 rounded-2xl flex items-center justify-center mb-5" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
          <svg class="w-7 h-7" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
          </svg>
        </div>
        <h2 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Session Not Found</h2>
        <p class="text-sm mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">This consultation may have been deleted or the link is invalid.</p>
        <p class="text-xs mb-6" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Consultations are stored locally on your device and may be cleared if browser data is deleted.</p>
        <div class="flex gap-3">
          <router-link to="/reports" class="px-4 py-2 rounded-lg text-xs font-medium transition-colors" :class="isDark ? 'bg-slate-800 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">View All Reports</router-link>
          <router-link to="/consult" class="px-4 py-2 rounded-lg text-xs font-medium bg-blue-600 text-white hover:bg-blue-500 transition-colors">Start New Consultation</router-link>
        </div>
      </div>

      <template v-else>
        <!-- Chief Complaint -->
        <div v-if="session.symptoms" class="p-4 rounded-xl border" :class="isDark ? 'bg-slate-800/40 border-slate-700/40' : 'bg-slate-50 border-slate-200'">
          <div class="text-[10px] uppercase font-semibold mb-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Chief Complaint</div>
          <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ session.symptoms }}</p>
        </div>

        <!-- Row 1: Confidence Chart + Agent Performance -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Confidence Chart (2/3) -->
          <div class="lg:col-span-2 rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
            <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Differential Diagnoses Confidence</h2>
            </div>
            <div class="p-5">
              <div v-if="causes.length > 0" class="space-y-3">
                <div v-for="(cause, i) in causes" :key="'chart-'+i" class="flex items-center gap-3">
                  <div class="w-6 text-right text-[10px] font-bold flex-shrink-0" :class="isDark ? 'text-slate-500' : 'text-slate-400'">#{{ i+1 }}</div>
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                      <span class="text-xs font-medium truncate pr-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ cause.cause }}</span>
                      <span class="text-xs font-bold flex-shrink-0" :class="cause.value >= 50 ? 'text-emerald-500' : cause.value >= 20 ? 'text-amber-500' : (isDark ? 'text-slate-400' : 'text-slate-500')">{{ cause.value }}%</span>
                    </div>
                    <div class="w-full h-2.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700/50' : 'bg-slate-100'">
                      <div class="h-full rounded-full transition-all duration-1000 ease-out" :style="{ width: cause.value + '%' }" :class="cause.value >= 50 ? 'bg-emerald-500' : cause.value >= 20 ? 'bg-amber-500' : (isDark ? 'bg-slate-500' : 'bg-slate-300')"></div>
                    </div>
                  </div>
                  <span class="text-[9px] font-semibold uppercase px-1.5 py-0.5 rounded flex-shrink-0" :class="cause.urgency === 'urgent' || cause.urgency === 'emergency' ? (isDark ? 'bg-red-500/20 text-red-400' : 'bg-red-50 text-red-600') : (isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-100 text-slate-500')">{{ cause.urgency }}</span>
                </div>
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
              <div v-for="agent in agentList" :key="agent.name" class="flex items-center gap-3 text-xs">
                <div class="w-2 h-2 rounded-full flex-shrink-0" :style="{ backgroundColor: agent.color }"></div>
                <span class="flex-1 truncate" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ agent.name }}</span>
                <div class="w-20 rounded-full h-1.5" :class="isDark ? 'bg-slate-700/50' : 'bg-slate-200'">
                  <div class="h-1.5 rounded-full transition-all" :style="{ width: agent.barWidth + '%', backgroundColor: agent.color }"></div>
                </div>
                <span class="text-slate-500 w-12 text-right tabular-nums">{{ agent.timeStr }}</span>
              </div>
              <div class="border-t pt-2 mt-3 space-y-1.5" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
                <div class="flex items-center justify-between text-xs">
                  <span class="font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Total Pipeline</span>
                  <span class="font-bold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ formatTime(totalPipelineTime) }}</span>
                </div>
                <div class="flex items-center justify-between text-xs">
                  <span class="font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">AI Cost</span>
                  <span class="font-bold tabular-nums" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">${{ estimatedCost }}</span>
                </div>
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
              v-for="(cause, i) in causes" :key="i"
              :cause="cause" :rank="i + 1"
              :red-flags="i === 0 ? redFlags : []"
              :recommended-tests="i === 0 ? recommendedTests : []"
            />
          </div>
          <div v-if="causes.length === 0" class="text-center py-8 text-slate-500 text-sm">No diagnoses available.</div>
        </div>

        <!-- Row 3: Recommended Tests + Body Systems -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Recommended Tests -->
          <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
            <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
              <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Recommended Tests</h2>
            </div>
            <div class="p-4">
              <div v-if="recommendedTests.length > 0" class="space-y-2">
                <label v-for="(test, i) in recommendedTests" :key="i"
                  class="flex items-start gap-3 p-2.5 rounded-lg cursor-pointer transition-colors group" :class="isDark ? 'hover:bg-slate-700/30' : 'hover:bg-slate-50'">
                  <input type="checkbox" v-model="testChecked[i]" class="mt-0.5 rounded border-slate-600 bg-slate-700 text-blue-500 focus:ring-blue-500/50 focus:ring-offset-0" />
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
                <div v-for="system in bodySystems" :key="system.name"
                  :title="system.full || system.name"
                  class="flex flex-col items-center gap-1.5 p-3 rounded-xl border transition-all cursor-default"
                  :class="system.active
                    ? (isDark ? 'bg-blue-500/10 border-blue-500/30 text-blue-300' : 'bg-blue-50 border-blue-300 text-blue-600')
                    : (isDark ? 'bg-slate-800/30 border-slate-700/30 text-slate-500' : 'bg-slate-50 border-slate-200 text-slate-400')">
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
                <label v-for="(item, i) in actionChecklist" :key="i"
                  class="flex items-start gap-3 p-2.5 rounded-lg cursor-pointer transition-colors group" :class="isDark ? 'hover:bg-slate-700/30' : 'hover:bg-slate-50'">
                  <input type="checkbox" v-model="actionChecked[i]" class="mt-0.5 rounded focus:ring-amber-500/50 focus:ring-offset-0" :class="isDark ? 'border-slate-600 bg-slate-700 text-amber-500' : 'border-slate-300 bg-white text-amber-600'" />
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
              <div class="flex items-center gap-2 mb-4">
                <span class="text-xs font-bold uppercase px-3 py-1.5 rounded-full" :class="safetyStatusClass">{{ safetyStatusLabel }}</span>
              </div>
              <div v-if="safetyWarnings.length > 0" class="space-y-2">
                <div v-for="(warning, i) in safetyWarnings" :key="i"
                  class="flex items-start gap-2.5 p-2.5 bg-red-500/5 border border-red-500/10 rounded-lg">
                  <svg class="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  <span class="text-xs leading-relaxed" :class="isDark ? 'text-red-300' : 'text-red-600'">{{ warning }}</span>
                </div>
              </div>
              <div v-if="redFlags.length > 0" class="mt-3 space-y-2">
                <div class="text-[10px] font-semibold text-red-400 uppercase mb-1">Red Flags</div>
                <div v-for="(flag, i) in redFlags" :key="'rf-'+i" class="flex items-start gap-2 text-xs" :class="isDark ? 'text-red-300' : 'text-red-600'">
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

        <!-- Row 5: Treatment & Dietary -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Treatment Plan -->
          <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
            <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
              <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
              <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Treatment Recommendations</h2>
            </div>
            <div class="p-4">
              <div v-if="medications.length > 0" class="mb-4">
                <div class="text-[10px] font-semibold uppercase mb-2" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Medications</div>
                <div v-for="med in medications" :key="typeof med === 'string' ? med : med.name" class="text-xs mb-2 p-2.5 rounded-lg" :class="isDark ? 'bg-slate-700/30' : 'bg-slate-50'">
                  <div class="font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ typeof med === 'string' ? med : med.name }}</div>
                  <div v-if="med.dose" class="text-[10px] mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ med.dose }} {{ med.frequency ? '— ' + med.frequency : '' }}</div>
                  <div v-if="med.warnings" class="text-[10px] mt-0.5 text-amber-400">&#9888; {{ med.warnings }}</div>
                </div>
              </div>
              <div v-if="lifestyleRecs.length > 0">
                <div class="text-[10px] font-semibold uppercase mb-2" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Lifestyle & Healing</div>
                <ul class="space-y-1.5">
                  <li v-for="rec in lifestyleRecs" :key="rec" class="text-xs flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <span class="text-emerald-400 mt-0.5 flex-shrink-0">&#10003;</span>{{ rec }}
                  </li>
                </ul>
              </div>
              <div v-if="medications.length === 0 && lifestyleRecs.length === 0" class="text-center py-4 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                Treatment details will appear after diagnosis
              </div>
            </div>
          </div>

          <!-- Dietary Recommendations -->
          <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
            <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
              <span class="text-base">&#127957;</span>
              <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Dietary & Healing Guidance</h2>
            </div>
            <div class="p-4">
              <div v-if="dietaryRecs.length > 0" class="space-y-1.5">
                <div v-for="(rec, i) in dietaryRecs" :key="i" class="text-xs flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  <span class="flex-shrink-0 mt-0.5">{{ ['\uD83E\uDD6C','\uD83E\uDED0','\uD83E\uDD5B','\uD83D\uDCA7','\uD83E\uDDD8','\uD83D\uDE34'][i % 6] }}</span>
                  <span>{{ rec }}</span>
                </div>
              </div>
              <div v-else class="space-y-2">
                <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">General healing recommendations:</p>
                <div v-for="(tip, i) in defaultDietaryTips" :key="i" class="text-xs flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  <span class="flex-shrink-0 mt-0.5">{{ tip.icon }}</span>
                  <span>{{ tip.text }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Row 6: Find Nearby Specialists -->
        <div class="rounded-xl overflow-hidden border transition-colors" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
          <div class="px-5 py-3 border-b flex items-center gap-2" :class="isDark ? 'border-slate-700/30' : 'border-slate-200'">
            <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Find Nearby Specialists</h2>
          </div>
          <div class="p-4">
            <!-- Location input -->
            <div class="flex gap-2 mb-3">
              <input v-model="searchZip" @keyup.enter="updateMapSearch" placeholder="Enter zip code or city..."
                class="flex-1 rounded-lg px-3 py-2 text-sm border focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'" />
              <select v-model="selectedSpecForMap" @change="updateMapSearch" class="rounded-lg px-3 py-2 text-xs border" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-700'">
                <option v-for="spec in uniqueSpecialties" :key="spec" :value="spec">{{ spec }}</option>
              </select>
              <button @click="updateMapSearch" class="px-4 py-2 rounded-lg text-xs font-medium bg-blue-600 text-white hover:bg-blue-500 transition-colors">Search</button>
            </div>

            <!-- Map embed -->
            <div class="rounded-lg overflow-hidden mb-4 border" :class="isDark ? 'border-slate-700' : 'border-slate-200'" style="height: 350px">
              <iframe :src="mapSrc" width="100%" height="100%" style="border:0" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>

            <!-- Specialty search links -->
            <div class="flex flex-wrap gap-2">
              <a v-for="spec in uniqueSpecialties" :key="spec"
                :href="'https://www.google.com/maps/search/' + encodeURIComponent(spec + (searchZip ? ' near ' + searchZip : ' near me'))"
                target="_blank" rel="noopener"
                class="inline-flex items-center gap-1.5 text-xs px-3 py-2 rounded-lg border transition-colors"
                :class="isDark ? 'bg-slate-700/50 border-slate-600/50 text-slate-300 hover:bg-blue-500/15 hover:border-blue-500/30 hover:text-blue-300' : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700'">
                <svg class="w-3.5 h-3.5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                {{ spec }}
              </a>
            </div>

            <!-- Doctor Listings -->
            <div class="mt-4">
              <div class="flex items-center justify-between mb-3">
                <h3 class="text-xs font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  <span class="inline-flex items-center gap-1.5">
                    <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    Providers Near You
                  </span>
                </h3>
                <span v-if="doctorResults.length > 0" class="text-[10px] tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ doctorResults.length }} found</span>
              </div>
              <div v-if="doctorsLoading" class="flex items-center justify-center py-8 gap-2">
                <svg class="w-4 h-4 animate-spin text-blue-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Searching NPI Registry...</span>
              </div>
              <div v-else-if="doctorResults.length > 0" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                <div v-for="doc in doctorResults" :key="doc.npi"
                  class="p-3.5 rounded-xl border transition-all group"
                  :class="isDark ? 'bg-slate-700/30 border-slate-600/30 hover:border-blue-500/30 hover:bg-slate-700/50' : 'bg-slate-50 border-slate-200 hover:border-blue-300 hover:bg-blue-50/30'">
                  <div class="flex items-start gap-3">
                    <div class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-bold"
                      :class="isDark ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-100 text-blue-600'">
                      {{ doc.name.split(' ').filter(w => w.length > 1 && w[0] === w[0].toUpperCase()).map(w => w[0]).slice(0, 2).join('') || '?' }}
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="text-sm font-semibold truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ doc.name }}</div>
                      <div class="text-[11px] mt-0.5" :class="isDark ? 'text-blue-400' : 'text-blue-600'">{{ doc.specialty }}</div>
                      <div class="text-[11px] mt-1 whitespace-pre-line leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ doc.address }}</div>
                      <div v-if="doc.phone" class="flex items-center gap-1 mt-1.5">
                        <svg class="w-3 h-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                        <a :href="'tel:' + doc.phone" class="text-[11px] hover:underline" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ formatPhone(doc.phone) }}</a>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center gap-2 mt-3 pt-2.5 border-t" :class="isDark ? 'border-slate-600/20' : 'border-slate-200'">
                    <a :href="'https://www.google.com/maps/search/' + encodeURIComponent(doc.name + ' ' + doc.address.replace(/\\n/g, ' '))"
                      target="_blank" rel="noopener"
                      class="text-[10px] px-2 py-1 rounded-md transition-colors inline-flex items-center gap-1"
                      :class="isDark ? 'bg-slate-600/30 text-slate-300 hover:bg-slate-600/50' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                      Map
                    </a>
                    <a v-if="doc.phone" :href="'tel:' + doc.phone"
                      class="text-[10px] px-2 py-1 rounded-md transition-colors inline-flex items-center gap-1"
                      :class="isDark ? 'bg-blue-500/15 text-blue-300 hover:bg-blue-500/25' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                      Call
                    </a>
                    <a :href="'https://npiregistry.cms.hhs.gov/provider-view/' + doc.npi"
                      target="_blank" rel="noopener"
                      class="text-[10px] px-2 py-1 rounded-md transition-colors inline-flex items-center gap-1 ml-auto"
                      :class="isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-400 hover:text-slate-600'">
                      NPI: {{ doc.npi }}
                      <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                  </div>
                </div>
              </div>
              <div v-else-if="doctorsSearched" class="text-center py-6 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                No providers found. Try a different zip code or specialty.
              </div>
              <div v-else class="text-center py-6 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                Enter a zip code and click Search to find providers.
              </div>
            </div>

            <p class="text-[10px] mt-3" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Provider data from the NPI National Registry (CMS.gov). Always verify credentials and check with your insurance provider.</p>
          </div>
        </div>

        <!-- Chat Transcript -->
        <div v-if="session.chatMessages && session.chatMessages.length">
          <div class="flex items-center gap-2 mb-3">
            <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
            <h2 class="text-sm font-bold uppercase tracking-wide" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Conversation Transcript</h2>
          </div>
          <div class="space-y-2 max-h-[500px] overflow-y-auto pr-2">
            <div v-for="(msg, i) in session.chatMessages" :key="i"
              class="p-3 rounded-lg text-xs leading-relaxed"
              :class="msg.sender === 'user'
                ? (isDark ? 'bg-blue-500/10 border border-blue-500/20 text-blue-200 ml-8' : 'bg-blue-50 border border-blue-200 text-blue-800 ml-8')
                : (isDark ? 'bg-slate-800/60 border border-slate-700/40 text-slate-300 mr-8' : 'bg-slate-50 border border-slate-200 text-slate-600 mr-8')">
              <div class="text-[10px] font-semibold uppercase mb-1" :class="msg.sender === 'user' ? 'text-blue-400' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                {{ msg.sender === 'user' ? 'You' : 'Dr. AI' }}
              </div>
              {{ msg.text }}
            </div>
          </div>
        </div>

        <!-- Bottom Actions -->
        <div class="flex justify-center gap-4 flex-wrap py-4">
          <button @click="exportPdf" :disabled="isExporting"
            class="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:opacity-60 disabled:cursor-wait rounded-xl text-sm font-semibold text-white shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30 transition-all">
            <svg v-if="isExporting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            {{ isExporting ? 'Exporting...' : 'Download PDF' }}
          </button>
          <router-link to="/consult"
            class="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold border transition-all"
            :class="isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-white hover:bg-slate-50 border-slate-300 hover:border-slate-400 text-slate-700'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            New Assessment
          </router-link>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getSession } from '@/services/historyService.js'
import { getProfile } from '@/services/userService.js'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import DiagnosisCard from '@/components/DiagnosisCard.vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
const route = useRoute()
const session = ref(null)
const isExporting = ref(false)
const reportContent = ref(null)

onMounted(() => {
  const id = route.params.id
  if (id) session.value = getSession(id)

  // Pre-fill specialist search location from profile
  const profile = getProfile()
  if (profile.zipCode) {
    searchZip.value = profile.zipCode
  } else if (profile.city) {
    searchZip.value = profile.city + (profile.stateRegion ? ', ' + profile.stateRegion : '')
  }
})

const diagnosisData = computed(() => session.value?.diagnosisResult || {})
const causes = computed(() => diagnosisData.value?.causes || [])
const redFlags = computed(() => diagnosisData.value?.red_flags || diagnosisData.value?.redFlags || [])
const recommendedTests = computed(() => diagnosisData.value?.recommended_tests || diagnosisData.value?.recommendedTests || [])
const safetyWarnings = computed(() => diagnosisData.value?.safety_warnings || diagnosisData.value?.safetyWarnings || [])

const actionChecklist = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  const direct = d.action_checklist || d.actionChecklist || []
  if (direct.length > 0) return direct
  const empathy = d.agent_details?.empathy || {}
  const fromEmpathy = empathy.action_checklist || empathy.actions || empathy.next_steps || empathy.recommendations || []
  if (fromEmpathy.length > 0) return fromEmpathy
  const treatment = d.agent_details?.treatment || {}
  const fromTreatment = treatment.action_items || treatment.action_checklist || treatment.next_steps || []
  if (fromTreatment.length > 0) return fromTreatment
  const items = []
  const tests = d.recommended_tests || d.recommendedTests || []
  if (tests.length > 0) items.push('Schedule recommended diagnostic tests (see Recommended Tests section)')
  const flags = d.red_flags || d.redFlags || []
  flags.forEach(f => items.push('Monitor: ' + f))
  const meds = _extractMedications(d)
  meds.forEach(m => {
    const name = typeof m === 'string' ? m : m.name
    if (name) items.push('Discuss with physician: ' + name)
  })
  if (items.length > 0) {
    items.push('Schedule follow-up appointment with your physician')
    return items
  }
  return []
})

function _extractMedications(d) {
  if (!d) return []
  const direct = d.medications || []
  if (direct.length > 0) return direct
  const treatment = d.agent_details?.treatment || {}
  if (treatment.medications?.length > 0) return treatment.medications
  const plans = treatment.treatment_plans || treatment.treatmentPlans || []
  if (Array.isArray(plans)) {
    for (const plan of plans) {
      if (plan.medications?.length > 0) return plan.medications
      if (plan.pharmacological?.length > 0) return plan.pharmacological
    }
  }
  const stepped = treatment.stepped_care || treatment.steppedCare || {}
  const firstLine = stepped.first_line || stepped.firstLine || {}
  if (firstLine.medications?.length > 0) return firstLine.medications
  return []
}

function _extractLifestyle(d) {
  if (!d) return []
  const direct = d.lifestyle_recommendations || d.lifestyleRecommendations || []
  if (direct.length > 0) return direct
  const treatment = d.agent_details?.treatment || {}
  if (treatment.lifestyle_recommendations?.length > 0) return treatment.lifestyle_recommendations
  if (treatment.lifestyle?.length > 0) return treatment.lifestyle
  const plans = treatment.treatment_plans || treatment.treatmentPlans || []
  if (Array.isArray(plans)) {
    for (const plan of plans) {
      if (plan.lifestyle_recommendations?.length > 0) return plan.lifestyle_recommendations
      if (plan.lifestyle?.length > 0) return plan.lifestyle
      if (plan.conservative?.length > 0) return plan.conservative
    }
  }
  return []
}

const medications = computed(() => _extractMedications(diagnosisData.value))
const lifestyleRecs = computed(() => _extractLifestyle(diagnosisData.value))

const dietaryRecs = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  const direct = d.dietary_recommendations || []
  if (direct.length > 0) return direct
  const treatment = d.agent_details?.treatment || {}
  return treatment.dietary_recommendations || treatment.diet || []
})

const defaultDietaryTips = [
  { icon: '\uD83D\uDCA7', text: 'Stay well hydrated \u2014 aim for 8+ glasses of water daily to support healing' },
  { icon: '\uD83E\uDD6C', text: 'Eat anti-inflammatory foods: leafy greens, berries, fatty fish, nuts, and olive oil' },
  { icon: '\uD83E\uDED0', text: 'Include antioxidant-rich foods: blueberries, tomatoes, spinach, and bell peppers' },
  { icon: '\uD83E\uDD5B', text: 'Ensure adequate protein intake for tissue repair \u2014 lean meats, eggs, legumes, dairy' },
  { icon: '\uD83D\uDE34', text: 'Prioritize 7-9 hours of quality sleep \u2014 critical for immune function and healing' },
  { icon: '\uD83E\uDDD8', text: 'Manage stress through meditation, deep breathing, or gentle exercise' },
]

const topUrgency = computed(() => {
  if (!causes.value.length) return ''
  const u = causes.value.map(c => c.urgency || 'routine')
  if (u.includes('emergency')) return 'emergency'
  if (u.includes('urgent')) return 'urgent'
  if (u.includes('soon')) return 'soon'
  return 'routine'
})

const urgencyClass = computed(() => {
  const u = topUrgency.value
  if (u === 'emergency') return 'bg-red-500/20 text-red-300 border border-red-500/30'
  if (u === 'urgent') return 'bg-red-500/15 text-red-400 border border-red-500/20'
  if (u === 'soon') return 'bg-amber-500/15 text-amber-400 border border-amber-500/20'
  return 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20'
})

// Safety
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

// Agent performance
const agentTimingsData = computed(() => diagnosisData.value?.agent_timings || diagnosisData.value?.agentTimings || {})
const totalPipelineTime = computed(() => diagnosisData.value?.total_time || diagnosisData.value?.totalTime || 0)

const agentColors = {
  'triage': '#3b82f6',
  'diagnostician_and_research': '#8b5cf6',
  'diagnostician': '#6366f1',
  'research': '#10b981',
  'specialist': '#f59e0b',
  'treatment': '#ef4444',
  'safety': '#06b6d4',
  'empathy': '#ec4899',
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
  if (entries.length === 0) return []
  const maxTime = Math.max(...entries.map(([, t]) => t), 1)
  return entries.map(([name, time]) => ({
    name,
    time,
    timeStr: formatTime(time),
    barWidth: Math.round((time / maxTime) * 100),
    color: agentColors[name] || '#64748b'
  }))
})

const estimatedCost = computed(() => {
  const d = diagnosisData.value
  if (!d) return '0.00'
  if (d.estimated_cost != null && d.estimated_cost > 0) return d.estimated_cost.toFixed(2)
  const usage = d.token_usage
  if (usage && usage.total_tokens > 0) {
    const inputCost = (usage.total_input_tokens / 1_000_000) * 3.00
    const outputCost = (usage.total_output_tokens / 1_000_000) * 15.00
    return (inputCost + outputCost).toFixed(2)
  }
  if (d.total_time) return (d.total_time * 0.002).toFixed(2)
  return '0.00'
})

function formatTime(seconds) {
  if (!seconds || seconds === 0) return '--'
  if (seconds < 1) return (seconds * 1000).toFixed(0) + 'ms'
  return seconds.toFixed(1) + 's'
}

function formatDate(ts) {
  try { return new Date(ts).toLocaleString() } catch { return ts }
}

// Body systems
const allBodySystems = [
  { name: 'Heart', icon: '\u2764\uFE0F', keywords: ['heart', 'cardiac', 'cardio', 'chest pain', 'palpitation', 'cardiovascular'] },
  { name: 'Brain', icon: '\uD83E\uDDE0', keywords: ['brain', 'neuro', 'headache', 'migraine', 'dizzy', 'cognitive', 'mental'] },
  { name: 'Lungs', icon: '\uD83E\uDEC1', keywords: ['lung', 'respiratory', 'breath', 'cough', 'pulmonary', 'asthma'] },
  { name: 'Digestive', icon: '\uD83E\uDE79', full: 'Gastrointestinal Tract', keywords: ['stomach', 'digest', 'gastro', 'bowel', 'abdominal', 'nausea', 'gi'] },
  { name: 'Muscles & Joints', icon: '\uD83E\uDDB4', full: 'Musculoskeletal System', keywords: ['muscle', 'joint', 'bone', 'musculoskeletal', 'back', 'arthritis', 'pain'] },
  { name: 'Skin', icon: '\uD83E\uDE7A', keywords: ['skin', 'dermat', 'rash', 'itch', 'eczema', 'psoriasis', 'lip', 'cheilit'] },
  { name: 'Kidneys', icon: '\uD83E\uDEC0', keywords: ['kidney', 'renal', 'urinary', 'bladder'] },
  { name: 'Liver', icon: '\uD83E\uDEDB', keywords: ['liver', 'hepat', 'biliary', 'gallbladder'] },
  { name: 'Endocrine', icon: '\uD83E\uDDEA', keywords: ['thyroid', 'diabetes', 'hormone', 'endocrine', 'adrenal'] },
  { name: 'Immune', icon: '\uD83D\uDEE1\uFE0F', keywords: ['immune', 'autoimmune', 'allergy', 'infection', 'virus', 'bacteria', 'fungal'] },
  { name: 'Eyes', icon: '\uD83D\uDC41\uFE0F', keywords: ['eye', 'vision', 'ophthalm', 'retina'] },
  { name: 'Ear, Nose & Throat', icon: '\uD83D\uDC42', full: 'ENT / Otolaryngology', keywords: ['ear', 'nose', 'throat', 'sinus', 'tonsil'] },
]

const bodySystems = computed(() => {
  const allText = causes.value.map(c =>
    ((c.cause || '') + ' ' + (c.explanation || '') + ' ' + (c.specialty || '')).toLowerCase()
  ).join(' ')
  const testsText = recommendedTests.value.join(' ').toLowerCase()
  const fullText = allText + ' ' + testsText
  return allBodySystems.map(system => ({
    ...system,
    active: system.keywords.some(kw => fullText.includes(kw))
  }))
})

// Specialist search
const uniqueSpecialties = computed(() => {
  const specs = causes.value.map(c => c.specialty).filter(Boolean)
  const allText = causes.value.map(c => ((c.cause || '') + ' ' + (c.specialty || '')).toLowerCase()).join(' ')
  if (allText.includes('skin') || allText.includes('dermat') || allText.includes('cheilit') || allText.includes('lip') || allText.includes('rash') || allText.includes('acne')) {
    specs.push('Dermatologist')
  }
  return [...new Set(specs)].slice(0, 6)
})

const searchZip = ref('')
const selectedSpecForMap = ref('')
const mapSearchQuery = ref('')
const doctorResults = ref([])
const doctorsLoading = ref(false)
const doctorsSearched = ref(false)

function updateMapSearch() {
  const spec = selectedSpecForMap.value || uniqueSpecialties.value[0] || 'doctor'
  const location = searchZip.value.trim() || 'near me'
  mapSearchQuery.value = spec + ' ' + location
  fetchDoctors()
}

async function fetchDoctors() {
  const zip = searchZip.value.trim()
  const spec = selectedSpecForMap.value || uniqueSpecialties.value[0] || 'Primary Care'
  if (!zip) return
  doctorsLoading.value = true
  doctorsSearched.value = true
  try {
    const params = new URLSearchParams({ specialty: spec, location: zip, limit: '12' })
    const resp = await fetch('http://localhost:8000/api/find-doctors?' + params)
    const data = await resp.json()
    doctorResults.value = data.results || []
  } catch (e) {
    console.error('Doctor search failed:', e)
    doctorResults.value = []
  } finally {
    doctorsLoading.value = false
  }
}

function formatPhone(phone) {
  if (!phone) return ''
  const digits = phone.replace(/\D/g, '')
  if (digits.length === 10) return `(${digits.slice(0,3)}) ${digits.slice(3,6)}-${digits.slice(6)}`
  return phone
}

const mapSrc = computed(() => {
  const query = mapSearchQuery.value || (uniqueSpecialties.value[0] || 'doctor') + ' near me'
  return 'https://maps.google.com/maps?q=' + encodeURIComponent(query) + '&output=embed'
})

watch(uniqueSpecialties, (specs) => {
  if (specs.length > 0 && !selectedSpecForMap.value) {
    selectedSpecForMap.value = specs[0]
  }
}, { immediate: true })

// Checkbox state
const testChecked = reactive({})
const actionChecked = reactive({})

// PDF export
async function exportPdf() {
  if (isExporting.value || !reportContent.value) return
  isExporting.value = true
  try {
    const html2pdf = (await import('html2pdf.js')).default
    await html2pdf().set({
      margin: [10, 10, 10, 10],
      filename: `consultation-${route.params.id}.pdf`,
      image: { type: 'jpeg', quality: 0.95 },
      html2canvas: { scale: 2, backgroundColor: isDark.value ? '#0f172a' : '#ffffff' },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    }).from(reportContent.value).save()
  } catch (err) {
    console.error('PDF export failed:', err)
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
