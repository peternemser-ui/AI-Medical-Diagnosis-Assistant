import { defineConfig, devices } from '@playwright/test'

/**
 * Playwright E2E test configuration.
 *
 * Tests run against a local Vite dev server (http://localhost:3000).
 * The webServer block starts the dev server automatically before the test
 * run and tears it down afterwards.
 *
 * Run:  npm run test:e2e
 */
export default defineConfig({
  testDir: './e2e',
  testMatch: '**/*.spec.js',

  /* Global timeout for each test */
  timeout: 30_000,

  /* Retry once on CI, none locally */
  retries: process.env.CI ? 1 : 0,

  /* Parallelism — single worker keeps state predictable for auth tests */
  workers: process.env.CI ? 1 : undefined,

  /* Reporter */
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],

  use: {
    baseURL: 'http://localhost:3000',

    /* Collect traces on retry so failures are diagnosable */
    trace: 'on-first-retry',

    /* Screenshot on failure */
    screenshot: 'only-on-failure',

    /* Consistent viewport */
    viewport: { width: 1280, height: 720 },
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],

  /* Start Vite dev server before tests run */
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
    stdout: 'pipe',
    stderr: 'pipe',
  },
})
