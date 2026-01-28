<template>
  <Modal :is-open="isOpen" :title="title" size="sm" @close="cancel">
    <p class="text-gray-600 dark:text-gray-400">{{ message }}</p>
    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="cancel"
          class="px-4 py-2 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
        >
          {{ cancelText }}
        </button>
        <button
          @click="confirm"
          :class="[
            'px-4 py-2 rounded-lg text-white',
            variant === 'danger' ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'
          ]"
        >
          {{ confirmText }}
        </button>
      </div>
    </template>
  </Modal>
</template>

<script setup>
import Modal from '../ui/Modal.vue'

defineProps({
  isOpen: { type: Boolean, default: false },
  title: { type: String, default: 'Confirm' },
  message: { type: String, default: 'Are you sure?' },
  confirmText: { type: String, default: 'Confirm' },
  cancelText: { type: String, default: 'Cancel' },
  variant: { type: String, default: 'primary' }
})

const emit = defineEmits(['confirm', 'cancel'])
const confirm = () => emit('confirm')
const cancel = () => emit('cancel')
</script>
