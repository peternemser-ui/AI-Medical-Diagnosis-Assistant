<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-4xl mx-auto px-4">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-6">Diagnosis History</h1>

      <div class="mb-6 flex gap-4">
        <input v-model="searchQuery" type="search" placeholder="Search diagnoses..." class="flex-1 px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
        <select v-model="urgencyFilter" class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          <option value="">All urgency levels</option>
          <option value="routine">Routine</option>
          <option value="soon">Soon</option>
          <option value="urgent">Urgent</option>
          <option value="emergency">Emergency</option>
        </select>
      </div>

      <div v-if="filteredHistory.length === 0" class="bg-white dark:bg-gray-800 rounded-xl p-12 text-center">
        <svg class="mx-auto w-16 h-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">No diagnosis history</h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">Start your first diagnosis to see your history here.</p>
        <router-link to="/" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Start Diagnosis</router-link>
      </div>

      <div v-else class="space-y-4">
        <div v-for="item in filteredHistory" :key="item.id" class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
          <div class="flex justify-between items-start mb-4">
            <div>
              <span :class="['px-2 py-1 text-xs rounded-full', urgencyClasses[item.urgency]]">{{ item.urgency }}</span>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">{{ formatDate(item.createdAt) }}</p>
            </div>
            <div class="text-right">
              <p class="font-semibold text-gray-900 dark:text-white">{{ item.conditions[0]?.name }}</p>
              <p class="text-sm text-blue-600">{{ item.conditions[0]?.confidence }}% confidence</p>
            </div>
          </div>
          <p class="text-gray-600 dark:text-gray-400 text-sm mb-4">{{ item.symptomDescription }}</p>
          <div class="flex gap-2">
            <button @click="viewDetails(item)" class="text-sm text-blue-600 hover:text-blue-700">View Details</button>
            <button @click="exportDiagnosis(item)" class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-700">Export</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const urgencyFilter = ref('')

const history = ref([
  { id: '1', urgency: 'routine', createdAt: '2024-01-20', conditions: [{ name: 'Tension Headache', confidence: 85 }], symptomDescription: 'Headache for 2 days' },
  { id: '2', urgency: 'urgent', createdAt: '2024-01-18', conditions: [{ name: 'Acute Gastritis', confidence: 72 }], symptomDescription: 'Severe stomach pain' }
])

const urgencyClasses = {
  routine: 'bg-green-100 text-green-800',
  soon: 'bg-yellow-100 text-yellow-800',
  urgent: 'bg-orange-100 text-orange-800',
  emergency: 'bg-red-100 text-red-800'
}

const filteredHistory = computed(() => {
  return history.value.filter(item => {
    const matchesSearch = !searchQuery.value || item.symptomDescription.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesUrgency = !urgencyFilter.value || item.urgency === urgencyFilter.value
    return matchesSearch && matchesUrgency
  })
})

const formatDate = (date) => new Date(date).toLocaleDateString()
const viewDetails = (item) => console.log('View:', item)
const exportDiagnosis = (item) => console.log('Export:', item)
</script>
