import { useMutation, useQuery } from "@tanstack/react-query";

import { queryKeys } from "lib/api/queryKeys";
import { getMissingAnalysis, getRecipeDetail, getRecommendations } from "services/recipeApi";

export function useRecommendationsQuery(scene: string) {
  return useQuery({
    queryKey: queryKeys.recommendations({ scene }),
    queryFn: () => getRecommendations(scene),
  });
}

export function useRecipeDetailQuery(recipeId: string | null) {
  return useQuery({
    queryKey: queryKeys.recipeDetail(recipeId),
    queryFn: () => getRecipeDetail(recipeId as string),
    enabled: Boolean(recipeId),
  });
}

export function useMissingAnalysisMutation() {
  return useMutation({
    mutationFn: getMissingAnalysis,
  });
}
