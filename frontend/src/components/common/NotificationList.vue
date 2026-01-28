<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-50 space-y-2 w-96">
      <TransitionGroup name="notification">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'flex items-start p-4 rounded-lg shadow-lg',
            typeClasses[notification.type]
          ]"
        >
          <component :is="typeIcons[notification.type]" class="w-5 h-5 mr-3 flex-shrink-0" />
          <div class="flex-1 min-w-0">
            <p v-if="notification.title" class="font-medium">{{ notification.title }}</p>
            <p class="text-sm opacity-90">{{ notification.message }}</p>
          </div>
          <button
            v-if="notification.dismissible"
            @click="dismiss(notification.id)"
            class="ml-3 opacity-70 hover:opacity-100"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { h } from 'vue'
import { useNotifications } from '@/composables/useNotifications'

const { notifications, dismiss } = useNotifications()

const typeClasses = {
  success: 'bg-green-600 text-white',
  error: 'bg-red-600 text-white',
  warning: 'bg-yellow-500 text-white',
  info: 'bg-blue-600 text-white',
  loading: 'bg-gray-700 text-white'
}

const typeIcons = {
  success: h('svg', { fill: 'currentColor', viewBox: '0 0 20 20' }, [h('path', { 'fill-rule': 'evenodd', d: 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z', 'clip-rule': 'evenodd' })]),
  error: h('svg', { fill: 'currentColor', viewBox: '0 0 20 20' }, [h('path', { 'fill-rule': 'evenodd', d: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z', 'clip-rule': 'evenodd' })]),
  warning: h('svg', { fill: 'currentColor', viewBox: '0 0 20 20' }, [h('path', { 'fill-rule': 'evenodd', d: 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z', 'clip-rule': 'evenodd' })]),
  info: h('svg', { fill: 'currentColor', viewBox: '0 0 20 20' }, [h('path', { 'fill-rule': 'evenodd', d: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z', 'clip-rule': 'evenodd' })]),
  loading: h('svg', { class: 'animate-spin', fill: 'none', viewBox: '0 0 24 24' }, [h('circle', { class: 'opacity-25', cx: '12', cy: '12', r: '10', stroke: 'currentColor', 'stroke-width': '4' }), h('path', { class: 'opacity-75', fill: 'currentColor', d: 'M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z' })])
}
</script>

<style scoped>
.notification-enter-active { transition: all 0.3s ease; }
.notification-leave-active { transition: all 0.3s ease; }
.notification-enter-from { opacity: 0; transform: translateX(100%); }
.notification-leave-to { opacity: 0; transform: translateX(100%); }
</style>
