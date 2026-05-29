import { useMutation } from "@tanstack/react-query";

import { checkoutRedirect, createPurchasePlan, matchProducts } from "services/purchaseApi";

export function usePurchasePlanMutation() {
  return useMutation({
    mutationFn: ({ recipeIds, strategy }: { recipeIds: string[]; strategy: "lowest_cost" | "minimum_items" }) =>
      createPurchasePlan(recipeIds, strategy),
  });
}

export function useProductMatchMutation() {
  return useMutation({
    mutationFn: matchProducts,
  });
}

export function useCheckoutRedirectMutation() {
  return useMutation({
    mutationFn: ({ selectedProductIds, seniorModeDelegatePay }: { selectedProductIds: string[]; seniorModeDelegatePay: boolean }) =>
      checkoutRedirect(selectedProductIds, seniorModeDelegatePay),
  });
}
