<template>
  <div class="loading-skeleton" :class="skeletonClass" role="status" aria-live="polite" aria-label="Loading">
    <div v-if="variant === 'text'" class="skeleton-text" :style="textStyle"></div>

    <div v-else-if="variant === 'circle'" class="skeleton-circle" :style="circleStyle"></div>

    <div v-else-if="variant === 'rectangle'" class="skeleton-rectangle" :style="rectangleStyle"></div>

    <div v-else-if="variant === 'card'" class="skeleton-card">
      <div class="skeleton-card-header">
        <div class="skeleton-circle" style="width: 48px; height: 48px;"></div>
        <div class="skeleton-text-group">
          <div class="skeleton-text" style="width: 60%;"></div>
          <div class="skeleton-text" style="width: 40%; height: 12px;"></div>
        </div>
      </div>
      <div class="skeleton-card-content">
        <div class="skeleton-text" style="width: 100%;"></div>
        <div class="skeleton-text" style="width: 90%;"></div>
        <div class="skeleton-text" style="width: 75%;"></div>
      </div>
    </div>

    <div v-else-if="variant === 'message'" class="skeleton-message">
      <div class="skeleton-message-avatar skeleton-circle"></div>
      <div class="skeleton-message-content">
        <div class="skeleton-text" style="width: 30%; height: 14px; margin-bottom: 8px;"></div>
        <div class="skeleton-text" style="width: 100%;"></div>
        <div class="skeleton-text" style="width: 80%;"></div>
      </div>
    </div>

    <div v-else-if="variant === 'list'" class="skeleton-list">
      <div v-for="i in count" :key="i" class="skeleton-list-item">
        <div class="skeleton-text" style="width: 100%; height: 20px;"></div>
      </div>
    </div>

    <span class="sr-only">Loading content...</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'circle', 'rectangle', 'card', 'message', 'list'].includes(value)
  },
  width: {
    type: [String, Number],
    default: '100%'
  },
  height: {
    type: [String, Number],
    default: '20px'
  },
  count: {
    type: Number,
    default: 3
  },
  animation: {
    type: String,
    default: 'wave',
    validator: (value) => ['wave', 'pulse', 'none'].includes(value)
  },
  dark: {
    type: Boolean,
    default: false
  }
})

const skeletonClass = computed(() => ({
  [`skeleton-${props.animation}`]: props.animation !== 'none',
  'skeleton-dark': props.dark
}))

const textStyle = computed(() => ({
  width: typeof props.width === 'number' ? `${props.width}px` : props.width,
  height: typeof props.height === 'number' ? `${props.height}px` : props.height
}))

const circleStyle = computed(() => {
  const size = typeof props.width === 'number' ? `${props.width}px` : props.width
  return {
    width: size,
    height: size
  }
})

const rectangleStyle = computed(() => ({
  width: typeof props.width === 'number' ? `${props.width}px` : props.width,
  height: typeof props.height === 'number' ? `${props.height}px` : props.height
}))
</script>

<style scoped>
.loading-skeleton {
  display: block;
}

.skeleton-text,
.skeleton-circle,
.skeleton-rectangle {
  background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);
  background-size: 200% 100%;
  border-radius: 4px;
}

.skeleton-dark .skeleton-text,
.skeleton-dark .skeleton-circle,
.skeleton-dark .skeleton-rectangle {
  background: linear-gradient(90deg, #2a2a2a 25%, #3a3a3a 50%, #2a2a2a 75%);
  background-size: 200% 100%;
}

.skeleton-text {
  height: 20px;
  margin-bottom: 8px;
}

.skeleton-circle {
  border-radius: 50%;
}

.skeleton-rectangle {
  border-radius: 8px;
}

/* Animations */
.skeleton-wave .skeleton-text,
.skeleton-wave .skeleton-circle,
.skeleton-wave .skeleton-rectangle {
  animation: wave 1.5s ease-in-out infinite;
}

.skeleton-pulse .skeleton-text,
.skeleton-pulse .skeleton-circle,
.skeleton-pulse .skeleton-rectangle {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes wave {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Card skeleton */
.skeleton-card {
  padding: 16px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.skeleton-card-header {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.skeleton-text-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-card-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Message skeleton */
.skeleton-message {
  display: flex;
  gap: 12px;
  padding: 12px;
}

.skeleton-message-avatar {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.skeleton-message-content {
  flex: 1;
}

/* List skeleton */
.skeleton-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-list-item {
  padding: 12px;
}

/* Screen reader only */
.sr-only {
  position: absolute;
  left: -10000px;
  width: 1px;
  height: 1px;
  overflow: hidden;
}
</style>
