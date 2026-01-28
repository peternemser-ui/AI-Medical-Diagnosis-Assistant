// User-related types

export type UserRole = 'patient' | 'doctor' | 'admin'

export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  emailVerified: boolean
  isActive: boolean
  profileComplete: boolean
  createdAt: string
  updatedAt: string
}

export interface UserProfile extends User {
  dateOfBirth?: string
  gender?: 'male' | 'female' | 'other' | 'prefer-not-to-say'
  phone?: string
  address?: string
  bloodType?: string
  allergies: string[]
  medications: string[]
  conditions: string[]
  emergencyContact?: EmergencyContact
  preferences: UserPreferences
}

export interface EmergencyContact {
  name: string
  relationship: string
  phone: string
  email?: string
}

export interface UserPreferences {
  language: string
  theme: 'light' | 'dark' | 'system'
  emailNotifications: boolean
  pushNotifications: boolean
  shareData: boolean
  measurementUnit: 'metric' | 'imperial'
}

export interface UserCredentials {
  email: string
  password: string
}

export interface UserRegistration extends UserCredentials {
  name: string
  confirmPassword: string
  termsAccepted: boolean
}

export interface PasswordChange {
  currentPassword: string
  newPassword: string
  confirmNewPassword: string
}

export interface PasswordReset {
  token: string
  newPassword: string
  confirmNewPassword: string
}

export interface Session {
  id: string
  userId: string
  token: string
  deviceInfo?: string
  ipAddress?: string
  userAgent?: string
  isActive: boolean
  createdAt: string
  expiresAt: string
  lastActivity: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export interface AuthResponse {
  token: string
  user: User
}

export interface TokenPayload {
  sub: string
  email: string
  role: UserRole
  exp: number
  iat: number
}
