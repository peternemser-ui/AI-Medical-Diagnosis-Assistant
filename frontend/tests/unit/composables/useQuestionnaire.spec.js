import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useQuestionnaire } from '@/composables/useQuestionnaire'

describe('useQuestionnaire', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes at step 0', () => {
    const { currentStep } = useQuestionnaire()
    expect(currentStep.value).toBe(0)
  })

  it('advances to next step', () => {
    const { currentStep, nextStep } = useQuestionnaire()
    nextStep()
    expect(currentStep.value).toBe(1)
  })

  it('goes back to previous step', () => {
    const { currentStep, nextStep, prevStep } = useQuestionnaire()
    nextStep()
    nextStep()
    prevStep()
    expect(currentStep.value).toBe(1)
  })

  it('cannot go below step 0', () => {
    const { currentStep, prevStep } = useQuestionnaire()
    prevStep()
    expect(currentStep.value).toBe(0)
  })

  it('stores answers', () => {
    const { answers, setAnswer } = useQuestionnaire()
    setAnswer('symptoms', 'headache')
    expect(answers.value.symptoms).toBe('headache')
  })

  it('provides current question', () => {
    const { currentQuestion } = useQuestionnaire()
    expect(currentQuestion.value).toBeDefined()
  })

  it('calculates progress percentage', () => {
    const { progress, nextStep } = useQuestionnaire()
    nextStep()
    expect(progress.value).toBeGreaterThan(0)
  })

  it('indicates completion status', () => {
    const { isComplete } = useQuestionnaire()
    expect(typeof isComplete.value).toBe('boolean')
  })

  it('resets questionnaire', () => {
    const { currentStep, nextStep, reset, answers, setAnswer } = useQuestionnaire()
    nextStep()
    setAnswer('test', 'value')
    reset()
    expect(currentStep.value).toBe(0)
    expect(answers.value).toEqual({})
  })

  it('validates current step', () => {
    const { isStepValid, setAnswer } = useQuestionnaire()
    setAnswer('symptoms', '')
    expect(typeof isStepValid.value).toBe('boolean')
  })

  it('provides total steps count', () => {
    const { totalSteps } = useQuestionnaire()
    expect(totalSteps.value).toBeGreaterThan(0)
  })

  it('skips optional questions', () => {
    const { currentStep, skipStep } = useQuestionnaire()
    skipStep()
    expect(currentStep.value).toBe(1)
  })
})
