const CACHE_NAME = 'meddiagnose-v1'
const STATIC_CACHE = 'meddiagnose-static-v1'

// App shell files to cache on install
const APP_SHELL = [
  '/',
  '/index.html',
  '/manifest.json',
]

// Install: cache app shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(APP_SHELL)
    })
  )
  self.skipWaiting()
})

// Activate: clean old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME && name !== STATIC_CACHE)
          .map((name) => caches.delete(name))
      )
    })
  )
  self.clients.claim()
})

// Fetch handler
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)

  // Skip non-GET requests
  if (request.method !== 'GET') return

  // Network-first for API calls
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/health')) {
    event.respondWith(networkFirst(request))
    return
  }

  // Cache-first for static assets (JS, CSS, images, fonts)
  if (isStaticAsset(url.pathname)) {
    event.respondWith(cacheFirst(request))
    return
  }

  // Network-first for navigation / HTML
  event.respondWith(networkFirst(request))
})

function isStaticAsset(pathname) {
  return /\.(js|css|png|jpg|jpeg|svg|gif|ico|woff2?|ttf|eot)$/i.test(pathname)
}

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
    // Return nothing if both cache and network fail
    return new Response('', { status: 503, statusText: 'Service Unavailable' })
  }
}

async function networkFirst(request) {
  try {
    const response = await fetch(request)
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME)
      cache.put(request, response.clone())
    }
    return response
  } catch {
    const cached = await caches.match(request)
    if (cached) return cached

    // For navigation requests, return cached index.html (SPA fallback)
    if (request.mode === 'navigate') {
      const fallback = await caches.match('/index.html')
      if (fallback) return fallback
    }

    return new Response(
      JSON.stringify({ error: 'You are offline and this content is not cached.' }),
      { status: 503, headers: { 'Content-Type': 'application/json' } }
    )
  }
}
