import apiClient from './client';
import type { PaginatedResponse, RunGroup, TestRun, TriggerRunRequest, RunListParams } from '@/types';

/**
 * Trigger a new execution run with selected test cases.
 */
export async function triggerRun(data: TriggerRunRequest): Promise<RunGroup> {
  const response = await apiClient.post<RunGroup>('/runs', data);
  return response.data;
}

/**
 * Get paginated list of run batches.
 */
export async function getBatches(params?: RunListParams): Promise<PaginatedResponse<RunGroup>> {
  const response = await apiClient.get<PaginatedResponse<RunGroup>>('/runs/batches', { params });
  return response.data;
}

/**
 * Get detail of a specific batch including all test runs.
 */
export async function getBatchDetail(id: string): Promise<{ batch: RunGroup; runs: TestRun[] }> {
  const response = await apiClient.get<{ batch: RunGroup; runs: TestRun[] }>(`/runs/batches/${id}`);
  return response.data;
}

/**
 * Cancel a running batch.
 */
export async function cancelBatch(id: string): Promise<void> {
  await apiClient.post(`/runs/batches/${id}/cancel`);
}

/**
 * Cancel a single test run.
 */
export async function cancelRun(id: string): Promise<void> {
  await apiClient.post(`/runs/${id}/cancel`);
}
