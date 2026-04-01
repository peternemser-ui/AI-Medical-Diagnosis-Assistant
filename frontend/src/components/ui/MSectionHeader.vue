<template>
  <div class="section-header">
    <div v-if="icon" class="w-8 h-8 rounded-btn flex items-center justify-center flex-shrink-0" :class="iconBgClass">
      <span class="text-body">{{ icon }}</span>
    </div>
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2">
        <h3 class="section-title truncate">{{ title }}</h3>
        <slot name="badge" />
      </div>
      <p v-if="subtitle" class="section-subtitle mt-0.5">{{ subtitle }}</p>
    </div>
    <div v-if="$slots.actions" class="flex items-center gap-2 flex-shrink-0">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  title: { type: String, required: true },
  subtitle: String,
  icon: String,
  iconVariant: { type: String, default: 'blue' },
})

const iconBgClasses = {
  blue:    'bg-blue-500/10 text-blue-600 dark:text-blue-400',
  brand:   'bg-brand-500/10 text-brand-600 dark:text-brand-400',
  purple:  'bg-purple-500/10 text-purple-600 dark:text-purple-400',
  red:     'bg-red-500/10 text-red-600 dark:text-red-400',
  amber:   'bg-amber-500/10 text-amber-600 dark:text-amber-400',
  slate:   'bg-slate-500/10 text-slate-600 dark:text-slate-400',
}

const iconBgClass = computed(() => iconBgClasses[props.iconVariant] || iconBgClasses.blue)
</script>
