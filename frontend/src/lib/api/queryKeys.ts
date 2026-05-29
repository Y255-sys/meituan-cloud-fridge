export const queryKeys = {
  profile: ["profile"] as const,
  inventory: (params: unknown) => ["inventory", params] as const,
  recommendations: (params: unknown) => ["recommendations", params] as const,
  recipeDetail: (recipeId: string | null) => ["recipe-detail", recipeId] as const,
};

