import { apiPost } from "lib/api/client";
import { runtimeConfig } from "lib/config/runtime";
import { mockApi } from "lib/mock/api";
import type { AuthPayload } from "types/contracts";

export async function login(input: { phone: string; password: string }) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.login(input.phone, input.password);
  }
  return apiPost<AuthPayload>("/auth/login", input);
}

export async function register(input: { phone: string; password: string; nickname: string }) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.register(input.phone, input.password, input.nickname);
  }
  return apiPost<AuthPayload>("/auth/register", input);
}
