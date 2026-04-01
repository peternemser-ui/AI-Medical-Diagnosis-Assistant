<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Header -->
    <div class="backdrop-blur-xl border-b py-3 px-6 shadow-xl transition-colors relative z-50 sticky top-0" :class="isDark ? 'bg-slate-900/95 border-slate-700/50' : 'bg-white/95 border-slate-200'">
      <!-- Subtle gradient line at top of header -->
      <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500"></div>
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-lg shadow-blue-500/25 animate-pulse-slow">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
          </div>
          <div>
            <h1 class="text-lg font-bold leading-tight" :class="isDark ? 'text-white' : 'text-slate-900'">Clinical Assessment</h1>
            <p class="text-caption" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Multi-Agent Diagnostic Report</p>
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
          <span class="px-3 py-1 rounded-full text-caption font-bold uppercase tracking-wider"
                :class="urgencyBadgeClass">
            {{ overallUrgency }}
          </span>
          <!-- Simple/Advanced toggle -->
          <button @click="viewMode = viewMode === 'simple' ? 'advanced' : 'simple'"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-caption font-semibold transition-colors"
            :class="viewMode === 'advanced'
              ? (isDark ? 'bg-purple-500/15 border-purple-500/30 text-purple-300' : 'bg-purple-50 border-purple-200 text-purple-700')
              : (isDark ? 'bg-slate-800/60 border-slate-700/50 text-slate-300' : 'bg-slate-100 border-slate-200 text-slate-600')">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"/></svg>
            {{ viewMode === 'advanced' ? 'Advanced' : 'Simple' }}
          </button>
        </div>

        <div class="flex items-center gap-2">
          <ThemeLangControls />
          <!-- Share dropdown -->
          <div class="relative" ref="shareDropdownRef">
            <button @click="showShareMenu = !showShareMenu"
              class="flex items-center gap-1.5 px-3 py-2 text-xs rounded-lg border transition-colors"
              :class="isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-slate-100 hover:bg-slate-200 border-slate-200 hover:border-slate-300 text-slate-700'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
              Share
            </button>
            <!-- Dropdown menu -->
            <div v-if="showShareMenu"
              class="absolute right-0 top-full mt-1 w-56 rounded-xl border shadow-2xl z-[200] overflow-hidden"
              :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'">
              <button @click="copyReportLink" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs transition-colors" :class="isDark ? 'hover:bg-slate-700/50 text-slate-300' : 'hover:bg-slate-50 text-slate-700'">
                <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
                {{ copySuccess ? 'Copied!' : 'Copy Report Text' }}
              </button>
              <button @click="shareViaEmail" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs transition-colors" :class="isDark ? 'hover:bg-slate-700/50 text-slate-300' : 'hover:bg-slate-50 text-slate-700'">
                <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                Email Report
              </button>
              <button @click="printReport" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs transition-colors" :class="isDark ? 'hover:bg-slate-700/50 text-slate-300' : 'hover:bg-slate-50 text-slate-700'">
                <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
                Print Report
              </button>
              <button v-if="canNativeShare" @click="nativeShare" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs transition-colors" :class="isDark ? 'hover:bg-slate-700/50 text-slate-300' : 'hover:bg-slate-50 text-slate-700'">
                <svg class="w-4 h-4 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
                Share via...
              </button>
              <div class="border-t" :class="isDark ? 'border-slate-700' : 'border-slate-200'"></div>
              <button @click="downloadReport(); showShareMenu = false" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs transition-colors" :class="isDark ? 'hover:bg-slate-700/50 text-slate-300' : 'hover:bg-slate-50 text-slate-700'">
                <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                Download PDF
              </button>
              <button @click="sharePdf" class="w-full flex items-center gap-3 px-4 py-2.5 text-xs transition-colors" :class="isDark ? 'hover:bg-slate-700/50 text-slate-300' : 'hover:bg-slate-50 text-slate-700'">
                <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                {{ isSharePdf ? 'Generating...' : 'Share PDF via...' }}
              </button>
            </div>
          </div>
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
      <div class="flex items-center gap-2">
        <button @click="viewMode = viewMode === 'simple' ? 'advanced' : 'simple'"
          class="px-2 py-0.5 rounded-full text-detail font-bold uppercase transition-colors"
          :class="viewMode === 'advanced'
            ? (isDark ? 'bg-purple-500/15 text-purple-300' : 'bg-purple-50 text-purple-700')
            : (isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-200 text-slate-600')">
          {{ viewMode === 'advanced' ? 'ADV' : 'SMP' }}
        </button>
        <span class="px-2 py-0.5 rounded-full text-detail font-bold uppercase" :class="urgencyBadgeClass">{{ overallUrgency }}</span>
      </div>
    </div>

    <!-- Mobile section pill nav -->
    <div class="md:hidden overflow-x-auto scrollbar-hide border-b" :class="isDark ? 'bg-slate-900/80 border-slate-700/30' : 'bg-white/90 border-slate-200'">
      <div class="flex gap-1 px-3 py-2 min-w-max">
        <button v-for="nav in sectionNavItems" :key="nav.id"
          @click="scrollToSection(nav.id)"
          class="px-3 py-1.5 rounded-full text-detail font-semibold whitespace-nowrap transition-colors"
          :class="activeSection === nav.id
            ? (isDark ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30' : 'bg-blue-50 text-blue-700 border border-blue-200')
            : (isDark ? 'text-slate-400 hover:text-slate-300 hover:bg-slate-800' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100')">
          {{ nav.label }}
        </button>
      </div>
    </div>

    <!-- Main layout with sidebar nav -->
    <div class="max-w-7xl mx-auto flex">

      <!-- Sticky sidebar nav (desktop only) -->
      <nav class="hidden md:block w-48 flex-shrink-0 sticky top-0 self-start pt-6 pl-4 pr-2 max-h-screen overflow-y-auto">
        <div class="space-y-1">
          <button v-for="nav in sectionNavItems" :key="nav.id"
            @click="scrollToSection(nav.id)"
            class="w-full text-left flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-colors"
            :class="activeSection === nav.id
              ? (isDark ? 'bg-blue-500/15 text-blue-300 border border-blue-500/20' : 'bg-blue-50 text-blue-700 border border-blue-200')
              : (isDark ? 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50' : 'text-slate-500 hover:text-slate-700 hover:bg-slate-100')">
            <span class="w-1.5 h-1.5 rounded-full flex-shrink-0"
              :class="activeSection === nav.id ? 'bg-blue-400' : (isDark ? 'bg-slate-600' : 'bg-slate-300')"></span>
            {{ nav.label }}
          </button>
        </div>
      </nav>

      <!-- Main Content Area -->
      <div class="flex-1 min-w-0 px-4 py-5 space-y-5">

        <!-- ============================================================== -->
        <!-- LAYER 1: EXECUTIVE SUMMARY (Hero Area)                         -->
        <!-- ============================================================== -->
        <DiagnosisSummaryHeader
          ref="sectionSummaryRef"
          :causes="causes"
          :urgency="overallUrgency"
          :urgency-badge-class="urgencyBadgeClass"
          :chief-complaint="chiefComplaint"
          :patient-summary="patientSummary"
          :causes-count="causes.length"
          :tests-count="recommendedTests.length"
          :flags-count="redFlags.length"
          :exporting="isExporting"
          @download-pdf="downloadReport"
          @email="shareViaEmail"
        />

        <!-- Probability Distribution Chart -->
        <section v-if="causes.length > 1" class="rounded-xl overflow-hidden transition-colors surface-card">
          <div class="px-5 py-4">
            <div class="flex items-center gap-2.5 mb-4">
              <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center shadow-sm">
                <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              </div>
              <div>
                <h3 class="text-sm font-bold" :class="isDark ? 'text-slate-200' : 'text-slate-800'">Differential Diagnosis Probability</h3>
                <p class="text-detail" :class="isDark ? 'text-slate-400' : 'text-slate-500'">AI confidence distribution across {{ causes.length }} assessed conditions</p>
              </div>
            </div>
            <div class="space-y-2.5">
              <div v-for="(cause, idx) in causes.slice(0, 6)" :key="idx" class="group">
                <div class="flex items-center gap-3">
                  <!-- Rank -->
                  <span class="text-detail font-bold tabular-nums w-4 text-right flex-shrink-0"
                    :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ idx + 1 }}</span>
                  <!-- Label -->
                  <span class="text-xs font-medium truncate min-w-0"
                    :class="idx === 0 ? (isDark ? 'text-white' : 'text-slate-900') : (isDark ? 'text-slate-300' : 'text-slate-700')"
                    style="width: 180px; flex-shrink: 0;">{{ cause.cause }}</span>
                  <!-- Bar -->
                  <div class="flex-1 h-5 rounded-md overflow-hidden relative"
                    :class="isDark ? 'bg-slate-700/40' : 'bg-slate-100'">
                    <div class="h-full rounded-md transition-all duration-700 ease-out flex items-center justify-end pr-2"
                      :style="{
                        width: Math.max(cause.value, 4) + '%',
                        background: idx === 0
                          ? (isDark ? 'linear-gradient(90deg, #3b82f6, #6366f1)' : 'linear-gradient(90deg, #3b82f6, #6366f1)')
                          : (isDark ? `linear-gradient(90deg, ${getBarColor(cause.value)}88, ${getBarColor(cause.value)}55)` : `linear-gradient(90deg, ${getBarColor(cause.value)}cc, ${getBarColor(cause.value)}88)`)
                      }">
                      <span v-if="cause.value >= 15" class="text-tiny font-bold text-white tabular-nums drop-shadow-sm">{{ cause.value }}%</span>
                    </div>
                    <span v-if="cause.value < 15" class="absolute right-2 top-1/2 -translate-y-1/2 text-tiny font-bold tabular-nums"
                      :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ cause.value }}%</span>
                  </div>
                </div>
                <!-- Urgency + specialty tags on first item -->
                <div v-if="idx === 0 && cause.specialty" class="flex items-center gap-2 ml-7 mt-1">
                  <span class="text-tiny px-2 py-0.5 rounded-full font-semibold"
                    :class="(cause.urgency === 'urgent' || cause.urgency === 'emergency')
                      ? (isDark ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600')
                      : cause.urgency === 'soon'
                        ? (isDark ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600')
                        : (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-600')">
                    {{ cause.urgency || 'routine' }}
                  </span>
                  <span class="text-tiny" :class="isDark ? 'text-indigo-400' : 'text-indigo-600'">{{ cause.specialty }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- "Why This Diagnosis?" collapsible section -->
        <section v-if="causes.length > 0" id="section-why" class="space-y-0">
          <div class="rounded-xl overflow-hidden transition-colors surface-card">
            <button @click="expandedSections.whyDiagnosis = !expandedSections.whyDiagnosis"
              class="w-full flex items-center justify-between px-5 py-3 text-left transition-colors"
              :class="isDark ? 'hover:bg-slate-700/30' : 'hover:bg-slate-50'">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-blue-500 flex items-center justify-center shadow-md shadow-indigo-500/20">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                </div>
                <h3 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Why This Diagnosis?</h3>
              </div>
              <svg class="w-4 h-4 transition-transform" :class="[expandedSections.whyDiagnosis ? 'rotate-180' : '', isDark ? 'text-slate-400' : 'text-slate-500']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
            <div v-if="expandedSections.whyDiagnosis" class="px-5 pb-5 space-y-3">
              <!-- Key Takeaway box -->
              <div class="rounded-lg p-4 border-l-4 border-indigo-500" :class="isDark ? 'bg-indigo-500/5' : 'bg-indigo-50'">
                <div class="text-detail font-bold uppercase tracking-wider mb-1" :class="isDark ? 'text-indigo-400' : 'text-indigo-600'">Key Takeaway</div>
                <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-200' : 'text-slate-700'">
                  Based on the reported symptoms{{ chiefComplaint ? ' ("' + chiefComplaint + '")' : '' }}, the most likely condition is
                  <strong>{{ causes[0].cause }}</strong> with {{ causes[0].value }}% confidence.
                </p>
              </div>

              <!-- Supporting features from top diagnosis -->
              <div v-if="causes[0].explanation" class="space-y-2">
                <div class="text-detail font-bold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Clinical Reasoning</div>
                <p class="text-xs leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ causes[0].explanation }}</p>
              </div>

              <!-- Symptoms that led here -->
              <div v-if="causes[0].supporting_features || causes[0].supportingFeatures">
                <div class="text-detail font-bold uppercase tracking-wider mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Supporting Features</div>
                <ul class="space-y-1">
                  <li v-for="(feat, fi) in (causes[0].supporting_features || causes[0].supportingFeatures || [])" :key="'sf-' + fi"
                    class="text-xs flex items-start gap-1.5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <span class="text-blue-400 mt-0.5 flex-shrink-0">&#8226;</span>
                    <span>{{ feat }}</span>
                  </li>
                </ul>
              </div>

              <!-- How other diagnoses compare -->
              <div v-if="causes.length > 1">
                <div class="text-detail font-bold uppercase tracking-wider mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Why Not Other Conditions?</div>
                <div class="space-y-1.5">
                  <div v-for="(c, ci) in causes.slice(1, 4)" :key="'why-' + ci" class="text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <span class="font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ c.cause }} ({{ c.value }}%):</span>
                    {{ c.explanation || 'Lower probability based on symptom pattern analysis.' }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>


        <!-- ============================================================== -->
        <!-- LAYER 2: KEY FINDINGS                                          -->
        <!-- ============================================================== -->

        <!-- Top Diagnoses (ranked cards) + Body Diagram -->
        <section id="section-conditions">
          <div class="flex flex-col lg:flex-row gap-5">
            <!-- Diagnosis Cards (main) -->
            <div class="flex-1 min-w-0 space-y-3">
              <div class="flex items-center gap-2.5 mb-1">
                <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-500 flex items-center justify-center shadow-md shadow-emerald-500/20">
                  <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                </div>
                <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Differential Diagnoses</h2>
              </div>

              <!-- Top 5 ranked diagnosis cards -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <DiagnosisCard
                  v-for="(cause, index) in causes.slice(0, 5)"
                  :key="index"
                  :cause="cause"
                  :rank="index + 1"
                  :red-flags="index === 0 ? redFlags : []"
                  :recommended-tests="getTestsForCause(cause, index)"
                  @open-detail="selectedCause = cause; selectedCauseRank = index + 1; selectedCauseTests = getTestsForCause(cause, index)"
                />
              </div>
              <div v-if="causes.length === 0" class="text-center py-8 text-slate-500 text-sm">No diagnoses available.</div>
            </div>

            <!-- Right rail: Body Diagram + Agent Performance (sticky) -->
            <div class="lg:w-72 xl:w-80 flex-shrink-0 lg:sticky lg:top-4 lg:self-start space-y-4">
              <BodyDiagram
                :causes="causes"
                :body-systems="bodySystems"
                :recommended-tests="recommendedTests"
                :red-flags="redFlags"
                :gender="patientGender"
                compact
              />

              <!-- Compact Agent Performance — Neural Glow -->
              <div class="rounded-2xl overflow-hidden relative" style="background: linear-gradient(145deg, #0a0f1c, #070b16, #05070d); border: 1px solid rgba(255,255,255,0.06)">
                <!-- Ambient glow -->
                <div class="absolute inset-0 pointer-events-none overflow-hidden">
                  <div class="absolute w-[120px] h-[120px] -top-[40px] -right-[30px] rounded-full blur-[60px] opacity-[0.05]"
                    style="background: radial-gradient(circle, #8b5cf6, transparent)"></div>
                </div>

                <button @click="expandedSections.agentPerf = !expandedSections.agentPerf"
                  class="relative z-10 w-full px-3.5 py-2.5 flex items-center justify-between transition-colors hover:bg-white/[0.02]">
                  <div class="flex items-center gap-2">
                    <div class="w-6 h-6 rounded-lg bg-gradient-to-br from-violet-500/50 to-cyan-500/30 flex items-center justify-center border border-white/10">
                      <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                    </div>
                    <span class="text-detail font-bold uppercase tracking-wider text-white/70">Agent Performance</span>
                  </div>
                  <svg class="w-3.5 h-3.5 transition-transform text-white/20" :class="expandedSections.agentPerf ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
                </button>
                <div v-if="expandedSections.agentPerf" class="relative z-10 px-3.5 pb-3.5 space-y-2">
                  <div class="h-px w-full mb-1" style="background: linear-gradient(to right, transparent, rgba(255,255,255,0.06), transparent)"></div>
                  <div v-for="agent in agentList" :key="agent.name" class="flex items-center gap-2 text-detail group">
                    <span class="w-2 h-2 rounded-full flex-shrink-0" :style="{ backgroundColor: agent.color, boxShadow: `0 0 4px ${agent.color}40` }"></span>
                    <span class="w-20 truncate text-white/40 group-hover:text-white/60 transition-colors">{{ agent.name }}</span>
                    <div class="flex-1 h-1.5 rounded-full overflow-hidden bg-white/[0.04]">
                      <div class="h-full rounded-full transition-all duration-500" :style="{ width: agent.barWidth + '%', background: `linear-gradient(90deg, ${agent.color}90, ${agent.color}60)`, boxShadow: `0 0 6px ${agent.color}30` }"></div>
                    </div>
                    <span class="w-10 text-right tabular-nums font-medium text-white/35">{{ formatTime(agent.time) }}</span>
                  </div>
                  <div class="flex items-center justify-between pt-2 mt-1" style="border-top: 1px solid rgba(255,255,255,0.05)">
                    <span class="text-detail font-semibold text-white/50">Total</span>
                    <span class="text-detail font-bold tabular-nums" style="color: #60a5fa">{{ totalPipelineTime ? totalPipelineTime.toFixed(1) + 's' : '--' }}</span>
                  </div>
                  <div v-if="estimatedCost !== null" class="flex items-center justify-between text-detail">
                    <span class="text-white/30">AI Cost</span>
                    <span class="font-semibold" style="color: #22c55e">${{ estimatedCost }}</span>
                  </div>
                  <div v-if="tokenUsage" class="text-tiny text-right text-white/20">
                    {{ tokenUsage.total_input_tokens?.toLocaleString() || 0 }} in / {{ tokenUsage.total_output_tokens?.toLocaleString() || 0 }} out tokens
                  </div>
                </div>
                <!-- Collapsed summary -->
                <div v-else class="relative z-10 px-3.5 pb-2.5 flex items-center justify-between text-detail">
                  <span class="text-white/30 tabular-nums">{{ totalPipelineTime ? totalPipelineTime.toFixed(1) + 's' : '--' }} total</span>
                  <span v-if="estimatedCost !== null" class="font-semibold" style="color: #22c55e">${{ estimatedCost }}</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Red Flags callout -->
        <section v-if="redFlags.length > 0" id="section-redflags">
          <div class="rounded-xl p-4 border transition-colors" :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-200 shadow-sm'">
            <div class="flex items-center gap-2 mb-3">
              <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
              <span class="text-xs font-bold uppercase tracking-wider text-red-400">Red Flags Identified</span>
            </div>
            <ul class="space-y-1.5">
              <li v-for="flag in redFlags" :key="flag" class="text-xs flex items-start gap-2" :class="isDark ? 'text-red-300' : 'text-red-700'">
                <span class="text-red-500 mt-0.5 flex-shrink-0 font-bold">!</span>
                <span>{{ typeof flag === 'object' ? (flag.title || flag.message || flag.issue || flag.description || JSON.stringify(flag)) : flag }}</span>
              </li>
            </ul>
          </div>
        </section>

        <!-- Key Actions section -->
        <section id="section-actions">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <!-- Recommended Tests -->
            <div class="rounded-xl overflow-hidden border transition-colors relative" :class="isDark ? 'bg-slate-800/60 border-slate-700/50 hover:border-cyan-500/30' : 'bg-white border-slate-200 shadow-md hover:shadow-lg'">
              <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-cyan-500 to-blue-500"></div>
              <div class="px-4 py-2.5 border-b flex items-center gap-2.5" style="border-color: var(--clinical-border)">
                <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center shadow-sm shadow-cyan-500/20">
                  <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
                </div>
                <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Recommended Tests</h2>
                <span v-if="recommendedTests.length > 0" class="ml-auto text-detail font-semibold px-2 py-0.5 rounded-full" :class="isDark ? 'bg-cyan-500/15 text-cyan-300' : 'bg-cyan-50 text-cyan-600'">{{ recommendedTests.length }}</span>
              </div>
              <div class="p-3">
                <div v-if="recommendedTests.length > 0" class="space-y-1">
                  <label
                    v-for="(test, i) in recommendedTests"
                    :key="i"
                    class="flex items-start gap-2.5 px-2 py-2 rounded-lg cursor-pointer transition-colors group" :class="isDark ? 'hover:bg-slate-700/30' : 'hover:bg-slate-50'"
                  >
                    <input
                      type="checkbox"
                      v-model="testChecked[i]"
                      :aria-label="'Mark test complete: ' + test"
                      class="mt-0.5 rounded border-slate-600 bg-slate-700 text-blue-500 focus:ring-blue-500/50 focus:ring-offset-0"
                    />
                    <span class="text-xs leading-relaxed" :class="testChecked[i] ? 'line-through text-slate-400' : (isDark ? 'text-slate-300 group-hover:text-slate-200' : 'text-slate-600 group-hover:text-slate-900')">{{ test }}</span>
                  </label>
                </div>
                <div v-else class="text-center py-4 text-slate-500 text-xs">No tests recommended</div>
              </div>
            </div>

            <!-- Action Items (amber accent) -->
            <div class="rounded-xl overflow-hidden border transition-colors relative" :class="isDark ? 'bg-slate-800/60 border-slate-700/50 hover:border-amber-500/30' : 'bg-white border-slate-200 shadow-md hover:shadow-lg'">
              <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-amber-500 to-orange-500"></div>
              <div class="px-4 py-2.5 border-b flex items-center gap-2.5" style="border-color: var(--clinical-border)">
                <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center shadow-sm shadow-amber-500/20">
                  <svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
                </div>
                <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Action Items</h2>
                <span v-if="actionChecklist.length > 0" class="ml-auto text-detail font-semibold px-2 py-0.5 rounded-full" :class="isDark ? 'bg-amber-500/15 text-amber-300' : 'bg-amber-50 text-amber-600'">{{ actionChecklist.length }}</span>
              </div>
              <div class="p-3">
                <div v-if="actionChecklist.length > 0" class="space-y-1">
                  <label
                    v-for="(item, i) in actionChecklist"
                    :key="i"
                    class="flex items-start gap-2.5 px-2 py-2 rounded-lg cursor-pointer transition-colors group" :class="isDark ? 'hover:bg-slate-700/30' : 'hover:bg-slate-50'"
                  >
                    <input
                      type="checkbox"
                      v-model="actionChecked[i]"
                      :aria-label="'Mark action complete: ' + item"
                      class="mt-0.5 rounded focus:ring-amber-500/50 focus:ring-offset-0"
                      :class="isDark ? 'border-slate-600 bg-slate-700 text-amber-500' : 'border-slate-300 bg-white text-amber-600'"
                    />
                    <span class="text-xs leading-relaxed" :class="actionChecked[i] ? 'line-through text-slate-400' : (isDark ? 'text-slate-300 group-hover:text-slate-200' : 'text-slate-600 group-hover:text-slate-900')">{{ item }}</span>
                  </label>
                </div>
                <div v-else class="text-center py-4 text-slate-500 text-xs">No action items</div>
              </div>
            </div>
          </div>
        </section>

        <!-- Confidence Chart -->
        <section id="section-chart">
          <div class="rounded-xl overflow-hidden border transition-colors relative" :class="isDark ? 'bg-slate-800/60 border-slate-700/50 hover:border-blue-500/30' : 'bg-white border-slate-200 shadow-md hover:shadow-lg'">
            <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-blue-500 to-indigo-500"></div>
            <div class="px-5 py-3 border-b flex items-center gap-3" style="border-color: var(--clinical-border)">
              <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center shadow-md shadow-blue-500/20">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              </div>
              <div>
                <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Differential Diagnoses Confidence</h2>
                <p class="text-detail mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Likelihood of each condition based on clinical analysis</p>
              </div>
            </div>
            <div class="p-5">
              <div v-if="causes.length > 0" style="height: 250px; position: relative;">
                <Bar :data="chartData" :options="chartOptions" />
              </div>
              <div v-else class="text-center py-10 text-slate-500 text-sm">No diagnosis data available</div>
            </div>
          </div>
        </section>


        <!-- ============================================================== -->
        <!-- LAYER 3: DEEP ANALYSIS (hidden in simple mode)                 -->
        <!-- ============================================================== -->
        <template v-if="viewMode === 'advanced'">

          <!-- Additional Diagnosis Cards beyond top 5 -->
          <section v-if="causes.length > 5" id="section-more-diagnoses">
            <div class="flex items-center gap-3 mb-4">
              <h3 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-secondary)]">Additional Diagnoses</h3>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              <DiagnosisCard
                v-for="(cause, index) in causes.slice(5)"
                :key="'extra-' + index"
                :cause="cause"
                :rank="index + 6"
                :red-flags="[]"
                :recommended-tests="getTestsForCause(cause, index + 5)"
                @open-detail="selectedCause = cause; selectedCauseRank = index + 6; selectedCauseTests = getTestsForCause(cause, index + 5)"
              />
            </div>
          </section>

          <!-- Treatment & Medications (collapsible) -->
          <section id="section-treatment">
            <div class="rounded-xl overflow-hidden transition-colors relative surface-card">
              <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-teal-500 to-emerald-500"></div>
              <button @click="expandedSections.treatment = !expandedSections.treatment"
                class="w-full px-5 py-3 border-b flex items-center justify-between transition-colors"
                :class="isDark ? 'border-slate-700/30 hover:bg-slate-700/20' : 'border-slate-200 hover:bg-slate-50'">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center shadow-md shadow-teal-500/20">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
                  </div>
                  <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Treatment & Medications</h2>
                </div>
                <svg class="w-4 h-4 transition-transform" :class="[expandedSections.treatment ? 'rotate-180' : '', isDark ? 'text-slate-400' : 'text-slate-500']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
              </button>
              <div v-if="expandedSections.treatment" class="p-4">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <!-- Treatment Plan -->
                  <div>
                    <div v-if="medications.length > 0" class="mb-4">
                      <div class="text-detail font-semibold uppercase mb-2" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Medications</div>
                      <div v-for="med in medications" :key="typeof med === 'string' ? med : med.name" class="text-xs mb-2 p-2.5 rounded-lg" :class="isDark ? 'bg-slate-700/30' : 'bg-slate-50'">
                        <div class="font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ typeof med === 'string' ? med : med.name }}</div>
                        <div v-if="med.dose" class="text-detail mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ med.dose }} {{ med.frequency ? '-- ' + med.frequency : '' }}</div>
                        <div v-if="med.warnings" class="text-detail mt-0.5" :class="isDark ? 'text-red-400' : 'text-red-600'">Warning: {{ med.warnings }}</div>
                      </div>
                    </div>
                    <div v-if="lifestyleRecs.length > 0">
                      <div class="text-detail font-semibold uppercase mb-2" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Lifestyle & Healing</div>
                      <ul class="space-y-1.5">
                        <li v-for="rec in lifestyleRecs" :key="rec" class="text-xs flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                          <span class="text-emerald-400 mt-0.5 flex-shrink-0">&#10003;</span>{{ rec }}
                        </li>
                      </ul>
                    </div>
                    <!-- Warning signs -->
                    <div v-if="warningSignsData.length > 0" class="mt-4">
                      <div class="text-detail font-semibold uppercase mb-2" :class="isDark ? 'text-red-400' : 'text-red-600'">Escalation Triggers</div>
                      <ul class="space-y-1.5">
                        <li v-for="sign in warningSignsData" :key="sign" class="text-xs flex items-start gap-2" :class="isDark ? 'text-red-300' : 'text-red-600'">
                          <span class="text-red-400 mt-0.5 flex-shrink-0">!</span>{{ sign }}
                        </li>
                      </ul>
                    </div>
                    <div v-if="medications.length === 0 && lifestyleRecs.length === 0 && warningSignsData.length === 0" class="text-center py-4 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                      Treatment details will appear after diagnosis
                    </div>
                  </div>

                  <!-- Dietary Recommendations -->
                  <div>
                    <div class="flex items-center gap-2 mb-3">
                      <span class="text-base">&#127957;</span>
                      <div class="text-detail font-semibold uppercase" :class="isDark ? 'text-lime-400' : 'text-lime-600'">Dietary & Healing Guidance</div>
                    </div>
                    <div v-if="dietaryRecs.length > 0" class="space-y-1.5">
                      <div v-for="(rec, i) in dietaryRecs" :key="i" class="text-xs flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                        <span class="flex-shrink-0 mt-0.5">{{ ['&#129388;','&#129744;','&#129371;','&#128167;','&#129495;','&#128564;'][i % 6] }}</span>
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
            </div>
          </section>

          <!-- Safety Review (collapsible) -->
          <section id="section-safety">
            <div class="rounded-xl overflow-hidden transition-colors relative surface-card">
              <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-red-500 to-rose-500"></div>
              <button @click="expandedSections.safety = !expandedSections.safety"
                class="w-full px-5 py-3 border-b flex items-center justify-between transition-colors"
                :class="isDark ? 'border-slate-700/30 hover:bg-slate-700/20' : 'border-slate-200 hover:bg-slate-50'">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-red-500 to-rose-500 flex items-center justify-center shadow-md shadow-red-500/20">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
                  </div>
                  <div class="flex items-center gap-3">
                    <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Safety Review</h2>
                    <span class="text-xs font-bold uppercase px-2.5 py-1 rounded-full" :class="safetyStatusClass">{{ safetyStatusLabel }}</span>
                  </div>
                </div>
                <svg class="w-4 h-4 transition-transform" :class="[expandedSections.safety ? 'rotate-180' : '', isDark ? 'text-slate-400' : 'text-slate-500']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
              </button>
              <div v-if="expandedSections.safety" class="p-4">
                <!-- Warnings -->
                <div v-if="safetyWarnings.length > 0" class="space-y-2">
                  <div
                    v-for="(warning, i) in safetyWarnings"
                    :key="i"
                    class="flex items-start gap-2.5 p-2.5 rounded-lg border"
                    :class="isDark ? 'bg-red-500/5 border-red-500/10' : 'bg-red-50 border-red-200'"
                  >
                    <svg class="w-4 h-4 flex-shrink-0 mt-0.5" :class="isDark ? 'text-red-400' : 'text-red-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    <span class="text-xs leading-relaxed" :class="isDark ? 'text-red-300' : 'text-red-800'">{{ typeof warning === 'object' ? (warning.title || warning.message || warning.issue || warning.description || JSON.stringify(warning)) : warning }}</span>
                  </div>
                </div>
                <div v-if="redFlags.length > 0" class="mt-3 space-y-2">
                  <div class="text-detail font-semibold uppercase mb-1" :class="isDark ? 'text-red-400' : 'text-red-700'">Red Flags</div>
                  <div
                    v-for="(flag, i) in redFlags"
                    :key="'rf-' + i"
                    class="flex items-start gap-2 text-xs"
                    :class="isDark ? 'text-red-300' : 'text-red-700'"
                  >
                    <span class="mt-0.5 flex-shrink-0" :class="isDark ? 'text-red-500' : 'text-red-600'">!</span>
                    <span>{{ typeof flag === 'object' ? (flag.title || flag.message || flag.issue || flag.description || JSON.stringify(flag)) : flag }}</span>
                  </div>
                </div>
                <div v-if="safetyWarnings.length === 0 && redFlags.length === 0" class="text-center py-4 text-slate-500 text-sm">
                  No safety concerns identified
                </div>
              </div>
            </div>
          </section>

          <!-- Body System Indicators — Neural Glow UI -->
          <section id="section-bodysystems">
            <NeuralBodySystems :body-systems="bodySystems" />
          </section>

          <!-- Alternative Medicine — Natural Healing UI -->
          <section id="section-alternative">
            <NaturalHealingSection
              :tcm-recommendations="tcmRecommendations"
              :ayurvedic-recommendations="ayurvedicRecommendations"
              :holistic-recommendations="holisticRecommendations"
            />
          </section>

          <!-- Find Nearby Specialists (collapsible) -->
          <section id="section-specialists">
            <div class="rounded-xl overflow-hidden transition-colors relative surface-card">
              <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-violet-500 to-fuchsia-500"></div>
              <button @click="expandedSections.specialists = !expandedSections.specialists"
                class="w-full px-5 py-3 border-b flex items-center justify-between transition-colors"
                :class="isDark ? 'border-slate-700/30 hover:bg-slate-700/20' : 'border-slate-200 hover:bg-slate-50'">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-fuchsia-500 flex items-center justify-center shadow-md shadow-violet-500/20">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                  </div>
                  <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Find Nearby Specialists</h2>
                </div>
                <svg class="w-4 h-4 transition-transform" :class="[expandedSections.specialists ? 'rotate-180' : '', isDark ? 'text-slate-400' : 'text-slate-500']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
              </button>
              <div v-if="expandedSections.specialists" class="p-4">
                <!-- Specialist intro -->
                <p v-if="uniqueSpecialties.length > 0" class="text-xs mb-3 leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                  Based on the leading diagnoses, <span class="font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ uniqueSpecialties.slice(0, 2).join(' and ') }}</span> {{ uniqueSpecialties.length > 2 ? 'are among the' : uniqueSpecialties.length === 1 ? 'is the' : 'are the' }} most relevant {{ uniqueSpecialties.length === 1 ? 'specialty' : 'specialties' }} to consider.
                </p>

                <!-- Location input -->
                <div class="flex gap-2 mb-3">
                  <div class="flex-1 relative">
                    <input
                      v-model="searchZip"
                      @keyup.enter="updateMapSearch"
                      placeholder="Enter zip code or city..."
                      aria-label="Search by zip code or city"
                      class="w-full rounded-lg px-3 py-2 pr-9 text-sm border focus:outline-none focus:ring-2 focus:ring-blue-500/40"
                      :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'"
                    />
                    <button @click="useMyLocation" :disabled="geoLoading" class="absolute right-2 top-1/2 -translate-y-1/2 p-1 rounded transition-colors" :class="isDark ? 'text-slate-400 hover:text-blue-400' : 'text-slate-400 hover:text-blue-600'" title="Use my location">
                      <svg v-if="!geoLoading" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                      <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                    </button>
                  </div>
                  <select v-model="selectedSpecForMap" @change="updateMapSearch" class="rounded-lg px-3 py-2 text-xs border" :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-700'">
                    <option v-for="spec in uniqueSpecialties" :key="spec" :value="spec">{{ spec }}</option>
                  </select>
                  <button @click="updateMapSearch" class="px-4 py-2 rounded-lg text-xs font-medium bg-blue-600 text-white hover:bg-blue-500 transition-colors">Search</button>
                </div>

                <!-- Map embed -->
                <div class="rounded-lg overflow-hidden mb-4 border" :class="isDark ? 'border-slate-700' : 'border-slate-200'" style="height: 350px">
                  <iframe
                    :src="mapSrc"
                    width="100%" height="100%" style="border:0" allowfullscreen loading="lazy" referrerpolicy="no-referrer-when-downgrade"
                    title="Map showing nearby medical specialists"
                    aria-label="Map showing nearby medical specialists"
                  ></iframe>
                </div>

                <!-- Specialty search links -->
                <div class="flex flex-wrap gap-2">
                  <a v-for="spec in uniqueSpecialties" :key="spec"
                    :href="'https://www.google.com/maps/search/' + encodeURIComponent(spec + (searchZip ? ' near ' + searchZip : ' near me'))"
                    target="_blank" rel="noopener"
                    class="inline-flex items-center gap-1.5 text-xs px-3 py-2 rounded-lg border transition-colors"
                    :class="isDark ? 'bg-slate-700/50 border-slate-600/50 text-slate-300 hover:bg-blue-500/15 hover:border-blue-500/30 hover:text-blue-300' : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-blue-50 hover:border-blue-300 hover:text-blue-700'"
                  >
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
                    <span v-if="doctorResults.length > 0" class="text-detail tabular-nums" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ doctorResults.length }} found</span>
                  </div>

                  <!-- Loading -->
                  <div v-if="doctorsLoading" class="flex items-center justify-center py-8 gap-2">
                    <svg class="w-4 h-4 animate-spin text-blue-400" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                    <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Searching NPI Registry...</span>
                  </div>

                  <!-- Results grid -->
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
                          <div class="text-caption mt-0.5" :class="isDark ? 'text-blue-400' : 'text-blue-600'">{{ doc.specialty }}</div>
                          <div class="text-caption mt-1 whitespace-pre-line leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ doc.address }}</div>
                          <div v-if="doc.phone" class="flex items-center gap-1 mt-1.5">
                            <svg class="w-3 h-3" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                            <a :href="'tel:' + doc.phone" class="text-caption hover:underline" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ formatPhone(doc.phone) }}</a>
                          </div>
                        </div>
                      </div>
                      <div class="flex items-center gap-2 mt-3 pt-2.5 border-t" :class="isDark ? 'border-slate-600/20' : 'border-slate-200'">
                        <a :href="'https://www.google.com/maps/search/' + encodeURIComponent(doc.name + ' ' + doc.address.replace(/\\n/g, ' '))"
                          target="_blank" rel="noopener"
                          class="text-detail px-2 py-1 rounded-md transition-colors inline-flex items-center gap-1"
                          :class="isDark ? 'bg-slate-600/30 text-slate-300 hover:bg-slate-600/50' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                          Map
                        </a>
                        <a v-if="doc.phone" :href="'tel:' + doc.phone"
                          class="text-detail px-2 py-1 rounded-md transition-colors inline-flex items-center gap-1"
                          :class="isDark ? 'bg-blue-500/15 text-blue-300 hover:bg-blue-500/25' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                          Call
                        </a>
                        <a :href="'https://npiregistry.cms.hhs.gov/provider-view/' + doc.npi"
                          target="_blank" rel="noopener"
                          class="text-detail px-2 py-1 rounded-md transition-colors inline-flex items-center gap-1 ml-auto"
                          :class="isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-400 hover:text-slate-600'">
                          NPI: {{ doc.npi }}
                          <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                        </a>
                      </div>
                    </div>
                  </div>

                  <!-- No results -->
                  <div v-else-if="doctorsSearched" class="text-center py-6 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                    No providers found. Try a different zip code or specialty.
                  </div>

                  <!-- Not searched yet -->
                  <div v-else class="text-center py-6 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                    Enter a zip code and click Search to find providers.
                  </div>
                </div>

                <p class="text-detail mt-3" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Provider data from the NPI National Registry (CMS.gov). Always verify credentials and check with your insurance provider.</p>
              </div>
            </div>
          </section>

          <!-- Conversation Transcript (collapsible) -->
          <section v-if="chatTranscript.length > 0" id="section-transcript">
            <div class="rounded-xl overflow-hidden transition-colors relative surface-card">
              <div class="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-sky-500 to-blue-500"></div>
              <button @click="expandedSections.transcript = !expandedSections.transcript"
                class="w-full px-5 py-3 border-b flex items-center justify-between transition-colors"
                :class="isDark ? 'border-slate-700/30 hover:bg-slate-700/20' : 'border-slate-200 hover:bg-slate-50'">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-sky-500 to-blue-500 flex items-center justify-center shadow-md shadow-sky-500/20">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
                  </div>
                  <h2 class="text-body-sm font-bold uppercase tracking-wide text-[var(--text-primary)]">Conversation Transcript</h2>
                </div>
                <svg class="w-4 h-4 transition-transform" :class="[expandedSections.transcript ? 'rotate-180' : '', isDark ? 'text-slate-400' : 'text-slate-500']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
              </button>
              <div v-if="expandedSections.transcript" class="p-4 space-y-3 max-h-96 overflow-y-auto">
                <div v-for="(msg, idx) in chatTranscript" :key="idx">
                  <div v-if="msg.role === 'assistant'" class="mb-1">
                    <div class="text-detail font-semibold uppercase mb-1" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Dr. AI</div>
                    <p class="text-xs leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ msg.content }}</p>
                  </div>
                  <div v-else class="ml-4 p-2.5 rounded-lg" :class="isDark ? 'bg-blue-500/10 border border-blue-500/20' : 'bg-blue-50 border border-blue-100'">
                    <div class="text-detail font-semibold uppercase mb-1" :class="isDark ? 'text-blue-300' : 'text-blue-700'">You</div>
                    <p class="text-xs font-medium" :class="isDark ? 'text-blue-200' : 'text-blue-800'">{{ msg.content }}</p>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </template><!-- end advanced mode -->

        <!-- Bottom Actions -->
        <div class="flex justify-center gap-3 flex-wrap py-4">
          <button
            @click="downloadReport"
            :disabled="isExporting"
            class="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 hover:from-blue-700 hover:via-blue-600 hover:to-cyan-600 disabled:opacity-60 disabled:cursor-wait rounded-xl text-sm font-semibold text-white shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-105 transition-all"
          >
            <svg v-if="isExporting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            {{ isExporting ? 'Exporting...' : 'Download PDF' }}
          </button>
          <button
            @click="copyReportLink"
            class="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold border transition-all hover:scale-105"
            :class="copySuccess
              ? 'bg-emerald-500/15 border-emerald-500/30 text-emerald-400'
              : (isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-white hover:bg-slate-50 border-slate-300 hover:border-slate-400 text-slate-700')"
          >
            <svg v-if="copySuccess" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
            {{ copySuccess ? 'Copied!' : 'Copy Report' }}
          </button>
          <button
            @click="shareViaEmail"
            class="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold border transition-all hover:scale-105"
            :class="isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-white hover:bg-slate-50 border-slate-300 hover:border-slate-400 text-slate-700'"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            Email
          </button>
          <button
            v-if="canNativeShare"
            @click="nativeShare"
            class="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white shadow-lg shadow-purple-500/20 hover:shadow-purple-500/40 hover:scale-105 transition-all"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
            Share
          </button>
          <router-link
            to="/consult"
            class="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-semibold border transition-all hover:scale-105"
            :class="isDark ? 'bg-slate-800 hover:bg-slate-700 border-slate-700/50 hover:border-slate-600 text-white' : 'bg-white hover:bg-slate-50 border-slate-300 hover:border-slate-400 text-slate-700'"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            New Assessment
          </router-link>
        </div>
      </div>
    </div>

    <!-- ═══ Diagnosis Detail Modal ═══ -->
    <Teleport to="body">
      <Transition name="modal-fade">
        <div v-if="selectedCause" class="fixed inset-0 z-[100] flex items-center justify-center p-4" role="dialog" aria-modal="true" @keydown.escape="selectedCause = null">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/70 backdrop-blur-sm" @click="selectedCause = null"></div>
          <!-- Modal -->
          <div class="relative w-full max-w-2xl max-h-[85vh] overflow-y-auto rounded-2xl border shadow-2xl" :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-slate-200'">
            <!-- Close button -->
            <button @click="selectedCause = null" class="absolute top-4 right-4 z-10 p-1.5 rounded-lg transition-colors" :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-700' : 'text-slate-400 hover:text-slate-900 hover:bg-slate-100'">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>

            <!-- Header with gradient -->
            <div class="relative overflow-hidden">
              <div class="absolute top-0 left-0 right-0 h-1" :class="selectedCause.value >= 70 ? 'bg-gradient-to-r from-emerald-500 to-teal-500' : selectedCause.value >= 40 ? 'bg-gradient-to-r from-amber-500 to-orange-500' : 'bg-gradient-to-r from-blue-500 to-indigo-500'"></div>
              <div class="px-8 pt-8 pb-6">
                <div class="flex items-start gap-5">
                  <!-- Confidence circle -->
                  <div class="flex-shrink-0 w-20 h-20 rounded-full flex items-center justify-center"
                    :class="selectedCause.value >= 70 ? 'bg-emerald-500/15 ring-4 ring-emerald-500/20' : selectedCause.value >= 40 ? 'bg-amber-500/15 ring-4 ring-amber-500/20' : 'bg-blue-500/15 ring-4 ring-blue-500/20'">
                    <div class="text-center">
                      <div class="text-2xl font-black tabular-nums" :class="selectedCause.value >= 70 ? 'text-emerald-400' : selectedCause.value >= 40 ? 'text-amber-400' : 'text-blue-400'">{{ selectedCause.value }}%</div>
                      <div class="text-micro font-bold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">confidence</div>
                    </div>
                  </div>
                  <div class="flex-1 min-w-0 pt-1">
                    <div class="flex items-center gap-2 flex-wrap mb-1">
                      <span v-if="selectedCauseRank === 1" class="text-detail font-bold uppercase px-2 py-0.5 rounded-full bg-yellow-500/15 text-yellow-400">Most Likely</span>
                      <span class="text-detail font-bold uppercase px-2 py-0.5 rounded-full"
                        :class="(selectedCause.urgency === 'urgent' || selectedCause.urgency === 'emergency') ? 'bg-red-500/15 text-red-400' : selectedCause.urgency === 'soon' ? 'bg-amber-500/15 text-amber-400' : 'bg-emerald-500/15 text-emerald-400'">
                        {{ selectedCause.urgency || 'routine' }}
                      </span>
                    </div>
                    <h2 class="text-xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ selectedCause.cause }}</h2>
                    <div class="text-sm font-medium mt-1" :class="isDark ? 'text-blue-400' : 'text-blue-600'">{{ selectedCause.specialty || 'General Medicine' }}</div>
                    <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Rank #{{ selectedCauseRank }} of {{ causes.length }} differential diagnoses</div>
                  </div>
                </div>
                <!-- Confidence bar -->
                <div class="mt-4 h-2 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'">
                  <div class="h-full rounded-full transition-all duration-700" :class="selectedCause.value >= 70 ? 'bg-emerald-500' : selectedCause.value >= 40 ? 'bg-amber-500' : 'bg-blue-500'" :style="{ width: selectedCause.value + '%' }"></div>
                </div>
              </div>
            </div>

            <!-- Body content -->
            <div class="px-8 pb-8 space-y-5">
              <!-- Clinical reasoning -->
              <div v-if="selectedCause.explanation">
                <div class="text-detail font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Clinical Reasoning</div>
                <p class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ selectedCause.explanation }}</p>
              </div>

              <!-- Supporting features -->
              <div v-if="selectedCause.supporting_features?.length > 0 || selectedCause.supportingFeatures?.length > 0">
                <div class="text-detail font-bold uppercase tracking-wider mb-2 text-emerald-400">Supporting Evidence</div>
                <ul class="space-y-1.5">
                  <li v-for="(f, i) in (selectedCause.supporting_features || selectedCause.supportingFeatures)" :key="'sf-'+i" class="text-sm flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <span class="text-emerald-400 mt-0.5 flex-shrink-0 font-bold">+</span>
                    <span>{{ f }}</span>
                  </li>
                </ul>
              </div>

              <!-- Opposing features -->
              <div v-if="selectedCause.opposing_features?.length > 0 || selectedCause.opposingFeatures?.length > 0">
                <div class="text-detail font-bold uppercase tracking-wider mb-2 text-amber-400">Points Against</div>
                <ul class="space-y-1.5">
                  <li v-for="(f, i) in (selectedCause.opposing_features || selectedCause.opposingFeatures)" :key="'of-'+i" class="text-sm flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <span class="text-amber-400 mt-0.5 flex-shrink-0">-</span>
                    <span>{{ f }}</span>
                  </li>
                </ul>
              </div>

              <!-- Red flags for this condition -->
              <div v-if="selectedCauseRank === 1 && redFlags.length > 0">
                <div class="text-detail font-bold uppercase tracking-wider mb-2 text-red-400">Warning Signs</div>
                <div class="p-3 rounded-lg border" :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-200'">
                  <ul class="space-y-1.5">
                    <li v-for="flag in redFlags" :key="flag" class="text-sm flex items-start gap-2" :class="isDark ? 'text-red-300' : 'text-red-700'">
                      <span class="text-red-500 mt-0.5 flex-shrink-0 font-bold">!</span>
                      <span>{{ typeof flag === 'object' ? (flag.title || flag.message || flag.issue || flag.description || JSON.stringify(flag)) : flag }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <!-- Recommended tests -->
              <div v-if="selectedCauseTests.length > 0">
                <div class="text-detail font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Recommended Tests</div>
                <ul class="space-y-1.5">
                  <li v-for="test in selectedCauseTests" :key="test" class="text-sm flex items-start gap-2" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                    <svg class="w-4 h-4 mt-0.5 flex-shrink-0 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/></svg>
                    <span>{{ test }}</span>
                  </li>
                </ul>
              </div>

              <!-- Research links -->
              <div>
                <div class="text-detail font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Research</div>
                <div class="flex flex-wrap gap-2">
                  <a :href="'https://scholar.google.com/scholar?q=' + encodeURIComponent(selectedCause.cause)" target="_blank" rel="noopener"
                    class="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-2 rounded-lg transition-colors"
                    :class="isDark ? 'bg-blue-500/10 text-blue-400 hover:bg-blue-500/20' : 'bg-blue-50 text-blue-600 hover:bg-blue-100'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>
                    Google Scholar
                  </a>
                  <a :href="'https://www.mayoclinic.org/search/search-results?q=' + encodeURIComponent(selectedCause.cause)" target="_blank" rel="noopener"
                    class="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-2 rounded-lg transition-colors"
                    :class="isDark ? 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
                    Mayo Clinic
                  </a>
                  <a :href="'https://medlineplus.gov/search/?query=' + encodeURIComponent(selectedCause.cause)" target="_blank" rel="noopener"
                    class="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-2 rounded-lg transition-colors"
                    :class="isDark ? 'bg-purple-500/10 text-purple-400 hover:bg-purple-500/20' : 'bg-purple-50 text-purple-600 hover:bg-purple-100'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"/></svg>
                    MedlinePlus
                  </a>
                  <a :href="'https://en.wikipedia.org/wiki/' + encodeURIComponent(selectedCause.cause)" target="_blank" rel="noopener"
                    class="inline-flex items-center gap-1.5 text-xs font-medium px-3 py-2 rounded-lg transition-colors"
                    :class="isDark ? 'bg-slate-700/50 text-slate-300 hover:bg-slate-700' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                    Wikipedia
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, reactive, watch } from 'vue'
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
import BodyDiagram from './BodyDiagram.vue'
import NeuralBodySystems from './NeuralBodySystems.vue'
import NaturalHealingSection from './NaturalHealingSection.vue'
import DiagnosisSummaryHeader from './DiagnosisSummaryHeader.vue'
import ThemeLangControls from './ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'
import { getProfile } from '@/services/userService.js'
import { API_BASE_URL } from '@/services/api.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const { isDark } = useTheme()

// Data
const diagnosisData = ref(null)
const reportRef = ref(null)
const isExporting = ref(false)

// --- NEW: Redesign reactive state ---
const viewMode = ref('advanced')
const selectedCause = ref(null)
const selectedCauseRank = ref(0)
const selectedCauseTests = ref([])

const expandedSections = ref({
  whyDiagnosis: true,
  treatment: true,
  safety: true,
  bodySystems: false,
  alternative: false,
  specialists: true,
  performance: false,
  transcript: false,
  agentPerf: false,
})
const activeSection = ref('summary')
const sectionSummaryRef = ref(null)

const sectionNavItems = computed(() => {
  const items = [
    { id: 'summary', label: 'Summary' },
    { id: 'conditions', label: 'Conditions' },
    { id: 'actions', label: 'Actions' },
    { id: 'chart', label: 'Chart' },
  ]
  if (viewMode.value === 'advanced') {
    items.push(
      { id: 'treatment', label: 'Treatment' },
      { id: 'safety', label: 'Safety' },
      { id: 'specialists', label: 'Specialists' },
      { id: 'performance', label: 'Performance' },
    )
    if (chatTranscript.value.length > 0) {
      items.push({ id: 'transcript', label: 'Transcript' })
    }
  }
  return items
})

function scrollToSection(id) {
  const el = document.getElementById('section-' + id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    activeSection.value = id
  }
}

// Scroll spy for active section
let scrollObserver = null

function setupScrollSpy() {
  if (typeof IntersectionObserver === 'undefined') return
  if (scrollObserver) scrollObserver.disconnect()

  scrollObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        const id = entry.target.id?.replace('section-', '')
        if (id) activeSection.value = id
      }
    }
  }, { rootMargin: '-20% 0px -60% 0px', threshold: 0 })

  // Observe all section elements
  const sectionIds = ['summary', 'why', 'conditions', 'redflags', 'actions', 'chart', 'treatment', 'safety', 'bodysystems', 'alternative', 'specialists', 'performance', 'transcript', 'more-diagnoses']
  for (const id of sectionIds) {
    const el = document.getElementById('section-' + id)
    if (el) scrollObserver.observe(el)
  }
}

onMounted(() => {
  loadData()
  document.addEventListener('click', handleClickOutside)
  // Pre-fill specialist search location from profile and auto-search
  const profile = getProfile()
  if (profile.zipCode) {
    searchZip.value = profile.zipCode
  } else if (profile.city) {
    searchZip.value = profile.city + (profile.stateRegion ? ', ' + profile.stateRegion : '')
  }
  // Auto-search for doctors if we have a zip code
  if (searchZip.value) {
    // Wait for data to load so specialties are available
    setTimeout(() => {
      if (uniqueSpecialties.value.length > 0) {
        selectedSpecForMap.value = uniqueSpecialties.value[0]
      }
      updateMapSearch()
    }, 500)
  }
  // Setup scroll spy after a tick
  setTimeout(setupScrollSpy, 300)
})

onUnmounted(() => {
  if (scrollObserver) scrollObserver.disconnect()
  document.removeEventListener('click', handleClickOutside)
})

// Re-setup scroll spy when view mode changes
watch(viewMode, () => {
  setTimeout(setupScrollSpy, 100)
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
    medications: [
      { name: 'Omeprazole (Prilosec)', dose: '20mg once daily', frequency: 'Before breakfast', warnings: 'Limit to 8 weeks; reassess if symptoms persist' },
      { name: 'Calcium Carbonate (Tums)', dose: '500mg as needed', frequency: 'After meals', warnings: 'Do not exceed 6 tablets/day' },
    ],
    lifestyle_recommendations: [
      'Elevate the head of your bed 6-8 inches to reduce nighttime acid reflux',
      'Avoid eating within 3 hours of bedtime',
      'Reduce caffeine, alcohol, chocolate, and spicy food intake',
      'Maintain a healthy weight — excess abdominal fat increases reflux',
      'Quit smoking — nicotine relaxes the lower esophageal sphincter',
      'Wear loose-fitting clothing to reduce abdominal pressure',
      'Practice stress management — yoga, meditation, or deep breathing exercises',
    ],
    dietary_recommendations: [
      'Eat smaller, more frequent meals instead of 3 large meals',
      'Include alkaline foods: bananas, melons, oatmeal, and green vegetables',
      'Increase fiber intake with whole grains, fruits, and vegetables',
      'Choose lean proteins: chicken, fish, tofu — avoid fried or fatty meats',
      'Drink ginger or chamomile tea to soothe the digestive tract',
      'Avoid acidic foods: tomatoes, citrus, vinegar, and carbonated drinks',
      'Include probiotic-rich foods: yogurt, kefir, sauerkraut, kimchi',
      'Stay hydrated with water between meals (not during) to aid digestion',
    ],
    token_usage: {
      per_agent: {
        triage: { input_tokens: 1250, output_tokens: 580 },
        diagnostician: { input_tokens: 4800, output_tokens: 2100 },
        research: { input_tokens: 3900, output_tokens: 1800 },
        specialist: { input_tokens: 5200, output_tokens: 2400 },
        treatment: { input_tokens: 6100, output_tokens: 2800 },
        safety: { input_tokens: 5500, output_tokens: 1900 },
        empathy: { input_tokens: 4300, output_tokens: 2200 },
      },
      total_input_tokens: 31050,
      total_output_tokens: 13780,
      total_tokens: 44830,
    },
    estimated_cost: localStorage.getItem('ai_provider') === 'ollama' ? 0 : 0.30,
  }
}

// Extract causes from answer text when structured causes array is empty
function _extractCausesFromText(d) {
  if (!d) return []
  const text = d.answer || ''
  if (!text) return []
  const causes = []

  // Look for "DIFFERENTIAL DIAGNOSIS:" section in the answer text
  const diffMatch = text.match(/DIFFERENTIAL DIAGNOSIS[:\s]*\n([\s\S]*?)(?=\n(?:RESEARCH|TREATMENT|SPECIALIST|SUGGESTED|CLINICAL|$))/i)
  if (diffMatch) {
    const section = diffMatch[1]
    // Pattern: "1. Condition Name — Confidence: 80% — Urgency: routine"
    const pattern = /(\d+)\.\s+(.+?)\s*—\s*Confidence:\s*(\d+)%\s*—\s*Urgency:\s*(\w+)/gi
    let match
    while ((match = pattern.exec(section)) !== null) {
      const reasoningMatch = section.slice(match.index + match[0].length).match(/^\s*(?:—\s*Specialty:\s*([^\n]+))?\s*\n?\s*(?:Reasoning:\s*([^\n]+(?:\n(?!\s*\d+\.)[^\n]+)*))?/i)
      causes.push({
        cause: match[2].trim(),
        value: parseInt(match[3]),
        urgency: match[4].trim().toLowerCase(),
        specialty: reasoningMatch?.[1]?.trim() || 'Primary Care',
        explanation: reasoningMatch?.[2]?.trim() || ''
      })
    }
  }

  // Fallback: try extracting from agent_details.diagnosis
  if (causes.length === 0 && d.agent_details?.diagnosis) {
    const diag = d.agent_details.diagnosis
    const differential = diag.differential_diagnosis || diag.diagnoses || diag.differential || diag.conditions || []
    for (const item of differential.slice(0, 5)) {
      if (typeof item === 'object' && item !== null) {
        causes.push({
          cause: item.condition || item.name || item.diagnosis || 'Unknown',
          value: Math.min(100, Math.max(0, parseInt(item.confidence || item.confidence_pct || item.probability || 50))),
          urgency: item.urgency || item.priority || 'routine',
          specialty: item.specialty || item.recommended_specialty || 'Primary Care',
          explanation: item.reasoning || item.clinical_reasoning || item.bayesian_reasoning || item.explanation || ''
        })
      }
    }

    // If agent_details.diagnosis is raw_text, try extracting JSON from it
    if (causes.length === 0 && diag.raw_text) {
      try {
        // Find JSON objects in the raw text via bracket matching
        const raw = diag.raw_text
        const jsonObjects = []
        let depth = 0, start = -1
        for (let i = 0; i < raw.length; i++) {
          if (raw[i] === '{') { if (depth === 0) start = i; depth++ }
          else if (raw[i] === '}') { depth--; if (depth === 0 && start >= 0) { jsonObjects.push(raw.slice(start, i + 1)); start = -1 } }
        }
        jsonObjects.sort((a, b) => b.length - a.length)
        const diffKeys = ['differential_diagnosis', 'diagnoses', 'differential', 'conditions']
        for (const candidate of jsonObjects) {
          if (causes.length > 0) break
          try {
            const parsed = JSON.parse(candidate)
            if (typeof parsed !== 'object' || parsed === null) continue
            let diff = null
            for (const dk of diffKeys) {
              if (Array.isArray(parsed[dk]) && parsed[dk].length > 0) { diff = parsed[dk]; break }
            }
            if (!diff) continue
            for (const item of diff.slice(0, 5)) {
              if (typeof item === 'object' && item !== null) {
                const conf = item.confidence || item.confidence_pct || item.probability || item.likelihood || 50
                causes.push({
                  cause: item.condition || item.name || item.diagnosis || 'Unknown',
                  value: Math.min(100, Math.max(0, parseInt(String(conf).replace('%', '')) || 50)),
                  urgency: item.urgency || item.priority || 'routine',
                  specialty: item.specialty || item.recommended_specialty || 'Primary Care',
                  explanation: item.reasoning || item.clinical_reasoning || item.bayesian_reasoning || item.explanation || ''
                })
              }
            }
          } catch { /* skip unparseable candidates */ }
        }
      } catch { /* ignore extraction errors */ }
    }
  }

  return causes
}

// Computed
const causes = computed(() => {
  if (!diagnosisData.value) return []
  const direct = diagnosisData.value.causes || []
  if (direct.length > 0) return direct
  // Fallback: try to extract from answer text or agent_details
  return _extractCausesFromText(diagnosisData.value)
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

const chiefComplaint = computed(() => {
  const d = diagnosisData.value
  if (!d) return ''
  return d.chief_complaint || d.chiefComplaint || d.symptoms || ''
})

const patientSummary = computed(() => {
  const d = diagnosisData.value
  if (!d) return ''
  return d.patient_summary || d.patientSummary || ''
})

const recommendedTests = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  const direct = d.recommended_tests || d.recommendedTests || []
  if (direct.length > 0) return normalizeArray(direct)
  const specialist = d.agent_details?.specialist || {}
  if (specialist.recommended_tests?.length > 0) return normalizeArray(specialist.recommended_tests)
  if (specialist.diagnostic_tests?.length > 0) return normalizeArray(specialist.diagnostic_tests)
  const diag = d.agent_details?.diagnosis || {}
  if (diag.recommended_tests?.length > 0) return normalizeArray(diag.recommended_tests)
  return []
})
const redFlags = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  const direct = d.red_flags || d.redFlags || []
  if (direct.length > 0) return normalizeArray(direct)
  const triage = d.agent_details?.triage || {}
  return normalizeArray(triage.red_flags || triage.warning_signs || [])
})

// Distribute tests across cards — first card gets all, others get tests matching their specialty
function getTestsForCause(cause, index) {
  if (index === 0) return recommendedTests.value
  const specialty = (cause.specialty || '').toLowerCase()
  const condition = (cause.cause || '').toLowerCase()
  // Filter tests that seem relevant to this condition/specialty
  return recommendedTests.value.filter(test => {
    const t = test.toLowerCase()
    // Match by specialty keywords
    if (specialty.includes('cardio') && (t.includes('ecg') || t.includes('troponin') || t.includes('stress') || t.includes('heart') || t.includes('cardiac'))) return true
    if (specialty.includes('gastro') && (t.includes('endoscop') || t.includes('h. pylori') || t.includes('gi') || t.includes('stool') || t.includes('metabolic'))) return true
    if (specialty.includes('dermat') && (t.includes('skin') || t.includes('biopsy') || t.includes('patch') || t.includes('allergy'))) return true
    if (specialty.includes('pulmon') && (t.includes('chest') || t.includes('x-ray') || t.includes('ct') || t.includes('pulmon') || t.includes('spirom'))) return true
    if (specialty.includes('neuro') && (t.includes('mri') || t.includes('ct') || t.includes('eeg') || t.includes('neuro'))) return true
    if (specialty.includes('rheumat') && (t.includes('sed rate') || t.includes('esr') || t.includes('crp') || t.includes('ana') || t.includes('rheumat'))) return true
    if (specialty.includes('psych') && (t.includes('phq') || t.includes('gad') || t.includes('screen') || t.includes('mental'))) return true
    if (specialty.includes('endo') && (t.includes('thyroid') || t.includes('tsh') || t.includes('a1c') || t.includes('glucose') || t.includes('hormone'))) return true
    // Match by condition name keywords
    const condWords = condition.split(/\s+/).filter(w => w.length > 4)
    return condWords.some(w => t.includes(w))
  })
}
const actionChecklist = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  // Try top-level keys first
  const direct = d.action_checklist || d.actionChecklist || []
  if (direct.length > 0) return normalizeArray(direct)
  // Fallback: extract from agent_details.empathy
  const empathy = d.agent_details?.empathy || {}
  const fromEmpathy = empathy.action_checklist || empathy.actions || empathy.next_steps || empathy.recommendations || []
  if (fromEmpathy.length > 0) return normalizeArray(fromEmpathy)
  // Fallback: extract from treatment agent
  const treatment = d.agent_details?.treatment || {}
  const fromTreatment = treatment.action_items || treatment.action_checklist || treatment.next_steps || []
  if (fromTreatment.length > 0) return normalizeArray(fromTreatment)
  // Fallback: build from recommended tests + red flags
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
const safetyWarnings = computed(() => {
  const raw = diagnosisData.value?.safety_warnings || diagnosisData.value?.safetyWarnings || []
  return raw.map(w => {
    if (typeof w === 'string') {
      // Handle Python dict repr strings like "{'id': 'HIGH-001', 'title': '...'}"
      if (w.startsWith('{') && w.includes("'title':")) {
        const titleMatch = w.match(/'title':\s*'([^']*(?:''[^']*)*)'/)
        if (titleMatch) return titleMatch[1].replace(/''/g, "'")
      }
      if (w.startsWith('{') && w.includes("'issue':")) {
        const issueMatch = w.match(/'issue':\s*'([^']*(?:''[^']*)*)'/)
        if (issueMatch) return issueMatch[1].replace(/''/g, "'")
      }
      if (w.startsWith('{') && w.includes("'message':")) {
        const msgMatch = w.match(/'message':\s*'([^']*(?:''[^']*)*)'/)
        if (msgMatch) return msgMatch[1].replace(/''/g, "'")
      }
      return w
    }
    if (typeof w === 'object' && w !== null) return w.title || w.message || w.issue || w.description || w.text || JSON.stringify(w)
    return String(w)
  })
})

function _extractMedications(d) {
  if (!d) return []
  // Top-level
  const direct = d.medications || []
  if (direct.length > 0) return direct
  // From agent_details.treatment
  const treatment = d.agent_details?.treatment || {}
  if (treatment.medications?.length > 0) return treatment.medications
  // From nested treatment_plans
  const plans = treatment.treatment_plans || treatment.treatmentPlans || []
  if (Array.isArray(plans)) {
    for (const plan of plans) {
      if (plan.medications?.length > 0) return plan.medications
      if (plan.pharmacological?.length > 0) return plan.pharmacological
    }
  }
  // From stepped care
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
  // From nested treatment_plans
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
const lifestyleRecs = computed(() => normalizeArray(_extractLifestyle(diagnosisData.value)))
const dietaryRecs = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  const direct = d.dietary_recommendations || []
  if (direct.length > 0) return normalizeArray(direct)
  const treatment = d.agent_details?.treatment || {}
  return normalizeArray(treatment.dietary_recommendations || treatment.diet || [])
})

const chatTranscript = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  // From stored chat_transcript
  const transcript = d.chat_transcript || []
  if (transcript.length > 0) return transcript.filter(m => m.content)
  // Fallback: from localStorage chatHistory
  try {
    const raw = localStorage.getItem('chatHistory')
    if (raw) return JSON.parse(raw).filter(m => m.content)
  } catch { /* ignore */ }
  return []
})

const tokenUsage = computed(() => diagnosisData.value?.token_usage || { total_input_tokens: 0, total_output_tokens: 0, total_tokens: 0 })

const isOllamaProvider = computed(() => {
  const provider = localStorage.getItem('ai_provider') || ''
  return provider === 'ollama'
})

const estimatedCost = computed(() => {
  // Ollama is free — runs locally
  if (isOllamaProvider.value) return null
  const d = diagnosisData.value
  if (!d) return '0.00'
  // Use backend-calculated cost if available
  if (d.estimated_cost != null && d.estimated_cost > 0) return d.estimated_cost.toFixed(2)
  // Fallback: estimate from token usage
  const usage = d.token_usage
  if (usage && usage.total_tokens > 0) {
    const inputCost = (usage.total_input_tokens / 1_000_000) * 3.00
    const outputCost = (usage.total_output_tokens / 1_000_000) * 15.00
    return (inputCost + outputCost).toFixed(2)
  }
  // Fallback: rough estimate from pipeline time
  if (d.total_time) return (d.total_time * 0.002).toFixed(2)
  return '0.00'
})

const defaultDietaryTips = [
  { icon: '\uD83D\uDCA7', text: 'Stay well hydrated — aim for 8+ glasses of water daily to support healing' },
  { icon: '\uD83E\uDD6C', text: 'Eat anti-inflammatory foods: leafy greens, berries, fatty fish, nuts, and olive oil' },
  { icon: '\uD83E\uDED0', text: 'Include antioxidant-rich foods: blueberries, tomatoes, spinach, and bell peppers' },
  { icon: '\uD83E\uDD5B', text: 'Ensure adequate protein intake for tissue repair — lean meats, eggs, legumes, dairy' },
  { icon: '\uD83D\uDE34', text: 'Prioritize 7-9 hours of quality sleep — critical for immune function and healing' },
  { icon: '\uD83E\uDDD8', text: 'Manage stress through meditation, deep breathing, or gentle exercise' },
]

// Helper: normalize any value that might be an object to a readable string
function toText(item) {
  if (typeof item === 'string') {
    // Handle Python dict repr strings like "{'feature': 'Orthostatic vital signs', ...}"
    if (item.startsWith('{') && item.includes("':")) {
      // Try to extract the most useful field from the Python dict string
      for (const key of ['feature', 'title', 'name', 'message', 'issue', 'test', 'condition', 'action', 'recommendation']) {
        const match = item.match(new RegExp(`'${key}':\\s*'([^']*(?:''[^']*)*)'`))
        if (match) {
          let text = match[1].replace(/''/g, "'")
          // Also try to get detail/impact
          const detailMatch = item.match(/'(?:diagnostic_impact|detail|description|reasoning)':\s*'([^']*(?:''[^']*)*)'/)
          if (detailMatch) text += ' — ' + detailMatch[1].replace(/''/g, "'")
          return text
        }
      }
    }
    return item
  }
  if (typeof item === 'object' && item !== null) {
    // Try common text fields first
    const text = item.title || item.message || item.issue || item.description || item.text || item.name || item.recommendation || item.content || item.feature || item.test || item.condition || item.finding || item.action || item.step || item.item || item.value
    if (text) {
      // If the object has additional context, append it
      const detail = item.detail || item.diagnostic_impact || item.reasoning || item.explanation || ''
      return detail ? `${text} — ${detail}` : text
    }
    // Last resort: build readable string from key-value pairs
    const entries = Object.entries(item).filter(([k, v]) => typeof v === 'string' && v.length < 200).slice(0, 3)
    if (entries.length > 0) return entries.map(([k, v]) => `${v}`).join(' — ')
    return JSON.stringify(item)
  }
  return String(item)
}

// Helper: normalize an array of possibly-mixed items to strings
function normalizeArray(arr) {
  if (!Array.isArray(arr)) return []
  return arr.map(toText)
}

const warningSignsData = computed(() => {
  const d = diagnosisData.value
  if (!d) return []
  return normalizeArray(d.warning_signs || d.warningSignsData || d.agent_details?.treatment?.warning_signs || [])
})

// --- Holistic & Alternative Medicine Recommendations ---
// These are generated based on the top diagnosis conditions

const _conditionContext = computed(() => {
  const allText = causes.value.map(c => ((c.cause || '') + ' ' + (c.specialty || '')).toLowerCase()).join(' ')
  return allText
})

const tcmRecommendations = computed(() => {
  const ctx = _conditionContext.value
  const recs = []

  // Acupuncture
  const acuPoints = []
  if (ctx.includes('skin') || ctx.includes('dermat') || ctx.includes('eczema') || ctx.includes('atopic')) {
    acuPoints.push('LI-11 (Quchi) and SP-10 (Xuehai) to clear heat and cool blood for skin conditions')
    acuPoints.push('LI-4 (Hegu) for general immune regulation and anti-inflammatory effects')
  }
  if (ctx.includes('gastro') || ctx.includes('reflux') || ctx.includes('gerd') || ctx.includes('ulcer') || ctx.includes('digest')) {
    acuPoints.push('ST-36 (Zusanli) to strengthen digestive function and regulate stomach qi')
    acuPoints.push('CV-12 (Zhongwan) to harmonize the stomach and relieve epigastric discomfort')
  }
  if (ctx.includes('anxiety') || ctx.includes('stress') || ctx.includes('psych') || ctx.includes('mental') || ctx.includes('insomnia')) {
    acuPoints.push('HT-7 (Shenmen) to calm the mind and treat insomnia and anxiety')
    acuPoints.push('PC-6 (Neiguan) to open the chest, calm the spirit, and relieve nausea')
  }
  if (ctx.includes('pain') || ctx.includes('musculo') || ctx.includes('arthri') || ctx.includes('costo')) {
    acuPoints.push('GB-34 (Yanglingquan) for musculoskeletal pain and tendon health')
    acuPoints.push('BL-17 (Geshu) to invigorate blood and relieve chest/rib area pain')
  }
  if (ctx.includes('cardio') || ctx.includes('heart') || ctx.includes('chest') || ctx.includes('angina')) {
    acuPoints.push('PC-6 (Neiguan) to regulate heart qi and relieve chest oppression')
    acuPoints.push('HT-7 (Shenmen) to nourish the heart and calm the spirit')
  }
  if (acuPoints.length === 0) {
    acuPoints.push('ST-36 (Zusanli) — master point for overall health, immunity, and energy')
    acuPoints.push('LI-4 (Hegu) — powerful point for pain relief, immune support, and general well-being')
  }
  recs.push({ icon: '\uD83D\uDCCD', category: 'Acupuncture Points', recommendations: acuPoints })

  // Herbal formulas
  const herbs = []
  if (ctx.includes('skin') || ctx.includes('dermat') || ctx.includes('eczema') || ctx.includes('atopic') || ctx.includes('lichen')) {
    herbs.push('Xiao Feng San (Wind-Eliminating Powder) — for itchy skin lesions with wind-heat')
    herbs.push('Liang Xue Qing Fei Yin — to cool blood and clear lung heat manifesting in the skin')
    herbs.push('Chrysanthemum & honeysuckle tea — to clear heat-toxins and support skin healing')
  }
  if (ctx.includes('gastro') || ctx.includes('reflux') || ctx.includes('gerd') || ctx.includes('digest')) {
    herbs.push('Ban Xia Xie Xin Tang — harmonizes the stomach, addresses acid reflux and bloating')
    herbs.push('Si Jun Zi Tang (Four Gentlemen) — strengthens spleen qi and improves digestion')
  }
  if (ctx.includes('anxiety') || ctx.includes('stress') || ctx.includes('mental')) {
    herbs.push('Gui Pi Tang — nourishes heart blood and spleen qi, addresses anxiety with fatigue')
    herbs.push('Suan Zao Ren Tang — calms the spirit, for insomnia and restlessness')
  }
  if (ctx.includes('vitamin') || ctx.includes('deficien') || ctx.includes('anemia')) {
    herbs.push('Si Wu Tang (Four Substances) — classic blood-nourishing formula for deficiency')
    herbs.push('Ba Zhen Tang (Eight Treasures) — tonifies both qi and blood')
  }
  if (herbs.length === 0) {
    herbs.push('Liu Wei Di Huang Wan — foundational yin-nourishing formula for overall wellness')
    herbs.push('Bu Zhong Yi Qi Tang — raises qi and supports immune function')
  }
  recs.push({ icon: '\uD83C\uDF31', category: 'Herbal Formulas', recommendations: herbs })

  // Qigong / Tai Chi
  recs.push({ icon: '\uD83E\uDD4B', category: 'Movement Therapy', recommendations: [
    'Tai Chi — 20-30 minutes daily to improve circulation, reduce stress, and support immunity',
    'Baduanjin (Eight Brocades Qigong) — gentle exercises to balance organ systems',
  ]})

  return recs
})

const ayurvedicRecommendations = computed(() => {
  const ctx = _conditionContext.value
  const recs = []

  // Herbal remedies
  const herbs = []
  if (ctx.includes('skin') || ctx.includes('dermat') || ctx.includes('eczema') || ctx.includes('atopic') || ctx.includes('lichen')) {
    herbs.push('Neem (Nimba) — blood purifier, antibacterial; apply neem oil topically or take capsules')
    herbs.push('Turmeric (Haridra) — powerful anti-inflammatory; mix with warm milk (Golden Milk) before bed')
    herbs.push('Manjistha — blood cleanser that supports healthy skin complexion and reduces rashes')
  }
  if (ctx.includes('gastro') || ctx.includes('reflux') || ctx.includes('gerd') || ctx.includes('digest') || ctx.includes('ulcer')) {
    herbs.push('Amla (Indian Gooseberry) — natural antacid, rich in vitamin C, cools pitta')
    herbs.push('Yashtimadhu (Licorice root) — soothes inflamed gastric mucosa and reduces acid')
    herbs.push('Triphala — gentle digestive cleanser; take 1/2 tsp with warm water before bed')
  }
  if (ctx.includes('anxiety') || ctx.includes('stress') || ctx.includes('mental') || ctx.includes('insomnia')) {
    herbs.push('Ashwagandha — adaptogen that reduces cortisol, anxiety, and promotes restful sleep')
    herbs.push('Brahmi (Bacopa) — calms the nervous system and improves mental clarity')
  }
  if (ctx.includes('vitamin') || ctx.includes('deficien') || ctx.includes('anemia')) {
    herbs.push('Shatavari — nourishing tonic that supports nutrient absorption and vitality')
    herbs.push('Chyawanprash — traditional rejuvenative jam with 40+ herbs for overall nourishment')
  }
  if (herbs.length === 0) {
    herbs.push('Ashwagandha — adaptogenic herb for stress resilience and overall vitality')
    herbs.push('Triphala — balances all three doshas and supports healthy digestion')
  }
  recs.push({ icon: '\uD83E\uDEDA', category: 'Herbal Remedies', recommendations: herbs })

  // Dietary principles (dosha-based)
  const diet = []
  if (ctx.includes('skin') || ctx.includes('inflam') || ctx.includes('acid') || ctx.includes('reflux') || ctx.includes('gerd')) {
    diet.push('Follow a Pitta-pacifying diet: favor cooling foods like cucumber, coconut, cilantro, and mint')
    diet.push('Avoid spicy, sour, and fermented foods that increase internal heat')
  } else if (ctx.includes('anxiety') || ctx.includes('insomnia') || ctx.includes('pain')) {
    diet.push('Follow a Vata-pacifying diet: favor warm, grounding foods like soups, ghee, and cooked grains')
    diet.push('Eat meals at regular times; avoid cold, raw, and dry foods')
  } else {
    diet.push('Eat according to your dosha (body type) — consult an Ayurvedic practitioner for assessment')
    diet.push('Favor freshly cooked, seasonal, and whole foods; eat main meal at midday when digestion is strongest')
  }
  recs.push({ icon: '\uD83C\uDF72', category: 'Dietary Principles', recommendations: diet })

  // Practices
  recs.push({ icon: '\uD83E\uDDD8', category: 'Daily Practices (Dinacharya)', recommendations: [
    'Abhyanga — daily warm oil self-massage (sesame for Vata, coconut for Pitta) before bathing',
    'Pranayama — Nadi Shodhana (alternate nostril breathing) to balance nervous system, 5-10 min daily',
    'Tongue scraping upon waking — removes ama (toxins) and stimulates digestive fire',
  ]})

  return recs
})

const holisticRecommendations = computed(() => {
  const ctx = _conditionContext.value
  const recs = []

  // Herbal / supplement
  const supps = []
  if (ctx.includes('skin') || ctx.includes('dermat') || ctx.includes('eczema') || ctx.includes('atopic') || ctx.includes('lichen')) {
    supps.push('Omega-3 fatty acids (fish oil 2-3g/day) — reduces inflammatory mediators in skin conditions')
    supps.push('Evening Primrose Oil — gamma-linolenic acid supports skin barrier function')
    supps.push('Probiotics (Lactobacillus strains) — gut-skin axis modulation; emerging evidence for eczema')
    supps.push('Calendula cream — topical application for soothing irritated, dry, or inflamed skin')
  }
  if (ctx.includes('gastro') || ctx.includes('reflux') || ctx.includes('gerd') || ctx.includes('digest') || ctx.includes('ulcer')) {
    supps.push('Slippery Elm bark — forms protective mucilage coating on esophageal and gastric lining')
    supps.push('DGL (Deglycyrrhizinated Licorice) — stimulates mucus production; chew 2 tablets before meals')
    supps.push('L-Glutamine (5g/day) — supports intestinal mucosal repair and gut lining integrity')
    supps.push('Aloe Vera juice (2 oz before meals) — soothing and anti-inflammatory for the GI tract')
  }
  if (ctx.includes('anxiety') || ctx.includes('stress') || ctx.includes('mental') || ctx.includes('insomnia')) {
    supps.push('Magnesium glycinate (300-400mg at bedtime) — calms the nervous system and promotes sleep')
    supps.push('L-Theanine (200mg) — promotes relaxation without drowsiness; found naturally in green tea')
    supps.push('Valerian root extract — mild sedative for sleep support; take 30-60 minutes before bed')
    supps.push('Passionflower tea — anxiolytic effects comparable to some pharmaceuticals in mild anxiety')
  }
  if (ctx.includes('vitamin') || ctx.includes('deficien') || ctx.includes('b12') || ctx.includes('anemia')) {
    supps.push('Methylcobalamin B12 sublingual (1000-5000mcg) — better absorbed form for B12 deficiency')
    supps.push('Iron bisglycinate with Vitamin C — gentle, well-absorbed form for anemia support')
    supps.push('Spirulina — nutrient-dense superfood rich in B vitamins, iron, and plant protein')
  }
  if (ctx.includes('cardio') || ctx.includes('heart') || ctx.includes('angina') || ctx.includes('cholesterol')) {
    supps.push('CoQ10 (100-200mg) — supports heart energy production and reduces oxidative stress')
    supps.push('Hawthorn berry extract — traditional heart tonic; improves coronary blood flow')
  }
  if (supps.length === 0) {
    supps.push('Vitamin D3 (2000-4000 IU) — essential for immune function; many people are deficient')
    supps.push('Probiotics (multi-strain) — supports gut microbiome and overall immune health')
    supps.push('Omega-3 fatty acids — broad anti-inflammatory effects for cardiovascular and brain health')
  }
  recs.push({ icon: '\uD83D\uDC8A', category: 'Supplements & Herbs', recommendations: supps })

  // Mind-body
  const mindbody = []
  if (ctx.includes('pain') || ctx.includes('costo') || ctx.includes('musculo')) {
    mindbody.push('Therapeutic yoga — gentle stretches targeting chest wall and thoracic spine')
    mindbody.push('Guided imagery / body scan meditation — 15 min daily for pain modulation')
  }
  if (ctx.includes('skin') || ctx.includes('dermat')) {
    mindbody.push('Stress reduction meditation — skin conditions often worsen with psycho-emotional stress')
    mindbody.push('Cool water hydrotherapy — lukewarm baths with colloidal oatmeal for itch relief')
  }
  if (ctx.includes('gastro') || ctx.includes('reflux') || ctx.includes('gerd')) {
    mindbody.push('Diaphragmatic breathing — strengthens the lower esophageal sphincter to reduce reflux')
    mindbody.push('Progressive muscle relaxation after meals — reduces stress-induced acid production')
  }
  mindbody.push('Mindfulness-Based Stress Reduction (MBSR) — 8-week program with strong clinical evidence')
  recs.push({ icon: '\uD83E\uDDE0', category: 'Mind-Body Therapies', recommendations: mindbody })

  // Manual / energy therapies
  recs.push({ icon: '\uD83E\uDD32', category: 'Bodywork & Energy', recommendations: [
    'Therapeutic massage — improves lymphatic drainage, reduces cortisol, and relieves muscle tension',
    'Reflexology — stimulation of reflex points on feet corresponding to affected body systems',
    'Aromatherapy — lavender (calming), tea tree (antimicrobial), peppermint (digestive and pain relief)',
  ]})

  return recs
})

const uniqueSpecialties = computed(() => {
  const specs = causes.value.map(c => c.specialty).filter(Boolean)
  // Always include Dermatologist for skin-related conditions
  const allText = causes.value.map(c => ((c.cause || '') + ' ' + (c.specialty || '')).toLowerCase()).join(' ')
  if (allText.includes('skin') || allText.includes('dermat') || allText.includes('cheilit') || allText.includes('lip') || allText.includes('rash') || allText.includes('acne')) {
    specs.push('Dermatologist')
  }
  return [...new Set(specs)].slice(0, 6)
})

const searchZip = ref('')
const geoLoading = ref(false)

async function useMyLocation() {
  if (!navigator.geolocation) return
  geoLoading.value = true
  try {
    const pos = await new Promise((resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject, { timeout: 10000 }))
    // Reverse geocode via Nominatim (free, no key)
    const resp = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}&format=json&zoom=10`)
    const data = await resp.json()
    const zip = data.address?.postcode || ''
    const city = data.address?.city || data.address?.town || data.address?.village || ''
    searchZip.value = zip || city || `${pos.coords.latitude.toFixed(2)},${pos.coords.longitude.toFixed(2)}`
    updateMapSearch()
  } catch (e) {
    console.error('Geolocation failed:', e)
  } finally {
    geoLoading.value = false
  }
}
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
    const resp = await fetch(`${API_BASE_URL}/api/find-doctors?` + params)
    if (!resp.ok) throw new Error(`Doctor search returned ${resp.status}`)
    const data = await resp.json()
    doctorResults.value = data.results || []
  } catch {
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

// Initialize selected specialty
watch(uniqueSpecialties, (specs) => {
  if (specs.length > 0 && !selectedSpecForMap.value) {
    selectedSpecForMap.value = specs[0]
  }
}, { immediate: true })

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
  if (label === 'FAIL') return isDark.value ? 'bg-red-500/20 text-red-300' : 'bg-red-100 text-red-700 border border-red-200'
  if (label === 'CAUTION') return isDark.value ? 'bg-amber-500/20 text-amber-300' : 'bg-amber-100 text-amber-800 border border-amber-200'
  return isDark.value ? 'bg-emerald-500/20 text-emerald-300' : 'bg-emerald-100 text-emerald-700 border border-emerald-200'
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

function getBarColor(value) {
  if (value >= 70) return '#10b981'
  if (value >= 40) return '#f59e0b'
  return '#94a3b8'
}

function formatTime(seconds) {
  if (!seconds || seconds === 0) return '--'
  if (seconds < 1) return (seconds * 1000).toFixed(0) + 'ms'
  return seconds.toFixed(1) + 's'
}

// Chart data
const chartData = computed(() => {
  const labels = causes.value.map(c => c.cause || c.condition || 'Unknown')
  const values = causes.value.map(c => c.value || c.confidence || 0)
  const dark = isDark.value
  const colors = values.map(v => {
    if (v >= 70) return dark ? 'rgba(16, 185, 129, 0.8)' : 'rgba(5, 150, 105, 0.85)'
    if (v >= 40) return dark ? 'rgba(245, 158, 11, 0.8)' : 'rgba(217, 119, 6, 0.85)'
    if (v >= 15) return dark ? 'rgba(100, 116, 139, 0.8)' : 'rgba(59, 130, 246, 0.7)'
    return dark ? 'rgba(100, 116, 139, 0.8)' : 'rgba(148, 163, 184, 0.7)'
  })
  const borderColors = values.map(v => {
    if (v >= 70) return dark ? 'rgba(16, 185, 129, 1)' : 'rgba(5, 150, 105, 1)'
    if (v >= 40) return dark ? 'rgba(245, 158, 11, 1)' : 'rgba(217, 119, 6, 1)'
    if (v >= 15) return dark ? 'rgba(100, 116, 139, 1)' : 'rgba(59, 130, 246, 1)'
    return dark ? 'rgba(100, 116, 139, 1)' : 'rgba(148, 163, 184, 1)'
  })

  return {
    labels,
    datasets: [{
      label: 'Confidence %',
      data: values,
      backgroundColor: colors,
      borderColor: borderColors,
      borderWidth: dark ? 1 : 2,
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
      grid: { color: isDark.value ? 'rgba(51, 65, 85, 0.3)' : 'rgba(148, 163, 184, 0.4)' },
      ticks: { color: isDark.value ? '#94a3b8' : '#475569', font: { weight: isDark.value ? 'normal' : '500' }, callback: (v) => v + '%' }
    },
    y: {
      grid: { display: false },
      ticks: {
        color: isDark.value ? '#cbd5e1' : '#1e293b',
        font: { size: 11, weight: isDark.value ? 'normal' : '600' },
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
  { name: 'Digestive', icon: '\uD83E\uDE79', full: 'Gastrointestinal Tract', keywords: ['stomach', 'digest', 'gastro', 'bowel', 'abdominal', 'nausea', 'gi'] },
  { name: 'Muscles & Joints', icon: '\uD83E\uDDB4', full: 'Musculoskeletal System', keywords: ['muscle', 'joint', 'bone', 'musculoskeletal', 'back', 'arthritis', 'pain'] },
  { name: 'Skin', icon: '\uD83E\uDE7A', keywords: ['skin', 'dermat', 'rash', 'itch', 'eczema', 'psoriasis'] },
  { name: 'Kidneys', icon: '\uD83E\uDEC0', keywords: ['kidney', 'renal', 'urinary', 'bladder'] },
  { name: 'Liver', icon: '\uD83E\uDEDB', keywords: ['liver', 'hepat', 'biliary', 'gallbladder'] },
  { name: 'Endocrine', icon: '\uD83E\uDDEA', keywords: ['thyroid', 'diabetes', 'hormone', 'endocrine', 'adrenal'] },
  { name: 'Immune', icon: '\uD83D\uDEE1\uFE0F', keywords: ['immune', 'autoimmune', 'allergy', 'infection', 'virus', 'bacteria', 'fungal'] },
  { name: 'Eyes', icon: '\uD83D\uDC41\uFE0F', keywords: ['eye', 'vision', 'ophthalm', 'retina'] },
  { name: 'Ear, Nose & Throat', icon: '\uD83D\uDC42', full: 'ENT / Otolaryngology', keywords: ['ear', 'nose', 'throat', 'sinus', 'tonsil'] },
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

// --- Share functionality ---
const showShareMenu = ref(false)
const shareDropdownRef = ref(null)
const copySuccess = ref(false)
const isSharePdf = ref(false)
const canNativeShare = computed(() => !!navigator.share)

// Close share dropdown on click outside
function handleClickOutside(e) {
  if (shareDropdownRef.value && !shareDropdownRef.value.contains(e.target)) {
    showShareMenu.value = false
  }
}

// Build plain text report for sharing
function buildReportText() {
  const lines = []
  lines.push('=== MEDICAL CONSULTATION REPORT ===')
  lines.push(`Date: ${formattedDate.value}`)
  if (patientAge.value) lines.push(`Patient: Age ${patientAge.value}${patientGender.value ? ', ' + patientGender.value : ''}`)
  lines.push(`Priority: ${overallUrgency.value}`)
  lines.push('')

  if (chiefComplaint.value) {
    lines.push(`CHIEF COMPLAINT: ${chiefComplaint.value}`)
    lines.push('')
  }

  if (causes.value.length > 0) {
    lines.push('DIFFERENTIAL DIAGNOSES:')
    causes.value.forEach((c, i) => {
      lines.push(`  ${i + 1}. ${c.cause} — ${c.value}% confidence (${c.urgency}) [${c.specialty}]`)
      if (c.explanation) lines.push(`     ${c.explanation}`)
    })
    lines.push('')
  }

  if (redFlags.value.length > 0) {
    lines.push('RED FLAGS:')
    redFlags.value.forEach(f => lines.push(`  ! ${f}`))
    lines.push('')
  }

  if (recommendedTests.value.length > 0) {
    lines.push('RECOMMENDED TESTS:')
    recommendedTests.value.forEach(t => lines.push(`  - ${t}`))
    lines.push('')
  }

  if (actionChecklist.value.length > 0) {
    lines.push('ACTION ITEMS:')
    actionChecklist.value.forEach((a, i) => lines.push(`  ${i + 1}. ${a}`))
    lines.push('')
  }

  if (medications.value.length > 0) {
    lines.push('MEDICATIONS:')
    medications.value.forEach(m => {
      const name = typeof m === 'string' ? m : m.name
      const dose = m.dose ? ` — ${m.dose}` : ''
      lines.push(`  - ${name}${dose}`)
    })
    lines.push('')
  }

  if (safetyWarnings.value.length > 0) {
    lines.push('SAFETY WARNINGS:')
    safetyWarnings.value.forEach(w => lines.push(`  ⚠ ${w}`))
    lines.push('')
  }

  lines.push('---')
  lines.push('This AI-generated report is for informational purposes only.')
  lines.push('Always consult a qualified healthcare professional.')

  return lines.join('\n')
}

async function copyReportLink() {
  try {
    const text = buildReportText()
    await navigator.clipboard.writeText(text)
    copySuccess.value = true
    showShareMenu.value = false
    setTimeout(() => { copySuccess.value = false }, 2500)
  } catch {
    // Fallback for older browsers
    const text = buildReportText()
    const ta = document.createElement('textarea')
    ta.value = text
    ta.style.position = 'fixed'
    ta.style.opacity = '0'
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
    copySuccess.value = true
    showShareMenu.value = false
    setTimeout(() => { copySuccess.value = false }, 2500)
  }
}

function shareViaEmail() {
  const subject = encodeURIComponent(`Medical Consultation Report — ${formattedDate.value}`)
  const body = encodeURIComponent(buildReportText())
  window.open(`mailto:?subject=${subject}&body=${body}`, '_self')
  showShareMenu.value = false
}

function printReport() {
  showShareMenu.value = false
  window.print()
}

async function nativeShare() {
  showShareMenu.value = false
  try {
    await navigator.share({
      title: `Medical Consultation Report — ${formattedDate.value}`,
      text: buildReportText(),
    })
  } catch {
    // User cancelled or not supported — silently ignore
  }
}

async function sharePdf() {
  if (isSharePdf.value) return
  isSharePdf.value = true
  showShareMenu.value = false

  try {
    const { buildPrintReport } = await import('@/services/pdfReport.js')
    const { sharePdf: sharePdfUtil } = await import('@/services/pdfExport.js')

    const reportHtml = buildPrintReport(_buildReportData())
    const meta = { date: formattedDate.value, patientAge: patientAge.value, patientGender: patientGender.value, diagnosis: causes.value[0]?.cause }
    await sharePdfUtil(reportHtml, meta)
  } catch (err) {
    console.error('Share PDF failed:', err)
  } finally {
    isSharePdf.value = false
  }
}

// Shared data builder for PDF export
function _buildReportData() {
  return {
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
    chiefComplaint: chiefComplaint.value,
    medications: medications.value,
    lifestyleRecs: lifestyleRecs.value,
    dietaryRecs: dietaryRecs.value.length > 0 ? dietaryRecs.value : defaultDietaryTips.map(t => t.text),
    patientSummary: patientSummary.value,
    bodySystems: bodySystems.value,
    warningSignsData: warningSignsData.value,
    // Additional data for parity with screen report
    tcmRecommendations: tcmRecommendations.value,
    ayurvedicRecommendations: ayurvedicRecommendations.value,
    holisticRecommendations: holisticRecommendations.value,
    chatTranscript: chatTranscript.value,
    estimatedCost: estimatedCost.value,
    tokenUsage: tokenUsage.value,
  }
}

async function downloadReport() {
  if (isExporting.value) return
  isExporting.value = true

  try {
    const { buildPrintReport } = await import('@/services/pdfReport.js')
    const { downloadPdf } = await import('@/services/pdfExport.js')

    const reportHtml = buildPrintReport(_buildReportData())
    const meta = { date: formattedDate.value, patientAge: patientAge.value, patientGender: patientGender.value, diagnosis: causes.value[0]?.cause }
    await downloadPdf(reportHtml, meta)
  } catch (err) {
    console.error('PDF export failed:', err)
    alert('PDF export failed: ' + (err.message || 'Unknown error. Check browser console.'))
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
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.modal-fade-enter-active { transition: all 0.25s ease-out; }
.modal-fade-leave-active { transition: all 0.15s ease-in; }
.modal-fade-enter-from { opacity: 0; transform: scale(0.95); }
.modal-fade-leave-to { opacity: 0; transform: scale(0.97); }
</style>
