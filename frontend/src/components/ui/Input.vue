<template>
  <div class="w-full">
    <!-- Label -->
    <label
      v-if="label"
      :for="inputId"
      class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1"
    >
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>

    <!-- Input Wrapper -->
    <div class="relative">
      <!-- Prefix Icon/Text -->
      <div
        v-if="$slots.prefix || prefixIcon"
        class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
      >
        <slot name="prefix">
          <component
            v-if="prefixIcon"
            :is="prefixIcon"
            class="w-5 h-5 text-gray-400"
          />
        </slot>
      </div>

      <!-- Input Field -->
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :autocomplete="autocomplete"
        :class="[
          'block w-full rounded-lg border transition-colors',
          'focus:outline-none focus:ring-2 focus:ring-offset-0',
          sizeClasses,
          stateClasses,
          ($slots.prefix || prefixIcon) && 'pl-10',
          ($slots.suffix || suffixIcon || clearable) && 'pr-10'
        ]"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />

      <!-- Suffix Icon/Text or Clear Button -->
      <div
        v-if="$slots.suffix || suffixIcon || (clearable && modelValue)"
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
      >
        <button
          v-if="clearable && modelValue"
          type="button"
          @click="$emit('update:modelValue', '')"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <slot v-else name="suffix">
          <component
            v-if="suffixIcon"
            :is="suffixIcon"
            class="w-5 h-5 text-gray-400"
          />
        </slot>
      </div>
    </div>

    <!-- Helper/Error Text -->
    <p
      v-if="error || helperText"
      :class="[
        'mt-1 text-sm',
        error ? 'text-red-500' : 'text-gray-500 dark:text-gray-400'
      ]"
    >
      {{ error || helperText }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  helperText: {
    type: String,
    default: ''
  },
  error: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  clearable: {
    type: Boolean,
    default: false
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  prefixIcon: {
    type: [Object, Function],
    default: null
  },
  suffixIcon: {
    type: [Object, Function],
    default: null
  },
  autocomplete: {
    type: String,
    default: 'off'
  }
})

defineEmits(['update:modelValue', 'blur', 'focus'])

const inputId = `input-${Math.random().toString(36).substr(2, 9)}`

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'py-1.5 px-3 text-sm',
    md: 'py-2 px-4 text-sm',
    lg: 'py-3 px-4 text-base'
  }
  return sizes[props.size]
})

const stateClasses = computed(() => {
  if (props.disabled) {
    return 'bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-500 cursor-not-allowed'
  }
  if (props.error) {
    return 'border-red-500 dark:border-red-500 focus:ring-red-500 focus:border-red-500 text-gray-900 dark:text-white dark:bg-gray-700'
  }
  return 'border-gray-300 dark:border-gray-600 focus:ring-blue-500 focus:border-blue-500 text-gray-900 dark:text-white dark:bg-gray-700'
})
</script>
