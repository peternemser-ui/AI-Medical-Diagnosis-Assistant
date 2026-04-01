/**
 * History Service — HIPAA-compliant diagnosis session storage.
 *
 * All session data (PHI) is stored encrypted via encryptedStorage.
 * Falls back to plaintext localStorage for pre-migration data.
 */

import { isUnlocked } from './cryptoService.js'
import {
  getEncryptedHistory,
  saveEncryptedSession,
  deleteEncryptedSession,
  clearEncryptedHistory,
} from './encryptedStorage.js'

const STORAGE_KEY = 'diagnosis_history' // legacy plaintext key
const MAX_SESSIONS = 20

function generateId() {
  return Date.now().toString(36) + '-' + Math.random().toString(36).substring(2, 9)
}

/**
 * Internal: get raw sessions array from encrypted or plaintext storage.
 */
async function getAllSessionsAsync() {
  if (isUnlocked()) {
    return await getEncryptedHistory()
  }
  // Fallback: read plaintext (pre-migration or anonymous)
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    return JSON.parse(raw)
  } catch {
    return []
  }
}

/**
 * Synchronous fallback for getAllSessions — reads plaintext only.
 * Used by callers that haven't migrated to async yet.
 */
function getAllSessionsSync() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    return JSON.parse(raw)
  } catch {
    return []
  }
}

/**
 * Save a diagnosis session.
 * @param {Object} sessionData - { symptoms, age, gender, diagnosisResult, chatMessages, timestamp }
 * @returns {string} The generated session ID
 */
export async function saveSession(sessionData) {
  const id = generateId()

  const entry = {
    id,
    timestamp: sessionData.timestamp || new Date().toISOString(),
    symptoms: sessionData.symptoms || '',
    age: sessionData.age || '',
    gender: sessionData.gender || '',
    diagnosisResult: sessionData.diagnosisResult || null,
    chatMessages: sessionData.chatMessages || [],
  }

  if (isUnlocked()) {
    await saveEncryptedSession(entry)
  } else {
    // Anonymous mode: store in plaintext (will be migrated on next login)
    const sessions = getAllSessionsSync()
    sessions.unshift(entry)
    while (sessions.length > MAX_SESSIONS) sessions.pop()
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions))
    } catch { /* storage full */ }
  }

  return id
}

/**
 * Returns array of session summaries sorted by date descending.
 */
export function getSessions() {
  // Sync version for backward compat — reads plaintext
  const sessions = getAllSessionsSync()
  return _mapToSummaries(sessions)
}

/**
 * Async version that reads from encrypted storage.
 */
export async function getSessionsAsync() {
  const sessions = await getAllSessionsAsync()
  return _mapToSummaries(sessions)
}

function _mapToSummaries(sessions) {
  return sessions
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    .map(s => {
      const symptoms = s.symptoms || ''
      const symptomsSummary = symptoms.length > 80 ? symptoms.substring(0, 80) + '...' : symptoms

      let topDiagnosis = 'Assessment Complete'
      let confidence = 0
      let urgency = 'routine'

      if (s.diagnosisResult) {
        let causes = s.diagnosisResult.causes || []

        if (causes.length === 0 && s.diagnosisResult.agent_details?.diagnosis) {
          const diag = s.diagnosisResult.agent_details.diagnosis
          const differential = diag.differential_diagnosis || diag.diagnoses || diag.differential || diag.conditions || []
          causes = differential.slice(0, 1).filter(d => typeof d === 'object').map(d => ({
            cause: d.condition || d.name || d.diagnosis || 'Unknown',
            value: d.confidence || d.confidence_pct || d.probability || 50,
            urgency: d.urgency || d.priority || 'routine'
          }))
        }

        if (causes.length === 0 && s.diagnosisResult.answer) {
          const match = s.diagnosisResult.answer.match(/\d+\.\s+(.+?)\s*—\s*Confidence:\s*(\d+)%\s*—\s*Urgency:\s*(\w+)/i)
          if (match) {
            causes = [{ cause: match[1].trim(), value: parseInt(match[2]), urgency: match[3].toLowerCase() }]
          }
        }

        if (causes.length > 0) {
          topDiagnosis = causes[0].cause || causes[0].condition || 'Assessment'
          confidence = causes[0].value || causes[0].confidence || 0
          urgency = causes[0].urgency || 'routine'
        }
      }

      return {
        id: s.id,
        timestamp: s.timestamp,
        symptomsSummary,
        age: s.age,
        gender: s.gender,
        topDiagnosis,
        confidence,
        urgency
      }
    })
}

/**
 * Returns full session data for a given ID.
 */
export function getSession(id) {
  // Sync version for backward compat
  const sessions = getAllSessionsSync()
  return sessions.find(s => s.id === id) || null
}

/**
 * Async version that reads from encrypted storage.
 */
export async function getSessionAsync(id) {
  const sessions = await getAllSessionsAsync()
  return sessions.find(s => s.id === id) || null
}

/**
 * Remove a session by ID.
 */
export async function deleteSession(id) {
  if (isUnlocked()) {
    await deleteEncryptedSession(id)
  } else {
    let sessions = getAllSessionsSync()
    sessions = sessions.filter(s => s.id !== id)
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions))
    } catch { /* ignore */ }
  }
}

/**
 * Remove all sessions.
 */
export async function clearHistory() {
  if (isUnlocked()) {
    await clearEncryptedHistory()
  }
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch { /* ignore */ }
}
