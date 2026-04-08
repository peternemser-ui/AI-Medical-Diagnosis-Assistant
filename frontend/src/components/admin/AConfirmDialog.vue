<template>
  <Teleport to="body">
    <Transition name="a-dialog-backdrop">
      <div
        v-if="open"
        class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4"
        @click.self="$emit('cancel')"
      >
        <Transition name="a-dialog-panel" appear>
          <div
            v-if="open"
            :class="[
              'w-full max-w-md rounded-2xl border p-6 shadow-xl',
              isDark ? 'bg-slate-900 border-slate-800' : 'bg-white border-slate-200'
            ]"
          >
            <!-- Icon -->
            <div
              :class="[
                'w-12 h-12 rounded-full flex items-center justify-center mb-4',
                variantStyles.iconBg
              ]"
            >
              <svg
                v-if="variant === 'danger'"
                xmlns="http://www.w3.org/2000/svg"
                class="w-6 h-6"
                :class="variantStyles.iconColor"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg
                v-else-if="variant === 'warning'"
                xmlns="http://www.w3.org/2000/svg"
                class="w-6 h-6"
                :class="variantStyles.iconColor"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="w-6 h-6"
                :class="variantStyles.iconColor"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
            </div>

            <!-- Title -->
            <h3
              :class="[
                'text-lg font-semibold mb-2',
                isDark ? 'text-white' : 'text-slate-900'
              ]"
            >
              {{ title }}
            </h3>

            <!-- Message -->
            <p
              :class="[
                'text-sm mb-6',
                isDark ? 'text-slate-400' : 'text-slate-500'
              ]"
            >
              {{ message }}
            </p>

            <!-- Buttons -->
            <div class="flex items-center justify-end gap-3">
              <button
                :class="[
                  'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                  isDark
                    ? 'text-slate-300 hover:bg-slate-800'
                    : 'text-slate-600 hover:bg-slate-100'
                ]"
                @click="$emit('cancel')"
              >
                Cancel
              </button>
              <button
                :class="[
                  'px-4 py-2 text-sm font-medium rounded-lg text-white transition-colors',
                  variantStyles.button
                ]"
                @click="$emit('confirm')"
              >
                {{ confirmLabel }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  open: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: 'Confirm'
  },
  message: {
    type: String,
    default: ''
  },
  confirmLabel: {
    type: String,
    default: 'Confirm'
  },
  variant: {
    type: String,
    default: 'safe',
    validator: v => ['danger', 'warning', 'safe'].includes(v)
  }
})

defineEmits(['confirm', 'cancel'])

const variantStyles = computed(() => {
  const map = {
    danger: {
      iconBg: isDark.value ? 'bg-red-500/10' : 'bg-red-50',
      iconColor: isDark.value ? 'text-red-400' : 'text-red-500',
      button: 'bg-red-600 hover:bg-red-700'
    },
    warning: {
      iconBg: isDark.value ? 'bg-amber-500/10' : 'bg-amber-50',
      iconColor: isDark.value ? 'text-amber-400' : 'text-amber-500',
      button: 'bg-amber-600 hover:bg-amber-700'
    },
    safe: {
      iconBg: isDark.value ? 'bg-blue-500/10' : 'bg-blue-50',
      iconColor: isDark.value ? 'text-blue-400' : 'text-blue-500',
      button: 'bg-blue-600 hover:bg-blue-700'
    }
  }
  return map[props.variant]
})
</script>

<style scoped>
.a-dialog-backdrop-enter-active,
.a-dialog-backdrop-leave-active {
  transition: opacity 0.2s ease;
}
.a-dialog-backdrop-enter-from,
.a-dialog-backdrop-leave-to {
  opacity: 0;
}

.a-dialog-panel-enter-active {
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.2s ease;
}
.a-dialog-panel-leave-active {
  transition: transform 0.15s ease, opacity 0.15s ease;
}
.a-dialog-panel-enter-from {
  opacity: 0;
  transform: scale(0.95) translateY(8px);
}
.a-dialog-panel-leave-to {
  opacity: 0;
  transform: scale(0.97);
}
</style>
