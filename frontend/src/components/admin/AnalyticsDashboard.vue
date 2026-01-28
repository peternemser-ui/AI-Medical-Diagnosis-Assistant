<template>
  <div class="space-y-6">
    <!-- Time Range Selector -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm flex items-center space-x-4">
      <button
        v-for="range in timeRanges"
        :key="range.value"
        @click="selectedRange = range.value"
        :class="[
          'px-4 py-2 rounded-lg transition-colors',
          selectedRange === range.value
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
        ]"
      >
        {{ range.label }}
      </button>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div
        v-for="stat in analyticsStats"
        :key="stat.label"
        class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm"
      >
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-gray-600 dark:text-gray-400">{{ stat.label }}</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">{{ stat.value }}</p>
          </div>
          <div :class="['p-3 rounded-full', stat.bgColor]">
            <component :is="stat.icon" :class="['w-6 h-6', stat.iconColor]" />
          </div>
        </div>
        <div class="mt-4 flex items-center">
          <span :class="stat.trend > 0 ? 'text-green-600' : 'text-red-600'" class="text-sm font-medium">
            {{ stat.trend > 0 ? '+' : '' }}{{ stat.trend }}%
          </span>
          <span class="text-sm text-gray-500 dark:text-gray-400 ml-2">vs last period</span>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Diagnoses Over Time -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Diagnoses Over Time</h3>
        <div class="h-64 flex items-center justify-center text-gray-500">
          [Line Chart Placeholder]
        </div>
      </div>

      <!-- Condition Distribution -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Top Conditions</h3>
        <div class="space-y-4">
          <div v-for="condition in topConditions" :key="condition.name" class="flex items-center">
            <div class="flex-1">
              <div class="flex justify-between mb-1">
                <span class="text-sm text-gray-700 dark:text-gray-300">{{ condition.name }}</span>
                <span class="text-sm text-gray-500">{{ condition.count }}</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  class="bg-blue-600 h-2 rounded-full"
                  :style="{ width: `${condition.percentage}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Urgency Distribution -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Urgency Distribution</h3>
        <div class="grid grid-cols-2 gap-4">
          <div v-for="urgency in urgencyStats" :key="urgency.level" class="text-center p-4 rounded-lg" :class="urgency.bgClass">
            <p class="text-3xl font-bold" :class="urgency.textClass">{{ urgency.count }}</p>
            <p class="text-sm capitalize" :class="urgency.textClass">{{ urgency.level }}</p>
          </div>
        </div>
      </div>

      <!-- User Activity -->
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">User Activity</h3>
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <span class="text-gray-600 dark:text-gray-400">Active Users (24h)</span>
            <span class="font-semibold text-gray-900 dark:text-white">1,247</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-600 dark:text-gray-400">New Registrations</span>
            <span class="font-semibold text-gray-900 dark:text-white">89</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-600 dark:text-gray-400">Average Session Duration</span>
            <span class="font-semibold text-gray-900 dark:text-white">8m 32s</span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-gray-600 dark:text-gray-400">Return Users</span>
            <span class="font-semibold text-gray-900 dark:text-white">67%</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, markRaw } from 'vue'
import { Users, Activity, TrendingUp, Clock } from 'lucide-vue-next'

const selectedRange = ref('7d')

const timeRanges = [
  { label: 'Today', value: '1d' },
  { label: '7 Days', value: '7d' },
  { label: '30 Days', value: '30d' },
  { label: '90 Days', value: '90d' }
]

const analyticsStats = ref([
  { label: 'Total Diagnoses', value: '3,847', trend: 12, icon: markRaw(Activity), bgColor: 'bg-blue-100', iconColor: 'text-blue-600' },
  { label: 'Active Users', value: '1,247', trend: 8, icon: markRaw(Users), bgColor: 'bg-green-100', iconColor: 'text-green-600' },
  { label: 'Avg Confidence', value: '82%', trend: 3, icon: markRaw(TrendingUp), bgColor: 'bg-purple-100', iconColor: 'text-purple-600' },
  { label: 'Avg Response Time', value: '2.3s', trend: -15, icon: markRaw(Clock), bgColor: 'bg-orange-100', iconColor: 'text-orange-600' }
])

const topConditions = ref([
  { name: 'Tension Headache', count: 245, percentage: 100 },
  { name: 'Common Cold', count: 198, percentage: 81 },
  { name: 'Gastritis', count: 156, percentage: 64 },
  { name: 'Anxiety Disorder', count: 134, percentage: 55 },
  { name: 'Lower Back Pain', count: 112, percentage: 46 }
])

const urgencyStats = ref([
  { level: 'routine', count: 2847, bgClass: 'bg-green-100 dark:bg-green-900/30', textClass: 'text-green-700 dark:text-green-400' },
  { level: 'soon', count: 654, bgClass: 'bg-yellow-100 dark:bg-yellow-900/30', textClass: 'text-yellow-700 dark:text-yellow-400' },
  { level: 'urgent', count: 289, bgClass: 'bg-orange-100 dark:bg-orange-900/30', textClass: 'text-orange-700 dark:text-orange-400' },
  { level: 'emergency', count: 57, bgClass: 'bg-red-100 dark:bg-red-900/30', textClass: 'text-red-700 dark:text-red-400' }
])
</script>
