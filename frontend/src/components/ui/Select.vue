<template>
  <div class="w-full">
    <label
      v-if="label"
      :for="selectId"
      class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <div class="relative">
      <select
        :id="selectId"
        :value="modelValue"
        :disabled="disabled"
        :required="required"
        :class="[
          'block w-full rounded-lg border appearance-none pr-10',
          'focus:outline-none focus:ring-2 focus:ring-offset-0',
          sizeClasses,
          stateClasses
        ]"
        @change="$emit('update:modelValue', $event.target.value)"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option
          v-for="option in normalizedOptions"
          :key="option.value"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>

      <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
        <svg class="w-5 h-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </div>
    </div>

    <p
      v-if="error || helperText"
      :class="['mt-1 text-sm', error ? 'text-red-500' : 'text-gray-500 dark:text-gray-400']"
    >
      {{ error || helperText }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, default: () => [] },
  label: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  helperText: { type: String, default: '' },
  error: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  required: { type: Boolean, default: false },
  size: { type: String, default: 'md' }
})

defineEmits(['update:modelValue'])

const selectId = `select-${Math.random().toString(36).substr(2, 9)}`

const normalizedOptions = computed(() => {
  return props.options.map(opt => {
    if (typeof opt === 'object') return opt
    return { value: opt, label: opt }
  })
})

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
