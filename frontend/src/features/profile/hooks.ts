import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { queryKeys } from "lib/api/queryKeys";
import { getProfile, toggleSeniorMode, updateProfile } from "services/profileApi";

export function useProfileQuery() {
  return useQuery({
    queryKey: queryKeys.profile,
    queryFn: getProfile,
  });
}

export function useUpdateProfileMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: updateProfile,
    onSuccess: (data) => {
      queryClient.setQueryData(queryKeys.profile, data);
    },
  });
}

export function useToggleSeniorModeMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: toggleSeniorMode,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.profile });
    },
  });
}
