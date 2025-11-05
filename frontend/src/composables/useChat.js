import { ref, computed, nextTick } from 'vue'

/**
 * Chat Management Composable
 * Handles chat messages, history, and conversation state
 */
export function useChat() {
  const messages = ref([])
  const isTyping = ref(false)
  const autoScroll = ref(true)
  const conversationState = ref('initial') // initial, gathering, diagnosing, diagnosed
  const conversationHistory = ref([])

  /**
   * Message types
   */
  const MessageType = {
    USER: 'user',
    ASSISTANT: 'assistant',
    SYSTEM: 'system',
    ERROR: 'error'
  }

  /**
   * Add message to chat
   */
  function addMessage(content, sender = MessageType.ASSISTANT, metadata = {}) {
    const message = {
      id: Date.now() + Math.random(),
      sender,
      text: content,
      timestamp: new Date(),
      ...metadata
    }

    messages.value.push(message)
    console.log(`💬 Message added [${sender}]:`, content.substring(0, 50) + '...')

    // Save to history
    saveToHistory(message)

    return message
  }

  /**
   * Add user message
   */
  function addUserMessage(content, metadata = {}) {
    return addMessage(content, MessageType.USER, metadata)
  }

  /**
   * Add assistant message
   */
  function addAssistantMessage(content, metadata = {}) {
    return addMessage(content, MessageType.ASSISTANT, metadata)
  }

  /**
   * Add system message
   */
  function addSystemMessage(content, metadata = {}) {
    return addMessage(content, MessageType.SYSTEM, metadata)
  }

  /**
   * Add error message
   */
  function addErrorMessage(content, metadata = {}) {
    return addMessage(content, MessageType.ERROR, {
      ...metadata,
      isError: true
    })
  }

  /**
   * Add typing indicator
   */
  async function showTypingIndicator(duration = 0) {
    isTyping.value = true

    if (duration > 0) {
      setTimeout(() => {
        isTyping.value = false
      }, duration)
    }
  }

  /**
   * Hide typing indicator
   */
  function hideTypingIndicator() {
    isTyping.value = false
  }

  /**
   * Add message with typing effect
   */
  async function addMessageWithTyping(content, sender = MessageType.ASSISTANT, typingDuration = 1000, metadata = {}) {
    showTypingIndicator()

    return new Promise((resolve) => {
      setTimeout(() => {
        hideTypingIndicator()
        const message = addMessage(content, sender, metadata)
        resolve(message)
      }, typingDuration)
    })
  }

  /**
   * Update last message
   */
  function updateLastMessage(content, metadata = {}) {
    if (messages.value.length === 0) {
      return addMessage(content, MessageType.ASSISTANT, metadata)
    }

    const lastMessage = messages.value[messages.value.length - 1]
    lastMessage.text = content
    lastMessage.timestamp = new Date()

    // Merge metadata
    Object.assign(lastMessage, metadata)

    console.log('✏️ Last message updated')
    return lastMessage
  }

  /**
   * Delete message by ID
   */
  function deleteMessage(messageId) {
    const index = messages.value.findIndex(m => m.id === messageId)
    if (index !== -1) {
      messages.value.splice(index, 1)
      console.log('🗑️ Message deleted:', messageId)
      return true
    }
    return false
  }

  /**
   * Clear all messages
   */
  function clearMessages() {
    messages.value = []
    conversationHistory.value = []
    console.log('🧹 All messages cleared')
  }

  /**
   * Get messages by sender
   */
  function getMessagesBySender(sender) {
    return messages.value.filter(m => m.sender === sender)
  }

  /**
   * Get conversation summary
   */
  function getConversationSummary() {
    const userMessages = getMessagesBySender(MessageType.USER)
    const assistantMessages = getMessagesBySender(MessageType.ASSISTANT)

    return {
      totalMessages: messages.value.length,
      userMessages: userMessages.length,
      assistantMessages: assistantMessages.length,
      startTime: messages.value[0]?.timestamp,
      lastTime: messages.value[messages.value.length - 1]?.timestamp,
      state: conversationState.value
    }
  }

  /**
   * Export conversation as text
   */
  function exportAsText() {
    return messages.value.map(m => {
      const time = m.timestamp.toLocaleTimeString()
      const sender = m.sender === MessageType.USER ? 'You' : 'AI Assistant'
      return `[${time}] ${sender}: ${m.text}`
    }).join('\n\n')
  }

  /**
   * Export conversation as JSON
   */
  function exportAsJSON() {
    return JSON.stringify({
      conversation: messages.value,
      summary: getConversationSummary(),
      exportedAt: new Date().toISOString()
    }, null, 2)
  }

  /**
   * Save to history (for undo/redo)
   */
  function saveToHistory(message) {
    conversationHistory.value.push({
      action: 'add',
      message: { ...message },
      timestamp: new Date()
    })

    // Limit history size
    if (conversationHistory.value.length > 100) {
      conversationHistory.value.shift()
    }
  }

  /**
   * Search messages
   */
  function searchMessages(query) {
    if (!query || query.trim() === '') return []

    const lowerQuery = query.toLowerCase()
    return messages.value.filter(m =>
      m.text.toLowerCase().includes(lowerQuery)
    )
  }

  /**
   * Get last N messages
   */
  function getLastMessages(count = 10) {
    return messages.value.slice(-count)
  }

  /**
   * Get messages in time range
   */
  function getMessagesInRange(startTime, endTime) {
    return messages.value.filter(m =>
      m.timestamp >= startTime && m.timestamp <= endTime
    )
  }

  /**
   * Count messages by type
   */
  function countMessagesByType() {
    return messages.value.reduce((acc, m) => {
      acc[m.sender] = (acc[m.sender] || 0) + 1
      return acc
    }, {})
  }

  /**
   * Get conversation duration
   */
  const conversationDuration = computed(() => {
    if (messages.value.length < 2) return 0

    const start = messages.value[0].timestamp
    const end = messages.value[messages.value.length - 1].timestamp

    return Math.floor((end - start) / 1000) // seconds
  })

  /**
   * Get formatted conversation duration
   */
  const formattedDuration = computed(() => {
    const seconds = conversationDuration.value
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60

    if (minutes > 0) {
      return `${minutes}m ${remainingSeconds}s`
    }
    return `${seconds}s`
  })

  /**
   * Check if conversation is empty
   */
  const isEmpty = computed(() => messages.value.length === 0)

  /**
   * Get last message
   */
  const lastMessage = computed(() => {
    return messages.value[messages.value.length - 1] || null
  })

  /**
   * Get message count
   */
  const messageCount = computed(() => messages.value.length)

  return {
    // State
    messages,
    isTyping,
    autoScroll,
    conversationState,
    conversationHistory,

    // Computed
    conversationDuration,
    formattedDuration,
    isEmpty,
    lastMessage,
    messageCount,

    // Constants
    MessageType,

    // Methods
    addMessage,
    addUserMessage,
    addAssistantMessage,
    addSystemMessage,
    addErrorMessage,
    showTypingIndicator,
    hideTypingIndicator,
    addMessageWithTyping,
    updateLastMessage,
    deleteMessage,
    clearMessages,
    getMessagesBySender,
    getConversationSummary,
    exportAsText,
    exportAsJSON,
    searchMessages,
    getLastMessages,
    getMessagesInRange,
    countMessagesByType
  }
}
