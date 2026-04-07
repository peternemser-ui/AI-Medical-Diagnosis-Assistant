<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Calming ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-indigo-600/8' : 'bg-indigo-300/15'"></div>
      <div class="absolute bottom-1/3 right-1/4 w-80 h-80 rounded-full blur-[100px]"
        :class="isDark ? 'bg-purple-600/6' : 'bg-purple-300/12'"></div>
      <div class="absolute top-2/3 left-1/3 w-72 h-72 rounded-full blur-[110px]"
        :class="isDark ? 'bg-teal-600/5' : 'bg-teal-300/10'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="relative z-20 flex items-center justify-between px-6 py-3 border-b backdrop-blur-xl"
      style="background: color-mix(in srgb, var(--clinical-surface) 85%, transparent); border-color: var(--clinical-border)">
      <div class="flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
          </div>
          <span class="text-sm font-semibold hidden sm:inline text-[var(--text-primary)]">Medical AI</span>
        </router-link>
        <div class="w-px h-5 hidden sm:block bg-[var(--clinical-border)]"></div>
        <span class="text-sm font-medium hidden sm:inline text-[var(--text-secondary)]">Mental Health</span>
      </div>
      <div class="flex items-center gap-2">
        <ThemeLangControls />
        <router-link to="/consult" class="p-1.5 rounded-lg transition-colors"
          :class="isDark ? 'hover:bg-slate-800 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
          </svg>
        </router-link>
      </div>
    </nav>

    <!-- Crisis Disclaimer Banner -->
    <div class="relative z-10 max-w-4xl mx-auto px-4 mt-4">
      <div class="rounded-2xl border px-5 py-3 flex items-start gap-3"
        :class="isDark ? 'bg-indigo-950/40 border-indigo-800/50' : 'bg-indigo-50 border-indigo-200'">
        <svg class="w-5 h-5 mt-0.5 flex-shrink-0" :class="isDark ? 'text-indigo-400' : 'text-indigo-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <div>
          <p class="text-sm font-medium" :class="isDark ? 'text-indigo-300' : 'text-indigo-800'">
            This is a screening tool, not a diagnosis. If you're in crisis, call
            <a href="tel:988" class="underline font-bold">988</a>
            (Suicide &amp; Crisis Lifeline) or text HOME to 741741.
          </p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 max-w-4xl mx-auto px-4 py-6 space-y-8">

      <!-- Tab Navigation -->
      <div class="flex gap-1 p-1 rounded-2xl"
        :class="isDark ? 'bg-slate-800/60' : 'bg-slate-100'">
        <button v-for="tab in tabs" :key="tab.id" @click="activeTab = tab.id"
          class="flex-1 py-2.5 px-4 rounded-xl text-sm font-medium transition-all duration-200"
          :class="activeTab === tab.id
            ? (isDark ? 'bg-indigo-600/30 text-indigo-300 shadow-sm' : 'bg-white text-indigo-700 shadow-sm')
            : (isDark ? 'text-slate-400 hover:text-slate-300' : 'text-slate-500 hover:text-slate-700')">
          {{ tab.label }}
        </button>
      </div>

      <!-- ===== ASSESSMENT TAB ===== -->
      <div v-if="activeTab === 'assessment'">

        <!-- Assessment Type Selection -->
        <div v-if="!assessmentActive" class="space-y-4">
          <h2 class="text-xl font-bold text-[var(--text-primary)]">Weekly Mental Health Check-in</h2>
          <p class="text-sm text-[var(--text-secondary)]">Take a clinically validated screening to track your mental health over time.</p>

          <div class="grid sm:grid-cols-2 gap-4">
            <!-- PHQ-9 Card -->
            <button @click="startAssessment('phq9')"
              class="rounded-2xl border p-5 text-left transition-all hover:scale-[1.01] hover:shadow-lg"
              :class="isDark ? 'bg-slate-800/60 border-slate-700 hover:border-indigo-600' : 'bg-white border-slate-200 hover:border-indigo-400 shadow-sm'">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">
                  <span class="text-white text-sm font-bold">P9</span>
                </div>
                <div>
                  <h3 class="font-semibold text-[var(--text-primary)]">PHQ-9 Depression Screen</h3>
                  <p class="text-xs text-[var(--text-secondary)]">9 questions ~ 3 min</p>
                </div>
              </div>
              <p class="text-xs text-[var(--text-secondary)]">Patient Health Questionnaire for depression screening. Widely used in clinical settings.</p>
            </button>

            <!-- GAD-7 Card -->
            <button @click="startAssessment('gad7')"
              class="rounded-2xl border p-5 text-left transition-all hover:scale-[1.01] hover:shadow-lg"
              :class="isDark ? 'bg-slate-800/60 border-slate-700 hover:border-teal-600' : 'bg-white border-slate-200 hover:border-teal-400 shadow-sm'">
              <div class="flex items-center gap-3 mb-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center">
                  <span class="text-white text-sm font-bold">G7</span>
                </div>
                <div>
                  <h3 class="font-semibold text-[var(--text-primary)]">GAD-7 Anxiety Screen</h3>
                  <p class="text-xs text-[var(--text-secondary)]">7 questions ~ 2 min</p>
                </div>
              </div>
              <p class="text-xs text-[var(--text-secondary)]">Generalized Anxiety Disorder scale. Standard measure for anxiety severity.</p>
            </button>
          </div>

          <!-- Past Scores Summary -->
          <div v-if="scoreHistory.length > 0" class="rounded-2xl border p-5"
            :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
            <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-3">Recent Scores</h3>
            <div class="space-y-2">
              <div v-for="entry in scoreHistory.slice(0, 5)" :key="entry.date + entry.type"
                class="flex items-center justify-between text-sm">
                <div class="flex items-center gap-2">
                  <span class="w-10 text-xs font-mono" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ entry.type.toUpperCase() }}</span>
                  <span class="text-[var(--text-secondary)]">{{ formatDate(entry.date) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="font-semibold" :style="{ color: getSeverityColor(entry.score, entry.type) }">{{ entry.score }}</span>
                  <span class="text-xs px-2 py-0.5 rounded-full"
                    :style="{ background: getSeverityColor(entry.score, entry.type) + '20', color: getSeverityColor(entry.score, entry.type) }">
                    {{ getSeverityLabel(entry.score, entry.type) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Active Assessment Stepper -->
        <div v-else class="space-y-6">
          <!-- Progress Bar -->
          <div class="space-y-2">
            <div class="flex items-center justify-between text-xs text-[var(--text-secondary)]">
              <span>{{ currentAssessmentLabel }}</span>
              <span>Question {{ currentQuestion + 1 }} of {{ currentQuestions.length }}</span>
            </div>
            <div class="h-2 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
              <div class="h-full rounded-full transition-all duration-500 ease-out"
                :class="assessmentType === 'phq9' ? 'bg-gradient-to-r from-indigo-500 to-purple-500' : 'bg-gradient-to-r from-teal-500 to-emerald-500'"
                :style="{ width: ((currentQuestion + 1) / currentQuestions.length * 100) + '%' }"></div>
            </div>
          </div>

          <!-- Question Card -->
          <div class="rounded-2xl border p-6 sm:p-8 transition-all"
            :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
            <p class="text-sm text-[var(--text-secondary)] mb-2">Over the last 2 weeks, how often have you been bothered by:</p>
            <h3 class="text-lg font-semibold text-[var(--text-primary)] mb-6">
              {{ currentQuestions[currentQuestion] }}
            </h3>

            <div class="space-y-3">
              <button v-for="option in answerOptions" :key="option.value"
                @click="answerQuestion(option.value)"
                class="w-full text-left px-5 py-3.5 rounded-xl border text-sm font-medium transition-all"
                :class="answers[currentQuestion] === option.value
                  ? (isDark ? 'border-indigo-500 bg-indigo-500/15 text-indigo-300' : 'border-indigo-500 bg-indigo-50 text-indigo-700')
                  : (isDark ? 'border-slate-600 hover:border-slate-500 text-slate-300 hover:bg-slate-700/50' : 'border-slate-200 hover:border-slate-300 text-slate-700 hover:bg-slate-50')">
                <span class="inline-flex items-center gap-3">
                  <span class="w-7 h-7 rounded-lg flex items-center justify-center text-xs font-bold"
                    :class="answers[currentQuestion] === option.value
                      ? (isDark ? 'bg-indigo-500/30 text-indigo-300' : 'bg-indigo-100 text-indigo-600')
                      : (isDark ? 'bg-slate-700 text-slate-400' : 'bg-slate-100 text-slate-500')">
                    {{ option.value }}
                  </span>
                  {{ option.label }}
                </span>
              </button>
            </div>
          </div>

          <!-- Navigation -->
          <div class="flex items-center justify-between">
            <button @click="prevQuestion"
              :disabled="currentQuestion === 0"
              class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
              :class="currentQuestion === 0
                ? 'opacity-30 cursor-not-allowed text-[var(--text-secondary)]'
                : (isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-100')">
              Back
            </button>
            <button @click="cancelAssessment"
              class="px-4 py-2 rounded-xl text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
              Cancel
            </button>
          </div>
        </div>

        <!-- Results Card -->
        <div v-if="latestResult" class="rounded-2xl border p-6 mt-6"
          :style="{ borderColor: getSeverityColor(latestResult.score, latestResult.type) + '60' }"
          :class="isDark ? 'bg-slate-800/60' : 'bg-white shadow-sm'">
          <div class="flex items-start justify-between mb-4">
            <div>
              <h3 class="font-bold text-[var(--text-primary)]">{{ latestResult.type === 'phq9' ? 'PHQ-9' : 'GAD-7' }} Results</h3>
              <p class="text-xs text-[var(--text-secondary)] mt-0.5">Completed {{ formatDate(latestResult.date) }}</p>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold" :style="{ color: getSeverityColor(latestResult.score, latestResult.type) }">
                {{ latestResult.score }}
              </div>
              <div class="text-xs" :style="{ color: getSeverityColor(latestResult.score, latestResult.type) }">
                / {{ latestResult.type === 'phq9' ? '27' : '21' }}
              </div>
            </div>
          </div>

          <div class="rounded-xl px-4 py-3 mb-4"
            :style="{ background: getSeverityColor(latestResult.score, latestResult.type) + '15' }">
            <p class="text-sm font-semibold" :style="{ color: getSeverityColor(latestResult.score, latestResult.type) }">
              {{ getSeverityLabel(latestResult.score, latestResult.type) }}
            </p>
            <p class="text-xs mt-1 text-[var(--text-secondary)]">{{ getSeverityRecommendation(latestResult.score, latestResult.type) }}</p>
          </div>

          <button @click="latestResult = null" class="text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">
            Dismiss
          </button>
        </div>
      </div>

      <!-- ===== MOOD TRACKER TAB ===== -->
      <div v-if="activeTab === 'mood'">
        <h2 class="text-xl font-bold text-[var(--text-primary)] mb-1">Daily Mood Tracker</h2>
        <p class="text-sm text-[var(--text-secondary)] mb-6">Track how you feel each day to spot patterns over time.</p>

        <!-- Today's Mood Entry -->
        <div class="rounded-2xl border p-6 mb-6"
          :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4">How are you feeling today?</h3>
          <div class="flex items-center justify-center gap-3 sm:gap-5 mb-5">
            <button v-for="mood in moodOptions" :key="mood.value"
              @click="selectedMood = mood.value"
              class="flex flex-col items-center gap-1.5 p-3 rounded-xl transition-all"
              :class="selectedMood === mood.value
                ? 'scale-110 shadow-lg ' + (isDark ? 'bg-slate-700' : 'bg-slate-100')
                : 'hover:scale-105 ' + (isDark ? 'hover:bg-slate-800' : 'hover:bg-slate-50')">
              <span class="text-3xl">{{ mood.emoji }}</span>
              <span class="text-[10px] font-medium" :class="selectedMood === mood.value ? 'text-[var(--text-primary)]' : 'text-[var(--text-secondary)]'">
                {{ mood.label }}
              </span>
            </button>
          </div>

          <div class="mb-4">
            <label class="block text-xs font-medium text-[var(--text-secondary)] mb-1.5">What's on your mind? (optional)</label>
            <textarea v-model="journalEntry" rows="3" placeholder="Write anything you'd like to remember about today..."
              class="w-full px-4 py-3 rounded-xl border text-sm outline-none transition-colors resize-none"
              :class="isDark
                ? 'bg-slate-900/60 border-slate-600 text-white placeholder-slate-500 focus:border-indigo-500'
                : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400 focus:border-indigo-500'"></textarea>
          </div>

          <button @click="saveMoodEntry" :disabled="!selectedMood"
            class="px-6 py-2.5 rounded-xl text-sm font-semibold transition-all"
            :class="selectedMood
              ? 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:shadow-lg hover:shadow-indigo-500/25'
              : 'opacity-40 cursor-not-allowed ' + (isDark ? 'bg-slate-700 text-slate-500' : 'bg-slate-200 text-slate-400')">
            Log Today's Mood
          </button>

          <div v-if="moodSaved" class="mt-3 text-xs font-medium" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">
            Mood logged successfully!
          </div>
        </div>

        <!-- 30-Day Mood Calendar -->
        <div class="rounded-2xl border p-5 mb-6"
          :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4">30-Day Mood Calendar</h3>
          <div class="grid grid-cols-7 gap-1.5">
            <div v-for="(day, di) in ['S','M','T','W','T','F','S']" :key="'h'+di" class="text-center text-[10px] font-medium text-[var(--text-secondary)] pb-1">{{ day }}</div>
            <div v-for="(cell, idx) in calendarCells" :key="idx"
              class="aspect-square rounded-lg flex items-center justify-center text-xs relative group cursor-default"
              :class="cell.empty ? 'opacity-0' : ''"
              :style="cell.mood ? { background: getMoodColor(cell.mood) + '30' } : {}">
              <span v-if="!cell.empty" class="text-[10px]" :class="cell.isToday ? 'font-bold text-[var(--text-primary)]' : 'text-[var(--text-secondary)]'">
                {{ cell.day }}
              </span>
              <span v-if="cell.mood" class="absolute -top-1 -right-1 text-xs">{{ getMoodEmoji(cell.mood) }}</span>
              <!-- Tooltip -->
              <div v-if="cell.journal" class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 rounded-lg text-xs max-w-48 hidden group-hover:block z-30 whitespace-normal"
                :class="isDark ? 'bg-slate-700 text-slate-200 shadow-lg' : 'bg-white text-slate-700 shadow-lg border border-slate-200'">
                {{ cell.journal }}
              </div>
            </div>
          </div>
        </div>

        <!-- Weekly Trend -->
        <div class="rounded-2xl border p-5"
          :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4">Weekly Mood Trend</h3>
          <div class="flex items-end gap-2 h-28">
            <div v-for="(bar, idx) in weeklyTrend" :key="idx" class="flex-1 flex flex-col items-center gap-1">
              <div class="w-full rounded-t-lg transition-all duration-500"
                :style="{ height: (bar.avg / 5 * 100) + '%', background: getMoodColor(bar.avg) }"
                :class="!bar.avg ? 'opacity-20' : ''"></div>
              <span class="text-[9px] text-[var(--text-secondary)]">{{ bar.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== WELLNESS TAB ===== -->
      <div v-if="activeTab === 'wellness'">
        <h2 class="text-xl font-bold text-[var(--text-primary)] mb-1">AI Wellness Recommendations</h2>
        <p class="text-sm text-[var(--text-secondary)] mb-6">Personalized suggestions based on your recent screenings.</p>

        <!-- Breathing Exercise -->
        <div class="rounded-2xl border p-6 mb-6"
          :class="isDark ? 'bg-slate-800/60 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-2">Breathing Exercise</h3>
          <p class="text-xs text-[var(--text-secondary)] mb-5">4-7-8 technique: breathe in for 4s, hold for 7s, exhale for 8s.</p>

          <div class="flex flex-col items-center">
            <!-- Breathing circle -->
            <div class="relative w-40 h-40 mb-4">
              <div class="absolute inset-0 rounded-full border-2 transition-all duration-1000"
                :class="breathPhase === 'inhale' ? 'scale-100' : breathPhase === 'hold' ? 'scale-100' : breathPhase === 'exhale' ? 'scale-75' : 'scale-90'"
                :style="{ borderColor: breathPhaseColor }">
              </div>
              <div class="absolute inset-4 rounded-full transition-all duration-1000 flex items-center justify-center"
                :class="breathPhase === 'inhale' ? 'scale-100' : breathPhase === 'hold' ? 'scale-100' : breathPhase === 'exhale' ? 'scale-75' : 'scale-90'"
                :style="{ background: breathPhaseColor + '20' }">
                <div class="text-center">
                  <p class="text-lg font-bold text-[var(--text-primary)]">{{ breathTimer }}s</p>
                  <p class="text-xs font-medium" :style="{ color: breathPhaseColor }">
                    {{ breathPhase === 'inhale' ? 'Breathe In' : breathPhase === 'hold' ? 'Hold' : breathPhase === 'exhale' ? 'Breathe Out' : 'Ready' }}
                  </p>
                </div>
              </div>
            </div>

            <div class="flex gap-3">
              <button @click="startBreathing" v-if="!breathingActive"
                class="px-5 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:shadow-lg transition-all">
                Start Exercise
              </button>
              <button @click="stopBreathing" v-else
                class="px-5 py-2 rounded-xl text-sm font-medium transition-colors"
                :class="isDark ? 'bg-slate-700 text-slate-300 hover:bg-slate-600' : 'bg-slate-200 text-slate-700 hover:bg-slate-300'">
                Stop
              </button>
            </div>
            <p class="text-xs text-[var(--text-secondary)] mt-2">Cycle {{ breathCycles }} / 4</p>
          </div>
        </div>

        <!-- Personalized Recommendations -->
        <div class="grid sm:grid-cols-2 gap-4 mb-6">
          <div v-for="rec in wellnessRecommendations" :key="rec.title"
            class="rounded-2xl border p-5 transition-colors"
            :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
            <div class="flex items-center gap-2 mb-3">
              <span class="text-xl">{{ rec.icon }}</span>
              <h4 class="text-sm font-semibold text-[var(--text-primary)]">{{ rec.title }}</h4>
            </div>
            <ul class="space-y-1.5">
              <li v-for="(tip, i) in rec.tips" :key="i" class="text-xs text-[var(--text-secondary)] flex items-start gap-1.5">
                <span class="w-1 h-1 rounded-full mt-1.5 flex-shrink-0" :class="isDark ? 'bg-indigo-400' : 'bg-indigo-500'"></span>
                {{ tip }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Crisis Resources -->
        <div class="rounded-2xl border p-5"
          :class="isDark ? 'bg-indigo-950/30 border-indigo-800/40' : 'bg-indigo-50/80 border-indigo-200'">
          <h3 class="text-sm font-semibold mb-3" :class="isDark ? 'text-indigo-300' : 'text-indigo-800'">Talk to Someone</h3>
          <div class="space-y-2">
            <div class="flex items-center gap-3 text-sm">
              <span class="font-medium" :class="isDark ? 'text-indigo-200' : 'text-indigo-900'">988 Suicide &amp; Crisis Lifeline:</span>
              <a href="tel:988" class="font-bold underline" :class="isDark ? 'text-indigo-300' : 'text-indigo-700'">Call or text 988</a>
            </div>
            <div class="flex items-center gap-3 text-sm">
              <span class="font-medium" :class="isDark ? 'text-indigo-200' : 'text-indigo-900'">Crisis Text Line:</span>
              <span class="font-bold" :class="isDark ? 'text-indigo-300' : 'text-indigo-700'">Text HOME to 741741</span>
            </div>
            <div class="flex items-center gap-3 text-sm">
              <span class="font-medium" :class="isDark ? 'text-indigo-200' : 'text-indigo-900'">SAMHSA Helpline:</span>
              <a href="tel:1-800-662-4357" class="font-bold underline" :class="isDark ? 'text-indigo-300' : 'text-indigo-700'">1-800-662-4357</a>
            </div>
          </div>
        </div>
      </div>

      <!-- ===== PROGRESS TAB ===== -->
      <div v-if="activeTab === 'progress'">
        <h2 class="text-xl font-bold text-[var(--text-primary)] mb-1">Progress Over Time</h2>
        <p class="text-sm text-[var(--text-secondary)] mb-6">Track your mental health journey.</p>

        <!-- Milestones -->
        <div v-if="milestones.length > 0" class="flex flex-wrap gap-2 mb-6">
          <div v-for="m in milestones" :key="m.text"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium"
            :class="isDark ? 'bg-purple-500/15 text-purple-300' : 'bg-purple-50 text-purple-700'">
            <span>{{ m.icon }}</span> {{ m.text }}
          </div>
        </div>

        <!-- Score History Chart -->
        <div class="rounded-2xl border p-5 mb-6"
          :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4">Score History</h3>

          <div v-if="scoreHistory.length < 2" class="py-8 text-center">
            <p class="text-sm text-[var(--text-secondary)]">Complete at least 2 assessments to see your trend chart.</p>
          </div>

          <div v-else class="space-y-6">
            <!-- PHQ-9 Chart -->
            <div v-if="phq9History.length > 0">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full bg-indigo-500"></div>
                <span class="text-xs font-medium text-[var(--text-secondary)]">PHQ-9 Depression</span>
              </div>
              <div class="flex items-end gap-1 h-24">
                <div v-for="(pt, idx) in phq9History" :key="'p'+idx"
                  class="flex-1 flex flex-col items-center gap-1 group relative">
                  <div class="w-full rounded-t-md bg-indigo-500/80 transition-all"
                    :style="{ height: Math.max(4, pt.score / 27 * 100) + '%' }"></div>
                  <span class="text-[8px] text-[var(--text-secondary)]">{{ formatShortDate(pt.date) }}</span>
                  <div class="absolute bottom-full mb-1 px-2 py-1 rounded text-[10px] font-medium hidden group-hover:block z-10"
                    :class="isDark ? 'bg-slate-700 text-white' : 'bg-slate-800 text-white'">
                    {{ pt.score }} - {{ getSeverityLabel(pt.score, 'phq9') }}
                  </div>
                </div>
              </div>
            </div>

            <!-- GAD-7 Chart -->
            <div v-if="gad7History.length > 0">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-3 h-3 rounded-full bg-teal-500"></div>
                <span class="text-xs font-medium text-[var(--text-secondary)]">GAD-7 Anxiety</span>
              </div>
              <div class="flex items-end gap-1 h-24">
                <div v-for="(pt, idx) in gad7History" :key="'g'+idx"
                  class="flex-1 flex flex-col items-center gap-1 group relative">
                  <div class="w-full rounded-t-md bg-teal-500/80 transition-all"
                    :style="{ height: Math.max(4, pt.score / 21 * 100) + '%' }"></div>
                  <span class="text-[8px] text-[var(--text-secondary)]">{{ formatShortDate(pt.date) }}</span>
                  <div class="absolute bottom-full mb-1 px-2 py-1 rounded text-[10px] font-medium hidden group-hover:block z-10"
                    :class="isDark ? 'bg-slate-700 text-white' : 'bg-slate-800 text-white'">
                    {{ pt.score }} - {{ getSeverityLabel(pt.score, 'gad7') }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Improvement callout -->
            <div v-if="improvementText" class="rounded-xl px-4 py-3"
              :class="isDark ? 'bg-emerald-900/20 border border-emerald-800/40' : 'bg-emerald-50 border border-emerald-200'">
              <p class="text-sm font-medium" :class="isDark ? 'text-emerald-400' : 'text-emerald-700'">{{ improvementText }}</p>
            </div>
          </div>
        </div>

        <!-- Check-in Streak -->
        <div class="rounded-2xl border p-5"
          :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200 shadow-sm'">
          <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-3">Check-in Activity</h3>
          <div class="grid grid-cols-3 gap-4 text-center">
            <div>
              <div class="text-2xl font-bold text-[var(--text-primary)]">{{ scoreHistory.length }}</div>
              <div class="text-xs text-[var(--text-secondary)]">Total Screenings</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-[var(--text-primary)]">{{ moodEntries.length }}</div>
              <div class="text-xs text-[var(--text-secondary)]">Mood Entries</div>
            </div>
            <div>
              <div class="text-2xl font-bold" :class="isDark ? 'text-purple-400' : 'text-purple-600'">{{ currentStreak }}</div>
              <div class="text-xs text-[var(--text-secondary)]">Day Streak</div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useTheme } from '@/composables/useTheme'
import ThemeLangControls from '@/components/ThemeLangControls.vue'

const { isDark } = useTheme()

// ── Data Storage ──────────────────────────────────────────────
const STORAGE_KEY = 'mental_health_data'

function loadData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { scores: [], moods: [] }
    return JSON.parse(raw)
  } catch { return { scores: [], moods: [] } }
}

function saveData(data) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)) } catch { /* storage full */ }
}

// ── Tabs ──────────────────────────────────────────────────────
const tabs = [
  { id: 'assessment', label: 'Assessment' },
  { id: 'mood', label: 'Mood Tracker' },
  { id: 'wellness', label: 'Wellness' },
  { id: 'progress', label: 'Progress' }
]
const activeTab = ref('assessment')

// ── PHQ-9 Questions ───────────────────────────────────────────
const phq9Questions = [
  'Little interest or pleasure in doing things',
  'Feeling down, depressed, or hopeless',
  'Trouble falling or staying asleep, or sleeping too much',
  'Feeling tired or having little energy',
  'Poor appetite or overeating',
  'Feeling bad about yourself \u2014 or that you are a failure or have let yourself or your family down',
  'Trouble concentrating on things, such as reading the newspaper or watching television',
  'Moving or speaking so slowly that other people could have noticed? Or the opposite \u2014 being so fidgety or restless that you have been moving around a lot more than usual',
  'Thoughts that you would be better off dead, or of hurting yourself in some way'
]

// ── GAD-7 Questions ───────────────────────────────────────────
const gad7Questions = [
  'Feeling nervous, anxious, or on edge',
  'Not being able to stop or control worrying',
  'Worrying too much about different things',
  'Trouble relaxing',
  'Being so restless that it is hard to sit still',
  'Becoming easily annoyed or irritable',
  'Feeling afraid, as if something awful might happen'
]

const answerOptions = [
  { value: 0, label: 'Not at all' },
  { value: 1, label: 'Several days' },
  { value: 2, label: 'More than half the days' },
  { value: 3, label: 'Nearly every day' }
]

// ── Assessment State ──────────────────────────────────────────
const assessmentActive = ref(false)
const assessmentType = ref('')
const currentQuestion = ref(0)
const answers = ref([])
const latestResult = ref(null)

const currentQuestions = computed(() => assessmentType.value === 'phq9' ? phq9Questions : gad7Questions)
const currentAssessmentLabel = computed(() => assessmentType.value === 'phq9' ? 'PHQ-9 Depression Screening' : 'GAD-7 Anxiety Screening')

function startAssessment(type) {
  assessmentType.value = type
  currentQuestion.value = 0
  answers.value = new Array(type === 'phq9' ? 9 : 7).fill(null)
  assessmentActive.value = true
  latestResult.value = null
}

function answerQuestion(value) {
  answers.value[currentQuestion.value] = value
  if (currentQuestion.value < currentQuestions.value.length - 1) {
    currentQuestion.value++
  } else {
    finishAssessment()
  }
}

function prevQuestion() {
  if (currentQuestion.value > 0) currentQuestion.value--
}

function cancelAssessment() {
  assessmentActive.value = false
  assessmentType.value = ''
}

function finishAssessment() {
  const score = answers.value.reduce((sum, v) => sum + (v || 0), 0)
  const entry = {
    type: assessmentType.value,
    score,
    answers: [...answers.value],
    date: new Date().toISOString()
  }

  const data = loadData()
  data.scores.unshift(entry)
  saveData(data)

  latestResult.value = entry
  assessmentActive.value = false
  assessmentType.value = ''

  refreshData()
}

// ── Score History ─────────────────────────────────────────────
const scoreHistory = ref([])
const moodEntries = ref([])

function refreshData() {
  const data = loadData()
  scoreHistory.value = data.scores || []
  moodEntries.value = data.moods || []
}

onMounted(refreshData)

const phq9History = computed(() => scoreHistory.value.filter(s => s.type === 'phq9').slice(0, 12).reverse())
const gad7History = computed(() => scoreHistory.value.filter(s => s.type === 'gad7').slice(0, 12).reverse())

// ── Severity Helpers ──────────────────────────────────────────
function getSeverityLabel(score, type) {
  if (type === 'gad7') {
    if (score <= 4) return 'Minimal Anxiety'
    if (score <= 9) return 'Mild Anxiety'
    if (score <= 14) return 'Moderate Anxiety'
    return 'Severe Anxiety'
  }
  // PHQ-9
  if (score <= 4) return 'Minimal Depression'
  if (score <= 9) return 'Mild Depression'
  if (score <= 14) return 'Moderate Depression'
  if (score <= 19) return 'Moderately Severe'
  return 'Severe Depression'
}

function getSeverityColor(score, type) {
  const max = type === 'gad7' ? 21 : 27
  const pct = score / max
  if (pct <= 0.19) return '#10b981' // emerald
  if (pct <= 0.38) return '#6366f1' // indigo
  if (pct <= 0.57) return '#8b5cf6' // violet
  if (pct <= 0.76) return '#d97706' // amber
  return '#e879f0' // fuchsia (no harsh red per design spec)
}

function getSeverityRecommendation(score, type) {
  const max = type === 'gad7' ? 21 : 27
  const pct = score / max
  if (pct <= 0.19) return 'Your score suggests minimal symptoms. Continue monitoring and maintain healthy habits.'
  if (pct <= 0.38) return 'Mild symptoms detected. Consider stress-reduction techniques and regular exercise.'
  if (pct <= 0.57) return 'Moderate symptoms. We recommend discussing these results with a healthcare provider.'
  if (pct <= 0.76) return 'Moderately severe symptoms. Please consult a mental health professional for evaluation.'
  return 'Your score indicates severe symptoms. We strongly recommend seeking professional help. You are not alone.'
}

// ── Mood Tracker ──────────────────────────────────────────────
const moodOptions = [
  { value: 1, emoji: '\uD83D\uDE1E', label: 'Awful' },
  { value: 2, emoji: '\uD83D\uDE15', label: 'Bad' },
  { value: 3, emoji: '\uD83D\uDE10', label: 'Okay' },
  { value: 4, emoji: '\uD83D\uDE0A', label: 'Good' },
  { value: 5, emoji: '\uD83D\uDE04', label: 'Great' }
]

const selectedMood = ref(null)
const journalEntry = ref('')
const moodSaved = ref(false)

function saveMoodEntry() {
  if (!selectedMood.value) return
  const data = loadData()
  const today = new Date().toISOString().slice(0, 10)

  const existingIdx = (data.moods || []).findIndex(m => m.date === today)
  const entry = { date: today, mood: selectedMood.value, journal: journalEntry.value }
  if (existingIdx >= 0) {
    data.moods[existingIdx] = entry
  } else {
    if (!data.moods) data.moods = []
    data.moods.unshift(entry)
  }

  saveData(data)
  moodSaved.value = true
  selectedMood.value = null
  journalEntry.value = ''
  refreshData()
  setTimeout(() => { moodSaved.value = false }, 3000)
}

function getMoodColor(value) {
  const v = Math.round(value)
  const colors = { 1: '#8b5cf6', 2: '#a78bfa', 3: '#6366f1', 4: '#10b981', 5: '#059669' }
  return colors[v] || '#6366f1'
}

function getMoodEmoji(value) {
  const m = moodOptions.find(o => o.value === Math.round(value))
  return m ? m.emoji : ''
}

// ── Calendar ──────────────────────────────────────────────────
const calendarCells = computed(() => {
  const cells = []
  const today = new Date()
  const start = new Date(today)
  start.setDate(start.getDate() - 29)

  // Pad start to Sunday
  const padDays = start.getDay()
  for (let i = 0; i < padDays; i++) cells.push({ empty: true })

  for (let i = 0; i < 30; i++) {
    const d = new Date(start)
    d.setDate(start.getDate() + i)
    const key = d.toISOString().slice(0, 10)
    const entry = moodEntries.value.find(m => m.date === key)
    cells.push({
      day: d.getDate(),
      mood: entry ? entry.mood : null,
      journal: entry ? entry.journal : null,
      isToday: key === today.toISOString().slice(0, 10)
    })
  }
  return cells
})

// ── Weekly Trend ──────────────────────────────────────────────
const weeklyTrend = computed(() => {
  const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  const today = new Date()
  return labels.map((label, idx) => {
    const d = new Date(today)
    const dayOfWeek = d.getDay()
    const diff = (idx + 1) - dayOfWeek
    d.setDate(d.getDate() + (diff <= 0 ? diff : diff - 7))
    const key = d.toISOString().slice(0, 10)
    const entry = moodEntries.value.find(m => m.date === key)
    return { label, avg: entry ? entry.mood : 0 }
  })
})

// ── Breathing Exercise ────────────────────────────────────────
const breathingActive = ref(false)
const breathPhase = ref('ready')
const breathTimer = ref(0)
const breathCycles = ref(0)
let breathInterval = null

const breathPhaseColor = computed(() => {
  if (breathPhase.value === 'inhale') return '#818cf8'
  if (breathPhase.value === 'hold') return '#a78bfa'
  if (breathPhase.value === 'exhale') return '#5eead4'
  return '#94a3b8'
})

function startBreathing() {
  breathingActive.value = true
  breathCycles.value = 0
  runBreathCycle()
}

function runBreathCycle() {
  if (breathCycles.value >= 4) { stopBreathing(); return }

  breathPhase.value = 'inhale'
  breathTimer.value = 4
  breathInterval = setInterval(() => {
    breathTimer.value--
    if (breathTimer.value <= 0) {
      clearInterval(breathInterval)
      breathPhase.value = 'hold'
      breathTimer.value = 7
      breathInterval = setInterval(() => {
        breathTimer.value--
        if (breathTimer.value <= 0) {
          clearInterval(breathInterval)
          breathPhase.value = 'exhale'
          breathTimer.value = 8
          breathInterval = setInterval(() => {
            breathTimer.value--
            if (breathTimer.value <= 0) {
              clearInterval(breathInterval)
              breathCycles.value++
              if (breathingActive.value) runBreathCycle()
            }
          }, 1000)
        }
      }, 1000)
    }
  }, 1000)
}

function stopBreathing() {
  breathingActive.value = false
  breathPhase.value = 'ready'
  breathTimer.value = 0
  if (breathInterval) clearInterval(breathInterval)
}

onBeforeUnmount(() => { if (breathInterval) clearInterval(breathInterval) })

// ── Wellness Recommendations ──────────────────────────────────
const wellnessRecommendations = computed(() => {
  const latest = scoreHistory.value[0]
  const score = latest ? latest.score : 0
  const max = latest?.type === 'gad7' ? 21 : 27
  const pct = max ? score / max : 0

  const recs = [
    {
      icon: '\uD83C\uDF19',
      title: 'Sleep Hygiene',
      tips: [
        'Keep a consistent sleep schedule, even on weekends',
        'Avoid screens 1 hour before bed',
        'Keep your bedroom cool, dark, and quiet',
        pct > 0.4 ? 'Consider a relaxation routine before sleep' : 'Aim for 7-9 hours of quality sleep'
      ]
    },
    {
      icon: '\uD83C\uDFC3',
      title: 'Physical Activity',
      tips: [
        'Aim for 30 minutes of moderate activity most days',
        'Walking outdoors combines exercise with nature exposure',
        pct > 0.5 ? 'Even 10 minutes of movement can improve mood' : 'Try activities you enjoy \u2014 consistency matters more than intensity',
        'Yoga and stretching can reduce both anxiety and tension'
      ]
    },
    {
      icon: '\uD83E\uDDD8',
      title: 'Mindfulness & Relaxation',
      tips: [
        'Try the 4-7-8 breathing exercise above',
        'Start with just 5 minutes of daily meditation',
        'Progressive muscle relaxation can ease physical tension',
        'Journaling your thoughts can help process emotions'
      ]
    },
    {
      icon: '\uD83E\uDD1D',
      title: 'Social Connection',
      tips: [
        'Reach out to one person you trust today',
        'Maintain regular social activities even when you don\'t feel like it',
        pct > 0.5 ? 'Support groups can provide understanding and validation' : 'Quality time with loved ones is a powerful mood booster',
        'Volunteering can provide a sense of purpose and connection'
      ]
    }
  ]

  if (pct > 0.5) {
    recs.push({
      icon: '\uD83C\uDFE5',
      title: 'Professional Support',
      tips: [
        'Consider talking to a therapist or counselor',
        'Your primary care doctor can also help with mental health',
        'Cognitive Behavioral Therapy (CBT) is highly effective',
        'Medication may be appropriate \u2014 discuss options with your provider'
      ]
    })
  }

  return recs
})

// ── Progress & Milestones ─────────────────────────────────────
const currentStreak = computed(() => {
  const allDates = new Set()
  moodEntries.value.forEach(m => allDates.add(m.date))
  scoreHistory.value.forEach(s => allDates.add(s.date.slice(0, 10)))

  let streak = 0
  const today = new Date()
  for (let i = 0; i < 365; i++) {
    const d = new Date(today)
    d.setDate(d.getDate() - i)
    const key = d.toISOString().slice(0, 10)
    if (allDates.has(key)) streak++
    else break
  }
  return streak
})

const milestones = computed(() => {
  const m = []
  if (currentStreak.value >= 7) m.push({ icon: '\uD83D\uDD25', text: `${currentStreak.value}-day check-in streak!` })
  if (scoreHistory.value.length >= 4) m.push({ icon: '\uD83D\uDCCA', text: `${scoreHistory.value.length} screenings completed` })
  if (moodEntries.value.length >= 14) m.push({ icon: '\uD83C\uDF1F', text: '2+ weeks of mood tracking' })
  return m
})

const improvementText = computed(() => {
  const phq = phq9History.value
  if (phq.length >= 2) {
    const first = phq[0].score
    const last = phq[phq.length - 1].score
    if (last < first) {
      return `Your PHQ-9 depression score improved from ${first} to ${last} over ${phq.length} check-ins.`
    }
  }
  const gad = gad7History.value
  if (gad.length >= 2) {
    const first = gad[0].score
    const last = gad[gad.length - 1].score
    if (last < first) {
      return `Your GAD-7 anxiety score improved from ${first} to ${last} over ${gad.length} check-ins.`
    }
  }
  return ''
})

// ── Formatting ────────────────────────────────────────────────
function formatDate(iso) {
  try { return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) } catch { return iso }
}

function formatShortDate(iso) {
  try { return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) } catch { return '' }
}
</script>
