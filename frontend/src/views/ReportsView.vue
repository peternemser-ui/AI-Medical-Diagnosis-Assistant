<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-blue-600/5' : 'bg-blue-400/10'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-purple-600/5' : 'bg-purple-400/10'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="relative z-20 flex items-center justify-between px-6 py-3 border-b backdrop-blur-xl"
      style="background: color-mix(in srgb, var(--clinical-surface) 85%, transparent); border-color: var(--clinical-border)">
      <div class="flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <span class="text-sm font-semibold hidden sm:inline text-[var(--text-primary)]">Medical AI</span>
        </router-link>
        <div class="w-px h-5 hidden sm:block bg-[var(--clinical-border)]"></div>
        <span class="text-sm font-medium hidden sm:inline text-[var(--text-secondary)]">Reports</span>
      </div>
      <div class="flex items-center gap-2">
        <ThemeLangControls />
        <router-link to="/" class="p-1.5 rounded-lg transition-colors"
          :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </router-link>
      </div>
    </nav>

    <!-- Main content -->
    <div class="relative z-10 max-w-5xl mx-auto px-4 py-6">
      <!-- Header with stats -->
      <!-- Health Score Summary -->
      <div v-if="allSessions.length > 0" class="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        <div class="rounded-card p-3 text-center surface-card">
          <div class="text-heading font-bold text-[var(--text-primary)]">{{ allSessions.length }}</div>
          <div class="text-detail text-[var(--text-secondary)]">Consultations</div>
        </div>
        <div class="rounded-card p-3 text-center surface-card">
          <div class="text-heading font-bold" :class="avgConfidence >= 70 ? 'text-emerald-500' : avgConfidence >= 40 ? 'text-amber-500' : 'text-slate-400'">{{ avgConfidence }}%</div>
          <div class="text-detail text-[var(--text-secondary)]">Avg Confidence</div>
        </div>
        <div class="rounded-card p-3 text-center surface-card">
          <div class="text-heading font-bold" :class="routineCount === allSessions.length ? 'text-emerald-500' : 'text-amber-500'">{{ routineCount }}/{{ allSessions.length }}</div>
          <div class="text-detail text-[var(--text-secondary)]">Routine</div>
        </div>
        <div class="rounded-card p-3 text-center surface-card">
          <div class="text-heading font-bold text-blue-500">{{ healthScore }}</div>
          <div class="text-detail text-[var(--text-secondary)]">Health Score</div>
        </div>
      </div>

      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h1 class="text-2xl font-bold text-[var(--text-primary)]">Consultation Reports</h1>
          <div class="flex items-center gap-4 mt-1">
            <span class="text-xs text-[var(--text-secondary)]">
              {{ allSessions.length }} total consultation{{ allSessions.length !== 1 ? 's' : '' }}
            </span>
            <span v-if="allSessions.length > 0" class="text-xs text-[var(--text-secondary)]">
              Latest: {{ formatDate(allSessions[0]?.timestamp) }}
            </span>
          </div>
        </div>
        <div class="flex items-center gap-2 self-start">
          <button v-if="allSessions.length >= 2" @click="toggleCompareMode"
            class="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-medium border transition-colors"
            :class="compareMode
              ? (isDark ? 'border-blue-500 text-blue-300 bg-blue-500/15' : 'border-blue-400 text-blue-600 bg-blue-50')
              : (isDark ? 'border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800' : 'border-slate-300 text-slate-500 hover:text-slate-900 hover:bg-slate-100')">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>
            </svg>
            {{ compareMode ? 'Cancel Compare' : 'Compare Diagnoses' }}
          </button>
          <button v-if="allSessions.length > 0" @click="exportAllJson"
            class="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-medium border transition-colors"
            :class="isDark
              ? 'border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800'
              : 'border-slate-300 text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
            </svg>
            Export All as JSON
          </button>
        </div>
      </div>

      <!-- View toggle + Search -->
      <div class="flex items-center gap-3 mb-5">
        <div class="flex rounded-lg border overflow-hidden flex-shrink-0"
          :class="isDark ? 'border-slate-700' : 'border-slate-200'">
          <button @click="viewMode = 'list'"
            class="px-3 py-2 text-detail font-medium transition-colors flex items-center gap-1.5"
            :class="viewMode === 'list'
              ? (isDark ? 'bg-blue-500/15 text-blue-300' : 'bg-blue-50 text-blue-600')
              : (isDark ? 'text-slate-400 hover:bg-slate-800' : 'text-slate-500 hover:bg-slate-50')">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
            List
          </button>
          <button @click="viewMode = 'timeline'"
            class="px-3 py-2 text-detail font-medium transition-colors flex items-center gap-1.5"
            :class="viewMode === 'timeline'
              ? (isDark ? 'bg-blue-500/15 text-blue-300' : 'bg-blue-50 text-blue-600')
              : (isDark ? 'text-slate-400 hover:bg-slate-800' : 'text-slate-500 hover:bg-slate-50')">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Timeline
          </button>
        </div>
        <div class="relative flex-1">
          <svg class="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            v-model="searchQuery"
            placeholder="Search consultations..."
            class="w-full rounded-xl pl-10 pr-4 py-3 text-sm border focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
            :class="isDark
              ? 'bg-slate-900/80 border-slate-800 text-white placeholder-slate-600'
              : 'bg-white border-slate-200 text-slate-900 placeholder-slate-400'"
          />
        </div>
      </div>

      <!-- Compare mode action bar -->
      <div v-if="compareMode" class="mb-5 p-3 rounded-xl border flex items-center justify-between"
        :class="isDark ? 'bg-blue-500/5 border-blue-500/20' : 'bg-blue-50 border-blue-200'">
        <span class="text-sm" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
          <span v-if="selectedForCompare.length === 0">Select 2 consultations to compare</span>
          <span v-else-if="selectedForCompare.length === 1">Select 1 more consultation</span>
          <span v-else class="font-medium" :class="isDark ? 'text-blue-300' : 'text-blue-600'">2 selected — ready to compare</span>
        </span>
        <button
          :disabled="selectedForCompare.length !== 2"
          @click="showComparisonPanel = true"
          class="px-4 py-2 rounded-xl text-xs font-semibold transition-colors"
          :class="selectedForCompare.length === 2
            ? 'bg-blue-600 text-white hover:bg-blue-500 shadow-lg shadow-blue-500/25'
            : (isDark ? 'bg-slate-800 text-slate-600 cursor-not-allowed' : 'bg-slate-200 text-slate-400 cursor-not-allowed')">
          Compare Selected
        </button>
      </div>

      <!-- Comparison Panel Modal -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="showComparisonPanel" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" @click.self="showComparisonPanel = false">
          <div class="surface-card rounded-2xl shadow-2xl max-w-4xl w-full max-h-[85vh] overflow-y-auto">
            <!-- Header -->
            <div class="sticky top-0 z-10 flex items-center justify-between p-5 border-b backdrop-blur-xl"
              :class="isDark ? 'bg-slate-900/95 border-slate-800' : 'bg-white/95 border-slate-200'">
              <div>
                <h3 class="text-lg font-bold text-[var(--text-primary)]">Diagnosis Comparison</h3>
                <p class="text-xs mt-0.5 text-[var(--text-secondary)]">Side-by-side analysis of two consultations</p>
              </div>
              <button @click="showComparisonPanel = false"
                class="p-2 rounded-lg transition-colors"
                :class="isDark ? 'hover:bg-slate-800 text-slate-400' : 'hover:bg-slate-100 text-slate-500'">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- Side by side content -->
            <div class="p-5" v-if="comparisonData">
              <div class="grid grid-cols-2 gap-4 mb-6">
                <!-- Left session -->
                <div class="rounded-xl p-4 border" :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
                  <div class="text-xs font-bold uppercase tracking-wide mb-2" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Session A</div>
                  <div class="text-xs mb-1 text-[var(--text-secondary)]">{{ comparisonData.left.date }}</div>
                  <div class="text-sm font-semibold text-[var(--text-primary)] mb-2">{{ comparisonData.left.summary }}</div>
                  <div class="space-y-2">
                    <div>
                      <span class="text-detail text-[var(--text-secondary)]">Top Diagnosis</span>
                      <p class="text-sm font-medium text-[var(--text-primary)]">{{ comparisonData.left.topDiagnosis }}</p>
                    </div>
                    <div class="flex gap-4">
                      <div>
                        <span class="text-detail text-[var(--text-secondary)]">Confidence</span>
                        <p class="text-sm font-bold" :class="confidenceColor(comparisonData.left.confidence)">{{ comparisonData.left.confidence }}%</p>
                      </div>
                      <div>
                        <span class="text-detail text-[var(--text-secondary)]">Urgency</span>
                        <p class="text-sm font-bold">
                          <span class="px-2 py-0.5 rounded-full text-detail uppercase" :class="urgencyClass(comparisonData.left.urgency)">{{ comparisonData.left.urgency }}</span>
                        </p>
                      </div>
                    </div>
                    <div v-if="comparisonData.left.symptoms">
                      <span class="text-detail text-[var(--text-secondary)]">Symptoms</span>
                      <p class="text-xs text-[var(--text-primary)] mt-0.5">{{ comparisonData.left.symptoms }}</p>
                    </div>
                  </div>
                </div>

                <!-- Right session -->
                <div class="rounded-xl p-4 border" :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
                  <div class="text-xs font-bold uppercase tracking-wide mb-2" :class="isDark ? 'text-purple-400' : 'text-purple-600'">Session B</div>
                  <div class="text-xs mb-1 text-[var(--text-secondary)]">{{ comparisonData.right.date }}</div>
                  <div class="text-sm font-semibold text-[var(--text-primary)] mb-2">{{ comparisonData.right.summary }}</div>
                  <div class="space-y-2">
                    <div>
                      <span class="text-detail text-[var(--text-secondary)]">Top Diagnosis</span>
                      <p class="text-sm font-medium text-[var(--text-primary)]">{{ comparisonData.right.topDiagnosis }}</p>
                    </div>
                    <div class="flex gap-4">
                      <div>
                        <span class="text-detail text-[var(--text-secondary)]">Confidence</span>
                        <p class="text-sm font-bold" :class="confidenceColor(comparisonData.right.confidence)">{{ comparisonData.right.confidence }}%</p>
                      </div>
                      <div>
                        <span class="text-detail text-[var(--text-secondary)]">Urgency</span>
                        <p class="text-sm font-bold">
                          <span class="px-2 py-0.5 rounded-full text-detail uppercase" :class="urgencyClass(comparisonData.right.urgency)">{{ comparisonData.right.urgency }}</span>
                        </p>
                      </div>
                    </div>
                    <div v-if="comparisonData.right.symptoms">
                      <span class="text-detail text-[var(--text-secondary)]">Symptoms</span>
                      <p class="text-xs text-[var(--text-primary)] mt-0.5">{{ comparisonData.right.symptoms }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Diff analysis -->
              <div class="space-y-4">
                <!-- Common findings -->
                <div v-if="comparisonData.common.length > 0" class="rounded-xl p-4 border"
                  :class="isDark ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-emerald-50 border-emerald-200'">
                  <h4 class="text-sm font-bold mb-2 flex items-center gap-2" :class="isDark ? 'text-emerald-400' : 'text-emerald-700'">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.5 12.75l6 6 9-13.5"/></svg>
                    Common Findings
                  </h4>
                  <ul class="space-y-1">
                    <li v-for="(item, i) in comparisonData.common" :key="i" class="text-xs" :class="isDark ? 'text-emerald-300' : 'text-emerald-700'">
                      {{ item }}
                    </li>
                  </ul>
                </div>

                <!-- Differences -->
                <div v-if="comparisonData.differences.length > 0" class="rounded-xl p-4 border"
                  :class="isDark ? 'bg-amber-500/5 border-amber-500/20' : 'bg-amber-50 border-amber-200'">
                  <h4 class="text-sm font-bold mb-2 flex items-center gap-2" :class="isDark ? 'text-amber-400' : 'text-amber-700'">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/></svg>
                    Key Differences
                  </h4>
                  <ul class="space-y-1">
                    <li v-for="(item, i) in comparisonData.differences" :key="i" class="text-xs" :class="isDark ? 'text-amber-300' : 'text-amber-700'">
                      {{ item }}
                    </li>
                  </ul>
                </div>

                <!-- Changes summary -->
                <div class="rounded-xl p-4 border"
                  :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
                  <h4 class="text-sm font-bold mb-2 text-[var(--text-primary)] flex items-center gap-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z"/></svg>
                    Changes Since Last Visit
                  </h4>
                  <p class="text-xs leading-relaxed text-[var(--text-secondary)]">{{ comparisonData.changesSummary }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Empty state -->
      <div v-if="filteredSessions.length === 0" class="flex flex-col items-center justify-center py-20 text-center">
        <svg class="w-16 h-16 mb-4" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <h2 class="text-lg font-semibold mb-2 text-[var(--text-primary)]">
          {{ allSessions.length === 0 ? 'No consultations yet' : 'No matching results' }}
        </h2>
        <p class="text-sm mb-6 text-[var(--text-secondary)]">
          {{ allSessions.length === 0 ? 'Start your first consultation to see reports here.' : 'Try adjusting your search term.' }}
        </p>
        <router-link v-if="allSessions.length === 0" to="/consult"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-medium bg-blue-600 hover:bg-blue-500 text-white transition-colors">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          Start First Consultation
        </router-link>
      </div>

      <!-- Timeline view -->
      <div v-else-if="viewMode === 'timeline' && filteredSessions.length > 0" class="relative">
        <div v-for="(group, monthKey) in groupedByMonth" :key="monthKey" class="mb-8">
          <!-- Month header -->
          <div class="flex items-center gap-3 mb-4">
            <div class="w-3 h-3 rounded-full flex-shrink-0" :class="isDark ? 'bg-blue-400' : 'bg-blue-500'"></div>
            <h3 class="text-body-sm font-bold text-[var(--text-primary)]">{{ monthKey }}</h3>
            <div class="flex-1 h-px" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
            <span class="text-detail text-[var(--text-secondary)]">{{ group.length }} consultation{{ group.length > 1 ? 's' : '' }}</span>
          </div>
          <!-- Timeline cards -->
          <div class="ml-1.5 border-l-2 pl-6 space-y-4" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
            <div v-for="session in group" :key="session.id"
              class="relative surface-card rounded-xl p-4 cursor-pointer transition-all hover:shadow-elevated"
              :class="compareMode && isSelectedForCompare(session.id) ? (isDark ? 'ring-2 ring-blue-500/50' : 'ring-2 ring-blue-400/50') : ''"
              @click="compareMode ? toggleCompareSelection(session.id) : $router.push(`/reports/${session.id}`)">
              <!-- Timeline dot -->
              <div class="absolute -left-[1.85rem] top-5 w-2.5 h-2.5 rounded-full border-2"
                :class="isDark ? 'bg-slate-900 border-slate-600' : 'bg-white border-slate-300'"></div>
              <!-- Content -->
              <div class="flex items-start justify-between gap-3">
                <!-- Compare checkbox -->
                <div v-if="compareMode" class="flex-shrink-0 pt-1" @click.stop="toggleCompareSelection(session.id)">
                  <div class="w-5 h-5 rounded-md border-2 flex items-center justify-center transition-colors"
                    :class="isSelectedForCompare(session.id)
                      ? 'bg-blue-600 border-blue-600'
                      : (isDark ? 'border-slate-600 hover:border-slate-400' : 'border-slate-300 hover:border-slate-500')">
                    <svg v-if="isSelectedForCompare(session.id)" class="w-3 h-3 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/>
                    </svg>
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1 flex-wrap">
                    <span class="text-detail font-medium text-[var(--text-secondary)]">{{ formatDate(session.timestamp) }}</span>
                    <span class="px-2 py-0.5 rounded-full text-detail font-bold uppercase tracking-wide" :class="urgencyClass(session.urgency)">{{ session.urgency }}</span>
                  </div>
                  <p class="text-sm font-medium text-[var(--text-primary)] mb-1">{{ getSessionSummary(session.id) }}</p>
                  <div class="flex items-center gap-2 text-detail text-[var(--text-secondary)]">
                    <span>{{ session.topDiagnosis }}</span>
                    <span v-if="session.confidence" class="font-semibold"
                      :class="session.confidence >= 70 ? 'text-emerald-400' : session.confidence >= 40 ? 'text-amber-400' : 'text-slate-400'">
                      {{ session.confidence }}%
                    </span>
                  </div>
                </div>
                <svg class="w-4 h-4 flex-shrink-0 mt-1" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Session cards (list view) -->
      <div v-else-if="filteredSessions.length > 0" class="space-y-3">
        <div
          v-for="session in filteredSessions"
          :key="session.id"
          class="group surface-card backdrop-blur-xl rounded-2xl p-4 transition-all duration-200 cursor-pointer hover:shadow"
          :class="compareMode && isSelectedForCompare(session.id) ? (isDark ? 'ring-2 ring-blue-500/50' : 'ring-2 ring-blue-400/50') : ''"
          @click="compareMode ? toggleCompareSelection(session.id) : $router.push(`/reports/${session.id}`)"
        >
          <div class="flex items-start justify-between gap-3">
            <!-- Compare checkbox -->
            <div v-if="compareMode" class="flex-shrink-0 pt-1" @click.stop="toggleCompareSelection(session.id)">
              <div class="w-5 h-5 rounded-md border-2 flex items-center justify-center transition-colors"
                :class="isSelectedForCompare(session.id)
                  ? 'bg-blue-600 border-blue-600'
                  : (isDark ? 'border-slate-600 hover:border-slate-400' : 'border-slate-300 hover:border-slate-500')">
                <svg v-if="isSelectedForCompare(session.id)" class="w-3 h-3 text-white" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/>
                </svg>
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <!-- Date + Urgency badge + Message count -->
              <div class="flex items-center gap-2 mb-1.5 flex-wrap">
                <span class="text-xs font-medium text-[var(--text-secondary)]">
                  {{ formatDate(session.timestamp) }}
                </span>
                <span class="px-2 py-0.5 rounded-full text-detail font-bold uppercase tracking-wide"
                  :class="urgencyClass(session.urgency)">
                  {{ session.urgency }}
                </span>
                <span v-if="getMessageCount(session.id)" class="text-detail px-1.5 py-0.5 rounded-full"
                  :class="isDark ? 'bg-slate-800 text-slate-500' : 'bg-slate-100 text-slate-400'">
                  {{ getMessageCount(session.id) }} messages
                </span>
              </div>

              <!-- Summary (first user message truncated to ~80 chars) -->
              <p class="text-sm font-medium mb-1 leading-snug text-[var(--text-primary)]">
                {{ getSessionSummary(session.id) }}
              </p>

              <!-- Top diagnosis -->
              <div class="flex items-center gap-3 text-xs text-[var(--text-secondary)]">
                <span>{{ session.topDiagnosis }}</span>
                <span v-if="session.confidence" class="font-medium"
                  :class="session.confidence >= 70 ? 'text-emerald-400' : session.confidence >= 40 ? 'text-amber-400' : (isDark ? 'text-slate-500' : 'text-slate-400')">
                  {{ session.confidence }}%
                </span>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2 flex-shrink-0">
              <router-link :to="`/reports/${session.id}`"
                @click.stop
                class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
                :class="isDark
                  ? 'bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900'">
                View Details
              </router-link>
              <button
                @click.stop="handleDelete(session.id)"
                class="p-1.5 rounded-lg transition-all opacity-0 group-hover:opacity-100"
                :class="isDark
                  ? 'text-slate-600 hover:text-red-400 hover:bg-red-500/10'
                  : 'text-slate-400 hover:text-red-500 hover:bg-red-50'"
                title="Delete consultation"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm Dialog -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div v-if="confirmDialog.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
        <div class="surface-card rounded-2xl shadow-2xl max-w-sm w-full p-6">
          <p class="text-sm mb-5 text-[var(--text-primary)]">{{ confirmDialog.message }}</p>
          <div class="flex gap-3 justify-end">
            <button @click="confirmDialog.show = false"
              class="px-4 py-2 text-xs rounded-lg transition-colors"
              :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
              Cancel
            </button>
            <button @click="confirmDialog.action(); confirmDialog.show = false"
              class="px-4 py-2 text-xs text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors">
              Delete
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'
import { getSessions, getSession, deleteSession } from '@/services/historyService.js'

const { isDark } = useTheme()
const searchQuery = ref('')
const viewMode = ref('list') // 'list' or 'timeline'
const allSessions = ref(getSessions())

// Compare mode state
const compareMode = ref(false)
const selectedForCompare = ref([])
const showComparisonPanel = ref(false)

function toggleCompareMode() {
  compareMode.value = !compareMode.value
  if (!compareMode.value) {
    selectedForCompare.value = []
    showComparisonPanel.value = false
  }
}

function isSelectedForCompare(id) {
  return selectedForCompare.value.includes(id)
}

function toggleCompareSelection(id) {
  const idx = selectedForCompare.value.indexOf(id)
  if (idx >= 0) {
    selectedForCompare.value.splice(idx, 1)
  } else if (selectedForCompare.value.length < 2) {
    selectedForCompare.value.push(id)
  } else {
    // Replace the first selection
    selectedForCompare.value.shift()
    selectedForCompare.value.push(id)
  }
}

function confidenceColor(val) {
  if (val >= 70) return 'text-emerald-500'
  if (val >= 40) return 'text-amber-500'
  return isDark.value ? 'text-slate-400' : 'text-slate-500'
}

const comparisonData = computed(() => {
  if (selectedForCompare.value.length !== 2) return null

  const [idA, idB] = selectedForCompare.value
  const sessionA = allSessions.value.find(s => s.id === idA)
  const sessionB = allSessions.value.find(s => s.id === idB)
  if (!sessionA || !sessionB) return null

  const fullA = loadFullSession(idA)
  const fullB = loadFullSession(idB)

  const left = {
    date: formatDate(sessionA.timestamp),
    summary: getSessionSummary(idA),
    topDiagnosis: sessionA.topDiagnosis || 'N/A',
    confidence: sessionA.confidence || 0,
    urgency: sessionA.urgency || 'routine',
    symptoms: fullA?.symptoms || sessionA.symptomsSummary || '',
  }

  const right = {
    date: formatDate(sessionB.timestamp),
    summary: getSessionSummary(idB),
    topDiagnosis: sessionB.topDiagnosis || 'N/A',
    confidence: sessionB.confidence || 0,
    urgency: sessionB.urgency || 'routine',
    symptoms: fullB?.symptoms || sessionB.symptomsSummary || '',
  }

  // Find common and different aspects
  const common = []
  const differences = []

  if (left.topDiagnosis === right.topDiagnosis) {
    common.push(`Same primary diagnosis: ${left.topDiagnosis}`)
  } else {
    differences.push(`Diagnosis changed from "${left.topDiagnosis}" to "${right.topDiagnosis}"`)
  }

  if (left.urgency === right.urgency) {
    common.push(`Same urgency level: ${left.urgency}`)
  } else {
    differences.push(`Urgency changed from "${left.urgency}" to "${right.urgency}"`)
  }

  const confDiff = right.confidence - left.confidence
  if (Math.abs(confDiff) <= 5) {
    common.push(`Similar confidence levels (${left.confidence}% vs ${right.confidence}%)`)
  } else if (confDiff > 0) {
    differences.push(`Confidence increased by ${confDiff} percentage points (${left.confidence}% to ${right.confidence}%)`)
  } else {
    differences.push(`Confidence decreased by ${Math.abs(confDiff)} percentage points (${left.confidence}% to ${right.confidence}%)`)
  }

  // Symptom overlap analysis
  const sympA = (left.symptoms || '').toLowerCase().split(/[\s,;.]+/).filter(w => w.length > 3)
  const sympB = (right.symptoms || '').toLowerCase().split(/[\s,;.]+/).filter(w => w.length > 3)
  const commonSymptoms = sympA.filter(w => sympB.includes(w))
  if (commonSymptoms.length > 0) {
    common.push(`Shared symptom keywords: ${[...new Set(commonSymptoms)].slice(0, 5).join(', ')}`)
  }

  // Generate changes summary
  const dateA = new Date(sessionA.timestamp)
  const dateB = new Date(sessionB.timestamp)
  const daysDiff = Math.round(Math.abs(dateB - dateA) / (1000 * 60 * 60 * 24))
  let changesSummary = `These consultations are ${daysDiff} day${daysDiff !== 1 ? 's' : ''} apart. `

  if (differences.length === 0) {
    changesSummary += 'The assessments are largely consistent, suggesting a stable condition.'
  } else {
    if (confDiff > 10) {
      changesSummary += 'Confidence has improved, indicating clearer symptom presentation. '
    } else if (confDiff < -10) {
      changesSummary += 'Confidence has decreased, which may indicate evolving or ambiguous symptoms. '
    }
    if (left.topDiagnosis !== right.topDiagnosis) {
      changesSummary += 'The primary diagnosis has changed between visits — consider discussing this with your healthcare provider.'
    } else if (left.urgency !== right.urgency) {
      changesSummary += 'The urgency level has shifted — monitor symptoms closely.'
    }
  }

  return { left, right, common, differences, changesSummary }
})

// Health score metrics
const avgConfidence = computed(() => {
  const sessions = allSessions.value.filter(s => s.confidence > 0)
  if (!sessions.length) return 0
  return Math.round(sessions.reduce((sum, s) => sum + s.confidence, 0) / sessions.length)
})

const routineCount = computed(() =>
  allSessions.value.filter(s => !s.urgency || s.urgency === 'routine').length
)

const healthScore = computed(() => {
  if (!allSessions.value.length) return 'N/A'
  // Simple health score: weighted average of confidence + urgency factor
  const urgencyWeights = { routine: 100, soon: 70, urgent: 40, emergency: 10 }
  const scores = allSessions.value.map(s => {
    const conf = s.confidence || 50
    const urgW = urgencyWeights[s.urgency] || 80
    return Math.round((conf * 0.4 + urgW * 0.6))
  })
  const avg = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
  if (avg >= 80) return `${avg} Good`
  if (avg >= 60) return `${avg} Fair`
  return `${avg} Watch`
})

// Group sessions by month for timeline view
const groupedByMonth = computed(() => {
  const groups = {}
  for (const session of filteredSessions.value) {
    const date = new Date(session.timestamp)
    const key = date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
    if (!groups[key]) groups[key] = []
    groups[key].push(session)
  }
  return groups
})

// Cache for full session data (message counts, summaries)
const sessionCache = {}

function loadFullSession(id) {
  if (!sessionCache[id]) {
    sessionCache[id] = getSession(id)
  }
  return sessionCache[id]
}

function getMessageCount(id) {
  const full = loadFullSession(id)
  return full?.chatMessages?.length || 0
}

function getSessionSummary(id) {
  const full = loadFullSession(id)
  if (full?.chatMessages?.length > 0) {
    const firstUserMsg = full.chatMessages.find(m => m.role === 'user' || m.sender === 'user')
    if (firstUserMsg) {
      const text = firstUserMsg.content || firstUserMsg.text || firstUserMsg.message || ''
      return text.length > 80 ? text.substring(0, 80) + '...' : text
    }
  }
  // Fallback to symptoms summary
  const session = allSessions.value.find(s => s.id === id)
  return session?.symptomsSummary || 'No description available'
}

const filteredSessions = computed(() => {
  if (!searchQuery.value.trim()) return allSessions.value
  const q = searchQuery.value.toLowerCase()
  return allSessions.value.filter(s => {
    const summary = getSessionSummary(s.id).toLowerCase()
    return summary.includes(q) ||
      (s.symptomsSummary || '').toLowerCase().includes(q) ||
      (s.topDiagnosis || '').toLowerCase().includes(q)
  })
})

const confirmDialog = reactive({
  show: false,
  message: '',
  action: () => {},
})

function urgencyClass(urgency) {
  if (urgency === 'emergency') return 'bg-red-500/20 text-red-300'
  if (urgency === 'urgent') return 'bg-red-500/15 text-red-400'
  if (urgency === 'soon') return 'bg-amber-500/15 text-amber-400'
  return 'bg-emerald-500/15 text-emerald-400'
}

function formatDate(timestamp) {
  if (!timestamp) return ''
  try {
    const d = new Date(timestamp)
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return timestamp
  }
}

function handleDelete(id) {
  confirmDialog.message = 'Are you sure you want to delete this consultation? This cannot be undone.'
  confirmDialog.action = () => {
    deleteSession(id)
    delete sessionCache[id]
    allSessions.value = getSessions()
  }
  confirmDialog.show = true
}

function exportAllJson() {
  const data = {
    sessions: allSessions.value,
    exportedAt: new Date().toISOString(),
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `consultations-export-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
}
</script>
