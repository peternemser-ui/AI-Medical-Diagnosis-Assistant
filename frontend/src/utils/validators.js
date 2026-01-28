/**
 * Validation utility functions
 */

/**
 * Validate email format
 */
export function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(String(email).toLowerCase())
}

/**
 * Validate password strength
 */
export function validatePassword(password) {
  const errors = []

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters')
  }
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
  }
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  }
  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number')
  }
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Password must contain at least one special character')
  }

  return {
    isValid: errors.length === 0,
    errors,
    strength: getPasswordStrength(password)
  }
}

/**
 * Get password strength score (0-100)
 */
export function getPasswordStrength(password) {
  let strength = 0

  if (password.length >= 8) strength += 20
  if (password.length >= 12) strength += 10
  if (/[A-Z]/.test(password)) strength += 20
  if (/[a-z]/.test(password)) strength += 10
  if (/[0-9]/.test(password)) strength += 20
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength += 20

  return Math.min(strength, 100)
}

/**
 * Validate phone number
 */
export function isValidPhone(phone) {
  const cleaned = phone.replace(/\D/g, '')
  return cleaned.length >= 10 && cleaned.length <= 15
}

/**
 * Validate URL
 */
export function isValidUrl(url) {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * Validate required field
 */
export function isRequired(value) {
  if (value === null || value === undefined) return false
  if (typeof value === 'string') return value.trim().length > 0
  if (Array.isArray(value)) return value.length > 0
  return true
}

/**
 * Validate minimum length
 */
export function minLength(value, min) {
  if (!value) return false
  return String(value).length >= min
}

/**
 * Validate maximum length
 */
export function maxLength(value, max) {
  if (!value) return true
  return String(value).length <= max
}

/**
 * Validate number range
 */
export function inRange(value, min, max) {
  const num = Number(value)
  return !isNaN(num) && num >= min && num <= max
}

/**
 * Validate date is in the past
 */
export function isPastDate(date) {
  return new Date(date) < new Date()
}

/**
 * Validate date is in the future
 */
export function isFutureDate(date) {
  return new Date(date) > new Date()
}

/**
 * Validate age (minimum age)
 */
export function isMinAge(birthDate, minAge) {
  const today = new Date()
  const birth = new Date(birthDate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()

  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }

  return age >= minAge
}

/**
 * Sanitize input string
 */
export function sanitizeInput(input) {
  if (typeof input !== 'string') return input
  return input
    .replace(/[<>]/g, '')
    .replace(/javascript:/gi, '')
    .replace(/on\w+=/gi, '')
    .trim()
}

/**
 * Validate symptoms input
 */
export function validateSymptoms(symptoms) {
  const errors = []

  if (!symptoms || symptoms.trim().length < 10) {
    errors.push('Please provide more detail about your symptoms')
  }
  if (symptoms && symptoms.length > 5000) {
    errors.push('Description is too long (max 5000 characters)')
  }

  return {
    isValid: errors.length === 0,
    errors
  }
}
