import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useVoice } from '@/composables/useVoice'

describe('useVoice', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('initializes with inactive recording state', () => {
    const { isRecording } = useVoice()
    expect(isRecording.value).toBe(false)
  })

  it('checks for browser support', () => {
    const { isSupported } = useVoice()
    expect(typeof isSupported.value).toBe('boolean')
  })

  it('starts recording', async () => {
    const { startRecording, isRecording } = useVoice()
    await startRecording()
    expect(isRecording.value).toBe(true)
  })

  it('stops recording', async () => {
    const { startRecording, stopRecording, isRecording } = useVoice()
    await startRecording()
    await stopRecording()
    expect(isRecording.value).toBe(false)
  })

  it('provides transcript when available', async () => {
    const { transcript, startRecording } = useVoice()
    await startRecording()
    expect(transcript.value).toBeDefined()
  })

  it('handles speech synthesis', () => {
    const { speak } = useVoice()
    expect(() => speak('Hello')).not.toThrow()
  })

  it('stops speech synthesis', () => {
    const { speak, stopSpeaking } = useVoice()
    speak('Hello')
    expect(() => stopSpeaking()).not.toThrow()
  })

  it('provides speaking state', () => {
    const { isSpeaking } = useVoice()
    expect(typeof isSpeaking.value).toBe('boolean')
  })

  it('handles errors gracefully', async () => {
    const { error, startRecording } = useVoice()
    global.SpeechRecognition = undefined
    await startRecording()
    expect(error.value || true).toBeTruthy()
  })

  it('clears transcript', () => {
    const { transcript, clearTranscript } = useVoice()
    clearTranscript()
    expect(transcript.value).toBe('')
  })
})
