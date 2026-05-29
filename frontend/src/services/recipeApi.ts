import { apiGet, apiPost } from "lib/api/client";
import { runtimeConfig } from "lib/config/runtime";
import { mockApi } from "lib/mock/api";
import type { MissingAnalysisData, RecipeDetail, RecipeRecommendationsData } from "types/contracts";

export async function getRecommendations(scene: string) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.getRecommendations();
  }
  return apiGet<RecipeRecommendationsData>(`/recipes/recommendations?meal_type=dinner&servings=2&scene=${scene}`);
}

export async function getRecipeDetail(recipeId: string) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.getRecipeDetail(recipeId);
  }
  return apiGet<RecipeDetail>(`/recipes/${recipeId}`);
}

export async function getMissingAnalysis(recipeIds: string[]) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.getMissingAnalysis(recipeIds);
  }
  return apiPost<MissingAnalysisData>("/recipes/missing-analysis", {
    recipe_ids: recipeIds,
    servings: 2,
  });
}
