import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getCases, getCase, createCase, updateCase, deleteCase, uploadScript, getExecutionHistory } from '@/api/cases';
import type { TestCaseListParams, CreateCaseRequest, UpdateCaseRequest, PaginatedResponse, TestRun } from '@/types';

// ---------------------------------------------------------------------------
// Query keys factory
// ---------------------------------------------------------------------------

export const caseKeys = {
  all: ['cases'] as const,
  lists: () => [...caseKeys.all, 'list'] as const,
  list: (params: TestCaseListParams) => [...caseKeys.lists(), params] as const,
  details: () => [...caseKeys.all, 'detail'] as const,
  detail: (id: string) => [...caseKeys.details(), id] as const,
};

// ---------------------------------------------------------------------------
// Hooks
// ---------------------------------------------------------------------------

/**
 * Fetch paginated list of test cases. staleTime: 30s.
 */
export function useCases(params: TestCaseListParams) {
  return useQuery({
    queryKey: caseKeys.list(params),
    queryFn: () => getCases(params),
    staleTime: 30_000,
  });
}

/**
 * Fetch a single test case by ID. staleTime: 0 (instant-refetch after edit).
 */
export function useCase(id: string) {
  return useQuery({
    queryKey: caseKeys.detail(id),
    queryFn: () => getCase(id),
    staleTime: 0,
    enabled: !!id,
  });
}

/**
 * Create a new test case. Invalidates case lists on success.
 */
export function useCreateCase() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateCaseRequest) => createCase(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: caseKeys.lists() });
    },
  });
}

/**
 * Update an existing test case. Invalidates detail and list queries.
 */
export function useUpdateCase() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateCaseRequest }) => updateCase(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: caseKeys.all });
    },
  });
}

/**
 * Delete a test case. Invalidates case lists on success.
 */
export function useDeleteCase() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteCase(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: caseKeys.lists() });
    },
  });
}

/**
 * Fetch execution history for a test case. staleTime: 30s.
 */
export function useCaseRuns(caseId: string, params?: { page?: number; size?: number }): { data: PaginatedResponse<TestRun> | undefined; isLoading: boolean } {
  return useQuery({
    queryKey: ['case-runs', caseId, params],
    queryFn: () => getExecutionHistory(caseId, params),
    enabled: !!caseId,
    staleTime: 30_000,
  });
}

/**
 * Upload a Python script for a test case.
 */
export function useUploadScript() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, file }: { id: string; file: File }) => uploadScript(id, file),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: caseKeys.detail(variables.id) });
    },
  });
}
