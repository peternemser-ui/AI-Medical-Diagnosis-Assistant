<template>
  <div class="min-h-screen relative overflow-hidden transition-colors duration-300 surface-page">

    <!-- ═══════ BACKGROUND LAYER (z-0) ═══════ -->
    <canvas ref="bgCanvas" class="fixed inset-0 w-full h-full pointer-events-none" style="z-index:0"></canvas>

    <!-- Subtle grid overlay for texture -->
    <div class="fixed inset-0 pointer-events-none" style="z-index:1"
      :class="isDark ? 'opacity-[0.03]' : 'opacity-[0.04]'">
      <div class="w-full h-full" style="background-image: radial-gradient(circle, currentColor 0.5px, transparent 0.5px); background-size: 24px 24px;"></div>
    </div>

    <!-- Noise texture layer -->
    <div class="fixed inset-0 pointer-events-none mix-blend-overlay" style="z-index:1"
      :class="isDark ? 'opacity-[0.015]' : 'opacity-[0.02]'">
      <svg width="100%" height="100%"><filter id="noiseFilter"><feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#noiseFilter)"/></svg>
    </div>

    <!-- ═══════ NAVIGATION — sticky with backdrop blur ═══════ -->
    <nav class="sticky top-0 z-50 flex items-center justify-between px-6 sm:px-10 py-4 backdrop-blur-xl border-b transition-colors duration-300"
      style="background: color-mix(in srgb, var(--clinical-surface) 85%, transparent); border-color: var(--clinical-border)">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
          </svg>
        </div>
        <span class="text-base font-semibold tracking-tight" :class="isDark ? 'text-white' : 'text-slate-900'">{{ t('nav.brand') }}</span>
      </div>
      <div class="flex items-center gap-2">
        <router-link to="/reports" class="text-sm transition-colors px-3 py-1.5 hidden sm:inline" :class="isDark ? 'text-slate-400 hover:text-white' : 'text-slate-500 hover:text-slate-900'">
          {{ t('nav.reports') }}
        </router-link>
        <ThemeLangControls />
        <!-- Start Consultation CTA in nav — desktop only -->
        <button @click="startConsultation" class="hidden lg:inline-flex btn-blue btn-sm">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          {{ t('hero.startBtn') }}
        </button>
        <!-- User menu -->
        <div class="relative" ref="userMenuRef">
          <!-- Logged-in: avatar button -->
          <button v-if="isLoggedIn" @click="showUserMenu = !showUserMenu" class="flex items-center gap-1.5 px-2 py-1.5 rounded-lg transition-all" :class="isDark ? 'hover:bg-slate-800/60 text-slate-400 hover:text-white' : 'hover:bg-slate-200/60 text-slate-500 hover:text-slate-900'">
            <div class="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-detail font-bold text-white">
              {{ userInitials || '?' }}
            </div>
            <span class="hidden sm:inline text-sm font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ userName }}</span>
            <svg class="w-3 h-3 hidden sm:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <!-- Logged-out: Log In button -->
          <router-link v-else to="/profile" class="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700 shadow-md shadow-blue-500/20 hover:shadow-blue-500/30">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/></svg>
            Log In
          </router-link>
          <Transition enter-active-class="transition duration-150 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
            <div v-if="showUserMenu && isLoggedIn" class="absolute right-0 top-full mt-1 w-48 rounded-lg shadow-xl border z-50 overflow-hidden py-1" :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-slate-200'">
              <div class="px-3 py-2 border-b" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
                <div class="text-xs font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ userName }}</div>
                <div class="text-detail" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ userEmail || 'No email set' }}</div>
              </div>
              <router-link to="/profile" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                Profile
              </router-link>
              <router-link to="/settings" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                Settings
              </router-link>
              <router-link to="/reports" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                {{ t('nav.reports') }}
              </router-link>
              <router-link to="/setup" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
                API Keys
              </router-link>
              <!-- Divider + Log Out -->
              <div class="border-t my-1" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'"></div>
              <button @click="handleLogout" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors w-full text-left" :class="isDark ? 'text-red-400 hover:bg-slate-800' : 'text-red-500 hover:bg-red-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
                Log Out
              </button>
            </div>
          </Transition>
        </div>
      </div>
    </nav>

    <!-- ═══════ HERO — Two Column Layout ═══════ -->
    <div class="relative px-6 sm:px-10 pt-10 sm:pt-16 lg:pt-20 pb-12" style="z-index:20">
      <div class="max-w-6xl mx-auto flex flex-col lg:flex-row items-center gap-8 lg:gap-12">

        <!-- Left column: text + CTA -->
        <div class="lg:w-1/2 text-center lg:text-left">
          <!-- Eyebrow badge -->
          <div class="inline-flex items-center gap-2 rounded-full px-4 py-1.5 mb-6 border backdrop-blur-md"
            :class="isDark ? 'bg-blue-500/10 border-blue-500/20' : 'bg-white/60 border-blue-200'">
            <div class="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></div>
            <span class="text-xs font-medium" :class="isDark ? 'text-blue-300' : 'text-blue-600'">{{ t('hero.badge') }}</span>
          </div>

          <!-- Headline -->
          <h1 class="font-headline text-3xl sm:text-4xl lg:text-5xl font-bold mb-4" style="letter-spacing:0.05em; line-height:1.1">
            <span :class="isDark ? 'bg-gradient-to-r from-white via-white to-slate-400 bg-clip-text text-transparent' : 'text-slate-900'">{{ t('hero.title1') }}</span>
            <br />
            <span class="bg-gradient-to-r from-blue-500 to-purple-500 bg-clip-text text-transparent font-medium">{{ t('hero.title2') }}</span>
          </h1>

          <!-- Subtitle -->
          <p class="text-sm sm:text-base max-w-lg leading-relaxed mb-3" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
            {{ t('hero.subtitle') }}
          </p>

          <!-- Trust microcopy -->
          <div class="flex flex-wrap items-center gap-x-4 gap-y-1 mb-6 text-xs justify-center lg:justify-start" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
            <span class="flex items-center gap-1">
              <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              {{ t('hero.takes2min') }}
            </span>
            <span class="flex items-center gap-1">
              <svg class="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              {{ t('hero.noAccount') }}
            </span>
            <span class="flex items-center gap-1">
              <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
              {{ t('hero.sevenAgents') }}
            </span>
          </div>

          <!-- Symptom input box -->
          <div class="relative mt-2 max-w-lg mx-auto lg:mx-0">
            <input
              type="text"
              readonly
              @click="startConsultation"
              @keyup.enter="startConsultation"
              :placeholder="t('hero.inputPlaceholder')"
              class="input w-full py-4 pr-[7.5rem] cursor-pointer"
            />
            <button @click="startConsultation" class="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-600 hover:bg-blue-500 text-white px-3 py-2 rounded-lg text-xs sm:text-sm font-semibold flex items-center gap-1 sm:gap-1.5 transition-colors whitespace-nowrap">
              {{ t('hero.analyze') }}
              <svg class="w-3.5 h-3.5 sm:w-4 sm:h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </button>
          </div>

          <!-- CTA Buttons -->
          <div class="mt-6 flex flex-col sm:flex-row items-center lg:items-start gap-3">
            <button
              @click="startConsultation"
              class="group btn-blue btn-lg px-10 py-4 text-base shadow-lg shadow-blue-600/25 hover:shadow-xl hover:shadow-blue-500/30 hover:-translate-y-0.5"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
              {{ t('hero.startBtn') }}
              <svg class="w-4 h-4 transition-transform group-hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </button>
            <button
              @click="viewSampleReport"
              class="btn-secondary btn-lg px-6 py-4 backdrop-blur-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              {{ t('hero.reportBtn') }}
            </button>
          </div>
        </div>

        <!-- Right column: Dr. Hopps avatar -->
        <div class="lg:w-1/2 flex justify-center">
          <div class="relative">
            <!-- Avatar glow -->
            <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
              <div class="w-64 h-64 sm:w-80 sm:h-80 rounded-full blur-[80px] transition-colors duration-1000"
                :class="isDark ? 'opacity-25' : 'opacity-15'"
                style="background-color: #4a90d9"></div>
            </div>
            <div class="relative hero-avatar-float flex justify-center" ref="dogAvatarContainer">
              <!-- Medical equipment background -->
              <div class="absolute inset-0 flex items-center justify-center pointer-events-none" style="z-index: 0;">
                <svg viewBox="0 0 700 500" class="w-[140%] h-[110%] opacity-[0.12]" :class="isDark ? 'opacity-[0.08]' : 'opacity-[0.12]'" xmlns="http://www.w3.org/2000/svg">
                  <!-- ═══ LEFT SIDE: ECG Monitor ═══ -->
                  <g transform="translate(30, 80)">
                    <!-- Monitor stand -->
                    <rect x="55" y="200" width="10" height="80" rx="3" fill="#64748b"/>
                    <rect x="35" y="275" width="50" height="8" rx="4" fill="#64748b"/>
                    <!-- Monitor body -->
                    <rect x="5" y="20" width="110" height="180" rx="10" fill="#1e293b" stroke="#475569" stroke-width="2"/>
                    <!-- Screen -->
                    <rect x="12" y="28" width="96" height="120" rx="6" fill="#0f172a"/>
                    <!-- ECG waveform -->
                    <polyline fill="none" stroke="#22d3ee" stroke-width="1.8" stroke-linecap="round"
                      points="15,88 30,88 38,88 42,68 46,108 50,78 54,98 58,88 75,88 85,88 90,70 94,105 98,80 102,88">
                      <animate attributeName="stroke-dashoffset" values="200;0" dur="2s" repeatCount="indefinite"/>
                    </polyline>
                    <polyline fill="none" stroke="#34d399" stroke-width="1" stroke-linecap="round" opacity="0.6"
                      points="15,110 35,110 45,105 50,115 55,110 75,110 90,108 95,112 100,110">
                      <animate attributeName="stroke-dashoffset" values="150;0" dur="3s" repeatCount="indefinite"/>
                    </polyline>
                    <!-- Vital signs text -->
                    <text x="18" y="45" fill="#22d3ee" font-size="7" font-family="monospace" font-weight="bold">HR: 72</text>
                    <text x="70" y="45" fill="#34d399" font-size="7" font-family="monospace" font-weight="bold">SpO2: 98</text>
                    <text x="18" y="140" fill="#fbbf24" font-size="6" font-family="monospace">BP: 120/80</text>
                    <!-- Buttons -->
                    <circle cx="30" cy="165" r="5" fill="#334155" stroke="#475569" stroke-width="1"/>
                    <circle cx="50" cy="165" r="5" fill="#334155" stroke="#475569" stroke-width="1"/>
                    <circle cx="70" cy="165" r="5" fill="#22d3ee" opacity="0.4">
                      <animate attributeName="opacity" values="0.3;0.7;0.3" dur="2s" repeatCount="indefinite"/>
                    </circle>
                    <rect x="82" y="160" width="20" height="10" rx="3" fill="#334155" stroke="#475569" stroke-width="1"/>
                  </g>

                  <!-- ═══ LEFT: IV Drip Stand ═══ -->
                  <g transform="translate(155, 40)">
                    <!-- Pole -->
                    <rect x="18" y="30" width="4" height="300" rx="2" fill="#94a3b8"/>
                    <!-- Hook top -->
                    <rect x="5" y="20" width="30" height="4" rx="2" fill="#94a3b8"/>
                    <line x1="8" y1="24" x2="8" y2="40" stroke="#94a3b8" stroke-width="1.5"/>
                    <line x1="32" y1="24" x2="32" y2="40" stroke="#94a3b8" stroke-width="1.5"/>
                    <!-- IV bag -->
                    <path d="M0 45 Q0 38 8 38 L8 40 L32 40 L32 38 Q40 38 40 45 L38 100 Q38 108 20 108 Q2 108 2 100 Z" fill="#bfdbfe" stroke="#93c5fd" stroke-width="1" opacity="0.7"/>
                    <rect x="8" y="55" width="24" height="1" fill="#60a5fa" opacity="0.4"/>
                    <rect x="8" y="70" width="24" height="1" fill="#60a5fa" opacity="0.3"/>
                    <!-- Drip tube -->
                    <line x1="20" y1="108" x2="20" y2="200" stroke="#93c5fd" stroke-width="1" opacity="0.5"/>
                    <!-- Drip chamber -->
                    <rect x="15" y="115" width="10" height="18" rx="3" fill="#e0f2fe" stroke="#93c5fd" stroke-width="0.8"/>
                    <!-- Drip animation -->
                    <circle cx="20" cy="120" r="1.5" fill="#3b82f6" opacity="0.7">
                      <animate attributeName="cy" values="118;130;118" dur="1.5s" repeatCount="indefinite"/>
                      <animate attributeName="opacity" values="0.8;0.2;0.8" dur="1.5s" repeatCount="indefinite"/>
                    </circle>
                    <!-- Base -->
                    <circle cx="20" cy="332" r="15" fill="none" stroke="#94a3b8" stroke-width="2"/>
                  </g>

                  <!-- ═══ RIGHT SIDE: Defibrillator / AED ═══ -->
                  <g transform="translate(510, 160)">
                    <!-- Body -->
                    <rect x="0" y="0" width="130" height="100" rx="12" fill="#1e293b" stroke="#475569" stroke-width="2"/>
                    <!-- Screen -->
                    <rect x="10" y="10" width="70" height="45" rx="5" fill="#0f172a"/>
                    <!-- ECG on screen -->
                    <polyline fill="none" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round"
                      points="15,35 25,35 30,25 33,45 36,30 40,35 55,35 62,28 65,42 68,35 75,35">
                      <animate attributeName="stroke-dashoffset" values="120;0" dur="1.8s" repeatCount="indefinite"/>
                    </polyline>
                    <!-- Status indicators -->
                    <circle cx="92" cy="22" r="4" fill="#22c55e" opacity="0.6">
                      <animate attributeName="opacity" values="0.4;0.9;0.4" dur="1.5s" repeatCount="indefinite"/>
                    </circle>
                    <text x="100" y="25" fill="#94a3b8" font-size="5" font-family="monospace">RDY</text>
                    <circle cx="92" cy="38" r="4" fill="#eab308" opacity="0.3"/>
                    <!-- Buttons -->
                    <circle cx="25" cy="75" r="10" fill="#dc2626" opacity="0.2" stroke="#dc2626" stroke-width="1.5"/>
                    <text x="25" y="78" text-anchor="middle" fill="#dc2626" font-size="5" font-weight="bold">SHOCK</text>
                    <rect x="50" y="65" width="25" height="12" rx="4" fill="#334155" stroke="#475569" stroke-width="1"/>
                    <rect x="80" y="65" width="25" height="12" rx="4" fill="#334155" stroke="#475569" stroke-width="1"/>
                    <!-- Paddles -->
                    <path d="M120 30 Q140 30 145 50 L145 70 Q140 80 130 80 L125 70 L125 35 Z" fill="#475569" stroke="#64748b" stroke-width="1"/>
                    <ellipse cx="140" cy="55" rx="8" ry="14" fill="#64748b"/>
                  </g>

                  <!-- ═══ RIGHT: Microscope ═══ -->
                  <g transform="translate(580, 30)">
                    <!-- Base -->
                    <rect x="20" y="120" width="60" height="8" rx="3" fill="#64748b"/>
                    <!-- Stage -->
                    <rect x="30" y="95" width="40" height="5" rx="2" fill="#94a3b8"/>
                    <!-- Arm -->
                    <rect x="68" y="20" width="8" height="100" rx="3" fill="#64748b"/>
                    <!-- Eyepiece -->
                    <rect x="55" y="5" width="12" height="25" rx="4" fill="#475569"/>
                    <ellipse cx="61" cy="5" rx="8" ry="4" fill="#334155" stroke="#475569" stroke-width="1"/>
                    <!-- Objective lenses -->
                    <rect x="44" y="82" width="6" height="14" rx="2" fill="#475569"/>
                    <rect x="52" y="85" width="6" height="16" rx="2" fill="#475569"/>
                    <rect x="60" y="83" width="6" height="13" rx="2" fill="#475569"/>
                    <!-- Lens glow -->
                    <circle cx="55" cy="97" r="3" fill="#3b82f6" opacity="0.3">
                      <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3s" repeatCount="indefinite"/>
                    </circle>
                    <!-- Focus knobs -->
                    <circle cx="76" cy="60" r="6" fill="#475569" stroke="#64748b" stroke-width="1"/>
                    <circle cx="76" cy="80" r="4" fill="#475569" stroke="#64748b" stroke-width="1"/>
                  </g>

                  <!-- ═══ BOTTOM LEFT: Pill bottles ═══ -->
                  <g transform="translate(60, 340)">
                    <rect x="0" y="20" width="22" height="35" rx="4" fill="#7dd3fc" opacity="0.5" stroke="#38bdf8" stroke-width="0.8"/>
                    <rect x="-2" y="15" width="26" height="8" rx="3" fill="#bae6fd" opacity="0.5"/>
                    <text x="11" y="42" text-anchor="middle" fill="#0c4a6e" font-size="4" font-weight="bold" opacity="0.5">Rx</text>
                  </g>
                  <g transform="translate(95, 350)">
                    <rect x="0" y="15" width="18" height="28" rx="4" fill="#a5b4fc" opacity="0.4" stroke="#818cf8" stroke-width="0.8"/>
                    <rect x="-1" y="10" width="20" height="7" rx="3" fill="#c7d2fe" opacity="0.4"/>
                  </g>

                  <!-- ═══ BOTTOM RIGHT: Clipboard ═══ -->
                  <g transform="translate(540, 310)">
                    <rect x="10" y="0" width="50" height="65" rx="4" fill="#fef3c7" opacity="0.3" stroke="#fbbf24" stroke-width="1"/>
                    <rect x="22" y="-5" width="26" height="10" rx="3" fill="#d97706" opacity="0.3"/>
                    <!-- Lines -->
                    <line x1="18" y1="18" x2="52" y2="18" stroke="#d97706" stroke-width="0.8" opacity="0.2"/>
                    <line x1="18" y1="26" x2="48" y2="26" stroke="#d97706" stroke-width="0.8" opacity="0.2"/>
                    <line x1="18" y1="34" x2="52" y2="34" stroke="#d97706" stroke-width="0.8" opacity="0.2"/>
                    <line x1="18" y1="42" x2="40" y2="42" stroke="#d97706" stroke-width="0.8" opacity="0.2"/>
                    <!-- Check marks -->
                    <path d="M15 17 l2 2 l4-4" fill="none" stroke="#22c55e" stroke-width="1" opacity="0.3"/>
                    <path d="M15 25 l2 2 l4-4" fill="none" stroke="#22c55e" stroke-width="1" opacity="0.3"/>
                  </g>
                </svg>
              </div>

              <!-- AI Bunny Doctor SVG — robotic face with animations, 3x size -->
              <div class="w-[16rem] h-[20rem] sm:w-[18rem] sm:h-[23rem] lg:w-[20rem] lg:h-[26rem]" style="position: relative; z-index: 1;">
                <svg viewBox="-10 -30 260 380" class="w-full h-full" style="filter: drop-shadow(0 12px 32px rgba(0,0,0,0.15))">
                  <defs>
                    <linearGradient id="earGlow" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#7dd3fc" stop-opacity="0.3"/>
                      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
                    </linearGradient>
                    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#a78bfa"/>
                      <stop offset="100%" stop-color="#7c3aed"/>
                    </linearGradient>
                    <filter id="neonGlow">
                      <feGaussianBlur stdDeviation="2" result="blur"/>
                      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
                    </filter>
                  </defs>

                  <!-- Left ear -->
                  <g transform="rotate(-8 120 110)">
                    <ellipse cx="120" cy="55" rx="19" ry="65" fill="white" stroke="#64748b" stroke-width="2.5"/>
                    <ellipse cx="120" cy="50" rx="10" ry="46" fill="url(#earGlow)"/>
                    <line x1="120" y1="10" x2="120" y2="85" stroke="#38bdf8" stroke-width="0.8" opacity="0.4" stroke-dasharray="3 5">
                      <animate attributeName="stroke-dashoffset" values="0;16" dur="2s" repeatCount="indefinite"/>
                    </line>
                    <circle cx="120" cy="20" r="2" fill="#38bdf8" opacity="0.5">
                      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.5s" repeatCount="indefinite"/>
                    </circle>
                    <animateTransform attributeName="transform" type="rotate" values="-8 120 110;-10 120 110;-8 120 110;-6 120 110;-8 120 110" dur="5s" repeatCount="indefinite"/>
                  </g>

                  <!-- Right ear -->
                  <g transform="rotate(8 160 110)">
                    <ellipse cx="160" cy="50" rx="19" ry="65" fill="white" stroke="#64748b" stroke-width="2.5"/>
                    <ellipse cx="160" cy="45" rx="10" ry="46" fill="url(#earGlow)"/>
                    <line x1="160" y1="5" x2="160" y2="80" stroke="#38bdf8" stroke-width="0.8" opacity="0.4" stroke-dasharray="3 5">
                      <animate attributeName="stroke-dashoffset" values="0;-16" dur="2.2s" repeatCount="indefinite"/>
                    </line>
                    <circle cx="160" cy="16" r="2" fill="#38bdf8" opacity="0.5">
                      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.5s" repeatCount="indefinite" begin="0.8s"/>
                    </circle>
                    <animateTransform attributeName="transform" type="rotate" values="8 160 110;6 160 110;8 160 110;10 160 110;8 160 110" dur="4.5s" repeatCount="indefinite"/>
                  </g>

                  <!-- Antenna / sensor on right ear tip -->
                  <g>
                    <line x1="172" y1="30" x2="185" y2="5" stroke="#38bdf8" stroke-width="1.5" opacity="0.7"/>
                    <circle cx="185" cy="5" r="4.5" fill="#0ea5e9" opacity="0.9" filter="url(#neonGlow)">
                      <animate attributeName="r" values="3.5;5.5;3.5" dur="1.2s" repeatCount="indefinite"/>
                      <animate attributeName="opacity" values="0.6;1;0.6" dur="1.2s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="185" cy="5" r="6" fill="none" stroke="#38bdf8" stroke-width="0.8" opacity="0">
                      <animate attributeName="r" values="5;14" dur="1.8s" repeatCount="indefinite"/>
                      <animate attributeName="opacity" values="0.5;0" dur="1.8s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="185" cy="5" r="6" fill="none" stroke="#38bdf8" stroke-width="0.6" opacity="0">
                      <animate attributeName="r" values="5;18" dur="1.8s" repeatCount="indefinite" begin="0.6s"/>
                      <animate attributeName="opacity" values="0.3;0" dur="1.8s" repeatCount="indefinite" begin="0.6s"/>
                    </circle>
                  </g>

                  <!-- Head -->
                  <ellipse cx="140" cy="150" rx="65" ry="60" fill="white" stroke="#64748b" stroke-width="3"/>
                  <ellipse cx="140" cy="148" rx="55" ry="48" fill="none" stroke="#e2e8f0" stroke-width="0.8" stroke-dasharray="4 3" opacity="0.5"/>

                  <!-- Eyes -->
                  <rect x="100" y="126" width="32" height="24" rx="12" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="1.5"/>
                  <rect x="102" y="128" width="28" height="20" rx="10" fill="none" stroke="#3b82f6" stroke-width="0.5" opacity="0.3"/>
                  <circle ref="leftPupil" :cx="eyeOffset.lx || 116" :cy="eyeOffset.ly || 138" r="7" fill="#3b82f6" filter="url(#neonGlow)"/>
                  <circle :cx="(eyeOffset.lx || 116) - 2" :cy="(eyeOffset.ly || 138) - 2" r="2.5" fill="white" opacity="0.85"/>
                  <rect x="100" y="126" width="32" height="24" rx="12" fill="#e2e8f0" opacity="0">
                    <animate attributeName="opacity" values="0;0;0;1;0;0;0;0;0;0;0;0;0;0;0;0" dur="6s" repeatCount="indefinite"/>
                    <animate attributeName="height" values="24;24;24;2;24;24;24;24;24;24;24;24;24;24;24;24" dur="6s" repeatCount="indefinite"/>
                  </rect>

                  <rect x="148" y="126" width="32" height="24" rx="12" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="1.5"/>
                  <rect x="150" y="128" width="28" height="20" rx="10" fill="none" stroke="#3b82f6" stroke-width="0.5" opacity="0.3"/>
                  <circle ref="rightPupil" :cx="eyeOffset.rx || 164" :cy="eyeOffset.ry || 138" r="7" fill="#3b82f6" filter="url(#neonGlow)"/>
                  <circle :cx="(eyeOffset.rx || 164) - 2" :cy="(eyeOffset.ry || 138) - 2" r="2.5" fill="white" opacity="0.85"/>
                  <rect x="148" y="126" width="32" height="24" rx="12" fill="#e2e8f0" opacity="0">
                    <animate attributeName="opacity" values="0;0;0;1;0;0;0;0;0;0;0;0;0;0;0;0" dur="6s" repeatCount="indefinite"/>
                    <animate attributeName="height" values="24;24;24;2;24;24;24;24;24;24;24;24;24;24;24;24" dur="6s" repeatCount="indefinite"/>
                  </rect>

                  <!-- Nose -->
                  <polygon points="140,155 136,161 144,161" fill="#94a3b8" stroke="#64748b" stroke-width="1"/>
                  <circle cx="140" cy="159" r="1.5" fill="#3b82f6" opacity="0.6">
                    <animate attributeName="opacity" values="0.4;0.9;0.4" dur="2s" repeatCount="indefinite"/>
                  </circle>

                  <!-- Whiskers -->
                  <line x1="88" y1="152" x2="113" y2="156" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
                  <line x1="88" y1="162" x2="113" y2="161" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
                  <line x1="167" y1="156" x2="192" y2="152" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
                  <line x1="167" y1="161" x2="192" y2="162" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
                  <circle cx="88" cy="152" r="1.5" fill="#38bdf8" opacity="0.5"><animate attributeName="opacity" values="0.3;0.8;0.3" dur="2.5s" repeatCount="indefinite"/></circle>
                  <circle cx="88" cy="162" r="1.5" fill="#38bdf8" opacity="0.5"><animate attributeName="opacity" values="0.3;0.8;0.3" dur="2.5s" repeatCount="indefinite" begin="0.7s"/></circle>
                  <circle cx="192" cy="152" r="1.5" fill="#38bdf8" opacity="0.5"><animate attributeName="opacity" values="0.3;0.8;0.3" dur="2.5s" repeatCount="indefinite" begin="0.3s"/></circle>
                  <circle cx="192" cy="162" r="1.5" fill="#38bdf8" opacity="0.5"><animate attributeName="opacity" values="0.3;0.8;0.3" dur="2.5s" repeatCount="indefinite" begin="1s"/></circle>

                  <!-- Mouth — animated equalizer when speaking -->
                  <g v-if="heroSpeaking">
                    <rect x="122" y="167" width="36" height="8" rx="4" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="0.8"/>
                    <rect x="125" y="172" width="3" height="0" rx="0.5" fill="#3b82f6" opacity="0.8">
                      <animate attributeName="height" values="1;5;2;4;1" dur="0.4s" repeatCount="indefinite"/>
                      <animate attributeName="y" values="172;168;171;169;172" dur="0.4s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="130" y="172" width="3" height="0" rx="0.5" fill="#38bdf8" opacity="0.8">
                      <animate attributeName="height" values="2;5;1;5;2" dur="0.35s" repeatCount="indefinite"/>
                      <animate attributeName="y" values="171;168;172;168;171" dur="0.35s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="135" y="172" width="3" height="0" rx="0.5" fill="#0ea5e9" opacity="0.9">
                      <animate attributeName="height" values="3;6;2;6;3" dur="0.3s" repeatCount="indefinite"/>
                      <animate attributeName="y" values="170;167;171;167;170" dur="0.3s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="140" y="172" width="3" height="0" rx="0.5" fill="#38bdf8" opacity="0.8">
                      <animate attributeName="height" values="1;5;3;5;1" dur="0.38s" repeatCount="indefinite"/>
                      <animate attributeName="y" values="172;168;170;168;172" dur="0.38s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="145" y="172" width="3" height="0" rx="0.5" fill="#3b82f6" opacity="0.8">
                      <animate attributeName="height" values="4;1;5;2;4" dur="0.32s" repeatCount="indefinite"/>
                      <animate attributeName="y" values="169;172;168;171;169" dur="0.32s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="150" y="172" width="3" height="0" rx="0.5" fill="#38bdf8" opacity="0.7">
                      <animate attributeName="height" values="2;5;1;4;2" dur="0.36s" repeatCount="indefinite"/>
                      <animate attributeName="y" values="171;168;172;169;171" dur="0.36s" repeatCount="indefinite"/>
                    </rect>
                  </g>
                  <!-- Idle mouth -->
                  <g v-else>
                    <rect x="122" y="167" width="36" height="8" rx="4" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="0.8"/>
                    <rect x="128" y="170" width="24" height="2" rx="1" fill="#3b82f6" opacity="0.4">
                      <animate attributeName="opacity" values="0.3;0.5;0.3" dur="3s" repeatCount="indefinite"/>
                    </rect>
                  </g>

                  <!-- Body / scrubs -->
                  <path d="M90 200 Q90 185 105 178 L120 195 Q140 205 160 195 L175 178 Q190 185 190 200 L195 290 L85 290 Z" fill="url(#bodyGrad)" stroke="#64748b" stroke-width="2.5"/>
                  <path d="M110 195 L140 210 L170 195" fill="white" stroke="#94a3b8" stroke-width="1.5"/>
                  <g opacity="0.5">
                    <line x1="105" y1="225" x2="175" y2="225" stroke="#38bdf8" stroke-width="0.6" opacity="0.2"/>
                    <polyline fill="none" stroke="#38bdf8" stroke-width="1" stroke-linecap="round"
                      points="105,225 120,225 125,225 128,215 131,235 134,220 137,230 140,225 175,225" opacity="0.4">
                      <animate attributeName="stroke-dashoffset" values="100;0" dur="2s" repeatCount="indefinite"/>
                    </polyline>
                    <circle cx="140" cy="235" r="4" fill="#38bdf8" opacity="0.15">
                      <animate attributeName="r" values="3;8;3" dur="2s" repeatCount="indefinite"/>
                      <animate attributeName="opacity" values="0.2;0.05;0.2" dur="2s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="140" cy="235" r="2" fill="#38bdf8" opacity="0.5">
                      <animate attributeName="opacity" values="0.3;0.8;0.3" dur="1s" repeatCount="indefinite"/>
                    </circle>
                  </g>
                  <!-- Sleeves -->
                  <ellipse cx="88" cy="215" rx="15" ry="12" fill="url(#bodyGrad)" stroke="#64748b" stroke-width="2.5"/>
                  <ellipse cx="192" cy="215" rx="15" ry="12" fill="url(#bodyGrad)" stroke="#64748b" stroke-width="2.5"/>
                  <!-- Left hand -->
                  <circle cx="80" cy="230" r="10" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
                  <!-- Right hand (waves) -->
                  <g>
                    <animateTransform attributeName="transform" type="rotate" values="0 200 215;-20 200 215;15 200 215;-15 200 215;10 200 215;0 200 215;0 200 215;0 200 215;0 200 215;0 200 215;0 200 215;0 200 215;0 200 215;0 200 215;0 200 215;0 200 215" dur="8s" repeatCount="indefinite"/>
                    <circle cx="200" cy="230" r="10" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
                    <circle cx="196" cy="221" r="3" fill="white" stroke="#94a3b8" stroke-width="1.5" opacity="0.8"/>
                    <circle cx="200" cy="219" r="3" fill="white" stroke="#94a3b8" stroke-width="1.5" opacity="0.8"/>
                    <circle cx="204" cy="221" r="3" fill="white" stroke="#94a3b8" stroke-width="1.5" opacity="0.8"/>
                  </g>
                  <!-- Stethoscope -->
                  <path d="M130 200 Q125 225 135 240" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="135" cy="242" r="5" fill="none" stroke="#38bdf8" stroke-width="1.5"/>
                  <circle cx="135" cy="242" r="2" fill="#38bdf8" opacity="0.5">
                    <animate attributeName="opacity" values="0.3;0.8;0.3" dur="1.5s" repeatCount="indefinite"/>
                  </circle>
                  <!-- Feet -->
                  <ellipse cx="115" cy="298" rx="18" ry="12" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
                  <ellipse cx="165" cy="298" rx="18" ry="12" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
                  <!-- Name tag -->
                  <rect x="115" y="250" width="50" height="16" rx="4" fill="white" stroke="#38bdf8" stroke-width="1" filter="url(#neonGlow)"/>
                  <text x="140" y="262" text-anchor="middle" fill="#3b82f6" font-size="7.5" font-weight="bold" font-family="system-ui, sans-serif">DR. HOPPS</text>
                </svg>
              </div>
            </div>
            <!-- Avatar name + sound toggle -->
            <div class="mt-2 text-center">
              <div class="text-base font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Dr. Hopps</div>
              <div class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ heroAvatar.specialty }}</div>
              <!-- Sound toggle -->
              <button
                @click="toggleSound"
                class="mt-2 inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 border"
                :class="soundOn
                  ? (isDark ? 'bg-blue-500/15 border-blue-500/30 text-blue-300 hover:bg-blue-500/25' : 'bg-blue-50 border-blue-300 text-blue-600 hover:bg-blue-100')
                  : (isDark ? 'bg-slate-800/60 border-slate-700/50 text-slate-400 hover:text-slate-200 hover:bg-slate-800' : 'bg-slate-100 border-slate-300 text-slate-500 hover:text-slate-700 hover:bg-slate-200')"
              >
                <svg v-if="soundOn" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                </svg>
                <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"/>
                </svg>
                {{ soundOn ? 'Listening' : 'Tap to hear me' }}
                <span v-if="soundOn && heroSpeaking" class="flex items-center gap-0.5 ml-0.5">
                  <span class="w-0.5 h-2 rounded-full animate-pulse" :class="isDark ? 'bg-blue-400' : 'bg-blue-500'" style="animation-delay:0s"></span>
                  <span class="w-0.5 h-3 rounded-full animate-pulse" :class="isDark ? 'bg-blue-400' : 'bg-blue-500'" style="animation-delay:0.15s"></span>
                  <span class="w-0.5 h-2 rounded-full animate-pulse" :class="isDark ? 'bg-blue-400' : 'bg-blue-500'" style="animation-delay:0.3s"></span>
                </span>
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ═══════ TRUST BAND ═══════ -->
    <section class="relative z-10 border-y py-6" :class="isDark ? 'border-slate-800/50 bg-slate-900/30' : 'border-slate-200 bg-white/30'">
      <div class="max-w-6xl mx-auto px-6 flex flex-wrap items-center justify-center gap-x-10 gap-y-3 text-xs font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
        <span class="flex items-center gap-2">
          <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
          {{ t('trust.agents') }}
        </span>
        <span class="flex items-center gap-2">
          <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          {{ t('trust.safety') }}
        </span>
        <span class="flex items-center gap-2">
          <svg class="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          {{ t('trust.zeroData') }}
        </span>
        <span class="flex items-center gap-2">
          <svg class="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          {{ t('trust.clinical') }}
        </span>
        <span class="flex items-center gap-2">
          <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          {{ t('trust.speed') }}
        </span>
      </div>
    </section>

    <!-- ═══════ AGENT PIPELINE — How It Works ═══════ -->
    <div class="relative max-w-6xl mx-auto px-6 py-16" style="z-index:10">
      <div class="text-center mb-10">
        <h2 class="text-display font-bold text-[var(--text-primary)]">{{ t('hero.howItWorks') }}</h2>
        <p class="text-sm mt-2 max-w-lg mx-auto" :class="isDark ? 'text-slate-400' : 'text-slate-500'">7 specialized AI agents collaborate on every diagnosis</p>
      </div>

      <!-- Desktop: horizontal pipeline with connectors -->
      <div class="hidden lg:flex items-start justify-between gap-0">
        <template v-for="(agent, i) in agents" :key="agent.key">
          <div class="flex-1 flex flex-col items-center text-center group">
            <!-- Step number -->
            <div class="w-8 h-8 rounded-full flex items-center justify-center mb-3 text-xs font-bold border-2 transition-colors"
              :class="isDark ? 'bg-slate-800 border-slate-600 text-slate-300 group-hover:border-blue-500 group-hover:text-blue-400' : 'bg-white border-slate-300 text-slate-500 group-hover:border-blue-500 group-hover:text-blue-600 shadow-sm'">
              {{ i + 1 }}
            </div>
            <!-- Agent card -->
            <div class="rounded-xl p-4 transition-all duration-300 border w-full hover:-translate-y-1"
              :class="isDark
                ? 'bg-slate-800/50 border-slate-700/40 hover:border-blue-500/40 hover:bg-slate-800/70'
                : 'bg-white/70 border-slate-200/80 hover:border-blue-400/50 hover:bg-white shadow-card hover:shadow-elevated'">
              <div class="text-2xl mb-2">{{ agent.icon }}</div>
              <div class="text-xs font-semibold mb-1" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ t(agent.nameKey) }}</div>
              <div class="text-detail leading-snug" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ t(agent.descKey) }}</div>
            </div>
          </div>
          <!-- Connector arrow between agents -->
          <div v-if="i < agents.length - 1" class="flex items-center pt-4 px-0.5 flex-shrink-0">
            <svg class="w-5 h-5" :class="isDark ? 'text-slate-600' : 'text-slate-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </div>
        </template>
      </div>

      <!-- Mobile/Tablet: grid layout -->
      <div class="lg:hidden grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div
          v-for="(agent, i) in agents" :key="'m-'+agent.key"
          class="group relative rounded-xl p-3 text-center transition-all duration-300 border"
          :class="isDark
            ? 'bg-slate-800/50 border-slate-700/40 hover:border-slate-600/60 hover:bg-slate-800/70'
            : 'bg-white/70 border-slate-200/80 hover:border-slate-300 hover:bg-white shadow-sm'"
        >
          <div class="absolute -top-2 -left-1 w-5 h-5 rounded-full flex items-center justify-center border"
            :class="isDark ? 'bg-slate-800 border-slate-600' : 'bg-white border-slate-300 shadow-sm'">
            <span class="text-tiny font-bold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ i + 1 }}</span>
          </div>
          <div class="text-xl mb-1.5">{{ agent.icon }}</div>
          <div class="text-xs font-semibold" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ t(agent.nameKey) }}</div>
          <div class="text-detail mt-0.5" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ t(agent.descKey) }}</div>
        </div>
      </div>
    </div>

    <!-- ═══════ SAMPLE DIAGNOSTIC OUTPUT ═══════ -->
    <section class="relative z-10 py-16 px-6">
      <div class="max-w-6xl mx-auto">
        <div class="text-center mb-10">
          <h2 class="text-display font-bold text-[var(--text-primary)]">{{ t('sample.heading') }}</h2>
          <p class="text-sm mt-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('sample.subheading') }}</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 max-w-5xl mx-auto">
          <!-- Card 1: Differential Diagnosis -->
          <div class="rounded-xl border p-5 transition-all duration-200 hover:-translate-y-0.5"
            :class="isDark ? 'bg-slate-800/50 border-slate-700/40' : 'bg-white/70 border-slate-200/80 shadow-sm hover:shadow-md'">
            <div class="text-detail font-bold uppercase tracking-wider text-blue-400 mb-3">{{ t('sample.diffDx') }}</div>
            <div class="space-y-2.5">
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Tension Headache</span>
                <span class="text-xs font-bold tabular-nums text-emerald-400">78%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Migraine</span>
                <span class="text-xs font-bold tabular-nums text-amber-400">62%</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium" :class="isDark ? 'text-slate-200' : 'text-slate-700'">Sinusitis</span>
                <span class="text-xs font-bold tabular-nums text-orange-400">41%</span>
              </div>
            </div>
          </div>
          <!-- Card 2: Safety Review -->
          <div class="rounded-xl border p-5 transition-all duration-200 hover:-translate-y-0.5"
            :class="isDark ? 'bg-slate-800/50 border-slate-700/40' : 'bg-white/70 border-slate-200/80 shadow-sm hover:shadow-md'">
            <div class="text-detail font-bold uppercase tracking-wider text-emerald-400 mb-3">{{ t('sample.safetyReview') }}</div>
            <div class="flex items-center gap-2 mb-3">
              <span class="px-2 py-0.5 rounded-full text-detail font-bold bg-emerald-500/15 text-emerald-400">PASS</span>
              <span class="text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('sample.safetyPass') }}</span>
            </div>
            <div class="text-xs leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('sample.safetyDesc') }}</div>
          </div>
          <!-- Card 3: Treatment Plan -->
          <div class="rounded-xl border p-5 transition-all duration-200 hover:-translate-y-0.5"
            :class="isDark ? 'bg-slate-800/50 border-slate-700/40' : 'bg-white/70 border-slate-200/80 shadow-sm hover:shadow-md'">
            <div class="text-detail font-bold uppercase tracking-wider text-amber-400 mb-3">{{ t('sample.treatmentPlan') }}</div>
            <div class="space-y-1.5 text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
              <div class="flex items-start gap-2"><span class="text-amber-400 mt-0.5">&#8226;</span>OTC pain relief recommended</div>
              <div class="flex items-start gap-2"><span class="text-amber-400 mt-0.5">&#8226;</span>Hydration &amp; rest protocol</div>
              <div class="flex items-start gap-2"><span class="text-amber-400 mt-0.5">&#8226;</span>Follow-up if symptoms persist &gt;72h</div>
            </div>
          </div>
        </div>
        <div class="text-center mt-6">
          <button @click="viewSampleReport" class="text-sm font-medium px-5 py-2.5 rounded-lg border transition-all duration-200 hover:-translate-y-0.5"
            :class="isDark
              ? 'text-slate-300 hover:text-white border-slate-700/50 hover:border-slate-600 bg-slate-800/50 hover:bg-slate-800'
              : 'text-slate-600 hover:text-slate-900 border-slate-300 hover:border-slate-400 bg-white/60 hover:bg-white shadow-sm'">
            {{ t('sample.viewFull') }} &rarr;
          </button>
        </div>
      </div>
    </section>

    <!-- ═══════ FEATURE CARDS — Built for Medical Intelligence ═══════ -->
    <div class="relative max-w-5xl mx-auto px-6 py-16" style="z-index:10">
      <div class="text-center mb-10">
        <h2 class="text-display font-bold text-[var(--text-primary)]">{{ t('features.heading') }}</h2>
        <p class="text-sm mt-2" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('features.subheading') }}</p>
      </div>
      <div class="grid sm:grid-cols-3 gap-5">
        <div v-for="feat in features" :key="feat.titleKey"
          class="rounded-xl p-6 transition-all duration-300 border backdrop-blur-lg hover:-translate-y-1"
          :class="isDark
            ? 'bg-slate-900/40 border-slate-700/30 hover:border-slate-600/50 hover:bg-slate-900/60'
            : 'bg-white/50 border-white/60 hover:bg-white/70 shadow-lg shadow-slate-200/40 hover:shadow-slate-300/50'"
        >
          <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4" :class="feat.iconBg">
            <svg class="w-6 h-6" :class="feat.iconColor" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="feat.iconPath"/>
            </svg>
          </div>
          <h3 class="text-sm font-bold mb-1.5" :class="isDark ? 'text-white' : 'text-slate-800'">{{ t(feat.titleKey) }}</h3>
          <p class="text-xs leading-relaxed" :class="isDark ? 'text-slate-500' : 'text-slate-500'">{{ t(feat.descKey) }}</p>
        </div>
      </div>
    </div>

    <!-- ═══════ PRIVACY & SECURITY — Your Data Stays Private ═══════ -->
    <div class="relative max-w-4xl mx-auto px-6 py-16" style="z-index:10">
      <div class="rounded-2xl p-6 sm:p-8 backdrop-blur-lg border"
        :class="isDark
          ? 'bg-slate-900/40 border-slate-700/30'
          : 'bg-white/50 border-white/60 shadow-lg shadow-slate-200/50'">
        <div class="text-center mb-6">
          <div class="inline-flex items-center gap-2.5 mb-2">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center" :class="isDark ? 'bg-emerald-500/15' : 'bg-emerald-50'">
              <svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
            </div>
            <h2 class="text-heading font-bold text-[var(--text-primary)]">{{ t('privacy.title') }}</h2>
          </div>
          <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('privacy.subtitle') }}</p>
        </div>
        <div class="grid sm:grid-cols-3 gap-4">
          <div class="flex flex-col items-center text-center p-5 rounded-xl border transition-all duration-200 hover:-translate-y-0.5"
            :class="isDark ? 'bg-slate-800/40 border-slate-700/30 hover:border-slate-600/50' : 'bg-white/60 border-slate-200/60 hover:border-slate-300 hover:shadow-sm'">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-3" :class="isDark ? 'bg-emerald-500/15' : 'bg-emerald-50'">
              <svg class="w-6 h-6 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
            </div>
            <h3 class="text-xs font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-800'">{{ t('privacy.localTitle') }}</h3>
            <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('privacy.localDesc') }}</p>
          </div>
          <div class="flex flex-col items-center text-center p-5 rounded-xl border transition-all duration-200 hover:-translate-y-0.5"
            :class="isDark ? 'bg-slate-800/40 border-slate-700/30 hover:border-slate-600/50' : 'bg-white/60 border-slate-200/60 hover:border-slate-300 hover:shadow-sm'">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-3" :class="isDark ? 'bg-blue-500/15' : 'bg-blue-50'">
              <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"/></svg>
            </div>
            <h3 class="text-xs font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-800'">{{ t('privacy.noPassTitle') }}</h3>
            <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('privacy.noPassDesc') }}</p>
          </div>
          <div class="flex flex-col items-center text-center p-5 rounded-xl border transition-all duration-200 hover:-translate-y-0.5"
            :class="isDark ? 'bg-slate-800/40 border-slate-700/30 hover:border-slate-600/50' : 'bg-white/60 border-slate-200/60 hover:border-slate-300 hover:shadow-sm'">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-3" :class="isDark ? 'bg-purple-500/15' : 'bg-purple-50'">
              <svg class="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            </div>
            <h3 class="text-xs font-semibold mb-1" :class="isDark ? 'text-white' : 'text-slate-800'">{{ t('privacy.controlTitle') }}</h3>
            <p class="text-caption leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ t('privacy.controlDesc') }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="relative border-t py-6 px-6 text-center" style="z-index:10"
      :class="isDark ? 'border-slate-800/50' : 'border-slate-200'">
      <p class="text-caption max-w-lg mx-auto leading-relaxed" :class="isDark ? 'text-slate-600' : 'text-slate-400'">
        {{ t('hero.disclaimer') }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import DoctorAvatar from '@/components/DoctorAvatar.vue'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'
import { useUser } from '@/composables/useUser.js'

const router = useRouter()
const { isDark } = useTheme()
const { t } = useI18n()
const { profile, isLoggedIn, logout: doLogout } = useUser()

// User menu
const showUserMenu = ref(false)
const userMenuRef = ref(null)
const userName = computed(() => profile.value.name || '')
const userEmail = computed(() => profile.value.email || '')
const userInitials = computed(() =>
  userName.value
    ? userName.value.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
    : ''
)

function onClickOutsideUserMenu(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) showUserMenu.value = false
}
onMounted(() => document.addEventListener('click', onClickOutsideUserMenu))
onUnmounted(() => document.removeEventListener('click', onClickOutsideUserMenu))

function handleLogout() {
  showUserMenu.value = false
  doLogout()
}

// ─── Animated background ───
const bgCanvas = ref(null)
let animId = null
let blobs = []
let mouseX = -1
let mouseY = -1

const darkPalette = [
  [20, 60, 160],   // vivid blue
  [90, 30, 140],   // rich purple
  [10, 100, 110],  // teal
  [60, 15, 120],   // deep indigo
  [140, 40, 100],  // magenta
  [15, 80, 140],   // ocean blue
  [30, 50, 100],   // steel blue
  [80, 20, 160],   // electric violet
  [5, 110, 90],    // emerald teal
  [110, 30, 70],   // berry
]
const lightPalette = [
  [50, 100, 255],  // electric blue
  [140, 60, 255],  // vivid purple
  [0, 200, 200],   // cyan
  [255, 60, 130],  // hot pink
  [255, 120, 0],   // tangerine orange
  [0, 180, 255],   // azure
  [180, 0, 255],   // violet
  [0, 220, 120],   // emerald
  [255, 80, 80],   // coral red
  [80, 60, 255],   // indigo
]

function initBlobs(w, h) {
  const palette = isDark.value ? darkPalette : lightPalette
  // Dark: slower, more subtle drift. Light: moderate, visible but calm.
  const speedMult = isDark.value ? 0.4 : 0.8
  blobs = Array.from({ length: 10 }, (_, i) => ({
    x: Math.random() * w,
    y: Math.random() * h,
    r: (isDark.value ? 180 : 140) + Math.random() * (isDark.value ? 320 : 260),
    vx: (Math.random() - 0.5) * 0.35 * speedMult,
    vy: (Math.random() - 0.5) * 0.25 * speedMult,
    color: palette[i % palette.length],
    targetColor: palette[i % palette.length],
    phase: Math.random() * Math.PI * 2,
    pulseSpeed: (0.001 + Math.random() * 0.003) * speedMult,
    orbitRadius: (15 + Math.random() * 40) * (isDark.value ? 1 : 1.2),
    orbitSpeed: (0.0002 + Math.random() * 0.0005) * speedMult,
    orbitPhase: Math.random() * Math.PI * 2,
  }))
}

function lerpColor(a, b, t) {
  return [
    a[0] + (b[0] - a[0]) * t,
    a[1] + (b[1] - a[1]) * t,
    a[2] + (b[2] - a[2]) * t,
  ]
}

function renderBackground(time) {
  const canvas = bgCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const w = canvas.width
  const h = canvas.height

  // Base fill — light mode uses pure white so screen-blended colors pop
  ctx.fillStyle = isDark.value ? '#020617' : '#ffffff'
  ctx.fillRect(0, 0, w, h)

  // Dark: screen blend makes colors glow. Light: normal blend paints color directly.
  ctx.globalCompositeOperation = isDark.value ? 'screen' : 'source-over'

  const baseOpacity = isDark.value ? 0.3 : 0.25

  for (const blob of blobs) {
    // Orbital drift on top of linear movement
    const ox = Math.sin(time * blob.orbitSpeed + blob.orbitPhase) * blob.orbitRadius
    const oy = Math.cos(time * blob.orbitSpeed * 1.3 + blob.orbitPhase) * blob.orbitRadius * 0.7

    blob.x += blob.vx
    blob.y += blob.vy

    const drawX = blob.x + ox
    const drawY = blob.y + oy

    // Pulse
    const pulse = Math.sin(time * blob.pulseSpeed + blob.phase) * 0.25 + 1
    const r = blob.r * pulse

    // Bounce
    if (blob.x < -100) blob.vx = Math.abs(blob.vx)
    if (blob.x > w + 100) blob.vx = -Math.abs(blob.vx)
    if (blob.y < -100) blob.vy = Math.abs(blob.vy)
    if (blob.y > h + 100) blob.vy = -Math.abs(blob.vy)

    // Lerp color toward target for smooth theme transitions
    blob.color = lerpColor(blob.color, blob.targetColor, 0.02)

    // Mouse interaction: very gentle push
    if (mouseX >= 0) {
      const dx = drawX - mouseX
      const dy = drawY - mouseY
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < 300) {
        const force = (300 - dist) / 300 * 0.04
        blob.vx += (dx / dist) * force
        blob.vy += (dy / dist) * force
      }
    }

    // Dampen velocity — keeps blobs from accelerating over time
    blob.vx *= 0.997
    blob.vy *= 0.997

    // Draw blob with multiple gradient layers for richness
    const [cr, cg, cb] = blob.color
    const grad = ctx.createRadialGradient(drawX, drawY, 0, drawX, drawY, r)
    grad.addColorStop(0, `rgba(${cr|0}, ${cg|0}, ${cb|0}, ${baseOpacity})`)
    grad.addColorStop(0.3, `rgba(${cr|0}, ${cg|0}, ${cb|0}, ${baseOpacity * 0.6})`)
    grad.addColorStop(0.6, `rgba(${cr|0}, ${cg|0}, ${cb|0}, ${baseOpacity * 0.2})`)
    grad.addColorStop(1, `rgba(${cr|0}, ${cg|0}, ${cb|0}, 0)`)
    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.arc(drawX, drawY, r, 0, Math.PI * 2)
    ctx.fill()

    // Inner glow for hotspot — much brighter in light mode
    const glowMult = isDark.value ? 0.5 : 1.2
    const innerR = r * (isDark.value ? 0.35 : 0.5)
    const grad2 = ctx.createRadialGradient(drawX, drawY, 0, drawX, drawY, innerR)
    grad2.addColorStop(0, `rgba(${Math.min(255, (cr|0)+80)}, ${Math.min(255, (cg|0)+80)}, ${Math.min(255, (cb|0)+80)}, ${baseOpacity * glowMult})`)
    grad2.addColorStop(1, `rgba(${cr|0}, ${cg|0}, ${cb|0}, 0)`)
    ctx.fillStyle = grad2
    ctx.beginPath()
    ctx.arc(drawX, drawY, innerR, 0, Math.PI * 2)
    ctx.fill()
  }

  // Aurora streaks (horizontal light bands)
  ctx.globalCompositeOperation = isDark.value ? 'screen' : 'source-over'
  const streakCount = isDark.value ? 2 : 5
  for (let i = 0; i < streakCount; i++) {
    const yBase = isDark.value ? (0.25 + i * 0.4) : (0.1 + i * 0.18)
    const y = h * yBase + Math.sin(time * 0.0003 + i * 2) * h * 0.05
    const thickness = isDark.value ? 50 : 100
    const streakGrad = ctx.createLinearGradient(0, y - thickness, 0, y + thickness)
    const hue = (time * 0.008 + i * 50) % 360
    const alpha = isDark.value ? 0.04 : 0.12
    const sat = isDark.value ? 60 : 90
    const lum = isDark.value ? 45 : 60
    streakGrad.addColorStop(0, `hsla(${hue}, ${sat}%, ${lum}%, 0)`)
    streakGrad.addColorStop(0.5, `hsla(${hue}, ${sat}%, ${lum}%, ${alpha})`)
    streakGrad.addColorStop(1, `hsla(${hue}, ${sat}%, ${lum}%, 0)`)
    ctx.fillStyle = streakGrad
    ctx.fillRect(0, y - thickness, w, thickness * 2)
  }

  ctx.globalCompositeOperation = 'source-over'

  // ── Radiating lines — white rays emanating from a focal point with crescendo thickness ──
  ctx.lineCap = 'round'

  // Focal point: slightly above center, drifts slowly
  const focalX = w * 0.5 + Math.sin(time * 0.00008) * w * 0.05
  const focalY = h * 0.35 + Math.cos(time * 0.00006) * h * 0.03

  if (!isDark.value) {
    const rayCount = 60
    for (let i = 0; i < rayCount; i++) {
      const progress = i / (rayCount - 1)
      // Angle spread: full circle but weighted toward bottom half
      const angle = (i / rayCount) * Math.PI * 2 + time * 0.00003
      // Thickness crescendo as rays fan out
      const thickness = 0.3 + progress * progress * 6
      // Alpha: thin rays ghostly, thick rays bolder
      const alpha = 0.03 + Math.sin(progress * Math.PI) * 0.2
      // Ray length: extends well beyond screen
      const rayLen = Math.max(w, h) * 1.2

      const endX = focalX + Math.cos(angle) * rayLen
      const endY = focalY + Math.sin(angle) * rayLen

      ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`
      ctx.lineWidth = thickness
      ctx.beginPath()
      ctx.moveTo(focalX, focalY)
      ctx.lineTo(endX, endY)
      ctx.stroke()
    }
  } else {
    // Dark mode: fewer, subtler radiating rays
    const rayCount = 30
    for (let i = 0; i < rayCount; i++) {
      const progress = i / (rayCount - 1)
      const angle = (i / rayCount) * Math.PI * 2 + time * 0.00002
      const thickness = 0.2 + progress * progress * 1.8
      const alpha = 0.01 + Math.sin(progress * Math.PI) * 0.04
      const rayLen = Math.max(w, h) * 1.2

      const endX = focalX + Math.cos(angle) * rayLen
      const endY = focalY + Math.sin(angle) * rayLen

      ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`
      ctx.lineWidth = thickness
      ctx.beginPath()
      ctx.moveTo(focalX, focalY)
      ctx.lineTo(endX, endY)
      ctx.stroke()
    }
  }

  animId = requestAnimationFrame(renderBackground)
}

function onMouseMove(e) {
  mouseX = e.clientX
  mouseY = e.clientY
}

function resizeCanvas() {
  const canvas = bgCanvas.value
  if (!canvas) return
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
  initBlobs(canvas.width, canvas.height)
}

// Watch theme changes to smoothly transition blob colors
watch(isDark, () => {
  const palette = isDark.value ? darkPalette : lightPalette
  blobs.forEach((blob, i) => {
    blob.targetColor = palette[i % palette.length]
  })
})

onMounted(() => {
  resizeCanvas()
  animId = requestAnimationFrame(renderBackground)
  window.addEventListener('resize', resizeCanvas)
  window.addEventListener('mousemove', onMouseMove)
})

onUnmounted(() => {
  if (animId) cancelAnimationFrame(animId)
  window.removeEventListener('resize', resizeCanvas)
  window.removeEventListener('mousemove', onMouseMove)
  if (speakInterval) clearInterval(speakInterval)
  if (waveInterval) clearInterval(waveInterval)
  if (keepAliveInterval) clearInterval(keepAliveInterval)
  if (window.speechSynthesis) window.speechSynthesis.cancel()
})

// ─── Avatar ───
const defaultHeroAvatar = {
  name: 'Dr. AI', specialty: "Physician's Assistant",
  skinTone: '#F5CBA7', hairStyle: 'short', hairColor: '#3d2b1f', eyeColor: '#4A6FA5',
  coatColor: '#f0f0f0', glasses: true, bgColor: '#1e3a5f', lipColor: '#c9877a',
  accessoryColor: '#64748b', avatarStyle: 'realistic', photoUrl: '',
}
const saved = localStorage.getItem('doctor_avatar')
const heroAvatar = ref(saved ? { ...defaultHeroAvatar, ...JSON.parse(saved), specialty: "Physician's Assistant" } : defaultHeroAvatar)

const heroSpeaking = ref(false)
const heroWaving = ref(false)
const soundOn = ref(false)
let speakInterval = null
let keepAliveInterval = null
let waveInterval = null

// Dog eye tracking
const dogAvatarContainer = ref(null)
const eyeOffset = reactive({
  lsx: 119.5, lsy: 140.5,  // left pupil shine
  rsx: 163.5, rsy: 140.5,  // right pupil shine
})
const leftPupil = ref(null)
const rightPupil = ref(null)

function handleMouseMove(e) {
  if (!dogAvatarContainer.value) return
  const rect = dogAvatarContainer.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height * 0.37 // eye level
  const dx = e.clientX - centerX
  const dy = e.clientY - centerY
  const angle = Math.atan2(dy, dx)
  const dist = Math.min(Math.sqrt(dx * dx + dy * dy) / 200, 1)
  const maxMove = 4.5

  const ox = Math.cos(angle) * maxMove * dist
  const oy = Math.sin(angle) * maxMove * dist

  // Move pupils
  if (leftPupil.value) {
    leftPupil.value.setAttribute('cx', 118 + ox)
    leftPupil.value.setAttribute('cy', 142 + oy)
  }
  if (rightPupil.value) {
    rightPupil.value.setAttribute('cx', 162 + ox)
    rightPupil.value.setAttribute('cy', 142 + oy)
  }
  // Move shine spots (offset from pupil center)
  eyeOffset.lsx = 119.5 + ox
  eyeOffset.lsy = 140.5 + oy
  eyeOffset.rsx = 163.5 + ox
  eyeOffset.rsy = 140.5 + oy
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
})
onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})

// Greeting messages per language
const greetings = {
  en: `Hello! I'm ${heroAvatar.value.name}, your AI ${heroAvatar.value.specialty}. I'm here to help you understand your symptoms. Just click Start Consultation and describe how you're feeling. I'll guide you through a thorough assessment.`,
  zh: `\u4F60\u597D\uFF01\u6211\u662F${heroAvatar.value.name}\uFF0C\u60A8\u7684AI${heroAvatar.value.specialty}\u3002\u6211\u5728\u8FD9\u91CC\u5E2E\u52A9\u60A8\u4E86\u89E3\u60A8\u7684\u75C7\u72B6\u3002\u70B9\u51FB\u5F00\u59CB\u54A8\u8BE2\uFF0C\u63CF\u8FF0\u60A8\u7684\u611F\u53D7\u3002`,
  es: `\u00A1Hola! Soy ${heroAvatar.value.name}, su ${heroAvatar.value.specialty} con IA. Estoy aqu\u00ED para ayudarle a entender sus s\u00EDntomas. Haga clic en Iniciar Consulta y describa c\u00F3mo se siente.`,
  hi: `\u0928\u092E\u0938\u094D\u0924\u0947! \u092E\u0948\u0902 ${heroAvatar.value.name} \u0939\u0942\u0901\u0964 \u092E\u0948\u0902 \u0906\u092A\u0915\u0947 \u0932\u0915\u094D\u0937\u0923\u094B\u0902 \u0915\u094B \u0938\u092E\u091D\u0928\u0947 \u092E\u0947\u0902 \u0906\u092A\u0915\u0940 \u092E\u0926\u0926 \u0915\u0947 \u0932\u093F\u090F \u092F\u0939\u093E\u0901 \u0939\u0942\u0901\u0964 \u092A\u0930\u093E\u092E\u0930\u094D\u0936 \u0936\u0941\u0930\u0942 \u0915\u0930\u0947\u0902 \u092A\u0930 \u0915\u094D\u0932\u093F\u0915 \u0915\u0930\u0947\u0902\u0964`,
  fr: `Bonjour ! Je suis ${heroAvatar.value.name}, votre ${heroAvatar.value.specialty} IA. Je suis l\u00E0 pour vous aider \u00E0 comprendre vos sympt\u00F4mes. Cliquez sur Commencer la Consultation et d\u00E9crivez comment vous vous sentez.`,
}

function pickVoice() {
  if (!window.speechSynthesis) return null
  const voices = window.speechSynthesis.getVoices()
  if (!voices.length) return null

  const preferredName = heroAvatar.value.preferredVoice
  if (preferredName) {
    const match = voices.find(v => v.name === preferredName)
    if (match) return match
  }

  // Prefer robotic / synthesized sounding voices for the AI doctor
  const roboticNames = [
    'Microsoft Mark Online', 'Microsoft Mark', 'Google UK English Male',
    'Microsoft David Online', 'Microsoft David',
    'Google US English', 'Microsoft Guy Online',
    'Alex', 'Fred', 'Daniel',
  ]
  for (const n of roboticNames) {
    const v = voices.find(voice => voice.name.includes(n))
    if (v) return v
  }
  // Fallback: any English voice, prefer non-local (more synthetic)
  const en = voices.filter(v => v.lang.startsWith('en'))
  return en.find(v => !v.localService) || en[0] || voices[0]
}

function speakGreeting() {
  if (!window.speechSynthesis) return
  window.speechSynthesis.cancel()

  const { lang: currentLang } = useI18n()
  const text = greetings[currentLang.value] || greetings.en

  // Split into chunks for reliability
  const chunks = []
  let remaining = text
  while (remaining.length > 0) {
    if (remaining.length <= 200) { chunks.push(remaining); break }
    let idx = remaining.lastIndexOf('. ', 200)
    if (idx < 60) idx = remaining.lastIndexOf(', ', 200)
    if (idx < 60) idx = remaining.lastIndexOf(' ', 200)
    if (idx < 60) idx = 200
    chunks.push(remaining.substring(0, idx + 1))
    remaining = remaining.substring(idx + 1).trim()
  }

  const voice = pickVoice()
  const rate = heroAvatar.value.voiceRate || 0.95

  // Chrome keep-alive
  keepAliveInterval = setInterval(() => {
    if (window.speechSynthesis.speaking) window.speechSynthesis.resume()
  }, 5000)

  heroSpeaking.value = true

  function speakNext(i) {
    if (i >= chunks.length || !soundOn.value) {
      heroSpeaking.value = false
      if (keepAliveInterval) { clearInterval(keepAliveInterval); keepAliveInterval = null }
      return
    }
    const utt = new SpeechSynthesisUtterance(chunks[i])
    if (voice) utt.voice = voice
    utt.rate = 0.88  // slightly slower for robotic cadence
    utt.pitch = 0.75  // lower pitch for robotic tone
    utt.volume = 0.9
    utt.onend = () => speakNext(i + 1)
    utt.onerror = () => speakNext(i + 1)
    window.speechSynthesis.speak(utt)
  }

  // Small delay after cancel
  setTimeout(() => speakNext(0), 80)
}

function toggleSound() {
  soundOn.value = !soundOn.value
  if (soundOn.value) {
    speakGreeting()
  } else {
    if (window.speechSynthesis) window.speechSynthesis.cancel()
    heroSpeaking.value = false
    if (keepAliveInterval) { clearInterval(keepAliveInterval); keepAliveInterval = null }
  }
}

// Idle animations — mouth + wave
onMounted(() => {
  speakInterval = setInterval(() => {
    if (!soundOn.value) {
      heroSpeaking.value = true
      setTimeout(() => { heroSpeaking.value = false }, 2500)
    }
  }, 8000)
  // Initial wave on page load
  heroWaving.value = true
  setTimeout(() => { heroWaving.value = false }, 4000)
  // Wave periodically
  waveInterval = setInterval(() => {
    if (!heroSpeaking.value && !soundOn.value) {
      heroWaving.value = true
      setTimeout(() => { heroWaving.value = false }, 3500)
    }
  }, 12000)
  // Initial idle mouth animation
  if (!soundOn.value) {
    setTimeout(() => { heroSpeaking.value = true }, 1500)
    setTimeout(() => { heroSpeaking.value = false }, 4000)
  }
  // Preload voices
  if (window.speechSynthesis) {
    window.speechSynthesis.getVoices()
    window.speechSynthesis.addEventListener('voiceschanged', () => {})
  }
})

// ─── Data ───
const agents = [
  { key: 'triage', icon: '🚨', nameKey: 'agent.triage', descKey: 'agent.triage.desc' },
  { key: 'diagnostician', icon: '🔬', nameKey: 'agent.diagnostician', descKey: 'agent.diagnostician.desc' },
  { key: 'researcher', icon: '📚', nameKey: 'agent.researcher', descKey: 'agent.researcher.desc' },
  { key: 'specialist', icon: '🏥', nameKey: 'agent.specialist', descKey: 'agent.specialist.desc' },
  { key: 'treatment', icon: '💊', nameKey: 'agent.treatment', descKey: 'agent.treatment.desc' },
  { key: 'safety', icon: '🛡️', nameKey: 'agent.safety', descKey: 'agent.safety.desc' },
  { key: 'empathy', icon: '💬', nameKey: 'agent.empathy', descKey: 'agent.empathy.desc' },
]

const features = [
  {
    titleKey: 'feature.voice.title', descKey: 'feature.voice.desc',
    iconBg: 'bg-blue-500/10', iconColor: 'text-blue-400',
    iconPath: 'M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z',
  },
  {
    titleKey: 'feature.clinical.title', descKey: 'feature.clinical.desc',
    iconBg: 'bg-purple-500/10', iconColor: 'text-purple-400',
    iconPath: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01',
  },
  {
    titleKey: 'feature.safety.title', descKey: 'feature.safety.desc',
    iconBg: 'bg-emerald-500/10', iconColor: 'text-emerald-400',
    iconPath: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z',
  },
]

function startConsultation() {
  const hasKey = localStorage.getItem('api_key_configured')
  router.push(hasKey ? '/consult' : '/setup')
}

function viewSampleReport() {
  const sampleData = {
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
    estimated_cost: 0.30,
  }
  localStorage.setItem('latest_diagnosis_result', JSON.stringify(sampleData))
  router.push('/dashboard')
}
</script>

<style scoped>
.font-headline {
  font-family: 'Silkscreen', 'Jost', 'Century Gothic', cursive;
}
.hero-avatar-float {
  animation: float 6s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
