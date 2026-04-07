<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-emerald-600/8' : 'bg-emerald-400/12'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-teal-600/6' : 'bg-teal-400/10'"></div>
      <div class="absolute top-1/2 right-1/3 w-64 h-64 rounded-full blur-[100px]"
        :class="isDark ? 'bg-lime-600/4' : 'bg-lime-400/8'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="sticky top-0 z-50 flex items-center justify-between px-6 py-3 border-b backdrop-blur-xl"
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
        <span class="text-sm font-medium hidden sm:inline text-[var(--text-secondary)]">Nutrition Planner</span>
      </div>
      <div class="flex items-center gap-2">
        <router-link to="/journal" class="text-xs px-3 py-1.5 rounded-lg transition-colors hidden sm:inline"
          :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
          Symptom Journal
        </router-link>
        <ThemeLangControls />
        <router-link to="/consult"
          class="hidden sm:flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white shadow-lg shadow-emerald-500/20 hover:shadow-xl transition-all">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          Consult
        </router-link>
      </div>
    </nav>

    <!-- Main content -->
    <div class="relative z-10 max-w-5xl mx-auto px-4 py-6 space-y-6">

      <!-- ======= SECTION 1: Diet Profile ======= -->
      <section class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-800 bg-emerald-500/5' : 'border-slate-200 bg-emerald-50/50'">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center text-white text-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-[var(--text-primary)]">Personalized Diet Profile</h2>
            <p class="text-xs text-[var(--text-secondary)]">Customize your plan based on your health data</p>
          </div>
        </div>
        <div class="p-6 space-y-5">
          <!-- User info row -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div class="rounded-xl p-3 text-center border"
              :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
              <div class="text-xs text-[var(--text-secondary)] mb-1">Age</div>
              <div class="text-lg font-bold text-[var(--text-primary)]">{{ profile.age || '--' }}</div>
            </div>
            <div class="rounded-xl p-3 text-center border"
              :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
              <div class="text-xs text-[var(--text-secondary)] mb-1">Gender</div>
              <div class="text-lg font-bold text-[var(--text-primary)] capitalize">{{ profile.gender || '--' }}</div>
            </div>
            <div class="rounded-xl p-3 text-center border"
              :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
              <div class="text-xs text-[var(--text-secondary)] mb-1">Allergies</div>
              <div class="text-lg font-bold text-[var(--text-primary)]">{{ profile.allergies.length || 0 }}</div>
            </div>
            <div class="rounded-xl p-3 text-center border"
              :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
              <div class="text-xs text-[var(--text-secondary)] mb-1">Medications</div>
              <div class="text-lg font-bold text-[var(--text-primary)]">{{ profile.medications.length || 0 }}</div>
            </div>
          </div>

          <!-- Diet Goal -->
          <div>
            <label class="text-sm font-semibold text-[var(--text-primary)] mb-2 block">Diet Goal</label>
            <div class="flex flex-wrap gap-2">
              <button v-for="goal in dietGoals" :key="goal.value"
                @click="selectedGoal = goal.value"
                class="px-4 py-2 rounded-xl text-sm font-medium border transition-all duration-200"
                :class="selectedGoal === goal.value
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white border-transparent shadow-lg shadow-emerald-500/20'
                  : isDark ? 'border-slate-700 text-slate-300 hover:border-emerald-500/50 hover:text-emerald-400' : 'border-slate-300 text-slate-600 hover:border-emerald-400 hover:text-emerald-600'">
                {{ goal.emoji }} {{ goal.label }}
              </button>
            </div>
          </div>

          <!-- Dietary Restrictions -->
          <div>
            <label class="text-sm font-semibold text-[var(--text-primary)] mb-2 block">Dietary Restrictions</label>
            <div class="flex flex-wrap gap-2">
              <button v-for="r in dietaryRestrictions" :key="r.value"
                @click="toggleRestriction(r.value)"
                class="px-3 py-1.5 rounded-lg text-xs font-medium border transition-all duration-200"
                :class="selectedRestrictions.includes(r.value)
                  ? isDark ? 'bg-teal-500/20 border-teal-500/50 text-teal-300' : 'bg-teal-50 border-teal-300 text-teal-700'
                  : isDark ? 'border-slate-700 text-slate-400 hover:border-slate-600' : 'border-slate-300 text-slate-500 hover:border-slate-400'">
                {{ r.emoji }} {{ r.label }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- ======= SECTION 2: AI Meal Plan Generator ======= -->
      <section class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center justify-between"
          :class="isDark ? 'border-slate-800 bg-lime-500/5' : 'border-slate-200 bg-lime-50/50'">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-lime-500 to-emerald-600 flex items-center justify-center text-white text-lg">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            </div>
            <div>
              <h2 class="text-lg font-bold text-[var(--text-primary)]">7-Day Meal Plan</h2>
              <p class="text-xs text-[var(--text-secondary)]">AI-generated meals tailored to your profile</p>
            </div>
          </div>
          <button @click="generateMealPlan" :disabled="generating"
            class="flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-200 bg-gradient-to-r from-emerald-500 to-teal-600 text-white shadow-lg shadow-emerald-500/20 hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed">
            <svg v-if="generating" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
            {{ generating ? 'Generating...' : 'Generate Plan' }}
          </button>
        </div>

        <!-- Meal plan content -->
        <div v-if="mealPlan" class="p-6">
          <!-- Calorie target bar -->
          <div class="mb-6 p-4 rounded-xl border"
            :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-semibold text-[var(--text-primary)]">Daily Target</span>
              <span class="text-sm font-bold text-emerald-500">{{ mealPlan.calorie_target }} kcal</span>
            </div>
            <div class="w-full h-2 rounded-full overflow-hidden"
              :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
              <div class="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-500"
                style="width: 100%"></div>
            </div>
          </div>

          <!-- Day selector tabs -->
          <div class="flex gap-1 mb-5 overflow-x-auto pb-2">
            <button v-for="(day, idx) in mealPlan.days" :key="idx"
              @click="selectedDay = idx"
              class="flex-shrink-0 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-200"
              :class="selectedDay === idx
                ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white shadow-lg shadow-emerald-500/20'
                : isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
              {{ day.day.slice(0, 3) }}
            </button>
          </div>

          <!-- Selected day meals -->
          <div v-if="currentDay" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="mealType in ['breakfast', 'lunch', 'dinner']" :key="mealType"
              class="rounded-xl border p-4 transition-all duration-200 hover:shadow-md"
              :class="isDark ? 'bg-slate-800/40 border-slate-700 hover:border-slate-600' : 'bg-white border-slate-200 hover:border-slate-300'">
              <div class="flex items-center gap-3 mb-3">
                <span class="text-2xl">{{ currentDay[mealType]?.emoji || mealTypeEmoji(mealType) }}</span>
                <div>
                  <div class="text-[10px] uppercase tracking-wider font-bold"
                    :class="mealType === 'breakfast' ? 'text-amber-500' : mealType === 'lunch' ? 'text-blue-500' : 'text-purple-500'">
                    {{ mealType }}
                  </div>
                  <div class="text-sm font-bold text-[var(--text-primary)]">{{ currentDay[mealType]?.name }}</div>
                </div>
              </div>
              <div class="flex items-center gap-2 mb-3 text-xs text-[var(--text-secondary)]">
                <span class="flex items-center gap-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  {{ currentDay[mealType]?.prep_time }}
                </span>
                <span class="font-semibold text-emerald-500">{{ currentDay[mealType]?.calories }} kcal</span>
              </div>
              <!-- Nutrition bars -->
              <div class="space-y-1.5">
                <div v-for="nut in nutrientDefs" :key="nut.key" class="flex items-center gap-2">
                  <span class="text-[10px] w-12 text-right text-[var(--text-secondary)]">{{ nut.label }}</span>
                  <div class="flex-1 h-1.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
                    <div class="h-full rounded-full transition-all" :class="nut.color" :style="{ width: nutrientPercent(currentDay[mealType]?.[nut.key], nut.max) + '%' }"></div>
                  </div>
                  <span class="text-[10px] w-8 text-[var(--text-secondary)]">{{ currentDay[mealType]?.[nut.key] }}g</span>
                </div>
              </div>
            </div>

            <!-- Snacks card -->
            <div class="rounded-xl border p-4"
              :class="isDark ? 'bg-slate-800/40 border-slate-700' : 'bg-white border-slate-200'">
              <div class="flex items-center gap-3 mb-3">
                <span class="text-2xl">{{ currentDay.snacks?.[0]?.emoji || '&#x1F37F;' }}</span>
                <div>
                  <div class="text-[10px] uppercase tracking-wider font-bold text-emerald-500">Snacks</div>
                  <div class="text-sm font-bold text-[var(--text-primary)]">{{ currentDay.snacks?.[0]?.name }}</div>
                </div>
              </div>
              <div class="text-xs text-[var(--text-secondary)] mb-2">{{ currentDay.snacks?.[0]?.calories }} kcal</div>
              <!-- Daily totals -->
              <div class="mt-4 pt-3 border-t" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
                <div class="text-[10px] uppercase tracking-wider font-bold text-[var(--text-secondary)] mb-2">Daily Totals</div>
                <div class="grid grid-cols-2 gap-2 text-xs">
                  <div class="flex justify-between"><span class="text-[var(--text-secondary)]">Calories</span><span class="font-bold text-emerald-500">{{ currentDay.totals?.calories }}</span></div>
                  <div class="flex justify-between"><span class="text-[var(--text-secondary)]">Protein</span><span class="font-bold text-red-400">{{ currentDay.totals?.protein }}g</span></div>
                  <div class="flex justify-between"><span class="text-[var(--text-secondary)]">Carbs</span><span class="font-bold text-amber-400">{{ currentDay.totals?.carbs }}g</span></div>
                  <div class="flex justify-between"><span class="text-[var(--text-secondary)]">Fats</span><span class="font-bold text-blue-400">{{ currentDay.totals?.fats }}g</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else class="p-12 text-center">
          <div class="w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center"
            :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
            <span class="text-3xl">&#x1F957;</span>
          </div>
          <h3 class="text-lg font-semibold mb-2 text-[var(--text-primary)]">No Meal Plan Yet</h3>
          <p class="text-sm text-[var(--text-secondary)] max-w-sm mx-auto">Select your diet goals and dietary restrictions above, then click "Generate Plan" to create a personalized 7-day meal plan.</p>
        </div>
      </section>

      <!-- ======= SECTION 3: Condition-Specific Nutrition ======= -->
      <section v-if="mealPlan && Object.keys(mealPlan.condition_recommendations || {}).length > 0"
        class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-800 bg-orange-500/5' : 'border-slate-200 bg-orange-50/50'">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-[var(--text-primary)]">Condition-Specific Nutrition</h2>
            <p class="text-xs text-[var(--text-secondary)]">Dietary recommendations based on your health conditions</p>
          </div>
        </div>
        <div class="p-6 space-y-5">
          <div v-for="(recs, condition) in mealPlan.condition_recommendations" :key="condition"
            class="rounded-xl border p-5"
            :class="isDark ? 'bg-slate-800/30 border-slate-700' : 'bg-white border-slate-200'">
            <h3 class="text-sm font-bold text-[var(--text-primary)] mb-4 capitalize">
              Based on your condition: <span class="text-orange-500">{{ condition }}</span>
            </h3>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <!-- Foods to eat -->
              <div class="rounded-xl p-4 border"
                :class="isDark ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-emerald-50 border-emerald-100'">
                <h4 class="text-xs font-bold flex items-center gap-1.5 mb-2"
                  :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Eat More
                </h4>
                <ul class="space-y-1">
                  <li v-for="item in recs.eat" :key="item" class="text-xs"
                    :class="isDark ? 'text-emerald-300/80' : 'text-emerald-700'">{{ item }}</li>
                </ul>
              </div>
              <!-- Foods to avoid -->
              <div class="rounded-xl p-4 border"
                :class="isDark ? 'bg-red-500/5 border-red-500/20' : 'bg-red-50 border-red-100'">
                <h4 class="text-xs font-bold flex items-center gap-1.5 mb-2"
                  :class="isDark ? 'text-red-400' : 'text-red-600'">
                  <span class="w-2 h-2 rounded-full bg-red-500"></span> Avoid
                </h4>
                <ul class="space-y-1">
                  <li v-for="item in recs.avoid" :key="item" class="text-xs"
                    :class="isDark ? 'text-red-300/80' : 'text-red-700'">{{ item }}</li>
                </ul>
              </div>
              <!-- Foods in moderation -->
              <div class="rounded-xl p-4 border"
                :class="isDark ? 'bg-amber-500/5 border-amber-500/20' : 'bg-amber-50 border-amber-100'">
                <h4 class="text-xs font-bold flex items-center gap-1.5 mb-2"
                  :class="isDark ? 'text-amber-400' : 'text-amber-600'">
                  <span class="w-2 h-2 rounded-full bg-amber-500"></span> Moderation
                </h4>
                <ul class="space-y-1">
                  <li v-for="item in recs.moderate" :key="item" class="text-xs"
                    :class="isDark ? 'text-amber-300/80' : 'text-amber-700'">{{ item }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ======= SECTION 4: Medication-Food Interactions ======= -->
      <section v-if="mealPlan && Object.keys(mealPlan.medication_interactions || {}).length > 0"
        class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-800 bg-purple-500/5' : 'border-slate-200 bg-purple-50/50'">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-[var(--text-primary)]">Medication-Food Interactions</h2>
            <p class="text-xs text-[var(--text-secondary)]">Important dietary considerations for your medications</p>
          </div>
        </div>
        <div class="p-6 space-y-3">
          <div v-for="(info, med) in mealPlan.medication_interactions" :key="med"
            class="rounded-xl border p-4 flex flex-col sm:flex-row gap-4"
            :class="isDark ? 'bg-slate-800/30 border-slate-700' : 'bg-white border-slate-200'">
            <div class="flex items-center gap-3 sm:w-48 flex-shrink-0">
              <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white text-sm font-bold">
                {{ med[0].toUpperCase() }}
              </div>
              <div class="font-bold text-sm text-[var(--text-primary)] capitalize">{{ med }}</div>
            </div>
            <div class="flex-1 space-y-2">
              <div class="flex flex-wrap gap-1.5">
                <span v-for="item in info.avoid" :key="item"
                  class="px-2 py-0.5 rounded-md text-[10px] font-medium"
                  :class="isDark ? 'bg-red-500/15 text-red-300 border border-red-500/20' : 'bg-red-50 text-red-600 border border-red-100'">
                  {{ item }}
                </span>
              </div>
              <p class="text-xs italic text-[var(--text-secondary)]">{{ info.note }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ======= SECTION 5: Water & Nutrition Tracker ======= -->
      <section class="rounded-2xl border overflow-hidden backdrop-blur-xl"
        :class="isDark ? 'bg-slate-900/70 border-slate-800' : 'bg-white/80 border-slate-200'">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-800 bg-blue-500/5' : 'border-slate-200 bg-blue-50/50'">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white text-lg">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-[var(--text-primary)]">Daily Tracker</h2>
            <p class="text-xs text-[var(--text-secondary)]">Water intake and quick meal logging</p>
          </div>
        </div>
        <div class="p-6 space-y-6">
          <!-- Water tracker -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="text-sm font-semibold text-[var(--text-primary)]">Water Intake</span>
              <span class="text-xs font-medium text-blue-500">{{ waterGlasses }}/8 glasses</span>
            </div>
            <div class="flex gap-2 flex-wrap">
              <button v-for="i in 8" :key="i" @click="setWater(i)"
                class="w-10 h-12 rounded-xl border transition-all duration-200 flex items-center justify-center text-lg"
                :class="i <= waterGlasses
                  ? 'bg-gradient-to-b from-blue-400 to-blue-600 border-blue-500 text-white shadow-md shadow-blue-500/20'
                  : isDark ? 'border-slate-700 text-slate-600 hover:border-blue-500/50' : 'border-slate-300 text-slate-300 hover:border-blue-300'">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/></svg>
              </button>
            </div>
            <!-- Progress bar -->
            <div class="mt-3 h-2 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'">
              <div class="h-full rounded-full bg-gradient-to-r from-blue-400 to-cyan-400 transition-all duration-500"
                :style="{ width: (waterGlasses / 8 * 100) + '%' }"></div>
            </div>
          </div>

          <!-- Quick meal log -->
          <div>
            <label class="text-sm font-semibold text-[var(--text-primary)] mb-2 block">Quick Meal Log</label>
            <div class="flex gap-2">
              <input v-model="mealLogInput" type="text" placeholder="What did you eat? e.g. 'chicken salad with rice'"
                @keyup.enter="logMeal"
                class="flex-1 px-4 py-2.5 rounded-xl border text-sm transition-colors"
                :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:border-emerald-500' : 'bg-white border-slate-300 text-slate-900 placeholder-slate-400 focus:border-emerald-500'"
                style="outline: none" />
              <button @click="logMeal" :disabled="!mealLogInput.trim()"
                class="px-4 py-2.5 rounded-xl text-sm font-medium bg-gradient-to-r from-emerald-500 to-teal-600 text-white disabled:opacity-40 transition-all shadow-md shadow-emerald-500/20">
                Log
              </button>
            </div>
            <!-- Logged meals today -->
            <div v-if="todayMeals.length > 0" class="mt-3 space-y-2">
              <div v-for="(meal, idx) in todayMeals" :key="idx"
                class="flex items-center justify-between px-4 py-2.5 rounded-xl border"
                :class="isDark ? 'bg-slate-800/50 border-slate-700' : 'bg-slate-50 border-slate-200'">
                <span class="text-sm text-[var(--text-primary)]">{{ meal.description }}</span>
                <div class="flex items-center gap-3 text-xs">
                  <span class="font-medium text-emerald-500">~{{ meal.estimate?.calories || 0 }} kcal</span>
                  <button @click="removeMeal(idx)" class="text-[var(--text-secondary)] hover:text-red-400 transition-colors">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                  </button>
                </div>
              </div>
              <!-- Day total -->
              <div class="flex items-center justify-between px-4 py-2 rounded-xl border-2 border-dashed"
                :class="isDark ? 'border-slate-700' : 'border-slate-300'">
                <span class="text-xs font-semibold text-[var(--text-secondary)]">Today's Total</span>
                <span class="text-sm font-bold text-emerald-500">~{{ todayCalories }} kcal</span>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import ThemeLangControls from '@/components/ThemeLangControls.vue'

const { isDark } = useTheme()

// ── Profile data ──
const profile = ref({
  age: 0,
  gender: '',
  allergies: [],
  medications: [],
  conditions: [],
})

onMounted(() => {
  try {
    const raw = localStorage.getItem('user_profile')
    if (raw) {
      const p = JSON.parse(raw)
      profile.value.age = p.age || (p.dob ? calculateAge(p.dob) : 0)
      profile.value.gender = p.gender || p.sex || ''
      profile.value.allergies = Array.isArray(p.allergies) ? p.allergies : (p.allergies ? [p.allergies] : [])
      profile.value.medications = Array.isArray(p.medications) ? p.medications : (p.medications ? [p.medications] : [])
      profile.value.conditions = Array.isArray(p.conditions) ? p.conditions : (p.conditions ? [p.conditions] : [])
    }
  } catch (_e) { /* ignore */ }

  // Load saved tracker data
  try {
    const saved = localStorage.getItem('nutrition_tracker')
    if (saved) {
      const data = JSON.parse(saved)
      const today = new Date().toISOString().slice(0, 10)
      if (data.date === today) {
        waterGlasses.value = data.water || 0
        todayMeals.value = data.meals || []
      }
    }
  } catch (_e) { /* ignore */ }
})

function calculateAge(dob) {
  if (!dob) return 0
  const birth = new Date(dob)
  const today = new Date()
  let age = today.getFullYear() - birth.getFullYear()
  const m = today.getMonth() - birth.getMonth()
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--
  return age
}

// ── Diet settings ──
const dietGoals = [
  { value: 'weight_loss', label: 'Weight Loss', emoji: '\u26A1' },
  { value: 'heart_health', label: 'Heart Health', emoji: '\u2764\uFE0F' },
  { value: 'diabetes_management', label: 'Diabetes', emoji: '\u{1FA7A}' },
  { value: 'anti_inflammatory', label: 'Anti-Inflammatory', emoji: '\u{1F6E1}\uFE0F' },
  { value: 'general_wellness', label: 'General Wellness', emoji: '\u{1F33F}' },
]
const selectedGoal = ref('general_wellness')

const dietaryRestrictions = [
  { value: 'vegetarian', label: 'Vegetarian', emoji: '\u{1F96C}' },
  { value: 'vegan', label: 'Vegan', emoji: '\u{1F331}' },
  { value: 'gluten_free', label: 'Gluten-Free', emoji: '\u{1F33E}' },
  { value: 'dairy_free', label: 'Dairy-Free', emoji: '\u{1F95B}' },
  { value: 'keto', label: 'Keto', emoji: '\u{1F969}' },
  { value: 'mediterranean', label: 'Mediterranean', emoji: '\u{1FAD2}' },
]
const selectedRestrictions = ref([])

function toggleRestriction(val) {
  const idx = selectedRestrictions.value.indexOf(val)
  if (idx >= 0) selectedRestrictions.value.splice(idx, 1)
  else selectedRestrictions.value.push(val)
}

// ── Nutrient bar definitions ──
const nutrientDefs = [
  { key: 'protein', label: 'Protein', color: 'bg-red-400', max: 50 },
  { key: 'carbs', label: 'Carbs', color: 'bg-amber-400', max: 80 },
  { key: 'fats', label: 'Fats', color: 'bg-blue-400', max: 40 },
  { key: 'fiber', label: 'Fiber', color: 'bg-green-400', max: 15 },
]

// ── Meal plan ──
const mealPlan = ref(null)
const generating = ref(false)
const selectedDay = ref(0)

const currentDay = computed(() => mealPlan.value?.days?.[selectedDay.value] || null)

async function generateMealPlan() {
  generating.value = true
  try {
    const API_BASE = import.meta.env.VITE_API_BASE_URL || ''
    const payload = {
      profile: {
        age: profile.value.age,
        gender: profile.value.gender,
        allergies: profile.value.allergies,
        medications: profile.value.medications,
        conditions: profile.value.conditions,
        diet_goal: selectedGoal.value,
        dietary_restrictions: selectedRestrictions.value,
      },
      days: 7,
    }
    const resp = await fetch(`${API_BASE}/api/nutrition/meal-plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await resp.json()
    if (data.plan) {
      mealPlan.value = data.plan
      selectedDay.value = 0
    }
  } catch (e) {
    console.error('Failed to generate meal plan:', e)
  } finally {
    generating.value = false
  }
}

function mealTypeEmoji(type) {
  const map = { breakfast: '\u{1F305}', lunch: '\u2600\uFE0F', dinner: '\u{1F319}', snacks: '\u{1F37F}' }
  return map[type] || '\u{1F37D}\uFE0F'
}

function nutrientPercent(value, max) {
  if (!value || !max) return 0
  return Math.min(100, Math.round((value / max) * 100))
}

// ── Water tracker ──
const waterGlasses = ref(0)

function setWater(n) {
  waterGlasses.value = waterGlasses.value === n ? n - 1 : n
  saveTracker()
}

// ── Meal log ──
const mealLogInput = ref('')
const todayMeals = ref([])

const todayCalories = computed(() => todayMeals.value.reduce((sum, m) => sum + (m.estimate?.calories || 0), 0))

async function logMeal() {
  const desc = mealLogInput.value.trim()
  if (!desc) return

  let estimate = { calories: 300, protein: 15, carbs: 30, fats: 12, fiber: 3 }
  try {
    const API_BASE = import.meta.env.VITE_API_BASE_URL || ''
    const resp = await fetch(`${API_BASE}/api/nutrition/estimate-calories`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: desc }),
    })
    const data = await resp.json()
    if (data.estimate) estimate = data.estimate
  } catch (_e) { /* use default */ }

  todayMeals.value.push({ description: desc, estimate, time: new Date().toISOString() })
  mealLogInput.value = ''
  saveTracker()
}

function removeMeal(idx) {
  todayMeals.value.splice(idx, 1)
  saveTracker()
}

function saveTracker() {
  const today = new Date().toISOString().slice(0, 10)
  localStorage.setItem('nutrition_tracker', JSON.stringify({
    date: today,
    water: waterGlasses.value,
    meals: todayMeals.value,
  }))
}
</script>
