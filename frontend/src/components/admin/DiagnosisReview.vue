<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm flex items-center space-x-4">
      <select
        v-model="urgencyFilter"
        class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
      >
        <option value="">All Urgency Levels</option>
        <option value="emergency">Emergency</option>
        <option value="urgent">Urgent</option>
        <option value="soon">Soon</option>
        <option value="routine">Routine</option>
      </select>
      <select
        v-model="statusFilter"
        class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
      >
        <option value="">All Statuses</option>
        <option value="pending">Pending Review</option>
        <option value="reviewed">Reviewed</option>
        <option value="archived">Archived</option>
      </select>
      <input
        v-model="dateFilter"
        type="date"
        class="px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
      />
    </div>

    <!-- Diagnosis Cards -->
    <div class="grid gap-4">
      <div
        v-for="diagnosis in filteredDiagnoses"
        :key="diagnosis.id"
        class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm"
      >
        <div class="flex justify-between items-start mb-4">
          <div>
            <div class="flex items-center space-x-2">
              <span :class="getUrgencyClass(diagnosis.urgency)">
                {{ diagnosis.urgency }}
              </span>
              <span :class="getStatusClass(diagnosis.status)">
                {{ diagnosis.status }}
              </span>
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mt-2">
              {{ diagnosis.patientName }}
            </h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">
              {{ formatDate(diagnosis.createdAt) }}
            </p>
          </div>
          <div class="text-right">
            <p class="text-sm text-gray-600 dark:text-gray-400">Top Condition</p>
            <p class="font-semibold text-gray-900 dark:text-white">
              {{ diagnosis.conditions[0]?.name }}
            </p>
            <p class="text-sm text-blue-600">
              {{ diagnosis.conditions[0]?.confidence }}% confidence
            </p>
          </div>
        </div>

        <!-- Symptoms -->
        <div class="mb-4">
          <p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Reported Symptoms:</p>
          <p class="text-gray-600 dark:text-gray-400">{{ diagnosis.symptoms }}</p>
        </div>

        <!-- Red Flags -->
        <div v-if="diagnosis.redFlags.length > 0" class="mb-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
          <p class="text-sm font-medium text-red-700 dark:text-red-400 mb-1">Red Flags:</p>
          <ul class="text-sm text-red-600 dark:text-red-400 list-disc list-inside">
            <li v-for="flag in diagnosis.redFlags" :key="flag">{{ flag }}</li>
          </ul>
        </div>

        <!-- Actions -->
        <div class="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700">
          <div class="flex space-x-2">
            <button
              @click="viewDetails(diagnosis)"
              class="px-4 py-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg"
            >
              View Details
            </button>
            <button
              @click="contactPatient(diagnosis)"
              class="px-4 py-2 text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 rounded-lg"
            >
              Contact Patient
            </button>
          </div>
          <div class="flex space-x-2">
            <button
              @click="markReviewed(diagnosis)"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Mark Reviewed
            </button>
            <button
              @click="escalate(diagnosis)"
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Escalate
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const urgencyFilter = ref('')
const statusFilter = ref('')
const dateFilter = ref('')

const diagnoses = ref([
  {
    id: '1',
    patientName: 'John Doe',
    urgency: 'urgent',
    status: 'pending',
    symptoms: 'Severe chest pain, shortness of breath, sweating',
    conditions: [{ name: 'Acute Coronary Syndrome', confidence: 78 }],
    redFlags: ['Chest pain radiating to arm', 'Diaphoresis'],
    createdAt: '2024-01-20T10:30:00'
  },
  {
    id: '2',
    patientName: 'Jane Smith',
    urgency: 'routine',
    status: 'pending',
    symptoms: 'Persistent headache for 3 days, mild nausea',
    conditions: [{ name: 'Tension Headache', confidence: 85 }],
    redFlags: [],
    createdAt: '2024-01-20T09:15:00'
  }
])

const filteredDiagnoses = computed(() => {
  return diagnoses.value.filter(d => {
    if (urgencyFilter.value && d.urgency !== urgencyFilter.value) return false
    if (statusFilter.value && d.status !== statusFilter.value) return false
    return true
  })
})

function getUrgencyClass(urgency) {
  const classes = {
    emergency: 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-800 font-medium',
    urgent: 'px-2 py-1 text-xs rounded-full bg-orange-100 text-orange-800 font-medium',
    soon: 'px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800 font-medium',
    routine: 'px-2 py-1 text-xs rounded-full bg-green-100 text-green-800 font-medium'
  }
  return classes[urgency] || classes.routine
}

function getStatusClass(status) {
  const classes = {
    pending: 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800',
    reviewed: 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800',
    archived: 'px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800'
  }
  return classes[status] || classes.pending
}

function formatDate(date) {
  return new Date(date).toLocaleString()
}

function viewDetails(diagnosis) {
  console.log('View details:', diagnosis)
}

function contactPatient(diagnosis) {
  console.log('Contact patient:', diagnosis)
}

function markReviewed(diagnosis) {
  diagnosis.status = 'reviewed'
}

function escalate(diagnosis) {
  console.log('Escalate:', diagnosis)
}
</script>
