import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { queryKeys } from "lib/api/queryKeys";
import { createInventory, deleteInventory, getInventory, importRecognition, updateInventory } from "services/inventoryApi";

export function useInventoryQuery(filters: { keyword?: string; status?: string; category?: string }) {
  return useQuery({
    queryKey: queryKeys.inventory(filters),
    queryFn: () => getInventory(filters),
  });
}

export function useCreateInventoryMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: createInventory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
    },
  });
}

export function useUpdateInventoryMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ itemId, payload }: { itemId: string; payload: Parameters<typeof updateInventory>[1] }) =>
      updateInventory(itemId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
    },
  });
}

export function useDeleteInventoryMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: deleteInventory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
    },
  });
}

export function useImportRecognitionMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: importRecognition,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["inventory"] });
    },
  });
}
