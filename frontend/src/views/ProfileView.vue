<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ $t('profile.title') || 'Profile Settings' }}
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          {{ $t('profile.subtitle') || 'Manage your account settings and preferences' }}
        </p>
      </div>

      <!-- Profile Card -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
        <!-- Avatar Section -->
        <div class="p-6 bg-gradient-to-r from-blue-500 to-blue-600">
          <div class="flex items-center space-x-4">
            <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center text-2xl font-bold text-blue-600">
              {{ userInitials }}
            </div>
            <div class="text-white">
              <h2 class="text-xl font-semibold">{{ userName }}</h2>
              <p class="opacity-90">{{ userEmail }}</p>
            </div>
          </div>
        </div>

        <!-- Form Sections -->
        <div class="p-6 space-y-8">
          <!-- Personal Information -->
          <section>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              {{ $t('profile.personalInfo') || 'Personal Information' }}
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ $t('profile.fullName') || 'Full Name' }}
                </label>
                <input
                  v-model="profile.name"
                  type="text"
                  class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ $t('profile.email') || 'Email' }}
                </label>
                <input
                  v-model="profile.email"
                  type="email"
                  disabled
                  class="w-full px-4 py-2 border rounded-lg bg-gray-100 dark:bg-gray-600 dark:border-gray-600 dark:text-gray-300 cursor-not-allowed"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ $t('profile.dateOfBirth') || 'Date of Birth' }}
                </label>
                <input
                  v-model="profile.dateOfBirth"
                  type="date"
                  class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ $t('profile.gender') || 'Gender' }}
                </label>
                <select
                  v-model="profile.gender"
                  class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                >
                  <option value="">{{ $t('profile.selectGender') || 'Select gender' }}</option>
                  <option value="male">{{ $t('profile.male') || 'Male' }}</option>
                  <option value="female">{{ $t('profile.female') || 'Female' }}</option>
                  <option value="other">{{ $t('profile.other') || 'Other' }}</option>
                  <option value="prefer-not-to-say">{{ $t('profile.preferNotToSay') || 'Prefer not to say' }}</option>
                </select>
              </div>
            </div>
          </section>

          <!-- Medical Information -->
          <section class="pt-6 border-t border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              {{ $t('profile.medicalInfo') || 'Medical Information' }}
            </h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ $t('profile.allergies') || 'Known Allergies' }}
                </label>
                <textarea
                  v-model="profile.allergies"
                  rows="2"
                  class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  :placeholder="$t('profile.allergiesPlaceholder') || 'List any known allergies...'"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ $t('profile.medications') || 'Current Medications' }}
                </label>
                <textarea
                  v-model="profile.medications"
                  rows="2"
                  class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  :placeholder="$t('profile.medicationsPlaceholder') || 'List current medications...'"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  {{ $t('profile.conditions') || 'Medical Conditions' }}
                </label>
                <textarea
                  v-model="profile.conditions"
                  rows="2"
                  class="w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                  :placeholder="$t('profile.conditionsPlaceholder') || 'List any medical conditions...'"
                ></textarea>
              </div>
            </div>
          </section>

          <!-- Preferences -->
          <section class="pt-6 border-t border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">
              {{ $t('profile.preferences') || 'Preferences' }}
            </h3>
            <div class="space-y-4">
              <label class="flex items-center">
                <input
                  v-model="profile.emailNotifications"
                  type="checkbox"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded"
                />
                <span class="ml-3 text-gray-700 dark:text-gray-300">
                  {{ $t('profile.emailNotifications') || 'Email notifications for health reminders' }}
                </span>
              </label>
              <label class="flex items-center">
                <input
                  v-model="profile.shareData"
                  type="checkbox"
                  class="w-4 h-4 text-blue-600 border-gray-300 rounded"
                />
                <span class="ml-3 text-gray-700 dark:text-gray-300">
                  {{ $t('profile.shareData') || 'Share anonymized data for research' }}
                </span>
              </label>
            </div>
          </section>

          <!-- Actions -->
          <div class="pt-6 border-t border-gray-200 dark:border-gray-700 flex justify-between">
            <button
              @click="openChangePassword"
              class="px-4 py-2 text-blue-600 hover:text-blue-700 font-medium"
            >
              {{ $t('profile.changePassword') || 'Change Password' }}
            </button>
            <button
              @click="saveProfile"
              :disabled="isSaving"
              class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg disabled:opacity-50"
            >
              {{ isSaving ? ($t('profile.saving') || 'Saving...') : ($t('profile.saveChanges') || 'Save Changes') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Danger Zone -->
      <div class="mt-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <h3 class="text-lg font-medium text-red-600 mb-4">
          {{ $t('profile.dangerZone') || 'Danger Zone' }}
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          {{ $t('profile.deleteAccountWarning') || 'Once you delete your account, there is no going back. Please be certain.' }}
        </p>
        <button
          @click="confirmDeleteAccount"
          class="px-4 py-2 border border-red-500 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg"
        >
          {{ $t('profile.deleteAccount') || 'Delete Account' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'

const { user, userName, userEmail } = useAuth()

const profile = reactive({
  name: '',
  email: '',
  dateOfBirth: '',
  gender: '',
  allergies: '',
  medications: '',
  conditions: '',
  emailNotifications: true,
  shareData: false
})

const isSaving = ref(false)

const userInitials = computed(() => {
  if (!userName.value) return '?'
  return userName.value
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

onMounted(() => {
  if (user.value) {
    profile.name = user.value.name || ''
    profile.email = user.value.email || ''
  }
})

async function saveProfile() {
  isSaving.value = true
  try {
    // Save profile to backend
    await new Promise(resolve => setTimeout(resolve, 1000))
    // Show success message
  } catch (error) {
    console.error('Failed to save profile:', error)
  } finally {
    isSaving.value = false
  }
}

function openChangePassword() {
  // Open password change modal
}

function confirmDeleteAccount() {
  if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
    // Delete account
  }
}
</script>
