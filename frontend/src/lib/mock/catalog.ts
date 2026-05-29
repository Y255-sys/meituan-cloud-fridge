import type {
  InventoryItem,
  ProductMatchData,
  RecipeDetail,
  RecipeRecommendationsData,
  RecognitionResult,
  UserProfile,
} from "types/contracts";

const today = new Date();

function addDays(days: number) {
  const next = new Date(today);
  next.setDate(next.getDate() + days);
  return next.toISOString();
}

export const mockProfile: UserProfile = {
  user_id: "usr_demo",
  nickname: "小王",
  phone: "13800000000",
  household_name: "小王家",
  senior_mode_enabled: false,
  dietary_preferences: ["light"],
  allergy_tags: [],
  taste_tags: ["home_style"],
  city_code: "310100",
};

export const mockInventory: InventoryItem[] = [
  {
    id: "ui_tomato",
    ingredient_base_id: "ing_tomato",
    ingredient_name: "番茄",
    category: "蔬菜",
    quantity: 4,
    unit: "个",
    storage_location: "冷藏",
    status: "fresh",
    expire_at: addDays(3),
    days_to_expire: 3,
    source_type: "manual",
    source_ref_id: null,
    updated_at: new Date().toISOString(),
  },
  {
    id: "ui_egg",
    ingredient_base_id: "ing_egg",
    ingredient_name: "鸡蛋",
    category: "蛋奶",
    quantity: 6,
    unit: "个",
    storage_location: "冷藏",
    status: "fresh",
    expire_at: addDays(8),
    days_to_expire: 8,
    source_type: "manual",
    source_ref_id: null,
    updated_at: new Date().toISOString(),
  },
  {
    id: "ui_cucumber",
    ingredient_base_id: "ing_cucumber",
    ingredient_name: "黄瓜",
    category: "蔬菜",
    quantity: 1,
    unit: "根",
    storage_location: "冷藏",
    status: "expiring",
    expire_at: addDays(1),
    days_to_expire: 1,
    source_type: "manual",
    source_ref_id: null,
    updated_at: new Date().toISOString(),
  },
  {
    id: "ui_potato",
    ingredient_base_id: "ing_potato",
    ingredient_name: "土豆",
    category: "蔬菜",
    quantity: 2,
    unit: "个",
    storage_location: "常温",
    status: "fresh",
    expire_at: addDays(5),
    days_to_expire: 5,
    source_type: "manual",
    source_ref_id: null,
    updated_at: new Date().toISOString(),
  },
  {
    id: "ui_green_pepper",
    ingredient_base_id: "ing_green_pepper",
    ingredient_name: "青椒",
    category: "蔬菜",
    quantity: 2,
    unit: "个",
    storage_location: "冷藏",
    status: "expiring",
    expire_at: addDays(2),
    days_to_expire: 2,
    source_type: "manual",
    source_ref_id: null,
    updated_at: new Date().toISOString(),
  },
];

export const mockRecognitionResult: RecognitionResult = {
  recognition_id: "rec_mock_001",
  image_url: "/mock/recognition.jpg",
  items: [
    {
      temp_id: "tmp_1",
      ingredient_base_id: "ing_tomato",
      ingredient_name: "番茄",
      quantity: 4,
      unit: "个",
      confidence: 0.97,
      source: "vision_mock",
      editable: true,
      suggested_storage_location: "冷藏",
      suggested_expire_days: 4,
    },
    {
      temp_id: "tmp_2",
      ingredient_base_id: "ing_egg",
      ingredient_name: "鸡蛋",
      quantity: 6,
      unit: "个",
      confidence: 0.95,
      source: "vision_mock",
      editable: true,
      suggested_storage_location: "冷藏",
      suggested_expire_days: 10,
    },
  ],
};

export const mockRecommendations: RecipeRecommendationsData = {
  context: {
    meal_type: "dinner",
    scene: "worker_evening",
    inventory_count: 5,
  },
  groups: [
    {
      type: "cook_now",
      title: "不补购也能做",
      description: "优先消耗现有库存",
      recipes: [
        {
          recipe_id: "rcp_tomato_egg",
          recipe_name: "番茄炒蛋",
          cover_image: "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=800&q=80",
          cook_time_minutes: 12,
          match_score: 96,
          missing_count: 0,
          highlight_reason: "家里现有番茄和鸡蛋，可直接开做",
        },
        {
          recipe_id: "rcp_potato_egg",
          recipe_name: "土豆鸡蛋饼",
          cover_image: "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=80",
          cook_time_minutes: 15,
          match_score: 88,
          missing_count: 0,
          highlight_reason: "省事省钱，适合工作日晚餐",
        },
      ],
    },
    {
      type: "buy_little",
      title: "少量补购就能做",
      description: "差 1 到 2 样核心食材就能完成",
      recipes: [
        {
          recipe_id: "rcp_beef_pepper",
          recipe_name: "青椒牛肉",
          cover_image: "https://images.unsplash.com/photo-1514516345957-556ca7c90a29?auto=format&fit=crop&w=800&q=80",
          cook_time_minutes: 20,
          match_score: 72,
          missing_count: 1,
          highlight_reason: "只差一份牛肉，补购成本低",
        },
      ],
    },
    {
      type: "takeout",
      title: "不想做饭，直接外卖替代",
      description: "给今晚一个省事的备选方案",
      recipes: [
        {
          recipe_id: "takeout_beef",
          recipe_name: "青椒牛肉盖饭",
          cover_image: "https://images.unsplash.com/photo-1512058564366-18510be2db19?auto=format&fit=crop&w=800&q=80",
          cook_time_minutes: 32,
          match_score: 83,
          missing_count: 1,
          highlight_reason: "如果今晚不做饭，可直接替代",
        },
      ],
    },
  ],
};

export const mockRecipeDetails: Record<string, RecipeDetail> = {
  rcp_tomato_egg: {
    recipe_id: "rcp_tomato_egg",
    recipe_name: "番茄炒蛋",
    description: "12 分钟快手菜，适合工作日晚餐",
    cook_time_minutes: 12,
    difficulty: "easy",
    servings: 2,
    steps: ["番茄切块", "鸡蛋打散", "热锅翻炒", "调味出锅"],
    ingredients: [
      {
        ingredient_base_id: "ing_tomato",
        ingredient_name: "番茄",
        required_quantity: 2,
        unit: "个",
        owned_quantity: 4,
        missing_quantity: 0,
      },
      {
        ingredient_base_id: "ing_egg",
        ingredient_name: "鸡蛋",
        required_quantity: 3,
        unit: "个",
        owned_quantity: 6,
        missing_quantity: 0,
      },
    ],
    nutrition_tip: "酸甜下饭，适合工作日晚餐",
    can_cook_now: true,
  },
  rcp_beef_pepper: {
    recipe_id: "rcp_beef_pepper",
    recipe_name: "青椒牛肉",
    description: "差一点主料就能做，适合少量补购",
    cook_time_minutes: 20,
    difficulty: "medium",
    servings: 2,
    steps: ["牛肉切片腌制", "青椒切丝", "大火快炒", "调味出锅"],
    ingredients: [
      {
        ingredient_base_id: "ing_beef",
        ingredient_name: "牛肉",
        required_quantity: 250,
        unit: "g",
        owned_quantity: 0,
        missing_quantity: 250,
      },
      {
        ingredient_base_id: "ing_green_pepper",
        ingredient_name: "青椒",
        required_quantity: 2,
        unit: "个",
        owned_quantity: 2,
        missing_quantity: 0,
      },
    ],
    nutrition_tip: "补点牛肉就能完成高满足感晚饭",
    can_cook_now: false,
  },
};

export const mockProductMatchData: ProductMatchData = {
  plan_id: "plan_mock_001",
  products: [
    {
      ingredient_base_id: "ing_beef",
      ingredient_name: "牛肉",
      matched_product_id: "prd_beef_300g",
      product_name: "鲜切牛里脊 300g",
      price: 21.9,
      original_price: 25.9,
      discount_text: "限时直降 4 元",
      merchant_name: "美团买菜自营",
      eta_minutes: 29,
    },
  ],
  takeout_alternatives: [
    {
      merchant_id: "mt_rest_01",
      merchant_name: "下饭小馆",
      dish_name: "青椒牛肉盖饭",
      price: 26.8,
      eta_minutes: 32,
      reason: "如果今晚不做饭，可直接替代",
    },
  ],
};
