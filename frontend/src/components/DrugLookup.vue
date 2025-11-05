<template>
  <div class="drug-lookup-container">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center shadow-lg">
          <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"/>
          </svg>
        </div>
        <div>
          <h2 class="text-2xl font-bold text-white">💊 Drug Information</h2>
          <p class="text-sm text-gray-300">Search medications and check interactions</p>
        </div>
      </div>
      <button 
        @click="$emit('close')"
        class="p-2 hover:bg-white/10 rounded-lg transition-colors"
        title="Close"
      >
        <svg class="w-6 h-6 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Search Section -->
    <div class="search-section mb-6">
      <div class="relative">
        <input
          v-model="searchQuery"
          @keyup.enter="searchDrug"
          type="text"
          placeholder="Search for a medication (e.g., 'aspirin', 'lisinopril')..."
          class="w-full px-4 py-3 pl-12 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
        />
        <svg class="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
        </svg>
      </div>
      
      <button
        @click="searchDrug"
        :disabled="isLoading || !searchQuery.trim()"
        class="mt-3 w-full px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl transform hover:scale-[1.02]"
      >
        <span v-if="!isLoading">🔍 Search Drug Database</span>
        <span v-else class="flex items-center justify-center gap-2">
          <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Searching RxNorm Database...
        </span>
      </button>
    </div>

    <!-- Search Results -->
    <div v-if="searchResults.length > 0" class="search-results mb-6">
      <h3 class="text-lg font-semibold text-white mb-3 flex items-center gap-2">
        <svg class="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        Found {{ searchResults.length }} medication(s)
      </h3>
      
      <div class="space-y-2 max-h-64 overflow-y-auto custom-scrollbar">
        <div 
          v-for="drug in searchResults" 
          :key="drug.rxcui"
          @click="addToSelected(drug)"
          class="drug-result-card p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-lg hover:bg-white/10 hover:border-purple-500/50 cursor-pointer transition-all group"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h4 class="font-semibold text-white group-hover:text-purple-300 transition-colors">{{ drug.name }}</h4>
              <p class="text-xs text-gray-400 mt-1">RxCUI: {{ drug.rxcui }} • Type: {{ drug.tty }}</p>
            </div>
            <svg class="w-5 h-5 text-gray-400 group-hover:text-purple-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="searchPerformed && !isLoading" class="text-center py-8 text-gray-400">
      <svg class="w-16 h-16 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
      <p>No medications found for "{{ lastSearchQuery }}"</p>
      <p class="text-sm mt-1">Try searching for the generic name or brand name</p>
    </div>

    <!-- Selected Medications -->
    <div v-if="selectedDrugs.length > 0" class="selected-drugs mb-6">
      <h3 class="text-lg font-semibold text-white mb-3 flex items-center gap-2">
        <svg class="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
          <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
        </svg>
        Selected Medications ({{ selectedDrugs.length }})
      </h3>
      
      <div class="space-y-2 mb-4">
        <div 
          v-for="drug in selectedDrugs" 
          :key="drug.rxcui"
          class="selected-drug-card p-3 bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-400/30 rounded-lg flex items-center justify-between"
        >
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-500/30 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div>
              <p class="font-semibold text-white">{{ drug.name }}</p>
              <p class="text-xs text-gray-300">RxCUI: {{ drug.rxcui }}</p>
            </div>
          </div>
          <button
            @click="removeFromSelected(drug.rxcui)"
            class="p-2 hover:bg-red-500/20 rounded-lg transition-colors group"
            title="Remove"
          >
            <svg class="w-5 h-5 text-gray-400 group-hover:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
      </div>
      
      <button
        v-if="selectedDrugs.length >= 2"
        @click="checkInteractions"
        :disabled="isCheckingInteractions"
        class="w-full px-6 py-3 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-xl font-semibold hover:from-orange-700 hover:to-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        <span v-if="!isCheckingInteractions">⚠️ Check Drug Interactions</span>
        <span v-else>Checking interactions...</span>
      </button>
    </div>

    <!-- Interaction Results -->
    <div v-if="interactionResults" class="interaction-results">
      <div v-if="interactionResults.has_interactions" class="bg-red-500/20 border border-red-500/50 rounded-xl p-5 mb-4">
        <div class="flex items-start gap-3 mb-4">
          <svg class="w-8 h-8 text-red-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
          </svg>
          <div class="flex-1">
            <h3 class="text-xl font-bold text-red-300 mb-2">
              ⚠️ {{ interactionResults.interaction_count }} Drug Interaction(s) Found
            </h3>
            <p class="text-red-200 text-sm">
              The selected medications may interact with each other. Consult your doctor or pharmacist.
            </p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div 
            v-for="(interaction, idx) in interactionResults.interactions" 
            :key="idx"
            class="interaction-card bg-black/20 rounded-lg p-4 border-l-4"
            :class="{
              'border-red-500': interaction.severity === 'high',
              'border-orange-500': interaction.severity === 'moderate',
              'border-yellow-500': interaction.severity === 'low'
            }"
          >
            <div class="flex items-start justify-between mb-2">
              <div class="flex items-center gap-2">
                <span 
                  class="px-2 py-1 rounded text-xs font-bold"
                  :class="{
                    'bg-red-500 text-white': interaction.severity === 'high',
                    'bg-orange-500 text-white': interaction.severity === 'moderate',
                    'bg-yellow-500 text-black': interaction.severity === 'low'
                  }"
                >
                  {{ interaction.severity ? interaction.severity.toUpperCase() : 'UNKNOWN' }}
                </span>
              </div>
            </div>
            <p class="text-sm text-gray-200 mb-2">
              <strong class="text-white">{{ interaction.drug1 }}</strong> ↔️ <strong class="text-white">{{ interaction.drug2 }}</strong>
            </p>
            <p class="text-sm text-gray-300">{{ interaction.description }}</p>
          </div>
        </div>
      </div>
      
      <div v-else class="bg-green-500/20 border border-green-500/50 rounded-xl p-5">
        <div class="flex items-center gap-3">
          <svg class="w-8 h-8 text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          <div>
            <h3 class="text-xl font-bold text-green-300 mb-1">✅ No Known Interactions</h3>
            <p class="text-green-200 text-sm">
              No major drug-drug interactions found between the selected medications.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Info Box -->
    <div class="info-box mt-6 bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
      <div class="flex items-start gap-3">
        <svg class="w-6 h-6 text-blue-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
        </svg>
        <div class="flex-1 text-sm text-blue-200">
          <p class="font-semibold mb-1">About This Tool</p>
          <p class="text-blue-300">
            Drug information is sourced from <strong>RxNorm</strong>, a standardized nomenclature for clinical drugs maintained by the U.S. National Library of Medicine.
            Always consult your healthcare provider before starting or stopping any medication.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineEmits(['close'])

const searchQuery = ref('')
const lastSearchQuery = ref('')
const searchResults = ref([])
const selectedDrugs = ref([])
const interactionResults = ref(null)
const isLoading = ref(false)
const isCheckingInteractions = ref(false)
const searchPerformed = ref(false)

async function searchDrug() {
  if (!searchQuery.value.trim()) return
  
  isLoading.value = true
  searchPerformed.value = true
  lastSearchQuery.value = searchQuery.value
  interactionResults.value = null
  
  try {
    const response = await fetch('http://localhost:8000/api/drugs/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ drug_name: searchQuery.value })
    })
    
    const data = await response.json()
    
    if (data.success) {
      searchResults.value = data.drugs || []
    } else {
      searchResults.value = []
    }
  } catch (error) {
    console.error('Drug search error:', error)
    searchResults.value = []
  } finally {
    isLoading.value = false
  }
}

function addToSelected(drug) {
  // Check if already selected
  if (selectedDrugs.value.find(d => d.rxcui === drug.rxcui)) {
    return
  }
  
  selectedDrugs.value.push(drug)
  interactionResults.value = null // Clear old interaction results
}

function removeFromSelected(rxcui) {
  selectedDrugs.value = selectedDrugs.value.filter(d => d.rxcui !== rxcui)
  interactionResults.value = null
}

async function checkInteractions() {
  if (selectedDrugs.value.length < 2) return
  
  isCheckingInteractions.value = true
  
  try {
    const drug_ids = selectedDrugs.value.map(d => d.rxcui)
    
    const response = await fetch('http://localhost:8000/api/drugs/interactions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ drug_ids })
    })
    
    const data = await response.json()
    
    if (data.success) {
      interactionResults.value = data
    }
  } catch (error) {
    console.error('Interaction check error:', error)
  } finally {
    isCheckingInteractions.value = false
  }
}
</script>

<style scoped>
.drug-lookup-container {
  max-width: 800px;
  margin: 0 auto;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.5);
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 92, 246, 0.7);
}

.drug-result-card {
  transition: all 0.2s ease;
}

.drug-result-card:active {
  transform: scale(0.98);
}

.selected-drug-card {
  animation: slide-in 0.3s ease-out;
}

@keyframes slide-in {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.interaction-card {
  animation: fade-in 0.4s ease-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
