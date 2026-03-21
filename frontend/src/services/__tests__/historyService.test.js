import { describe, it, expect, beforeEach } from 'vitest'
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
  it('saves a session and returns an ID', () => {
    const id = saveSession({ symptoms: 'headache', age: '30', gender: 'male' })
    expect(id).toBeTruthy()
    expect(typeof id).toBe('string')
  })

  it('stores the session data in localStorage', () => {
    saveSession({ symptoms: 'cough' })
    const raw = localStorage.getItem('diagnosis_history')
    const sessions = JSON.parse(raw)
    expect(sessions).toHaveLength(1)
    expect(sessions[0].symptoms).toBe('cough')
  })

  it('defaults missing fields gracefully', () => {
    const id = saveSession({})
    const session = getSession(id)
    expect(session.symptoms).toBe('')
    expect(session.age).toBe('')
    expect(session.gender).toBe('')
    expect(session.diagnosisResult).toBeNull()
    expect(session.chatMessages).toEqual([])
  })
})

describe('getSession', () => {
  it('retrieves a session by ID', () => {
    const id = saveSession({ symptoms: 'fever', age: '25' })
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

  it('returns session summaries sorted by date descending', () => {
    saveSession({ symptoms: 'first', timestamp: '2025-01-01T00:00:00Z' })
    saveSession({ symptoms: 'second', timestamp: '2025-06-01T00:00:00Z' })

    const summaries = getSessions()
    expect(summaries).toHaveLength(2)
    // Most recent first
    expect(summaries[0].symptomsSummary).toBe('second')
    expect(summaries[1].symptomsSummary).toBe('first')
  })

  it('truncates long symptom strings to 80 chars', () => {
    const longSymptoms = 'a'.repeat(100)
    saveSession({ symptoms: longSymptoms })
    const summaries = getSessions()
    expect(summaries[0].symptomsSummary.length).toBeLessThanOrEqual(83) // 80 + '...'
    expect(summaries[0].symptomsSummary.endsWith('...')).toBe(true)
  })

  it('extracts top diagnosis info from the result', () => {
    saveSession({
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
  it('removes a session by ID', () => {
    const id1 = saveSession({ symptoms: 'a' })
    const id2 = saveSession({ symptoms: 'b' })

    deleteSession(id1)

    expect(getSession(id1)).toBeNull()
    expect(getSession(id2)).not.toBeNull()
    expect(getSessions()).toHaveLength(1)
  })

  it('does nothing when deleting a non-existent ID', () => {
    saveSession({ symptoms: 'x' })
    deleteSession('fake-id')
    expect(getSessions()).toHaveLength(1)
  })
})

describe('clearHistory', () => {
  it('removes all sessions', () => {
    saveSession({ symptoms: 'a' })
    saveSession({ symptoms: 'b' })
    clearHistory()
    expect(getSessions()).toEqual([])
  })
})
