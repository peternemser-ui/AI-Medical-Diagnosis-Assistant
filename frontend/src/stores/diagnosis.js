import { defineStore } from 'pinia'

export const useDiagnosisStore = defineStore('diagnosis', {
  state: () => ({
    result: null,
  }),
  getters: {
    causes(state) {
      return state.result?.causes || []
    },
    topDiagnosis(state) {
      const c = state.result?.causes
      return c && c.length > 0 ? c[0] : null
    },
    agentTimings(state) {
      return state.result?.agent_timings || state.result?.agentTimings || {}
    },
    totalTime(state) {
      return state.result?.total_time || state.result?.totalTime || 0
    },
    agentsUsed(state) {
      return state.result?.agents_used || state.result?.agentsUsed || []
    },
    agentDetails(state) {
      return state.result?.agent_details || state.result?.agentDetails || {}
    },
    recommendedTests(state) {
      return state.result?.recommended_tests || state.result?.recommendedTests || []
    },
    redFlags(state) {
      return state.result?.red_flags || state.result?.redFlags || []
    },
    actionChecklist(state) {
      return state.result?.action_checklist || state.result?.actionChecklist || []
    },
    safetyStatus(state) {
      return state.result?.safety_status || state.result?.safetyStatus || ''
    },
    safetyWarnings(state) {
      return state.result?.safety_warnings || state.result?.safetyWarnings || []
    },
    medications(state) {
      return state.result?.medications || []
    },
    lifestyleRecommendations(state) {
      return state.result?.lifestyle_recommendations || state.result?.lifestyleRecommendations || []
    },
    warningSignsList(state) {
      return state.result?.warning_signs || state.result?.warningSignsList || []
    },
    followUpTimeline(state) {
      return state.result?.follow_up_timeline || state.result?.followUpTimeline || ''
    },
    patientSummary(state) {
      return state.result?.patient_summary || state.result?.patientSummary || ''
    },
    confidenceScores(state) {
      return state.result?.confidence_scores || state.result?.confidenceScores || {}
    },
    overallUrgency(state) {
      const causes = state.result?.causes || []
      if (causes.length === 0) return 'routine'
      // Return highest urgency among causes
      const urgencies = causes.map(c => c.urgency || 'routine')
      if (urgencies.includes('emergency')) return 'emergency'
      if (urgencies.includes('urgent')) return 'urgent'
      if (urgencies.includes('soon')) return 'soon'
      return 'routine'
    },
    patientInfo(state) {
      return {
        age: state.result?.age || state.result?.patientAge || '',
        gender: state.result?.gender || state.result?.patientGender || '',
        symptoms: state.result?.symptoms || state.result?.chiefComplaint || '',
        date: state.result?.date || state.result?.timestamp || new Date().toISOString()
      }
    }
  },
  actions: {
    setResult(data) {
      this.result = data
    },
    loadFromLocalStorage() {
      try {
        const raw = localStorage.getItem('latest_diagnosis_result')
        if (raw) {
          this.result = JSON.parse(raw)
        }
      } catch (e) {
        console.error('Failed to load diagnosis from localStorage:', e)
      }
    },
    saveToLocalStorage() {
      try {
        if (this.result) {
          localStorage.setItem('latest_diagnosis_result', JSON.stringify(this.result))
        }
      } catch (e) {
        console.error('Failed to save diagnosis to localStorage:', e)
      }
    }
  },
})
