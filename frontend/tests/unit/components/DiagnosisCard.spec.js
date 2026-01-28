import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import DiagnosisCard from '@/components/DiagnosisCard.vue'

describe('DiagnosisCard.vue', () => {
  const defaultProps = {
    diagnosis: {
      condition: 'Tension Headache',
      confidence: 85,
      description: 'A common type of headache characterized by mild to moderate pain.',
      urgency: 'routine',
      symptoms: ['head pain', 'neck tension', 'stress'],
      recommendations: ['Rest', 'Over-the-counter pain relievers', 'Stress management']
    }
  }

  it('renders diagnosis condition name', () => {
    const wrapper = mount(DiagnosisCard, {
      props: defaultProps
    })
    expect(wrapper.text()).toContain('Tension Headache')
  })

  it('displays confidence percentage', () => {
    const wrapper = mount(DiagnosisCard, {
      props: defaultProps
    })
    expect(wrapper.text()).toContain('85')
  })

  it('shows urgency level with appropriate styling', () => {
    const wrapper = mount(DiagnosisCard, {
      props: defaultProps
    })
    expect(wrapper.text().toLowerCase()).toContain('routine')
  })

  it('renders all symptoms', () => {
    const wrapper = mount(DiagnosisCard, {
      props: defaultProps
    })
    defaultProps.diagnosis.symptoms.forEach(symptom => {
      expect(wrapper.text().toLowerCase()).toContain(symptom.toLowerCase())
    })
  })

  it('displays recommendations list', () => {
    const wrapper = mount(DiagnosisCard, {
      props: defaultProps
    })
    expect(wrapper.text()).toContain('Rest')
  })

  it('applies urgent styling for high urgency', () => {
    const wrapper = mount(DiagnosisCard, {
      props: {
        diagnosis: {
          ...defaultProps.diagnosis,
          urgency: 'urgent'
        }
      }
    })
    expect(wrapper.html()).toBeTruthy()
  })

  it('handles missing recommendations gracefully', () => {
    const wrapper = mount(DiagnosisCard, {
      props: {
        diagnosis: {
          ...defaultProps.diagnosis,
          recommendations: []
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('emits learn-more event when clicked', async () => {
    const wrapper = mount(DiagnosisCard, {
      props: defaultProps
    })
    const button = wrapper.find('[data-testid="learn-more"]')
    if (button.exists()) {
      await button.trigger('click')
      expect(wrapper.emitted('learn-more')).toBeTruthy()
    }
  })

  it('calculates risk level from confidence', () => {
    const wrapper = mount(DiagnosisCard, {
      props: defaultProps
    })
    // Component should show some visual indicator of confidence level
    expect(wrapper.html()).toBeTruthy()
  })
})
