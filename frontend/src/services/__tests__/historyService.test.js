import { describe, it, expect, beforeEach, vi } from 'vitest'

// Mock cryptoService so isUnlocked() returns false (plaintext/localStorage mode)
vi.mock('../cryptoService.js', () => ({
  isUnlocked: () => false,
  clearSessionKey: vi.fn(),
}))

// Mock encryptedStorage — not used when isUnlocked() is false, but needed for import
vi.mock('../encryptedStorage.js', () => ({
  getEncryptedHistory: vi.fn(async () => []),
  saveEncryptedSession: vi.fn(async () => {}),
  deleteEncryptedSession: vi.fn(async () => {}),
  clearEncryptedHistory: vi.fn(async () => {}),
}))

import {
  saveSession,
  getSessions,
  getSession,
  deleteSession,
  clearHistory,
} from '../historyService.js'

beforeEach(() => {
  localStorage.clear()
})

describe('saveSession', () => {
  it('saves a session and returns an ID', async () => {
    const id = await saveSession({ symptoms: 'headache', age: '30', gender: 'male' })
    expect(id).toBeTruthy()
    expect(typeof id).toBe('string')
  })

  it('stores the session data in localStorage', async () => {
    await saveSession({ symptoms: 'cough' })
    const raw = localStorage.getItem('diagnosis_history')
    const sessions = JSON.parse(raw)
    expect(sessions).toHaveLength(1)
    expect(sessions[0].symptoms).toBe('cough')
  })

  it('defaults missing fields gracefully', async () => {
    const id = await saveSession({})
    const session = getSession(id)
    expect(session.symptoms).toBe('')
    expect(session.age).toBe('')
    expect(session.gender).toBe('')
    expect(session.diagnosisResult).toBeNull()
    expect(session.chatMessages).toEqual([])
  })
})

describe('getSession', () => {
  it('retrieves a session by ID', async () => {
    const id = await saveSession({ symptoms: 'fever', age: '25' })
    const session = getSession(id)
    expect(session).not.toBeNull()
    expect(session.id).toBe(id)
    expect(session.symptoms).toBe('fever')
    expect(session.age).toBe('25')
  })

  it('returns null for a non-existent ID', () => {
    expect(getSession('does-not-exist')).toBeNull()
  })
})

describe('getSessions', () => {
  it('returns an empty array when no sessions exist', () => {
    expect(getSessions()).toEqual([])
  })

  it('returns session summaries sorted by date descending', async () => {
    await saveSession({ symptoms: 'first', timestamp: '2025-01-01T00:00:00Z' })
    await saveSession({ symptoms: 'second', timestamp: '2025-06-01T00:00:00Z' })

    const summaries = getSessions()
    expect(summaries).toHaveLength(2)
    // Most recent first
    expect(summaries[0].symptomsSummary).toBe('second')
    expect(summaries[1].symptomsSummary).toBe('first')
  })

  it('truncates long symptom strings to 80 chars', async () => {
    const longSymptoms = 'a'.repeat(100)
    await saveSession({ symptoms: longSymptoms })
    const summaries = getSessions()
    expect(summaries[0].symptomsSummary.length).toBeLessThanOrEqual(83) // 80 + '...'
    expect(summaries[0].symptomsSummary.endsWith('...')).toBe(true)
  })

  it('extracts top diagnosis info from the result', async () => {
    await saveSession({
      symptoms: 'chest pain',
      diagnosisResult: {
        causes: [
          { cause: 'Angina', value: 65, urgency: 'urgent' }
        ]
      }
    })
    const summaries = getSessions()
    expect(summaries[0].topDiagnosis).toBe('Angina')
    expect(summaries[0].confidence).toBe(65)
    expect(summaries[0].urgency).toBe('urgent')
  })
})

describe('deleteSession', () => {
  it('removes a session by ID', async () => {
    const id1 = await saveSession({ symptoms: 'a' })
    const id2 = await saveSession({ symptoms: 'b' })

    await deleteSession(id1)

    expect(getSession(id1)).toBeNull()
    expect(getSession(id2)).not.toBeNull()
    expect(getSessions()).toHaveLength(1)
  })

  it('does nothing when deleting a non-existent ID', async () => {
    await saveSession({ symptoms: 'x' })
    await deleteSession('fake-id')
    expect(getSessions()).toHaveLength(1)
  })
})

describe('clearHistory', () => {
  it('removes all sessions', async () => {
    await saveSession({ symptoms: 'a' })
    await saveSession({ symptoms: 'b' })
    await clearHistory()
    expect(getSessions()).toEqual([])
  })
})
