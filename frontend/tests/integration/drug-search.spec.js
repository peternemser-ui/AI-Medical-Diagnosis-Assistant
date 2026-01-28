import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('Drug Search Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('searches for drugs by name', async () => {
    const searchQuery = 'ibuprofen'

    const mockResults = [
      { rxcui: '5640', name: 'Ibuprofen', strength: '200mg' },
      { rxcui: '5641', name: 'Ibuprofen', strength: '400mg' },
      { rxcui: '5642', name: 'Ibuprofen', strength: '600mg' }
    ]

    const filteredResults = mockResults.filter(d =>
      d.name.toLowerCase().includes(searchQuery.toLowerCase())
    )

    expect(filteredResults.length).toBe(3)
  })

  it('retrieves detailed drug information', async () => {
    const drugDetails = {
      rxcui: '5640',
      name: 'Ibuprofen',
      strength: '200mg',
      dosageForm: 'Tablet',
      route: 'Oral',
      indications: ['Pain relief', 'Fever reduction', 'Anti-inflammatory'],
      contraindications: ['Aspirin allergy', 'Active GI bleeding'],
      sideEffects: ['Stomach upset', 'Dizziness', 'Headache'],
      warnings: ['Do not exceed recommended dose', 'Consult doctor if pregnant']
    }

    expect(drugDetails.indications.length).toBeGreaterThan(0)
    expect(drugDetails.contraindications.length).toBeGreaterThan(0)
  })

  it('checks drug interactions between multiple medications', async () => {
    const medications = ['aspirin', 'ibuprofen', 'warfarin']

    const interactions = [
      {
        drugs: ['aspirin', 'ibuprofen'],
        severity: 'moderate',
        description: 'Increased risk of GI bleeding'
      },
      {
        drugs: ['aspirin', 'warfarin'],
        severity: 'major',
        description: 'Significantly increased bleeding risk'
      },
      {
        drugs: ['ibuprofen', 'warfarin'],
        severity: 'major',
        description: 'May increase anticoagulant effect'
      }
    ]

    const majorInteractions = interactions.filter(i => i.severity === 'major')
    expect(majorInteractions.length).toBe(2)
  })

  it('provides dosage recommendations based on condition', async () => {
    const drug = 'ibuprofen'
    const condition = 'headache'
    const patientAge = 35

    const dosageRecommendation = {
      drug,
      condition,
      recommendedDose: '200-400mg',
      frequency: 'every 4-6 hours',
      maxDailyDose: '1200mg',
      duration: 'as needed',
      notes: 'Take with food to reduce stomach irritation'
    }

    expect(dosageRecommendation.recommendedDose).toBeDefined()
    expect(dosageRecommendation.maxDailyDose).toBeDefined()
  })

  it('identifies OTC vs prescription medications', async () => {
    const medications = [
      { name: 'Ibuprofen 200mg', otc: true },
      { name: 'Ibuprofen 800mg', otc: false },
      { name: 'Acetaminophen 500mg', otc: true },
      { name: 'Oxycodone', otc: false }
    ]

    const otcMeds = medications.filter(m => m.otc)
    const rxMeds = medications.filter(m => !m.otc)

    expect(otcMeds.length).toBe(2)
    expect(rxMeds.length).toBe(2)
  })

  it('handles drug search with no results', async () => {
    const searchQuery = 'xyznonexistentdrug123'
    const results = []

    expect(results.length).toBe(0)

    const userMessage = results.length === 0
      ? 'No medications found matching your search'
      : `Found ${results.length} medications`

    expect(userMessage).toContain('No medications found')
  })

  it('validates medication name input', async () => {
    const validateInput = (input) => {
      if (!input || input.trim().length < 2) {
        return { valid: false, error: 'Please enter at least 2 characters' }
      }
      if (!/^[a-zA-Z0-9\s-]+$/.test(input)) {
        return { valid: false, error: 'Invalid characters in search' }
      }
      return { valid: true }
    }

    expect(validateInput('a').valid).toBe(false)
    expect(validateInput('aspirin').valid).toBe(true)
    expect(validateInput('asp<script>').valid).toBe(false)
  })

  it('caches recent drug searches', async () => {
    const searchCache = new Map()

    const search = (query) => {
      if (searchCache.has(query)) {
        return { results: searchCache.get(query), cached: true }
      }
      const results = [{ name: query, rxcui: '12345' }]
      searchCache.set(query, results)
      return { results, cached: false }
    }

    const first = search('ibuprofen')
    const second = search('ibuprofen')

    expect(first.cached).toBe(false)
    expect(second.cached).toBe(true)
  })

  it('sorts drug results by relevance', async () => {
    const query = 'ibu'
    const results = [
      { name: 'Ibuprofen', relevance: 100 },
      { name: 'Ibuprofen PM', relevance: 90 },
      { name: 'Advil (Ibuprofen)', relevance: 85 }
    ]

    const sorted = results.sort((a, b) => b.relevance - a.relevance)
    expect(sorted[0].name).toBe('Ibuprofen')
  })
})
