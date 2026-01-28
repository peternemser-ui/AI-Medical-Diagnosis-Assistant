<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 w-64 bg-white dark:bg-gray-800 shadow-lg">
      <div class="p-4 border-b border-gray-200 dark:border-gray-700">
        <h1 class="text-xl font-bold text-gray-900 dark:text-white">Admin Panel</h1>
      </div>
      <nav class="p-4 space-y-2">
        <button
          v-for="item in menuItems"
          :key="item.id"
          @click="activeSection = item.id"
          :class="[
            'w-full flex items-center px-4 py-2 rounded-lg text-left transition-colors',
            activeSection === item.id
              ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
          ]"
        >
          <component :is="item.icon" class="w-5 h-5 mr-3" />
          {{ item.label }}
        </button>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="ml-64 p-8">
      <!-- Header -->
      <header class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ currentSection?.label }}
        </h2>
        <p class="text-gray-600 dark:text-gray-400">
          {{ currentSection?.description }}
        </p>
      </header>

      <!-- Stats Cards -->
      <div v-if="activeSection === 'overview'" class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div
          v-for="stat in stats"
          :key="stat.label"
          class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm"
        >
          <p class="text-sm text-gray-600 dark:text-gray-400">{{ stat.label }}</p>
          <p class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ stat.value }}</p>
          <p :class="['text-sm mt-1', stat.change > 0 ? 'text-green-600' : 'text-red-600']">
            {{ stat.change > 0 ? '+' : '' }}{{ stat.change }}% from last week
          </p>
        </div>
      </div>

      <!-- Dynamic Section Content -->
      <component :is="sectionComponent" v-if="sectionComponent" />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, markRaw } from 'vue'
import { Users, Activity, Settings, BarChart2, FileText, AlertTriangle } from 'lucide-vue-next'
import UserManagement from './UserManagement.vue'
import DiagnosisReview from './DiagnosisReview.vue'
import SystemSettings from './SystemSettings.vue'
import AnalyticsDashboard from './AnalyticsDashboard.vue'
import AuditLogs from './AuditLogs.vue'

const activeSection = ref('overview')

const menuItems = [
  { id: 'overview', label: 'Overview', icon: markRaw(BarChart2), description: 'System overview and statistics' },
  { id: 'users', label: 'Users', icon: markRaw(Users), description: 'Manage user accounts' },
  { id: 'diagnoses', label: 'Diagnoses', icon: markRaw(Activity), description: 'Review and manage diagnoses' },
  { id: 'analytics', label: 'Analytics', icon: markRaw(BarChart2), description: 'View system analytics' },
  { id: 'logs', label: 'Audit Logs', icon: markRaw(FileText), description: 'View system logs' },
  { id: 'settings', label: 'Settings', icon: markRaw(Settings), description: 'System configuration' }
]

const stats = ref([
  { label: 'Total Users', value: '2,451', change: 12 },
  { label: 'Diagnoses Today', value: '147', change: 8 },
  { label: 'Urgent Cases', value: '12', change: -5 },
  { label: 'System Health', value: '99.9%', change: 0.1 }
])

const currentSection = computed(() =>
  menuItems.find(item => item.id === activeSection.value)
)

const sectionComponents = {
  users: markRaw(UserManagement),
  diagnoses: markRaw(DiagnosisReview),
  analytics: markRaw(AnalyticsDashboard),
  logs: markRaw(AuditLogs),
  settings: markRaw(SystemSettings)
}

const sectionComponent = computed(() =>
  sectionComponents[activeSection.value] || null
)
</script>
