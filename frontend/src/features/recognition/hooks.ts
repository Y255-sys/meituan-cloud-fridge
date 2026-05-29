import { useMutation } from "@tanstack/react-query";

import { recognizeIngredients } from "services/recognitionApi";

export function useRecognitionMutation() {
  return useMutation({
    mutationFn: recognizeIngredients,
  });
}
