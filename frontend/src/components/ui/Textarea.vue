<template>
  <div class="w-full">
    <label v-if="label" :for="textareaId" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <textarea
      :id="textareaId"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="readonly"
      :required="required"
      :rows="rows"
      :maxlength="maxlength"
      :class="[
        'block w-full rounded-lg border transition-colors resize-none',
        'focus:outline-none focus:ring-2 focus:ring-offset-0',
        sizeClasses,
        stateClasses,
        resize && 'resize-y'
      ]"
      @input="$emit('update:modelValue', $event.target.value)"
      @blur="$emit('blur', $event)"
      @focus="$emit('focus', $event)"
    />

    <div class="flex justify-between mt-1">
      <p v-if="error || helperText" :class="['text-sm', error ? 'text-red-500' : 'text-gray-500 dark:text-gray-400']">
        {{ error || helperText }}
      </p>
      <p v-if="showCount && maxlength" class="text-sm text-gray-500 dark:text-gray-400">
        {{ modelValue?.length || 0 }} / {{ maxlength }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  helperText: { type: String, default: '' },
  error: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  readonly: { type: Boolean, default: false },
  required: { type: Boolean, default: false },
  rows: { type: Number, default: 3 },
  maxlength: { type: Number, default: null },
  showCount: { type: Boolean, default: false },
  resize: { type: Boolean, default: false },
  size: { type: String, default: 'md' }
})

defineEmits(['update:modelValue', 'blur', 'focus'])

const textareaId = `textarea-${Math.random().toString(36).substr(2, 9)}`

const sizeClasses = computed(() => {
  const sizes = { sm: 'py-1.5 px-3 text-sm', md: 'py-2 px-4 text-sm', lg: 'py-3 px-4 text-base' }
  return sizes[props.size]
})

const stateClasses = computed(() => {
  if (props.disabled) return 'bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-500 cursor-not-allowed'
  if (props.error) return 'border-red-500 focus:ring-red-500 focus:border-red-500 text-gray-900 dark:text-white dark:bg-gray-700'
  return 'border-gray-300 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500 text-gray-900 dark:text-white dark:bg-gray-700'
})
</script>
