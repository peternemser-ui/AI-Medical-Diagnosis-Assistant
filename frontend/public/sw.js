/**
 * MedAssist AI — Service Worker
 *
 * Caching strategy:
 *   - Cache-first  : static assets (JS, CSS, fonts, images)
 *   - Network-first: API calls (/api/*, /health) with offline JSON fallback
 *   - Network-first: navigation / HTML with cached index.html SPA fallback
 *
 * Cache versioning: bump CACHE_VERSION on every deploy to invalidate stale files.
 */

const CACHE_VERSION = 'v2'
const STATIC_CACHE = `medassist-static-${CACHE_VERSION}`
const DYNAMIC_CACHE = `medassist-dynamic-${CACHE_VERSION}`

// Files to pre-cache during the install phase (app shell)
const APP_SHELL = [
  '/',
  '/index.html',
  '/manifest.json',
  '/offline.html',
]

// ─── Install ──────────────────────────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      // addAll() fails atomically — any missing file aborts the install.
      // Use individual add() wrapped in try/catch to tolerate missing assets
      // at dev time while still caching what's available.
      return Promise.allSettled(APP_SHELL.map((url) => cache.add(url)))
    })
  )
  // Take control immediately — no waiting for old SW to expire.
  self.skipWaiting()
})

// ─── Activate ─────────────────────────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== STATIC_CACHE && name !== DYNAMIC_CACHE)
          .map((name) => caches.delete(name))
      )
    })
  )
  // Claim all open clients so the new SW takes effect immediately.
  self.clients.claim()
})

// ─── Fetch ────────────────────────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Only intercept same-origin GET requests (skip cross-origin requests like fonts CDN).
  if (request.method !== 'GET') return
  if (url.origin !== location.origin && !isCacheableExternalAsset(url)) return

  // Network-first for API endpoints — degrade gracefully offline.
  if (url.pathname.startsWith('/api/') || url.pathname === '/health') {
    event.respondWith(networkFirstAPI(request))
    return
  }

  // Cache-first for static assets (JS, CSS, images, fonts, woff).
  if (isStaticAsset(url.pathname) || isCacheableExternalAsset(url)) {
    event.respondWith(cacheFirst(request))
    return
  }

  // Network-first for navigation (HTML) — fall back to cached index.html for SPA.
  event.respondWith(networkFirstNav(request))
})

// ─── Helpers ─────────────────────────────────────────────────────────────────

function isStaticAsset(pathname) {
  return /\.(js|css|png|jpg|jpeg|webp|svg|gif|ico|woff2?|ttf|eot|avif)$/i.test(pathname)
}

function isCacheableExternalAsset(url) {
  // Cache Google Fonts stylesheets & font files
  return (
    url.hostname === 'fonts.googleapis.com' ||
    url.hostname === 'fonts.gstatic.com'
  )
}

/**
 * Cache-first: serve from cache, populate on cache miss.
 */
async function cacheFirst(request) {
  const cached = await caches.match(request)
  if (cached) return cached

  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(STATIC_CACHE)
      cache.put(request, response.clone())
    }
    return response
  } catch {
    // Static asset not cached and network unavailable — nothing useful to return.
    return new Response('', { status: 503, statusText: 'Offline — asset not cached' })
  }
}

/**
 * Network-first for API routes. Falls back to a structured offline JSON error.
 */
async function networkFirstAPI(request) {
  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(DYNAMIC_CACHE)
      cache.put(request, response.clone())
    }
    return response
  } catch {
    // Try stale cache for GET API requests
    const cached = await caches.match(request)
    if (cached) return cached

    return new Response(
      JSON.stringify({
        error: 'offline',
        message: 'You are offline. Please check your connection and try again.',
        offline: true,
      }),
      {
        status: 503,
        headers: {
          'Content-Type': 'application/json',
          'X-Served-By': 'ServiceWorker-Offline',
        },
      }
    )
  }
}

/**
 * Network-first for navigation (HTML pages). Falls back to index.html for SPA routing,
 * and to offline.html if even that is unavailable.
 */
async function networkFirstNav(request) {
  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(DYNAMIC_CACHE)
      cache.put(request, response.clone())
    }
    return response
  } catch {
    // Check dynamic cache first, then static cache
    const cached = await caches.match(request)
    if (cached) return cached

    // SPA fallback — return index.html so the Vue router can handle the route
    const indexFallback = await caches.match('/index.html')
    if (indexFallback) return indexFallback

    // Last-resort offline page
    const offlineFallback = await caches.match('/offline.html')
    if (offlineFallback) return offlineFallback

    return new Response(
      '<!DOCTYPE html><html><head><title>Offline — MedAssist AI</title></head><body><h1>You are offline</h1><p>Please reconnect to use MedAssist AI.</p></body></html>',
      { status: 503, headers: { 'Content-Type': 'text/html' } }
    )
  }
}
