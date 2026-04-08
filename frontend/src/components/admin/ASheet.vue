<template>
  <Teleport to="body">
    <Transition name="a-sheet-backdrop">
      <div
        v-if="open"
        class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
        @click.self="$emit('close')"
      />
    </Transition>
    <Transition name="a-sheet-panel">
      <div
        v-if="open"
        :class="[
          'fixed top-0 right-0 z-50 h-full flex flex-col shadow-2xl',
          widthClass,
          isDark ? 'bg-slate-900 border-l border-slate-800' : 'bg-white border-l border-slate-200'
        ]"
      >
        <!-- Header -->
        <div
          :class="[
            'flex items-center justify-between px-6 py-4 border-b flex-shrink-0',
            isDark ? 'border-slate-800' : 'border-slate-200'
          ]"
        >
          <h2
            :class="[
              'text-lg font-semibold',
              isDark ? 'text-white' : 'text-slate-900'
            ]"
          >
            {{ title }}
          </h2>
          <button
            :class="[
              'p-1.5 rounded-lg transition-colors',
              isDark
                ? 'hover:bg-slate-800 text-slate-400 hover:text-slate-200'
                : 'hover:bg-slate-100 text-slate-500 hover:text-slate-700'
            ]"
            @click="$emit('close')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>

        <!-- Body -->
        <div class="flex-1 overflow-y-auto px-6 py-4">
          <slot />
        </div>

        <!-- Footer -->
        <div
          v-if="$slots.footer"
          :class="[
            'px-6 py-4 border-t flex-shrink-0',
            isDark ? 'border-slate-800' : 'border-slate-200'
          ]"
        >
          <slot name="footer" />
        </div>
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
    default: ''
  },
  width: {
    type: String,
    default: 'md',
    validator: v => ['md', 'lg', 'xl'].includes(v)
  }
})

defineEmits(['close'])

const widthClass = computed(() => {
  const map = { md: 'w-[480px]', lg: 'w-[640px]', xl: 'w-[800px]' }
  return map[props.width]
})
</script>

<style scoped>
.a-sheet-backdrop-enter-active,
.a-sheet-backdrop-leave-active {
  transition: opacity 0.25s ease;
}
.a-sheet-backdrop-enter-from,
.a-sheet-backdrop-leave-to {
  opacity: 0;
}

.a-sheet-panel-enter-active,
.a-sheet-panel-leave-active {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.a-sheet-panel-enter-from,
.a-sheet-panel-leave-to {
  transform: translateX(100%);
}
</style>
