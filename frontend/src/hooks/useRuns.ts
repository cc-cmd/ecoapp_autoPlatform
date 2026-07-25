import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { triggerRun, getBatches, getBatchDetail, cancelBatch, cancelRun } from '@/api/runs';
import type { TriggerRunRequest, RunListParams } from '@/types';

// ---------------------------------------------------------------------------
// Query keys
// ---------------------------------------------------------------------------

export const runKeys = {
  all: ['runs'] as const,
  batchLists: () => [...runKeys.all, 'batch-list'] as const,
  batchList: (params: RunListParams) => [...runKeys.batchLists(), params] as const,
  batchDetails: () => [...runKeys.all, 'batch-detail'] as const,
  batchDetail: (id: string) => [...runKeys.batchDetails(), id] as const,
};

// ---------------------------------------------------------------------------
// Hooks
// ---------------------------------------------------------------------------

/**
 * Fetch paginated list of batches.
 * Polls every 3s while there are active (queued/running) batches.
 * staleTime: 0 ensures fresh data on each poll.
 */
export function useBatches(params: RunListParams) {
  return useQuery({
    queryKey: runKeys.batchList(params),
    queryFn: () => getBatches(params),
    staleTime: 0,
    refetchInterval: (query) => {
      // Stop polling if all batches in the last response are terminal
      const data = query.state.data;
      if (data && data.items.length > 0) {
        const allTerminal = data.items.every((b) => b.status === 'completed');
        if (allTerminal) return false;
      }
      return 3000;
    },
  });
}

/**
 * Fetch detail for a single batch. Polls every 3s while batch is active.
 */
export function useBatchDetail(id: string) {
  return useQuery({
    queryKey: runKeys.batchDetail(id),
    queryFn: () => getBatchDetail(id),
    staleTime: 0,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data && data.batch.status === 'completed') return false;
      return 3000;
    },
    enabled: !!id,
  });
}

/**
 * Trigger a new execution run.
 */
export function useTriggerRun() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: TriggerRunRequest) => triggerRun(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: runKeys.batchLists() });
    },
  });
}

/**
 * Cancel a single test run.
 */
export function useCancelRun() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => cancelRun(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: runKeys.all });
    },
  });
}

/**
 * Cancel an entire batch.
 */
export function useCancelBatch() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => cancelBatch(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: runKeys.all });
    },
  });
}
