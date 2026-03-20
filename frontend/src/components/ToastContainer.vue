<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[100] flex flex-col gap-2 pointer-events-none" style="max-width: 380px;">
      <TransitionGroup
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 translate-x-8 scale-95"
        enter-to-class="opacity-100 translate-x-0 scale-100"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 translate-x-0 scale-100"
        leave-to-class="opacity-0 translate-x-8 scale-95"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="pointer-events-auto flex items-start gap-2.5 px-4 py-3 rounded-xl shadow-2xl border backdrop-blur-xl text-sm"
          :class="toastClass(toast.type)"
        >
          <!-- Icon -->
          <div class="flex-shrink-0 mt-0.5">
            <svg v-if="toast.type === 'success'" class="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="toast.type === 'error'" class="w-4 h-4 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="toast.type === 'warning'" class="w-4 h-4 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
          </div>
          <!-- Message -->
          <span class="flex-1 leading-snug" :class="isDark ? 'text-slate-200' : 'text-slate-700'">{{ toast.message }}</span>
          <!-- Close -->
          <button @click="removeToast(toast.id)" class="flex-shrink-0 p-0.5 rounded-md transition-colors" :class="isDark ? 'text-slate-500 hover:text-slate-300' : 'text-slate-400 hover:text-slate-600'">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '@/composables/useToast.js'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()
const { toasts, removeToast } = useToast()

function toastClass(type) {
  if (isDark.value) {
    const base = 'bg-slate-900/95 border-slate-700/60'
    if (type === 'success') return base + ' border-l-2 border-l-emerald-500'
    if (type === 'error') return base + ' border-l-2 border-l-red-500'
    if (type === 'warning') return base + ' border-l-2 border-l-amber-500'
    return base + ' border-l-2 border-l-blue-500'
  } else {
    const base = 'bg-white/95 border-slate-200'
    if (type === 'success') return base + ' border-l-2 border-l-emerald-500'
    if (type === 'error') return base + ' border-l-2 border-l-red-500'
    if (type === 'warning') return base + ' border-l-2 border-l-amber-500'
    return base + ' border-l-2 border-l-blue-500'
  }
}
</script>
