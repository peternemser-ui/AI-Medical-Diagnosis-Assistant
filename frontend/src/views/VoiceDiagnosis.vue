<template>
  <div class="min-h-screen flex flex-col transition-colors duration-300 relative overflow-hidden surface-page">
    <!-- Subtle clinical background -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden" style="z-index: 0">
      <div class="absolute rounded-full blur-[100px]"
        :class="isDark ? 'opacity-20' : 'opacity-[0.08]'"
        style="width: 600px; height: 600px; top: -200px; right: -150px; background: radial-gradient(circle, #3b82f6, transparent)"></div>
      <div class="absolute rounded-full blur-[100px]"
        :class="isDark ? 'opacity-15' : 'opacity-[0.06]'"
        style="width: 500px; height: 500px; bottom: -100px; left: -150px; background: radial-gradient(circle, #10b981, transparent)"></div>
    </div>

    <!-- Skip to content link -->
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:px-4 focus:py-2 focus:bg-blue-600 focus:text-white focus:rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400">Skip to main content</a>

    <!-- Header -->
    <nav role="banner" aria-label="Main navigation" class="backdrop-blur-xl border-b py-3 px-4 sm:px-6 flex justify-between items-center transition-colors duration-300 sticky top-0" style="z-index: 100; background: var(--clinical-surface); border-color: var(--clinical-border)"
    >
      <!-- Left: Brand + Home link -->
      <div class="flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 flex-shrink-0">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
              <path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" />
            </svg>
          </div>
          <span class="text-base font-semibold hidden sm:inline transition-colors" :class="isDark ? 'text-white group-hover:text-blue-300' : 'text-slate-900 group-hover:text-blue-600'">{{ t('nav.brand') }}</span>
        </router-link>

        <!-- Home link -->
        <router-link to="/" class="hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-sm font-medium transition-all" :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z"/></svg>
          {{ t('nav.home') }}
        </router-link>

        <!-- Divider + Model Selector (desktop) -->
        <div class="hidden sm:flex items-center gap-2">
          <div class="w-px h-5" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>
          <!-- Model selector dropdown -->
          <div class="relative">
            <button @click="showModelPicker = !showModelPicker" class="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full border transition-colors cursor-pointer"
              :class="selectedModelInfo.free
                ? (isDark ? 'bg-orange-500/10 text-orange-400 border-orange-500/15 hover:bg-orange-500/20' : 'bg-orange-50 text-orange-600 border-orange-200 hover:bg-orange-100')
                : (isDark ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/15 hover:bg-emerald-500/20' : 'bg-emerald-50 text-emerald-600 border-emerald-200 hover:bg-emerald-100')
              ">
              <div class="w-1.5 h-1.5 rounded-full animate-pulse" :class="selectedModelInfo.free ? 'bg-orange-400' : 'bg-emerald-400'"></div>
              {{ selectedModelInfo.label }}
              <span class="opacity-60">{{ selectedModelInfo.price }}</span>
              <svg class="w-3 h-3 opacity-50 transition-transform" :class="showModelPicker ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
            </button>
            <!-- Dropdown -->
            <div v-if="showModelPicker" class="absolute top-full left-0 mt-1 w-72 rounded-xl border shadow-xl overflow-hidden" style="z-index: 9999"
              :class="isDark ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'">
              <div class="p-2 max-h-80 overflow-y-auto">
                <div v-for="model in modelPickerOptions" :key="model.id"
                  @click="selectModel(model.id)"
                  class="flex items-center justify-between gap-2 px-3 py-2 rounded-lg cursor-pointer transition-colors text-xs"
                  :class="[
                    modelPreference === model.id ? (isDark ? 'bg-blue-500/15 text-blue-300' : 'bg-blue-50 text-blue-700') : (isDark ? 'hover:bg-slate-700 text-slate-300' : 'hover:bg-slate-50 text-slate-700'),
                  ]">
                  <svg v-if="modelPreference === model.id" class="w-3.5 h-3.5 flex-shrink-0 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                  </svg>
                  <div v-else class="w-3.5 h-3.5 flex-shrink-0"></div>
                  <div class="flex-1 min-w-0">
                    <div class="font-medium flex items-center gap-1.5">
                      {{ model.name }}
                      <span v-if="model.badge" class="text-tiny px-1.5 py-0.5 rounded-full" :class="model.badgeClass">{{ model.badge }}</span>
                      <span v-if="!modelHasKey(model.id) && !model.free" class="text-micro px-1.5 py-0.5 rounded-full bg-red-500/15 text-red-400">{{ t('nav.noKey') }}</span>
                    </div>
                    <div class="text-detail mt-0.5 truncate" :class="!modelHasKey(model.id) && !model.free ? 'text-slate-600' : (isDark ? 'text-slate-500' : 'text-slate-400')">{{ model.desc }}</div>
                  </div>
                  <div class="text-detail font-mono flex-shrink-0 text-right" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    {{ model.price }}
                  </div>
                </div>
              </div>
              <div class="border-t px-3 py-2 text-detail" :class="isDark ? 'border-slate-700 text-slate-500' : 'border-slate-200 text-slate-400'">
                <div>{{ t('nav.pricesNote') }}</div>
                <div class="mt-1" :class="isDark ? 'text-slate-600' : 'text-slate-400'">Estimated API cost per diagnosis using your own key — no markup.</div>
                <div class="flex items-center gap-2 mt-1.5 flex-wrap">
                  <span class="flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full" :class="configuredKeys.anthropic ? 'bg-emerald-400' : 'bg-red-400'"></span>
                    Anthropic
                  </span>
                  <span class="flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full" :class="configuredKeys.openai ? 'bg-emerald-400' : 'bg-red-400'"></span>
                    OpenAI
                  </span>
                  <span class="flex items-center gap-1">
                    <span class="w-1.5 h-1.5 rounded-full" :class="configuredKeys.google ? 'bg-emerald-400' : 'bg-red-400'"></span>
                    Google
                  </span>
                </div>
              </div>
              <div class="border-t" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
                <router-link to="/setup"
                  @click.native="showModelPicker = false"
                  class="flex items-center gap-2 px-3 py-2.5 text-xs font-medium transition-colors"
                  :class="isDark ? 'text-blue-400 hover:bg-slate-700/50' : 'text-blue-600 hover:bg-blue-50'">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
                  {{ t('nav.configureApiKeys') }}
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right: Desktop toolbar (hidden on mobile) -->
      <div class="hidden sm:flex items-center gap-1">
        <button @click="handleStartOver" aria-label="New" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all" :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
          <span class="hidden lg:inline">{{ t('nav.new') }}</span>
        </button>
        <button @click="showHistory = true" aria-label="History" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all" :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <span class="hidden lg:inline">{{ t('nav.history') }}</span>
        </button>
        <router-link to="/reports" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all" :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          <span class="hidden lg:inline">{{ t('nav.reports') }}</span>
        </router-link>
        <router-link to="/medications" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all" :class="isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/></svg>
          <span class="hidden lg:inline">{{ t('nav.medications') }}</span>
        </router-link>
        <div class="w-px h-5 mx-0.5" :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>
        <ThemeLangControls />
        <button @click="goToApiSettings" class="p-2 rounded-lg transition-all" :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
        </button>
        <!-- User menu -->
        <div class="relative" ref="userMenuRef">
          <button v-if="isLoggedIn" @click="showUserMenu = !showUserMenu" class="flex items-center gap-1.5 px-2 py-1.5 rounded-lg transition-all" :class="isDark ? 'hover:bg-slate-700/60 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
            <div class="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-detail font-bold text-white">
              {{ userInitials }}
            </div>
            <span class="hidden lg:inline text-sm font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ userName }}</span>
            <svg class="w-3 h-3 hidden lg:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <router-link v-else to="/profile" class="p-2 rounded-lg transition-all" :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          </router-link>
          <Transition enter-active-class="transition duration-150 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
            <div v-if="showUserMenu && isLoggedIn" class="absolute right-0 top-full mt-1 w-48 rounded-lg shadow-xl border z-50 overflow-hidden py-1" :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-slate-200'">
              <div class="px-3 py-2 border-b" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
                <div class="text-xs font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ userName }}</div>
                <div class="text-detail" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ userEmail || 'No email set' }}</div>
              </div>
              <router-link to="/profile" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                {{ t('nav.profile') }}
              </router-link>
              <router-link to="/settings" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                {{ t('nav.settings2') }}
              </router-link>
              <router-link to="/reports" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                {{ t('nav.reports') }}
              </router-link>
              <router-link to="/setup" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/></svg>
                {{ t('nav.apiKeys') }}
              </router-link>
              <div class="border-t my-1" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'"></div>
              <button @click="handleLogout" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors w-full text-left" :class="isDark ? 'text-red-400 hover:bg-slate-800' : 'text-red-500 hover:bg-red-50'">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
                {{ t('nav.logOut') }}
              </button>
            </div>
          </Transition>
        </div>
      </div>

      <!-- Mobile: Avatar toggle + hamburger -->
      <div class="flex sm:hidden items-center gap-1">
        <button @click="showMobileMenu = !showMobileMenu" class="p-2 rounded-lg" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        </button>
      </div>

      <!-- Mobile dropdown menu -->
      <div v-if="showMobileMenu" class="absolute top-full left-0 right-0 border-b shadow-lg sm:hidden" style="z-index: 9999"
        :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
        <div class="p-3 space-y-1">
          <button @click="handleStartOver; showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
            {{ t('nav.newConsultation') }}
          </button>
          <button @click="showHistory = true; showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ t('nav.history') }}
          </button>
          <router-link to="/reports" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            {{ t('nav.reports') }}
          </router-link>
          <div class="border-t my-1" :class="isDark ? 'border-slate-800' : 'border-slate-100'"></div>
          <button @click="goToApiSettings; showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            {{ t('nav.settings2') }}
          </button>
          <template v-if="isLoggedIn">
            <div class="flex items-center gap-3 px-3 py-2.5">
              <div class="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-detail font-bold text-white">{{ userInitials }}</div>
              <div>
                <div class="text-sm font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ userName }}</div>
                <div class="text-detail" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ userEmail || '' }}</div>
              </div>
            </div>
            <router-link to="/profile" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              {{ t('nav.profile') }}
            </router-link>
            <button @click="handleLogout; showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-red-400 hover:bg-slate-800' : 'text-red-500 hover:bg-red-50'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
              {{ t('nav.logOut') }}
            </button>
          </template>
          <router-link v-else to="/profile" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ t('nav.logIn') }}
          </router-link>
          <div class="border-t my-1" :class="isDark ? 'border-slate-800' : 'border-slate-100'"></div>
          <div class="px-3 py-1">
            <ThemeLangControls />
          </div>
        </div>
      </div>
    </nav>

    <!-- Agent Pipeline - shown during diagnosis -->
    <AgentPipelineIndicator
      v-if="conversationState === 'diagnosing'"
      :active-agent="activeAgent"
      :completed-agents="completedAgents"
      :agent-timings="agentTimings"
      :total-time="diagnosisElapsed"
    />

    <!-- Agent Status Board -->
    <AgentStatusBoard
      v-if="conversationState === 'diagnosing'"
      :active-agent="activeAgent"
      :completed-agents="completedAgents"
      :agent-timings="agentTimings"
      :agent-findings="agentFindings"
      :errors="agentErrors"
    />

    <!-- Progress Indicator (horizontal, mobile only) -->
    <ProgressIndicator
      v-if="(conversationState === 'gathering' || conversationState === 'pa_interview' || conversationState === 'followup' || conversationState === 'awaiting-confirmation')"
      :visible="true"
      :progress="progressPercentage"
      :current-step="currentStep"
      :steps="progressSteps"
      :title="getProgressTitle()"
      :message="getProgressMessage()"
      class="lg:hidden"
    />

    <!-- ══════ AVATAR MODE ══════ -->
    <div v-if="avatarMode" id="main-content" role="main" class="flex-1 flex flex-col min-h-0 pb-20 relative overflow-hidden">
      <!-- Avatar area — centered, large -->
      <div class="flex-[1] flex flex-col items-center justify-center relative z-10">
        <div class="relative cursor-pointer" @click="showAvatarCustomizer = true" title="Click to customize">

          <!-- Cat Doctor Avatar -->
          <div v-if="(doctorAvatar.characterType || 'bunny') === 'cat'" class="w-48 h-52 sm:w-72 sm:h-80">
            <svg viewBox="0 0 300 320" class="w-full h-full" style="filter: drop-shadow(0 8px 20px rgba(0,0,0,0.15))">
              <!-- Pointed ears -->
              <polygon points="90,130 70,30 130,100" fill="#f5a623" stroke="#e8941e" stroke-width="2"/>
              <polygon points="210,130 230,30 170,100" fill="#f5a623" stroke="#e8941e" stroke-width="2"/>
              <polygon points="95,120 80,50 125,105" fill="#fce4b8"/>
              <polygon points="205,120 220,50 175,105" fill="#fce4b8"/>
              <!-- Head -->
              <ellipse cx="150" cy="155" rx="75" ry="70" fill="#f5a623"/>
              <ellipse cx="150" cy="160" rx="68" ry="60" fill="#f9bc4e" opacity="0.6"/>
              <!-- Eyes -->
              <ellipse cx="120" cy="145" rx="12" ry="14" fill="white"/>
              <ellipse cx="180" cy="145" rx="12" ry="14" fill="white"/>
              <circle cx="122" cy="145" r="8" fill="#4a4a4a"/>
              <circle cx="182" cy="145" r="8" fill="#4a4a4a"/>
              <circle cx="124" cy="143" r="3" fill="white" opacity="0.9"/>
              <circle cx="184" cy="143" r="3" fill="white" opacity="0.9"/>
              <!-- Nose -->
              <ellipse cx="150" cy="168" rx="6" ry="4.5" fill="#e87da0"/>
              <!-- Whiskers -->
              <line x1="75" y1="160" x2="120" y2="165" stroke="#d49a3e" stroke-width="1.5"/>
              <line x1="75" y1="172" x2="120" y2="172" stroke="#d49a3e" stroke-width="1.5"/>
              <line x1="75" y1="184" x2="120" y2="179" stroke="#d49a3e" stroke-width="1.5"/>
              <line x1="180" y1="165" x2="225" y2="160" stroke="#d49a3e" stroke-width="1.5"/>
              <line x1="180" y1="172" x2="225" y2="172" stroke="#d49a3e" stroke-width="1.5"/>
              <line x1="180" y1="179" x2="225" y2="184" stroke="#d49a3e" stroke-width="1.5"/>
              <!-- Mouth (animated) -->
              <g :class="isSpeakingAnimating ? 'cat-mouth-talking' : ''">
                <path v-if="!isSpeakingAnimating" d="M140 178 Q150 186 160 178" fill="none" stroke="#c0783a" stroke-width="2" stroke-linecap="round"/>
                <g v-if="isSpeakingAnimating">
                  <ellipse cx="150" cy="182" rx="10" ry="8" fill="#c0484a" class="cat-jaw"/>
                  <path d="M140 178 Q150 175 160 178" fill="none" stroke="#c0783a" stroke-width="2" stroke-linecap="round"/>
                  <ellipse cx="150" cy="188" rx="5" ry="4" fill="#e87d7d"/>
                </g>
              </g>
              <!-- Body / scrubs -->
              <path d="M95 220 Q95 205 115 198 L130 210 Q150 218 170 210 L185 198 Q205 205 205 220 L210 300 L90 300 Z" :fill="doctorAvatar.bunnyColor || '#4fc3f7'" stroke="#333" stroke-width="2.5"/>
              <path d="M125 210 L150 222 L175 210" fill="white" stroke="#333" stroke-width="1.5"/>
              <!-- Stethoscope -->
              <path d="M140 215 Q135 235 142 248" fill="none" stroke="#4a90d9" stroke-width="2" stroke-linecap="round"/>
              <circle cx="142" cy="250" r="4.5" fill="none" stroke="#4a90d9" stroke-width="1.8"/>
              <!-- Paws -->
              <circle cx="88" cy="245" r="10" fill="#f5a623" stroke="#333" stroke-width="2"/>
              <circle cx="212" cy="245" r="10" fill="#f5a623" stroke="#333" stroke-width="2"/>
              <!-- Feet -->
              <ellipse cx="125" cy="305" rx="16" ry="10" fill="#f5a623" stroke="#333" stroke-width="2"/>
              <ellipse cx="175" cy="305" rx="16" ry="10" fill="#f5a623" stroke="#333" stroke-width="2"/>
              <!-- Name tag -->
              <rect x="128" y="260" width="44" height="14" rx="3" fill="white" stroke="#b8d8e8" stroke-width="1"/>
              <text x="150" y="271" text-anchor="middle" fill="#4a7fa5" font-size="7" font-weight="bold" font-family="system-ui">DR. WHISKERS</text>
            </svg>
          </div>
          <!-- Dog Doctor Avatar -->
          <div v-else-if="(doctorAvatar.characterType || 'bunny') === 'dog'" class="w-48 h-52 sm:w-72 sm:h-80">
            <svg viewBox="0 0 300 320" class="w-full h-full" style="filter: drop-shadow(0 8px 20px rgba(0,0,0,0.15))">
              <!-- Floppy ears -->
              <ellipse cx="80" cy="130" rx="22" ry="40" fill="#8B5E3C" transform="rotate(-15 80 130)"/>
              <ellipse cx="220" cy="130" rx="22" ry="40" fill="#8B5E3C" transform="rotate(15 220 130)"/>
              <ellipse cx="82" cy="132" rx="14" ry="28" fill="#c49a6c" transform="rotate(-15 82 132)"/>
              <ellipse cx="218" cy="132" rx="14" ry="28" fill="#c49a6c" transform="rotate(15 218 132)"/>
              <!-- Head -->
              <ellipse cx="150" cy="150" rx="72" ry="68" fill="#c49a6c"/>
              <ellipse cx="150" cy="155" rx="65" ry="55" fill="#d4aa7c" opacity="0.5"/>
              <!-- Muzzle -->
              <ellipse cx="150" cy="175" rx="35" ry="25" fill="#e8c8a0"/>
              <!-- Eyes -->
              <ellipse cx="120" cy="140" rx="11" ry="12" fill="white" stroke="#b08860" stroke-width="0.5"/>
              <ellipse cx="180" cy="140" rx="11" ry="12" fill="white" stroke="#b08860" stroke-width="0.5"/>
              <circle cx="122" cy="140" r="7" fill="#3d2b1f"/>
              <circle cx="182" cy="140" r="7" fill="#3d2b1f"/>
              <circle cx="124" cy="138" r="2.5" fill="white" opacity="0.9"/>
              <circle cx="184" cy="138" r="2.5" fill="white" opacity="0.9"/>
              <!-- Eyebrows -->
              <path d="M110 130 Q120 125 130 131" fill="none" stroke="#7a5a3a" stroke-width="2.5" stroke-linecap="round"/>
              <path d="M170 131 Q180 125 190 130" fill="none" stroke="#7a5a3a" stroke-width="2.5" stroke-linecap="round"/>
              <!-- Nose -->
              <ellipse cx="150" cy="165" rx="10" ry="8" fill="#3d2b1f"/>
              <!-- Mouth (animated) -->
              <g :class="isSpeakingAnimating ? 'dog-mouth-talking' : ''">
                <path v-if="!isSpeakingAnimating" d="M138 178 Q150 188 162 178" fill="none" stroke="#7a5a3a" stroke-width="2" stroke-linecap="round"/>
                <path v-if="!isSpeakingAnimating" d="M146 182 Q150 194 154 182" fill="#e87d7d" stroke="#d06060" stroke-width="0.5"/>
                <g v-if="isSpeakingAnimating">
                  <ellipse cx="150" cy="184" rx="14" ry="10" fill="#5a3020" class="dog-jaw"/>
                  <ellipse cx="150" cy="180" rx="11" ry="5" fill="#c0584a"/>
                  <path d="M146 186 Q150 196 154 186" fill="#e87d7d"/>
                  <path d="M138 178 Q150 174 162 178" fill="none" stroke="#7a5a3a" stroke-width="2" stroke-linecap="round"/>
                </g>
              </g>
              <!-- Body / scrubs -->
              <path d="M95 220 Q95 205 115 198 L130 210 Q150 218 170 210 L185 198 Q205 205 205 220 L210 300 L90 300 Z" :fill="doctorAvatar.bunnyColor || '#81c784'" stroke="#333" stroke-width="2.5"/>
              <path d="M125 210 L150 222 L175 210" fill="white" stroke="#333" stroke-width="1.5"/>
              <!-- Stethoscope -->
              <path d="M140 215 Q135 235 142 248" fill="none" stroke="#4a90d9" stroke-width="2" stroke-linecap="round"/>
              <circle cx="142" cy="250" r="4.5" fill="none" stroke="#4a90d9" stroke-width="1.8"/>
              <!-- Paws -->
              <circle cx="88" cy="245" r="10" fill="#c49a6c" stroke="#333" stroke-width="2"/>
              <circle cx="212" cy="245" r="10" fill="#c49a6c" stroke="#333" stroke-width="2"/>
              <!-- Feet -->
              <ellipse cx="125" cy="305" rx="16" ry="10" fill="#c49a6c" stroke="#333" stroke-width="2"/>
              <ellipse cx="175" cy="305" rx="16" ry="10" fill="#c49a6c" stroke="#333" stroke-width="2"/>
              <!-- Name tag -->
              <rect x="128" y="260" width="44" height="14" rx="3" fill="white" stroke="#b8d8e8" stroke-width="1"/>
              <text x="150" y="271" text-anchor="middle" fill="#4a7fa5" font-size="7.5" font-weight="bold" font-family="system-ui">DR. BUDDY</text>
            </svg>
          </div>
          <div v-else-if="(doctorAvatar.characterType || 'bunny') === 'human'" class="w-72 h-80 flex items-center justify-center">
            <DoctorAvatar :avatar="doctorAvatar" :speaking="isSpeakingAnimating" :size="avatarSize" :show-name="false" />
          </div>

          <!-- Bunny Doctor Avatar (robotic style matching homepage) -->
          <div v-else class="w-52 h-64 sm:w-[18rem] sm:h-[23rem] lg:w-[20rem] lg:h-[26rem]">
            <svg viewBox="-10 -30 260 380" class="w-full h-full" style="filter: drop-shadow(0 12px 32px rgba(0,0,0,0.15))">
              <defs>
                <linearGradient id="cEarGlow" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7dd3fc" stop-opacity="0.3"/><stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/></linearGradient>
                <linearGradient id="cBodyGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#a78bfa"/><stop offset="100%" stop-color="#7c3aed"/></linearGradient>
                <filter id="cGlow"><feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
              </defs>
              <!-- Left ear -->
              <g><ellipse cx="120" cy="55" rx="19" ry="65" fill="white" stroke="#64748b" stroke-width="2.5" transform="rotate(-8 120 110)"/>
              <ellipse cx="120" cy="50" rx="10" ry="46" fill="url(#cEarGlow)" transform="rotate(-8 120 110)"/></g>
              <!-- Right ear -->
              <g><ellipse cx="160" cy="50" rx="19" ry="65" fill="white" stroke="#64748b" stroke-width="2.5" transform="rotate(8 160 110)"/>
              <ellipse cx="160" cy="45" rx="10" ry="46" fill="url(#cEarGlow)" transform="rotate(8 160 110)"/></g>
              <!-- Antenna -->
              <line x1="172" y1="30" x2="185" y2="5" stroke="#38bdf8" stroke-width="1.5" opacity="0.7"/>
              <circle cx="185" cy="5" r="4" fill="#0ea5e9" opacity="0.9" filter="url(#cGlow)">
                <animate attributeName="r" values="3;5;3" dur="1.2s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0.6;1;0.6" dur="1.2s" repeatCount="indefinite"/>
              </circle>
              <!-- Head -->
              <ellipse cx="140" cy="150" rx="65" ry="60" fill="white" stroke="#64748b" stroke-width="3"/>
              <ellipse cx="140" cy="148" rx="55" ry="48" fill="none" stroke="#e2e8f0" stroke-width="0.8" stroke-dasharray="4 3" opacity="0.5"/>
              <!-- Eyes (robotic rectangles) -->
              <rect x="100" y="126" width="32" height="24" rx="12" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="1.5"/>
              <circle cx="116" cy="138" r="7" fill="#3b82f6" filter="url(#cGlow)"/>
              <circle cx="114" cy="136" r="2.5" fill="white" opacity="0.85"/>
              <rect x="148" y="126" width="32" height="24" rx="12" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="1.5"/>
              <circle cx="164" cy="138" r="7" fill="#3b82f6" filter="url(#cGlow)"/>
              <circle cx="162" cy="136" r="2.5" fill="white" opacity="0.85"/>
              <!-- Nose -->
              <polygon points="140,155 136,161 144,161" fill="#94a3b8" stroke="#64748b" stroke-width="1"/>
              <circle cx="140" cy="159" r="1.5" fill="#3b82f6" opacity="0.6"><animate attributeName="opacity" values="0.4;0.9;0.4" dur="2s" repeatCount="indefinite"/></circle>
              <!-- Whiskers -->
              <line x1="88" y1="152" x2="113" y2="156" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
              <line x1="88" y1="162" x2="113" y2="161" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
              <line x1="167" y1="156" x2="192" y2="152" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
              <line x1="167" y1="161" x2="192" y2="162" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
              <!-- Mouth — equalizer when speaking, idle bar otherwise -->
              <g v-if="isSpeakingAnimating">
                <rect x="122" y="167" width="36" height="8" rx="4" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="0.8"/>
                <rect x="125" y="172" width="3" height="0" rx="0.5" fill="#3b82f6" opacity="0.8"><animate attributeName="height" values="1;5;2;4;1" dur="0.4s" repeatCount="indefinite"/><animate attributeName="y" values="172;168;171;169;172" dur="0.4s" repeatCount="indefinite"/></rect>
                <rect x="130" y="172" width="3" height="0" rx="0.5" fill="#38bdf8" opacity="0.8"><animate attributeName="height" values="2;5;1;5;2" dur="0.35s" repeatCount="indefinite"/><animate attributeName="y" values="171;168;172;168;171" dur="0.35s" repeatCount="indefinite"/></rect>
                <rect x="135" y="172" width="3" height="0" rx="0.5" fill="#0ea5e9" opacity="0.9"><animate attributeName="height" values="3;6;2;6;3" dur="0.3s" repeatCount="indefinite"/><animate attributeName="y" values="170;167;171;167;170" dur="0.3s" repeatCount="indefinite"/></rect>
                <rect x="140" y="172" width="3" height="0" rx="0.5" fill="#38bdf8" opacity="0.8"><animate attributeName="height" values="1;5;3;5;1" dur="0.38s" repeatCount="indefinite"/><animate attributeName="y" values="172;168;170;168;172" dur="0.38s" repeatCount="indefinite"/></rect>
                <rect x="145" y="172" width="3" height="0" rx="0.5" fill="#3b82f6" opacity="0.8"><animate attributeName="height" values="4;1;5;2;4" dur="0.32s" repeatCount="indefinite"/><animate attributeName="y" values="169;172;168;171;169" dur="0.32s" repeatCount="indefinite"/></rect>
                <rect x="150" y="172" width="3" height="0" rx="0.5" fill="#38bdf8" opacity="0.7"><animate attributeName="height" values="2;5;1;4;2" dur="0.36s" repeatCount="indefinite"/><animate attributeName="y" values="171;168;172;169;171" dur="0.36s" repeatCount="indefinite"/></rect>
              </g>
              <g v-else>
                <rect x="122" y="167" width="36" height="8" rx="4" :fill="isDark ? '#0f172a' : '#e2e8f0'" stroke="#94a3b8" stroke-width="0.8"/>
                <rect x="128" y="170" width="24" height="2" rx="1" fill="#3b82f6" opacity="0.4"><animate attributeName="opacity" values="0.3;0.5;0.3" dur="3s" repeatCount="indefinite"/></rect>
              </g>
              <!-- Body / scrubs -->
              <path d="M90 200 Q90 185 105 178 L120 195 Q140 205 160 195 L175 178 Q190 185 190 200 L195 290 L85 290 Z" fill="url(#cBodyGrad)" stroke="#64748b" stroke-width="2.5"/>
              <path d="M110 195 L140 210 L170 195" fill="white" stroke="#94a3b8" stroke-width="1.5"/>
              <!-- Heartbeat line on scrubs -->
              <g opacity="0.5">
                <line x1="105" y1="225" x2="175" y2="225" stroke="#38bdf8" stroke-width="0.6" opacity="0.2"/>
                <polyline fill="none" stroke="#38bdf8" stroke-width="1" stroke-linecap="round" points="105,225 120,225 125,225 128,215 131,235 134,220 137,230 140,225 175,225" opacity="0.4"/>
              </g>
              <!-- Sleeves + hands -->
              <ellipse cx="88" cy="215" rx="15" ry="12" fill="url(#cBodyGrad)" stroke="#64748b" stroke-width="2.5"/>
              <ellipse cx="192" cy="215" rx="15" ry="12" fill="url(#cBodyGrad)" stroke="#64748b" stroke-width="2.5"/>
              <circle cx="80" cy="230" r="10" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
              <circle cx="200" cy="230" r="10" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
              <!-- Feet -->
              <ellipse cx="115" cy="298" rx="18" ry="12" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
              <ellipse cx="165" cy="298" rx="18" ry="12" fill="white" stroke="#94a3b8" stroke-width="2.5"/>
              <!-- Name tag -->
              <rect x="118" y="250" width="44" height="14" rx="3" fill="white" stroke="#94a3b8" stroke-width="0.8"/>
              <text x="140" y="261" text-anchor="middle" fill="#3b82f6" font-size="7.5" font-weight="bold" font-family="system-ui, sans-serif">DR. HOPPS</text>
            </svg>
          </div>
        </div>
        <div class="mt-1 text-center">
          <div class="text-base sm:text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ doctorAvatar.name || 'Dr. Hopps' }}</div>
          <div class="text-caption sm:text-xs" :class="isDark ? 'text-slate-400' : 'text-slate-600'">{{ t('voice.physicianAssistant') }}</div>
          <div class="text-detail mt-1 hidden sm:block" :class="isDark ? 'text-slate-600' : 'text-slate-400'">{{ t('voice.clickToCustomize') }}</div>
        </div>
      </div>

      <!-- Subtitle area -->
      <div class="flex-[1] flex flex-col justify-start items-center relative z-10 px-4">
        <div v-if="lastUserText" class="mb-2 text-center">
          <span class="inline-block text-sm px-4 py-1.5 rounded-full border" :class="isDark ? 'bg-blue-600/20 text-blue-200 border-blue-500/15' : 'bg-blue-600 text-white border-blue-700'">{{ lastUserText }}</span>
        </div>
        <div v-if="lastAssistantText" class="w-full max-w-3xl rounded-xl px-6 py-5 text-center border shadow-2xl" :class="isDark ? 'bg-black/60 border-slate-700/20' : 'bg-slate-900 border-slate-800'">
          <p class="text-white text-lg sm:text-xl leading-relaxed font-medium" v-html="formatSubtitle(lastAssistantText)"></p>
        </div>
        <!-- Toggle removed — use nav button instead -->
      </div>
    </div>

    <!-- ══════ CHAT MODE ══════ -->
    <div v-else id="main-content" role="main" class="flex-1 flex min-h-0 pb-20">
      <!-- Vertical step sidebar (desktop only, visible during interview) — fixed position -->
      <aside
        v-if="showStepSidebar"
        class="hidden lg:flex flex-col w-56 flex-shrink-0 fixed top-14 left-0 bottom-20 overflow-y-auto pt-6 pb-6 pl-4 pr-3 ml-4 z-30"
        :class="isDark ? 'border-slate-800/60 bg-slate-900/30' : 'border-gray-200 bg-gray-50/50'"
        aria-label="Interview progress steps"
      >
        <!-- Progress percentage -->
        <div class="mb-4 px-2">
          <div class="text-detail font-bold uppercase tracking-wider mb-1.5" :class="isDark ? 'text-slate-500' : 'text-gray-400'">{{ t('voice.progress') }}</div>
          <div class="flex items-center gap-2">
            <div class="flex-1 h-1.5 rounded-full overflow-hidden" :class="isDark ? 'bg-slate-800' : 'bg-gray-200'">
              <div class="h-full rounded-full transition-all duration-700 ease-out" :class="progressPercentage >= 80 ? 'bg-emerald-500' : 'bg-blue-500'" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <span class="text-xs font-bold tabular-nums" :class="progressPercentage >= 80 ? 'text-emerald-400' : (isDark ? 'text-slate-400' : 'text-gray-500')">{{ Math.round(progressPercentage) }}%</span>
          </div>
        </div>

        <!-- Vertical steps -->
        <div class="space-y-0.5">
          <div v-for="(step, index) in progressSteps" :key="index" class="relative flex items-start gap-2.5 group">
            <!-- Vertical connector line -->
            <div class="flex flex-col items-center flex-shrink-0" style="width: 20px;">
              <!-- Circle/check -->
              <div class="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 transition-all duration-300 z-10"
                :class="currentStep > index
                  ? 'bg-emerald-500 text-white shadow-sm shadow-emerald-500/30'
                  : currentStep === index
                    ? (isDark ? 'bg-blue-500 text-white shadow-md shadow-blue-500/40 ring-2 ring-blue-500/20' : 'bg-blue-500 text-white shadow-md shadow-blue-500/30 ring-2 ring-blue-200')
                    : (isDark ? 'bg-slate-800 border border-slate-700 text-slate-600' : 'bg-gray-200 border border-gray-300 text-gray-400')">
                <svg v-if="currentStep > index" class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                </svg>
                <div v-else-if="currentStep === index" class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></div>
                <span v-else class="text-micro font-bold">{{ index + 1 }}</span>
              </div>
              <!-- Line -->
              <div v-if="index < progressSteps.length - 1" class="w-0.5 flex-1 min-h-[20px] transition-colors duration-300"
                :class="currentStep > index ? 'bg-emerald-500/50' : (isDark ? 'bg-slate-800' : 'bg-gray-200')"></div>
            </div>
            <!-- Label -->
            <div class="py-0.5 pb-3 min-w-0">
              <span class="text-xs font-medium leading-tight transition-colors duration-300"
                :class="currentStep > index
                  ? (isDark ? 'text-emerald-400' : 'text-emerald-600')
                  : currentStep === index
                    ? (isDark ? 'text-blue-300 font-semibold' : 'text-blue-600 font-semibold')
                    : (isDark ? 'text-slate-500' : 'text-gray-400')">
                {{ step }}
              </span>
            </div>
          </div>
        </div>
      </aside>

      <!-- Chat content -->
      <div class="flex-1 flex flex-col min-w-0" :class="showStepSidebar ? 'lg:ml-60' : ''">
        <div class="flex-1 overflow-y-auto" ref="chatScrollRef">
          <div class="max-w-4xl mx-auto px-2">
            <ChatArea
              ref="chatAreaRef"
              :messages="chatMessages"
              :is-typing="showTyping"
              :auto-scroll="autoScroll"
              :sound-enabled="soundEnabled"
              :pa-mode="conversationState === 'gathering' || conversationState === 'pa_interview'"
              :pa-character="doctorAvatar.characterType || 'bunny'"
              :specialist-mode="conversationState === 'specialist_handoff'"
              :active-specialist="activeSpecialist"
              @followup-selected="handleQuickQuestion"
              @replay-message="speakMessage"
              @toggle-avatar="avatarMode = true; localStorage.setItem('avatar_mode', 'true')"
            />
            <!-- Specialist Handoff Transition Card -->
            <HandoffTransitionCard
              v-if="showHandoffTransition && activeSpecialist"
              :pa-name="paAvatarName"
              :pa-character="doctorAvatar.characterType || 'bunny'"
              :specialist="activeSpecialist"
              :specialty="paRouting?.specialties?.[0] || 'general_medicine'"
              :reason="paRouting?.patient_summary || 'Based on clinical assessment'"
              :visible="showHandoffTransition"
            />
            <!-- Live Diagnosis View — shows during agent analysis -->
            <LiveDiagnosisView
              v-if="conversationState === 'diagnosing' && liveAgentResults.length > 0"
              :results="liveAgentResults"
              :active-agent="activeAgent"
              :completed-agents="completedAgents"
              :elapsed="diagnosisElapsed"
            />
          </div>
        </div>

        <!-- Symptom chips -->
        <SymptomChips
          v-if="conversationState === 'gathering' && questionnaire.currentQuestionIndex <= 2"
          :visible="true"
          class="px-3 py-2 max-w-4xl mx-auto w-full"
          @select="handleQuickQuestion"
        />

        <!-- Skip to Diagnosis button (appears after 4+ PA exchanges) -->
        <div v-if="conversationState === 'pa_interview' && paExchangeCount >= 4 && !isLoading"
          class="flex justify-center px-3 py-2">
          <button
            @click="skipToDiagnosis"
          class="inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-medium border transition-all shadow-sm"
          :class="isDark
            ? 'bg-emerald-500/15 border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/25'
            : 'bg-emerald-50 border-emerald-300 text-emerald-700 hover:bg-emerald-100'"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
            {{ t('voice.skipToDiagnosis') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Input Controls - fixed at bottom -->
    <div class="fixed bottom-0 left-0 right-0 z-50" style="padding-bottom: env(safe-area-inset-bottom, 0px)">
      <InputControls
        ref="inputControlsRef"
        :disabled="isLoading"
        :is-processing="isLoading"
        :is-speaking="isTTSSpeaking"
        :voice-enabled="voiceEnabled"
        :sound-enabled="soundEnabled"
        :avatar-mode="avatarMode"
        :quick-actions="getQuickActions()"
        @send-message="handleSendMessage"
        @start-recording="startVoiceRecording"
        @stop-recording="stopVoiceRecording"
        @voice-input="handleVoiceResult"
        @voice-toggle="toggleVoiceEnabled"
        @sound-toggle="soundEnabled = !soundEnabled"
        @avatar-toggle="avatarMode = !avatarMode; localStorage.setItem('avatar_mode', String(avatarMode))"
        @open-voice-settings="showAvatarCustomizer = true"
        @open-camera="showCameraOverlay = true"
      />
    </div>

    <!-- Avatar Customizer Modal -->
    <AvatarCustomizer
      v-if="showAvatarCustomizer"
      :current-avatar="doctorAvatar"
      @close="showAvatarCustomizer = false"
      @save="saveDoctorAvatar"
    />

    <!-- Camera Capture Overlay -->
    <div v-if="showCameraOverlay" class="fixed inset-0 z-[9999] bg-black">
      <CameraCapture
        mode="general"
        :show-guide="false"
        :quality="0.92"
        @capture="handleCameraCapture"
        @close="showCameraOverlay = false"
        @error="handleCameraError"
      />
    </div>

    <!-- Image Description Modal -->
    <ImageDescriptionModal
      :visible="showImageDescriptionModal"
      :image-url="pendingImageUrl"
      @close="closeImageDescriptionModal"
      @submit="handleImageDescriptionSubmit"
    />

    <!-- Input controls are fixed at bottom above -->

    <!-- Error Message -->
    <ErrorMessage 
      :visible="!!error"
      :message="error || ''"
      :show-retry="true"
      @close="clearError"
      @retry="clearError"
    />
    
    <!-- Help Modal -->
    <HelpModal v-if="showHelp" @close="showHelp = false" />
    
    <!-- Settings Panel -->
    <SettingsPanel 
      v-if="showSettings" 
      :visible="showSettings"
      :initial-settings="{ voiceInput: voiceEnabled, autoScroll: autoScroll, soundEffects: soundEnabled }"
      @close="showSettings = false"
      @settings-changed="handleSettingsChange"
      @clear-conversation="handleStartOver"
    />

    <!-- History Drawer -->
    <HistoryDrawer
      v-model="showHistory"
      @view-session="handleViewHistorySession"
    />

    <!-- Session Timeout Warning Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="sessionWarningVisible" class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div class="rounded-2xl shadow-2xl p-6 max-w-sm mx-4 text-center border"
            :class="isDark ? 'bg-slate-800 border-slate-700 text-white' : 'bg-white border-slate-200 text-slate-900'">
            <div class="w-14 h-14 rounded-full mx-auto mb-4 flex items-center justify-center"
              :class="isDark ? 'bg-amber-500/20' : 'bg-amber-100'">
              <svg class="w-7 h-7 text-amber-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M12 2a10 10 0 100 20 10 10 0 000-20z"/>
              </svg>
            </div>
            <h3 class="text-lg font-semibold mb-2">Session Expiring Soon</h3>
            <p class="text-sm mb-5" :class="isDark ? 'text-slate-300' : 'text-slate-600'">
              Your session will expire in about 2 minutes due to inactivity. Move your mouse, press a key, or click below to stay logged in.
            </p>
            <button @click="sessionWarningVisible = false"
              class="px-5 py-2.5 rounded-xl text-sm font-medium transition-colors bg-blue-600 hover:bg-blue-700 text-white">
              Stay Logged In
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Onboarding Tour -->
    <OnboardingTour
      :visible="showOnboarding"
      @close="showOnboarding = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import DOMPurify from 'dompurify'
import { diagnose, diagnoseStream, followup, generateQuestion, interview, healthCheck, ApiError } from '@/services/api.js'
import { getProfile } from '@/services/userService.js'

// Import core components
import ChatArea from '@/components/ChatArea.vue'
import LiveDiagnosisView from '@/components/LiveDiagnosisView.vue'
import InputControls from '@/components/InputControls.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import AgentPipelineIndicator from '@/components/AgentPipelineIndicator.vue'
import AgentStatusBoard from '@/components/AgentStatusBoard.vue'
import QuickActions from '@/components/QuickActions.vue'
import HelpModal from '@/components/HelpModal.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'
import DoctorAvatar from '@/components/DoctorAvatar.vue'
import AvatarCustomizer from '@/components/AvatarCustomizer.vue'
import HistoryDrawer from '@/components/HistoryDrawer.vue'
import SymptomChips from '@/components/SymptomChips.vue'
import ThemeLangControls from '@/components/ThemeLangControls.vue'
import OnboardingTour from '@/components/OnboardingTour.vue'
import ImageDescriptionModal from '@/components/ImageDescriptionModal.vue'
import CameraCapture from '@/components/CameraCapture.vue'
import HandoffTransitionCard from '@/components/HandoffTransitionCard.vue'
import { getSpecialist } from '@/data/specialistDoctors.js'
import { saveSession } from '@/services/historyService.js'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'
import { useUser } from '@/composables/useUser.js'
import { useToast } from '@/composables/useToast.js'
import { useSessionTimeout } from '@/composables/useSessionTimeout.js'

const { isDark } = useTheme()
const { t, lang } = useI18n()
const toast = useToast()
const { profile: userProfile, isLoggedIn, logout: doLogout } = useUser()

const userName = computed(() => userProfile.value?.name || '')
const userEmail = computed(() => userProfile.value?.email || '')
const userInitials = computed(() => {
  const name = userName.value
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  return parts.length >= 2
    ? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
    : name.slice(0, 2).toUpperCase()
})
const showUserMenu = ref(false)
const userMenuRef = ref(null)

function handleLogout() {
  doLogout()
  showUserMenu.value = false
  router.push('/')
}

function calculateAge(dob) {
  if (!dob) return null
  const birth = new Date(dob)
  if (isNaN(birth)) return null
  const now = new Date()
  let age = now.getFullYear() - birth.getFullYear()
  if (now.getMonth() < birth.getMonth() || (now.getMonth() === birth.getMonth() && now.getDate() < birth.getDate())) age--
  return age > 0 && age < 150 ? age : null
}

// Close user menu on outside click
function onDocClickUserMenu(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    showUserMenu.value = false
  }
}
const { startSessionTimer, stopTimer: stopSessionTimer, isWarningVisible: sessionWarningVisible } = useSessionTimeout()

// When language changes mid-conversation, update the greeting if it's the only message
watch(lang, () => {
  if (chatMessages.value.length === 1 && chatMessages.value[0].sender === 'assistant' && conversationState.value === 'gathering' && questionnaire.value.currentQuestionIndex === 0) {
    chatMessages.value[0].text = t('chat.greeting')
    chatMessages.value = [...chatMessages.value]
  }
  // Update speech recognition language when UI language changes
  if (speechRecognition.value) {
    speechRecognition.value.lang = getSttLanguageCode()
  }
})

// Medical Questionnaire Manager — Structured Clinical Interview
class MedicalQuestionnaireManager {
  constructor() {
    // Questions use i18n keys — translated at display time via t()
    // Core structured questions — HPI detail questions (character through associated_symptoms)
    // will be replaced with AI-generated context-aware questions after symptoms are provided
    this.questions = [
      { id: 'age', i18nKey: 'q.age', type: 'number', phase: 'demographics' },
      { id: 'gender', i18nKey: 'q.gender', type: 'open', phase: 'demographics' },
      { id: 'symptoms', i18nKey: 'q.symptoms', type: 'open', phase: 'chief_complaint' },
      { id: 'onset', i18nKey: 'q.onset', type: 'open', phase: 'hpi' },
      // HPI detail slots — will be replaced with AI-generated questions after symptoms are known
      { id: 'hpi_detail_1', i18nKey: 'q.character', type: 'open', phase: 'hpi', aiGenerated: false },
      { id: 'hpi_detail_2', i18nKey: 'q.location', type: 'open', phase: 'hpi', aiGenerated: false },
      { id: 'hpi_detail_3', i18nKey: 'q.severity', type: 'open', phase: 'hpi', aiGenerated: false },
      { id: 'hpi_detail_4', i18nKey: 'q.timing', type: 'open', phase: 'hpi', aiGenerated: false },
      { id: 'hpi_detail_5', i18nKey: 'q.aggravating', type: 'open', phase: 'hpi', aiGenerated: false },
      { id: 'hpi_detail_6', i18nKey: 'q.associated', type: 'open', phase: 'hpi', aiGenerated: false },
      { id: 'past_medical', i18nKey: 'q.pastMedical', type: 'open', phase: 'medical_history' },
      { id: 'medications', i18nKey: 'q.medications', type: 'open', phase: 'medical_history' },
      { id: 'allergies', i18nKey: 'q.allergies', type: 'open', phase: 'medical_history' },
      { id: 'family_history', i18nKey: 'q.familyHistory', type: 'open', phase: 'medical_history' },
      { id: 'lifestyle', i18nKey: 'q.lifestyle', type: 'open', phase: 'social' },
    ]
    this.hpiQuestionsGenerated = false
    this.currentQuestionIndex = 0
    this.userResponses = {}
    this.isComplete = false
  }

  getNextQuestion() {
    if (this.currentQuestionIndex < this.questions.length) {
      const q = this.questions[this.currentQuestionIndex]
      // AI-generated questions store text directly, static ones use i18nKey
      return q.aiGenerated ? q.text : q.i18nKey
    }
    this.isComplete = true
    return null
  }

  addResponse(response) {
    if (this.currentQuestionIndex < this.questions.length) {
      const questionId = this.questions[this.currentQuestionIndex].id
      this.userResponses[questionId] = response
      this.currentQuestionIndex++
    }
  }

  getAllResponses() {
    return Object.values(this.userResponses).join('\n\n')
  }

  getProgress() {
    return {
      current: this.currentQuestionIndex,
      total: this.questions.length,
      percentage: Math.round((this.currentQuestionIndex / this.questions.length) * 100)
    }
  }

  /**
   * Detect symptom category from the user's symptom description and generate
   * contextually appropriate HPI questions. Works without an API key.
   */
  adaptQuestionsToSymptoms() {
    if (this.hpiQuestionsGenerated) return
    const symptoms = (this.userResponses.symptoms || '').toLowerCase()
    if (!symptoms) return

    // Symptom category detection with keyword matching
    const categories = {
      skin_oral: {
        keywords: ['lip', 'lips', 'mouth', 'sore', 'crack', 'rash', 'skin', 'lesion', 'ulcer', 'bump', 'mole', 'spot', 'blister', 'wart', 'acne', 'eczema', 'psoriasis', 'dermatitis', 'hives', 'itchy skin', 'dry skin', 'wound', 'cut', 'boil', 'cyst', 'scab', 'peel', 'flak', 'sun damage', 'sunburn', 'discolor'],
        questions: [
          'Can you describe the appearance of the affected area? (color, size, shape, texture — e.g., red, crusty, oozing, raised, flat)',
          'Has the appearance changed over time? Is it getting bigger, changing color, or spreading?',
          'Is there any pain, itching, burning, or numbness in the affected area?',
          'Have you had any sun exposure, chemical contact, or injury to the area? Do you use sun protection regularly?',
          'Have you noticed any similar spots or sores elsewhere on your body?',
          'Have you tried any treatments on it? (ointments, creams, lip balm, medications) Did anything help?'
        ]
      },
      sexual_urological: {
        keywords: ['erect', 'erectile', 'impotence', 'libido', 'sex drive', 'sexual', 'penis', 'testicle', 'prostate', 'urination', 'urinary', 'pee', 'bladder', 'hard on', 'orgasm', 'ejaculat', 'fertility', 'infertil'],
        questions: [
          'How would you rate the severity of this issue? Is it partial or complete? Does it happen every time or only sometimes?',
          'Are you able to achieve normal function in some situations (e.g., morning, during certain activities) but not others?',
          'Have you noticed any changes in desire or interest, or is this primarily a physical issue?',
          'Are you currently taking any medications? (blood pressure meds, antidepressants, and other drugs can affect this)',
          'How are your stress levels, mood, and sleep quality? Any significant life changes or relationship factors?',
          'Do you have any chronic conditions such as diabetes, high blood pressure, heart disease, or high cholesterol?'
        ]
      },
      mental_health: {
        keywords: ['anxiety', 'anxious', 'depress', 'sad', 'mood', 'stress', 'panic', 'worry', 'sleep', 'insomnia', 'suicid', 'self-harm', 'mental', 'emotional', 'overwhelm', 'hopeless', 'irritab', 'anger', 'ptsd', 'trauma', 'ocd', 'obsess', 'phobia', 'eating disorder', 'anorex', 'bulimi'],
        questions: [
          'How is this affecting your daily life? (work, relationships, activities you normally enjoy)',
          'How would you rate the severity — is it mild/manageable, or is it significantly interfering with your ability to function?',
          'Are there specific triggers or situations that make it worse? Are there times when it improves?',
          'How is your sleep? Any changes in appetite, energy levels, or ability to concentrate?',
          'Have you experienced anything like this before? If so, what helped previously?',
          'Are you currently seeing a counselor/therapist, or have you received any mental health treatment before?'
        ]
      },
      digestive: {
        keywords: ['stomach', 'nausea', 'vomit', 'diarrhea', 'constipat', 'bloat', 'gas', 'heartburn', 'acid reflux', 'gerd', 'abdomin', 'bowel', 'digest', 'appetite', 'weight loss', 'weight gain', 'ibs', 'crohn', 'colit', 'swallow', 'throat'],
        questions: [
          'Can you describe the discomfort more specifically? (cramping, burning, sharp, dull, pressure)',
          'Is this related to eating? Does it happen before, during, or after meals? Are certain foods triggers?',
          'Have you noticed any changes in your bowel habits? (frequency, consistency, color, blood or mucus)',
          'Have you experienced any unintentional weight changes, loss of appetite, or difficulty swallowing?',
          'How severe is it on a scale of 1-10? Does it interfere with your daily activities or sleep?',
          'Have you tried any remedies? (antacids, dietary changes, over-the-counter medications) What helped?'
        ]
      },
      respiratory: {
        keywords: ['cough', 'breath', 'wheez', 'chest', 'lung', 'asthma', 'pneumonia', 'bronchit', 'congestion', 'sinus', 'nasal', 'sneez', 'allerg', 'phlegm', 'mucus', 'shortness of breath', 'sob'],
        questions: [
          'Is it a dry cough or are you producing mucus/phlegm? If so, what color is it?',
          'Does it worsen at certain times? (night, with exertion, lying down, in certain environments)',
          'Are you experiencing any shortness of breath, wheezing, or chest tightness?',
          'Do you have any fever, chills, or night sweats?',
          'How severe is it on a scale of 1-10? Is it affecting your sleep or daily activities?',
          'Have you been exposed to anyone who is sick, or have you traveled recently? Any smoking history?'
        ]
      },
      musculoskeletal: {
        keywords: ['back pain', 'joint', 'knee', 'shoulder', 'neck', 'hip', 'ankle', 'wrist', 'elbow', 'arthrit', 'stiff', 'swell', 'sprain', 'strain', 'fracture', 'broke', 'muscle', 'weak', 'numb', 'tingl'],
        questions: [
          'How would you describe the pain? (sharp, dull, aching, throbbing, burning, stabbing)',
          'Where exactly is the pain? Does it radiate or spread to other areas?',
          'On a scale of 1-10, how severe is it? What is the worst it has been?',
          'What makes it worse? (movement, rest, certain positions, weight-bearing, time of day)',
          'What makes it better? Have you tried any treatments? (ice, heat, pain relievers, rest)',
          'Is there any swelling, redness, stiffness, or limited range of motion? Any numbness or tingling?'
        ]
      },
      hair_nails: {
        keywords: ['hair loss', 'hair fall', 'bald', 'alopecia', 'thin hair', 'scalp', 'dandruff', 'nail', 'brittle', 'fungal nail'],
        questions: [
          'Where is the hair loss occurring? Is it all over or in specific patches?',
          'Have you noticed the hair thinning gradually or falling out in clumps?',
          'Is there any itching, redness, scaling, or pain on the scalp?',
          'Have you had any recent major stress, illness, surgery, or significant weight changes?',
          'Are you taking any new medications or supplements? Any hormonal changes?',
          'Does anyone in your family have a history of hair loss or similar conditions?'
        ]
      },
      headache_neuro: {
        keywords: ['headache', 'migraine', 'dizzy', 'vertigo', 'faint', 'seizure', 'tremor', 'memory', 'confusion', 'vision', 'blur', 'double vision', 'tinnitus', 'hearing'],
        questions: [
          'Where in your head do you feel it? (forehead, temples, back of head, one side, all over)',
          'How would you describe it? (throbbing, pressure, stabbing, band-like, pulsating)',
          'On a scale of 1-10, how severe is it? What is the worst it has been?',
          'Are there any warning signs before it starts? (visual changes, aura, nausea)',
          'Is it associated with light sensitivity, sound sensitivity, nausea, or vomiting?',
          'What makes it better or worse? (rest, darkness, caffeine, medications, movement, screen time)'
        ]
      },
    }

    // Find the best matching category
    let bestCategory = null
    let bestScore = 0
    for (const [name, cat] of Object.entries(categories)) {
      const score = cat.keywords.filter(kw => symptoms.includes(kw)).length
      if (score > bestScore) {
        bestScore = score
        bestCategory = name
      }
    }

    // If a category matched, replace the HPI questions
    if (bestCategory && bestScore > 0) {
      this.replaceHpiQuestions(categories[bestCategory].questions)
    }
  }

  /**
   * Replace HPI detail question slots with AI-generated context-aware questions.
   * @param {string[]} aiQuestions — array of AI-generated question strings
   */
  replaceHpiQuestions(aiQuestions) {
    if (this.hpiQuestionsGenerated) return
    this.hpiQuestionsGenerated = true

    // Find the HPI detail slot indices (hpi_detail_1 through hpi_detail_6)
    const slotStart = this.questions.findIndex(q => q.id === 'hpi_detail_1')
    if (slotStart === -1) return

    // Count how many HPI slots we have
    let slotCount = 0
    for (let i = slotStart; i < this.questions.length; i++) {
      if (this.questions[i].id.startsWith('hpi_detail_')) slotCount++
      else break
    }

    // Build replacement questions from AI output
    const replacements = aiQuestions.slice(0, slotCount).map((q, i) => ({
      id: `hpi_detail_${i + 1}`,
      text: q, // Store the actual question text directly
      type: 'open',
      phase: 'hpi',
      aiGenerated: true
    }))

    // If AI returned fewer questions than slots, trim the extras
    this.questions.splice(slotStart, slotCount, ...replacements)
  }

  reset() {
    this.currentQuestionIndex = 0
    this.userResponses = {}
    this.isComplete = false
    this.hpiQuestionsGenerated = false
  }
}

// Composables
const router = useRouter()

// === REACTIVE STATE ===
const currentInput = ref('')
const isLoading = ref(false)
const error = ref(null)
const pendingImageBase64 = ref(null) // Stored image for diagnosis request
const showImageDescriptionModal = ref(false)
const pendingImageUrl = ref(null) // Data URL for image preview in modal
const pendingImageBase64Raw = ref(null) // Raw base64 for the pending image
const showCameraOverlay = ref(false) // Camera capture overlay visibility
const estimatedCost = ref(0.0)
const hasStarted = ref(false)
const chatMessages = ref([])
const chatAreaRef = ref(null)
const chatScrollRef = ref(null)
const inputControlsRef = ref(null)
const showTyping = ref(false)
const showHelp = ref(false)
const showSettings = ref(false)
const showMobileMenu = ref(false)
const showModelPicker = ref(false)
const modelPreference = ref(localStorage.getItem('model_preference') || 'auto')

const modelPickerOptions = [
  { id: 'auto', name: 'Auto', desc: 'Uses Claude Sonnet 4.6 — best balance of quality & speed', badge: 'default', badgeClass: 'bg-blue-500/20 text-blue-400', price: '~$0.50', free: false },
  { id: 'opus', name: 'Claude Opus 4.6', desc: 'Highest quality clinical reasoning', badge: 'best', badgeClass: 'bg-purple-500/20 text-purple-400', price: '~$2.50', free: false },
  { id: 'sonnet', name: 'Claude Sonnet 4.6', desc: 'Fast and capable', badge: 'fast', badgeClass: 'bg-emerald-500/20 text-emerald-400', price: '~$0.50', free: false },
  { id: 'haiku', name: 'Claude Haiku 4.5', desc: 'Fastest, simple cases', badge: 'budget', badgeClass: 'bg-amber-500/20 text-amber-400', price: '~$0.10', free: false },
  { id: 'gpt-4o', name: 'GPT-4o', desc: 'OpenAI flagship', badge: 'OpenAI', badgeClass: 'bg-green-500/20 text-green-400', price: '~$0.40', free: false },
  { id: 'gpt-4o-mini', name: 'GPT-4o Mini', desc: 'Fast OpenAI model', badge: 'OpenAI', badgeClass: 'bg-green-500/20 text-green-400', price: '~$0.06', free: false },
  { id: 'gemini-2.5-pro', name: 'Gemini 2.5 Pro', desc: 'Google flagship', badge: 'Google', badgeClass: 'bg-sky-500/20 text-sky-400', price: '~$0.35', free: false },
  { id: 'gemini-2.5-flash', name: 'Gemini 2.5 Flash', desc: 'Fast Google model', badge: 'Google', badgeClass: 'bg-sky-500/20 text-sky-400', price: '~$0.05', free: false },
  { id: 'llama3.1:8b', name: 'Llama 3.1 8B', desc: 'Local via Ollama', badge: 'free', badgeClass: 'bg-orange-500/20 text-orange-400', price: 'Free', free: true },
  { id: 'qwen2.5:7b', name: 'Qwen 2.5 7B', desc: 'Local via Ollama', badge: 'free', badgeClass: 'bg-orange-500/20 text-orange-400', price: 'Free', free: true },
]

const configuredKeys = computed(() => ({
  anthropic: !!localStorage.getItem('anthropic_api_key'),
  openai: !!localStorage.getItem('openai_api_key'),
  google: !!localStorage.getItem('google_api_key'),
  ollama: true, // always "available" as option
}))

function modelHasKey(modelId) {
  if (modelId === 'auto') return configuredKeys.value.anthropic || configuredKeys.value.openai || configuredKeys.value.google
  if (modelId.startsWith('gpt')) return configuredKeys.value.openai
  if (modelId.startsWith('gemini')) return configuredKeys.value.google
  if (['opus', 'sonnet', 'haiku'].includes(modelId)) return configuredKeys.value.anthropic
  return true // Ollama models
}

const selectedModelInfo = computed(() => {
  const m = modelPickerOptions.find(o => o.id === modelPreference.value) || modelPickerOptions[0]
  return { label: m.name, price: m.price, free: m.free }
})

function selectModel(id) {
  modelPreference.value = id
  localStorage.setItem('model_preference', id)
  showModelPicker.value = false
}

// Close model picker on outside click
function handleDocClick(e) {
  if (showModelPicker.value && !e.target.closest('.relative')) {
    showModelPicker.value = false
  }
}
const showHistory = ref(false)
const showOnboarding = ref(localStorage.getItem('onboarding_complete') !== 'true')
const viewingHistorySession = ref(false)
const apiStatus = ref(null) // null = checking, true = AI enabled, false = fallback mode

// Conversation management
const conversationState = ref('initial') // initial, gathering, followup, diagnosing, diagnosed
const questionnaire = ref(new MedicalQuestionnaireManager())
const currentStep = ref(0)
const totalSteps = ref(8) // Progress bar steps: Demographics, Symptoms, HPI, Details, History, Lifestyle, AI Follow-up, Review

// AI follow-up questions (up to 5 targeted questions to improve diagnosis accuracy)
const MAX_AI_FOLLOWUPS = 5
const aiFollowupCount = ref(0)
const aiFollowupQuestions = ref([])
const aiFollowupResponses = ref([])

// PA Interview state
const paConversation = ref([])  // [{role: "user"|"assistant", content: "..."}]
const paRouting = ref(null)     // { specialties: [...], urgency: "...", patient_summary: "..." }
const paExchangeCount = ref(0)
const paCharacter = ref(localStorage.getItem('pa_character') || 'dog') // 'dog' or 'cat'

const paAvatarName = computed(() => {
  const names = { bunny: 'Dr. Hopps', cat: 'Dr. Whiskers', dog: 'Dr. Buddy', human: 'Dr. AI' }
  return names[doctorAvatar.value?.characterType || paCharacter.value] || 'Dr. Hopps'
})

// Specialist Handoff state
const activeSpecialist = ref(null)           // Current specialist doctor object from registry
const specialistConversation = ref([])       // Specialist's Q&A exchanges
const specialistExchangeCount = ref(0)       // How many specialist questions answered (0-2)
const showHandoffTransition = ref(false)     // Controls the handoff card visibility

// Doctor avatar state
const avatarMode = ref(localStorage.getItem('avatar_mode') === 'true')
const showAvatarCustomizer = ref(false)
const defaultAvatar = {
  name: 'Dr. AI',
  specialty: "Physician's Assistant",
  skinTone: '#F5CBA7',
  hairStyle: 'short',
  hairColor: '#3d2b1f',
  eyeColor: '#4A6FA5',
  coatColor: '#f0f0f0',
  glasses: true,
  bgColor: '#1e3a5f',
  lipColor: '#c9877a',
  accessoryColor: '#64748b',
  avatarStyle: 'illustrated',
  photoUrl: '',
}
const doctorAvatar = ref({ ...JSON.parse(localStorage.getItem('doctor_avatar') || JSON.stringify(defaultAvatar)), specialty: "Physician's Assistant" })

const lastAssistantMessage = computed(() => {
  const msgs = chatMessages.value.filter(m => m.sender === 'assistant')
  return msgs.length > 0 ? msgs[msgs.length - 1] : null
})
const lastAssistantText = computed(() => {
  const msg = lastAssistantMessage.value
  if (!msg) return ''
  return (msg.text || '').replace(/\*\*/g, '')
})
const lastUserText = computed(() => {
  const msgs = chatMessages.value.filter(m => m.sender === 'user')
  if (msgs.length === 0) return ''
  return (msgs[msgs.length - 1].text || '').substring(0, 100)
})
const isMobile = ref(window.innerWidth < 640)
const avatarSize = computed(() => isMobile.value ? 'xxl' : 'xxxl')
const avatarTalking = ref(false)
let avatarTalkingTimer = null

function triggerAvatarTalking(durationMs = 3000) {
  avatarTalking.value = true
  clearTimeout(avatarTalkingTimer)
  avatarTalkingTimer = setTimeout(() => { avatarTalking.value = false }, durationMs)
}

const isSpeakingAnimating = computed(() => {
  // Don't animate mouth during agent pipeline — the doctor isn't speaking, just processing
  if (conversationState.value === 'diagnosing') return false
  return isTTSSpeaking.value || avatarTalking.value || showTyping.value
})
const showStepSidebar = computed(() => {
  return conversationState.value === 'gathering' || conversationState.value === 'pa_interview' || conversationState.value === 'specialist_handoff' || conversationState.value === 'followup' || conversationState.value === 'awaiting-confirmation'
})

const progressSteps = computed(() => {
  if (conversationState.value === 'specialist_handoff') {
    return ['Demographics', 'Symptoms', 'PA Interview', 'Specialist Review', 'Diagnosis']
  }
  if (conversationState.value === 'pa_interview') {
    return ['Demographics', 'Symptoms', 'PA Interview', 'Details', 'History', 'Review']
  }
  return [t('step.demographics'), t('step.symptoms'), t('step.details'), t('step.character'),
    t('step.history'), t('step.lifestyle'), t('step.followup'), t('step.review')]
})

function formatSubtitle(text) {
  if (!text) return ''
  // Extract the last meaningful block — find the last question or last 1-2 sentences
  let t = text.replace(/\*\*/g, '')

  // Split into sentences
  const sentences = t.split(/(?<=[.?!])\s+/).filter(s => s.trim())

  if (sentences.length === 0) return text

  // If there's a question, show from the last question onward
  const lastQuestionIdx = sentences.findLastIndex(s => s.includes('?'))
  if (lastQuestionIdx >= 0) {
    // Show the question and 1 sentence before it for context (max 2 sentences)
    const start = Math.max(lastQuestionIdx - 1, 0)
    t = sentences.slice(start).join(' ')
  } else {
    // No question — show last 2 sentences
    t = sentences.slice(-2).join(' ')
  }

  // Bold key terms
  t = t.replace(/\*\*(.*?)\*\*/g, '<strong class="text-blue-300">$1</strong>')
  return DOMPurify.sanitize(t, { ALLOWED_TAGS: ['strong', 'em'], ALLOWED_ATTR: ['class'] })
}

function saveDoctorAvatar(avatar) {
  doctorAvatar.value = avatar
  localStorage.setItem('doctor_avatar', JSON.stringify(avatar))
  showAvatarCustomizer.value = false
  toast.success('Avatar updated!')
}

watch(avatarMode, (val) => {
  localStorage.setItem('avatar_mode', val ? 'true' : 'false')
})

// Agent pipeline state
const activeAgent = ref(null)
const completedAgents = ref([])
const agentTimings = ref({})
const agentFindings = ref({})
const agentErrors = ref({})
const diagnosisElapsed = ref(0)
const liveAgentResults = ref([])  // Live streaming results for LiveDiagnosisView
const agentSimTimer = ref(null)
const elapsedTimer = ref(null)
const activeProvider = ref(null)

// Voice recording
const voiceRecording = ref({
  isRecording: false,
  isSupported: false,
  mediaRecorder: null,
  stream: null,
  chunks: []
})

// Settings
const voiceEnabled = ref(true)
const autoScroll = ref(true)
const soundEnabled = ref(localStorage.getItem('sound_enabled') !== 'false') // Sound ON by default for full voice experience

// Diagnosis completion actions
const diagnosisActions = ref([
  {
    id: 'view-dashboard',
    text: 'View Detailed Dashboard',
    category: 'results',
    description: 'See comprehensive analysis with charts and recommendations',
    icon: 'dashboard',
    action: 'navigate',
    route: '/dashboard'
  },
  {
    id: 'manual-dashboard',
    text: 'Go to Dashboard (Direct)',
    category: 'debug',
    description: 'Direct navigation to dashboard for testing',
    icon: 'build',
    action: 'manual-navigate',
    route: '/dashboard'
  },
  {
    id: 'when-doctor',
    text: 'When should I see a doctor?',
    category: 'care',
    description: 'Get guidance on when to seek medical attention',
    icon: 'person',
    action: 'question'
  },
  {
    id: 'home-remedies',
    text: 'What can I do at home?',
    category: 'treatment',
    description: 'Learn about home care options',
    icon: 'home',
    action: 'question'
  },
  {
    id: 'medications',
    text: 'Can I take over-the-counter medications?',
    category: 'treatment',
    description: 'Ask about medication options',
    icon: 'medication',
    action: 'question'
  },
  {
    id: 'symptoms-worse',
    text: 'Are my symptoms getting worse?',
    category: 'severity',
    description: 'Ask about symptom progression',
    icon: 'trending_down',
    action: 'question'
  }
])

// Speech Recognition (if available)
const speechRecognition = ref(null)
const speechSynthesis = ref(null)

// Computed properties
const canSubmit = computed(() => {
  return currentInput.value.trim() && !isLoading.value
})

const progressPercentage = computed(() => {
  if (conversationState.value === 'initial') return 0
  if (conversationState.value === 'gathering') {
    // Demographics: 0-20%
    const current = questionnaire.value.getProgress().current
    return Math.round((current / 3) * 20)
  }
  if (conversationState.value === 'pa_interview') {
    // PA interview: 20-85%
    return 20 + Math.round(Math.min(paExchangeCount.value / 10, 1) * 65)
  }
  if (conversationState.value === 'followup') {
    return 80 + Math.round((aiFollowupCount.value / MAX_AI_FOLLOWUPS) * 10)
  }
  if (conversationState.value === 'awaiting-confirmation') return 92
  if (conversationState.value === 'diagnosing') return 90
  if (conversationState.value === 'diagnosed') return 100
  return 0
})

// === WATCHERS ===
watch(chatMessages, async () => {
  if (autoScroll.value) {
    await nextTick()
    scrollToBottom()
  }
}, { deep: true })

watch(conversationState, (newState) => {
})

// === HELPER FUNCTIONS ===
function restoreInputFocus() {
  nextTick(() => {
    setTimeout(() => {
      if (inputControlsRef.value && inputControlsRef.value.focus) {
        inputControlsRef.value.focus()
      }
    }, 100)
  })
}

// === WATCHERS ===
watch(soundEnabled, (newVal) => {
  localStorage.setItem('sound_enabled', String(newVal))
  if (newVal && speechSynthesis.value) {
    // When turning on, play a brief confirmation
    setTimeout(() => {
      const utterance = new SpeechSynthesisUtterance('Voice enabled')
      const voice = pickDoctorVoice()
      if (voice) utterance.voice = voice
      utterance.rate = 0.95
      utterance.pitch = 0.75
      utterance.volume = 0.9
      window.speechSynthesis.speak(utterance)
    }, 100)
  } else if (!newVal) {
    // When turning off, cancel everything and clean up
    if (speakAbort) speakAbort.cancelled = true
    if (speechSynthesis.value) speechSynthesis.value.cancel()
    isTTSSpeaking.value = false
    stopKeepAlive()
  }
})

// === LIFECYCLE ===
const handleResize = () => { isMobile.value = window.innerWidth < 640 }
onMounted(async () => {
  window.addEventListener('resize', handleResize)
  document.addEventListener('click', handleDocClick)
  document.addEventListener('click', onDocClickUserMenu)

  // Start session inactivity timer (auto-logout after 30 min)
  startSessionTimer()

  // Initialize voice capabilities FIRST
  setupVoiceCapabilities()
  
  // Check API status
  checkApiStatus()
  
  // Force complete reset
  chatMessages.value = []
  hasStarted.value = false
  conversationState.value = 'initial'
  isLoading.value = false
  showTyping.value = false
  questionnaire.value.reset()
  
  // Add initial AI greeting — personalized if logged in with profile data
  setTimeout(() => {
    const profile = userProfile.value || {}
    const profileName = profile.name ? profile.name.split(' ')[0] : ''
    const profileAge = profile.age || profile.dateOfBirth ? (profile.age || calculateAge(profile.dateOfBirth)) : null
    const profileGender = profile.gender || ''

    // Pre-fill demographics from profile if available
    let skippedQuestions = 0
    if (profileAge) {
      questionnaire.value.answers.age = String(profileAge)
      skippedQuestions++
    }
    if (profileGender) {
      questionnaire.value.answers.gender = profileGender
      skippedQuestions++
    }
    if (skippedQuestions > 0) {
      questionnaire.value.currentQuestionIndex = skippedQuestions
    }

    // Build personalized greeting using i18n translations
    let greeting
    if (profileName && skippedQuestions >= 2) {
      greeting = t('chat.greetingWithProfile')
        .replace('{name}', profileName)
        .replace('{age}', profileAge)
        .replace('{gender}', profileGender)
    } else if (profileName) {
      greeting = t('chat.greetingWithName').replace('{name}', profileName)
    } else {
      greeting = t('chat.greeting')
    }

    chatMessages.value = [{
      id: Date.now(),
      sender: 'assistant',
      text: greeting,
      timestamp: new Date()
    }]

    hasStarted.value = true
    conversationState.value = 'gathering'
    // Speak the initial greeting if sound is enabled (uses same translated text)
    // Wait for voices to load (Chrome loads them async) before speaking
    if (soundEnabled.value && speechSynthesis.value) {
      const trySpeak = () => {
        const voices = speechSynthesis.value.getVoices()
        if (voices.length > 0) {
          speakMessage(greeting)
        } else {
          // Voices not loaded yet — wait for voiceschanged event
          const onVoices = () => {
            speechSynthesis.value.removeEventListener('voiceschanged', onVoices)
            speakMessage(greeting)
          }
          speechSynthesis.value.addEventListener('voiceschanged', onVoices)
          // Fallback: try once more after 2s in case event doesn't fire
          setTimeout(() => {
            speechSynthesis.value.removeEventListener('voiceschanged', onVoices)
            if (speechSynthesis.value.getVoices().length > 0) {
              speakMessage(greeting)
            }
          }, 2000)
        }
      }
      setTimeout(trySpeak, 800)
    }

    // Focus input on initial load
    restoreInputFocus()
  }, 500)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('click', handleDocClick)
  document.removeEventListener('click', onDocClickUserMenu)
  stopSessionTimer()
  cleanup()
  // Clean up TTS
  if (speakAbort) speakAbort.cancelled = true
  if (speechSynthesis.value) speechSynthesis.value.cancel()
  stopKeepAlive()
})

// === INITIALIZATION ===
async function checkApiStatus() {
  try {
    const anthropicKey = localStorage.getItem('anthropic_api_key')
    const openaiKey = localStorage.getItem('openai_api_key')

    if (anthropicKey && anthropicKey.trim() && anthropicKey.startsWith('sk-ant-')) {
      apiStatus.value = true
      activeProvider.value = 'anthropic'
    } else if (openaiKey && openaiKey.trim() && openaiKey.startsWith('sk-')) {
      apiStatus.value = true
      activeProvider.value = 'openai'
    } else {
      // Check if Ollama is available via backend health check
      try {
        const health = await healthCheck()
        if (health?.ollama_available) {
          apiStatus.value = true
          activeProvider.value = 'ollama'
        } else {
          apiStatus.value = false
          activeProvider.value = null
        }
      } catch {
        apiStatus.value = false
        activeProvider.value = null
      }
    }
  } catch (err) {
    console.error('API status check failed:', err)
    apiStatus.value = false
  }
}

async function initializeApp() {
  try {
    const isHealthy = await healthCheck()
    if (isHealthy) {
      // API connection successful
    } else {
      handleError('Backend API is not healthy. Please try again later.')
    }
  } catch (err) {
    // API connection failed — handled by handleError below
    handleError('Failed to connect to the backend API. Please check your network connection and try again.')
  }
}

function setupVoiceCapabilities() {
  try {
    // Check for speech recognition support (don't fully init — startVoiceRecording does that)
    const hasSpeechRecognition = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window
    if (!hasSpeechRecognition) {
      voiceEnabled.value = false
    }
    voiceRecording.value.isSupported = hasSpeechRecognition

    // Speech synthesis for text-to-speech
    if ('speechSynthesis' in window) {
      speechSynthesis.value = window.speechSynthesis
      // Force voice list to load (Chrome loads them async)
      speechSynthesis.value.getVoices()
      speechSynthesis.value.addEventListener('voiceschanged', () => {
        // Voice list updated — pickDoctorVoice() reads fresh each time, so nothing else needed
      })
    }
  } catch (err) {
    voiceEnabled.value = false
    speechSynthesis.value = null
    speechRecognition.value = null
  }
}

function setupKeyboardShortcuts() {
  const handleKeydown = (event) => {
    // Ctrl/Cmd + Enter to send message
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      if (canSubmit.value) {
        handleSendMessage(currentInput.value)
      }
    }
    
    // ESC to cancel/clear
    if (event.key === 'Escape') {
      if (voiceRecording.value.isRecording) {
        stopVoiceRecording()
      } else {
        currentInput.value = ''
      }
    }
    
    // F1 for help
    if (event.key === 'F1') {
      event.preventDefault()
      showHelp.value = !showHelp.value
    }
  }
  
  document.addEventListener('keydown', handleKeydown)
  
  // Store cleanup function
  window.__voiceDiagnosisKeydownHandler = handleKeydown
}

function cleanup() {
  if (voiceRecording.value.stream) {
    voiceRecording.value.stream.getTracks().forEach(track => track.stop())
  }

  if (speechRecognition.value) {
    speechRecognition.value.stop()
  }

  if (window.__voiceDiagnosisKeydownHandler) {
    document.removeEventListener('keydown', window.__voiceDiagnosisKeydownHandler)
  }

  // Clear any active diagnosis timers
  if (elapsedTimer.value) {
    clearInterval(elapsedTimer.value)
    elapsedTimer.value = null
  }
  if (agentSimTimer.value) {
    clearInterval(agentSimTimer.value)
    agentSimTimer.value = null
  }
  if (avatarTalkingTimer) {
    clearTimeout(avatarTalkingTimer)
    avatarTalkingTimer = null
  }
}

// === CORE FUNCTIONS ===

/**
 * Handles the start of the conversation
 */
function handleStart() {
  hasStarted.value = true
  conversationState.value = 'gathering'

  // Pre-fill demographics from user profile to skip redundant questions
  const profile = getProfile()
  const prefilled = []

  // Age — calculate from DOB
  let profileAge = 0
  if (profile.dateOfBirth) {
    const dob = new Date(profile.dateOfBirth)
    profileAge = Math.floor((Date.now() - dob.getTime()) / (365.25 * 24 * 60 * 60 * 1000))
    if (profileAge > 0 && profileAge < 150) {
      questionnaire.value.userResponses['age'] = String(profileAge)
      questionnaire.value.currentQuestionIndex++
      prefilled.push(`Age: ${profileAge}`)
    }
  }

  // Gender
  if (profile.gender && questionnaire.value.currentQuestionIndex === 1) {
    const genderMap = { male: 'Male', female: 'Female', other: 'Other', prefer_not_to_say: 'Other' }
    const genderStr = genderMap[profile.gender] || profile.gender
    questionnaire.value.userResponses['gender'] = genderStr
    questionnaire.value.currentQuestionIndex++
    prefilled.push(`Gender: ${genderStr}`)
  }

  // Build greeting — skip demographics if we have them from profile
  if (prefilled.length > 0) {
    const profileSummary = prefilled.join(', ')
    const allergies = (profile.allergies || []).filter(a => a && a.toLowerCase() !== 'none').join(', ')
    const meds = (profile.medications || []).filter(m => m && m.toLowerCase() !== 'none').join(', ')

    let profileNote = `From your profile: **${profileSummary}**`
    if (allergies) profileNote += ` | Allergies: **${allergies}**`
    if (meds) profileNote += ` | Medications: **${meds}**`

    const greeting = `Hello${profile.name ? ', ' + profile.name.split(' ')[0] : ''}! I'm Dr. Hopps, your AI medical assistant. Welcome back — great to see you.\n\n${profileNote}\n\nI already have some of your details on file, so we can skip ahead. I'll ask about your symptoms, how they feel, and any relevant history. Then our team of 7 AI specialists will collaborate to give you a thorough, safety-checked analysis.\n\nEverything stays private on your device. Let's get started!\n\n**What brings you here today? Please describe your main symptoms or health concerns in as much detail as possible.**`

    addMessage('assistant', greeting)
  } else {
    addMessage('assistant', t('chat.greeting'))
  }
}

/**
 * Validates user input based on the current question type
 */
function validateInput(message, questionType) {
  const trimmed = message.trim()
  
  if (!trimmed) {
    return { valid: false, error: 'Please provide a response.' }
  }
  
  // Get current question
  const currentQ = questionnaire.value.questions[questionnaire.value.currentQuestionIndex]
  
  if (!currentQ) {
    return { valid: true } // No specific validation needed
  }
  
  // Validate based on question ID
  switch (currentQ.id) {
    case 'symptoms':
      if (trimmed.length < 5) {
        return { valid: false, error: 'Please provide more detail about your symptoms (at least 5 characters).' }
      }
      // Check if it's just gibberish or non-medical text
      if (/^[^a-zA-Z]*$/.test(trimmed) || /^(.)\1+$/.test(trimmed)) {
        return { valid: false, error: 'Please describe your symptoms using words.' }
      }
      break
      
    case 'duration':
      // Accept either free text or one of the options
      // No strict validation needed as any time description is acceptable
      break
      
    case 'severity':
      // Try to extract a number
      const severityMatch = trimmed.match(/\b(\d+)\b/)
      if (!severityMatch) {
        return { valid: false, error: 'Please provide a number between 1 and 10 to rate the severity.' }
      }
      const severity = parseInt(severityMatch[1])
      if (severity < 1 || severity > 10) {
        return { valid: false, error: 'Please provide a severity rating between 1 and 10.' }
      }
      break
      
    case 'age':
      const ageMatch = trimmed.match(/\b(\d+)\b/)
      if (!ageMatch) {
        return { valid: false, error: 'Please provide your age as a number (e.g., 25).' }
      }
      const age = parseInt(ageMatch[1])
      if (age < 1 || age > 120) {
        return { valid: false, error: 'Please provide a valid age between 1 and 120.' }
      }
      break
      
    case 'gender':
      const validGenders = ['male', 'female', 'man', 'woman', 'non-binary', 'nonbinary', 'other', 'prefer not to say']
      const genderLower = trimmed.toLowerCase()
      const isValidGender = validGenders.some(g => genderLower.includes(g))
      if (!isValidGender && trimmed.length < 3) {
        return { valid: false, error: 'Please specify your gender (e.g., male, female, non-binary, or prefer not to say).' }
      }
      break
  }
  
  return { valid: true }
}

/**
 * Handles sending a message from the user
 */
async function handleSendMessage(message, imageBase64Param = null) {
  // If an image was uploaded, show the description modal instead of sending immediately
  if (imageBase64Param) {
    pendingImageBase64Raw.value = imageBase64Param
    pendingImageUrl.value = `data:image/jpeg;base64,${imageBase64Param}`
    showImageDescriptionModal.value = true
    return
  }

  if (!message.trim() || isLoading.value) {
    return
  }

  // Validate input if in gathering state
  if (conversationState.value === 'gathering') {
    const validation = validateInput(message, 'current')
    if (!validation.valid) {
      // Show error message to user
      addMessage('assistant', `❌ ${validation.error}`)
      // Restore focus and wait for corrected input
      restoreInputFocus()
      return
    }
  }

  // Clear input and add user message
  currentInput.value = ''
  const imageUrl = imageBase64Param ? `data:image/jpeg;base64,${imageBase64Param}` : null
  addMessage('user', message, imageUrl ? { imageUrl } : {})
  
  // Restore focus to input immediately after clearing
  restoreInputFocus()
  
  // Show typing indicator
  showTyping.value = true
  isLoading.value = true
  
  try {
    if (conversationState.value === 'gathering') {
      // Store response in questionnaire for regular questions
      questionnaire.value.addResponse(message)
      await handleGatheringMessage()
    } else if (conversationState.value === 'pa_interview') {
      // PA Interview mode — send to PA agent
      await handlePaInterview(message)
    } else if (conversationState.value === 'specialist_handoff') {
      // Specialist follow-up questions
      await handleSpecialistQuestion(message)
    } else if (conversationState.value === 'followup') {
      // Store AI follow-up response and ask next follow-up or proceed
      aiFollowupResponses.value.push(message)
      await handleAiFollowup()
    } else if (conversationState.value === 'awaiting-confirmation') {
      // Check if this is a "yes" response to proceed with diagnosis
      const isConfirmation = /^(yes|y|sure|ok|okay|proceed|go ahead|continue|let's go)$/i.test(message.trim())
      
      if (isConfirmation) {
        // User confirmed to proceed with diagnosis
        await handleProceedToDiagnosis()
      } else {
        // User declined or unclear response
        addMessage('assistant', "I understand. Would you like me to proceed with the health assessment analysis? Please respond with 'yes' when you're ready.")
        await waitForSpeech()
      }
    } else if (conversationState.value === 'diagnosed') {
      await handleFollowUpMessage(message)
    } else {
      // If state is initial, start the conversation
      handleStart()
      // Then handle the message
      questionnaire.value.addResponse(message)
      await handleGatheringMessage()
    }
  } catch (err) {
    // Message handling failed — shown in UI via handleError
    handleError(err instanceof ApiError ? err.message : 'An unexpected error occurred. Please try again.')
  } finally {
    showTyping.value = false

    // Wait for the doctor to finish speaking before re-enabling input
    // This prevents the user from sending while the doctor is mid-sentence
    if (soundEnabled.value && speechSynthesis.value) {
      await waitForSpeech()
    }

    isLoading.value = false
    restoreInputFocus()
  }
}

/**
 * Handle photo captured from the CameraCapture overlay.
 * Feeds the image into the existing pendingImage -> ImageDescriptionModal flow.
 */
function handleCameraCapture({ base64 }) {
  showCameraOverlay.value = false
  if (base64) {
    pendingImageBase64Raw.value = base64
    pendingImageUrl.value = `data:image/jpeg;base64,${base64}`
    showImageDescriptionModal.value = true
  }
}

/**
 * Handle camera error from the CameraCapture overlay.
 */
function handleCameraError(errMsg) {
  showCameraOverlay.value = false
  if (errMsg) {
    addMessage('assistant', `Camera error: ${errMsg}. You can try uploading an image instead.`)
  }
}

/**
 * Close the image description modal without sending
 */
function closeImageDescriptionModal() {
  showImageDescriptionModal.value = false
  pendingImageUrl.value = null
  pendingImageBase64Raw.value = null
}

/**
 * Handle submission from the image description modal
 * Adds the image + description to the chat and includes description in symptoms
 */
function handleImageDescriptionSubmit({ imageUrl, description }) {
  showImageDescriptionModal.value = false

  // Store the raw base64 for the diagnosis request
  pendingImageBase64.value = pendingImageBase64Raw.value

  // Build a message that includes the visual description
  const imageMessage = `[Image attached] ${description}`

  // Add the user message with the image preview
  addMessage('user', imageMessage, { imageUrl })

  // Append the visual description to the current questionnaire response
  // so it gets included in the symptoms data sent to the backend
  if (conversationState.value === 'gathering') {
    // If we're in the middle of gathering, store as additional context
    const currentQ = questionnaire.value.questions[questionnaire.value.currentQuestionIndex]
    if (currentQ) {
      // Don't advance the questionnaire, just note the image was added
      addMessage('assistant', 'Thank you for sharing the image. I\'ve noted your visual description. Please continue answering the current question.')
    }
  }

  // Clean up pending state
  pendingImageUrl.value = null
  pendingImageBase64Raw.value = null
}

/**
 * Handles gathering medical information through questions.
 * After demographics (age, gender) and chief complaint, transitions to PA interview.
 */
async function handleGatheringMessage() {
  // Brief thinking pause
  await new Promise(resolve => setTimeout(resolve, 800))

  const currentIndex = questionnaire.value.currentQuestionIndex
  const fixedQuestionCount = questionnaire.value.questions.length

  // After chief complaint is collected (3 questions: age, gender, symptoms),
  // transition to PA Interview mode
  const prevQuestionId = currentIndex > 0 ? questionnaire.value.questions[currentIndex - 1]?.id : null
  if (prevQuestionId === 'symptoms') {
    // Initialize PA conversation with what we've collected
    const responses = questionnaire.value.userResponses
    paConversation.value = [
      { role: 'user', content: responses.symptoms }
    ]
    paExchangeCount.value = 1

    // Transition to PA interview — keep whatever mode the user is in
    conversationState.value = 'pa_interview'
    await handlePaInterview(null)  // null = don't add user message, just get first PA question
    return
  }


  // After all fixed questions, transition to AI follow-up phase
  if (currentIndex >= fixedQuestionCount) {
    // Enter follow-up phase with up to 5 targeted AI questions
    conversationState.value = 'followup'
    await handleAiFollowup()
    return
  }

  // Auto-fill from profile if data is available for the upcoming question
  const upcomingQ = questionnaire.value.questions[currentIndex]
  if (upcomingQ) {
    const profile = getProfile()
    const autoFillMap = {
      'allergies': (profile.allergies || []).join(', '),
      'medications': (profile.medications || []).join(', '),
    }
    const autoVal = autoFillMap[upcomingQ.id]
    if (autoVal && autoVal.trim()) {
      // Auto-fill and show what we used
      questionnaire.value.userResponses[upcomingQ.id] = autoVal
      questionnaire.value.currentQuestionIndex++
      addMessage('assistant', `From your profile: **${autoVal}**`)
      addMessage('user', autoVal)
      // Recurse to handle the next question
      await handleGatheringMessage()
      return
    }
  }

  // Get the current question
  const currentQ = questionnaire.value.questions[currentIndex]
  if (!currentQ) return

  // Determine question text — AI-generated questions use .text, static ones use i18n
  let questionText
  if (currentQ.aiGenerated && currentQ.text) {
    questionText = currentQ.text
  } else if (currentQ.i18nKey) {
    const nextQuestionKey = questionnaire.value.getNextQuestion()
    if (!nextQuestionKey) return
    questionText = t(nextQuestionKey)
  } else {
    return
  }

  // Add phase transition prefix if entering a new phase
  const prevQ = currentIndex > 0 ? questionnaire.value.questions[currentIndex - 1] : null
  let prefix = ''
  if (currentQ.phase !== prevQ?.phase) {
    const phaseKeys = {
      'demographics': '',
      'chief_complaint': '',
      'hpi': 'q.phase.hpi',
      'medical_history': 'q.phase.medical',
      'social': 'q.phase.social',
    }
    const phaseKey = phaseKeys[currentQ.phase]
    prefix = phaseKey ? t(phaseKey) : ''
  }

  addMessage('assistant', prefix + questionText)
  await waitForSpeech()
  currentStep.value = Math.min(currentIndex, totalSteps.value - 1)
}

/**
 * Skip the remaining PA interview and proceed directly to diagnosis.
 */
async function skipToDiagnosis() {
  const responses = questionnaire.value.userResponses
  const symptoms = (responses.symptoms || '') .toLowerCase()
  // Detect specialty from symptoms
  const cats = { skin: ['lip','skin','rash','sore','crack','mole','wound'], cardiac: ['chest','heart','palpitat'], mental: ['anxiety','depress','stress','mood','sleep'], digestive: ['stomach','nausea','bowel','bloat'], neuro: ['headache','dizzy','numb','seizure'], nutrition: ['diet','weight','nutrition','food','eating','appetite','obesity','malnutrition','vitamin','deficiency'] }
  const specMap = { skin: 'dermatology', cardiac: 'cardiology', mental: 'psychiatry', digestive: 'gastroenterology', neuro: 'neurology', nutrition: 'nutrition' }
  let spec = 'general_medicine'
  for (const [cat, kws] of Object.entries(cats)) {
    if (kws.some(kw => symptoms.includes(kw))) { spec = specMap[cat]; break }
  }

  paRouting.value = {
    specialties: [spec],
    urgency: 'routine',
    patient_summary: paConversation.value.filter(m => m.role === 'user').map(m => m.content).join('. '),
    chief_complaint: responses.symptoms || ''
  }

  const specialtyName = spec.replace(/_/g, ' ').replace(/^\w/, c => c.toUpperCase())
  addMessage('assistant', `Great, I have enough to work with! I'm referring you to our **${specialtyName}** team for analysis.\n\nOur 7 AI agents will now collaborate on your case.`)
  await waitForSpeech()

  questionnaire.value.userResponses.symptoms = paConversation.value.filter(m => m.role === 'user').map(m => m.content).join('\n')
  questionnaire.value.userResponses.specialist_routing = [spec]
  currentStep.value = totalSteps.value
  await handleProceedToDiagnosis()
}

/**
 * Handles the PA (Physician's Assistant) interview.
 * Each user response is sent to the PA agent, which returns either a follow-up question or a routing decision.
 * @param {string|null} userMessage - The user's message, or null for initial PA question
 */
async function handlePaInterview(userMessage) {
  // Add user message to PA conversation history (if not the initial call)
  if (userMessage) {
    paConversation.value.push({ role: 'user', content: userMessage })
    paExchangeCount.value++
  }

  // Smart scripted fallback — detect symptom category and ask relevant questions
  const symptoms = (questionnaire.value.userResponses.symptoms || '').toLowerCase()
  const symptomCategories = {
    skin: { keywords: ['lip', 'lips', 'skin', 'rash', 'mole', 'sore', 'crack', 'itch', 'bump', 'wound', 'acne', 'blister', 'dry', 'peel', 'sun'], specialty: 'dermatology', questions: [
      'Can you describe how it looks? (color, size, texture — red, crusty, flaky, raised?)',
      'Has the appearance changed over time — getting bigger, spreading, or changing color?',
      'Is there any pain, itching, burning, or bleeding in the area?',
      'Have you had significant sun exposure or used tanning beds?',
      'Have you tried any treatments — creams, ointments, lip balm, medications?',
      'Do you have any medical conditions or take any medications regularly?',
      'Any known allergies to medications or skincare products?',
      'Does anyone in your family have a history of skin conditions or skin cancer?',
    ]},
    cardiac: { keywords: ['chest', 'heart', 'palpitat', 'blood pressure', 'pulse', 'racing'], specialty: 'cardiology', questions: [
      'Can you describe exactly what you feel? (pressure, squeezing, sharp, fluttering?)',
      'Does it happen with physical activity, stress, or at rest?',
      'Does it radiate to your arm, jaw, neck, or back?',
      'How long do episodes last? Seconds, minutes, or hours?',
      'Do you experience shortness of breath, dizziness, or sweating with it?',
      'Do you have high blood pressure, diabetes, or high cholesterol?',
      'Are you currently taking any medications?',
      'Does anyone in your family have heart disease?',
    ]},
    mental: { keywords: ['anxious', 'anxiety', 'depress', 'sad', 'stress', 'sleep', 'mood', 'panic', 'worry', 'hopeless'], specialty: 'psychiatry', questions: [
      'How would you describe what you\'re experiencing day to day?',
      'How is this affecting your work, relationships, and daily activities?',
      'How is your sleep? Any changes in appetite or energy levels?',
      'Are there specific situations or triggers that make it worse?',
      'Have you experienced anything like this before?',
      'Are you currently seeing a therapist or taking any medications?',
      'Do you use alcohol, caffeine, or any other substances regularly?',
      'Do you have a support system — family, friends, someone you can talk to?',
    ]},
    digestive: { keywords: ['stomach', 'nausea', 'vomit', 'diarrhea', 'bloat', 'heartburn', 'bowel', 'appetite', 'swallow'], specialty: 'gastroenterology', questions: [
      'Where exactly do you feel the discomfort? Upper, lower, left, or right?',
      'Is it related to eating? Before, during, or after meals?',
      'Have you noticed changes in bowel habits? Any blood or unusual color?',
      'Any nausea, vomiting, or unintended weight changes?',
      'Are certain foods or drinks triggers?',
      'Do you take any medications, especially NSAIDs or aspirin?',
      'Any known allergies or food intolerances?',
      'Does anyone in your family have GI conditions?',
    ]},
    neuro: { keywords: ['headache', 'migraine', 'dizzy', 'numb', 'tingl', 'vision', 'seizure', 'tremor', 'memory'], specialty: 'neurology', questions: [
      'Can you describe exactly what you experience? Where is it located?',
      'How often does this happen and how long does each episode last?',
      'Is there anything that triggers it or makes it worse?',
      'Do you experience any visual changes, nausea, or sensitivity to light/sound?',
      'Have you had any recent head injuries or falls?',
      'Do you have any medical conditions or take medications?',
      'Any numbness, weakness, or difficulty with coordination?',
      'Does anyone in your family have neurological conditions?',
    ]},
  }

  // Find matching category
  let matchedCategory = null
  let bestScore = 0
  for (const [, cat] of Object.entries(symptomCategories)) {
    const score = cat.keywords.filter(kw => symptoms.includes(kw)).length
    if (score > bestScore) { bestScore = score; matchedCategory = cat }
  }

  // Fallback generic questions if no category matched
  const scriptedQuestions = matchedCategory ? matchedCategory.questions : [
    'When did this first start? Was it sudden or gradual?',
    'On a scale of 1-10, how severe is this?',
    'Have you noticed any other symptoms alongside this?',
    'Do you have any existing medical conditions or take any medications?',
    'Do you have any known allergies?',
    'Does anything make it better or worse?',
    'Is there any family history of similar conditions?',
    'How is this affecting your daily life?',
  ]
  const matchedSpecialty = matchedCategory?.specialty || 'general_medicine'

  try {
    const responses = questionnaire.value.userResponses
    const typingMsg = addMessage('assistant', '...')

    let result
    try {
      result = await interview({
        conversation: paConversation.value,
        age: parseInt(responses.age) || 30,
        gender: responses.gender || 'unknown',
        language: lang.value || 'en',
        model_preference: 'auto'
      })
    } catch (apiErr) {
      // PA API call failed — using scripted fallback
      result = null
    }

    // Detect generic/unhelpful responses and replace with scripted questions
    const isGeneric = !result || (
      result.question && (
        result.question.includes('tell me more about your symptoms') ||
        result.question.includes('Could you tell me more') ||
        result.question.includes('What brings you')
      )
    )

    if (isGeneric && result?.action !== 'route') {
      // Use scripted fallback instead
      const qIdx = Math.max(0, paExchangeCount.value - 1)
      if (qIdx < scriptedQuestions.length) {
        result = { action: 'ask', question: scriptedQuestions[qIdx] }
      } else {
        // Enough scripted questions asked — route to detected specialist
        result = {
          action: 'route',
          routing: {
            specialties: [matchedSpecialty],
            urgency: 'routine',
            patient_summary: paConversation.value.filter(m => m.role === 'user').map(m => m.content).join('. '),
            chief_complaint: responses.symptoms || ''
          }
        }
      }
    }

    // Handle any response that has a question-like text (Ollama may not use exact "ask"/"route")
    if (result && result.action !== 'route') {
      const questionText = result.question || result.response
      if (questionText) {
        result.action = 'ask'
        result.question = questionText
      }
    }

    if (result && result.action === 'route') {
      // PA has decided to route to specialist(s)
      removeMessage(typingMsg)
      paRouting.value = result.routing

      const specialties = result.routing?.specialties || ['general_medicine']
      const summary = result.routing?.patient_summary || ''

      // Build comprehensive symptoms from PA conversation
      const fullSymptoms = paConversation.value
        .filter(m => m.role === 'user')
        .map(m => m.content)
        .join('\n')

      // Store the full interview in questionnaire responses
      questionnaire.value.userResponses.symptoms = fullSymptoms
      questionnaire.value.userResponses.pa_summary = summary
      questionnaire.value.userResponses.specialist_routing = specialties

      // ── Specialist Handoff ──────────────────────────────
      await handleSpecialistHandoff(specialties, summary)
    } else {
      // PA wants to ask another question — typewriter effect
      const question = result.question || 'Could you tell me more about your symptoms?'
      await typewriterMessage(typingMsg, question)
      await waitForSpeech()

      // Store PA's question in conversation history
      paConversation.value.push({ role: 'assistant', content: question })

      // Update progress (PA interview is ~20-80% of the progress bar)
      const progress = Math.min(20 + Math.round((paExchangeCount.value / 15) * 60), 80)
      currentStep.value = Math.round((progress / 100) * totalSteps.value)
    }
  } catch (err) {
    console.error('PA interview error:', err)
    // Remove typing indicator on error
    removeMessage(typingMsg)
    // On error with enough data, proceed to diagnosis; otherwise ask a scripted follow-up
    if (paExchangeCount.value >= 6) {
      // Set routing from matched category
      paRouting.value = { specialties: [matchedSpecialty], urgency: 'routine', patient_summary: '' }
      addMessage('assistant', 'I have enough information to proceed. Let me connect you with our diagnostic team.')
      await waitForSpeech()
      currentStep.value = totalSteps.value
      await handleProceedToDiagnosis()
    } else {
      // Use category-specific scripted questions
      const idx = Math.max(0, paExchangeCount.value - 1)
      const fallbackQ = scriptedQuestions[Math.min(idx, scriptedQuestions.length - 1)]
      addMessage('assistant', fallbackQ)
      paConversation.value.push({ role: 'assistant', content: fallbackQ })
    }
  }
}

/**
 * Handles AI-generated follow-up questions (up to 5) for improved diagnosis accuracy.
 * Called after the fixed 15 questions are complete, and after each follow-up response.
 */
async function handleAiFollowup() {
  // If we've asked enough follow-ups, proceed to diagnosis
  if (aiFollowupCount.value >= MAX_AI_FOLLOWUPS) {
    addMessage('assistant', t('chat.analysisStart'))
    await waitForSpeech()
    currentStep.value = totalSteps.value
    await handleProceedToDiagnosis()
    return
  }

  // Build context from the interview so far
  const responses = questionnaire.value.userResponses
  const symptomsSummary = [
    responses.symptoms,
    responses.onset ? `Onset: ${responses.onset}` : '',
    responses.character ? `Character: ${responses.character}` : '',
    responses.location_radiation ? `Location: ${responses.location_radiation}` : '',
    responses.severity ? `Severity: ${responses.severity}` : '',
    responses.associated_symptoms ? `Associated: ${responses.associated_symptoms}` : '',
    responses.past_medical ? `PMH: ${responses.past_medical}` : '',
    responses.medications ? `Meds: ${responses.medications}` : '',
    responses.lifestyle ? `Social: ${responses.lifestyle}` : '',
  ].filter(Boolean).join('. ')

  try {
    // Show a brief typing indicator
    const typingMsg = addMessage('assistant', '...')

    const result = await generateQuestion({
      symptoms: symptomsSummary,
      age: parseInt(responses.age) || 30,
      gender: responses.gender || 'unknown',
      language: lang.value || 'en',
      conversation_history: aiFollowupResponses.value,
      previous_questions: aiFollowupQuestions.value,
      questions_asked: aiFollowupCount.value,
      total_ai_questions: MAX_AI_FOLLOWUPS,
    })

    const question = result?.question
    if (!question || question.trim().length < 5) {
      // AI couldn't generate a useful question — proceed to diagnosis
      removeMessage(typingMsg)
      addMessage('assistant', t('chat.analysisStart'))
      await waitForSpeech()
      currentStep.value = totalSteps.value
      await handleProceedToDiagnosis()
      return
    }

    // Replace typing indicator with the actual question
    const qNum = aiFollowupCount.value + 1
    const prefix = qNum === 1
      ? `I have a few follow-up questions to improve diagnostic accuracy. (${qNum}/${MAX_AI_FOLLOWUPS})\n\n`
      : `(${qNum}/${MAX_AI_FOLLOWUPS}) `
    updateMessage(typingMsg, prefix + question)
    await waitForSpeech()

    aiFollowupQuestions.value.push(question)
    aiFollowupCount.value++
    currentStep.value = Math.min(questionnaire.value.questions.length + aiFollowupCount.value, totalSteps.value - 1)
  } catch (err) {
    console.error('AI follow-up question failed:', err)
    // On error, proceed to diagnosis rather than blocking
    addMessage('assistant', t('chat.analysisStart'))
    await waitForSpeech()
    currentStep.value = totalSteps.value
    await handleProceedToDiagnosis()
  }
}

/**
 * Proceeds with medical diagnosis after questions are complete
 */
function startAgentSimulation() {
  const agentOrder = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']
  let idx = 0
  activeAgent.value = agentOrder[0]
  completedAgents.value = []
  agentTimings.value = {}
  diagnosisElapsed.value = 0

  // Elapsed timer
  const startTime = Date.now()
  elapsedTimer.value = setInterval(() => {
    diagnosisElapsed.value = (Date.now() - startTime) / 1000
  }, 200)

  // Simulate agent progression every ~2 seconds, with diagnostician+research in parallel
  agentSimTimer.value = setInterval(() => {
    if (idx < agentOrder.length - 1) {
      // Complete current agent(s)
      completedAgents.value = [...completedAgents.value, agentOrder[idx]]
      agentTimings.value = { ...agentTimings.value, [agentOrder[idx]]: 1.5 + Math.random() * 1.5 }
      idx++

      // Run diagnostician and research in parallel (both activate after triage)
      if (agentOrder[idx] === 'diagnostician' && idx + 1 < agentOrder.length && agentOrder[idx + 1] === 'research') {
        activeAgent.value = agentOrder[idx]
        // Complete both diagnostician and research together on next tick
        setTimeout(() => {
          completedAgents.value = [...completedAgents.value, 'diagnostician']
          agentTimings.value = { ...agentTimings.value, diagnostician: 1.5 + Math.random() * 1.5 }
          completedAgents.value = [...completedAgents.value, 'research']
          agentTimings.value = { ...agentTimings.value, research: 1.5 + Math.random() * 1.5 }
          idx = idx + 2 // skip past both
          if (idx < agentOrder.length) {
            activeAgent.value = agentOrder[idx]
          }
        }, 2000)
      } else {
        activeAgent.value = agentOrder[idx]
      }
    }
  }, 2000)
}

function stopAgentSimulation(realTimings) {
  clearInterval(agentSimTimer.value)
  clearInterval(elapsedTimer.value)
  agentSimTimer.value = null
  elapsedTimer.value = null

  if (realTimings) {
    agentTimings.value = realTimings
  }
  completedAgents.value = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']
  activeAgent.value = null
}

// ── Specialist Handoff ────────────────────────────────────────────

async function handleSpecialistHandoff(specialties, summary) {
  const specialty = specialties[0] || 'general_medicine'
  const doctor = getSpecialist(specialty)
  activeSpecialist.value = doctor
  specialistConversation.value = []
  specialistExchangeCount.value = 0

  // PA farewell — announces the referral
  const specialtyName = specialty.replace(/_/g, ' ')
  addMessage('assistant',
    `Based on our conversation, I'd like to bring in our ${specialtyName} specialist, **${doctor.name}**, ${doctor.credentials}. I'm sharing your case notes with them now.`
  )
  await waitForSpeech()

  // Show the animated handoff card
  conversationState.value = 'specialist_handoff'
  showHandoffTransition.value = true

  // Let the card animate in
  await new Promise(r => setTimeout(r, 2500))
  showHandoffTransition.value = false

  // Specialist introduces themselves
  const paName = paAvatarName.value || 'Dr. Hopps'
  const greeting = doctor.greeting.replace('{paName}', paName)
  addMessage('assistant', greeting, { specialistMessage: true })
  await waitForSpeech()

  // Ask first specialist question
  await new Promise(r => setTimeout(r, 600))
  addMessage('assistant', doctor.questions[0], { specialistMessage: true })
}

async function handleSpecialistQuestion(userMessage) {
  specialistConversation.value.push({ role: 'user', content: userMessage })
  specialistExchangeCount.value++

  if (specialistExchangeCount.value < activeSpecialist.value.questions.length) {
    // Ask the next specialist question
    showTyping.value = true
    await new Promise(r => setTimeout(r, 800))
    showTyping.value = false
    addMessage('assistant', activeSpecialist.value.questions[specialistExchangeCount.value], { specialistMessage: true })
  } else {
    // All specialist questions answered — proceed to diagnosis
    showTyping.value = true
    await new Promise(r => setTimeout(r, 600))
    showTyping.value = false

    const farewell = activeSpecialist.value.farewell || "Thank you. Let me coordinate with our diagnostic team for a thorough analysis."
    addMessage('assistant', farewell, { specialistMessage: true })
    await waitForSpeech()

    // Merge specialist answers into questionnaire for the diagnosis pipeline
    questionnaire.value.userResponses.specialist_followup = specialistConversation.value
      .filter(m => m.role === 'user')
      .map(m => m.content)
      .join('\n')

    currentStep.value = totalSteps.value
    await handleProceedToDiagnosis()
  }
}

// ── Diagnosis Pipeline ───────────────────────────────────────────

async function handleProceedToDiagnosis() {
  isLoading.value = true
  showTyping.value = true
  conversationState.value = 'diagnosing'

  // Scroll to top so user sees the agent pipeline status
  window.scrollTo({ top: 0, behavior: 'smooth' })

  // Reset agent pipeline state for real-time streaming
  activeAgent.value = 'triage'
  completedAgents.value = []
  agentTimings.value = {}
  agentFindings.value = {}
  agentErrors.value = {}
  diagnosisElapsed.value = 0
  liveAgentResults.value = []

  // Start elapsed timer with timeout warning
  const diagStartTime = Date.now()
  let timeoutWarned = false
  elapsedTimer.value = setInterval(() => {
    diagnosisElapsed.value = (Date.now() - diagStartTime) / 1000
    if (diagnosisElapsed.value > 45 && !timeoutWarned) {
      timeoutWarned = true
      toast.warning('Analysis is taking longer than expected. Please wait...')
    }
  }, 200)

  // Agent order for determining the next active agent
  const agentOrder = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']

  // Add thinking message with helpful context
  addMessage('assistant', "Starting multi-agent analysis — 7 specialized AI agents will now analyze your case. This typically takes 15-30 seconds.\n\nAgents: Triage > Diagnostician + Research > Specialist > Treatment > Safety > Summary")

  try {
    // Extract all responses from questionnaire
    const responses = questionnaire.value.userResponses
    
    // Parse age - extract number from response text
    let age = 30
    if (responses.age) {
      const ageMatch = responses.age.match(/\d+/)
      age = ageMatch ? parseInt(ageMatch[0]) : 30
    }
    
    const gender = responses.gender || 'unknown'
    const duration = responses.duration || 'recent'
    
    // Parse severity - extract number from response text
    let severity = 5
    if (responses.severity) {
      const severityMatch = responses.severity.match(/\d+/)
      severity = severityMatch ? parseInt(severityMatch[0]) : 5
    }
    
    // Build comprehensive clinical summary from structured interview
    const symptomParts = [
      `Chief Complaint: ${responses.symptoms || 'Not specified'}`,
    ]
    if (responses.onset) symptomParts.push(`Onset: ${responses.onset}`)
    if (responses.character) symptomParts.push(`Character/Quality: ${responses.character}`)
    if (responses.location_radiation) symptomParts.push(`Location/Radiation: ${responses.location_radiation}`)
    symptomParts.push(`Severity: ${severity}/10`)
    if (responses.timing_pattern) symptomParts.push(`Timing/Pattern: ${responses.timing_pattern}`)
    if (responses.aggravating_alleviating) symptomParts.push(`Aggravating/Alleviating factors: ${responses.aggravating_alleviating}`)
    if (responses.associated_symptoms) symptomParts.push(`Associated Symptoms: ${responses.associated_symptoms}`)
    symptomParts.push(`Duration: ${duration}`)
    if (responses.past_medical) symptomParts.push(`Past Medical History: ${responses.past_medical}`)
    if (responses.medications) symptomParts.push(`Current Medications: ${responses.medications}`)
    if (responses.allergies) symptomParts.push(`Allergies: ${responses.allergies}`)
    if (responses.family_history) symptomParts.push(`Family History: ${responses.family_history}`)
    if (responses.lifestyle) symptomParts.push(`Social/Lifestyle: ${responses.lifestyle}`)

    // Include AI follow-up Q&A pairs for richer diagnostic context
    if (aiFollowupQuestions.value.length > 0) {
      symptomParts.push('\nAI Follow-up Interview:')
      aiFollowupQuestions.value.forEach((q, i) => {
        const answer = aiFollowupResponses.value[i] || 'No answer'
        symptomParts.push(`Q: ${q}\nA: ${answer}`)
      })
    }

    // Include visual symptom descriptions from uploaded images
    const imageMessages = chatMessages.value.filter(m => m.sender === 'user' && m.text && m.text.startsWith('[Image attached]'))
    if (imageMessages.length > 0) {
      symptomParts.push('\nVisual Symptom Description:')
      imageMessages.forEach(m => {
        const desc = m.text.replace('[Image attached] ', '')
        if (desc) symptomParts.push(desc)
      })
    }

    const symptomsText = symptomParts.join('\n\n')

    // Extract structured fields separately for richer backend context
    const diagnosisData = {
      symptoms: symptomsText,
      age: age,
      gender: gender,
      duration: duration,
      severity: severity,
      language: lang.value || 'en',
      image_base64: pendingImageBase64.value || null,
      // Send structured fields separately so the backend can build a better clinical summary
      medical_history: responses.past_medical || null,
      current_medications: responses.medications || null,
      allergies: responses.allergies || null,
      family_history: responses.family_history || null,
      social_history: responses.lifestyle || null,
      // Model preference from settings
      model_preference: localStorage.getItem('model_preference') || 'auto',
      // Specialist routing from PA agent (if available)
      specialist_routing: paRouting.value?.specialties || responses.specialist_routing || null,
    }

    // Clear the pending image after building the request
    pendingImageBase64.value = null

    // SSE streaming callback for real-time agent updates
    const agentLabels = {
      triage: 'Triage', diagnostician: 'Diagnostician', research: 'Research',
      specialist: 'Specialist', treatment: 'Treatment', safety: 'Safety', empathy: 'Summary'
    }

    const onAgentEvent = (event) => {
      if (event.event === 'agent_complete') {
        const agentName = event.agent

        // Update completed agents
        if (!completedAgents.value.includes(agentName)) {
          completedAgents.value = [...completedAgents.value, agentName]
        }

        // Update timings and findings
        agentTimings.value = { ...agentTimings.value, [agentName]: event.elapsed }
        agentFindings.value = { ...agentFindings.value, [agentName]: event.key_findings }

        // Push to live results for LiveDiagnosisView
        liveAgentResults.value = [...liveAgentResults.value, {
          agent: agentName,
          elapsed: event.elapsed,
          findings: event.key_findings,
          highlights: event.highlights || {},
          data: event.data || {}
        }]
        // Trigger avatar mouth animation
        triggerAvatarTalking(2000)

        // Determine next active agent
        const allCompleted = new Set(completedAgents.value)
        let nextActive = null
        for (const a of agentOrder) {
          if (!allCompleted.has(a)) {
            nextActive = a
            break
          }
        }
        activeAgent.value = nextActive

        // Update the thinking message in-place so user sees live progress
        const thinkingMsg = chatMessages.value.find(m => m.sender === 'assistant' && m.text.includes('multi-agent analysis'))
        if (thinkingMsg) {
          const done = completedAgents.value.length
          const total = agentOrder.length
          const completed = completedAgents.value.map(a => `${agentLabels[a] || a}`).join(', ')
          const next = nextActive ? agentLabels[nextActive] || nextActive : 'Finalizing'
          thinkingMsg.text = `Multi-agent analysis in progress (${done}/${total})...\n\nCompleted: ${completed}\nNow running: ${next}\n\nElapsed: ${diagnosisElapsed.value.toFixed(0)}s`
          chatMessages.value = [...chatMessages.value] // trigger reactivity
        }
      }
    }

    // Try streaming first, fall back to non-streaming
    let result
    try {
      result = await diagnoseStream(diagnosisData, onAgentEvent)
    } catch (streamErr) {
      // SSE streaming failed — falling back to standard request
      toast.warning(`Streaming failed (${streamErr.message}), trying standard request...`)
      startAgentSimulation()
      const isOllama = activeProvider.value === 'ollama' || localStorage.getItem('ai_provider') === 'ollama'
      const timeoutMs = isOllama ? 600000 : 90000  // 10 min for Ollama, 90s for cloud
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error(`Diagnosis request timed out after ${timeoutMs / 1000} seconds`)), timeoutMs)
      )
      try {
        result = await Promise.race([
          diagnose(diagnosisData),
          timeoutPromise
        ])
        stopAgentSimulation(result.agent_timings || null)
      } catch (fallbackErr) {
        stopAgentSimulation(null)
        throw new Error(`Stream: ${streamErr.message} | Fallback: ${fallbackErr.message}`)
      }
    }

    // Stop elapsed timer
    if (elapsedTimer.value) {
      clearInterval(elapsedTimer.value)
      elapsedTimer.value = null
    }

    estimatedCost.value += result.estimated_cost || 0.05

    // Check for API key / authentication errors in agent results
    const agentDetails = result.agent_details || {}
    const authErrors = Object.entries(agentDetails)
      .filter(([_, v]) => v && typeof v === 'object' && typeof v.error === 'string' && (v.error.includes('401') || v.error.includes('authentication') || v.error.includes('invalid') || v.error.includes('api_key') || v.error.includes('unauthorized')))
    if (authErrors.length > 0 && (!result.causes || result.causes.length === 0)) {
      // Determine which provider failed based on model preference and error content
      const mp = modelPreference.value || 'auto'
      const errText = authErrors.map(([_, v]) => v.error || '').join(' ')
      let providerName = 'AI Provider'
      if (mp.startsWith('gpt') || errText.includes('openai') || errText.includes('platform.openai')) providerName = 'OpenAI'
      else if (mp.startsWith('gemini') || errText.includes('google')) providerName = 'Google'
      else if (mp.startsWith('llama') || mp.startsWith('qwen')) providerName = 'Ollama'
      else if (errText.includes('anthropic') || errText.includes('x-api-key')) providerName = 'Anthropic'
      else providerName = (localStorage.getItem('ai_provider') || 'anthropic') === 'openai' ? 'OpenAI' : 'Anthropic'

      // Stop timers
      if (elapsedTimer.value) { clearInterval(elapsedTimer.value); elapsedTimer.value = null }

      // Remove thinking message
      if (chatMessages.value.length > 0 && chatMessages.value[chatMessages.value.length - 1].text.includes('multi-agent')) {
        chatMessages.value.pop()
      }

      // Show prominent error
      addMessage('assistant', `**API Key Error:** Your ${providerName} API key is invalid or has expired. All ${authErrors.length} diagnostic agents failed to authenticate.\n\n**To fix this:**\n1. Go to Settings (gear icon) and check your API key\n2. Generate a new key at your provider's dashboard\n3. Make sure billing/credits are active\n4. Re-enter the key and try again`)
      toast.error(`${providerName} API key is invalid or expired. Please update it in Settings.`, { duration: 10000 })

      conversationState.value = 'diagnosed'
      isLoading.value = false
      showTyping.value = false
      return
    }

    // Finalize agent state
    completedAgents.value = ['triage', 'diagnostician', 'research', 'specialist', 'treatment', 'safety', 'empathy']
    activeAgent.value = null
    if (result.agent_timings) agentTimings.value = result.agent_timings
    if (result.total_time) diagnosisElapsed.value = result.total_time

    // Check if AI was used
    if (result.estimated_cost > 0 && result.causes && result.causes.length > 0) {
      apiStatus.value = true
    } else {
      apiStatus.value = false
    }

    // Remove thinking message and add structured diagnosis
    chatMessages.value.pop()

    const diagnosisText = result.answer || "I've analyzed your symptoms. Based on the information provided, I recommend consulting with a healthcare professional."

    // Add the diagnosis message with structured agent data
    chatMessages.value.push({
      id: Date.now() + Math.random(),
      sender: 'assistant',
      text: diagnosisText,
      timestamp: new Date(),
      // Structured multi-agent data
      causes: result.causes || [],
      redFlags: result.red_flags || [],
      recommendedTests: result.recommended_tests || [],
      additionalQuestions: result.additional_questions || [],
      confidenceScores: result.confidence_scores || {},
      agentDetails: result.agent_details || {},
      agentTimings: result.agent_timings || {},
      multiAgent: result.multi_agent || false,
      agentsUsed: result.agents_used || [],
      // Enhanced structured data
      patientSummary: result.patient_summary || '',
      actionChecklist: result.action_checklist || [],
      safetyStatus: result.safety_status || '',
      safetyWarnings: result.safety_warnings || [],
      medications: result.medications || [],
      lifestyleRecommendations: result.lifestyle_recommendations || [],
      warningSignsList: result.warning_signs || [],
      followUpTimeline: result.follow_up_timeline || '',
      totalTime: result.total_time || 0
    })

    conversationState.value = 'diagnosed'

    // Save full structured result to localStorage for the dashboard FIRST
    // (before storeDiagnosisForDashboard which handles legacy format)
    try {
      const symptoms = questionnaire.value.userResponses.symptoms || ''
      const fullResult = {
        ...result,
        age: questionnaire.value.userResponses.age || '',
        gender: questionnaire.value.userResponses.gender || '',
        symptoms: symptoms,
        chief_complaint: symptoms,
        date: new Date().toISOString(),
        // Include chat transcript for dashboard
        chat_transcript: chatMessages.value.map(m => ({
          role: m.sender === 'user' ? 'user' : 'assistant',
          content: m.text,
          timestamp: m.timestamp
        }))
      }
      localStorage.setItem('latest_diagnosis_result', JSON.stringify(fullResult))
    } catch (e) {
      // Failed to store full diagnosis result — non-critical
    }

    // Store legacy format for backward compatibility
    storeDiagnosisForDashboard()

    // Save to conversation history
    try {
      saveSession({
        symptoms: questionnaire.value.userResponses.symptoms || '',
        age: questionnaire.value.userResponses.age || '',
        gender: questionnaire.value.userResponses.gender || '',
        diagnosisResult: result,
        chatMessages: chatMessages.value.map(m => ({ sender: m.sender, text: m.text, timestamp: m.timestamp })),
        timestamp: new Date().toISOString()
      })
    } catch (e) {
      // Failed to save session — non-critical
    }

    // Show diagnosis summary before redirecting to dashboard
    const topCause = result.causes?.[0]
    const specialist = paRouting.value?.specialties?.[0] || 'general medicine'
    const summaryMsg = topCause
      ? `Diagnosis complete! Top finding: **${topCause.cause}** (${topCause.value}% confidence). Specialist consulted: **${specialist.replace(/_/g, ' ')}**.\n\nOpening your full report...`
      : `Diagnosis complete! Your full report is ready.\n\nOpening your consultation report...`
    addMessage('assistant', summaryMsg)
    toast.success('Diagnosis complete!')

    setTimeout(() => {
      router.push('/dashboard')
    }, 2500)

  } catch (err) {
    const errMsg = err.message || 'Unknown error'
    const isAuthError = errMsg.includes('401') || errMsg.includes('authentication') || errMsg.includes('invalid') && errMsg.includes('key') || errMsg.includes('unauthorized') || (err.status === 401)
    if (isAuthError) {
      const mp = modelPreference.value || 'auto'
      const providerName = mp.startsWith('gpt') ? 'OpenAI' : mp.startsWith('gemini') ? 'Google' : (localStorage.getItem('ai_provider') === 'openai' ? 'OpenAI' : 'Anthropic')
      toast.error(`${providerName} API key is invalid or expired. Please update it in Settings.`, { duration: 10000 })
      addMessage('assistant', `**API Key Error:** Your ${providerName} API key is invalid or has expired.\n\nPlease go to Settings (gear icon) to update your API key.`)
    } else {
      toast.error(`Diagnosis failed: ${errMsg}`)
    }
    document.title = `ERR: ${errMsg.substring(0, 80)}`
    // Stop timers
    if (elapsedTimer.value) {
      clearInterval(elapsedTimer.value)
      elapsedTimer.value = null
    }
    stopAgentSimulation(null)

    // Remove thinking message
    if (chatMessages.value.length > 0 && chatMessages.value[chatMessages.value.length - 1].text.includes('Multi-agent')) {
      chatMessages.value.pop()
    }
    
    // Store basic diagnosis data for dashboard even when API fails
    const fallbackDiagnosis = [{
      condition: "Medical Assessment Needed",
      confidence: 75,
      explanation: `Based on your symptoms: ${questionnaire.value.getAllResponses().substring(0, 100)}..., I recommend consulting with a healthcare professional for proper evaluation and diagnosis.`,
      finalPlan: {
        content: `1. Schedule an appointment with your primary care physician\n2. Bring a list of all symptoms and their duration\n3. Mention any medications or treatments you've tried\n4. Ask about any tests that might be needed`
      }
    }]
    localStorage.setItem('finalDiagnosis', JSON.stringify(fallbackDiagnosis))
    
    // Store conversation history
    const chatHistory = chatMessages.value.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text
    }))
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory))
    
    // Switch to chat mode so user can see the error message properly
    if (avatarMode.value) {
      avatarMode.value = false
      localStorage.setItem('avatar_mode', 'false')
    }

    // Add error message with details so user can report the issue
    const errDetail = err.message || 'Unknown error'
    addMessage('assistant',
      `I apologize, but I'm having trouble processing your diagnosis right now.\n\n**Error:** ${errDetail}\n\n**Please check:**\n1. Your API key is valid (Settings > API Keys)\n2. The backend server is running on port 8000\n3. Your internet connection is stable\n\nYou can try again by clicking '+ New' in the header.`
    )

    conversationState.value = 'diagnosed'
  } finally {
    showTyping.value = false
    isLoading.value = false
    // Restore focus after diagnosis completes
    restoreInputFocus()
  }
}

/**
 * Handles follow-up questions after diagnosis
 */
async function handleFollowUpMessage(message) {
  // Wait a bit to simulate thinking
  await new Promise(resolve => setTimeout(resolve, 800))
  
  try {
    const result = await followup({
      question: message,
      previous_messages: chatMessages.value.slice(-10),
      original_symptoms: questionnaire.value.userResponses.symptoms || ''
    })

    estimatedCost.value += result.estimated_cost || 0.02
    addMessage('assistant', result.answer)
    
    // Play notification sound if enabled
    if (soundEnabled.value) {
      playNotificationSound()
    }
  } catch (err) {
    // Follow-up failed — shown in UI
    handleError(err instanceof ApiError ? err.message : 'Failed to process follow-up question. Please try again.')
  }
}

/**
 * Handle viewing a past session from history drawer
 */
function handleViewHistorySession(session) {
  if (!session || !session.chatMessages) return
  viewingHistorySession.value = true
  // Load the session's chat messages into the current view as read-only
  chatMessages.value = session.chatMessages.map((m, i) => ({
    id: Date.now() + i,
    sender: m.sender || (m.role === 'user' ? 'user' : 'assistant'),
    text: m.text || m.content || '',
    timestamp: m.timestamp ? new Date(m.timestamp) : new Date()
  }))
  conversationState.value = 'diagnosed'
  hasStarted.value = true

  // If the session has a full diagnosis result, store it for dashboard access
  if (session.diagnosisResult) {
    try {
      localStorage.setItem('latest_diagnosis_result', JSON.stringify({
        ...session.diagnosisResult,
        age: session.age || '',
        gender: session.gender || '',
        symptoms: session.symptoms || '',
        date: session.timestamp || new Date().toISOString()
      }))
    } catch (e) {
      // Failed to store history session — non-critical
    }
  }
}

/**
 * Handles quick questions from predefined options
 */
function handleQuickQuestion(question) {
  currentInput.value = question
  handleSendMessage(question)
}

/**
 * Handles quick actions including navigation and questions
 */
function handleQuickAction(action) {
  if (action.action === 'navigate' || action.action === 'manual-navigate') {
    // Always store diagnosis data before navigating
    storeDiagnosisForDashboard()
    
    if (action.action === 'manual-navigate') {
      // Force direct navigation for debug
      window.location.href = action.route
    } else {
      // Use Vue router
      router.push(action.route).catch(err => {
        // Navigation failed — non-critical
        handleError('Failed to navigate to dashboard. Please try refreshing the page.')
      })
    }
  } else if (action.action === 'question') {
    // Handle as a regular question
    currentInput.value = action.text
    handleSendMessage(action.text)
  } else {
    // Default behavior - treat as question
    handleQuickQuestion(action.text || action.id)
  }
}

/**
 * Stores current diagnosis data in localStorage for dashboard
 */
function storeDiagnosisForDashboard() {
  try {
    // Find the diagnosis message in chat (look for the main diagnosis response)
    // Check both chatMessages (live) and localStorage (for stored data)
    let diagnosisMessage = chatMessages.value.find(msg => 
      (msg.sender === 'assistant' || msg.role === 'assistant') && 
      (msg.text || msg.content) && 
      (msg.text?.length > 100 || msg.content?.length > 100) && 
      !msg.text?.includes('Analyzing') &&
      (msg.text?.includes('Differential diagnosis') || msg.content?.includes('Differential diagnosis'))
    )
    
    let dashboardData = []
    let treatmentSteps = []
    let holisticOptions = []
    
    // Get the text content from either msg.text or msg.content
    const text = diagnosisMessage?.text || diagnosisMessage?.content
    
    if (text) {
      // Look for "Differential diagnosis:" section - be more flexible with ending
      const diffDiagSection = text.match(/Differential diagnosis[s]?:([\s\S]*?)(?=Additional information|Suggested diagnostic|Clinical recommendations|Urgency:|Assessment summary:|$)/i)
      
      if (diffDiagSection) {
        const diagnosisText = diffDiagSection[1]
        
        // Use regex to match complete diagnosis entries including multiline clinical reasoning
        // Pattern: 1. Name — Confidence: 85% — Urgency: routine — Specialty: Primary Care
        //             Clinical reasoning: ...text...
        const diagnosisPattern = /(\d+)\.\s+([^\n—]+?)\s*—\s*Confidence:\s*(\d+)%\s*—\s*Urgency:\s*(\w+)\s*—\s*Specialty:\s*([^\n]+?)(?:\n\s*Clinical reasoning:\s*([^\n]+(?:\n(?!\d+\.)[^\n]+)*))?/gi
        
        let match
        while ((match = diagnosisPattern.exec(diagnosisText)) !== null) {
          const condition = match[2].trim()
          const confidence = parseInt(match[3])
          const urgency = match[4].trim()
          const specialty = match[5].trim()
          const explanation = match[6] ? match[6].trim() : 'Assessment based on clinical symptoms and patient history.'
          
          dashboardData.push({
            condition,
            confidence,
            urgency,
            specialty,
            explanation
          })
        }
        
      }
      
      // Extract treatment recommendations
      const recommendationsMatch = text.match(/Clinical recommendations:([\s\S]*?)(?=\n\n|Urgency:|$)/i)
      if (recommendationsMatch) {
        const recs = recommendationsMatch[1].match(/- (.+?)(?=\n|$)/g)
        if (recs) {
          treatmentSteps = recs.map(r => r.replace(/^-\s*/, '').trim())
        }
      }
      
      // Extract diagnostic tests as holistic options
      const testsMatch = text.match(/Suggested diagnostic tests:([\s\S]*?)(?=\n\n|Clinical recommendations:|$)/i)
      if (testsMatch) {
        const tests = testsMatch[1].match(/- (.+?)(?=\n|$)/g)
        if (tests) {
          holisticOptions = tests.map(t => t.replace(/^-\s*/, '').trim())
        }
      }
    }
    
    // Fallback if no diagnoses were parsed
    if (dashboardData.length === 0) {
      const symptoms = questionnaire.value.getAllResponses()
      dashboardData = [{
        condition: "Health Assessment Complete",
        confidence: 80,
        urgency: "routine",
        specialty: "Primary Care",
        explanation: `Based on your reported symptoms and medical history, a comprehensive evaluation by a healthcare professional is recommended for proper diagnosis and treatment planning.`
      }]
      
      treatmentSteps = [
        "Consult with your primary care physician or appropriate specialist",
        "Provide them with detailed symptom information",
        "Discuss duration, severity, and any triggering factors",
        "Follow recommended diagnostic tests or treatments",
        "Schedule follow-up appointments as needed"
      ]
    }
    
    // Add treatment and holistic options to first diagnosis item
    if (dashboardData.length > 0) {
      dashboardData[0].finalPlan = {
        content: treatmentSteps.join('\n')
      }
      dashboardData[0].holisticOptions = holisticOptions
    }
    
    // Sanitize any HTML-like content in finalPlan before storing to avoid many <br> tags
    const sanitizeHtmlToText = (html) => {
      if (!html || typeof html !== 'string') return html
      let txt = html
      // Remove <style> blocks entirely (and any CSS inside)
      txt = txt.replace(/<style[\s\S]*?<\/style>/gi, '')
      // Remove link tags that may reference stylesheets
      txt = txt.replace(/<link[^>]*>/gi, '')
      // Replace <br> tags with newlines
      txt = txt.replace(/<br\s*\/?\>/gi, '\n')
      // Strip remaining HTML tags
      txt = txt.replace(/<[^>]+>/g, '')
      // Collapse 3+ blank lines into two newlines
      txt = txt.replace(/(\n\s*){3,}/g, '\n\n')
      // Trim trailing/leading whitespace
      return txt.trim()
    }

    // Apply sanitization to all string fields in each diagnosis item to remove CSS and HTML
    const sanitizeItem = (item) => {
      const out = { ...item }
      if (out.condition && typeof out.condition === 'string') {
        out.condition = sanitizeHtmlToText(out.condition)
      }
      if (out.explanation && typeof out.explanation === 'string') {
        out.explanation = sanitizeHtmlToText(out.explanation)
      }
      if (out.finalPlan && out.finalPlan.content && typeof out.finalPlan.content === 'string') {
        out.finalPlan = { ...out.finalPlan, content: sanitizeHtmlToText(out.finalPlan.content) }
      }
      return out
    }

    dashboardData = dashboardData.map(sanitizeItem)

    // Store in localStorage
    localStorage.setItem('finalDiagnosis', JSON.stringify(dashboardData))
    
    // Also store chat history
    const chatHistory = chatMessages.value.map(msg => ({
      role: msg.sender === 'user' ? 'user' : 'assistant',
      content: msg.text
    }))
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory))
    
  } catch (error) {
    // Error storing diagnosis data — non-critical
  }
}

// === VOICE FUNCTIONS ===

/**
 * Toggles voice recording enabled/disabled
 */
function toggleVoiceEnabled(enabled) {
  voiceEnabled.value = enabled
  if (!enabled && voiceRecording.value.isRecording) {
    stopVoiceRecording()
  }
}

/**
 * Toggles voice recording
 */
async function toggleVoiceRecording() {
  if (!voiceEnabled.value) {
    handleError('Voice recording is disabled. Please enable it in settings.')
    return
  }

  if (voiceRecording.value.isRecording) {
    stopVoiceRecording()
  } else {
    await startVoiceRecording()
  }
}

/**
 * Starts voice recording
 */
async function startVoiceRecording() {
  // Check if already recording
  if (voiceRecording.value.isRecording) return

  // Try to initialize speech recognition if not already done
  if (!speechRecognition.value) {
    const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition
    if (SpeechRecognitionClass) {
      try {
        speechRecognition.value = new SpeechRecognitionClass()
        speechRecognition.value.continuous = false
        speechRecognition.value.interimResults = true
        speechRecognition.value.lang = getSttLanguageCode()
        speechRecognition.value.maxAlternatives = 1

        speechRecognition.value.onresult = (event) => {
          // Build transcript from all results
          let transcript = ''
          for (let i = 0; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript
          }
          // If this is a final result, send the message
          if (event.results[event.results.length - 1].isFinal) {
            voiceRecording.value.isRecording = false
            if (transcript && transcript.trim()) {
              handleSendMessage(transcript.trim())
            }
          }
        }

        speechRecognition.value.onerror = (event) => {
          voiceRecording.value.isRecording = false
          if (event.error === 'not-allowed' || event.error === 'permission-denied') {
            handleError('Microphone permission denied. Please allow microphone access in your browser settings (click the lock icon in the address bar).')
            voiceEnabled.value = false
          } else if (event.error === 'no-speech') {
            handleError('No speech detected. Please try again and speak clearly into your microphone.')
          } else if (event.error === 'network') {
            handleError('Speech recognition needs an internet connection. Please check your network.')
          } else if (event.error === 'aborted') {
            // User cancelled — not an error
          } else {
            handleError(`Voice recognition error: ${event.error}. Please type your message instead.`)
          }
        }

        speechRecognition.value.onend = () => {
          voiceRecording.value.isRecording = false
        }
      } catch (initErr) {
        speechRecognition.value = null
      }
    }
  }

  if (!speechRecognition.value) {
    handleError(
      'Voice input is not supported in this browser. Please use Google Chrome for voice features, or type your message instead.'
    )
    voiceEnabled.value = false
    return
  }

  try {
    // Stop any existing session first
    try { speechRecognition.value.abort() } catch (_) {}

    speechRecognition.value.start()
    voiceRecording.value.isRecording = true
  } catch (err) {
    voiceRecording.value.isRecording = false
    if (err.message && err.message.includes('already')) {
      voiceRecording.value.isRecording = true
    } else {
      handleError('Could not start voice recording. Please try again or type your message.')
    }
  }
}

/**
 * Stops voice recording
 */
function stopVoiceRecording() {
  try {
    if (speechRecognition.value) {
      try { speechRecognition.value.stop() } catch (_) {}
    }

    if (voiceRecording.value.mediaRecorder) {
      try {
        if (voiceRecording.value.mediaRecorder.state !== 'inactive') {
          voiceRecording.value.mediaRecorder.stop()
        }
      } catch (_) {}
    }

    if (voiceRecording.value.stream) {
      try {
        voiceRecording.value.stream.getTracks().forEach(track => {
          track.stop()
        })
        voiceRecording.value.stream = null
      } catch (err) {
        // Error stopping stream — expected in some states
      }
    }
    
    voiceRecording.value.isRecording = false
    voiceRecording.value.mediaRecorder = null
    voiceRecording.value.chunks = []
  } catch (err) {
    // Error stopping voice recording — non-critical
    // Force reset state
    voiceRecording.value.isRecording = false
    voiceRecording.value.mediaRecorder = null
    voiceRecording.value.stream = null
    voiceRecording.value.chunks = []
  }
}

/**
 * Handles voice recognition result
 */
function handleVoiceResult(transcript) {
  currentInput.value = transcript
  voiceRecording.value.isRecording = false
}

// === UTILITY FUNCTIONS ===

/**
 * Gets quick actions for current state
 */
function getQuickActions() {
  if (conversationState.value === 'gathering' && !questionnaire.value.isComplete) {
    return []
  }
  return []
}

/**
 * Handles settings changes from settings panel
 */
function handleSettingsChange(settings) {
  if (settings.voiceInput !== undefined) {
    voiceEnabled.value = settings.voiceInput
  }
  if (settings.autoScroll !== undefined) {
    autoScroll.value = settings.autoScroll
  }
  if (settings.soundEffects !== undefined) {
    soundEnabled.value = settings.soundEffects
  }
}

/**
 * Gets progress title based on current state
 */
function getProgressTitle() {
  switch (conversationState.value) {
    case 'gathering':
      return 'Collecting Information'
    case 'diagnosing':
      return 'Analyzing Symptoms'
    case 'diagnosed':
      return 'Assessment Complete'
    default:
      return 'Getting Started'
  }
}

/**
 * Gets progress message based on current state
 */
function getProgressMessage() {
  switch (conversationState.value) {
    case 'gathering':
      return `Gathering medical information (${questionnaire.value.getProgress().current}/${questionnaire.value.getProgress().total})`
    case 'diagnosing':
      return 'Processing your symptoms and generating health insights...'
    case 'diagnosed':
      return 'Your health assessment is ready. Feel free to ask follow-up questions.'
    default:
      return 'Ready to begin your health assessment'
  }
}

/**
 * Adds a message to the chat
 */
// Resolves when the doctor finishes speaking (or immediately if sound off)
let currentSpeechPromise = null

function addMessage(role, content, additionalData = {}) {
  // Sanitize message content
  const sanitizeMessage = (txt) => {
    if (!txt || typeof txt !== 'string') return txt
    let t = txt.replace(/<br\s*\/?\>/gi, '\n')
    t = t.replace(/<[^>]+>/g, '')
    t = t.replace(/(\n\s*){3,}/g, '\n\n')
    return t.trim()
  }

  const cleanContent = sanitizeMessage(content)

  const message = {
    id: Date.now() + Math.random(),
    sender: role,
    text: cleanContent,
    timestamp: new Date(),
    ...additionalData
  }

  chatMessages.value.push(message)
  chatMessages.value = [...chatMessages.value]

  // Animate avatar mouth when assistant speaks
  if (role === 'assistant' && cleanContent && cleanContent !== '...') {
    const wordCount = cleanContent.split(/\s+/).length
    triggerAvatarTalking(Math.min(Math.max(wordCount * 200, 2000), 6000))
  }

  // Speak message if it's from assistant and speech synthesis is enabled
  if (role === 'assistant' && speechSynthesis.value && soundEnabled.value) {
    // Create a promise that resolves when speech finishes
    currentSpeechPromise = new Promise((resolve) => {
      setTimeout(async () => {
        await speakMessage(cleanContent)
        resolve()
      }, 300)
    })
  } else {
    currentSpeechPromise = Promise.resolve()
  }
  return message
}

function removeMessage(msgOrId) {
  const id = typeof msgOrId === 'object' ? msgOrId.id : msgOrId
  chatMessages.value = chatMessages.value.filter(m => m.id !== id)
}

function updateMessage(msgOrId, newText) {
  const id = typeof msgOrId === 'object' ? msgOrId.id : msgOrId
  const msg = chatMessages.value.find(m => m.id === id)
  if (msg) msg.text = newText
  chatMessages.value = [...chatMessages.value]
}

/** Typewriter effect — reveals text character by character AND speaks via TTS */
async function typewriterMessage(msgOrId, fullText, speed = 20) {
  const id = typeof msgOrId === 'object' ? msgOrId.id : msgOrId
  const msg = chatMessages.value.find(m => m.id === id)
  if (!msg) return
  triggerAvatarTalking(fullText.length * speed + 500)

  // Start TTS in parallel with the typewriter animation
  if (speechSynthesis.value && soundEnabled.value) {
    const cleanText = fullText.replace(/\*\*/g, '').replace(/[#`_~]/g, '').trim()
    if (cleanText) {
      currentSpeechPromise = new Promise((resolve) => {
        setTimeout(async () => {
          await speakMessage(cleanText)
          resolve()
        }, 100)
      })
    }
  }

  for (let i = 0; i <= fullText.length; i++) {
    msg.text = fullText.slice(0, i)
    chatMessages.value = [...chatMessages.value]
    if (i < fullText.length) await new Promise(r => setTimeout(r, speed))
  }
}

/**
 * Waits for the doctor to finish speaking before continuing.
 * Returns immediately if sound is off.
 */
async function waitForSpeech() {
  if (currentSpeechPromise) {
    await currentSpeechPromise
    currentSpeechPromise = null
  }
}

/**
 * Speaks a message using text-to-speech
 */
// Track speaking state for avatar lip sync
const isTTSSpeaking = ref(false)

// Chrome workaround: speechSynthesis silently pauses after ~15s.
// Periodically call resume() to keep it alive.
let keepAliveInterval = null
function startKeepAlive() {
  stopKeepAlive()
  keepAliveInterval = setInterval(() => {
    if (speechSynthesis.value && speechSynthesis.value.speaking) {
      speechSynthesis.value.resume()
    }
  }, 5000)
}
function stopKeepAlive() {
  if (keepAliveInterval) { clearInterval(keepAliveInterval); keepAliveInterval = null }
}

/**
 * Find the best voice for the doctor avatar.
 * Always re-reads the voice list (never stale).
 */
// Language-to-BCP47 mapping for voice selection and STT
const LANG_VOICE_MAP = {
  en: { bcp47: ['en-US', 'en-GB', 'en-AU', 'en'], sttCode: 'en-US', preferred: {
    female: ['Google UK English Female', 'Google US English', 'Microsoft Jenny Online', 'Microsoft Zira', 'Samantha', 'Karen', 'Moira', 'Microsoft Aria Online'],
    male: ['Google UK English Male', 'Microsoft Guy Online', 'Microsoft David', 'Microsoft Ryan Online', 'Daniel', 'Alex', 'Tom'],
  }},
  es: { bcp47: ['es-ES', 'es-MX', 'es-US', 'es'], sttCode: 'es-ES', preferred: {
    female: ['Google español', 'Microsoft Elvira Online', 'Microsoft Sabina Online', 'Paulina', 'Monica', 'Microsoft Helena'],
    male: ['Microsoft Pablo Online', 'Microsoft Alvaro Online', 'Jorge', 'Diego', 'Juan'],
  }},
  fr: { bcp47: ['fr-FR', 'fr-CA', 'fr'], sttCode: 'fr-FR', preferred: {
    female: ['Google français', 'Microsoft Denise Online', 'Microsoft Caroline Online', 'Amelie', 'Marie', 'Thomas'],
    male: ['Microsoft Henri Online', 'Microsoft Paul Online', 'Thomas', 'Nicolas'],
  }},
  zh: { bcp47: ['zh-CN', 'zh-TW', 'zh-HK', 'zh'], sttCode: 'zh-CN', preferred: {
    female: ['Google 普通话', 'Microsoft Xiaoxiao Online', 'Microsoft Xiaoyi Online', 'Ting-Ting', 'Microsoft Huihui'],
    male: ['Microsoft Yunxi Online', 'Microsoft Yunyang Online', 'Microsoft Kangkang'],
  }},
  hi: { bcp47: ['hi-IN', 'hi'], sttCode: 'hi-IN', preferred: {
    female: ['Google हिन्दी', 'Microsoft Swara Online', 'Lekha'],
    male: ['Microsoft Madhur Online', 'Microsoft Prabhat Online'],
  }},
  ar: { bcp47: ['ar-SA', 'ar-EG', 'ar'], sttCode: 'ar-SA', preferred: {
    female: ['Microsoft Zariyah Online', 'Maged'],
    male: ['Microsoft Hamed Online', 'Maged'],
  }},
  de: { bcp47: ['de-DE', 'de-AT', 'de'], sttCode: 'de-DE', preferred: {
    female: ['Google Deutsch', 'Microsoft Katja Online', 'Anna', 'Petra'],
    male: ['Microsoft Conrad Online', 'Microsoft Stefan Online', 'Markus'],
  }},
  pt: { bcp47: ['pt-BR', 'pt-PT', 'pt'], sttCode: 'pt-BR', preferred: {
    female: ['Google português do Brasil', 'Microsoft Francisca Online', 'Luciana'],
    male: ['Microsoft Antonio Online', 'Microsoft Valério Online'],
  }},
  ja: { bcp47: ['ja-JP', 'ja'], sttCode: 'ja-JP', preferred: {
    female: ['Google 日本語', 'Microsoft Nanami Online', 'Kyoko', 'O-Ren'],
    male: ['Microsoft Keita Online', 'Otoya'],
  }},
  ko: { bcp47: ['ko-KR', 'ko'], sttCode: 'ko-KR', preferred: {
    female: ['Google 한국의', 'Microsoft SunHi Online', 'Yuna'],
    male: ['Microsoft InJoon Online'],
  }},
  ru: { bcp47: ['ru-RU', 'ru'], sttCode: 'ru-RU', preferred: {
    female: ['Google русский', 'Microsoft Svetlana Online', 'Milena'],
    male: ['Microsoft Dmitry Online', 'Yuri'],
  }},
  it: { bcp47: ['it-IT', 'it'], sttCode: 'it-IT', preferred: {
    female: ['Google italiano', 'Microsoft Elsa Online', 'Alice', 'Federica'],
    male: ['Microsoft Diego Online', 'Luca'],
  }},
}

function pickDoctorVoice() {
  if (!speechSynthesis.value) return null
  const voices = speechSynthesis.value.getVoices()
  if (voices.length === 0) return null

  // Check user preference first (exact match)
  const preferredName = doctorAvatar.value.preferredVoice
  if (preferredName) {
    const match = voices.find(v => v.name === preferredName)
    if (match) return match
  }

  // Determine target language
  const currentLangCode = lang.value || 'en'
  const langConfig = LANG_VOICE_MAP[currentLangCode] || LANG_VOICE_MAP.en
  const bcp47Prefixes = langConfig.bcp47

  // Determine gender preference from avatar name
  const avatarName = (doctorAvatar.value.name || '').toLowerCase()
  const femaleNames = ['sarah','maria','amara','emma','lisa','anna','jessica','rachel','emily','sofia','elena','mei','priya','yuki','fatima']
  const preferFemale = femaleNames.some(n => avatarName.includes(n))
  const genderKey = preferFemale ? 'female' : 'male'

  // Filter voices matching the target language
  // Windows uses underscores (zh_CN), browsers use hyphens (zh-CN) — normalize both
  const langVoices = voices.filter(v => {
    const vLang = (v.lang || '').replace(/_/g, '-').toLowerCase()
    return bcp47Prefixes.some(prefix => vLang.startsWith(prefix.toLowerCase()))
  })
  console.log(`[TTS] Language: ${currentLangCode}, prefixes: ${bcp47Prefixes.join(',')}, found ${langVoices.length} voices:`, langVoices.map(v => `${v.name} (${v.lang})`).join(', '))

  // Try preferred voice names for this language + gender
  const preferredNames = langConfig.preferred[genderKey] || []
  for (const name of preferredNames) {
    const v = langVoices.find(voice => voice.name.includes(name))
    if (v) return v
  }
  // Try the other gender's preferred voices as fallback
  const otherGender = genderKey === 'female' ? 'male' : 'female'
  const otherNames = langConfig.preferred[otherGender] || []
  for (const name of otherNames) {
    const v = langVoices.find(voice => voice.name.includes(name))
    if (v) return v
  }

  // Prefer cloud voices over local for the target language
  const cloudVoice = langVoices.find(v => !v.localService)
  if (cloudVoice) return cloudVoice
  if (langVoices.length > 0) return langVoices[0]

  // Final fallback: English, then any voice
  const enVoices = voices.filter(v => v.lang.startsWith('en'))
  if (enVoices.length > 0) return enVoices[0]
  return voices[0] || null
}

/** Returns the BCP-47 STT language code for the current UI language */
function getSttLanguageCode() {
  const currentLangCode = lang.value || 'en'
  return (LANG_VOICE_MAP[currentLangCode] || LANG_VOICE_MAP.en).sttCode
}

/**
 * Sequentially speaks an array of text chunks using a promise chain.
 * Each chunk waits for the previous to finish before starting.
 */
let speakAbort = null // AbortController-like flag for cancellation

function speakChunk(text, voice, rate) {
  return new Promise((resolve) => {
    if (speakAbort?.cancelled) { resolve(); return }
    const utterance = new SpeechSynthesisUtterance(text)
    if (voice) {
      utterance.voice = voice
      utterance.lang = voice.lang // Ensure utterance language matches voice
    } else {
      // Fallback: set language from current UI language
      const currentLangCode = lang.value || 'en'
      const langConfig = LANG_VOICE_MAP[currentLangCode] || LANG_VOICE_MAP.en
      utterance.lang = langConfig.bcp47[0]
    }
    utterance.rate = rate * 0.92  // slightly slower for robotic cadence
    utterance.pitch = 0.75  // lower pitch for robotic AI tone
    utterance.volume = 0.9

    utterance.onstart = () => { isTTSSpeaking.value = true }
    utterance.onend = () => { resolve() }
    utterance.onerror = (e) => {
      // 'interrupted' and 'canceled' are expected when we cancel
      if (e.error !== 'interrupted' && e.error !== 'canceled') {
        console.warn('[TTS] Chunk error:', e.error, 'text:', text.substring(0, 50))
      }
      resolve()
    }

    speechSynthesis.value.speak(utterance)
  })
}

async function speakMessage(text) {
  if (!text || typeof text !== 'string' || text.trim().length === 0) return
  if (!speechSynthesis.value) return
  if (!soundEnabled.value) return

  // Cancel any in-progress speech
  if (speakAbort) speakAbort.cancelled = true
  speechSynthesis.value.cancel()
  isTTSSpeaking.value = false

  // Small delay after cancel — some browsers need this
  await new Promise(r => setTimeout(r, 50))

  const abort = { cancelled: false }
  speakAbort = abort

  try {
    // Clean text for speech
    let cleanText = text
      .replace(/<[^>]*>/g, '')       // HTML tags
      .replace(/\*\*/g, '')          // Bold markdown
      .replace(/[#`_~]/g, '')        // Other markdown
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Markdown links → just text
      .replace(/[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu, '') // Emoji
      .replace(/---+/g, '. ')
      .replace(/={2,}/g, '. ')
      .replace(/-{2,}/g, '. ')
      .replace(/\n+/g, '. ')
      .replace(/\.\s*\./g, '.')
      .replace(/\s+/g, ' ')
      .trim()

    if (!cleanText) return

    // Split into chunks — keep them shorter (200 chars) for reliability.
    // Shorter chunks recover faster from errors and feel more responsive.
    const maxLen = 200
    const chunks = []
    let remaining = cleanText
    while (remaining.length > 0) {
      if (remaining.length <= maxLen) {
        chunks.push(remaining)
        break
      }
      // Prefer breaking at sentence boundaries, then commas, then spaces
      let breakIdx = remaining.lastIndexOf('. ', maxLen)
      if (breakIdx < maxLen * 0.3) breakIdx = remaining.lastIndexOf(', ', maxLen)
      if (breakIdx < maxLen * 0.3) breakIdx = remaining.lastIndexOf(' ', maxLen)
      if (breakIdx < maxLen * 0.3) breakIdx = maxLen
      chunks.push(remaining.substring(0, breakIdx + 1))
      remaining = remaining.substring(breakIdx + 1).trim()
    }

    // Always pick voice fresh (respects user changes without page reload)
    const voice = pickDoctorVoice()
    const rate = doctorAvatar.value.voiceRate || 0.95
    console.log(`[TTS] Speaking ${chunks.length} chunks, voice: ${voice?.name || 'NONE'} (${voice?.lang || '??'}), rate: ${rate}`)

    // If no voice at all, skip silently
    if (!voice) {
      console.warn('[TTS] No voice available for language:', lang.value)
      return
    }

    // Start Chrome keep-alive workaround
    startKeepAlive()

    // Speak chunks sequentially
    for (const chunk of chunks) {
      if (abort.cancelled || !soundEnabled.value) break
      await speakChunk(chunk, voice, rate)
    }
  } catch (err) {
    // TTS error — non-critical, voice continues
  } finally {
    isTTSSpeaking.value = false
    stopKeepAlive()
    if (speakAbort === abort) speakAbort = null
  }
}

/**
 * Plays a notification sound
 */
function playNotificationSound() {
  // Create a simple notification sound
  const audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const oscillator = audioContext.createOscillator()
  const gainNode = audioContext.createGain()
  
  oscillator.connect(gainNode)
  gainNode.connect(audioContext.destination)
  
  oscillator.frequency.setValueAtTime(800, audioContext.currentTime)
  oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1)
  
  gainNode.gain.setValueAtTime(0, audioContext.currentTime)
  gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.01)
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2)
  
  oscillator.start(audioContext.currentTime)
  oscillator.stop(audioContext.currentTime + 0.2)
}

/**
 * Scrolls chat to bottom
 */
function scrollToBottom() {
  if (chatAreaRef.value && chatAreaRef.value.scrollToBottom) {
    chatAreaRef.value.scrollToBottom()
  }
  // Also scroll the outer scroll container
  if (chatScrollRef.value) {
    chatScrollRef.value.scrollTo({ top: chatScrollRef.value.scrollHeight, behavior: 'smooth' })
  }
}

/**
 * Extracts age from responses
 */
function extractAge() {
  const responses = Object.values(questionnaire.value.userResponses).join(' ')
  const ageMatch = responses.match(/\b(\d{1,3})\b/)
  return ageMatch ? parseInt(ageMatch[1]) : null
}

/**
 * Extracts gender from responses
 */
function extractGender() {
  const responses = Object.values(questionnaire.value.userResponses).join(' ').toLowerCase()
  if (responses.includes('male') && !responses.includes('female')) return 'male'
  if (responses.includes('female')) return 'female'
  return 'unknown'
}

/**
 * Extracts severity from responses
 */
function extractSeverity() {
  const responses = Object.values(questionnaire.value.userResponses).join(' ')
  const severityMatch = responses.match(/\b([1-9]|10)\b/)
  return severityMatch ? parseInt(severityMatch[1]) : null
}

/**
 * Handles errors by displaying them to the user
 */
function handleError(message) {
  // Use toast for network/minor errors, keep modal for critical ones
  const isCritical = message.includes('API') || message.includes('backend') || message.includes('connect')
  if (isCritical) {
    error.value = message
    setTimeout(() => { if (error.value === message) error.value = null }, 8000)
  } else {
    toast.error(message)
  }
}

/**
 * Clears the current error
 */
function clearError() {
  error.value = null
}

/**
 * Navigate to API key setup page
 */
function goToApiSettings() {
  router.push('/setup')
}

/**
 * Test speech synthesis
 */
function testSpeech() {
  if (window.speechSynthesis) {
    const utterance = new SpeechSynthesisUtterance('Hello, I am your AI health assistant. I can speak to you.')
    utterance.rate = 0.92
    utterance.pitch = 0.75
    utterance.volume = 0.9
    window.speechSynthesis.speak(utterance)
  } else {
    // Speech synthesis not available in this browser
  }
}

// Make test functions available globally for debugging
if (import.meta.env.DEV) {
  window.testSpeech = testSpeech

  // Diagnostic: test streaming endpoint from browser
  window.testDiagnosis = async function() {
    const body = JSON.stringify({ symptoms: 'headache', age: 30, gender: 'male', severity: 3 })
    const headers = { 'Content-Type': 'application/json' }

    console.log('=== Test 1: POST /api/diagnose/stream (should get HTTP 200 fast) ===')
    try {
      const r = await fetch('/api/diagnose/stream', { method: 'POST', headers, body })
      console.log(`✅ Stream response: HTTP ${r.status}, type: ${r.headers.get('content-type')}`)
      const reader = r.body.getReader()
      const decoder = new TextDecoder()
      console.log('Waiting for first SSE chunk (up to 30s)...')
      const { done, value } = await Promise.race([
        reader.read(),
        new Promise((_, rej) => setTimeout(() => rej(new Error('No data after 30s')), 30000))
      ])
      if (done) { console.log('Stream ended immediately (empty)') }
      else { console.log(`✅ First chunk: ${decoder.decode(value).substring(0, 200)}`) }
      reader.cancel()
    } catch (e) {
      console.error(`❌ Stream test failed: ${e.name}: ${e.message}`)
    }

    console.log('=== Test 2: POST /api/diagnose/stream (direct to 127.0.0.1:8000) ===')
    try {
      const r = await fetch('http://127.0.0.1:8000/api/diagnose/stream', { method: 'POST', headers, body })
      console.log(`✅ Direct stream: HTTP ${r.status}, type: ${r.headers.get('content-type')}`)
      const reader = r.body.getReader()
      const decoder = new TextDecoder()
      const { done, value } = await Promise.race([
        reader.read(),
        new Promise((_, rej) => setTimeout(() => rej(new Error('No data after 30s')), 30000))
      ])
      if (done) { console.log('Stream ended immediately') }
      else { console.log(`✅ First chunk: ${decoder.decode(value).substring(0, 200)}`) }
      reader.cancel()
    } catch (e) {
      console.error(`❌ Direct stream failed: ${e.name}: ${e.message}`)
    }

    console.log('=== Done ===')
  }
}

/**
 * Resets the entire conversation
 */
function handleStartOver() {
  if (chatMessages.value.length > 0) {
    if (!confirm('Are you sure you want to start over? This will clear your current conversation.')) {
      return
    }
  }

  // Cancel any ongoing speech
  if (speakAbort) speakAbort.cancelled = true
  if (speechSynthesis.value) speechSynthesis.value.cancel()
  isTTSSpeaking.value = false
  stopKeepAlive()

  chatMessages.value = []
  currentInput.value = ''
  hasStarted.value = false
  conversationState.value = 'initial'
  questionnaire.value.reset()
  aiFollowupCount.value = 0
  aiFollowupQuestions.value = []
  aiFollowupResponses.value = []
  error.value = null
  currentStep.value = 0
  showTyping.value = false

  // Reset specialist handoff state
  activeSpecialist.value = null
  specialistConversation.value = []
  specialistExchangeCount.value = 0
  showHandoffTransition.value = false

  // Stop any ongoing voice recording
  if (voiceRecording.value.isRecording) {
    stopVoiceRecording()
  }

  toast.info('Conversation cleared. Ready for a new consultation.')
}

// Export for debugging
if (import.meta.env.DEV) {
  window.voiceDiagnosisDebug = {
    questionnaire,
    chatMessages,
    conversationState,
    handleStartOver,
    handleError
  }
}
</script>

<style scoped>
/* Bunny mouth talking animation */
.bunny-mouth-talking .bunny-jaw {
  animation: bunnyJaw 0.25s ease-in-out infinite alternate;
  transform-origin: 150px 152px;
}
@keyframes bunnyJaw {
  0% { transform: scaleY(0.5); }
  100% { transform: scaleY(1.3); }
}

/* Cat mouth talking animation */
.cat-mouth-talking .cat-jaw {
  animation: catJaw 0.22s ease-in-out infinite alternate;
  transform-origin: 150px 178px;
}
@keyframes catJaw {
  0% { transform: scaleY(0.4); }
  100% { transform: scaleY(1.2); }
}

/* Dog mouth talking animation */
.dog-mouth-talking .dog-jaw {
  animation: dogJaw 0.28s ease-in-out infinite alternate;
  transform-origin: 150px 178px;
}
@keyframes dogJaw {
  0% { transform: scaleY(0.5); }
  100% { transform: scaleY(1.3); }
}
</style>