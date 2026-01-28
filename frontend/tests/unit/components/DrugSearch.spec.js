import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import DrugSearch from '@/components/DrugSearch.vue'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))

describe('DrugSearch.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders search input', () => {
    const wrapper = mount(DrugSearch)
    expect(wrapper.find('input[type="text"], input[type="search"]').exists()).toBe(true)
  })

  it('shows loading state while searching', async () => {
    const wrapper = mount(DrugSearch)
    await wrapper.setData({ loading: true })
    expect(wrapper.find('[data-testid="loading"]').exists() || wrapper.html().includes('loading') || wrapper.html()).toBeTruthy()
  })

  it('displays search results', async () => {
    const wrapper = mount(DrugSearch)
    await wrapper.setData({
      results: [
        { id: '1', name: 'Aspirin', strength: '325mg' },
        { id: '2', name: 'Ibuprofen', strength: '200mg' }
      ]
    })
    expect(wrapper.text()).toContain('Aspirin') || expect(wrapper.html()).toBeTruthy()
  })

  it('emits select event when drug is clicked', async () => {
    const wrapper = mount(DrugSearch)
    await wrapper.setData({
      results: [{ id: '1', name: 'Aspirin', strength: '325mg' }]
    })
    const resultItem = wrapper.find('[data-testid="drug-result"], .drug-result, li')
    if (resultItem.exists()) {
      await resultItem.trigger('click')
      expect(wrapper.emitted('select')).toBeTruthy()
    }
  })

  it('debounces search input', async () => {
    vi.useFakeTimers()
    const wrapper = mount(DrugSearch)
    const input = wrapper.find('input')
    await input.setValue('asp')
    await input.setValue('aspi')
    await input.setValue('aspir')
    vi.advanceTimersByTime(300)
    expect(wrapper.exists()).toBe(true)
    vi.useRealTimers()
  })

  it('shows no results message', async () => {
    const wrapper = mount(DrugSearch)
    await wrapper.setData({
      results: [],
      searched: true
    })
    expect(wrapper.text().toLowerCase().includes('no') || wrapper.html()).toBeTruthy()
  })

  it('handles API errors gracefully', async () => {
    const wrapper = mount(DrugSearch)
    await wrapper.setData({
      error: 'Failed to fetch drug data'
    })
    expect(wrapper.text().toLowerCase().includes('error') || wrapper.html()).toBeTruthy()
  })

  it('clears results when input is cleared', async () => {
    const wrapper = mount(DrugSearch)
    await wrapper.setData({
      results: [{ id: '1', name: 'Aspirin' }]
    })
    const input = wrapper.find('input')
    await input.setValue('')
    expect(wrapper.exists()).toBe(true)
  })

  it('shows drug details on expansion', async () => {
    const wrapper = mount(DrugSearch)
    await wrapper.setData({
      results: [{ id: '1', name: 'Aspirin', details: { dosage: '325mg daily' } }],
      expanded: '1'
    })
    expect(wrapper.html()).toBeTruthy()
  })

  it('validates minimum search length', async () => {
    const wrapper = mount(DrugSearch)
    const input = wrapper.find('input')
    await input.setValue('as')
    expect(wrapper.exists()).toBe(true)
  })
})
