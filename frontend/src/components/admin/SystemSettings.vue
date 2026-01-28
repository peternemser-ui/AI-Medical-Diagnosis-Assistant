<template>
  <div class="space-y-6">
    <!-- AI Configuration -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">AI Configuration</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">AI Model</label>
          <select v-model="settings.aiModel" class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
            <option value="gpt-4o">GPT-4o (Recommended)</option>
            <option value="gpt-4-turbo">GPT-4 Turbo</option>
            <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Temperature</label>
          <input
            v-model.number="settings.temperature"
            type="range"
            min="0"
            max="1"
            step="0.1"
            class="w-full"
          />
          <p class="text-sm text-gray-500 mt-1">Current: {{ settings.temperature }}</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Max Tokens</label>
          <input
            v-model.number="settings.maxTokens"
            type="number"
            min="100"
            max="4000"
            class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>
      </div>
    </div>

    <!-- Rate Limiting -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Rate Limiting</h3>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Requests per minute (per user)</label>
          <input
            v-model.number="settings.rateLimitPerUser"
            type="number"
            class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Global rate limit</label>
          <input
            v-model.number="settings.rateLimitGlobal"
            type="number"
            class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>
      </div>
    </div>

    <!-- Security Settings -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Security</h3>
      <div class="space-y-4">
        <label class="flex items-center">
          <input v-model="settings.requireEmailVerification" type="checkbox" class="w-4 h-4 text-blue-600 rounded" />
          <span class="ml-3 text-gray-700 dark:text-gray-300">Require email verification</span>
        </label>
        <label class="flex items-center">
          <input v-model="settings.enable2FA" type="checkbox" class="w-4 h-4 text-blue-600 rounded" />
          <span class="ml-3 text-gray-700 dark:text-gray-300">Enable two-factor authentication option</span>
        </label>
        <label class="flex items-center">
          <input v-model="settings.auditLogging" type="checkbox" class="w-4 h-4 text-blue-600 rounded" />
          <span class="ml-3 text-gray-700 dark:text-gray-300">Enable audit logging</span>
        </label>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Session timeout (minutes)</label>
          <input
            v-model.number="settings.sessionTimeout"
            type="number"
            class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>
      </div>
    </div>

    <!-- Notification Settings -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Notifications</h3>
      <div class="space-y-4">
        <label class="flex items-center">
          <input v-model="settings.emailOnUrgent" type="checkbox" class="w-4 h-4 text-blue-600 rounded" />
          <span class="ml-3 text-gray-700 dark:text-gray-300">Email admins on urgent diagnoses</span>
        </label>
        <label class="flex items-center">
          <input v-model="settings.emailOnEmergency" type="checkbox" class="w-4 h-4 text-blue-600 rounded" />
          <span class="ml-3 text-gray-700 dark:text-gray-300">Email admins on emergency cases</span>
        </label>
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Admin notification email</label>
          <input
            v-model="settings.adminEmail"
            type="email"
            class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="flex justify-end">
      <button
        @click="saveSettings"
        :disabled="isSaving"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {{ isSaving ? 'Saving...' : 'Save Settings' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

const isSaving = ref(false)

const settings = reactive({
  aiModel: 'gpt-4o',
  temperature: 0.3,
  maxTokens: 2000,
  rateLimitPerUser: 20,
  rateLimitGlobal: 1000,
  requireEmailVerification: true,
  enable2FA: false,
  auditLogging: true,
  sessionTimeout: 30,
  emailOnUrgent: true,
  emailOnEmergency: true,
  adminEmail: 'admin@example.com'
})

async function saveSettings() {
  isSaving.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    console.log('Settings saved:', settings)
  } finally {
    isSaving.value = false
  }
}
</script>
