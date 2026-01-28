/**
 * Application constants
 */

export const APP_NAME = 'AI Medical Diagnosis Assistant'
export const APP_VERSION = '1.0.0'

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const API_TIMEOUT = 30000

// Authentication
export const TOKEN_KEY = 'auth_token'
export const REFRESH_TOKEN_KEY = 'refresh_token'
export const TOKEN_EXPIRY_KEY = 'token_expiry'

// Storage Keys
export const THEME_KEY = 'theme'
export const LANGUAGE_KEY = 'language'
export const USER_PREFERENCES_KEY = 'user_preferences'
export const RECENT_SEARCHES_KEY = 'recent_searches'

// Urgency Levels
export const URGENCY_LEVELS = {
  ROUTINE: 'routine',
  SOON: 'soon',
  URGENT: 'urgent',
  EMERGENCY: 'emergency'
}

export const URGENCY_COLORS = {
  routine: { bg: 'bg-green-100', text: 'text-green-800', border: 'border-green-500' },
  soon: { bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-500' },
  urgent: { bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-500' },
  emergency: { bg: 'bg-red-100', text: 'text-red-800', border: 'border-red-500' }
}

// User Roles
export const USER_ROLES = {
  PATIENT: 'patient',
  DOCTOR: 'doctor',
  ADMIN: 'admin'
}

// Diagnosis Status
export const DIAGNOSIS_STATUS = {
  PENDING: 'pending',
  COMPLETED: 'completed',
  REVIEWED: 'reviewed',
  ARCHIVED: 'archived'
}

// Supported Languages
export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'zh', name: '中文', flag: '🇨🇳' },
  { code: 'pt', name: 'Português', flag: '🇧🇷' }
]

// Body Locations for symptom mapping
export const BODY_LOCATIONS = [
  { id: 'head', name: 'Head', region: 'upper' },
  { id: 'neck', name: 'Neck', region: 'upper' },
  { id: 'chest', name: 'Chest', region: 'torso' },
  { id: 'abdomen', name: 'Abdomen', region: 'torso' },
  { id: 'back', name: 'Back', region: 'torso' },
  { id: 'arms', name: 'Arms', region: 'upper' },
  { id: 'hands', name: 'Hands', region: 'upper' },
  { id: 'legs', name: 'Legs', region: 'lower' },
  { id: 'feet', name: 'Feet', region: 'lower' }
]

// Severity Scale
export const SEVERITY_LABELS = {
  1: 'Minimal',
  2: 'Very Mild',
  3: 'Mild',
  4: 'Mild-Moderate',
  5: 'Moderate',
  6: 'Moderate-Severe',
  7: 'Severe',
  8: 'Very Severe',
  9: 'Extreme',
  10: 'Unbearable'
}

// Export Formats
export const EXPORT_FORMATS = [
  { value: 'json', label: 'JSON', extension: '.json' },
  { value: 'csv', label: 'CSV', extension: '.csv' },
  { value: 'html', label: 'HTML', extension: '.html' },
  { value: 'pdf', label: 'PDF', extension: '.pdf' }
]

// Pagination Defaults
export const DEFAULT_PAGE_SIZE = 20
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100]

// Emergency Keywords
export const EMERGENCY_KEYWORDS = [
  'chest pain',
  'difficulty breathing',
  'can\'t breathe',
  'stroke',
  'heart attack',
  'severe bleeding',
  'unconscious',
  'seizure',
  'overdose',
  'suicidal'
]

// Rate Limiting
export const MAX_REQUESTS_PER_MINUTE = 20
export const RETRY_DELAY_MS = 1000
export const MAX_RETRIES = 3
