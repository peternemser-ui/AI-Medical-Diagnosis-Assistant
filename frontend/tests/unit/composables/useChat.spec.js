import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useChat } from '@/composables/useChat'

describe('useChat', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes with empty messages', () => {
    const { messages } = useChat()
    expect(messages.value).toEqual([])
  })

  it('adds user message', () => {
    const { messages, addMessage } = useChat()
    addMessage('Hello', 'user')
    expect(messages.value.length).toBe(1)
    expect(messages.value[0].role).toBe('user')
  })

  it('adds assistant message', () => {
    const { messages, addMessage } = useChat()
    addMessage('How can I help?', 'assistant')
    expect(messages.value[0].role).toBe('assistant')
  })

  it('generates unique message IDs', () => {
    const { messages, addMessage } = useChat()
    addMessage('First', 'user')
    addMessage('Second', 'user')
    expect(messages.value[0].id).not.toBe(messages.value[1].id)
  })

  it('clears all messages', () => {
    const { messages, addMessage, clearMessages } = useChat()
    addMessage('Test', 'user')
    clearMessages()
    expect(messages.value).toEqual([])
  })

  it('tracks loading state', () => {
    const { isLoading, setLoading } = useChat()
    expect(isLoading.value).toBe(false)
    setLoading(true)
    expect(isLoading.value).toBe(true)
  })

  it('provides message count', () => {
    const { messageCount, addMessage } = useChat()
    expect(messageCount.value).toBe(0)
    addMessage('Test', 'user')
    expect(messageCount.value).toBe(1)
  })

  it('gets last message', () => {
    const { lastMessage, addMessage } = useChat()
    addMessage('First', 'user')
    addMessage('Last', 'assistant')
    expect(lastMessage.value.content).toBe('Last')
  })

  it('updates existing message', () => {
    const { messages, addMessage, updateMessage } = useChat()
    addMessage('Original', 'user')
    const id = messages.value[0].id
    updateMessage(id, 'Updated')
    expect(messages.value[0].content).toBe('Updated')
  })

  it('removes specific message', () => {
    const { messages, addMessage, removeMessage } = useChat()
    addMessage('First', 'user')
    addMessage('Second', 'user')
    const id = messages.value[0].id
    removeMessage(id)
    expect(messages.value.length).toBe(1)
  })
})
