import { apiDelete, apiGet, apiPatch, apiPost } from "lib/api/client";
import { runtimeConfig } from "lib/config/runtime";
import { mockApi } from "lib/mock/api";
import type {
  ImportRecognitionData,
  ImportRecognitionPayload,
  InventoryCreatePayload,
  InventoryItem,
  InventoryListData,
  InventoryUpdatePayload,
} from "types/contracts";

export async function getInventory(filters: { keyword?: string; status?: string; category?: string }) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.getInventory(filters);
  }
  const searchParams = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) {
      searchParams.set(key, value);
    }
  });
  const query = searchParams.toString();
  return apiGet<InventoryListData>(`/inventory${query ? `?${query}` : ""}`);
}

export async function createInventory(payload: InventoryCreatePayload) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.createInventory(payload);
  }
  return apiPost<InventoryItem>("/inventory", payload);
}

export async function updateInventory(itemId: string, payload: InventoryUpdatePayload) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.updateInventory(itemId, payload);
  }
  return apiPatch<InventoryItem>(`/inventory/${itemId}`, payload);
}

export async function deleteInventory(itemId: string) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.deleteInventory(itemId);
  }
  return apiDelete<{ deleted: boolean }>(`/inventory/${itemId}`);
}

export async function importRecognition(payload: ImportRecognitionPayload) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.importRecognition(payload);
  }
  return apiPost<ImportRecognitionData>("/inventory/import-recognition", payload);
}
