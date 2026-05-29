import { apiFormPost } from "lib/api/client";
import { runtimeConfig } from "lib/config/runtime";
import { mockApi } from "lib/mock/api";
import type { RecognitionResult } from "types/contracts";

export async function recognizeIngredients(input: { file: File; scene: string }) {
  if (runtimeConfig.apiMode === "mock") {
    return mockApi.recognize();
  }
  const formData = new FormData();
  formData.append("image", input.file);
  formData.append("scene", input.scene);
  return apiFormPost<RecognitionResult>("/recognitions", formData);
}
