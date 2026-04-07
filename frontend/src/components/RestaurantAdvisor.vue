<template>
  <div class="restaurant-advisor">
    <!-- Cuisine Filter -->
    <div class="flex flex-wrap gap-2 mb-4">
      <button v-for="c in cuisineFilters" :key="c" @click="activeCuisine = c"
        class="px-3 py-1.5 rounded-full text-xs font-semibold transition-all duration-200"
        :class="activeCuisine === c
          ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30'
          : isDark ? 'bg-slate-700/60 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
        {{ c }}
      </button>
    </div>

    <!-- Restaurant Grid -->
    <div v-if="!selectedRestaurant" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 mb-4">
      <button v-for="r in filteredRestaurants" :key="r.key" @click="selectRestaurant(r.key)"
        class="flex flex-col items-center gap-1.5 p-3 rounded-xl border transition-all duration-200 hover:scale-105"
        :class="isDark
          ? 'bg-slate-800/60 border-slate-700/50 hover:border-emerald-500/50 hover:shadow-lg hover:shadow-emerald-500/10'
          : 'bg-white border-slate-200 hover:border-emerald-400 hover:shadow-md'">
        <span class="text-2xl">{{ r.emoji }}</span>
        <span class="text-xs font-bold text-center leading-tight" :class="isDark ? 'text-white' : 'text-slate-800'">{{ r.name }}</span>
        <span class="text-[10px] font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ r.cuisine }}</span>
      </button>
    </div>

    <!-- Menu Browser -->
    <div v-if="selectedRestaurant">
      <!-- Restaurant Header -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center gap-3">
          <button @click="selectedRestaurant = null; compareItems = []"
            class="w-8 h-8 rounded-lg flex items-center justify-center transition-colors"
            :class="isDark ? 'bg-slate-700 hover:bg-slate-600 text-slate-300' : 'bg-slate-100 hover:bg-slate-200 text-slate-600'">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          </button>
          <span class="text-xl">{{ currentRestaurant.emoji }}</span>
          <h3 class="text-lg font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">{{ currentRestaurant.name }}</h3>
        </div>
        <button @click="showCompare = !showCompare" :disabled="compareItems.length < 2" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition-all" :class="compareItems.length >= 2 ? 'bg-violet-500 text-white shadow-lg shadow-violet-500/30 hover:bg-violet-600' : isDark ? 'bg-slate-700/40 text-slate-500 cursor-not-allowed' : 'bg-slate-100 text-slate-400 cursor-not-allowed'">
          Compare ({{ compareItems.length }}/3)</button>
      </div>

      <!-- Category Tabs -->
      <div class="flex gap-1.5 mb-4 overflow-x-auto pb-1">
        <button v-for="cat in menuCategories" :key="cat.key" @click="activeCategory = cat.key"
          class="px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all"
          :class="activeCategory === cat.key
            ? 'bg-emerald-500 text-white shadow-md'
            : isDark ? 'bg-slate-700/50 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
          {{ cat.label }}
        </button>
      </div>

      <!-- Compare Panel -->
      <div v-if="showCompare && compareItems.length >= 2" class="mb-4 rounded-xl border overflow-hidden" :class="isDark ? 'bg-slate-800/80 border-slate-700/50' : 'bg-white border-slate-200'">
        <div class="px-4 py-3 border-b" :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
          <h4 class="text-sm font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Side-by-Side Comparison</h4></div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead>
              <tr :class="isDark ? 'bg-slate-700/30' : 'bg-slate-50'">
                <th class="text-left px-3 py-2 font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Metric</th>
                <th v-for="item in compareItems" :key="item.name" class="text-center px-3 py-2 font-bold" :class="isDark ? 'text-white' : 'text-slate-800'">{{ item.name }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="metric in compareMetrics" :key="metric.key" class="border-t" :class="isDark ? 'border-slate-700/30' : 'border-slate-100'">
                <td class="px-3 py-2 font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ metric.label }}</td>
                <td v-for="item in compareItems" :key="item.name + metric.key" class="text-center px-3 py-2 font-semibold"
                  :class="isBestInMetric(item, metric.key) ? 'text-emerald-400' : isDark ? 'text-slate-300' : 'text-slate-700'">
                  {{ item[metric.key] }}{{ metric.unit }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="px-4 py-3 border-t" :class="isDark ? 'border-slate-700/50 bg-emerald-500/5' : 'border-slate-200 bg-emerald-50'">
          <p class="text-xs font-medium" :class="isDark ? 'text-emerald-400' : 'text-emerald-700'">
            <span class="font-bold">AI Recommendation:</span> {{ compareRecommendation }}
          </p>
        </div>
      </div>

      <!-- Menu Items -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div v-for="item in activeMenuItems" :key="item.name" class="rounded-xl border p-3 transition-all duration-200 hover:scale-[1.02]" :class="[isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm', isInCompare(item) ? (isDark ? 'ring-2 ring-violet-500/60' : 'ring-2 ring-violet-400') : '']">
          <div class="flex items-start justify-between mb-2">
            <h4 class="text-sm font-bold leading-tight" :class="isDark ? 'text-white' : 'text-slate-900'">{{ item.name }}</h4>
            <span class="text-lg font-bold ml-2 whitespace-nowrap" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">{{ item.cal }}<span class="text-[10px] font-normal ml-0.5">cal</span></span>
          </div>

          <!-- Macros Row -->
          <div class="flex gap-2 mb-2.5 flex-wrap">
            <span class="text-[10px] font-semibold px-1.5 py-0.5 rounded" :class="isDark ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-600'">P {{ item.protein }}g</span>
            <span class="text-[10px] font-semibold px-1.5 py-0.5 rounded" :class="isDark ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-600'">C {{ item.carbs }}g</span>
            <span class="text-[10px] font-semibold px-1.5 py-0.5 rounded" :class="isDark ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-600'">F {{ item.fat }}g</span>
            <span class="text-[10px] font-semibold px-1.5 py-0.5 rounded" :class="isDark ? 'bg-purple-500/15 text-purple-400' : 'bg-purple-50 text-purple-600'">Na {{ item.sodium }}mg</span>
          </div>

          <!-- AI Labels -->
          <div class="flex flex-wrap gap-1 mb-3">
            <span v-for="label in getItemLabels(item)" :key="label.text"
              class="text-[10px] font-semibold px-1.5 py-0.5 rounded-full"
              :class="label.class">
              {{ label.text }}
            </span>
          </div>

          <!-- Actions -->
          <div class="flex items-center gap-2">
            <button @click="addToToday(item)" class="flex-1 text-[10px] font-semibold py-1.5 rounded-lg transition-colors" :class="isDark ? 'bg-emerald-500/15 text-emerald-400 hover:bg-emerald-500/25' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100'">Add to Today</button>
            <button @click="toggleFavorite(item)" class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors" :class="isFavorite(item) ? 'bg-rose-500/20 text-rose-400' : isDark ? 'bg-slate-700/50 text-slate-400 hover:text-rose-400' : 'bg-slate-100 text-slate-400 hover:text-rose-500'">
              <svg class="w-3.5 h-3.5" :fill="isFavorite(item) ? 'currentColor' : 'none'" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg></button>
            <button @click="toggleCompare(item)" :disabled="!isInCompare(item) && compareItems.length >= 3" class="w-7 h-7 rounded-lg flex items-center justify-center transition-colors text-[10px] font-bold" :class="isInCompare(item) ? 'bg-violet-500/20 text-violet-400' : compareItems.length >= 3 ? (isDark ? 'bg-slate-700/30 text-slate-600 cursor-not-allowed' : 'bg-slate-50 text-slate-300 cursor-not-allowed') : (isDark ? 'bg-slate-700/50 text-slate-400 hover:text-violet-400' : 'bg-slate-100 text-slate-400 hover:text-violet-500')">VS</button>
          </div>
        </div>
      </div>

      <p v-if="activeMenuItems.length === 0" class="text-center py-8 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
        No items in this category.
      </p>
    </div>

    <!-- Today's Selections -->
    <div v-if="todayItems.length > 0" class="mt-4 rounded-xl border p-3" :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200'">
      <div class="flex items-center justify-between mb-2">
        <h4 class="text-xs font-bold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">Today's Selections</h4>
        <span class="text-xs font-bold" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">{{ todayCalories }} cal total</span>
      </div>
      <div class="flex flex-wrap gap-1.5">
        <span v-for="(item, i) in todayItems" :key="i" class="inline-flex items-center gap-1 text-[10px] font-semibold px-2 py-1 rounded-full" :class="isDark ? 'bg-slate-700/50 text-slate-300' : 'bg-slate-100 text-slate-600'">
          {{ item.name }} ({{ item.cal }}) <button @click="todayItems.splice(i, 1)" class="ml-0.5 hover:text-red-400">&times;</button>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTheme } from '../composables/useTheme'

const { isDark } = useTheme()

const props = defineProps({
  dietGoal: { type: String, default: '' },
  restrictions: { type: Array, default: () => [] },
  allergies: { type: Array, default: () => [] },
  medications: { type: Array, default: () => [] }
})

const activeCuisine = ref('All')
const selectedRestaurant = ref(null)
const activeCategory = ref('mains')
const compareItems = ref([])
const showCompare = ref(false)
const todayItems = ref([])
const favorites = ref([])

const cuisineFilters = ['All', 'Burgers', 'Pizza', 'Mexican', 'Chicken', 'Coffee', 'Sandwich', 'Asian']

const RESTAURANTS = {
  mcdonalds: {
    name: "McDonald's", emoji: '🍔', cuisine: 'Burgers',
    menu: {
      breakfast: [
        { name: 'Egg McMuffin', cal: 300, protein: 17, carbs: 26, fat: 13, sodium: 750, sugar: 3 },
        { name: 'Hotcakes', cal: 580, protein: 9, carbs: 101, fat: 16, sodium: 600, sugar: 45 }
      ],
      mains: [
        { name: 'Big Mac', cal: 550, protein: 25, carbs: 45, fat: 30, sodium: 1010, sugar: 9 },
        { name: 'McChicken', cal: 400, protein: 14, carbs: 39, fat: 21, sodium: 560, sugar: 5 },
        { name: 'Quarter Pounder w/ Cheese', cal: 520, protein: 30, carbs: 42, fat: 26, sodium: 1110, sugar: 10 },
        { name: '6pc Chicken McNuggets', cal: 250, protein: 15, carbs: 15, fat: 15, sodium: 500, sugar: 0 }
      ],
      sides: [
        { name: 'Medium Fries', cal: 320, protein: 5, carbs: 43, fat: 15, sodium: 260, sugar: 0 },
        { name: 'Side Salad', cal: 15, protein: 1, carbs: 3, fat: 0, sodium: 10, sugar: 2 }
      ],
      drinks: [
        { name: 'Medium Coke', cal: 210, protein: 0, carbs: 58, fat: 0, sodium: 5, sugar: 58 },
        { name: 'Medium Iced Coffee', cal: 140, protein: 2, carbs: 22, fat: 5, sodium: 55, sugar: 21 }
      ],
      desserts: [
        { name: 'McFlurry Oreo', cal: 510, protein: 12, carbs: 80, fat: 17, sodium: 280, sugar: 63 }
      ]
    }
  },
  starbucks: {
    name: 'Starbucks', emoji: '☕', cuisine: 'Coffee',
    menu: {
      breakfast: [
        { name: 'Spinach Feta Wrap', cal: 290, protein: 20, carbs: 34, fat: 10, sodium: 840, sugar: 4 },
        { name: 'Egg Bites (Bacon Gruyere)', cal: 310, protein: 19, carbs: 9, fat: 22, sodium: 600, sugar: 2 }
      ],
      drinks: [
        { name: 'Caffe Latte (Grande)', cal: 190, protein: 13, carbs: 19, fat: 7, sodium: 170, sugar: 17 },
        { name: 'Caramel Frappuccino', cal: 370, protein: 5, carbs: 54, fat: 15, sodium: 250, sugar: 50 },
        { name: 'Cold Brew (Grande)', cal: 5, protein: 0, carbs: 0, fat: 0, sodium: 10, sugar: 0 },
        { name: 'Iced Americano', cal: 10, protein: 1, carbs: 2, fat: 0, sodium: 10, sugar: 0 }
      ],
      desserts: [
        { name: 'Blueberry Muffin', cal: 360, protein: 6, carbs: 55, fat: 13, sodium: 310, sugar: 29 }
      ]
    }
  },
  subway: {
    name: 'Subway', emoji: '🥖', cuisine: 'Sandwich',
    menu: {
      mains: [
        { name: 'Turkey Breast 6"', cal: 280, protein: 18, carbs: 40, fat: 4, sodium: 780, sugar: 6 },
        { name: 'Veggie Delite 6"', cal: 200, protein: 8, carbs: 39, fat: 2, sodium: 310, sugar: 5 },
        { name: 'Chicken Teriyaki 6"', cal: 330, protein: 26, carbs: 44, fat: 5, sodium: 850, sugar: 10 },
        { name: 'Italian BMT 6"', cal: 370, protein: 17, carbs: 41, fat: 14, sodium: 1190, sugar: 6 }
      ],
      sides: [
        { name: 'Baked Chips', cal: 130, protein: 2, carbs: 19, fat: 6, sodium: 150, sugar: 2 }
      ]
    }
  },
  kfc: {
    name: 'KFC', emoji: '🍗', cuisine: 'Chicken',
    menu: {
      mains: [
        { name: 'Original Recipe Breast', cal: 390, protein: 39, carbs: 11, fat: 21, sodium: 1190, sugar: 0 },
        { name: 'Grilled Chicken Breast', cal: 210, protein: 38, carbs: 0, fat: 7, sodium: 710, sugar: 0 },
        { name: 'Chicken Sandwich', cal: 650, protein: 28, carbs: 49, fat: 38, sodium: 1440, sugar: 6 }
      ],
      sides: [
        { name: 'Corn on the Cob', cal: 70, protein: 2, carbs: 13, fat: 2, sodium: 0, sugar: 3 },
        { name: 'Green Beans', cal: 25, protein: 1, carbs: 4, fat: 0, sodium: 290, sugar: 1 }
      ]
    }
  },
  burgerking: {
    name: 'Burger King', emoji: '👑', cuisine: 'Burgers',
    menu: {
      mains: [
        { name: 'Whopper', cal: 660, protein: 28, carbs: 49, fat: 40, sodium: 980, sugar: 11 },
        { name: 'Impossible Whopper', cal: 630, protein: 25, carbs: 58, fat: 34, sodium: 1080, sugar: 12 },
        { name: 'Chicken Royale', cal: 530, protein: 26, carbs: 48, fat: 25, sodium: 890, sugar: 6 }
      ],
      sides: [
        { name: 'Medium Fries', cal: 380, protein: 4, carbs: 53, fat: 17, sodium: 320, sugar: 0 }
      ]
    }
  },
  dominos: {
    name: "Domino's", emoji: '🍕', cuisine: 'Pizza',
    menu: {
      mains: [
        { name: 'Pepperoni Pizza (2 slices)', cal: 420, protein: 18, carbs: 48, fat: 18, sodium: 980, sugar: 6 },
        { name: 'Margherita (2 slices)', cal: 370, protein: 16, carbs: 46, fat: 14, sodium: 720, sugar: 5 },
        { name: 'Thin Crust Cheese (2 slices)', cal: 290, protein: 14, carbs: 24, fat: 16, sodium: 560, sugar: 3 }
      ],
      sides: [
        { name: 'Caesar Salad', cal: 90, protein: 5, carbs: 5, fat: 6, sodium: 240, sugar: 2 }
      ]
    }
  },
  pizzahut: {
    name: 'Pizza Hut', emoji: '🍕', cuisine: 'Pizza',
    menu: {
      mains: [
        { name: 'Pepperoni Pan Pizza (2 slices)', cal: 480, protein: 18, carbs: 50, fat: 24, sodium: 1060, sugar: 6 },
        { name: 'Veggie Lover\'s (2 slices)', cal: 380, protein: 14, carbs: 48, fat: 16, sodium: 780, sugar: 7 },
        { name: 'Thin & Crispy Cheese (2 slices)', cal: 320, protein: 14, carbs: 28, fat: 18, sodium: 620, sugar: 4 }
      ],
      sides: [
        { name: 'Chicken Wings (4)', cal: 340, protein: 24, carbs: 4, fat: 26, sodium: 860, sugar: 1 }
      ]
    }
  },
  tacobell: {
    name: 'Taco Bell', emoji: '🌮', cuisine: 'Mexican',
    menu: {
      mains: [
        { name: 'Crunchy Taco', cal: 170, protein: 8, carbs: 13, fat: 10, sodium: 310, sugar: 1 },
        { name: 'Chicken Quesadilla', cal: 510, protein: 27, carbs: 37, fat: 27, sodium: 1180, sugar: 3 },
        { name: 'Power Bowl (Chicken)', cal: 470, protein: 26, carbs: 50, fat: 18, sodium: 1230, sugar: 3 },
        { name: 'Bean Burrito', cal: 380, protein: 14, carbs: 55, fat: 11, sodium: 1060, sugar: 3 }
      ],
      sides: [
        { name: 'Chips & Guac', cal: 230, protein: 3, carbs: 24, fat: 14, sodium: 350, sugar: 1 }
      ]
    }
  },
  chickfila: {
    name: 'Chick-fil-A', emoji: '🐔', cuisine: 'Chicken',
    menu: {
      mains: [
        { name: 'Original Chicken Sandwich', cal: 440, protein: 28, carbs: 40, fat: 18, sodium: 1400, sugar: 5 },
        { name: 'Grilled Chicken Sandwich', cal: 320, protein: 28, carbs: 36, fat: 6, sodium: 800, sugar: 8 },
        { name: 'Grilled Nuggets (8ct)', cal: 130, protein: 25, carbs: 2, fat: 3, sodium: 440, sugar: 1 },
        { name: 'Cobb Salad', cal: 510, protein: 40, carbs: 28, fat: 27, sodium: 1310, sugar: 6 }
      ],
      sides: [
        { name: 'Waffle Fries (Med)', cal: 420, protein: 5, carbs: 45, fat: 24, sodium: 240, sugar: 0 },
        { name: 'Fruit Cup', cal: 50, protein: 0, carbs: 13, fat: 0, sodium: 0, sugar: 10 }
      ]
    }
  },
  wendys: {
    name: "Wendy's", emoji: '🟥', cuisine: 'Burgers',
    menu: {
      mains: [
        { name: 'Dave\'s Single', cal: 590, protein: 30, carbs: 39, fat: 34, sodium: 1170, sugar: 8 },
        { name: 'Grilled Chicken Sandwich', cal: 370, protein: 35, carbs: 36, fat: 10, sodium: 820, sugar: 8 },
        { name: 'Jr. Cheeseburger', cal: 290, protein: 15, carbs: 26, fat: 14, sodium: 620, sugar: 5 }
      ],
      sides: [
        { name: 'Chili (Small)', cal: 170, protein: 15, carbs: 16, fat: 5, sodium: 780, sugar: 5 },
        { name: 'Baked Potato (plain)', cal: 270, protein: 7, carbs: 61, fat: 0, sodium: 25, sugar: 3 }
      ]
    }
  },
  dunkin: {
    name: "Dunkin'", emoji: '🍩', cuisine: 'Coffee',
    menu: {
      breakfast: [
        { name: 'Egg & Cheese Wake-Up Wrap', cal: 180, protein: 10, carbs: 14, fat: 10, sodium: 480, sugar: 1 },
        { name: 'Avocado Toast', cal: 250, protein: 8, carbs: 32, fat: 11, sodium: 470, sugar: 4 }
      ],
      mains: [
        { name: 'Glazed Donut', cal: 240, protein: 3, carbs: 31, fat: 11, sodium: 330, sugar: 12 }
      ],
      drinks: [
        { name: 'Med Iced Coffee', cal: 120, protein: 2, carbs: 20, fat: 4, sodium: 60, sugar: 18 },
        { name: 'Cold Brew (Med)', cal: 5, protein: 0, carbs: 1, fat: 0, sodium: 10, sugar: 0 }
      ]
    }
  },
  chipotle: {
    name: 'Chipotle', emoji: '🌯', cuisine: 'Mexican',
    menu: {
      mains: [
        { name: 'Chicken Burrito', cal: 1005, protein: 54, carbs: 105, fat: 37, sodium: 2070, sugar: 6 },
        { name: 'Chicken Bowl', cal: 740, protein: 52, carbs: 59, fat: 30, sodium: 1790, sugar: 4 },
        { name: 'Veggie Bowl', cal: 630, protein: 20, carbs: 72, fat: 28, sodium: 1340, sugar: 6 }
      ],
      sides: [
        { name: 'Chips & Guacamole', cal: 770, protein: 10, carbs: 67, fat: 52, sodium: 550, sugar: 3 }
      ]
    }
  },
  panera: {
    name: 'Panera Bread', emoji: '🥐', cuisine: 'Sandwich',
    menu: {
      mains: [
        { name: 'Turkey Avocado BLT', cal: 550, protein: 32, carbs: 51, fat: 24, sodium: 1260, sugar: 7 },
        { name: 'Mediterranean Veggie Sandwich', cal: 520, protein: 16, carbs: 64, fat: 22, sodium: 1290, sugar: 8 },
        { name: 'Broccoli Cheddar Soup (Bowl)', cal: 360, protein: 16, carbs: 30, fat: 21, sodium: 1310, sugar: 6 },
        { name: 'Asian Sesame Salad', cal: 430, protein: 31, carbs: 32, fat: 20, sodium: 780, sugar: 12 }
      ],
      drinks: [
        { name: 'Iced Green Tea', cal: 70, protein: 0, carbs: 18, fat: 0, sodium: 15, sugar: 17 }
      ]
    }
  },
  nandos: {
    name: "Nando's", emoji: '🔥', cuisine: 'Chicken',
    menu: {
      mains: [
        { name: '1/4 Chicken Breast', cal: 265, protein: 40, carbs: 1, fat: 11, sodium: 620, sugar: 0 },
        { name: 'Chicken Burger', cal: 490, protein: 34, carbs: 38, fat: 20, sodium: 880, sugar: 5 },
        { name: 'Chicken Caesar Salad', cal: 340, protein: 38, carbs: 10, fat: 16, sodium: 720, sugar: 3 }
      ],
      sides: [
        { name: 'Peri Chips', cal: 340, protein: 4, carbs: 44, fat: 16, sodium: 280, sugar: 0 },
        { name: 'Corn on the Cob', cal: 130, protein: 4, carbs: 20, fat: 5, sodium: 10, sugar: 4 }
      ]
    }
  },
  popeyes: {
    name: 'Popeyes', emoji: '🍗', cuisine: 'Chicken',
    menu: {
      mains: [
        { name: 'Chicken Sandwich', cal: 700, protein: 28, carbs: 50, fat: 42, sodium: 1440, sugar: 8 },
        { name: 'Blackened Chicken Tenders (3)', cal: 170, protein: 26, carbs: 2, fat: 7, sodium: 640, sugar: 0 },
        { name: 'Mild Chicken Breast', cal: 360, protein: 32, carbs: 14, fat: 20, sodium: 1230, sugar: 0 }
      ],
      sides: [
        { name: 'Red Beans & Rice', cal: 230, protein: 9, carbs: 30, fat: 8, sodium: 680, sugar: 1 },
        { name: 'Cajun Fries (Reg)', cal: 260, protein: 3, carbs: 34, fat: 14, sodium: 490, sugar: 0 }
      ]
    }
  },
  shakeshack: {
    name: 'Shake Shack', emoji: '🍔', cuisine: 'Burgers',
    menu: {
      mains: [
        { name: 'ShackBurger', cal: 530, protein: 28, carbs: 27, fat: 34, sodium: 1140, sugar: 7 },
        { name: 'Chicken Shack', cal: 580, protein: 30, carbs: 48, fat: 29, sodium: 1350, sugar: 8 },
        { name: 'Shroom Burger', cal: 490, protein: 18, carbs: 32, fat: 32, sodium: 860, sugar: 7 }
      ],
      sides: [
        { name: 'Crinkle Cut Fries', cal: 470, protein: 5, carbs: 52, fat: 27, sodium: 900, sugar: 0 }
      ],
      drinks: [
        { name: 'Chocolate Shake', cal: 750, protein: 16, carbs: 95, fat: 34, sodium: 350, sugar: 77 }
      ]
    }
  },
  fiveguys: {
    name: 'Five Guys', emoji: '🍟', cuisine: 'Burgers',
    menu: {
      mains: [
        { name: 'Cheeseburger', cal: 840, protein: 47, carbs: 40, fat: 55, sodium: 1050, sugar: 8 },
        { name: 'Little Cheeseburger', cal: 550, protein: 27, carbs: 39, fat: 32, sodium: 690, sugar: 8 },
        { name: 'Bacon Burger', cal: 920, protein: 51, carbs: 39, fat: 62, sodium: 1310, sugar: 8 }
      ],
      sides: [
        { name: 'Regular Fries', cal: 530, protein: 6, carbs: 63, fat: 29, sodium: 100, sugar: 0 }
      ]
    }
  },
  timhortons: {
    name: 'Tim Hortons', emoji: '🍁', cuisine: 'Coffee',
    menu: {
      mains: [
        { name: 'Turkey Bacon Club', cal: 440, protein: 28, carbs: 40, fat: 18, sodium: 1160, sugar: 5 },
        { name: 'Chicken Wrap', cal: 350, protein: 22, carbs: 36, fat: 13, sodium: 780, sugar: 3 }
      ],
      drinks: [
        { name: 'Double Double (Med)', cal: 230, protein: 4, carbs: 24, fat: 14, sodium: 50, sugar: 24 },
        { name: 'Steeped Tea', cal: 0, protein: 0, carbs: 0, fat: 0, sodium: 0, sugar: 0 }
      ]
    }
  },
  costa: {
    name: 'Costa Coffee', emoji: '☕', cuisine: 'Coffee',
    menu: {
      mains: [
        { name: 'Chicken & Bacon Panini', cal: 480, protein: 30, carbs: 42, fat: 20, sodium: 1020, sugar: 4 }
      ],
      drinks: [
        { name: 'Flat White (Med)', cal: 130, protein: 8, carbs: 12, fat: 6, sodium: 100, sugar: 11 },
        { name: 'Americano', cal: 8, protein: 0, carbs: 1, fat: 0, sodium: 5, sugar: 0 }
      ]
    }
  },
  pandaexpress: {
    name: 'Panda Express', emoji: '🐼', cuisine: 'Asian',
    menu: {
      mains: [
        { name: 'Orange Chicken', cal: 490, protein: 25, carbs: 51, fat: 21, sodium: 820, sugar: 19 },
        { name: 'Grilled Teriyaki Chicken', cal: 300, protein: 36, carbs: 14, fat: 13, sodium: 530, sugar: 8 },
        { name: 'Broccoli Beef', cal: 150, protein: 9, carbs: 13, fat: 7, sodium: 520, sugar: 7 },
        { name: 'Kung Pao Chicken', cal: 290, protein: 16, carbs: 14, fat: 19, sodium: 730, sugar: 5 }
      ],
      sides: [
        { name: 'Fried Rice', cal: 520, protein: 12, carbs: 85, fat: 16, sodium: 820, sugar: 3 },
        { name: 'Super Greens', cal: 90, protein: 6, carbs: 10, fat: 3, sodium: 260, sugar: 3 }
      ]
    }
  }
}

const restaurantList = computed(() =>
  Object.entries(RESTAURANTS).map(([key, r]) => ({ key, ...r }))
)

const filteredRestaurants = computed(() =>
  activeCuisine.value === 'All'
    ? restaurantList.value
    : restaurantList.value.filter(r => r.cuisine === activeCuisine.value)
)

const currentRestaurant = computed(() => RESTAURANTS[selectedRestaurant.value] || {})

const menuCategories = computed(() => {
  if (!selectedRestaurant.value) return []
  const menu = currentRestaurant.value.menu || {}
  const labels = { breakfast: 'Breakfast', mains: 'Burgers/Mains', sides: 'Sides', drinks: 'Drinks', desserts: 'Desserts' }
  return Object.keys(menu).map(k => ({ key: k, label: labels[k] || k }))
})

const activeMenuItems = computed(() => {
  if (!selectedRestaurant.value) return []
  return (currentRestaurant.value.menu || {})[activeCategory.value] || []
})

const compareMetrics = [
  { key: 'cal', label: 'Calories', unit: '' },
  { key: 'protein', label: 'Protein', unit: 'g' },
  { key: 'carbs', label: 'Carbs', unit: 'g' },
  { key: 'fat', label: 'Fat', unit: 'g' },
  { key: 'sodium', label: 'Sodium', unit: 'mg' },
  { key: 'sugar', label: 'Sugar', unit: 'g' }
]

function selectRestaurant(key) {
  selectedRestaurant.value = key
  const menu = RESTAURANTS[key].menu
  activeCategory.value = Object.keys(menu)[0] || 'mains'
  compareItems.value = []
  showCompare.value = false
}

function getItemLabels(item) {
  const labels = []
  const goal = (props.dietGoal || '').toLowerCase()
  const isLowCal = item.cal <= 400
  const isHighProtein = item.protein >= 20
  const isHighSodium = item.sodium >= 1000
  const isHighSugar = item.sugar >= 25
  const isHeartFriendly = item.sodium < 600 && item.fat < 15

  if ((goal.includes('weight') || goal.includes('loss') || goal.includes('deficit')) && isLowCal) {
    labels.push({ text: '\u2705 Better Choice', class: isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700' })
  }
  if ((goal.includes('muscle') || goal.includes('protein') || goal.includes('gain')) && isHighProtein) {
    labels.push({ text: '\u2705 Better Choice', class: isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700' })
  }
  if (isHighProtein) {
    labels.push({ text: '\u26A1 Post-Workout', class: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-700' })
  }
  if (isHighSodium) {
    labels.push({ text: '\uD83E\uDDC2 High Sodium', class: isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-700' })
  }
  if (isHighSugar) {
    labels.push({ text: '\uD83C\uDF6C High Sugar', class: isDark.value ? 'bg-orange-500/15 text-orange-400' : 'bg-orange-50 text-orange-700' })
  }
  if (isHeartFriendly) {
    labels.push({ text: '\uD83D\uDC9A Heart-Friendly', class: isDark.value ? 'bg-green-500/15 text-green-400' : 'bg-green-50 text-green-700' })
  }
  if (props.allergies && props.allergies.length) {
    const n = item.name.toLowerCase()
    const allergenMap = { dairy: /cheese|cream|latte|mocha|frosty|mcflurry|frappuccino|shake/i, milk: /cheese|cream|latte|mocha|frosty|mcflurry|frappuccino|shake/i, gluten: /bread|bun|wrap|pizza|donut|muffin|croissant|bagel|biscuit|pancake|taco|burrito|sandwich|panini|roll|toastie|nugget|brownie|cookie|pie|timbits/i, wheat: /bread|bun|wrap|pizza|donut|muffin|croissant|bagel|biscuit|pancake|taco|burrito|sandwich|panini/i, shellfish: /shrimp/i, fish: /fish|filet-o/i, egg: /egg/i, eggs: /egg/i, soy: /soy|tofu|sofritas/i, peanuts: /peanut|nut|pecan/i, nuts: /peanut|nut|pecan/i }
    if (props.allergies.some(a => (allergenMap[a.toLowerCase()] || /^$/).test(n))) {
      labels.push({ text: '\u26A0\uFE0F Allergy Risk', class: isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-700' })
    }
  }
  return labels
}

function addToToday(item) {
  todayItems.value.push({ ...item })
}

function toggleFavorite(item) {
  const idx = favorites.value.findIndex(f => f.name === item.name)
  if (idx >= 0) favorites.value.splice(idx, 1)
  else favorites.value.push({ ...item })
}

function isFavorite(item) {
  return favorites.value.some(f => f.name === item.name)
}

function toggleCompare(item) {
  const idx = compareItems.value.findIndex(c => c.name === item.name)
  if (idx >= 0) {
    compareItems.value.splice(idx, 1)
  } else if (compareItems.value.length < 3) {
    compareItems.value.push(item)
  }
}

function isInCompare(item) {
  return compareItems.value.some(c => c.name === item.name)
}

function isBestInMetric(item, key) {
  if (compareItems.value.length < 2) return false
  if (key === 'protein') return item[key] === Math.max(...compareItems.value.map(c => c[key]))
  return item[key] === Math.min(...compareItems.value.map(c => c[key]))
}

const compareRecommendation = computed(() => {
  if (compareItems.value.length < 2) return ''
  const goal = (props.dietGoal || '').toLowerCase()
  const sorted = [...compareItems.value]
  if (goal.includes('weight') || goal.includes('loss')) {
    sorted.sort((a, b) => a.cal - b.cal)
    return `${sorted[0].name} is the best choice at only ${sorted[0].cal} calories, saving you ${sorted[sorted.length - 1].cal - sorted[0].cal} calories compared to ${sorted[sorted.length - 1].name}.`
  }
  if (goal.includes('muscle') || goal.includes('protein')) {
    sorted.sort((a, b) => b.protein - a.protein)
    return `${sorted[0].name} offers the most protein at ${sorted[0].protein}g, ideal for muscle building goals.`
  }
  sorted.sort((a, b) => (a.cal + a.sodium / 10) - (b.cal + b.sodium / 10))
  return `${sorted[0].name} is the most balanced option with ${sorted[0].cal} cal and ${sorted[0].sodium}mg sodium.`
})

const todayCalories = computed(() => todayItems.value.reduce((s, i) => s + i.cal, 0))
</script>
