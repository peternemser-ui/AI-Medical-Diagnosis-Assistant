<template>
  <div class="health-timeline">
    <!-- Header -->
    <div class="timeline-header">
      <MaterialIcon icon="timeline" class="header-icon" />
      <h2 class="header-title">Health History Timeline</h2>
      <p class="header-subtitle">Your diagnosis journey over time</p>
    </div>

    <!-- Empty State -->
    <div v-if="!diagnoses || diagnoses.length === 0" class="empty-state">
      <MaterialIcon icon="event_note" class="empty-icon" />
      <p class="empty-text">No diagnosis history yet</p>
      <p class="empty-subtext">Complete your first diagnosis to see it here</p>
    </div>

    <!-- Timeline -->
    <div v-else class="timeline-container">
      <!-- Timeline Line -->
      <div class="timeline-line"></div>

      <!-- Timeline Items -->
      <div
        v-for="(diagnosis, index) in sortedDiagnoses"
        :key="index"
        class="timeline-item"
        :class="{ 'is-latest': index === 0 }"
      >
        <!-- Timeline Dot -->
        <div class="timeline-dot" :style="{ background: getColorForIndex(index) }">
          <MaterialIcon icon="local_hospital" class="dot-icon" />
        </div>

        <!-- Timeline Content -->
        <div class="timeline-content">
          <!-- Date Badge -->
          <div class="date-badge" :style="{ borderColor: getColorForIndex(index) }">
            <MaterialIcon icon="calendar_today" class="date-icon" />
            <span class="date-text">{{ formatDate(diagnosis.timestamp) }}</span>
            <span v-if="index === 0" class="latest-badge">Latest</span>
          </div>

          <!-- Diagnosis Card -->
          <div class="diagnosis-card">
            <!-- Top Diagnoses -->
            <div class="diagnoses-list">
              <div
                v-for="(diag, dIndex) in diagnosis.diagnoses.slice(0, 3)"
                :key="dIndex"
                class="diagnosis-item"
              >
                <div class="diagnosis-info">
                  <span class="diagnosis-name">{{ diag.condition }}</span>
                  <div class="confidence-bar-container">
                    <div
                      class="confidence-bar"
                      :style="{
                        width: diag.confidence + '%',
                        background: getConfidenceColor(diag.confidence)
                      }"
                    ></div>
                    <span class="confidence-text">{{ diag.confidence }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Symptoms Summary -->
            <div class="symptoms-summary">
              <MaterialIcon icon="medical_information" class="summary-icon" />
              <div class="summary-content">
                <span class="summary-label">Symptoms:</span>
                <span class="summary-text">{{ getSymptomsText(diagnosis) }}</span>
              </div>
            </div>

            <!-- Patient Info -->
            <div class="patient-info">
              <div class="info-item">
                <MaterialIcon icon="person" class="info-icon" />
                <span>{{ diagnosis.age }}yo {{ diagnosis.gender }}</span>
              </div>
              <div v-if="diagnosis.urgency" class="info-item urgency">
                <MaterialIcon icon="warning" class="info-icon" />
                <span>{{ diagnosis.urgency }}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="action-buttons">
              <button
                @click="viewDetails(diagnosis)"
                class="action-btn view-btn"
              >
                <MaterialIcon icon="visibility" class="btn-icon" />
                View Details
              </button>
              <button
                @click="compareWith(diagnosis)"
                class="action-btn compare-btn"
                v-if="index > 0"
              >
                <MaterialIcon icon="compare_arrows" class="btn-icon" />
                Compare
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Section -->
    <div v-if="diagnoses && diagnoses.length > 0" class="statistics-section">
      <h3 class="stats-title">
        <MaterialIcon icon="analytics" class="stats-icon" />
        Timeline Statistics
      </h3>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">{{ diagnoses.length }}</div>
          <div class="stat-label">Total Diagnoses</div>
          <MaterialIcon icon="medical_services" class="stat-icon-bg" />
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ getTotalSymptoms() }}</div>
          <div class="stat-label">Symptoms Tracked</div>
          <MaterialIcon icon="fact_check" class="stat-icon-bg" />
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ getDaysSinceFirst() }}</div>
          <div class="stat-label">Days Tracking</div>
          <MaterialIcon icon="event" class="stat-icon-bg" />
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ getAverageConfidence() }}%</div>
          <div class="stat-label">Avg Confidence</div>
          <MaterialIcon icon="trending_up" class="stat-icon-bg" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import MaterialIcon from './MaterialIcon.vue'

const diagnoses = ref([])

// Load diagnoses from localStorage
onMounted(() => {
  loadDiagnosisHistory()
})

const loadDiagnosisHistory = () => {
  try {
    const historyJson = localStorage.getItem('diagnosisHistory')
    if (historyJson) {
      diagnoses.value = JSON.parse(historyJson)
    } else {
      // Try to load current diagnosis for backward compatibility
      const currentDiagnosis = localStorage.getItem('diagnosisData')
      if (currentDiagnosis) {
        const data = JSON.parse(currentDiagnosis)
        if (!data.timestamp) {
          data.timestamp = new Date().toISOString()
        }
        diagnoses.value = [data]
        // Save to history
        localStorage.setItem('diagnosisHistory', JSON.stringify(diagnoses.value))
      }
    }
  } catch (error) {
    console.error('Error loading diagnosis history:', error)
    diagnoses.value = []
  }
}

// Computed: Sort diagnoses by date (newest first)
const sortedDiagnoses = computed(() => {
  return [...diagnoses.value].sort((a, b) => {
    const dateA = new Date(a.timestamp || 0)
    const dateB = new Date(b.timestamp || 0)
    return dateB - dateA
  })
})

// Format date for display
const formatDate = (timestamp) => {
  if (!timestamp) return 'Unknown date'
  
  const date = new Date(timestamp)
  const now = new Date()
  const diffTime = now - date
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return 'Today'
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays} days ago`
  } else if (diffDays < 30) {
    const weeks = Math.floor(diffDays / 7)
    return `${weeks} week${weeks > 1 ? 's' : ''} ago`
  } else if (diffDays < 365) {
    const months = Math.floor(diffDays / 30)
    return `${months} month${months > 1 ? 's' : ''} ago`
  } else {
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    })
  }
}

// Get color for timeline item based on index
const getColorForIndex = (index) => {
  const colors = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', // Purple (latest)
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)', // Pink
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', // Blue
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)', // Green
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)', // Orange
    'linear-gradient(135deg, #30cfd0 0%, #330867 100%)', // Teal
  ]
  return colors[index % colors.length]
}

// Get confidence color
const getConfidenceColor = (confidence) => {
  if (confidence >= 75) {
    return 'linear-gradient(90deg, #10b981 0%, #059669 100%)'
  } else if (confidence >= 50) {
    return 'linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)'
  } else if (confidence >= 30) {
    return 'linear-gradient(90deg, #f59e0b 0%, #d97706 100%)'
  } else {
    return 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)'
  }
}

// Get symptoms text
const getSymptomsText = (diagnosis) => {
  if (diagnosis.symptoms && typeof diagnosis.symptoms === 'string') {
    return diagnosis.symptoms.length > 100 
      ? diagnosis.symptoms.substring(0, 100) + '...'
      : diagnosis.symptoms
  }
  return 'No symptoms recorded'
}

// Statistics functions
const getTotalSymptoms = () => {
  return diagnoses.value.reduce((total, diag) => {
    if (diag.symptoms && typeof diag.symptoms === 'string') {
      // Count number of symptom phrases (split by comma or period)
      return total + diag.symptoms.split(/[,.]/).filter(s => s.trim()).length
    }
    return total
  }, 0)
}

const getDaysSinceFirst = () => {
  if (diagnoses.value.length === 0) return 0
  
  const dates = diagnoses.value
    .map(d => new Date(d.timestamp || 0))
    .sort((a, b) => a - b)
  
  const firstDate = dates[0]
  const now = new Date()
  const diffTime = now - firstDate
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  return diffDays
}

const getAverageConfidence = () => {
  if (diagnoses.value.length === 0) return 0
  
  let totalConfidence = 0
  let count = 0
  
  diagnoses.value.forEach(diag => {
    if (diag.diagnoses && Array.isArray(diag.diagnoses)) {
      diag.diagnoses.forEach(d => {
        if (d.confidence) {
          totalConfidence += d.confidence
          count++
        }
      })
    }
  })
  
  return count > 0 ? Math.round(totalConfidence / count) : 0
}

// Action handlers
const viewDetails = (diagnosis) => {
  // Store this diagnosis as current and navigate to dashboard
  localStorage.setItem('diagnosisData', JSON.stringify(diagnosis))
  window.location.reload()
}

const compareWith = (diagnosis) => {
  // Future feature: Compare two diagnoses
  alert('Compare feature coming soon! This will show differences between diagnoses.')
}
</script>

<style scoped>
.health-timeline {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Header */
.timeline-header {
  text-align: center;
  margin-bottom: 3rem;
}

.header-icon {
  font-size: 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.header-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.header-subtitle {
  font-size: 1rem;
  color: #6b7280;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 1rem;
  border: 2px dashed #d1d5db;
}

.empty-icon {
  font-size: 4rem;
  color: #9ca3af;
  margin-bottom: 1rem;
}

.empty-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: #4b5563;
  margin-bottom: 0.5rem;
}

.empty-subtext {
  font-size: 0.875rem;
  color: #6b7280;
}

/* Timeline Container */
.timeline-container {
  position: relative;
  padding-left: 3rem;
}

.timeline-line {
  position: absolute;
  left: 1.25rem;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #e5e7eb 100%);
  border-radius: 2px;
}

/* Timeline Item */
.timeline-item {
  position: relative;
  margin-bottom: 2.5rem;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.timeline-item.is-latest .timeline-dot {
  width: 2.5rem;
  height: 2.5rem;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(102, 126, 234, 0.1);
  }
}

.timeline-dot {
  position: absolute;
  left: -2.5rem;
  top: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.dot-icon {
  font-size: 1rem;
  color: white;
}

/* Timeline Content */
.timeline-content {
  margin-left: 1.5rem;
}

.date-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 2px solid;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.date-icon {
  font-size: 1rem;
}

.latest-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  margin-left: 0.5rem;
}

/* Diagnosis Card */
.diagnosis-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 1px 3px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.diagnosis-card:hover {
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);
  transform: translateY(-2px);
}

/* Diagnoses List */
.diagnoses-list {
  margin-bottom: 1.5rem;
}

.diagnosis-item {
  margin-bottom: 1rem;
}

.diagnosis-item:last-child {
  margin-bottom: 0;
}

.diagnosis-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.diagnosis-name {
  font-size: 1rem;
  font-weight: 600;
  color: #1f2937;
}

.confidence-bar-container {
  position: relative;
  width: 100%;
  height: 1.5rem;
  background: #f3f4f6;
  border-radius: 0.75rem;
  overflow: hidden;
}

.confidence-bar {
  height: 100%;
  border-radius: 0.75rem;
  transition: width 0.5s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 0.5rem;
}

.confidence-text {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* Symptoms Summary */
.symptoms-summary {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  border-radius: 0.75rem;
  margin-bottom: 1rem;
}

.summary-icon {
  font-size: 1.5rem;
  color: #667eea;
  flex-shrink: 0;
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.summary-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.summary-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.5;
}

/* Patient Info */
.patient-info {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.75rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
}

.info-item.urgency {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  font-weight: 600;
}

.info-icon {
  font-size: 1rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.compare-btn {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.compare-btn:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
}

.btn-icon {
  font-size: 1.125rem;
}

/* Statistics Section */
.statistics-section {
  margin-top: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
  border-radius: 1rem;
  border: 2px solid #e5e7eb;
}

.stats-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.stats-icon {
  font-size: 1.75rem;
  color: #667eea;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.stat-card {
  position: relative;
  padding: 1.5rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  z-index: 10;
  position: relative;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  z-index: 10;
  position: relative;
}

.stat-icon-bg {
  position: absolute;
  right: -0.5rem;
  bottom: -0.5rem;
  font-size: 4rem;
  color: #f3f4f6;
  opacity: 0.5;
  z-index: 1;
}

/* Responsive */
@media (max-width: 640px) {
  .health-timeline {
    padding: 1rem 0.5rem;
  }

  .timeline-container {
    padding-left: 2rem;
  }

  .timeline-line {
    left: 0.75rem;
  }

  .timeline-dot {
    left: -1.75rem;
    width: 1.5rem;
    height: 1.5rem;
  }

  .dot-icon {
    font-size: 0.875rem;
  }

  .timeline-item.is-latest .timeline-dot {
    width: 2rem;
    height: 2rem;
  }

  .diagnosis-card {
    padding: 1rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
