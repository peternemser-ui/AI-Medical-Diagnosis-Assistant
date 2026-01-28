<template>
  <div class="relative inline-block" @mouseenter="show" @mouseleave="hide" @focus="show" @blur="hide">
    <slot />
    <Transition name="tooltip">
      <div
        v-if="isVisible && content"
        :class="['absolute z-50 px-2 py-1 text-xs font-medium text-white bg-gray-900 dark:bg-gray-700 rounded shadow-lg whitespace-nowrap', positionClasses]"
        role="tooltip"
      >
        {{ content }}
        <div :class="['absolute w-2 h-2 bg-gray-900 dark:bg-gray-700 transform rotate-45', arrowClasses]" />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  content: { type: String, default: '' },
  position: { type: String, default: 'top', validator: v => ['top', 'bottom', 'left', 'right'].includes(v) },
  delay: { type: Number, default: 200 }
})

const isVisible = ref(false)
let timeout = null

function show() {
  timeout = setTimeout(() => { isVisible.value = true }, props.delay)
}

function hide() {
  clearTimeout(timeout)
  isVisible.value = false
}

const positionClasses = computed(() => {
  const positions = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2'
  }
  return positions[props.position]
})

const arrowClasses = computed(() => {
  const arrows = {
    top: 'top-full left-1/2 -translate-x-1/2 -mt-1',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 -mb-1',
    left: 'left-full top-1/2 -translate-y-1/2 -ml-1',
    right: 'right-full top-1/2 -translate-y-1/2 -mr-1'
  }
  return arrows[props.position]
})
</script>

<style scoped>
.tooltip-enter-active, .tooltip-leave-active { transition: opacity 0.15s ease; }
.tooltip-enter-from, .tooltip-leave-to { opacity: 0; }
</style>
