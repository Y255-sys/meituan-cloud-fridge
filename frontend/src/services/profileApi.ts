import { apiGet, apiPatch } from "lib/api/client";
import { runtimeConfig } from "lib/config/runtime";
import { mockApi } from "lib/mock/api";
import type { UserProfile } from "types/contracts";

export async function getProfile() {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.getProfile();
  }
  return apiGet<UserProfile>("/profile");
}

export async function updateProfile(payload: Partial<UserProfile>) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.updateProfile(payload);
  }
  return apiPatch<UserProfile>("/profile", payload);
}

export async function toggleSeniorMode(enabled: boolean) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.toggleSeniorMode(enabled);
  }
  return apiPatch<{ enabled: boolean }>("/profile/senior-mode", { enabled });
}
