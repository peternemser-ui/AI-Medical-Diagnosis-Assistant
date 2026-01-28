import { reactive, computed, ref } from 'vue'

/**
 * Form handling composable
 */
export function useForm(initialValues = {}, validationRules = {}) {
  const values = reactive({ ...initialValues })
  const errors = reactive({})
  const touched = reactive({})
  const isSubmitting = ref(false)

  // Validation functions
  const validators = {
    required: (value) => {
      if (value === null || value === undefined || value === '') return false
      if (Array.isArray(value)) return value.length > 0
      return true
    },
    email: (value) => {
      if (!value) return true
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
    },
    minLength: (value, min) => {
      if (!value) return true
      return String(value).length >= min
    },
    maxLength: (value, max) => {
      if (!value) return true
      return String(value).length <= max
    },
    pattern: (value, pattern) => {
      if (!value) return true
      return new RegExp(pattern).test(value)
    },
    min: (value, min) => {
      if (value === null || value === undefined || value === '') return true
      return Number(value) >= min
    },
    max: (value, max) => {
      if (value === null || value === undefined || value === '') return true
      return Number(value) <= max
    },
    match: (value, fieldName, formValues) => {
      return value === formValues[fieldName]
    }
  }

  // Validate a single field
  function validateField(fieldName) {
    const rules = validationRules[fieldName]
    if (!rules) return true

    const value = values[fieldName]
    errors[fieldName] = ''

    for (const rule of rules) {
      let isValid = true
      let message = rule.message || 'Invalid value'

      if (typeof rule === 'function') {
        isValid = rule(value, values)
      } else if (rule.type === 'custom' && rule.validator) {
        isValid = rule.validator(value, values)
        message = rule.message
      } else if (rule.type === 'match') {
        isValid = validators.match(value, rule.field, values)
        message = rule.message || `Must match ${rule.field}`
      } else if (validators[rule.type]) {
        isValid = validators[rule.type](value, rule.value)
        message = rule.message || `Validation failed: ${rule.type}`
      }

      if (!isValid) {
        errors[fieldName] = message
        return false
      }
    }

    return true
  }

  // Validate all fields
  function validate() {
    let isValid = true
    for (const fieldName of Object.keys(validationRules)) {
      if (!validateField(fieldName)) {
        isValid = false
      }
    }
    return isValid
  }

  // Handle field change
  function handleChange(fieldName, value) {
    values[fieldName] = value
    if (touched[fieldName]) {
      validateField(fieldName)
    }
  }

  // Handle field blur
  function handleBlur(fieldName) {
    touched[fieldName] = true
    validateField(fieldName)
  }

  // Reset form
  function reset(newValues = initialValues) {
    Object.assign(values, { ...newValues })
    Object.keys(errors).forEach(key => errors[key] = '')
    Object.keys(touched).forEach(key => touched[key] = false)
    isSubmitting.value = false
  }

  // Set field value
  function setFieldValue(fieldName, value) {
    values[fieldName] = value
  }

  // Set field error
  function setFieldError(fieldName, error) {
    errors[fieldName] = error
  }

  // Set multiple errors
  function setErrors(newErrors) {
    Object.assign(errors, newErrors)
  }

  // Submit handler wrapper
  async function handleSubmit(onSubmit) {
    // Touch all fields
    Object.keys(values).forEach(key => touched[key] = true)

    if (!validate()) {
      return { success: false, errors }
    }

    isSubmitting.value = true

    try {
      const result = await onSubmit(values)
      return { success: true, data: result }
    } catch (error) {
      if (error.fieldErrors) {
        setErrors(error.fieldErrors)
      }
      return { success: false, error }
    } finally {
      isSubmitting.value = false
    }
  }

  // Computed properties
  const isValid = computed(() => {
    return Object.values(errors).every(e => !e)
  })

  const isDirty = computed(() => {
    return Object.keys(values).some(key => values[key] !== initialValues[key])
  })

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    isDirty,
    handleChange,
    handleBlur,
    handleSubmit,
    validate,
    validateField,
    reset,
    setFieldValue,
    setFieldError,
    setErrors
  }
}

/**
 * Create validation rules helper
 */
export function createValidationRules() {
  return {
    required: (message = 'This field is required') => ({
      type: 'required',
      message
    }),
    email: (message = 'Please enter a valid email') => ({
      type: 'email',
      message
    }),
    minLength: (min, message) => ({
      type: 'minLength',
      value: min,
      message: message || `Must be at least ${min} characters`
    }),
    maxLength: (max, message) => ({
      type: 'maxLength',
      value: max,
      message: message || `Must be no more than ${max} characters`
    }),
    pattern: (pattern, message = 'Invalid format') => ({
      type: 'pattern',
      value: pattern,
      message
    }),
    min: (min, message) => ({
      type: 'min',
      value: min,
      message: message || `Must be at least ${min}`
    }),
    max: (max, message) => ({
      type: 'max',
      value: max,
      message: message || `Must be no more than ${max}`
    }),
    match: (field, message) => ({
      type: 'match',
      field,
      message: message || `Must match ${field}`
    }),
    custom: (validator, message = 'Invalid value') => ({
      type: 'custom',
      validator,
      message
    })
  }
}
