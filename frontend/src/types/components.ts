// Component prop and event types

import type { UrgencyLevel, Condition, Recommendation } from './diagnosis'

// Chart component types
export interface ChartData {
  labels: string[]
  datasets: ChartDataset[]
}

export interface ChartDataset {
  label: string
  data: number[]
  backgroundColor?: string | string[]
  borderColor?: string | string[]
  borderWidth?: number
}

export interface ChartOptions {
  responsive?: boolean
  maintainAspectRatio?: boolean
  plugins?: {
    legend?: {
      display?: boolean
      position?: 'top' | 'bottom' | 'left' | 'right'
    }
    tooltip?: {
      enabled?: boolean
    }
  }
  scales?: {
    x?: AxisOptions
    y?: AxisOptions
  }
}

export interface AxisOptions {
  display?: boolean
  title?: {
    display?: boolean
    text?: string
  }
  min?: number
  max?: number
  ticks?: {
    stepSize?: number
    callback?: (value: number) => string
  }
}

// Modal types
export interface ModalProps {
  isOpen: boolean
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  closeOnOverlay?: boolean
  closeOnEscape?: boolean
  showCloseButton?: boolean
}

export interface ConfirmModalProps extends ModalProps {
  message: string
  confirmText?: string
  cancelText?: string
  confirmVariant?: 'primary' | 'danger' | 'warning'
}

// Form types
export interface FormField {
  name: string
  label: string
  type: 'text' | 'email' | 'password' | 'number' | 'textarea' | 'select' | 'checkbox' | 'radio' | 'date' | 'file'
  placeholder?: string
  required?: boolean
  disabled?: boolean
  options?: SelectOption[]
  validation?: ValidationRule[]
  helpText?: string
}

export interface SelectOption {
  value: string | number
  label: string
  disabled?: boolean
}

export interface ValidationRule {
  type: 'required' | 'email' | 'minLength' | 'maxLength' | 'pattern' | 'custom'
  value?: any
  message: string
  validator?: (value: any) => boolean
}

export interface FormState {
  values: Record<string, any>
  errors: Record<string, string>
  touched: Record<string, boolean>
  isSubmitting: boolean
  isValid: boolean
}

// Table types
export interface TableColumn<T = any> {
  key: keyof T | string
  label: string
  sortable?: boolean
  width?: string
  align?: 'left' | 'center' | 'right'
  formatter?: (value: any, row: T) => string
  component?: any
}

export interface TableProps<T = any> {
  columns: TableColumn<T>[]
  data: T[]
  loading?: boolean
  emptyText?: string
  selectable?: boolean
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
}

// Toast/Notification types
export interface ToastOptions {
  type: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  duration?: number
  dismissible?: boolean
  action?: {
    label: string
    onClick: () => void
  }
}

// Diagnosis card types
export interface DiagnosisCardProps {
  condition: Condition
  rank: number
  showDetails?: boolean
}

export interface UrgencyBadgeProps {
  level: UrgencyLevel
  size?: 'sm' | 'md' | 'lg'
}

export interface RecommendationListProps {
  recommendations: Recommendation[]
  maxItems?: number
  showAll?: boolean
}

// Body diagram types
export interface BodyLocation {
  id: string
  name: string
  x: number
  y: number
  width: number
  height: number
}

export interface BodyDiagramProps {
  selectedLocations: string[]
  onLocationSelect: (locationId: string) => void
  viewMode?: 'front' | 'back'
  highlightColor?: string
}

// Slider types
export interface SliderProps {
  min: number
  max: number
  step?: number
  value: number
  label?: string
  showValue?: boolean
  marks?: SliderMark[]
  disabled?: boolean
}

export interface SliderMark {
  value: number
  label: string
}

// Timeline types
export interface TimelineItem {
  id: string
  title: string
  description?: string
  date: string
  type: string
  icon?: any
  color?: string
}

export interface TimelineProps {
  items: TimelineItem[]
  orientation?: 'vertical' | 'horizontal'
}
