<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm">
    <!-- Filters -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center space-x-4">
      <select
        v-model="actionFilter"
        class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
      >
        <option value="">All Actions</option>
        <option value="login">Login</option>
        <option value="logout">Logout</option>
        <option value="diagnosis">Diagnosis</option>
        <option value="profile_update">Profile Update</option>
        <option value="settings_change">Settings Change</option>
        <option value="user_create">User Create</option>
        <option value="user_delete">User Delete</option>
      </select>
      <select
        v-model="levelFilter"
        class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
      >
        <option value="">All Levels</option>
        <option value="info">Info</option>
        <option value="warning">Warning</option>
        <option value="error">Error</option>
      </select>
      <input
        v-model="dateFilter"
        type="date"
        class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
      />
      <button
        @click="exportLogs"
        class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
      >
        Export CSV
      </button>
    </div>

    <!-- Logs Table -->
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Timestamp</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">User</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Action</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Level</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">Details</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase">IP Address</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr v-for="log in filteredLogs" :key="log.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
            <td class="px-6 py-4 text-sm text-gray-900 dark:text-white whitespace-nowrap">
              {{ formatTimestamp(log.timestamp) }}
            </td>
            <td class="px-6 py-4">
              <div class="text-sm text-gray-900 dark:text-white">{{ log.userName }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ log.userEmail }}</div>
            </td>
            <td class="px-6 py-4 text-sm text-gray-900 dark:text-white">
              {{ log.action }}
            </td>
            <td class="px-6 py-4">
              <span :class="getLevelClass(log.level)">{{ log.level }}</span>
            </td>
            <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400 max-w-xs truncate">
              {{ log.details }}
            </td>
            <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
              {{ log.ipAddress }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-between items-center">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Showing {{ filteredLogs.length }} logs
      </p>
      <div class="flex space-x-2">
        <button
          @click="loadMore"
          class="px-4 py-2 border rounded-lg dark:border-gray-600 dark:text-white hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          Load More
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const actionFilter = ref('')
const levelFilter = ref('')
const dateFilter = ref('')

const logs = ref([
  { id: '1', timestamp: '2024-01-20T10:30:00', userName: 'John Doe', userEmail: 'john@example.com', action: 'login', level: 'info', details: 'Successful login from Chrome on Windows', ipAddress: '192.168.1.100' },
  { id: '2', timestamp: '2024-01-20T10:32:00', userName: 'John Doe', userEmail: 'john@example.com', action: 'diagnosis', level: 'info', details: 'Created new diagnosis request', ipAddress: '192.168.1.100' },
  { id: '3', timestamp: '2024-01-20T10:35:00', userName: 'Admin', userEmail: 'admin@example.com', action: 'settings_change', level: 'warning', details: 'Modified AI temperature setting', ipAddress: '192.168.1.1' },
  { id: '4', timestamp: '2024-01-20T09:15:00', userName: 'Jane Smith', userEmail: 'jane@example.com', action: 'login', level: 'error', details: 'Failed login attempt - invalid password', ipAddress: '192.168.1.50' },
  { id: '5', timestamp: '2024-01-20T09:00:00', userName: 'System', userEmail: 'system', action: 'user_create', level: 'info', details: 'New user registered: mike@example.com', ipAddress: 'N/A' }
])

const filteredLogs = computed(() => {
  return logs.value.filter(log => {
    if (actionFilter.value && log.action !== actionFilter.value) return false
    if (levelFilter.value && log.level !== levelFilter.value) return false
    return true
  })
})

function getLevelClass(level) {
  const classes = {
    info: 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800',
    warning: 'px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800',
    error: 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-800'
  }
  return classes[level] || classes.info
}

function formatTimestamp(timestamp) {
  return new Date(timestamp).toLocaleString()
}

function exportLogs() {
  console.log('Exporting logs...')
}

function loadMore() {
  console.log('Loading more logs...')
}
</script>
