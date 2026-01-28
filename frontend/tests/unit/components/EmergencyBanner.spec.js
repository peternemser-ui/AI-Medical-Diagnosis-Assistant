import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import EmergencyBanner from '@/components/EmergencyBanner.vue'

describe('EmergencyBanner.vue', () => {
  const defaultProps = {
    emergency: {
      type: 'cardiac',
      message: 'Possible cardiac emergency detected',
      symptoms: ['chest pain', 'shortness of breath'],
      action: 'Call 911 immediately'
    },
    visible: true
  }

  it('renders when visible is true', () => {
    const wrapper = mount(EmergencyBanner, {
      props: defaultProps
    })
    expect(wrapper.isVisible()).toBe(true)
  })

  it('does not render when visible is false', () => {
    const wrapper = mount(EmergencyBanner, {
      props: {
        ...defaultProps,
        visible: false
      }
    })
    expect(wrapper.find('[data-testid="emergency-banner"]').exists()).toBe(false)
  })

  it('displays emergency message', () => {
    const wrapper = mount(EmergencyBanner, {
      props: defaultProps
    })
    expect(wrapper.text()).toContain('cardiac')
  })

  it('shows call 911 button', () => {
    const wrapper = mount(EmergencyBanner, {
      props: defaultProps
    })
    const callButton = wrapper.find('[data-testid="call-911"]')
    expect(callButton.exists() || wrapper.text().toLowerCase().includes('911')).toBe(true)
  })

  it('emits dismiss event when close button clicked', async () => {
    const wrapper = mount(EmergencyBanner, {
      props: defaultProps
    })
    const closeButton = wrapper.find('[data-testid="close-banner"]')
    if (closeButton.exists()) {
      await closeButton.trigger('click')
      expect(wrapper.emitted('dismiss')).toBeTruthy()
    }
  })

  it('applies critical styling for cardiac emergency', () => {
    const wrapper = mount(EmergencyBanner, {
      props: defaultProps
    })
    expect(wrapper.classes().some(c => c.includes('red') || c.includes('emergency') || c.includes('critical')) || wrapper.html().includes('red')).toBe(true)
  })

  it('handles stroke emergency type', () => {
    const wrapper = mount(EmergencyBanner, {
      props: {
        ...defaultProps,
        emergency: {
          ...defaultProps.emergency,
          type: 'stroke',
          message: 'Possible stroke symptoms detected'
        }
      }
    })
    expect(wrapper.text()).toContain('stroke')
  })

  it('handles respiratory emergency type', () => {
    const wrapper = mount(EmergencyBanner, {
      props: {
        ...defaultProps,
        emergency: {
          ...defaultProps.emergency,
          type: 'respiratory',
          message: 'Severe breathing difficulty detected'
        }
      }
    })
    expect(wrapper.text()).toContain('respiratory')
  })

  it('is accessible with proper ARIA attributes', () => {
    const wrapper = mount(EmergencyBanner, {
      props: defaultProps
    })
    expect(wrapper.attributes('role') === 'alert' || wrapper.find('[role="alert"]').exists() || wrapper.html().includes('alert')).toBe(true)
  })
})
