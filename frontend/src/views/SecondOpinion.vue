<template>
  <div class="min-h-screen transition-colors duration-300 surface-page">
    <AppNav currentPage="second-opinion" />

    <div class="max-w-5xl mx-auto px-4 py-6 space-y-6">

      <!-- Page Header -->
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-2xl bg-sky-600 flex items-center justify-center flex-shrink-0 shadow-sm">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </div>
        <div>
          <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">AI Second Opinion</h1>
          <p class="text-sm mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Run the same case through multiple AI models and review consensus for higher confidence</p>
        </div>
      </div>

      <!-- Horizontal Stepper -->
      <div class="bg-white border border-slate-200 rounded-xl shadow-sm p-5"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <div class="flex items-center">
          <!-- Step 1 -->
          <div class="flex items-center gap-3 flex-1">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ring-2"
              :class="isDark ? 'bg-sky-600 text-white ring-sky-500' : 'bg-sky-600 text-white ring-sky-300'">1</div>
            <div class="hidden sm:block">
              <div class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Select Case</div>
              <div class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Enter symptoms</div>
            </div>
          </div>
          <!-- Connector -->
          <div class="flex-1 h-px mx-2" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>
          <!-- Step 2 -->
          <div class="flex items-center gap-3 flex-1">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ring-2"
              :class="isDark ? 'bg-sky-600 text-white ring-sky-500' : 'bg-sky-600 text-white ring-sky-300'">2</div>
            <div class="hidden sm:block">
              <div class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Select Models</div>
              <div class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Choose AI models</div>
            </div>
          </div>
          <!-- Connector -->
          <div class="flex-1 h-px mx-2" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>
          <!-- Step 3 -->
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ring-2"
              :class="results
                ? isDark ? 'bg-emerald-600 text-white ring-emerald-500' : 'bg-emerald-600 text-white ring-emerald-300'
                : isDark ? 'bg-slate-700 text-slate-400 ring-slate-600' : 'bg-slate-100 text-slate-400 ring-slate-200'">
              <svg v-if="results" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              <span v-else>3</span>
            </div>
            <div class="hidden sm:block">
              <div class="text-sm font-semibold" :class="results ? (isDark ? 'text-emerald-400' : 'text-emerald-700') : (isDark ? 'text-slate-400' : 'text-slate-400')">Review Results</div>
              <div class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Compare opinions</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 1: Case Selection -->
      <div class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-700 bg-sky-900/10' : 'border-slate-200 bg-sky-50/60'">
          <div class="w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">1</div>
          <div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Select Case</h2>
            <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Choose a past diagnosis or describe symptoms manually</p>
          </div>
        </div>
        <div class="p-6">

          <!-- Past Sessions -->
          <div v-if="pastSessions.length > 0" class="space-y-2 mb-5">
            <p class="text-xs font-medium mb-3" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Recent diagnoses</p>
            <button v-for="sess in pastSessions.slice(0, 5)" :key="sess.id"
              @click="selectSession(sess)"
              class="w-full text-left px-4 py-3 rounded-xl border text-sm transition-all"
              :class="selectedCase?.id === sess.id
                ? isDark ? 'border-sky-500 bg-sky-900/20 text-sky-300' : 'border-sky-500 bg-sky-50 text-sky-700'
                : isDark ? 'border-slate-700 hover:border-slate-600 text-slate-300 hover:bg-slate-800/40' : 'border-slate-200 hover:border-slate-300 text-slate-700 hover:bg-slate-50'">
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <span class="font-medium truncate block" :class="isDark ? 'text-white' : 'text-slate-900'">{{ sess.topDiagnosis }}</span>
                  <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ sess.symptomsSummary }}</span>
                </div>
                <div class="text-right flex-shrink-0 ml-3">
                  <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ formatDate(sess.timestamp) }}</span>
                  <div v-if="sess.confidence" class="text-xs font-semibold" :class="sess.confidence >= 70 ? 'text-emerald-500' : 'text-amber-500'">
                    {{ sess.confidence }}% conf.
                  </div>
                </div>
              </div>
            </button>
          </div>

          <!-- Manual Entry -->
          <div class="space-y-4">
            <p v-if="pastSessions.length === 0" class="text-xs mb-3" :class="isDark ? 'text-slate-400' : 'text-slate-500'">No past diagnoses found. Describe symptoms manually below.</p>
            <div>
              <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Symptoms, duration &amp; severity</label>
              <textarea v-model="manualSymptoms" rows="3" placeholder="Describe symptoms, duration, severity..."
                class="w-full px-4 py-3 rounded-xl border text-sm outline-none transition-colors resize-none"
                :class="isDark
                  ? 'bg-slate-800 border-slate-600 text-white placeholder-slate-500 focus:border-sky-500'
                  : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400 focus:border-sky-500'"></textarea>
            </div>
            <div class="flex gap-3">
              <div class="w-28">
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Age</label>
                <input v-model.number="manualAge" type="number" min="1" max="120" placeholder="35"
                  class="w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors"
                  :class="isDark
                    ? 'bg-slate-800 border-slate-600 text-white focus:border-sky-500'
                    : 'bg-slate-50 border-slate-200 text-slate-900 focus:border-sky-500'" />
              </div>
              <div class="w-36">
                <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Gender</label>
                <select v-model="manualGender"
                  class="w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors appearance-none cursor-pointer"
                  :class="isDark
                    ? 'bg-slate-800 border-slate-600 text-white focus:border-sky-500'
                    : 'bg-slate-50 border-slate-200 text-slate-900 focus:border-sky-500'">
                  <option value="female">Female</option>
                  <option value="male">Male</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Model Selection -->
      <div class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <div class="px-6 py-4 border-b flex items-center gap-3"
          :class="isDark ? 'border-slate-700 bg-sky-900/10' : 'border-slate-200 bg-sky-50/60'">
          <div class="w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">2</div>
          <div>
            <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Select Models</h2>
            <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Choose 2 or more models — more models increase confidence in consensus</p>
          </div>
        </div>
        <div class="p-6">
          <!-- Model Cards Grid -->
          <div class="grid sm:grid-cols-2 gap-3">
            <label v-for="model in availableModels" :key="model.id"
              class="relative flex items-start gap-4 px-5 py-4 rounded-xl border-2 cursor-pointer transition-all"
              :class="selectedModels.includes(model.id)
                ? isDark ? 'border-sky-500 bg-sky-900/20' : 'border-sky-500 bg-sky-50'
                : isDark ? 'border-slate-700 hover:border-slate-600 bg-slate-800/30' : 'border-slate-200 hover:border-slate-300'">
              <input type="checkbox" :value="model.id" v-model="selectedModels" class="mt-0.5 w-4 h-4 rounded border-2 accent-sky-500 flex-shrink-0" />
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between gap-2 mb-1">
                  <span class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ model.name }}</span>
                  <span class="text-xs px-2 py-0.5 rounded-md font-mono font-medium"
                    :class="isDark ? 'bg-slate-700 text-slate-300' : 'bg-slate-100 text-slate-600'">
                    {{ model.estimatedCost }}
                  </span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs font-medium" :class="isDark ? 'text-sky-400' : 'text-sky-600'">{{ model.vendor }}</span>
                  <span class="text-slate-300 text-xs">·</span>
                  <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ model.description }}</span>
                </div>
                <!-- Quality indicator -->
                <div class="flex items-center gap-1.5 mt-2">
                  <div v-for="i in 5" :key="i" class="w-6 h-1 rounded-full"
                    :class="i <= model.quality
                      ? isDark ? 'bg-sky-500' : 'bg-sky-500'
                      : isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>
                  <span class="text-[10px] ml-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Quality</span>
                </div>
              </div>
            </label>
          </div>

          <div class="mt-4 flex items-center justify-between text-xs pt-4 border-t" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
            <span :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ selectedModels.length }} model{{ selectedModels.length !== 1 ? 's' : '' }} selected</span>
            <span v-if="selectedModels.length >= 2" class="font-semibold" :class="isDark ? 'text-sky-400' : 'text-sky-600'">
              Est. total: {{ estimatedTotal }}
            </span>
          </div>
        </div>
      </div>

      <!-- Run Button -->
      <div class="flex justify-center">
        <button @click="runComparison" :disabled="!canRun || running"
          class="px-10 py-3.5 rounded-xl text-sm font-bold transition-all shadow-sm"
          :class="canRun && !running
            ? 'bg-sky-600 text-white hover:bg-sky-700 hover:shadow-md'
            : 'opacity-40 cursor-not-allowed ' + (isDark ? 'bg-slate-700 text-slate-500' : 'bg-slate-200 text-slate-400')">
          <span v-if="running" class="flex items-center gap-2">
            <span class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            Running analysis...
          </span>
          <span v-else>Get Second Opinion</span>
        </button>
      </div>

      <!-- Progress -->
      <div v-if="running" class="bg-white border border-slate-200 rounded-xl shadow-sm p-5"
        :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
        <h3 class="text-sm font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Running Models...</h3>
        <div class="space-y-3">
          <div v-for="model in runningModels" :key="model.id" class="flex items-center gap-3">
            <div class="w-5 h-5 flex items-center justify-center flex-shrink-0">
              <span v-if="model.status === 'done'" class="text-emerald-500">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
              </span>
              <span v-else-if="model.status === 'error'" class="text-amber-500">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
              </span>
              <span v-else class="w-4 h-4 border-2 border-sky-500 border-t-transparent rounded-full animate-spin block"></span>
            </div>
            <span class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ model.name }}</span>
            <span class="text-xs ml-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              {{ model.status === 'done' ? model.time + 's' : model.status === 'error' ? 'Failed' : 'Running...' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Results -->
      <div v-if="results" class="space-y-5">

        <!-- Consensus Report -->
        <div class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
          <div class="px-6 py-4 border-b flex items-center gap-3"
            :class="isDark ? 'border-slate-700 bg-sky-900/10' : 'border-slate-200 bg-sky-50/60'">
            <div class="w-8 h-8 rounded-full bg-sky-600 text-white flex items-center justify-center flex-shrink-0">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
            </div>
            <div>
              <h2 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Consensus Report</h2>
              <p class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ results.modelResults.length }} models analyzed</p>
            </div>
          </div>
          <div class="p-6 space-y-5">
            <!-- Consensus Banner -->
            <div class="rounded-xl px-5 py-4 border"
              :class="consensusLevel === 'strong'
                ? isDark ? 'bg-emerald-900/20 border-emerald-700/50' : 'bg-emerald-50 border-emerald-200'
                : consensusLevel === 'mixed'
                  ? isDark ? 'bg-amber-900/15 border-amber-700/50' : 'bg-amber-50 border-amber-200'
                  : isDark ? 'bg-purple-900/15 border-purple-700/50' : 'bg-purple-50 border-purple-200'">
              <div class="flex items-start gap-4">
                <div class="text-3xl flex-shrink-0">
                  {{ consensusLevel === 'strong' ? '✅' : consensusLevel === 'mixed' ? '⚠️' : '🔍' }}
                </div>
                <div>
                  <h3 class="font-bold text-base"
                    :class="consensusLevel === 'strong'
                      ? isDark ? 'text-emerald-300' : 'text-emerald-800'
                      : consensusLevel === 'mixed'
                        ? isDark ? 'text-amber-300' : 'text-amber-800'
                        : isDark ? 'text-purple-300' : 'text-purple-800'">
                    {{ consensusDiagnosis }}
                  </h3>
                  <p class="text-sm mt-1" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ consensusSummary }}</p>
                </div>
              </div>
            </div>

            <!-- Agreement Matrix -->
            <div>
              <h3 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Agreement Matrix</h3>
              <div class="overflow-x-auto rounded-xl border" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
                <table class="w-full text-sm">
                  <thead>
                    <tr class="border-b" :class="isDark ? 'border-slate-700 bg-slate-800/40' : 'border-slate-200 bg-slate-50'">
                      <th class="text-left px-4 py-2.5 text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Model</th>
                      <th class="text-left px-4 py-2.5 text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Top Diagnosis</th>
                      <th class="text-center px-4 py-2.5 text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Agrees</th>
                      <th class="text-right px-4 py-2.5 text-xs font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Confidence</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="mr in results.modelResults" :key="mr.model" class="border-t" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
                      <td class="px-4 py-3 font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ mr.modelName }}</td>
                      <td class="px-4 py-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ mr.topDiagnosis }}</td>
                      <td class="px-4 py-3 text-center">
                        <span v-if="mr.agreesWithConsensus" class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-500/15 text-emerald-500 text-xs font-bold">Y</span>
                        <span v-else class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-500/15 text-amber-500 text-xs font-bold">N</span>
                      </td>
                      <td class="px-4 py-3 text-right">
                        <span class="font-semibold" :class="mr.confidence >= 70 ? 'text-emerald-500' : mr.confidence >= 40 ? 'text-amber-500' : 'text-slate-400'">
                          {{ mr.confidence }}%
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Combined Confidence -->
            <div class="flex items-center gap-4">
              <div class="text-center flex-shrink-0">
                <div class="text-3xl font-bold" :class="results.combinedConfidence >= 70 ? 'text-emerald-500' : results.combinedConfidence >= 40 ? 'text-amber-500' : 'text-slate-400'">
                  {{ results.combinedConfidence }}%
                </div>
                <div class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Combined Confidence</div>
              </div>
              <div class="flex-1 h-3 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
                <div class="h-full rounded-full transition-all duration-1000"
                  :class="results.combinedConfidence >= 70 ? 'bg-emerald-500' : results.combinedConfidence >= 40 ? 'bg-amber-500' : 'bg-slate-400'"
                  :style="{ width: results.combinedConfidence + '%' }"></div>
              </div>
            </div>

            <!-- Recommended Action -->
            <div class="rounded-xl px-4 py-4 border" :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-slate-50 border-slate-200'">
              <p class="text-xs font-bold uppercase tracking-wider mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Recommended Action</p>
              <p class="text-sm" :class="isDark ? 'text-slate-200' : 'text-slate-800'">{{ recommendedAction }}</p>
            </div>
          </div>
        </div>

        <!-- Disagreements -->
        <div v-if="disagreements.length > 0"
          class="bg-white border border-slate-200 rounded-xl shadow-sm p-5"
          :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
          <h3 class="text-sm font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Points of Disagreement</h3>
          <div class="space-y-3">
            <div v-for="(d, idx) in disagreements" :key="idx"
              class="rounded-xl border px-4 py-3"
              :class="isDark ? 'border-amber-800/40 bg-amber-900/10' : 'border-amber-200 bg-amber-50/60'">
              <p class="text-sm font-medium" :class="isDark ? 'text-amber-300' : 'text-amber-800'">
                {{ d.modelName }} suggests: {{ d.topDiagnosis }}
              </p>
              <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
                Confidence: {{ d.confidence }}% &mdash; {{ d.reasoning || 'Different weighting of presented symptoms.' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Side-by-Side Comparison -->
        <div class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-700' : ''">
          <div class="px-6 py-4 border-b" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
            <h3 class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Side-by-Side Comparison</h3>
          </div>
          <div class="p-6">
            <!-- Card layout for comparison -->
            <div class="grid sm:grid-cols-2 gap-4">
              <div v-for="mr in results.modelResults" :key="mr.model + '_card'"
                class="rounded-xl border p-4"
                :class="mr.agreesWithConsensus
                  ? isDark ? 'border-emerald-700/50 bg-emerald-900/10' : 'border-emerald-200 bg-emerald-50/50'
                  : isDark ? 'border-amber-700/40 bg-amber-900/10' : 'border-amber-200 bg-amber-50/50'">
                <!-- Model header -->
                <div class="flex items-center justify-between mb-3">
                  <span class="text-sm font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ mr.modelName }}</span>
                  <span class="text-xs px-2.5 py-1 rounded-full font-semibold"
                    :class="mr.agreesWithConsensus
                      ? isDark ? 'bg-emerald-900/30 text-emerald-400' : 'bg-emerald-100 text-emerald-700'
                      : isDark ? 'bg-amber-900/30 text-amber-400' : 'bg-amber-100 text-amber-700'">
                    {{ mr.agreesWithConsensus ? 'Agrees' : 'Differs' }}
                  </span>
                </div>
                <!-- Diagnosis -->
                <div class="mb-3">
                  <div class="text-xs font-semibold uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Primary Diagnosis</div>
                  <div class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ mr.topDiagnosis }}</div>
                </div>
                <!-- Confidence bar -->
                <div class="mb-3">
                  <div class="flex justify-between text-xs mb-1">
                    <span :class="isDark ? 'text-slate-400' : 'text-slate-500'">Confidence</span>
                    <span class="font-semibold" :class="mr.confidence >= 70 ? 'text-emerald-500' : 'text-amber-500'">{{ mr.confidence }}%</span>
                  </div>
                  <div class="h-2 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'">
                    <div class="h-full rounded-full" :class="mr.confidence >= 70 ? 'bg-emerald-500' : 'bg-amber-500'" :style="{ width: mr.confidence + '%' }"></div>
                  </div>
                </div>
                <!-- Tests -->
                <div v-if="mr.tests && mr.tests !== 'N/A'" class="mb-2">
                  <div class="text-xs font-semibold uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Key Tests</div>
                  <div class="text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ mr.tests }}</div>
                </div>
                <!-- Treatment -->
                <div v-if="mr.treatment && mr.treatment !== 'N/A'">
                  <div class="text-xs font-semibold uppercase tracking-wider mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Treatment</div>
                  <div class="text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ mr.treatment }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Disclaimer -->
        <div class="text-center pb-2">
          <p class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            This multi-model analysis is for informational purposes only and does not constitute medical advice.
            Always consult a qualified healthcare provider for diagnosis and treatment.
          </p>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTheme } from '@/composables/useTheme'
import AppNav from '@/components/AppNav.vue'
import { diagnose } from '@/services/api'
import { getSessionsAsync, getSessionAsync } from '@/services/historyService'

const { isDark } = useTheme()

// ── Past Sessions ─────────────────────────────────────────────
const pastSessions = ref([])
const selectedCase = ref(null)
const manualSymptoms = ref('')
const manualAge = ref(35)
const manualGender = ref('female')

onMounted(async () => {
  try {
    pastSessions.value = await getSessionsAsync()
  } catch {
    pastSessions.value = []
  }
})

async function selectSession(sess) {
  selectedCase.value = sess
  // Load full session to extract symptoms
  try {
    const full = await getSessionAsync(sess.id)
    if (full) {
      manualSymptoms.value = full.symptoms || sess.symptomsSummary || ''
      manualAge.value = parseInt(full.age) || 35
      manualGender.value = full.gender || 'female'
    }
  } catch {
    manualSymptoms.value = sess.symptomsSummary || ''
  }
}

// ── Model Selection ───────────────────────────────────────────
const availableModels = [
  { id: 'claude-sonnet', name: 'Claude Sonnet', vendor: 'Anthropic', estimatedCost: '$0.02', quality: 5, description: 'Best quality' },
  { id: 'claude-haiku', name: 'Claude Haiku', vendor: 'Anthropic', estimatedCost: '$0.005', quality: 3, description: 'Fast & efficient' },
  { id: 'gpt-4o', name: 'GPT-4o', vendor: 'OpenAI', estimatedCost: '$0.03', quality: 5, description: 'High accuracy' },
  { id: 'gpt-4o-mini', name: 'GPT-4o Mini', vendor: 'OpenAI', estimatedCost: '$0.005', quality: 3, description: 'Cost-effective' },
]

const selectedModels = ref(['claude-sonnet', 'gpt-4o'])

const estimatedTotal = computed(() => {
  const costs = { 'claude-sonnet': 0.02, 'claude-haiku': 0.005, 'gpt-4o': 0.03, 'gpt-4o-mini': 0.005 }
  const total = selectedModels.value.reduce((sum, id) => sum + (costs[id] || 0), 0)
  return '$' + total.toFixed(3)
})

const canRun = computed(() => {
  return selectedModels.value.length >= 2 && (manualSymptoms.value.trim().length > 5)
})

// ── Run Comparison ────────────────────────────────────────────
const running = ref(false)
const runningModels = ref([])
const results = ref(null)

async function runComparison() {
  if (!canRun.value || running.value) return
  running.value = true
  results.value = null

  const models = selectedModels.value.map(id => availableModels.find(m => m.id === id))
  runningModels.value = models.map(m => ({ id: m.id, name: m.name, status: 'running', time: null }))

  const modelResults = []

  // Run each model sequentially through the diagnose endpoint
  for (let i = 0; i < models.length; i++) {
    const model = models[i]
    const startTime = Date.now()
    try {
      const payload = {
        symptoms: manualSymptoms.value,
        age: manualAge.value,
        gender: manualGender.value,
        model_hint: model.id
      }
      const result = await diagnose(payload)
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1)
      runningModels.value[i].status = 'done'
      runningModels.value[i].time = elapsed

      // Parse the result
      const causes = result.causes || []
      const topCause = causes[0] || {}
      const tests = (result.recommended_tests || []).slice(0, 3).join(', ')
      const treatment = (result.recommended_actions || result.recommendations || []).slice(0, 2).join(', ')

      modelResults.push({
        model: model.id,
        modelName: model.name,
        topDiagnosis: topCause.cause || topCause.condition || 'Unable to determine',
        confidence: topCause.value || topCause.confidence || 0,
        tests: tests || 'Standard workup',
        treatment: treatment || 'See full report',
        allCauses: causes,
        reasoning: topCause.reasoning || '',
        raw: result
      })
    } catch (err) {
      runningModels.value[i].status = 'error'
      modelResults.push({
        model: model.id,
        modelName: model.name,
        topDiagnosis: 'Error',
        confidence: 0,
        tests: 'N/A',
        treatment: 'N/A',
        allCauses: [],
        reasoning: err.message || 'Model unavailable',
        raw: null
      })
    }
  }

  // Build consensus
  const validResults = modelResults.filter(r => r.confidence > 0)

  // Find most common top diagnosis (case-insensitive)
  const diagCounts = {}
  validResults.forEach(r => {
    const key = r.topDiagnosis.toLowerCase().trim()
    diagCounts[key] = (diagCounts[key] || 0) + 1
  })
  const sortedDiags = Object.entries(diagCounts).sort((a, b) => b[1] - a[1])
  const topConsensus = sortedDiags[0] ? sortedDiags[0][0] : ''
  const topCount = sortedDiags[0] ? sortedDiags[0][1] : 0

  // Mark agreement
  modelResults.forEach(r => {
    r.agreesWithConsensus = r.topDiagnosis.toLowerCase().trim() === topConsensus
  })

  // Combined confidence
  const avgConfidence = validResults.length > 0
    ? Math.round(validResults.reduce((sum, r) => sum + r.confidence, 0) / validResults.length)
    : 0

  results.value = {
    modelResults,
    topConsensus: validResults.find(r => r.topDiagnosis.toLowerCase().trim() === topConsensus)?.topDiagnosis || 'Inconclusive',
    agreementCount: topCount,
    totalModels: modelResults.length,
    combinedConfidence: avgConfidence
  }

  running.value = false
}

// ── Consensus Computed ────────────────────────────────────────
const consensusLevel = computed(() => {
  if (!results.value) return ''
  const pct = results.value.agreementCount / results.value.totalModels
  if (pct >= 0.8) return 'strong'
  if (pct >= 0.5) return 'mixed'
  return 'disagree'
})

const consensusDiagnosis = computed(() => {
  if (!results.value) return ''
  if (consensusLevel.value === 'strong') {
    return `${results.value.agreementCount} of ${results.value.totalModels} models agree: ${results.value.topConsensus}`
  }
  if (consensusLevel.value === 'mixed') {
    return `Partial agreement: ${results.value.topConsensus}`
  }
  return 'Models disagree on primary diagnosis'
})

const consensusSummary = computed(() => {
  if (!results.value) return ''
  if (consensusLevel.value === 'strong') {
    return 'Strong consensus across AI models supports this diagnosis with high confidence.'
  }
  if (consensusLevel.value === 'mixed') {
    return 'Some models agree, but there are alternative possibilities worth discussing with your doctor.'
  }
  return 'The AI models produced different primary diagnoses. A specialist evaluation is recommended for clarity.'
})

const recommendedAction = computed(() => {
  if (!results.value) return ''
  if (consensusLevel.value === 'strong' && results.value.combinedConfidence >= 70) {
    return 'Your diagnosis is well-supported across multiple AI models. Discuss these findings with your healthcare provider for confirmation.'
  }
  if (consensusLevel.value === 'mixed') {
    return 'Consider discussing these possibilities with your doctor. The partial agreement suggests multiple viable diagnoses that clinical examination can help distinguish.'
  }
  return 'The AI models disagree significantly. We recommend a specialist evaluation to clarify the diagnosis. Bring these results to your appointment for discussion.'
})

const disagreements = computed(() => {
  if (!results.value) return []
  return results.value.modelResults.filter(r => !r.agreesWithConsensus && r.confidence > 0)
})

// ── Formatting ────────────────────────────────────────────────
function formatDate(iso) {
  try { return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) } catch { return iso }
}
</script>
