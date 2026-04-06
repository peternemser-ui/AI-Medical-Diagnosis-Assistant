import { describe, it, expect, beforeEach, vi } from 'vitest'

// Mock encrypted storage dependencies
vi.mock('../cryptoService.js', () => ({
  isUnlocked: vi.fn(() => false),
}))

vi.mock('../encryptedStorage.js', () => ({
  getEncryptedProfile: vi.fn(() => Promise.resolve({})),
  saveEncryptedProfile: vi.fn(() => Promise.resolve()),
  clearAllEncryptedData: vi.fn(),
  getEncryptedHistory: vi.fn(() => Promise.resolve([])),
}))

import {
  getProfile,
  saveProfile,
  clearUserData,
  getPreferences,
  savePreference,
  savePreferences,
  isProfileComplete,
} from '../userService.js'

beforeEach(() => {
  localStorage.clear()
})

describe('getProfile', () => {
  it('returns a default profile when localStorage is empty', () => {
    const profile = getProfile()
    expect(profile).toHaveProperty('id')
    expect(profile.name).toBe('')
    expect(profile.email).toBe('')
    expect(profile.allergies).toEqual([])
    expect(profile.medications).toEqual([])
    expect(profile.createdAt).toBeTruthy()
  })

  it('merges stored data with defaults', () => {
    localStorage.setItem('user_profile', JSON.stringify({ name: 'Alice' }))
    const profile = getProfile()
    expect(profile.name).toBe('Alice')
    // default fields still present
    expect(profile.email).toBe('')
    expect(profile.allergies).toEqual([])
  })

  it('reads from auth_user cache as fallback', () => {
    localStorage.setItem('auth_user', JSON.stringify({ name: 'JWT User', email: 'jwt@test.com', id: 'u1' }))
    const profile = getProfile()
    expect(profile.name).toBe('JWT User')
    expect(profile.email).toBe('jwt@test.com')
  })
})

describe('saveProfile', () => {
  it('persists profile to localStorage', async () => {
    await saveProfile({ name: 'Bob', email: 'bob@test.com' })
    const raw = localStorage.getItem('user_profile')
    expect(raw).toBeTruthy()
    const parsed = JSON.parse(raw)
    expect(parsed.name).toBe('Bob')
    expect(parsed.email).toBe('bob@test.com')
  })

  it('reads back the same data via getProfile()', async () => {
    await saveProfile({ name: 'Carol', city: 'NYC' })
    const profile = getProfile()
    expect(profile.name).toBe('Carol')
    expect(profile.city).toBe('NYC')
  })

  it('preserves existing fields when saving partial data', async () => {
    await saveProfile({ name: 'Carol', email: 'carol@test.com', city: 'NYC' })
    await saveProfile({ city: 'LA' })
    const profile = getProfile()
    expect(profile.name).toBe('Carol')
    expect(profile.city).toBe('LA')
  })

  it('profile survives across save/load cycle', async () => {
    const data = {
      name: 'Test User',
      email: 'test@example.com',
      bloodType: 'O+',
      allergies: ['penicillin'],
      gender: 'female',
    }
    await saveProfile(data)
    const loaded = getProfile()
    expect(loaded.name).toBe('Test User')
    expect(loaded.email).toBe('test@example.com')
    expect(loaded.bloodType).toBe('O+')
    expect(loaded.allergies).toEqual(['penicillin'])
    expect(loaded.gender).toBe('female')
  })
})

describe('clearUserData', () => {
  it('removes preferences', async () => {
    await saveProfile({ name: 'Hank', email: 'hank@test.com' })
    localStorage.setItem('user_preferences', JSON.stringify({ theme: 'light' }))

    clearUserData()

    expect(localStorage.getItem('user_preferences')).toBeNull()
  })

  it('does NOT delete API keys', async () => {
    localStorage.setItem('anthropic_api_key', 'sk-ant-test-key')
    localStorage.setItem('openai_api_key', 'sk-test-key')
    localStorage.setItem('google_api_key', 'AIza-test-key')

    clearUserData()

    expect(localStorage.getItem('anthropic_api_key')).toBe('sk-ant-test-key')
    expect(localStorage.getItem('openai_api_key')).toBe('sk-test-key')
    expect(localStorage.getItem('google_api_key')).toBe('AIza-test-key')
  })
})

describe('preferences', () => {
  it('returns defaults when empty', () => {
    const prefs = getPreferences()
    expect(prefs.theme).toBe('dark')
    expect(prefs.language).toBe('en')
    expect(prefs.voiceInput).toBe(true)
  })

  it('savePreference updates a single key', () => {
    savePreference('theme', 'light')
    const prefs = getPreferences()
    expect(prefs.theme).toBe('light')
    expect(prefs.language).toBe('en') // other defaults preserved
  })

  it('savePreferences merges multiple keys', () => {
    savePreferences({ theme: 'light', language: 'es' })
    const prefs = getPreferences()
    expect(prefs.theme).toBe('light')
    expect(prefs.language).toBe('es')
  })
})

describe('isProfileComplete', () => {
  it('returns false for empty profile', () => {
    expect(isProfileComplete()).toBe(false)
  })

  it('returns true when name is set', async () => {
    await saveProfile({ name: 'Test User' })
    expect(isProfileComplete()).toBe(true)
  })

  it('returns false when name is only whitespace', async () => {
    await saveProfile({ name: '   ' })
    expect(isProfileComplete()).toBe(false)
  })
})
