<template>
  <div class="skeleton-loader">
    <div v-for="n in count" :key="n" :class="n > 1 ? 'mt-4' : ''">

      <!-- chat-message: circle avatar + 3 lines of varying width -->
      <div v-if="type === 'chat-message'" class="flex items-start gap-3">
        <div
          class="w-9 h-9 rounded-full flex-shrink-0 skeleton-shimmer"
          :class="shimmerBg"
        />
        <div class="flex-1 space-y-2.5 pt-1">
          <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 75%" />
          <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 90%" />
          <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 55%" />
        </div>
      </div>

      <!-- card: rounded rectangle with title bar + 2 body lines -->
      <div
        v-else-if="type === 'card'"
        class="rounded-xl border p-4"
        :class="isDark ? 'border-slate-700/40 bg-slate-800/30' : 'border-slate-200 bg-white'"
      >
        <div class="h-5 rounded-lg skeleton-shimmer mb-3" :class="shimmerBg" style="width: 45%" />
        <div class="space-y-2.5">
          <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 100%" />
          <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 80%" />
        </div>
      </div>

      <!-- list: 4-5 rows with icon placeholder + text -->
      <div v-else-if="type === 'list'" class="space-y-3">
        <div
          v-for="(w, i) in listWidths"
          :key="'list-' + i"
          class="flex items-center gap-3"
        >
          <div
            class="w-7 h-7 rounded-lg flex-shrink-0 skeleton-shimmer"
            :class="shimmerBg"
          />
          <div class="h-3 rounded-lg skeleton-shimmer flex-1" :class="shimmerBg" :style="{ maxWidth: w }" />
        </div>
      </div>

      <!-- report-header: large title + 3 metadata pills + badge -->
      <div v-else-if="type === 'report-header'" class="space-y-4">
        <div class="h-7 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 55%" />
        <div class="flex items-center gap-3 flex-wrap">
          <div
            v-for="pw in pillWidths"
            :key="'pill-' + pw"
            class="h-6 rounded-full skeleton-shimmer"
            :class="shimmerBg"
            :style="{ width: pw }"
          />
          <div class="h-6 w-16 rounded-md skeleton-shimmer" :class="shimmerBg" />
        </div>
      </div>

      <!-- text-block: 4 lines of varying width -->
      <div v-else-if="type === 'text-block'" class="space-y-2.5">
        <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 100%" />
        <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 85%" />
        <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 92%" />
        <div class="h-3 rounded-lg skeleton-shimmer" :class="shimmerBg" style="width: 60%" />
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme.js'

const { isDark } = useTheme()

defineProps({
  type: {
    type: String,
    default: 'text-block',
    validator: (v) => ['chat-message', 'card', 'list', 'report-header', 'text-block'].includes(v)
  },
  count: {
    type: Number,
    default: 1
  }
})

const shimmerBg = computed(() =>
  isDark.value ? 'skeleton-shimmer-dark' : 'skeleton-shimmer-light'
)

const listWidths = ['85%', '70%', '90%', '60%', '75%']
const pillWidths = ['6rem', '7.5rem', '5.5rem']
</script>

<style scoped>
.skeleton-shimmer {
  position: relative;
  overflow: hidden;
}

.skeleton-shimmer-dark {
  background: rgba(51, 65, 85, 0.35);
}

.skeleton-shimmer-light {
  background: rgba(203, 213, 225, 0.6);
}

.skeleton-shimmer::after {
  content: '';
  position: absolute;
  inset: 0;
  transform: translateX(-100%);
  animation: shimmer 1.8s infinite ease-in-out;
}

.skeleton-shimmer-dark::after {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(148, 163, 184, 0.08) 40%,
    rgba(148, 163, 184, 0.14) 50%,
    rgba(148, 163, 184, 0.08) 60%,
    transparent 100%
  );
}

.skeleton-shimmer-light::after {
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.5) 40%,
    rgba(255, 255, 255, 0.7) 50%,
    rgba(255, 255, 255, 0.5) 60%,
    transparent 100%
  );
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
