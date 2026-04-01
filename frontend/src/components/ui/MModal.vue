<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="close">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" aria-hidden="true" />

        <!-- Panel -->
        <div
          role="dialog"
          aria-modal="true"
          :class="[
            'relative w-full surface-modal rounded-panel overflow-hidden animate-scale-in',
            sizeClasses[size],
          ]"
        >
          <!-- Header -->
          <div v-if="title || $slots.header" class="flex items-center justify-between px-6 py-4 border-b divider">
            <slot name="header">
              <h2 class="text-title font-semibold text-[var(--text-primary)]">{{ title }}</h2>
            </slot>
            <button v-if="closable" @click="close" class="btn-icon p-1.5 -mr-1.5">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div :class="['overflow-y-auto', noPadding ? '' : 'px-6 py-5']" :style="{ maxHeight: 'calc(85vh - 8rem)' }">
            <slot />
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="flex items-center justify-end gap-3 px-6 py-4 border-t divider">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const props = defineProps({
  modelValue: Boolean,
  title: String,
  size: { type: String, default: 'md', validator: v => ['sm', 'md', 'lg', 'xl'].includes(v) },
  closable: { type: Boolean, default: true },
  noPadding: Boolean,
})

const emit = defineEmits(['update:modelValue'])

const sizeClasses = {
  sm: 'max-w-sm',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
}

function close() {
  emit('update:modelValue', false)
}
</script>

<style scoped>
.modal-enter-active { transition: opacity 0.2s ease; }
.modal-enter-active > div:last-child { transition: opacity 0.2s ease, transform 0.2s ease; }
.modal-leave-active { transition: opacity 0.15s ease; }
.modal-leave-active > div:last-child { transition: opacity 0.15s ease, transform 0.15s ease; }
.modal-enter-from { opacity: 0; }
.modal-enter-from > div:last-child { opacity: 0; transform: scale(0.95); }
.modal-leave-to { opacity: 0; }
.modal-leave-to > div:last-child { opacity: 0; transform: scale(0.95); }
</style>
