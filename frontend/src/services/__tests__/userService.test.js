import { describe, it, expect, beforeEach } from 'vitest'
import {
  getProfile,
  saveProfile,
  getSavedAccounts,
  saveAccountToList,
  loginWithEmail,
  clearUserData,
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
})

describe('saveProfile', () => {
  it('merges new data into existing profile', () => {
    saveProfile({ name: 'Bob', email: 'bob@test.com' })
    const profile = getProfile()
    expect(profile.name).toBe('Bob')
    expect(profile.email).toBe('bob@test.com')
  })

  it('preserves existing fields when saving partial data', () => {
    saveProfile({ name: 'Carol', email: 'carol@test.com', city: 'NYC' })
    saveProfile({ city: 'LA' })
    const profile = getProfile()
    expect(profile.name).toBe('Carol')
    expect(profile.city).toBe('LA')
  })

  it('adds the profile to accounts list when name and email are set', () => {
    saveProfile({ name: 'Dan', email: 'dan@test.com' })
    const accounts = getSavedAccounts()
    expect(accounts).toHaveLength(1)
    expect(accounts[0].email).toBe('dan@test.com')
  })
})

describe('getSavedAccounts', () => {
  it('returns an empty array when no accounts are stored', () => {
    expect(getSavedAccounts()).toEqual([])
  })
})

describe('saveAccountToList', () => {
  it('adds a new account', () => {
    saveAccountToList({ name: 'Eve', email: 'eve@test.com' })
    const accounts = getSavedAccounts()
    expect(accounts).toHaveLength(1)
    expect(accounts[0].name).toBe('Eve')
  })

  it('updates an existing account with the same email', () => {
    saveAccountToList({ name: 'Eve', email: 'eve@test.com' })
    saveAccountToList({ name: 'Eve Updated', email: 'eve@test.com' })
    const accounts = getSavedAccounts()
    expect(accounts).toHaveLength(1)
    expect(accounts[0].name).toBe('Eve Updated')
  })

  it('keeps multiple accounts with different emails', () => {
    saveAccountToList({ name: 'A', email: 'a@test.com' })
    saveAccountToList({ name: 'B', email: 'b@test.com' })
    expect(getSavedAccounts()).toHaveLength(2)
  })
})

describe('loginWithEmail', () => {
  it('returns the matching account and sets it as active profile', () => {
    saveAccountToList({ name: 'Frank', email: 'frank@test.com', city: 'Boston' })
    const result = loginWithEmail('frank@test.com')
    expect(result).not.toBeNull()
    expect(result.name).toBe('Frank')

    const profile = getProfile()
    expect(profile.name).toBe('Frank')
  })

  it('performs case-insensitive email matching', () => {
    saveAccountToList({ name: 'Grace', email: 'grace@test.com' })
    const result = loginWithEmail('Grace@Test.com')
    expect(result).not.toBeNull()
    expect(result.name).toBe('Grace')
  })

  it('returns null when no matching account exists', () => {
    const result = loginWithEmail('nobody@test.com')
    expect(result).toBeNull()
  })
})

describe('clearUserData', () => {
  it('removes profile and preferences but preserves accounts list', () => {
    saveProfile({ name: 'Hank', email: 'hank@test.com' })
    localStorage.setItem('user_preferences', JSON.stringify({ theme: 'light' }))

    clearUserData()

    // Profile should be reset to defaults
    const profile = getProfile()
    expect(profile.name).toBe('')

    // Preferences should be gone
    expect(localStorage.getItem('user_preferences')).toBeNull()

    // Accounts list should still contain Hank
    const accounts = getSavedAccounts()
    expect(accounts.some(a => a.email === 'hank@test.com')).toBe(true)
  })
})
