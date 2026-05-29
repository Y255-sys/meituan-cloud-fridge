import { clearToken, getToken, setToken } from "lib/utils/storage";
import type {
  AuthPayload,
  CheckoutRedirectData,
  ImportRecognitionData,
  ImportRecognitionPayload,
  InventoryCreatePayload,
  InventoryItem,
  InventoryListData,
  InventorySummary,
  InventoryUpdatePayload,
  MissingAnalysisData,
  OrderSyncData,
  ProductMatchData,
  PurchasePlan,
  RecognitionResult,
  RecipeDetail,
  RecipeRecommendationsData,
  UserProfile,
} from "types/contracts";

import {
  mockProductMatchData,
  mockRecognitionResult,
  mockRecipeDetails,
  mockRecommendations,
} from "./catalog";
import { loadMockState, saveMockState } from "./store";

function wait(ms = 350) {
  return new Promise((resolve) => {
    window.setTimeout(resolve, ms);
  });
}

function getSummary(items: InventoryItem[]): InventorySummary {
  return {
    total_items: items.length,
    expiring_items: items.filter((item) => item.status === "expiring").length,
    expired_items: items.filter((item) => item.status === "expired").length,
  };
}

function requireAuth() {
  if (!getToken()) {
    throw new Error("请先登录");
  }
}

export const mockApi = {
  async login(phone: string, password: string): Promise<AuthPayload> {
    await wait();
    if (phone !== "13800000000" || password !== "12345678") {
      throw new Error("手机号或密码错误");
    }
    const payload: AuthPayload = {
      user: {
        id: "usr_demo",
        phone,
        nickname: "小王",
      },
      token: "mock-token",
    };
    setToken(payload.token);
    return payload;
  },

  async register(phone: string, password: string, nickname: string): Promise<AuthPayload> {
    await wait();
    const payload: AuthPayload = {
      user: {
        id: "usr_registered",
        phone,
        nickname,
      },
      token: `mock-token-${password.length}`,
    };
    setToken(payload.token);
    return payload;
  },

  async logout() {
    await wait(120);
    clearToken();
  },

  async getProfile(): Promise<UserProfile> {
    requireAuth();
    await wait();
    return loadMockState().profile;
  },

  async updateProfile(payload: Partial<UserProfile>): Promise<UserProfile> {
    requireAuth();
    await wait();
    const state = loadMockState();
    state.profile = {
      ...state.profile,
      ...payload,
    };
    saveMockState(state);
    return state.profile;
  },

  async toggleSeniorMode(enabled: boolean): Promise<{ enabled: boolean }> {
    requireAuth();
    await wait();
    const state = loadMockState();
    state.profile.senior_mode_enabled = enabled;
    saveMockState(state);
    return { enabled };
  },

  async recognize(): Promise<RecognitionResult> {
    requireAuth();
    await wait(500);
    return {
      ...mockRecognitionResult,
      recognition_id: `rec_${Date.now()}`,
    };
  },

  async importRecognition(payload: ImportRecognitionPayload): Promise<ImportRecognitionData> {
    requireAuth();
    await wait();
    const state = loadMockState();
    payload.items.forEach((item, index) => {
      state.inventory.unshift({
        id: `ui_import_${Date.now()}_${index}`,
        ingredient_base_id: item.ingredient_base_id ?? null,
        ingredient_name: item.ingredient_name,
        category: "识别食材",
        quantity: item.quantity,
        unit: item.unit,
        storage_location: item.storage_location,
        status: "fresh",
        expire_at: item.expire_at ?? null,
        days_to_expire: item.expire_at ? 3 : null,
        source_type: "recognition",
        source_ref_id: payload.recognition_id,
        updated_at: new Date().toISOString(),
      });
    });
    saveMockState(state);
    return {
      imported_count: payload.items.length,
      summary: getSummary(state.inventory),
    };
  },

  async getInventory(filters?: { keyword?: string; status?: string; category?: string }): Promise<InventoryListData> {
    requireAuth();
    await wait();
    const state = loadMockState();
    let items = [...state.inventory];
    if (filters?.keyword) {
      items = items.filter((item) => item.ingredient_name.includes(filters.keyword ?? ""));
    }
    if (filters?.status) {
      items = items.filter((item) => item.status === filters.status);
    }
    if (filters?.category) {
      items = items.filter((item) => item.category === filters.category);
    }
    return {
      summary: getSummary(items),
      items,
    };
  },

  async createInventory(payload: InventoryCreatePayload): Promise<InventoryItem> {
    requireAuth();
    await wait();
    const state = loadMockState();
    const item: InventoryItem = {
      id: `ui_${Date.now()}`,
      ingredient_base_id: payload.ingredient_base_id ?? null,
      ingredient_name: payload.ingredient_name,
      category: payload.category ?? "手动录入",
      quantity: payload.quantity,
      unit: payload.unit,
      storage_location: payload.storage_location,
      status: "fresh",
      expire_at: payload.expire_at ?? null,
      days_to_expire: payload.expire_at ? 4 : null,
      source_type: "manual",
      source_ref_id: null,
      updated_at: new Date().toISOString(),
    };
    state.inventory.unshift(item);
    saveMockState(state);
    return item;
  },

  async updateInventory(itemId: string, payload: InventoryUpdatePayload): Promise<InventoryItem> {
    requireAuth();
    await wait();
    const state = loadMockState();
    const target = state.inventory.find((item) => item.id === itemId);
    if (!target) {
      throw new Error("库存项不存在");
    }
    Object.assign(target, payload, { updated_at: new Date().toISOString() });
    saveMockState(state);
    return target;
  },

  async deleteInventory(itemId: string): Promise<{ deleted: boolean }> {
    requireAuth();
    await wait();
    const state = loadMockState();
    state.inventory = state.inventory.filter((item) => item.id !== itemId);
    saveMockState(state);
    return { deleted: true };
  },

  async getRecommendations(): Promise<RecipeRecommendationsData> {
    requireAuth();
    await wait();
    const state = loadMockState();
    return {
      ...mockRecommendations,
      context: {
        ...mockRecommendations.context,
        inventory_count: state.inventory.length,
      },
    };
  },

  async getRecipeDetail(recipeId: string): Promise<RecipeDetail> {
    requireAuth();
    await wait();
    const recipe = mockRecipeDetails[recipeId];
    if (!recipe) {
      throw new Error("菜谱不存在");
    }
    return recipe;
  },

  async getMissingAnalysis(recipeIds: string[]): Promise<MissingAnalysisData> {
    requireAuth();
    await wait();
    if (recipeIds.includes("rcp_beef_pepper")) {
      return {
        recipes: [
          {
            recipe_id: "rcp_beef_pepper",
            recipe_name: "青椒牛肉",
            missing_ingredients: [
              {
                ingredient_base_id: "ing_beef",
                ingredient_name: "牛肉",
                missing_quantity: 250,
                unit: "g",
              },
            ],
          },
        ],
        aggregated_missing: [
          {
            ingredient_base_id: "ing_beef",
            ingredient_name: "牛肉",
            missing_quantity: 250,
            unit: "g",
          },
        ],
      };
    }
    return {
      recipes: [],
      aggregated_missing: [],
    };
  },

  async createPurchasePlan(recipeIds: string[], strategy: "lowest_cost" | "minimum_items"): Promise<PurchasePlan> {
    requireAuth();
    await wait();
    return {
      plan_id: `plan_${Date.now()}`,
      strategy,
      recipes: [
        {
          recipe_id: recipeIds[0] ?? "rcp_beef_pepper",
          recipe_name: "青椒牛肉",
        },
      ],
      items: [
        {
          ingredient_base_id: "ing_beef",
          ingredient_name: "牛肉",
          required_quantity: 250,
          unit: "g",
          estimated_price: 21.9,
          reason: "核心主料缺失",
        },
      ],
      promotion_explanation:
        strategy === "lowest_cost" ? "当前方案优先选择刚好够用的小规格，减少浪费" : "当前方案优先减少件数，方便一键下单",
      estimated_total_price: 21.9,
    };
  },

  async matchProducts(planId: string): Promise<ProductMatchData> {
    requireAuth();
    await wait();
    return {
      ...mockProductMatchData,
      plan_id: planId,
    };
  },

  async checkoutRedirect(): Promise<CheckoutRedirectData> {
    requireAuth();
    await wait();
    return {
      checkout_url: "https://mock.meituan.com/checkout/demo",
      delegate_pay: {
        enabled: true,
        share_message: "妈，今晚做饭差一份牛肉，我已经帮你选好了，点这里让孩子代付。",
      },
    };
  },

  async syncOrder(): Promise<OrderSyncData> {
    requireAuth();
    await wait();
    return {
      synced: true,
      order_id: `ord_${Date.now()}`,
      imported_items: 3,
    };
  },
};
