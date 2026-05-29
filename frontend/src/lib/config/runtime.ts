import type { AppRuntimeConfig, ApiMode } from "types/contracts";

const apiMode = (import.meta.env.VITE_API_MODE ?? "real") as ApiMode;

export const runtimeConfig: AppRuntimeConfig = {
  apiMode,
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1",
};

