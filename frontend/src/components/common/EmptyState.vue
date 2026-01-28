<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <div v-if="$slots.icon || icon" class="mb-4">
      <slot name="icon">
        <component :is="icon" class="w-16 h-16 text-gray-400" />
      </slot>
    </div>
    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
      {{ title }}
    </h3>
    <p v-if="description" class="text-sm text-gray-500 dark:text-gray-400 max-w-sm mb-6">
      {{ description }}
    </p>
    <slot name="action">
      <button
        v-if="actionLabel"
        @click="$emit('action')"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        {{ actionLabel }}
      </button>
    </slot>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: 'No data found' },
  description: { type: String, default: '' },
  icon: { type: [Object, Function], default: null },
  actionLabel: { type: String, default: '' }
})
defineEmits(['action'])
</script>
