<template>
  <div class="min-h-screen flex flex-col surface-page">

    <!-- ═══════ GLOBAL TOP NAV BAR ═══════ -->
    <nav class="sticky top-0 z-50 flex items-center justify-between px-4 sm:px-6 py-3 backdrop-blur-xl border-b transition-colors"
      style="background: color-mix(in srgb, var(--clinical-surface) 90%, transparent); border-color: var(--clinical-border)">
      <!-- Left: Brand + main nav links -->
      <div class="flex items-center gap-2 sm:gap-4">
        <router-link to="/" class="flex items-center gap-2 group">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20 flex-shrink-0">
            <svg class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="currentColor"><path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7V2z" /></svg>
          </div>
          <span class="text-sm font-semibold hidden sm:inline transition-colors" :class="isDark ? 'text-white group-hover:text-blue-300' : 'text-slate-900 group-hover:text-blue-600'">MedDiagnose AI</span>
        </router-link>

        <div class="hidden sm:block w-px h-5" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'"></div>

        <!-- Main nav links -->
        <div class="flex items-center gap-1">
          <router-link to="/"
            class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all"
            :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800/60' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z"/></svg>
            <span class="hidden md:inline">Home</span>
          </router-link>
          <router-link to="/consult"
            class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all"
            :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800/60' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
            <span class="hidden md:inline">Consultation</span>
          </router-link>
          <router-link to="/medications"
            class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all"
            :class="isDark ? 'bg-violet-500/15 text-violet-400' : 'bg-violet-50 text-violet-700'">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/></svg>
            <span class="hidden md:inline">Medications</span>
          </router-link>
          <router-link to="/reports"
            class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all"
            :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800/60' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span class="hidden md:inline">Reports</span>
          </router-link>
        </div>
      </div>

      <!-- Right: User menu -->
      <div class="flex items-center gap-2">
        <button @click="toggleTheme()" class="p-2 rounded-lg transition-colors"
          :class="isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800' : 'text-slate-500 hover:text-slate-900 hover:bg-slate-100'">
          <svg v-if="isDark" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
        </button>
        <!-- User avatar -->
        <router-link v-if="isLoggedIn" to="/profile" class="flex items-center gap-1.5 px-2 py-1.5 rounded-lg transition-all"
          :class="isDark ? 'hover:bg-slate-800/60 text-slate-400 hover:text-white' : 'hover:bg-slate-100 text-slate-500 hover:text-slate-900'">
          <div class="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-detail font-bold text-white">{{ userInitials }}</div>
          <span class="hidden lg:inline text-xs font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ userName }}</span>
        </router-link>
        <router-link v-else to="/profile" class="text-xs px-3 py-1.5 rounded-lg font-medium bg-gradient-to-r from-blue-500 to-purple-600 text-white">Log In</router-link>
      </div>
    </nav>

    <!-- ═══════ BODY: Sidebar + Content ═══════ -->
    <div class="flex-1 flex">
      <!-- Mobile sidebar toggle -->
      <button @click="mobileOpen = !mobileOpen"
        class="fixed top-16 left-3 z-40 p-2 rounded-lg sm:hidden"
        :class="isDark ? 'bg-slate-800 text-white' : 'bg-white text-slate-900 shadow'">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>

      <!-- Mobile overlay -->
      <div v-if="mobileOpen" @click="mobileOpen = false" class="fixed inset-0 bg-black/50 z-30 sm:hidden" style="top: 52px;"></div>

      <!-- Sidebar -->
      <aside class="fixed left-0 h-[calc(100vh-52px)] border-r flex flex-col transition-all duration-300 z-30" style="top: 52px;"
        :class="[
          isDark ? 'bg-slate-950 border-slate-800' : 'bg-white border-slate-200',
          sidebarCollapsed ? 'w-14' : 'w-56',
          mobileOpen ? 'translate-x-0' : '-translate-x-full sm:translate-x-0'
        ]">
        <!-- Nav items -->
        <nav class="flex-1 py-2 px-1.5 space-y-0.5 overflow-y-auto">
          <router-link v-for="item in navItems" :key="item.path" :to="item.path" @click="mobileOpen = false"
            class="flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-[13px] font-medium transition-all group"
            :class="[
              isActive(item.path)
                ? (isDark ? 'bg-violet-500/10 text-violet-400' : 'bg-violet-50 text-violet-700')
                : (isDark ? 'text-slate-400 hover:text-white hover:bg-slate-800/60' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'),
            ]">
            <div class="w-4.5 h-4.5 flex-shrink-0" v-html="item.icon"></div>
            <span v-if="!sidebarCollapsed" class="truncate">{{ item.label }}</span>
          </router-link>
        </nav>

        <!-- Bottom: collapse toggle -->
        <div class="px-1.5 py-2 border-t" :class="isDark ? 'border-slate-800' : 'border-slate-200'">
          <button @click="sidebarCollapsed = !sidebarCollapsed"
            class="hidden sm:flex w-full items-center gap-2.5 px-2.5 py-2 rounded-lg text-xs transition-colors"
            :class="isDark ? 'text-slate-500 hover:text-slate-300 hover:bg-slate-800/60' : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'">
            <svg class="w-4 h-4 transition-transform" :class="sidebarCollapsed ? 'rotate-180' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/></svg>
            <span v-if="!sidebarCollapsed">Collapse</span>
          </button>
        </div>
      </aside>

      <!-- Main content area -->
      <div class="flex-1 flex flex-col transition-all duration-300" :class="sidebarCollapsed ? 'sm:ml-14' : 'sm:ml-56'">
        <!-- Breadcrumb sub-header -->
        <div class="flex items-center justify-between px-4 sm:px-6 py-2.5 border-b text-xs"
          :class="isDark ? 'bg-slate-900/50 border-slate-800/50' : 'bg-slate-50 border-slate-100'">
          <div class="flex items-center gap-1.5 pl-10 sm:pl-0">
            <router-link to="/medications" class="transition-colors" :class="isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-400 hover:text-slate-600'">Medications</router-link>
            <svg class="w-3 h-3" :class="isDark ? 'text-slate-700' : 'text-slate-300'" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/></svg>
            <span class="font-medium" :class="isDark ? 'text-white' : 'text-slate-900'">{{ currentPageTitle }}</span>
          </div>
          <div class="flex items-center gap-1.5" :class="isDark ? 'text-violet-400' : 'text-violet-600'">
            <div class="w-1.5 h-1.5 rounded-full bg-violet-500 animate-pulse"></div>
            <span>Active</span>
          </div>
        </div>

        <!-- Page content -->
        <main class="flex-1 overflow-y-auto">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 py-6">
            <router-view />
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'
import { useUser } from '@/composables/useUser.js'

const { isDark, toggleTheme } = useTheme()
const { profile, isLoggedIn } = useUser()
const route = useRoute()
const sidebarCollapsed = ref(false)
const mobileOpen = ref(false)

const userName = computed(() => profile.value?.name || '')
const userInitials = computed(() => {
  const name = userName.value
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  return parts.length >= 2
    ? (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
    : name.slice(0, 2).toUpperCase()
})

const navItems = [
  { path: '/medications', label: 'My Medications', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 3h6v4a1 1 0 01-1 1h-4a1 1 0 01-1-1V3zm-2 4h10v14a2 2 0 01-2 2H9a2 2 0 01-2-2V7z"/></svg>' },
  { path: '/medications/interactions', label: 'Interactions', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"/></svg>' },
  { path: '/medications/food', label: 'Food & Lifestyle', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8.25v-1.5m0 1.5c-1.355 0-2.697.056-4.024.166C6.845 8.51 6 9.473 6 10.608v2.513m6-4.871c1.355 0 2.697.056 4.024.166C17.155 8.51 18 9.473 18 10.608v2.513M15 8.25v-1.5m-6 1.5v-1.5m12 9.75l-1.5.75a3.354 3.354 0 01-3 0 3.354 3.354 0 00-3 0 3.354 3.354 0 01-3 0 3.354 3.354 0 00-3 0 3.354 3.354 0 01-3 0L3 16.5m18-12.75v14.25"/></svg>' },
  { path: '/medications/side-effects', label: 'Side Effects', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z"/></svg>' },
  { path: '/medications/schedule', label: 'Schedule', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>' },
  { path: '/medications/scan', label: 'Scan Rx', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z"/><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z"/></svg>' },
  { path: '/medications/refills', label: 'Refills', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182M21.015 4.356v4.992"/></svg>' },
  { path: '/medications/identify', label: 'Pill ID', icon: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"/></svg>' },
]

function isActive(path) {
  if (path === '/medications') return route.path === '/medications'
  return route.path.startsWith(path)
}

const currentPageTitle = computed(() => {
  const item = navItems.find(n => isActive(n.path))
  return item?.label || 'My Medications'
})
</script>
