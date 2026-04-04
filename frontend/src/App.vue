<template>
  <div id="app">
    <Transition name="offline-bar">
      <div
        v-if="!isOnline"
        class="fixed top-0 left-0 right-0 z-[9999] bg-amber-500 text-amber-950 text-center text-sm font-medium py-1.5 px-4 shadow-md"
      >
        You're offline — some features may be limited
      </div>
    </Transition>
    <router-view v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </router-view>
    <ToastContainer />
  </div>
</template>

<script setup>
import ToastContainer from '@/components/ToastContainer.vue'
import { useOnlineStatus } from '@/composables/useOnlineStatus'

const { isOnline } = useOnlineStatus()
</script>

<style>
/* Global styles */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

* {
  box-sizing: border-box;
}

/* Page transitions */
.page-enter-active {
  transition: opacity 0.2s ease-out;
}
.page-leave-active {
  transition: opacity 0.15s ease-in;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}

/* Offline bar transition */
.offline-bar-enter-active {
  transition: transform 0.3s ease-out, opacity 0.3s ease-out;
}
.offline-bar-leave-active {
  transition: transform 0.2s ease-in, opacity 0.2s ease-in;
}
.offline-bar-enter-from,
.offline-bar-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
