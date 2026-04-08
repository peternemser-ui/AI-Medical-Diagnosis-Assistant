/**
 * useSEO — composable for managing page-level SEO meta tags dynamically.
 *
 * Usage (typically called from router.afterEach):
 *   setSEO({ title: 'Consultation', description: 'Start an AI consultation', keywords: 'symptoms, diagnosis' })
 */

const SITE_NAME = 'MedAssist AI'
const DEFAULT_DESCRIPTION =
  'AI-powered medical diagnosis assistant with 7 specialized agents for comprehensive clinical analysis.'
const DEFAULT_KEYWORDS =
  'AI medical diagnosis, symptom checker, health AI, medical assistant, clinical analysis, telemedicine'
const DEFAULT_OG_TYPE = 'website'
const BASE_URL = 'https://medassist.ai'

/**
 * Upsert a <meta> tag by attribute selector.
 * @param {string} attr - The attribute name to match ('name' or 'property')
 * @param {string} attrValue - The attribute value to match
 * @param {string} content - The content to set
 */
function upsertMeta(attr, attrValue, content) {
  let el = document.querySelector(`meta[${attr}="${attrValue}"]`)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, attrValue)
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}

/**
 * Set document title and update all relevant meta tags.
 *
 * @param {object} options
 * @param {string} [options.title]       - Page name (will be formatted as "Title | MedAssist AI")
 * @param {string} [options.description] - Page description for meta + og:description
 * @param {string} [options.keywords]    - Comma-separated keywords
 * @param {string} [options.ogType]      - Open Graph type (default: 'website')
 * @param {string} [options.ogImage]     - Absolute URL to og:image
 * @param {string} [options.canonical]   - Canonical URL for this page
 */
export function setSEO({
  title,
  description = DEFAULT_DESCRIPTION,
  keywords = DEFAULT_KEYWORDS,
  ogType = DEFAULT_OG_TYPE,
  ogImage = `${BASE_URL}/og-image.png`,
  canonical,
} = {}) {
  // --- Document title ---
  const formattedTitle = title ? `${title} | ${SITE_NAME}` : SITE_NAME
  document.title = formattedTitle

  // --- Standard meta ---
  upsertMeta('name', 'description', description)
  upsertMeta('name', 'keywords', keywords)

  // --- Open Graph ---
  upsertMeta('property', 'og:site_name', SITE_NAME)
  upsertMeta('property', 'og:title', formattedTitle)
  upsertMeta('property', 'og:description', description)
  upsertMeta('property', 'og:type', ogType)
  upsertMeta('property', 'og:image', ogImage)

  if (canonical) {
    upsertMeta('property', 'og:url', canonical)
    upsertCanonical(canonical)
  }

  // --- Twitter Card ---
  upsertMeta('property', 'twitter:title', formattedTitle)
  upsertMeta('property', 'twitter:description', description)
  upsertMeta('property', 'twitter:image', ogImage)
}

/**
 * Upsert the <link rel="canonical"> tag.
 * @param {string} href
 */
function upsertCanonical(href) {
  let el = document.querySelector('link[rel="canonical"]')
  if (!el) {
    el = document.createElement('link')
    el.setAttribute('rel', 'canonical')
    document.head.appendChild(el)
  }
  el.setAttribute('href', href)
}

/** Composable hook — returns setSEO for use in components if needed. */
export function useSEO() {
  return { setSEO }
}
