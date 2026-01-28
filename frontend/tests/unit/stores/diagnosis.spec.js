import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useDiagnosisStore } from '@/stores/diagnosis'

describe('Diagnosis Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with empty state', () => {
    const store = useDiagnosisStore()
    expect(store.diagnoses).toEqual([])
    expect(store.symptoms).toEqual([])
  })

  it('adds symptoms', () => {
    const store = useDiagnosisStore()
    store.addSymptom('headache')
    expect(store.symptoms).toContain('headache')
  })

  it('removes symptoms', () => {
    const store = useDiagnosisStore()
    store.addSymptom('headache')
    store.removeSymptom('headache')
    expect(store.symptoms).not.toContain('headache')
  })

  it('sets diagnoses', () => {
    const store = useDiagnosisStore()
    const diagnoses = [
      { condition: 'Migraine', confidence: 80 }
    ]
    store.setDiagnoses(diagnoses)
    expect(store.diagnoses).toEqual(diagnoses)
  })

  it('clears all data', () => {
    const store = useDiagnosisStore()
    store.addSymptom('headache')
    store.setDiagnoses([{ condition: 'Test', confidence: 50 }])
    store.clearAll()
    expect(store.symptoms).toEqual([])
    expect(store.diagnoses).toEqual([])
  })

  it('provides top diagnosis', () => {
    const store = useDiagnosisStore()
    store.setDiagnoses([
      { condition: 'Low', confidence: 30 },
      { condition: 'High', confidence: 90 },
      { condition: 'Mid', confidence: 60 }
    ])
    expect(store.topDiagnosis.confidence).toBe(90)
  })

  it('tracks loading state', () => {
    const store = useDiagnosisStore()
    expect(store.isLoading).toBe(false)
    store.setLoading(true)
    expect(store.isLoading).toBe(true)
  })

  it('stores conversation history', () => {
    const store = useDiagnosisStore()
    store.addMessage({ role: 'user', content: 'I have a headache' })
    expect(store.messages.length).toBe(1)
  })

  it('calculates urgency level', () => {
    const store = useDiagnosisStore()
    store.setDiagnoses([
      { condition: 'Emergency', confidence: 90, urgency: 'urgent' }
    ])
    expect(store.highestUrgency).toBe('urgent')
  })

  it('exports data to JSON', () => {
    const store = useDiagnosisStore()
    store.addSymptom('headache')
    const exported = store.exportData()
    expect(exported.symptoms).toContain('headache')
  })

  it('imports data from JSON', () => {
    const store = useDiagnosisStore()
    store.importData({
      symptoms: ['fever', 'cough'],
      diagnoses: []
    })
    expect(store.symptoms).toContain('fever')
  })

  it('validates imported data', () => {
    const store = useDiagnosisStore()
    expect(() => store.importData('invalid')).toThrow()
  })
})
