import { runtimeConfig } from "lib/config/runtime";
import { getToken } from "lib/utils/storage";
import type { ApiResponse } from "types/contracts";

async function parseResponse<T>(response: Response): Promise<T> {
  const payload = (await response.json()) as ApiResponse<T>;
  if (!response.ok || payload.code !== 0) {
    throw new Error(payload.message || "请求失败");
  }
  return payload.data;
}

export async function apiGet<T>(path: string) {
  const token = getToken();
  const response = await fetch(`${runtimeConfig.apiBaseUrl}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
  });
  return parseResponse<T>(response);
}

export async function apiPost<T>(path: string, body?: unknown) {
  const token = getToken();
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  const response = await fetch(`${runtimeConfig.apiBaseUrl}${path}`, {
    method: "POST",
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });
  return parseResponse<T>(response);
}

export async function apiPatch<T>(path: string, body: unknown) {
  const token = getToken();
  const response = await fetch(`${runtimeConfig.apiBaseUrl}${path}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });
  return parseResponse<T>(response);
}

export async function apiDelete<T>(path: string) {
  const token = getToken();
  const response = await fetch(`${runtimeConfig.apiBaseUrl}${path}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return parseResponse<T>(response);
}

export async function apiFormPost<T>(path: string, formData: FormData) {
  const token = getToken();
  const response = await fetch(`${runtimeConfig.apiBaseUrl}${path}`, {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : undefined,
    body: formData,
  });
  return parseResponse<T>(response);
}
