<template>
  <div>
    <div :class="['border-b border-gray-200 dark:border-gray-700', variant === 'pills' && 'border-none']">
      <nav :class="['-mb-px flex', variant === 'pills' ? 'space-x-2' : 'space-x-8']" role="tablist">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          role="tab"
          :aria-selected="modelValue === tab.id"
          :disabled="tab.disabled"
          :class="[
            'whitespace-nowrap font-medium focus:outline-none transition-colors',
            tabClasses(tab.id),
            tab.disabled && 'opacity-50 cursor-not-allowed'
          ]"
          @click="!tab.disabled && $emit('update:modelValue', tab.id)"
        >
          <component v-if="tab.icon" :is="tab.icon" class="w-4 h-4 mr-2" />
          {{ tab.label }}
          <span v-if="tab.count !== undefined" class="ml-2 px-2 py-0.5 text-xs rounded-full bg-gray-100 dark:bg-gray-700">
            {{ tab.count }}
          </span>
        </button>
      </nav>
    </div>
    <div class="mt-4">
      <slot :active-tab="modelValue" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, required: true },
  tabs: { type: Array, required: true },
  variant: { type: String, default: 'underline', validator: v => ['underline', 'pills'].includes(v) }
})

defineEmits(['update:modelValue'])

const tabClasses = computed(() => (tabId) => {
  const isActive = props.modelValue === tabId
  if (props.variant === 'pills') {
    return isActive
      ? 'px-4 py-2 text-sm rounded-lg bg-blue-600 text-white'
      : 'px-4 py-2 text-sm rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
  }
  return isActive
    ? 'py-4 px-1 text-sm border-b-2 border-blue-600 text-blue-600'
    : 'py-4 px-1 text-sm border-b-2 border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300'
})
</script>
