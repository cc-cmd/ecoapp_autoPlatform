import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getDevices, discoverDevices } from '@/api/devices';

// ---------------------------------------------------------------------------
// Query keys
// ---------------------------------------------------------------------------

export const deviceKeys = {
  all: ['devices'] as const,
};

// ---------------------------------------------------------------------------
// Hooks
// ---------------------------------------------------------------------------

/**
 * Fetch device list with 5-second polling for real-time status updates.
 */
export function useDevices() {
  return useQuery({
    queryKey: deviceKeys.all,
    queryFn: getDevices,
    refetchInterval: 5000,
    staleTime: 0,
  });
}

/**
 * Trigger device discovery via ADB/iOS tools.
 * Invalidates device list on success.
 */
export function useDiscoverDevices() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: discoverDevices,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: deviceKeys.all });
    },
  });
}
