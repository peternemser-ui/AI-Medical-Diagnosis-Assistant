<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="visible" class="fixed inset-0 z-[9999] flex items-center justify-center p-4"
        @click.self="$emit('close')">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

        <!-- Modal -->
        <div class="relative w-full max-w-3xl max-h-[90vh] overflow-hidden rounded-2xl border shadow-2xl flex flex-col"
          :class="isDark
            ? 'bg-slate-900 border-slate-700/50'
            : 'bg-white border-slate-200'">

          <!-- Header -->
          <div class="flex-shrink-0 px-6 py-5 border-b"
            :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg shadow-emerald-500/20">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                </div>
                <div>
                  <h2 class="text-lg font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Find Specialists</h2>
                  <p class="text-xs mt-0.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Recommended based on your diagnosis</p>
                </div>
              </div>
              <button @click="$emit('close')"
                class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors"
                :class="isDark ? 'hover:bg-slate-700 text-slate-400' : 'hover:bg-slate-100 text-slate-500'">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <!-- Appointment type selector -->
            <div class="flex flex-wrap gap-2 mt-4">
              <button v-for="apt in appointmentTypes" :key="apt.key"
                @click="selectedType = apt.key"
                class="px-3 py-1.5 text-xs font-semibold rounded-lg border transition-all"
                :class="selectedType === apt.key
                  ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-400'
                  : isDark
                    ? 'bg-slate-800/60 border-slate-700/50 text-slate-400 hover:border-slate-600'
                    : 'bg-slate-50 border-slate-200 text-slate-600 hover:border-slate-300'">
                {{ apt.label }}
              </button>
            </div>

            <!-- Search bar -->
            <div class="flex gap-3 mt-4">
              <div class="flex-1 relative">
                <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4"
                  :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                <input v-model="locationQuery" type="text"
                  placeholder="Zip code, city, or state (e.g. 10001, Chicago, NY)"
                  class="w-full pl-10 pr-4 py-2.5 text-sm rounded-xl border transition-colors"
                  :class="isDark
                    ? 'bg-slate-800/60 border-slate-700/50 text-white placeholder:text-slate-500 focus:border-emerald-500/50'
                    : 'bg-slate-50 border-slate-200 text-slate-900 placeholder:text-slate-400 focus:border-emerald-500'"
                  @keydown.enter="searchDoctors"
                />
              </div>
              <button @click="searchDoctors"
                :disabled="loading"
                class="px-5 py-2.5 text-sm font-semibold rounded-xl bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-700 hover:to-teal-600 text-white shadow-lg shadow-emerald-500/20 transition-all disabled:opacity-60 flex items-center gap-2">
                <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                Search
              </button>
            </div>
          </div>

          <!-- Specialty tag -->
          <div v-if="specialty" class="flex-shrink-0 px-6 py-3 border-b"
            :class="isDark ? 'border-slate-700/30 bg-slate-800/30' : 'border-slate-100 bg-slate-50/50'">
            <div class="flex items-center gap-2 text-xs">
              <svg class="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
              <span class="font-semibold" :class="isDark ? 'text-emerald-400' : 'text-emerald-700'">
                Searching for: {{ specialty }}
              </span>
              <span :class="isDark ? 'text-slate-500' : 'text-slate-400'">|</span>
              <span :class="isDark ? 'text-slate-400' : 'text-slate-600'">
                {{ doctors.length }} provider{{ doctors.length !== 1 ? 's' : '' }} found
              </span>
            </div>
          </div>

          <!-- Results -->
          <div class="flex-1 overflow-y-auto px-6 py-4 space-y-3" style="min-height: 200px">
            <!-- Loading state -->
            <div v-if="loading" class="flex flex-col items-center justify-center py-16 gap-3">
              <div class="w-10 h-10 border-3 border-emerald-500/30 border-t-emerald-500 rounded-full animate-spin"></div>
              <p class="text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                Searching NPI registry...
              </p>
            </div>

            <!-- Empty state -->
            <div v-else-if="searched && doctors.length === 0" class="flex flex-col items-center justify-center py-16 gap-3">
              <div class="w-14 h-14 rounded-full flex items-center justify-center"
                :class="isDark ? 'bg-slate-800' : 'bg-slate-100'">
                <svg class="w-7 h-7" :class="isDark ? 'text-slate-600' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
              </div>
              <p class="text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                No providers found. Try a different location or broader search.
              </p>
            </div>

            <!-- Initial state -->
            <div v-else-if="!searched" class="flex flex-col items-center justify-center py-16 gap-3">
              <div class="w-14 h-14 rounded-full flex items-center justify-center"
                :class="isDark ? 'bg-emerald-500/10' : 'bg-emerald-50'">
                <svg class="w-7 h-7 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
              <p class="text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">
                Enter a location to find {{ specialty || 'healthcare' }} providers near you.
              </p>
            </div>

            <!-- Doctor cards -->
            <div v-else class="space-y-3">
              <div v-for="doc in doctors" :key="doc.npi"
                class="rounded-xl border p-4 transition-all"
                :class="isDark
                  ? 'bg-slate-800/40 border-slate-700/40 hover:border-slate-600/60'
                  : 'bg-white border-slate-200 hover:border-slate-300 hover:shadow-md'">
                <div class="flex items-start gap-4">
                  <!-- Avatar -->
                  <div class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 text-lg font-bold"
                    :class="isDark
                      ? 'bg-gradient-to-br from-emerald-500/20 to-teal-500/20 text-emerald-400'
                      : 'bg-gradient-to-br from-emerald-50 to-teal-50 text-emerald-700'">
                    {{ getInitials(doc.name) }}
                  </div>

                  <!-- Info -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-start justify-between gap-2">
                      <div>
                        <h3 class="text-sm font-bold truncate" :class="isDark ? 'text-white' : 'text-slate-900'">
                          {{ doc.name }}
                        </h3>
                        <p class="text-xs mt-0.5" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">
                          {{ doc.specialty }}
                        </p>
                      </div>
                      <span v-if="doc.accepting_patients"
                        class="flex-shrink-0 px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-full"
                        :class="isDark ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700'">
                        Accepting
                      </span>
                    </div>

                    <!-- Address -->
                    <div class="flex items-start gap-1.5 mt-2">
                      <svg class="w-3.5 h-3.5 mt-0.5 flex-shrink-0" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                      </svg>
                      <span class="text-xs leading-relaxed" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
                        {{ formatAddress(doc.address) }}
                      </span>
                    </div>

                    <!-- Phone -->
                    <div v-if="doc.phone" class="flex items-center gap-1.5 mt-1.5">
                      <svg class="w-3.5 h-3.5 flex-shrink-0" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                      </svg>
                      <span class="text-xs font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-600'">
                        {{ formatPhone(doc.phone) }}
                      </span>
                    </div>

                    <!-- Actions -->
                    <div class="flex items-center gap-2 mt-3">
                      <a v-if="doc.phone" :href="'tel:' + doc.phone"
                        class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors"
                        :class="isDark
                          ? 'bg-blue-500/15 text-blue-400 hover:bg-blue-500/25'
                          : 'bg-blue-50 text-blue-700 hover:bg-blue-100'">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                        </svg>
                        Call Office
                      </a>
                      <a :href="getDirectionsUrl(doc.address)" target="_blank" rel="noopener"
                        class="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors"
                        :class="isDark
                          ? 'bg-purple-500/15 text-purple-400 hover:bg-purple-500/25'
                          : 'bg-purple-50 text-purple-700 hover:bg-purple-100'">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"/>
                        </svg>
                        Get Directions
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="flex-shrink-0 px-6 py-3 border-t text-center"
            :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
            <p class="text-[10px] leading-relaxed"
              :class="isDark ? 'text-slate-500' : 'text-slate-400'">
              Provider data sourced from the CMS NPI Registry. Verify availability directly with the provider's office.
            </p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

const props = defineProps({
  visible: { type: Boolean, default: false },
  specialty: { type: String, default: '' },
})

defineEmits(['close'])

const appointmentTypes = [
  { key: 'emergency', label: 'Emergency' },
  { key: 'urgent_care', label: 'Urgent Care' },
  { key: 'specialist', label: 'Specialist Visit' },
  { key: 'telehealth', label: 'Telehealth' },
  { key: 'follow_up', label: 'Follow-up' },
]

const selectedType = ref('specialist')
const locationQuery = ref('')
const loading = ref(false)
const searched = ref(false)
const doctors = ref([])
const error = ref('')

// Reset state when modal opens
watch(() => props.visible, (val) => {
  if (val) {
    searched.value = false
    doctors.value = []
    error.value = ''
  }
})

async function searchDoctors() {
  if (loading.value) return
  loading.value = true
  searched.value = true
  error.value = ''
  doctors.value = []

  try {
    const params = new URLSearchParams({
      specialty: props.specialty || 'Primary Care',
      location: locationQuery.value.trim(),
      limit: '12',
    })
    const resp = await fetch(`${API_BASE_URL}/api/find-doctors?${params}`, {
      headers: { 'Content-Type': 'application/json' },
    })
    if (!resp.ok) throw new Error(`Request failed: ${resp.status}`)
    const data = await resp.json()
    doctors.value = data.results || []
  } catch (e) {
    error.value = e.message
    doctors.value = []
  } finally {
    loading.value = false
  }
}

function getInitials(name) {
  // Strip credentials after comma
  const clean = name.split(',')[0].trim()
  const parts = clean.split(' ').filter(Boolean)
  if (parts.length >= 2) return parts[0][0] + parts[parts.length - 1][0]
  return parts[0]?.[0] || '?'
}

function formatAddress(addr) {
  if (!addr) return 'Address not available'
  return addr.replace(/\n/g, ', ')
}

function formatPhone(phone) {
  if (!phone) return ''
  const digits = phone.replace(/\D/g, '')
  if (digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`
  }
  return phone
}

function getDirectionsUrl(address) {
  if (!address) return '#'
  const query = address.replace(/\n/g, ', ')
  return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(query)}`
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-active > div:last-child,
.modal-leave-active > div:last-child {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from > div:last-child,
.modal-leave-to > div:last-child {
  transform: scale(0.95) translateY(10px);
  opacity: 0;
}
</style>
