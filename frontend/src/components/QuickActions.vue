<template>
  <div v-if="actions.length > 0" class="p-4 border-t border-gray-700 bg-gray-800">
    <h4 class="text-sm font-medium text-gray-300 mb-3">{{ title }}</h4>
    <div class="flex flex-wrap gap-2">
      <button
        v-for="action in actions"
        :key="action.id || action.text"
        @click="selectAction(action)"
        :disabled="disabled"
        class="text-sm bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-600 text-white px-4 py-2 rounded-full transition-all duration-200 transform hover:scale-105 disabled:hover:scale-100 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg"
        :title="action.description"
      >
        <div class="flex items-center gap-2">
          <!-- Material Icon if provided -->
          <MaterialIcon v-if="action.icon" :icon="action.icon" size="sm" />
          <span>{{ action.text }}</span>
        </div>
      </button>
    </div>
    
    <!-- Action categories -->
    <div v-if="categorizedActions && Object.keys(categorizedActions).length > 1" class="mt-4 space-y-3">
      <div v-for="(categoryActions, category) in categorizedActions" :key="category">
        <h5 class="text-xs font-medium text-gray-400 mb-2 uppercase tracking-wide">{{ category }}</h5>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="action in categoryActions"
            :key="action.id || action.text"
            @click="selectAction(action)"
            :disabled="disabled"
            class="text-xs bg-gray-700 hover:bg-gray-600 text-gray-300 hover:text-white px-3 py-1 rounded-full transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            :title="action.description"
          >
            {{ action.text }}
          </button>
        </div>
      </div>
    </div>

    <!-- Help text -->
    <div v-if="helpText" class="mt-3 text-xs text-gray-500">
      {{ helpText }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import MaterialIcon from './MaterialIcon.vue'

const props = defineProps({
  actions: {
    type: Array,
    default: () => [],
    validator: (actions) => {
      return actions.every(action => 
        typeof action === 'object' && 
        action.text && 
        typeof action.text === 'string'
      )
    }
  },
  title: {
    type: String,
    default: 'Quick Actions'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  helpText: {
    type: String,
    default: ''
  },
  categorize: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['action-selected'])

// Predefined quick actions for health diagnosis
const defaultHealthActions = [
  {
    id: 'symptoms-worse',
    text: 'Are my symptoms getting worse?',
    category: 'severity',
    description: 'Ask about symptom progression',
    icon: 'trending_down'
  },
  {
    id: 'when-doctor',
    text: 'When should I see a doctor?',
    category: 'care',
    description: 'Get guidance on when to seek medical attention',
    icon: 'person'
  },
  {
    id: 'home-remedies',
    text: 'What can I do at home?',
    category: 'treatment',
    description: 'Learn about home care options',
    icon: 'home'
  },
  {
    id: 'medications',
    text: 'Can I take over-the-counter medications?',
    category: 'treatment',
    description: 'Ask about medication options',
    icon: 'medication'
  },
  {
    id: 'contagious',
    text: 'Am I contagious?',
    category: 'safety',
    description: 'Learn about contagion risk',
    icon: 'groups'
  },
  {
    id: 'prevention',
    text: 'How can I prevent this in the future?',
    category: 'prevention',
    description: 'Get prevention advice',
    icon: 'shield'
  }
]

// Use provided actions or default health actions
const finalActions = computed(() => {
  return props.actions.length > 0 ? props.actions : defaultHealthActions
})

// Categorize actions if requested
const categorizedActions = computed(() => {
  if (!props.categorize) return null
  
  const categories = {}
  finalActions.value.forEach(action => {
    const category = action.category || 'general'
    if (!categories[category]) {
      categories[category] = []
    }
    categories[category].push(action)
  })
  
  return categories
})

const selectAction = (action) => {
  if (props.disabled) return
  
  emit('action-selected', action)
}
</script>

<style scoped>
/* Custom button hover effects */
.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* Gradient button animation */
.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradient-shift 3s ease infinite;
}

@keyframes gradient-shift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Category title styling */
.uppercase {
  letter-spacing: 0.05em;
}
</style>
