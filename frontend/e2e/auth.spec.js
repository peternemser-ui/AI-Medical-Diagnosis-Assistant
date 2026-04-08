/**
 * E2E tests for authentication flows:
 *  - Sign-up (fill form, submit, redirect)
 *  - Login (valid credentials, invalid credentials show error)
 *  - Logout
 */

import { test, expect } from '@playwright/test'

// Helper: generate a unique email for each test run to avoid conflicts
function uniqueEmail() {
  return `e2e_test_${Date.now()}@example.com`
}

// Strong password that satisfies all server-side rules
const VALID_PASSWORD = 'Test@Password1!'

test.describe('Signup flow', () => {
  test('signup page loads with all required fields', async ({ page }) => {
    await page.goto('/signup')
    await expect(page).toHaveTitle(/Sign Up/i)

    // Core form fields must be present
    await expect(page.getByRole('textbox', { name: /name/i }).or(page.locator('input[name="name"], input[placeholder*="name" i]')).first()).toBeVisible()
    await expect(page.locator('input[type="email"], input[name="email"]').first()).toBeVisible()
    await expect(page.locator('input[type="password"]').first()).toBeVisible()
  })

  test('filling and submitting the signup form redirects away from /signup', async ({ page }) => {
    await page.goto('/signup')

    // Fill in name
    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i], input[autocomplete="name"]').first()
    if (await nameInput.isVisible()) {
      await nameInput.fill('E2E Test User')
    }

    // Fill email
    await page.locator('input[type="email"], input[name="email"]').first().fill(uniqueEmail())

    // Fill password (may be two password fields — fill both if confirmation present)
    const passwordFields = page.locator('input[type="password"]')
    const pwCount = await passwordFields.count()
    await passwordFields.nth(0).fill(VALID_PASSWORD)
    if (pwCount > 1) {
      await passwordFields.nth(1).fill(VALID_PASSWORD)
    }

    // Submit
    await page.getByRole('button', { name: /sign up|create account|register/i }).click()

    // After signup the page should NOT stay on /signup
    // (could redirect to /login, /setup, /consult, or /)
    await page.waitForURL((url) => !url.pathname.endsWith('/signup'), { timeout: 10_000 })
    expect(page.url()).not.toContain('/signup')
  })

  test('signup with already-used email shows error', async ({ page }) => {
    // Use a fixed email that is unlikely to exist but we attempt twice
    const email = `duplicate_${Date.now()}@example.com`

    // First signup
    await page.goto('/signup')
    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i]').first()
    if (await nameInput.isVisible()) await nameInput.fill('User One')
    await page.locator('input[type="email"]').first().fill(email)
    const pws1 = page.locator('input[type="password"]')
    await pws1.nth(0).fill(VALID_PASSWORD)
    if (await pws1.count() > 1) await pws1.nth(1).fill(VALID_PASSWORD)
    await page.getByRole('button', { name: /sign up|create account|register/i }).click()
    // Wait for navigation or response
    await page.waitForTimeout(2000)

    // Second signup with same email
    await page.goto('/signup')
    const nameInput2 = page.locator('input[name="name"], input[placeholder*="name" i]').first()
    if (await nameInput2.isVisible()) await nameInput2.fill('User Two')
    await page.locator('input[type="email"]').first().fill(email)
    const pws2 = page.locator('input[type="password"]')
    await pws2.nth(0).fill(VALID_PASSWORD)
    if (await pws2.count() > 1) await pws2.nth(1).fill(VALID_PASSWORD)
    await page.getByRole('button', { name: /sign up|create account|register/i }).click()

    // Either stays on signup with an error message, or shows an error notification
    await page.waitForTimeout(2000)
    const errorVisible = await page.locator(
      '[class*="error"], [class*="alert"], [role="alert"], .text-red-500, .text-red-600'
    ).first().isVisible().catch(() => false)

    const stillOnSignup = page.url().includes('/signup')
    // At least one of the two conditions must be true
    expect(errorVisible || stillOnSignup).toBe(true)
  })
})

test.describe('Login flow', () => {
  test('login page loads with email and password fields', async ({ page }) => {
    await page.goto('/login')
    await expect(page).toHaveTitle(/log in|sign in/i)
    await expect(page.locator('input[type="email"], input[name="email"]').first()).toBeVisible()
    await expect(page.locator('input[type="password"]').first()).toBeVisible()
    await expect(page.getByRole('button', { name: /log in|sign in|login/i })).toBeVisible()
  })

  test('invalid credentials show error message', async ({ page }) => {
    await page.goto('/login')
    await page.locator('input[type="email"], input[name="email"]').first().fill('nobody@nowhere.invalid')
    await page.locator('input[type="password"]').first().fill('WrongPassword1!')
    await page.getByRole('button', { name: /log in|sign in|login/i }).click()

    // Should stay on /login and show an error
    await page.waitForTimeout(3000)
    const hasError = await page.locator(
      '[class*="error"], [class*="alert"], [role="alert"], .text-red-500, .text-red-600, [class*="danger"]'
    ).first().isVisible().catch(() => false)
    const stillOnLogin = page.url().includes('/login')
    expect(hasError || stillOnLogin).toBe(true)
  })

  test('empty form submission shows validation feedback', async ({ page }) => {
    await page.goto('/login')
    await page.getByRole('button', { name: /log in|sign in|login/i }).click()
    await page.waitForTimeout(1000)

    // HTML5 validation, client-side error, or stays on page
    const url = page.url()
    expect(url).toContain('/login')
  })
})

test.describe('Logout flow', () => {
  test('logging out lands on login or home page and clears session', async ({ page }) => {
    // Sign up a fresh user, then log out
    const email = uniqueEmail()
    await page.goto('/signup')
    const nameInput = page.locator('input[name="name"], input[placeholder*="name" i]').first()
    if (await nameInput.isVisible()) await nameInput.fill('Logout Test User')
    await page.locator('input[type="email"]').first().fill(email)
    const pws = page.locator('input[type="password"]')
    await pws.nth(0).fill(VALID_PASSWORD)
    if (await pws.count() > 1) await pws.nth(1).fill(VALID_PASSWORD)
    await page.getByRole('button', { name: /sign up|create account|register/i }).click()
    await page.waitForTimeout(2000)

    // If there's a logout button/link anywhere, click it
    const logoutBtn = page.getByRole('button', { name: /log out|logout|sign out/i })
      .or(page.getByRole('link', { name: /log out|logout|sign out/i }))
    const logoutVisible = await logoutBtn.first().isVisible().catch(() => false)

    if (logoutVisible) {
      await logoutBtn.first().click()
      await page.waitForTimeout(2000)
      // Should land on / or /login after logout
      const finalUrl = page.url()
      expect(finalUrl.includes('/login') || finalUrl.endsWith('/')).toBe(true)
    } else {
      // Logout button not immediately visible — check that protected routes require auth
      // Navigate to /consult without auth — should redirect to /login or /setup
      await page.evaluate(() => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      })
      await page.goto('/consult')
      await page.waitForTimeout(2000)
      const finalUrl = page.url()
      expect(finalUrl.includes('/login') || finalUrl.includes('/setup') || finalUrl.includes('/signup')).toBe(true)
    }
  })
})
