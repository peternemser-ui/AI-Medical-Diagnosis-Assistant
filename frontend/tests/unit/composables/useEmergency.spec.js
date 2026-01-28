import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useEmergency } from '@/composables/useEmergency'

describe('useEmergency', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes with no emergency', () => {
    const { hasEmergency, emergency } = useEmergency()
    expect(hasEmergency.value).toBe(false)
    expect(emergency.value).toBeNull()
  })

  it('detects cardiac emergency symptoms', () => {
    const { checkSymptoms, hasEmergency, emergency } = useEmergency()
    checkSymptoms('severe chest pain radiating to arm')
    expect(hasEmergency.value).toBe(true)
    expect(emergency.value.type).toBe('cardiac')
  })

  it('detects stroke symptoms', () => {
    const { checkSymptoms, hasEmergency, emergency } = useEmergency()
    checkSymptoms('sudden facial drooping and slurred speech')
    expect(hasEmergency.value).toBe(true)
    expect(emergency.value.type).toBe('stroke')
  })

  it('detects respiratory emergency', () => {
    const { checkSymptoms, hasEmergency, emergency } = useEmergency()
    checkSymptoms('cannot breathe severe difficulty breathing')
    expect(hasEmergency.value).toBe(true)
    expect(emergency.value.type).toBe('respiratory')
  })

  it('does not trigger for normal symptoms', () => {
    const { checkSymptoms, hasEmergency } = useEmergency()
    checkSymptoms('mild headache for two days')
    expect(hasEmergency.value).toBe(false)
  })

  it('clears emergency state', () => {
    const { checkSymptoms, clearEmergency, hasEmergency } = useEmergency()
    checkSymptoms('severe chest pain')
    clearEmergency()
    expect(hasEmergency.value).toBe(false)
  })

  it('provides emergency action message', () => {
    const { checkSymptoms, emergency } = useEmergency()
    checkSymptoms('severe chest pain')
    expect(emergency.value.action).toContain('911')
  })

  it('detects multiple symptom combinations', () => {
    const { checkSymptoms, emergency } = useEmergency()
    checkSymptoms('numbness on one side of body confusion headache')
    expect(emergency.value).not.toBeNull()
  })

  it('prioritizes most severe emergency', () => {
    const { checkSymptoms, emergency } = useEmergency()
    checkSymptoms('chest pain and difficulty breathing')
    expect(['cardiac', 'respiratory']).toContain(emergency.value.type)
  })

  it('provides emergency phone number', () => {
    const { emergencyPhone } = useEmergency()
    expect(emergencyPhone.value).toBe('911')
  })
})
