<template>
  <nav role="banner" aria-label="Main navigation"
    class="sticky top-0 z-50 backdrop-blur-xl border-b py-3 px-4 sm:px-6 flex justify-between items-center transition-colors duration-300"
    style="background: color-mix(in srgb, var(--clinical-surface) 85%, transparent); border-color: var(--clinical-border)">

    <!-- Left: Brand + Nav Links -->
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

      <div class="hidden sm:flex items-center gap-2">
        <div class="w-px h-5" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>

        <!-- Model selector slot (only for consult page) -->
        <slot name="model-selector"></slot>
      </div>
    </div>

    <!-- Right: Desktop toolbar (hidden on mobile) -->
    <div class="hidden sm:flex items-center gap-1">
      <!-- Consult -->
      <router-link to="/consult" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all"
        :class="[
          currentPage === 'consult'
            ? (isDark ? 'text-white bg-slate-700/80' : 'text-slate-900 bg-slate-200/80')
            : (isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100')
        ]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
        <span class="hidden lg:inline">Consult</span>
      </router-link>

      <!-- Reports -->
      <router-link to="/reports" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all"
        :class="[
          currentPage === 'reports'
            ? (isDark ? 'text-white bg-slate-700/80' : 'text-slate-900 bg-slate-200/80')
            : (isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100')
        ]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
        <span class="hidden lg:inline">Reports</span>
      </router-link>

      <!-- Medications -->
      <router-link to="/medications" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all"
        :class="[
          currentPage === 'medications'
            ? (isDark ? 'text-white bg-slate-700/80' : 'text-slate-900 bg-slate-200/80')
            : (isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100')
        ]">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/></svg>
        <span class="hidden lg:inline">{{ t('nav.medications') }}</span>
      </router-link>

      <!-- More dropdown -->
      <div class="relative" ref="moreMenuRef">
        <button @click="showMoreMenu = !showMoreMenu" aria-label="More navigation options" :aria-expanded="showMoreMenu" class="flex items-center gap-1.5 px-2.5 py-2 rounded-lg text-sm font-medium transition-all"
          :class="[
            morePages.includes(currentPage)
              ? (isDark ? 'text-white bg-slate-700/80' : 'text-slate-900 bg-slate-200/80')
              : (isDark ? 'text-slate-300 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100')
          ]">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h.01M12 12h.01M19 12h.01"/></svg>
          <span class="hidden lg:inline">More</span>
          <svg class="w-3 h-3 opacity-50 transition-transform" :class="showMoreMenu ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </button>
        <Transition enter-active-class="transition duration-150 ease-out" enter-from-class="opacity-0 scale-95" enter-to-class="opacity-100 scale-100" leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100 scale-100" leave-to-class="opacity-0 scale-95">
          <div v-if="showMoreMenu" class="absolute right-0 top-full mt-1 w-52 rounded-xl shadow-xl border overflow-hidden py-1" style="z-index: 9999"
            :class="isDark ? 'bg-slate-900 border-slate-700/50' : 'bg-white border-slate-200'">
            <router-link to="/nutrition" @click="showMoreMenu = false" class="flex items-center gap-2.5 px-3.5 py-2.5 text-sm transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800 hover:text-white' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'">
              <span class="text-base">&#x1F957;</span> Nutrition
              <span class="ml-auto text-[10px] font-bold uppercase px-1.5 py-0.5 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 text-white">NEW</span>
            </router-link>
            <router-link to="/mental-health" @click="showMoreMenu = false" class="flex items-center gap-2.5 px-3.5 py-2.5 text-sm transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800 hover:text-white' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'">
              <span class="text-base">&#x1F9E0;</span> Mental Health
              <span class="ml-auto text-[10px] font-bold uppercase px-1.5 py-0.5 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 text-white">NEW</span>
            </router-link>
            <router-link to="/journal" @click="showMoreMenu = false" class="flex items-center gap-2.5 px-3.5 py-2.5 text-sm transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800 hover:text-white' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'">
              <span class="text-base">&#x1F4D3;</span> Journal
              <span class="ml-auto text-[10px] font-bold uppercase px-1.5 py-0.5 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 text-white">NEW</span>
            </router-link>
            <router-link to="/second-opinion" @click="showMoreMenu = false" class="flex items-center gap-2.5 px-3.5 py-2.5 text-sm transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800 hover:text-white' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'">
              <span class="text-base">&#x1F52C;</span> Second Opinion
              <span class="ml-auto text-[10px] font-bold uppercase px-1.5 py-0.5 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 text-white">NEW</span>
            </router-link>
            <div class="border-t my-1" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'"></div>
            <router-link to="/features" @click="showMoreMenu = false" class="flex items-center gap-2.5 px-3.5 py-2.5 text-sm font-medium transition-colors" :class="isDark ? 'text-emerald-400 hover:bg-slate-800' : 'text-emerald-600 hover:bg-slate-50'">
              <span class="text-base">&#x2728;</span> All Features
            </router-link>
          </div>
        </Transition>
      </div>

      <div class="w-px h-5 mx-0.5" :class="isDark ? 'bg-slate-700' : 'bg-slate-300'"></div>

      <ThemeLangControls />

      <!-- User menu -->
      <div class="relative" ref="userMenuRef">
        <button v-if="isLoggedIn" @click="showUserMenu = !showUserMenu" aria-label="User menu" :aria-expanded="showUserMenu" class="flex items-center gap-1.5 px-2 py-1.5 rounded-lg transition-all" :class="isDark ? 'hover:bg-slate-700/60 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <div class="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-detail font-bold text-white">
            {{ userInitials }}
          </div>
          <span class="hidden lg:inline text-sm font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ userName }}</span>
          <svg class="w-3 h-3 hidden lg:block" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
        </button>
        <router-link v-else to="/profile" aria-label="Sign in or view profile" class="p-2 rounded-lg transition-all" :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-700/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'">
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
            <router-link v-if="userProfile?.role === 'admin'" to="/admin" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-violet-400 hover:bg-slate-800' : 'text-violet-600 hover:bg-violet-50'">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/></svg>
              Admin Dashboard
            </router-link>
            <router-link to="/help" @click="showUserMenu = false" class="flex items-center gap-2 px-3 py-2 text-xs transition-colors" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-600 hover:bg-slate-50'">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              Help
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

    <!-- Mobile: hamburger -->
    <div class="flex sm:hidden items-center gap-1">
      <button @click="showMobileMenu = !showMobileMenu" class="p-2 rounded-lg" :class="isDark ? 'text-slate-400' : 'text-slate-500'" aria-label="Toggle navigation menu" :aria-expanded="showMobileMenu">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>

    <!-- Mobile dropdown menu -->
    <div v-if="showMobileMenu" class="absolute top-full left-0 right-0 border-b shadow-lg sm:hidden" style="z-index: 9999"
      :class="isDark ? 'bg-slate-900 border-slate-700' : 'bg-white border-slate-200'">
      <div class="p-3 space-y-1">
        <router-link to="/consult" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
          {{ t('nav.newConsultation') }}
        </router-link>
        <router-link to="/reports" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          {{ t('nav.reports') }}
        </router-link>
        <router-link to="/medications" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/></svg>
          {{ t('nav.medications') }}
        </router-link>
        <div class="border-t my-1" :class="isDark ? 'border-slate-800' : 'border-slate-100'"></div>
        <router-link to="/nutrition" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <span class="text-base">&#x1F957;</span> Nutrition
        </router-link>
        <router-link to="/mental-health" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <span class="text-base">&#x1F9E0;</span> Mental Health
        </router-link>
        <router-link to="/journal" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <span class="text-base">&#x1F4D3;</span> Journal
        </router-link>
        <router-link to="/second-opinion" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <span class="text-base">&#x1F52C;</span> Second Opinion
        </router-link>
        <router-link to="/features" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium" :class="isDark ? 'text-emerald-400 hover:bg-slate-800' : 'text-emerald-600 hover:bg-slate-50'">
          <span class="text-base">&#x2728;</span> All Features
        </router-link>
        <div class="border-t my-1" :class="isDark ? 'border-slate-800' : 'border-slate-100'"></div>
        <router-link to="/setup" @click="showMobileMenu = false" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm" :class="isDark ? 'text-slate-300 hover:bg-slate-800' : 'text-slate-700 hover:bg-slate-50'">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          {{ t('nav.settings2') }}
        </router-link>
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
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'
import { useI18n } from '@/composables/useI18n.js'
import { useUser } from '@/composables/useUser.js'
import ThemeLangControls from '@/components/ThemeLangControls.vue'

const props = defineProps({
  currentPage: {
    type: String,
    default: ''
  }
})

const router = useRouter()
const { isDark } = useTheme()
const { t } = useI18n()
const { profile: userProfile, isLoggedIn, logout: doLogout } = useUser()

const showMoreMenu = ref(false)
const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const moreMenuRef = ref(null)
const userMenuRef = ref(null)

const morePages = ['nutrition', 'mental-health', 'journal', 'second-opinion', 'features']

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

function handleLogout() {
  doLogout()
  showUserMenu.value = false
  showMobileMenu.value = false
  router.push('/')
}

// Close menus on outside click
function handleClickOutside(e) {
  if (moreMenuRef.value && !moreMenuRef.value.contains(e.target)) {
    showMoreMenu.value = false
  }
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
