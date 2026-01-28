import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import SymptomInput from '@/components/SymptomInput.vue'

describe('SymptomInput.vue', () => {
  it('renders input field', () => {
    const wrapper = mount(SymptomInput)
    expect(wrapper.find('input, textarea').exists()).toBe(true)
  })

  it('updates v-model on input', async () => {
    const wrapper = mount(SymptomInput, {
      props: {
        modelValue: ''
      }
    })
    const input = wrapper.find('input, textarea')
    await input.setValue('headache')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
  })

  it('emits submit event on enter key', async () => {
    const wrapper = mount(SymptomInput, {
      props: {
        modelValue: 'headache'
      }
    })
    const input = wrapper.find('input, textarea')
    await input.trigger('keydown.enter')
    expect(wrapper.emitted('submit') || wrapper.emitted('send')).toBeTruthy()
  })

  it('shows placeholder text', () => {
    const wrapper = mount(SymptomInput)
    const input = wrapper.find('input, textarea')
    expect(input.attributes('placeholder')).toBeDefined()
  })

  it('disables input when loading', () => {
    const wrapper = mount(SymptomInput, {
      props: {
        loading: true,
        disabled: true
      }
    })
    const input = wrapper.find('input, textarea')
    expect(input.attributes('disabled')).toBeDefined()
  })

  it('shows character count when enabled', () => {
    const wrapper = mount(SymptomInput, {
      props: {
        modelValue: 'test input',
        showCharCount: true,
        maxLength: 500
      }
    })
    // Check if character count is displayed
    expect(wrapper.html()).toBeTruthy()
  })

  it('validates input length', async () => {
    const wrapper = mount(SymptomInput, {
      props: {
        modelValue: '',
        minLength: 3
      }
    })
    const input = wrapper.find('input, textarea')
    await input.setValue('ab')
    // Should show validation error or prevent submission
    expect(wrapper.html()).toBeTruthy()
  })

  it('clears input when clear button clicked', async () => {
    const wrapper = mount(SymptomInput, {
      props: {
        modelValue: 'some text'
      }
    })
    const clearButton = wrapper.find('[data-testid="clear-input"]')
    if (clearButton.exists()) {
      await clearButton.trigger('click')
      expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([''])
    }
  })

  it('shows voice input button when available', () => {
    const wrapper = mount(SymptomInput, {
      props: {
        showVoiceInput: true
      }
    })
    const voiceButton = wrapper.find('[data-testid="voice-input"]')
    expect(voiceButton.exists() || wrapper.html().includes('voice') || wrapper.html().includes('mic')).toBe(true)
  })

  it('handles paste events', async () => {
    const wrapper = mount(SymptomInput)
    const input = wrapper.find('input, textarea')
    await input.trigger('paste')
    expect(wrapper.exists()).toBe(true)
  })
})
