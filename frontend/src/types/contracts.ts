export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  request_id: string;
}

export interface User {
  id: string;
  phone: string;
  nickname: string;
}

export interface AuthPayload {
  user: User;
  token: string;
}

export interface UserProfile {
  user_id: string;
  nickname: string;
  phone: string;
  household_name: string;
  senior_mode_enabled: boolean;
  dietary_preferences: string[];
  allergy_tags: string[];
  taste_tags: string[];
  city_code: string;
}

export interface RecognitionItem {
  temp_id: string;
  ingredient_base_id: string | null;
  ingredient_name: string;
  quantity: number;
  unit: string;
  confidence: number;
  source: "vision_mock" | "vision_real";
  editable: boolean;
  suggested_storage_location: "冷藏" | "冷冻" | "常温";
  suggested_expire_days: number;
}

export interface RecognitionResult {
  recognition_id: string;
  image_url: string;
  items: RecognitionItem[];
}

export type InventoryStatus = "fresh" | "expiring" | "expired";

export interface InventorySummary {
  total_items: number;
  expiring_items: number;
  expired_items: number;
}

export interface InventoryItem {
  id: string;
  ingredient_base_id: string | null;
  ingredient_name: string;
  category: string;
  quantity: number;
  unit: string;
  storage_location: "冷藏" | "冷冻" | "常温";
  status: InventoryStatus;
  expire_at: string | null;
  days_to_expire: number | null;
  source_type: "manual" | "recognition" | "order_sync";
  source_ref_id: string | null;
  updated_at: string;
}

export interface InventoryListData {
  summary: InventorySummary;
  items: InventoryItem[];
}

export interface InventoryCreatePayload {
  ingredient_base_id?: string | null;
  ingredient_name: string;
  category?: string | null;
  quantity: number;
  unit: string;
  storage_location: "冷藏" | "冷冻" | "常温";
  expire_at?: string | null;
  notes?: string | null;
}

export interface InventoryUpdatePayload {
  ingredient_name?: string;
  category?: string | null;
  quantity?: number;
  unit?: string;
  storage_location?: "冷藏" | "冷冻" | "常温";
  expire_at?: string | null;
  notes?: string | null;
}

export interface ImportRecognitionPayload {
  recognition_id: string;
  items: Array<{
    ingredient_base_id?: string | null;
    ingredient_name: string;
    quantity: number;
    unit: string;
    storage_location: "冷藏" | "冷冻" | "常温";
    expire_at?: string | null;
  }>;
}

export interface ImportRecognitionData {
  imported_count: number;
  summary: InventorySummary;
}

export type RecommendationGroupType = "cook_now" | "buy_little" | "takeout";

export interface RecipeCard {
  recipe_id: string;
  recipe_name: string;
  cover_image: string;
  cook_time_minutes: number;
  match_score: number;
  missing_count: number;
  highlight_reason: string;
}

export interface RecommendationGroup {
  type: RecommendationGroupType;
  title: string;
  description: string;
  recipes: RecipeCard[];
}

export interface RecipeRecommendationsData {
  context: {
    meal_type: string;
    scene: string;
    inventory_count: number;
  };
  groups: RecommendationGroup[];
}

export interface RecipeIngredientUsage {
  ingredient_base_id: string | null;
  ingredient_name: string;
  required_quantity: number;
  unit: string;
  owned_quantity: number;
  missing_quantity: number;
}

export interface RecipeDetail {
  recipe_id: string;
  recipe_name: string;
  description: string;
  cook_time_minutes: number;
  difficulty: string;
  servings: number;
  steps: string[];
  ingredients: RecipeIngredientUsage[];
  nutrition_tip: string;
  can_cook_now: boolean;
}

export interface MissingIngredient {
  ingredient_base_id: string | null;
  ingredient_name: string;
  missing_quantity: number;
  unit: string;
}

export interface MissingAnalysisData {
  recipes: Array<{
    recipe_id: string;
    recipe_name: string;
    missing_ingredients: MissingIngredient[];
  }>;
  aggregated_missing: MissingIngredient[];
}

export interface PurchasePlan {
  plan_id: string;
  strategy: "lowest_cost" | "minimum_items";
  recipes: Array<{
    recipe_id: string;
    recipe_name: string;
  }>;
  items: Array<{
    ingredient_base_id: string | null;
    ingredient_name: string;
    required_quantity: number;
    unit: string;
    estimated_price: number;
    reason: string;
  }>;
  promotion_explanation: string;
  estimated_total_price: number;
}

export interface ProductMatchData {
  plan_id: string;
  products: Array<{
    ingredient_base_id: string | null;
    ingredient_name: string;
    matched_product_id: string;
    product_name: string;
    price: number;
    original_price: number;
    discount_text: string;
    merchant_name: string;
    eta_minutes: number;
  }>;
  takeout_alternatives: Array<{
    merchant_id: string;
    merchant_name: string;
    dish_name: string;
    price: number;
    eta_minutes: number;
    reason: string;
  }>;
}

export interface CheckoutRedirectData {
  checkout_url: string;
  delegate_pay: {
    enabled: boolean;
    share_message: string;
  };
}

export interface OrderSyncData {
  synced: boolean;
  order_id: string;
  imported_items: number;
}

export type ApiMode = "mock" | "real";

export interface AppRuntimeConfig {
  apiBaseUrl: string;
  apiMode: ApiMode;
}
