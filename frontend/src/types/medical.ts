// Medical-specific types

export interface MedicalHistory {
  id: string
  userId: string
  entryType: 'symptom' | 'diagnosis' | 'medication' | 'procedure' | 'test' | 'vaccination'
  title: string
  description?: string
  date: string
  provider?: string
  notes?: string
  attachments: string[]
  createdAt: string
  updatedAt: string
}

export interface Medication {
  rxcui: string
  name: string
  genericName?: string
  brandNames: string[]
  strength?: string
  dosageForm?: string
  route?: string
  frequency?: string
  startDate?: string
  endDate?: string
  prescribedBy?: string
  notes?: string
}

export interface Allergy {
  id: string
  allergen: string
  type: 'drug' | 'food' | 'environmental' | 'other'
  severity: 'mild' | 'moderate' | 'severe'
  reactions: string[]
  diagnosedDate?: string
  notes?: string
}

export interface VitalSign {
  id: string
  type: 'blood_pressure' | 'heart_rate' | 'temperature' | 'weight' | 'height' | 'bmi' | 'blood_oxygen'
  value: string | number
  unit: string
  measuredAt: string
  notes?: string
}

export interface LabResult {
  id: string
  testName: string
  testCode?: string
  value: string | number
  unit: string
  referenceRange?: string
  status: 'normal' | 'abnormal' | 'critical'
  collectedAt: string
  resultedAt: string
  orderedBy?: string
  lab?: string
  notes?: string
}

export interface Immunization {
  id: string
  vaccine: string
  cvxCode?: string
  doseNumber?: number
  lotNumber?: string
  administeredAt: string
  administeredBy?: string
  site?: string
  route?: string
  nextDueDate?: string
  notes?: string
}

export interface FamilyHistory {
  id: string
  relationship: string
  condition: string
  ageOfOnset?: number
  deceased: boolean
  ageAtDeath?: number
  causeOfDeath?: string
  notes?: string
}

export interface SocialHistory {
  smokingStatus: 'never' | 'former' | 'current'
  alcoholUse: 'none' | 'occasional' | 'moderate' | 'heavy'
  exerciseFrequency: 'none' | 'occasional' | 'regular' | 'daily'
  diet?: string
  occupation?: string
  livingSituation?: string
  stressLevel?: 'low' | 'moderate' | 'high'
  sleepHours?: number
  notes?: string
}

export interface InsuranceInfo {
  id: string
  providerId: string
  providerName: string
  planName: string
  memberId: string
  groupNumber?: string
  effectiveDate: string
  terminationDate?: string
  isPrimary: boolean
  copay?: number
  deductible?: number
}

export interface EmergencyContact {
  name: string
  relationship: string
  phone: string
  email?: string
  address?: string
  isPrimary: boolean
}

export interface HealthGoal {
  id: string
  type: 'weight' | 'exercise' | 'diet' | 'medication' | 'custom'
  title: string
  targetValue?: number
  currentValue?: number
  unit?: string
  startDate: string
  targetDate: string
  status: 'active' | 'completed' | 'abandoned'
  progress: number
  notes?: string
}
