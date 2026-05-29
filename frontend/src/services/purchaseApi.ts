import { apiPost } from "lib/api/client";
import { runtimeConfig } from "lib/config/runtime";
import { mockApi } from "lib/mock/api";
import type { CheckoutRedirectData, ProductMatchData, PurchasePlan } from "types/contracts";

export async function createPurchasePlan(recipeIds: string[], strategy: "lowest_cost" | "minimum_items") {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.createPurchasePlan(recipeIds, strategy);
  }
  return apiPost<PurchasePlan>("/purchase-plans", {
    recipe_ids: recipeIds,
    strategy,
  });
}

export async function matchProducts(planId: string) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.matchProducts(planId);
  }
  return apiPost<ProductMatchData>("/products/match", {
    plan_id: planId,
  });
}

export async function checkoutRedirect(selectedProductIds: string[], seniorModeDelegatePay: boolean) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.checkoutRedirect();
  }
  return apiPost<CheckoutRedirectData>("/checkout/redirect", {
    source_type: "grocery",
    selected_product_ids: selectedProductIds,
    senior_mode_delegate_pay: seniorModeDelegatePay,
  });
}
