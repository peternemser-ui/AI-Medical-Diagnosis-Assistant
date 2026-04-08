<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950 text-white' : 'bg-slate-50 text-slate-900'">
    <!-- Skip to main content (WCAG 2.1 AA) -->
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[9999] focus:px-4 focus:py-2 focus:rounded-lg focus:font-semibold focus:text-white focus:bg-indigo-600">
      Skip to main content
    </a>

    <AppNav currentPage="home" />

    <main id="main-content">

    <!-- ─── S1: Hero ─────────────────────────────────────────── -->
    <section class="relative overflow-hidden py-20 sm:py-28 px-4" :class="isDark ? 'bg-slate-950' : 'bg-white'">
      <!-- Subtle background grid -->
      <div class="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div class="absolute inset-0 opacity-[0.025]"
          :style="isDark
            ? 'background-image: linear-gradient(rgba(99,102,241,0.4) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.4) 1px,transparent 1px); background-size: 64px 64px;'
            : 'background-image: linear-gradient(rgba(99,102,241,0.15) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.15) 1px,transparent 1px); background-size: 64px 64px;'">
        </div>
        <!-- Single, subtle tinted gradient — no heavy blobs -->
        <div class="absolute top-0 right-0 w-[600px] h-[600px] opacity-[0.06] rounded-full"
          style="background: radial-gradient(circle at center, #4f46e5, transparent 70%); transform: translate(25%,-25%);"></div>
      </div>

      <div class="max-w-6xl mx-auto relative z-10 flex flex-col lg:flex-row items-center gap-14">
        <!-- Left: Copy -->
        <div class="flex-1 text-center lg:text-left">
          <!-- Dr. Hopps badge — small, supporting role -->
          <div class="inline-flex items-center gap-2.5 mb-6">
            <span class="inline-flex items-center justify-center w-8 h-8 rounded-full bg-indigo-600 text-white text-xs font-bold shadow-md shadow-indigo-500/30 flex-shrink-0">H</span>
            <span class="text-xs font-semibold px-3 py-1 rounded-full"
              :class="isDark ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-indigo-50 text-indigo-700 border border-indigo-200'">
              Multi-Agent Clinical AI · Powered by Claude
            </span>
          </div>

          <h1 class="text-display mb-5" style="font-size: clamp(2.25rem, 5vw, 3.5rem); line-height: 1.08; font-weight: 800; letter-spacing: -0.03em;">
            AI-Powered Medical<br class="hidden sm:inline" />
            <span class="bg-gradient-to-r from-indigo-500 via-indigo-400 to-sky-400 bg-clip-text text-transparent"> Diagnosis </span>
            in Minutes
          </h1>

          <p class="text-body-lg max-w-lg mb-8 mx-auto lg:mx-0" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            Seven specialized AI agents collaborate on every consultation — triage, diagnosis, research, and safety checks — delivering clinical-grade insights instantly.
          </p>

          <div class="flex flex-wrap gap-4 justify-center lg:justify-start mb-10">
            <router-link to="/consult"
              class="btn-primary px-8 py-3.5 text-base bg-indigo-700 hover:bg-indigo-600 text-white shadow-lg shadow-indigo-700/30">
              Start Free Consultation
            </router-link>
            <a href="#how-it-works"
              class="btn-secondary px-8 py-3.5 text-base"
              :class="isDark ? 'border-slate-700 text-slate-300 hover:bg-slate-800/60' : 'border-slate-300 text-slate-700 hover:bg-slate-50'">
              See How It Works
            </a>
          </div>

          <!-- Trust badges -->
          <div class="flex flex-wrap gap-3 justify-center lg:justify-start">
            <span v-for="badge in trustBadges" :key="badge.label"
              class="trust-badge"
              :class="isDark ? 'bg-slate-800/60 text-slate-400 border-slate-700/50' : 'bg-slate-50 text-slate-600 border-slate-200'">
              <span>{{ badge.icon }}</span> {{ badge.label }}
            </span>
          </div>
        </div>

        <!-- Right: Consultation mockup -->
        <div class="flex-shrink-0 w-full max-w-sm lg:max-w-md">
          <div class="rounded-2xl border overflow-hidden shadow-2xl"
            :class="isDark ? 'bg-slate-900 border-slate-800 shadow-black/50' : 'bg-white border-slate-200 shadow-slate-200/80'">
            <!-- Mockup header bar -->
            <div class="px-4 py-3 border-b flex items-center gap-2"
              :class="isDark ? 'bg-slate-950 border-slate-800' : 'bg-slate-50 border-slate-200'">
              <div class="w-3 h-3 rounded-full bg-red-400/70"></div>
              <div class="w-3 h-3 rounded-full bg-amber-400/70"></div>
              <div class="w-3 h-3 rounded-full bg-emerald-400/70"></div>
              <div class="ml-2 text-xs font-medium" :class="isDark ? 'text-slate-500' : 'text-slate-400'">MedDiagnose AI · Consultation</div>
            </div>
            <!-- Mockup body -->
            <div class="p-5 space-y-4">
              <!-- User message -->
              <div class="flex justify-end">
                <div class="max-w-[80%] rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm bg-indigo-600 text-white shadow-md">
                  I have a persistent headache for 3 days with sensitivity to light.
                </div>
              </div>
              <!-- Agent pipeline chips -->
              <div class="flex flex-wrap gap-1.5">
                <span v-for="(a, i) in pipelineMockup" :key="a"
                  class="text-[10px] font-semibold px-2 py-0.5 rounded-full border transition-all"
                  :class="i < 4 ? (isDark ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-emerald-50 text-emerald-700 border-emerald-200')
                    : i === 4 ? (isDark ? 'bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse' : 'bg-blue-50 text-blue-700 border-blue-200 animate-pulse')
                    : (isDark ? 'bg-slate-800 text-slate-600 border-slate-700' : 'bg-slate-100 text-slate-400 border-slate-200')">
                  {{ a }}
                </span>
              </div>
              <!-- AI response card -->
              <div class="rounded-xl border p-3.5 space-y-2"
                :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-slate-50 border-slate-200'">
                <div class="text-[10px] font-bold uppercase tracking-widest" :class="isDark ? 'text-indigo-400' : 'text-indigo-600'">AI Assessment</div>
                <div class="text-xs leading-relaxed" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
                  Top differential: <strong>Migraine with photophobia</strong> (74%). Safety agent confirmed no red flags. Recommend rest, hydration, and OTC analgesics.
                </div>
                <div class="flex flex-wrap gap-1.5 pt-1">
                  <span class="text-[10px] px-2 py-0.5 rounded-full font-medium"
                    :class="isDark ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-indigo-50 text-indigo-700 border border-indigo-200'">
                    Migraine 74%
                  </span>
                  <span class="text-[10px] px-2 py-0.5 rounded-full font-medium"
                    :class="isDark ? 'bg-slate-700 text-slate-400 border border-slate-600' : 'bg-white text-slate-500 border border-slate-200'">
                    Tension HA 18%
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── S2: Stats bar ──────────────────────────────────────── -->
    <section class="py-8 px-4 border-y"
      :class="isDark ? 'bg-slate-900/60 border-slate-800' : 'bg-slate-50 border-slate-200'">
      <div class="max-w-5xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-6 text-center">
        <div v-for="stat in heroStats" :key="stat.label">
          <div class="text-2xl sm:text-3xl font-extrabold tracking-tight mb-1"
            :class="isDark ? 'text-white' : 'text-slate-900'">{{ stat.value }}</div>
          <div class="text-xs font-medium" :class="isDark ? 'text-slate-500' : 'text-slate-500'">{{ stat.label }}</div>
        </div>
      </div>
    </section>

    <!-- ─── S3: Platform Overview ──────────────────────────────── -->
    <section id="pillars" class="section-module px-4" :class="isDark ? 'bg-slate-950' : 'bg-white'">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-12">
          <div class="text-xs font-bold uppercase tracking-widest mb-3"
            :class="isDark ? 'text-indigo-400' : 'text-indigo-600'">Platform</div>
          <h2 class="text-headline mb-3">One Platform, Complete Health Intelligence</h2>
          <p class="text-body-lg max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            Six specialized domains — each powered by dedicated AI agents trained for clinical accuracy.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <router-link v-for="p in pillars" :key="p.title" :to="p.link"
            class="group rounded-2xl border p-6 transition-all duration-200 hover:-translate-y-1 hover:shadow-xl"
            :class="isDark
              ? 'bg-slate-900 border-slate-800 hover:shadow-black/30 hover:border-slate-700'
              : 'bg-white border-slate-200 hover:shadow-slate-100 hover:border-slate-300'">
            <div class="w-11 h-11 rounded-xl flex items-center justify-center mb-4 transition-colors"
              :style="{ background: isDark ? p.darkBg : p.lightBg }">
              <span class="text-xl">{{ p.icon }}</span>
            </div>
            <div class="text-title mb-1.5" :class="isDark ? 'text-white' : 'text-slate-900'">{{ p.title }}</div>
            <div class="text-body" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ p.desc }}</div>
            <div class="mt-4 h-0.5 w-0 group-hover:w-full transition-all duration-300 rounded" :style="{ background: p.color }"></div>
          </router-link>
        </div>
      </div>
    </section>

    <!-- ─── S4: How It Works ───────────────────────────────────── -->
    <section id="how-it-works" class="section-module px-4"
      :class="isDark ? 'bg-slate-900/50 border-t border-slate-800' : 'bg-slate-50 border-t border-slate-200'">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-12">
          <div class="text-xs font-bold uppercase tracking-widest mb-3"
            :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">Pipeline</div>
          <h2 class="text-headline mb-3">How It Works</h2>
          <p class="text-body-lg max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            Seven agents process every consultation through a clinical-grade pipeline — in parallel where possible.
          </p>
        </div>

        <!-- Pipeline flow — horizontal scroll on mobile -->
        <div class="relative">
          <!-- Connector line (desktop) -->
          <div class="hidden lg:block absolute top-[2.25rem] left-[calc(3.5rem)] right-[calc(3.5rem)] h-px"
            :class="isDark ? 'bg-slate-700' : 'bg-slate-200'" aria-hidden="true"></div>

          <div class="flex flex-wrap lg:flex-nowrap justify-center gap-3 lg:gap-0 lg:justify-between">
            <div v-for="(agent, i) in pipelineAgents" :key="agent.name"
              class="flex flex-col items-center gap-2 relative pipeline-step"
              :class="{ 'lg:flex-1': true }"
              :style="{ '--step-delay': `${i * 80}ms` }">
              <!-- Step dot + icon -->
              <div class="relative z-10 w-[4.5rem] h-[4.5rem] rounded-full border-2 flex flex-col items-center justify-center transition-all"
                :class="isDark
                  ? 'bg-slate-900 border-slate-700 hover:border-indigo-500'
                  : 'bg-white border-slate-200 shadow-sm hover:border-indigo-400 hover:shadow-indigo-100'">
                <span class="text-2xl leading-none">{{ agent.icon }}</span>
              </div>
              <!-- Label -->
              <div class="text-center">
                <div class="text-xs font-bold" :class="isDark ? 'text-white' : 'text-slate-800'">{{ agent.name }}</div>
                <div class="text-[10px] mt-0.5 max-w-[5rem] leading-tight" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ agent.role }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Live demo widget -->
        <div class="mt-12 rounded-2xl border overflow-hidden"
          :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200 shadow-lg'">
          <div class="p-5 border-b" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
            <label class="text-label mb-2 block" :class="isDark ? 'text-slate-500' : 'text-slate-400'">Try a sample symptom</label>
            <div class="flex gap-3">
              <input v-model="demoInput" type="text" placeholder="e.g. persistent headache with blurry vision"
                class="flex-1 rounded-xl border px-4 py-2.5 text-sm transition-colors outline-none focus:ring-2 focus:ring-indigo-500/30"
                :class="isDark ? 'bg-slate-800 border-slate-700 text-white placeholder-slate-600' : 'bg-slate-50 border-slate-200 text-slate-900 placeholder-slate-400'"
                @keydown.enter="runDemo" />
              <button @click="runDemo"
                class="btn-primary px-5 py-2.5 bg-indigo-700 hover:bg-indigo-600 text-white text-sm"
                :disabled="demoRunning">
                {{ demoRunning ? 'Analyzing...' : 'Analyze' }}
              </button>
            </div>
          </div>
          <div v-if="demoStarted" class="p-5">
            <div class="flex flex-wrap gap-2 mb-5">
              <div v-for="(agent, i) in pipelineAgents" :key="agent.name"
                class="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-500"
                :class="agentClass(i)">
                <div class="w-1.5 h-1.5 rounded-full transition-colors duration-500"
                  :class="i < currentAgentIndex ? 'bg-emerald-400' : i === currentAgentIndex ? 'bg-blue-400 animate-pulse' : (isDark ? 'bg-slate-600' : 'bg-slate-300')"></div>
                {{ agent.name }}
              </div>
            </div>
            <Transition enter-active-class="transition duration-500" enter-from-class="opacity-0 translate-y-4" enter-to-class="opacity-100 translate-y-0">
              <div v-if="demoComplete" class="rounded-xl p-4 space-y-3"
                :class="isDark ? 'bg-slate-800/60 border border-slate-700/50' : 'bg-slate-50 border border-slate-200'">
                <div class="text-label" :class="isDark ? 'text-indigo-400' : 'text-indigo-600'">AI Assessment</div>
                <div class="text-body" :class="isDark ? 'text-slate-300' : 'text-slate-700'">
                  Based on your symptoms, the pipeline identified <strong>3 possible conditions</strong> ranked by probability.
                  The diagnostician flagged potential neurological involvement, while the safety agent verified no dangerous red flags requiring emergency care.
                </div>
                <div class="flex flex-wrap gap-2 pt-1">
                  <span v-for="tag in demoTags" :key="tag"
                    class="text-xs px-3 py-1 rounded-full font-medium"
                    :class="isDark ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' : 'bg-indigo-50 text-indigo-700 border border-indigo-200'">
                    {{ tag }}
                  </span>
                </div>
                <div class="pt-2">
                  <router-link to="/consult" class="text-xs font-semibold text-indigo-500 hover:text-indigo-400 transition-colors">
                    Try it with your own symptoms &rarr;
                  </router-link>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── S5: Trust & Compliance ────────────────────────────── -->
    <section class="section-module px-4" :class="isDark ? 'bg-slate-950 border-t border-slate-800' : 'bg-white border-t border-slate-200'">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-12">
          <div class="text-xs font-bold uppercase tracking-widest mb-3"
            :class="isDark ? 'text-teal-400' : 'text-teal-600'">Compliance</div>
          <h2 class="text-headline mb-3">Built for Trust</h2>
          <p class="text-body-lg max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            Privacy-first architecture designed around clinical compliance standards.
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div v-for="t in trustCards" :key="t.title"
            class="rounded-2xl border p-6 transition-all hover:-translate-y-0.5"
            :class="isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'">
            <div class="w-11 h-11 rounded-xl flex items-center justify-center text-xl mb-4"
              :style="{ background: isDark ? 'rgba(13,148,136,0.12)' : 'rgba(13,148,136,0.08)' }">
              {{ t.icon }}
            </div>
            <div class="text-title mb-1.5" :class="isDark ? 'text-white' : 'text-slate-900'">{{ t.title }}</div>
            <div class="text-body" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t.desc }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── S6: Pricing ───────────────────────────────────────── -->
    <section class="section-module px-4" :class="isDark ? 'bg-slate-900/60 border-t border-slate-800' : 'bg-slate-50 border-t border-slate-200'">
      <div class="max-w-5xl mx-auto">
        <div class="text-center mb-12">
          <div class="text-xs font-bold uppercase tracking-widest mb-3"
            :class="isDark ? 'text-indigo-400' : 'text-indigo-600'">Pricing</div>
          <h2 class="text-headline mb-3">Simple, Transparent Pricing</h2>
          <p class="text-body-lg max-w-xl mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
            Start free. Upgrade when you need more.
          </p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          <div v-for="plan in plans" :key="plan.name"
            class="rounded-2xl border p-6 transition-all relative"
            :class="[
              isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200',
              plan.featured ? (isDark ? 'ring-2 ring-indigo-500/50 shadow-lg shadow-indigo-500/10' : 'ring-2 ring-indigo-400/40 shadow-lg shadow-indigo-100') : ''
            ]">
            <span v-if="plan.featured"
              class="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] font-bold uppercase px-3 py-0.5 rounded-full bg-indigo-700 text-white shadow">
              Popular
            </span>
            <div class="text-label mb-2" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ plan.name }}</div>
            <div class="text-headline mb-0.5" :class="isDark ? 'text-white' : 'text-slate-900'">{{ plan.price }}</div>
            <div class="text-meta mb-4" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ plan.period }}</div>
            <ul class="space-y-2 mb-6">
              <li v-for="f in plan.features" :key="f" class="flex items-start gap-2 text-body"
                :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                <span class="text-emerald-500 mt-0.5 flex-shrink-0">&#10003;</span> {{ f }}
              </li>
            </ul>
            <router-link :to="plan.cta.link"
              class="block text-center rounded-xl py-2.5 text-sm font-semibold transition-all"
              :class="plan.featured
                ? 'bg-indigo-700 hover:bg-indigo-600 text-white shadow-md shadow-indigo-700/30'
                : (isDark ? 'border border-slate-700 text-slate-300 hover:bg-slate-800' : 'border border-slate-300 text-slate-700 hover:bg-slate-50')">
              {{ plan.cta.label }}
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- ─── S7: CTA Close ─────────────────────────────────────── -->
    <section class="py-24 px-4 text-center"
      :class="isDark ? 'bg-slate-950 border-t border-slate-800' : 'bg-white border-t border-slate-200'">
      <div class="max-w-2xl mx-auto">
        <div class="w-14 h-14 mx-auto mb-6 rounded-2xl bg-indigo-700 flex items-center justify-center shadow-xl shadow-indigo-700/30">
          <svg class="w-7 h-7 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
          </svg>
        </div>
        <h2 class="text-headline sm:text-display mb-4">Ready to Get Started?</h2>
        <p class="text-body-lg mb-8" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          Join thousands of users getting AI-powered health insights from our 7-agent clinical pipeline.
        </p>
        <router-link to="/consult"
          class="btn-primary px-10 py-4 text-base bg-indigo-700 hover:bg-indigo-600 text-white shadow-xl shadow-indigo-700/25">
          Start Your Free Consultation
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t py-8 px-4 text-center text-xs"
      :class="isDark ? 'border-slate-800 text-slate-600' : 'border-slate-200 text-slate-400'">
      &copy; {{ new Date().getFullYear() }} MedDiagnose AI &mdash; For informational purposes only. Not a substitute for professional medical advice.
    </footer>

    </main>
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

/* ── Stats ── */
const heroStats = [
  { value: '7', label: 'AI Agents' },
  { value: '50+', label: 'Conditions Analyzed' },
  { value: '<3s', label: 'Real-time Analysis' },
  { value: '24/7', label: 'Always Available' },
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

/* ── Pipeline agents (with short role labels) ── */
const pipelineAgents = [
  { name: 'Triage', icon: '\uD83D\uDEA8', role: 'Urgency & red flags' },
  { name: 'Diagnostician', icon: '\uD83E\uDE7A', role: 'Differential dx' },
  { name: 'Research', icon: '\uD83D\uDCDA', role: 'Evidence base' },
  { name: 'Specialist', icon: '\uD83D\uDC68\u200D\u2695\uFE0F', role: 'Domain analysis' },
  { name: 'Treatment', icon: '\uD83D\uDC89', role: 'Care plan' },
  { name: 'Safety', icon: '\uD83D\uDEE1\uFE0F', role: 'Contraindications' },
  { name: 'Empathy', icon: '\uD83D\uDC9A', role: 'Plain language' },
]

/* ── Mockup pipeline chips for hero ── */
const pipelineMockup = ['Triage', 'Diagnostician', 'Research', 'Specialist', 'Treatment', 'Safety', 'Empathy']

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
  { icon: '\uD83D\uDEE1\uFE0F', title: 'HIPAA Compliance', desc: 'Architecture follows HIPAA guidelines with audit logging, access controls, and data minimization principles.' },
  { icon: '\uD83D\uDD12', title: 'Medical AI Safety', desc: 'Every diagnosis passes through a dedicated Safety Agent that checks for dangerous conditions and contraindications.' },
  { icon: '\u2705', title: 'Data Encryption', desc: 'API keys and health data stay on your device. AES-256 encryption. No server-side storage of personal information.' },
]

/* ── Pricing ── */
const plans = [
  { name: 'Free', price: '$0', period: 'forever', featured: false, features: ['3 consultations/day', 'Basic diagnosis', '7-agent pipeline'], cta: { label: 'Get Started', link: '/consult' } },
  { name: 'Plus', price: '$9', period: '/month', featured: false, features: ['Unlimited consults', 'Nutrition planner', 'Symptom journal'], cta: { label: 'Upgrade', link: '/pricing' } },
  { name: 'Pro', price: '$19', period: '/month', featured: true, features: ['Everything in Plus', 'Second opinion', 'PDF reports', 'Priority pipeline'], cta: { label: 'Go Pro', link: '/pricing' } },
  { name: 'Family', price: '$29', period: '/month', featured: false, features: ['Up to 6 members', 'Shared dashboard', 'All Pro features'], cta: { label: 'Choose Family', link: '/pricing' } },
]
</script>

<style scoped>
.pipeline-step {
  animation: stepFadeIn 0.4s ease both;
  animation-delay: var(--step-delay, 0ms);
}

@keyframes stepFadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
