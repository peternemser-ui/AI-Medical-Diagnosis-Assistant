<template>
  <button
    @click="toggleTheme"
    class="theme-toggle"
    :class="{ 'is-dark': isDark }"
    :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    aria-label="Toggle theme"
  >
    <!-- Sun Icon (Light Mode) -->
    <transition name="icon-fade">
      <svg
        v-if="!isDark"
        class="icon sun-icon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      </svg>
    </transition>
    
    <!-- Moon Icon (Dark Mode) -->
    <transition name="icon-fade">
      <svg
        v-if="isDark"
        class="icon moon-icon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    </transition>
    
    <!-- Label (optional) -->
    <span v-if="showLabel" class="theme-label">
      {{ isDark ? 'Dark' : 'Light' }}
    </span>
  </button>
</template>

<script setup>
import { onMounted } from 'vue'
import { useTheme } from '../composables/useTheme.js'

defineProps({
  showLabel: {
    type: Boolean,
    default: false
  }
})

const { isDark, toggleTheme, initializeTheme } = useTheme()

onMounted(() => {
  initializeTheme()
})
</script>

<style scoped>
.theme-toggle {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.theme-toggle:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.theme-toggle:active {
  transform: translateY(0);
}

.theme-toggle.is-dark {
  background: rgba(30, 30, 46, 0.8);
  border-color: rgba(147, 197, 253, 0.3);
}

.theme-toggle.is-dark:hover {
  background: rgba(30, 30, 46, 0.95);
  border-color: rgba(147, 197, 253, 0.5);
  box-shadow: 0 4px 12px rgba(147, 197, 253, 0.2);
}

.icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #ffffff;
  transition: all 0.3s ease;
}

.sun-icon {
  color: #fbbf24;
  filter: drop-shadow(0 0 4px rgba(251, 191, 36, 0.5));
}

.moon-icon {
  color: #93c5fd;
  filter: drop-shadow(0 0 4px rgba(147, 197, 253, 0.5));
}

.theme-toggle:hover .sun-icon {
  transform: rotate(45deg);
  color: #f59e0b;
}

.theme-toggle:hover .moon-icon {
  transform: rotate(-15deg);
  color: #60a5fa;
}

.theme-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #ffffff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

/* Icon transition animations */
.icon-fade-enter-active,
.icon-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.icon-fade-enter-from {
  opacity: 0;
  transform: rotate(-90deg) scale(0.5);
}

.icon-fade-leave-to {
  opacity: 0;
  transform: rotate(90deg) scale(0.5);
}

.icon-fade-enter-to,
.icon-fade-leave-from {
  opacity: 1;
  transform: rotate(0) scale(1);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .theme-toggle {
    padding: 0.5rem;
  }
  
  .icon {
    width: 1.125rem;
    height: 1.125rem;
  }
  
  .theme-label {
    font-size: 0.8125rem;
  }
}

/* Dark mode specific styles */
:root[data-theme="dark"] .theme-toggle {
  background: rgba(30, 41, 59, 0.7);
  border-color: rgba(148, 163, 184, 0.3);
}

:root[data-theme="dark"] .theme-toggle:hover {
  background: rgba(30, 41, 59, 0.9);
  border-color: rgba(148, 163, 184, 0.5);
}
</style>
