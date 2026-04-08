/**
 * Profile-based medication service.
 *
 * Reads the user's medication list from their profile (localStorage)
 * and enriches each entry with clinical data from the medication database.
 *
 * This replaces the hardcoded demo medication arrays that were previously
 * used as fallback data in every medication sub-page.
 */

import { getProfile } from '@/services/userService.js'
import { enrichMedication } from '@/data/medicationDatabase.js'

/**
 * Get the user's medications from their profile, enriched with clinical data.
 *
 * @returns {{ medications: Array, hasProfile: boolean }}
 *   - medications: Array of enriched medication objects
 *   - hasProfile: Whether the user has any medications in their profile
 */
export function getProfileMedications() {
  const profile = getProfile()
  const rawMeds = profile?.medications

  if (!Array.isArray(rawMeds) || rawMeds.length === 0) {
    return { medications: [], hasProfile: false }
  }

  const medications = rawMeds
    .filter(m => typeof m === 'string' && m.trim().length > 0)
    .map((name, index) => {
      const enriched = enrichMedication(name)
      return {
        id: index + 1,
        ...enriched,
        active: true,
        adherence: 0
      }
    })

  return { medications, hasProfile: medications.length > 0 }
}

/**
 * Get just the medication names from the user's profile.
 * Useful for pages that only need name strings (e.g., interactions matrix).
 *
 * @returns {string[]}
 */
export function getProfileMedicationNames() {
  const { medications } = getProfileMedications()
  return medications.map(m => m.name)
}
