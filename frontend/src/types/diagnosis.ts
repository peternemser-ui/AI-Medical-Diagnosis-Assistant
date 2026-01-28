// Diagnosis-related types

export type UrgencyLevel = 'routine' | 'soon' | 'urgent' | 'emergency'

export type DiagnosisStatus = 'pending' | 'completed' | 'reviewed' | 'archived'

export interface Symptom {
  name: string
  severity: number
  duration: string
  location?: string
  description?: string
}

export interface Condition {
  name: string
  confidence: number
  description: string
  icdCode?: string
  specialty?: string
}

export interface Recommendation {
  type: 'lifestyle' | 'medication' | 'specialist' | 'test' | 'emergency'
  title: string
  description: string
  priority: number
  urgency?: UrgencyLevel
}

export interface RedFlag {
  symptom: string
  reason: string
  action: string
}

export interface DiagnosisRequest {
  symptoms: string[]
  symptomDescription: string
  severity?: number
  duration?: string
  bodyLocation?: string
  medicalHistory?: string[]
  currentMedications?: string[]
  imageUrl?: string
}

export interface DiagnosisResponse {
  id: string
  conditions: Condition[]
  recommendations: Recommendation[]
  urgency: UrgencyLevel
  redFlags: RedFlag[]
  followUpQuestions: string[]
  disclaimer: string
  createdAt: string
}

export interface DiagnosisHistory {
  id: string
  userId: string
  symptoms: string[]
  symptomDescription: string
  conditions: Condition[]
  urgency: UrgencyLevel
  status: DiagnosisStatus
  createdAt: string
  updatedAt: string
  reviewedBy?: string
  reviewedAt?: string
  reviewNotes?: string
}

export interface FollowUpQuestion {
  id: string
  question: string
  type: 'text' | 'select' | 'multiselect' | 'scale' | 'boolean'
  options?: string[]
  required: boolean
}

export interface FollowUpAnswer {
  questionId: string
  answer: string | string[] | number | boolean
}

export interface ConversationMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: string
  metadata?: Record<string, any>
}

export interface DiagnosisSession {
  id: string
  userId: string
  diagnosisId?: string
  messages: ConversationMessage[]
  currentStep: number
  totalSteps: number
  isComplete: boolean
  startedAt: string
  completedAt?: string
}
