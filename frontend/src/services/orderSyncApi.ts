import { apiPost } from "lib/api/client";
import { runtimeConfig } from "lib/config/runtime";
import { mockApi } from "lib/mock/api";
import type { OrderSyncData } from "types/contracts";

export async function syncOrder() {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.syncOrder();
  }
  return apiPost<OrderSyncData>("/order-sync", {
    channel: "meituan_grocery",
    external_order_id: "mt_20260522001",
  });
}
