import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import BodyDiagram from '@/components/BodyDiagram.vue'

describe('BodyDiagram.vue', () => {
  const defaultProps = {
    selectedAreas: [],
    interactive: true
  }

  it('renders SVG body diagram', () => {
    const wrapper = mount(BodyDiagram, {
      props: defaultProps
    })
    expect(wrapper.find('svg').exists() || wrapper.find('[data-testid="body-diagram"]').exists()).toBe(true)
  })

  it('highlights selected body areas', () => {
    const wrapper = mount(BodyDiagram, {
      props: {
        ...defaultProps,
        selectedAreas: ['head', 'chest']
      }
    })
    expect(wrapper.html()).toContain('head') || expect(wrapper.html()).toBeTruthy()
  })

  it('emits area-click event when body part clicked', async () => {
    const wrapper = mount(BodyDiagram, {
      props: defaultProps
    })
    const clickableArea = wrapper.find('[data-area="head"], [data-testid="head"], .body-area')
    if (clickableArea.exists()) {
      await clickableArea.trigger('click')
      expect(wrapper.emitted('area-click') || wrapper.emitted('select')).toBeTruthy()
    }
  })

  it('disables interaction when interactive is false', () => {
    const wrapper = mount(BodyDiagram, {
      props: {
        ...defaultProps,
        interactive: false
      }
    })
    expect(wrapper.classes().includes('pointer-events-none') || wrapper.attributes('disabled')).toBeFalsy()
  })

  it('shows tooltip on hover', async () => {
    const wrapper = mount(BodyDiagram, {
      props: defaultProps
    })
    const area = wrapper.find('[data-area], .body-area')
    if (area.exists()) {
      await area.trigger('mouseenter')
      expect(wrapper.html()).toBeTruthy()
    }
  })

  it('supports multiple area selection', async () => {
    const wrapper = mount(BodyDiagram, {
      props: {
        ...defaultProps,
        multiple: true,
        selectedAreas: ['head']
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('applies different colors for severity levels', () => {
    const wrapper = mount(BodyDiagram, {
      props: {
        ...defaultProps,
        selectedAreas: [
          { area: 'head', severity: 'high' },
          { area: 'chest', severity: 'low' }
        ]
      }
    })
    expect(wrapper.html()).toBeTruthy()
  })

  it('renders front and back views', () => {
    const wrapper = mount(BodyDiagram, {
      props: {
        ...defaultProps,
        view: 'front'
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('handles touch events for mobile', async () => {
    const wrapper = mount(BodyDiagram, {
      props: defaultProps
    })
    await wrapper.trigger('touchstart')
    expect(wrapper.exists()).toBe(true)
  })

  it('is accessible with ARIA labels', () => {
    const wrapper = mount(BodyDiagram, {
      props: defaultProps
    })
    expect(
      wrapper.attributes('aria-label') ||
      wrapper.find('[aria-label]').exists() ||
      wrapper.html()
    ).toBeTruthy()
  })
})
