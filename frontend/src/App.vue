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
    <Transition name="offline-bar">
      <div
        v-if="showUpdateBanner"
        class="fixed top-0 left-0 right-0 z-[9998] bg-blue-600 text-white text-center text-sm font-medium py-1.5 px-4 shadow-md flex items-center justify-center gap-3"
      >
        New version available — refresh to update
        <button @click="reloadPage" class="underline font-semibold hover:text-blue-200">Refresh</button>
        <button @click="showUpdateBanner = false" class="ml-2 text-blue-200 hover:text-white">&times;</button>
      </div>
    </Transition>
    <ErrorBoundary>
      <router-view v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </ErrorBoundary>
    <HelpButton v-if="showHelpButton" />
    <ToastContainer />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import ToastContainer from '@/components/ToastContainer.vue'
import HelpButton from '@/components/HelpButton.vue'
import ErrorBoundary from '@/components/ErrorBoundary.vue'
import { useOnlineStatus } from '@/composables/useOnlineStatus'
import { useKeyboardShortcuts } from '@/composables/useKeyboardShortcuts'
import { trackPageView } from '@/composables/useAnalytics'

const { isOnline } = useOnlineStatus()
const route = useRoute()

useKeyboardShortcuts()

// Track page views on every route change (local analytics only, no external services)
watch(
  () => route.path,
  (path) => {
    if (path) trackPageView(path)
  },
  { immediate: true }
)

const showHelpButton = computed(() => {
  const path = route.path || ''
  return !path.startsWith('/help') && !path.startsWith('/admin')
})

// App update notification
const showUpdateBanner = ref(false)

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    showUpdateBanner.value = true
  })
}

function reloadPage() {
  window.location.reload()
}
</script>

<style>
/*
  App.vue scoped global layout — minimal.
  Page transition classes (.page-*) live in index.css @layer utilities.
*/

/* Offline / update banner slide-down transition */
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

@media (prefers-reduced-motion: reduce) {
  .offline-bar-enter-active,
  .offline-bar-leave-active {
    transition-duration: 0ms;
  }
}
</style>
