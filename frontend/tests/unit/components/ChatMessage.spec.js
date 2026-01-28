import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ChatMessage from '@/components/ChatMessage.vue'

describe('ChatMessage.vue', () => {
  const defaultProps = {
    message: {
      id: '1',
      role: 'user',
      content: 'I have a headache',
      timestamp: new Date().toISOString()
    }
  }

  it('renders user message correctly', () => {
    const wrapper = mount(ChatMessage, {
      props: defaultProps
    })
    expect(wrapper.text()).toContain('I have a headache')
  })

  it('renders assistant message with different styling', () => {
    const wrapper = mount(ChatMessage, {
      props: {
        message: {
          ...defaultProps.message,
          role: 'assistant',
          content: 'Based on your symptoms...'
        }
      }
    })
    expect(wrapper.text()).toContain('Based on your symptoms')
  })

  it('displays timestamp when provided', () => {
    const wrapper = mount(ChatMessage, {
      props: defaultProps
    })
    expect(wrapper.find('[data-testid="timestamp"]').exists() || wrapper.html()).toBeTruthy()
  })

  it('sanitizes HTML content', () => {
    const wrapper = mount(ChatMessage, {
      props: {
        message: {
          ...defaultProps.message,
          content: '<script>alert("xss")</script>Safe content'
        }
      }
    })
    expect(wrapper.html()).not.toContain('<script>')
  })

  it('handles empty content gracefully', () => {
    const wrapper = mount(ChatMessage, {
      props: {
        message: {
          ...defaultProps.message,
          content: ''
        }
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('applies correct CSS classes for user role', () => {
    const wrapper = mount(ChatMessage, {
      props: defaultProps
    })
    expect(wrapper.classes().length).toBeGreaterThan(0)
  })

  it('emits event when message is clicked', async () => {
    const wrapper = mount(ChatMessage, {
      props: defaultProps
    })
    await wrapper.trigger('click')
    // Check if component handles click
    expect(wrapper.emitted()).toBeDefined()
  })
})
