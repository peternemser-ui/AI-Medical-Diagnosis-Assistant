const STORAGE_KEY = 'diagnosis_history'
const MAX_SESSIONS = 20

/**
 * Generate a unique session ID
 */
function generateId() {
  return Date.now().toString(36) + '-' + Math.random().toString(36).substring(2, 9)
}

/**
 * Save a diagnosis session to localStorage.
 * @param {Object} sessionData - { symptoms, age, gender, diagnosisResult, chatMessages, timestamp }
 * @returns {string} The generated session ID
 */
export function saveSession(sessionData) {
  const sessions = getAllSessions()
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

  sessions.unshift(entry)

  // Trim to MAX_SESSIONS (remove oldest)
  while (sessions.length > MAX_SESSIONS) {
    sessions.pop()
  }

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions))
  } catch (e) {
    console.error('Failed to save session to localStorage:', e)
  }

  return id
}

/**
 * Internal: get raw sessions array
 */
function getAllSessions() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return []
    return JSON.parse(raw)
  } catch {
    return []
  }
}

/**
 * Returns array of session summaries sorted by date descending.
 * Each entry: { id, timestamp, symptomsSummary, age, gender, topDiagnosis, confidence, urgency }
 */
export function getSessions() {
  const sessions = getAllSessions()

  return sessions
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
    .map(s => {
      const symptoms = s.symptoms || ''
      const symptomsSummary = symptoms.length > 80 ? symptoms.substring(0, 80) + '...' : symptoms

      // Extract top diagnosis info
      let topDiagnosis = 'Assessment Complete'
      let confidence = 0
      let urgency = 'routine'

      if (s.diagnosisResult) {
        const causes = s.diagnosisResult.causes || []
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
 * Returns full session data for a given ID
 */
export function getSession(id) {
  const sessions = getAllSessions()
  return sessions.find(s => s.id === id) || null
}

/**
 * Remove a session by ID
 */
export function deleteSession(id) {
  let sessions = getAllSessions()
  sessions = sessions.filter(s => s.id !== id)
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions))
  } catch (e) {
    console.error('Failed to delete session:', e)
  }
}

/**
 * Remove all sessions
 */
export function clearHistory() {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch (e) {
    console.error('Failed to clear history:', e)
  }
}
