<template>
  <div class="supermarket-advisor">
    <!-- Shopping Mission Selector -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 mb-4">
      <button v-for="m in missions" :key="m.key" @click="activeMission = activeMission === m.key ? null : m.key"
        class="flex flex-col items-center gap-1.5 p-3 rounded-xl border transition-all duration-200 hover:scale-105"
        :class="activeMission === m.key
          ? 'bg-emerald-500/15 border-emerald-500/50 shadow-lg shadow-emerald-500/10'
          : isDark ? 'bg-slate-800/60 border-slate-700/50 hover:border-emerald-500/30' : 'bg-white border-slate-200 hover:border-emerald-400'">
        <span class="text-xl">{{ m.emoji }}</span>
        <span class="text-[10px] font-bold text-center leading-tight" :class="isDark ? 'text-white' : 'text-slate-800'">{{ m.label }}</span>
      </button>
    </div>

    <!-- Category Tabs -->
    <div class="flex gap-1.5 mb-4 overflow-x-auto pb-1">
      <button v-for="cat in categoryTabs" :key="cat.key" @click="activeCategory = cat.key"
        class="px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-all"
        :class="activeCategory === cat.key
          ? 'bg-emerald-500 text-white shadow-md'
          : isDark ? 'bg-slate-700/50 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
        {{ cat.label }}
      </button>
    </div>

    <!-- Product Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
      <div v-for="product in filteredProducts" :key="product.name"
        class="rounded-xl border p-3 transition-all duration-200"
        :class="isDark ? 'bg-slate-800/60 border-slate-700/50' : 'bg-white border-slate-200 shadow-sm'">
        <div class="flex items-start justify-between mb-1.5">
          <h4 class="text-sm font-bold leading-tight" :class="isDark ? 'text-white' : 'text-slate-900'">{{ product.name }}</h4>
          <span class="text-xs font-bold ml-2 whitespace-nowrap" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">{{ product.calPerServing }}<span class="text-[10px] font-normal ml-0.5">cal</span></span>
        </div>

        <!-- Key nutrient -->
        <p class="text-[10px] font-semibold mb-1.5" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ product.keyNutrient }}</p>

        <!-- Stars -->
        <div class="flex items-center gap-1 mb-2">
          <span v-for="s in 5" :key="s" class="text-xs" :class="s <= product.stars ? 'text-amber-400' : (isDark ? 'text-slate-600' : 'text-slate-300')">&#9733;</span>
          <span class="text-[10px] font-medium ml-1" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ product.stars }}/5</span>
        </div>

        <!-- Tags -->
        <div class="flex flex-wrap gap-1 mb-2.5">
          <span v-for="tag in getProductTags(product)" :key="tag.text"
            class="text-[10px] font-semibold px-1.5 py-0.5 rounded-full" :class="tag.class">
            {{ tag.text }}
          </span>
        </div>

        <!-- Smart Alternatives -->
        <div v-if="product.warnings && product.warnings.length"
          class="mb-2.5 p-2 rounded-lg border"
          :class="isDark ? 'bg-slate-700/30 border-slate-600/30' : 'bg-slate-50 border-slate-200'">
          <p class="text-[10px] font-bold mb-1" :class="isDark ? 'text-amber-400' : 'text-amber-600'">Consider instead:</p>
          <div class="flex flex-col gap-1">
            <div v-for="alt in product.alternatives" :key="alt.name" class="flex items-center justify-between">
              <span class="text-[10px] font-medium" :class="isDark ? 'text-slate-300' : 'text-slate-700'">{{ alt.name }}</span>
              <span class="text-[10px] font-semibold" :class="isDark ? 'text-emerald-400' : 'text-emerald-600'">{{ alt.calPerServing }} cal &middot; {{ alt.keyNutrient }}</span>
            </div>
          </div>
        </div>

        <!-- Add to List -->
        <button @click="addToList(product)"
          class="w-full text-[10px] font-semibold py-1.5 rounded-lg transition-colors"
          :class="isInList(product)
            ? (isDark ? 'bg-emerald-500/25 text-emerald-400' : 'bg-emerald-100 text-emerald-700')
            : (isDark ? 'bg-emerald-500/15 text-emerald-400 hover:bg-emerald-500/25' : 'bg-emerald-50 text-emerald-600 hover:bg-emerald-100')">
          {{ isInList(product) ? '\u2713 Added' : 'Add to List' }}
        </button>
      </div>
    </div>

    <p v-if="filteredProducts.length === 0" class="text-center py-8 text-sm" :class="isDark ? 'text-slate-500' : 'text-slate-400'">
      No products in this category.
    </p>

    <!-- Shopping List -->
    <div v-if="shoppingList.length > 0"
      class="rounded-xl border overflow-hidden"
      :class="isDark ? 'bg-slate-800/80 border-slate-700/50' : 'bg-white border-slate-200'">
      <div class="px-4 py-3 border-b flex items-center justify-between"
        :class="isDark ? 'border-slate-700/50' : 'border-slate-200'">
        <h4 class="text-sm font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Shopping List ({{ shoppingList.length }} items)</h4>
        <div class="flex gap-2">
          <button @click="copyList"
            class="px-2.5 py-1 rounded-lg text-[10px] font-semibold transition-colors"
            :class="copied
              ? (isDark ? 'bg-emerald-500/20 text-emerald-400' : 'bg-emerald-100 text-emerald-600')
              : (isDark ? 'bg-slate-700/50 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200')">
            {{ copied ? 'Copied!' : 'Copy List' }}
          </button>
          <button @click="shareList"
            class="px-2.5 py-1 rounded-lg text-[10px] font-semibold transition-colors"
            :class="isDark ? 'bg-slate-700/50 text-slate-300 hover:bg-slate-600' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'">
            Share
          </button>
        </div>
      </div>

      <!-- Estimated weekly calories -->
      <div class="px-4 py-2 border-b" :class="isDark ? 'border-slate-700/30 bg-emerald-500/5' : 'border-slate-100 bg-emerald-50'">
        <span class="text-[10px] font-semibold" :class="isDark ? 'text-emerald-400' : 'text-emerald-700'">
          Est. weekly calories: {{ estimatedWeeklyCal.toLocaleString() }} cal (based on ~2 servings/item/day)
        </span>
      </div>

      <!-- Grouped Items -->
      <div v-for="group in groupedList" :key="group.category" class="border-b last:border-b-0"
        :class="isDark ? 'border-slate-700/30' : 'border-slate-100'">
        <div class="px-4 py-1.5" :class="isDark ? 'bg-slate-700/20' : 'bg-slate-50'">
          <span class="text-[10px] font-bold uppercase tracking-wider" :class="isDark ? 'text-slate-400' : 'text-slate-500'">{{ group.category }}</span>
        </div>
        <div v-for="item in group.items" :key="item.name"
          class="flex items-center gap-2 px-4 py-2 hover:bg-slate-700/10 transition-colors">
          <input type="checkbox" v-model="item.checked"
            class="w-3.5 h-3.5 rounded border-slate-400 text-emerald-500 focus:ring-emerald-500/30" />
          <span class="flex-1 text-xs font-medium" :class="[
            isDark ? 'text-slate-300' : 'text-slate-700',
            item.checked ? 'line-through opacity-50' : ''
          ]">{{ item.name }}</span>
          <span class="text-[10px] font-semibold" :class="isDark ? 'text-slate-500' : 'text-slate-400'">{{ item.calPerServing }} cal</span>
          <button @click="removeFromList(item)" class="text-slate-500 hover:text-red-400 text-xs">&times;</button>
        </div>
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

const activeMission = ref(null)
const activeCategory = ref('produce')
const shoppingList = ref([])
const copied = ref(false)

const missions = [
  { key: 'budget', label: 'Budget Healthy Week', emoji: '\uD83D\uDCB0' },
  { key: 'antiinflammatory', label: 'Anti-Inflammatory Shopping', emoji: '\uD83C\uDF3F' },
  { key: 'highprotein', label: 'High-Protein Muscle Gain', emoji: '\uD83D\uDCAA' },
  { key: 'heartsmart', label: 'Heart-Smart Pantry', emoji: '\u2764\uFE0F' },
  { key: 'diabetes', label: 'Diabetes-Friendly', emoji: '\uD83E\uDE78' },
  { key: 'mediterranean', label: 'Mediterranean Diet Staples', emoji: '\uD83E\uDED2' },
  { key: 'kidfriendly', label: 'Kid-Friendly Healthy', emoji: '\uD83D\uDC76' }
]

const categoryTabs = [
  { key: 'produce', label: 'Produce' },
  { key: 'proteins', label: 'Proteins' },
  { key: 'dairy', label: 'Dairy' },
  { key: 'grains', label: 'Grains' },
  { key: 'frozen', label: 'Frozen' },
  { key: 'snacks', label: 'Snacks' },
  { key: 'beverages', label: 'Beverages' },
  { key: 'pantry', label: 'Pantry' }
]

const PRODUCTS = {
  produce: [
    { name: 'Baby Spinach (5oz)', calPerServing: 7, keyNutrient: 'Iron 1.5mg, Vitamin K 145mcg', stars: 5, tags: ['good-staple'], missions: ['budget', 'antiinflammatory', 'heartsmart', 'mediterranean'] },
    { name: 'Blueberries (6oz)', calPerServing: 85, keyNutrient: 'Antioxidants, Vitamin C 14mg', stars: 5, tags: ['good-staple'], missions: ['antiinflammatory', 'diabetes', 'kidfriendly'] },
    { name: 'Avocados (each)', calPerServing: 240, keyNutrient: 'Healthy fats 22g, Potassium 485mg', stars: 5, tags: ['good-staple'], missions: ['heartsmart', 'mediterranean'] },
    { name: 'Sweet Potatoes (1 lb)', calPerServing: 112, keyNutrient: 'Fiber 4g, Vitamin A 438%', stars: 5, tags: ['good-staple'], missions: ['budget', 'diabetes', 'kidfriendly'] },
    { name: 'Bananas (bunch)', calPerServing: 105, keyNutrient: 'Potassium 422mg, Vitamin B6', stars: 4, tags: ['good-staple'], missions: ['budget', 'kidfriendly', 'highprotein'] },
    { name: 'Broccoli Crowns (1 lb)', calPerServing: 50, keyNutrient: 'Vitamin C 135%, Fiber 4g', stars: 5, tags: ['good-staple'], missions: ['budget', 'antiinflammatory', 'heartsmart'] },
    { name: 'Cherry Tomatoes (pint)', calPerServing: 27, keyNutrient: 'Lycopene, Vitamin C 21mg', stars: 4, tags: ['good-staple'], missions: ['mediterranean', 'heartsmart'] },
    { name: 'Pre-cut Fruit Mix', calPerServing: 60, keyNutrient: 'Mixed vitamins', stars: 3, tags: ['limit-frequency'], missions: ['kidfriendly'], warnings: ['Higher cost per nutrient'], alternatives: [{ name: 'Whole fruit (seasonal)', calPerServing: 70, keyNutrient: 'More fiber, less cost' }] }
  ],
  proteins: [
    { name: 'Chicken Breast (1 lb)', calPerServing: 165, keyNutrient: 'Protein 31g', stars: 5, tags: ['good-staple'], missions: ['highprotein', 'budget', 'diabetes'] },
    { name: 'Wild Salmon Fillets (6oz)', calPerServing: 280, keyNutrient: 'Protein 34g, Omega-3 2.2g', stars: 5, tags: ['good-staple'], missions: ['heartsmart', 'antiinflammatory', 'mediterranean'] },
    { name: 'Lean Ground Turkey (1 lb)', calPerServing: 170, keyNutrient: 'Protein 21g', stars: 4, tags: ['good-staple'], missions: ['highprotein', 'budget'] },
    { name: 'Eggs (dozen)', calPerServing: 72, keyNutrient: 'Protein 6g, Choline 147mg', stars: 5, tags: ['good-staple'], missions: ['budget', 'highprotein', 'kidfriendly'] },
    { name: 'Extra-Firm Tofu (14oz)', calPerServing: 90, keyNutrient: 'Protein 10g, Calcium 20%', stars: 4, tags: ['good-staple'], missions: ['antiinflammatory', 'heartsmart', 'mediterranean'] },
    { name: 'Deli Turkey Breast (8oz)', calPerServing: 60, keyNutrient: 'Protein 13g', stars: 3, tags: ['limit-frequency'], missions: ['highprotein'], warnings: ['High sodium ~500mg/serving'], alternatives: [{ name: 'Home-roasted turkey', calPerServing: 55, keyNutrient: 'Protein 13g, 60mg sodium' }, { name: 'Canned tuna in water', calPerServing: 70, keyNutrient: 'Protein 16g, 200mg sodium' }] },
    { name: 'Beef Hot Dogs (8ct)', calPerServing: 190, keyNutrient: 'Protein 7g', stars: 1, tags: ['ultra-processed'], missions: [], warnings: ['Ultra-processed, high sodium 500mg, nitrates'], alternatives: [{ name: 'Chicken sausage (uncured)', calPerServing: 120, keyNutrient: 'Protein 14g, less sodium' }, { name: 'Turkey burger patties', calPerServing: 170, keyNutrient: 'Protein 21g' }] },
    { name: 'Canned Sardines (in olive oil)', calPerServing: 130, keyNutrient: 'Omega-3 1.4g, Calcium 35%', stars: 5, tags: ['good-staple'], missions: ['mediterranean', 'antiinflammatory', 'heartsmart'] }
  ],
  dairy: [
    { name: 'Greek Yogurt Plain 0% (32oz)', calPerServing: 100, keyNutrient: 'Protein 17g, Calcium 15%', stars: 5, tags: ['good-staple'], missions: ['highprotein', 'budget', 'kidfriendly'] },
    { name: 'Whole Milk (gal)', calPerServing: 150, keyNutrient: 'Protein 8g, Calcium 30%', stars: 4, tags: ['good-staple'], missions: ['kidfriendly'] },
    { name: 'Cheddar Cheese Block (8oz)', calPerServing: 110, keyNutrient: 'Protein 7g, Calcium 20%', stars: 3, tags: ['limit-frequency'], missions: ['kidfriendly'], warnings: ['Saturated fat 6g/serving'], alternatives: [{ name: 'Part-skim mozzarella', calPerServing: 80, keyNutrient: 'Protein 7g, less sat fat' }] },
    { name: 'Cottage Cheese Low-fat (16oz)', calPerServing: 90, keyNutrient: 'Protein 14g, Calcium 10%', stars: 5, tags: ['good-staple'], missions: ['highprotein', 'diabetes'] },
    { name: 'Unsweetened Almond Milk (64oz)', calPerServing: 30, keyNutrient: 'Calcium 45%, Vitamin D 25%', stars: 4, tags: ['good-staple'], missions: ['heartsmart', 'antiinflammatory'] },
    { name: 'Flavored Yogurt Cups (4-pack)', calPerServing: 150, keyNutrient: 'Protein 5g', stars: 2, tags: ['ultra-processed'], missions: [], warnings: ['Added sugar ~19g per cup'], alternatives: [{ name: 'Plain Greek yogurt + berries', calPerServing: 120, keyNutrient: 'Protein 17g, 4g natural sugar' }, { name: 'Skyr (Icelandic yogurt)', calPerServing: 110, keyNutrient: 'Protein 15g, lower sugar' }] }
  ],
  grains: [
    { name: 'Rolled Oats (42oz)', calPerServing: 150, keyNutrient: 'Fiber 4g, Beta-glucan', stars: 5, tags: ['good-staple'], missions: ['budget', 'heartsmart', 'diabetes'] },
    { name: 'Brown Rice (2 lb)', calPerServing: 215, keyNutrient: 'Fiber 3.5g, Magnesium 21%', stars: 4, tags: ['good-staple'], missions: ['budget', 'highprotein'] },
    { name: 'Whole Wheat Bread', calPerServing: 80, keyNutrient: 'Fiber 3g', stars: 4, tags: ['good-staple'], missions: ['budget', 'kidfriendly'] },
    { name: 'Quinoa (1 lb)', calPerServing: 220, keyNutrient: 'Protein 8g, Complete amino acids', stars: 5, tags: ['good-staple'], missions: ['highprotein', 'mediterranean', 'antiinflammatory'] },
    { name: 'White Sandwich Bread', calPerServing: 70, keyNutrient: 'Minimal fiber', stars: 2, tags: ['limit-frequency'], missions: [], warnings: ['Refined flour, low fiber'], alternatives: [{ name: 'Whole wheat bread', calPerServing: 80, keyNutrient: 'Fiber 3g' }, { name: 'Ezekiel sprouted bread', calPerServing: 80, keyNutrient: 'Protein 5g, Fiber 3g' }] },
    { name: 'Whole Wheat Pasta (16oz)', calPerServing: 180, keyNutrient: 'Fiber 6g, Protein 7g', stars: 4, tags: ['good-staple'], missions: ['budget', 'mediterranean'] },
    { name: 'Instant Ramen (6-pack)', calPerServing: 380, keyNutrient: 'Sodium 1500mg', stars: 1, tags: ['ultra-processed'], missions: [], warnings: ['Very high sodium, low nutrition'], alternatives: [{ name: 'Rice noodles + broth', calPerServing: 200, keyNutrient: 'Lower sodium, customizable' }, { name: 'Soba noodles', calPerServing: 200, keyNutrient: 'Protein 8g, more minerals' }] }
  ],
  frozen: [
    { name: 'Frozen Broccoli Florets (12oz)', calPerServing: 30, keyNutrient: 'Vitamin C 90%, Fiber 3g', stars: 5, tags: ['good-staple'], missions: ['budget', 'antiinflammatory'] },
    { name: 'Frozen Wild Blueberries (12oz)', calPerServing: 70, keyNutrient: 'Antioxidants, Fiber 3g', stars: 5, tags: ['good-staple'], missions: ['antiinflammatory', 'heartsmart'] },
    { name: 'Frozen Salmon Fillets (1 lb)', calPerServing: 200, keyNutrient: 'Protein 22g, Omega-3 1.8g', stars: 5, tags: ['good-staple'], missions: ['heartsmart', 'highprotein', 'mediterranean'] },
    { name: 'Frozen Edamame (12oz)', calPerServing: 120, keyNutrient: 'Protein 11g, Fiber 5g', stars: 5, tags: ['good-staple'], missions: ['highprotein', 'antiinflammatory'] },
    { name: 'Frozen Chicken Nuggets', calPerServing: 270, keyNutrient: 'Protein 12g', stars: 2, tags: ['ultra-processed'], missions: ['kidfriendly'], warnings: ['Breaded, high sodium ~600mg'], alternatives: [{ name: 'Frozen grilled chicken strips', calPerServing: 130, keyNutrient: 'Protein 20g, 300mg sodium' }, { name: 'Homemade baked nuggets', calPerServing: 160, keyNutrient: 'Protein 18g, less sodium' }] },
    { name: 'Frozen Pizza (DiGiorno)', calPerServing: 310, keyNutrient: 'Sodium 810mg', stars: 1, tags: ['ultra-processed'], missions: [], warnings: ['High sodium, saturated fat, refined crust'], alternatives: [{ name: 'Cauliflower crust pizza', calPerServing: 190, keyNutrient: 'Less carbs, 420mg sodium' }, { name: 'Naan + tomato sauce + cheese', calPerServing: 220, keyNutrient: 'Less processed, customizable' }] }
  ],
  snacks: [
    { name: 'Mixed Nuts (unsalted, 1 lb)', calPerServing: 170, keyNutrient: 'Healthy fats 15g, Protein 6g', stars: 5, tags: ['good-staple'], missions: ['heartsmart', 'mediterranean', 'antiinflammatory'] },
    { name: 'Hummus (10oz)', calPerServing: 70, keyNutrient: 'Protein 2g, Fiber 1g', stars: 4, tags: ['good-staple'], missions: ['mediterranean', 'kidfriendly'] },
    { name: 'Dark Chocolate 85% (3oz bar)', calPerServing: 170, keyNutrient: 'Iron 19%, Magnesium 16%', stars: 4, tags: ['good-staple'], missions: ['antiinflammatory'] },
    { name: 'Rice Cakes (plain)', calPerServing: 35, keyNutrient: 'Low calorie base', stars: 3, tags: ['good-staple'], missions: ['budget', 'diabetes'] },
    { name: 'Potato Chips (Family Size)', calPerServing: 160, keyNutrient: 'Sodium 170mg', stars: 1, tags: ['ultra-processed'], missions: [], warnings: ['High fat, easy to over-consume'], alternatives: [{ name: 'Popcorn (air-popped)', calPerServing: 30, keyNutrient: 'Fiber 1g, whole grain' }, { name: 'Veggie straws', calPerServing: 130, keyNutrient: 'Lower fat' }] },
    { name: 'Protein Bars (box of 12)', calPerServing: 200, keyNutrient: 'Protein 20g', stars: 3, tags: ['limit-frequency'], missions: ['highprotein'], warnings: ['Some contain sugar alcohols'], alternatives: [{ name: 'Hard-boiled eggs', calPerServing: 72, keyNutrient: 'Protein 6g, whole food' }] },
    { name: 'Apple Sauce Pouches (no sugar added)', calPerServing: 50, keyNutrient: 'Vitamin C 10%', stars: 3, tags: ['good-staple'], missions: ['kidfriendly', 'budget'] }
  ],
  beverages: [
    { name: 'Green Tea Bags (40ct)', calPerServing: 0, keyNutrient: 'Catechins, L-theanine', stars: 5, tags: ['good-staple'], missions: ['antiinflammatory', 'heartsmart', 'budget'] },
    { name: 'Sparkling Water (12-pack)', calPerServing: 0, keyNutrient: 'Zero calories, zero sugar', stars: 5, tags: ['good-staple'], missions: ['diabetes', 'budget'] },
    { name: 'Coconut Water (33oz)', calPerServing: 45, keyNutrient: 'Potassium 470mg, Electrolytes', stars: 4, tags: ['good-staple'], missions: ['highprotein'] },
    { name: 'Orange Juice (64oz)', calPerServing: 110, keyNutrient: 'Vitamin C 137%', stars: 3, tags: ['limit-frequency'], missions: ['kidfriendly'], warnings: ['High natural sugar ~22g, no fiber'], alternatives: [{ name: 'Whole orange', calPerServing: 62, keyNutrient: 'Fiber 3g, Vitamin C 116%' }, { name: 'Infused water (citrus)', calPerServing: 0, keyNutrient: 'Hydration, minimal sugar' }] },
    { name: 'Soda (12-pack)', calPerServing: 140, keyNutrient: 'Sugar 39g', stars: 1, tags: ['ultra-processed'], missions: [], warnings: ['39g added sugar, zero nutrition'], alternatives: [{ name: 'Sparkling water + lemon', calPerServing: 0, keyNutrient: 'Zero sugar, refreshing' }, { name: 'Kombucha', calPerServing: 30, keyNutrient: 'Probiotics, 4g sugar' }] },
    { name: 'Unsweetened Iced Tea (64oz)', calPerServing: 0, keyNutrient: 'Polyphenols, zero sugar', stars: 4, tags: ['good-staple'], missions: ['diabetes', 'budget'] }
  ],
  pantry: [
    { name: 'Extra Virgin Olive Oil (16oz)', calPerServing: 120, keyNutrient: 'Healthy fats 14g, Polyphenols', stars: 5, tags: ['good-staple'], missions: ['mediterranean', 'heartsmart', 'antiinflammatory'] },
    { name: 'Canned Black Beans (15oz)', calPerServing: 110, keyNutrient: 'Protein 7g, Fiber 8g', stars: 5, tags: ['good-staple'], missions: ['budget', 'highprotein', 'diabetes'] },
    { name: 'Canned Diced Tomatoes (28oz)', calPerServing: 25, keyNutrient: 'Lycopene, Vitamin C 15%', stars: 5, tags: ['good-staple'], missions: ['budget', 'mediterranean'] },
    { name: 'Chia Seeds (12oz)', calPerServing: 140, keyNutrient: 'Fiber 10g, Omega-3 5g', stars: 5, tags: ['good-staple'], missions: ['antiinflammatory', 'heartsmart'] },
    { name: 'Peanut Butter Natural (16oz)', calPerServing: 190, keyNutrient: 'Protein 7g, Healthy fats 16g', stars: 4, tags: ['good-staple'], missions: ['highprotein', 'budget', 'kidfriendly'] },
    { name: 'Honey (16oz)', calPerServing: 60, keyNutrient: 'Antioxidants (raw)', stars: 3, tags: ['limit-frequency'], missions: [], warnings: ['Still sugar, 17g per tbsp'], alternatives: [{ name: 'Date syrup', calPerServing: 50, keyNutrient: 'Potassium, fiber traces' }] },
    { name: 'Canned Tuna in Water (5oz)', calPerServing: 70, keyNutrient: 'Protein 16g, Omega-3 0.5g', stars: 4, tags: ['good-staple'], missions: ['highprotein', 'budget'] },
    { name: 'Lentils Dry (1 lb)', calPerServing: 230, keyNutrient: 'Protein 18g, Fiber 16g', stars: 5, tags: ['good-staple'], missions: ['budget', 'heartsmart', 'mediterranean', 'highprotein'] }
  ]
}

const filteredProducts = computed(() => {
  let products = PRODUCTS[activeCategory.value] || []
  if (activeMission.value) {
    const relevant = products.filter(p => p.missions.includes(activeMission.value))
    const rest = products.filter(p => !p.missions.includes(activeMission.value))
    // Tag "Best for Plan" on relevant, show them first
    products = [...relevant, ...rest]
  }
  return products
})

function getProductTags(product) {
  const tags = []
  const goal = (props.dietGoal || '').toLowerCase()

  if (activeMission.value && product.missions.includes(activeMission.value)) {
    tags.push({ text: 'Best for Plan', class: isDark.value ? 'bg-emerald-500/15 text-emerald-400' : 'bg-emerald-50 text-emerald-700' })
  }

  if (product.tags.includes('good-staple')) {
    tags.push({ text: 'Good Staple', class: isDark.value ? 'bg-blue-500/15 text-blue-400' : 'bg-blue-50 text-blue-700' })
  }
  if (product.tags.includes('limit-frequency')) {
    tags.push({ text: 'Limit Frequency', class: isDark.value ? 'bg-amber-500/15 text-amber-400' : 'bg-amber-50 text-amber-700' })
  }
  if (product.tags.includes('ultra-processed')) {
    tags.push({ text: 'Ultra-Processed \u26A0\uFE0F', class: isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-700' })
  }

  // Allergy warnings
  if (props.allergies && props.allergies.length) {
    const nameL = product.name.toLowerCase()
    const hasAllergen = props.allergies.some(a => {
      const al = a.toLowerCase()
      if (al === 'dairy' || al === 'milk') return /yogurt|milk|cheese|cottage|cream/i.test(nameL)
      if (al === 'gluten' || al === 'wheat') return /bread|pasta|oats|ramen|wheat|noodle/i.test(nameL)
      if (al === 'peanuts' || al === 'nuts' || al === 'tree nuts') return /nut|peanut/i.test(nameL)
      if (al === 'soy') return /soy|tofu|edamame/i.test(nameL)
      if (al === 'fish' || al === 'shellfish') return /salmon|tuna|fish|sardine|shrimp/i.test(nameL)
      if (al === 'eggs' || al === 'egg') return /egg/i.test(nameL)
      return false
    })
    if (hasAllergen) {
      tags.push({ text: '\u26A0\uFE0F Allergy Risk', class: isDark.value ? 'bg-red-500/15 text-red-400' : 'bg-red-50 text-red-700' })
    }
  }

  return tags
}

function addToList(product) {
  if (!isInList(product)) {
    shoppingList.value.push({ ...product, checked: false, category: activeCategory.value })
  }
}

function isInList(product) {
  return shoppingList.value.some(i => i.name === product.name)
}

function removeFromList(item) {
  const idx = shoppingList.value.findIndex(i => i.name === item.name)
  if (idx >= 0) shoppingList.value.splice(idx, 1)
}

const groupedList = computed(() => {
  const groups = {}
  const labels = { produce: 'Produce', proteins: 'Proteins', dairy: 'Dairy', grains: 'Grains', frozen: 'Frozen', snacks: 'Snacks', beverages: 'Beverages', pantry: 'Pantry' }
  for (const item of shoppingList.value) {
    const cat = labels[item.category] || item.category
    if (!groups[cat]) groups[cat] = []
    groups[cat].push(item)
  }
  return Object.entries(groups).map(([category, items]) => ({ category, items }))
})

const estimatedWeeklyCal = computed(() =>
  shoppingList.value.reduce((sum, item) => sum + item.calPerServing * 14, 0)
)

async function copyList() {
  const text = groupedList.value.map(g =>
    `${g.category}:\n` + g.items.map(i => `  ${i.checked ? '[x]' : '[ ]'} ${i.name}`).join('\n')
  ).join('\n\n')
  try {
    await navigator.clipboard.writeText(text)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2000)
  } catch {
    // Fallback: do nothing
  }
}

function shareList() {
  const text = groupedList.value.map(g =>
    `${g.category}:\n` + g.items.map(i => `- ${i.name}`).join('\n')
  ).join('\n\n')
  if (navigator.share) {
    navigator.share({ title: 'Shopping List', text })
  } else {
    copyList()
  }
}
</script>
