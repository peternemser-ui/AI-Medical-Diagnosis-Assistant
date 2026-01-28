<template>
  <div class="relative inline-block text-left" ref="dropdownRef">
    <div @click="toggle">
      <slot name="trigger">
        <button type="button" class="inline-flex justify-center w-full px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          Options
          <svg class="w-5 h-5 ml-2 -mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </slot>
    </div>

    <Transition name="dropdown">
      <div
        v-if="isOpen"
        :class="['absolute z-50 mt-2 rounded-lg bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none', widthClass, alignmentClass]"
      >
        <div class="py-1" role="menu">
          <slot>
            <button
              v-for="item in items"
              :key="item.id || item.label"
              type="button"
              :disabled="item.disabled"
              :class="[
                'flex items-center w-full px-4 py-2 text-sm text-left transition-colors',
                item.disabled
                  ? 'text-gray-400 cursor-not-allowed'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700',
                item.danger && 'text-red-600 dark:text-red-400'
              ]"
              @click="selectItem(item)"
            >
              <component v-if="item.icon" :is="item.icon" class="w-4 h-4 mr-3" />
              {{ item.label }}
            </button>
          </slot>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  items: { type: Array, default: () => [] },
  align: { type: String, default: 'left', validator: v => ['left', 'right'].includes(v) },
  width: { type: String, default: '48' }
})

const emit = defineEmits(['select'])

const isOpen = ref(false)
const dropdownRef = ref(null)

function toggle() { isOpen.value = !isOpen.value }
function close() { isOpen.value = false }

function selectItem(item) {
  if (!item.disabled) {
    emit('select', item)
    close()
  }
}

function handleClickOutside(event) {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    close()
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))

const widthClass = computed(() => `w-${props.width}`)
const alignmentClass = computed(() => props.align === 'right' ? 'right-0' : 'left-0')
</script>

<style scoped>
.dropdown-enter-active, .dropdown-leave-active { transition: opacity 0.1s ease, transform 0.1s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: scale(0.95); }
</style>
