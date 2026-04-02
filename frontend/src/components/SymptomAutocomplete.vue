<template>
  <div class="relative" ref="containerRef">
    <!-- Dropdown -->
    <Transition name="fade">
      <div v-if="showSuggestions && filtered.length > 0"
        class="absolute bottom-full left-0 right-0 mb-1 rounded-card overflow-hidden shadow-elevated z-50 max-h-48 overflow-y-auto scrollbar-thin"
        :class="isDark ? 'bg-slate-800 border border-slate-700' : 'bg-white border border-slate-200'">
        <button
          v-for="(item, i) in filtered" :key="item.term"
          @mousedown.prevent="selectSuggestion(item)"
          class="w-full text-left px-3 py-2 text-body-sm flex items-center gap-2.5 transition-colors"
          :class="[
            i === activeIndex
              ? (isDark ? 'bg-blue-500/15 text-blue-300' : 'bg-blue-50 text-blue-700')
              : (isDark ? 'text-slate-300 hover:bg-slate-700/60' : 'text-slate-700 hover:bg-slate-50')
          ]">
          <span class="text-base flex-shrink-0">{{ item.icon }}</span>
          <div class="flex-1 min-w-0">
            <div class="font-medium">{{ item.term }}</div>
            <div class="text-detail truncate" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ item.category }}</div>
          </div>
          <span class="text-micro px-1.5 py-0.5 rounded-pill flex-shrink-0"
            :style="{ background: item.color + '15', color: item.color }">
            {{ item.specialty }}
          </span>
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  query: { type: String, default: '' },
  visible: { type: Boolean, default: false },
})

const emit = defineEmits(['select'])
const containerRef = ref(null)
const activeIndex = ref(0)
const showSuggestions = computed(() => props.visible && props.query.length >= 2 && filtered.value.length > 0)

// Common symptoms database
const symptoms = [
  // Head & Neuro
  { term: 'Headache', category: 'Head & Brain', specialty: 'Neurology', icon: '🧠', color: '#a855f7' },
  { term: 'Migraine', category: 'Head & Brain', specialty: 'Neurology', icon: '🧠', color: '#a855f7' },
  { term: 'Dizziness', category: 'Head & Brain', specialty: 'Neurology', icon: '🧠', color: '#a855f7' },
  { term: 'Memory problems', category: 'Head & Brain', specialty: 'Neurology', icon: '🧠', color: '#a855f7' },
  { term: 'Numbness or tingling', category: 'Nerves', specialty: 'Neurology', icon: '🧠', color: '#a855f7' },

  // Chest & Cardio
  { term: 'Chest pain', category: 'Heart & Chest', specialty: 'Cardiology', icon: '❤️', color: '#ef4444' },
  { term: 'Heart palpitations', category: 'Heart & Chest', specialty: 'Cardiology', icon: '❤️', color: '#ef4444' },
  { term: 'Shortness of breath', category: 'Lungs', specialty: 'Pulmonology', icon: '🫁', color: '#06b6d4' },
  { term: 'Persistent cough', category: 'Lungs', specialty: 'Pulmonology', icon: '🫁', color: '#06b6d4' },
  { term: 'Wheezing', category: 'Lungs', specialty: 'Pulmonology', icon: '🫁', color: '#06b6d4' },

  // Skin
  { term: 'Skin rash', category: 'Skin', specialty: 'Dermatology', icon: '🌸', color: '#f43f5e' },
  { term: 'Itchy skin', category: 'Skin', specialty: 'Dermatology', icon: '🌸', color: '#f43f5e' },
  { term: 'Acne', category: 'Skin', specialty: 'Dermatology', icon: '🌸', color: '#f43f5e' },
  { term: 'Skin discoloration', category: 'Skin', specialty: 'Dermatology', icon: '🌸', color: '#f43f5e' },
  { term: 'Hair loss', category: 'Skin & Hair', specialty: 'Dermatology', icon: '🌸', color: '#f43f5e' },

  // Digestive
  { term: 'Stomach pain', category: 'Digestive', specialty: 'GI', icon: '🫁', color: '#f59e0b' },
  { term: 'Nausea', category: 'Digestive', specialty: 'GI', icon: '🫁', color: '#f59e0b' },
  { term: 'Bloating', category: 'Digestive', specialty: 'GI', icon: '🫁', color: '#f59e0b' },
  { term: 'Acid reflux', category: 'Digestive', specialty: 'GI', icon: '🫁', color: '#f59e0b' },
  { term: 'Diarrhea', category: 'Digestive', specialty: 'GI', icon: '🫁', color: '#f59e0b' },
  { term: 'Constipation', category: 'Digestive', specialty: 'GI', icon: '🫁', color: '#f59e0b' },

  // Mental Health
  { term: 'Anxiety', category: 'Mental Health', specialty: 'Psychiatry', icon: '🧘', color: '#6366f1' },
  { term: 'Depression', category: 'Mental Health', specialty: 'Psychiatry', icon: '🧘', color: '#6366f1' },
  { term: 'Insomnia', category: 'Sleep', specialty: 'Psychiatry', icon: '🧘', color: '#6366f1' },
  { term: 'Panic attacks', category: 'Mental Health', specialty: 'Psychiatry', icon: '🧘', color: '#6366f1' },
  { term: 'Stress', category: 'Mental Health', specialty: 'Psychiatry', icon: '🧘', color: '#6366f1' },

  // Musculoskeletal
  { term: 'Back pain', category: 'Muscles & Joints', specialty: 'Orthopedics', icon: '🦴', color: '#64748b' },
  { term: 'Joint pain', category: 'Muscles & Joints', specialty: 'Orthopedics', icon: '🦴', color: '#64748b' },
  { term: 'Knee pain', category: 'Muscles & Joints', specialty: 'Orthopedics', icon: '🦴', color: '#64748b' },
  { term: 'Shoulder pain', category: 'Muscles & Joints', specialty: 'Orthopedics', icon: '🦴', color: '#64748b' },
  { term: 'Muscle cramps', category: 'Muscles', specialty: 'Orthopedics', icon: '🦴', color: '#64748b' },

  // General
  { term: 'Fatigue', category: 'General', specialty: 'Internal Med', icon: '🩺', color: '#3b82f6' },
  { term: 'Fever', category: 'General', specialty: 'Internal Med', icon: '🩺', color: '#3b82f6' },
  { term: 'Weight loss (unexplained)', category: 'General', specialty: 'Internal Med', icon: '🩺', color: '#3b82f6' },
  { term: 'Swollen lymph nodes', category: 'General', specialty: 'Internal Med', icon: '🩺', color: '#3b82f6' },

  // Nutrition
  { term: 'Poor appetite', category: 'Nutrition', specialty: 'Nutrition', icon: '🥗', color: '#84cc16' },
  { term: 'Food intolerance', category: 'Nutrition', specialty: 'Nutrition', icon: '🥗', color: '#84cc16' },
  { term: 'Weight gain', category: 'Nutrition', specialty: 'Nutrition', icon: '🥗', color: '#84cc16' },

  // Endocrine
  { term: 'Excessive thirst', category: 'Hormonal', specialty: 'Endocrine', icon: '⚗️', color: '#14b8a6' },
  { term: 'Thyroid issues', category: 'Hormonal', specialty: 'Endocrine', icon: '⚗️', color: '#14b8a6' },
  { term: 'Hot flashes', category: 'Hormonal', specialty: 'Endocrine', icon: '⚗️', color: '#14b8a6' },

  // Eye / ENT
  { term: 'Sore throat', category: 'Throat', specialty: 'General', icon: '🩺', color: '#3b82f6' },
  { term: 'Ear pain', category: 'Ear', specialty: 'General', icon: '🩺', color: '#3b82f6' },
  { term: 'Blurred vision', category: 'Eyes', specialty: 'General', icon: '🩺', color: '#3b82f6' },
]

const filtered = computed(() => {
  if (!props.query || props.query.length < 2) return []
  const q = props.query.toLowerCase()
  return symptoms
    .filter(s => s.term.toLowerCase().includes(q) || s.category.toLowerCase().includes(q))
    .slice(0, 8)
})

watch(() => props.query, () => { activeIndex.value = 0 })

function selectSuggestion(item) {
  emit('select', item.term)
}

// Keyboard navigation (handled by parent via exposed methods)
function moveUp() {
  if (activeIndex.value > 0) activeIndex.value--
}
function moveDown() {
  if (activeIndex.value < filtered.value.length - 1) activeIndex.value++
}
function selectActive() {
  if (filtered.value[activeIndex.value]) {
    selectSuggestion(filtered.value[activeIndex.value])
  }
}

defineExpose({ moveUp, moveDown, selectActive, hasSuggestions: showSuggestions })
</script>

<style scoped>
.fade-enter-active { transition: opacity 0.15s ease; }
.fade-enter-from { opacity: 0; }
.fade-leave-active { transition: opacity 0.1s ease; }
.fade-leave-to { opacity: 0; }
</style>
