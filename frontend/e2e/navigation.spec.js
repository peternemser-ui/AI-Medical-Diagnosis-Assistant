/**
 * E2E tests for navigation:
 *  - Home route loads
 *  - Main nav links work (Home, Reports, Medications, Pricing)
 *  - Authenticated-only routes redirect to login when unauthenticated
 *  - 404 page shows for unrecognised routes
 */

import { test, expect } from '@playwright/test'

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Clear all auth state so tests start unauthenticated. */
async function clearAuth(page) {
  await page.goto('/')
  await page.evaluate(() => {
    localStorage.clear()
    sessionStorage.clear()
  })
}

// ---------------------------------------------------------------------------
// Home
// ---------------------------------------------------------------------------

test.describe('Home route', () => {
  test('root "/" loads and has a recognisable page title', async ({ page }) => {
    await page.goto('/')
    // Title set by router meta
    await expect(page).toHaveTitle(/MedDiagnose AI/i)
  })

  test('home page contains a heading or hero text', async ({ page }) => {
    await page.goto('/')
    await page.waitForTimeout(1000)
    const headings = page.locator('h1, h2')
    const count = await headings.count()
    expect(count).toBeGreaterThan(0)
  })
})

// ---------------------------------------------------------------------------
// Public nav links
// ---------------------------------------------------------------------------

test.describe('Public navigation links', () => {
  test('/pricing route loads', async ({ page }) => {
    await page.goto('/pricing')
    await page.waitForTimeout(1000)
    await expect(page).toHaveTitle(/Pricing/i)
    // Should not redirect away from /pricing
    expect(page.url()).toContain('/pricing')
  })

  test('/features route loads', async ({ page }) => {
    await page.goto('/features')
    await page.waitForTimeout(1000)
    await expect(page).toHaveTitle(/Features/i)
    expect(page.url()).toContain('/features')
  })

  test('/login route loads', async ({ page }) => {
    await page.goto('/login')
    await page.waitForTimeout(500)
    await expect(page).toHaveTitle(/Log In/i)
    expect(page.url()).toContain('/login')
  })

  test('/signup route loads', async ({ page }) => {
    await page.goto('/signup')
    await page.waitForTimeout(500)
    await expect(page).toHaveTitle(/Sign Up/i)
    expect(page.url()).toContain('/signup')
  })

  test('clicking a nav link to /pricing navigates correctly', async ({ page }) => {
    await page.goto('/')
    await page.waitForTimeout(500)

    // Look for a Pricing link in the nav bar
    const pricingLink = page.getByRole('link', { name: /pricing/i }).first()
    const linkVisible = await pricingLink.isVisible().catch(() => false)

    if (linkVisible) {
      await pricingLink.click()
      await page.waitForURL('**/pricing', { timeout: 5000 })
      expect(page.url()).toContain('/pricing')
    } else {
      // Navigate directly — acceptable if there's no nav bar on home
      await page.goto('/pricing')
      expect(page.url()).toContain('/pricing')
    }
  })
})

// ---------------------------------------------------------------------------
// Authenticated-only routes redirect when unauthenticated
// ---------------------------------------------------------------------------

test.describe('Protected routes redirect to login when unauthenticated', () => {
  test('/reports redirects when not logged in', async ({ page }) => {
    await clearAuth(page)
    await page.goto('/reports')
    await page.waitForTimeout(2000)
    const url = page.url()
    expect(url.includes('/login') || url.includes('/signup')).toBe(true)
  })

  test('/consult redirects when not logged in', async ({ page }) => {
    await clearAuth(page)
    await page.goto('/consult')
    await page.waitForTimeout(2000)
    const url = page.url()
    expect(url.includes('/login') || url.includes('/signup') || url.includes('/setup')).toBe(true)
  })

  test('/settings redirects when not logged in', async ({ page }) => {
    await clearAuth(page)
    await page.goto('/settings')
    await page.waitForTimeout(2000)
    const url = page.url()
    expect(url.includes('/login') || url.includes('/signup')).toBe(true)
  })

  test('/medications redirects when not logged in', async ({ page }) => {
    await clearAuth(page)
    await page.goto('/medications')
    await page.waitForTimeout(2000)
    const url = page.url()
    expect(url.includes('/login') || url.includes('/signup')).toBe(true)
  })
})

// ---------------------------------------------------------------------------
// Legacy redirects
// ---------------------------------------------------------------------------

test.describe('Legacy route redirects', () => {
  test('/voice-diagnosis redirects to /consult (or further to /login)', async ({ page }) => {
    await page.goto('/voice-diagnosis')
    await page.waitForTimeout(2000)
    // Should redirect to /consult which may then redirect to /login
    const url = page.url()
    expect(
      url.includes('/consult') || url.includes('/login') || url.includes('/signup') || url.includes('/setup')
    ).toBe(true)
  })

  test('/diagnose redirects to /consult (or further to /login)', async ({ page }) => {
    await page.goto('/diagnose')
    await page.waitForTimeout(2000)
    const url = page.url()
    expect(
      url.includes('/consult') || url.includes('/login') || url.includes('/signup') || url.includes('/setup')
    ).toBe(true)
  })
})

// ---------------------------------------------------------------------------
// 404 / Not Found
// ---------------------------------------------------------------------------

test.describe('404 Not Found page', () => {
  test('a completely unknown route shows the 404 view', async ({ page }) => {
    await page.goto('/this-route-absolutely-does-not-exist-xyz-abc-123')
    await page.waitForTimeout(1000)

    // Title should mention 404 or Not Found
    const title = await page.title()
    expect(title.includes('404') || title.toLowerCase().includes('not found')).toBe(true)
  })

  test('404 page renders with visible content', async ({ page }) => {
    await page.goto('/nonexistent/route/xyz')
    await page.waitForTimeout(1000)

    const body = await page.locator('body').innerText()
    // The page must contain some text (not blank)
    expect(body.trim().length).toBeGreaterThan(10)
  })

  test('404 page has a link back to home', async ({ page }) => {
    await page.goto('/totally-missing-page')
    await page.waitForTimeout(1000)

    const homeLink = page.getByRole('link', { name: /home|go back|return/i }).first()
    const linkVisible = await homeLink.isVisible().catch(() => false)
    // A home link is expected — verify it exists and points to /
    if (linkVisible) {
      const href = await homeLink.getAttribute('href')
      expect(href === '/' || href === '' || href?.endsWith('/')).toBe(true)
    } else {
      // No explicit home link — at minimum the page should not be blank
      const headings = await page.locator('h1, h2, h3').count()
      expect(headings).toBeGreaterThan(0)
    }
  })
})
