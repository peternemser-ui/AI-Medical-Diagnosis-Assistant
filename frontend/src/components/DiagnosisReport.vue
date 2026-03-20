<template>
  <div class="diagnosis-report" style="background: #fff; color: #1a1a1a; font-family: 'Segoe UI', Arial, sans-serif; padding: 32px; max-width: 800px; margin: 0 auto; line-height: 1.6;">

    <!-- Header -->
    <div style="border-bottom: 3px solid #2563eb; padding-bottom: 16px; margin-bottom: 24px;">
      <h1 style="font-size: 22px; font-weight: 700; color: #1e3a5f; margin: 0 0 4px 0;">AI Medical Assessment Report</h1>
      <div style="display: flex; justify-content: space-between; font-size: 12px; color: #6b7280;">
        <span>Generated: {{ reportDate }}</span>
        <span v-if="patientInfo.age || patientInfo.gender">
          Patient: {{ patientInfo.age ? patientInfo.age + ' years' : '' }}{{ patientInfo.age && patientInfo.gender ? ' / ' : '' }}{{ patientInfo.gender || '' }}
        </span>
      </div>
    </div>

    <!-- Patient Summary -->
    <div v-if="diagnosisData.patientSummary" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Patient Summary</h2>
      <p style="font-size: 13px; color: #374151; white-space: pre-wrap; margin: 0;">{{ diagnosisData.patientSummary }}</p>
    </div>

    <!-- Differential Diagnoses Table -->
    <div v-if="diagnosisData.causes && diagnosisData.causes.length" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Differential Diagnoses</h2>
      <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
        <thead>
          <tr style="background: #f3f4f6;">
            <th style="text-align: left; padding: 8px; border: 1px solid #d1d5db; font-weight: 600;">#</th>
            <th style="text-align: left; padding: 8px; border: 1px solid #d1d5db; font-weight: 600;">Condition</th>
            <th style="text-align: center; padding: 8px; border: 1px solid #d1d5db; font-weight: 600;">Confidence</th>
            <th style="text-align: center; padding: 8px; border: 1px solid #d1d5db; font-weight: 600;">Urgency</th>
            <th style="text-align: left; padding: 8px; border: 1px solid #d1d5db; font-weight: 600;">Specialty</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(cause, i) in diagnosisData.causes" :key="i">
            <td style="padding: 8px; border: 1px solid #d1d5db;">{{ i + 1 }}</td>
            <td style="padding: 8px; border: 1px solid #d1d5db; font-weight: 600;">{{ cause.cause || cause.condition }}</td>
            <td style="padding: 8px; border: 1px solid #d1d5db; text-align: center;">{{ cause.value || cause.confidence }}%</td>
            <td style="padding: 8px; border: 1px solid #d1d5db; text-align: center;">
              <span :style="{ color: urgencyColor(cause.urgency) }">{{ cause.urgency || 'routine' }}</span>
            </td>
            <td style="padding: 8px; border: 1px solid #d1d5db;">{{ cause.specialty || 'Primary Care' }}</td>
          </tr>
        </tbody>
      </table>
      <!-- Reasoning details -->
      <div v-for="(cause, i) in diagnosisData.causes" :key="'r'+i" style="margin-top: 8px;">
        <div v-if="cause.explanation" style="font-size: 11px; color: #4b5563; margin-bottom: 6px;">
          <strong>{{ cause.cause || cause.condition }}:</strong> {{ cause.explanation }}
        </div>
      </div>
    </div>

    <!-- Red Flags -->
    <div v-if="diagnosisData.redFlags && diagnosisData.redFlags.length" style="margin-bottom: 24px; background: #fef2f2; border: 1px solid #fca5a5; border-radius: 6px; padding: 12px 16px;">
      <h2 style="font-size: 14px; font-weight: 700; color: #991b1b; margin: 0 0 8px 0;">Warning Signs / Red Flags</h2>
      <ul style="margin: 0; padding-left: 20px;">
        <li v-for="flag in diagnosisData.redFlags" :key="flag" style="font-size: 12px; color: #7f1d1d; margin-bottom: 4px;">{{ flag }}</li>
      </ul>
    </div>

    <!-- Recommended Tests -->
    <div v-if="diagnosisData.recommendedTests && diagnosisData.recommendedTests.length" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Recommended Tests</h2>
      <ul style="margin: 0; padding-left: 20px;">
        <li v-for="test in diagnosisData.recommendedTests" :key="test" style="font-size: 12px; color: #374151; margin-bottom: 4px;">{{ test }}</li>
      </ul>
    </div>

    <!-- Treatment Recommendations -->
    <div v-if="diagnosisData.actionChecklist && diagnosisData.actionChecklist.length" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Treatment Recommendations / Action Checklist</h2>
      <ol style="margin: 0; padding-left: 20px;">
        <li v-for="(item, i) in diagnosisData.actionChecklist" :key="i" style="font-size: 12px; color: #374151; margin-bottom: 4px;">
          {{ typeof item === 'string' ? item : item.action || JSON.stringify(item) }}
        </li>
      </ol>
    </div>

    <!-- Medications -->
    <div v-if="diagnosisData.medications && diagnosisData.medications.length" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Medications</h2>
      <ul style="margin: 0; padding-left: 20px;">
        <li v-for="med in diagnosisData.medications" :key="typeof med === 'string' ? med : med.name" style="font-size: 12px; color: #374151; margin-bottom: 4px;">
          <template v-if="typeof med === 'object'">
            <strong>{{ med.name || med.medication }}</strong>: {{ med.dose || med.dosage || '' }}
          </template>
          <template v-else>{{ med }}</template>
        </li>
      </ul>
    </div>

    <!-- Safety Review -->
    <div v-if="diagnosisData.safetyStatus" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Safety Review</h2>
      <p style="font-size: 12px; margin: 0 0 8px 0;">
        Status:
        <span :style="{ fontWeight: 700, color: diagnosisData.safetyStatus === 'PASS' ? '#059669' : '#d97706' }">
          {{ diagnosisData.safetyStatus }}
        </span>
      </p>
      <ul v-if="diagnosisData.safetyWarnings && diagnosisData.safetyWarnings.length" style="margin: 0; padding-left: 20px;">
        <li v-for="w in diagnosisData.safetyWarnings" :key="w" style="font-size: 12px; color: #92400e; margin-bottom: 4px;">{{ w }}</li>
      </ul>
    </div>

    <!-- Warning Signs -->
    <div v-if="diagnosisData.warningSignsList && diagnosisData.warningSignsList.length" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">When to Seek Immediate Care</h2>
      <ul style="margin: 0; padding-left: 20px;">
        <li v-for="s in diagnosisData.warningSignsList" :key="typeof s === 'string' ? s : JSON.stringify(s)" style="font-size: 12px; color: #991b1b; margin-bottom: 4px;">
          {{ typeof s === 'string' ? s : JSON.stringify(s) }}
        </li>
      </ul>
    </div>

    <!-- Lifestyle Recommendations -->
    <div v-if="diagnosisData.lifestyleRecommendations && diagnosisData.lifestyleRecommendations.length" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Lifestyle Recommendations</h2>
      <ul style="margin: 0; padding-left: 20px;">
        <li v-for="r in diagnosisData.lifestyleRecommendations" :key="r" style="font-size: 12px; color: #374151; margin-bottom: 4px;">{{ r }}</li>
      </ul>
    </div>

    <!-- Follow-up Timeline -->
    <div v-if="diagnosisData.followUpTimeline" style="margin-bottom: 24px;">
      <h2 style="font-size: 15px; font-weight: 700; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 8px 0; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px;">Follow-up Timeline</h2>
      <p style="font-size: 12px; color: #374151; margin: 0;">{{ typeof diagnosisData.followUpTimeline === 'string' ? diagnosisData.followUpTimeline : JSON.stringify(diagnosisData.followUpTimeline) }}</p>
    </div>

    <!-- Agent Analysis Summary -->
    <div v-if="diagnosisData.totalTime" style="margin-bottom: 24px; background: #f9fafb; border-radius: 6px; padding: 10px 16px;">
      <p style="font-size: 11px; color: #6b7280; margin: 0;">
        Analyzed by {{ (diagnosisData.agentsUsed || []).length }} AI agents in {{ diagnosisData.totalTime.toFixed(1) }}s
        <span v-if="diagnosisData.agentsUsed && diagnosisData.agentsUsed.length">
          ({{ diagnosisData.agentsUsed.join(', ') }})
        </span>
      </p>
    </div>

    <!-- Footer / Disclaimer -->
    <div style="border-top: 2px solid #e5e7eb; padding-top: 16px; margin-top: 24px;">
      <p style="font-size: 11px; color: #9ca3af; margin: 0 0 4px 0; font-style: italic;">
        DISCLAIMER: This AI-generated medical assessment is for informational purposes only.
        It is NOT a substitute for professional medical care, diagnosis, or treatment.
        Always consult a qualified healthcare provider for medical advice.
        In emergencies, call your local emergency services immediately.
      </p>
      <p style="font-size: 10px; color: #d1d5db; margin: 0; text-align: right;">
        Generated by AI Medical Diagnosis Assistant
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  diagnosisData: {
    type: Object,
    required: true
  },
  patientInfo: {
    type: Object,
    default: () => ({ age: '', gender: '', symptoms: '' })
  }
})

const reportDate = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
})

function urgencyColor(urgency) {
  if (!urgency) return '#374151'
  const u = urgency.toLowerCase()
  if (u.includes('immediate') || u.includes('emergency') || u.includes('urgent')) return '#dc2626'
  if (u.includes('soon') || u.includes('within')) return '#d97706'
  return '#059669'
}
</script>
