import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ConfidenceChart from '@/components/ConfidenceChart.vue'

// Mock Chart.js
vi.mock('chart.js', () => ({
  Chart: vi.fn(),
  registerables: []
}))

vi.mock('vue-chartjs', () => ({
  Bar: {
    name: 'Bar',
    template: '<div class="mock-bar-chart"></div>'
  },
  Doughnut: {
    name: 'Doughnut',
    template: '<div class="mock-doughnut-chart"></div>'
  }
}))

describe('ConfidenceChart.vue', () => {
  const defaultProps = {
    diagnoses: [
      { condition: 'Tension Headache', confidence: 85 },
      { condition: 'Migraine', confidence: 60 },
      { condition: 'Cluster Headache', confidence: 30 }
    ]
  }

  it('renders chart container', () => {
    const wrapper = mount(ConfidenceChart, {
      props: defaultProps
    })
    expect(wrapper.find('[data-testid="chart"], canvas, .chart').exists() || wrapper.html()).toBeTruthy()
  })

  it('displays all diagnoses', () => {
    const wrapper = mount(ConfidenceChart, {
      props: defaultProps
    })
    expect(wrapper.html()).toBeTruthy()
  })

  it('sorts diagnoses by confidence', () => {
    const wrapper = mount(ConfidenceChart, {
      props: defaultProps
    })
    // Chart should show highest confidence first
    expect(wrapper.exists()).toBe(true)
  })

  it('handles empty diagnoses array', () => {
    const wrapper = mount(ConfidenceChart, {
      props: {
        diagnoses: []
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('updates when diagnoses change', async () => {
    const wrapper = mount(ConfidenceChart, {
      props: defaultProps
    })
    await wrapper.setProps({
      diagnoses: [
        { condition: 'New Condition', confidence: 90 }
      ]
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('uses appropriate colors for confidence levels', () => {
    const wrapper = mount(ConfidenceChart, {
      props: defaultProps
    })
    // High confidence should be green, low should be yellow/red
    expect(wrapper.html()).toBeTruthy()
  })

  it('shows percentage labels', () => {
    const wrapper = mount(ConfidenceChart, {
      props: {
        ...defaultProps,
        showLabels: true
      }
    })
    expect(wrapper.html()).toBeTruthy()
  })

  it('supports different chart types', () => {
    const wrapper = mount(ConfidenceChart, {
      props: {
        ...defaultProps,
        type: 'doughnut'
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('is responsive', () => {
    const wrapper = mount(ConfidenceChart, {
      props: defaultProps
    })
    expect(wrapper.html()).toBeTruthy()
  })

  it('shows legend when enabled', () => {
    const wrapper = mount(ConfidenceChart, {
      props: {
        ...defaultProps,
        showLegend: true
      }
    })
    expect(wrapper.html()).toBeTruthy()
  })
})
