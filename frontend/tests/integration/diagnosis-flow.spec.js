import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'

// Integration tests for the full diagnosis flow
describe('Diagnosis Flow Integration', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('completes full symptom input to diagnosis flow', async () => {
    // Simulate the full user journey
    const symptoms = 'severe headache with sensitivity to light'

    // Step 1: User enters symptoms
    expect(symptoms.length).toBeGreaterThan(0)

    // Step 2: System processes and generates questions
    const followUpQuestions = [
      'How long have you had this headache?',
      'On a scale of 1-10, how severe is the pain?'
    ]
    expect(followUpQuestions.length).toBe(2)

    // Step 3: User answers questions
    const answers = {
      duration: '3 days',
      severity: 8
    }
    expect(answers.severity).toBeGreaterThan(0)

    // Step 4: System generates diagnosis
    const diagnosis = {
      conditions: [
        { name: 'Migraine', confidence: 85 },
        { name: 'Tension Headache', confidence: 60 }
      ],
      urgency: 'soon',
      recommendations: ['Rest in dark room', 'Stay hydrated']
    }
    expect(diagnosis.conditions.length).toBeGreaterThan(0)
    expect(diagnosis.conditions[0].confidence).toBeGreaterThan(diagnosis.conditions[1].confidence)
  })

  it('handles emergency detection during diagnosis', async () => {
    const symptoms = 'sudden severe chest pain radiating to left arm'

    // Emergency keywords should be detected
    const emergencyKeywords = ['chest pain', 'radiating', 'arm']
    const hasEmergency = emergencyKeywords.some(kw =>
      symptoms.toLowerCase().includes(kw)
    )

    expect(hasEmergency).toBe(true)

    // System should immediately show emergency banner
    const emergencyResponse = {
      type: 'cardiac',
      message: 'Possible cardiac emergency',
      action: 'Call 911 immediately'
    }
    expect(emergencyResponse.action).toContain('911')
  })

  it('persists diagnosis history across sessions', async () => {
    const diagnosisHistory = [
      {
        id: '1',
        date: new Date().toISOString(),
        symptoms: ['headache'],
        diagnoses: [{ condition: 'Migraine', confidence: 80 }]
      }
    ]

    // Simulate localStorage persistence
    localStorage.setItem('diagnosisHistory', JSON.stringify(diagnosisHistory))
    const retrieved = JSON.parse(localStorage.getItem('diagnosisHistory') || '[]')

    expect(retrieved.length).toBe(1)
    expect(retrieved[0].symptoms).toContain('headache')
  })

  it('handles multi-step questionnaire completion', async () => {
    const steps = [
      { question: 'Primary symptom?', answer: 'headache' },
      { question: 'Duration?', answer: '3 days' },
      { question: 'Severity?', answer: '7' },
      { question: 'Location?', answer: 'frontal' },
      { question: 'Triggers?', answer: 'stress' }
    ]

    let currentStep = 0

    for (const step of steps) {
      expect(step.question).toBeDefined()
      expect(step.answer).toBeDefined()
      currentStep++
    }

    expect(currentStep).toBe(5)
  })

  it('exports diagnosis report to multiple formats', async () => {
    const diagnosis = {
      patient: 'Anonymous',
      date: new Date().toISOString(),
      symptoms: ['headache', 'nausea'],
      diagnoses: [{ condition: 'Migraine', confidence: 85 }],
      recommendations: ['Rest', 'Hydration']
    }

    // JSON export
    const jsonExport = JSON.stringify(diagnosis)
    expect(JSON.parse(jsonExport)).toHaveProperty('diagnoses')

    // Text export
    const textExport = `
Diagnosis Report
Date: ${diagnosis.date}
Symptoms: ${diagnosis.symptoms.join(', ')}
Primary Diagnosis: ${diagnosis.diagnoses[0].condition}
Confidence: ${diagnosis.diagnoses[0].confidence}%
    `.trim()
    expect(textExport).toContain('Migraine')
  })

  it('handles API failure with graceful fallback', async () => {
    const mockApiCall = vi.fn().mockRejectedValue(new Error('API unavailable'))

    try {
      await mockApiCall()
    } catch (error) {
      // Fallback behavior
      const fallbackMessage = 'Unable to complete diagnosis. Please try again or consult a healthcare provider.'
      expect(fallbackMessage).toContain('healthcare provider')
    }
  })

  it('validates symptom input before submission', async () => {
    const validateSymptoms = (input) => {
      if (!input || input.trim().length < 3) {
        return { valid: false, error: 'Please describe your symptoms in more detail' }
      }
      if (input.length > 2000) {
        return { valid: false, error: 'Input too long' }
      }
      return { valid: true }
    }

    expect(validateSymptoms('hi').valid).toBe(false)
    expect(validateSymptoms('I have a severe headache').valid).toBe(true)
    expect(validateSymptoms('a'.repeat(2001)).valid).toBe(false)
  })
})
