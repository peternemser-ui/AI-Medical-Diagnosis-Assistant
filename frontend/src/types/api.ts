// API-related types

export interface ApiResponse<T> {
  data: T
  success: boolean
  message?: string
  errors?: ApiError[]
}

export interface ApiError {
  code: string
  message: string
  field?: string
  details?: Record<string, any>
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: Pagination
}

export interface Pagination {
  page: number
  pageSize: number
  totalItems: number
  totalPages: number
  hasNext: boolean
  hasPrevious: boolean
}

export interface PaginationParams {
  page?: number
  pageSize?: number
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

export interface SearchParams extends PaginationParams {
  query?: string
  filters?: Record<string, string | string[] | boolean | number>
}

export interface ApiRequestConfig {
  baseURL?: string
  headers?: Record<string, string>
  timeout?: number
  withCredentials?: boolean
}

export interface HealthCheckResponse {
  status: 'healthy' | 'degraded' | 'unhealthy'
  version: string
  timestamp: string
  services: ServiceHealth[]
}

export interface ServiceHealth {
  name: string
  status: 'up' | 'down' | 'degraded'
  latencyMs?: number
  message?: string
}

// Drug API types
export interface DrugSearchResult {
  rxcui: string
  name: string
  synonym?: string
  tty?: string
}

export interface DrugDetails {
  rxcui: string
  name: string
  strength?: string
  dosageForm?: string
  route?: string
  brandNames: string[]
  genericName?: string
  indications: string[]
  contraindications: string[]
  sideEffects: string[]
  warnings: string[]
  interactions: DrugInteraction[]
}

export interface DrugInteraction {
  rxcui: string
  drugName: string
  severity: 'minor' | 'moderate' | 'major'
  description: string
  recommendation: string
}

export interface DrugInteractionRequest {
  rxcuis: string[]
}

export interface DrugInteractionResponse {
  interactions: DrugInteraction[]
  checkedDrugs: string[]
  timestamp: string
}

// Image analysis types
export interface ImageAnalysisRequest {
  imageBase64: string
  context?: string
  symptoms?: string[]
}

export interface ImageAnalysisResponse {
  analysis: string
  observations: string[]
  recommendations: string[]
  confidence: number
  disclaimer: string
}

// Webhook types
export interface WebhookEvent {
  id: string
  type: string
  data: Record<string, any>
  timestamp: string
  signature: string
}

export type WebhookEventType =
  | 'diagnosis.created'
  | 'diagnosis.completed'
  | 'diagnosis.reviewed'
  | 'user.created'
  | 'user.updated'
  | 'emergency.detected'
