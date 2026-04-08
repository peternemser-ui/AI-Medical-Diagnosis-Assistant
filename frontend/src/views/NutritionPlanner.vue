<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]" :class="isDark ? 'bg-emerald-600/8' : 'bg-emerald-400/12'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]" :class="isDark ? 'bg-teal-600/6' : 'bg-teal-400/10'"></div>
    </div>
    <AppNav currentPage="nutrition" />

    <div class="relative z-10 max-w-5xl mx-auto px-4 py-6 space-y-5">
      <!-- Tab Bar -->
      <div class="relative rounded-2xl border overflow-hidden backdrop-blur-xl bg-clip-padding" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
        <div class="flex overflow-x-auto scrollbar-hide relative">
          <button v-for="(tab,idx) in tabs" :key="tab.id" :ref="el=>{if(el)tabRefs[idx]=el}" @click="activeTab=tab.id"
            class="relative flex items-center gap-2.5 px-6 py-4 text-sm font-semibold whitespace-nowrap transition-all duration-200 flex-shrink-0"
            :class="[activeTab===tab.id ? 'text-emerald-500 tab-premium-active' : isDark ? 'text-slate-400 hover:text-slate-200' : 'text-slate-500 hover:text-slate-800']">
            <span class="text-lg">{{ tab.icon }}</span><span>{{ tab.label }}</span>
          </button>
          <div class="absolute bottom-0 h-[3px] bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full transition-all duration-300 ease-out" :style="underlineStyle"></div>
        </div>
      </div>

      <Transition name="tab-fade" mode="out-in">
        <!-- ==================== TAB 1: MEAL PLAN ==================== -->
        <div v-if="activeTab==='meal-plan'" key="meal-plan" class="space-y-6">

          <!-- Personalized Planning Summary Bar -->
          <div class="rounded-xl border p-4 flex items-center gap-3 flex-wrap backdrop-blur-xl border-l-2 border-l-emerald-500" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Your Plan Profile:</span>
            <span class="plan-profile-pill" :class="dc('bg-emerald-500/15 text-emerald-400 border-emerald-500/20','bg-emerald-50 text-emerald-700 border-emerald-200')">{{ currentGoalObj?.emoji || '&#x2728;' }} {{ currentGoalObj?.label || 'General Wellness' }}</span>
            <span v-for="r in selectedRestrictions" :key="r" class="plan-profile-pill" :class="dc('bg-teal-500/10 text-teal-400 border-teal-500/20','bg-teal-50 text-teal-600 border-teal-200')">{{ restrictionObj(r)?.emoji }} {{ restrictionObj(r)?.label }}</span>
            <span v-if="profile.allergies?.length" class="plan-profile-pill" :class="dc('bg-amber-500/10 text-amber-400 border-amber-500/20','bg-amber-50 text-amber-600 border-amber-200')">&#x26A0;&#xFE0F; {{ profile.allergies.length }} allergies</span>
            <span v-if="profile.medications?.length" class="plan-profile-pill" :class="dc('bg-blue-500/10 text-blue-400 border-blue-500/20','bg-blue-50 text-blue-600 border-blue-200')">&#x1F48A; {{ profile.medications.length }} medications</span>
            <button @click="showProfileEditor=!showProfileEditor" class="ml-auto text-xs font-medium px-3 py-1.5 rounded-lg transition-all hover:underline underline-offset-2" :class="isDark ? 'text-emerald-400 hover:bg-emerald-500/10' : 'text-emerald-600 hover:bg-emerald-50'">{{ showProfileEditor ? 'Hide Profile' : 'Edit Profile' }}</button>
          </div>

          <!-- Profile Editor -->
          <Transition name="slide-down">
            <div v-if="showProfileEditor" class="rounded-2xl border overflow-hidden backdrop-blur-xl" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
              <div class="section-header" :class="dc('border-slate-800 bg-emerald-500/5','border-slate-200 bg-emerald-50/50')">
                <div class="icon-box bg-gradient-to-br from-emerald-500 to-teal-600"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg></div>
                <div><h2 class="text-xl font-bold tracking-tight text-[var(--text-primary)]">Diet Profile</h2><p class="text-xs leading-relaxed text-[var(--text-secondary)]">Your health data</p></div>
              </div>
              <div class="p-6 grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div v-for="s in profileStats" :key="s.label" class="rounded-xl p-3 text-center border" :class="dc('bg-slate-800/50 border-slate-700','bg-slate-50 border-slate-200')">
                  <div class="text-xs text-[var(--text-secondary)] mb-1">{{ s.label }}</div>
                  <div class="text-lg font-bold text-[var(--text-primary)]">{{ s.value }}</div>
                </div>
              </div>
            </div>
          </Transition>

          <!-- Profile Completeness -->
          <div v-if="profileCompleteness<100" class="rounded-xl border p-4 backdrop-blur-xl" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="flex items-center gap-3">
              <div class="flex-1 h-1.5 rounded-full overflow-hidden" :class="dc('bg-slate-800','bg-slate-200')">
                <div class="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-500" :style="{width:profileCompleteness+'%'}"></div>
              </div>
              <span class="text-[10px] text-[var(--text-secondary)] whitespace-nowrap">Profile {{ profileCompleteness }}% complete{{ profileHint }}</span>
            </div>
          </div>

          <!-- Diet Goal Cards -->
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="px-6 py-4 border-b" :class="dc('border-slate-800','border-slate-200')"><h3 class="text-sm font-bold text-[var(--text-primary)]">Diet Goal</h3></div>
            <div class="p-5 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
              <button v-for="g in dietGoals" :key="g.value" @click="selectedGoal=g.value"
                class="relative rounded-xl p-4 text-left transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
                :class="selectedGoal===g.value ? (isDark?'bg-emerald-500/10 border-2 border-emerald-500/50 ring-1 ring-emerald-500/30':'bg-emerald-50 border-2 border-emerald-400 ring-1 ring-emerald-300') : dc('border border-slate-700 hover:border-slate-600 bg-slate-800/30','border border-slate-200 hover:border-slate-300 bg-white')">
                <div v-if="selectedGoal===g.value" class="absolute top-2 right-2 w-5 h-5 rounded-full bg-emerald-500 flex items-center justify-center shadow-sm shadow-emerald-500/30">
                  <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                </div>
                <div class="text-3xl mb-2">{{ g.emoji }}</div>
                <div class="text-sm font-semibold text-[var(--text-primary)] mb-0.5">{{ g.label }}</div>
                <div class="text-[10px] leading-tight text-[var(--text-secondary)]">{{ g.subtitle }}</div>
              </button>
            </div>
          </div>

          <!-- Dietary Restrictions -->
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="px-6 py-4 border-b" :class="dc('border-slate-800','border-slate-200')"><h3 class="text-sm font-bold text-[var(--text-primary)]">Dietary Restrictions</h3></div>
            <div class="p-5 flex flex-wrap gap-2.5">
              <button v-for="r in dietaryRestrictions" :key="r.value" @click="toggleRestriction(r.value)"
                class="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border transition-all duration-200"
                :class="selectedRestrictions.includes(r.value) ? dc('bg-teal-500/15 border-teal-500/50 text-teal-300 shadow-md shadow-teal-500/10','bg-teal-50 border-teal-400 text-teal-700 shadow-md shadow-teal-500/10') : dc('border-slate-700 text-slate-400 hover:border-slate-500 bg-slate-800/30','border-slate-200 text-slate-500 hover:border-slate-400 bg-white')">
                <span class="text-lg">{{ r.emoji }}</span>{{ r.label }}
                <svg v-if="selectedRestrictions.includes(r.value)" class="w-3.5 h-3.5 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
              </button>
            </div>
          </div>

          <!-- AI Meal Planning Studio -->
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="section-header justify-between flex-wrap gap-3" :class="dc('border-slate-800 bg-gradient-to-r from-emerald-500/5 to-teal-500/5','border-slate-200 bg-gradient-to-r from-emerald-50/50 to-teal-50/50')">
              <div class="flex items-center gap-3">
                <div class="icon-box bg-gradient-to-br from-emerald-500 to-teal-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>
                </div>
                <div>
                  <h2 class="text-xl font-bold tracking-tight text-[var(--text-primary)]">AI Meal Planning Studio</h2>
                  <p class="text-xs leading-relaxed text-[var(--text-secondary)]">Choose a planning mode and generate your personalized 7-day plan</p>
                </div>
              </div>
              <div v-if="mealPlan" class="flex items-center gap-2">
                <span class="text-xs text-[var(--text-secondary)]">Plan active</span>
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              </div>
            </div>

            <!-- GENERATED PLAN VIEW -->
            <div v-if="mealPlan" class="p-6 space-y-6">
              <!-- Daily Target -->
              <div class="p-4 rounded-xl border" :class="dc('bg-slate-800/50 border-slate-700','bg-slate-50 border-slate-200')">
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-semibold text-[var(--text-primary)]">Daily Target</span>
                  <span class="text-sm font-bold text-emerald-500">{{ mealPlan.calorie_target }} kcal</span>
                </div>
                <div class="w-full h-2 rounded-full overflow-hidden" :class="dc('bg-slate-700','bg-slate-200')">
                  <div class="h-full rounded-full bg-gradient-to-r from-emerald-500 to-teal-500" style="width:100%"></div>
                </div>
              </div>

              <!-- Day Tab Strip -->
              <div class="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                <button v-for="(day,idx) in mealPlan.days" :key="idx" @click="selectedDay=idx"
                  class="flex-shrink-0 px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-200"
                  :class="selectedDay===idx
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white shadow-lg shadow-emerald-500/25'
                    : dc('text-slate-400 bg-slate-800/60 hover:bg-slate-700','text-slate-500 bg-slate-100 hover:bg-slate-200')">
                  {{ dayLabels[idx]||day.day?.slice(0,3) }}
                </button>
              </div>

              <!-- 4 Meal Cards -->
              <div v-if="currentDay" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="mt in ['breakfast','lunch','dinner','snack']" :key="mt"
                    class="meal-card-premium rounded-xl overflow-hidden transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5 group"
                    :class="[dc('bg-slate-800/40 border-slate-700 hover:border-slate-600','bg-white border-slate-200 hover:border-slate-300'), mt==='breakfast'?'border-l-[3px] border-l-amber-400 border-y border-r':mt==='lunch'?'border-l-[3px] border-l-blue-400 border-y border-r':mt==='dinner'?'border-l-[3px] border-l-purple-400 border-y border-r':'border-l-[3px] border-l-emerald-400 border-y border-r']">
                    <!-- Colored header bar -->
                    <div class="px-4 py-3 flex items-center justify-between"
                      :class="mealHeaderBg(mt)">
                      <span class="text-sm font-bold flex items-center gap-2">
                        <span>{{ mealTypeEmoji(mt) }}</span>
                        <span class="capitalize">{{ mt }}</span>
                      </span>
                      <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full" :class="dc('bg-black/15','bg-white/60')">{{ getMealData(mt)?.calories||0 }} kcal</span>
                    </div>
                    <div class="p-4">
                      <h4 class="font-bold text-sm tracking-tight text-[var(--text-primary)] mb-1">{{ getMealData(mt)?.name }}</h4>
                      <!-- AI Smart Labels -->
                      <div class="flex flex-wrap gap-1.5 mb-2">
                        <span v-if="getMealData(mt)?.calories && selectedGoal" class="smart-label" :class="dc('bg-emerald-500/10 text-emerald-400','bg-emerald-50 text-emerald-600')">&#x2705; Fits your goal</span>
                        <span v-if="selectedGoal==='heart_health' || selectedRestrictions.includes('mediterranean')" class="smart-label" :class="dc('bg-green-500/10 text-green-400','bg-green-50 text-green-600')">&#x1F49A; Heart-healthy</span>
                        <span v-if="getMealData(mt)?.prep_time && (getMealData(mt).prep_time.includes('10') || getMealData(mt).prep_time.includes('5 ')|| getMealData(mt).prep_time.includes('15'))" class="smart-label" :class="dc('bg-amber-500/10 text-amber-400','bg-amber-50 text-amber-600')">&#x26A1; Quick prep</span>
                        <span v-if="selectedRestrictions.includes('vegan') || selectedRestrictions.includes('vegetarian')" class="smart-label" :class="dc('bg-lime-500/10 text-lime-400','bg-lime-50 text-lime-600')">&#x1F331; Plant-based</span>
                      </div>
                      <!-- Macro Pills -->
                      <div class="flex gap-2 mb-3">
                        <span class="macro-pill" :class="dc('bg-red-500/10 text-red-400','bg-red-50 text-red-500')">P: <span class="font-mono">{{ getMealData(mt)?.protein||0 }}</span>g</span>
                        <span class="macro-pill" :class="dc('bg-amber-500/10 text-amber-400','bg-amber-50 text-amber-600')">C: <span class="font-mono">{{ getMealData(mt)?.carbs||0 }}</span>g</span>
                        <span class="macro-pill" :class="dc('bg-blue-500/10 text-blue-400','bg-blue-50 text-blue-500')">F: <span class="font-mono">{{ getMealData(mt)?.fats||0 }}</span>g</span>
                      </div>
                      <!-- Prep time -->
                      <div class="flex items-center gap-3 mb-3 text-xs text-[var(--text-secondary)]">
                        <span class="flex items-center gap-1">
                          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                          {{ getMealData(mt)?.prep_time||'--' }}
                        </span>
                      </div>
                      <!-- Nutrient bars -->
                      <div class="space-y-1.5 mb-3">
                        <div v-for="n in nutrientDefs" :key="n.key" class="flex items-center gap-2">
                          <span class="text-[10px] w-12 text-right text-[var(--text-secondary)]">{{ n.label }}</span>
                          <div class="flex-1 h-1.5 rounded-full overflow-hidden" :class="dc('bg-slate-700','bg-slate-200')">
                            <div class="h-full rounded-full macro-bar-refined transition-all duration-500" :class="n.color" :style="{width:nutrientPct(getMealData(mt)?.[n.key],n.max)+'%'}"></div>
                          </div>
                          <span class="text-[10px] w-8 text-[var(--text-secondary)]">{{ getMealData(mt)?.[n.key]||0 }}g</span>
                        </div>
                      </div>
                      <!-- Action buttons -->
                      <div class="flex gap-2 pt-2 border-t" :class="dc('border-slate-700/50','border-slate-100')">
                        <button @click="expandedMeals[mt]=!expandedMeals[mt]" class="meal-action-btn group/btn" :class="dc('hover:bg-slate-700 hover:text-slate-200 border-slate-700','hover:bg-blue-50 hover:text-blue-600 border-slate-200')">
                          {{ expandedMeals[mt] ? '&#x1F4D6; Less' : '&#x1F4D6; Details' }}
                        </button>
                        <button class="meal-action-btn group/btn" :class="dc('hover:bg-slate-700 hover:text-slate-200 border-slate-700','hover:bg-blue-50 hover:text-blue-600 border-slate-200')">&#x1F504; Swap</button>
                        <button class="meal-action-btn group/btn" :class="dc('hover:bg-slate-700 hover:text-rose-300 border-slate-700','hover:bg-rose-50 hover:text-rose-500 border-slate-200')">&#x2764;&#xFE0F; Save</button>
                        <button class="meal-action-btn group/btn" :class="dc('hover:bg-slate-700 hover:text-emerald-300 border-slate-700','hover:bg-emerald-50 hover:text-emerald-600 border-slate-200')">&#x1F6D2; List</button>
                      </div>
                    </div>
                    <!-- Expandable details -->
                    <Transition name="slide-down">
                      <div v-if="expandedMeals[mt]" class="px-4 pb-4 pt-2 border-t text-xs text-[var(--text-secondary)]" :class="dc('border-slate-700 bg-slate-800/20','border-slate-100 bg-slate-50/50')">
                        <div v-if="getMealData(mt)?.ingredients" class="mb-2"><strong class="text-[var(--text-primary)]">Ingredients:</strong> {{ Array.isArray(getMealData(mt).ingredients)?getMealData(mt).ingredients.join(', '):getMealData(mt).ingredients }}</div>
                        <div v-if="getMealData(mt)?.instructions"><strong class="text-[var(--text-primary)]">Instructions:</strong> {{ getMealData(mt).instructions }}</div>
                      </div>
                    </Transition>
                  </div>
                </div>

                <!-- Daily Summary Bar -->
                <div class="sticky bottom-0 z-10 rounded-xl border border-t-2 p-4 backdrop-blur-md" :class="dc('bg-slate-800/80 border-slate-700 border-t-emerald-500/30','bg-slate-50/90 border-slate-200 border-t-emerald-400/40')">
                  <div class="flex flex-wrap items-center justify-between gap-4 mb-3">
                    <span class="text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)]">Daily Totals</span>
                    <div class="flex items-center gap-5 text-sm">
                      <span v-for="m in macroSummary" :key="m.label" class="flex items-center gap-1.5">
                        <span class="w-2 h-2 rounded-full" :class="m.dot"></span>
                        <strong :class="[m.cls, m.label==='kcal'?'text-lg font-extrabold':'']">{{ m.val }}</strong>
                        <span class="text-[var(--text-secondary)] text-xs">{{ m.label }}</span>
                      </span>
                    </div>
                  </div>
                  <!-- Macro progress bars -->
                  <div class="grid grid-cols-3 gap-3">
                    <div>
                      <div class="flex items-center justify-between text-[10px] mb-1"><span class="text-[var(--text-secondary)]">Protein</span><span class="font-semibold font-mono text-red-400">{{ currentDay?.totals?.protein||0 }}g</span></div>
                      <div class="h-2 rounded-full overflow-hidden" :class="dc('bg-slate-700','bg-slate-200')"><div class="h-full rounded-full bg-red-400 macro-bar-refined" :style="{width: Math.min(100, ((currentDay?.totals?.protein||0)/150)*100)+'%'}"></div></div>
                    </div>
                    <div>
                      <div class="flex items-center justify-between text-[10px] mb-1"><span class="text-[var(--text-secondary)]">Carbs</span><span class="font-semibold font-mono text-amber-400">{{ currentDay?.totals?.carbs||0 }}g</span></div>
                      <div class="h-2 rounded-full overflow-hidden" :class="dc('bg-slate-700','bg-slate-200')"><div class="h-full rounded-full bg-amber-400 macro-bar-refined" :style="{width: Math.min(100, ((currentDay?.totals?.carbs||0)/250)*100)+'%'}"></div></div>
                    </div>
                    <div>
                      <div class="flex items-center justify-between text-[10px] mb-1"><span class="text-[var(--text-secondary)]">Fats</span><span class="font-semibold font-mono text-blue-400">{{ currentDay?.totals?.fats||0 }}g</span></div>
                      <div class="h-2 rounded-full overflow-hidden" :class="dc('bg-slate-700','bg-slate-200')"><div class="h-full rounded-full bg-blue-400 macro-bar-refined" :style="{width: Math.min(100, ((currentDay?.totals?.fats||0)/80)*100)+'%'}"></div></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Regenerate button -->
              <div class="flex justify-center">
                <button @click="generateMealPlan" :disabled="generating"
                  class="max-w-md w-full py-3.5 rounded-xl text-sm font-bold bg-gradient-to-r from-violet-500 to-indigo-500 text-white shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:hover:scale-100 transition-all duration-200">
                  &#x1F504; Regenerate Plan
                </button>
              </div>
            </div>

            <!-- EMPTY STATE: Plan Creation Studio -->
            <div v-else class="p-6 space-y-6">

              <!-- Plan Creation Mode Tiles -->
              <div>
                <h3 class="text-sm font-bold text-[var(--text-primary)] mb-3">Choose Your Planning Mode</h3>
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
                  <button v-for="mode in planModes" :key="mode.id" @click="planMode=mode.id"
                    class="relative rounded-xl border p-4 text-left transition-all duration-200"
                    :class="planMode===mode.id
                      ? (isDark ? 'bg-emerald-500/10 border-emerald-500/50 ring-1 ring-emerald-500/30 shadow-lg shadow-emerald-500/10' : 'bg-emerald-50 border-emerald-400 ring-1 ring-emerald-300 shadow-lg shadow-emerald-500/10')
                      : dc('border-slate-700 hover:border-slate-600 bg-slate-800/30 hover:bg-slate-800/50','border-slate-200 hover:border-slate-300 bg-white hover:bg-slate-50')">
                    <div v-if="planMode===mode.id" class="absolute top-2 right-2 w-5 h-5 rounded-full bg-emerald-500 flex items-center justify-center">
                      <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/></svg>
                    </div>
                    <div class="text-2xl mb-2">{{ mode.icon }}</div>
                    <div class="text-sm font-semibold text-[var(--text-primary)] mb-0.5 leading-tight">{{ mode.title }}</div>
                    <div class="text-[10px] leading-tight text-[var(--text-secondary)]">{{ mode.desc }}</div>
                  </button>
                </div>
              </div>

              <!-- Generate Button -->
              <button @click="generateMealPlan" :disabled="generating"
                class="w-full py-4 rounded-xl text-base font-bold bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-xl hover:shadow-2xl hover:scale-[1.01] active:scale-[0.99] disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:scale-100 transition-all duration-200">
                <span v-if="generating" class="flex items-center justify-center gap-3">
                  <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                  </svg>
                  {{ generatingStage }}
                </span>
                <span v-else>&#x2728; Generate My 7-Day Meal Plan</span>
              </button>

              <!-- Premium Empty State Preview -->
              <div class="opacity-40 pointer-events-none select-none">
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                  <div v-for="meal in ['Breakfast', 'Lunch', 'Dinner', 'Snack']" :key="meal"
                    class="rounded-xl border p-4" :class="dc('bg-slate-800/40 border-slate-700','bg-white border-slate-200')">
                    <div class="text-[10px] uppercase tracking-wider font-bold text-[var(--text-secondary)] mb-2">{{ meal }}</div>
                    <div class="h-3 w-3/4 rounded-full mt-2" :class="dc('bg-slate-700','bg-slate-200')"></div>
                    <div class="h-2 w-1/2 rounded-full mt-1.5" :class="dc('bg-slate-700','bg-slate-200')"></div>
                    <div class="flex gap-2 mt-3">
                      <div class="h-2 w-10 rounded-full bg-emerald-500/20"></div>
                      <div class="h-2 w-8 rounded-full bg-amber-500/20"></div>
                      <div class="h-2 w-8 rounded-full bg-blue-500/20"></div>
                    </div>
                  </div>
                </div>
                <p class="text-center text-xs mt-3 text-[var(--text-secondary)]">Your personalized 7-day plan will appear here</p>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== TAB 2: VISUAL MENU ==================== -->
        <div v-else-if="activeTab==='visual-menu'" key="visual-menu" class="space-y-5">
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="section-header" :class="dc('border-slate-800 bg-amber-500/5','border-slate-200 bg-amber-50/50')">
              <div class="icon-box bg-gradient-to-br from-amber-500 to-orange-500 text-lg">&#x1F372;</div>
              <div><h2 class="text-lg font-bold text-[var(--text-primary)]">Visual Menu Gallery</h2><p class="text-xs text-[var(--text-secondary)]">Browse meals by category</p></div>
            </div>
            <div class="p-6">
              <div class="flex gap-2 mb-5 overflow-x-auto pb-2 scrollbar-hide">
                <button v-for="c in menuCategories" :key="c.id" @click="selectedMenuCat=c.id; selectedTags=[]"
                  class="flex-shrink-0 px-4 py-2 rounded-full text-xs font-semibold transition-all duration-200"
                  :class="selectedMenuCat===c.id ? 'bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-md' : dc('text-slate-400 bg-slate-800 hover:bg-slate-700','text-slate-500 bg-slate-100 hover:bg-slate-200')">{{ c.icon }} {{ c.label }}</button>
              </div>
              <div v-if="availableTags.length" class="flex gap-2 mb-5 overflow-x-auto pb-2 scrollbar-hide flex-wrap">
                <button v-for="tag in availableTags" :key="tag.id" @click="toggleTag(tag.id)"
                  class="flex-shrink-0 px-3 py-1.5 rounded-full text-[11px] font-semibold border transition-all duration-200"
                  :class="selectedTags.includes(tag.id) ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white border-emerald-500/50 shadow-sm' : dc('text-slate-400 bg-slate-800/60 border-slate-700 hover:border-slate-500','text-slate-500 bg-slate-50 border-slate-200 hover:border-slate-400')">{{ tag.label }}</button>
                <button v-if="selectedTags.length" @click="selectedTags=[]" class="flex-shrink-0 px-3 py-1.5 rounded-full text-[11px] font-semibold transition-all duration-200" :class="dc('text-red-400 bg-red-500/10 hover:bg-red-500/20','text-red-500 bg-red-50 hover:bg-red-100')">Clear filters</button>
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="item in filteredMenuItems" :key="item.name" class="rounded-xl border overflow-hidden transition-all duration-200 hover:shadow-lg cursor-pointer" :class="dc('bg-slate-800/40 border-slate-700 hover:border-amber-500/30','bg-white border-slate-200 hover:border-amber-300')">
                  <div class="h-28 flex items-center justify-center text-5xl" :class="dc('bg-slate-800/60','bg-slate-50')">{{ item.emoji }}</div>
                  <div class="p-4">
                    <div class="text-sm font-bold text-[var(--text-primary)] mb-1">{{ item.name }}</div>
                    <div class="flex items-center gap-3 text-xs text-[var(--text-secondary)] mb-2"><span class="font-semibold text-emerald-500">{{ item.calories }} kcal</span><span>{{ item.prepTime }}</span></div>
                    <div class="flex gap-1.5 mb-2">
                      <span class="macro-pill" :class="dc('bg-red-500/10 text-red-400','bg-red-50 text-red-500')">P:{{ item.protein }}g</span>
                      <span class="macro-pill" :class="dc('bg-amber-500/10 text-amber-400','bg-amber-50 text-amber-600')">C:{{ item.carbs }}g</span>
                      <span class="macro-pill" :class="dc('bg-blue-500/10 text-blue-400','bg-blue-50 text-blue-500')">F:{{ item.fats }}g</span>
                    </div>
                    <div v-if="item.tags && item.tags.length" class="flex gap-1 flex-wrap">
                      <span v-for="t in item.tags.slice(0,3)" :key="t" class="px-1.5 py-0.5 rounded text-[9px] font-medium" :class="dc('bg-slate-700/60 text-slate-400','bg-slate-100 text-slate-500')">{{ t }}</span>
                      <span v-if="item.tags.length > 3" class="px-1.5 py-0.5 rounded text-[9px] font-medium" :class="dc('bg-slate-700/60 text-slate-400','bg-slate-100 text-slate-500')">+{{ item.tags.length - 3 }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== TAB 3: RESTAURANT GUIDE ==================== -->
        <div v-else-if="activeTab==='restaurant'" key="restaurant" class="space-y-5">
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="section-header" :class="dc('border-slate-800 bg-rose-500/5','border-slate-200 bg-rose-50/50')">
              <div class="icon-box bg-gradient-to-br from-rose-500 to-pink-600 text-lg">&#x1F37D;&#xFE0F;</div>
              <div><h2 class="text-lg font-bold text-[var(--text-primary)]">Restaurant Guide</h2><p class="text-xs text-[var(--text-secondary)]">Healthy choices when eating out</p></div>
            </div>
            <div class="p-6 space-y-4">
              <div v-for="r in restaurantTips" :key="r.name" class="rounded-xl border p-5 transition-all hover:shadow-md" :class="dc('bg-slate-800/30 border-slate-700 hover:border-slate-600','bg-white border-slate-200 hover:border-slate-300')">
                <div class="flex items-center gap-3 mb-3"><span class="text-2xl">{{ r.icon }}</span><div><div class="text-sm font-bold text-[var(--text-primary)]">{{ r.name }}</div><div class="text-xs text-[var(--text-secondary)]">{{ r.cuisine }}</div></div></div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div class="rounded-lg p-3 border" :class="dc('bg-emerald-500/5 border-emerald-500/20','bg-emerald-50 border-emerald-100')">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-1.5" :class="dc('text-emerald-400','text-emerald-600')">Best Choices</div>
                    <ul class="space-y-1"><li v-for="c in r.good" :key="c" class="text-xs" :class="dc('text-emerald-300/80','text-emerald-700')">{{ c }}</li></ul>
                  </div>
                  <div class="rounded-lg p-3 border" :class="dc('bg-red-500/5 border-red-500/20','bg-red-50 border-red-100')">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-1.5" :class="dc('text-red-400','text-red-600')">Avoid</div>
                    <ul class="space-y-1"><li v-for="c in r.avoid" :key="c" class="text-xs" :class="dc('text-red-300/80','text-red-700')">{{ c }}</li></ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== TAB 4: SHOPPING ADVISOR ==================== -->
        <div v-else-if="activeTab==='shopping'" key="shopping" class="space-y-5">
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="section-header" :class="dc('border-slate-800 bg-indigo-500/5','border-slate-200 bg-indigo-50/50')">
              <div class="icon-box bg-gradient-to-br from-indigo-500 to-violet-600 text-lg">&#x1F6D2;</div>
              <div><h2 class="text-lg font-bold text-[var(--text-primary)]">Smart Shopping Advisor</h2><p class="text-xs text-[var(--text-secondary)]">Weekly grocery lists from your meal plan</p></div>
            </div>
            <div class="p-6">
              <div v-if="!mealPlan" class="text-center py-10"><span class="text-4xl block mb-3">&#x1F6D2;</span><p class="text-sm text-[var(--text-secondary)]">Generate a meal plan first to get a personalized shopping list.</p></div>
              <div v-else class="space-y-4">
                <div v-for="cat in shoppingCategories" :key="cat.name" class="rounded-xl border p-4" :class="dc('bg-slate-800/30 border-slate-700','bg-white border-slate-200')">
                  <div class="flex items-center gap-2 mb-3"><span class="text-lg">{{ cat.icon }}</span><h3 class="text-sm font-bold text-[var(--text-primary)]">{{ cat.name }}</h3><span class="ml-auto text-[10px] px-2 py-0.5 rounded-full" :class="dc('bg-slate-700 text-slate-400','bg-slate-100 text-slate-500')">{{ cat.items.length }}</span></div>
                  <div class="flex flex-wrap gap-2">
                    <span v-for="item in cat.items" :key="item" @click="shoppingChecked[item]=!shoppingChecked[item]"
                      class="px-3 py-1.5 rounded-lg text-xs font-medium border cursor-pointer transition-all duration-200"
                      :class="shoppingChecked[item] ? dc('bg-emerald-500/10 border-emerald-500/30 text-emerald-400 line-through opacity-60','bg-emerald-50 border-emerald-200 text-emerald-600 line-through opacity-60') : dc('bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-500','bg-white border-slate-200 text-slate-600 hover:border-slate-400')">{{ item }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== TAB 5: DAILY TRACKER ==================== -->
        <div v-else-if="activeTab==='tracker'" key="tracker" class="space-y-5">
          <!-- Hydration -->
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="section-header" :class="dc('border-slate-800 bg-blue-500/5','border-slate-200 bg-blue-50/50')">
              <div class="icon-box bg-gradient-to-br from-blue-500 to-cyan-500 text-lg">&#x1F4A7;</div>
              <div><h2 class="text-lg font-bold text-[var(--text-primary)]">Hydration Tracker</h2><p class="text-xs text-[var(--text-secondary)]">Daily water intake</p></div>
            </div>
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <span class="text-sm font-semibold text-[var(--text-primary)]">{{ waterGlasses }} of 8 glasses <span class="text-[var(--text-secondary)] font-normal">({{ waterGlasses*250 }}ml)</span></span>
                <Transition name="pop"><span v-if="waterGlasses>=8" class="text-xs font-semibold text-emerald-500">Goal reached!</span></Transition>
              </div>
              <div class="flex gap-3 justify-center mb-5">
                <button v-for="i in 8" :key="i" @click="setWater(i)"
                  class="relative w-12 h-16 rounded-xl border-2 overflow-hidden transition-all duration-300 flex items-end justify-center"
                  :class="i<=waterGlasses ? 'border-blue-400 shadow-md shadow-blue-500/20' : dc('border-slate-700 hover:border-blue-500/40','border-slate-200 hover:border-blue-300')">
                  <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-blue-500 to-cyan-400 transition-all duration-500 rounded-b-lg" :style="{height:i<=waterGlasses?'100%':'0%'}"></div>
                  <svg class="w-6 h-6 relative z-10 mb-1 transition-colors duration-300" :class="i<=waterGlasses?'text-white':dc('text-slate-600','text-slate-300')" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/></svg>
                </button>
              </div>
              <div class="h-2.5 rounded-full overflow-hidden" :class="dc('bg-slate-800','bg-slate-200')">
                <div class="h-full rounded-full transition-all duration-500" :class="waterGlasses>=8?'bg-gradient-to-r from-emerald-400 to-emerald-500':'bg-gradient-to-r from-blue-400 to-cyan-400'" :style="{width:(waterGlasses/8*100)+'%'}"></div>
              </div>
            </div>
          </div>

          <!-- Meal Logger -->
          <div class="card-section" :class="dc('bg-slate-900/70 border-slate-800','bg-white/80 border-slate-200')">
            <div class="section-header" :class="dc('border-slate-800 bg-emerald-500/5','border-slate-200 bg-emerald-50/50')">
              <div class="icon-box bg-gradient-to-br from-emerald-500 to-teal-600 text-lg">&#x1F4DD;</div>
              <div><h2 class="text-lg font-bold text-[var(--text-primary)]">Meal Logger</h2><p class="text-xs text-[var(--text-secondary)]">AI estimates calories</p></div>
            </div>
            <div class="p-6 space-y-5">
              <div class="flex gap-2">
                <input v-model="mealLogInput" type="text" placeholder="What did you eat? e.g. 'chicken salad with rice'" @keyup.enter="logMeal"
                  class="flex-1 px-4 py-3 rounded-xl border text-sm transition-colors outline-none" :class="dc('bg-slate-800 border-slate-700 text-white placeholder-slate-500 focus:border-emerald-500','bg-white border-slate-300 text-slate-900 placeholder-slate-400 focus:border-emerald-500')"/>
                <button @click="logMeal" :disabled="!mealLogInput.trim()||loggingMeal" class="px-5 py-3 rounded-xl text-sm font-semibold bg-gradient-to-r from-emerald-500 to-teal-600 text-white disabled:opacity-40 shadow-md shadow-emerald-500/20 hover:shadow-lg transition-all">
                  <svg v-if="loggingMeal" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                  <span v-else>Log</span>
                </button>
              </div>
              <div v-if="todayMeals.length>0" class="px-4 py-2.5 rounded-xl" :class="dc('bg-slate-800/50','bg-slate-50')">
                <span class="text-xs text-[var(--text-secondary)]">Logged <strong class="text-[var(--text-primary)]">{{ todayMeals.length }} meal{{ todayMeals.length>1?'s':'' }}</strong> today &mdash; <strong class="text-emerald-500">{{ todayCalories }} cal</strong></span>
              </div>
              <div v-if="todayMeals.length>0" class="space-y-2">
                <TransitionGroup name="list">
                  <div v-for="(meal,idx) in todayMeals" :key="meal.time||idx" class="flex items-center justify-between px-4 py-3 rounded-xl border" :class="dc('bg-slate-800/50 border-slate-700','bg-white border-slate-200')">
                    <div class="flex items-center gap-3"><span class="text-lg">&#x1F37D;&#xFE0F;</span><div><span class="text-sm font-medium text-[var(--text-primary)]">{{ meal.description }}</span><div class="text-[10px] text-[var(--text-secondary)]">{{ fmtTime(meal.time) }}</div></div></div>
                    <div class="flex items-center gap-3">
                      <div class="text-right"><span class="text-sm font-bold text-emerald-500">~{{ meal.estimate?.calories||0 }} kcal</span><div class="flex gap-2 text-[10px] text-[var(--text-secondary)]"><span>P:{{ meal.estimate?.protein||0 }}g</span><span>C:{{ meal.estimate?.carbs||0 }}g</span><span>F:{{ meal.estimate?.fats||0 }}g</span></div></div>
                      <button @click="removeMeal(idx)" class="text-[var(--text-secondary)] hover:text-red-400 transition-colors p-1"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
                    </div>
                  </div>
                </TransitionGroup>
                <div class="flex items-center justify-between px-4 py-3 rounded-xl border-2 border-dashed" :class="dc('border-slate-700','border-slate-300')"><span class="text-xs font-bold text-[var(--text-secondary)]">Today's Total</span><span class="text-base font-bold text-emerald-500">~{{ todayCalories }} kcal</span></div>
              </div>
              <div v-else class="text-center py-8"><span class="text-3xl block mb-2">&#x1F34E;</span><p class="text-sm text-[var(--text-secondary)]">Start logging meals to track daily nutrition.</p></div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from 'vue'
import { useTheme } from '@/composables/useTheme'
import AppNav from '@/components/AppNav.vue'
import { RECIPE_CATEGORIES, RECIPE_DATABASE, RECIPE_TAGS } from '@/data/recipeDatabase.js'

const { isDark } = useTheme()
const dc = (dark, light) => isDark.value ? dark : light

// ── Tabs ──
const tabs = [
  { id: 'meal-plan', label: 'Meal Plan', icon: '\u{1F957}' },
  { id: 'visual-menu', label: 'Visual Menu', icon: '\u{1F372}' },
  { id: 'restaurant', label: 'Restaurant Guide', icon: '\u{1F37D}\uFE0F' },
  { id: 'shopping', label: 'Shopping Advisor', icon: '\u{1F6D2}' },
  { id: 'tracker', label: 'Daily Tracker', icon: '\u{1F4CA}' },
]
const activeTab = ref('meal-plan')
const tabRefs = reactive({})
const underlineStyle = computed(() => {
  const el = tabRefs[tabs.findIndex(t => t.id === activeTab.value)]
  return el ? { left: el.offsetLeft + 'px', width: el.offsetWidth + 'px' } : { left: '0px', width: '0px' }
})
watch(activeTab, () => nextTick(() => {}))

// ── Profile ──
const profile = ref({ age: 0, gender: '', allergies: [], medications: [], conditions: [] })
const showProfileEditor = ref(false)
const profileStats = computed(() => [
  { label: 'Age', value: profile.value.age || '--' },
  { label: 'Gender', value: profile.value.gender || '--' },
  { label: 'Allergies', value: profile.value.allergies.length || 0 },
  { label: 'Medications', value: profile.value.medications.length || 0 },
])
const profileCompleteness = computed(() => {
  let s = 0
  if (profile.value.age) s += 20
  if (profile.value.gender) s += 20
  if (selectedGoal.value) s += 20
  if (profile.value.allergies.length) s += 20
  if (profile.value.medications.length) s += 20
  return s
})
const profileHint = computed(() => {
  if (!profile.value.age) return ' \u2014 add age for better recommendations'
  if (!profile.value.allergies.length) return ' \u2014 add allergies for safer plans'
  if (!profile.value.medications.length) return ' \u2014 add medications for interaction checks'
  return ''
})

onMounted(() => {
  try {
    const raw = localStorage.getItem('user_profile')
    if (raw) {
      const p = JSON.parse(raw)
      profile.value.age = p.age || (p.dob ? calcAge(p.dob) : 0)
      profile.value.gender = p.gender || p.sex || ''
      const arr = v => Array.isArray(v) ? v : (v ? [v] : [])
      profile.value.allergies = arr(p.allergies)
      profile.value.medications = arr(p.medications)
      profile.value.conditions = arr(p.conditions)
    }
  } catch (_) {}
  try {
    const saved = localStorage.getItem('nutrition_tracker')
    if (saved) { const d = JSON.parse(saved); if (d.date === new Date().toISOString().slice(0,10)) { waterGlasses.value = d.water||0; todayMeals.value = d.meals||[] } }
  } catch (_) {}
  nextTick(() => { activeTab.value = activeTab.value })
})

function calcAge(dob) {
  if (!dob) return 0
  const b = new Date(dob), t = new Date()
  let a = t.getFullYear() - b.getFullYear()
  if (t.getMonth() - b.getMonth() < 0 || (t.getMonth() === b.getMonth() && t.getDate() < b.getDate())) a--
  return a
}

// ── Diet Settings ──
const dietGoals = [
  { value: 'weight_loss', label: 'Weight Loss', emoji: '\u{1F3AF}', subtitle: 'Calorie deficit focus' },
  { value: 'heart_health', label: 'Heart Health', emoji: '\u2764\uFE0F', subtitle: 'Low sodium, healthy fats' },
  { value: 'diabetes_management', label: 'Diabetes Mgmt', emoji: '\u{1FA78}', subtitle: 'Blood sugar control' },
  { value: 'anti_inflammatory', label: 'Anti-Inflammatory', emoji: '\u{1F33F}', subtitle: 'Reduce inflammation' },
  { value: 'general_wellness', label: 'General Wellness', emoji: '\u2728', subtitle: 'Balanced nutrition' },
]
const showUserMenu = ref(false)
const selectedGoal = ref('general_wellness')
const currentGoalObj = computed(() => dietGoals.find(g => g.value === selectedGoal.value))
const dietaryRestrictions = [
  { value: 'vegetarian', label: 'Vegetarian', emoji: '\u{1F96C}' }, { value: 'vegan', label: 'Vegan', emoji: '\u{1F331}' },
  { value: 'gluten_free', label: 'Gluten-Free', emoji: '\u{1F6AB}' }, { value: 'dairy_free', label: 'Dairy-Free', emoji: '\u{1F95B}' },
  { value: 'keto', label: 'Keto', emoji: '\u{1F969}' }, { value: 'mediterranean', label: 'Mediterranean', emoji: '\u{1FAD2}' },
]
const selectedRestrictions = ref([])
function toggleRestriction(v) { const i = selectedRestrictions.value.indexOf(v); i >= 0 ? selectedRestrictions.value.splice(i, 1) : selectedRestrictions.value.push(v) }
function restrictionObj(v) { return dietaryRestrictions.find(r => r.value === v) }

// ── Nutrients & Meal Plan ──
const nutrientDefs = [
  { key: 'protein', label: 'Protein', color: 'bg-red-400', max: 50 }, { key: 'carbs', label: 'Carbs', color: 'bg-amber-400', max: 80 },
  { key: 'fats', label: 'Fats', color: 'bg-blue-400', max: 40 }, { key: 'fiber', label: 'Fiber', color: 'bg-green-400', max: 15 },
]
const nutrientPct = (v, m) => (!v || !m) ? 0 : Math.min(100, Math.round((v / m) * 100))
const mealPlan = ref(null), generating = ref(false), selectedDay = ref(0), expandedMeals = reactive({})
const planMode = ref('goal')
const generatingStage = ref('')
let stageInterval = null

const planModes = [
  { id: 'goal', icon: '\u{1F3AF}', title: 'Goal-Based Plan', desc: 'Aligned to your selected wellness goal' },
  { id: 'quick', icon: '\u26A1', title: 'Quick Meals Only', desc: 'Everything under 15 minutes prep' },
  { id: 'macro', icon: '\u{1F4CA}', title: 'Macro-Focused', desc: 'Hit specific protein/carb/fat targets' },
  { id: 'budget', icon: '\u{1F4B0}', title: 'Budget-Friendly', desc: 'Affordable ingredients, no waste' },
  { id: 'world', icon: '\u{1F30D}', title: 'World Cuisine Explorer', desc: 'Different cuisine each day' },
  { id: 'protein', icon: '\u{1F3CB}\uFE0F', title: 'High-Protein Builder', desc: '30g+ protein every meal' },
  { id: 'mediterranean', icon: '\u{1FAD2}', title: 'Mediterranean Week', desc: 'Heart-healthy Mediterranean diet' },
  { id: 'plant', icon: '\u{1F331}', title: 'Plant-Based Week', desc: '100% plant-powered meals' },
  { id: 'restaurant', icon: '\u{1F37D}\uFE0F', title: 'Restaurant + Home Mix', desc: 'Include restaurant meals' },
  { id: 'supermarket', icon: '\u{1F6D2}', title: 'Supermarket Smart', desc: 'Built from grocery staples' },
]
const dayLabels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
const currentDay = computed(() => mealPlan.value?.days?.[selectedDay.value] || null)
function getMealData(mt) { if (!currentDay.value) return null; return mt === 'snack' ? (currentDay.value.snacks?.[0] || currentDay.value.snack) : currentDay.value[mt] }
const mealTypeEmoji = t => ({ breakfast: '\u{1F305}', lunch: '\u2600\uFE0F', dinner: '\u{1F319}', snack: '\u{1F37F}' })[t] || '\u{1F37D}\uFE0F'
const mealTypeColor = t => ({ breakfast: 'text-amber-500', lunch: 'text-blue-500', dinner: 'text-purple-500', snack: 'text-emerald-500' })[t] || 'text-slate-400'
const mealHeaderBg = t => {
  const map = {
    breakfast: isDark.value ? 'bg-amber-500/10 text-amber-300' : 'bg-amber-50 text-amber-700',
    lunch: isDark.value ? 'bg-blue-500/10 text-blue-300' : 'bg-blue-50 text-blue-700',
    dinner: isDark.value ? 'bg-purple-500/10 text-purple-300' : 'bg-purple-50 text-purple-700',
    snack: isDark.value ? 'bg-emerald-500/10 text-emerald-300' : 'bg-emerald-50 text-emerald-700',
  }
  return map[t] || (isDark.value ? 'bg-slate-800 text-slate-300' : 'bg-slate-50 text-slate-600')
}
const macroSummary = computed(() => {
  const d = currentDay.value?.totals || {}
  return [
    { label: 'kcal', val: d.calories||0, dot: 'bg-emerald-500', cls: 'text-emerald-500' },
    { label: 'protein', val: (d.protein||0)+'g', dot: 'bg-red-400', cls: 'text-red-400' },
    { label: 'carbs', val: (d.carbs||0)+'g', dot: 'bg-amber-400', cls: 'text-amber-400' },
    { label: 'fats', val: (d.fats||0)+'g', dot: 'bg-blue-400', cls: 'text-blue-400' },
  ]
})

async function generateMealPlan() {
  generating.value = true
  const stages = ['Analyzing your goals...', 'Checking dietary restrictions...', 'Balancing calories & macros...', 'Building meal variety...', 'Preparing your plan...']
  let stageIdx = 0
  generatingStage.value = stages[0]
  stageInterval = setInterval(() => {
    stageIdx = (stageIdx + 1) % stages.length
    generatingStage.value = stages[stageIdx]
  }, 2000)
  try {
    const API = import.meta.env.VITE_API_BASE_URL || ''
    const resp = await fetch(`${API}/api/nutrition/meal-plan`, { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ profile: { age: profile.value.age, gender: profile.value.gender, allergies: profile.value.allergies, medications: profile.value.medications, conditions: profile.value.conditions, diet_goal: selectedGoal.value, dietary_restrictions: selectedRestrictions.value, plan_mode: planMode.value }, days: 7 }) })
    const data = await resp.json()
    if (data.plan) { mealPlan.value = data.plan; selectedDay.value = 0 }
  } catch (e) { console.error('Meal plan error:', e) }
  finally { clearInterval(stageInterval); generatingStage.value = ''; generating.value = false }
}

// ── Visual Menu (Tab 2) ──
const menuCategories = RECIPE_CATEGORIES
const selectedMenuCat = ref('all')
const selectedTags = ref([])
const menuItems = RECIPE_DATABASE
const toggleTag = (tagId) => {
  const idx = selectedTags.value.indexOf(tagId)
  if (idx === -1) selectedTags.value.push(tagId)
  else selectedTags.value.splice(idx, 1)
}
const availableTags = computed(() => {
  const catItems = selectedMenuCat.value === 'all' ? menuItems : menuItems.filter(i => i.category === selectedMenuCat.value)
  const tagSet = new Set()
  catItems.forEach(i => (i.tags || []).forEach(t => tagSet.add(t)))
  return RECIPE_TAGS.filter(t => tagSet.has(t.id))
})
const filteredMenuItems = computed(() => {
  let items = selectedMenuCat.value === 'all' ? menuItems : menuItems.filter(i => i.category === selectedMenuCat.value)
  if (selectedTags.value.length > 0) {
    items = items.filter(i => selectedTags.value.every(t => (i.tags || []).includes(t)))
  }
  return items
})

// ── Restaurant Guide (Tab 3) ──
const restaurantTips = [
  { name: 'Asian / Sushi', cuisine: 'Japanese, Chinese, Thai', icon: '\u{1F363}', good: ['Sashimi (low cal, high protein)', 'Edamame', 'Miso soup', 'Brown rice'], avoid: ['Tempura (deep fried)', 'Sweet teriyaki sauces', 'Cream cheese rolls'] },
  { name: 'Italian', cuisine: 'Pizza, Pasta, Risotto', icon: '\u{1F355}', good: ['Grilled fish or chicken', 'Minestrone soup', 'Caprese salad'], avoid: ['Alfredo / cream sauces', 'Garlic bread basket', 'Deep dish pizza'] },
  { name: 'Mexican', cuisine: 'Tacos, Burritos, Bowls', icon: '\u{1F32E}', good: ['Burrito bowls (no tortilla)', 'Grilled chicken tacos', 'Black beans'], avoid: ['Chips & queso', 'Sour cream heavy dishes', 'Chimichangas'] },
  { name: 'Fast Casual', cuisine: 'Burgers, Sandwiches', icon: '\u{1F354}', good: ['Grilled chicken sandwich', 'Side salad instead of fries', 'Water instead of soda'], avoid: ['Double patty burgers', 'Milkshakes', 'Supersized combos'] },
]

// ── Shopping (Tab 4) ──
const shoppingChecked = reactive({})
const shoppingCategories = computed(() => !mealPlan.value ? [] : [
  { name: 'Proteins', icon: '\u{1F969}', items: ['Chicken breast', 'Salmon fillets', 'Eggs', 'Greek yogurt', 'Tofu'] },
  { name: 'Vegetables', icon: '\u{1F966}', items: ['Spinach', 'Broccoli', 'Bell peppers', 'Sweet potatoes', 'Tomatoes', 'Kale'] },
  { name: 'Fruits', icon: '\u{1F34E}', items: ['Bananas', 'Berries', 'Avocados', 'Lemons', 'Apples'] },
  { name: 'Grains & Pantry', icon: '\u{1F35E}', items: ['Brown rice', 'Quinoa', 'Oats', 'Whole wheat bread', 'Olive oil'] },
  { name: 'Dairy & Alts', icon: '\u{1F95B}', items: ['Almond milk', 'Cheese', 'Butter', 'Coconut yogurt'] },
])

// ── Water Tracker ──
const waterGlasses = ref(0)
function setWater(n) { waterGlasses.value = waterGlasses.value === n ? n - 1 : n; saveTracker() }

// ── Meal Logger ──
const mealLogInput = ref(''), todayMeals = ref([]), loggingMeal = ref(false)
const todayCalories = computed(() => todayMeals.value.reduce((s, m) => s + (m.estimate?.calories || 0), 0))
const fmtTime = iso => iso ? new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : ''

async function logMeal() {
  const desc = mealLogInput.value.trim(); if (!desc) return; loggingMeal.value = true
  let est = { calories: 300, protein: 15, carbs: 30, fats: 12, fiber: 3 }
  try { const API = import.meta.env.VITE_API_BASE_URL || ''; const r = await fetch(`${API}/api/nutrition/estimate-calories`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ description: desc }) }); const d = await r.json(); if (d.estimate) est = d.estimate } catch (_) {}
  todayMeals.value.push({ description: desc, estimate: est, time: new Date().toISOString() }); mealLogInput.value = ''; loggingMeal.value = false; saveTracker()
}
function removeMeal(i) { todayMeals.value.splice(i, 1); saveTracker() }
function saveTracker() { localStorage.setItem('nutrition_tracker', JSON.stringify({ date: new Date().toISOString().slice(0, 10), water: waterGlasses.value, meals: todayMeals.value })) }
</script>

<style scoped>
.tab-fade-enter-active, .tab-fade-leave-active { transition: opacity .2s ease, transform .2s ease; }
.tab-fade-enter-from { opacity: 0; transform: translateY(8px); }
.tab-fade-leave-to { opacity: 0; transform: translateY(-4px); }
.slide-down-enter-active, .slide-down-leave-active { transition: all .25s ease; overflow: hidden; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; max-height: 0; transform: translateY(-8px); }
.slide-down-enter-to, .slide-down-leave-from { opacity: 1; max-height: 500px; }
.pop-enter-active { transition: all .3s cubic-bezier(.34,1.56,.64,1); }
.pop-leave-active { transition: all .15s ease; }
.pop-enter-from { opacity: 0; transform: scale(.6); }
.pop-leave-to { opacity: 0; transform: scale(.8); }
.list-enter-active { transition: all .3s ease; }
.list-leave-active { transition: all .2s ease; }
.list-enter-from { opacity: 0; transform: translateX(-20px); }
.list-leave-to { opacity: 0; transform: translateX(20px); }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
.card-section { @apply rounded-2xl border overflow-hidden backdrop-blur-xl; }
.section-header { @apply px-6 py-4 border-b flex items-center gap-3; }
.icon-box { @apply w-10 h-10 rounded-xl flex items-center justify-center text-white; }
.pill-stat { @apply inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium bg-[color-mix(in_srgb,var(--clinical-surface)_90%,transparent)] text-[var(--text-secondary)]; }
.macro-pill { @apply px-2.5 py-1 rounded-md text-[10px] font-semibold; }
.plan-profile-pill { @apply inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold border; }
.smart-label { @apply inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[9px] font-semibold; }
.meal-action-btn { @apply text-xs px-2.5 py-1.5 rounded-lg border font-medium transition-all duration-150 text-[var(--text-secondary)]; }

/* Premium card hover */
.meal-card-premium {
  transition: all 0.2s ease;
}
.meal-card-premium:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1), 0 4px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Refined macro bar */
.macro-bar-refined {
  height: 6px;
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Tab premium active */
.tab-premium-active {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
  border-bottom: 3px solid currentColor;
}
</style>
