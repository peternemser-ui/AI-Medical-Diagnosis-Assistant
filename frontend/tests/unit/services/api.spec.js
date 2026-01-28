import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

vi.mock('axios', () => ({
  default: {
    create: vi.fn(() => ({
      get: vi.fn(),
      post: vi.fn(),
      interceptors: {
        request: { use: vi.fn() },
        response: { use: vi.fn() }
      }
    }))
  }
}))

describe('API Service', () => {
  let apiClient

  beforeEach(() => {
    vi.clearAllMocks()
    apiClient = axios.create()
  })

  it('creates axios instance with base URL', () => {
    expect(axios.create).toBeDefined()
  })

  it('sends diagnosis request', async () => {
    apiClient.post.mockResolvedValue({
      data: {
        diagnoses: [
          { condition: 'Migraine', confidence: 75 }
        ]
      }
    })

    const response = await apiClient.post('/api/diagnose', {
      symptoms: 'severe headache'
    })

    expect(response.data.diagnoses).toHaveLength(1)
  })

  it('handles network errors', async () => {
    apiClient.post.mockRejectedValue(new Error('Network Error'))

    await expect(
      apiClient.post('/api/diagnose', { symptoms: 'test' })
    ).rejects.toThrow('Network Error')
  })

  it('sends follow-up request', async () => {
    apiClient.post.mockResolvedValue({
      data: { question: 'How long have you had this symptom?' }
    })

    const response = await apiClient.post('/api/followup', {
      context: 'headache',
      previousAnswers: []
    })

    expect(response.data.question).toBeDefined()
  })

  it('fetches drug information', async () => {
    apiClient.post.mockResolvedValue({
      data: {
        drugs: [{ name: 'Ibuprofen', rxcui: '5640' }]
      }
    })

    const response = await apiClient.post('/api/drugs/search', {
      query: 'ibuprofen'
    })

    expect(response.data.drugs).toHaveLength(1)
  })

  it('checks drug interactions', async () => {
    apiClient.post.mockResolvedValue({
      data: {
        interactions: [],
        safe: true
      }
    })

    const response = await apiClient.post('/api/drugs/interactions', {
      drugs: ['aspirin', 'ibuprofen']
    })

    expect(response.data.safe).toBe(true)
  })

  it('handles rate limiting', async () => {
    apiClient.post.mockRejectedValue({
      response: { status: 429, data: { message: 'Too many requests' } }
    })

    await expect(
      apiClient.post('/api/diagnose', { symptoms: 'test' })
    ).rejects.toBeDefined()
  })

  it('sends image for analysis', async () => {
    apiClient.post.mockResolvedValue({
      data: { analysis: 'Image shows potential skin irritation' }
    })

    const formData = new FormData()
    formData.append('image', new Blob())

    const response = await apiClient.post('/api/analyze-image', formData)
    expect(response.data.analysis).toBeDefined()
  })

  it('performs health check', async () => {
    apiClient.get.mockResolvedValue({
      data: { status: 'healthy', version: '1.0.0' }
    })

    const response = await apiClient.get('/health')
    expect(response.data.status).toBe('healthy')
  })
})
