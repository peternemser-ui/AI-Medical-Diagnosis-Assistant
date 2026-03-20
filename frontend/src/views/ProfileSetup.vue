<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDark ? 'bg-slate-950' : 'bg-white'">
    <!-- Ambient background -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-blue-600/5' : 'bg-blue-400/10'"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 rounded-full blur-[120px]"
        :class="isDark ? 'bg-purple-600/5' : 'bg-purple-400/10'"></div>
    </div>

    <!-- Nav bar -->
    <nav class="relative z-20 flex items-center justify-between px-6 py-3 border-b"
      :class="isDark ? 'border-slate-800 bg-slate-950/80 backdrop-blur-xl' : 'border-slate-200 bg-white/80 backdrop-blur-xl'">
      <router-link to="/" class="flex items-center gap-2">
        <div class="p-1.5 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"/>
          </svg>
        </div>
        <span class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Medical AI</span>
      </router-link>
      <ThemeLangControls />
    </nav>

    <!-- Main content -->
    <div class="relative z-10 flex justify-center px-4 py-10">
      <div class="max-w-lg w-full space-y-6">
        <!-- Title -->
        <div class="text-center">
          <div class="inline-flex p-3 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-xl shadow-blue-500/20 mb-5">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          <h1 class="text-2xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Profile Setup</h1>
          <p class="text-sm mt-1" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Set up your profile for a personalized experience</p>
        </div>

        <!-- Form Card -->
        <div class="backdrop-blur-xl rounded-2xl border shadow-2xl overflow-hidden"
          :class="isDark ? 'bg-slate-900/80 border-slate-800' : 'bg-white/80 border-slate-200'">
          <div class="p-6 space-y-6">

            <!-- Basic Info Section -->
            <div>
              <h3 class="text-xs uppercase tracking-wider font-semibold mb-4"
                :class="isDark ? 'text-slate-500' : 'text-slate-400'">Basic Information</h3>
              <div class="space-y-4">
                <!-- Name -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Name <span class="text-red-400">*</span>
                  </label>
                  <input
                    v-model="form.name"
                    type="text"
                    placeholder="Your full name"
                    @blur="nameBlurred = true"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="[
                      isDark ? 'bg-slate-800/80 border text-white placeholder-slate-600' : 'bg-slate-50 border text-slate-900 placeholder-slate-400',
                      nameBlurred && !form.name.trim() ? 'border-red-500/50 ring-1 ring-red-500/20' : (isDark ? 'border-slate-700/50' : 'border-slate-200')
                    ]"
                  />
                  <p v-if="nameBlurred && !form.name.trim()" class="text-[11px] text-red-400 mt-1">Name is required</p>
                </div>
                <!-- Email -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Email <span class="text-slate-600 text-[10px]">(optional)</span>
                  </label>
                  <input
                    v-model="form.email"
                    type="email"
                    placeholder="your@email.com"
                    @blur="emailBlurred = true"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="[
                      isDark ? 'bg-slate-800/80 border text-white placeholder-slate-600' : 'bg-slate-50 border text-slate-900 placeholder-slate-400',
                      emailBlurred && form.email && !isValidEmail(form.email) ? 'border-amber-500/50 ring-1 ring-amber-500/20' : (isDark ? 'border-slate-700/50' : 'border-slate-200')
                    ]"
                  />
                  <p v-if="emailBlurred && form.email && !isValidEmail(form.email)" class="text-[11px] text-amber-400 mt-1">Please enter a valid email address</p>
                </div>
                <!-- Gender -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Gender</label>
                  <select
                    v-model="form.gender"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white'
                      : 'bg-slate-50 border border-slate-200 text-slate-900'"
                  >
                    <option value="">Select gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                    <option value="prefer_not_to_say">Prefer not to say</option>
                  </select>
                </div>
                <!-- Date of Birth -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Date of Birth</label>
                  <input
                    v-model="form.dateOfBirth"
                    type="date"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white'
                      : 'bg-slate-50 border border-slate-200 text-slate-900'"
                  />
                </div>
              </div>
            </div>

            <!-- Medical Info Section -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-xs uppercase tracking-wider font-semibold"
                  :class="isDark ? 'text-slate-500' : 'text-slate-400'">Medical Information</h3>
                <span class="text-[10px] px-2 py-0.5 rounded-full"
                  :class="isDark ? 'bg-slate-800 text-slate-500' : 'bg-slate-100 text-slate-400'">Optional</span>
              </div>
              <div class="space-y-4">
                <!-- Blood Type -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Blood Type</label>
                  <select
                    v-model="form.bloodType"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white'
                      : 'bg-slate-50 border border-slate-200 text-slate-900'"
                  >
                    <option value="">Select blood type</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </select>
                </div>
                <!-- Allergies -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Allergies <span class="text-[10px] font-normal" :class="isDark ? 'text-slate-600' : 'text-slate-400'">(comma-separated)</span>
                  </label>
                  <input
                    v-model="allergiesText"
                    type="text"
                    placeholder="e.g. Penicillin, Peanuts, Latex"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
                <!-- Current Medications -->
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                    Current Medications <span class="text-[10px] font-normal" :class="isDark ? 'text-slate-600' : 'text-slate-400'">(comma-separated)</span>
                  </label>
                  <input
                    v-model="medicationsText"
                    type="text"
                    placeholder="e.g. Lisinopril, Metformin"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
              </div>
            </div>

            <!-- Emergency Contact Section -->
            <div>
              <h3 class="text-xs uppercase tracking-wider font-semibold mb-4"
                :class="isDark ? 'text-slate-500' : 'text-slate-400'">Emergency Contact</h3>
              <div class="space-y-4">
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Contact Name</label>
                  <input
                    v-model="form.emergencyContactName"
                    type="text"
                    placeholder="Emergency contact name"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
                <div>
                  <label class="text-xs font-medium mb-1.5 block" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Contact Phone</label>
                  <input
                    v-model="form.emergencyContactPhone"
                    type="tel"
                    placeholder="+1 (555) 000-0000"
                    class="w-full rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-transparent transition-all"
                    :class="isDark
                      ? 'bg-slate-800/80 border border-slate-700/50 text-white placeholder-slate-600'
                      : 'bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400'"
                  />
                </div>
              </div>
            </div>

            <!-- Privacy Note -->
            <div class="flex items-start gap-2 p-3 rounded-lg"
              :class="isDark ? 'bg-blue-500/10 border border-blue-500/20' : 'bg-blue-50 border border-blue-200'">
              <svg class="w-4 h-4 flex-shrink-0 mt-0.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              <p class="text-xs" :class="isDark ? 'text-blue-300/80' : 'text-blue-600'">
                Stored locally on your device only. Your medical information is never sent to any server.
              </p>
            </div>

            <!-- Error message -->
            <div v-if="error" class="flex items-start gap-2 p-3 bg-red-500/10 border border-red-500/20 rounded-lg">
              <svg class="w-4 h-4 text-red-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              <p class="text-red-300 text-xs">{{ error }}</p>
            </div>

            <!-- Save Button -->
            <button
              @click="handleSave"
              :disabled="!form.name.trim()"
              class="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed text-white font-medium py-3 rounded-xl text-sm transition-all duration-200 flex items-center justify-center gap-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              Save Profile
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from '@/composables/useTheme.js'
import { getProfile, saveProfile } from '@/services/userService.js'
import ThemeLangControls from '@/components/ThemeLangControls.vue'

export default {
  name: 'ProfileSetup',
  components: { ThemeLangControls },
  setup() {
    const router = useRouter()
    const { isDark } = useTheme()
    const error = ref('')
    const nameBlurred = ref(false)
    const emailBlurred = ref(false)

    function isValidEmail(email) {
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
    }

    const form = ref({
      name: '',
      email: '',
      gender: '',
      dateOfBirth: '',
      bloodType: '',
      emergencyContactName: '',
      emergencyContactPhone: '',
    })

    const allergiesText = ref('')
    const medicationsText = ref('')

    onMounted(() => {
      const profile = getProfile()
      form.value.name = profile.name || ''
      form.value.email = profile.email || ''
      form.value.gender = profile.gender || ''
      form.value.dateOfBirth = profile.dateOfBirth || ''
      form.value.bloodType = profile.bloodType || ''
      form.value.emergencyContactName = profile.emergencyContactName || ''
      form.value.emergencyContactPhone = profile.emergencyContactPhone || ''
      allergiesText.value = (profile.allergies || []).join(', ')
      medicationsText.value = (profile.medications || []).join(', ')
    })

    function parseCommaSeparated(text) {
      if (!text.trim()) return []
      return text.split(',').map(s => s.trim()).filter(Boolean)
    }

    function handleSave() {
      error.value = ''
      if (!form.value.name.trim()) {
        error.value = 'Name is required.'
        return
      }

      const data = {
        ...form.value,
        allergies: parseCommaSeparated(allergiesText.value),
        medications: parseCommaSeparated(medicationsText.value),
        emergencyContact: form.value.emergencyContactName
          ? `${form.value.emergencyContactName}${form.value.emergencyContactPhone ? ' - ' + form.value.emergencyContactPhone : ''}`
          : '',
      }

      saveProfile(data)
      router.push('/consult')
    }

    return {
      isDark,
      form,
      allergiesText,
      medicationsText,
      error,
      nameBlurred,
      emailBlurred,
      isValidEmail,
      handleSave,
    }
  }
}
</script>
