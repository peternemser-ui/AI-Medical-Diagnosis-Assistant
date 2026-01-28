<template>
  <nav class="flex items-center justify-between" aria-label="Pagination">
    <div v-if="showInfo" class="text-sm text-gray-700 dark:text-gray-300">
      Showing <span class="font-medium">{{ startItem }}</span> to <span class="font-medium">{{ endItem }}</span> of <span class="font-medium">{{ total }}</span> results
    </div>
    <div class="flex items-center space-x-2">
      <button
        :disabled="currentPage === 1"
        :class="[buttonClasses, { 'opacity-50 cursor-not-allowed': currentPage === 1 }]"
        @click="goToPage(currentPage - 1)"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
      </button>

      <template v-for="page in visiblePages" :key="page">
        <span v-if="page === '...'" class="px-3 py-2 text-gray-500">...</span>
        <button
          v-else
          :class="[buttonClasses, page === currentPage ? 'bg-blue-600 text-white border-blue-600' : '']"
          @click="goToPage(page)"
        >
          {{ page }}
        </button>
      </template>

      <button
        :disabled="currentPage === totalPages"
        :class="[buttonClasses, { 'opacity-50 cursor-not-allowed': currentPage === totalPages }]"
        @click="goToPage(currentPage + 1)"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, required: true },
  totalPages: { type: Number, required: true },
  total: { type: Number, default: 0 },
  perPage: { type: Number, default: 10 },
  showInfo: { type: Boolean, default: true },
  maxVisible: { type: Number, default: 5 }
})

const emit = defineEmits(['update:currentPage'])

const buttonClasses = 'px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors'

const startItem = computed(() => (props.currentPage - 1) * props.perPage + 1)
const endItem = computed(() => Math.min(props.currentPage * props.perPage, props.total))

const visiblePages = computed(() => {
  const pages = []
  const half = Math.floor(props.maxVisible / 2)
  let start = Math.max(1, props.currentPage - half)
  let end = Math.min(props.totalPages, start + props.maxVisible - 1)
  if (end - start < props.maxVisible - 1) start = Math.max(1, end - props.maxVisible + 1)

  if (start > 1) { pages.push(1); if (start > 2) pages.push('...') }
  for (let i = start; i <= end; i++) pages.push(i)
  if (end < props.totalPages) { if (end < props.totalPages - 1) pages.push('...'); pages.push(props.totalPages) }

  return pages
})

function goToPage(page) {
  if (page >= 1 && page <= props.totalPages) emit('update:currentPage', page)
}
</script>
