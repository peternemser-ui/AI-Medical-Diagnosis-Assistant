<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950 text-white' : 'bg-white text-slate-900'">

    <!-- Nav -->
    <nav class="sticky top-0 z-50 backdrop-blur-xl border-b py-3 px-4 sm:px-6 flex justify-between items-center transition-colors"
      :style="{ background: 'var(--clinical-surface, ' + (isDark ? '#0f172a' : '#ffffff') + ')', borderColor: 'var(--clinical-border, ' + (isDark ? '#1e293b' : '#e2e8f0') + ')' }">
      <router-link to="/" class="flex items-center gap-2.5 group">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor"><path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" /></svg>
        </div>
        <span class="text-base font-semibold hidden sm:inline" :class="isDark ? 'text-white' : 'text-slate-900'">MedDiagnose AI</span>
      </router-link>
      <div class="flex items-center gap-3">
        <router-link to="/consult" class="text-sm font-medium px-4 py-2 rounded-lg bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:shadow-lg hover:shadow-emerald-500/25 transition-all">
          Start Consultation
        </router-link>
      </div>
    </nav>

    <!-- HERO -->
    <section class="relative overflow-hidden py-20 sm:py-28 px-4">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute rounded-full blur-[120px] opacity-20" style="width:700px;height:700px;top:-200px;right:-100px;background:radial-gradient(circle,#3b82f6,transparent)"></div>
        <div class="absolute rounded-full blur-[120px] opacity-15" style="width:500px;height:500px;bottom:-100px;left:-100px;background:radial-gradient(circle,#10b981,transparent)"></div>
      </div>
      <div class="max-w-4xl mx-auto text-center relative z-10">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold mb-6"
          :class="isDark ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'">
          AI-Powered Health Platform
        </div>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight mb-6">
          Your Complete
          <span class="bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent"> AI Health </span>
          Platform
        </h1>
        <p class="text-lg sm:text-xl max-w-2xl mx-auto mb-12" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Diagnosis, nutrition, mental health, medications, and more — powered by 7 specialized AI agents working together.
        </p>
        <!-- Animated counters -->
        <div class="flex flex-wrap justify-center gap-8 sm:gap-16">
          <div v-for="stat in heroStats" :key="stat.label" class="text-center">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent">
              {{ stat.value }}
            </div>
            <div class="text-sm mt-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURE GRID -->
    <section class="py-16 px-4" :class="isDark ? 'bg-slate-900/50' : 'bg-slate-50'">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-3xl font-bold text-center mb-4">Everything You Need</h2>
        <p class="text-center mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          A comprehensive platform covering every aspect of your health journey.
        </p>

        <div v-for="(row, ri) in featureRows" :key="ri" class="mb-12 last:mb-0">
          <h3 class="text-xs font-bold uppercase tracking-widest mb-5 px-1"
            :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ row.label }}</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <router-link v-for="f in row.features" :key="f.title" :to="f.link"
              class="group relative rounded-2xl border p-5 transition-all duration-200 hover:-translate-y-1 hover:shadow-xl"
              :class="isDark
                ? 'bg-slate-800/60 border-slate-700/50 hover:border-emerald-500/30 hover:shadow-emerald-500/5'
                : 'bg-white border-slate-200 hover:border-emerald-300 hover:shadow-emerald-100'">
              <span v-if="f.isNew"
                class="absolute top-3 right-3 text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 text-white shadow-sm">
                NEW
              </span>
              <div class="text-3xl mb-3">{{ f.icon }}</div>
              <div class="font-semibold text-sm mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">{{ f.title }}</div>
              <div class="text-xs leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ f.desc }}</div>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- INTERACTIVE DEMO -->
    <section class="py-20 px-4">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-3xl font-bold text-center mb-4">See It In Action</h2>
        <p class="text-center mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Watch how our 7-agent pipeline analyzes symptoms in real-time.
        </p>

        <div class="rounded-2xl border overflow-hidden"
          :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-lg'">
          <!-- Input area -->
          <div class="p-6 border-b" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <label class="block text-xs font-semibold uppercase tracking-wider mb-2"
              :class="isDark ? 'text-slate-500' : 'text-slate-400'">Try a sample symptom</label>
            <div class="flex gap-3">
              <input v-model="demoInput" type="text" placeholder="e.g. persistent headache with blurry vision"
                class="flex-1 rounded-xl border px-4 py-3 text-sm transition-colors outline-none focus:ring-2 focus:ring-emerald-500/30"
                :class="isDark ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-600' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'"
                @keydown.enter="runDemo" />
              <button @click="runDemo"
                class="px-6 py-3 rounded-xl text-sm font-semibold bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:shadow-lg hover:shadow-emerald-500/25 transition-all"
                :disabled="demoRunning">
                {{ demoRunning ? 'Analyzing...' : 'Analyze' }}
              </button>
            </div>
          </div>

          <!-- Pipeline visualization -->
          <div v-if="demoStarted" class="p-6">
            <div class="flex flex-wrap gap-3 mb-6">
              <div v-for="(agent, i) in pipelineAgents" :key="agent.name"
                class="flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-500"
                :class="agentClass(i)">
                <div class="w-2 h-2 rounded-full transition-colors duration-500"
                  :class="i < currentAgentIndex ? 'bg-emerald-400' : i === currentAgentIndex ? 'bg-blue-400 animate-pulse' : (isDark ? 'bg-slate-600' : 'bg-slate-300')"></div>
                {{ agent.name }}
              </div>
            </div>

            <!-- Demo result -->
            <Transition enter-active-class="transition duration-500" enter-from-class="opacity-0 translate-y-4" enter-to-class="opacity-100 translate-y-0">
              <div v-if="demoComplete" class="rounded-xl p-5 space-y-3"
                :class="isDark ? 'bg-slate-900/80 border border-slate-700/50' : 'bg-slate-50 border border-slate-200'">
                <div class="text-xs font-bold uppercase tracking-wider" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">AI Assessment</div>
                <div class="text-sm leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  Based on your symptoms, the pipeline identified <strong>3 possible conditions</strong> ranked by probability. The diagnostician flagged potential neurological involvement, while the safety agent verified no dangerous red flags requiring emergency care.
                </div>
                <div class="flex flex-wrap gap-2 pt-2">
                  <span v-for="tag in ['Tension Headache (72%)', 'Migraine with Aura (18%)', 'Hypertension (10%)']" :key="tag"
                    class="text-xs px-3 py-1 rounded-full font-medium"
                    :class="isDark ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 'bg-blue-50 text-blue-700 border border-blue-200'">
                    {{ tag }}
                  </span>
                </div>
                <div class="pt-3">
                  <router-link to="/consult" class="text-xs font-semibold text-emerald-500 hover:text-emerald-400 transition-colors">
                    Try it with your own symptoms &rarr;
                  </router-link>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </section>

    <!-- COMPARISON TABLE -->
    <section class="py-20 px-4" :class="isDark ? 'bg-slate-900/50' : 'bg-slate-50'">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-3xl font-bold text-center mb-4">How We Compare</h2>
        <p class="text-center mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          See why MedDiagnose AI leads the market in features and capability.
        </p>

        <div class="overflow-x-auto rounded-2xl border"
          :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
          <table class="w-full text-sm">
            <thead>
              <tr :class="isDark ? 'bg-slate-800/80' : 'bg-slate-100'">
                <th class="text-left px-5 py-4 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Feature</th>
                <th v-for="comp in competitors" :key="comp" class="px-5 py-4 font-semibold text-center"
                  :class="comp === 'MedDiagnose AI'
                    ? (isDark ? 'text-emerald-400 bg-emerald-500/5' : 'text-emerald-700 bg-emerald-50')
                    : (isDark ? 'text-slate-400' : 'text-slate-500')">
                  {{ comp }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in comparisonData" :key="row.feature"
                class="border-t transition-colors"
                :class="isDark ? 'border-slate-700/30 hover:bg-slate-800/40' : 'border-slate-100 hover:bg-slate-50'">
                <td class="px-5 py-3.5 font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ row.feature }}</td>
                <td v-for="comp in competitors" :key="comp" class="px-5 py-3.5 text-center"
                  :class="comp === 'MedDiagnose AI' ? (isDark ? 'bg-emerald-500/5' : 'bg-emerald-50/50') : ''">
                  <span v-if="row[comp]" class="text-emerald-500 text-base">&#10003;</span>
                  <span v-else class="text-base" :class="isDark ? 'text-slate-700' : 'text-slate-300'">&#8212;</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-24 px-4 text-center relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute rounded-full blur-[150px] opacity-20" style="width:600px;height:600px;top:50%;left:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,#10b981,transparent)"></div>
      </div>
      <div class="relative z-10 max-w-2xl mx-auto">
        <h2 class="text-3xl sm:text-4xl font-bold mb-4">Ready to Experience Smarter Healthcare?</h2>
        <p class="mb-8" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Join thousands of users getting AI-powered health insights from our 7-agent clinical pipeline.
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <router-link to="/consult"
            class="px-8 py-3.5 rounded-xl text-sm font-semibold bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:shadow-xl hover:shadow-emerald-500/25 transition-all">
            Start Your Free Consultation
          </router-link>
          <router-link to="/pricing"
            class="px-8 py-3.5 rounded-xl text-sm font-semibold border transition-all"
            :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-300 text-slate-700 hover:bg-slate-50'">
            View Pricing
          </router-link>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t py-8 px-4 text-center text-xs"
      :class="isDark ? 'border-slate-800 text-slate-600' : 'border-slate-200 text-slate-400'">
      &copy; {{ new Date().getFullYear() }} MedDiagnose AI. For informational purposes only — not a substitute for professional medical advice.
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, inject, onMounted } from 'vue'

const isDark = inject('isDark', ref(false))

const heroStats = [
  { value: '75+', label: 'Features' },
  { value: '7', label: 'AI Agents' },
  { value: '12', label: 'Languages' },
]

const featureRows = [
  {
    label: 'Core',
    features: [
      { icon: '\uD83C\uDFE5', title: 'AI Diagnosis', desc: '7-agent clinical pipeline with Bayesian reasoning, triage, and safety checks.', link: '/consult', isNew: false },
      { icon: '\uD83D\uDCF8', title: 'Photo Analysis', desc: 'Upload skin photos, annotate areas of concern, get AI visual assessment.', link: '/consult', isNew: true },
      { icon: '\uD83D\uDDE3\uFE0F', title: 'Voice Consultation', desc: 'Speak naturally with Dr. Hopps — real-time speech-to-text diagnosis.', link: '/consult', isNew: false },
      { icon: '\uD83C\uDF10', title: '12 Languages', desc: 'Full multilingual support for global accessibility and inclusivity.', link: '/consult', isNew: false },
    ]
  },
  {
    label: 'Health Tracking',
    features: [
      { icon: '\uD83E\uDD57', title: 'Nutrition Planner', desc: 'AI-generated meal plans tailored to your medical conditions.', link: '/nutrition', isNew: true },
      { icon: '\uD83E\uDDE0', title: 'Mental Health', desc: 'PHQ-9, GAD-7 screening tools with mood tracking and insights.', link: '/mental-health', isNew: true },
      { icon: '\uD83D\uDCD3', title: 'Symptom Journal', desc: 'Daily symptom logging with AI-powered pattern detection.', link: '/journal', isNew: true },
      { icon: '\uD83D\uDC8A', title: 'Medication Manager', desc: 'Drug interactions, dosage schedule, refill reminders.', link: '/medications', isNew: false },
    ]
  },
  {
    label: 'Clinical Tools',
    features: [
      { icon: '\uD83D\uDD2C', title: 'Second Opinion', desc: 'Multi-model consensus analysis for added diagnostic confidence.', link: '/second-opinion', isNew: true },
      { icon: '\uD83D\uDC68\u200D\u2695\uFE0F', title: 'Find Specialists', desc: 'Search the NPI registry to find doctors near you.', link: '/consult', isNew: false },
      { icon: '\uD83D\uDCCB', title: 'Clinical Reports', desc: 'Downloadable PDF reports with full medical disclaimers.', link: '/reports', isNew: false },
      { icon: '\uD83C\uDFE5', title: 'Body Systems', desc: 'Interactive body diagram for precise diagnostic mapping.', link: '/consult', isNew: false },
    ]
  },
  {
    label: 'Platform',
    features: [
      { icon: '\uD83D\uDD12', title: 'HIPAA Security', desc: 'AES-256 encryption with field-level data protection.', link: '/features', isNew: false },
      { icon: '\uD83D\uDCF1', title: 'Mobile Ready', desc: 'Progressive Web App + Capacitor for iOS and Android.', link: '/features', isNew: false },
      { icon: '\uD83E\uDD16', title: 'Self-Learning', desc: 'Quality Auditor continuously improves diagnostic accuracy.', link: '/features', isNew: false },
      { icon: '\uD83D\uDCB0', title: '5 Revenue Streams', desc: 'Subscriptions, API access, referrals, and more.', link: '/pricing', isNew: false },
    ]
  }
]

// Demo section
const demoInput = ref('persistent headache with blurry vision')
const demoStarted = ref(false)
const demoRunning = ref(false)
const demoComplete = ref(false)
const currentAgentIndex = ref(-1)

const pipelineAgents = [
  { name: 'Triage' },
  { name: 'Diagnostician' },
  { name: 'Research' },
  { name: 'Specialist' },
  { name: 'Treatment' },
  { name: 'Safety' },
  { name: 'Empathy' },
]

function agentClass(i) {
  if (i < currentAgentIndex.value) {
    return isDark.value
      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
      : 'bg-emerald-50 text-emerald-700 border-emerald-200'
  }
  if (i === currentAgentIndex.value) {
    return isDark.value
      ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
      : 'bg-blue-50 text-blue-700 border-blue-200'
  }
  return isDark.value
    ? 'bg-slate-800/60 text-slate-500 border-slate-700/50'
    : 'bg-slate-100 text-slate-400 border-slate-200'
}

async function runDemo() {
  if (demoRunning.value) return
  demoStarted.value = true
  demoRunning.value = true
  demoComplete.value = false
  currentAgentIndex.value = 0

  for (let i = 0; i < pipelineAgents.length; i++) {
    currentAgentIndex.value = i
    await new Promise(r => setTimeout(r, 400 + Math.random() * 300))
  }
  currentAgentIndex.value = pipelineAgents.length
  demoComplete.value = true
  demoRunning.value = false
}

// Comparison table
const competitors = ['MedDiagnose AI', 'Ada Health', 'Babylon', 'K Health']

const comparisonData = [
  { feature: 'Multi-Agent Pipeline', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': false, 'K Health': false },
  { feature: 'Voice Consultation', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': true, 'K Health': false },
  { feature: 'Photo / Image Analysis', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': false, 'K Health': false },
  { feature: 'Medication Manager', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': false, 'K Health': true },
  { feature: 'Mental Health Screening', 'MedDiagnose AI': true, 'Ada Health': true, 'Babylon': true, 'K Health': true },
  { feature: 'Nutrition Planning', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': false, 'K Health': false },
  { feature: 'PDF Clinical Reports', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': true, 'K Health': false },
  { feature: '12+ Languages', 'MedDiagnose AI': true, 'Ada Health': true, 'Babylon': false, 'K Health': false },
  { feature: 'HIPAA Compliant', 'MedDiagnose AI': true, 'Ada Health': true, 'Babylon': true, 'K Health': true },
  { feature: 'Second Opinion (Multi-Model)', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': false, 'K Health': false },
  { feature: 'Symptom Journal', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': false, 'K Health': false },
  { feature: 'Self-Improving AI', 'MedDiagnose AI': true, 'Ada Health': false, 'Babylon': false, 'K Health': false },
]
</script>
