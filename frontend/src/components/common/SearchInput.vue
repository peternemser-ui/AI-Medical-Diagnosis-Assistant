<template>
  <div class="relative">
    <input
      :value="modelValue"
      type="search"
      :placeholder="placeholder"
      :class="[
        'w-full pl-10 pr-4 py-2 border rounded-lg',
        'focus:outline-none focus:ring-2 focus:ring-blue-500',
        'dark:bg-gray-700 dark:border-gray-600 dark:text-white'
      ]"
      @input="$emit('update:modelValue', $event.target.value)"
      @keyup.enter="$emit('search', modelValue)"
    />
    <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
    </svg>
    <button
      v-if="modelValue"
      @click="clear"
      class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
    >
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Search...' }
})

const emit = defineEmits(['update:modelValue', 'search', 'clear'])

const clear = () => {
  emit('update:modelValue', '')
  emit('clear')
}
</script>
