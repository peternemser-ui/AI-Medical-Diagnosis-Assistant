/**
 * Recipe Database — 212 meals organized by category with nutritional data and tags.
 * Imported by NutritionPlanner.vue to power the Visual Menu Gallery.
 */

export const RECIPE_TAGS = [
  { id: 'high-protein', label: 'High Protein', color: 'red' },
  { id: 'low-carb', label: 'Low Carb', color: 'amber' },
  { id: 'low-fat', label: 'Low Fat', color: 'blue' },
  { id: 'low-sodium', label: 'Low Sodium', color: 'cyan' },
  { id: 'high-fiber', label: 'High Fiber', color: 'lime' },
  { id: 'anti-inflammatory', label: 'Anti-Inflammatory', color: 'purple' },
  { id: 'heart-healthy', label: 'Heart Healthy', color: 'rose' },
  { id: 'diabetes-friendly', label: 'Diabetes Friendly', color: 'teal' },
  { id: 'keto', label: 'Keto', color: 'orange' },
  { id: 'vegan', label: 'Vegan', color: 'green' },
  { id: 'vegetarian', label: 'Vegetarian', color: 'emerald' },
  { id: 'gluten-free', label: 'Gluten Free', color: 'indigo' },
  { id: 'dairy-free', label: 'Dairy Free', color: 'violet' },
  { id: 'quick', label: 'Quick', color: 'sky' },
  { id: 'meal-prep', label: 'Meal Prep', color: 'slate' },
]

export const RECIPE_CATEGORIES = [
  { id: 'all', label: 'All', icon: '\u{1F30D}' },
  { id: 'breakfast', label: 'Breakfast', icon: '\u{1F95E}' },
  { id: 'asian', label: 'Asian', icon: '\u{1F363}' },
  { id: 'mediterranean', label: 'Mediterranean', icon: '\u{1F957}' },
  { id: 'indian', label: 'Indian', icon: '\u{1F35B}' },
  { id: 'african', label: 'African', icon: '\u{1F372}' },
  { id: 'latin', label: 'Latin American', icon: '\u{1F32E}' },
  { id: 'european', label: 'European', icon: '\u{1F956}' },
  { id: 'middle-eastern', label: 'Middle Eastern', icon: '\u{1F9C6}' },
  { id: 'proteins', label: 'Proteins', icon: '\u{1F357}' },
  { id: 'bowls', label: 'Bowls & Grains', icon: '\u{1F35C}' },
  { id: 'vegan', label: 'Plant-Based', icon: '\u{1F331}' },
  { id: 'snacks', label: 'Snacks & Light', icon: '\u{1F34E}' },
  { id: 'soups', label: 'Soups', icon: '\u{1F372}' },
]

export const RECIPE_DATABASE = [
  // ════════════════════════════════════════════════════════════════════
  // BREAKFAST (20)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Egg White Omelette', emoji: '\u{1F373}', calories: 180, protein: 24, carbs: 4, fats: 8, prepTime: '10 min', category: 'breakfast', tags: ['high-protein', 'low-carb', 'keto', 'gluten-free', 'quick'] },
  { name: 'Protein Pancakes', emoji: '\u{1F95E}', calories: 320, protein: 28, carbs: 34, fats: 8, prepTime: '15 min', category: 'breakfast', tags: ['high-protein', 'meal-prep'] },
  { name: 'Smoothie Bowl', emoji: '\u{1FAD0}', calories: 340, protein: 12, carbs: 55, fats: 10, prepTime: '10 min', category: 'breakfast', tags: ['vegan', 'high-fiber', 'quick', 'dairy-free'] },
  { name: 'Steel-Cut Oatmeal', emoji: '\u{1F35A}', calories: 300, protein: 10, carbs: 52, fats: 6, prepTime: '20 min', category: 'breakfast', tags: ['high-fiber', 'vegan', 'heart-healthy', 'diabetes-friendly'] },
  { name: 'Breakfast Burrito', emoji: '\u{1F32F}', calories: 420, protein: 22, carbs: 40, fats: 18, prepTime: '15 min', category: 'breakfast', tags: ['high-protein', 'meal-prep'] },
  { name: 'French Toast', emoji: '\u{1F35E}', calories: 350, protein: 12, carbs: 45, fats: 14, prepTime: '15 min', category: 'breakfast', tags: ['vegetarian'] },
  { name: 'Bircher Muesli', emoji: '\u{1F95B}', calories: 310, protein: 10, carbs: 48, fats: 10, prepTime: '5 min', category: 'breakfast', tags: ['vegetarian', 'high-fiber', 'meal-prep', 'quick'] },
  { name: 'Eggs Benedict (Lighter)', emoji: '\u{1F373}', calories: 340, protein: 20, carbs: 26, fats: 18, prepTime: '20 min', category: 'breakfast', tags: ['high-protein'] },
  { name: 'Croissant & Jam', emoji: '\u{1F950}', calories: 290, protein: 6, carbs: 38, fats: 14, prepTime: '5 min', category: 'breakfast', tags: ['vegetarian', 'quick'] },
  { name: 'Spanish Tortilla', emoji: '\u{1F373}', calories: 280, protein: 14, carbs: 22, fats: 16, prepTime: '25 min', category: 'breakfast', tags: ['vegetarian', 'gluten-free'] },
  { name: 'Congee', emoji: '\u{1F35C}', calories: 220, protein: 8, carbs: 40, fats: 4, prepTime: '30 min', category: 'breakfast', tags: ['low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Miso Soup & Rice', emoji: '\u{1F35C}', calories: 260, protein: 10, carbs: 44, fats: 4, prepTime: '15 min', category: 'breakfast', tags: ['low-fat', 'vegan', 'dairy-free'] },
  { name: 'Nasi Goreng', emoji: '\u{1F35B}', calories: 380, protein: 14, carbs: 50, fats: 14, prepTime: '15 min', category: 'breakfast', tags: ['dairy-free', 'quick'] },
  { name: 'Japanese Tamago', emoji: '\u{1F373}', calories: 200, protein: 14, carbs: 6, fats: 14, prepTime: '10 min', category: 'breakfast', tags: ['low-carb', 'gluten-free', 'quick'] },
  { name: 'Turkish Menemen', emoji: '\u{1F345}', calories: 280, protein: 14, carbs: 18, fats: 16, prepTime: '15 min', category: 'breakfast', tags: ['vegetarian', 'gluten-free', 'low-carb'] },
  { name: 'Ful Medames', emoji: '\u{1F963}', calories: 310, protein: 18, carbs: 42, fats: 8, prepTime: '20 min', category: 'breakfast', tags: ['vegan', 'high-fiber', 'high-protein', 'dairy-free'] },
  { name: 'Labneh & Za\'atar', emoji: '\u{1F95B}', calories: 240, protein: 12, carbs: 20, fats: 14, prepTime: '5 min', category: 'breakfast', tags: ['vegetarian', 'quick'] },
  { name: 'Chilaquiles', emoji: '\u{1F32E}', calories: 360, protein: 16, carbs: 36, fats: 18, prepTime: '20 min', category: 'breakfast', tags: ['gluten-free'] },
  { name: 'Arepas', emoji: '\u{1F35E}', calories: 290, protein: 10, carbs: 40, fats: 10, prepTime: '20 min', category: 'breakfast', tags: ['gluten-free', 'vegetarian', 'dairy-free'] },
  { name: 'Idli & Sambar', emoji: '\u{1F35B}', calories: 250, protein: 10, carbs: 44, fats: 4, prepTime: '25 min', category: 'breakfast', tags: ['vegan', 'low-fat', 'dairy-free'] },

  // ════════════════════════════════════════════════════════════════════
  // ASIAN (25)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Sashimi', emoji: '\u{1F363}', calories: 180, protein: 26, carbs: 0, fats: 8, prepTime: '5 min', category: 'asian', tags: ['high-protein', 'low-carb', 'keto', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Teriyaki Salmon', emoji: '\u{1F41F}', calories: 380, protein: 34, carbs: 16, fats: 18, prepTime: '20 min', category: 'asian', tags: ['high-protein', 'heart-healthy', 'anti-inflammatory'] },
  { name: 'Edamame Rice Bowl', emoji: '\u{1F35A}', calories: 390, protein: 18, carbs: 52, fats: 12, prepTime: '15 min', category: 'asian', tags: ['vegetarian', 'high-fiber'] },
  { name: 'Miso Ramen', emoji: '\u{1F35C}', calories: 450, protein: 20, carbs: 55, fats: 16, prepTime: '20 min', category: 'asian', tags: ['dairy-free'] },
  { name: 'Yakitori', emoji: '\u{1F362}', calories: 260, protein: 28, carbs: 8, fats: 12, prepTime: '20 min', category: 'asian', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free'] },
  { name: 'Okonomiyaki', emoji: '\u{1F95E}', calories: 390, protein: 16, carbs: 42, fats: 18, prepTime: '25 min', category: 'asian', tags: [] },
  { name: 'Soba Noodles', emoji: '\u{1F35C}', calories: 320, protein: 14, carbs: 56, fats: 4, prepTime: '15 min', category: 'asian', tags: ['low-fat', 'vegan', 'dairy-free'] },
  { name: 'Kung Pao Chicken', emoji: '\u{1F357}', calories: 420, protein: 30, carbs: 24, fats: 22, prepTime: '20 min', category: 'asian', tags: ['high-protein', 'gluten-free'] },
  { name: 'Steamed Dim Sum', emoji: '\u{1F95F}', calories: 280, protein: 14, carbs: 32, fats: 10, prepTime: '15 min', category: 'asian', tags: ['low-fat'] },
  { name: 'Mapo Tofu', emoji: '\u{1F961}', calories: 320, protein: 20, carbs: 14, fats: 20, prepTime: '15 min', category: 'asian', tags: ['vegan', 'gluten-free', 'low-carb', 'quick'] },
  { name: 'Stir-Fry Vegetables', emoji: '\u{1F96C}', calories: 200, protein: 8, carbs: 24, fats: 10, prepTime: '10 min', category: 'asian', tags: ['vegan', 'low-carb', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Wonton Soup', emoji: '\u{1F35C}', calories: 260, protein: 16, carbs: 28, fats: 8, prepTime: '20 min', category: 'asian', tags: ['low-fat'] },
  { name: 'Bibimbap', emoji: '\u{1F35A}', calories: 490, protein: 22, carbs: 65, fats: 14, prepTime: '25 min', category: 'asian', tags: ['high-fiber'] },
  { name: 'Japchae', emoji: '\u{1F35D}', calories: 340, protein: 12, carbs: 50, fats: 10, prepTime: '25 min', category: 'asian', tags: ['dairy-free'] },
  { name: 'Kimchi Jjigae', emoji: '\u{1F372}', calories: 300, protein: 20, carbs: 18, fats: 16, prepTime: '25 min', category: 'asian', tags: ['anti-inflammatory', 'gluten-free', 'dairy-free'] },
  { name: 'Korean BBQ Lettuce Wraps', emoji: '\u{1F969}', calories: 340, protein: 32, carbs: 10, fats: 18, prepTime: '20 min', category: 'asian', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Green Curry', emoji: '\u{1F35B}', calories: 420, protein: 24, carbs: 30, fats: 22, prepTime: '30 min', category: 'asian', tags: ['gluten-free', 'dairy-free'] },
  { name: 'Pad Thai', emoji: '\u{1F35D}', calories: 440, protein: 18, carbs: 56, fats: 16, prepTime: '20 min', category: 'asian', tags: ['gluten-free', 'dairy-free'] },
  { name: 'Tom Yum Soup', emoji: '\u{1F35C}', calories: 180, protein: 16, carbs: 12, fats: 8, prepTime: '20 min', category: 'asian', tags: ['low-carb', 'low-fat', 'gluten-free', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Thai Basil Chicken', emoji: '\u{1F357}', calories: 380, protein: 28, carbs: 22, fats: 18, prepTime: '15 min', category: 'asian', tags: ['high-protein', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Pho', emoji: '\u{1F35C}', calories: 350, protein: 28, carbs: 40, fats: 6, prepTime: '20 min', category: 'asian', tags: ['low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Banh Mi', emoji: '\u{1F956}', calories: 380, protein: 20, carbs: 44, fats: 14, prepTime: '15 min', category: 'asian', tags: ['dairy-free', 'quick'] },
  { name: 'Spring Rolls (Fresh)', emoji: '\u{1F961}', calories: 160, protein: 8, carbs: 24, fats: 4, prepTime: '15 min', category: 'asian', tags: ['low-fat', 'low-carb', 'gluten-free', 'dairy-free', 'vegan'] },
  { name: 'Bun Cha', emoji: '\u{1F35C}', calories: 400, protein: 26, carbs: 42, fats: 14, prepTime: '25 min', category: 'asian', tags: ['dairy-free'] },
  { name: 'Teriyaki Tofu Bowl', emoji: '\u{1F961}', calories: 380, protein: 18, carbs: 48, fats: 12, prepTime: '20 min', category: 'asian', tags: ['vegan', 'dairy-free'] },

  // ════════════════════════════════════════════════════════════════════
  // MEDITERRANEAN (20)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Souvlaki', emoji: '\u{1F962}', calories: 350, protein: 30, carbs: 24, fats: 14, prepTime: '20 min', category: 'mediterranean', tags: ['high-protein', 'gluten-free'] },
  { name: 'Moussaka', emoji: '\u{1F346}', calories: 380, protein: 20, carbs: 28, fats: 20, prepTime: '45 min', category: 'mediterranean', tags: ['gluten-free'] },
  { name: 'Spanakopita', emoji: '\u{1F96C}', calories: 280, protein: 12, carbs: 24, fats: 16, prepTime: '35 min', category: 'mediterranean', tags: ['vegetarian'] },
  { name: 'Greek Salad', emoji: '\u{1F957}', calories: 240, protein: 8, carbs: 14, fats: 18, prepTime: '10 min', category: 'mediterranean', tags: ['vegetarian', 'low-carb', 'gluten-free', 'quick'] },
  { name: 'Tzatziki Bowl', emoji: '\u{1F95B}', calories: 200, protein: 10, carbs: 16, fats: 12, prepTime: '10 min', category: 'mediterranean', tags: ['vegetarian', 'low-carb', 'gluten-free', 'quick'] },
  { name: 'Shakshuka', emoji: '\u{1F373}', calories: 290, protein: 16, carbs: 18, fats: 16, prepTime: '20 min', category: 'mediterranean', tags: ['vegetarian', 'gluten-free', 'low-carb'] },
  { name: 'Adana Kebab', emoji: '\u{1F356}', calories: 400, protein: 34, carbs: 10, fats: 24, prepTime: '25 min', category: 'mediterranean', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Pide', emoji: '\u{1F956}', calories: 420, protein: 18, carbs: 48, fats: 16, prepTime: '30 min', category: 'mediterranean', tags: [] },
  { name: 'Lentil Soup (Turkish)', emoji: '\u{1F963}', calories: 240, protein: 14, carbs: 36, fats: 4, prepTime: '25 min', category: 'mediterranean', tags: ['vegan', 'high-fiber', 'low-fat', 'dairy-free', 'heart-healthy'] },
  { name: 'Falafel Wrap', emoji: '\u{1F32F}', calories: 400, protein: 14, carbs: 48, fats: 18, prepTime: '15 min', category: 'mediterranean', tags: ['vegan', 'dairy-free', 'high-fiber'] },
  { name: 'Tabbouleh', emoji: '\u{1F33F}', calories: 160, protein: 4, carbs: 22, fats: 8, prepTime: '15 min', category: 'mediterranean', tags: ['vegan', 'low-fat', 'dairy-free'] },
  { name: 'Fattoush', emoji: '\u{1F957}', calories: 180, protein: 4, carbs: 20, fats: 10, prepTime: '10 min', category: 'mediterranean', tags: ['vegan', 'dairy-free', 'quick'] },
  { name: 'Hummus Plate', emoji: '\u{1F963}', calories: 300, protein: 12, carbs: 30, fats: 16, prepTime: '10 min', category: 'mediterranean', tags: ['vegan', 'high-fiber', 'dairy-free', 'quick'] },
  { name: 'Shawarma', emoji: '\u{1F32F}', calories: 440, protein: 30, carbs: 36, fats: 18, prepTime: '25 min', category: 'mediterranean', tags: ['high-protein', 'dairy-free'] },
  { name: 'Caprese', emoji: '\u{1F345}', calories: 220, protein: 14, carbs: 8, fats: 16, prepTime: '5 min', category: 'mediterranean', tags: ['vegetarian', 'low-carb', 'gluten-free', 'quick'] },
  { name: 'Minestrone', emoji: '\u{1F372}', calories: 200, protein: 8, carbs: 30, fats: 6, prepTime: '30 min', category: 'mediterranean', tags: ['vegan', 'high-fiber', 'low-fat', 'dairy-free', 'heart-healthy'] },
  { name: 'Grilled Branzino', emoji: '\u{1F41F}', calories: 300, protein: 36, carbs: 2, fats: 16, prepTime: '20 min', category: 'mediterranean', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'heart-healthy', 'keto'] },
  { name: 'Panzanella', emoji: '\u{1F957}', calories: 280, protein: 8, carbs: 32, fats: 14, prepTime: '15 min', category: 'mediterranean', tags: ['vegan', 'dairy-free'] },
  { name: 'Gazpacho', emoji: '\u{1F345}', calories: 120, protein: 3, carbs: 14, fats: 6, prepTime: '15 min', category: 'mediterranean', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Paella', emoji: '\u{1F35B}', calories: 460, protein: 26, carbs: 52, fats: 16, prepTime: '40 min', category: 'mediterranean', tags: ['gluten-free', 'dairy-free'] },

  // ════════════════════════════════════════════════════════════════════
  // INDIAN (18)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Dal Tadka', emoji: '\u{1F35B}', calories: 280, protein: 16, carbs: 38, fats: 8, prepTime: '25 min', category: 'indian', tags: ['vegan', 'high-fiber', 'high-protein', 'dairy-free', 'gluten-free'] },
  { name: 'Tandoori Chicken', emoji: '\u{1F357}', calories: 320, protein: 36, carbs: 8, fats: 14, prepTime: '30 min', category: 'indian', tags: ['high-protein', 'low-carb', 'gluten-free'] },
  { name: 'Palak Paneer', emoji: '\u{1F96C}', calories: 350, protein: 18, carbs: 14, fats: 24, prepTime: '25 min', category: 'indian', tags: ['vegetarian', 'gluten-free', 'low-carb', 'anti-inflammatory'] },
  { name: 'Chana Masala', emoji: '\u{1F35B}', calories: 300, protein: 12, carbs: 44, fats: 8, prepTime: '20 min', category: 'indian', tags: ['vegan', 'high-fiber', 'dairy-free', 'gluten-free'] },
  { name: 'Chicken Tikka Masala', emoji: '\u{1F372}', calories: 420, protein: 30, carbs: 20, fats: 24, prepTime: '30 min', category: 'indian', tags: ['high-protein', 'gluten-free'] },
  { name: 'Aloo Gobi', emoji: '\u{1F954}', calories: 250, protein: 6, carbs: 34, fats: 10, prepTime: '25 min', category: 'indian', tags: ['vegan', 'gluten-free', 'dairy-free'] },
  { name: 'Rajma', emoji: '\u{1F963}', calories: 310, protein: 16, carbs: 46, fats: 6, prepTime: '30 min', category: 'indian', tags: ['vegan', 'high-fiber', 'high-protein', 'dairy-free', 'gluten-free'] },
  { name: 'Butter Chicken (Lighter)', emoji: '\u{1F357}', calories: 380, protein: 32, carbs: 16, fats: 20, prepTime: '30 min', category: 'indian', tags: ['high-protein', 'gluten-free'] },
  { name: 'Fish Curry', emoji: '\u{1F41F}', calories: 320, protein: 28, carbs: 14, fats: 16, prepTime: '25 min', category: 'indian', tags: ['high-protein', 'gluten-free', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Vegetable Biryani', emoji: '\u{1F35A}', calories: 400, protein: 10, carbs: 62, fats: 12, prepTime: '35 min', category: 'indian', tags: ['vegetarian', 'gluten-free'] },
  { name: 'Dosa & Chutney', emoji: '\u{1F95E}', calories: 260, protein: 8, carbs: 40, fats: 8, prepTime: '20 min', category: 'indian', tags: ['vegan', 'gluten-free', 'dairy-free'] },
  { name: 'Samosa (Baked)', emoji: '\u{1F95F}', calories: 220, protein: 6, carbs: 30, fats: 8, prepTime: '30 min', category: 'indian', tags: ['vegan', 'dairy-free', 'meal-prep'] },
  { name: 'Paneer Tikka', emoji: '\u{1F9C0}', calories: 300, protein: 20, carbs: 10, fats: 20, prepTime: '20 min', category: 'indian', tags: ['vegetarian', 'low-carb', 'gluten-free', 'high-protein'] },
  { name: 'Khichdi', emoji: '\u{1F35A}', calories: 280, protein: 12, carbs: 44, fats: 6, prepTime: '20 min', category: 'indian', tags: ['vegan', 'gluten-free', 'dairy-free', 'low-fat'] },
  { name: 'Rasam', emoji: '\u{1F963}', calories: 100, protein: 4, carbs: 14, fats: 2, prepTime: '15 min', category: 'indian', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free', 'anti-inflammatory', 'quick'] },
  { name: 'Upma', emoji: '\u{1F35A}', calories: 240, protein: 6, carbs: 38, fats: 8, prepTime: '15 min', category: 'indian', tags: ['vegetarian', 'dairy-free', 'quick'] },
  { name: 'Chole Bhature (Baked)', emoji: '\u{1F35E}', calories: 400, protein: 14, carbs: 52, fats: 14, prepTime: '35 min', category: 'indian', tags: ['vegetarian', 'high-fiber'] },
  { name: 'Matar Paneer', emoji: '\u{1F9C0}', calories: 340, protein: 18, carbs: 18, fats: 22, prepTime: '25 min', category: 'indian', tags: ['vegetarian', 'gluten-free'] },

  // ════════════════════════════════════════════════════════════════════
  // AFRICAN (15)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Jollof Rice', emoji: '\u{1F35A}', calories: 420, protein: 12, carbs: 62, fats: 12, prepTime: '35 min', category: 'african', tags: ['gluten-free', 'dairy-free'] },
  { name: 'Suya Kebabs', emoji: '\u{1F362}', calories: 320, protein: 34, carbs: 4, fats: 18, prepTime: '20 min', category: 'african', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Egusi Soup', emoji: '\u{1F372}', calories: 380, protein: 22, carbs: 16, fats: 26, prepTime: '35 min', category: 'african', tags: ['gluten-free', 'dairy-free'] },
  { name: 'Fufu & Light Soup', emoji: '\u{1F35C}', calories: 360, protein: 18, carbs: 52, fats: 8, prepTime: '30 min', category: 'african', tags: ['gluten-free', 'dairy-free', 'low-fat'] },
  { name: 'Plantain & Beans', emoji: '\u{1F34C}', calories: 340, protein: 14, carbs: 56, fats: 6, prepTime: '20 min', category: 'african', tags: ['vegan', 'high-fiber', 'low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Injera & Lentil Stew', emoji: '\u{1F372}', calories: 350, protein: 18, carbs: 50, fats: 8, prepTime: '30 min', category: 'african', tags: ['vegan', 'high-fiber', 'dairy-free'] },
  { name: 'Nyama Choma', emoji: '\u{1F969}', calories: 380, protein: 38, carbs: 2, fats: 24, prepTime: '30 min', category: 'african', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Ugali & Sukuma Wiki', emoji: '\u{1F96C}', calories: 300, protein: 8, carbs: 54, fats: 6, prepTime: '20 min', category: 'african', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Moroccan Tagine', emoji: '\u{1F372}', calories: 380, protein: 28, carbs: 35, fats: 14, prepTime: '40 min', category: 'african', tags: ['gluten-free', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Couscous Royale', emoji: '\u{1F35A}', calories: 440, protein: 24, carbs: 56, fats: 12, prepTime: '35 min', category: 'african', tags: ['dairy-free'] },
  { name: 'Harira Soup', emoji: '\u{1F963}', calories: 260, protein: 16, carbs: 34, fats: 6, prepTime: '30 min', category: 'african', tags: ['high-fiber', 'low-fat', 'dairy-free'] },
  { name: 'Shakshuka (North African)', emoji: '\u{1F373}', calories: 290, protein: 16, carbs: 18, fats: 16, prepTime: '20 min', category: 'african', tags: ['vegetarian', 'gluten-free', 'low-carb'] },
  { name: 'Bobotie', emoji: '\u{1F35B}', calories: 380, protein: 26, carbs: 22, fats: 20, prepTime: '45 min', category: 'african', tags: ['gluten-free'] },
  { name: 'Chakalaka', emoji: '\u{1F336}\uFE0F', calories: 180, protein: 6, carbs: 28, fats: 6, prepTime: '25 min', category: 'african', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free', 'high-fiber'] },
  { name: 'Bunny Chow', emoji: '\u{1F35E}', calories: 440, protein: 22, carbs: 50, fats: 16, prepTime: '30 min', category: 'african', tags: ['dairy-free'] },

  // ════════════════════════════════════════════════════════════════════
  // LATIN AMERICAN (15)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Burrito Bowl', emoji: '\u{1F32E}', calories: 450, protein: 32, carbs: 48, fats: 14, prepTime: '15 min', category: 'latin', tags: ['high-protein', 'gluten-free', 'meal-prep'] },
  { name: 'Ceviche', emoji: '\u{1F990}', calories: 200, protein: 24, carbs: 12, fats: 6, prepTime: '30 min', category: 'latin', tags: ['high-protein', 'low-carb', 'low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Acai Bowl', emoji: '\u{1FAD0}', calories: 380, protein: 8, carbs: 60, fats: 12, prepTime: '10 min', category: 'latin', tags: ['vegan', 'dairy-free', 'anti-inflammatory', 'quick'] },
  { name: 'Fish Tacos', emoji: '\u{1F32E}', calories: 340, protein: 26, carbs: 30, fats: 12, prepTime: '20 min', category: 'latin', tags: ['high-protein'] },
  { name: 'Cuban Black Beans', emoji: '\u{1F963}', calories: 280, protein: 16, carbs: 42, fats: 4, prepTime: '25 min', category: 'latin', tags: ['vegan', 'high-fiber', 'low-fat', 'gluten-free', 'dairy-free', 'heart-healthy'] },
  { name: 'Empanadas (Baked)', emoji: '\u{1F95F}', calories: 300, protein: 14, carbs: 32, fats: 12, prepTime: '30 min', category: 'latin', tags: ['meal-prep'] },
  { name: 'Arroz con Pollo', emoji: '\u{1F35A}', calories: 420, protein: 30, carbs: 48, fats: 12, prepTime: '30 min', category: 'latin', tags: ['high-protein', 'gluten-free', 'dairy-free'] },
  { name: 'Lomo Saltado', emoji: '\u{1F969}', calories: 440, protein: 32, carbs: 34, fats: 18, prepTime: '20 min', category: 'latin', tags: ['high-protein', 'gluten-free', 'dairy-free'] },
  { name: 'Moqueca', emoji: '\u{1F41F}', calories: 380, protein: 28, carbs: 18, fats: 22, prepTime: '30 min', category: 'latin', tags: ['gluten-free', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Pupusas', emoji: '\u{1F35E}', calories: 320, protein: 12, carbs: 40, fats: 12, prepTime: '25 min', category: 'latin', tags: ['gluten-free'] },
  { name: 'Gallo Pinto', emoji: '\u{1F35A}', calories: 300, protein: 12, carbs: 48, fats: 6, prepTime: '15 min', category: 'latin', tags: ['vegan', 'high-fiber', 'low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Elote', emoji: '\u{1F33D}', calories: 220, protein: 6, carbs: 30, fats: 10, prepTime: '10 min', category: 'latin', tags: ['vegetarian', 'gluten-free', 'quick'] },
  { name: 'Churrasco', emoji: '\u{1F969}', calories: 400, protein: 38, carbs: 4, fats: 26, prepTime: '20 min', category: 'latin', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Ajiaco', emoji: '\u{1F372}', calories: 320, protein: 22, carbs: 36, fats: 10, prepTime: '35 min', category: 'latin', tags: ['gluten-free'] },
  { name: 'Feijoada (Lighter)', emoji: '\u{1F372}', calories: 400, protein: 28, carbs: 40, fats: 14, prepTime: '40 min', category: 'latin', tags: ['high-protein', 'high-fiber', 'gluten-free', 'dairy-free'] },

  // ════════════════════════════════════════════════════════════════════
  // EUROPEAN (15)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Ratatouille', emoji: '\u{1F346}', calories: 220, protein: 6, carbs: 28, fats: 10, prepTime: '35 min', category: 'european', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Schnitzel', emoji: '\u{1F357}', calories: 400, protein: 34, carbs: 22, fats: 18, prepTime: '25 min', category: 'european', tags: ['high-protein'] },
  { name: 'Gazpacho (Spanish)', emoji: '\u{1F345}', calories: 120, protein: 3, carbs: 14, fats: 6, prepTime: '15 min', category: 'european', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Swedish Meatballs', emoji: '\u{1F356}', calories: 380, protein: 28, carbs: 18, fats: 22, prepTime: '30 min', category: 'european', tags: ['high-protein', 'meal-prep'] },
  { name: 'Chicken Kyiv', emoji: '\u{1F357}', calories: 420, protein: 30, carbs: 20, fats: 24, prepTime: '30 min', category: 'european', tags: ['high-protein'] },
  { name: 'Fish & Chips (Baked)', emoji: '\u{1F41F}', calories: 380, protein: 28, carbs: 38, fats: 14, prepTime: '30 min', category: 'european', tags: ['high-protein'] },
  { name: 'Beef Stroganoff', emoji: '\u{1F356}', calories: 440, protein: 30, carbs: 28, fats: 22, prepTime: '30 min', category: 'european', tags: ['high-protein'] },
  { name: 'Pierogi', emoji: '\u{1F95F}', calories: 360, protein: 12, carbs: 46, fats: 14, prepTime: '35 min', category: 'european', tags: ['vegetarian', 'meal-prep'] },
  { name: 'Goulash', emoji: '\u{1F372}', calories: 380, protein: 28, carbs: 24, fats: 18, prepTime: '40 min', category: 'european', tags: ['high-protein', 'gluten-free', 'dairy-free'] },
  { name: 'Coq au Vin', emoji: '\u{1F357}', calories: 400, protein: 32, carbs: 14, fats: 22, prepTime: '45 min', category: 'european', tags: ['high-protein', 'gluten-free', 'dairy-free'] },
  { name: 'Bouillabaisse', emoji: '\u{1F41F}', calories: 300, protein: 30, carbs: 16, fats: 12, prepTime: '35 min', category: 'european', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'heart-healthy'] },
  { name: 'Sauerbraten', emoji: '\u{1F356}', calories: 420, protein: 34, carbs: 22, fats: 20, prepTime: '45 min', category: 'european', tags: ['high-protein', 'dairy-free'] },
  { name: 'Bangers & Mash', emoji: '\u{1F356}', calories: 440, protein: 20, carbs: 42, fats: 22, prepTime: '25 min', category: 'european', tags: ['gluten-free'] },
  { name: 'Norwegian Salmon', emoji: '\u{1F41F}', calories: 360, protein: 36, carbs: 4, fats: 22, prepTime: '20 min', category: 'european', tags: ['high-protein', 'low-carb', 'gluten-free', 'heart-healthy', 'anti-inflammatory', 'keto'] },
  { name: 'Souvlaki (Greek)', emoji: '\u{1F962}', calories: 350, protein: 30, carbs: 24, fats: 14, prepTime: '20 min', category: 'european', tags: ['high-protein', 'gluten-free'] },

  // ════════════════════════════════════════════════════════════════════
  // MIDDLE EASTERN (12)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Kabsa', emoji: '\u{1F35A}', calories: 460, protein: 28, carbs: 52, fats: 16, prepTime: '40 min', category: 'middle-eastern', tags: ['gluten-free', 'dairy-free'] },
  { name: 'Mansaf', emoji: '\u{1F35B}', calories: 500, protein: 30, carbs: 48, fats: 20, prepTime: '45 min', category: 'middle-eastern', tags: ['high-protein'] },
  { name: 'Koshari', emoji: '\u{1F35C}', calories: 380, protein: 14, carbs: 62, fats: 8, prepTime: '30 min', category: 'middle-eastern', tags: ['vegan', 'high-fiber', 'low-fat', 'dairy-free'] },
  { name: 'Ful Medames (ME)', emoji: '\u{1F963}', calories: 310, protein: 18, carbs: 42, fats: 8, prepTime: '20 min', category: 'middle-eastern', tags: ['vegan', 'high-fiber', 'high-protein', 'dairy-free', 'gluten-free'] },
  { name: 'Kibbeh', emoji: '\u{1F356}', calories: 340, protein: 20, carbs: 28, fats: 16, prepTime: '35 min', category: 'middle-eastern', tags: ['dairy-free'] },
  { name: 'Maqluba', emoji: '\u{1F35A}', calories: 440, protein: 24, carbs: 50, fats: 16, prepTime: '40 min', category: 'middle-eastern', tags: ['dairy-free', 'gluten-free'] },
  { name: 'Musakhan', emoji: '\u{1F357}', calories: 420, protein: 28, carbs: 38, fats: 18, prepTime: '35 min', category: 'middle-eastern', tags: ['dairy-free'] },
  { name: 'Fatayer', emoji: '\u{1F95F}', calories: 280, protein: 10, carbs: 32, fats: 12, prepTime: '30 min', category: 'middle-eastern', tags: ['vegetarian', 'meal-prep'] },
  { name: 'Lamb Kofta', emoji: '\u{1F362}', calories: 360, protein: 28, carbs: 8, fats: 24, prepTime: '20 min', category: 'middle-eastern', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free'] },
  { name: 'Rice Pilaf', emoji: '\u{1F35A}', calories: 320, protein: 8, carbs: 52, fats: 10, prepTime: '25 min', category: 'middle-eastern', tags: ['vegan', 'gluten-free', 'dairy-free'] },
  { name: 'Chicken Shawarma Plate', emoji: '\u{1F357}', calories: 440, protein: 34, carbs: 36, fats: 16, prepTime: '25 min', category: 'middle-eastern', tags: ['high-protein', 'dairy-free'] },
  { name: 'Grilled Halloumi', emoji: '\u{1F9C0}', calories: 280, protein: 18, carbs: 4, fats: 22, prepTime: '10 min', category: 'middle-eastern', tags: ['vegetarian', 'low-carb', 'gluten-free', 'keto', 'quick'] },

  // ════════════════════════════════════════════════════════════════════
  // PROTEINS (15)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Grilled Chicken Breast', emoji: '\u{1F357}', calories: 280, protein: 42, carbs: 2, fats: 10, prepTime: '20 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto', 'meal-prep'] },
  { name: 'Baked Salmon', emoji: '\u{1F41F}', calories: 350, protein: 38, carbs: 0, fats: 22, prepTime: '25 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'heart-healthy', 'anti-inflammatory', 'keto'] },
  { name: 'Turkey Meatballs', emoji: '\u{1F356}', calories: 260, protein: 28, carbs: 10, fats: 12, prepTime: '20 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'meal-prep'] },
  { name: 'Shrimp Skewers', emoji: '\u{1F990}', calories: 200, protein: 30, carbs: 4, fats: 6, prepTime: '15 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'low-fat', 'gluten-free', 'dairy-free', 'keto', 'quick'] },
  { name: 'Pan-Seared Tuna', emoji: '\u{1F41F}', calories: 240, protein: 36, carbs: 0, fats: 10, prepTime: '10 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto', 'quick'] },
  { name: 'Lamb Chops', emoji: '\u{1F356}', calories: 360, protein: 32, carbs: 0, fats: 26, prepTime: '20 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Bison Burger', emoji: '\u{1F354}', calories: 320, protein: 34, carbs: 24, fats: 10, prepTime: '15 min', category: 'proteins', tags: ['high-protein', 'low-fat'] },
  { name: 'Pork Tenderloin', emoji: '\u{1F356}', calories: 300, protein: 36, carbs: 2, fats: 16, prepTime: '25 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free'] },
  { name: 'Duck Breast', emoji: '\u{1F986}', calories: 340, protein: 28, carbs: 0, fats: 24, prepTime: '20 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Cod Fillet', emoji: '\u{1F41F}', calories: 200, protein: 32, carbs: 0, fats: 8, prepTime: '15 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'low-fat', 'gluten-free', 'dairy-free', 'keto', 'quick'] },
  { name: 'Chicken Thighs', emoji: '\u{1F357}', calories: 320, protein: 30, carbs: 0, fats: 22, prepTime: '25 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto', 'meal-prep'] },
  { name: 'Steak (Sirloin)', emoji: '\u{1F969}', calories: 380, protein: 40, carbs: 0, fats: 24, prepTime: '15 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Tofu Steak', emoji: '\u{1F961}', calories: 200, protein: 18, carbs: 6, fats: 12, prepTime: '15 min', category: 'proteins', tags: ['vegan', 'low-carb', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Tempeh Strips', emoji: '\u{1F331}', calories: 220, protein: 20, carbs: 10, fats: 12, prepTime: '15 min', category: 'proteins', tags: ['vegan', 'high-protein', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Egg White Frittata', emoji: '\u{1F373}', calories: 180, protein: 24, carbs: 6, fats: 6, prepTime: '15 min', category: 'proteins', tags: ['high-protein', 'low-carb', 'low-fat', 'gluten-free', 'keto', 'quick'] },

  // ════════════════════════════════════════════════════════════════════
  // BOWLS & GRAINS (15)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Quinoa Power Bowl', emoji: '\u{1F35C}', calories: 420, protein: 18, carbs: 55, fats: 14, prepTime: '20 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'gluten-free', 'dairy-free', 'meal-prep'] },
  { name: 'Poke Bowl', emoji: '\u{1F363}', calories: 450, protein: 28, carbs: 50, fats: 14, prepTime: '15 min', category: 'bowls', tags: ['high-protein', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Buddha Bowl', emoji: '\u{1F966}', calories: 380, protein: 16, carbs: 48, fats: 14, prepTime: '20 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'dairy-free', 'meal-prep'] },
  { name: 'Couscous & Veg', emoji: '\u{1F33E}', calories: 340, protein: 12, carbs: 52, fats: 10, prepTime: '20 min', category: 'bowls', tags: ['vegan', 'dairy-free'] },
  { name: 'Brown Rice & Black Bean', emoji: '\u{1F35A}', calories: 380, protein: 14, carbs: 62, fats: 6, prepTime: '20 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Farro Salad', emoji: '\u{1F33E}', calories: 320, protein: 12, carbs: 50, fats: 8, prepTime: '25 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'dairy-free', 'meal-prep'] },
  { name: 'Grain Bowl', emoji: '\u{1F35C}', calories: 400, protein: 16, carbs: 56, fats: 12, prepTime: '20 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'dairy-free'] },
  { name: 'Harvest Bowl', emoji: '\u{1F33D}', calories: 420, protein: 14, carbs: 58, fats: 14, prepTime: '25 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'dairy-free'] },
  { name: 'Burrito Bowl (Grain)', emoji: '\u{1F32E}', calories: 460, protein: 24, carbs: 56, fats: 14, prepTime: '15 min', category: 'bowls', tags: ['gluten-free', 'dairy-free', 'high-protein', 'quick'] },
  { name: 'Sushi Bowl', emoji: '\u{1F363}', calories: 400, protein: 22, carbs: 54, fats: 10, prepTime: '15 min', category: 'bowls', tags: ['dairy-free', 'quick'] },
  { name: 'Nourish Bowl', emoji: '\u{1F96C}', calories: 380, protein: 14, carbs: 48, fats: 16, prepTime: '20 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'anti-inflammatory', 'dairy-free'] },
  { name: 'Macro Bowl', emoji: '\u{1F4AA}', calories: 440, protein: 30, carbs: 44, fats: 16, prepTime: '20 min', category: 'bowls', tags: ['high-protein', 'meal-prep', 'gluten-free'] },
  { name: 'Korean Bibimbap Bowl', emoji: '\u{1F35A}', calories: 490, protein: 22, carbs: 62, fats: 16, prepTime: '25 min', category: 'bowls', tags: ['dairy-free'] },
  { name: 'Moroccan Grain Bowl', emoji: '\u{1F33E}', calories: 400, protein: 14, carbs: 56, fats: 14, prepTime: '25 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Sweet Potato Bowl', emoji: '\u{1F360}', calories: 360, protein: 12, carbs: 54, fats: 12, prepTime: '25 min', category: 'bowls', tags: ['vegan', 'high-fiber', 'gluten-free', 'dairy-free'] },

  // ════════════════════════════════════════════════════════════════════
  // PLANT-BASED (15)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Lentil Bolognese', emoji: '\u{1F35D}', calories: 340, protein: 18, carbs: 48, fats: 6, prepTime: '25 min', category: 'vegan', tags: ['vegan', 'high-fiber', 'low-fat', 'dairy-free', 'heart-healthy', 'meal-prep'] },
  { name: 'Cauliflower Steak', emoji: '\u{1F966}', calories: 220, protein: 8, carbs: 18, fats: 14, prepTime: '25 min', category: 'vegan', tags: ['vegan', 'low-carb', 'gluten-free', 'dairy-free', 'keto'] },
  { name: 'Tofu Stir-Fry', emoji: '\u{1F961}', calories: 300, protein: 20, carbs: 28, fats: 12, prepTime: '15 min', category: 'vegan', tags: ['vegan', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Black Bean Burger', emoji: '\u{1F354}', calories: 350, protein: 16, carbs: 40, fats: 12, prepTime: '20 min', category: 'vegan', tags: ['vegan', 'high-fiber', 'dairy-free', 'meal-prep'] },
  { name: 'Chickpea Curry', emoji: '\u{1F35B}', calories: 320, protein: 14, carbs: 42, fats: 10, prepTime: '20 min', category: 'vegan', tags: ['vegan', 'high-fiber', 'gluten-free', 'dairy-free'] },
  { name: 'Mushroom Stroganoff', emoji: '\u{1F344}', calories: 340, protein: 10, carbs: 38, fats: 16, prepTime: '25 min', category: 'vegan', tags: ['vegan', 'dairy-free'] },
  { name: 'Vegan Pad Thai', emoji: '\u{1F35D}', calories: 400, protein: 14, carbs: 56, fats: 14, prepTime: '20 min', category: 'vegan', tags: ['vegan', 'gluten-free', 'dairy-free'] },
  { name: 'Jackfruit Tacos', emoji: '\u{1F32E}', calories: 280, protein: 8, carbs: 40, fats: 10, prepTime: '20 min', category: 'vegan', tags: ['vegan', 'gluten-free', 'dairy-free'] },
  { name: 'Tempeh Bowl', emoji: '\u{1F331}', calories: 380, protein: 22, carbs: 42, fats: 14, prepTime: '20 min', category: 'vegan', tags: ['vegan', 'high-protein', 'dairy-free', 'gluten-free'] },
  { name: 'Sweet Potato & Black Bean', emoji: '\u{1F360}', calories: 340, protein: 14, carbs: 52, fats: 8, prepTime: '25 min', category: 'vegan', tags: ['vegan', 'high-fiber', 'low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Eggplant Parm (Vegan)', emoji: '\u{1F346}', calories: 300, protein: 10, carbs: 34, fats: 14, prepTime: '30 min', category: 'vegan', tags: ['vegan', 'dairy-free'] },
  { name: 'Coconut Lentil Soup', emoji: '\u{1F963}', calories: 300, protein: 14, carbs: 36, fats: 12, prepTime: '25 min', category: 'vegan', tags: ['vegan', 'high-fiber', 'gluten-free', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Veggie Sushi Rolls', emoji: '\u{1F363}', calories: 260, protein: 8, carbs: 48, fats: 4, prepTime: '25 min', category: 'vegan', tags: ['vegan', 'low-fat', 'dairy-free'] },
  { name: 'Stuffed Peppers', emoji: '\u{1F336}\uFE0F', calories: 280, protein: 12, carbs: 36, fats: 10, prepTime: '30 min', category: 'vegan', tags: ['vegan', 'high-fiber', 'gluten-free', 'dairy-free', 'meal-prep'] },
  { name: 'Zucchini Noodles', emoji: '\u{1F33F}', calories: 200, protein: 10, carbs: 14, fats: 12, prepTime: '15 min', category: 'vegan', tags: ['vegan', 'low-carb', 'gluten-free', 'dairy-free', 'keto', 'quick'] },

  // ════════════════════════════════════════════════════════════════════
  // SNACKS & LIGHT (15)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Mixed Nuts', emoji: '\u{1F95C}', calories: 170, protein: 6, carbs: 6, fats: 15, prepTime: '0 min', category: 'snacks', tags: ['high-protein', 'low-carb', 'vegan', 'gluten-free', 'dairy-free', 'keto', 'quick'] },
  { name: 'Apple & Almond Butter', emoji: '\u{1F34E}', calories: 200, protein: 5, carbs: 22, fats: 12, prepTime: '2 min', category: 'snacks', tags: ['vegan', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Hummus & Veggies', emoji: '\u{1F955}', calories: 150, protein: 6, carbs: 16, fats: 8, prepTime: '5 min', category: 'snacks', tags: ['vegan', 'high-fiber', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Edamame', emoji: '\u{1F96C}', calories: 120, protein: 12, carbs: 8, fats: 5, prepTime: '5 min', category: 'snacks', tags: ['vegan', 'high-protein', 'low-carb', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Dark Chocolate & Berries', emoji: '\u{1F36B}', calories: 180, protein: 3, carbs: 22, fats: 10, prepTime: '2 min', category: 'snacks', tags: ['vegan', 'gluten-free', 'dairy-free', 'anti-inflammatory', 'quick'] },
  { name: 'Protein Balls', emoji: '\u{1F36A}', calories: 200, protein: 12, carbs: 18, fats: 10, prepTime: '10 min', category: 'snacks', tags: ['high-protein', 'meal-prep', 'gluten-free'] },
  { name: 'Trail Mix', emoji: '\u{1F95C}', calories: 220, protein: 6, carbs: 24, fats: 12, prepTime: '0 min', category: 'snacks', tags: ['vegan', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Rice Cakes & Avocado', emoji: '\u{1F951}', calories: 180, protein: 4, carbs: 20, fats: 10, prepTime: '3 min', category: 'snacks', tags: ['vegan', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Cottage Cheese & Fruit', emoji: '\u{1F353}', calories: 160, protein: 16, carbs: 14, fats: 4, prepTime: '3 min', category: 'snacks', tags: ['high-protein', 'low-fat', 'gluten-free', 'quick'] },
  { name: 'Greek Yogurt & Granola', emoji: '\u{1F95B}', calories: 240, protein: 16, carbs: 28, fats: 8, prepTime: '3 min', category: 'snacks', tags: ['high-protein', 'vegetarian', 'quick'] },
  { name: 'Smoothie', emoji: '\u{1F964}', calories: 220, protein: 10, carbs: 36, fats: 4, prepTime: '5 min', category: 'snacks', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Chia Pudding', emoji: '\u{1F95B}', calories: 200, protein: 8, carbs: 22, fats: 10, prepTime: '5 min', category: 'snacks', tags: ['vegan', 'high-fiber', 'gluten-free', 'dairy-free', 'meal-prep', 'quick'] },
  { name: 'Caprese Skewers', emoji: '\u{1F345}', calories: 160, protein: 10, carbs: 6, fats: 12, prepTime: '5 min', category: 'snacks', tags: ['vegetarian', 'low-carb', 'gluten-free', 'quick'] },
  { name: 'Bruschetta', emoji: '\u{1F35E}', calories: 180, protein: 4, carbs: 22, fats: 8, prepTime: '10 min', category: 'snacks', tags: ['vegan', 'dairy-free', 'quick'] },
  { name: 'Date & Nut Bars', emoji: '\u{1F36B}', calories: 190, protein: 4, carbs: 28, fats: 8, prepTime: '5 min', category: 'snacks', tags: ['vegan', 'gluten-free', 'dairy-free', 'meal-prep', 'quick'] },

  // ════════════════════════════════════════════════════════════════════
  // SOUPS (12)
  // ════════════════════════════════════════════════════════════════════
  { name: 'Tom Yum Soup', emoji: '\u{1F35C}', calories: 180, protein: 16, carbs: 12, fats: 8, prepTime: '20 min', category: 'soups', tags: ['low-carb', 'low-fat', 'gluten-free', 'dairy-free', 'anti-inflammatory'] },
  { name: 'Minestrone Soup', emoji: '\u{1F372}', calories: 200, protein: 8, carbs: 30, fats: 6, prepTime: '30 min', category: 'soups', tags: ['vegan', 'high-fiber', 'low-fat', 'dairy-free', 'heart-healthy'] },
  { name: 'Chicken Noodle Soup', emoji: '\u{1F35C}', calories: 240, protein: 20, carbs: 24, fats: 8, prepTime: '25 min', category: 'soups', tags: ['low-fat', 'dairy-free'] },
  { name: 'Lentil Soup', emoji: '\u{1F963}', calories: 260, protein: 16, carbs: 38, fats: 4, prepTime: '25 min', category: 'soups', tags: ['vegan', 'high-fiber', 'low-fat', 'gluten-free', 'dairy-free', 'heart-healthy', 'diabetes-friendly'] },
  { name: 'Miso Soup', emoji: '\u{1F35C}', calories: 80, protein: 6, carbs: 8, fats: 2, prepTime: '10 min', category: 'soups', tags: ['vegan', 'low-fat', 'low-carb', 'dairy-free', 'quick'] },
  { name: 'French Onion Soup', emoji: '\u{1F9C5}', calories: 300, protein: 12, carbs: 28, fats: 16, prepTime: '35 min', category: 'soups', tags: ['vegetarian'] },
  { name: 'Butternut Squash Soup', emoji: '\u{1F383}', calories: 200, protein: 4, carbs: 34, fats: 8, prepTime: '30 min', category: 'soups', tags: ['vegan', 'gluten-free', 'dairy-free', 'low-fat', 'anti-inflammatory'] },
  { name: 'Pho Soup', emoji: '\u{1F35C}', calories: 350, protein: 28, carbs: 40, fats: 6, prepTime: '20 min', category: 'soups', tags: ['low-fat', 'gluten-free', 'dairy-free'] },
  { name: 'Gazpacho Soup', emoji: '\u{1F345}', calories: 120, protein: 3, carbs: 14, fats: 6, prepTime: '15 min', category: 'soups', tags: ['vegan', 'low-fat', 'gluten-free', 'dairy-free', 'quick'] },
  { name: 'Harira', emoji: '\u{1F963}', calories: 260, protein: 16, carbs: 34, fats: 6, prepTime: '30 min', category: 'soups', tags: ['high-fiber', 'low-fat', 'dairy-free', 'gluten-free'] },
  { name: 'Wonton Soup', emoji: '\u{1F35C}', calories: 260, protein: 16, carbs: 28, fats: 8, prepTime: '20 min', category: 'soups', tags: ['low-fat'] },
  { name: 'Black Bean Soup', emoji: '\u{1F963}', calories: 280, protein: 16, carbs: 40, fats: 4, prepTime: '25 min', category: 'soups', tags: ['vegan', 'high-fiber', 'low-fat', 'gluten-free', 'dairy-free', 'heart-healthy'] },
]
