<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950 text-white' : 'bg-white text-slate-900'">
    <AppNav currentPage="home" />

    <!-- S1: Hero -->
    <section class="relative overflow-hidden py-20 sm:py-28 px-4">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute rounded-full blur-[120px] opacity-20" style="width:700px;height:700px;top:-200px;right:-100px;background:radial-gradient(circle,#4f46e5,transparent)"></div>
        <div class="absolute rounded-full blur-[120px] opacity-15" style="width:500px;height:500px;bottom:-100px;left:-100px;background:radial-gradient(circle,#10b981,transparent)"></div>
      </div>
      <div class="max-w-6xl mx-auto relative z-10 flex flex-col lg:flex-row items-center gap-12">
        <div class="flex-1 text-center lg:text-left">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold mb-6"
            :class="isDark ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-indigo-50 text-indigo-700 border border-indigo-200'">
            Multi-Agent Clinical AI
          </div>
          <h1 class="text-display mb-6">
            Your AI Medical
            <span class="bg-gradient-to-r from-indigo-400 via-emerald-400 to-teal-400 bg-clip-text text-transparent"> Intelligence </span>
            Platform
          </h1>
          <p class="text-body-lg max-w-xl mb-8" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            7 specialized agents collaborate on every diagnosis — from triage to treatment, with safety checks and evidence-based reasoning.
          </p>
          <div class="flex flex-wrap gap-4 justify-center lg:justify-start mb-10">
            <router-link to="/consult"
              class="btn-primary px-8 py-3.5 bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:shadow-xl hover:shadow-emerald-500/25">
              Start Free Consultation
            </router-link>
            <a href="#pillars"
              class="btn-secondary px-8 py-3.5"
              :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800' : 'border-slate-300 text-slate-700 hover:bg-slate-50'">
              Explore Features
            </a>
          </div>
          <div class="flex flex-wrap gap-3 justify-center lg:justify-start">
            <span v-for="badge in trustBadges" :key="badge.label"
              class="trust-badge"
              :class="isDark ? 'bg-slate-800/60 text-slate-400 border-slate-700/50' : 'bg-slate-50 text-slate-600 border-slate-200'">
              <span>{{ badge.icon }}</span> {{ badge.label }}
            </span>
          </div>
        </div>
        <div class="flex-shrink-0 hidden lg:flex items-center justify-center">
          <div class="w-72 h-72 rounded-3xl flex items-center justify-center text-8xl"
            :class="isDark ? 'bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700/50' : 'bg-gradient-to-br from-slate-50 to-slate-100 border border-slate-200'">
            &#x1F430;
          </div>
        </div>
      </div>
    </section>

    <!-- S2: Platform Pillars -->
    <section id="pillars" class="section-module px-4" :class="isDark ? 'bg-slate-900/50' : 'bg-slate-50'">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-headline text-center mb-3">Platform Pillars</h2>
        <p class="text-center text-body-lg mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Six specialized domains — each powered by dedicated AI agents.
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <router-link v-for="p in pillars" :key="p.title" :to="p.link"
            class="group rounded-2xl border p-6 transition-all duration-200 hover:-translate-y-1 hover:shadow-xl"
            :class="isDark
              ? 'bg-slate-800/60 border-slate-700/50 hover:shadow-black/20'
              : 'bg-white border-slate-200 hover:shadow-slate-200'">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-4 transition-colors"
              :style="{ background: isDark ? p.darkBg : p.lightBg }">
              {{ p.icon }}
            </div>
            <div class="text-title mb-1.5" :class="isDark ? 'text-white' : 'text-slate-900'">{{ p.title }}</div>
            <div class="text-body" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ p.desc }}</div>
            <div class="mt-3 h-0.5 w-0 group-hover:w-full transition-all duration-300 rounded" :style="{ background: p.color }"></div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- S3: How It Works -->
    <section class="section-module px-4">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-headline text-center mb-3">How It Works</h2>
        <p class="text-center text-body-lg mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Seven agents process every consultation through a clinical-grade pipeline.
        </p>
        <div class="flex flex-wrap justify-center gap-3">
          <div v-for="(agent, i) in pipelineAgents" :key="agent.name" class="flex items-center gap-3">
            <div class="rounded-xl border px-5 py-3 text-center transition-all"
              :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
              <div class="text-xl mb-1">{{ agent.icon }}</div>
              <div class="text-meta" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ agent.name }}</div>
            </div>
            <span v-if="i < pipelineAgents.length - 1" class="text-slate-400 text-lg hidden sm:inline">&rarr;</span>
          </div>
        </div>
      </div>
    </section>

    <!-- S4: Try It -->
    <section class="section-module px-4" :class="isDark ? 'bg-slate-900/50' : 'bg-slate-50'">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-headline text-center mb-3">See It In Action</h2>
        <p class="text-center text-body-lg mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Watch our 7-agent pipeline analyze symptoms in real-time.
        </p>
        <div class="rounded-2xl border overflow-hidden"
          :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-lg'">
          <div class="p-6 border-b" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <label class="text-label mb-2 block" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Try a sample symptom</label>
            <div class="flex gap-3">
              <input v-model="demoInput" type="text" placeholder="e.g. persistent headache with blurry vision"
                class="flex-1 rounded-xl border px-4 py-3 text-sm transition-colors outline-none focus:ring-2 focus:ring-emerald-500/30"
                :class="isDark ? 'bg-slate-900 border-slate-700 text-white placeholder-slate-600' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'"
                @keydown.enter="runDemo" />
              <button @click="runDemo"
                class="btn-primary px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-600 text-white"
                :disabled="demoRunning">
                {{ demoRunning ? 'Analyzing...' : 'Analyze' }}
              </button>
            </div>
          </div>
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
            <Transition enter-active-class="transition duration-500" enter-from-class="opacity-0 translate-y-4" enter-to-class="opacity-100 translate-y-0">
              <div v-if="demoComplete" class="rounded-xl p-5 space-y-3"
                :class="isDark ? 'bg-slate-900/80 border border-slate-700/50' : 'bg-slate-50 border border-slate-200'">
                <div class="text-label" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">AI Assessment</div>
                <div class="text-body" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  Based on your symptoms, the pipeline identified <strong>3 possible conditions</strong> ranked by probability.
                  The diagnostician flagged potential neurological involvement, while the safety agent verified no dangerous red flags requiring emergency care.
                </div>
                <div class="flex flex-wrap gap-2 pt-2">
                  <span v-for="tag in demoTags" :key="tag"
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

    <!-- S5: Trust & Privacy -->
    <section class="section-module px-4">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-headline text-center mb-3">Built for Medical Trust</h2>
        <p class="text-center text-body-lg mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Privacy-first architecture designed around clinical compliance standards.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div v-for="t in trustCards" :key="t.title"
            class="rounded-2xl border p-6 transition-all"
            :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200'">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl mb-4"
              :style="{ background: isDark ? 'rgba(13,148,136,0.15)' : 'rgba(13,148,136,0.08)' }">
              {{ t.icon }}
            </div>
            <div class="text-title mb-1.5" :class="isDark ? 'text-white' : 'text-slate-900'">{{ t.title }}</div>
            <div class="text-body" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t.desc }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- S6: Pricing Preview -->
    <section class="section-module px-4" :class="isDark ? 'bg-slate-900/50' : 'bg-slate-50'">
      <div class="max-w-5xl mx-auto">
        <h2 class="text-headline text-center mb-3">Simple Pricing</h2>
        <p class="text-center text-body-lg mb-12 max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Start free. Upgrade when you need more.
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div v-for="plan in plans" :key="plan.name"
            class="rounded-2xl border p-6 transition-all relative"
            :class="[
              isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200',
              plan.featured ? (isDark ? 'ring-2 ring-emerald-500/40' : 'ring-2 ring-emerald-400/50') : ''
            ]">
            <span v-if="plan.featured"
              class="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase px-3 py-0.5 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 text-white">
              Popular
            </span>
            <div class="text-label mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ plan.name }}</div>
            <div class="text-headline mb-1" :class="isDark ? 'text-white' : 'text-slate-900'">{{ plan.price }}</div>
            <div class="text-meta mb-4" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ plan.period }}</div>
            <ul class="space-y-2 mb-6">
              <li v-for="f in plan.features" :key="f" class="flex items-start gap-2 text-body"
                :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                <span class="text-emerald-500 mt-0.5">&#10003;</span> {{ f }}
              </li>
            </ul>
            <router-link :to="plan.cta.link"
              class="block text-center rounded-xl py-2.5 text-sm font-semibold transition-all"
              :class="plan.featured
                ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:shadow-lg hover:shadow-emerald-500/25'
                : (isDark ? 'border border-slate-700 text-slate-300 hover:bg-slate-700' : 'border border-slate-300 text-slate-700 hover:bg-slate-50')">
              {{ plan.cta.label }}
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- S7: CTA Banner -->
    <section class="py-24 px-4 text-center relative overflow-hidden">
      <div class="absolute inset-0 pointer-events-none">
        <div class="absolute rounded-full blur-[150px] opacity-20" style="width:600px;height:600px;top:50%;left:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,#10b981,transparent)"></div>
      </div>
      <div class="relative z-10 max-w-2xl mx-auto">
        <h2 class="text-headline sm:text-display mb-4">Ready to Get Started?</h2>
        <p class="text-body-lg mb-8" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Join thousands of users getting AI-powered health insights from our 7-agent clinical pipeline.
        </p>
        <router-link to="/consult"
          class="btn-primary px-10 py-4 text-base bg-gradient-to-r from-emerald-500 to-teal-600 text-white hover:shadow-xl hover:shadow-emerald-500/25">
          Start Your Free Consultation
        </router-link>
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
import { ref, inject } from 'vue'
import AppNav from '@/components/AppNav.vue'

const isDark = inject('isDark', ref(false))

/* ── Hero trust badges ── */
const trustBadges = [
  { icon: '\uD83D\uDEE1\uFE0F', label: 'HIPAA-Aware Design' },
  { icon: '\uD83D\uDD12', label: 'AES-256 Encrypted' },
  { icon: '\uD83E\uDD16', label: '7 AI Agents' },
  { icon: '\uD83C\uDF0D', label: '12 Languages' },
]

/* ── Platform Pillars ── */
const pillars = [
  { icon: '\uD83D\uDD2C', title: 'AI Diagnosis', desc: '7-agent pipeline with Bayesian clinical reasoning, triage, and safety checks.', link: '/consult', color: '#4f46e5', lightBg: 'rgba(79,70,229,0.08)', darkBg: 'rgba(79,70,229,0.15)' },
  { icon: '\uD83E\uDD57', title: 'Nutrition', desc: 'AI meal plans, restaurant guide, and smart shopping advisor.', link: '/nutrition', color: '#059669', lightBg: 'rgba(5,150,105,0.08)', darkBg: 'rgba(5,150,105,0.15)' },
  { icon: '\uD83E\uDDE0', title: 'Mental Health', desc: 'PHQ-9, GAD-7 screening, mood tracking, and guided insights.', link: '/mental-health', color: '#7c3aed', lightBg: 'rgba(124,58,237,0.08)', darkBg: 'rgba(124,58,237,0.15)' },
  { icon: '\uD83D\uDC8A', title: 'Medications', desc: 'Drug interactions, dosage schedule, and pill identifier.', link: '/medications', color: '#9333ea', lightBg: 'rgba(147,51,234,0.08)', darkBg: 'rgba(147,51,234,0.15)' },
  { icon: '\uD83D\uDCCB', title: 'Reports', desc: 'Clinical reports, health history, and comparison analytics.', link: '/reports', color: '#0284c7', lightBg: 'rgba(2,132,199,0.08)', darkBg: 'rgba(2,132,199,0.15)' },
  { icon: '\uD83D\uDD0D', title: 'Second Opinion', desc: 'Multi-model consensus analysis for added diagnostic confidence.', link: '/second-opinion', color: '#0d9488', lightBg: 'rgba(13,148,136,0.08)', darkBg: 'rgba(13,148,136,0.15)' },
]

/* ── Pipeline agents ── */
const pipelineAgents = [
  { name: 'Triage', icon: '\uD83D\uDEA8' },
  { name: 'Diagnostician', icon: '\uD83E\uDE7A' },
  { name: 'Research', icon: '\uD83D\uDCDA' },
  { name: 'Specialist', icon: '\uD83D\uDC68\u200D\u2695\uFE0F' },
  { name: 'Treatment', icon: '\uD83D\uDC89' },
  { name: 'Safety', icon: '\uD83D\uDEE1\uFE0F' },
  { name: 'Empathy', icon: '\uD83D\uDC9A' },
]

/* ── Demo state ── */
const demoInput = ref('persistent headache with blurry vision')
const demoStarted = ref(false)
const demoRunning = ref(false)
const demoComplete = ref(false)
const currentAgentIndex = ref(-1)
const demoTags = ['Tension Headache (72%)', 'Migraine with Aura (18%)', 'Hypertension (10%)']

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

/* ── Trust & Privacy cards ── */
const trustCards = [
  { icon: '\uD83D\uDEE1\uFE0F', title: 'HIPAA-Aware Design', desc: 'Architecture follows HIPAA guidelines with audit logging, access controls, and data minimization.' },
  { icon: '\uD83D\uDCF1', title: 'Local-First Data', desc: 'API keys and health data stay on your device. No server-side storage of personal information.' },
  { icon: '\u2705', title: 'Safety Review Pipeline', desc: 'Every diagnosis passes through a dedicated Safety Agent that checks for dangerous conditions and contraindications.' },
]

/* ── Pricing ── */
const plans = [
  { name: 'Free', price: '$0', period: 'forever', featured: false, features: ['3 consultations/day', 'Basic diagnosis', '7-agent pipeline'], cta: { label: 'Get Started', link: '/consult' } },
  { name: 'Plus', price: '$9', period: '/month', featured: false, features: ['Unlimited consults', 'Nutrition planner', 'Symptom journal'], cta: { label: 'Upgrade', link: '/pricing' } },
  { name: 'Pro', price: '$19', period: '/month', featured: true, features: ['Everything in Plus', 'Second opinion', 'PDF reports', 'Priority pipeline'], cta: { label: 'Go Pro', link: '/pricing' } },
  { name: 'Family', price: '$29', period: '/month', featured: false, features: ['Up to 6 members', 'Shared dashboard', 'All Pro features'], cta: { label: 'Choose Family', link: '/pricing' } },
]
</script>
