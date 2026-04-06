<template>
  <div class="space-y-6">
    <!-- Page header -->
    <div>
      <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Model Comparison</h1>
      <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Compare AI models for diagnostic quality, speed, and cost</p>
    </div>

    <!-- Test Configuration -->
    <div class="rounded-2xl border p-5 transition-colors"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <h2 class="text-sm font-semibold mb-4" :class="isDark ? 'text-white' : 'text-slate-900'">Test Configuration</h2>

      <!-- Sample case -->
      <div class="mb-4">
        <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Sample Case</label>
        <textarea v-model="sampleCase" rows="3"
          class="w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors resize-none"
          :class="isDark
            ? 'bg-slate-800 border-slate-600 text-white focus:border-blue-500'
            : 'bg-white border-slate-300 text-slate-900 focus:border-blue-500'"></textarea>
      </div>

      <!-- Age & Gender row -->
      <div class="flex gap-4 mb-4">
        <div class="w-32">
          <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Age</label>
          <input v-model.number="age" type="number" min="1" max="120"
            class="w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors"
            :class="isDark
              ? 'bg-slate-800 border-slate-600 text-white focus:border-blue-500'
              : 'bg-white border-slate-300 text-slate-900 focus:border-blue-500'" />
        </div>
        <div class="w-40">
          <label class="block text-xs font-medium mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Gender</label>
          <select v-model="gender"
            class="w-full px-3 py-2 rounded-lg border text-sm outline-none transition-colors appearance-none cursor-pointer"
            :class="isDark
              ? 'bg-slate-800 border-slate-600 text-white focus:border-blue-500'
              : 'bg-white border-slate-300 text-slate-900 focus:border-blue-500'">
            <option value="female">Female</option>
            <option value="male">Male</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>

      <!-- Model selection -->
      <div class="mb-4">
        <label class="block text-xs font-medium mb-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Models</label>
        <div v-if="modelsLoading" class="flex items-center gap-2 py-4">
          <div class="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Loading available models...</span>
        </div>
        <div v-else-if="modelsByVendor.length === 0" class="py-4 text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          No models available. Configure API keys in Settings.
        </div>
        <div v-else class="space-y-4">
          <div v-for="group in modelsByVendor" :key="group.vendor">
            <div class="text-[11px] font-semibold uppercase tracking-wider mb-2"
              :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ group.vendor }}</div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              <label v-for="model in group.models" :key="model.id"
                class="flex items-start gap-2.5 px-3 py-2.5 rounded-xl border cursor-pointer transition-colors"
                :class="[
                  selectedModels.includes(model.id)
                    ? (isDark ? 'bg-blue-500/10 border-blue-500/40' : 'bg-blue-50 border-blue-300')
                    : (isDark ? 'bg-slate-800/50 border-slate-700 hover:border-slate-600' : 'bg-slate-50 border-slate-200 hover:border-slate-300'),
                  !model.available ? 'opacity-50' : ''
                ]">
                <input type="checkbox" :value="model.id" v-model="selectedModels" :disabled="!model.available"
                  class="mt-0.5 rounded border-slate-400" />
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-1.5">
                    <div class="w-1.5 h-1.5 rounded-full flex-shrink-0"
                      :class="model.available ? 'bg-emerald-500' : 'bg-slate-400'"></div>
                    <span class="text-xs font-medium truncate" :class="isDark ? 'text-white' : 'text-slate-900'">{{ model.name || model.id }}</span>
                  </div>
                  <div v-if="model.pricing" class="text-[10px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
                    Input: ${{ model.pricing.input }} / Output: ${{ model.pricing.output }} per 1M tokens
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Pricing graph — always visible when models are loaded -->
      <div v-if="pricingChartData.length > 0" class="mb-5">
        <label class="block text-xs font-medium mb-3" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Pricing per 1M Tokens</label>
        <div class="rounded-xl border p-4" :class="isDark ? 'bg-slate-800/40 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
          <!-- Chart area -->
          <div class="flex items-end gap-2 justify-center" style="height: 200px;">
            <div v-for="(item, idx) in pricingChartData" :key="item.model"
              class="flex flex-col items-center flex-1 max-w-[70px] min-w-[36px] h-full justify-end group relative">
              <!-- Tooltip on hover -->
              <div class="absolute bottom-full mb-2 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-10">
                <div class="rounded-lg px-2.5 py-1.5 text-[10px] whitespace-nowrap shadow-lg"
                  :class="isDark ? 'bg-slate-900 border border-slate-700 text-white' : 'bg-white border border-slate-200 text-slate-900 shadow-md'">
                  <div class="font-semibold">{{ item.model }}</div>
                  <div :class="isDark ? 'text-slate-400' : 'text-slate-500'">In: ${{ item.input }} &middot; Out: ${{ item.output }}</div>
                  <div :class="isDark ? 'text-slate-400' : 'text-slate-500'">Total: ${{ item.total.toFixed(2) }}</div>
                </div>
              </div>
              <!-- Cost label on top -->
              <div class="text-[8px] font-bold tabular-nums mb-1 transition-colors"
                :class="isDark ? 'text-slate-400 group-hover:text-white' : 'text-slate-500 group-hover:text-slate-900'">
                ${{ item.total < 1 ? item.total.toFixed(2) : item.total.toFixed(1) }}
              </div>
              <!-- Stacked bars: input (bottom) + output (top) -->
              <div class="w-full flex flex-col items-stretch justify-end rounded-t-md overflow-hidden transition-all duration-500"
                :style="{ height: pricingBarHeight(item.total) }">
                <div class="transition-all duration-500" :style="{ flex: item.output + ' 0 0', background: pricingColor(idx, 'output') }"></div>
                <div class="transition-all duration-500" :style="{ flex: item.input + ' 0 0', background: pricingColor(idx, 'input') }"></div>
              </div>
              <!-- Model name -->
              <div class="mt-1.5 text-[8px] font-medium text-center leading-tight truncate w-full transition-colors"
                :class="isDark ? 'text-slate-500 group-hover:text-slate-200' : 'text-slate-400 group-hover:text-slate-700'">
                {{ item.shortName }}
              </div>
              <!-- Vendor dot -->
              <div class="w-1.5 h-1.5 rounded-full mt-0.5" :style="{ background: vendorDotColor(item.vendor) }"></div>
            </div>
          </div>
          <!-- Legend -->
          <div class="flex items-center justify-center gap-4 mt-4 pt-3 border-t" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <div class="flex items-center gap-1.5">
              <div class="w-2 h-2 rounded-sm" style="background: #60a5fa"></div>
              <span class="text-[9px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Input</span>
            </div>
            <div class="flex items-center gap-1.5">
              <div class="w-2 h-2 rounded-sm" style="background: #a78bfa"></div>
              <span class="text-[9px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Output</span>
            </div>
            <div class="w-px h-3" :class="isDark ? 'bg-slate-700' : 'bg-slate-200'"></div>
            <div v-for="v in pricingVendors" :key="v.name" class="flex items-center gap-1">
              <div class="w-2 h-2 rounded-full" :style="{ background: v.color }"></div>
              <span class="text-[9px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ v.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Run button -->
      <button @click="runComparison" :disabled="running || selectedModels.length === 0"
        class="px-5 py-2.5 rounded-xl text-sm font-medium transition-colors disabled:opacity-50"
        :class="isDark ? 'bg-blue-600 text-white hover:bg-blue-500' : 'bg-blue-600 text-white hover:bg-blue-700'">
        {{ running ? 'Running...' : 'Run Comparison' }}
      </button>
    </div>

    <!-- Running progress -->
    <div v-if="running" class="rounded-2xl border p-5 transition-colors"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="flex items-center gap-3">
        <div class="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <div>
          <div class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ progressText }}</div>
          <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">This may take several minutes depending on the number of models selected.</div>
        </div>
      </div>
      <!-- Progress bar -->
      <div class="mt-3 h-2 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
        <div class="h-full rounded-full bg-blue-500 transition-all duration-500"
          :style="{ width: progressPct + '%' }"></div>
      </div>
    </div>

    <!-- Results section -->
    <template v-if="result && result.results && result.results.length > 0">
      <!-- Summary bar -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div v-for="metric in resultSummary" :key="metric.label"
          class="rounded-2xl border p-4 transition-colors"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
          <div class="text-xl font-semibold tabular-nums" :class="isDark ? 'text-white' : 'text-slate-900'">{{ metric.value }}</div>
          <div class="text-xs mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ metric.label }}</div>
        </div>
      </div>

      <!-- Comparison table -->
      <div class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Comparison Results</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr :class="isDark ? 'bg-slate-800/50' : 'bg-slate-50'">
                <th class="text-left px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Model</th>
                <th class="text-left px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Vendor</th>
                <th class="text-left px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Status</th>
                <th class="text-right px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Time</th>
                <th class="text-right px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Cost</th>
                <th class="text-right px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Diagnoses</th>
                <th class="text-left px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Top Diagnosis</th>
                <th class="text-right px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Confidence</th>
                <th class="text-right px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Red Flags</th>
                <th class="text-right px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Tests</th>
                <th class="text-right px-4 py-3 font-semibold" :class="isDark ? 'text-slate-300' : 'text-slate-600'">Tokens</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in result.results" :key="r.model"
                class="border-t transition-colors"
                :class="[
                  isDark ? 'border-slate-800 hover:bg-slate-800/30' : 'border-slate-100 hover:bg-slate-50',
                  r.status === 'failed' ? (isDark ? 'opacity-60' : 'opacity-60') : ''
                ]">
                <td class="px-4 py-3 font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ r.model }}</td>
                <td class="px-4 py-3" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ r.vendor || '--' }}</td>
                <td class="px-4 py-3">
                  <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium"
                    :class="r.status === 'completed'
                      ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700')
                      : r.status === 'failed'
                        ? (isDark ? 'bg-red-500/15 text-red-400' : 'bg-red-100 text-red-700')
                        : (isDark ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-500')">
                    <div class="w-1.5 h-1.5 rounded-full"
                      :class="r.status === 'completed' ? 'bg-emerald-500' : r.status === 'failed' ? 'bg-red-500' : 'bg-slate-400'"></div>
                    {{ r.status }}
                  </span>
                </td>
                <td class="px-4 py-3 text-right tabular-nums"
                  :class="isBestValue(r, 'time') ? 'text-emerald-500 font-semibold' : (isDark ? 'text-slate-300' : 'text-slate-600')">
                  {{ getTimeMs(r) ? (getTimeMs(r) / 1000).toFixed(1) + 's' : '--' }}
                </td>
                <td class="px-4 py-3 text-right tabular-nums"
                  :class="isBestValue(r, 'cost') ? 'text-emerald-500 font-semibold' : (isDark ? 'text-slate-300' : 'text-slate-600')">
                  {{ getCost(r) != null ? '$' + getCost(r).toFixed(4) : '--' }}
                </td>
                <td class="px-4 py-3 text-right tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  {{ r.causes_count ?? r.diagnoses_count ?? '--' }}
                </td>
                <td class="px-4 py-3 max-w-[200px] truncate" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  {{ r.top_diagnosis || '--' }}
                </td>
                <td class="px-4 py-3 text-right tabular-nums"
                  :class="isBestValue(r, 'confidence') ? 'text-emerald-500 font-semibold' : (isDark ? 'text-slate-300' : 'text-slate-600')">
                  {{ getConfidence(r) != null ? getConfidence(r) + '%' : '--' }}
                </td>
                <td class="px-4 py-3 text-right tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  {{ r.red_flags_count ?? '--' }}
                </td>
                <td class="px-4 py-3 text-right tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  {{ r.tests_count ?? '--' }}
                </td>
                <td class="px-4 py-3 text-right tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  {{ getTotalTokens(r) ?? '--' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Side-by-side diagnostic output -->
      <div v-if="outputResults.length > 0" class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b flex items-center justify-between" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <div>
            <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Diagnostic Output Comparison</h2>
            <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Side-by-side view of each model's full diagnostic output</p>
          </div>
          <!-- Section toggle buttons -->
          <div class="flex gap-1">
            <button v-for="sec in outputSections" :key="sec.key" @click="toggleOutputSection(sec.key)"
              class="px-2 py-1 rounded-md text-[10px] font-medium transition-colors"
              :class="activeOutputSections.includes(sec.key)
                ? (isDark ? 'bg-blue-500/20 text-blue-400' : 'bg-blue-100 text-blue-700')
                : (isDark ? 'bg-slate-800 text-slate-500 hover:text-slate-300' : 'bg-slate-100 text-slate-400 hover:text-slate-600')">
              {{ sec.label }}
            </button>
          </div>
        </div>
        <!-- Top model scroller — visible when models overflow -->
        <div v-if="outputResults.length > 2" class="border-b overflow-x-auto flex items-center gap-1 px-4 py-2"
          :class="isDark ? 'border-slate-800 bg-slate-900/60' : 'border-slate-100 bg-slate-50/60'"
          ref="outputTabsRef"
          @scroll="syncScrollFromTabs">
          <button v-for="(r, idx) in outputResults" :key="r.model"
            @click="scrollToOutputModel(idx)"
            class="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[10px] font-medium transition-all border"
            :class="activeOutputModel === idx
              ? (isDark ? 'bg-blue-500/15 border-blue-500/40 text-blue-400' : 'bg-blue-50 border-blue-300 text-blue-700')
              : (isDark ? 'bg-slate-800/60 border-slate-700/50 text-slate-400 hover:text-white hover:border-slate-600' : 'bg-white border-slate-200 text-slate-500 hover:text-slate-900 hover:border-slate-300')">
            <div class="w-1.5 h-1.5 rounded-full flex-shrink-0" :class="r.status === 'completed' ? 'bg-emerald-500' : 'bg-red-500'"></div>
            {{ r.model }}
            <span v-if="getCost(r) != null" class="tabular-nums opacity-70">${{ getCost(r).toFixed(4) }}</span>
          </button>
        </div>
        <!-- Top scrollbar — mirrors the bottom scroll -->
        <div class="overflow-x-auto" ref="topScrollRef" @scroll="syncFromTop"
          :class="isDark ? 'border-b border-slate-800' : 'border-b border-slate-100'"
          style="height: 12px; overflow-y: hidden;">
          <div :style="{ width: outputResults.length * 350 + 'px', height: '1px' }"></div>
        </div>
        <div class="overflow-x-auto" ref="outputScrollRef" @scroll="syncFromBottom">
          <div class="flex min-w-0" :style="{ minWidth: outputResults.length * 350 + 'px' }">
            <!-- One column per model -->
            <div v-for="r in outputResults" :key="r.model"
              class="flex-1 min-w-[350px] max-w-[500px] border-r last:border-r-0"
              :class="isDark ? 'border-slate-800' : 'border-slate-100'">
              <!-- Model header -->
              <div class="sticky top-0 px-4 py-3 border-b"
                :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-slate-50 border-slate-100'">
                <div class="flex items-center gap-2">
                  <div class="w-2 h-2 rounded-full" :class="r.status === 'completed' ? 'bg-emerald-500' : 'bg-red-500'"></div>
                  <span class="text-xs font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ r.model }}</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded-full" :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-200 text-slate-500'">{{ r.vendor }}</span>
                </div>
                <div class="flex items-center gap-3 mt-1.5">
                  <div v-if="getConfidence(r) != null" class="text-[10px]" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Top: {{ r.top_diagnosis }} ({{ getConfidence(r) }}%)
                  </div>
                </div>
                <!-- Pricing stats -->
                <div class="flex items-center gap-2.5 mt-1.5 flex-wrap">
                  <span v-if="getCost(r) != null" class="inline-flex items-center gap-1 text-[10px] font-semibold px-1.5 py-0.5 rounded-md"
                    :class="getCost(r) === 0
                      ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-600')
                      : getCost(r) < 0.01
                        ? (isDark ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-600')
                        : getCost(r) < 0.5
                          ? (isDark ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600')
                          : (isDark ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600')">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    ${{ getCost(r).toFixed(4) }}
                  </span>
                  <span v-if="getTimeMs(r)" class="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded-md"
                    :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    {{ (getTimeMs(r) / 1000).toFixed(1) }}s
                  </span>
                  <span v-if="getTotalTokens(r)" class="inline-flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded-md"
                    :class="isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-500'">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"/></svg>
                    {{ getTotalTokens(r).toLocaleString() }} tok
                  </span>
                </div>
              </div>
              <div class="p-4 space-y-4 text-xs" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                <template v-if="r.diagnosis_output && hasAnyOutput(r.diagnosis_output)">
                  <!-- Differential Diagnoses -->
                  <div v-if="activeOutputSections.includes('diagnoses') && r.diagnosis_output.causes?.length">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-blue-400' : 'text-blue-600'">Differential Diagnoses</div>
                    <div v-for="(c, i) in r.diagnosis_output.causes" :key="i" class="mb-2 pl-2 border-l-2"
                      :class="i === 0
                        ? (isDark ? 'border-emerald-500' : 'border-emerald-400')
                        : (isDark ? 'border-slate-700' : 'border-slate-200')">
                      <div class="flex items-baseline gap-1.5">
                        <span class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ c.cause || c.condition || c.name || '--' }}</span>
                        <span v-if="getDxConfidence(c)" class="text-[10px] font-medium"
                          :class="getDxConfidence(c) >= 50 ? 'text-emerald-500' : (isDark ? 'text-slate-500' : 'text-slate-400')">{{ getDxConfidence(c) }}%</span>
                      </div>
                      <p v-if="c.reasoning || c.explanation || c.bayesian_reasoning" class="mt-0.5 text-[11px] leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ c.reasoning || c.explanation || c.bayesian_reasoning }}</p>
                    </div>
                  </div>

                  <!-- Red Flags -->
                  <div v-if="activeOutputSections.includes('redflags') && r.diagnosis_output.red_flags?.length">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-red-400' : 'text-red-600'">Red Flags</div>
                    <ul class="space-y-1">
                      <li v-for="(flag, i) in r.diagnosis_output.red_flags" :key="i" class="flex items-start gap-1.5">
                        <span class="text-red-500 flex-shrink-0 mt-0.5">!</span>
                        <span>{{ typeof flag === 'string' ? flag : (flag.flag || flag.description || flag.message || JSON.stringify(flag)) }}</span>
                      </li>
                    </ul>
                  </div>

                  <!-- Recommended Tests -->
                  <div v-if="activeOutputSections.includes('tests') && r.diagnosis_output.recommended_tests?.length">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-amber-400' : 'text-amber-600'">Recommended Tests</div>
                    <ul class="space-y-1">
                      <li v-for="(test, i) in r.diagnosis_output.recommended_tests" :key="i" class="flex items-start gap-1.5">
                        <span class="flex-shrink-0 mt-0.5" :class="isDark ? 'text-amber-500' : 'text-amber-600'">&#8594;</span>
                        <span>{{ typeof test === 'string' ? test : (test.test || test.name || test.description || JSON.stringify(test)) }}</span>
                      </li>
                    </ul>
                  </div>

                  <!-- Treatment Plan -->
                  <div v-if="activeOutputSections.includes('treatment') && hasTreatment(r.diagnosis_output)">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Treatment Plan</div>
                    <div class="space-y-2 text-[11px] leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                      <template v-if="Array.isArray(r.diagnosis_output.treatment_plan)">
                        <div v-for="(t, i) in r.diagnosis_output.treatment_plan" :key="i" class="pl-2 border-l-2" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
                          <span class="font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ t.name || t.condition || t.title || `Plan ${i+1}` }}</span>
                          <p v-if="t.description || t.approach || t.details" class="mt-0.5">{{ t.description || t.approach || t.details }}</p>
                          <ul v-if="t.medications?.length" class="mt-1 space-y-0.5">
                            <li v-for="(med, j) in t.medications" :key="j">&#8226; {{ formatMed(med) }}</li>
                          </ul>
                          <ul v-if="t.lifestyle?.length" class="mt-1 space-y-0.5">
                            <li v-for="(l, j) in t.lifestyle" :key="j" class="text-emerald-400">&#10003; {{ typeof l === 'string' ? l : (l.recommendation || JSON.stringify(l)) }}</li>
                          </ul>
                        </div>
                      </template>
                      <template v-else-if="typeof r.diagnosis_output.treatment_plan === 'object'">
                        <pre class="whitespace-pre-wrap text-[10px]">{{ JSON.stringify(r.diagnosis_output.treatment_plan, null, 2) }}</pre>
                      </template>
                    </div>
                    <!-- Standalone medications list -->
                    <div v-if="r.diagnosis_output.medications?.length" class="mt-2">
                      <div class="text-[10px] font-semibold mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Medications</div>
                      <ul class="space-y-0.5 text-[11px]" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                        <li v-for="(med, i) in r.diagnosis_output.medications" :key="i">&#8226; {{ formatMed(med) }}</li>
                      </ul>
                    </div>
                    <!-- Lifestyle -->
                    <div v-if="r.diagnosis_output.lifestyle?.length" class="mt-2">
                      <div class="text-[10px] font-semibold mb-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Lifestyle</div>
                      <ul class="space-y-0.5 text-[11px]" :class="isDark ? 'text-emerald-400/80' : 'text-emerald-600'">
                        <li v-for="(l, i) in r.diagnosis_output.lifestyle" :key="i">&#10003; {{ typeof l === 'string' ? l : (l.recommendation || l.name || JSON.stringify(l)) }}</li>
                      </ul>
                    </div>
                  </div>

                  <!-- Safety -->
                  <div v-if="activeOutputSections.includes('safety') && hasSafety(r.diagnosis_output)">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-purple-400' : 'text-purple-600'">Safety Review</div>
                    <div class="text-[11px] leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                      <div v-if="r.diagnosis_output.safety_status" class="mb-1 font-medium"
                        :class="r.diagnosis_output.safety_status === 'safe' ? 'text-emerald-500' : 'text-amber-500'">
                        Status: {{ r.diagnosis_output.safety_status }}
                      </div>
                      <p v-if="r.diagnosis_output.safety?.safety_summary">{{ r.diagnosis_output.safety.safety_summary }}</p>
                      <ul v-if="r.diagnosis_output.safety_warnings?.length" class="mt-1 space-y-0.5">
                        <li v-for="(w, i) in r.diagnosis_output.safety_warnings" :key="i">&#9888; {{ typeof w === 'string' ? w : (w.warning || w.message || JSON.stringify(w)) }}</li>
                      </ul>
                      <ul v-else-if="r.diagnosis_output.safety?.warnings?.length" class="mt-1 space-y-0.5">
                        <li v-for="(w, i) in r.diagnosis_output.safety.warnings" :key="i">&#9888; {{ typeof w === 'string' ? w : (w.warning || w.message || JSON.stringify(w)) }}</li>
                      </ul>
                    </div>
                  </div>

                  <!-- Summary -->
                  <div v-if="activeOutputSections.includes('summary') && r.diagnosis_output.summary">
                    <div class="text-[10px] font-bold uppercase tracking-wider mb-2" :class="isDark ? 'text-teal-400' : 'text-teal-600'">Patient Summary</div>
                    <p class="text-[11px] leading-relaxed whitespace-pre-line" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ r.diagnosis_output.summary }}</p>
                    <!-- Action checklist -->
                    <ul v-if="r.diagnosis_output.action_checklist?.length" class="mt-2 space-y-0.5">
                      <li v-for="(a, i) in r.diagnosis_output.action_checklist" :key="i" class="text-[11px]" :class="isDark ? 'text-blue-400' : 'text-blue-600'">&#9744; {{ typeof a === 'string' ? a : (a.action || a.item || JSON.stringify(a)) }}</li>
                    </ul>
                    <!-- Warning signs -->
                    <div v-if="r.diagnosis_output.warning_signs?.length" class="mt-2">
                      <div class="text-[10px] font-semibold mb-1 text-amber-500">Warning Signs</div>
                      <ul class="space-y-0.5 text-[11px]" :class="isDark ? 'text-amber-400/80' : 'text-amber-600'">
                        <li v-for="(w, i) in r.diagnosis_output.warning_signs" :key="i">&#9888; {{ w }}</li>
                      </ul>
                    </div>
                  </div>
                </template>
                <div v-else class="py-8 text-center" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
                  <template v-if="r.status === 'failed'">
                    <p class="text-red-400">Failed: {{ r.error || 'Unknown error' }}</p>
                  </template>
                  <template v-else>
                    No diagnostic output available
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Per-agent timing breakdown -->
      <div v-if="completedResults.length > 0" class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Per-Agent Timing Breakdown</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Processing time per agent for each model</p>
        </div>
        <div class="p-5 space-y-6">
          <div v-for="r in completedResults" :key="r.model">
            <div class="text-xs font-semibold mb-2" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ r.model }}</div>
            <div v-if="r.agent_timings && Object.keys(r.agent_timings).length > 0" class="space-y-1.5">
              <div v-for="(ms, agent) in r.agent_timings" :key="agent" class="flex items-center gap-3">
                <span class="text-[10px] font-medium capitalize w-20 text-right flex-shrink-0"
                  :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ agent }}</span>
                <div class="flex-1 h-4 rounded-md overflow-hidden"
                  :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                  <div class="h-full rounded-md transition-all duration-500"
                    :class="agentTimingBarColor(ms)"
                    :style="{ width: agentTimingBarWidth(r.agent_timings, ms) }"></div>
                </div>
                <span class="text-[10px] tabular-nums w-12 flex-shrink-0"
                  :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ (ms / 1000).toFixed(1) }}s</span>
              </div>
            </div>
            <div v-else class="text-xs" :class="isDark ? 'text-slate-500' : 'text-slate-400'">No agent timing data available</div>
          </div>
        </div>
      </div>

      <!-- Cost Graph -->
      <div v-if="costChartData.length > 0" class="rounded-2xl border overflow-hidden"
        :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
        <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
          <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Cost Comparison</h2>
          <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Total cost per model, sorted cheapest to most expensive</p>
        </div>
        <div class="p-5">
          <!-- Y-axis scale labels -->
          <div class="flex items-end gap-1 mb-1" style="padding-left: 0; padding-right: 16px;">
            <div class="w-full flex justify-between text-[9px] tabular-nums" :class="isDark ? 'text-slate-600' : 'text-slate-300'">
              <span>$0</span>
              <span>${{ (costChartMax / 4).toFixed(4) }}</span>
              <span>${{ (costChartMax / 2).toFixed(4) }}</span>
              <span>${{ (costChartMax * 3 / 4).toFixed(4) }}</span>
              <span>${{ costChartMax.toFixed(4) }}</span>
            </div>
          </div>
          <!-- Grid lines -->
          <div class="relative" :style="{ height: costChartData.length * 52 + 'px' }">
            <div class="absolute inset-0 flex justify-between pointer-events-none" style="padding: 0">
              <div v-for="i in 5" :key="i" class="h-full border-l" :class="isDark ? 'border-slate-800/80' : 'border-slate-100'" :style="{ left: ((i - 1) * 25) + '%' }"></div>
            </div>
            <!-- Bars -->
            <div class="relative space-y-2">
              <div v-for="(item, idx) in costChartData" :key="item.model" class="flex items-center gap-3">
                <span class="text-[10px] font-medium w-32 text-right flex-shrink-0 truncate"
                  :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ item.model }}</span>
                <div class="flex-1 flex items-center gap-0 h-9 relative">
                  <!-- Input cost bar -->
                  <div class="h-full rounded-l-md transition-all duration-700 relative group"
                    :class="idx === 0 ? 'bg-emerald-500' : 'bg-blue-500'"
                    :style="{ width: costBarPct(item.inputCost) + '%', minWidth: item.inputCost > 0 ? '2px' : '0' }">
                    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-[8px] font-bold text-white whitespace-nowrap z-10">
                      ${{ item.inputCost.toFixed(4) }}
                    </div>
                  </div>
                  <!-- Output cost bar -->
                  <div class="h-full rounded-r-md transition-all duration-700 relative group"
                    :class="idx === 0 ? 'bg-emerald-400' : 'bg-purple-500'"
                    :style="{ width: costBarPct(item.outputCost) + '%', minWidth: item.outputCost > 0 ? '2px' : '0' }">
                    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity text-[8px] font-bold text-white whitespace-nowrap z-10">
                      ${{ item.outputCost.toFixed(4) }}
                    </div>
                  </div>
                  <!-- Total label -->
                  <span class="ml-2 text-[10px] tabular-nums font-semibold flex-shrink-0"
                    :class="idx === 0 ? 'text-emerald-500' : (isDark ? 'text-slate-300' : 'text-slate-600')">
                    ${{ item.total.toFixed(4) }}
                  </span>
                  <!-- Cheapest badge -->
                  <span v-if="idx === 0 && costChartData.length > 1"
                    class="ml-1.5 text-[8px] font-bold px-1.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400">
                    CHEAPEST
                  </span>
                </div>
              </div>
            </div>
          </div>
          <!-- Legend + total -->
          <div class="flex items-center justify-between mt-4 pt-3 border-t" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
            <div class="flex items-center gap-4">
              <div class="flex items-center gap-1.5">
                <div class="w-2.5 h-2.5 rounded-sm bg-blue-500"></div>
                <span class="text-[10px]" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Input tokens</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div class="w-2.5 h-2.5 rounded-sm bg-purple-500"></div>
                <span class="text-[10px]" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Output tokens</span>
              </div>
              <div class="flex items-center gap-1.5">
                <div class="w-2.5 h-2.5 rounded-sm bg-emerald-500"></div>
                <span class="text-[10px]" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Cheapest model</span>
              </div>
            </div>
            <div class="text-[10px] font-semibold tabular-nums" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
              Total: ${{ costChartData.reduce((s, d) => s + d.total, 0).toFixed(4) }}
            </div>
          </div>
          <!-- Cost multiplier comparison -->
          <div v-if="costChartData.length >= 2" class="mt-3 text-[10px]" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            Most expensive ({{ costChartData[costChartData.length - 1].model }}) is
            <span class="font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">
              {{ costChartData[0].total > 0 ? (costChartData[costChartData.length - 1].total / costChartData[0].total).toFixed(1) : '--' }}x
            </span>
            the cost of cheapest ({{ costChartData[0].model }})
          </div>
        </div>
      </div>
    </template>

    <!-- History section -->
    <div class="rounded-2xl border overflow-hidden"
      :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white border-slate-200 shadow-sm'">
      <div class="px-5 py-4 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-100'">
        <h2 class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Comparison History</h2>
        <p class="text-[11px] mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Past model comparisons</p>
      </div>
      <div class="p-5">
        <div v-if="historyLoading" class="flex items-center justify-center py-8">
          <div class="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
        <div v-else-if="history.length === 0" class="text-center py-8 text-xs"
          :class="isDark ? 'text-slate-500' : 'text-slate-400'">
          No comparison history yet. Run a comparison to get started.
        </div>
        <div v-else class="space-y-2">
          <button v-for="entry in history" :key="entry.id" @click="loadComparison(entry.id)"
            class="w-full flex items-center gap-4 px-4 py-3 rounded-xl border text-left transition-colors"
            :class="isDark
              ? 'bg-slate-800/40 border-slate-700 hover:bg-slate-800/70'
              : 'bg-slate-50 border-slate-200 hover:bg-slate-100'">
            <span class="text-[10px] font-mono flex-shrink-0" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ entry.id?.slice(0, 8) || '--' }}</span>
            <span class="text-xs flex-shrink-0" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ formatDate(entry.created_at || entry.started_at) }}</span>
            <span class="text-xs flex-1 truncate" :class="isDark ? 'text-slate-300' : 'text-slate-600'">{{ (entry.models || entry.models_requested || []).join(', ') }}</span>
            <span class="text-[10px] px-2 py-0.5 rounded-full flex-shrink-0"
              :class="entry.status === 'completed'
                ? (isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-100 text-emerald-700')
                : (isDark ? 'bg-slate-500/15 text-slate-400' : 'bg-slate-100 text-slate-500')">
              {{ entry.status || 'completed' }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Error toast -->
    <Teleport to="body">
      <Transition enter-active-class="transition ease-out duration-200" enter-from-class="opacity-0 translate-y-2" enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-150" leave-from-class="opacity-100 translate-y-0" leave-to-class="opacity-0 translate-y-2">
        <div v-if="toast.show" class="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-xl shadow-lg text-sm font-medium flex items-center gap-2"
          :class="toast.type === 'success'
            ? 'bg-emerald-600 text-white'
            : 'bg-red-600 text-white'">
          <svg v-if="toast.type === 'success'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
          {{ toast.message }}
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useTheme } from '@/composables/useTheme.js'
import { getAvailableModels, runModelComparison, getComparisons, getComparison } from '@/services/adminApi.js'

const { isDark } = useTheme()

// Form state
const sampleCase = ref('I have been experiencing persistent headaches for the past 2 weeks, mostly on the right side. The pain is throbbing, rated 6/10. I also have some light sensitivity and occasional nausea.')
const age = ref(35)
const gender = ref('female')
const selectedModels = ref([])

// Models
const availableModels = ref([])
const modelsLoading = ref(true)

// Comparison state
const running = ref(false)
const progressText = ref('Starting comparison...')
const progressPct = ref(0)
const result = ref(null)

// History
const history = ref([])
const historyLoading = ref(false)

// Toast
const toast = ref({ show: false, message: '', type: 'success' })

function showToast(message, type = 'success') {
  toast.value = { show: true, message, type }
  setTimeout(() => { toast.value.show = false }, 3000)
}

// Pricing chart data — from catalog pricing, always visible
const VENDOR_COLORS = {
  anthropic: '#f97316',  // orange
  openai: '#22c55e',     // green
  google: '#3b82f6',     // blue
  ollama: '#a855f7',     // purple
}
const BAR_COLORS = [
  ['#f97316', '#fb923c'], // orange
  ['#ef4444', '#f87171'], // red
  ['#3b82f6', '#60a5fa'], // blue
  ['#8b5cf6', '#a78bfa'], // violet
  ['#22c55e', '#4ade80'], // green
  ['#ec4899', '#f472b6'], // pink
  ['#14b8a6', '#2dd4bf'], // teal
  ['#f59e0b', '#fbbf24'], // amber
  ['#06b6d4', '#22d3ee'], // cyan
  ['#6366f1', '#818cf8'], // indigo
  ['#d946ef', '#e879f9'], // fuchsia
  ['#84cc16', '#a3e635'], // lime
  ['#64748b', '#94a3b8'], // slate
  ['#e11d48', '#fb7185'], // rose
  ['#0ea5e9', '#38bdf8'], // sky
  ['#10b981', '#34d399'], // emerald
]

const pricingChartData = computed(() => {
  return availableModels.value
    .filter(m => m.pricing && m.pricing.input + m.pricing.output > 0)
    .map(m => ({
      model: m.id,
      shortName: m.id.replace('claude-', '').replace('gemini-', 'gem-'),
      vendor: m.vendor,
      input: m.pricing.input,
      output: m.pricing.output,
      total: m.pricing.input + m.pricing.output,
    }))
    .sort((a, b) => a.total - b.total)
})

const pricingChartMax = computed(() => {
  if (pricingChartData.value.length === 0) return 1
  return Math.max(...pricingChartData.value.map(d => d.total))
})

const pricingVendors = computed(() => {
  const seen = new Set()
  return pricingChartData.value
    .filter(d => { if (seen.has(d.vendor)) return false; seen.add(d.vendor); return true })
    .map(d => ({ name: d.vendor, color: VENDOR_COLORS[d.vendor] || '#64748b' }))
})

function pricingBarHeight(total) {
  const pct = (total / pricingChartMax.value) * 100
  return Math.max(pct, 3) + '%'
}

function pricingColor(idx, type) {
  const pair = BAR_COLORS[idx % BAR_COLORS.length]
  return type === 'input' ? pair[0] : pair[1]
}

function vendorDotColor(vendor) {
  return VENDOR_COLORS[vendor] || '#64748b'
}

// Group models by vendor
const modelsByVendor = computed(() => {
  const groups = {}
  for (const model of availableModels.value) {
    const vendor = model.vendor || 'Other'
    if (!groups[vendor]) groups[vendor] = []
    groups[vendor].push(model)
  }
  return Object.entries(groups).map(([vendor, models]) => ({ vendor, models }))
})

// Completed results for charts
const completedResults = computed(() => {
  if (!result.value?.results) return []
  return result.value.results.filter(r => r.status === 'completed')
})

// Results that have diagnostic output (for side-by-side view)
const outputResults = computed(() => {
  if (!result.value?.results) return []
  return result.value.results.filter(r => r.status === 'completed' || r.status === 'failed')
})

// Output section toggles
const outputSections = [
  { key: 'diagnoses', label: 'Diagnoses' },
  { key: 'redflags', label: 'Red Flags' },
  { key: 'tests', label: 'Tests' },
  { key: 'treatment', label: 'Treatment' },
  { key: 'safety', label: 'Safety' },
  { key: 'summary', label: 'Summary' },
]
const activeOutputSections = ref(['diagnoses', 'redflags', 'tests', 'treatment', 'safety', 'summary'])

function toggleOutputSection(key) {
  const idx = activeOutputSections.value.indexOf(key)
  if (idx >= 0) activeOutputSections.value.splice(idx, 1)
  else activeOutputSections.value.push(key)
}

// Output scroll sync
const outputScrollRef = ref(null)
const outputTabsRef = ref(null)
const topScrollRef = ref(null)
const activeOutputModel = ref(0)
let _syncingScroll = false

function scrollToOutputModel(idx) {
  activeOutputModel.value = idx
  const container = outputScrollRef.value
  if (!container) return
  const colWidth = container.scrollWidth / outputResults.value.length
  const left = colWidth * idx
  container.scrollTo({ left, behavior: 'smooth' })
}

function syncFromBottom() {
  if (_syncingScroll) return
  _syncingScroll = true
  const bottom = outputScrollRef.value
  const top = topScrollRef.value
  if (bottom && top) {
    top.scrollLeft = bottom.scrollLeft
  }
  if (bottom && outputResults.value.length > 0) {
    const colWidth = bottom.scrollWidth / outputResults.value.length
    activeOutputModel.value = Math.round(bottom.scrollLeft / colWidth)
  }
  requestAnimationFrame(() => { _syncingScroll = false })
}

function syncFromTop() {
  if (_syncingScroll) return
  _syncingScroll = true
  const bottom = outputScrollRef.value
  const top = topScrollRef.value
  if (bottom && top) {
    bottom.scrollLeft = top.scrollLeft
  }
  if (bottom && outputResults.value.length > 0) {
    const colWidth = bottom.scrollWidth / outputResults.value.length
    activeOutputModel.value = Math.round(top.scrollLeft / colWidth)
  }
  requestAnimationFrame(() => { _syncingScroll = false })
}

function hasTreatment(output) {
  if (!output) return false
  if (output.treatment_plan) {
    if (Array.isArray(output.treatment_plan)) return output.treatment_plan.length > 0
    return true
  }
  return !!(output.medications?.length || output.lifestyle?.length)
}

function hasSafety(output) {
  if (!output) return false
  return !!(
    output.safety_status ||
    output.safety_warnings?.length ||
    (output.safety && Object.keys(output.safety).length)
  )
}

function hasAnyOutput(output) {
  if (!output) return false
  return !!(
    output.causes?.length ||
    output.red_flags?.length ||
    output.recommended_tests?.length ||
    hasTreatment(output) ||
    hasSafety(output) ||
    output.summary
  )
}

function getDxConfidence(c) {
  return c.value || c.confidence || c.confidence_pct || null
}

function formatMed(med) {
  if (typeof med === 'string') return med
  const name = med.name || med.medication || med.drug || ''
  const dose = med.dosage || med.dose || ''
  const freq = med.frequency || ''
  if (name && dose) return `${name} — ${dose}${freq ? ' ' + freq : ''}`
  if (name) return name
  return JSON.stringify(med)
}

// Summary metrics
const resultSummary = computed(() => {
  if (!result.value?.results) return []
  const results = result.value.results
  const completed = results.filter(r => r.status === 'completed')
  const times = completed.map(r => getTimeMs(r)).filter(Boolean)
  const costs = completed.map(r => getCost(r)).filter(c => c != null)
  const totalCost = costs.reduce((s, c) => s + c, 0)

  return [
    { label: 'Models Tested', value: results.length },
    { label: 'Total Cost', value: totalCost > 0 ? '$' + totalCost.toFixed(4) : '--' },
    { label: 'Best Time', value: times.length > 0 ? (Math.min(...times) / 1000).toFixed(1) + 's' : '--' },
    { label: 'Best Cost', value: costs.length > 0 ? '$' + Math.min(...costs).toFixed(4) : '--' },
  ]
})

// Field accessors — backend uses total_time/estimated_cost/top_confidence, template expects time_ms/cost/confidence
function getTimeMs(r) { return r.time_ms ?? r.total_time ?? null }
function getCost(r) { return r.cost ?? r.estimated_cost ?? null }
function getConfidence(r) { return r.confidence ?? r.top_confidence ?? null }
function getTotalTokens(r) {
  if (r.total_tokens != null) return r.total_tokens
  if (r.token_usage) {
    const u = r.token_usage
    return (u.total_input || 0) + (u.total_output || 0) || (u.input_tokens || 0) + (u.output_tokens || 0) || null
  }
  return null
}

// Best value detection for color-coding
function isBestValue(row, field) {
  if (!result.value?.results || row.status !== 'completed') return false
  const completed = result.value.results.filter(r => r.status === 'completed')
  if (field === 'time') {
    const times = completed.map(r => getTimeMs(r)).filter(Boolean)
    return times.length > 0 && getTimeMs(row) === Math.min(...times)
  }
  if (field === 'cost') {
    const costs = completed.map(r => getCost(r)).filter(c => c != null)
    return costs.length > 0 && getCost(row) === Math.min(...costs)
  }
  if (field === 'confidence') {
    const confs = completed.map(r => getConfidence(r)).filter(c => c != null)
    return confs.length > 0 && getConfidence(row) === Math.max(...confs)
  }
  return false
}

// Agent timing bar helpers
function agentTimingBarWidth(timings, ms) {
  const max = Math.max(...Object.values(timings), 1)
  return (ms / max * 100) + '%'
}

function agentTimingBarColor(ms) {
  if (ms < 3000) return 'bg-emerald-500'
  if (ms < 8000) return 'bg-amber-500'
  return 'bg-red-500'
}

// Cost chart data — sorted cheapest first
const costChartData = computed(() => {
  return completedResults.value
    .map(r => {
      const total = getCost(r) || 0
      const tu = r.token_usage || {}
      // Estimate input vs output cost split from token counts if available
      const inputTokens = tu.total_input || tu.input_tokens || 0
      const outputTokens = tu.total_output || tu.output_tokens || 0
      const totalTokens = inputTokens + outputTokens
      const inputCost = totalTokens > 0 ? total * (inputTokens / totalTokens) : total * 0.4
      const outputCost = totalTokens > 0 ? total * (outputTokens / totalTokens) : total * 0.6
      return { model: r.model, vendor: r.vendor, total, inputCost, outputCost }
    })
    .sort((a, b) => a.total - b.total)
})

const costChartMax = computed(() => {
  if (costChartData.value.length === 0) return 1
  return Math.max(...costChartData.value.map(d => d.total), 0.0001)
})

function costBarPct(value) {
  return (value / costChartMax.value) * 100
}

function formatDate(ts) {
  if (!ts) return '--'
  try {
    const d = new Date(ts)
    return d.toLocaleDateString() + ' ' + d.toLocaleTimeString()
  } catch (e) {
    return ts
  }
}

// Fetch available models
async function fetchModels() {
  modelsLoading.value = true
  try {
    const data = await getAvailableModels()
    const raw = data.models || data || []
    // Normalize backend fields to what the template expects
    availableModels.value = raw.map(m => ({
      id: m.id || m.model || m.model_id,
      name: m.name || m.model || m.model_id || m.id,
      vendor: m.vendor || 'unknown',
      available: m.available ?? false,
      pricing: (m.input_price != null || m.output_price != null)
        ? { input: m.input_price ?? 0, output: m.output_price ?? 0 }
        : m.pricing || null,
    }))
    // Don't auto-select — let the user choose which models to compare
  } catch (e) {
    console.error('Failed to fetch models:', e)
    showToast('Failed to load available models', 'error')
  } finally {
    modelsLoading.value = false
  }
}

// Fetch comparison history
async function fetchHistory() {
  historyLoading.value = true
  try {
    const data = await getComparisons(20)
    history.value = data.comparisons || data || []
  } catch (e) {
    console.error('Failed to fetch comparison history:', e)
  } finally {
    historyLoading.value = false
  }
}

// Run comparison — starts backend job then polls for results
let pollTimer = null
async function runComparison() {
  if (selectedModels.value.length === 0) return
  running.value = true
  result.value = null
  progressPct.value = 0
  progressText.value = 'Starting comparison...'

  const totalModels = selectedModels.value.length

  try {
    // POST kicks off background work, returns immediately with { id, status }
    const data = await runModelComparison({
      symptoms: sampleCase.value,
      age: age.value,
      gender: gender.value,
      models: selectedModels.value,
    })

    const compId = data.id
    if (!compId) {
      // Fallback: backend returned full result synchronously (legacy)
      result.value = data
      progressPct.value = 100
      progressText.value = 'Comparison complete!'
      showToast('Comparison completed successfully', 'success')
      fetchHistory()
      running.value = false
      return
    }

    // Poll for incremental results
    pollTimer = setInterval(async () => {
      try {
        const comp = await getComparison(compId)
        if (!comp) return

        const doneCount = (comp.results || []).length
        progressPct.value = Math.round((doneCount / totalModels) * 100)

        if (doneCount > 0) {
          const latest = comp.results[doneCount - 1]
          progressText.value = `Completed ${doneCount} of ${totalModels}: ${latest.model} (${latest.status})`
        } else {
          progressText.value = `Running model 1 of ${totalModels}...`
        }

        // Show partial results as they come in
        result.value = comp

        if (comp.status === 'completed' || comp.status === 'partial' || doneCount >= totalModels) {
          clearInterval(pollTimer)
          pollTimer = null
          running.value = false
          progressPct.value = 100
          progressText.value = 'Comparison complete!'
          showToast('Comparison completed successfully', 'success')
          fetchHistory()
        }
      } catch (pollErr) {
        console.error('Poll error:', pollErr)
      }
    }, 5000)
  } catch (e) {
    console.error('Comparison failed:', e)
    showToast(e.message || 'Comparison failed', 'error')
    running.value = false
  }
}

// Load a past comparison
async function loadComparison(id) {
  try {
    const data = await getComparison(id)
    result.value = data
  } catch (e) {
    console.error('Failed to load comparison:', e)
    showToast('Failed to load comparison', 'error')
  }
}

onMounted(() => {
  fetchModels()
  fetchHistory()
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>
